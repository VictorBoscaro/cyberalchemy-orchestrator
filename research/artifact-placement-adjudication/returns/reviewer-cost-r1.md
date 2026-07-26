# R-C (Cunningham, Ward) — lens: cost falsification — round 1 review of S-C

## Verdict
FIX

## Findings

1. **I2 — substitution attack.** Claim: "bidirectional pointer lines (~2 edits)" is a cheaper instrument than consolidating into `docs/features/skill-control-center/`. Reality: `docs/features/README.md:16-17` states explicitly — "Each package keeps its own discovery, specs, reviews and work-pack together, so that everything governing a feature travels with it rather than being scattered." A pointer does not make the artifacts travel together; it documents that they don't and stops there. This is the textbook substitution the lens targets: an index line that names the split instead of closing it. Falls to attack (3). Severity: MAJOR. Correction: price the pointer as "compliance-with-the-rule: 0%," not as a solved problem.

2. **I5 — substitution attack, sharper than I2.** Claim: a one-line in-file disclaimer ("client case, not governed experiment") is cheaper than a move. Reality: `ls experiments/` (verified) returns exactly three entries — `foodstogo-jbp-2025`, `skill-control-center`, `skill-relationship-graph`. The failing reader is anyone scanning that directory listing, who never opens the file the disclaimer lives in. 1-of-3 top-level experiment directories is not a governed experiment; the disclaimer is invisible at the point of failure. Falls to attack (3). Severity: MAJOR. Correction: the remedy must act at the listing level (rename or move), not inside a file nobody who needs it will open.

3. **Debt of staying, unpriced.** The subject concedes in "What my angle cannot see" that inbound-reference counting is structurally blind to recurring/future-reader cost and to convention erosion, then holds every verdict anyway on the strength of "no reader observed failing." Nowhere is the erosion cost priced: `docs/features/README.md`'s co-location rule is already violated by I2's existence, and an unenforced rule invites the next contributor's next feature to split the same way. Falls to attack (2), the primary target. Severity: CRITICAL — it is the systemic pattern behind both I2 and I5, not a one-off.

4. **I1 recount.** Claim: 26 occurrences / 9 files, ~10 refs / 6 external files after exclusion. Re-run (`experiments/skill-relationship-graph`): 30 occurrences / 12 files raw; excluding this dispatch's growing artifact trail (proposal-v2/v3/v4 + 3 returns, none of which existed when S-C wrote its return), external footprint is 10 occurrences across 5 files (`control-center.md`×6, `architecture.md`×1, `research-initial-definitions.md`×1, `research/research.md`×1, `backend-task-session-context.md`×1). Off by one file, immaterial. Attack (1). Severity: MINOR. Correction: 5 external files, not 6.

5. **I2 link-count recount.** Claim: "7 outbound `../../../` links" in `meta-orchestration/research.md`. Re-run: 7 matching lines but 8 actual link occurrences (line 7 contains two). Materially, none of the 8 point at `skill-control-center`'s own feature package — targets are `agent-provenance-telemetry`, the `maestro-trama` vault, `.claude/skills`, and `implementations/`. The re-depth cost is real (moving into `docs/features/` adds one directory level: 3-deep under `experiments/` vs 4-deep under `docs/features/`), so the cost claim survives, but it is a generic path-depth tax, not evidence specific to opposing consolidation. Attack (1). Severity: MINOR.

6. **I4 recount.** Claim: "3 files, all this dispatch's own proposals" (zero organic refs). Re-run (`final-review`): 6 files, all self/dispatch (3 return files + 3 proposal versions, again dispatch growth since r1 was written) — zero external files. Conclusion holds; only the self-count is stale. Attack (1). Severity: MINOR.

## Costs that held

- **I6**: 24 raw matches for `reviews/2026`, minus this dispatch's own return file = 23 external files — exact match to the claim. Read `implementations/tests/runtime/test_orchestration_bridge.py:150-156` and `test_host_dispatch_hook.py:37-43`: both call `.read_text()` at test-run time on `docs/features/agents-communication-infra/reviews/2026-07-23-stage-a-freeze/profile-registry-manifest.json` — a hardcoded path actually opened, not a comment or string decoration. Moving that review folder without a corresponding test update produces `FileNotFoundError`. The subject's "breaks running code and data, not just prose" claim is confirmed for at least these two files; accepted as-is.
- **I7**: 14 raw matches minus self = 13 external files — exact match.
- **I8**: 0 matches in `README.md` for `experiments/` — confirmed.
- **I3**: `research-review/` confirmed absent; `experiments/skill-control-center/research/review/review.md` confirmed present — the two `control-center.md` links are indeed dangling on a typo, not a placement problem. Accepted.

## What I could not check

- I9's "4 self-referential files" claim was not independently re-run; it sits outside the eight items the cost lens was asked to falsify and did not bear on the STAY-uniformity concern.
- Whether `internal-tools/ui-experimentation/data/dispatches.json`'s reference (line 272, a `working_folder` field) is read at runtime by any live tool, or is inert fixture data — could not trace the consuming code within budget, so I did not fold it into the I6 "breaks code" tally beyond the two confirmed test files.
