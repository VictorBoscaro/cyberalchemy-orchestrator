# Context pack — SWU-ACI-AGENT-CONTINUATION-001

## Identity and objective

- Task: `TASK-CONT-001`
- Descriptor: `work-pack/descriptors/SWU-ACI-AGENT-CONTINUATION-001.json`
- Claim: CONF-001 authority consumer/component only
- Minimum proof: one effect-free suspension event/aggregate/members/receipt unit

## Obligation coverage

| Obligation | Evidence selector | Resolution |
|---|---|---|
| Completed confirmed author source | `operations.md#SuspendAgentContinuation`, O-CONT-S1/S5 | Test-only full `AttemptLifecycle` through generic journal acceptance; no production attempt writer. |
| Frozen snapshot and awaited mappings | O-CONT-S2/S4, T-ACI-CONT1 | Immutable terminal snapshot binding; exact confirmed mappings; exact zero-of-two official facts. |
| Stable replay/conflict | O-CONT-S4 | Service-derived fixed scope/key and fully discriminating semantic intent. |
| Effect-free atomic acceptance | Suspend postconditions, T-ACI-CONT1/8 | Generic `RuntimeJournal.accept`; one event/head/mutation/receipt; zero effects. |
| Invalid lifecycle rejection | T-ACI-CONT9 | Pure reducer and base L2 Cartesian rejection matrix. |
| Runtime/legacy separation | CONF-001 evidence + migrations 009/010/012 | Four isolated migration 013 tables, direct CONF-001 parents, zero backfill, legacy unchanged. |

## Selected evidence

- `development/invoke-runs/20260831-resumable-feedback/evidence/CONF-001.md` — closed predecessor.
- `specs/fixtures/confirmed-dispatch-v1/manifest.json` — frozen confirmed graph/mapping oracle.
- `TEST-SPEC.md#bounded-resumable-feedback` — T-ACI-CONT1 and base T-ACI-CONT9 proof.
- `specs/operations.md#SuspendAgentContinuation` — O-CONT-S1..S5 and zero-effect postcondition.
- `specs/domain.md#AgentContinuation` — aggregate fields and invariants.
- `runtime/migrations/009_host_workflow_binding.sql` and `010_agent_reference_delivery.sql` — legacy boundary.
- `runtime/migrations/012_runtime_confirmation.sql` — confirmed runtime parents.
- `runtime/journal.py#RuntimeJournal.accept` — generic atomic acceptance seam.
- `robot-talks/2026-09-01-continuation-l2-d0/findings.md` — resolved D0 tensions.
- exact task, descriptor and readiness receipt — write/validation authority.

## Resolved contradictions

- A production attempt creator is not required for a component consumer proof; a seeded terminal row
  is also insufficient. The harness traverses the complete journal-backed lifecycle and exposes no
  production symbol or `ACI_SCHEMAS` widening; it binds the test-only event validators directly to
  the journal.
- Generic acceptance is sufficient only with service-derived fixed scope/key and one create
  identity. Caller control or identity sharing is a stop condition.
- Deadline authority comes from confirmation, not deferred opening verification.
- Partial/full official input facts belong to CONT-002; L2 accepts only exact zero-of-two.
- Stable replay precedes current-fact evaluation. Existing rows reconstruct command/event/intent
  from persisted bytes; only create prechecks and transactionally revalidates zero-of-two.
- Runtime authority uses isolated direct CONF-001 parents; compatibility tables grant none.
- Service may use read-only SELECTs and mutation SQL only on the connection supplied by generic
  journal acceptance. It cannot open a write connection, commit, create another transaction/writer
  or relocate repository methods into `database.py`.

## Constraints and fallback

The exact descriptor owns write scope, semantic discriminants, stop conditions and commands. If an
obligation cannot be met without editing a read-only path, adding an effect, changing legacy or
CONF-001 rows, resolving official contributions, or widening the claim, stop and return the gap to
planning. Do not improvise a compatibility or direct terminal-row shortcut.
