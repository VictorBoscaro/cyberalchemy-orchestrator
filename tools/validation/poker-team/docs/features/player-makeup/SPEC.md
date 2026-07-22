---
id: player-makeup
feature: player-makeup
title: Player Makeup DomainSpec
summary: Domain specification for makeup debt reads, adjustments, and settlement policy integration.
status: implemented
pillar: finance
domain: player-makeup
audience:
  - developers
  - finance
priority: p1
lang: en
owners:
  - finance-core
  - backend-core
  - web-core
updatedAt: 2026-04-17
dependencies:
  - player-management
  - financial-settlement
includes:
  - domain.md
  - operations.md
  - states.md
  - interfaces.md
  - events.md
  - queries.md
  - mappings.md
  - workflows.md
  - STORIES.md
---

# Player Makeup

## Overview

Player Makeup tracks debt carried by each player and controls how debt is adjusted manually and consumed during settlement. It exposes operational read models for current debt and audit history. In MVP, policy resolution is player-aware with deterministic fallback to default policy values.

## Scope

- Manual makeup adjustments via API.
- Makeup history timeline for operational audit.
- Deterministic settlement makeup application contract.
- REST contracts consumed by backend and web adapters.

## Out Of Scope

- Multi-currency makeup accounting.

## Pilot Gate Decisions

| Decision                                  | Value                                                                                                                            | Status   |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Wave 1 scope                              | Read makeup snapshot/history, manual makeup adjustments, policy endpoint usage. Settlement execution is out of scope for Wave 1. | resolved |
| Player-role visibility                    | Player is self-only; manager and admin can read/write any player by permission                                                   | resolved |
| Rakeback policy during pilot              | Configurable per player                                                                                                          | resolved |
| Rounding authority                        | Half-up non-negative (`floor(x + 0.5)`)                                                                                          | resolved |
| Approval for `decrease` and `set`         | Managers only, single approval                                                                                                   | resolved |
| Settlement auth gate                      | Mandatory blocker before GO                                                                                                      | resolved |
| Settlement storage dedupe gate            | Mandatory blocker before GO for `(type, playerId, date)` on MAKEUP_APPLIED/PAYOUT                                                | resolved |
| Required manual-adjustment audit metadata | actorId, requestId, reasonCode, sourceChannel                                                                                    | resolved |
| Mutation failure policy                   | Atomic transaction required (all-or-nothing)                                                                                     | resolved |
| GO/NO-GO decision model                   | Automatic GO when all Wave 1 P0 blockers are closed and all Wave 1 P0 tests pass in one archived gate run                        | resolved |

## Concepts

| Concept                                                                                 | ID                                                | Type          | Description                                                               |
| --------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------- | ------------------------------------------------------------------------- |
| [MakeupBalance](domain.md#makeupbalance)                                                | player-makeup.MakeupBalance                       | Value Object  | Non-negative debt amount for a player                                     |
| [MakeupPolicy](domain.md#makeuppolicy)                                                  | player-makeup.MakeupPolicy                        | Value Object  | Effective policy used by settlement (player override or default fallback) |
| [MakeupOperationType](domain.md#makeupoperationtype)                                    | player-makeup.MakeupOperationType                 | Enum          | Allowed manual adjustment operation values                                |
| [AdjustPlayerMakeup](operations.md#adjustplayermakeup)                                  | player-makeup.AdjustPlayerMakeup                  | Operation     | Increase, decrease, or set debt                                           |
| [GetPlayerMakeup](queries.md#getplayermakeup)                                           | player-makeup.GetPlayerMakeup                     | Query         | Current debt and policy                                                   |
| [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory)                             | player-makeup.GetPlayerMakeupHistory              | Query         | Timeline of makeup-related transactions                                   |
| [GetMakeupPolicy](queries.md#getmakeuppolicy)                                           | player-makeup.GetMakeupPolicy                     | Query         | Effective policy for player or default fallback                           |
| [MakeupDebtState](states.md#makeupdebtstate)                                            | player-makeup.MakeupDebtState                     | State Machine | Debt lifecycle (zero vs debt)                                             |
| [MakeupAPI](interfaces.md#external-makeupapi-rest)                                      | player-makeup.MakeupAPI                           | Interface     | REST boundary for makeup operations                                       |
| [PlayerDirectoryAPI](interfaces.md#external-playerdirectoryapi-rest)                    | player-makeup.PlayerDirectoryAPI                  | Interface     | Player list endpoint consumed by selector                                 |
| [MakeupAdjusted](events.md#makeupadjusted)                                              | player-makeup.MakeupAdjusted                      | Event         | Emitted on manual adjustment                                              |
| [MakeupApplied](events.md#makeupapplied)                                                | player-makeup.MakeupApplied                       | Event         | Emitted when settlement consumes debt                                     |
| [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow)                       | player-makeup.MakeupAdjustmentWorkflow            | Workflow      | Adjustment validation and persistence path                                |
| [SettlementMakeupApplicationContract](workflows.md#settlementmakeupapplicationcontract) | player-makeup.SettlementMakeupApplicationContract | Workflow      | Contract for settlement makeup consumption                                |

## Feature Concept Graph

| From                                            | Edge         | To                                              | Evidence                                        | Notes                                       |
| ----------------------------------------------- | ------------ | ----------------------------------------------- | ----------------------------------------------- | ------------------------------------------- |
| player-makeup.MakeupAPI                         | exposes      | player-makeup.AdjustPlayerMakeup               | interfaces.md#external-makeupapi-rest          | API exposes adjustment mutation             |
| player-makeup.MakeupAPI                         | exposes      | player-makeup.GetPlayerMakeup                  | interfaces.md#external-makeupapi-rest          | API exposes current makeup query            |
| player-makeup.MakeupAdjustmentWorkflow          | orchestrates | player-makeup.AdjustPlayerMakeup               | workflows.md#makeupadjustmentworkflow          | Workflow coordinates adjustment path        |
| player-makeup.AdjustPlayerMakeup                | produces     | player-makeup.MakeupAdjusted                   | operations.md#adjustplayermakeup               | Operation emits adjustment event            |
| player-makeup.MakeupApplied                     | transitions  | player-makeup.MakeupDebtState                  | states.md#makeupdebtstate                      | Settlement application event updates state  |
| player-makeup.GetPlayerMakeup                   | queries      | player-makeup.MakeupBalance                    | queries.md#getplayermakeup                     | Query reads authoritative makeup balance    |

## Aspects

- [Domain](domain.md)
- [Operations](operations.md)
- [States](states.md)
- [Interfaces](interfaces.md)
- [Events](events.md)
- [Queries](queries.md)
- [Mappings](mappings.md)
- [Workflows](workflows.md)

## Cross-Feature Dependencies

| Depends On           | Relationship | Why                                                   |
| -------------------- | ------------ | ----------------------------------------------------- |
| player-management    | queries      | Resolve player and persist makeup on player aggregate |
| financial-settlement | produces-for | Provides debt policy and debt state consumed in settlement flows |

## Produces For

| Consumer                  | Via           | What                             |
| ------------------------- | ------------- | -------------------------------- |
| financial-settlement      | Query + state | Current debt and policy baseline |
| frontend makeup dashboard | Interface     | Current state and timeline       |

## Stories

See [STORIES.md](STORIES.md) for capability-scoped user stories with classic + BDD format, acceptance checks, and Story Coverage Matrix.

## User Stories

See [STORIES.md](STORIES.md) for classic and BDD story definitions.

## Story Coverage Matrix

See [Story Coverage Matrix](STORIES.md#story-coverage-matrix) for concept and capability coverage.

## Pilot Decisions

Pilot policy and verification decisions are recorded in [PILOT-DECISIONS.md](PILOT-DECISIONS.md).

## Acceptance Baseline

- Makeup can be increased, decreased, and set explicitly.
- Adjustment and settlement applications are auditable in timeline queries.
- Settlement applies makeup policy deterministically and idempotently per player and period.
- API contracts, auth rules, and error schema are authoritative in [interfaces.md](interfaces.md).
