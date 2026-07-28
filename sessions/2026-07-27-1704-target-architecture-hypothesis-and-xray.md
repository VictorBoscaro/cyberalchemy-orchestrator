---
tags: [agents-infrastructure, architecture-hypothesis, system-view, engineer-view, x-ray, adversarial-review, source-integrity]
artifact_kind: session
layer: domain
version: 0.1.0
created_at: 2026-07-27T17:04:25-03:00
updated_at: 2026-07-27T17:04:25-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
  - implementations/server/runtime/local_pilot.py
promoted_candidates: []
expected_importance: 7
importance_rationale: "Produced a fresh architecture hypothesis authored under the system-view and engineer-view contracts and a validated visual x-ray of it, then had both survive three adversarial rounds that exposed several over-claims running in the direction that makes an unbuilt proposal look ratified."
---

# Target architecture hypothesis and its x-ray

## Summary

The session opened on a review of the previous session's record and moved into judging whether the
existing infrastructure essay served the owner's actual intent, which turned out to be a hypothesis
for the final state of the architecture presented high-level as problem, then properties, then
services. That essay was found to be missing its middle step — it moved from problem straight to
services, so the services arrived asserted rather than derived, and its verdict vocabulary made a
proposal read as a decision record. A new essay was authored in its place, first freehand and then
rewritten under the `system-view` and `engineer-view` skill contracts, which forced three things the
freehand draft lacked: nine named stances each routed to exactly one verdict, an alternative-framings
table per major section, and an authority citation on every decision row including the four that
have none. The opening was rewritten a second time after the owner rejected reasoning from the
current inventory, so the ideal is now worked out on its own terms and existing components are
compared to it only afterwards. A visual x-ray of the eight proposed services was then authored as a
lane model plus a local L0 HTML page, passing the Arcanum schema validator, which is ahead of the
local example and required a reader contract the local example predates. Two reviewers on
structurally opposed poles of one fidelity axis — the artifact flatters its subject versus the
artifact fails its reader — attacked it across three zig-zag rounds and both reached ACCEPT. They
converged in round one on six defects, and the sharpest findings were over-claims all leaning the
same way: a status the essay does not contain, a gate column answering "no" for four rows while the
header said six, and a citation to the essay section holding the build-something-cheaper
alternatives while reproducing none of them. Agent launches were blocked three times by the Stage-E
source-integrity gate; the first block was a scaffolder wiping the Codex lifecycle policy from
`AGENTS.md`, which was restored, and the next two were real authored policy landing in both
`AGENTS.md` and `CLAUDE.md`, which were re-digested across both levels of the integrity chain. The
hypothesis carries one hole its own refutation condition names: the surface requires work to run
under authority and none of the eight services provides it.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The new essay and its x-ray belong to this root Plan's substrate, and the tracking-and-linking objective they are built on is the absent provenance spine its §5 names as the pivot. |
| [Emission contract and tracking-spine primitives](2026-07-27-1514-emission-contract-and-spine-primitives.md) | `derives-from` | This session executed that session's keystone recommendation — settle which objective governs before repairing anything — by authoring a new essay under the tracking-and-linking objective rather than refining the old one. |
| [A High-Level View of Work Context Infrastructure](../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md) | `derives-from` | Three of the new essay's requirements were carried from this companion: identity surviving description, a thing participating in several contexts at once, and projections never manufacturing facts. |
| [Frontmatter & Connections](../.claude/skills/custom/frontmatter.md) | `contradicts` | The guide states `artifact_kind` is the single document-kind discriminator and that `node_type` must not be used, while the essay authored this session carries `node_type` because every governed sibling under `plans/` still does. |

## Open questions

- Does authority need a ninth service, or is it a property of the record? The essay's §1 requires work
  to run under authority and none of its eight services provides it. This is the hypothesis's own
  stated refutation condition — a requirement with no service — occurring inside the hypothesis.
- Two reviewers on opposed angles both reached ACCEPT. Is that convergence evidence the artifact is
  faithful, or evidence of a shared base model's blind spot? Nothing measured here separates the two,
  and the same question was left open by the previous session about a three-reviewer convergence.
- Should `AGENTS.md` and `CLAUDE.md` remain inside the Stage-E source manifest's scope? They are under
  active edit, and every edit invalidates the manifest and blocks agent launches until both levels of
  the chain are re-digested.
- Is a working context something an artifact belongs to, or something it participates in? Carried
  forward unresolved; the new essay assumes typed relations either way but the two readings give
  different shapes for cross-context links.

## Next steps

1. Re-digest the Stage-E manifest and the `local_pilot.py` pin whenever `AGENTS.md` or `CLAUDE.md`
   changes, until their manifest scope is decided — the gate will keep blocking otherwise.
2. Give the x-ray's five SVGs real accessible names via `<title>`/`<desc>` rather than one
   `aria-label` each; both reviewers recorded this below the ACCEPT line as a degradation.
3. Reconcile `node_type` against `artifact_kind` in the new essay and across `plans/`, or record the
   drift explicitly so new artifacts stop having to choose between the guide and their siblings.

## Recommendation

Attack D9 first — the authority hole. It is the keystone because it is the one place the hypothesis
refutes itself by its own criterion, and because every other open item is either labour or a question
about confidence rather than about the design. The licensing fact is that the essay already names "a
requirement with no service" as a refutation condition and then supplies an instance of it, so
closing D9 does not widen scope; it discharges a debt the document has already booked. Deciding it
also settles whether the service count is eight or nine, which the x-ray would then need to redraw —
so doing it before any further visual work avoids repainting the picture twice.

## Files touched

- plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/essay.md
- plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/x-ray/infrastructure.html
- plans/governed-agent-work-infrastructure/essays/target-architecture-hypothesis/x-ray/infrastructure.lanes.json
- AGENTS.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- implementations/server/runtime/local_pilot.py
- telemetry/agents/subagents-dispatch.yaml
