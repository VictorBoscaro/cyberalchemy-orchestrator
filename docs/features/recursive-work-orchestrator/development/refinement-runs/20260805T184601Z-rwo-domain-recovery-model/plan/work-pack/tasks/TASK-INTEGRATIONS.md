# TASK-INTEGRATIONS — Owner Seam Conformance

## Objective

Bind separately accepted domain, exact-effect, and optional ARE evidence to the
pure recovery model without reallocating owner authority. This task owns
SWU-RRD-007 through 009 and maps to S-003/L2/W3.

## Shared Rule

Each SWU is independently blocked until its named owner accepts an exact schema
version, producer, consumer, admission receipt, revocation/expiry behavior, and
negative substitution tests. Documentation resemblance is not conformance.

## SWU-RRD-007 — Domain Signal And Policy Admission

- Primary behavior: only domain/policy handles admitted by WorkDefinition-bound
  owners can enter CaseAssembler.
- Dependencies: SWU-RRD-005 and resolved G1.
- Write scope: exactly `allowed-routes.json#rrd-l2-domain.write_scope`.
- Done: mapping is total and pure; unsupported events block; handle binds owner,
  contract, exact input/output digest, epoch, and acceptance record; missing
  policy becomes OwnerGapCase only with an admitted escalation owner.
- Acceptance evidence: valid signal/policy; forged owner; stale epoch;
  substituted input; ambiguous mapping; absent policy; domain/journal mismatch.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_domain -v`.
- Execution owner: manual owner route followed by Task Session.
- Split analysis: signal and policy admission jointly define one domain-to-case
  seam; testing either alone cannot prove no permissive combination.

## SWU-RRD-008 — Exact Effect And Reconciliation

- Primary behavior: admitted exact-effect evidence distinguishes failed-known
  effect-attempt retry from outcome-unknown bounded reconciliation.
- Dependencies: SWU-RRD-006 and resolved G2.
- Write scope: exactly `allowed-routes.json#rrd-l2-effect.write_scope`.
- Done: permit nonce/expiry and exact intent bind; failed-known may allocate only
  an effect attempt; unknown may allocate only a stable reconciliation intent;
  reconciliation counter/deadline/exhaustion remain original-effect-scoped.
- Acceptance evidence: failed-known permit; revoked/foreign permit; unknown
  zero-retry; still-unknown remaining/exhausted; duplicated reconciliation trigger.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_effect -v`.
- Execution owner: manual exact-effect owner route followed by Task Session.
- Split analysis: retry and reconciliation must be tested together to prove
  mutual exclusion for the same effect posture.

## SWU-RRD-009 — Optional ARE Semantic Evidence

- Primary behavior: an admitted ARE semantic receipt may be referenced by the
  domain mapping, while raw/failed/absent ARE output never becomes case kind,
  disposition, authority, or a fallback call.
- Dependencies: SWU-RRD-007 and resolved G3; 008 is not required for pure
  semantic binding but is required before full L2 closure.
- Write scope: exactly `allowed-routes.json#rrd-l2-are-aci.write_scope`.
- Done: exact receipt schema/version and admission chain bind; zero-call path is
  first-class; caller cannot inject model text or bypass mapping owner.
- Acceptance evidence: admitted receipt; raw model output; ACI rejection;
  artifact admission missing; optional ARE absent; replay with zero ARE calls.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_semantic_evidence -v`.
- Execution owner: manual ARE/ACI owner route followed by Task Session.
- Split analysis: receipt binding and zero-call behavior are two sides of one
  optional evidence contract and cannot be accepted independently.

## Synchronization And Completion

- 007, 008, and 009 may run in parallel only after their prerequisites pass;
  their write scopes are disjoint.
- Full task completion additionally runs all L0/L1 suites and asserts zero
  external network/effect calls in fixtures.
- Owner acceptance receipts are evidence inputs, not copied authority.

