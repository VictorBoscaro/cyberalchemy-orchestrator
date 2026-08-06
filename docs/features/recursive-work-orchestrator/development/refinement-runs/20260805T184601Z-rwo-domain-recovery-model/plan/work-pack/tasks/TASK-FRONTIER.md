# TASK-FRONTIER — Accepted History And Atomicity

## Objective

Prove cross-case arbitration and one-shot acceptance under concurrency and
restart. This task owns SWU-RRD-005 and 006 and maps to S-002/L1/W2.

## Source Contracts

- `../../../stages/08-distill-repair.md`, sections 1.2 and 8
- `implementations/server/runtime/journal.py`
- `implementations/server/runtime/database.py`
- `implementations/server/runtime/schema.sql`

## Dependencies And Gaps

- SWU-RRD-004 must pass.
- SWU-RRD-006 is blocked by G1 until the journal/domain owner accepts the exact
  frontier and mismatch contract. SWU-RRD-005 may use pure accepted-record fixtures.

## SWU-RRD-005 — RecoveryFrontier Reducer

- Primary behavior: reduce accepted records into at most one actionable trigger
  per overlapping subject scope with closed inhibition and trigger consumption.
- Dependencies: SWU-RRD-004.
- Write scope: exactly `allowed-routes.json#rrd-l1-frontier.write_scope`.
- Done: reducer is pure/versioned; conflict, resume, unresolved effect,
  cancellation/terminal, compensation, and consumed-trigger precedence are
  explicit; disjoint scopes remain independently actionable.
- Acceptance evidence: ADV-01/02 games, ancestor/descendant scope cases,
  consumed-trigger rebuild, and order-independent record fixtures.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_frontier -v`.
- Execution owner: local-fallback via Task Session.
- Split analysis: selection and inhibition are one reducer invariant; separating
  them would recreate independently valid conflicting cases.

## SWU-RRD-006 — Atomic Decision Acceptance

- Primary behavior: compare the complete DecisionValidationVector and atomically
  append one decision, consume one trigger, debit counters, allocate identities,
  and advance the frontier—or perform none of them.
- Dependencies: SWU-RRD-005 and resolved G1 owner prerequisite.
- Write scope: exactly `allowed-routes.json#rrd-l1-acceptance.write_scope`.
- Done: immutable migration/checksum discipline is preserved; journal idempotency
  and prerequisite semantics are reused; every vector member is compared inside
  the write transaction; failpoints cannot leave partial consumption/debit.
- Acceptance evidence: two writers from H0; rebuilt loser; policy/authority/
  deadline/permit revocation; failpoint after every internal step; process
  restart; database integrity and existing runtime regression.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_acceptance -v && python3 -m unittest discover -s implementations/tests/runtime -p 'test_*.py'`.
- Execution owner: local-fallback only after typed owner prerequisite.
- Split analysis: compare and append cannot be separate SWUs because the atomic
  boundary is the behavior being proven.

## Synchronization And Completion

- 006 cannot start from prose approval; its Task Session must carry the typed G1
  owner-prerequisite record and return to the same attempt.
- Any migration checksum drift or existing runtime regression blocks closeout.
- Task completion does not imply domain truth, effect, or ARE conformance.

