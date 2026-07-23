# Storage and Artifact Policy Review Packet

- Packet status: `ready-for-independent-review`
- Review verdict: `pending`
- Scope: `SWU-ACI-APT-VS-001`
- Authority owner: `agents-communication-infra`

## Selected bounded policy

The local vertical slice uses the single ACI-owned SQLite database. The exact accepted bound
research-submission envelope is stored only as a protected runtime-owned artifact BLOB. Artifact
bytes, artifact metadata, ordered events, affected heads, uniqueness keys and the durable command
receipt commit in one `BEGIN IMMEDIATE` transaction. APT never opens SQLite and never finalizes an
artifact.

The final answer may exist in SQL only in `artifacts.body`. It is forbidden in event payload JSON,
APT projection columns or JSON, receipts, logs, traces, metrics, SSE, validation errors and
dispatch-ledger rows. `ResearchAnswer` stores only artifact identity, digest and the exact selector.
The separately authorized answer read dereferences the artifact and selector through ACI.

## Classification and access

| Item | Classification | Read rule |
|---|---|---|
| Bound research-submission envelope | `sensitive-output` | Authenticated principal authorized for the linked Session/Dispatch/capture |
| APT event payload | `runtime-internal` | Internal verified-prefix reader; no raw answer |
| APT projection | `runtime-internal` | Authorized provenance query; no raw answer |
| Completion telemetry | `runtime-internal` | Bounded IDs/digests/status only |

Mutation and raw-answer reads require authentication even on loopback. Caller bodies cannot supply
paths, actor/owner identity, IDs, timestamps, digests, receipts, finalization flags or offsets.
Configured repository paths, database paths and artifact access remain server-owned.

## Limits and lifecycle

- Exact policy bundle:
  `apt.artifact-policy-bundle@1`,
  `sha256:6345bde1c44f9832ce6a4c8e07f5f9484ac265ff4c96276d4dfa47c590149299`.
- Required metadata refs are
  `apt.retention.local-sensitive-output@1`,
  `apt.tombstone.preserve-identity-and-audit@1`, and
  `apt.authorization.provenance-artifact-read@1`; the accepted artifact binds all three plus the
  exact bundle digest above.
- The closed classification enum and selected `sensitive-output` value are frozen in
  `policies/apt-artifact-policy-bundle@1.json`. Unknown or mismatched policy refs, digests or
  classifications reject before append/read.
- Reject invalid UTF-8, duplicate JSON keys, unknown fields and non-finite numbers.
- Bound the request, answer bytes, question bytes, list counts and every reference/problem/
  formalization field before artifact construction.
- Redact request bodies and validation values from logs and errors.
- Retention and tombstone policies are immutable refs on the artifact. L0 does not physically erase
  accepted bytes. A later ACI-owned tombstone operation may make bytes unavailable while preserving
  identity, digest, receipt and audit facts.
- Database files and backups require owner-only OS permissions. Secrets never enter the database.

## Atomicity, recovery and projection

- No filesystem artifact backend is used in this slice, so an accepted event cannot reference an
  uncommitted file and a failed transaction cannot leave an artifact BLOB orphan.
- APT projections are disposable. ACI's `ProjectionManager` alone executes their migration and
  writes. `apt_source_through_offset` advances over every complete verified command group,
  including unrelated groups that are deterministically skipped.
- Projector failure after journal commit does not negate success. The stable receipt is returned
  with `projection_status=pending`; reads requiring a later offset return `PROJECTION_LAG`.
- Startup, explicit catch-up and exact command retry repair projection lag without changing the
  original receipt.

## Required independent checks

The reviewer must verify: atomic artifact/event/head/receipt failure points; answer-body absence
outside `artifacts.body`; authorization on mutation and raw reads; limit/redaction behavior;
tombstone semantics; projection rebuild/lag; restart readback; and byte-identical dispatch ledger.
Until a digest-bound PASS receipt exists, `storage_and_artifact_policy_review` is false.
