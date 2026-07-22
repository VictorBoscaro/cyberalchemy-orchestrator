---
id: player-progression-ui
feature: player-progression
title: Player Progression UI Specification
summary: Frontend design contract for progression eligibility check and criteria display.
status: draft
pillar: operations
domain: player-progression-ui
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
  - STORIES.md
includes: []
constitution: docs/UI-ARCHITECTURE.md
---

# UI Specification: Player Progression

> Governs the frontend presentation of progression eligibility checks and criteria breakdowns.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

---

## Route Table

| Route                       | Page Title         | Layout          | Auth Required | Permission                                    |
| --------------------------- | ------------------ | --------------- | ------------- | --------------------------------------------- |
| `/players/[id]/progression` | Player Progression | DashboardLayout | Yes           | `player-management.read.getPlayerProgression` |

---

## Page Layouts

### /players/[id]/progression

```
┌─────────────────────────────────────────────────┐
│ Header: "Progression: {playerName}"             │
│ Period: (●) Bi-weekly (15d)  ( ) Monthly (30d)  │
├─────────────────────────────────────────────────┤
│ ProgressionCard                                 │
│ ┌─────────────────────────────────────────────┐ │
│ │  Current Limit: NL40                        │ │
│ │  Eligible: ✅ YES  /  ❌ NO                 │ │
│ │  Reason: "Meets all criteria"               │ │
│ │                                             │ │
│ │  Criteria Breakdown                         │ │
│ │  ┌──────────┬──────────┬────────┬────────┐  │ │
│ │  │Criterion │Required  │Actual  │Met?    │  │ │
│ │  ├──────────┼──────────┼────────┼────────┤  │ │
│ │  │Avg Hands │≥1000/day │1,507   │✅      │  │ │
│ │  │Winrate   │≥7.5bb/100│8.2     │✅      │  │ │
│ │  └──────────┴──────────┴────────┴────────┘  │ │
│ │                                             │ │
│ │  Next Limit: NL60 (if eligible)             │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## Component Inventory

| Component               | Type  | Location                                           | Purpose                                 |
| ----------------------- | ----- | -------------------------------------------------- | --------------------------------------- |
| `ProgressionCard`       | Card  | `components/progression/ProgressionCard.tsx`       | Eligibility result + criteria breakdown |
| `CriteriaTable`         | Table | `components/progression/CriteriaTable.tsx`         | Criteria rows with met/not-met status   |
| `EligibilityBadge`      | Badge | `components/progression/EligibilityBadge.tsx`      | YES/NO eligibility display              |
| `PlayerProgressionPage` | Page  | `components/progression/PlayerProgressionPage.tsx` | Orchestrates period select + card       |

---

## Data Flow

### /players/[id]/progression

| API Call                                        | Hook                         | Cache Key                                     |
| ----------------------------------------------- | ---------------------------- | --------------------------------------------- |
| `GET /players/:id/progression?period=BI_WEEKLY` | `useProgression(id, period)` | `queryKeys.players.detail(id), "progression"` |

Period parameter maps:

- Bi-weekly radio → `period=BI_WEEKLY` (15 days)
- Monthly radio → `period=MONTHLY` (30 days)

---

## Form Contracts

### Period Selector (inline, not a submit form)

| Field  | Type   | HTML Input    | Options                      |
| ------ | ------ | ------------- | ---------------------------- |
| period | string | `radio-group` | BI_WEEKLY (default), MONTHLY |

Changing the radio refetches progression data automatically.

---

## State-to-UI Mapping

| Condition              | UI Representation                                  |
| ---------------------- | -------------------------------------------------- |
| Eligible for promotion | Green badge "Eligible", show next limit suggestion |
| Not eligible           | Red badge "Not Eligible", reason displayed         |
| Criterion met          | Green check icon + green text for actual value     |
| Criterion not met      | Red cross icon + red text for actual value         |
| Loading                | Skeleton card with shimmer                         |
| Player not found       | Error card with "Player not found" message         |

---

## Accessibility Requirements

| Component        | Requirement                                           |
| ---------------- | ----------------------------------------------------- |
| ProgressionCard  | Semantic heading, badge status announced              |
| CriteriaTable    | `role="table"`, met/not-met conveyed via `aria-label` |
| Period radio     | `role="radiogroup"`, `aria-label="Evaluation period"` |
| EligibilityBadge | `aria-label` includes "Eligible" or "Not eligible"    |
