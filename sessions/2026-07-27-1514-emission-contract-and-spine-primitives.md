---
tags: [agents-infrastructure, emission-contract, provenance-spine, primitives, adversarial-review, experiment-design]
artifact_kind: session
layer: domain
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
timestamp: 2026-07-27T15:14:52-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
  - implementations/server/runtime/local_pilot.py
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session produced the first written contract for agent emission, had it structurally refuted by independent review, and established that the owner's stated objective for the infrastructure differs from the one the artifacts were built on."
---

# Emission contract and tracking-spine primitives

## Summary

The session opened on the existing x-ray of `implementations/` and turned to designing its
target-state counterpart: the infrastructure running from dispatch classification through agent
emission. Working inline from `plans/` — Agent launches were blocked by a Stage-E source-manifest
digest mismatch, repaired mid-session — the owner's description was organised into services rather
than pipeline stages, with two compilations, two confirmations, and an emission model expressed as
independent axes rather than a small enumeration of emission types. The owner then made two
corrections that reshaped the work: execution is a service of its own that resolves prompts at run
time, and the shared objective of the composed services is tracking everything done and linking
artifacts within one context and across different ones — an objective materially different from the
one the essay had been built on, and one that matches the absent provenance spine the root Plan
already names as its pivot. A hybrid system-view and engineer-view essay was authored in one file,
naming nine stances and deciding each exactly once alongside contracts, mechanics and nine failure
modes. One independent reviewer attacked it across three zig-zag exchanges and returned a structural
verdict: the three-axis emission contract is the wrong decomposition, because its address field
fuses a boolean to an identifier and does three jobs at once, and because a sealed emission is not
unaddressed but addressed to the aggregator under a delivery condition. The replacement moves
release onto the recipient and lets the recipient set carry cardinality; it dissolves five findings,
leaves fifteen surviving unchanged, and opens six new ones. The reviewer further established that
the essay's flat claim of aggregator determinism is incoherent because the aggregator was modelled
as an agent with a prompt binding, and that repairing it costs the essay two of its three
externally-authorised verdicts, since amending a prohibition inside the document that benefits from
the amendment is the move candidate invariant K1 forbids. Against a recorded recommendation that
hypothesis work was premature for the experiment route, the owner directed an experiment anyway; an
initial-definitions document and a criterion were authored under the experiment skills and attacked
by three parallel reviewers on structurally opposed angles. All three returned do-not-freeze,
converging independently on five defects, and the orthogonal reviewer concluded that the criterion's
boundedness was manufactured by deleting the unsettled architecture and pre-registering the
countable residue, offering a single-countermodel replacement in its place. Two factual errors in
the authored documents were located by inspection and recorded rather than repaired, since the
standing verdict recommends replacing the design rather than refining it.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The emission contract and the tracking-spine work belong to this root Plan's Front 3 substrate and to the absent provenance spine its §5 names as the pivot several other things wait on. |
| [A Composable Language for Governed Agent Work](../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md) | `derives-from` | The new essay's compilation vocabulary, its shallow-authority constraint, and its confirmed-dispatch immutability property were built on this companion's §6, §8 and §16.6. |
| [Frontmatter & Connections](../.agents/skills/custom/frontmatter.md) | `contradicts` | This guide states that `artifact_kind` is the single document-kind discriminator and that `node_type` must not be used, while every governed artifact under `plans/` still carries `node_type` and the artifacts authored this session followed the siblings rather than the guide. |

## Open questions

- Which objective governs the infrastructure artifacts: making a fan-out inspectable, or tracking
  and linking artifacts across contexts? The two rank the components differently, and one surviving
  review finding (angle collapse) is fatal under the first reading and out of scope under the
  second.
- Is a working context a classification an artifact belongs to, or a composition an artifact
  participates in? Two existing essays lean opposite ways and neither decides.
- Do links hold between files or between identity-bearing objects that files merely locate? The
  artifacts state that placement is a projection, but no link in the repository is built on that.
- Does the emission re-cut survive a reviewer who did not propose it? It was attacked in the third
  exchange by its own author, which is better than nothing and is not independence.
- Three reviewers with opposed angles converged on five defects. Is that convergence evidence of
  real defects, or evidence of a shared base model's blind spots? Nothing measured here separates
  the two.
- Does the 60-row concept registry in the provenance-telemetry specs supersede the eleven-name
  constituent list, or are they at different altitudes and both needed?

## Next steps

1. Decide which objective governs, then rewrite the essay's surface and layering sections before
   repairing any of the twenty-one outstanding findings — the ordering matters because the finding
   list reorders under the second objective.
2. Supply fresh owner direction for the fabric's new powers (computing a derived fact, persisting
   it, being named as a principal), which the aggregator repair moved out from under the direction
   that resolved the original row.
3. Repair the two recorded factual errors — the claim that the constituent names were never
   assembled, and the claim that the `subplans/` to `plans/` migration is in version history — or
   discard the documents that carry them.
4. Repair the two live dangling references to `subplans/` in the root Plan's child registry and in
   the essays index, and commit or revert the uncommitted migration that created them.
5. Reconcile `node_type` against `artifact_kind` across `plans/`, or record the drift explicitly so
   new artifacts stop having to choose between the guide and their siblings.

## Recommendation

Settle the objective first. It is the keystone because it is upstream of everything else recorded
here: it decides whether angle collapse blocks or is out of scope, it decides whether the record is
the core service or a side effect of the fabric, and it decides whether the constituent work is
about a fan-out contract or about a provenance spine. The licensing fact is that the root Plan
already asserts the spine's absence, its four disjoint identifier spaces, and three suspected
consequences — so choosing the tracking-and-linking objective would not widen scope, it would point
the work at something the Plan has already identified as its pivot. Everything else on the list is
labour that can be sequenced afterwards; doing it first risks repairing a document whose purpose is
about to change.

## Files touched

- plans/governed-agent-work-infrastructure/essays/agents-infrastructure-system-and-engineer-view/essay.md
- plans/governed-agent-work-infrastructure/essays/agents-infrastructure-system-and-engineer-view/review/review.md
- experiments/tracking-spine-primitives/experiment-initial-definitions.md
- experiments/tracking-spine-primitives/criterion.md
- experiments/tracking-spine-primitives/review.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- implementations/server/runtime/local_pilot.py
