# TASK-000 — Freeze Slice-0 contracts

## Objective

Resolve every decision that would otherwise be encoded accidentally in persistence, state or
migration code. This task authorizes contracts, not runtime implementation.

- **Layer/slice:** L0 / S-000 / W0.
- **Sources:** feature README sections 4.1-4.3, 9.1, 12, 14 and 17; engine constitution EG-1.
- **Gate:** ready for documentation work; blocks all runtime-code tasks.

## Smallest Working Units

### SWU-ACI-001 — Persistence and replay ADR

- **Dependencies:** none.
- **Write scope:** `docs/features/agents-communication-infra/adrs/`, decision/gap ledgers.
- **Inputs:** OQ-PERSISTENCE, OQ-STREAM, D-102, D-103.
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
  and the sole-writer guard is designed.
- **Verification:** review against engine constitution EG-1/EG-6 and current appender behavior.
- **Owner:** manual.

## Completion evidence

- Five Slice-0 OQs plus ledger consistency are decided or explicitly narrow 0B-0D scope.
- Event/command/state catalogue and one golden end-to-end trace are frozen.
- `WORK-PACK.md` blockers B-001 through B-003 are closed before its gate changes to `pass`.

