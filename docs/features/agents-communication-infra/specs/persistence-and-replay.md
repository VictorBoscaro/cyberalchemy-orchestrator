---
tags: [agents-communication-infra, spec, persistence, replay]
node_type: spec
is_session: false
layer: [application, infrastructure]
nature: [technical, reference]
status: draft
version: 0.1.0
last_updated: 2026-07-21
---

# Persistence and Replay: Agents Communication Infra

This document ratifies the DomainSpec answer to OQ-ACI1 and OQ-ACI7. It is the candidate W0
contract that a persistence ADR must accept or explicitly supersede before runtime implementation.
It does not close WORK-PACK blockers, authorize code or claim production SQLite exists.

## 1. Authority boundary

One local SQLite database is authoritative for command deduplication, accepted runtime events,
aggregate concurrency heads and durable effect intent. It runs in WAL mode behind one validated
journal-writer boundary. Multiple logical publishers or worker processes may call that boundary;
they are not independent physical writers.

The YAML audit ledger remains outside SQLite authority and is written only by the existing validated
appender. Artifact bytes remain behind the artifact boundary; SQLite owns their immutable metadata
and references. Projections are reconstructible and disposable.

## 2. Required database policy

| Setting | Proof/pilot requirement | Reason |
|---|---|---|
| `journal_mode` | `WAL` | Same-host readers can observe committed state without becoming writers. |
| `synchronous` | `FULL` | Ratifies OQ-ACI7; every atomic acceptance has the same durability claim. |
| `foreign_keys` | `ON` | Reject dangling authoritative references where SQL can enforce them. |
| write boundary | one serialized journal service/store | Preserves EG-1 scoped writer authority. |
| busy handling | bounded and explicit | `BUSY` rejects/retries at command boundary; it never returns a false receipt. |
| migrations | monotonic schema version plus checksum | Unknown or divergent migration blocks writes and replay. |

Changing `synchronous` requires a superseding decision supported by crash/fault measurements. It is
not a per-event optimization toggle.

## 3. Candidate logical schema

Column names and normalization may change in the accepted W0 ADR, but authority, uniqueness and
transaction membership below may not change silently.

### 3.1 Authoritative tables

#### `command_receipts`

| Column | Constraint / meaning |
|---|---|
| `command_id` | Primary key. |
| `scope_key`, `idempotency_key` | `UNIQUE(scope_key, idempotency_key)`. |
| `command_digest` | Canonical digest; immutable. |
| `aggregate_id`, `expected_version` | Target and submitted CAS expectation. |
| `status` | `accepted` or deterministic rejection category retained by policy. |
| `result_receipt_json`, `first_offset`, `last_offset` | Stable committed response and event span. |
| `created_at` | Journal-recorded metadata, not ordering authority. |

A matching scoped key/digest returns `result_receipt_json`. A different digest produces permanent
`IDEMPOTENCY_CONFLICT` and cannot replace this row.

#### `events`

| Column | Constraint / meaning |
|---|---|
| `journal_offset` | `INTEGER PRIMARY KEY`; global committed order for this database. |
| `event_id` | Globally unique; enforced by `UNIQUE(event_id)`. |
| `aggregate_type`, `aggregate_id`, `aggregate_version` | `UNIQUE(aggregate_id, aggregate_version)`; versions contiguous. |
| `event_type`, `schema_ref`, `schema_digest` | Immutable event contract. |
| `command_id`, `causation_id`, `correlation_id` | Provenance. |
| `recorded_at`, `observed_at` | Recorded/external time; neither replaces offset ordering. |
| `payload_ref`, `payload_hash` | Finalized immutable evidence. |
| `authority_context_json` | Runtime-derived run/group/seat/attempt/principal identities where applicable. |

`journal_offset` is global, while `aggregate_version` is contiguous only inside its aggregate.
Global offset gaps caused by rolled-back SQLite allocation are not observable as committed events;
consumers require monotonic committed order, not arithmetic density across aborted transactions.

#### `aggregate_heads`

| Column | Constraint / meaning |
|---|---|
| `aggregate_id` | Primary key. |
| `aggregate_type` | Stable aggregate category. |
| `current_version` | Non-negative current CAS version. |
| `state_hash` | Hash of canonical state after `current_version`. |
| `last_event_id`, `last_offset` | Event/offset represented by the head. |
| `reducer_version` | Exact reducer contract used to produce `state_hash`. |

The writer updates a head only with `WHERE current_version = expected_version`; affected-row count
must equal one. New aggregates require expected version zero.

#### `effect_intents`

| Column | Constraint / meaning |
|---|---|
| `effect_id` | Primary key. |
| `command_id`, `requested_event_id` | Unique causal origin as declared by effect type. |
| `effect_type`, `payload_ref`, `payload_digest` | Immutable effect request. |
| `retry_class` | `retryable` or `non_retryable`. |
| `status` | `pending`, `claimed`, `succeeded`, `failed` or `unknown`. |
| `claim_epoch`, `claimed_by` | Durable single-host CAS fence. |
| `attempt_count` | Physical deliveries; never a logical acceptance count. |
| `outcome_event_id` | Accepted outcome observation when known. |
| `outcome_digest` | Nullable canonical digest of the accepted terminal outcome; immutable once set. |

New effect intents join the command transaction. Later claim/outcome transitions use independent
CAS transactions and become events before reduced protocol state depends on them.

#### `artifacts`

| Column | Constraint / meaning |
|---|---|
| `artifact_id` | Primary key. |
| `content_hash` | Unique with canonical algorithm/bytes semantics. |
| `media_type`, `schema_ref`, `classification` | Validated metadata. |
| `size_bytes` | Non-negative and verified. |
| `storage_ref` | Opaque finalized payload location. |
| `created_event_id` | Provenance for runtime-created artifacts. |
| `tombstoned_at`, `tombstone_reason` | Nullable crypto-erasure/deletion evidence. |

An event can reference an artifact only after content finalization and metadata commit. Orphan
uploads are not authoritative and may expire. Only the validated artifact-store writer may create
or mutate authoritative artifact metadata; journal, adapter and projection implementations use its
interface and never insert into `artifacts` directly.

#### `publication_candidates`

| Column | Constraint / meaning |
|---|---|
| `candidate_id`, `message_id` | `candidate_id` primary key; `message_id` globally unique stable message identity. |
| `publication_event_id` | Unique FK to the candidate's `publication.persisted` event. |
| `group_aggregate_id`, `seat_id`, `round_id`, `message_type` | Logical contribution key. |
| `attempt_id`, `operation_id` | Authenticated owning physical/logical execution. |
| `payload_ref`, `payload_hash`, `idempotency_key` | Immutable publication content and scoped retry identity. |
| `receipt_bytes`, `receipt_digest`, `journal_offset` | Canonical byte-stable receipt and committed position. |
| `status` | `active`, `officially_accepted`, or `abandoned`. |
| `candidate_version` | Monotonic CAS version. |
| `official_accepted_event_id`, `abandoned_event_id` | Mutually exclusive nullable terminal references. |

The database enforces one active reservation with a partial unique index:

```sql
CREATE UNIQUE INDEX one_active_candidate_per_logical_key
ON publication_candidates(group_aggregate_id, seat_id, round_id, message_type)
WHERE status = 'active';
```

It also rejects any row with both terminal references, an `officially_accepted` row without its
official event, or an `abandoned` row without its abandonment event. Candidate creation joins the
`publication.persisted` command transaction. Official acceptance CASes `active ->
officially_accepted`; abandonment CASes `active -> abandoned`. Historical rows are never deleted or
reopened. Candidate creation additionally requires that no official `messages` row already owns the
logical key; an accepted contribution therefore prevents every later candidate even though its
candidate row is no longer `active`.

### 3.2 Rebuildable constrained indexes and projections

These tables accelerate checks and reads. Their contents must be derivable from authoritative events
and artifacts, and rebuilding them cannot invoke effects.

| Table | Required keys / constraints | Purpose |
|---|---|---|
| `attempts` | PK `attempt_id`; index `(operation_id, attempt_no)` and partial unique index `UNIQUE(operation_id) WHERE accepted_result = 1` | Unlimited retry rows with at most one accepted winner per operation. |
| `messages` | PK `message_id`; authoritative `UNIQUE(group_aggregate_id, seat_id, round_id, message_type)` plus FKs to official acceptance event, source candidate and artifact | Official receipt-verified contributions only; candidate rows never appear here. |
| `publication_receipts` | PK/FK `event_id -> events(event_id)`; unique `message_id`; scoped idempotency key, payload hash and canonical receipt bytes/digest | Rebuildable append-before-ack receipt lookup; authoritative candidate state remains in `publication_candidates`. |
| `reveal_manifests` | PK `reveal_manifest_id`; unique `(group_aggregate_id, round_id)`; unique `reveal_event_id`; manifest hash | Frozen accepted message IDs/hashes and reveal event. |
| `reveal_manifest_entries` | PK `(reveal_manifest_id, ordinal)`; unique `(reveal_manifest_id, message_id)`; FKs to manifest/message | Canonical ordered membership with stored message/payload hashes. |
| `usage_observations` | PK `usage_event_id`; provider/model/attempt dimensions nullable by contract | Immutable event projection for provenance-safe rollups. |
| `runtime_projections` | PK `(projection_name, projection_key)` plus `last_offset` | Disposable API/SSE state and cursor. |

If a table/index participates in command validation (for example active-candidate or official
logical-message uniqueness), it is
a synchronous constrained acceptance record even if it is rebuildable: the writer updates it in the
same transaction and the database enforces its authoritative unique key. A disposable asynchronous
projection alone cannot guard a write. Minimum lookup indexes include `events(command_id)`,
`events(aggregate_id, aggregate_version)`, `events(correlation_id)`,
`effect_intents(status, effect_type)`, `messages(group_aggregate_id, round_id)` and
`reveal_manifest_entries(message_id)`; every declared event/artifact/manifest reference has a
foreign key unless the referenced authority is explicitly cross-store.

#### `pricing_sources`, `usage_rollups` and `cost_calculations`

| Table | Required contract |
|---|---|
| `pricing_sources` | PK `pricing_source_id`; immutable provider/model applicability, effective interval, currency, unit semantics, canonical source artifact/ref and `pricing_digest`; unique canonical version/digest. |
| `usage_rollups` | PK `(rollup_kind, rollup_key, semantics_version, source_through_offset)`; counters, observation count, missing-count per dimension, provider/model grouping and nullable currency/cost summary; every value derives only through `source_through_offset`. |
| `cost_calculations` | PK `cost_calculation_id`; FK to pricing source and rollup/observation scope; immutable quantity, unit price, currency, pricing digest, source offset and calculation digest. A row exists only when compatible pricing permits an actual calculation. |

`usage_rollups` are rebuildable and their `source_through_offset` makes staleness explicit. Missing
dimensions remain counted and never become zero. `cost_calculations` are immutable derived evidence,
not provider invoices or billing truth; absent or incompatible pricing produces no cost-calculation
row, while the usage observation remains intact.

### 3.3 Checkpoints

The ADR may add a `checkpoints` table with:

```text
(checkpoint_id, aggregate_id, aggregate_version, journal_offset,
 state_artifact_id, state_hash, reducer_version, spec_digest, recipe_digest)
```

A checkpoint is usable only after its artifact/hash and referenced event prefix verify. It is an
optimization, never permission to delete uniqueness tombstones or events still required to recover
an active run, explain a retained commitment or validate that checkpoint.

## 4. Atomic command acceptance

The ordered contract is:

```text
validate schema, authenticated authority and command digest
BEGIN IMMEDIATE
  lookup (scope_key, idempotency_key)
  if same digest: return stored receipt after transaction ends; write nothing
  if different digest: fail IDEMPOTENCY_CONFLICT; write nothing

  load target aggregate_heads row and every declared prerequisite_heads[] row
  require target current_version = expected_version
  require each prerequisite head still matches its declared aggregate/version/state hash
  reduce current state + command -> events[], effect_intents[], next_state
  validate contiguous event versions and every invariant/unique logical key
  insert events[] (allocating global journal_offset)
  insert newly requested effect_intents[]
  update aggregate_heads by CAS with next version/state hash/offset
  update any synchronous constrained indexes
  insert command_receipts with stable result receipt and offset span
COMMIT
return stored stable receipt
```

`prerequisite_heads[]` is part of the canonical command digest. Validation and target-head CAS occur
inside the same write transaction. Commands that start an attempt/effect therefore race safely with
group/run close, cancellation and run terminality: if any prerequisite head advanced, the start
loses with `VERSION_CONFLICT` and creates no event, receipt or effect intent.

The reducer is pure. It cannot call the clock, adapter, tool, appender, artifact upload or random
source. Any nondeterministic observation must already exist as command input backed by an accepted
event/artifact, and the resulting accepted fact precedes state dependence.

### 4.1 Atomic effect-outcome acceptance

An effect delivery returning is only an outcome candidate. The journal writer accepts it with one
transaction fenced by `(effect_id, claim_epoch)`:

```text
canonicalize outcome and compute outcome_digest
BEGIN IMMEDIATE
  load effect_intent
  if terminal with same outcome_digest: return stored command receipt; write nothing
  if terminal with different digest: fail OUTCOME_CONFLICT; write nothing
  require status = claimed and claim_epoch = submitted epoch
  verify target head and prerequisite_heads[] by CAS contract
  insert terminal observation event with UNIQUE(event_id)
  update aggregate head and constrained indexes
  set effect_intents.status, claim_epoch, outcome_event_id and outcome_digest
  insert/update the outcome command receipt with stable event/head span
COMMIT
return the official stored receipt
```

Terminal/idempotency comparison deliberately precedes the `claimed`/epoch guard: after a successful
terminal commit the row is no longer `claimed`, so an identical lost-response retry must still
return the stored receipt, while a different digest must remain a permanent conflict. Only a new
nonterminal outcome candidate must prove the current claim epoch.

The receipt row, event, head transition and effect terminal fields are all-or-none. Outcome
acceptance exposes failpoints immediately before and after each SQL member and commit; crash tests
must prove that a retry with the same digest converges and a different digest cannot replace the
accepted outcome. No separate `EventJournal.appendDecision`-style write is a permitted contract:
implementations must satisfy the atomic command/outcome obligations exposed by
[interfaces.md](interfaces.md), not append a decision independently of its receipt, head and intent.

## 5. Crash boundaries and observable outcomes

| Crash point | Durable result | Recovery behavior |
|---|---|---|
| Before `BEGIN` or before commit | No command acceptance member is visible. | Safe retry with same key/digest. |
| After inserts, before commit | SQLite rolls back receipt, events, head and new intents together. | Safe retry; no receipt may have been returned. |
| After commit, before response | Whole acceptance exists. | Retry returns stored stable receipt without duplicate event/effect. |
| After effect claim, before external start | Claim is durable but external start may be absent. | Reconcile/status or re-deliver according to retry class and stable identity. |
| After external start, before outcome event | Outcome is potentially unknown. | Query status when supported; `non_retryable` becomes `unknown` rather than repeated. |
| During outcome acceptance before commit | No terminal member is visible. | Same epoch/digest may retry; failpoints prove receipt/event/head/intent atomicity. |
| After outcome commit, before response | Official terminal outcome and receipt exist together. | Candidate retry returns the stored receipt; different digest is `OUTCOME_CONFLICT`. |
| After candidate commit, before terminal evidence | Active candidate exists but is not official. | Reconcile the owning attempt; never count it or let another attempt bypass its active reservation. |
| After attempt becomes terminal `unknown` with no recoverable terminal evidence | Active candidate remains reserved. | If retry is authorized, CAS candidate to `abandoned` with an audit event, then permit a new attempt; otherwise surface unknown/repair-required. |
| Verification races abandonment | Candidate starts `active`; exactly one CAS can win. | Official winner creates the message/event pair; abandonment winner rejects late verification forever. |
| After audit append, before journal acknowledgement | Audit row may exist while intent remains pending. | Compare identity and exact canonical row: identical => acknowledge; absent => append/verify; divergent => `reconciliation_required`. |
| After `collection.closed`, before `reveal.published` | Frozen set exists; peer read remains denied. | Replay reconstitutes closed collection and later publishes/reconciles one manifest. |

Database corruption, an unknown migration checksum or a non-contiguous aggregate stream fails closed;
it is not handled by skipping events as a lenient UI reader would.

## 6. Replay algorithm and proof obligation

For each aggregate:

1. Select the latest verified compatible checkpoint, or the empty state at version zero.
2. Read accepted events after its global offset for that aggregate, ordered by `journal_offset`.
3. Verify event identity, schema digest, payload hash, aggregate-version contiguity and causation data.
4. Fold the exact reducer version without invoking any effect.
5. Compare the resulting aggregate version/state hash with `aggregate_heads`.
6. Quarantine/fail closed on mismatch; never repair authority from a projection or operational log.

```text
Replay(checkpoint, events, reducer_version) -> (aggregate_version, state_hash)

Replay(C, E, R) = Replay(C, E, R)
external_calls(Replay) = 0
```

Runtime-wide reconstruction consumes the global offset to build cursor-addressable projections.
Aggregate decisions use their own contiguous versions. Realtime clients may resume after a global
cursor or be required to fetch a consistent snapshot when the retained cursor has expired.

## 7. Publication, reveal and artifact persistence

Publication acceptance applies authenticated context before the command transaction. The agent
supplies only the fields allowed by [BusPublication](domain.md#buspublication). Within the atomic
transaction, the writer creates one `publication.persisted` event, one authoritative active
`publication_candidates` row and one byte-stable [PublicationReceipt](domain.md#publicationreceipt).
It does not create an official `messages` row. The receipt is emitted after commit; an identical
retry returns the same receipt bytes, while optional `transport_replayed` metadata stays outside the
receipt.

The tool response held by the agent/adapter is evidence about a candidate, not authority. It can
authorize an official contribution only when the parent/runtime independently loads the committed
event and authoritative active candidate row and matches version/status/event/message/offset,
logical publication key, payload hash and scoped idempotency key. Verification atomically CASes the
candidate, inserts the official `messages` row and appends both official acceptance events. Missing,
mismatched or abandoned evidence leaves the model completion merely terminal as a provider attempt;
it does not create an official contribution.

Effective input capture follows this ordering:

1. Runtime creates a provider-neutral [AgentInvocationPlan](domain.md#agentinvocationplan).
2. Adapter deterministically produces [MaterializedAgentInvocation](domain.md#materializedagentinvocation)
   from that plan; the artifact boundary finalizes the ordered effective-input manifest and exact
   provider-native invocation by hash.
3. Kernel validates plan/materialization digests and seals
   [AgentExecutionRequest](domain.md#agentexecutionrequest).
4. Only a later claimed, sandboxed and authority-fenced effect may start the sealed request.
5. Raw provider output is finalized separately, and only receipt verification of an active
   candidate can create an official contribution.

After `collection.closed`, the kernel derives one canonical ordered message/hash set. Its
[RevealManifest](domain.md#revealmanifest) and `reveal.published` event become durable before any
peer delivery. Delivered reveal content is referenced in the receiving attempt's effective-input
manifest, preserving exactly what that attempt could observe.

Recovery from `bus_publish` through attempt terminality follows persisted authority: after a lost
tool response, retrying the same key/digest returns the committed receipt; after provider completion,
the adapter presents its candidate receipt and terminal result to atomic outcome acceptance; after a
crash before outcome commit, recovery re-verifies the publication and retries that acceptance; after
commit, it returns the stored terminal receipt. Recovery never infers publication from raw output,
nor terminal acceptance from a candidate receipt alone. If the attempt becomes durably `unknown`
without recoverable terminal evidence, a retry-authorized command may CAS the active candidate to
`abandoned` and append `publication.candidate_abandoned`; only that committed transition releases
the logical key. Official acceptance and abandonment race on the same candidate version, so exactly
one can win and late evidence cannot revive an abandoned row.

## 8. Cross-store reconciliation

SQLite cannot atomically commit with the audit ledger. A durable effect intent therefore carries the
canonical row digest and stable opening/close identity. The materializer uses:

```text
existing identity + identical canonical row => already_applied, verify, acknowledge in journal
identity absent                           => append via validated appender, verify, acknowledge
existing identity + divergent row        => reconciliation_required, release nothing
```

No provider/tool effect may start before the opening acknowledgement event. A run becomes officially
closed only after the close row is similarly verified and acknowledged. The materializer never
writes YAML directly and never rewrites historical rows.

## 9. Security, retention and erasure boundary

OQ-ACI9 is settled only at the invariant boundary:

- effective inputs and raw provider outputs are immutable sensitive artifacts;
- journal payloads contain references/digests, not durable credentials or secrets;
- runtime operators receive minimum default access; break-glass is explicit and audited;
- non-local deployments require encryption at rest;
- erasure preserves a tombstone and provenance sufficient to explain missing content without
  requiring the reducer to read erased bytes.

Concrete TTLs, legal-hold precedence, keyed-digest policy, encryption keys and crypto-erasure periods
remain deferred to accepted Slice-1 retention and credential ADRs. No implicit infinite-retention or
plaintext-production default is authorized.

## 10. Usage persistence and rollups

Every reported record becomes an immutable usage event and `usage_observations` projection keyed to
attempt, provider, adapter and model. Input, cached-input, output, reasoning and provider-specific
dimensions remain nullable. Rollups may group by attempt, operation, seat, group, run and dispatch,
but they carry `source_through_offset`, observation count, missing-dimension counts, provider
semantics and currency where cost is present. Price/cost requires an applicable immutable
`pricing_sources` row and matching `pricing_digest`; only a successful compatible calculation
creates an immutable `cost_calculations` row. Usage, estimated cost and provider invoice remain
explicitly different authorities; none of these tables is presented as billing truth.

## 11. Acceptance fixtures required before implementation

1. Same key/same digest returns byte-identical receipt and unchanged event count.
2. Same key/different digest is a permanent conflict.
3. Two commands at the same expected version produce one CAS winner.
4. Crash at every transaction boundary yields either all four acceptance members or none.
5. Replay from zero and from a checkpoint yields the same aggregate/state hash and zero effects.
6. Duplicate publication retries yield one message/event/receipt logical set.
7. A forged authority field or forged receipt is rejected.
8. `collection.closed` without `reveal.published` remains unreadable after restart.
9. Audit row absent/identical/divergent exercises append, acknowledge and reconciliation-required.
10. `synchronous=FULL`, WAL and migration checksum are asserted at writer startup.
11. Mixed provider/model attempts populate the same canonical tables and event schemas.
12. Missing usage dimensions remain null through every rollup.
13. Unlimited retry attempts coexist with exactly zero or one `accepted_result=1` row per operation.
14. Start racing close/cancel/run-terminal loses when any `prerequisite_heads[]` value changes.
15. Every outcome-acceptance failpoint proves all-or-none receipt/event/head/effect-intent state and stable `outcome_digest` retry.
16. Manifest-entry uniqueness/FKs reject duplicate ordinals, duplicate messages and dangling references.
17. Rollups expose `source_through_offset` and missing counts; incompatible/missing prices create no cost calculation.
18. Candidate publication atomically creates event, active candidate and byte-identical receipt but no official message.
19. Official verification and abandonment race on candidate CAS; exactly one wins, and only the official winner creates `messages`/official events.
20. Terminal-unknown without recoverable evidence cannot release a candidate unless retry policy is persisted and authorizes abandonment.
21. Effect-outcome matrix covers nonterminal wrong epoch, terminal same digest and terminal different digest in both pre/post-response retry paths.

## 12. OQ disposition and gate status

| Question | Disposition | Consequence |
|---|---|---|
| OQ-ACI1 | **Ratified** | One SQLite/WAL database, one writer boundary, global offset, contiguous aggregate version and atomic receipt/events/head/new-intents transaction. |
| OQ-ACI7 | **Ratified** | `synchronous=FULL` throughout proof and pilot. |
| OQ-ACI4 | **Ratified by reference** | Frozen inputs are defined by [DispatchSpec](domain.md#dispatchspec); observations remain events. |
| OQ-ACI8 | **Ratified by reference** | Exact ordered effective input is one content-addressed artifact per attempt. |
| OQ-ACI9 | **Boundary ratified; parameters deferred** | Sensitive immutable references and tombstones are required; retention/key ADRs still block Slice 1. |

This draft does **not** set `workPackGateStatus=pass`. The W0 persistence ADR, schema/crash tests,
audit-writer drift disposition and sole-writer guard still require acceptance evidence.

## Connections

| Document | Type | Description |
|---|---|---|
| [Domain model](domain.md) | `maps` | Persistence identities and immutable values. |
| [Rules](rules.md) | `governed-by` | Atomicity, idempotency, authority and replay invariants. |
| [TASK-000](work-pack/tasks/TASK-000.md) | `specified-by` | W0 decision task this contract informs without completing. |
| [Engine constitution](../../../vault/constitution/engine-constitution.md) | `governed-by` | EG-1 scoped writer and EG-6 historical-artifact rules. |
| [Discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Sections 5.1–5.3 and OQ recommendations. |
