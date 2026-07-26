# Reconciled placement table — post-crosstalk

Assembled by the parent from the three seats' crosstalk contributions. Pre-crosstalk baseline is
bound by `workflow/crosstalk-turn-0.json`. This document is the input to the second-review pass.

## Parent convergence check (final_approver obligation 2)

Diffed against the three bound pre-crosstalk tables. **No row became unanimous during crosstalk
without a marked DRIFT.** Two DRIFTs were declared, both by S-A, both naming their mover and the
argument that moved them:

- **I5, S-A: MOVE → STAY.** Moved by S-C's finding 2. Ground: `experiment/SKILL.md` lines 49-50 is
  a definition of the dispatch type, not a placement rule — it proves the label false but licenses
  no eviction. S-A applied its own standing rule ("a rule I cannot quote does not exist for my
  purposes") against itself.
- **I8, S-A: MOVE → STAY, label only.** Moved by S-C. The object is an absence; neither token
  describes it. Substance unchanged.

**The seats crossed rather than collapsed on I5:** S-C moved STAY→MOVE at zig-zag round 2, S-A moved
MOVE→STAY at crosstalk. A converged trio does not produce opposing drift on the same row. S-B
declared no drift on any row and held all nine after engaging.

Residual convergence risk carried, not closed: the fluency-capture channel named by check-tension
round 4 (S-A runs the strongest model on the normative angle). Mitigated here by the fact that S-A's
only two drifts moved it *away* from action, toward the weakest-model seat's position.

## Reconciled table

| item | object | reconciled verdict | destination | status |
|---|---|---|---|---|
| I1 | `experiments/skill-relationship-graph/` | **STAY** | — | Unanimous pre-crosstalk on three independent grounds: rule-absence (S-A), live runtime read (S-B), stay-debt 0 (S-C). Parent-verified: `implementations/server/control_center/service.py:101` and `implementations/fixtures/skill-control-center/build_fixtures.py:63` read `graph.json` at runtime. Moving it breaks executing code. |
| I2 | `experiments/skill-control-center/` | **MOVE out of `experiments/`** | `docs/features/skill-control-center/`, subfolder names preserved as direct children | Unanimous that it leaves `experiments/` (it has no `criterion.md`, so it is not an experiment). **SHAPE CONTESTED** — see residue 1. |
| I3 | `.../research/review/review.md` | **MOVE with I2's `research/`**, plus repair 3 dangling links | `docs/features/skill-control-center/research/review/review.md` | Substantive 3/3 (S-C's STAY label is "relocates with I2" by its own text). Parent-verified: 3 dangling `research-review/` links at `control-center.md` lines 29, 559, 617. |
| I4 | `.../implementation/final-review.md` | **RENAME to `review.md`** (warrant unanimous, zero cost) + move; **DESTINATION CONTESTED** | see residue 2 | `.claude/skills/review/SKILL.md` line 25 mandates the single name; the pre-2026-07-13 exemption covers only `attacks.md`/`findings.md`. |
| I5 | `experiments/foodstogo-jbp-2025/` | **CONTESTED 2 STAY / 1 MOVE** after crosstalk; no seat produced a licensed destination | — | See residue 3. All three agree the directory name asserts a provenance the tree lacks. |
| I6 | the six dated review rounds under `docs/features/*/reviews/` | **STAY** | — | Unanimous pre-crosstalk. Parent-verified: `implementations/tests/runtime/test_orchestration_bridge.py:150-156` and `test_host_dispatch_hook.py:37-43` `.read_text()` a hardcoded path into `reviews/2026-07-23-stage-a-freeze/` at test-run time. Moving breaks tests. |
| I7 | `docs/features/agents-communication-infra/experiments/` | **STAY** | — | No seat proposes a move. S-B records `bus-publication-probe/` lineage as *unproven* rather than affirmed; that epistemic difference is preserved, not folded into a three-way confirmation. |
| I8 | `experiments/` absent from root `README.md` | **Add the row** (verdict token cosmetic) | `README.md` navigation table | Substantively unanimous from the start. The row must describe `experiments/` accurately, including that its entries are not uniformly governed experiments. |
| I9 | `research/artifact-placement-adjudication/` | **STAY** | — | Unanimous. No seat claimed an exemption for this dispatch's own output. |

## Residue — unreconciled dissent, for the parent

**1. I2 shape.** Whole-tree (S-A, S-C) vs split, sending `implementation/` + `agent-runtime/` toward
`implementations/` (S-B).
- S-B's evidence, parent-verified: 7 of 10 files in the disputed subtree self-declare
  `implementations/` paths as their own write-scope in their own text — all four `agent-runtime/`
  files plus `backend-context-pack.md`, `backend-task-session.md`, `frontend-task-session.md`.
- S-A's counter, parent-verified: commit `64b028d` contains **nine** files, and S-B cited a subset.
  The omitted row is `docs/features/skill-control-center/BACKLOG.md` — so the commit couples the
  disputed file with the feature package *and* the runtime in one act, discriminating between
  neither. Reference-absence is symmetric: zero from `docs/` into the subtree, zero from
  `implementations/`+`tests/` back.
- S-A's second counter: `implementations/README.md` lines 1-9 charters that directory as a runnable
  read-only control plane; `find implementations -name "*.md"` returns three files, all operational
  contracts, no build record. S-B concedes the exact subfolder is unproven.
- S-C's count: **zero markdown links cross the split line**, so both shapes cost ~20 edits. Cost is
  indifferent; it declines to fake a tiebreak. Extra cost of the split: two `git mv` destinations
  instead of one, plus minting a build-record convention where no precedent exists.

**2. I4 destination.** Three candidates: `docs/features/skill-control-center/implementation/review.md`
(S-A, on the rule that the declared `working_folder` governs where a review lands), `implementations/`
with subfolder unproven (S-B, on self-declared write-scope), inside the relocated I2 tree (S-C, which
withdrew its preference as never independently counted). Cost is 0 link edits at all three.

**3. I5.** S-B holds STAY (weakly, 1-vs-2, self-flagged low-confidence: `git grep` finds zero external
references to foodstogo anywhere in the repo, so no lineage points elsewhere; `4e69b2f` is the owner's
own placement act). S-A drifted to STAY on the ground that its rule licenses no eviction. S-C holds
MOVE with the only counted cost (2 file edits) and the listing-level legibility argument. S-A
explicitly rejects S-C's `cases/` destination as the same unlicensed minting it just refused for
itself; S-C flags `cases/` unvalidated.

**4. I6 artifact-shape defect (S-A, engaged by neither other seat).** Three post-2026-07-13 rounds
persist `REPORT.md`/`BASELINE.md`/`FINAL-BASELINE.md`, and `2026-07-23-stage-a-freeze/` contains no
`review.md` at all — against `.claude/skills/review/SKILL.md` line 25 and standing rule 5. This is an
artifact-shape defect in the correct home, **not** a placement defect, and the remedy is constrained
to be additive because that directory's path is load-bearing for executing tests. Must not be
silently folded into I6's STAY row.

**5. I7 reason divergence.** Verdicts align, grounds do not. S-A binds both subfolders by the
ownership rule; S-B can evidence only `skill-protocol-compilation/` and defaults on the other. The
row must not read as three independent confirmations.

**6. I2 destination naming (S-A vs S-C).** `research/` as a direct child of the feature package,
cited to `.claude/skills/research/SKILL.md` line 167 (`docs/features/<feature>/research/<dispatch-slug>/`),
versus S-C's invented `work-record/` parent. The citation is one-sided; S-C called the name the
parent's call.

## Cost-axis carry (final_approver obligation 3)

Neither second-review seat guards the cost pole. S-C's surviving cost objections, carried here so the
parent cannot drop them unanswered: (a) I6 STAY is backed by real code breakage in two test files —
strongest-evidenced row in the dispatch; (b) I2 whole-move is cheaper than the split by ~2 edits and
one naming decision, a thin margin S-C itself called weak; (c) I4 is cost-indifferent across all
three destinations; (d) I5's move costs 2 file edits, one of which (`README.md`) I8 obliges anyway;
(e) every move must repair inbound links in the same commit so no intermediate state dangles, and the
whole step must be revertible in one operation.
