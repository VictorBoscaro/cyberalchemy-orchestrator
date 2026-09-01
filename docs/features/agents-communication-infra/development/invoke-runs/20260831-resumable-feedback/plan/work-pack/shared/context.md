# Shared Context

## Objective

After human confirmation, execute one finite author-reviewer-author feedback graph from journal facts
without the chat orchestrator supervising or either agent polling the bus.

## Controlling sources

- [ACI-CONT-001](../../../../../../../../decisions/aci-resumable-agent-continuation.md)
- [Capability](../../../../../../specs/capabilities/resumable-agent-continuation.md)
- [Operations](../../../../../../specs/operations.md#suspendagentcontinuation)
- [Lifecycle](../../../../../../specs/states.md#agentcontinuationlifecycle)
- [TEST-SPEC](../../../../../../TEST-SPEC.md#bounded-resumable-feedback)
- [Architecture](../../../../../../specs/architecture.md#bounded-feedback-continuation)
- [Layering](../../implementation-layering.md)

## Existing implementation seams

- `implementations/server/runtime/journal.py`: atomic command/event/head acceptance.
- `implementations/server/runtime/service.py`: current command validation and multi-row transactions.
- `implementations/server/runtime/reveal_delivery.py`: deterministic effective-input construction model.
- `implementations/server/runtime/migrations/001_aci_slice0.sql` through `011_bus_reveal_delivery.sql`:
  ordered SQLite migration baseline.
- `implementations/tests/runtime/test_bus_reveal_delivery.py`: failpoint and atomic materialization patterns.

## Hard constraints

- No Schema Service work.
- No host `WorkflowInputManifest` reuse for continuation input.
- No provider-memory-only correctness, generic inbox, bus polling or unbounded loop.
- No real Codex adapter in L0/L1.
- Preserve unrelated dirty-worktree changes.
- Each mutation SWU uses two read-only auditors, one coder and one independent verifier.
