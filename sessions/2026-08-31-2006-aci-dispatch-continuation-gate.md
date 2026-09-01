---
tags: [agent-dispatch, event-journal, agent-continuation, runtime-authority]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-31T20:06:52-03:00
updated_at: 2026-09-01T04:13:51-03:00
expires: 2026-10-30
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agents-communication-infra/TEST-SPEC.md
  - docs/features/agents-communication-infra/specs/SPEC.md
  - docs/features/agents-communication-infra/specs/architecture.md
  - docs/features/agents-communication-infra/specs/capabilities/resumable-agent-continuation.md
  - docs/features/agents-communication-infra/specs/domain.md
  - docs/features/agents-communication-infra/specs/events.md
  - docs/features/agents-communication-infra/specs/glossary.md
  - docs/features/agents-communication-infra/specs/interfaces.md
  - docs/features/agents-communication-infra/specs/mappings.md
  - docs/features/agents-communication-infra/specs/operations.md
  - docs/features/agents-communication-infra/specs/rules.md
  - docs/features/agents-communication-infra/specs/states.md
  - docs/features/agents-communication-infra/specs/workflows.md
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session fixed the bounded continuation contract and exposed the missing confirmed-dispatch authority that must precede autonomous execution."
---

# ACI dispatch continuation and confirmation gate

## Summary

The repository objective is to keep delegated agent work connected to explicit objectives, authority, decisions and evidence across every handoff. This session focused that objective on deterministic dispatch infrastructure and explicitly removed Schema Service from the active scope. The owner accepted a finite `author:0 -> reviewer:0 -> author:1` workflow in which a terminal author turn is parked without polling and later receives exact official bus contributions through runtime materialization. Same-session continuation was retained as an optimization while immutable reconstruction input became the correctness boundary. DomainSpec contracts, lifecycle states, mappings, operations, interfaces, rules, architecture, glossary and tests were aligned and independently reviewed. A bounded host probe showed same-agent-reference follow-up with prior-turn recall and active interruption, but did not prove restart durability or project-adapter support. A sequential three-task implementation pack, reviewer topology, context scaffolds and pre-mutation test baseline were prepared. At the 2026-08-31 pre-code checkpoint, audit contradicted the initial readiness result because no runtime-managed `ConfirmedDispatch` writer or confirmed turn graph then existed; readiness was corrected to BLOCK and no continuation code had yet been written. The 2026-09-01 continuation below records that the bounded CONF, CONT, HEADS and BUS components later passed and that PRODUCT-PASS is now the active blocker.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Infrastructure Craft ledger](../docs/features/agents-communication-infra/CRAFT.md) | `is-part-of` | This session records the current state, decisions and residue of that feature scope. |
| [ACI resumable agent continuation](../docs/decisions/aci-resumable-agent-continuation.md) | `derives-from` | The accepted continuation decision governs the bounded lifecycle and identity model developed here. |
| [Continuation decision gate](../docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/DECISION-GATE.md) | `contextualizes` | The gate preserves the authority-source contradiction found before code entry and the two remaining options. |

## Open questions

- What exact revision-instruction and prompt bytes/refs/digests, role/task/provider references,
  resource/sandbox/fence policies and canonical audit-opening 0.6.4 mapping should define the real
  CONF v2 dispatch authority?

## Next steps

1. Resolve PRODUCT-PASS with the exact product-owned bytes, references, policies and complete
   canonical audit-opening 0.6.4 mapping.
2. Create a new dispatch identity and CONF v2 authority package because those inputs change
   `confirmed_authority_digest`; obtain a new explicit user confirmation.
3. Issue separate exact workpacks/readiness for OPEN, positive Run transition, RESUME, WORKER and
   VERIFY. Do not promote CONT-002 before those gates pass.

## Recommendation

Keep CONF v1 as a component fixture. Do not infer product authority or reuse its dispatch identity;
real execution must begin from the newly confirmed CONF v2 package.

## 2026-09-01 continuation

The durable authority path was selected and implemented in bounded stages. CONF-000, CONF-001,
CONT-001, HEADS-001 and BUS-001 all reached independently reviewed PASS within their declared
component ceilings. BUS-001 records 23/23 focused tests, HEADS 8/8, CONT 9/9, CONF 8/8,
traceability 1/1, Stage-C 8/8, bridge 18/18, runtime 200/200, Control Center 36/36, Stage-E 75/75,
compile/diff PASS and red-team `PASS / KEEP`.

The accepted publication placement keeps the candidate on the Attempt stream; official acceptance
adds `attempt.result_accepted` plus the typed position/critique event to the Group stream. The
Attempt link does not transition the completed Attempt, while the Group advances exactly `+2`.

The remaining blocker is product authority, not an unresolved technical implementation choice.
PRODUCT-PASS must supply revision-instruction and prompt bytes/refs/digests, role/task/provider
references, resource/sandbox/execution-fence policies and the complete canonical audit-opening
0.6.4 mapping. OPEN, RESUME, WORKER and VERIFY remain unpromoted.

## Files touched

- `docs/decisions/aci-resumable-agent-continuation.md`
- `docs/features/agents-communication-infra/TEST-SPEC.md`
- `docs/features/agents-communication-infra/specs/SPEC.md`
- `docs/features/agents-communication-infra/specs/architecture.md`
- `docs/features/agents-communication-infra/specs/capabilities/resumable-agent-continuation.md`
- `docs/features/agents-communication-infra/specs/domain.md`
- `docs/features/agents-communication-infra/specs/events.md`
- `docs/features/agents-communication-infra/specs/glossary.md`
- `docs/features/agents-communication-infra/specs/interfaces.md`
- `docs/features/agents-communication-infra/specs/mappings.md`
- `docs/features/agents-communication-infra/specs/operations.md`
- `docs/features/agents-communication-infra/specs/rules.md`
- `docs/features/agents-communication-infra/specs/states.md`
- `docs/features/agents-communication-infra/specs/workflows.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/probes/host-continuation-probe.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/implementation-layering.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/WORK-PACK.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/DECISION-GATE.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/READINESS.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/TASK-CONT-001-DRY-RUN.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/BASELINE.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/shared/context.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/shared/traceability.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-001.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-002.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-003.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/waves/W0.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/waves/W1.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/waves/W2.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/work-pack/waves/W3.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-CONT-001-CONTEXT.md`
- `docs/features/agents-communication-infra/work-pack/context/TASK-CONT-001-SCAFFOLD.md`
- `docs/features/agents-communication-infra/.craft/ledger.yml`
- `docs/features/agents-communication-infra/.craft/artifacts/progress-snapshot-2026-08-31.md`
- `docs/features/agents-communication-infra/CRAFT.md`
- `sessions/2026-08-31-2006-aci-dispatch-continuation-gate.md`
