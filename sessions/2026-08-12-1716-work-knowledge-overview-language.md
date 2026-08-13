---
tags: [agent-work, knowledge, observability, recursive-orchestration, technical-writing]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-12T17:16:10-03:00
updated_at: 2026-08-12T17:16:10-03:00
expires: 2026-10-11
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session made the proposed system easier to understand while exposing a direct conflict in its orchestration model."
---

# Work and knowledge overview language

## Summary

The repository needs a system overview that connects agent work to the objectives, authority, evidence, and knowledge that give it meaning. This session revised that overview so a first-time reader can first understand the problem, then imagine using the system, and only afterward examine its structure. The system is now described as ephemeral infrastructure created for a specific body of agent work, while its event history and accepted knowledge persist after execution ends. User and system shape the work together; the system maintains the approved dispatch and returns decisions that exceed delegated authority. Orchestrator is defined as a participant role that may invoke another orchestrator within a configurable depth limit, with one nested level recommended initially. A separate observation layer reads the growing event history to show current work and to reconstruct past execution from the same records. The prose was revised to replace vague claims about judgment and trust with explicit statements about goals, approvals, evidence, and recorded events. The `write-need-driven-documents` skill was updated to require careful naming and concrete but lively language while rejecting rhetorical catalogues and mechanical simplification. The revised orchestration model contradicts the companion system view, which still forbids nested orchestrator invocation and therefore needs an explicit design decision before the documents can be aligned.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The session revises the project-level explanation of the infrastructure proposed by this Plan. |
| [Infrastructure for AI Agent Work](../plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md) | `contextualizes` | The session records the decisions and editorial reasoning behind the overview revision. |
| [A Composable Language for Governed Agent Work](../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md) | `contradicts` | The overview allows nested orchestrator invocation under a depth limit, while this system view prohibits it. |

## Open questions

- Should recursive orchestrator invocation replace the existing no-nested-orchestrator rule, or should the overview distinguish a different kind of nested planning role?
- Which parts of the system are created and removed with each body of work, and which shared services remain available across work?

## Next steps

1. Resolve the recursive-orchestration contradiction before revising the companion system view or treating the overview as an aligned architecture statement.
2. Review the complete overview for a consistent balance between plain language and an engaging voice.
3. Define the boundary between ephemeral work infrastructure and persistent shared infrastructure once the high-level model is stable.

## Recommendation

Resolve the orchestrator recursion rule first, because it changes the authority model and the meaning of the nesting diagram.

## Files touched

- `.agents/skills/write-need-driven-documents/SKILL.md`
- `.codex/skills/write-need-driven-documents/SKILL.md`
- `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md`
- `sessions/2026-08-12-1716-work-knowledge-overview-language.md`
