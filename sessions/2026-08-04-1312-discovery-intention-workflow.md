---
tags: [dispatch-spec, workflow-graph, discovery-intention, agent-orchestration]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-04T13:12:53-03:00
updated_at: 2026-08-04T13:12:53-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session separated participant, workflow, communication, and completion semantics and added the framing gate required before future discoveries harden those distinctions."
---

# DispatchSpec, Workflow Graph, and Discovery Intention

## Summary

The repository seeks to keep agent execution connected to confirmed objectives, decisions, authority, and evidence rather than relying on implicit chat coordination. This session began by clarifying what the current `DispatchSpec` receives, where it is defined, and why its open `object` fields do not yet explain how a `DispatchCandidate` becomes executable. Inspection and independent review established that agents, seats, workflow nodes, attempts, communication routes, collective coordination, and terminal outcomes must remain distinct until their mappings are explicitly decided. The user chose an envelope-oriented direction with dispatch information, per-agent initialization, workflow dependencies, communication authorization, resources, budgets, and completion semantics. The agents-communication discovery was updated with a non-ratified `DispatchSpec` decomposition and eight smaller OQ-ACP3 settlement questions, while preserving the existing ownership boundary. A repository-wide [workflow graph brief](../docs/discovery/workflow-graph/README.md) was then created to ask whether execution is one graph or a composition of protocol topology, confirmed workflow, runtime state, communication, coordination, and completion. The next design step identified that a discovery itself should not be the first durable record of why understanding is needed. A new local `discovery-intention` skill and validator were created under `.agents`, and `discovery-writing` now requires an active framing intention for new or materially reframed discoveries while retaining an explicit legacy mode. Validator and forward-test objections closed bypasses involving optional enforcement, incomplete intention validation, use of intentions as evidence, agent-subject ambiguity, and owner/supersession lifecycle. Two independent subagents ultimately returned `NO_OBJECTION`, and `.claude` was deliberately left unchanged for a later controlled synchronization.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Protocols discovery](../docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md) | `refines` | This session decomposed the open candidate-to-DispatchSpec problem without promoting a normative schema. |
| [Workflow Graph discovery brief](../docs/discovery/workflow-graph/README.md) | `contextualizes` | This session records why the repository-wide graph investigation was opened and which distinctions motivated it. |

## Open questions

- What exact cardinalities and identities relate `agent_id`, `Seat`, workflow node, runtime agent instance, and `Attempt`?
- Will every downstream pipeline accept the new repository-wide discovery path, or does its owning contract still require promotion?
- Should the existing workflow-graph README be distilled into the first formal `discovery-intention`, or explicitly retained as a richer antecedent with a separate concise intention?

## Next steps

1. Merge the `.agents` `discovery-intention` package and `discovery-writing` changes into `.claude` without deleting the additional review/provenance rules already present there.
2. Validate the synchronized `.claude` skills and run the same intention and discovery validator self-tests.
3. Use the workflow-graph topic as the first end-to-end `discovery-intention` case, obtain owner confirmation, and only then begin its discovery.
4. Resolve the workflow identity, topology, coordination, communication, completion, and total-mapping questions before promoting a closed `DispatchSpec` schema.

## Recommendation

Synchronize and validate the skills first, then use workflow graph as the proving case; this tests whether the new framing boundary prevents both premature architecture and duplicate sources of purpose.

## Files touched

- `.agents/skills/discovery-intention/SKILL.md`
- `.agents/skills/discovery-intention/agents/openai.yaml`
- `.agents/skills/discovery-intention/scripts/validate-discovery-intention.py`
- `.agents/skills/discovery-writing/SKILL.md`
- `.agents/skills/discovery-writing/scripts/validate-discovery.py`
- `.codex/workflow-inputs/2026-08-04-dispatchspec-agent-graph-review/`
- `.codex/workflow-inputs/2026-08-04-dispatchspec-agent-graph-review-r2/`
- `docs/discovery/README.md`
- `docs/discovery/workflow-graph/README.md`
- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-04-1312-discovery-intention-workflow.md`

