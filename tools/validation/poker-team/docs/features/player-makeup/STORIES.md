---
id: player-makeup-stories
feature: player-makeup
title: Player Makeup User Stories
summary: Capability-scoped user stories for makeup debt tracking, adjustment, and settlement integration.
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
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
includes: []
---

# Player Makeup — User Stories

> Source of storytelling truth for [player-makeup](SPEC.md).

## US-01 Public Journey: View Player Makeup Snapshot And Timeline

**Classic format**
As an authorized operations user, I want to view a player's current makeup and history, so that I can understand debt status and recent makeup activity before taking action.

**BDD scenario**
Given a player exists and I have read permission
When I request the player makeup snapshot and makeup history
Then I receive the current makeup, effective policy, and history entries sorted newest-first

**Acceptance checks**

- [ ] Reading current makeup follows [GetPlayerMakeup](queries.md#getplayermakeup) and returns `playerId`, `currentMakeup`, and policy from [MakeupPolicy](domain.md#makeuppolicy).
- [ ] Reading timeline follows [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory) and returns only makeup-related transactions in newest-first order.
- [ ] Access control and status behavior follow [External: MakeupAPI (REST)](interfaces.md#external-makeupapi-rest), including read permission requirements and documented response codes.
- [ ] Policy retrieval behavior follows [GetMakeupPolicy](queries.md#getmakeuppolicy) and returns effective player policy with deterministic default fallback.

**Capability link**: [SPEC — Concepts](SPEC.md#concepts)

**Concept and aspect links**

- player-makeup.GetPlayerMakeup: [GetPlayerMakeup](queries.md#getplayermakeup)
- player-makeup.GetPlayerMakeupHistory: [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory)
- player-makeup.GetMakeupPolicy: [GetMakeupPolicy](queries.md#getmakeuppolicy)
- player-makeup.MakeupPolicy: [MakeupPolicy](domain.md#makeuppolicy)
- player-makeup.MakeupAPI: [External: MakeupAPI (REST)](interfaces.md#external-makeupapi-rest)
- player-makeup.PlayerDirectoryAPI: [External: PlayerDirectoryAPI (REST)](interfaces.md#external-playerdirectoryapi-rest)

---

## US-02 Admin Operations Journey: Adjust Player Makeup Debt

**Classic format**
As an authorized operations user, I want to increase, decrease, or set player makeup debt, so that debt records reflect operational decisions with auditability.

**BDD scenario**
Given I have write permission and submit a valid adjustment request for an existing player
When the adjustment is processed
Then the resulting makeup is persisted as non-negative and an audit transaction is created only when the value changes

**Acceptance checks**

- [ ] Mutation behavior follows [AdjustPlayerMakeup](operations.md#adjustplayermakeup), including valid operations, finite non-negative amount, and player existence checks.
- [ ] Amount normalization and resulting debt calculations follow the formulas documented in [AdjustPlayerMakeup](operations.md#adjustplayermakeup).
- [ ] State transitions follow [MakeupDebtState](states.md#makeupdebtstate) with no negative debt.
- [ ] Workflow orchestration follows [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow), including authorization, validation, execution, and audit persistence.
- [ ] API request/response and auth behavior follow [PATCH /players/:id/makeup](interfaces.md#patch-playersidmakeup) and mapping in [AdjustMakeupRequestToInput](mappings.md#adjustmakeuprequesttoinput).
- [ ] Audit/event semantics follow [MakeupAdjusted](events.md#makeupadjusted), including no adjustment transaction when delta is zero.

**Capability link**: [SPEC — Concepts](SPEC.md#concepts)

**Concept and aspect links**

- player-makeup.AdjustPlayerMakeup: [AdjustPlayerMakeup](operations.md#adjustplayermakeup)
- player-makeup.MakeupOperationType: [MakeupOperationType](domain.md#makeupoperationtype)
- player-makeup.MakeupDebtState: [MakeupDebtState](states.md#makeupdebtstate)
- player-makeup.MakeupAdjustmentWorkflow: [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow)
- player-makeup.MakeupAdjusted: [MakeupAdjusted](events.md#makeupadjusted)

---

## US-03 Cross-Feature Integration: Apply Makeup During Settlement

**Classic format**
As the settlement flow in financial-settlement, I want makeup to be applied deterministically and idempotently per player and period, so that payouts and debt reduction remain consistent across repeated executions.

**BDD scenario**
Given a player has makeup debt and settlement is generated for a period
When settlement applies makeup according to policy
Then makeup is consumed in documented order and duplicate settlement-period makeup application events are not created

**Acceptance checks**

- [ ] Integration contract follows [SettlementMakeupApplicationContract](workflows.md#settlementmakeupapplicationcontract).
- [ ] Policy application order follows S1-S4 in [SettlementMakeupApplicationContract](workflows.md#settlementmakeupapplicationcontract), using [MakeupPolicy](domain.md#makeuppolicy) resolved per player with deterministic default fallback.
- [ ] Settlement-driven state effects follow [MakeupDebtState](states.md#makeupdebtstate), including debt clearing when applied amount covers debt.
- [ ] Event idempotency and deduplication constraints follow [MakeupApplied](events.md#makeupapplied), including uniqueness per player and period.
- [ ] History inclusion of settlement consumption follows [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory).

**Capability link**: [SPEC — Concepts](SPEC.md#concepts)

**Concept and aspect links**

- player-makeup.SettlementMakeupApplicationContract: [SettlementMakeupApplicationContract](workflows.md#settlementmakeupapplicationcontract)
- player-makeup.MakeupApplied: [MakeupApplied](events.md#makeupapplied)
- player-makeup.MakeupDebtState: [MakeupDebtState](states.md#makeupdebtstate)
- player-makeup.MakeupPolicy: [MakeupPolicy](domain.md#makeuppolicy)
- player-makeup.GetPlayerMakeupHistory: [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory)

---

## US-04 Error And Edge Case Journey: Reject Invalid And Non-Actionable Paths

**Classic format**
As an authorized operations user or integrated caller, I want invalid, unauthorized, and non-actionable requests handled deterministically, so that the system remains safe, auditable, and free of inconsistent makeup effects.

**BDD scenario**
Given a request is unauthorized, invalid, or would violate documented transition or idempotency constraints
When the request is processed
Then the API returns structured errors or rejects the transition, and no invalid duplicate or no-op audit artifacts are created

**Acceptance checks**

- [ ] Error response contract follows [Error Contract](interfaces.md#error-contract) with structured error fields.
- [ ] Authorization failures for protected routes follow [Auth Contract](interfaces.md#auth-contract) and route permission matrix.
- [ ] Validation failures follow [AdjustPlayerMakeup](operations.md#adjustplayermakeup), including invalid amount/operation and player-not-found outcomes.
- [ ] History query pagination edge validation follows [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory), including out-of-range limit returning validation error.
- [ ] Invalid transition behavior follows [MakeupDebtState](states.md#makeupdebtstate), including documented rejected transitions.
- [ ] No-op and duplicate protections follow [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow) invariant and [MakeupApplied](events.md#makeupapplied) idempotency rules.

**Capability link**: [SPEC — Concepts](SPEC.md#concepts)

**Concept and aspect links**

- player-makeup.MakeupAPI: [External: MakeupAPI (REST)](interfaces.md#external-makeupapi-rest)
- player-makeup.AdjustPlayerMakeup: [AdjustPlayerMakeup](operations.md#adjustplayermakeup)
- player-makeup.GetPlayerMakeupHistory: [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory)
- player-makeup.MakeupDebtState: [MakeupDebtState](states.md#makeupdebtstate)
- player-makeup.MakeupAdjustmentWorkflow: [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow)
- player-makeup.MakeupApplied: [MakeupApplied](events.md#makeupapplied)

---

## Story Coverage Matrix

| Story | Mandatory Slice           | Concepts Covered                                                                                                                                                                                    | Aspect Anchors                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----- | ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| US-01 | Public journey            | player-makeup.GetPlayerMakeup, player-makeup.GetPlayerMakeupHistory, player-makeup.GetMakeupPolicy, player-makeup.MakeupPolicy, player-makeup.MakeupAPI, player-makeup.PlayerDirectoryAPI           | [GetPlayerMakeup](queries.md#getplayermakeup), [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory), [GetMakeupPolicy](queries.md#getmakeuppolicy), [MakeupPolicy](domain.md#makeuppolicy), [MakeupAPI](interfaces.md#external-makeupapi-rest), [PlayerDirectoryAPI](interfaces.md#external-playerdirectoryapi-rest)                                                                                                      |
| US-02 | Admin operations journey  | player-makeup.AdjustPlayerMakeup, player-makeup.MakeupOperationType, player-makeup.MakeupDebtState, player-makeup.MakeupAdjustmentWorkflow, player-makeup.MakeupAdjusted                            | [AdjustPlayerMakeup](operations.md#adjustplayermakeup), [MakeupOperationType](domain.md#makeupoperationtype), [MakeupDebtState](states.md#makeupdebtstate), [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow), [MakeupAdjusted](events.md#makeupadjusted), [AdjustMakeupRequestToInput](mappings.md#adjustmakeuprequesttoinput)                                                                                  |
| US-03 | Cross-feature integration | player-makeup.SettlementMakeupApplicationContract, player-makeup.MakeupApplied, player-makeup.MakeupDebtState, player-makeup.MakeupPolicy, player-makeup.GetPlayerMakeupHistory                     | [SettlementMakeupApplicationContract](workflows.md#settlementmakeupapplicationcontract), [MakeupApplied](events.md#makeupapplied), [MakeupDebtState](states.md#makeupdebtstate), [MakeupPolicy](domain.md#makeuppolicy), [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory)                                                                                                                                             |
| US-04 | Error and edge case       | player-makeup.MakeupAPI, player-makeup.AdjustPlayerMakeup, player-makeup.GetPlayerMakeupHistory, player-makeup.MakeupDebtState, player-makeup.MakeupAdjustmentWorkflow, player-makeup.MakeupApplied | [MakeupAPI](interfaces.md#external-makeupapi-rest), [Error Contract](interfaces.md#error-contract), [Auth Contract](interfaces.md#auth-contract), [AdjustPlayerMakeup](operations.md#adjustplayermakeup), [GetPlayerMakeupHistory](queries.md#getplayermakeuphistory), [MakeupDebtState](states.md#makeupdebtstate), [MakeupAdjustmentWorkflow](workflows.md#makeupadjustmentworkflow), [MakeupApplied](events.md#makeupapplied) |

**Coverage gap check**: No uncovered concepts from the Player Makeup concept table were identified for the four mandatory story slices.
