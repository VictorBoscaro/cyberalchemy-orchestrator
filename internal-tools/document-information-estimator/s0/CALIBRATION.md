# P-GUARD calibration pass (OQ-AS6) — 2026-07-23

Owner calibration pass for the near-duplicate predicate's scale-invariant
companion (`--neardup-k`), closing OQ-AS6's outstanding recommendation
("a dedicated calibration pass before S1"). Read-only over the corpus — no
`.claude/skills/*` file was modified to produce this. Ground truth was built
by reading actual `SKILL.md` files in this repo, not fabricated.

## 1. The labelled set

**Positives — genuine cross-skill repetition**, verified by reading the
full body of each file:

- `ontology-view` / `system-view` / `engineer-view` (the `paired-views`
  triad): three hand-authored files sharing the same section skeleton
  (`<altitude>`, `<cross-reference-contract>`, `<quality-bar>`,
  `<anti-patterns>`, `<observability>`, `<promotion-gate>`), near-identical
  boilerplate sentences ("preserve seed status until live examples and
  Experiment Harness evidence support promotion"), and a deliberately
  cross-referenced single-owner discipline across all three — the clearest,
  strongest positive: authored on purpose, by design, to be structurally
  parallel.
- `sigil-maintenance-loop` / `observed-invocation-loop`: both
  `generated_by: tools/bootstrap_arcanum.sh --profile` "Composed Arcanum
  spell" stubs sharing the same generator template (`## Identity`,
  `## Trigger Conditions`, `## Required Sigils`, `## Execution Phases`,
  `## Observability`, `## Output Contract`).
- `whisper` vs `invoke` / `necronomicon`: same generator template family,
  fuller bodies, real shared phrasing beyond headers (Prerequisites, Shared
  State, Output Contract framing).

**Caveat found while labelling:** the "genuine" class is itself two
different phenomena gzip cannot tell apart — (a) the triad's deliberately
*authored* parallelism, and (b) shared *generator boilerplate* from
`bootstrap_arcanum.sh` that also appears in several files judged
"artifact" below (`discovery-to-inventory`, `implementation-readiness` are
structurally the same minimal "Composed Arcanum spell: X" stub class as
`sigil-maintenance-loop`). This ambiguity is itself evidence for the
ceiling stated in §4.

**Negatives — plainly unrelated skill pairs** (8, spot-read to confirm no
topical or template overlap): `commit-message`↔`necronomicon`,
`robot-talks`↔`feature-glossary`, `codex-goal-profile`↔`ux-evidence-validator`,
`emit-topic-tags`↔`repository-harness`, `craft`↔`whisper`,
`check-tension`↔`necronomicon`, `anti-bias-vector-composition`↔`repository-harness`,
`skill-decomposer`↔`repository-harness`.

**Artifact class** — the baseline (`k=1.0`, disabled) `protected` set minus
the positives: `repository-harness` (`A≈0.2500`, essentially at
`NEARDUP_TAU`), `ontology-harness` (`A≈0.2648`), `arcanum-bootstrap`,
`implementation-readiness`, `discovery-to-inventory`,
`publication-research-pipeline`, `observed-invocation-loop`, `necronomicon`
— read to confirm each has a low, near-`τ` `A(u)` and a large near-dup
partner list (`repository-harness` alone: 68/68).

## 2. Empirical characterization — `pair_B(u,v) / A(u)`

Computed with the shipped `pair_B` and `A` formulas (unchanged), via a
throwaway analysis script (`compute_A_B_delta` + `compute_pair_matrix`
imported from `assay_s0.py`, not re-implemented):

| Class | ratio range observed |
|---|---|
| Positive (labelled genuine) | 0.58 – 0.92 |
| Negative (labelled unrelated) | 0.88 – 0.96 |
| Artifact-class pairs (`A(u)≈τ`) | 0.66 – 0.96 |

**Finding: the ranges overlap.** There is no `k` such that
`ratio ≤ k` accepts every positive and rejects every negative/artifact —
paraphrase-heavy positives (`whisper`, ratio ≈0.83–0.92) sit inside the
negative range, and some artifact-class pairs (`implementation-readiness`↔
`arcanum-bootstrap`, ratio ≈0.66) sit inside the positive range. This
confirms and sharpens the discovery's existing note that `k≈0.85` only
trims the artifact marginally (12→11): a *single-pair* ratio threshold
cannot cleanly separate the classes on this corpus.

Because `protected_flag` is a *set*-level predicate (≥2 distinct qualifying
partners per unit, not a single pair), a sweep was run over the resulting
**protected-unit set**, not just individual pair ratios, at `k` from `1.0`
down to `0.59` in `0.005` steps. This surfaced a stable plateau at
`k ∈ [0.635, 0.69]` (0.695 exclusive — `repository-harness` re-enters at 0.695): the protected set is constant there —
`{discovery-to-inventory, engineer-view, implementation-readiness,
sigil-maintenance-loop, system-view}` (5 units) — a wider, non-fragile
window than the single-point `k≈0.62` where the set is briefly "3 units, 0
artifacts" (window width <0.005, too fragile to ship as a default).

## 3. Chosen default

**`DEFAULT_NEARDUP_K = 0.65`** (predicate unchanged:
`pair_B(u,v) ≤ NEARDUP_TAU AND pair_B(u,v) ≤ NEARDUP_K · A(u)`, both
required; `NEARDUP_TAU = 0.25` untouched).

Rationale:

- Sits mid-plateau (`[0.635, 0.69]`), not on a cliff edge — small corpus
  edits won't flip the result.
- Removes 6 of 8 artifact-class units, including the flagship over-trigger
  `repository-harness` (`A≈τ`, was near-dup of 68/68, now near-dup of 0).
- Keeps 3 of 5 labelled-positive units protected (`system-view`,
  `engineer-view`, `sigil-maintenance-loop`).
- `--acceptance` still PASSes: Assertion 2 (P-GUARD fires on body-identical
  `SKILL.md`↔`README.md` pairs) checks only the absolute `NEARDUP_TAU`
  clause, not the `k` companion, so it is unaffected by this change.

## 4. Honest ceiling — what gzip provably cannot catch here

- **`whisper` drops out.** Its overlap with `invoke`/`necronomicon` is
  paraphrase-level (ratio 0.83–0.92), indistinguishable by ratio from the
  unrelated-pair range (0.88–0.96). No `k` keeps `whisper` protected
  without re-admitting several artifact units.
- **`ontology-view` was never recovered, at any `k`, including `k=1.0`.**
  `pair_B(ontology-view, system-view) = 0.2536` and
  `pair_B(ontology-view, engineer-view) = 0.2574` both exceed the absolute
  `NEARDUP_TAU = 0.25` outright — this is a `pair_B` **asymmetry**
  (`ontology-view` is the floor the other two views *reference*, so it is
  less "explained by" them than they are explained by it), not something
  `NEARDUP_K` can fix without also loosening `NEARDUP_TAU` (out of scope:
  that threshold is pinned by discovery §3.4, not this pass).
- **Two retained units (`discovery-to-inventory`, `implementation-readiness`)
  are the same generator-template stub class as the kept-genuine
  `sigil-maintenance-loop`.** Whether their protection is "genuine" (shared
  authored template, defensible) or "artifact" (accidental boilerplate
  overlap) is a judgment call gzip cannot resolve — it measures bytes, not
  intent. This is precisely discovery §4's boundary: S0 measures
  redundancy, not cut-safety, and (per this pass) not even redundancy
  *kind*.
- **Net:** a compressor-only compound guard can suppress the worst
  low-`A` over-triggers but cannot reliably separate deliberate rule
  restatement from (a) generator boilerplate or (b) paraphrase. Both need
  the S2 LM kernel (`llmlingua.get_ppl`) to resolve, per discovery OQ-AS6's
  original recommendation. `protected` remains, as discovery §4 already
  states for the whole S0 map, advisory — now with a materially smaller
  and better-targeted false-positive set, not a solved one.

## 5. Reproduce

```sh
python assay_s0.py                        # uses the new default (k=0.65)
python assay_s0.py --neardup-k 1.0         # reproduces the pre-calibration (disabled) behavior
python assay_s0.py --acceptance            # S0 -> S1 gate, unaffected by k, still PASS
```
