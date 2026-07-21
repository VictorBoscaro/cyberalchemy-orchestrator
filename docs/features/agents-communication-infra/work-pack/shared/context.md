# Shared Context

## Start here

The feature architecture already owns the target runtime. This plan does not create a competing
`orchestration-runtime` feature; it introduces an implementation package inside the existing
feature boundary.

## Current implemented surfaces

| Surface | Current behavior | Migration use |
|---|---|---|
| `implementations/server/main.py` | FastAPI read APIs, disk-snapshot SSE and `/api/confirm` marker write. | Host the first command/query boundary; keep legacy response compatibility during cutover. |
| `implementations/server/ledger.py` | Lenient, cached reader for historical ledger and pending sheets. | Verification/query helper only; never an authoritative writer. |
| `.claude/skills/register-dispatch/append-dispatch.cjs` | Strict, idempotent-by-ID appender for v0.6.1 opening and close rows. | Sole physical audit-ledger writer invoked by materializers. |
| `telemetry/agents/pending/` | Editable pre-confirm sheets and `.confirmed` markers. | Compatibility input; confirmed spec becomes immutable runtime input. |
| `telemetry/agents/subagents-dispatch.yaml` | Append-only audit authorization/outcome record. | Remains authoritative only for official opening and closing. |
| `implementations/static/ui/linear/index.html` | The only UI variant currently wired to call `/api/confirm`; nine variants remain disabled. | First compatibility client; broader UI enablement stays after runtime confirmation semantics are stable. |
| Existing skills | Author, validate, confirm, launch and close through session coordination. | Gradually become command clients; retain legacy fallback until cutover gate. |

## Target package boundaries

Future paths are deliberately plain text until created:

```text
implementations/server/runtime/
  domain/          pure commands, events, state and reducer
  application/     command service, reactors and query service
  persistence/     SQLite journal/outbox and migrations
  materializers/   audit-ledger opening/close and reconciliation
  adapters/        fake first, then provider implementations
  projections/     runtime query/SSE projections
  api/             request/response mapping only

implementations/tests/runtime/
  fixtures/
  fault/
  contract/
```

Dependency direction:

```text
api/adapters/materializers/persistence -> application -> domain
projections                           -> domain contracts
domain                                -> no infrastructure imports
```

## Required authority split

- Command/journal: accepted workflow intent and runtime facts.
- Audit appender/ledger: official authorization opening and outcome closing.
- Adapter: external execution only; never protocol authority.
- Projection/SSE: reconstructible view only.
- Skills/UI: authors and command clients, never physical store writers.

## Migration rule

Use a compatibility façade, not dual authority. During cutover `/api/confirm` may translate the
existing request into the new command service and preserve its response shape. A marker may remain
a compatibility projection, but discovering or refreshing a marker cannot independently authorize
a run once the runtime path is enabled. The legacy flow deletes the pending sheet and marker after
registration; the runtime-managed path must therefore freeze the exact sheet bytes/digest before
any cleanup and make cleanup a retryable compatibility effect, never the source of run state.

## Source anchors

- [Feature architecture](../../README.md): target states, stores, MVP and open questions.
- [Engine constitution](../../../../../vault/constitution/engine-constitution.md): EG-1 through EG-8.
- [Current reader](../../../../../implementations/server/ledger.py).
- [Current FastAPI surface](../../../../../implementations/server/main.py).
- [Current UI contract](../../../../../implementations/UI-CONTRACT.md).
- [Validated audit appender](../../../../../.claude/skills/register-dispatch/append-dispatch.cjs).
- [Implemented Phase-2 confirm handoff](../../phase-2-confirm-handoff.md).
