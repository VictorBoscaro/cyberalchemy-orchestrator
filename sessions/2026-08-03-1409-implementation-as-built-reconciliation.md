---
tags: [agent-work-harness, provenance, authority, reconstruction, subagent-dispatch]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-03T14:09:19-03:00
updated_at: 2026-08-03T14:09:19-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "This session established the code-first current state and ordered frontier for the repository's central governed-work harness."
---

# Implementation AS-BUILT reconciliation

## Summary

The repository's main objective is to keep agent work connected to the objectives, decisions, authority, context, actions, and evidence that give it meaning. This session set out to determine the current code-first state under `implementations/`, identify work that had started but stopped, and explain what the next tasks buy for the harness rather than merely listing technical components. It decided that current code is authoritative for implementation state while tests, operational receipts, accepted decisions, and documents remain separate evidence dimensions. Seven independent worker/reviewer pairs investigated system boundaries, host adoption, authority, recovery, handoffs, reconstruction, and human control before a synthesizer composed the result. The investigation found strong transactional integrity and replay inside the governed SQLite runtime, but no universal guarantee that real host work enters that runtime. It also found self-asserted authority, requested rather than enforced seat limits, no exact terminal-output commitment, and no complete cold reconstruction path. An executable counterexample showed that two messages from one BUS seat can currently manufacture nominal two-seat quorum. This dispatch itself had repository artifacts but no runtime host bindings, making it direct evidence of the capture/adoption gap, while an unattributed concurrent change to `service.py` was preserved as temporal drift rather than silently absorbed. The resulting [AS-BUILT](../implementations/AS-BUILT.md) separates implementation, proof, operation, authority, official adoption, and reconstructibility across 40 indexed claims. The recommended order is to enforce and reconcile host binding, fix false quorum, persist exact terminal outputs, measure contribution completeness, authenticate authority, complete handoff and recovery, and only then expose a joined reconstruction view.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Implementation AS-BUILT](../implementations/AS-BUILT.md) | `contextualizes` | This session records the objective, investigation method, material contradictions, and decisions that produced the code-first AS-BUILT. |

## Open questions

- Which external identity and entitlement mechanism should authenticate a human decision before capability issuance?
- Should `implementations/agent-runtime` remain an experimental oracle, be mined and retired, or converge with the governed server runtime?
- What evidence, if any, can establish the authorship and intent of the mid-investigation `service.py` drift?

## Next steps

1. Make host binding obligatory and reconcile every declared seat and turn against durable runtime records.
2. Count BUS quorum from distinct eligible seats under an explicit message policy.
3. Persist the exact terminal output and observed effects for every bound turn.
4. Record every expected contribution as captured, partial, missing, or failed.
5. Separate declared decision, authorization evidence, authenticated identity, and verified entitlement.
6. Complete provider delivery, recovery, restore, and claim-support checks before building the aggregate reconstruction view.

## Recommendation

Start with host adoption and reconciliation because every later authority, evidence, handoff, and reconstruction improvement depends on knowing that the work entered the governed memory at all.

## Files touched

- `implementations/AS-BUILT.md`
- `implementations/as-built/build_dispatch_payload.py`
- `implementations/as-built/build_source_manifest.py`
- `implementations/as-built/capability-review-receipt.json`
- `implementations/as-built/check-tension-checker-receipt.json`
- `implementations/as-built/check-tension-reviewer-receipt.json`
- `implementations/as-built/dispatch-payload.json`
- `implementations/as-built/dispatch-record.json`
- `implementations/as-built/pair-output-schema.json`
- `implementations/as-built/pairs/pair-01-system-of-record.json`
- `implementations/as-built/pairs/pair-01-system-of-record.md`
- `implementations/as-built/pairs/pair-02-host-adoption.json`
- `implementations/as-built/pairs/pair-02-host-adoption.md`
- `implementations/as-built/pairs/pair-03-authority.json`
- `implementations/as-built/pairs/pair-03-authority.md`
- `implementations/as-built/pairs/pair-04-memory-recovery.json`
- `implementations/as-built/pairs/pair-04-memory-recovery.md`
- `implementations/as-built/pairs/pair-05-handoff-integrity.json`
- `implementations/as-built/pairs/pair-05-handoff-integrity.md`
- `implementations/as-built/pairs/pair-06-reconstruction.json`
- `implementations/as-built/pairs/pair-06-reconstruction.md`
- `implementations/as-built/pairs/pair-07-human-control.json`
- `implementations/as-built/pairs/pair-07-human-control.md`
- `implementations/as-built/source-drift-record.json`
- `implementations/as-built/source-manifest.json`
- `implementations/as-built/source-manifest-current.json`
- `implementations/as-built/structural-proposal.json`
- `implementations/as-built/synthesis-report.json`
- `implementations/as-built/synthesis-report-schema.json`
- `telemetry/agents/subagents-dispatch.yaml`
