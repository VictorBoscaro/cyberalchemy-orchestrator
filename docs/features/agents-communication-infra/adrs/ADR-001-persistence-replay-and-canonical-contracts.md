---
feature: agents-communication-infra
adr: ADR-001
title: Persistence, replay and canonical contracts for Slice 0
status: accepted
acceptance_status: accepted-by-independent-review
acceptance_receipt: ../reviews/2026-07-21-swu-aci-001-implementation/REPORT.md
date: 2026-07-21
layer: L0
slice: S-000
swu: SWU-ACI-001
runtime_gate: block
---

# ADR-001: Persistence, replay and canonical contracts for Slice 0

## Status and decision boundary

This ADR is **accepted for the W0 decision scope** by the independent
[SWU-ACI-001 review receipt](../reviews/2026-07-21-swu-aci-001-implementation/REPORT.md). It is a documentation artifact for
`SWU-ACI-001`; it does not assert that production persistence, migrations, recovery or canonical
fixtures exist. It does not change `workPackGateStatus=block` and authorizes no runtime code.

An accepting review may freeze this contract for TASK-010. It must not release TASK-010 until every
other W0 entry obligation named by the [WORK-PACK](../WORK-PACK.md#gate-checks) is independently
satisfied. Audit-ledger materializer/cutover remains blocked on TASK-020 physical evidence, and a
real provider remains blocked until S-003/L2/W3.

## Context and controlling decisions

The runtime needs one recoverable authority for command deduplication, accepted events, aggregate
concurrency and durable effect intent. Those facts cannot be reconstructed from provider state,
the YAML audit ledger or projections. At the same time, acceptance identity must not depend on
Pydantic serialization defaults that may change across library releases.

This proposal accepts or specializes the following controlling decisions:

| Source | Decision applied here |
|---|---|
| [SPEC ACI-D2/ACI-D4/ACI-D11](../SPEC.md#decisions) | SQLite journal facts, YAML audit facts and artifact bytes retain distinct owners; replay reduces journal facts; durable effect intent and cross-store reconciliation are required. |
| [SPEC OQ-ACI1/OQ-ACI7/OQ-ETA1](../SPEC.md#open-question-disposition) | One SQLite/WAL authority, global offset, aggregate CAS and atomic acceptance; `synchronous=FULL`; Pydantic and canonical-byte policy must be pinned before runtime. |
| [ACI-R5](../rules.md#aci-r5--command-idempotency-is-not-conflict-tolerance) | Same scoped key and digest replays the stored receipt; another digest conflicts; stale target or prerequisite heads conflict. |
| [ACI-R6](../rules.md#aci-r6--atomic-local-acceptance) | Receipt, events, head and new intents are one transaction; effect-outcome acceptance is likewise all-or-none. |
| [ACI-R7](../rules.md#aci-r7--pure-replay) | Replay is a pure fold over verified persisted facts and invokes no effects. |
| [ACI-R14](../rules.md#aci-r14--durability-is-a-feature-level-contract) | WAL and `synchronous=FULL` are feature-level proof/pilot policy, not per-command tuning. |
| [ACI-R16](../rules.md#aci-r16--canonical-contract-policy) | Pydantic validates decoded models; versioned runtime-owned projection, canonical JSON and SHA-256 define acceptance identity. |
| [External Tool Adoptions ETD-1/ETD-2/ETD-4/ETD-6](../discovery/external-tool-adoptions.md#decisions-baked-in) | Keep the Python/FastAPI host; use Pydantic core only for validation; admit no external runtime authority or second normative Node schema. |

## Decision

### 1. Authority and physical writer

Use one local SQLite database as the authoritative store for command receipts, accepted events,
aggregate heads and effect intents. The runtime exposes one validated `EventJournal` write boundary
with one serialized, process-owned writer connection. Logical publishers and workers call that
boundary; they do not open independent write connections. Read-only connections may observe
committed state.

This writer does not own YAML audit-ledger bytes. Audit opening/close remains a durable effect
intent reconciled through the existing validated appender. Artifact content remains behind the
artifact boundary; journal rows store finalized references and digests.

Required connection policy at writer startup:

```text
PRAGMA journal_mode = WAL;       -- returned value must be "wal"
PRAGMA synchronous = FULL;       -- effective value must be 2
PRAGMA foreign_keys = ON;        -- effective value must be 1 on every connection
PRAGMA busy_timeout = 5000;      -- bounded pilot wait, milliseconds
```

The writer verifies effective values after setting them. A mismatch fails startup before accepting
commands. Every write starts with `BEGIN IMMEDIATE`; after the bounded busy wait expires, the
command returns a retryable `STORE_BUSY` without a success receipt or partial acceptance. The
runtime does not spin indefinitely and does not silently downgrade durability.

### 2. Logical schema and constraints

The implementation migration may add columns needed by the full DomainSpec, but it must preserve
the following authority and constraints. Types below are a schema sketch, not an executable
migration.

```sql
CREATE TABLE schema_migrations (
  version       INTEGER PRIMARY KEY CHECK (version > 0),
  name          TEXT NOT NULL UNIQUE,
  sha256        TEXT NOT NULL CHECK (
                  length(sha256) = 71
                  AND substr(sha256, 1, 7) = 'sha256:'
                  AND substr(sha256, 8) NOT GLOB '*[^0-9a-f]*'
                ),
  applied_at    TEXT NOT NULL
);

CREATE TABLE command_receipts (
  command_id          TEXT PRIMARY KEY,
  scope_key           TEXT NOT NULL,
  idempotency_key     TEXT NOT NULL,
  command_digest      TEXT NOT NULL,
  aggregate_id        TEXT NOT NULL,
  expected_version    INTEGER NOT NULL CHECK (expected_version >= 0),
  status              TEXT NOT NULL,
  result_receipt_json BLOB NOT NULL,
  first_offset        INTEGER,
  last_offset         INTEGER,
  created_at          TEXT NOT NULL,
  UNIQUE (scope_key, idempotency_key),
  CHECK ((first_offset IS NULL) = (last_offset IS NULL)),
  CHECK (first_offset IS NULL OR first_offset <= last_offset)
);

CREATE TABLE events (
  journal_offset      INTEGER PRIMARY KEY,
  event_id            TEXT NOT NULL UNIQUE,
  aggregate_type      TEXT NOT NULL,
  aggregate_id        TEXT NOT NULL,
  aggregate_version   INTEGER NOT NULL CHECK (aggregate_version > 0),
  event_type          TEXT NOT NULL,
  schema_ref          TEXT NOT NULL,
  schema_digest       TEXT NOT NULL,
  command_id          TEXT NOT NULL REFERENCES command_receipts(command_id),
  causation_id        TEXT,
  correlation_id      TEXT NOT NULL,
  recorded_at         TEXT NOT NULL,
  observed_at         TEXT,
  payload_ref         TEXT NOT NULL,
  payload_hash        TEXT NOT NULL,
  authority_context_json BLOB NOT NULL,
  UNIQUE (aggregate_id, aggregate_version)
);

CREATE TABLE aggregate_heads (
  aggregate_id      TEXT PRIMARY KEY,
  aggregate_type    TEXT NOT NULL,
  current_version   INTEGER NOT NULL CHECK (current_version >= 0),
  state_hash        TEXT NOT NULL,
  last_event_id     TEXT,
  last_offset       INTEGER,
  reducer_version   TEXT NOT NULL,
  FOREIGN KEY (last_event_id) REFERENCES events(event_id),
  FOREIGN KEY (last_offset) REFERENCES events(journal_offset),
  CHECK ((last_event_id IS NULL) = (last_offset IS NULL)),
  CHECK ((current_version = 0) = (last_event_id IS NULL))
);

CREATE TABLE effect_intents (
  effect_id           TEXT PRIMARY KEY,
  command_id          TEXT NOT NULL REFERENCES command_receipts(command_id),
  requested_event_id  TEXT NOT NULL REFERENCES events(event_id),
  effect_type         TEXT NOT NULL,
  payload_ref         TEXT NOT NULL,
  payload_digest      TEXT NOT NULL,
  retry_class         TEXT NOT NULL CHECK (retry_class IN ('retryable','non_retryable')),
  status              TEXT NOT NULL CHECK (status IN ('pending','claimed','succeeded','failed','unknown')),
  claim_epoch         INTEGER NOT NULL DEFAULT 0 CHECK (claim_epoch >= 0),
  claimed_by          TEXT,
  attempt_count       INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  outcome_event_id    TEXT UNIQUE REFERENCES events(event_id),
  outcome_digest      TEXT,
  UNIQUE (command_id, requested_event_id, effect_type),
  CHECK ((outcome_event_id IS NULL) = (outcome_digest IS NULL))
);
```

The executable schema must also include the constrained acceptance records and indexes specified
in [Persistence and Replay section 3](../persistence-and-replay.md#3-candidate-logical-schema),
including candidate/message logical uniqueness, attempt-winner uniqueness and foreign keys. A
projection used to validate a command is updated synchronously in the command transaction and must
have a database-enforced unique key; an asynchronous projection cannot guard acceptance.

`journal_offset` is the monotonically increasing committed cursor for the database. Offset gaps
from rolled-back allocation are allowed and invisible; clients must not require arithmetic density.
`aggregate_version` is contiguous per aggregate and unique with `aggregate_id`.

### 3. Atomic transaction boundary

The only conforming new-command path is:

```text
strictly validate decoded command and authenticated authority
project canonical command -> canonical bytes -> command_digest
BEGIN IMMEDIATE
  find receipt by (scope_key, idempotency_key)
  if found with same digest: end transaction; return stored receipt bytes
  if found with another digest: ROLLBACK; return IDEMPOTENCY_CONFLICT

  load target aggregate head and every canonical prerequisite_heads[] entry
  require target current_version == expected_version
  require every prerequisite version/state_hash still matches
  pure-reduce current state + command -> events[], effect_intents[], next_state
  validate event-version contiguity and synchronous uniqueness constraints
  reserve/insert command_receipt identity for event foreign keys
  insert all events and allocate their global journal offsets
  insert all new effect intents
  CAS aggregate head using WHERE current_version = expected_version; require one row
  update all synchronous constrained acceptance records
  finalize the byte-stable receipt and its event span
COMMIT
return only the stored receipt bytes
```

Any failed insert, invariant, prerequisite or CAS rolls back every member. The stored receipt cannot
be returned before commit. Implementations may order SQL members differently to satisfy immediate
foreign keys, but may not split receipt, event, head or new intent across transactions.

Effect-outcome acceptance is a second atomic command fenced by `(effect_id, claim_epoch)`. It
canonicalizes the outcome, compares an already-terminal digest before the active-claim check, then
commits the stable receipt, terminal event, head/constrained records and intent
status/epoch/outcome ID/outcome digest together. Same accepted digest returns the stored receipt;
another digest returns permanent `OUTCOME_CONFLICT`.

### 4. Migration, busy and corruption policy

Migrations are immutable, ordered UTF-8 files with monotonically increasing integer versions. Their
exact bytes are sealed as lowercase `sha256:<64 hex>` and recorded in `schema_migrations`.
`PRAGMA user_version` must equal the highest applied manifest version. Before exposing the writer,
startup compares the compiled migration manifest, table rows, checksums and `user_version`:

- a known unapplied suffix is applied in order under an exclusive migration transaction;
- an unknown applied version, missing historical version, checksum mismatch, downgrade or partially
  applied migration fails closed;
- an applied migration is never edited or automatically reversed; correction is a new migration;
- startup and migrations run with no command writer admitted.

Writer startup runs `PRAGMA quick_check` and requires `ok`. `SQLITE_CORRUPT`, `SQLITE_NOTADB`, a
failed check or a non-contiguous authoritative aggregate stream moves the store to quarantined
read-only diagnostics and rejects command/effect acceptance as `STORE_CORRUPT`. The runtime never
deletes rows, skips events, recreates the database or promotes a projection as automatic repair.
Recovery requires an operator-owned procedure and subsequent replay/hash verification; that
procedure is outside this ADR and remains a blocker for production readiness.

### 5. Pure replay

For each aggregate, replay selects the latest verified compatible checkpoint or version-zero empty
state, reads accepted events after its offset ordered by `journal_offset`, verifies event/schema/
payload digests and contiguous aggregate versions, and folds the exact `reducer_version`.

```text
Replay(checkpoint, events, reducer_version) -> (aggregate_version, state_hash)
same inputs => byte-identical canonical state and state_hash
providers + tools + materializers + clock + randomness + new events during replay = 0
```

The result must match `aggregate_heads`. A mismatch, unknown reducer/schema/migration or corrupt
prefix fails closed and is never repaired from an API projection, provider log or audit ledger.
Checkpoint use is optional and cannot delete uniqueness tombstones or required event history.

### 6. Pydantic and canonical acceptance bytes

For the Slice-0 proof/pilot, pin `pydantic==2.13.4` and `pydantic-core==2.46.4`. These are the exact
versions observed in the Python/FastAPI host when this proposal was written. Independent acceptance
still requires adding and verifying those exact pins in the implementation dependency artifact;
the current transitive dependency is not evidence. Any version change requires rerunning every
golden vector and explicitly accepting any byte difference.

Boundary models use strict validation, reject unknown fields unless a versioned schema explicitly
allows them, and validate before canonical projection. `model_dump`, `model_dump_json` and their
defaults are never accepted-byte authority.

Canonical contract version `aci-cjson-1` applies these rules:

1. The runtime projects the validated value into a versioned JSON-compatible envelope containing
   the explicit contract `schema_version`; provider-only and transport-only fields are excluded.
2. Object keys are strings, normalized to Unicode NFC, then sorted by Unicode scalar value.
   A normalization collision is invalid. Arrays retain schema-defined order.
3. String values are normalized to NFC and encoded as UTF-8 without a BOM. JSON control characters,
   quotation mark and reverse solidus use the required short JSON escapes; non-ASCII text is not
   ASCII-escaped.
4. A field absent from the decoded input remains omitted. A present nullable field remains JSON
   `null`. Validation defaults do not silently turn omission into an accepted field.
5. Booleans are JSON booleans, never integers. Integers use shortest base-10 form with no leading
   zero; an admitted integer spelling of `-0` projects to JSON integer `0`, so accepted bytes never
   contain negative zero. Binary floating-point values, NaN and infinities are forbidden in the
   canonical projection. Fractional domain quantities use a schema-defined canonical decimal
   string and unit/scale rather than a JSON float.
6. Objects use `,` and `:` with no surrounding whitespace. There is no trailing newline.
7. The digest is over exactly those bytes and its normative stored/compared/rendered value is
   `sha256:<lowercase 64-hex>`. A fixture may additionally expose the 64-character raw hexadecimal
   result as `sha256_hex`, but that derived helper is not a `ContentDigest` and cannot replace the
   prefixed `digest` assertion.

Golden fixtures must cover omission versus explicit null, composed versus decomposed Unicode,
post-normalization key collision, property order, integers including zero and negative values,
rejected floats/non-finite values, array order, schema-version change and exact digest bytes. A
cross-boundary validator such as Zod may consume these fixtures only after a real consumer is
inventoried; it cannot redefine them.

The schema-version case uses the same semantic body under two admitted explicit versions and proves
that both canonical bytes and prefixed digests differ. Integer coverage includes positive, zero,
negative, signed 64-bit boundaries and an input `-0` case whose canonical integer is `0`. Every
rejection vector must be independently executable: it supplies a complete input, or names a
versioned valid base plus one unambiguous mutation, and declares the stable error identity expected
from the targeted invariant. Rejection for an incidental missing field does not satisfy the vector.

The normative fixture and its test plan must record and assert both exact resolved versions,
`pydantic==2.13.4` and `pydantic-core==2.46.4`; a compatible range or a Pydantic-only assertion does
not freeze this ADR's dependency contract.

## Crash boundaries and recovery obligations

| Crash/failure point | Permitted durable observation | Required retry/recovery result |
|---|---|---|
| Before `BEGIN` or before command commit | No acceptance member. | Same key/digest may retry. |
| After any command SQL member, before commit | None; SQLite rolls back receipt, events, head, constrained records and intents. | Same key/digest converges; no receipt was returned. |
| After command commit, before response | Complete acceptance only. | Identical retry returns byte-identical stored receipt and no duplicate event/effect. |
| During effect-outcome transaction, before commit | No terminal member. | Same epoch/digest may retry; wrong epoch conflicts. |
| After effect-outcome commit, before response | Receipt, terminal event, head and terminal intent fields all exist. | Same digest returns stored receipt; another digest is `OUTCOME_CONFLICT`. |
| After effect claim, before external start | Durable claim; start may be absent. | Reconcile/status or redeliver only under persisted retry class and stable identity. |
| After external start, before accepted outcome | Outcome may be unknown. | Query status when supported; do not repeat a non-retryable effect; persist `unknown`. |
| `SQLITE_BUSY`/locked past 5 seconds | No new receipt or partial acceptance. | Return retryable `STORE_BUSY`; caller may retry with the same identity. |
| Corruption, unknown migration or checksum mismatch | No new writes. | Quarantine/fail closed; require operator recovery and verified replay. |
| After audit append, before journal acknowledgement | Exact audit row may exist while intent remains pending. | Identical row is verified/acknowledged; absence is appended through validated appender; divergence becomes `reconciliation_required`. |

TASK-010 must expose failpoints immediately before and after every SQL member and commit so the
all-or-none claims are executable rather than inferred.

## Alternatives considered

| Alternative | Disposition |
|---|---|
| PostgreSQL or a broker for Slice 0 | Rejected for the single-host pilot: adds operational authority without evidence that SQLite cannot satisfy the required proof. Revisit only through a superseding ADR. |
| JSONL/YAML journal | Rejected: cannot enforce the required CAS, uniqueness, FK and receipt/event/head/intent transaction as one local acceptance boundary. |
| Multiple SQLite writer connections/processes | Rejected for the pilot: conflicts with the selected serialized writer boundary and makes busy/fencing behavior needlessly ambiguous. |
| `synchronous=NORMAL` or per-command durability | Rejected by OQ-ACI7/ACI-R14. Relaxation requires measured fault evidence and a superseding feature-level decision. |
| Separate event, receipt and outbox transactions | Rejected: creates observable partial acceptance and lost/duplicate effect windows contrary to ACI-R6. |
| Treat Pydantic serialization as canonical | Rejected: library defaults do not freeze omitted/null, Unicode, numeric, ordering or upgrade behavior. |
| Adopt an external runtime or a second normative Zod schema | Rejected by ETD-1/ETD-4/ETD-6 because it overlaps authority or forks the contract. |
| Automatically rebuild authority after corruption from projections/provider logs | Rejected: those sources are not authoritative and would make replay non-auditable. |

## Decision acceptance and downstream implementation evidence

ADR acceptance in W0 and executable conformance in TASK-010 are deliberately separate gates. This
ADR was accepted for the **decision scope** of SWU-ACI-001 after an independent closure review
confirmed that:

1. this ADR is internally consistent with the controlling DomainSpec decisions;
2. the SQL contract fixture applies to a clean SQLite database and enforces the declared schema
   constraints under adversarial fixture checks;
3. the canonical corpus parses, reproduces its exact bytes/prefixed digests, covers the cases named
   in section 6 and records the exact Pydantic/Pydantic Core versions selected by this decision; and
4. the test plan names every downstream falsifier required for transaction, startup, crash and
   replay conformance.

That independent contract review is sufficient to accept the ADR. It does **not** require
production journal code, an implementation dependency diff/lock, runtime failpoint results or a
production recovery demonstration; requiring TASK-010 results to accept the ADR that authorizes
TASK-010 would create a gate cycle.

| Stage | Evidence | Required proof | Current reference/status |
|---|---|---|---|
| W0 ADR acceptance | Schema contract | Contract schema applies cleanly and its fixture checks reject duplicate IDs/versions/logical keys, dangling FKs, invalid transitions/statuses and malformed digests. | [Slice-0 schema contract fixture](fixtures/slice0-schema.sql); independently reviewed `PASS`. |
| W0 ADR acceptance | Canonical contract | Exact bytes/prefixed digests cover omitted/null, Unicode, numbers, ordering and schema version; fixture metadata freezes `pydantic==2.13.4` and `pydantic-core==2.46.4` as the implementation target. | [Canonical contract vectors](fixtures/canonical-contract-vectors.json); independently reviewed `PASS`. |
| W0 ADR acceptance | Executable obligations | Every required downstream falsifier has a unique, reviewable test name and expected result. | [SWU-ACI-001 test plan](fixtures/SWU-ACI-001-TEST-PLAN.md); independently reviewed `PASS`. |
| W0 ADR acceptance | Independent decision receipt | Reviewer accepts, amends or rejects this proposal and records unresolved risks without claiming runtime proof. | [Final PASS/PASS/PASS receipt](../reviews/2026-07-21-swu-aci-001-implementation/REPORT.md). |
| TASK-010 conformance | Transaction crash matrix | Runtime failpoints prove all-or-none command/effect-outcome membership and stable lost-response retry. | [T-ACI-R6](../TEST-SPEC.md#t-aci-r6--atomic-command-acceptance); executable evidence pending TASK-010. |
| TASK-010 conformance | Idempotency and CAS | Same digest replays; different digest conflicts; one version-race winner; prerequisite race loses. | [T-ACI-R5](../TEST-SPEC.md#t-aci-r5--idempotency-and-cas); executable evidence pending TASK-010. |
| TASK-010 conformance | Durability/startup | Runtime asserts effective WAL/FULL/FK/busy settings and migration checksums; mismatches fail closed. | [T-ACI-R14](../TEST-SPEC.md#t-aci-r14--sqlite-durability-policy); executable evidence pending TASK-010. |
| TASK-010 conformance | Replay | Runtime zero/checkpoint replay agrees and effect spies remain at zero; corrupt/gapped streams fail closed. | [T-ACI-R7](../TEST-SPEC.md#t-aci-r7--pure-replay); executable evidence pending TASK-010. |
| TASK-010 conformance | Dependency resolution | Production declaration/lock resolves exactly `pydantic==2.13.4` and `pydantic-core==2.46.4`, then the full canonical corpus passes. | `PENDING: TASK-010 implementation dependency diff and lock/install receipt` |

Accepting this ADR alone does not authorize TASK-010. TASK-010 may start only after B-001/B-002 and
B-003's W0 contract obligations satisfy the complete [WORK-PACK gate checks](../WORK-PACK.md#gate-checks).
Once that separate W0 entry gate passes, dependency locking and executable conformance are TASK-010
implementation obligations; a failure blocks TASK-010 completion and subsequent promotion, not the
prior architectural decision receipt.

## Consequences and unresolved blockers

The decision makes command acceptance, retry and replay falsifiable with one database and one
canonical-byte policy. It deliberately accepts SQLite single-writer throughput and stricter input
projection in exchange for unambiguous authority during the pilot.

It does **not** provide production SQLite code, applied dependency locks, an operator
corruption-recovery runbook, the complete W0 ADR set, target-host sole-writer evidence, sandbox
isolation, a real provider adapter, multiple providers/writers or persistent cost aggregation.
Therefore B-001 is only partially repaired; B-002 and B-003 remain open,
`workPackGateStatus` remains `block`, and
no runtime task is promoted by this file.

## Trace and review target

- Task contract: [TASK-000 / SWU-ACI-001](../work-pack/tasks/TASK-000.md#swu-aci-001--persistence-and-replay-adr)
- Candidate detailed contract: [Persistence and Replay](../persistence-and-replay.md)
- Interface boundary: [EventJournal](../interfaces.md#internal-eventjournal)
- External-tool review result: [PASS/PASS/PASS report](../reviews/2026-07-21-external-tools-spec-review/REPORT.md)
