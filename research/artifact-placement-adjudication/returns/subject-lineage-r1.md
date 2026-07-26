# S-B (Torvalds, Linus) — angle: lineage binds — round 1 return

## Verdict table

| item | verdict | destination path | one-line reason |
|---|---|---|---|
| I1 | STAY | experiments/skill-relationship-graph/ | Self-contained probe (criterion+experiment+findings) with no downstream feature that claims it; it fed a decision but produced no docs/features artifact of its own. |
| I2 | SPLIT | research/→docs/features/skill-control-center/research/; meta-orchestration/→stays; implementation/+agent-runtime/→docs/features/skill-control-center/session-evidence/ | The tree has three distinct lineages, proven by same-commit coupling and repo precedent, not one home. |
| I3 | MOVE | docs/features/skill-control-center/research/review.md | Travels with the two files it attacked, which move for the same reason. |
| I4 | MOVE | docs/features/skill-control-center/session-evidence/final-review.md | Its target is the runtime, but the repo's own precedent for *where a runtime-verifying task-session review lives* is docs/features/<feature>/session-evidence/, not implementations/ itself. |
| I5 | STAY | experiments/foodstogo-jbp-2025/ | Its own move commit says the rename was spelling consolidation, not an experimental-lineage claim; no target anywhere else in the repo. |
| I6 | STAY | (already correct) | Front-matter self-declares `feature:` binding to what each review attacked; already co-located. |
| I7 | STAY | (already correct) | Feature-scoped probes commissioned by and attacking agents-communication-infra specifically; distinct corpus from repo-wide experiments/. |
| I8 | STAY | — | The omission is not a defect under lineage: experiments/ is genuinely heterogeneous (repo-wide, feature-owned, client-owned), so no single row would state a true lineage claim. |
| I9 | STAY | research/artifact-placement-adjudication/ | It is itself a research artifact, correctly filed with the research/ corpus alongside its own prior proposal versions. |

## Reasoning

**I1.** `git log --follow --stat -- experiments/skill-relationship-graph/` → one commit, `22cbebb feat: probe the skill graph and decide the control-center shape`, created the full criterion/experiment/findings/build set atomically. Nothing downstream re-targets it. Derives-from-here = belongs-here since no other object claims it as input.

**I2/I3/I4.** `git log --diff-filter=R --find-renames -- experiments/skill-control-center/` surfaces the rename baked into `06bd467`: `.../{research-review => research/review}/review.md`. Commit body: *"Moves `research-review/` to `research/review/` so review material sits under the research root instead of beside it"* — an internal reorg, not a cross-tree claim.

The load-bearing fact is that `583683f fix: correct the control-center research contract after review` touches **both** trees in one commit:
```
experiments/skill-control-center/research-review/review.md | 92 ++
experiments/skill-control-center/research/findings.md      | 95 +-
experiments/skill-control-center/research/research.md      |  6 +-
docs/features/skill-control-center/discovery/control-center.md | 478 ++
```
One atomic commit both fixes the research contract *and* writes the docs/features discovery from it. That is producer→target in the same breath — stronger than "it came from here," it is "this commit's whole point was to hand this off there." I3 (review.md) and its siblings research.md/findings.md move together (a review belongs with what it attacked, and what it attacked is moving).

`meta-orchestration/` was born in `22cbebb`, the *same* commit as I1, and its content (`grep '\.\./\.\./\.\.'`) cites `agent-provenance-telemetry` UI-SPEC/queries/observability paths, not skill-control-center's own SPEC. It is the progenitor memo that spawned the whole skill-control-center probe, not a document commissioned by skill-control-center's docs package — so it stays with what it produced (I2's root), not with what research/ produced.

`implementation/` + `agent-runtime/` (commit `06bd467`, message: *"Keeps the context packs, task sessions, agent-runtime records and final review that produced Phase 1, so the implementation's provenance is readable from the repo"*) verify `implementations/static/control-center` routes and tests — `final-review.md` line 9: *"The external Control Center inventory remains exactly six `/v1/control-center/*` routes"*. But `implementations/` itself has no docs/review precedent (`find implementations -maxdepth 3 -name "*.md"` → only README.md, UI-CONTRACT.md, agent-runtime/README.md, none of which are build-record docs). The repo's actual precedent for this artifact type is `docs/features/agent-provenance-telemetry/session-evidence/TASK-100/{context-pack.md,task-session.md}` and `TASK-105/layering-self-review.md` — a feature package already houses exactly this shape (task-session pack + terminal review) under `session-evidence/`. Lineage-by-precedent says I4 and its siblings belong at the analogous `docs/features/skill-control-center/session-evidence/`.

**I5.** `git show --stat 4e69b2f`: *"Relocate the RappiAds business case from `experimentations/` to `experiments/`, retiring a directory whose name was a Portuguese-shaped coinage and consolidating on the spelling the rest of the repo already uses... Pure rename: all 15 files move byte-for-byte, with no content edit."* This is the artifact's own commit admitting the move was orthographic, not evidentiary. No criterion.md exists, and no other tree references it. Lineage has nothing pointing this object anywhere else, so absent a target, STAY is the only lineage-supported call.

**I6.** `head -10` on `BASELINE.md` and `system-tags-and-lens-review.md` shows explicit front-matter: `feature: agents-communication-infra` / `feature: agent-provenance-telemetry`. Self-declared binding plus physical co-location under the feature's own `reviews/` — lineage is already satisfied.

**I7.** `git log` on the two subfolders: `53cff55 feat: record the rejected skill-protocol-compilation prototype` — the prototype's own history frames it as belonging to that feature's decision record, not the repo-wide experiments/ corpus.

**I8.** No command moves a README table row by itself; this is a documentation-completeness question, and my angle can only say the underlying territory (experiments/) is not one lineage but at least three (I1/I5 repo-wide, I7 feature-owned) — so silence is defensible, not obviously wrong.

**I9.** `ls research/artifact-placement-adjudication/` shows `dispatch-open.json, proposal-v2/v3/v4.json` already resident — it is following the same convention as every other dispatch's research/ home; no evidence points it elsewhere.

## What my angle cannot see

The strongest declared-rule objection: `docs/features/README.md` states every package keeps discovery, specs, reviews **and work-pack** together — which would pull all of I2 (including meta-orchestration/) into docs/features/skill-control-center/ in one motion, not the three-way split I derived. My split rests on meta-orchestration's *content* pointing elsewhere (APT paths) rather than on a documented exception to that rule. I hold my position because the same-commit coupling evidence (583683f) is a stronger, narrower signal than the general rule, but I concede the rule-angle can fairly call my split an under-application of a contract that names no such carve-out.

The cost objection: moving I3/I4 breaks the `../../../` relative links inside `meta-orchestration/research.md` and other siblings that resolve today; every such move creates a repair obligation with no named reader currently blocked. I cannot see whether any live process actually consumes those links today — I only see that they exist and resolve.

## Claim <= proof (low confidence)

- **I2/meta-orchestration placement**: the "stays with what it produced" argument is inferential (content topic ≠ formal target declaration); no commit or front-matter explicitly says "meta-orchestration belongs at I2's root." Low confidence.
- **I4/agent-runtime destination** (`session-evidence/`): based on structural analogy to APT's precedent, not on any internal reference from final-review.md or the task-session files naming that path. Low confidence.
- **I8**: no verdict mechanism truly fits "absence of a row"; STAY is a default, not a proven claim.
- **I7 "no written rule" being fine**: I infer feature-scoped vs. repo-wide corpus split from commit messages alone; no artifact states this taxonomy explicitly.
