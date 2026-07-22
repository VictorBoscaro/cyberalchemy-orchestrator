---
id: player-progression-stories
feature: player-progression
title: Player Progression User Stories
summary: Capability-scoped user stories for player progression evaluation.
status: implemented
pillar: operations
domain: player-progression
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
includes: []
---

# Player Progression — User Stories

## US-01: Public Journey — Check Player Progression Status

**As a** operations manager,
**I want** to check a player's promotion readiness for a given period,
**so that** I can decide whether to promote the player to the next limit.

### BDD

**Given** a player with id "p1" exists with currentLimit "NL20"
**And** the player has stats entries within the last 15 days
**When** I call GET /players/p1/progression
**Then** the response contains `eligibleForPromotion`, `reason`, `avgHands`, `winrate`, `period`
**And** `period` is "BI_WEEKLY" (default)

### Acceptance Checks

- [ ] Response shape matches [ProgressionResult](domain.md#progressionresult)
- [ ] Default period is BI_WEEKLY (15 days)
- [ ] `period=MONTHLY` maps to 30-day window
- [ ] Links: [CheckProgression](operations.md#checkprogression), [GetProgressionStatus](queries.md#getprogressionstatus)

---

## US-02: Admin Operations Journey — Evaluate Monthly Progression

**As a** operations manager,
**I want** to evaluate a player's monthly progression,
**so that** I can assess longer-term performance trends.

### BDD

**Given** a player with sufficient stats over 30 days
**When** I call GET /players/p1/progression?period=MONTHLY
**Then** the response contains `period: "MONTHLY"`
**And** criteria are evaluated over 30 days

### Acceptance Checks

- [ ] Period parameter correctly switches evaluation window
- [ ] avgHands is computed as totalHands / periodDays
- [ ] winrate is computed as (totalProfit / bbValue) / (totalHands / 100)
- [ ] Links: [CheckProgression](operations.md#checkprogression)

---

## US-03: Cross-Feature Integration — Progression Delegates to Stats

**As a** the player-management module,
**I want** to delegate progression checks to player-progression,
**so that** progression logic is encapsulated and reusable.

### BDD

**Given** player-management registers GET /players/:id/progression
**When** the route handler is invoked
**Then** it calls `checkProgressionUseCase` with `playerStatsRepo` and `playerRepo`
**And** the use-case reads player stats via [player-stats](../player-stats/SPEC.md)

### Acceptance Checks

- [ ] Route is registered under player-management prefix
- [ ] Permission is `player-management.read.getPlayerProgression`
- [ ] Use-case depends on PlayerStatsRepository (not DailyStatsRepository)
- [ ] Links: [player-management.PlayerAPI](../player-management/interfaces.md#get-playersidprogression)

---

## US-04: Error and Edge Case Journey — Handle Missing Player and Empty Stats

**As a** the system,
**I want** to return clear error responses for invalid progression checks,
**so that** callers can handle failures gracefully.

### BDD

**Scenario: Player not found**
**Given** no player exists with id "missing"
**When** I call GET /players/missing/progression
**Then** the response is 404 with code "PLAYER_NOT_FOUND"

**Scenario: No stats in period**
**Given** a player exists but has no stats entries
**When** I call GET /players/p1/progression
**Then** `eligibleForPromotion` is false
**And** `reason` is "No stats in period"
**And** `avgHands` is 0 and `winrate` is 0

**Scenario: Invalid period query**
**Given** a valid player id
**When** I call GET /players/p1/progression?period=WEEKLY
**Then** the response is 400 with code "VALIDATION_ERROR"

### Acceptance Checks

- [ ] 404 for unknown player
- [ ] 401 without auth token
- [ ] 403 without required permission
- [ ] Invalid period returns deterministic 400 validation error
- [ ] Empty stats returns deterministic zero result
- [ ] Links: [CheckProgression error states](operations.md#checkprogression)

---

## Story Coverage Matrix

| Capability       | US-01 | US-02 | US-03 | US-04 |
| ---------------- | ----- | ----- | ----- | ----- |
| CheckProgression | ✓     | ✓     | ✓     | ✓     |
| BI_WEEKLY period | ✓     |       |       | ✓     |
| MONTHLY period   |       | ✓     |       |       |
| Cross-module     |       |       | ✓     |       |
| Error handling   |       |       |       | ✓     |
