# TASK-CONTRACT — Pure Recovery Contract

## Objective

Make candidate-2 mechanically falsifiable without persistence, owner services,
ARE, or effects. This task owns SWU-RRD-001 through 004 and maps to S-001/L0/W1.

## Source Contracts

- `../../../stages/08-distill-repair.md`, sections 2–9
- `../../../stages/08-scenario-matrix.json`
- `implementations/server/runtime/canonical.py`
- `implementations/server/runtime/errors.py`

## Dependencies And Gaps

- W0 must pin the current canonical profile ID/version/digest and test baseline.
- No G1–G4 owner decision is required.
- The task cannot edit journal/database, current ontology, ARE, or adapters.

## SWU-RRD-001 — Canonical Recovery IDs

- Primary behavior: equal admitted recovery objects produce one byte-identical,
  object-kind-separated ID; invalid canonical values reject.
- Dependencies: W0 only.
- Write scope: exactly `allowed-routes.json#rrd-l0-canonical.write_scope`.
- Done: wrapper delegates payload bytes to `aci.canonical-json@1`, frames kind
  and length, excludes declared self-fields, and rejects unknown kind/profile.
- Acceptance evidence: golden vectors for every object kind; two kinds with the
  same payload have different IDs; NFC equivalents converge; floats and
  out-of-int64 values reject.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_canonical -v`.
- Execution owner: local-fallback via Task Session.
- Split analysis: wrapper without vectors is unproven; vectors without wrapper
  have no executable owner. Retain together.
- Handoff: no caller integration and no new general canonicalizer.

## SWU-RRD-002 — Closed Case Admission

- Primary behavior: exactly the eight candidate-2 case variants pass structural
  admission and every invalid/unknown/cross-family shape rejects.
- Dependencies: SWU-RRD-001.
- Write scope: exactly `allowed-routes.json#rrd-l0-case-contract.write_scope`.
- Done: trigger and case schemas are closed; conflict enters through `pass`;
  owner-gap sentinels are typed; impossible combinations and unknown versions
  reject; owner admission is an explicit validator input.
- Acceptance evidence: at least one positive per variant; negatives for missing
  owner admission, effect-unknown without attempt-start, cancellation without
  terminal fact, extra property, foreign run, and malformed fence.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_contract -v`.
- Execution owner: local-fallback via Task Session.
- Split analysis: schema and admission validator implement one closed-boundary
  behavior and cannot pass independently.
- Handoff: do not add permissive unknown variants or fallback mappings.

## SWU-RRD-003 — Pure Single-Valued Classifier

- Primary behavior: one admitted case/frontier pair produces exactly one valid
  treatment candidate or one previously accepted reference.
- Dependencies: SWU-RRD-002.
- Write scope: exactly `allowed-routes.json#rrd-l0-classifier.write_scope`.
- Done: ordered algorithm, case tables, reason/disposition pair validation,
  terminal-before-continuation, and no EffectCase/Work-retry crossing exist as
  pure code with zero mutable/external calls.
- Acceptance evidence: all 20 Stage 08 scenarios plus totality/non-overlap
  fixtures; every unknown enum rejects.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_classifier -v`.
- Execution owner: local-fallback via Task Session.
- Split analysis: per-case modules could pass while precedence collisions remain;
  total classifier behavior is the smallest acceptance boundary.
- Handoff: policy and owner inputs remain immutable fixtures, not lookups.

## SWU-RRD-004 — Identity Transitions And Stable Intents

- Primary behavior: materialize the exact preserve/allocate/debit transition for
  a valid treatment without executing it.
- Dependencies: SWU-RRD-003.
- Write scope: exactly `allowed-routes.json#rrd-l0-identity.write_scope`.
- Done: all thirteen dispositions validate against the identity matrix;
  effect retry preserves Work Attempt; compensation and reconciliation intents
  are stable under re-observation; resume/stale/terminal allocate nothing.
- Acceptance evidence: one positive per disposition and collision negatives
  for delivery-vs-Work, Work-vs-effect, and duplicate compensation identity.
- Validation: `python3 -m unittest implementations.tests.runtime.test_recovery_identity -v`.
- Execution owner: local-fallback via Task Session.
- Split analysis: individual transitions are not independently safe because the
  invariant is mutual exclusion across the closed disposition set.
- Handoff: outputs are proposed transitions with `authority_effect: none`.

## Synchronization And Completion

- Execute sequentially: 001 -> 002 -> 003 -> 004.
- Each closeout updates only its exact execution receipt.
- Task completes only when all four targeted suites and the existing runtime
  suite pass, `git diff --check` is clean, and no forbidden source was touched.

