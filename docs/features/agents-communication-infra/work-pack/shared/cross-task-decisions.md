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
| D-106 | The bounded APT vertical slice uses one ACI SQLite authority, ACI ArtifactStore and ACI ProjectionManager; it never writes the audit ledger. | ADR-002 and storage policy; exact named-SWU receipt required. |
| D-107 | Test mutation and local-pilot serving are separate gates; production, external network, provider execution, materializer and cutover stay blocked. | `SWU-ACI-APT-VS-001` descriptor and W0 closure packet. |
| D-108 | A publication candidate becomes official only in an atomic parent-verification command that writes the official event and unique `messages` fact. | ADR-002; candidate/receipt/message fault tests. |
| D-109 | Runtime authority comes from opaque server-side capability resolution; HTTP/loopback and request bodies never supply identity, phase or scope. | Exact capability profile in the named SWU. |
| D-110 | Four immutable digest-bound profiles are required, including reference-probe because the selected outcome includes official probe lineage. | Profile registry; removing implementation removes the profile and claim. |
| D-CVR-001 | Keep CVR as a transport-neutral L0 adjunct under `implementations/vault_read/`, delivered as documentation, artifacts plus raw declarations, then endpoint/logical edges. | Named owner/root acceptance of the exact ApprovalPacket; CVR-001 proves source projection/preservation before CVR-002 extends the same core. |
| D-CVR-002 | Use an empty-default host policy and an exactly pinned restricted YAML loader, with source bytes authoritative over inventory. | Host/operator and architecture acceptance plus reproducible pin/loader goldens. |
| D-CVR-003 | A named CVR authorization is single-use and exact-scope; prepared status and the proposed predicate are non-pass/non-operative. | Root approves/requests cancellation only; one external bootstrap finalizer completes GUARD, while the common guard/finalizer exclusively completes CVR-001/002. |
| D-CVR-004 | Use staged privacy admission, operation-specific capture and typed/versioned canonical JSON digests. | Privacy precedence, unrelated-source get, parser-ceiling and exact-byte golden fixtures. |
| D-CVR-005 | Bind acceptance to four shared documents plus one deterministic closed descriptor. | Descriptors are immutable governance entries, not per-execution artifacts. |
| D-CVR-006 | Sequence `000 -> GUARD-001 -> 001 -> 002`; bootstrap GUARD non-recursively with an external trusted executor. | No self-authorization or integration surface enters the carve-out. |
| D-CVR-007 | Persist exactly one content-addressed authorization, claim and applicable authority-owned `ExecutionReceipt` per execution: the external bootstrap finalizer owns GUARD completion, while the common guard/finalizer owns CVR-001/002 completion. | No execution has two finalizers; no current pointer, revocation artifact, ClaimReceipt or second receipt; withdrawal is pre-claim and cancellation terminalizes. |
| D-CVR-008 | CVR-002 binds CVR-001 PASS receipt/baseline, allowed delta and pre-write hashes and reruns CVR-001 tests. | Edge work cannot silently mutate or regress the artifact layer. |

## Decision discipline

- Decisions that change authority, data loss behavior, retry semantics or public contracts require
  an ADR before code.
- A later wave may supersede a decision only with migration and compatibility consequences.
- Provider and business semantics never silently revise kernel decisions.
