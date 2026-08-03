---
tags: [agent-orchestration, dispatch-routing, workflow-binding, telemetry]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-03T14:06:39-03:00
updated_at: 2026-08-03T14:06:39-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: [implementations/contracts/dispatch-type-registry.v1.json, .claude/skills/domainspec-subagents-strategy/SKILL.md, .claude/skills/subagents-dispatch-lifecycle/SKILL.md, .claude/skills/register-dispatch/SKILL.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session converted the subagent entrypoint from an abstract router into a tested path that resolves one canonical type, opens one parent dispatch, binds its seats and closes it through the existing infrastructure."
---

# Operational Subagent Dispatch Entrypoint

## Summary

The repository seeks to preserve the connection from an objective and human decision through delegated work to registered evidence. This session set out to determine whether the simplified subagent strategy still selected a real dispatch type, registered work through the infrastructure and launched agents with the intended host bindings. The audit contradicted the earlier confidence: `dispatch_type` had become implicit, the lifecycle could double-register a parent and compatibility children, and the documented runtime-managed tools were not implemented. The decision was to make one machine-readable infrastructure registry the sole owner of dispatch types, status, capability mapping, authority modes and ledger projections, while keeping the strategy responsible only for routing. A deterministic `dispatch_workflow` adapter now resolves routes, compiles turn-zero manifests and `ACI-WORKFLOW-BINDING-V1` envelopes, opens the parent through the bridge and sole appender, and closes it only after bound seats terminate. The bridge, hook and appender now consume the registry instead of maintaining independent enums, and RESERVED types fail closed rather than being recorded with a warning. The entrypoint, lifecycle and register skills were rewritten around concrete commands and receipts, with active `.agents` mirrors synchronized. An integrated test proved one parent opening, one bound seat and one parent close without an orphan compatibility row, while the complete runtime suite passed 108 tests and the sealed source manifest reported zero mismatches. The current executable profile remains `host/inherited@1`; custom tool-profile enforcement and governed follow-up-turn compilation remain explicit future work rather than claimed capabilities.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Infrastructure](../docs/features/agents-communication-infra/README.md) | `is-part-of` | The implemented registry and legacy dispatch adapter are a current operational capability inside the broader ACI feature. |
| [Canonical Dispatch Authority Discovery and Review](2026-08-03-1322-canonical-dispatch-authority-review.md) | `derives-from` | This session operationalized the single-parent authority and turn-zero binding seam exposed by the earlier review while preserving its unresolved follow-up boundary. |

## Open questions

- What host/runtime contract will enforce custom tool profiles rather than merely identify the inherited host surface?
- What governed compiler operation should materialize `turn_ordinal > 0` bindings with exact producer-output manifests?

## Next steps

1. Add a governed follow-up compilation command that binds an existing terminal agent, frozen prompt template and producer-output manifest.
2. Add runtime capability-resolution receipts before advertising any tool profile other than `host/inherited@1`.
3. Replace the legacy-managed adapter with the same registry-backed contract when the runtime-managed ACI command surface becomes executable.

## Recommendation

Use the new legacy-managed route immediately for independent turn-zero seats, and treat follow-ups or custom tool profiles as unavailable until their enforcement receipts are implemented and tested.

## Files touched

- `.agents/skills/domainspec-subagents-strategy/SKILL.md`
- `.agents/skills/domainspec-subagents-strategy/agents/openai.yaml`
- `.agents/skills/register-dispatch/SKILL.md`
- `.agents/skills/register-dispatch/append-dispatch.cjs`
- `.agents/skills/register-dispatch/agents/openai.yaml`
- `.agents/skills/subagents-dispatch-lifecycle/SKILL.md`
- `.agents/skills/subagents-dispatch-lifecycle/agents/openai.yaml`
- `.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `.claude/skills/domainspec-subagents-strategy/agents/openai.yaml`
- `.claude/skills/register-dispatch/SKILL.md`
- `.claude/skills/register-dispatch/append-dispatch.cjs`
- `.claude/skills/register-dispatch/agents/openai.yaml`
- `.claude/skills/subagents-dispatch-lifecycle/SKILL.md`
- `.claude/skills/subagents-dispatch-lifecycle/agents/openai.yaml`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `implementations/contracts/dispatch-type-registry.v1.json`
- `implementations/server/runtime/dispatch_types.py`
- `implementations/server/runtime/dispatch_workflow.py`
- `implementations/server/runtime/host_dispatch_hook.py`
- `implementations/server/runtime/local_pilot.py`
- `implementations/server/runtime/orchestration_bridge.py`
- `implementations/tests/runtime/test_agent_reference_delivery.py`
- `implementations/tests/runtime/test_dispatch_workflow.py`
- `implementations/tests/runtime/test_host_dispatch_hook.py`
- `implementations/tests/runtime/test_host_ingestion_hook.py`
- `implementations/tests/runtime/test_host_workflow_binding.py`
- `implementations/tests/runtime/test_orchestration_bridge.py`
- `sessions/2026-08-03-1406-operational-subagent-dispatch-entrypoint.md`
