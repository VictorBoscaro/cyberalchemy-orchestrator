import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const proposal = JSON.parse(
  fs.readFileSync(
    path.join(
      root,
      "plans/governed-agent-work-infrastructure/workstreams/phase-a-post-gate-review-concrete-core-v1.json",
    ),
    "utf8",
  ),
);
const bindings = [...proposal.target_bindings, ...proposal.authority_bindings];
const sources = bindings.map((binding) => {
  const bytes = fs.readFileSync(path.join(root, binding.path));
  const actual = crypto.createHash("sha256").update(bytes).digest("hex");
  if (actual !== binding.sha256) {
    throw new Error(`binding drift: ${binding.path}`);
  }
  return {
    source_kind: "repository",
    producer_binding_id: null,
    path: binding.path,
    sha256: `sha256:${actual}`,
    size_bytes: bytes.length,
  };
});
const seats = [
  { file: "hoare-manifest.json", seatIndex: 0, attemptId: "attempt-hoare-0" },
  { file: "liskov-manifest.json", seatIndex: 1, attemptId: "attempt-liskov-0" },
  { file: "parnas-manifest.json", seatIndex: 2, attemptId: "attempt-parnas-0" },
];
for (const seat of seats) {
  const manifest = {
    schema: "aci-workflow-input-manifest/v1",
    dispatch_id: "2026-07-26-phase-a-post-gate-review",
    target: {
      group_id: "attackers",
      seat_index: seat.seatIndex,
      turn_ordinal: 0,
      attempt_id: seat.attemptId,
    },
    slots: [
      {
        name: "review_corpus",
        data_schema_ref: "application/octet-stream",
        cardinality: { min: 27, max: 27 },
        max_bytes: 1300000,
        purpose: "Read the complete frozen review target corpus and its governing authorities while keeping runtime evidence queries read-only and selector-bounded.",
        sources,
      },
    ],
  };
  fs.writeFileSync(
    path.join(root, ".codex/workflow-inputs/2026-07-26-phase-a-post-gate-review", seat.file),
    `${JSON.stringify(manifest)}\n`,
    "utf8",
  );
}
