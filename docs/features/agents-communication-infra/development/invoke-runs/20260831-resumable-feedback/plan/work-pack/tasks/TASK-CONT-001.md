# TASK-CONT-001 — CONF-001-backed continuation suspension

## Promotion status

- **State:** `implemented-reviewed-pass`
- **Evidence:** [TASK-CONT-001](../../evidence/TASK-CONT-001.md)
- **Historical entry descriptor:** `sha256:e440c54ee65aa4c90596aca12dbcbef9b86e3d919d869e7fd66babc4812ad620`
- **Historical entry readiness:** `sha256:cc017802059b3a4a29f5af232c0bc0b05c023861cae139e39cc4b3db9e6ee6a0`

The readiness receipt remains pinned to the pre-implementation descriptor bytes and is not repinned
after status promotion.

## Objective and claim

Prove only that the continuation component consumes writer-created CONF-001 authority and persists
one effect-free suspension. The proof does not create or claim a production attempt writer.

The minimum accepted unit is one `AgentContinuation`, its two confirmed mapping members, one
`continuation.suspended` event and one stable command receipt committed atomically with zero new
effects.

## Entry evidence

- CONF-001 is `implemented-reviewed-pass`: [evidence](../../../evidence/CONF-001.md).
- The D0 Robot Talks decisions are closed: [findings](../../../../../../robot-talks/2026-09-01-continuation-l2-d0/findings.md).
- The exact descriptor is `SWU-ACI-AGENT-CONTINUATION-001`.
- Code entry was authorized by the historical exact `domainspec-code-readiness@1` PASS.

## D0 decision lock

1. `TASK-CONT-001` makes a component/consumer claim only.
2. The source attempt is a test-only prerequisite. The harness must accept the full
   `requested -> starting -> running -> completed` lifecycle through `RuntimeJournal.accept`, then
   finalize and immutably link the reconstruction snapshot to the terminal event/offset. No
   production source-attempt writer or helper symbol may be added. The test harness wires the
   attempt event schemas/validators directly to the journal; production `ACI_SCHEMAS` is unchanged.
3. Suspension uses generic `RuntimeJournal.accept`. `RuntimeService` derives
   `scope_key = aci.agent-continuation:<continuation_id>` and `idempotency_key = suspend@1`; callers
   provide neither.
4. The UTC deadline is `confirmed_at + wall_clock_seconds`. Audit opening does not extend it.
5. The service queries official journal facts for the exact two confirmed `source_message_id`
   values. Exact zero-of-two means both mapping IDs are awaited in confirmed order. Any one-of-two,
   two-of-two or ambiguous result rejects as `continuation_mixed_source_state`; those semantics
   belong to CONT-002.
6. Derived-key replay precedes current-fact evaluation. If the continuation exists, reconstruct the
   command, event and semantic intent from persisted bytes and call generic acceptance for
   replay/drift without querying newer official facts. On create, precheck zero-of-two and revalidate
   the exact source-message facts inside the journal mutation closure before any insert. A later
   official fact does not invalidate the first receipt; caller drift, including an operation-supplied
   provider-handle digest, conflicts.
7. Migration 013 creates isolated runtime tables with direct CONF-001 parents and no backfill:
   `runtime_agent_attempts`, `runtime_attempt_snapshot_bindings`, `agent_continuations` and
   `agent_continuation_mapping_members`. Existing legacy tables, foreign keys and behavior remain
   unchanged.

## Semantic intent discriminants

The service-derived `semantic_intent` must bind all and only the suspension meaning needed for
replay/conflict comparison:

- confirmed-authority digest, `dispatch_id` and `continuation_id`;
- source `attempt_id`, turn ordinal, seat ID and agent-instance ID;
- both mapping IDs in confirmed order and both awaited mapping IDs in that same order;
- reconstruction snapshot artifact ID and content hash;
- optional provider continuation-handle digest, never the opaque handle;
- confirmed resume-policy reference; and
- the derived UTC deadline.

The event payload and receipt must carry enough of these discriminants to reproduce authority and
diagnose conflict without exposing an opaque provider handle.

## Persistence and layering

- `continuation.py` owns strict projection, identity/mapping/deadline validation, semantic-intent
  construction and the pure lifecycle reducer. It imports no SQLite, journal, service, adapter,
  filesystem, clock or legacy module.
- `service.py` owns authorization, CONF-001/source-attempt/snapshot/official-fact reads, fixed command
  construction and application orchestration. It may run read-only SELECTs through
  `database.connect()` and define mutation SQL executed only on the connection supplied to the
  `RuntimeJournal.accept` closure. It must not call `database.write()`, commit, open a second
  transaction/writer, move repository methods into `database.py`, or accept caller idempotency.
- `RuntimeJournal.accept` remains the transaction owner. No specialized journal method is added.
- migration 013 and `database.py` own only isolated persistence and ordered discovery.
- `errors.py` may add task-specific fail-closed discriminants, including
  `continuation_mixed_source_state`.
- Tests alone construct the full predecessor lifecycle; production code only consumes it.

## Exact ordered code write scope

1. `implementations/server/runtime/migrations/013_agent_continuation.sql`
2. `implementations/server/runtime/database.py`
3. `implementations/server/runtime/continuation.py`
4. `implementations/server/runtime/service.py`
5. `implementations/server/runtime/errors.py`
6. `implementations/tests/runtime/test_agent_continuation.py`
7. `implementations/tests/runtime/test_runtime_confirmation.py`
8. `implementations/tests/runtime/aci-test-traceability.json`
9. `implementations/tests/runtime/test_aci_traceability.py`
10. `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
11. `implementations/server/runtime/local_pilot.py`
12. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
13. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256`

`journal.py`, `artifacts.py`, `api.py`, `__init__.py`, every legacy migration/table, `confirmation.py`,
all specs and all fixtures are read-only.

## Test matrix

| Matrix | Required proof |
|---|---|
| Migration | Apply/reopen idempotently; four isolated runtime tables; direct CONF-001 parents; legacy schema/row bytes unchanged; zero backfill. |
| Prerequisite harness | Full journal-backed attempt lifecycle; finalized immutable snapshot binding references terminal event/offset; no seeded terminal shortcut; no production attempt-writer symbol. |
| Authority | Derive continuation, dispatch, source attempt/turn/seat/instance and both ordered mappings from CONF-001; caller/legacy/cross-dispatch substitutions reject before write. |
| Awaited facts | Exact zero-of-two accepts both ordered mapping IDs; one-of-two, two-of-two, duplicate or ambiguous facts reject `continuation_mixed_source_state` with no write. |
| Replay/TOCTOU | Existing continuation reconstructs persisted command/event/intent and replays before fact reads; create revalidates exact facts in the mutation transaction; inject a fact between precheck and closure to reject all inserts; accept a fact after commit and require retry to return the first receipt. |
| Deadline | UTC exact addition from `confirmed_at` and confirmed `wall_clock_seconds`; timezone, overflow/invalid and opening-relative substitutions reject. |
| Atomicity | Every mutation/failpoint is all-or-none for continuation, members, event, head and receipt; effect count remains zero. |
| Replay | Same derived scope/key and byte-identical semantic intent returns the first receipt even after a later official fact; any listed discriminant drift, including supplied provider-handle digest drift, conflicts. |
| Lifecycle | T-ACI-CONT1 plus the L2/base T-ACI-CONT9 state/event Cartesian matrix rejects every unlisted pair without mutation. |
| CONF-001 migration regression | In `test_runtime_confirmation.py`, change only the post-migration `user_version` expectation to 13 and add/retain proof of migration 013 name, checksum and reopen; preserve every AUTH1–8 and all other assertions. |
| Non-regression | CONF-001, reference delivery, traceability, Stage-C, bridge and complete runtime discovery remain green; Stage-E pins final bytes. |

## Stop conditions

Stop on any inconsistent CONF-001 authority/digest; a source attempt that is absent, nonterminal,
wrong-role, wrong-seat/instance/turn or not journal-backed through the full lifecycle; an absent or
misbound snapshot; any pre-existing target attempt; any official-source result other than exact
zero-of-two; any new effect; any mutation of CONF-001 or legacy rows; any need for caller-controlled
scope/key or a second create sharing the continuation identity; any write outside scope; or any
CONF/AUTH/baseline regression requiring a wider layer.

## Validation commands

```text
python -B -m unittest implementations.tests.runtime.test_agent_continuation -v
python -B -m unittest implementations.tests.runtime.test_runtime_confirmation -v
python -B -m unittest implementations.tests.runtime.test_agent_reference_delivery -v
python -B -m unittest implementations.tests.runtime.test_aci_traceability -v
python -B -m unittest implementations.tests.runtime.test_stage_c -v
python -B -m unittest implementations.tests.runtime.test_orchestration_bridge -v
python -B -m unittest discover -s implementations/tests/runtime -t .
python -B -m compileall implementations/server/runtime implementations/tests/runtime
git diff --check
```

## Completion topology

One code writer owned the ordered scope. A different reviewer accepted the final diff and evidence.
The 9/9 focused suite, 40/40 regressions, 169/169 runtime discovery and 36/36 Control Center
canonical suite passed. This task now permits planning CONT-002; it does not authorize official contribution
resolution, resume, target attempts, effects, adapters, providers or deployment.
