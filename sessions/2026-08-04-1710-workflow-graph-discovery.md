---
tags: [workflow-graph, upstream-results, digest-binding, release-authority, dispatch-spec]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-04T17:10:48-03:00
updated_at: 2026-08-04T17:10:48-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session separates existing digest validation from the missing canonical acceptance-and-release chain and prevents premature workflow-schema promotion."
---

# Workflow graph discovery and upstream result binding

## Summary

The repository objective is to keep delegated work connected to the authority, decisions, and evidence that make its results usable downstream. This session set out to determine whether the project lacks the extension required to connect upstream returns by digest and what that claim means for Workflow Graph. The evidence contradicted the broad claim because the current runtime already validates a declared producer binding, artifact path, SHA-256 digest, size, and terminal producer state. It supported the narrower concern because completion records, workflow compilation, and connection handling do not yet form a canonical chain from owner-accepted result to downstream release and consumed input. A confirmed [discovery intention](../docs/discovery/workflow-graph/discovery-intention.md) bounded the work to discovery rather than implementation or schema promotion. The resulting [Workflow Graph discovery](../docs/discovery/workflow-graph/workflow-graph.md) proposes separate definition, owner-fact, derived-state, communication-policy, and provenance responsibilities while marking all ten investigation questions as retaining recommendation-blocking requirements. Two independent reviewers examined the discovery in two rounds and caused corrections to WGQ disposition, Attempt cardinality, collective coordination, rework, projection equivalence, and owner mappings. The second-round corrections were applied after the agreed ceiling without a third terminal review, so the outcome remains inconclusive and no candidate was promoted.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Workflow Graph discovery](../docs/discovery/workflow-graph/workflow-graph.md) | `contextualizes` | This session records the motivating claim, evidence boundary, independent review, corrections, and reason the discovery remains inconclusive. |

## Open questions

- Which component canonically owns workflow topology and the general `AcceptedOutputRef`, and how is that authority preserved through `DispatchSpec` compilation?
- How do `RoutingPlan`, Work Bus visibility and delivery, ACI input acceptance, and workflow release compose without making a dependency edge an implicit communication grant?
- Which closed node, connection, collective-coordination, completion, rework, and projection contracts survive independent witnesses and equivalence tests?

## Next steps

1. Resolve OQ-WG1, OQ-WG2, and OQ-WG6 in a joint Workflow Graph, Work Bus, ACI, and dispatch architecture decision.
2. Amend the discovery with the selected owners and total source-to-destination mappings, then close or reclassify every WGQ against new evidence.
3. Author an executable schema only after the recommendation-blocking questions and terminal independent review are closed.

## Recommendation

Prioritize the joint ownership decision: until topology, accepted result, communication policy, and downstream release each have one explicit authority and total mappings between them, further schema work would encode the disputed boundary rather than resolve it.

## Files touched

- `docs/discovery/workflow-graph/discovery-intention.md`
- `docs/discovery/workflow-graph/workflow-graph.md`
- `sessions/2026-08-04-1710-workflow-graph-discovery.md`
