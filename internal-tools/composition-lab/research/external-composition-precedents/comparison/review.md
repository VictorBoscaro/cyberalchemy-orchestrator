# Review — provisional external comparison

## Coverage

| reviewer | lens | targets attacked | result |
|---|---|---|---|
| independent comparison reviewer | fidelity to accepted owner maps | both owner maps and both acceptance reviews; `correspondences.md`; `transfer-skeptic.md`; `findings.md` | No source-owner claim was found to have been materially falsified or strengthened beyond its local account. |
| independent comparison reviewer | unsupported convergence and universalization | every claimed weak convergence, rejected transfer, candidate field, implication, and unknown in `findings.md` | One selection-conditioned recurrence is presented without the necessary corpus-construction caveat. No universal theory or formal-law transfer survives. |
| independent comparison reviewer | incompatibility and residue preservation | `correspondences.md`, T1–T8 in `transfer-skeptic.md`, and the synthesis sections on rejected transfers and unknowns | Material incompatibilities are preserved; emergence, associativity, identity, closure, decomposition, and recoverability remain unresolved or blocked. |
| independent comparison reviewer | citation completeness and epistemic provenance | all substantive paragraphs, bullets, table rows, and recommendations in `findings.md` | Claims are locally linked to inputs, but one input is repeatedly mislabeled as a review. |
| independent comparison reviewer | clarity and objectivity | full `findings.md` | The document is concise, direct, and explicit about its bounded authority apart from the two findings below. |

Lens coverage is complete for the declared target corpus. This review did not inspect or rely on the internal-repository research.

## `findings.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 1 | `comparison/findings.md` | “**Admissibility is relational:** every accepted account constrains a proposed combination through some relation…” and “**Failures help identify the operation:** … reveal different formation boundaries.” | MAJOR | State that these recurrences are **selection- and schema-conditioned**: the engineered map excluded a candidate for lacking a sufficiently explicit combining operation and required every admitted account to record operation, conditions, and failure/non-example; the formal map was collected under the same field-oriented question. Retain them as useful comparison constraints, but do not present their prevalence in this corpus as independent evidence of a cross-domain regularity. |
| 2 | `comparison/findings.md` | The synthesis repeatedly cites `transfer-skeptic.md` as “**transfer review**,” including “([…] [transfer review, T1–T8](transfer-skeptic.md))”. | MINOR | Rename these citation labels to “transfer-skeptic analysis” (or equivalent) and distinguish it from the two actual acceptance reviews. This preserves the input's adversarial role without implying a review-dispatch status it does not have. |

**Verdict:** FIX

## Other comparison artifacts

No independently verified CRITICAL or MAJOR finding survives against the two accepted owner maps, their reviews, `correspondences.md`, or `transfer-skeptic.md`. The correspondence matrix consistently limits rows to `partial analogy`, `vocabulary only`, or `unresolved`; the skeptic preserves operation, authority, preservation, evidence-stage, object-identity, and ordering incompatibilities.

**Verdict:** KEEP

## Change requests

1. **MAJOR** — Mark admissibility/failure recurrences as conditioned by the corpus admission criteria and collection schema, and separate their diagnostic usefulness from any empirical claim that they recur independently across composition domains.
2. **MINOR** — Relabel references to `transfer-skeptic.md` so they do not masquerade as an acceptance review.

## Final disposition

**FIX.** The synthesis is substantively cautious and well cited, but the MAJOR selection-effect omission must be corrected before its “surviving convergences” can serve as evidence for the next research design.

`exit_reason: resolved-with-change-requests`  
`agents_spawned: 0`

---

## Re-review — 2026-08-13

### Scope

Second independent pass over the corrected `comparison/findings.md`, using this prior review and only the previously authorized external inputs. Checks covered: placement and adequacy of the selection/schema caveat; separation of diagnostic constraint from empirical prevalence; claim downgrading; `transfer-skeptic.md` labels; new claims or concepts; citations; and preservation of incompatibilities.

### Corrections verified

- **Finding 1's substantive correction passes.** The synthesis now places “**Corpus-construction caveat:** the recurrences below are selection- and schema-conditioned” before any recurrence, identifies the formal inquiry and engineered admission/schema mechanisms, and says their recurrence “**is not independent evidence that these features prevail across composition domains**.”
- **Diagnostic use is separated from prevalence.** The two most selection-sensitive bullets now say “**in the admitted cases**,” label the result schema-conditioned, and restrict it to “**diagnostic use only**.” The remaining bullets are likewise bounded to “these accounts.”
- **The next-research implication is appropriately downgraded.** It now says the comparison fields test “**candidate constraints without presuming they are universal or independently prevalent**.”
- **Finding 2 passes.** All occurrences inspected use `transfer-skeptic analysis`; no surviving `transfer review` label was found.
- **No new external theory or universal mechanism was introduced.** The changes add a methodological limitation and narrower claim language. Rejected transfers, incompatible operation kinds, formal-law limits, emergence limits, and unresolved decomposition/residue remain intact.

### Surviving regression

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| R1 | `comparison/findings.md` | The frontmatter declares `inputs: accepted-owner-maps-and-bounded-comparison-only`, but the corrected synthesis now cites “**[comparison review, finding 1](review.md)**” in the caveat, two recurrence bullets, and implication 3. | MAJOR | Remove citations from `findings.md` to its own downstream `review.md`. Keep the caveat and downgraded wording, citing only the owner-map passages that demonstrate collection/admission conditioning (and the authorized comparison inputs where applicable). A review change request can cause a correction, but the review is not source evidence for the corrected research claim; citing it creates a circular dependency and contradicts the declared input boundary. |

### Re-review disposition

**BLOCK / FIX.** The original substantive findings are correctly addressed, but R1 must be removed before `findings.md` is accepted. No other finding survives this pass.

`exit_reason: resolved-with-one-regression-change-request`  
`agents_spawned: 0`

---

## Final narrow verification — 2026-08-13

### Checks

- **Zero downstream-review references:** `comparison/findings.md` contains no link or label referring to `comparison/review.md`.
- **Exactly two legitimate owner-map reviews remain:** the formal-account paragraph cites `../runs/formal-structural-owner-map/review.md`, and the engineered-account paragraph cites `../runs/engineered-systems-owner-map/review.md`. Both are the acceptance reviews for the owner maps they accompany.
- **Caveat remains directly supported:** the selection/schema caveat still cites the formal map's question and boundary plus the engineered map's source/search log and completion checklist—the passages that establish how the corpus was elicited and admitted.
- **No substantive regression:** the caveat still precedes all recurrences; diagnostic usefulness remains separated from empirical prevalence; claims remain bounded to admitted cases/accounts; `transfer-skeptic analysis` labels remain correct; rejected transfers and recorded incompatibilities remain unchanged.

### Final verdict

**PASS / KEEP.** R1 is resolved. No blocker or surviving change request remains within this verification scope.

`exit_reason: resolved`  
`agents_spawned: 0`
