---
tags: [agent-work, system-overview, editorial-progression, user-capabilities, provenance]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-12T17:57:06-03:00
updated_at: 2026-08-12T17:57:06-03:00
expires: 2026-10-11
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session corrected a material drift in how the project presents the purpose and reader progression of its external system overview."
---

# Work Overview Editorial Drift

## Summary

The repository objective is to keep agent work connected to the objectives, decisions, actions,
and evidence that give it meaning. This session set out to revise the external work-and-knowledge
overview so concepts would appear gradually, in precise scientific-business language, and receive
names only after their practical relations were understandable. The first review correctly found
that the document introduced plans, approval, infrastructure, observation, authority, and knowledge
too early, but the subsequent rewrite generalized the system into support for any composition of
work. The user rejected that rewrite because it drifted from the intended product framing: the
infrastructure exists to expand one person's capacity to organize and execute work with AI agents
while keeping that work understandable and controllable. The preferred progression now starts with
the objective and introduction, then explains what the user must be able to do before increasing
detail toward agent communication, governing contracts, and the provenance connecting execution
with knowledge. Agents remain local participants in the work rather than bearers of responsibility
for coordinating the surrounding system. A draft internal-tools package and a rewritten overview
were created, but the overview is not accepted and must be revised from the user-provided framing
rather than treated as the new baseline. The governed review runtime could not compile its connected
topology, so the review was performed through explicitly authorized direct read-only subagents and
was not represented as a governed dispatch.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure Plan](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The overview under revision explains the project direction governed by this Plan. |
| [Work and Knowledge System Overview](../plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md) | `contextualizes` | This session records why the current rewritten draft was rejected and which framing should guide its next revision. |

## Open questions

- How much of the rejected rewrite can be retained without weakening the restored framing around one
  person's capacity to work through AI agents?
- At which exact points should `dispatch`, agent communication, governing contracts, knowledge, and
  provenance receive their names in the revised progression?

## Next steps

1. Rewrite the overview from the user's supplied `Objective`, `Introduction`, and `User capabilities`
   framing rather than incrementally repairing the rejected generalization.
2. Preserve the gradual increase in detail while keeping the product subject stable: one person
   organizing and executing more complex work through AI agents.
3. Review the resulting draft against the user-provided passage before extending the internal skill.
4. Reconcile the essays index title only after the overview title and framing are accepted.

## Recommendation

Treat the user's supplied passage as the new editorial anchor and validate the next draft section by
section before performing another whole-document rewrite.

## Files touched

- `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md`
- `plans/governed-agent-work-infrastructure/essays/README.md`
- `internal-tools/need-driven-system-writing/README.md`
- `internal-tools/need-driven-system-writing/INITIAL-REVIEW.md`
- `sessions/2026-08-12-1757-work-overview-editorial-drift.md`
