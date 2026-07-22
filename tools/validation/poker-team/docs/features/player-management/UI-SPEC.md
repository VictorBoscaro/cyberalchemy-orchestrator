---
id: player-management-ui
feature: player-management
title: Player Management UI Specification
summary: Frontend design contract for player CRUD, coach management, and assignment operations.
status: draft
pillar: platform
domain: player-management-ui
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

# UI Specification: Player Management

> Governs the frontend presentation of player CRUD, coach lifecycle, and coach-player assignments.
> Constrained by [UI-ARCHITECTURE.md](../../UI-ARCHITECTURE.md).

---

## Route Table

| Route                        | Page Title       | Layout          | Auth Required | Permission                                  |
| ---------------------------- | ---------------- | --------------- | ------------- | ------------------------------------------- |
| `/players`                   | All Players      | DashboardLayout | Yes           | `player-management.read.getAllPlayers`      |
| `/players/new`               | Create Player    | DashboardLayout | Yes           | `player-management.write.createPlayer`      |
| `/players/overview`          | Players Overview | DashboardLayout | Yes           | `player-management.read.getPlayersOverview` |
| `/coaches`                   | All Coaches      | DashboardLayout | Yes           | `player-management.read.getAllCoaches`      |
| `/coaches/new`               | Create Coach     | DashboardLayout | Yes           | `player-management.write.createCoach`       |
| `/coaches/[coachId]/players` | Coach Players    | DashboardLayout | Yes           | `player-management.read.getCoachPlayers`    |

---

## Page Layouts

### /players (All Players)

```
┌─────────────────────────────────────────────┐
│ Header: "All Players"   [+ Create Player]   │
├─────────────────────────────────────────────┤
│ PlayersTable                                │
│ ┌─────┬──────┬───────┬────────┬──────────┐  │
│ │Name │Email │Limit  │Status  │Actions   │  │
│ ├─────┼──────┼───────┼────────┼──────────┤  │
│ │...  │...   │NL20   │●Active │View │Del │  │
│ └─────┴──────┴───────┴────────┴──────────┘  │
└─────────────────────────────────────────────┘
```

### /players/new (Create Player)

```
┌─────────────────────────────────────────────┐
│ Header: "Create Player"                     │
├─────────────────────────────────────────────┤
│ CreatePlayerForm                            │
│   name          [________________]          │
│   email         [________________]          │
│   currentLimit  [NL20 ▼]                    │
│   bankroll      [________________]          │
│                 [Create Player]              │
└─────────────────────────────────────────────┘
```

### /players/overview (Players Overview)

```
┌─────────────────────────────────────────────┐
│ Header: "Players Overview"                  │
│ Period: [30 days ▼]                         │
├─────────────────────────────────────────────┤
│ PlayersOverviewTable                        │
│ ┌────┬──────┬──────┬────────┬───────┬─────┐ │
│ │Name│Limit │Profit│AvgHands│Winrate│Mkup │ │
│ ├────┼──────┼──────┼────────┼───────┼─────┤ │
│ │... │NL40  │$1200 │1500    │8.2    │$0   │ │
│ └────┴──────┴──────┴────────┴───────┴─────┘ │
└─────────────────────────────────────────────┘
```

### /coaches (All Coaches)

```
┌─────────────────────────────────────────────┐
│ Header: "Coaches"          [+ Create Coach] │
├─────────────────────────────────────────────┤
│ CoachesTable                                │
│ ┌─────┬──────────┬────────┬──────────────┐  │
│ │Name │Email     │Status  │Actions       │  │
│ ├─────┼──────────┼────────┼──────────────┤  │
│ │...  │...       │●Active │Players │Edit │  │
│ └─────┴──────────┴────────┴──────────────┘  │
└─────────────────────────────────────────────┘
```

### /coaches/[coachId]/players (Coach Players)

```
┌─────────────────────────────────────────────┐
│ Header: "Coach: {name} — Players"           │
│ [+ Assign Player]                           │
├─────────────────────────────────────────────┤
│ CoachPlayersTable                           │
│ ┌─────┬──────┬───────┬────────┬──────────┐  │
│ │Name │Email │Limit  │Status  │Unassign  │  │
│ └─────┴──────┴───────┴────────┴──────────┘  │
│                                             │
│ AssignPlayerDialog (modal)                  │
│   Select player: [Player Name ▼]            │
│   [Assign]  [Cancel]                        │
└─────────────────────────────────────────────┘
```

---

## Component Inventory

| Component              | Type   | Location                                      | Purpose                           |
| ---------------------- | ------ | --------------------------------------------- | --------------------------------- |
| `PlayersTable`         | Table  | `components/players/PlayersTable.tsx`         | List all players with sort/filter |
| `PlayersOverviewTable` | Table  | `components/players/PlayersOverviewTable.tsx` | Enriched player list with stats   |
| `CreatePlayerForm`     | Form   | `components/players/CreatePlayerForm.tsx`     | Player creation form              |
| `PlayerStatusBadge`    | Badge  | `components/players/PlayerStatusBadge.tsx`    | OBSERVATION/ACTIVE/INACTIVE badge |
| `CoachesTable`         | Table  | `components/coaches/CoachesTable.tsx`         | List all coaches                  |
| `CreateCoachForm`      | Form   | `components/coaches/CreateCoachForm.tsx`      | Coach creation form               |
| `CoachPlayersTable`    | Table  | `components/coaches/CoachPlayersTable.tsx`    | Players assigned to a coach       |
| `AssignPlayerDialog`   | Dialog | `components/coaches/AssignPlayerDialog.tsx`   | Modal to assign player to coach   |
| `LimitBadge`           | Badge  | `components/players/LimitBadge.tsx`           | NL20/NL40/etc display             |

---

## Data Flow

### /players

| API Call       | Hook           | Cache Key                  | Triggers   |
| -------------- | -------------- | -------------------------- | ---------- |
| `GET /players` | `usePlayers()` | `queryKeys.players.list()` | Page mount |

### /players/new

| API Call        | Hook                | On Success                                        |
| --------------- | ------------------- | ------------------------------------------------- |
| `POST /players` | `useCreatePlayer()` | Invalidate `players.list`, navigate to `/players` |

### /players/overview

| API Call                              | Hook                       | Cache Key                           |
| ------------------------------------- | -------------------------- | ----------------------------------- |
| `GET /players/overview?periodDays=30` | `usePlayersOverview(days)` | `queryKeys.players.all, "overview"` |

### /coaches

| API Call       | Hook           | Cache Key               |
| -------------- | -------------- | ----------------------- |
| `GET /coaches` | `useCoaches()` | `queryKeys.coaches.all` |

### /coaches/new

| API Call        | Hook               | On Success                                       |
| --------------- | ------------------ | ------------------------------------------------ |
| `POST /coaches` | `useCreateCoach()` | Invalidate `coaches.all`, navigate to `/coaches` |

### /coaches/[coachId]/players

| API Call                                     | Hook                       | On Success                         |
| -------------------------------------------- | -------------------------- | ---------------------------------- |
| `GET /coaches/:coachId/players`              | `useCoachPlayers(coachId)` | —                                  |
| `POST /coaches/:coachId/players/:playerId`   | `useAssignCoach()`         | Invalidate `coaches.assignments()` |
| `DELETE /coaches/:coachId/players/:playerId` | `useUnassignCoach()`       | Invalidate `coaches.assignments()` |

---

## Form Contracts

### CreatePlayerForm

| Field           | Type   | HTML Input | Validation                                 | Error Message                   |
| --------------- | ------ | ---------- | ------------------------------------------ | ------------------------------- |
| name            | string | `text`     | Required, min 1                            | "Name is required"              |
| email           | string | `email`    | Required, valid email                      | "Valid email is required"       |
| currentLimit    | string | `select`   | Required, one of NL20/NL40/NL60/NL80/NL100 | "Select a limit"                |
| initialBankroll | number | `number`   | Optional, >= 0                             | "Bankroll must be 0 or greater" |

**Zod schema:**

```typescript
z.object({
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Valid email is required"),
  currentLimit: z.enum(["NL20", "NL40", "NL60", "NL80", "NL100"], {
    required_error: "Select a limit",
  }),
  initialBankroll: z.coerce
    .number()
    .min(0, "Bankroll must be 0 or greater")
    .optional(),
});
```

**Error Code → UI Message Mapping:**

| API Error Code    | HTTP Status | UI Message                         |
| ----------------- | ----------- | ---------------------------------- |
| `DUPLICATE_EMAIL` | 409         | "A player with this email exists." |
| (validation)      | 400         | Show field-level errors            |

### CreateCoachForm

| Field       | Type   | HTML Input | Validation      | Error Message              |
| ----------- | ------ | ---------- | --------------- | -------------------------- |
| principalId | string | `text`     | Required        | "Principal ID is required" |
| name        | string | `text`     | Required        | "Name is required"         |
| email       | string | `email`    | Required, valid | "Valid email is required"  |

**Zod schema:**

```typescript
z.object({
  principalId: z.string().min(1, "Principal ID is required"),
  name: z.string().min(1, "Name is required"),
  email: z.string().email("Valid email is required"),
});
```

### AssignPlayerDialog

| Field    | Type   | HTML Input | Validation | Error Message     |
| -------- | ------ | ---------- | ---------- | ----------------- |
| playerId | string | `select`   | Required   | "Select a player" |

**Error Code → UI Message Mapping:**

| API Error Code            | HTTP Status | UI Message                            |
| ------------------------- | ----------- | ------------------------------------- |
| `PLAYER_ALREADY_ASSIGNED` | 409         | "This player already has a coach."    |
| `COACH_INACTIVE`          | 409         | "Cannot assign to an inactive coach." |

---

## State-to-UI Mapping

| Entity State       | Badge Variant | Color                   | Label       |
| ------------------ | ------------- | ----------------------- | ----------- |
| Player.OBSERVATION | `outline`     | `text-yellow-500`       | Observation |
| Player.ACTIVE      | `default`     | `text-green-500`        | Active      |
| Player.INACTIVE    | `secondary`   | `text-muted-foreground` | Inactive    |
| Coach.ACTIVE       | `default`     | `text-green-500`        | Active      |
| Coach.INACTIVE     | `secondary`   | `text-muted-foreground` | Inactive    |

---

## Accessibility Requirements

| Component          | Requirement                                                  |
| ------------------ | ------------------------------------------------------------ |
| PlayersTable       | `role="table"`, sortable column headers with `aria-sort`     |
| CreatePlayerForm   | `role="form"`, `aria-label`, focus on first input            |
| AssignPlayerDialog | Focus trap, `aria-modal="true"`, Escape to close             |
| PlayerStatusBadge  | `aria-label` includes status text                            |
| LimitBadge         | `aria-label` with full limit description                     |
| Action buttons     | `aria-label` describing action (e.g., "View player details") |
