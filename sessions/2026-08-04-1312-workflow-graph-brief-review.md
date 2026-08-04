---
tags: [workflow-graph, dispatch-spec, authority-boundaries, runtime-state, discovery-governance]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-04T13:12:06-03:00
updated_at: 2026-08-04T13:12:06-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "The session hardens the investigation contract required before workflow topology can become confirmed DispatchSpec authority."
---

# Workflow graph discovery brief review

## Summary

The repository objective is to keep agent execution connected to distinct objectives, decisions, authorities and evidence across compilation, confirmation and runtime. This session set out to explain and critically assess the workflow-graph discovery brief, then revise it without prematurely selecting an architecture. The review agreed that the actual proposal is a governed investigation into whether workflow structure, execution authority, allocation, communication, coordination and runtime state require one graph or a composition of structures. It found that the brief did not initially make “smallest” decidable, treated a draft Bus Contracts discovery too strongly as an owner, left destination provenance uncovered and lacked a strict recommendation gate. The brief was revised to separate five semantic dimensions, require bidirectional mappings and unique fact ownership, protect ratified authority boundaries, trace output acceptance through release and completion, and compare alternatives against explicit gates and evidence. Two independent reviewers then challenged the revision through three zig-zag rounds, surfacing and driving corrections for authority collapse, composite provenance, release ownership, blocker classification and incomplete counterexamples. The resulting brief requires dispositions for all ten investigation questions, decision-to-evidence traceability and 23 counterexamples before any `DispatchSpec` schema recommendation. The third-round objections were incorporated, but the loop ceiling prevented a further independent check of those final edits, so the brief remains a draft investigation contract rather than validated architecture.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Workflow Graph — Discovery Brief](../docs/discovery/workflow-graph/README.md) | `refines` | This session critically reviewed and hardened the brief's evidence, authority, mapping, counterexample and exit requirements. |

## Open questions

- Which executable representation survives the discovery: one canonical graph with projections, multiple mapped graphs, or a topology combined with policies and state machines?
- Which transformations may confirmation apply between `DispatchCandidate` and `DispatchSpec` without weakening lineage or creating authority implicitly?

## Next steps

1. Run a fresh independent review of the final third-round edits before treating the brief as the stable investigation contract.
2. Execute the evidence inventory and candidate comparison required by the brief in `workflow-graph.md`.

## Recommendation

Use the revised brief to govern the actual discovery, and do not promote a `DispatchSpec` graph schema until every recommendation gate is satisfied or explicitly blocks promotion.

## Files touched

- `docs/discovery/workflow-graph/README.md`
