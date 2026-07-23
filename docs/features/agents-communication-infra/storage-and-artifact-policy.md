---
feature: agents-communication-infra
title: Storage, artifact and rebuild authority policy
status: accepted-independent-PASS
version: 1
date: 2026-07-23
runtime_gate: pass-for-exact-swu-mutation-only
---

# Storage, artifact and rebuild authority policy

## Physical ownership

| Boundary | Sole physical writer | Authoritative content |
|---|---|---|
| Event journal | `RuntimeJournal` | accepted command identity/digest/span, events and constrained acceptance facts |
| Artifact store | `ArtifactStore` | immutable BLOB bytes, metadata, classification, finalization identity and content digest |
| Audit ledger | validated `register-dispatch` appender | official dispatch opening and close rows |
| Projections | ACI `ProjectionManager` | no new authority; rebuildable query state only |

Logical services receive ports, never database handles. `RuntimeJournal` may coordinate one SQLite
transaction but cannot insert artifact BLOBs except through `ArtifactStore`; projection handlers
return pure changes and cannot execute SQL.

## Finalization before reference

For raw bytes, `ArtifactStore` validates media type, classification, size and retention metadata;
computes canonical content bytes and digest; inserts the BLOB, metadata and finalization record;
and only then permits an event/candidate/message reference in the same accepted transaction.
Pre-finalized references are dereferenced and digest-verified before use. Rollback removes every
member. No accepted event can reference missing, partial, mutable or digest-divergent bytes.

Raw model/provider output remains distinct from an official message. Final answers and large
research bodies appear in APT facts only by finalized artifact reference.

## Authority versus rebuildability

Authoritative or acceptance-critical rows:

- immutable migration and registered-profile bytes/digests;
- finalized artifact BLOB, metadata and digest;
- command identity, digest, accepted event span and idempotency fact;
- event envelope, payload reference and payload digest;
- aggregate heads and prerequisite heads used for CAS;
- publication candidate status/logical reservation;
- official `messages` fact.

Derived/rebuildable values:

- serialized `PublicationReceipt` response bytes, deterministically derived from the persisted
  candidate/event scope and checked on every verification;
- complete-command-group read responses;
- runtime and APT projection rows.

`command_receipts` are not deleted during rebuild: they are authoritative idempotency evidence.
Receipt response serialization may be recomputed and compared byte-for-byte.

## ProjectionManager

ACI owns registration, synchronous application and rebuild of all projection handlers. A handler:

1. consumes only complete committed command groups with first/last offsets;
2. reads payload bytes only through verified ArtifactStore dereference;
3. is pure over its prior state and input group;
4. returns deterministic upserts/deletes to the manager; and
5. cannot mutate authoritative tables.

Rebuild proof runs on a database copy, clears only declared rebuildable tables, replays verified
complete groups, compares projection/receipt digests, and proves authoritative-table hashes remain
unchanged.

## Enablement boundary

This policy authorizes no runtime code by itself. Test mutation requires the exact
`SWU-ACI-APT-VS-001` authorization receipt. Local pilot serving requires a later independent PASS.
Production, external networking, agent execution, materializer and audit-ledger cutover remain
blocked.
