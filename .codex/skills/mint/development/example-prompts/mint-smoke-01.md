# Example: mint-smoke-01 — additions smoke test on a fresh domain

TASK-ID: mint-smoke-01
REGIME: smoke (single bounded emit + self-check; not the loop-first promotion regime)
GOAL: exercise the 13 committed additions on a domain OTHER than resonantos, and run §7 self-checks 1–9.

## The test `<DOMAIN>` spec (compact, deliberately non-economics/non-governance)
- `<DOMAIN>` = **tide-tables**
- objective sentence = "researches reproducible coastal tide predictions"
- governed subject = tidal predictions for a named coast
- primary source = the national tidal authority's published harmonic constituents
- proposal unit = a candidate tidal invariant (a condition a prediction must preserve)
- **domain-originated authority kind** = "prediction-provenance authority" — governs which harmonic-
  constituent dataset *version* a prediction derives from. cav2 has no analog; new owner route =
  `constituent-version-governance` (lexically AND owner-route new → passes F3(c)).
- separable concerns = raw observations vs. fitted constituents vs. published predictions
- one conflation to refuse = "a fitted constituent set is not an observed tide"

## What the run must produce (emit into the scratch target, NOT the repo)
Emit the additions-relevant spine for `tide-tables` following EMIT-PROCEDURE Steps 1–3 + 7–12:
- `authority/AUTHORITY-MODEL.md` (with the domain-originated kind PROPOSED + default-deny row + the #5 CLOSED declaration + #1 owner-routing + #2 derivation sections)
- `definitions/DEFINITIONS.md` + `DEFINITIONS-INDEX.md` + `DEFINITION-DRIFT-AUDIT.md` (#8)
- `authority/METHODS-CATALOGUE.md` (#13 — a methods block for prediction-provenance authority)
- `authority/decisions/<date>-mint.md` (propose) + `<date>-ratify-mint.md` (#11 — ratify, no kind left PROPOSED)
- `authority/AUTHORITY-POSTURES.md` (#3 — tide-tables' OWN postures, none of cav2's 8) + `authority/constitutions/CONSTITUTION-IMPORT-PACK.md` (#17 — no CAV2-C bodies)

## Then run §7 self-checks 1–9 and report PASS/FLAG/BLOCK per check, with the exact evidence (grep/inspection) for each.
