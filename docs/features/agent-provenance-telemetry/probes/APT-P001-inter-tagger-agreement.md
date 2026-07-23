# APT-P001 — Inter-tagger agreement

## Claim under test

Two informationally isolated agents given the same immutable task bundle produce measurable overlap and divergence
that can support an attributable multi-perspective lens. Low agreement does not make emissions
worthless or refute a lens; it refutes treating their intersection as a shared classification.

## Method

1. Use the 12 shared fixtures from the probe registry.
2. For each fixture, launch two isolated taggers with identical task/context bytes, no peer output and
   the same output schema. Counterbalance seat order; do not tell either agent that agreement is the
   target.
3. Freeze a seed registry independently of these fixtures, but do not show its labels or suggestions
   during the primary free-emission phase. Ask each tagger for the topics materially needed to
   understand or execute the task. Seal both emissions before either output is revealed.
4. Normalize free terms mechanically, then resolve them through the pinned seed registry in a separate
   system projection. Do not merge synonyms or let a parent repair emissions.
5. For each fixture compute Jaccard separately for exact normalized free terms and resolved tag IDs:

   `J(A,B) = |A ∩ B| / |A ∪ B|`.

   A joint empty pair is `joint_abstention`, excluded from the median and reported separately; it is
   never scored as perfect agreement.

6. Report both medians, interquartile ranges, zero-overlap and joint-abstention counts, tag-count
   distribution and raw common core for each fixture. Never pool free-term and resolved-ID metrics.
7. With a pinned random seed, permute one seat across different fixtures and compute chance/baseline
   medians separately. Report `agreement_lift_free` and `agreement_lift_resolved`, each equal to its
   paired median minus its permuted median. These are diagnostic and cannot replace the preregistered
   absolute thresholds.

## Preregistered decision

- **Refutes shared classification (takes precedence):** resolved-ID median `J < 0.25`, at least 5
  fixtures have zero overlap, or more than 2 fixtures are joint abstentions.
- **Supports shared navigation:** otherwise, resolved-ID median `J >= 0.50`, at most 2/12 fixtures have zero overlap and
  `agreement_lift_resolved > 0`.
- **Lens-with-divergence:** every remaining valid result. Preserve tags
  per agent and test whether APT-P007 can represent their stable complement; do not aggregate them into
  a canonical dispatch classification.

These are pilot engineering thresholds, not universal epistemic constants. They may be changed only
before the first run and with a version bump.

## Falsifiers and invalid runs

- Any tagger sees the other's output, prior tags or original agent identity.
- The seed registry is derived from or changed after seeing these fixtures.
- A human or model performs synonym merging before the primary metric.
- Input or prompt digests differ within a pair.
- Missing emissions are deleted instead of recorded as missing observations.
- Free and registry-assisted selections are combined in one agreement metric.

## Output

Raw paired snapshots, normalized sets, per-fixture metrics and a decision record referencing exact
digests. No vocabulary mutation is an output of this probe.
