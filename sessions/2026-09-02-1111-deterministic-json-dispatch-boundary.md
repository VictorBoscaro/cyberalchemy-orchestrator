---
tags: [agents-communication-infrastructure, deterministic-dispatch, execution-graphs, host-bindings, orchestration]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-09-02T11:11:44-03:00
updated_at: 2026-09-02T11:11:44-03:00
expires: 2026-11-01
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/draft-graph-v1.proposed.schema.json
  - docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/COMPILATION-CONTRACT.md
  - docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001/WORK-PACK.md
promoted_candidates: []
expected_importance: 9
importance_rationale: "This session established deterministic local JSON execution and isolated the remaining host-bound launch boundary without overstating production capability."
---

# Deterministic JSON dispatch boundary

## Summary

The repository objective is to keep multi-agent work structurally connected to its governing intent, decisions, execution, and evidence. This session pursued deterministic dispatch from governed JSON through an executable agent graph. The DraftGraph identity and role work received `KEEP` at review SHA-256 `E67819A7896AF0B58599233600853D0A70E8586F4594E5FDCDABC8F5CA4AE7DB`, including allocator-owned `display_name` values and a versioned closed role registry. The local runtime received `KEEP` at review SHA-256 `8B5F152CD04AE9BBE44BC868802241432C779ACAE5FA3C01E0828937EB8F9DFF` for the bounded path from nine manifested JSON inputs through compilation, exact acceptance, SQLite scheduling, `ScriptedLocalAdapter`, and terminal state, but not for live or host-bound execution. Lifecycle research then proved that the current compiler deadlocks a sequential handoff by requiring the producer receipt before launching the producer and does not execute `feedback` plus `loop_cap`, as recorded by review SHA-256 `9173AB80B3C7FE1F1B2FC6017B97021F9CBD440262A3E3A4DB05C97B5A785F9B`. A Stage-E manifest drift repair received `KEEP` at SHA-256 `4076878260B43E714AD9C79E525DF6705AC9D5A8D8DC1278BF32E4E4FB9BB71C`, and the Craft opening JSON remained valid at SHA-256 `4265998B14E796081709510D5A916AB727496529E358F9CBF75B221277D57464`. The subsequent Craft dispatch opened session `ses_87e29f91b9d29b273730af26b0c9b37e` but produced zero host bindings, its seat was interrupted, and it closed with `error` in event `evt_03d42c9a639768c5ddab0085d7b78983`; its partial outputs were later recovered and independently kept only as ledger evidence, with ledger SHA-256 `5BCEBF0EA2E3130158086A7509A9D6405E57CF31F81965EBE236B03753CC5115`. The attempted host-bound repair was interrupted at the user's request before producing a distinct source or workflow artifact, and this session closes because the user invoked `close-session`.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Infrastructure](../docs/features/agents-communication-infra/README.md) | `is-part-of` | The session advances the feature's governed dispatch and execution capability. |
| [Execution graph refinement session](2026-09-01-1524-aci-execution-graph-refinement.md) | `derives-from` | This work continued the DraftGraph and executable-graph boundary established in the preceding session. |
| [Identity and role implementation review](../docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001/review.md) | `derives-from` | Its final `KEEP` supports the identity and role capability recorded here. |
| [Execution runtime review](../docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md) | `derives-from` | Its final `KEEP` defines the exact local-runtime capability ceiling. |
| [Deterministic JSON lifecycle review](../docs/features/agents-communication-infra/research/deterministic-json-dispatch/review-research-lifecycle.md) | `derives-from` | Its executable failure evidence establishes the sequential-handoff and feedback blockers. |
| [Craft lifecycle residue](../.codex/workflow-inputs/2026-09-02-craft-ledger-json-dispatch-update/lifecycle-residue.md) | `derives-from` | It records the failed host-binding lifecycle and prevents partial outputs from being treated as dispatch success. |

## Open questions

- Why did the host hook create no `host_workflow_turn_bindings` row after receiving a generated binding-first prompt?

## Next steps

1. Repair and independently review one terminal, parent-bound single-seat launch from validated JSON.
2. Implement incremental ready-group compilation so downstream bindings are created only after verified producer receipts exist.
3. Implement governed `feedback` and `loop_cap` scheduling with worker/reviewer correction evidence.
4. Prove the complete JSON-to-host-bound-seat path end to end without expanding the accepted local-runtime claim into production readiness.

## Recommendation

Repair and independently review the terminal, parent-bound single-seat launch first.

## Files touched

- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-DRAFT-GRAPH-001/`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001/`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001/`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001/`
- `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/`
- `implementations/server/runtime/execution_graph_runtime.py`
- `implementations/server/runtime/migrations/016_local_execution_graph_runtime.sql`
- `implementations/tests/runtime/test_execution_graph_runtime.py`
- `docs/features/agents-communication-infra/research/deterministic-json-dispatch/`
- `.codex/workflow-inputs/2026-09-02-deterministic-json-dispatch-host-gap/`
- `.codex/workflow-inputs/2026-09-02-stage-e-manifest-repair/`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256`
- `.codex/workflow-inputs/2026-09-02-craft-ledger-json-dispatch-update/`
- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `docs/features/agents-communication-infra/CRAFT.md`
- `docs/features/agents-communication-infra/.craft/artifacts/2026-09-02-json-dispatch-ledger-update/update-report.md`
- `sessions/2026-09-02-1111-deterministic-json-dispatch-boundary.md`
