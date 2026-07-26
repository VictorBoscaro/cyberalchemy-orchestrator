# S-A (Meyer, Bertrand) — angle: the declared contract binds — round 1 return

All 23 target-binding hashes verified clean. Verdict follows.

## Verdict table

| item | verdict | destination path or em-dash | one-line reason |
|---|---|---|---|
| I1 | STAY | — | Only object here that satisfies the experiment skill's defining property (a frozen `criterion.md`); no written rule names a different home. |
| I2 | MOVE | `docs/features/skill-control-center/` (subfolders `research/`, `meta-orchestration/`, `implementation/`, `agent-runtime/` preserved) | No `criterion.md` → not an experiment; a feature package of that exact name exists, and the features rule forbids scattering what governs a feature. |
| I3 | MOVE | `docs/features/skill-control-center/research/review/review.md` | Already correctly named; travels with I2 as part of the feature's reviews. |
| I4 | RENAME | `docs/features/skill-control-center/implementation/review.md` | `review.md` is review's only artifact and the name is mandated; the historical exemption covers `attacks.md`/`findings.md` only. |
| I5 | MOVE | — (out of `experiments/`; no rule names its destination) | No frozen criterion → the directory name asserts a type the tree does not satisfy; nothing written tells me where it belongs. |
| I6 | STAY | — | Feature-owned reviews of feature-owned targets; the features rule puts them exactly there. (Separate, non-placement artifact-shape defect noted below.) |
| I7 | STAY | — | The features rule's ownership test resolves the "no written rule" claim: a feature-owned experiment travels with its feature. |
| I8 | MOVE | add `experiments/` to `README.md` §Navigation "Knowledge & investigations" | `node_type: readme` obliges the file to reflect what is actually in the directory; `experiments/` is there and unlisted. |
| I9 | STAY | — | `research/<dispatch-slug>/` is the prescribed home for repository-wide work with no clear feature owner. |

## Reasoning

**The governing rule for I2, I3, I6, I7** — `docs/features/README.md` lines 16-18: *"Each package keeps its own discovery, specs, reviews and work-pack together, so that everything governing a feature travels with it rather than being scattered across the repository."* The operative clause is `rather than being scattered across the repository`, and it is a prohibition, not a preference.

**I1.** `.claude/skills/experiment/SKILL.md` lines 49-50: *"The load-bearing property is **pre-registration**: the criterion is frozen *before* the result exists (research is judged *after*, by coverage)."* Line 187 and 193-194 name the three artifacts: `criterion.md` (the proposal's deliverable), then `experiment.md` and `findings.md` from the later run. `experiments/skill-relationship-graph/` carries all three, and its `criterion.md` line 3 reads *"Status: frozen before the first probe run."* It is an experiment by the written test. No rule in the corpus fixes where an experiment's `working_folder` sits — the skill says only *"in `working_folder`"* (line 185). Absence of a rule is not a warrant to move.

**I2.** The same test fails: no `criterion.md` anywhere in the tree (verified). Positively, `.claude/skills/research/SKILL.md` lines 166-168: *"`working_folder`: when one feature clearly owns the research question, use `docs/features/<feature>/research/<dispatch-slug>/`. Use `research/<dispatch-slug>/` only for repository-wide research with no clear feature owner."* `docs/features/skill-control-center/SPEC.md` exists (hash verified), and `docs/features/README.md` lines 53-58 indexes the package as a live feature. One feature clearly owns it. I take the whole tree, not a slice: the features rule's harm is scattering, and a partial move does not cure scattering, it performs it.

**I3.** `.claude/skills/review/SKILL.md` line 21: `persisted` | written as `<working_folder>/review.md`. The file is already conformant in name. Its placement is derivative of I2.

**I4.** `.claude/skills/review/SKILL.md` line 25 (§14 box header): *"`review.md` is review's ONLY artifact — a deliberate exception; do not 'fix' it"*, and standing rule 5, lines 221-222: *"**One document, two channels** — `review.md` is the only artifact; `inline` vs `persisted` is the human's call at the gate, and it changes where it lands, never what it contains."* The only exemption granted is lines 45-46: *"reviews before 2026-07-13 wrote `attacks.md` + `findings.md`. Those files stay on disk as history."* `final-review.md` is neither pre-cutover nor one of those two names, so it is not exempt. Note the second half of standing rule 5 also disposes of the lineage counter-claim that a review "follows its target": where a review lands is the human's declared `working_folder`, not a function of its target. I relocate it only because I2 relocates.

**I5.** Same experiment test as I1, failed: the tree is `content/`, `designs/`, `model/`, `out/`, `render.sh` — no criterion, therefore nothing frozen before the result, therefore not an experiment under lines 49-50. That is all the text proves. `.claude/skills/research/SKILL.md` line 167-168 arguably *excludes* `research/` for it (a client business case is not "repository-wide research"), and no rule names a home for a client deliverable. I state the eviction and refuse to invent the destination.

**I6.** Home is correct under the features rule. Separately and outside the placement question: three of the six rounds (`2026-07-21-spec-review/`, `-external-tools-spec-review/`, `-swu-aci-001-implementation/`) persist `REPORT.md`, `BASELINE.md`, `FINAL-BASELINE.md`, `SQL-REVIEW.md` etc., and `2026-07-23-stage-a-freeze/` has no `review.md` at all. All postdate 2026-07-13, so lines 45-46 do not cover them and they violate line 25 / standing rule 5. Only `2026-07-22-bus-contracts/` and `2026-07-25-host-bus-phase-a-close/` are conformant. This is an artifact-shape defect in the right home, not a placement defect; a multi-file round cannot be *renamed* into one document without a merge, which exceeds placement.

**I7.** The proposal's premise — "under no written rule of which to use" — is false. The features rule (lines 16-18) supplies the test, and `docs/features/README.md` line 48 records `experiments/` as a constituent of that package. Feature-owned experiment, feature-owned home.

**I8.** `vault/ontology-conventions.md` line 408: *"| `readme` | Reflects what's actually in a directory. | any `README.md` |"*, restated at line 121 as the maintenance obligation *"Update it to reflect what's actually in the directory."* `README.md` line 3 declares `node_type: readme`, and `experiments/` is actually in the root directory. The `readme-pattern.md` completeness rule (line 25, *"Every file and subfolder must be listed here"*) is scoped at line 7 to folders inside `/specs/` and does **not** bind the root README — I do not use it. Note the fix is conditional on the directory surviving: if I1 stays, `experiments/` must be listed.

**I9.** `.claude/skills/research/SKILL.md` line 168: *"Use `research/<dispatch-slug>/` only for repository-wide research with no clear feature owner."* A repo-wide placement adjudication spanning `experiments/`, `docs/features/`, `implementations/` and the root README has no single feature owner; `research/artifact-placement-adjudication/` is the prescribed form. I claim no exemption for it — it earns the same test I applied to I2.

## What my angle cannot see

The strongest objection is the cost angle's, on **I2**, in its best form: the tree carries `../../../docs/features/...` relative links, and moving it changes the depth of every one of them, so a "pure" `git mv` silently strands links that resolved a moment ago; against that real breakage the benefit is that a reader who is not currently lost would have one fewer place to look. **I hold**, but narrowly and on one ground only: the features rule is stated as a prohibition on scattering, not as a convenience, and a link that must be rewritten is a mechanical cost, not a counter-rule. Cost bounds *how* the parent executes (rewrite every inbound relative link in the same commit and re-resolve them), never *whether* the rule binds.

The lineage angle's best objection lands on **I4**: the artifact verifies routes and tests under `implementations/`, so its causal home is the runtime, not the docs package. **I concede half.** I hold the RENAME — the filename rule is unambiguous and the lineage angle offers no rule against it. I hold the destination only weakly: my warrant is that it follows I2, so if the parent rejects I2 the I4 destination collapses with it and only `review.md` survives.

## Claim ≤ proof — low confidence

- **I5 destination** — em-dash is not modesty, it is the finding. "Not an experiment" is proven from `experiment/SKILL.md` lines 49-50; the destination is unproven and I decline to name one.
- **I2, `meta-orchestration/` and `agent-runtime/` specifically** — the features rule enumerates "discovery, specs, reviews and work-pack." Context packs, task-session records and meta-orchestration research are covered only by the broader clause "everything governing a feature," which is a reading, not an enumeration. `research/` and `implementation/` are solidly covered; these two ride on the general clause.
- **I1 STAY** — rests on the absence of a rule assigning experiments a home, not on a rule assigning them `experiments/`. If a home rule for `experiment` working folders exists outside the corpus I was pointed at, this verdict is void.
- **I6 artifact-shape finding** — the violation is cited and firm, but it is not a placement verdict and I did not price the remedy.
- **I3 sub-path** — no rule mandates a `reviews/` directory inside a feature package; `agents-communication-infra`'s `reviews/` is described at `docs/features/README.md` lines 48-49 descriptively, for one package. I therefore preserve the existing `research/review/` position rather than inventing a `reviews/` convention.
