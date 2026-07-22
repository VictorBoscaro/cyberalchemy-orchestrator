---
id: domainspec-coverage
feature: domainspec-coverage
title: Layering Alignment Plan
summary: Dependency-ordered plan to move domain behavior from use-cases into domain layers and enforce this pattern in DomainSpec workflows.
status: in-progress
pillar: platform
domain: documentation-governance
audience:
  - developers
  - leadership
priority: p1
lang: en
owners:
  - architecture-core
  - backend-core
updatedAt: 2026-04-09
dependencies:
  - spec.en.md
  - layering-audit.en.md
includes: []
---

## Mode Selection

Mode: gsd-phase

Rationale:
- Cross-cutting changes across docs, backend domain layer, use-cases, and test suites.
- Multiple feature dependencies and migration sequencing constraints.
- Need checkpointed waves with rollback-safe behavior.

## Enforcement Plan In DomainSpec Repository

1. Add layering-specific auditor and command skill.
- Added agent: domainspec-layering-auditor.
- Added skill: domainspec-audit-layering.

2. Add mandatory layering gate before plan and implementation flows when feature code already exists.
- Updated skills: domainspec-plan-phase-bridge and domainspec-implement.
- Gate rule: run domainspec-audit-layering before planning or code edits.

3. Keep enforcement in distributable pack and local integration layer.
- Updated both domainspec/.github and domainspec/copilot packs.

4. Add framework changelog entry for traceability.
- Updated domainspec/CHANGELOG.md.

## Alignment Waves In Root Repository

## Execution Progress

Completed on 2026-04-09:
- Wave 1 implemented in backend domain and use-case layers.
- Wave 2 implemented in backend domain and use-case layers.
- Wave 3 player-stats domain contract cleanup implemented.

Still pending:
- None.

### Wave 1: Highest-Risk Policy Extraction

1. player-progression
- Concepts: player-progression.CheckProgression, player-progression.ProgressionStatus.
- Tasks:
  - Create backend/src/domain/progression/progression-policy.service.ts.
  - Move threshold and eligibility reason logic from use-case.
  - Keep use-case as orchestrator only.

2. player-onboarding
- Concepts: player-onboarding.SubmitCandidateApplication, player-onboarding.CandidateApplicationState.
- Tasks:
  - Create backend/src/domain/onboarding/candidate-application-policy.service.ts.
  - Create backend/src/domain/onboarding/candidate-review-policy.service.ts.
  - Move validation, transition, and retention rules into domain services/value objects.

3. player-makeup
- Concepts: player-makeup.AdjustPlayerMakeup, player-makeup.MakeupBalance.
- Tasks:
  - Create backend/src/domain/makeup/makeup-adjustment.service.ts.
  - Move operation validation and makeup floor logic from use-case.

### Wave 2: Projection and Settlement Consolidation

1. player-management
- Concepts: player-management.GetPlayersOverview, player-management.PlayerToOverviewDto.
- Tasks:
  - Create backend/src/domain/player/player-overview.service.ts.
  - Move winrate and period aggregation formulas from use-case.

2. financial-settlement
- Concepts: financial-settlement.GenerateSettlement, financial-settlement.SettlementWorkflow, player-makeup.SettlementMakeupApplicationContract.
- Tasks:
  - Create backend/src/domain/settlement/settlement.service.ts.
  - Move period filtering and side-effect decision policy from use-case.
  - Keep repository calls and idempotency orchestration in use-case.

3. player-makeup history
- Concepts: player-makeup.GetPlayerMakeupHistory.
- Tasks:
  - Create backend/src/domain/makeup/makeup-history.service.ts.
  - Move sorting and cursor policy to domain-level helper/service.

### Wave 3: Cleanup, Naming, and Documentation Tightening

1. player-stats
- Concepts: player-stats.RecordPlayerStats (was RecordDailyStats), player-stats.PlayerStatsSnapshot (was BankrollResetCalculation).
- Tasks:
  - Keep existing bankroll domain service as authority.
  - Add explicit domain contract tests for pre/post conditions.

2. docs alignment
- Tasks:
  - Update each feature docs with explicit "domain service owns policy" statements.
  - Add links from operations/workflows to created domain services.

3. generated indexes
- Tasks:
  - Run npm run docs:index after docs updates.

## Verification Commands Per Wave

1. npm run test:backend
2. npm run test --workspace backend -- backend/src/use-cases
3. npm run typecheck --workspace backend
4. npm run docs:index

## Done Criteria

1. No use-case file contains feature policy thresholds, domain invariant logic, or domain state transitions.
2. Domain services exist for each migrated policy and are unit-tested.
3. Each migrated feature has updated docs and concept-to-code traceability.
4. DomainSpec planner/implement skills enforce layering audit before edits on existing codebases.

## Assumptions

1. Current repository keeps use-cases as application orchestrators.
2. Domain repositories remain infrastructure-facing abstractions.
3. Behavior remains semantically unchanged during extraction unless feature docs are explicitly updated.
