---
id: domainspec-coverage
feature: domainspec-coverage
title: Domain Layering Drift Audit
summary: Cross-feature audit of domain behavior misplaced in use-case/application layers.
status: in-progress
pillar: platform
domain: documentation-governance
audience:
  - leadership
  - developers
priority: p1
lang: en
owners:
  - architecture-core
  - backend-core
updatedAt: 2026-04-09
dependencies:
  - spec.en.md
includes: []
---

## Audit Scope

- player-management
- player-makeup
- player-stats
- player-progression
- financial-settlement
- player-onboarding

## Classification Rules

Misplaced in use-case/application layer when code contains:

- domain policy math or threshold formulas
- invariant and state-transition guards that should be reusable domain behavior
- value normalization/parsing of domain primitives
- domain event decision logic

Allowed in use-case/application layer:

- orchestration of repositories/services
- transaction and idempotency coordination
- transport DTO mapping

## Findings By Feature

| Feature              | DomainSpec Concepts                                                                                                                 | Drift Level | Evidence                                                                                                                            | Required Move Target                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| player-makeup        | player-makeup.AdjustPlayerMakeup, player-makeup.MakeupBalance, player-makeup.MakeupOperationType                                    | high        | backend/src/use-cases/makeup/adjust-player-makeup.ts keeps operation validation, amount normalization, and debt floor logic         | Move to backend/src/domain/makeup/makeup-adjustment.service.ts and expose a deterministic applyAdjustment API         |
| player-makeup        | player-makeup.GetPlayerMakeupHistory                                                                                                | medium      | backend/src/use-cases/makeup/get-player-makeup-history.ts owns cursor encoding/decoding and timeline ordering policy                | Move ordering and cursor policy to backend/src/domain/makeup/makeup-history.service.ts                                |
| financial-settlement | financial-settlement.GenerateSettlement, financial-settlement.SettlementWorkflow, player-makeup.SettlementMakeupApplicationContract | high        | backend/src/use-cases/financial-settlement/generate-settlement.ts owns period filtering and MAKEUP_APPLIED/PAYOUT emission decisions | Move settlement period aggregation and side-effect policy to backend/src/domain/settlement/settlement.service.ts      |
| player-progression   | player-progression.CheckProgression, player-progression.ProgressionStatus                                                           | critical    | backend/src/use-cases/progression/check-progression.ts owns thresholds (1000 hands/day, 7.5 and 5 winrate) and eligibility reasons  | Move criteria evaluation to backend/src/domain/progression/progression-policy.service.ts                              |
| player-management    | player-management.GetPlayersOverview, player-management.PlayerToOverviewDto                                                         | high        | backend/src/use-cases/player/get-players-overview.ts calculates lifetime/period metrics and winrate formula                         | Move overview projection math to backend/src/domain/player/player-overview.service.ts                                 |
| player-management    | player-management.CreatePlayer, player-management.Player                                                                            | medium      | backend/src/use-cases/player/create-player.ts keeps identity field validation and limit constraints                                 | Move invariant constructors/guards to backend/src/domain/player/player-policy.service.ts                              |
| player-onboarding    | player-onboarding.SubmitCandidateApplication, player-onboarding.RuleAcceptance                                                      | critical    | backend/src/use-cases/onboarding/submit-candidate-application.ts owns age, city/state, email and tracker detail business validation | Move onboarding invariants and normalization to backend/src/domain/onboarding/candidate-application-policy.service.ts |
| player-onboarding    | player-onboarding.ReviewCandidateApplication, player-onboarding.CandidateApplicationState                                           | high        | backend/src/use-cases/onboarding/review-candidate-application.ts owns transition guards and retention policy                        | Move transition and retention policy to backend/src/domain/onboarding/candidate-review-policy.service.ts              |
| player-stats          | player-stats.RecordPlayerStats (was RecordDailyStats), player-stats.PlayerStatsSnapshot (was BankrollResetCalculation)                 | low         | backend/src/use-cases/player-stats/record-player-stats.ts computes gross bankroll in use-case                                         | Keep orchestration in use-case, but move pre/post conditions to domain bankroll contract                              |

## Cross-Feature Root Causes

1. Domain entities are mostly type declarations, with little executable behavior.
2. Use-cases were used as both orchestration and policy layers.
3. Missing mandatory layering gate in existing planning and implementation skills.
4. Missing explicit "domain service target" task in feature execution plans.

## Risk If Unaddressed

1. Policy drift across endpoints and future regressions.
2. Low reuse of core rules between APIs and workflows.
3. Harder deterministic test generation from DomainSpec because logic location is unstable.
4. Increased coupling of transport concerns to business behavior.
