# S-C (Boehm, Barry) — angle: the cost of the move binds — round 2, FINAL pre-crosstalk position

## Response to review

**Finding 1 (I2 pointer = 0% compliance) — CONCEDE.** Re-priced honestly: the pointer buys navigation, not co-location; against `docs/features/README.md:16-17` it scores compliance 0%. With the stay-debt now priced (below), the counted move cost — 4 files, ~20 mechanical ref edits — is smaller than a permanent standing violation. Verdict flips to MOVE.

**Finding 2 (I5 disclaimer invisible at point of failure) — CONCEDE.** The failing reader scans `ls experiments/` (3 entries, verified) and never opens the disclaimer file. I had already recorded that cost cannot carry a veto here if the name asserts false provenance; the remedy must act at listing level. Verdict flips to MOVE. Counted move cost: 1 `.gitignore` edit (line 39) + 1 README table row (a row I8 obliges anyway) = 2 file edits, zero inbound markdown links.

**Finding 3 (CRITICAL — debt of staying unpriced) — CONCEDE, and the price is now in the ledger.** Erosion priced by count: `ls docs/features/` → 6 feature packages; exactly 1 (skill-control-center) violates the co-location rule; `experiments/` has 3 entries of which 2 (I2, I5) misstate their governance. So the standing debt is 1-of-6 packages non-compliant and 2-of-3 experiment slots mislabeled — a 33–67% corruption rate of the two listings a newcomer reads first. That debt recurs per reader and licenses the next split; the moves that retire it cost 6 file edits total (I2: 4, I5: 2). Where no rule is violated and no listing lies (I1, I3, I6, I7, I8, I9), the stay-debt is priced at ~0 and those verdicts HOLD on counted evidence.

**Finding 4 (I1: 5 external files, not 6) — CONCEDE the count**, verdict unchanged; immaterial per reviewer.

**Finding 5 (I2: 8 link occurrences on 7 lines; none point at the feature's own package) — CONCEDE the count** and its implication: the re-depth cost is a generic +1-level tax, mechanically scriptable, not consolidation-specific evidence. This weakens the STAY case I have now abandoned; folded into the flip.

**Finding 6 (I4: zero external refs confirmed) — CONCEDE the stale self-count**, and apply my ledger symmetrically: move cost is 0 link edits, stay-debt is nonzero (orphaned PASS record, nonstandard name). I4 now travels with I2's tree; verdict MOVE.

**HOLD on I6** — reviewer confirmed 23 external files and independently verified `test_orchestration_bridge.py:150-156` / `test_host_dispatch_hook.py:37-43` `.read_text()` a hardcoded `reviews/2026-07-23-stage-a-freeze/` path at test-run time. Strongly held. HOLD likewise on I3 (typo, confirmed), I7 (13 files, documented home), I8 (0 matches, edit-not-move), I9 (self-referential only).

## Verdict table

| item | verdict | destination path or em-dash | one-line reason |
|---|---|---|---|
| I1 | STAY | — | Compliant experiment (criterion+experiment+findings); 10 refs / 5 external files; stay-debt 0. |
| I2 | MOVE | docs/features/skill-control-center/work-record/ (subtree intact; final name is parent's call) | Pointer prices at 0% compliance; move = 4 files / ~20 mechanical edits vs permanent 1-of-6 rule violation. |
| I3 | STAY | — | Failing reader is a typo (`research-review/` nonexistent); fix 2 links in `control-center.md:559,617`; path itself relocates with I2 and the fix lands post-move. |
| I4 | MOVE | inside relocated I2 tree; rename to `review.md` costs 0 (zero inbound refs) | Move cost 0 link edits, stay-debt nonzero; symmetric ledger flips it; travels with I2. |
| I5 | MOVE | cases/foodstogo-jbp-2025/ (top-level home; name is parent's call) | Listing-level lie (`experiments/` asserts provenance it lacks); move cost = 2 file edits (.gitignore:39 + README row). |
| I6 | STAY | — | 23 external files incl. two tests that `.read_text()` the path at run time; moving produces FileNotFoundError. |
| I7 | STAY | — | Feature-owned home is documented (`docs/features/README.md:48`); 13 binding files; the gap is an unwritten tiebreak rule — a paragraph, not a move. |
| I8 | STAY | — | Remedy is one README table row (plus the `cases/` row from I5); the failing README navigator is real; no move exists to make. |
| I9 | STAY | — | 4 self-referential files; mid-dispatch move breaks `dispatch-open.json` bindings and hook-managed closes; stay-debt 0. |

## Cost ledger

**I2 — MOVE, priced both ways.** Move cost (counted): `docs/features/skill-control-center/discovery/control-center.md` — 10 occurrences of `experiments/skill-control-center` (`grep -c` = 10; includes the 2 dangling typo links fixed in the same pass); `experiments/skill-control-center/meta-orchestration/research.md` — 8 outbound link occurrences on 7 lines needing +1 depth (reviewer's recount, accepted); `implementation/frontend-context-pack.md` and `backend-task-session.md` — 1 self-path each. Total: 4 files, ~20 edits, all mechanical, verifiable by re-resolving every link post-move; `git mv` of the intact subtree preserves follow-history. Stay cost (now counted): 1 of 6 feature packages permanently non-compliant with `docs/features/README.md:16-17`, recurring per reader, precedent-setting. Payer if moved: whoever edits 4 files once. Payer if kept: every future package author and reader, indefinitely. The bounded one-time cost loses to the unbounded recurring one.

**I5 — MOVE.** Inbound: `.gitignore:39` only (grep confirmed, 4 files raw, 3 self). Move cost: 2 file edits. Stay cost: 1 of 3 entries in the `experiments/` listing asserts false provenance at the exact point the failing reader looks; no in-file text can reach them. Payer if moved: nobody measurable. Payer if kept: every `ls experiments/` reader.

**I4 — MOVE (carried by I2).** External refs: 0 (reviewer-confirmed). Marginal cost of the move and of the `review.md` rename: 0 link edits. Stay cost: a PASS record findable only by someone who already knows it exists.

**I6 — STAY.** 23 external files; `implementations/tests/runtime/test_orchestration_bridge.py:150-156` and `test_host_dispatch_hook.py:37-43` open the path at run time (reviewer-verified). Highest move cost in inventory; breaks executing code.

**I1 (10 refs / 5 external files, corrected), I3 (2-link typo fix), I7 (13 files + documented rule at `docs/features/README.md:48`), I8 (0 matches; one-row edit), I9 (4 self-refs)** — unchanged from round 1, all counts either reviewer-confirmed or reviewer-corrected as immaterial; stay-debt priced ~0 for each.

Sequencing note for the parent (cost-relevant, not a verdict): apply I2's typo fix (I3) and link rewrites in the same commit as the `git mv`, so no intermediate state has dangling links; the whole step is reversible by a single revert.

## What my angle cannot see

The strongest remaining objection now comes from the other side — R-D's executability/inertia pole, in its best form: "You flipped I2 on a rule-compliance price, but pricing rule-debt is the normative angle's job; your instrument measured 4 files and 20 edits and then let someone else's axis pick the sign. If cost yields whenever a written rule exists, the cost seat adds nothing at crosstalk." I hold against it: my flip is not deference — the ledger changed because the reviewer forced both columns to be filled, and 20 bounded mechanical edits versus an unbounded recurring cost is a cost comparison, made with my instrument. But I concede the boundary risk is real for I7, where a written rule could likewise be invoked to force consolidation; there I hold STAY because the rule on record (`docs/features/README.md:48`) endorses the current layout, and 13 binding files price forced consolidation above any named benefit.

## Claim <= proof

Low-confidence, asserted without counting:
- "Recurring, unbounded" stay-debt for I2/I5: direction argued, magnitude unmeasured — I have no reader-traffic data; the 1-of-6 / 2-of-3 corruption rates are proxies, not costs.
- `cases/` as I5's destination: no precedent directory exists; the name is unvalidated and the parent may choose otherwise at equal cost.
- Internal relative links within the I2 subtree surviving an intact move: inferred from relative-path mechanics, not exhaustively enumerated file-by-file.
- `git mv` preserving usable blame via `--follow`: standard behavior, not verified against this repo's history depth.
- I9's self-reference count (4 files) predates this round's new return files and was not re-run; the reviewer also flagged it unchecked.
