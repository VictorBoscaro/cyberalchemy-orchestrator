import test from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { mkdtemp, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const serverPath = path.resolve(here, "../src/mcp-server.mjs");
const context = {
  run_id: "run-rpc",
  dispatch_id: "dispatch-rpc",
  group_id: "group-rpc",
  group_version: 1,
  seat_id: "seat-rpc",
  agent_instance_id: "agent-rpc",
  attempt_id: "attempt-rpc",
  actor_principal_id: "principal-rpc",
  phase: "collect",
};

function frame(message) {
  return `${JSON.stringify(message)}\n`;
}

test("MCP surface exposes publish only and rejects peer reads", async (t) => {
  const dir = await mkdtemp(path.join(os.tmpdir(), "agent-bus-mcp-"));
  const state = path.join(dir, "phase-state.json");
  await writeFile(state, JSON.stringify({ closed_phases: [] }));
  const child = spawn(process.execPath, [serverPath], {
    env: {
      ...process.env,
      BUS_CONTEXT_JSON: JSON.stringify(context),
      BUS_JOURNAL_PATH: path.join(dir, "journal.jsonl"),
      BUS_PHASE_STATE_PATH: state,
    },
    stdio: ["pipe", "pipe", "pipe"],
  });
  t.after(() => child.kill());

  let buffer = "";
  const pending = new Map();
  child.stdout.on("data", (chunk) => {
    buffer += chunk.toString("utf8");
    while (true) {
      const boundary = buffer.indexOf("\n");
      if (boundary < 0) return;
      const line = buffer.slice(0, boundary).replace(/\r$/, "");
      buffer = buffer.slice(boundary + 1);
      if (!line.trim()) continue;
      const message = JSON.parse(line);
      pending.get(message.id)?.(message);
      pending.delete(message.id);
    }
  });

  let id = 0;
  const rpc = (method, params = {}) => new Promise((resolve, reject) => {
    const requestId = ++id;
    const timer = setTimeout(() => reject(new Error(`timeout waiting for ${method}`)), 3000);
    pending.set(requestId, (message) => {
      clearTimeout(timer);
      resolve(message);
    });
    child.stdin.write(frame({ jsonrpc: "2.0", id: requestId, method, params }));
  });

  const initialized = await rpc("initialize", { protocolVersion: "2024-11-05" });
  assert.equal(initialized.result.serverInfo.name, "agent-bus-publication-probe");
  const listed = await rpc("tools/list");
  assert.deepEqual(listed.result.tools.map((tool) => tool.name), ["bus_publish"]);

  const peerRead = await rpc("tools/call", { name: "bus_read_peer", arguments: {} });
  assert.equal(peerRead.error.code, -32602);

  const published = await rpc("tools/call", {
    name: "bus_publish",
    arguments: {
      idempotency_key: "rpc-key",
      operation_id: "rpc-operation",
      round_id: "round-1",
      message_type: "position",
      payload: { answer: 42 },
    },
  });
  const receipt = JSON.parse(published.result.content[0].text);
  assert.equal(receipt.status, "accepted");
});
