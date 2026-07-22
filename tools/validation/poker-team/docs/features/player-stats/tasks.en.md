---
id: player-stats
feature: player-stats
title: Player Stats Tracking Tasks
summary: Dependency-ordered execution plan driven by alignment and layering audits.
status: implemented
pillar: operations
domain: player-stats-delivery
audience:
  - developers
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
  - queries.md
  - events.md
  - states.md
  - workflows.md
  - mappings.md
  - TEST-SPEC.md
includes: []
---

# Player Stats Tracking — Implementation Plan

> **Planning mode:** GSD-phase orchestration with DomainSpec semantic authority.
> **Complexity:** HIGH — cross-cutting rename, layering extraction, 14 concepts, 22 test obligations.
> **Source:** Consolidated from alignment audit (0 compliant / 4 partial / 10 missing / 2 extra) and layering audit (6 findings: 1 critical, 2 high, 2 medium, 1 low).

## Assumptions

1. `financial-settlement` feature owns bankroll reset, transaction creation, and gross bankroll computation. Player-stats emits events; settlement reacts.
2. Auth middleware pattern exists or will be created in `auth-access-control` — player-stats wires it but does not implement it.
3. Database migrations use Drizzle Kit (`npx drizzle-kit generate` / `npx drizzle-kit push`).
4. Event infrastructure is in-process for now (function call or simple EventEmitter); async bus deferred to platform work.

## Risks

| Risk                                                                       | Mitigation                                                                                        |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Rename breaks existing imports across repo                                 | Execute rename as isolated Wave 0 with full grep verification before proceeding                   |
| Financial settlement extraction creates temporarily broken settlement flow | Stub event handler in Wave 1; full settlement implementation is out of scope for player-stats     |
| Auth middleware not yet available                                          | Wire placeholder `requirePermission` that can be swapped; add `// TODO: wire auth-access-control` |

---

## Wave 0 — Rename & Schema Migration (foundation)

> Blocks all subsequent waves. No behavioral changes — pure rename and schema expansion.

| Task  | Type    | Concept IDs                        | Files                                                                                                              | Description                                                                                                                                                                                                                                                                   |
| ----- | ------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W0-T1 | backend | all                                | `backend/src/domain/daily-stats/` → `backend/src/domain/player-stats/`                                             | Rename domain directory from `daily-stats` to `player-stats`. Rename files: `daily-stats.entity.ts` → `player-stats.entity.ts`, `daily-stats.repository.ts` → `player-stats.repository.ts`. Delete `daily-stats-recording.service.ts` and its test (reimplemented in Wave 2). |
| W0-T2 | backend | all                                | `backend/src/use-cases/daily-stats/` → `backend/src/use-cases/player-stats/`                                       | Rename use-case directory. Rename `record-daily-stats.ts` → `record-player-stats.ts`, `record-daily-stats.test.ts` → `record-player-stats.test.ts`.                                                                                                                           |
| W0-T3 | backend | all                                | `backend/src/infrastructure/repositories/drizzle-daily-stats.repository.ts` → `drizzle-player-stats.repository.ts` | Rename repository file with updated imports.                                                                                                                                                                                                                                  |
| W0-T4 | backend | all                                | `backend/src/infrastructure/http/routes/daily-stats.routes.ts` → `player-stats.routes.ts`                          | Rename route file. Update route prefix from `/daily-stats` to `/player-stats`.                                                                                                                                                                                                |
| W0-T5 | backend | `player-stats.PlayerStatsSnapshot` | `backend/src/infrastructure/database/schema.ts`                                                                    | Rename `dailyStats` → `playerStats` export. Add missing columns: `rake`, `session_duration`, `source_type`, `status`, `updated_at`. Add unique constraint on `(player_id, date)`.                                                                                             |
| W0-T6 | backend | all                                | `backend/src/infrastructure/database/schema.ts`                                                                    | Add `statsSourceTypeEnum` (`MANUAL`, `IMPORT`, `API`) and `statsRecordStatusEnum` (`RECORDED`, `CORRECTED`) to Drizzle schema.                                                                                                                                                |
| W0-T7 | backend | —                                  | `backend/src/index.ts`, all import sites                                                                           | Update all import paths referencing `daily-stats` to `player-stats`. Search: `grep -rn "daily-stats\|dailyStats\|DailyStats" backend/src/`.                                                                                                                                   |
| W0-T8 | backend | —                                  | Drizzle migration                                                                                                  | Generate migration: `npx drizzle-kit generate`. Verify migration SQL adds columns and constraint.                                                                                                                                                                             |

**Verification:**

```bash
# Zero references to old naming remain
grep -rn "daily-stats\|dailyStats\|DailyStats\|daily_stats" backend/src/ | grep -v node_modules
# TypeScript compiles
cd backend && npx tsc --noEmit
```

---

## Wave 1 — Extract Financial Settlement Logic (critical layering fix)

> Unblocks clean domain model. Removes cross-domain behavior from player-stats bounded context.
> **Audit source:** Layering findings F1, F2, F3.

| Task  | Type    | Concept IDs | Files                                                                   | Description                                                                                                                                                                                                                                                                                                                                                                                             |
| ----- | ------- | ----------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W1-T1 | backend | —           | `backend/src/use-cases/player-stats/record-player-stats.ts`             | Strip lines 17–45 (gross bankroll computation, `getLimitBuyIn`, `calculateBankrollReset`, transaction creation, player bankroll mutation). Remove imports of `getLimitBuyIn`, `calculateBankrollReset`, `TransactionRepository`. Remove `TransactionRepository` and `PlayerRepository.update` from factory parameters. Use case should only: validate player exists → persist snapshot → return result. |
| W1-T2 | backend | —           | `backend/src/infrastructure/http/routes/player-stats.routes.ts`         | Remove `drizzleTransactionRepository` import and wiring. Use case factory now takes only `playerStatsRepo` and `playerRepo` (read-only for existence check).                                                                                                                                                                                                                                            |
| W1-T3 | backend | —           | New: `backend/src/use-cases/financial-settlement/settle-after-stats.ts` | **Stub only.** Create placeholder file that accepts a `PlayerStatsRecorded` event payload and contains `// TODO: move bankroll reset logic from old daily-stats use case`. Full implementation is `financial-settlement` feature scope.                                                                                                                                                                 |
| W1-T4 | backend | —           | `backend/src/use-cases/player-stats/record-player-stats.test.ts`        | Delete all bankroll/transaction assertions. Rewrite to test pure stats recording (player exists → snapshot created with input values → returned).                                                                                                                                                                                                                                                       |

**Verification:**

```bash
# Zero cross-domain imports in player-stats
grep -rn "import.*from.*limit\|import.*from.*bankroll\|import.*from.*transaction" backend/src/use-cases/player-stats/ backend/src/domain/player-stats/
# Tests pass
cd backend && npx vitest run src/use-cases/player-stats/
```

---

## Wave 2 — Align Domain Model with SPEC

> Establishes type-safe domain model matching all 4 domain concepts.
> **Audit source:** Alignment audit (4 partial, 10 missing), Layering finding F4.

| Task  | Type    | Concept IDs                                                      | Files                                                                        | Description                                                                                                                                                                                                                                                                                                                                                                              |
| ----- | ------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W2-T1 | backend | `player-stats.PlayerStatsSnapshot`                               | `backend/src/domain/player-stats/player-stats.entity.ts`                     | Redefine `PlayerStatsSnapshot` type with all 13 SPEC fields: `id`, `playerId`, `statDate` (rename from `date`), `hands`, `profit`, `rakeback`, `rake`, `closingBankroll`, `sessionDuration`, `sourceType`, `status`, `createdAt`, `updatedAt`. Rename `DailyStats` → `PlayerStatsSnapshot`. Rename `CreateDailyStatsInput` → `RecordPlayerStatsInput` with all 9 operation input fields. |
| W2-T2 | backend | `player-stats.StatsSourceType`, `player-stats.StatsRecordStatus` | `backend/src/domain/player-stats/player-stats.entity.ts`                     | Add TypeScript enum/union types: `StatsSourceType = 'MANUAL' \| 'IMPORT' \| 'API'` and `StatsRecordStatus = 'RECORDED' \| 'CORRECTED'`.                                                                                                                                                                                                                                                  |
| W2-T3 | backend | `player-stats.PlayerStatsWindow`                                 | New: `backend/src/domain/player-stats/player-stats-window.vo.ts`             | Create `PlayerStatsWindow` value object type with all 11 SPEC fields: `playerId`, `fromDate`, `toDate`, `totalHands`, `totalProfit`, `totalRakeback`, `totalRake`, `totalSessionMinutes`, `sessionCount`, `avgHandsPerDay`, `winrateBbPer100`.                                                                                                                                           |
| W2-T4 | backend | `player-stats.PlayerStatsSnapshot`                               | `backend/src/domain/player-stats/player-stats.repository.ts`                 | Expand `PlayerStatsRepository` interface: `create(data)`, `update(id, data)`, `findByPlayerAndDate(playerId, statDate)`, `findByPlayerId(playerId, filters?)`, `aggregateWindow(playerId, fromDate, toDate)`.                                                                                                                                                                            |
| W2-T5 | backend | `player-stats.PlayerStatsSnapshot`                               | `backend/src/infrastructure/repositories/drizzle-player-stats.repository.ts` | Implement expanded repository: map all entity fields, implement `findByPlayerAndDate` query, implement `aggregateWindow` with SQL sum/count, implement upsert via `ON CONFLICT (player_id, date)`.                                                                                                                                                                                       |

**Verification:**

```bash
cd backend && npx tsc --noEmit
```

---

## Wave 3 — Implement RecordPlayerStats Operation (rules + calculations)

> Core mutation logic with all 8 rules and 2 calculations.
> **Concept IDs:** `player-stats.RecordPlayerStats`, `player-stats.RecordStatsWorkflow`

| Task  | Type    | Concept IDs                      | Files                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----- | ------- | -------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W3-T1 | backend | `player-stats.RecordPlayerStats` | `backend/src/use-cases/player-stats/record-player-stats.ts`   | Implement full operation: (1) Validate R1: player exists → `PLAYER_NOT_FOUND`. (2) Validate R2: `statDate` format → `VALIDATION_ERROR`. (3) Validate R3: hands ≥ 0 integer → `VALIDATION_ERROR`. (4) Validate R4: sourceType in enum → `VALIDATION_ERROR`. (5) Validate R7: rake ≥ 0 → `VALIDATION_ERROR`. (6) Validate R8: sessionDuration ≥ 0 integer → `VALIDATION_ERROR`. (7) Check R5: `findByPlayerAndDate` for existing record. (8) If existing: check R6 at-least-one-field-changed → `NO_CHANGES_DETECTED`. (9) Compute C1 snapshotKey, C2 status (`RECORDED` or `CORRECTED`). (10) Upsert snapshot. (11) Return result with status indicator. |
| W3-T2 | backend | `player-stats.RecordPlayerStats` | `backend/src/domain/player-stats/player-stats.validation.ts`  | Create validation helpers: `validateStatDate(d)`, `validateHands(h)`, `validateSourceType(s)`, `validateRake(r)`, `validateSessionDuration(sd)`. Pure functions, testable in isolation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| W3-T3 | backend | `player-stats.RecordPlayerStats` | `backend/src/domain/player-stats/player-stats.corrections.ts` | Create `detectEffectiveChange(existing, input)` → returns `changedFields[]` or throws `NO_CHANGES_DETECTED`. Used by R6 enforcement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

**Verification:**

```bash
cd backend && npx tsc --noEmit
```

---

## Wave 4 — Implement Events + State Machine

> Wire domain events into the record flow.
> **Concept IDs:** `player-stats.PlayerStatsRecorded`, `player-stats.PlayerStatsCorrected`, `player-stats.PlayerStatsRecordLifecycle`

| Task  | Type    | Concept IDs                                                             | Files                                                         | Description                                                                                                                                                                                                                 |
| ----- | ------- | ----------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W4-T1 | backend | `player-stats.PlayerStatsRecorded`, `player-stats.PlayerStatsCorrected` | New: `backend/src/domain/player-stats/player-stats.events.ts` | Define event types: `PlayerStatsRecordedEvent { snapshotId, playerId, statDate, occurredAt }` and `PlayerStatsCorrectedEvent { snapshotId, playerId, statDate, changedFields[], occurredAt }`.                              |
| W4-T2 | backend | `player-stats.PlayerStatsRecordLifecycle`                               | `backend/src/use-cases/player-stats/record-player-stats.ts`   | After upsert, emit `PlayerStatsRecorded` (new record) or `PlayerStatsCorrected` (correction). Use simple callback/emitter pattern. Status transitions: `[new] → RECORDED`, `RECORDED → CORRECTED`, `CORRECTED → CORRECTED`. |

**Verification:**

```bash
cd backend && npx tsc --noEmit
```

---

## Wave 5 — Implement Queries

> Read paths for history and window aggregate.
> **Concept IDs:** `player-stats.GetPlayerStatsHistory`, `player-stats.GetPlayerStatsWindow`

| Task  | Type    | Concept IDs                          | Files                                                                        | Description                                                                                                                                                                                                                                                                                                                             |
| ----- | ------- | ------------------------------------ | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W5-T1 | backend | `player-stats.GetPlayerStatsHistory` | New: `backend/src/use-cases/player-stats/get-player-stats-history.ts`        | Query: accept `playerId`, optional `fromDate`/`toDate`, `limit` (default 50, max 200), `cursor`. Return newest-first page with `nextCursor`.                                                                                                                                                                                            |
| W5-T2 | backend | `player-stats.GetPlayerStatsWindow`  | New: `backend/src/use-cases/player-stats/get-player-stats-window.ts`         | Query: accept `playerId`, `fromDate`, `toDate`, optional `currentLimit`. Validate R1-R3 (dates valid, ordering). Aggregate via repository. Compute `avgHandsPerDay = totalHands / sessionCount`. Compute `winrateBbPer100 = (totalProfit / bbValue) / (totalHands / 100)` when `currentLimit` provided and `totalHands > 0`, else null. |
| W5-T3 | backend | `player-stats.GetPlayerStatsHistory` | `backend/src/infrastructure/repositories/drizzle-player-stats.repository.ts` | Add `findByPlayerFiltered(playerId, fromDate?, toDate?, limit, cursor)` with cursor-based pagination.                                                                                                                                                                                                                                   |

**Verification:**

```bash
cd backend && npx tsc --noEmit
```

---

## Wave 6 — Complete API Layer (routes, validation, auth, mappings)

> Full REST contract matching [PlayerStatsAPI](interfaces.md).
> **Concept IDs:** `player-stats.PlayerStatsAPI`, `player-stats.PlayerStatsEntityToHistoryItem`, `player-stats.PlayerStatsWindowToProjection`

| Task  | Type    | Concept IDs                                   | Files                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----- | ------- | --------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| W6-T1 | backend | `player-stats.PlayerStatsAPI`                 | `backend/src/infrastructure/http/routes/player-stats.routes.ts`          | Rewrite route file: (1) `POST /player-stats` — Zod schema matching 9 operation input fields, `requirePermission('player-stats.write.recordPlayerStats')`, wire `recordPlayerStats` use case, return 200/400/401/403/404/500 per interface contract. (2) `GET /player-stats/:playerId/history` — query params validation, auth, wire history query, return paginated response. (3) `GET /player-stats/:playerId/window` — query params validation, auth, wire window query, return aggregate projection. |
| W6-T2 | backend | `player-stats.PlayerStatsEntityToHistoryItem` | New: `backend/src/infrastructure/http/mappings/player-stats.mappings.ts` | Implement `toHistoryItem(snapshot)` and `toWindowProjection(window)` mapping functions per [mappings.md](mappings.md).                                                                                                                                                                                                                                                                                                                                                                                  |
| W6-T3 | backend | `player-stats.PlayerStatsAPI`                 | `backend/src/index.ts` or route registration                             | Update route registration: replace `dailyStatsRoutes` with `playerStatsRoutes`, prefix `/player-stats`.                                                                                                                                                                                                                                                                                                                                                                                                 |

**Verification:**

```bash
cd backend && npx tsc --noEmit
```

---

## Wave 7 — Complete Test Suite (22 TEST-SPEC obligations)

> All tests mapped to [TEST-SPEC.md](TEST-SPEC.md) test IDs.
> **Source:** 22 deterministic test obligations across 7 categories.

| Task  | Type  | Test IDs                                                                                         | Files                                                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----- | ----- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| W7-T1 | tests | DST-RULE-001, DST-RULE-002, DST-RULE-003, DST-RULE-004, DST-RULE-005, DST-RULE-006, DST-RULE-007 | `backend/src/use-cases/player-stats/record-player-stats.test.ts`           | 7 rule validation tests: (DST-RULE-001) unknown player → `PLAYER_NOT_FOUND`, (DST-RULE-002) invalid date → `VALIDATION_ERROR`, (DST-RULE-003) negative hands → `VALIDATION_ERROR`, (DST-RULE-004) invalid sourceType → `VALIDATION_ERROR`, (DST-RULE-005) unchanged correction → `NO_CHANGES_DETECTED`, (DST-RULE-006) negative rake → `VALIDATION_ERROR`, (DST-RULE-007) negative sessionDuration → `VALIDATION_ERROR`. |
| W7-T2 | tests | DST-CALC-001                                                                                     | `backend/src/use-cases/player-stats/record-player-stats.test.ts`           | Calculation test: new snapshot → status `RECORDED`; correction → status `CORRECTED`.                                                                                                                                                                                                                                                                                                                                     |
| W7-T3 | tests | DST-STATE-001, DST-STATE-002, DST-INV-001, DST-INV-002                                           | `backend/src/use-cases/player-stats/record-player-stats.test.ts`           | State/invariant tests: first write → `RECORDED` status, correction → `CORRECTED` status, unique per player/date enforced, hands never negative after persist.                                                                                                                                                                                                                                                            |
| W7-T4 | tests | DST-EVT-001, DST-EVT-002                                                                         | `backend/src/use-cases/player-stats/record-player-stats.test.ts`           | Event tests: new record → `PlayerStatsRecorded` emitted with correct payload, correction → `PlayerStatsCorrected` emitted with `changedFields`.                                                                                                                                                                                                                                                                          |
| W7-T5 | tests | DST-QUERY-001                                                                                    | New: `backend/src/use-cases/player-stats/get-player-stats-history.test.ts` | Query test: date filtering, newest-first ordering, cursor pagination, page size limits.                                                                                                                                                                                                                                                                                                                                  |
| W7-T6 | tests | DST-QUERY-002, DST-QUERY-003, DST-QUERY-004                                                      | New: `backend/src/use-cases/player-stats/get-player-stats-window.test.ts`  | Query tests: aggregates match sum of snapshots, avgHandsPerDay/winrate derived correctly, winrate null when no limit or zero hands.                                                                                                                                                                                                                                                                                      |
| W7-T7 | tests | DST-API-001, DST-API-002, DST-API-003                                                            | New: `backend/src/infrastructure/http/routes/player-stats.routes.test.ts`  | API contract tests: POST response codes/shape, GET history pagination/auth codes, GET window projection/auth codes.                                                                                                                                                                                                                                                                                                      |
| W7-T8 | tests | DST-WF-001                                                                                       | `backend/src/use-cases/player-stats/record-player-stats.test.ts`           | Workflow test: verify authorize → validate → persist → emit event sequence.                                                                                                                                                                                                                                                                                                                                              |

**Verification:**

```bash
cd backend && npx vitest run src/use-cases/player-stats/ src/infrastructure/http/routes/player-stats*
# All 22 TEST-SPEC obligations covered
```

---

## Wave 8 — Verification & Docs Sync

> Final audit gate before marking feature as `implemented`.

| Task  | Type          | Concept IDs | Files                                | Description                                                                              |
| ----- | ------------- | ----------- | ------------------------------------ | ---------------------------------------------------------------------------------------- |
| W8-T1 | cross-cutting | —           | —                                    | Run alignment audit: `domainspec-audit-alignment player-stats`. Target: 14/14 COMPLIANT. |
| W8-T2 | cross-cutting | —           | —                                    | Run layering audit: `domainspec-audit-layering player-stats`. Target: 0 findings.        |
| W8-T3 | cross-cutting | —           | —                                    | Run verification: `domainspec-verify-feature player-stats`. Target: PASS verdict.        |
| W8-T4 | docs          | —           | `docs/features/player-stats/SPEC.md` | Update frontmatter `status: implemented`.                                                |
| W8-T5 | docs          | —           | —                                    | Run `npm run docs:index` to refresh feature-map and tag-index.                           |

**Verification:**

```bash
npm run docs:index
# Verify indexes
cat docs/index/feature-map.md | grep player-stats
```

---

## Concept Traceability Matrix

| Concept ID                                    | Type          | Wave   | Tasks                      |
| --------------------------------------------- | ------------- | ------ | -------------------------- |
| `player-stats.PlayerStatsSnapshot`            | Entity        | W0, W2 | W0-T1, W0-T5, W2-T1        |
| `player-stats.StatsSourceType`                | Enum          | W0, W2 | W0-T6, W2-T2               |
| `player-stats.StatsRecordStatus`              | Enum          | W0, W2 | W0-T6, W2-T2               |
| `player-stats.PlayerStatsWindow`              | Value Object  | W2, W5 | W2-T3, W5-T2               |
| `player-stats.RecordPlayerStats`              | Operation     | W1, W3 | W1-T1, W3-T1, W3-T2, W3-T3 |
| `player-stats.GetPlayerStatsHistory`          | Query         | W5     | W5-T1, W5-T3               |
| `player-stats.GetPlayerStatsWindow`           | Query         | W5     | W5-T2                      |
| `player-stats.PlayerStatsAPI`                 | Interface     | W6     | W6-T1, W6-T3               |
| `player-stats.PlayerStatsRecorded`            | Event         | W4     | W4-T1, W4-T2               |
| `player-stats.PlayerStatsCorrected`           | Event         | W4     | W4-T1, W4-T2               |
| `player-stats.PlayerStatsRecordLifecycle`     | State Machine | W4     | W4-T2                      |
| `player-stats.RecordStatsWorkflow`            | Workflow      | W3, W4 | W3-T1, W4-T2               |
| `player-stats.PlayerStatsEntityToHistoryItem` | Mapping       | W6     | W6-T2                      |
| `player-stats.PlayerStatsWindowToProjection`  | Mapping       | W6     | W6-T2                      |

## Ownership Labels

- backend (W0–W7: 28 tasks)
- tests (W7: 8 tasks)
- docs (W8: 2 tasks)
- cross-cutting (W8: 3 tasks)

## Done Criteria

- All 14 SPEC concepts have compliant implementations.
- All 22 TEST-SPEC obligations are covered by passing automated tests.
- Zero cross-domain imports from `limit/`, `bankroll/`, `transaction/` in player-stats bounded context.
- Alignment audit returns 14/14 COMPLIANT.
- Layering audit returns 0 findings.
- Verification returns PASS verdict.
- Feature status updated to `implemented` with refreshed doc indexes.
