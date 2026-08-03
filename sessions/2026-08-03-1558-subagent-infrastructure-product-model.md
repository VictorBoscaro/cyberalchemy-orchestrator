---
tags: [subagents, agent-work, infrastructure, product-model, dispatch]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-03T15:58:37-03:00
updated_at: 2026-08-03T15:58:37-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "This session establishes the product-level frame from which the target architecture, services, contracts, and implementation slices will be derived."
---

# Subagent Work Infrastructure Product Model

## Summary

This session connected the repository's objective of keeping agent work tied to purpose, authority, action, and evidence to a new product-level model for subagent infrastructure. Its objective was to create a fresh branch and charter for reasoning from the intended final system rather than adapting the current implementation. The product was framed as a unified platform for organizing, authorizing, executing, validating, observing, and recovering structured work performed by subagents. We decided that a graph is one component of the system, while confirmed Dispatches, autonomous runtime execution, governed communication, prompts, events, artifacts, history, and relational observability belong to the wider product. We established ten product capabilities (`PC-1` through `PC-10`), ten supporting system properties (`SP-1` through `SP-10`), and an initial trace from capabilities to properties that will later extend to services, contracts, and evidence. We corrected two earlier premises: execution requires trusted human confirmation of the concrete workflow, and the infrastructure must actually run that confirmed workflow without relying on the chat agent as an implicit scheduler or message relay. The branch charter now begins with the product problem, explains the capabilities and their value, and derives the properties that the eventual architecture must guarantee. Existing material under `/plans` supplied useful context for prompt, record, fabric, event, input-manifest, and launcher responsibilities, but was not adopted as binding target architecture. The next artifact must derive a detailed high-level system model and candidate service responsibilities from the accepted product capabilities and properties before JSON schemas or implementation design begin.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Subagent Work Infrastructure](../plans/autonomous-agent-graph-system/README.md) | `is-part-of` | This session established and refined the product framing and branch charter represented by the README. |

## Open questions

- Which service boundaries are actually required to enforce the accepted `SP-*` properties without creating a monolith?
- What are the minimum authoritative contracts for workflow proposal, confirmation, Dispatch, Run, agent invocation, bus message, event, artifact, and terminal result?
- How should description-only tasks obtain a reusable or task-specific workflow without allowing an agent to silently create its own authority?
- Should the branch and directory be renamed now that the target is broader than an autonomous graph system?

## Next steps

1. Write the detailed high-level target model, deriving candidate service responsibilities from `PC-*` and `SP-*`.
2. Walk one read-only workflow and one artifact-producing workflow through the model before defining schemas.
3. Extend the traceability chain from `PC → SP` to `service → contract → test and operational evidence`.
4. Settle the product, workflow, Dispatch, message, event, and artifact vocabulary before implementation planning.

## Recommendation

Keep `PC → SP → service → contract → evidence` as the controlling derivation: introduce no service or payload field unless it supports an accepted product capability and has a named authority and validation boundary.

## Files touched

- `plans/autonomous-agent-graph-system/README.md`
- `sessions/2026-08-03-1558-subagent-infrastructure-product-model.md`
