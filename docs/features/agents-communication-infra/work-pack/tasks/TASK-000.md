# TASK-000 — Freeze Slice-0 contracts

## Objective

Resolve every decision that would otherwise be encoded accidentally in persistence, state or
migration code. This task authorizes contracts, not runtime implementation.

- **Layer/slice:** L0 / S-000 / W0.
- **Sources:** feature README sections 4.1-4.3, 9.1, 12, 14 and 17; engine constitution EG-1.
- **Gate:** ready for documentation work; blocks all runtime-code tasks.

## Smallest Working Units

### SWU-ACI-001 — Persistence and replay ADR

- **Status:** complete for its W0 decision scope; accepted by the
  [independent review receipt](../../reviews/2026-07-21-swu-aci-001-implementation/REPORT.md).
- **Boundary:** this closes only `SWU-ACI-001`; `TASK-000`, all runtime gates and downstream
  executable conformance remain open.

- **Dependencies:** none.
- **Write scope:** `docs/features/agents-communication-infra/adrs/`, decision/gap ledgers.
- **Inputs:** OQ-PERSISTENCE, OQ-STREAM, D-102, D-103.
- **Additional inputs:** OQ-ETA1 and ETD-1/ETD-2/ETD-4/ETD-6; pin Pydantic and canonical JSON/digest semantics without admitting an external runtime authority.
- **Output:** accepted ADR defining SQLite/WAL durability, tables/constraints, transaction boundary,
  global journal offset, aggregate version CAS, idempotency digest conflict and pure replay.
- **Ordered rules:** validate command -> compare idempotency digest -> load expected aggregate version
  -> derive events/effect intents -> append events, update head and enqueue effects in one transaction
  -> commit -> return stable receipt.
- **Edge cases:** duplicate command, conflicting digest, stale aggregate version, writer crash before
  commit, database busy/corrupt and migration mismatch.
- **Done when:** schema sketch, transaction pseudocode, crash boundaries and acceptance tests are
  reviewed and the ADR is `accepted`.
- **Verification:** human review plus executable SQL constraints/tests named for TASK-010.
- **Owner:** manual.

### SWU-ACI-002 — Compatibility, ledger and protocol ADR set

- **Dependencies:** none; may run beside SWU-ACI-001 with disjoint ADR files.
- **Write scope:** `docs/features/agents-communication-infra/adrs/`, feature README question status,
  writer-boundary test specification.
- **Inputs:** OQ-DECISION, OQ-TERMINAL, OQ-SNAPSHOT, promoted OQ-LEDGER-CONSISTENCY, historical drift.
- **Output:** accepted ADRs for fixed decision rule, terminal mapping, frozen input digest, exact-row
  ledger reconciliation and explicit legacy/runtime cutover ownership.
- **Required decisions:** same ID + identical ledger row is applied; same ID + divergent row is
  `reconciliation_required`; `.confirmed` marker is compatibility/projection only for runtime-managed
  runs; no legacy watcher and runtime worker may own the same dispatch.
- **Done when:** golden opening/close fixtures exist as specifications, drift has an owner/disposition,
  and the `SoleWriterEvidenceBundle` schema, sole-writer guard and named positive/negative tests are
  fully specified. Complete target-host process/ACL/inventory/bypass evidence is produced by
  TASK-020 before materializer cutover and is not a prerequisite for TASK-010 journal work.
- **Verification:** review against engine constitution EG-1/EG-6 and current appender behavior.
- **Owner:** manual.

## Completion evidence

- Five Slice-0 OQs plus ledger consistency are decided or explicitly narrow 0B-0D scope.
- Event/command/state catalogue and one golden end-to-end trace are frozen.
- B-001 and B-002 are closed before the W0 runtime-entry gate changes to `pass`; B-003's W0
  contract obligations (bundle schema, drift disposition, guard specification and named tests) are
  frozen. B-003's physical proof remains open for TASK-020/materializer cutover without blocking
  TASK-010.

## DomainSpec Coverage

Primary coverage here means freezing the cross-cutting contract before implementation tasks consume it.

| Source Aspect | Coverage IDs |
|---|---|
| `domain.md` | `agents-communication-infra.DispatchSpec`, `agents-communication-infra.ContentDigest`, `agents-communication-infra.VersionedReference`, `agents-communication-infra.ExecutionAuthorityMode`, `agents-communication-infra.ResourceBudget`, `agents-communication-infra.SandboxPolicy`, `agents-communication-infra.ExecutionAuthorityFence` |
| `rules.md` | `agents-communication-infra.ExternalToolAdoptionPolicy`, `agents-communication-infra.CanonicalContractPolicy`, `agents-communication-infra.BoundaryValidationPolicy` |
