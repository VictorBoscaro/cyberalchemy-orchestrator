# APT-P007 — Emergent multi-agent lens

## Amendment status

Added after discovery v0.1.0 when the owner chose a system-governed tag registry and isolated
per-agent emissions. It is preregistered before any probe execution or result inspection. This version
incorporates two independent pre-run reviews that rejected the original unequal-information baselines.

## Claim under test

A deterministic projection over sealed, informationally isolated topic emissions produces a useful,
attributable organization of shared subjects and lexical differences beyond an equally informative
seat-by-tag view.

“Emergent” means the lens is not directly authored by any seat and appears only after the system
projects sealed emissions. It does not mean statistical independence, objective ontology, hidden
structure or substantive consensus. The first lens represents tag presence only; it does not encode
intensity, negation, qualification, use, criticism or rejection.

## Preconditions and variants

P007 runs only after P001–P004 disposition the seed registry and cadence:

- if P003 rejects canonical resolution, all conditions use normalized free terms plus residue;
- if P002/P004 choose close-only capture, temporal drift is removed from every condition and claim;
- same-model, cross-model and cross-profile seat compositions are separate strata and are never pooled
  into one independence claim.

The seed registry is frozen independently of the fixtures. All compared projections use identical
sealed emissions, resolutions, provenance references and registry version.

## Compared projections

- `B0 — incidence`: canonical `seat × tag/term` matrix with counts, residue and supporting emission
  references; no interpretive grouping.
- `B1 — grouped`: per-seat lists plus a support-count-sorted global list, with the same counts, residue
  and references; no `shared_core` or `perspective` labels.
- `L1 — lens`: the same information organized as thresholded shared core, per-seat perspectives,
  optional temporal drift, residue and supporting emission references.

The conditions vary organization only. Union/majority summaries that discard provenance may be
reported as descriptive anti-baselines, but cannot license the comparative utility claim.

Every projection must round-trip to the identical canonical relation
`seat × activation × tag/term × count × emission_ref`. A missing or additional tuple invalidates the
utility comparison. Every rendering states `interpretation_limit: tag_presence_only`; opposed-position
loss is reported as an explicit boundary observation, outside the lexical utility claim.

## Gold tasks and labels

Before producing `B0`, `B1` or `L1`, two annotators independently inspect the immutable task bundle,
complete work artifacts and sealed emissions. They label:

1. exact subjects shared by seats;
2. seat-specific lexical emphases material to reconstructing who addressed what;
3. unresolved terms;
4. same-tag/opposed-position cases where tag presence loses substantive divergence.

The annotation unit, rubric and disagreement rule are frozen before projection. Inter-annotator
agreement is reported; disagreements are adjudicated by a third blinded annotator. If agreement falls
below the preregistered floor of Cohen's `kappa = 0.60`, perspective-utility results are unresolved.

## Method

1. Use the 12 shared fixtures with at least three isolated seats per fixture and the composition strata
   above. A seat never sees another seat's current-round emission before sealing.
2. Build `B0`, `B1` and `L1` from the same canonical input manifest.
3. Round-trip each projection back to the canonical relation and require byte-identical tuples.
4. Test replay determinism twice in fresh processes and test enumeration invariance by permuting seat
   and observation order.
5. Test sensitivity with leave-one-seat-out and bootstrap resampling. Report shared-core Jaccard,
   perspective-set Jaccard and residue-set Jaccard with 95% bootstrap intervals. This measures sample
   stability; replay equality alone does not.
6. Assign every fixture × projection to evaluators using a balanced incomplete-block design so each
   projection is evaluated equally often per fixture and evaluator effects can be estimated. Formatting
   and names are blinded; at least three evaluator judgments are collected per fixture × projection.
7. Evaluators answer fixed questions about shared subject labels, who emitted which lexical emphasis,
   unresolved terms and traceable support. Score against the frozen gold labels.
8. Report:

   - relation round-trip equality, replay equality, enumeration invariance and support-reference completeness;
   - shared-subject precision/recall;
   - seat-perspective precision/recall;
   - residue precision/recall;
   - opposed-position loss count;
   - unsupported-element count;
   - evaluator time, confidence and error rate;
   - verbosity concentration: maximum fraction of displayed elements attributable to one seat;
   - leave-one-seat-out and bootstrap stability by composition stratum.

## Preregistered decision

- **Structurally valid:** 100% relation round-trip equality, replay equality, enumeration invariance and support-reference
  completeness, with zero unsupported elements. Failure of any item refutes the current contract.
- **Supports L1 lexical utility:** structural validity passes; gold-label `kappa >= 0.60`; L1 lexical-perspective
  recall is at least 0.80 and at least 0.10 above both equally informative baselines; L1 does not lose
  shared-subject or residue recall by more than 0.05 versus the best baseline; and median evaluator time
  is no more than 20% slower than the faster baseline.
- **Sample-stable core:** median leave-one-seat-out shared-core Jaccard is at least 0.70 and the lower
  95% bootstrap bound is at least 0.50 within each claimed composition stratum. This licenses only the
  shared-core stability claim; perspective/residue stability are reported separately.
- **Narrow lens:** structural validity passes but a utility or stability threshold fails. Retain the
  incidence relation and provenance; do not promote L1 as default UI or call its core stable.
- **Refutes current lens contract:** structural validity fails or L1 is worse than both equivalent
  baselines on perspective recall.

## Falsifiers and invalid runs

- A seat sees a peer's current-round emission before its own is sealed.
- Conditions receive different emissions, resolutions, provenance or registry versions.
- Gold labels or materiality rubric are changed after projections or results are visible.
- Fixture × projection assignment is unbalanced or evaluators can infer projection identity from labels.
- A semantic mapper rewrites raw terms or drops residue.
- Same-tag/opposed-position fixtures are presented as semantic consensus without a loss marker.

## Output

Pinned emissions, resolutions, registry and projection manifests; canonical projection bytes;
pre-projection gold labels and agreement; balanced evaluation assignments; replay, stability and
utility metrics by composition stratum; and a disposition of `supports-l1`, `narrow-lens` or
`refuted-current-contract`.
