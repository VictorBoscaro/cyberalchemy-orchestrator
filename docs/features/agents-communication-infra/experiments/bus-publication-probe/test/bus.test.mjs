import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { BusError, PublicationBus, verifyReceipt } from "../src/bus.mjs";

const context = {
  run_id: "run-probe-1",
  dispatch_id: "dispatch-probe-1",
  group_id: "group-probe-1",
  group_version: 1,
  seat_id: "seat-a",
  agent_instance_id: "agent-a-1",
  attempt_id: "attempt-a-1",
  actor_principal_id: "principal-seat-a",
  phase: "collect",
};

const valid = {
  idempotency_key: "position:seat-a:round-1",
  operation_id: "operation-a-1",
  round_id: "round-1",
  message_type: "position",
  payload: { claim: "The bus accepted this contribution.", confidence: 0.8 },
};

async function fixture(overrides = {}) {
  const dir = await mkdtemp(path.join(os.tmpdir(), "agent-bus-probe-"));
  const journalPath = path.join(dir, "journal.jsonl");
  const phaseStatePath = path.join(dir, "phase-state.json");
  await writeFile(phaseStatePath, JSON.stringify({ closed_phases: [] }));
  let id = 0;
  const bus = new PublicationBus({
    journalPath,
    phaseStatePath,
    context,
    now: () => new Date("2026-07-21T12:00:00.000Z"),
    uuid: () => `00000000-0000-4000-8000-${String(++id).padStart(12, "0")}`,
    ...overrides,
  });
  return { bus, journalPath, phaseStatePath };
}

async function rejectsCode(promise, code) {
  await assert.rejects(promise, (error) => error instanceof BusError && error.code === code);
}

test("normal publication is persisted before a receipt is returned", async () => {
  const { bus, journalPath } = await fixture();
  const receipt = await bus.publish(valid);
  assert.equal(receipt.status, "accepted");
  assert.equal(receipt.journal_offset, 1);
  const event = await verifyReceipt({ journalPath, receipt });
  assert.deepEqual(event.payload, valid.payload);
  assert.equal(event.seat_id, context.seat_id);
});

test("parent gate rejects a subagent result without a receipt", async () => {
  const { journalPath } = await fixture();
  await rejectsCode(verifyReceipt({ journalPath, receipt: undefined }), "missing_receipt");
});

test("invalid payload is rejected and not appended", async () => {
  const { bus, journalPath } = await fixture();
  await rejectsCode(bus.publish({ ...valid, payload: undefined }), "invalid_payload");
  await assert.rejects(readFile(journalPath, "utf8"), { code: "ENOENT" });
});

test("identical retry returns the stable receipt without a duplicate event", async () => {
  const { bus, journalPath } = await fixture();
  const first = await bus.publish(valid);
  const second = await bus.publish({ ...valid, payload: { confidence: 0.8, claim: valid.payload.claim } });
  assert.equal(second.replayed, true);
  assert.equal(second.event_id, first.event_id);
  assert.equal((await readFile(journalPath, "utf8")).trim().split(/\r?\n/).length, 1);
});

test("same idempotency key with different content is a permanent conflict", async () => {
  const { bus } = await fixture();
  await bus.publish(valid);
  await rejectsCode(
    bus.publish({ ...valid, payload: { claim: "different" } }),
    "idempotency_conflict",
  );
});

test("a second idempotency key cannot bypass logical message uniqueness", async () => {
  const { bus } = await fixture();
  await bus.publish(valid);
  await rejectsCode(
    bus.publish({ ...valid, idempotency_key: "another-key" }),
    "logical_duplicate",
  );
});

test("publication after the authenticated phase closes is denied", async () => {
  const { bus, phaseStatePath } = await fixture();
  await writeFile(phaseStatePath, JSON.stringify({ closed_phases: ["collect"] }));
  await rejectsCode(bus.publish(valid), "phase_closed");
});

test("a forged receipt is rejected", async () => {
  const { bus, journalPath } = await fixture();
  const receipt = await bus.publish(valid);
  await rejectsCode(
    verifyReceipt({ journalPath, receipt: { ...receipt, payload_hash: "sha256:forged" } }),
    "receipt_not_found",
  );
});

test("two concurrent identical calls append only once", async () => {
  const { bus, journalPath } = await fixture();
  const [a, b] = await Promise.all([bus.publish(valid), bus.publish(valid)]);
  assert.equal(a.event_id, b.event_id);
  assert.equal((await readFile(journalPath, "utf8")).trim().split(/\r?\n/).length, 1);
});
