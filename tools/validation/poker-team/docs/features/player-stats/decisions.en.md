---
id: player-stats
feature: player-stats
title: Player Stats Tracking Decisions
summary: Architecture and product decisions for player stats tracking behavior.
status: implemented
pillar: operations
domain: player-stats-decisions
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - queries.md
includes: []
---

## Confirmed Decisions

- Snapshot identity is `playerId + statDate` with upsert correction semantics.
- Tracking write contract is a single operation `RecordPlayerStats`.
- History ordering is newest-first by statDate then updatedAt.
- Window aggregates are deterministic sums from source snapshots.
- Permission model is explicit per capability (`write.record`, `read.history`, `read.window`).

## Open Decisions

- Whether to expose bulk import operation in v1 or defer to v2.
- Whether correction payload should require explicit reason field.

## Deferred Scope

- Multi-player batch upload API.
- Real-time streaming ingestion pipeline.
- Cross-region replication policy for stats writes.
