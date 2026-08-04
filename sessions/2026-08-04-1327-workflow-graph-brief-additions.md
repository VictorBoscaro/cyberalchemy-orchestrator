---
tags: [workflow-graph, protocol-compilation, skill-execution-profile, protocol-recipe, dispatch-review, anti-bias]
artifact_kind: session
layer: domain
version: 0.1.0
created_at: 2026-08-04T13:27:20-03:00
updated_at: 2026-08-04T13:27:20-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 6
importance_rationale: "The session closed the upstream-boundary gap in a fresh discovery brief and, in doing so, produced a checkable instance of the tension-pair review catching factual error in the parent's own work."
---

# Workflow-graph brief additions and their tension-pair review

## Summary

The session began by recovering the recorded direction for a skill-compiling protocol — a skill that
decomposes another skill into a typed graph consumed by the subagents-strategy interface — and found
that its downstream half had shipped that morning as bounded, non-authoritative protocol compilation
while its upstream half, the decomposition itself, remained unbuilt. The running dispatch control
plane was then exercised over twelve repositories and 1174 ledger rows to see the existing
visualizations. Reading the new `workflow-graph` discovery brief showed it continues the shipped
compiler downstream from `ProtocolRecipe` and recovers the derived-view principle, but never mentions
skills at all, omits the deliberate-opposition review pattern the repository actually runs, and drops
the rigor-variation question raised on 2026-07-25. A conceptual question about where a skill sits was
resolved from the promoted schemas: a skill yields a `SkillExecutionProfile`, its meaning, while a
`ProtocolRecipe` is authored against that profile and is a choice of method, which is what makes the
two invalidate for different reasons and what lets a digest cache be useful rather than thrash. Five
additions were applied to the brief on that basis, then reviewed by two subagents given deliberately
opposed priors, registered and closed as a governed review dispatch. The reviews found that the claim
of an undeclared owner for the upstream step was refuted by ACI-PG-001, which assigns contract and
lifecycle ownership of profile, binding and recipe to ACI Protocol Governance, leaving only the
transform undeclared. They also found the cited prototype carries no profiles — its `profiles/`
directory is empty and the `medium`/`high` distinction lives as two `protocol-graph` blocks with a
`work_granularity` field in non-confirmable examples — and that the new counterexample had smuggled a
verdict on the sufficiency of a promoted edge kind into a brief that authorizes nothing. All three
defects were corrected, the standalone evidence row was folded into the existing taxonomy row rather
than becoming a fourteenth gate, and the rigor question was demoted to a residual inside WGQ-9
because that question is structurally unable to receive a not-applicable disposition. The reviewers
disagreed on whether the rigor paragraph was the best or the worst addition, and that disagreement
was settled by checking the prototype directly rather than by preferring either verdict.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Workflow Graph discovery brief](../docs/discovery/workflow-graph/README.md) | `refines` | The session added five items to the brief, then corrected three of them against sources, leaving its subject unchanged. |
| [ACI-PG-001 Protocol Governance ownership](../docs/decisions/aci-protocol-governance-ownership.md) | `derives-from` | The corrected non-decision wording is built on this record's assignment of profile, binding and recipe ownership. |
| [domainspec-spec-feature protocol design](../docs/features/agents-communication-infra/experiments/skill-protocol-compilation/prototypes/domainspec-spec-feature/protocol-design.md) | `derives-from` | The corrected WGQ-9 paragraph reports what this prototype actually contains, replacing an inaccurate profile citation. |
| [Protocol Governance compiler session](2026-08-04-1026-protocol-governance-compiler.md) | `contextualizes` | That session promoted the compilation contract from which this brief starts and which bounded these edits. |

## Open questions

- Who performs the transform from a skill revision to a profile and a recipe, and against what
  standard? Both endpoints have assigned owners; the act between them does not.
- Where does declared variation in rigor belong — a compilation parameter of one recipe, a separate
  recipe revision, a separate recipe identity, or some other structure?
- Does the selection of one topology among several, which the prototype performs before compilation,
  belong inside the WGQ-9 pipeline? Until it resolves, the set of admitted source paths that the
  totality requirement quantifies over is not well defined.

## Next steps

1. Express the existing `domainspec-spec-feature` prototype in the v1 closed schemas and record
   exactly which constructs fail to map; the taxonomy evidence row now depends on it.
2. Decide whether the `workflow-graph` brief, still untracked, should be committed as a draft or
   held until the upstream boundary has an owner.

## Recommendation

The keystone is the first next step. It is the only item that tests the admitted node and edge kinds
from the skill side rather than the runtime side, and the prototype already supplies a real
obligation set with a source-coverage trace, so the work is bounded transcription plus an honest
record of what does not fit. Its licensing fact is that the prototype's vocabulary — `owns`,
`robot_talks`, `zig_zag`, `join`, `foreach`, bidirectional edges — is visibly disjoint from the v1
taxonomy, so the mismatch is already observable and only needs to be made precise.

## Files touched

- docs/discovery/workflow-graph/README.md
- telemetry/agents/subagents-dispatch.yaml
- sessions/2026-08-04-1327-workflow-graph-brief-additions.md
