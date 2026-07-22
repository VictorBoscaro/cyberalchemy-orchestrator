---
id: player-makeup-ui
feature: player-makeup
title: Player Makeup UI Specification
summary: Frontend design contract for makeup viewing, adjustment, history, and policy management.
status: draft
pillar: finance
domain: player-makeup-ui
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

# UI Specification: Player Makeup

> Governs the frontend presentation of makeup debt tracking, adjustments, history, and policy configuration.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

**Note:** This feature has a partial UI implementation. The spec documents both existing and missing functionality (policy editing).

---

## Route Table

| Route                  | Page Title    | Layout          | Auth Required | Permission                      |
| ---------------------- | ------------- | --------------- | ------------- | ------------------------------- |
| `/players/[id]/makeup` | Player Makeup | DashboardLayout | Yes           | `player-makeup.read.viewMakeup` |

---

## Page Layouts

### /players/[id]/makeup

```
┌─────────────────────────────────────────────────┐
│ Header: "Makeup: {playerName}"                  │
│ Player selector: [Select player ▼]              │
├─────────────────────────────────────────────────┤
│ MakeupSummaryCard                               │
│ ┌─────────────────────────────────────────────┐ │
│ │ Current Makeup: $1,250                      │ │
│ │ Status: ● In Debt                           │ │
│ │ [Adjust Makeup]  [Edit Policy]              │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ MakeupPolicyCard                                │
│ ┌─────────────────────────────────────────────┐ │
│ │ Apply profit first:    Yes                  │ │
│ │ Apply rakeback second: Yes                  │ │
│ │ Player rakeback share: 50%                  │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ AdjustMakeupDialog (modal)                      │
│   Operation: (●) Increase  ( ) Decrease  ( ) Set│
│   Amount:    [________]                         │
│   Reason:    [________________]                 │
│   [Apply]  [Cancel]                             │
│                                                 │
│ EditPolicyDialog (modal) — NEW                  │
│   Apply profit first:    [✓]                    │
│   Apply rakeback second: [✓]                    │
│   Rakeback share:        [0.50___]              │
│   [Save Policy]  [Cancel]                       │
│                                                 │
│ MakeupHistoryTable                              │
│ ┌──────┬───────────────────┬────────┬─────────┐ │
│ │Date  │Type               │Amount  │Created  │ │
│ ├──────┼───────────────────┼────────┼─────────┤ │
│ │04/15 │MAKEUP_ADJUSTMENT  │+$500   │10:30    │ │
│ │04/14 │MAKEUP_APPLIED     │-$200   │23:00    │ │
│ └──────┴───────────────────┴────────┴─────────┘ │
│ [Load more]                                     │
└─────────────────────────────────────────────────┘
```

---

## Component Inventory

| Component               | Type   | Location                                      | Purpose                               |
| ----------------------- | ------ | --------------------------------------------- | ------------------------------------- |
| `PlayerMakeupDashboard` | Page   | `components/makeup/PlayerMakeupDashboard.tsx` | Orchestrator for all makeup sub-views |
| `MakeupSummaryCard`     | Card   | `components/makeup/MakeupSummaryCard.tsx`     | Current debt display + actions        |
| `MakeupPolicyCard`      | Card   | `components/makeup/MakeupPolicyCard.tsx`      | Read-only policy display              |
| `AdjustMakeupDialog`    | Dialog | `components/makeup/AdjustMakeupDialog.tsx`    | Increase/decrease/set makeup form     |
| `EditPolicyDialog`      | Dialog | `components/makeup/EditPolicyDialog.tsx`      | **NEW** — Policy edit form            |
| `MakeupHistoryTable`    | Table  | `components/makeup/MakeupHistoryTable.tsx`    | Paginated transaction history         |
| `MakeupDebtBadge`       | Badge  | `components/makeup/MakeupDebtBadge.tsx`       | Settled/InDebt badge                  |

---

## Data Flow

### /players/[id]/makeup

| API Call                           | Hook                   | Cache Key                                 |
| ---------------------------------- | ---------------------- | ----------------------------------------- |
| `GET /players`                     | `usePlayers()`         | `queryKeys.players.list()`                |
| `GET /players/:id/makeup`          | `usePlayerMakeup(id)`  | `queryKeys.players.makeup(id)`            |
| `GET /players/:id/makeup/history`  | `useMakeupHistory(id)` | `queryKeys.players.makeup(id), "history"` |
| `GET /players/makeup/policy`       | `useMakeupPolicy(id)`  | `queryKeys.players.makeup(id), "policy"`  |
| `PATCH /players/:id/makeup`        | `useAdjustMakeup()`    | Invalidate makeup + history               |
| `PATCH /players/:id/makeup/policy` | `useSetMakeupPolicy()` | Invalidate policy                         |

---

## Form Contracts

### AdjustMakeupForm (inside dialog)

| Field      | Type   | HTML Input    | Validation                       | Error Message                 |
| ---------- | ------ | ------------- | -------------------------------- | ----------------------------- |
| operation  | string | `radio-group` | Required (increase/decrease/set) | "Select an operation"         |
| amount     | number | `number`      | Required, >= 0                   | "Amount must be 0 or greater" |
| reasonCode | string | `text`        | Required                         | "Reason is required"          |

**Zod schema:**

```typescript
z.object({
  operation: z.enum(["increase", "decrease", "set"], {
    required_error: "Select an operation",
  }),
  amount: z.coerce.number().min(0, "Amount must be 0 or greater"),
  reasonCode: z.string().min(1, "Reason is required"),
});
```

### EditPolicyForm (inside dialog — NEW)

| Field               | Type    | HTML Input | Validation        | Error Message                   |
| ------------------- | ------- | ---------- | ----------------- | ------------------------------- |
| applyProfitFirst    | boolean | `checkbox` | —                 | —                               |
| applyRakebackSecond | boolean | `checkbox` | —                 | —                               |
| playerRakebackShare | number  | `number`   | 0.0–1.0, required | "Share must be between 0 and 1" |

**Zod schema:**

```typescript
z.object({
  applyProfitFirst: z.boolean(),
  applyRakebackSecond: z.boolean(),
  playerRakebackShare: z.coerce
    .number()
    .min(0)
    .max(1, "Share must be between 0 and 1"),
});
```

---

## State-to-UI Mapping

| Makeup State | Badge Variant | Color            | Label   |
| ------------ | ------------- | ---------------- | ------- |
| Settled      | `default`     | `text-green-500` | Settled |
| InDebt       | `destructive` | —                | In Debt |

| Transaction Type  | Display              | Color             |
| ----------------- | -------------------- | ----------------- |
| MAKEUP_ADJUSTMENT | Amount with +/- sign | `text-foreground` |
| MAKEUP_APPLIED    | Negative amount      | `text-green-500`  |

---

## Accessibility Requirements

| Component          | Requirement                                              |
| ------------------ | -------------------------------------------------------- |
| AdjustMakeupDialog | Focus trap, `aria-modal="true"`, Escape to close         |
| EditPolicyDialog   | Focus trap, `aria-modal="true"`, Escape to close         |
| MakeupHistoryTable | `role="table"`, cursor pagination accessible             |
| MakeupSummaryCard  | Current debt as `aria-label` on card heading             |
| Operation radio    | `role="radiogroup"`, `aria-label="Adjustment operation"` |
