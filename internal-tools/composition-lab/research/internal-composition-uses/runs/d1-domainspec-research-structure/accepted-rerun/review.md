# Independent review — D1 native rerun

## Verdict

**FIX.** The source bindings and final source integrity pass, and the findings are broadly traceable and appropriately bounded. Four localized wording corrections are required before this can be accepted as the first bounded internal lot. No new research is needed.

This review is a native bounded task. It is not a governed dispatch, has no ACI binding, and does not validate orchestration infrastructure.

## Authority and scope

- D1 identifiers were resolved from the exact D1 manifest entry only: repository `C:/Users/victo/domainspec-core`, revision `9bfec22712e4675d39c4cf1c21b36dc66614136c`, and the three path/byte/SHA-256 bindings below.
- Semantic review used only `source-receipt.md`, `findings.md`, the three bound D1 sources, and `research-program.md` lines 111–132 for contribution and gate limits.
- No prior `scout-return.md`, `audit.md`, or prior findings content was opened or used as authority or comparison. The rerun's prior-attempt statement is treated as a process declaration, not as source evidence.

## Recomputed bindings and final integrity

| Source | Bytes | SHA-256 | Scoped Git status | Result |
|---|---:|---|---|---|
| `projects/domainspec-v2/README.md` | 6246 | `ca5cfbc0a467e3f14e459236d373db4c046f428930c0fae7571246bfe0aeefff` | clean | PASS |
| `projects/domainspec-v2/research/TWO-LANE-DISCIPLINE.md` | 2575 | `cb09d2412e53288ae891ad6d1f03ff5d56c10808824bf0d7e025fc233cd93557` | clean | PASS |
| `projects/domainspec-v2/research/domainspec-v2-research-towers.dispatch.json` | 15381 | `83206a57f4ed8d05a1c623ede6db17ae058e74fcfdc184150d20f2f7096147fd` | clean | PASS |

`git rev-parse HEAD` returned the declared revision. The JSON parses and contains dispatch id `domainspec-v2-research-towers-20260611`, mode `research`, six steps, three gates, and seven configured trace-event names.

Before this review was created, scoped Git status for the rerun directory listed exactly two new files: `source-receipt.md` and `findings.md`. After creation, the only additional file is this reviewer-owned `review.md`. This establishes final scoped state and reproducibility; it does not purport to prove that no temporary write ever occurred.

## Coverage

- Sources: 3/3 read in full; every line was checked.
- Analytic units in `findings.md`: 60/60 checked, defined as all seven gate rows, 27 source-observation rows, five cross-source observations, four inferences, four hypotheses, five negatives/ambiguities, three limits, and five next-lot questions.
- Selectors: all 185 selector occurrences (109 distinct selector strings) were resolved against the frozen bytes; none points outside its source or beyond EOF.
- Status, scope, disposition, and prior-attempt declarations were also checked separately from source-derived claims.

## Critical-check results

| Check | Result | Evidence |
|---|---|---|
| Identity and authority | PASS | Revision, paths, bytes, hashes, and scoped cleanliness all recompute; receipt values match. |
| Source dependency | PASS | Every substantive source claim is traceable to S1–S3; linked artifacts are explicitly excluded. |
| Observation / prescription / configuration / execution / effect separation | FIX | The overall separation is strong, but the S2 evidence-state row overstates the whole document as “Prescription only.” |
| Negatives, absences, ambiguities | FIX | The configured-route negative is supported but one sentence is broad enough to read as a corpus-wide absence. |
| External theory, premature classification, causality, recommendation | PASS | None is incorporated; inferences and hypotheses are labeled and do not become recommendations. |
| Generalization beyond three sources | PASS | Limits repeatedly prohibit D1-external and corpus-wide conclusions. |
| Gate contribution and incompleteness | PASS | The findings explicitly mark lenses as not covered, skills as reference-only, interfaces as partial, and execution effects as absent. |
| Isolation from the prior attempt | PASS, declaration-bounded | No old content entered this review; the rerun records only a filename-existence check. The truth of its process history is not independently provable from final filesystem state. |
| Final source integrity and rerun outputs | PASS | All three source paths remain clean and bound; rerun additions are the two researcher files plus this review. |

## Verified change requests

### 1. Necessary capabilities are broadened to all v1 capabilities

- **Severity:** MAJOR
- **File/evidence:** `findings.md:44` says, “The README claims v1 capabilities are imported and reformulated into v2, with DROP items excluded.” S1:L7-L12 says only “the necessary capabilities” are imported and reformulated. S1 does not establish that every non-DROP v1 capability is imported.
- **Correction:** Replace the opening with: “The README claims necessary v1 capabilities are imported and reformulated into v2, and states separately that four DROP-verdict capabilities are never imported.”

### 2. The source counts DROP capabilities but does not name them

- **Severity:** MAJOR
- **File/evidence:** `findings.md:46` says, “The README names four DROP capabilities.” S1:L20 and S1:L80 state that there are four DROP-verdict capabilities but do not identify their names.
- **Correction:** Replace “names four DROP capabilities” with “states that four DROP-verdict capabilities are never imported.”

### 3. S2's evidence-state label is too categorical

- **Severity:** MAJOR
- **File/evidence:** `findings.md:62` says, “Prescription only.” S2 is principally normative, but it also self-identifies its status/date (S2:L1-L4), supplies illustrative alternatives (S2:L25-L27), and asserts a rationale about anchoring (S2:L29-L30). Those are not execution or observed effects, but “only” erases their distinct textual roles.
- **Correction:** Use: “Normative project convention with illustrative examples and an asserted rationale; no execution is recorded and no effect is observed.”

### 4. Two negative boundaries need explicit referents

- **Severity:** MINOR
- **File/evidence:** `findings.md:27` says, “Artifact contents ... are not covered,” although S1–S3 are themselves artifact contents. `findings.md:107` says no “produced output” is evidenced, while the intended referent is the configured route, not every DomainSpec activity mentioned by S1.
- **Correction:** Change line 27 to “Contents of the referenced route outputs and actual knowledge preservation are not covered.” Change line 107 to begin “No executed run of the configured route, spawned agent for that route, emitted trace, completed receipt, or produced route output ...”.

## Gate contribution

After the four edits, D1 can enter as the first accepted **bounded, partial** internal finding set. It contributes direct evidence for DomainSpec v2, declared/configured workflows, artifact handoffs and authority boundaries; partial interface evidence; and explicit negative execution status and uncertainties. It does not satisfy the program exit condition by itself: lenses are absent as an explicit unit, skills are reference-only, runtime behavior and effects are unobserved, and no cross-line or general claim is authorized. The program's deferred gates remain unresolved.

## Terminal verdict

**FIX — four localized corrections; no new research required.**

## Re-review — 2026-08-13

**PASS / KEEP.** This narrow re-review applies to the corrected `findings.md` and supersedes the initial `FIX` as the current disposition. No finding survives.

| Prior change request | Re-review result | Evidence |
|---|---|---|
| Necessary capabilities were broadened | PASS | The text now says “necessary v1 capabilities,” matching S1:L9-L10, and separately reports the four DROP-verdict capabilities from S1:L20 and S1:L80. |
| DROP capabilities were said to be named | PASS | The text now says the README “states that four” exist; it no longer implies that their identities are enumerated. |
| S2 was labeled “Prescription only” | PASS | The revised row distinguishes normative convention, illustrative examples, asserted rationale, execution, and observed effect, with selectors expanded to S2:L3-L8, S2:L25-L30, and S2:L40-L50. |
| Negative referents were ambiguous | PASS | The artifact-content boundary now refers to “referenced route outputs”; the execution negative now refers to the “configured route” and “route output.” |

The edits narrow or classify existing claims; they introduce no new source object, execution claim, effect, causal relation, recommendation, or generalization. The non-governed declaration remains explicit at `findings.md:5`, and the partial-gate limits remain explicit at lines 7, 29–30, and 116–117.

The receipt remains 1,702 bytes with the same repository, revision, paths, byte counts, hashes, scoped-clean declarations, and non-governed boundary. The three sources remain at revision `9bfec22712e4675d39c4cf1c21b36dc66614136c`; all three byte counts and SHA-256 values still match, and scoped Git status is clean. Final-state verification supports integrity and reproducibility only; it does not claim that no temporary write occurred.

**Current terminal verdict: KEEP — accepted as one bounded, partial internal lot; the program gate remains unresolved.**
