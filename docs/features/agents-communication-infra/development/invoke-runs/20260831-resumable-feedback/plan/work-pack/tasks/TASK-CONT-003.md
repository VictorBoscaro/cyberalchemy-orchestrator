# TASK-CONT-003 — Continuation failure and recovery hardening

## Objective

Implement explicit reconstruction, unknown reconciliation, cancellation, expiry and all crash/race
cases without duplicating physical work.

## Dependencies

- TASK-CONT-002 completed and independently verified.

## DomainSpec Coverage

CONT-I4..I7, O-CONT-X1..X6, O-CONT-C1..C4, continuation loss/unknown/cancel/expiry events, AgentAdapter
status/dispose/cancel contracts, T-ACI-CONT5..9.

## Architecture References

- [Shared context](../shared/context.md)
- [Dependency rules](../../../../../../../../../domainspec/architecture/pattern-library/DEPENDENCY-RULES.md)
- [Testing alignment](../../../../../../../../../domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md)
- [Bounded sequence](../../../../../../specs/architecture.md#bounded-feedback-continuation)

## Implementation Directives

- Treat `capability_absent_no_handle` and `handle_definitively_unavailable_no_start` as the only
  reconstruction-enabling evidence; unknown blocks replacement.
- Reconstruct in one atomic unit with a new instance/attempt and the same input semantics.
- Cancellation before claim must atomically make the effect unclaimable; claimed cancellation must
  reconcile the target attempt. Deadline after claim routes through cancellation.
- Add failpoints at every resume/reconstruct acceptance member and reopen SQLite after each.
- Parameterize every continuation state/event pair and assert no mutation for unlisted pairs.

## Write Scope

- `implementations/server/runtime/continuation.py`
- `implementations/server/runtime/continuation_runtime.py`
- `implementations/server/runtime/service.py`
- `implementations/tests/runtime/test_agent_continuation.py`
- `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/WORK-PACK.md`
- this task file and `../waves/W3.md`
- `../shared/traceability.md`
- `../../evidence/TASK-CONT-003.md` (review/test/closure evidence; new)

## Gaps and Questions

Real provider retention and cancellation are not evidence for this task; fake observations must
exercise the same typed adapter contract. Schema changes are not permitted here; a missing column or
index returns BLOCK for an explicit TASK-CONT-001 amendment.

## Decision Lock

At most one reconstruction. Unknown never falls back automatically.

## Done Criteria

- T-ACI-CONT5..9 pass, including exhaustive transitions and all failpoints.
- Unknown, cancellation and expiry never permit duplicate claim/start.
- SQLite reopen/replay converges to one target/replacement/effect/terminal.
- The full runtime suite adds no signature beyond [the pre-mutation baseline](../../BASELINE.md),
  and the independent verifier accepts. An unqualified full-suite PASS remains unavailable until
  the separately owned manifest/fixture drift is repaired.

## Agent Topology

Two read-only auditors, one `domainspec-implement` coder and one independent `review` verifier;
single writer, sequential dependency on TASK-CONT-002.
