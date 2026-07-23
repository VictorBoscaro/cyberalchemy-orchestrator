# Experimental Agent Runtime L0

This isolated, local-only shadow runtime proves the smallest durable slice for:

- sessions and opaque host/conversation correlation;
- session-to-dispatch links;
- `reference-scout` runs and recommendations;
- append-only journal events and verifiable command receipts;
- deterministic projection replay.
- read/compare-only shadow reconciliation against `subagents-dispatch.yaml`.

It is experimental. It does not replace the current ledger writer, launch
agents, store transcripts, or constitute a production cutover.

## Frozen vocabulary and boundaries

- A `Session` is not a conversation. `origin_kind` and `origin_ref` may point
  opaquely to a host conversation; no transcript or raw prompt is stored.
- The product capability is `reference-scout`. Product commands and projections
  use Scout names; frozen v1 wire compatibility retains `probe_id` and
  `probe.*` event names.
- The existing `bus-publication-probe` experiment is understood as a
  publication-receipt spike. Its dirty directory is intentionally untouched.
- `journal_events` and `command_receipts` are authoritative. `sessions`,
  `session_dispatch_links`, `reference_scout_runs`, and
  `reference_recommendations` are rebuildable projections.
- `Residue.lean` and `CodensityUnitResidue.lean` are not unified. This runtime
  has no `residue_score`. If source evaluation needs comparability, the only
  explicit states are `comparable`, `incommensurable`, and `count_capped`.
- Compression and masking are out of scope for L0.

## Durability semantics

Every accepted command runs in one `BEGIN IMMEDIATE` transaction:

1. validate `operation_id` idempotency against the canonical payload digest;
2. append a hash-chained journal event;
3. update the projection;
4. persist the command receipt;
5. commit, then return the receipt.

A retry with the same command, `operation_id`, and canonical payload returns
the original receipt. Reusing the operation ID differently conflicts. A
projection failure rolls back the event and receipt together.
Receipts are visibly namespaced `experimental_rcpt_*` and bind canonical
payload, result, and receipt digests. They are not production ACI receipts.

## Commands

The API supports:

- `ensure_session`
- `link_session_dispatch`
- `start_reference_scout`
- `publish_scout_contribution`
- `commit_reference_bundle`
- `deliver_reference_bundle`

Example from this directory:

```powershell
python -m agent_runtime --database .\shadow.sqlite3 init
python -m agent_runtime --database .\shadow.sqlite3 command ensure_session op-1 '{"session_id":"ses-1","ensure_key":"host:opaque-1","origin_kind":"codex","origin_ref":"conversation:opaque-1"}'
python -m agent_runtime --database .\shadow.sqlite3 show sessions
python -m agent_runtime --database .\shadow.sqlite3 replay
python -m agent_runtime --database .\shadow.sqlite3 reconcile-ledger C:\repo\telemetry\agents\subagents-dispatch.yaml dispatch-1
```

The library exposes the same operations through `agent_runtime.Runtime`.

## Tests

```powershell
python -m unittest discover -s tests -v
```

The tests cover the end-to-end state machine, receipt verification, exact
retry, conflicting retry, transactional rollback, deterministic replay,
journal tamper detection, dispatch ownership, and rejection of transcript,
prompt, messages, and privileged `residue_score` fields.

The reconciler derives a discardable
`subagents-dispatch.runtime_refs@0.7` candidate from the sole accepted
Session-to-Dispatch link. It compares that fragment with the observed opening
row and classifies it as `absent`, `identical`, `divergent`, `malformed`, or
`orphan_close`. It never writes YAML, invokes the appender, repairs a row, or
treats comparison as acknowledgement.

## Known L0 gaps

- no integration with the launcher or MCP host; YAML integration is
  read/compare-only;
- no outbox, multi-process writer service, retention, backup, or recovery job;
- no authorization, artifact store, redaction, compression, or masking;
- receipts prove local durable publication, not remote delivery;
- no schema upgrade beyond migration version 1;
- no write materializer or cutover for `subagents-dispatch.yaml`;
- timestamps and IDs are host-generated rather than supplied by a trusted
  runtime authority.
