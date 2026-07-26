---
tags: [dispatch, agents, orchestration, anti-bias, architecture, skills]
node_type: audit
is_session: true
layer: architecture, domain
nature: explanatory
status: active
created: 2026-07-26
timestamp: 2026-07-26T00:43:36-03:00
expires: 2026-09-24
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "It unblocked the mandatory dispatch bridge for all future subagent launches and produced first production evidence that pairwise reviewer tension catches defects neither lens finds alone."
---

# docs/ and plans/ README index, and the defect repair it surfaced

## Summary

The session set out to decide where the repository should have READMEs, then to author them with
the `readme-pattern` skill under subagent dispatch. Three read-only investigators with opposed
lenses — newcomer disorientation, rot-skepticism, machine-traversal — ranked candidate folders,
and their disagreements decided the ranking: the rot-skeptic's evidence killed the newcomer's top
pick (`.claude/skills/`, whose count the root README already reports wrong at 67 vs 72), while the
machine reader's reproduced append-only interception won `telemetry/agents/` the top slot.
Authoring by subagent was then blocked twice by the mandatory dispatch bridge — first a
half-landed schema 0.6.2 bump (the appender required 0.6.2 while the hook emitted 0.6.1, 17 files
pinned 0.6.1, and `legacy.py` hard-raises on any non-0.6.1 opening row), then a Stage-E
source-digest mismatch. The owner chose to have the parent author inline rather than repair a
migration another session was mid-flight on, so ten index READMEs were written directly for
`docs/` and `plans/` and self-reviewed on both a form gate and a veracity gate, which caught and
removed one fabricated skill reference. Writing them surfaced three real defects: a dead
`companion_to` reference, `PLAN.md` indexing only one of ten workstream artifacts, and two
non-feature validator fixtures sitting in `docs/features/`. The owner then authorized a subagent
repair, which itself required repairing the bridge: an audit of all 47 Stage-E pins found exactly
two stale, both from the reverted 0.6.2 work and pinning digests matching no file and no git
object, and re-pinning them restored launches. Dispatch `2026-07-26-docs-defect-repair` was gated
by two independent check-tension helpers (both PASS), confirmed by the owner, registered, and run
as two disjoint n=1 fixers feeding one tensioned n=2 reviewer pair on the attack-vector axis. The
tension earned its keep — the form reviewer found a missing version bump invisible to the evidence
gate, and the evidence reviewer found that fixing the defect had made this session's own
`essays/README.md` stale — while parent verification overturned one subagent's self-report, since
the essay writer claimed to have left two body references untouched but had in fact repaired all
three, and `git diff` misled both reviewers because that essay is untracked by git. A README
written the previous day was already wrong within hours when a tenth workstream artifact landed at
02:57, which is the rot the skeptical lens predicted and the main argument for generated indexes
over hand-maintained ones on churning folders.

## Contradictions

- validates [[anti-noise-orchestration]] — one production instance, not a proof: the tensioned
  reviewer pair surfaced two defects each visible to only one lens (a missing version bump to the
  form gate, a stale README to the evidence gate), which is the structural-opposition mechanism
  `HYP-ORCH-NOISE` predicts.

## Open questions

- Is a hand-maintained Navigation section ever the right instrument for a folder whose child set
  changes daily, or is README-as-index only defensible over frozen folders? Two data points
  argue the latter: `workstreams/README.md` went stale within hours of being written, and the root
  README's skill count has been wrong since before this session.
- Does `readme-pattern`'s mandatory "Business Context" section have an honest filling for
  machine-contract folders such as `telemetry/agents/`, `telemetry/runtime/` and
  `.codex/delegation-receipts/`, where the load-bearing content is an append-only or
  generated-artifact contract rather than a business context? The three highest-ranked candidates
  from the investigation all sit in this category and were therefore never authored.

## Next steps

1. Decide whether the Stage-E `source-manifest.json` is a freeze artifact or a tracking artifact.
   That single choice determines whether a `SKILL.md` edit must re-pin it or must be forbidden
   mid-migration; today it silently blocked every launch.
2. Land or revert the 0.6.2 migration deliberately. The working tree is now incoherent in a way
   that happens to work: `SCHEMA_VERSION` is back to `0.6.1` while `LIVE_TYPES` still contains
   `others`, which is the only reason this session could register its dispatch honestly.
3. Diagnose why the bridge rejects a second `Agent` call batched in one message
   (`orphan event outside accepted command group`) when three concurrent launches succeeded
   earlier in the same session. Concurrency across groups is currently unavailable.
4. Repair review recommendations 2–5 on the work-context system-view essay; only #1 was in scope.
5. Decide the fate of `docs/features/{validator-fixture,discovery-validator-fixture}/` — untracked
   empty directories referenced by nothing, currently documented as non-features.

## Recommendation

Next step 1 is the keystone, and it is deliberately ordered ahead of the larger 0.6.2 decision it
gates: while the manifest's status is ambiguous, any edit to a governed skill file can block all
agent work without warning, which is exactly how this session lost two attempts. The licensing fact is the
47-pin audit — exactly two entries were stale, both from the reverted 0.6.2 work, and both pinned
digests matching no file and no git object, so the manifest was already tracking a state that had
ceased to exist rather than freezing a state anyone had reviewed. Resolve that, then land or
revert 0.6.2 as one deliberate change rather than the current partial revert.

## Files touched

- docs/README.md
- docs/decisions/README.md
- docs/discovery/README.md
- docs/essays/README.md
- docs/features/README.md
- docs/signals/README.md
- docs/temps/README.md
- plans/governed-agent-work-infrastructure/essays/README.md
- plans/governed-agent-work-infrastructure/subplans/README.md
- plans/governed-agent-work-infrastructure/workstreams/README.md
- plans/governed-agent-work-infrastructure/PLAN.md
- plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- telemetry/agents/subagents-dispatch.yaml

## Extra section

Owner directions issued this session, recorded because they are standing preferences rather than
one-off calls:

- **Do not repair another session's in-flight migration to unblock yourself.** Offered the choice
  between finishing the 0.6.2 bump and authoring inline, the owner chose inline authoring
  explicitly to avoid colliding with a concurrent session mid-migration. Surface the blocker and
  deliver the work by another route.
- **Subagent work is wanted with a review pass attached, not instead of one.** The instruction was
  "invoke subagents to fix those and then subagents to review" — fixers and reviewers as separate
  seats, with the reviewers tensioned rather than duplicated.
- **The first investigation was explicitly scoped "no dispatch"** — three investigators returning
  to the parent for ranking, with no ledger row. The owner distinguishes an unregistered
  fan-out for the parent's own judgment from a registered dispatch that produces artifacts.
