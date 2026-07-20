# Example: mint-smoke-02 — Universal Governance Baseline smoke test

TASK-ID: mint-smoke-02
REGIME: smoke
GOAL: exercise EMIT-PROCEDURE Steps 13–14 (the universal-governance-baseline addition) on the tide-tables
domain and run §7 self-checks #11–#13 + the D11/D31/D40 strip-binding greps.

## Domain: tide-tables (reuse mint-smoke-01 spec)
- domain-originated kind = "prediction-provenance authority" / owner route = constituent-version-governance.

## Emit (into scratch) following EMIT-PROCEDURE Steps 13–14
- `authority/constitutions/tide-tables-BASELINE-CONSTITUTION.md` (9 rule-baselines B1..B9, PROPOSED)
- `authority/BASELINE-PRIMITIVES.md` (18 primitive refs, PROPOSED)
- `authority/PROJECT-SPACE-ROLES.md` (D15 role format, tide-tables' own folders)

## Checks
- #11 four-facet: an emitted action-governing artifact declares the four facets or typed residue (or vacuous).
- #12 baseline-present: all 9 rules + all 18 primitive refs present.
- #13 baseline-no-leak: `grep CAV2` over the baseline files → only `(CAV2-D<k>)` tags; NO `authority_scope=CAV2`, NO cav2 space/consumer list.
- strip-bindings: D31 authority_scope = tide-tables (not CAV2); D11 no cav2 space list; D40 protocol only.
