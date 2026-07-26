import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const evidenceRoot = ".codex/workflow-inputs/2026-07-26-phase-a-host-bus-integrity";
const proposalPath =
  "plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-concrete-core-v2.json";
const proposal = JSON.parse(fs.readFileSync(path.join(root, proposalPath), "utf8"));
const bound = new Map(proposal.bound_inputs.map((item) => [item.path, item.sha256]));

const targets = [
  {
    seat: "alignment-audits/alignment",
    seatIndex: 0,
    attemptId: "attempt-liskov-0",
    output: "alignment-manifest.json",
  },
  {
    seat: "alignment-audits/layering",
    seatIndex: 1,
    attemptId: "attempt-parnas-0",
    output: "layering-manifest.json",
  },
];

for (const target of targets) {
  const contract = proposal.workflow_input_contracts[target.seat][0];
  const sources = contract.allowed_paths.map((relativePath) => {
    const bytes = fs.readFileSync(path.join(root, relativePath));
    const actual = crypto.createHash("sha256").update(bytes).digest("hex");
    if (actual !== bound.get(relativePath)) {
      throw new Error(`bound input drift: ${relativePath}`);
    }
    return {
      source_kind: "repository",
      producer_binding_id: null,
      path: relativePath,
      sha256: `sha256:${actual}`,
      size_bytes: bytes.length,
    };
  });
  if (
    sources.length !== contract.cardinality.min ||
    sources.length !== contract.cardinality.max
  ) {
    throw new Error(`cardinality mismatch: ${target.seat}`);
  }
  const manifest = {
    schema: "aci-workflow-input-manifest/v1",
    dispatch_id: "2026-07-26-phase-a-host-bus-integrity",
    target: {
      group_id: "alignment-audits",
      seat_index: target.seatIndex,
      turn_ordinal: 0,
      attempt_id: target.attemptId,
    },
    slots: [
      {
        name: contract.name,
        data_schema_ref: contract.data_schema_ref,
        cardinality: contract.cardinality,
        max_bytes: contract.max_bytes,
        purpose: contract.purpose,
        sources,
      },
    ],
  };
  fs.writeFileSync(
    path.join(root, evidenceRoot, target.output),
    `${JSON.stringify(manifest)}\n`,
    "utf8",
  );
}
