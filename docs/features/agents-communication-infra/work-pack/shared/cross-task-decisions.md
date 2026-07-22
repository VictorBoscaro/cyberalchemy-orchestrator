# Cross-Task Decisions

## Locked

| ID | Decision | Consequence |
|---|---|---|
| D-001 | `agents-communication-infra` owns the runtime feature. | Runtime implementation is a module boundary, not a new feature boundary. |
| D-002 | Migrate incrementally; preserve the legacy path until a tested cutover. | Every slice supplies compatibility and rollback evidence. |
| D-003 | Journal owns workflow facts; the audit ledger owns official opening/closing. | Cross-store work uses outbox, verification and reconciliation rather than shared transactions. |
| D-004 | The current appender remains the sole audit-ledger physical writer. | Materializers invoke it and independently verify exact persisted content. |
| D-005 | Replay is pure. | Replay never invokes reactors, appender, adapter, clock or tools. |
| D-006 | Begin with deterministic fake effects. | Provider nondeterminism cannot mask persistence/kernel failures. |
| D-007 | MVP is single-host and single-tenant. | SQLite/WAL and durable local claims are eligible; distributed leases are not. |
| D-008 | Runtime host remains Python/FastAPI; Pydantic core validates boundary models only. | Canonical projection, JSON bytes and SHA-256 sealing remain runtime-owned. |
| D-009 | First real provider is a local subprocess adapter behind `SandboxLauncher`. | Fake and host-specific admission evidence precede registration. |
| D-010 | Octopus Runtime and Eve are reference-only; PydanticAI is deferred; Zod is derived-boundary-only. | No external tool receives kernel or authoritative-store ownership. |
| D-011 | Single-import lint is auxiliary EG-1 evidence. | Only a complete `SoleWriterEvidenceBundle` can close the sole-writer proof. |
| D-012 | W0 freezes the sole-writer evidence schema, drift disposition, guard specification and tests; TASK-020 proves them physically on the target host. | TASK-010 journal work is not circularly blocked by materializer/cutover evidence; the materializer and cutover remain blocked until the proof passes. |
| D-102 | One monotonic journal offset per SQLite database and one contiguous aggregate version per aggregate. | Accepted by ADR-001 for the W0 decision scope; TASK-010 must prove executable conformance. |
| D-103 | `same idempotency_key + same command digest` returns the original receipt; a different digest is a permanent conflict. | Accepted by ADR-001 with canonical vectors; TASK-010 must prove receipt and crash behavior. |

## Proposed in this plan; accept or amend in W0

| ID | Proposal | Acceptance evidence |
|---|---|---|
| D-101 | Put runtime code under `implementations/server/runtime/`. | Dependency review shows it can coexist with reader APIs without circular imports. |
| D-104 | Expose distinct lifecycle states: `confirmed`, `opening_pending`, `ready`, `running`, `execution_terminal`, `close_pending`, `closed`, `reconciliation_required`. | Transition table and API schema. |
| D-105 | Slice 0 is internally gated as 0A contracts, 0B journal, 0C opening barrier, 0D fake execution/close, then 0E fixed group protocol. | Each sub-gate has an independent falsifier and receipt. |

## Decision discipline

- Decisions that change authority, data loss behavior, retry semantics or public contracts require
  an ADR before code.
- A later wave may supersede a decision only with migration and compatibility consequences.
- Provider and business semantics never silently revise kernel decisions.
