# TASK-010 — Journal, command boundary and pure reducer

## Objective

Build the deterministic spine without invoking the audit appender, fake adapter, clock or network.

- **Layer/slice:** L0 / S-001 subgates 0B and part of 0E / W1.
- **Dependencies:** TASK-000 pass.
- **Proposed write scope:** `implementations/server/runtime/domain/`,
  `implementations/server/runtime/persistence/`, `implementations/tests/runtime/`.

## Implementation contract

Inputs are versioned commands plus `expected_aggregate_version`. Outputs are stable command receipts
or typed conflicts. A transaction must atomically append events, advance the aggregate head and add
minimal effect intents. Reducers consume events only and produce a canonical state serialization and
hash. No reducer emits an effect or reads infrastructure.

## Smallest Working Units

### SWU-ACI-003 — SQLite journal and command receipt

- Implement migrations for commands/receipts, events, aggregate heads and minimal outbox/effect intents.
- Enforce unique command ID, unique idempotency key with digest, global offset and per-aggregate version.
- Verify WAL/durability settings on startup; fail closed on incompatible schema or failed integrity check.
- Tests: duplicate same digest, conflicting digest, stale CAS, concurrent append, rollback before commit.

### SWU-ACI-004 — Domain state, transitions and replay

- Implement immutable command/event/state types and a pure reducer for lifecycle states first, then
  the fixed group protocol after 0B-0D pass.
- Serialize state canonically and calculate a deterministic state hash.
- Reject illegal transitions without appending partial facts.
- Tests: golden traces, replay N times, event permutation rejection, deadline represented only by an
  accepted event and spies proving replay invokes no effects.

## Done when

- The journal reconstructs identical state/hash after process restart.
- Command/event/outbox atomicity has a fault test at every transaction boundary.
- The first closed lifecycle trace is representable, even though no external effect has run yet.

## DomainSpec Coverage

| Source Aspect | Coverage IDs |
|---|---|
| `domain.md` | `agents-communication-infra.Run`, `agents-communication-infra.EffectIntent`, `agents-communication-infra.RuntimeCommand`, `agents-communication-infra.RuntimeEventEnvelope`, `agents-communication-infra.AggregateVersion`, `agents-communication-infra.JournalOffset` |
| `operations.md` | `agents-communication-infra.AcceptRuntimeCommand` |
| `states.md` | `agents-communication-infra.RunLifecycle` |
| `interfaces.md` | `agents-communication-infra.EventJournal` |
