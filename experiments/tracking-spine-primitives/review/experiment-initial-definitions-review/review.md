---
tags: [experiment, review, criterion, validity, anti-bias]
node_type: review
is_session: false
status: complete
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
authority: proposal-only
reviews: experiments/tracking-spine-primitives/criterion.md
reviewed_version: 0.1.0
review_kind: independent-parallel-opposed-angles
reviewers: 3
verdict: DO-NOT-FREEZE
---

# Review — Tracking Spine Primitives criterion v0.1.0

Three independent reviewers, run in parallel and blind to one another. Angles were structurally
opposed rather than merely distinct: **A** prosecuted "this criterion cannot fail", **B** prosecuted
the opposite pole of the same axis, "this criterion cannot pass", and **C** ran orthogonal to both,
assuming internal validity and attacking decision value and routing.

**Verdict: DO NOT FREEZE.** A returns INVALID-by-design on the count arm; B returns no; C returns
replace.

## 1. Convergence

Five defects were found independently by reviewers whose angles were opposed. Convergence under
opposed angles is the strongest signal this review produced, and these should be treated as
established rather than as claims:

| Defect | Found by |
|---|---|
| The hypothesis is quantified per-link; the verdict rule counts a union across the sample. They are different claims and only one is written twice. | A, B |
| The threshold of six is unsourced, and no downstream artifact branches on the cardinality of the constituent set. | A, B, C |
| `experiment-initial-definitions.md` violates its own Boundaries by proposing a rival method and naming counterexamples — and the criterion then imports that leakage as its own open question. | A, B |
| "Expression" — the probe's central artifact — is never defined or pre-registered, which voids the stated confound mitigation. | A, B |
| The criterion carries no record of the design-time validity gates the experiment skill requires before freeze. | A, B |

## 2. The defects that kill the design

**`NECESSARY` has no evidence path (A).** The probe records used subsets and omission reasons;
nothing in that record establishes "cannot be expressed without." The only mechanism that creates a
`NECESSARY` is a failed omission reason. So a probe that uses all eleven constituents on every link
omits nothing, produces zero failed reasons, and yields `NECESSARY = 0 ≤ 6` — SURVIVED, certifying a
vocabulary of at most six from a run in which all eleven were used.

**The count arm cannot reach seven (A).** The sample's unit is a two-endpoint link, and five or six
of the eleven describe dispatch machinery no two-endpoint relation can require. Three of those are
additionally defined in terms of other constituents, so they are excluded by the definition table
before any artifact is opened. The honest ceiling is five or six; the threshold was set at six.

**The inexpressibility arm is closed by construction (A).** `edge` is defined as a typed directed
relationship between two endpoints, and the sample is drawn from link relationships. A link that is
not an edge cannot be sampled, so "cannot be expressed at all" is unsatisfiable for four of the five
strata.

**The S5 fallback falsifies outside the hypothesis's own quantifier (B).** The hypothesis ranges
over *instantiated* links; the fallback constructs cases that carry no link today and lets them
trigger FALSIFIED. The criterion can return FALSIFIED while the hypothesis is true.

**The rule would misclassify the one reduction already earned (C).** The repository has already
established that a group carries no membership list because its members are derivable. Under this
rule, any sampled link relating an emission to its group scores `group` as NECESSARY — the
instrument rules "primitive" on the constituent the repository has already shown is a view. A scale
that disagrees with a result the owner already holds cannot move a decision.

**All three verdicts terminate in the same next action (C).** SURVIVED, FALSIFIED-by-count and
FALSIFIED-by-inexpressibility all end in "author a transition set"; only the arity of a list already
in hand changes, and no artifact's content differs at six versus eight.

**Wrong row of the repository's own routing table (C).** Every item in the Known Gaps is an
unsettled-architecture item, which the operating rule routes to discovery authoring. The criterion
then removes exactly those from scope as non-goals. Boundedness was manufactured by deleting the
unsettled architecture and pre-registering the countable residue — the evidence state never changed.

## 3. Two factual errors in the authored documents

Both were found by inspection of the repository, and both cut against the documents that contain
them:

1. **The claim that the eleven names were "never assembled into one list" is false (A).**
   `docs/features/agent-provenance-telemetry/specs/glossary.md` carries a versioned 60-row concept
   registry for this domain, including typed link entities the eleven-name list flattens or misses.
   Because the count is bounded at eleven by construction with no twelfth slot, drawing the list from
   the essays alone caps the reachable count — the criterion's own open question about that bias is
   answered, and the answer is yes.
2. **The claim that the `subplans/` → `plans/` migration is "visible in version history" is false (B).**
   It is an uncommitted working-tree change. Two live dangling references exist right now, in the
   root Plan's child registry and in the essays index. S3 remains populable from other committed
   renames, but not from the evidence the document cites.

## 4. What survived attack

Recorded because it was attacked deliberately and held:

- **Non-goals is disciplined (A).** Six exclusions, each removing a real second claim, keeping the
  hypothesis to one.
- **The discrimination check is not tilted toward SURVIVED (A).** It says FALSIFIED teaches more and
  correctly identifies inexpressibility as the highest-value observation available.
- **The sampling is severity, not rigging (B).** B was assigned the rigged-sample charge and could
  not make it stick: deliberately including the strata that can falsify is severity, and a sample
  avoiding them would be the actual defect. Under an existential necessity rule, stratum sizes are
  inert, so a differently-stratified sample would not reach the opposite verdict.
- **The confound section names the right risk unprompted (A, B).** Author-chooses-the-expression is
  the principal internal-validity threat, and separating adjudicator from author is the right
  instinct. The defect is that it was left in prose rather than promoted to a rule, and that the
  adjudication clause ratchets in one direction only.
- **S4 and S5 earn their place (C).** Expressing a link that does not exist yet, before the spine is
  designed, guards against fitting a spine to whatever artifacts it happened to encounter.
- **Pre-registration is not decoration here (C).** In a repository with a documented habit of
  assembling name-lists by inspection and then defending them, freezing the list before looking is
  cheap discipline that pays.

## 5. The cheapest alternative offered

From C, and it is concrete: take one already-documented failure — the two out-of-enum close rows
that hold the engine constitution's single-writer rule at medium veracity and block Front 3 — and
attempt one expression of *this row → the activation that wrote it → its trail* using only the
eleven names. If it expresses, the vocabulary is adequate and you have a worked example plus a real
trace. If it does not, the missing primitive is located against a failure the owner already treats
as blocking. One construction, one page, no strata, no second adjudicator.

This is the repository's own precedent: its candidate kernel invariants were attacked by countermodel
— a Lean probe finding rootless cycles — not by measurement.

## 6. Open Questions

- Does the countermodel route need a governed dispatch at all, or is it parent-inline work?
- Do the two subsidiary architecture questions — context as classification or composition, links
  between files or identity-bearing objects — get answered before or after the countermodel?
- Does the 60-row concept registry supersede the eleven-name list, or are they at different
  altitudes and both needed?
- The three reviewers converged on five defects from opposed angles. Is that convergence evidence of
  real defects, or evidence that all three share a base model's blind spots? The repository's own
  anti-bias thesis says opposed angles reduce correlated error without eliminating it, and no
  measurement here separates the two.
