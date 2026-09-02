---
tags: [agent-dispatch, confirmed-dispatch, runtime-continuation, execution-policy, deterministic-replay]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-09-01T13:26:40-03:00
updated_at: 2026-09-01T15:24:00-03:00
expires: 2026-10-31
decisions_made: true
contradictions_found: false
specs_updated:
  - docs/features/agents-communication-infra/TEST-SPEC.md
  - docs/features/agents-communication-infra/specs/TEST-SPEC.md
  - docs/features/agents-communication-infra/specs/architecture.md
  - docs/features/agents-communication-infra/specs/confirmation-authority.md
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session completed the bounded durable ACI path through POLICY-002 while preserving the product-authority boundary before autonomous execution."
---

# ACI bounded roadmap closure through POLICY-002

## Summary

The repository objective is to keep delegated agent work bound to explicit objectives, authority, decisions and evidence across every handoff. This session resumed the ACI continuation gate to establish who confirms a dispatch and how that authority becomes durable runtime state. The owner decided that explicit user confirmation is authoritative, whether supplied in chat now or through a future UI, provided it binds the exact dispatch content. CONF-000 froze the contract fixture and CONF-001 implemented the durable `ConfirmedDispatch` writer with a Run ending at `opening_pending` and no external action. CONT-001, HEADS-001 and BUS-001 then implemented and independently reviewed bounded suspension, graph heads, fencing and official result publication. POLICY-000 through POLICY-002 established a non-executable ladder ending in one deterministic, durable, test-only fake denial with fail-closed replay, corruption and concurrency handling. Final evidence reports 12/12 focused POLICY-002 tests, 59/59 combined policy tests and 260/260 curated runtime tests across 27 modules, with the external Lean bridge explicitly excluded. The canonical Control Center validation passed 36/36, while the earlier repaired 152/152 runtime baseline remains separate historical evidence; this session required no additional baseline repair. The feature ledger now records the completed bounded increments, preserves `DEC-ACI-PRODUCT-PASS-001` as the sole active blocking decision and records the transversal roadmap review only as a planned, unexecuted artifact. A deterministic JSON compiler exists, but no resident worker yet consumes `ConfirmedDispatch` through opening, invocation, adapter execution and result continuation without an orchestrating parent.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [ACI dispatch continuation and confirmation gate](2026-08-31-2006-aci-dispatch-continuation-gate.md) | `derives-from` | This node closes the bounded implementation arc opened by the earlier continuation and authority gate. |
| [Agents Communication Infrastructure Craft ledger](../docs/features/agents-communication-infra/CRAFT.md) | `contextualizes` | This session supplies the narrative context for the completed increments, current blocker, residue and planned review recorded by the feature ledger. |
| [POLICY-002 implementation review](../docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-IMPLEMENTATION-REVIEW.md) | `derives-from` | The closing claims about POLICY-002 and its validation boundary are grounded in this final PASS/KEEP evidence. |
| [ExecutionGraph authority refinement and compiler boundary](2026-09-01-1524-aci-execution-graph-refinement.md) | `grounds` | This session's unresolved product-authority question and technical graph gap became the starting evidence for the later refinement. |

## Open questions

- Which exact revision-instruction and prompt bytes, references, digests, role/task/provider
  references, resource budget, sandbox policy, execution fence and complete audit-opening 0.6.4
  mapping should define the product-owned CONF v2 authority package?

## Next steps

1. Resolve `DEC-ACI-PRODUCT-PASS-001` with the exact product-owned CONF v2 inputs.
2. Create a new dispatch identity, freeze its authority package and obtain explicit confirmation
   bound to those exact bytes and digests.
3. Execute the planned transversal closure review before promoting real L3 execution claims.
4. Prepare separate workpacks and readiness gates for OPEN, RESUME, WORKER, VERIFY and
   POLICY-003/L3.

## Recommendation

Keep the implemented CONF through POLICY-002 path as the bounded durable foundation, but do not
describe it as an autonomous dispatcher; use the planned cross-cutting review to challenge the
integration boundary before the product-owned CONF v2 package authorizes any L3 work.

## Files touched

- `docs/decisions/aci-resumable-agent-continuation.md`
- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `docs/features/agents-communication-infra/CRAFT.md`
- `docs/features/agents-communication-infra/TEST-SPEC.md`
- `docs/features/agents-communication-infra/specs/TEST-SPEC.md`
- `docs/features/agents-communication-infra/specs/architecture.md`
- `docs/features/agents-communication-infra/specs/confirmation-authority.md`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-CONF-000.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-CONF-001.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-POLICY-000.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-POLICY-001.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-POLICY-002.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-CONT-001-CONTEXT.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-CONT-001-SCAFFOLD.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-POLICY-002-CONTEXT.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-POLICY-002-SCAFFOLD.md`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-AGENT-CONTINUATION-001.json`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CONFIRMED-DISPATCH-001.json`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-EXECUTION-POLICY-ORACLE-000.json`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-EXECUTION-POLICY-LINEAGE-001.json`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/evidence/CONF-000.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/evidence/CONF-001.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-CONT-001.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-HEADS-001.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-BUS-001.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-IMPLEMENTATION-REVIEW.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-IMPLEMENTATION-REVIEW.md`
- `implementations/server/runtime/artifacts.py`
- `implementations/server/runtime/confirmation.py`
- `implementations/server/runtime/confirmed_bus.py`
- `implementations/server/runtime/continuation.py`
- `implementations/server/runtime/database.py`
- `implementations/server/runtime/errors.py`
- `implementations/server/runtime/execution_policy.py`
- `implementations/server/runtime/journal.py`
- `implementations/server/runtime/run_group.py`
- `implementations/server/runtime/service.py`
- `implementations/server/runtime/migrations/012_runtime_confirmation.sql`
- `implementations/server/runtime/migrations/013_agent_continuation.sql`
- `implementations/server/runtime/migrations/014_runtime_run_group_heads.sql`
- `implementations/server/runtime/migrations/015_runtime_attempt_result_bus.sql`
- `implementations/tests/runtime/test_runtime_confirmation.py`
- `implementations/tests/runtime/test_runtime_confirmed_bus.py`
- `implementations/tests/runtime/test_agent_continuation.py`
- `implementations/tests/runtime/test_runtime_run_group_heads.py`
- `implementations/tests/runtime/test_agent_reference_delivery.py`
- `implementations/tests/runtime/execution_policy_oracle_v1.json`
- `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json`
- `implementations/tests/runtime/execution_policy_denial_oracle_v1.json`
- `implementations/tests/runtime/policy_lineage_harness.py`
- `implementations/tests/runtime/policy_denial_harness.py`
- `implementations/tests/runtime/test_execution_policy.py`
- `implementations/tests/runtime/test_execution_policy_lineage.py`
- `implementations/tests/runtime/test_execution_policy_denial.py`
- `sessions/2026-09-01-1326-aci-bounded-roadmap-closure.md`
