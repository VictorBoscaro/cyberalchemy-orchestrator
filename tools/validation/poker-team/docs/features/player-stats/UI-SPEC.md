---
id: player-stats-ui
feature: player-stats
title: Player Stats UI Specification
summary: Frontend design contract for stats recording, history, and rolling window views.
status: draft
pillar: platform
domain: player-stats-ui
audience:
  - developers
priority: p1
lang: en
owners:
  - web-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - interfaces.md
  - operations.md
  - queries.md
  - states.md
  - events.md
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Player Stats

> Governs the frontend presentation of stats recording, history viewing, and rolling window summaries.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

---

## Route Table

| Route                 | Page Title   | Layout          | Auth Required | Permission                                |
| --------------------- | ------------ | --------------- | ------------- | ----------------------------------------- |
| `/players/[id]/stats` | Player Stats | DashboardLayout | Yes           | `player-stats.read.getPlayerStatsHistory` |
| `/stats/record`       | Record Stats | DashboardLayout | Yes           | `player-stats.write.recordPlayerStats`    |

---

## Page Layouts

### /players/[id]/stats (Player Stats)

```
┌─────────────────────────────────────────────────┐
│ Header: "Stats: {playerName}"                   │
├─────────────────────────────────────────────────┤
│ StatsWindowCard                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ Period: [fromDate] to [toDate]              │ │
│ │ ┌──────────┬──────────┬──────────┬────────┐ │ │
│ │ │ Hands    │ Profit   │ Rakeback │Winrate │ │ │
│ │ │ 45,200   │ $3,400   │ $800     │7.2bb   │ │ │
│ │ └──────────┴──────────┴──────────┴────────┘ │ │
│ │ Sessions: 30  │  Avg hands/day: 1,507      │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ StatsHistoryTable                               │
│ ┌──────┬──────┬───────┬────────┬──────┬───────┐ │
│ │Date  │Hands │Profit │Rakeback│Rake  │Source │ │
│ ├──────┼──────┼───────┼────────┼──────┼───────┤ │
│ │04/15 │1800  │$120   │$30     │$45   │MANUAL │ │
│ └──────┴──────┴───────┴────────┴──────┴───────┘ │
│ [Load more]                                     │
│                                                 │
│ [+ Record Stats] button                         │
└─────────────────────────────────────────────────┘
```

### /stats/record (Record Stats)

```
┌─────────────────────────────────────────────────┐
│ Header: "Record Stats"                          │
├─────────────────────────────────────────────────┤
│ RecordStatsForm                                 │
│   Player    [Select player ▼]                   │
│   Date      [2026-04-15]                        │
│   Hands     [________]                          │
│   Profit    [________]                          │
│   Rakeback  [________]                          │
│   Rake      [________]                          │
│   Closing   [________]                          │
│   Duration  [________] min                      │
│   Source    [MANUAL ▼]                           │
│             [Record Stats]                      │
└─────────────────────────────────────────────────┘
```

---

## Component Inventory

| Component           | Type  | Location                                 | Purpose                                 |
| ------------------- | ----- | ---------------------------------------- | --------------------------------------- |
| `StatsWindowCard`   | Card  | `components/stats/StatsWindowCard.tsx`   | Rolling window aggregate summary        |
| `StatsHistoryTable` | Table | `components/stats/StatsHistoryTable.tsx` | Paginated stats history with cursor     |
| `RecordStatsForm`   | Form  | `components/stats/RecordStatsForm.tsx`   | Form to record/correct daily stats      |
| `StatsStatusBadge`  | Badge | `components/stats/StatsStatusBadge.tsx`  | RECORDED/CORRECTED badge                |
| `PlayerStatsPage`   | Page  | `components/stats/PlayerStatsPage.tsx`   | Orchestrates window + history + actions |

---

## Data Flow

### /players/[id]/stats

| API Call                                     | Hook                           | Cache Key                                |
| -------------------------------------------- | ------------------------------ | ---------------------------------------- |
| `GET /player-stats/:id/window?from&to`       | `useStatsWindow(id, from, to)` | `queryKeys.players.stats(id), "window"`  |
| `GET /player-stats/:id/history?limit&cursor` | `useStatsHistory(id)`          | `queryKeys.players.stats(id), "history"` |

### /stats/record

| API Call             | Hook               | On Success                                 |
| -------------------- | ------------------ | ------------------------------------------ |
| `GET /players`       | `usePlayers()`     | Populate player select                     |
| `POST /player-stats` | `useRecordStats()` | Invalidate stats cache, show success toast |

---

## Form Contracts

### RecordStatsForm

| Field           | Type    | HTML Input | Validation                  | Error Message                   |
| --------------- | ------- | ---------- | --------------------------- | ------------------------------- |
| playerId        | string  | `select`   | Required                    | "Select a player"               |
| statDate        | string  | `date`     | Required, valid date        | "Date is required"              |
| hands           | integer | `number`   | Required, >= 0              | "Hands must be 0 or greater"    |
| profit          | number  | `number`   | Required                    | "Profit is required"            |
| rakeback        | number  | `number`   | Required                    | "Rakeback is required"          |
| rake            | number  | `number`   | Required, >= 0              | "Rake must be 0 or greater"     |
| closingBankroll | number  | `number`   | Required                    | "Closing bankroll is required"  |
| sessionDuration | integer | `number`   | Required, >= 0              | "Duration must be 0 or greater" |
| sourceType      | string  | `select`   | Required, MANUAL/IMPORT/API | "Select source type"            |

**Zod schema:**

```typescript
z.object({
  playerId: z.string().min(1, "Select a player"),
  statDate: z.string().min(1, "Date is required"),
  hands: z.coerce.number().int().min(0, "Hands must be 0 or greater"),
  profit: z.coerce.number({ required_error: "Profit is required" }),
  rakeback: z.coerce.number({ required_error: "Rakeback is required" }),
  rake: z.coerce.number().min(0, "Rake must be 0 or greater"),
  closingBankroll: z.coerce.number({
    required_error: "Closing bankroll is required",
  }),
  sessionDuration: z.coerce
    .number()
    .int()
    .min(0, "Duration must be 0 or greater"),
  sourceType: z.enum(["MANUAL", "IMPORT", "API"], {
    required_error: "Select source type",
  }),
});
```

**Error Code → UI Message Mapping:**

| API Error Code     | HTTP Status | UI Message              |
| ------------------ | ----------- | ----------------------- |
| `PLAYER_NOT_FOUND` | 404         | "Player not found."     |
| (validation)       | 400         | Show field-level errors |

---

## State-to-UI Mapping

| Record Status | Badge Variant | Color             | Label     |
| ------------- | ------------- | ----------------- | --------- |
| RECORDED      | `default`     | `text-green-500`  | Recorded  |
| CORRECTED     | `outline`     | `text-yellow-500` | Corrected |

---

## Accessibility Requirements

| Component         | Requirement                                              |
| ----------------- | -------------------------------------------------------- |
| StatsHistoryTable | `role="table"`, sortable columns with `aria-sort`        |
| StatsWindowCard   | Semantic heading, values labeled with `aria-label`       |
| RecordStatsForm   | `role="form"`, focus on first input, error announcements |
| Load more button  | `aria-label="Load more stats entries"`                   |
