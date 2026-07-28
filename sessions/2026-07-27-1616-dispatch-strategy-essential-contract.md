---
tags: [agent-orchestration, dispatch-strategy, multi-agent-work, workflow-governance]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-07-27T16:16:06-03:00
updated_at: 2026-07-27T16:16:06-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session recenters the work on the dispatch strategy and defines its proposed essential responsibility boundary before decomposition or implementation."
---

# Dispatch strategy essential contract

## Summary

The session began by examining how research artifacts, work context, hierarchy, and lineage might compose, but the owner identified that this exploration had moved away from the immediate objective. The work was explicitly recentered on improving `domainspec-subagents-strategy`, with `research` deferred as a later consumer and validation case. Context hierarchy, the tracking spine, ontology, and a generic skill compiler were parked unless a dispatch-strategy decision directly requires them. The proposed purpose of the strategy is to transform a work objective into an understandable, authorized, coherent multi-agent execution while preserving the objective through result recomposition. Its essential ownership is limited to deciding whether dispatch is warranted, organizing the division of work, exposing the proposed strategy for authorization, governing material changes, coordinating the authorized topology, and closing with a verified joined result. Type-specific epistemology, persisted record mechanics, runtime enforcement, and broader work-context modeling remain outside this skill and must be routed to their respective owners. No existing skill was changed; this is a proposed responsibility boundary to guide the next inspection and redesign.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | Improving the dispatch strategy is part of the infrastructure for governed agent work. |
| [Current dispatch strategy](../.agents/skills/domainspec-subagents-strategy/SKILL.md) | `refines` | The session proposes a smaller responsibility boundary against which the current skill can be inspected. |
| [Research type skill](../.agents/skills/research/SKILL.md) | `contextualizes` | Research is deferred as a type-specific consumer and later validation case for the improved router. |

## Open questions

- Which responsibilities in the current strategy are genuinely universal dispatch policy, and which belong to type skills, proposal tooling, persisted records, or runtime infrastructure?
- Is coordination of the authorized topology part of the strategy skill itself or only a contract delegated to the runtime?

## Next steps

1. Inspect the current `domainspec-subagents-strategy` by responsibility rather than by section.
2. Classify each responsibility as keep, route, or remove using the proposed boundary.
3. Propose the smallest revised skill structure before editing its contents.
4. Use `research` only after that structure is stable, as the first type-specific validation case.

## Recommendation

Start with the responsibility inventory because it tests the proposed boundary against the actual skill without prematurely selecting a new schema, workflow, or implementation.

## Files touched

- `sessions/2026-07-27-1616-dispatch-strategy-essential-contract.md`
