# TASK-030 — Fixed protocol with deterministic fake adapters

## Objective

Complete the first vertical run after the lifecycle bridge is proven: confirm a frozen spec, execute
two deterministic seats, commit one result and close officially.

- **Layer/slice:** L0 / S-001 subgates 0D-0E / W1.
- **Dependencies:** TASK-010 and opening portion of TASK-020.
- **Proposed write scope:** `implementations/server/runtime/application/`,
  `implementations/server/runtime/adapters/fake.py`, runtime API/query modules and E2E tests.

## Protocol

```text
confirmed -> opening_pending -> ready
ready -> collecting -> revealing -> voting -> committing
committing -> execution_terminal -> close_pending -> closed
```

The fixed fake returns fixture-defined structured positions/votes. Start requires a durable claimed
effect intent and `opening.verified`. A repeated start/result creates no second logical contribution.

## Smallest Working Units

### SWU-ACI-008 — Fake adapter and durable worker loop

- Define `start/events/result/cancel/status` port, implementing only the subset needed by L0.
- Worker startup scans pending intents, claims by operation/attempt/epoch, executes and records an
  observation command; replay itself never scans or executes.
- Test same attempt+digest reconciliation and different digest conflict.

### SWU-ACI-009 — Fixed group kernel

- Add two seats and fixed `collect -> reveal -> vote -> commit` transitions on top of the proven
  lifecycle bridge; enforce one position/vote per seat/round.
- Persist reveal manifest/hash before peer visibility changes.
- Use the ADR-selected rule; preserve dissent in the committed envelope.

### SWU-ACI-010 — Confirm/query integration and explicit cutover mode

- Freeze bytes/digest of a valid pending sheet at confirm; later sheet mutation conflicts.
- Route runtime-managed confirmation through command service while preserving legacy API response
  compatibility; prevent both legacy watcher and runtime worker owning one dispatch.
- Freeze the exact sheet before the legacy cleanup convention can delete the pending JSON/marker;
  cleanup becomes a retryable compatibility effect after opening is verified.
- Add run query exposing distinct `ready`, `running`, `execution_terminal`, `close_pending`, `closed`
  and `reconciliation_required` states.

### SWU-ACI-011 — L0 E2E and crash matrix

- Restart after every journal, claim, appender and acknowledgement boundary.
- Re-deliver commands, fake results and materializer intents N times.
- Assert stable state hash, one logical result/terminal and one official opening/close.
- Verify existing reader/endpoint tests remain green and document rollback to legacy mode.

## Done when

All L0 falsifiers pass and the result explicitly states what fake execution does not prove: real
provider reconciliation, process sandboxing, alternate-channel sealing and product value.

## DomainSpec Coverage

| Source Aspect | Coverage IDs |
|---|---|
| `domain.md` | `agents-communication-infra.ConfirmedDispatch`, `agents-communication-infra.Group`, `agents-communication-infra.Seat`, `agents-communication-infra.Attempt`, `agents-communication-infra.GroupResult`, `agents-communication-infra.SeatId`, `agents-communication-infra.AgentInvocationPlan`, `agents-communication-infra.MaterializedAgentInvocation`, `agents-communication-infra.AgentTerminalResult` |
| `operations.md` | `agents-communication-infra.ConfirmRuntimeDispatch`, `agents-communication-infra.StartAgentAttempt`, `agents-communication-infra.CommitGroupResult` |
| `queries.md` | `agents-communication-infra.GetRunStatus` |
| `states.md` | `agents-communication-infra.GroupLifecycle`, `agents-communication-infra.AttemptLifecycle` |
| `interfaces.md` | `agents-communication-infra.RuntimeCommandAPI` |
| `workflows.md` | `agents-communication-infra.RunExecutionWorkflow`, `agents-communication-infra.GroupDeliberationWorkflow`, `agents-communication-infra.ExecutionAuthorityCutoverWorkflow` |
