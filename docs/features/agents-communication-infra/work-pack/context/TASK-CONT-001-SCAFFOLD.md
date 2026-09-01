# Implementation scaffold — SWU-ACI-AGENT-CONTINUATION-001

## Function-first targets

| Obligation | Owner | Required shape |
|---|---|---|
| Isolated persistence | `013_agent_continuation.sql`, `database.py` | `runtime_agent_attempts`, immutable `runtime_attempt_snapshot_bindings`, `agent_continuations`, and ordered `agent_continuation_mapping_members`; direct CONF-001 parents; no backfill/legacy mutation. |
| Pure policy | `continuation.py` | Closed projection, UTC deadline derivation, ordered mapping validation, semantic intent, lifecycle reducer; no I/O/import inversion. |
| Consumer orchestration | `RuntimeService` | Read exact authority with SELECTs through `database.connect()`; derive fixed scope/key; supply mutation SQL only through the generic journal closure; no `database.write()`, commit, second transaction/writer, caller key or effect. |
| Fail-closed vocabulary | `errors.py` | Task-specific errors, including `continuation_mixed_source_state`; no broad hierarchy refactor. |
| Component harness | `test_agent_continuation.py` | Test-only full attempt lifecycle via generic journal acceptance, immutable terminal snapshot linkage, no production attempt creator. |
| Integrity | traceability + Stage-E paths | Map T-ACI-CONT1/base CONT9 to real selectors and repin only final task-owned bytes while preserving prior repairs. |

## Required command shape

```text
scope_key       = aci.agent-continuation:<continuation_id>
idempotency_key = suspend@1
expected_version = 0
```

Neither scope nor key is accepted from the caller. `semantic_intent` binds the confirmed-authority
digest; continuation/dispatch; source attempt, turn, seat and instance; ordered mapping IDs; both
awaited IDs; snapshot ID/hash; optional handle digest; policy reference; and derived UTC deadline.

## Required query boundary

Query official journal facts using the exact two confirmed source-message identities. Only zero
official facts accepts, with both mappings awaited in confirmed order. One, two, duplicate or
ambiguous facts reject as `continuation_mixed_source_state` without mutation. Resolution of those
facts is CONT-002 work.

Before that query, check for the derived-key continuation. When present, reconstruct the
command/event/semantic intent from persisted bytes and call generic acceptance for replay/drift;
do not consult current official facts. For a new continuation, precheck zero-of-two and repeat the
exact query inside the mutation closure before inserts. Test both a fact inserted between precheck
and closure (no write) and a fact inserted after commit (retry returns the first receipt).

## Required test-only predecessor

The harness accepts `requested -> starting -> running -> completed` through
`RuntimeJournal.accept`, finalizes snapshot metadata and inserts the immutable attempt/snapshot
binding linked to the terminal event/offset. It may use test-local mutation callbacks, but must not
add a production writer/helper, widen production `ACI_SCHEMAS`, or seed a completed row directly.

`database.py` registers migration 013 only. Do not move service/repository query methods into it.

## Read-only boundaries

Do not edit `journal.py`, `artifacts.py`, `api.py`, `__init__.py`, `confirmation.py`, migration 012,
legacy migrations/tables, specs or fixtures. Do not create target attempts, effects, official-input
resolution, resume, adapter/provider calls or host/UI surfaces.
