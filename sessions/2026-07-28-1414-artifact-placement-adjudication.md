---
tags: [repository-layout, artifact-placement, provenance, subagent-dispatch, anti-bias-tension, control-center]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-28T14:14:31-03:00
updated_at: 2026-07-28T14:14:31-03:00
expires: 2026-09-26
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 6
importance_rationale: "Restored the missing research-and-review provenance of a live feature package and produced the first measured cost of the check-tension gate on a small question."
---

# Artifact placement adjudication — the Control Center build record moves home

## Summary

The owner asked what each top-level entry in `experiments/` actually is and whether the
repository's review artifacts belonged inside one of them. An initial read found the opposite
vector: the six dated review rounds under `docs/features/` sit correctly beside the targets they
attacked, while `experiments/skill-control-center/` was never an experiment at all and held the
research and review lineage that its own feature package was missing. The owner then asked for
this to be adjudicated by three independent subagents, each with its own reviewer, zig-zag to a
ceiling of three rounds, then robot-talks crosstalk, then a second reviewer pass, with the parent
adjudicating and applying. The three angles were deliberately opposed — the declared rule binds,
lineage binds, the cost of moving binds — and all three converged unprompted on leaving the dated
review rounds untouched. The move was licensed not by criterion-absence, which proves only that a
label is false, but by the feature package actively claiming those files as `derives-from` in its
own Connections table; that same distinction is why the FOODSToGo business case stayed where it
is. Fifteen files moved with history preserved, `final-review.md` was renamed to the mandated
`review.md`, and twenty-six references were repaired — three of which had been dangling since an
earlier reorganisation and were found only because one angle was tasked with counting inbound
links. Verification confirmed zero dangling links and no surviving references to the old tree,
but the runtime test suite could not be executed because no `pytest` or virtualenv exists under
`implementations/`. The dispatch also produced a finding about itself: the check-tension gate
rejected the sheet three times over four rounds and nine helpers, every rejection legitimate,
including one that correctly called an earlier fix cosmetic. A round-four helper judged the gate
had become the dominant cost and located the defect in the topology rather than the gate, since
nothing scales gate depth to question size. Two governance frictions surfaced unresolved: the two
experiment homes still have no written rule of which to use, and the append-only hook continues to
block `git add` on the ledger, leaving two rows uncommitted.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [docs/features/skill-control-center/SPEC.md](../docs/features/skill-control-center/SPEC.md) | `validates` | The move restored the research and review lineage this package specifies but could not previously evidence, so the spec's provenance claims are now checkable in place. |
| [docs/features/skill-control-center/discovery/control-center.md](../docs/features/skill-control-center/discovery/control-center.md) | `resolves` | Three of this discovery's `derives-from` links had pointed at a `research-review/` directory that stopped existing in an earlier reorganisation; the session repaired them and the ten live links the move would have broken. |
| [README.md](../README.md) | `contradicts` | The root directory tables omitted `experiments/` entirely while it held a live runtime dependency; the session records what the directory actually contains and that its entries are not uniformly governed experiments. |
| [docs/features/README.md](../docs/features/README.md) | `refines` | Its `skill-control-center` entry described a package shape that the move made false; the entry now names the incoming build record. |
| [research/artifact-placement-adjudication/reconciled-table.md](../research/artifact-placement-adjudication/reconciled-table.md) | `derives-from` | The applied plan is the parent's adjudication of this reconciled table and its six-item residue list. |

## Open questions

- Which of the two experiment homes a new probe belongs in — top-level `experiments/` or a
  feature-owned `docs/features/<feature>/experiments/` — remains unwritten. The session recorded
  the gap in the root README rather than inventing a rule, because no seat could cite one and the
  owner has not ruled.
- Whether the check-tension gate needs a proportionality circuit-breaker, or whether the
  discipline of designing smaller topologies for smaller questions is sufficient. Four rounds and
  nine helpers to place directories is measured, not disputed; the remedy is not settled.
- Whether `experiments/foodstogo-jbp-2025/` should keep a directory name that overstates it. All
  three angles agreed the label is false; none produced a licensed destination, and the cheapest
  proposed move turned out to be non-reversible because of a root-anchored `.gitignore` entry and
  nineteen untracked build artifacts.

## Next steps

1. Install `pytest` or provision a virtualenv under `implementations/` and run `tests/runtime`,
   closing the one verification this session could not perform. The four test files that read a
   hardcoded path into `reviews/2026-07-23-stage-a-freeze/` were confirmed to still resolve, but
   confirmation of a path is not execution of a test.
2. Decide the ledger-staging question: either add a hook carve-out for `git add` and `git commit`
   on `telemetry/agents/subagents-dispatch.yaml`, or accept that ledger rows are permanently local
   and record that as the intended behaviour. Two rows from this session are uncommitted.
3. Repair the artifact-shape defect under `docs/features/agents-communication-infra/reviews/`:
   three post-2026-07-13 rounds persist `REPORT.md`/`BASELINE.md`/`FINAL-BASELINE.md` and
   `2026-07-23-stage-a-freeze/` carries no `review.md` at all. The remedy must be additive,
   because that directory's path is load-bearing for executing tests.

## Recommendation

Attack the ledger-staging decision first. It is the only item that compounds: every future
dispatch appends rows that cannot enter a commit, so the gap between what the repository claims
as its append-only record and what the repository actually preserves widens with each use. The
licensing fact is that the file is tracked and was committed before, at `1eb315c`, so the
prohibition is a hook behaviour rather than a settled policy — which means the decision is
genuinely open rather than a constraint to work around. The test-execution gap is real but
bounded and does not grow.

## Files touched

- README.md
- docs/features/README.md
- docs/features/skill-control-center/discovery/control-center.md
- docs/features/skill-control-center/research/findings.md
- docs/features/skill-control-center/research/research.md
- docs/features/skill-control-center/research/review/review.md
- docs/features/skill-control-center/meta-orchestration/findings.md
- docs/features/skill-control-center/meta-orchestration/research.md
- docs/features/skill-control-center/implementation/backend-context-pack.md
- docs/features/skill-control-center/implementation/backend-task-session.md
- docs/features/skill-control-center/implementation/frontend-constitution-check.md
- docs/features/skill-control-center/implementation/frontend-context-pack.md
- docs/features/skill-control-center/implementation/frontend-task-session.md
- docs/features/skill-control-center/implementation/review.md
- docs/features/skill-control-center/agent-runtime/backend-task-session-context.md
- docs/features/skill-control-center/agent-runtime/backend-task-session-result.md
- docs/features/skill-control-center/agent-runtime/frontend-task-session-context.md
- docs/features/skill-control-center/agent-runtime/frontend-task-session-result.md
- research/artifact-placement-adjudication/proposal-v2.json
- research/artifact-placement-adjudication/proposal-v3.json
- research/artifact-placement-adjudication/proposal-v4.json
- research/artifact-placement-adjudication/dispatch-open.json
- research/artifact-placement-adjudication/dispatch-close.json
- research/artifact-placement-adjudication/reconciled-table.md
- research/artifact-placement-adjudication/returns/subject-normative-r1.md
- research/artifact-placement-adjudication/returns/subject-lineage-r1.md
- research/artifact-placement-adjudication/returns/subject-lineage-r2-final.md
- research/artifact-placement-adjudication/returns/subject-cost-r1.md
- research/artifact-placement-adjudication/returns/subject-cost-r2-final.md
- research/artifact-placement-adjudication/returns/reviewer-lineage-r1.md
- research/artifact-placement-adjudication/returns/reviewer-cost-r1.md
- research/artifact-placement-adjudication/workflow/reviewer-normative-turn-0.json
- research/artifact-placement-adjudication/workflow/reviewer-lineage-turn-0.json
- research/artifact-placement-adjudication/workflow/reviewer-cost-turn-0.json
- research/artifact-placement-adjudication/workflow/crosstalk-turn-0.json
- output/playwright/ux-validator/skill-control-center-phase1/evidence-cards.md
- telemetry/agents/subagents-dispatch.yaml
