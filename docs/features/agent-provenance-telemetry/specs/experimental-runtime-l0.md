---
feature: agent-provenance-telemetry
artifact: experimental-runtime-l0
status: experimental
version: 0.1.0
created: 2026-07-23
last_updated: 2026-07-23
runtimeGate: shadow-only
productionCutoverGate: block
---

# Experimental Runtime L0: Session and Reference Scout

## Decision

This document permits one local SQLite vertical slice to test durable Session and Reference Scout
behavior. It does not promote the experiment to the ACI runtime, enable a production writer, mutate
the dispatch ledger contract or satisfy the feature's blocked mutation gate.

The experiment answers:

> After E0, do append-before-ack journal facts and command receipts deterministically rebuild
> Session and Reference Scout projections under retry, conflict and replay?

## Frozen boundaries

1. **Session is not Conversation.** Session is the durable orchestration context owned here.
   Conversation is a host-owned origin which may be named only by opaque `origin_kind` and
   `origin_ref`. One conversation may originate a Session; identity is never inferred in either
   direction.
2. **No transcript storage.** E0 stores no prompt, message, response, chain of thought or raw
   conversation body. It stores identifiers, bounded labels, lifecycle facts, digests and opaque
   evidence references only.
3. **No compression or masking yet.** E0 neither implements nor claims a privacy transform. The
   absence of raw conversation bodies is a data-minimization boundary, not a masking guarantee.
4. **Reference Scout is the product name.** `reference-probe` remains a legacy alias and remains in
   frozen v1 schema/profile identifiers. New operation and projection names use
   `reference_scout`.
5. **Publication-receipt spike is distinct.** The executable under
   `agents-communication-infra/experiments/bus-publication-probe/` tests publish/receipt mechanics;
   it is not the Reference Scout product capability.
6. **No unified residue metric.** `Residue.lean` entropy and
   `CodensityUnitResidue.lean` non-invertibility remain separate constructions. E0 introduces no
   `residue_score`, ordering, conversion or privileged metric. If source evidence carries
   `incommensurable` or `count_capped`, those states remain explicit and uncompressed.

## Authority model

Within the isolated experiment:

```text
validated command
      |
      v
SQLite transaction
  journal_events + command_receipts   <-- experimental authority
      |
      v
rebuildable projections
  sessions
  session_dispatch_links
  reference_scout_runs
  reference_recommendations
```

`journal_events` and `command_receipts` are the only experimental write authority. Projection rows
are caches and may be deleted and rebuilt from an accepted journal prefix. A projection mutation
without its accepted source event and receipt is invalid.

ACI remains the intended production authority. E0 must not claim ACI-compatible canonical bytes,
registered profile evidence or production receipts unless it actually invokes the registered ACI
boundary. Local receipts are visibly namespaced/marked experimental.

### Experimental authority tables

E0 accepts exactly one journal event per local command. It does not implement ACI multi-event atomic
groups.

| Table | Minimum fields and invariants |
|---|---|
| `journal_events` | Monotonic global `seq`; unique `event_id` and `operation_id`; closed `event_type`; `occurred_at`; local canonical `payload_json` plus `payload_digest`; `previous_event_hash` and unique `event_hash` forming one verified chain. |
| `command_receipts` | `receipt_id` in the `experimental_rcpt_*` namespace; unique `operation_id`; `command_name`; exact `payload_digest`; exactly one accepted `event_id`/`committed_seq`; local canonical `result_json` plus `result_digest`; unique `receipt_digest`; `created_at`. |

`receipt_digest` binds the experimental namespace, receipt/operation/command identities, payload
digest, accepted event/offset, result digest and commit instant. These local canonical JSON/digest
rules exist only to compare retries and replay inside E0; they do not claim ACI canonical bytes.

## Projection contract

### `sessions`

| Field | Constraint |
|---|---|
| `session_id` | Primary key; opaque and host-minted or runtime-minted. |
| `ensure_key` | Unique idempotency key for the originating execution context. |
| `origin_kind`, `origin_ref` | Opaque host-origin tuple; not a transcript and not Session identity. |
| `initial_name`, `current_name` | Bounded display labels; E0 may keep them equal because rename is deferred. |
| `started_at`, `last_activity_at` | Derived from accepted Session-linked facts. |
| `source_through_seq` | Last accepted E0 journal offset reflected by the row. |

### `session_dispatch_links`

| Field | Constraint |
|---|---|
| `session_dispatch_link_id` | Primary key. |
| `session_id` | Existing Session. |
| `dispatch_id` | Opaque external Dispatch-shaped identity; unique in E0. E0 has no authoritative Dispatch reader and does not prove external existence. |
| `linked_at`, `source_event_id` | Accepted link time and sole authoritative source event. |

`session.dispatch_linked` is the only persisted Session-to-Dispatch join. Any later `session_id` in
`subagents-dispatch.yaml` is derived correlation only and must carry a source-event reference; it
must not become a competing join authority.

### `reference_scout_runs`

| Field | Constraint |
|---|---|
| `scout_run_id` | Primary key; new product terminology. |
| `probe_id` | Frozen v1 compatibility identity mapped one-to-one to `scout_run_id`; not a second run. |
| `session_id` | Mandatory existing Session. |
| `dispatch_id` | Nullable opaque identity; when present it must resolve to the same Session through the E0 link projection, without claiming external existence. |
| `objective_ref` | Opaque bounded objective/evidence reference, never a raw conversation body. |
| `shape`, `source_mode` | Closed E0 enums: shape is `small` or `tensioned`; source mode is `internal`, `external` or `internal-and-external`. E0 persists them but launches neither shape. |
| `protocol_profile_id/version/digest` | Mandatory host-declared coordinates, syntactically validated and replayed exactly. They are `unverified_host_coordinates`, not ACI registration or Scout execution authorization. The pending APT lineage profile is not reused as an execution profile. |
| `state` | `requested`, `collecting`, `committed` or `delivered`. |
| `bundle_digest`, `committed_event_id`, `delivered_at` | Nullable until the corresponding accepted transition. |
| `requested_at` | Host-supplied request instant persisted by the accepted start command. |
| `source_through_seq` | Last accepted E0 journal offset reflected by the row. |

### `reference_recommendations`

| Field | Constraint |
|---|---|
| `recommendation_id` | Primary key. |
| `scout_run_id` | Existing Reference Scout run. |
| `reference_id` | Stable reference identity; unique within the run. |
| `source_class`, `locator_observed`, `access_state` | Host-observed bounded evidence; never inferred. |
| `found_by_seat_id`, `evaluated_by_seat_id` | Exact contributing/evaluating seat identities. |
| `evaluation`, `why_inspect` | Bounded recommendation result and navigation reason. |
| `comparability_state` | Nullable closed state: `comparable`, `incommensurable` or `count_capped`; no ordering or score. |
| `source_event_id` | The accepted bundle-commit event that materialized the recommendation. |
| `source_through_seq` | Exact commit event offset reflected by the row. |

`sessions.last_activity_at` is the maximum accepted event time among its start, Dispatch-link and
Scout lifecycle events. Replay updates it only from those accepted event types; recommendation rows
do not introduce a second clock.

## Command and receipt contract

The E0 Interface exposes these six local commands. They are adapter commands for the isolated proof,
not newly ratified DomainSpec Operations, production ACI wire names or an assertion that the full
Scout Workflow exists:

| Operation | Minimum accepted effect |
|---|---|
| `ensure_session` | Append `session.started` once and return/reuse its receipt. |
| `link_session_dispatch` | Append the sole `session.dispatch_linked` fact once. |
| `start_reference_scout` | Append `reference_scout.requested` for one validated Session lineage. |
| `publish_scout_contribution` | Persist a seat-attributed contribution before acknowledgement. |
| `commit_reference_bundle` | Atomically append a committed bundle fact and materialize its recommendations. |
| `deliver_reference_bundle` | Append delivery only after a committed bundle/receipt verifies. |

Missing profile coordinates, malformed digest syntax, out-of-enum shape/source mode and a caller
claiming `profile_verification_state=verified` are rejected before mutation. E0 cannot detect a
registry digest mismatch because it has no ACI registry reader; that proof remains a production
gate.

For local canonical command payload `p`, operation identity `o`, durable receipt `r` and journal delta
`ΔJ`:

```text
same(o, digest(p))    => ΔJ = 0 and same(r)
same(o), different digest(p) => conflict and ΔJ = 0
acknowledged(o)       => exists durable r bound to accepted event IDs
projection(o)         => derived only from the complete accepted transaction
```

Every mutating command uses one SQLite transaction covering semantic validation, journal append,
projection update and receipt persistence. A fault before commit exposes none of those effects. A
lost response after commit is recovered by the identical operation identity.

## Replay

The runtime must be able to:

1. read journal events in strict offset order;
2. reject the rebuild transaction at malformed, unknown, hash-invalid or out-of-order events rather
   than guess or expose a partial replacement;
3. build fresh projection tables in an empty target;
4. apply each accepted fact exactly once;
5. compare the rebuilt canonical projection rows with the live projections.

E0 has one global inclusive `seq` prefix. It does not implement the production verified-group
`requested_o`/`effective_as_of` distinction because every local command accepts one event. For live
projection `L`, an empty fresh projection `F`, local projector `P`, and explicit accepted prefix
`J≤seq_max`:

```text
canonical_local_rows(L at seq_max) = canonical_local_rows(P(F, J≤seq_max))
P(F, J≤seq_max ++ duplicate_retry_events=∅) = P(F, J≤seq_max)
```

Comparison includes all semantic columns, source event IDs and source offsets. It excludes only
SQLite physical row order and database-internal metadata; rows are sorted by declared primary key
and serialized with the E0 local canonical JSON function. There is no checkpoint in E0. The
production ACI adapter must replace this narrower prefix model with verified group boundaries.

Replay has no access to current conversations, mutable dispatch ledger rows, network sources or
filesystem heuristics.

## Ledger shadow boundary

E0 does not write `subagents-dispatch.yaml`. A future shadow materializer may derive a canonical
opening/closing row from accepted facts, but must invoke the sole strict ledger appender and then
reread/compare the durable row before acknowledging the effect.

- The ledger remains authority for official Dispatch opening/closing.
- The journal remains authority for runtime intent, Session links and Scout lifecycle.
- Existing v0.6.1 rows remain grandfathered byte-for-byte.
- A derived `session_id` is correlation, never link authority; it must reference the accepted
  `session.dispatch_linked` event.
- ID-only appender no-op is insufficient evidence of equivalence.
- Any mismatch becomes `reconciliation_required`; E0 performs no cutover or repair.

E0 may implement a read/compare-only reconciler now. It classifies each observed effect as
`absent`, `identical`, `divergent`, `malformed` or `orphan_close` and may persist only its own
discardable cursor/projection. It must not write YAML, invoke the appender, mark
`audit_verified=true` or release an external effect.

## Correlated operational logging

Structured E0 logs use an allowlist and may include:

```text
operation_id, event_id, receipt_id, event_type, journal_offset,
session_id, dispatch_id, scout_run_id, state, outcome, error_code
```

Logs must not include command payload JSON, objective text, locator bodies, prompts, messages,
responses, chain of thought, raw artifacts or transcripts. Correlation fields are observational and
cannot authorize mutation. A command receipt remains the durable proof; a log line never substitutes
for one.

## Required evidence

The E0 test suite must cover:

- schema migration from an empty database;
- happy path across all six operations;
- identical command retry returns the same receipt with zero journal delta;
- operation-ID reuse with a different payload conflicts with zero partial effects;
- duplicate and contradictory Session-to-Dispatch links;
- syntactically valid opaque Dispatch IDs are accepted without claiming external existence; missing
  or malformed IDs are rejected;
- Scout dispatch/session mismatch;
- missing/malformed host profile coordinates and out-of-enum shape/source mode;
- proof that persisted profile coordinates remain explicitly unverified by E0;
- publish-before-ack and commit-before-deliver;
- duplicate recommendation/reference identity;
- replay into empty projections and byte/canonical-row comparison;
- structured-log correlation across operation/event/receipt IDs with no raw command payload;
- ledger read/compare classification without YAML mutation;
- rejection of transcript-like/raw conversation fields;
- explicit preservation of `incommensurable` and `count_capped` if accepted as typed evidence;
- explicit absence of `residue_score`;
- process restart against the same SQLite file.

## Promotion and non-goals

E0 is successful when the isolated runtime passes the evidence above and remains visibly
experimental. It does not unlock production cutover.

Deferred:

- ACI profile registration and owner mutation-gate PASS;
- production bus/runtime integration;
- dispatch-ledger v0.7 design or appender changes;
- transcript/body artifacts, compression, masking and retention policy;
- external acquisition and multi-agent Scout launch;
- tensioned four-seat recipes, cross-group reveal and second round;
- UI/API deployment, recovery daemon, scale and multi-process writer arbitration;
- any theorem or metric unifying the two residue constructions.

## Connections

| Document | Type | Description |
|---|---|---|
| [Feature specification](SPEC.md) | `refines` | Adds an isolated experimental execution slice without changing the blocked production gate. |
| [Architecture](architecture.md) | `constrained-by` | Preserves ACI authority and projection-only APT persistence. |
| [Persistence and replay](persistence-and-replay.md) | `constrained-by` | Reuses append-before-ack, receipt and deterministic replay requirements. |
| [Coarse session registry](../session-registry.md) | `implements-experimentally` | Supplies the Session identity and sole Dispatch-link rules. |
| [Reference Scout](../probes/reference-scout-tool.md) | `implements-partially` | Implements lifecycle persistence, not source acquisition or multi-agent launch. |
