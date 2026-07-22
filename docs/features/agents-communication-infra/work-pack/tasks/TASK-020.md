# TASK-020 — Audit-ledger materialization and reconciliation

## Objective

Bridge journal facts to official audit-ledger opening/closing without creating a second writer or
pretending SQLite and YAML share a transaction.

- **Layer/slice:** L0-L1 / S-001-S-002 / W1-W2.
- **Dependencies:** TASK-000 and journal/outbox portions of TASK-010.
- **Proposed write scope:** `implementations/server/runtime/materializers/`, runtime contract tests;
  the appender is read/invoked but not replaced.

## Algorithm

```text
claim effect intent durably
derive canonical v0.6.1 row from frozen spec/terminal event
inspect ledger through a verification adapter
if identical row exists: record verified acknowledgement
if same identity differs: record reconciliation_required and stop
if absent: invoke append-dispatch.cjs with a temporary validated record
re-read and compare exact normalized row
if identical: record verified acknowledgement
else: retain pending/reconciliation state; never unlock execution/closed status
```

The adapter must distinguish the appender's current ID-only no-op from proof that the existing row
is identical. A subprocess exit code alone is not acknowledgement.

## Smallest Working Units

### SWU-ACI-005 — Opening materializer

- **Write scope:** opening materializer, verification port, fixtures/tests.
- **Done when:** `opening.verified` is the only transition to `ready`; failures and divergent rows
  cannot enqueue/start fake execution.
- **Faults:** crash before call, after YAML append, before journal acknowledgement and during re-read.

### SWU-ACI-006 — Close materializer

- **Dependencies:** opening materializer and terminal mapping ADR.
- **Done when:** `execution_terminal` becomes `close_pending`; only verified close becomes `closed`;
  one terminal/exit reason wins; identical retry adds no row.
- **Faults:** divergent close, absent opening, appender failure and crash after physical append.

### SWU-ACI-007 — EG-1 writer guard and golden compatibility

- Scan/guard runtime code against direct audit-ledger write APIs and paths.
- Produce the complete target-host `SoleWriterEvidenceBundle`: process identity, filesystem ACL,
  writer inventory and negative bypass tests; record single-import lint only as auxiliary evidence.
- Compare runtime-produced rows to golden rows from the legacy appender.
- Record the historical drift disposition before materializer cutover.

This SWU consumes the W0-frozen bundle schema, drift disposition, guard specification and named
tests. It owns the complete physical target-host proof; neither this proof nor materializer cutover
is a dependency of TASK-010 journal implementation.

## Done when

Crash recovery converges, identical rows count as applied, divergent rows require repair, and the
adapter start spy remains zero until opening acknowledgement is persisted.

## DomainSpec Coverage

| Source Aspect | Coverage IDs |
|---|---|
| `domain.md` | `agents-communication-infra.ReconciliationState` |
| `workflows.md` | `agents-communication-infra.AuditLedgerMaterializer`, `agents-communication-infra.ExternalEffectReconciliationWorkflow` |
| `mappings.md` | `agents-communication-infra.FrozenAuthorityToAuditLedgerRow`, `agents-communication-infra.RuntimeTerminalToExitReason` |
| `interfaces.md` | `agents-communication-infra.AuditLedgerAppenderPort` |
| `domain.md` | `agents-communication-infra.SoleWriterEvidenceBundle` |
