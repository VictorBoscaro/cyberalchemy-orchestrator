---
id: player-stats
feature: player-stats
title: Player Stats Tracking User Stories
summary: Story set for player stats tracking with capability coverage and acceptance checks.
status: implemented
pillar: operations
domain: player-stats-stories
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
includes: []
---

# User Stories: Player Stats Tracking

> Navigate by capability: [Record Player Stats](#record-player-stats) · [Get Player Stats History](#get-player-stats-history) · [Get Player Stats Window](#get-player-stats-window)

## Record Player Stats

### US-01: Operations records daily stats for a player

As an **operations manager**, I want **to record a player's daily stats snapshot**, so that **performance tracking stays current and usable for decisions**.

**Given** the player exists and I have write permission
**When** I submit a valid stats payload for one player and statDate
**Then** the system persists a single authoritative snapshot and emits `PlayerStatsRecorded` or `PlayerStatsCorrected`

**Acceptance checks**

- [ ] Validation follows [RecordPlayerStats](operations.md#recordplayerstats) rules R1-R6.
- [ ] New records emit [PlayerStatsRecorded](events.md#playerstatsrecorded).
- [ ] Corrections emit [PlayerStatsCorrected](events.md#playerstatscorrected).
- [ ] Lifecycle follows [PlayerStatsRecordLifecycle](states.md#playerstatsrecordlifecycle).

**Domain coverage**

- Concepts: [PlayerStatsSnapshot](domain.md#playerstatssnapshot), [RecordPlayerStats](operations.md#recordplayerstats)
- States/Rules: [PlayerStatsRecordLifecycle](states.md#playerstatsrecordlifecycle)
- Interfaces/Flows: [POST /player-stats](interfaces.md#post-player-stats), [RecordStatsWorkflow](workflows.md#recordstatsworkflow)

**Capability links**

- [Record Player Stats](SPEC.md#record-player-stats)

## Get Player Stats History

### US-02: Operations reviews player stats history timeline

As an **operations analyst**, I want **to review historical tracked snapshots for one player**, so that **I can audit progression and corrections over time**.

**Given** I have read permission and a valid player id
**When** I query player history with optional date filters and pagination
**Then** I receive newest-first snapshots and a deterministic next cursor when more data exists

**Acceptance checks**

- [ ] Query behavior follows [GetPlayerStatsHistory](queries.md#getplayerstatshistory).
- [ ] Response mapping follows [PlayerStatsEntityToHistoryItem](mappings.md#playerstatsentitytohistoryitem).
- [ ] API behavior follows [GET /player-stats/:playerId/history](interfaces.md#get-player-statsplayeridhistory).

**Domain coverage**

- Concepts: [GetPlayerStatsHistory](queries.md#getplayerstatshistory), [PlayerStatsSnapshot](domain.md#playerstatssnapshot)
- States/Rules: [RecordPlayerStats](operations.md#recordplayerstats)
- Interfaces/Flows: [GET /player-stats/:playerId/history](interfaces.md#get-player-statsplayeridhistory)

**Capability links**

- [Get Player Stats History](SPEC.md#get-player-stats-history)

## Get Player Stats Window

### US-03: Player overview and settlement consume aggregated stats window

As a **downstream feature consumer**, I want **windowed player stats aggregates**, so that **overview and settlement calculations use deterministic inputs**.

**Given** a player and date window
**When** I request the stats window projection
**Then** I receive totalHands, totalProfit, totalRakeback, totalRake, totalSessionMinutes, sessionCount, avgHandsPerDay, and optionally winrateBbPer100 derived from matching snapshots

**Acceptance checks**

- [ ] Aggregation behavior follows [GetPlayerStatsWindow](queries.md#getplayerstatswindow).
- [ ] Projection mapping follows [PlayerStatsWindowToProjection](mappings.md#playerstatswindowtoprojection).
- [ ] Cross-feature consumption aligns with [Produces For](SPEC.md#produces-for).

**Domain coverage**

- Concepts: [GetPlayerStatsWindow](queries.md#getplayerstatswindow), [PlayerStatsWindow](domain.md#playerstatswindow)
- States/Rules: [RecordPlayerStats](operations.md#recordplayerstats)
- Interfaces/Flows: [GET /player-stats/:playerId/window](interfaces.md#get-player-statsplayeridwindow)

**Capability links**

- [Get Player Stats Window](SPEC.md#get-player-stats-window)

## Error And Edge Cases

### US-04: Invalid and duplicate tracking inputs are rejected deterministically

As an **operations user**, I want **invalid tracking payloads and unauthorized calls rejected consistently**, so that **the stats ledger stays correct and auditable**.

**Given** malformed input, missing permission, or invalid date range
**When** I call write or read stats endpoints
**Then** the system returns structured validation or authorization errors and does not persist invalid data

**Acceptance checks**

- [ ] Invalid payloads and ranges follow [Error States](operations.md#error-states) and [queries](queries.md).
- [ ] Auth failures follow [External: PlayerStatsAPI (REST)](interfaces.md#external-playerstatsapi-rest).
- [ ] No invalid transitions violate [PlayerStatsRecordLifecycle](states.md#playerstatsrecordlifecycle) invariants.

**Domain coverage**

- Concepts: [RecordPlayerStats](operations.md#recordplayerstats), [GetPlayerStatsHistory](queries.md#getplayerstatshistory), [GetPlayerStatsWindow](queries.md#getplayerstatswindow)
- States/Rules: [PlayerStatsRecordLifecycle](states.md#playerstatsrecordlifecycle)
- Interfaces/Flows: [External: PlayerStatsAPI (REST)](interfaces.md#external-playerstatsapi-rest), [RecordStatsWorkflow](workflows.md#recordstatsworkflow)

**Capability links**

- [Record Player Stats](SPEC.md#record-player-stats)
- [Get Player Stats History](SPEC.md#get-player-stats-history)
- [Get Player Stats Window](SPEC.md#get-player-stats-window)

## Story Coverage Matrix

| Capability | Story IDs | Covered Concepts | Notes |
| ---------- | --------- | ---------------- | ----- |
| Record Player Stats | US-01, US-04 | player-stats.RecordPlayerStats, player-stats.PlayerStatsSnapshot, player-stats.PlayerStatsRecorded, player-stats.PlayerStatsCorrected | Admin/operations + edge coverage |
| Get Player Stats History | US-02, US-04 | player-stats.GetPlayerStatsHistory, player-stats.PlayerStatsEntityToHistoryItem | Public journey (consumer read) + edge coverage |
| Get Player Stats Window | US-03, US-04 | player-stats.GetPlayerStatsWindow, player-stats.PlayerStatsWindow, player-stats.PlayerStatsWindowToProjection | Cross-feature integration + edge coverage |
