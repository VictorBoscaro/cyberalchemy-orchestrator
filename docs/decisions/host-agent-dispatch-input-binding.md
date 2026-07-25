---
status: accepted
date: 2026-07-25
scope: host-agent-dispatch-input-binding
related_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Host Agent Dispatch Input Binding

## Decision question

Which implementation boundary should make downstream host-agent inputs durable enough to run the
planned multi-stage research topology?

## Verified current state

- Every `Agent` or `spawn_agent` call is currently wrapped by
  `implementations/server/runtime/host_dispatch_hook.py` as its own compatibility Dispatch.
- The hook persists lifecycle opening and closing but does not receive a confirmed parent Dispatch,
  group, seat, prompt-template revision, or dynamic-slot manifest.
- The live runtime has a journal, immutable artifact store, capability resolution, orchestration
  bridge, and host hooks.
- `StartAgentAttempt`, `MaterializedAgentInvocation`, `AgentExecutionRequest`, and the general
  `EffectiveInputArtifact` pipeline remain specified but are not implemented.
- The host hook cannot observe every provider-side/system input and therefore cannot honestly claim
  to capture a complete `EffectiveInputArtifact`.

## Options

### A — Bounded host-workflow binding bridge (recommended)

Add an explicit, digest-bound launch envelope for the local Claude/Codex host hooks. It binds a
confirmed parent Dispatch, group, seat, frozen prompt template, data-only workflow input manifest,
and exact source/output artifact hashes before launch. Persist the host-observable manifest,
attempt binding, and returned output evidence without claiming complete provider input capture.

- Benefit: enables the planned research topology with a bounded local compatibility surface.
- Cost/risk: introduces a temporary bridge that must later map into the general ACI runtime.
- When to choose: immediate governed local multi-agent work is the priority.
- Downstream impact: new migration, hook envelope/parser, runtime binding service, lifecycle tests,
  and an explicit compatibility/non-correspondence statement.

### B — General ACI invocation pipeline

Implement the complete `AgentInvocationPlan -> MaterializedAgentInvocation +
EffectiveInputArtifact -> AgentExecutionRequest -> StartAgentAttempt` pipeline, including the
reveal, sandbox, authority-fence, outbox/recovery, provider and effect contracts.

- Benefit: builds the intended general architecture directly.
- Cost/risk: crosses TASK-030, TASK-040, and TASK-050; several dependencies and ADRs are not ready.
- When to choose: the research dispatch may wait for the general runtime program.
- Downstream impact: a multi-SWU program with additional owner decisions, security review, fake
  adapter proof, recovery testing, and later provider admission.

### C — Keep the runtime unchanged and segment the research

Run each handoff as a separately confirmed Dispatch, binding completed files and hashes as static
sources for the next Dispatch.

- Benefit: executable with the current bridge.
- Cost/risk: does not provide the requested single-Dispatch topology.
- When to choose: avoiding runtime mutation matters more than topology continuity.
- Downstream impact: more Dispatch records and confirmation boundaries, no new runtime code.

### Explain / more context

This is non-committal and leaves the gate blocked. Request it to expand the evidence, reversibility,
and implementation cone of each option.

## Current recommendation

Option A. It supplies the missing property for the immediate research wave while keeping the claim
strictly below a complete ACI/provider effective-input guarantee.

## Decision

Option A accepted from the repository owner's direction to repair the binding so the requested
single-Dispatch research topology can run. The bridge is intentionally bounded to host-observable,
repository-local inputs and outputs.

## Implemented boundary

- One already-confirmed parent Dispatch may declare multiple groups and seats.
- Each spawn/follow-up is persisted as a `host_workflow_turn_bindings` row and journal aggregate.
- A strict manifest binds each turn to exact repository-relative source bytes and SHA-256 digests.
- Follow-ups require a frozen prompt-template digest in the confirmed seat prompt and target the
  previously bound host agent.
- The parent Dispatch cannot close while any bound turn remains running.
- Bound turns do not append independent YAML Dispatch openings or closings.

## Explicit non-goals

- This bridge does not claim to capture hidden provider/system inputs.
- It is not the general `EffectiveInputArtifact` or `AgentExecutionRequest` pipeline.
- It does not replace the later TASK-030/040/050 implementation cone.
