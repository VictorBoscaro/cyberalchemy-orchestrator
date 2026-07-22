---
id: domainspec-coverage
feature: domainspec-coverage
title: DomainSpec Gaps and Undefined Decisions
summary: Gaps discovered while reverse-specifying implemented code into DomainSpec.
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
updatedAt: 2026-04-04
dependencies:
  - spec.en.md
includes: []
---

## Critical Gaps

1. Missing input schema validation in multiple routes

- Player and player-stats endpoints still rely on `as any` payload casting.
- Domain rules are now specified, but runtime enforcement is incomplete.

2. Weak idempotency boundary for settlement

- Deduplication checks only on `(type, date)` and not on `(playerId, periodStart, periodEnd, type)`.
- Reprocessing risk remains if date is reused in different settlement contexts.

3. No transactional boundary for multi-write operations

- Settlement and player-stats perform multiple repository writes without explicit transaction guarantees.
- Partial write failure can produce inconsistent state.

## High Gaps

1. Ambiguous monetary unit contract

- Code treats values as integer monetary units, but no explicit currency/unit value object exists in shared docs.
- Need standardized money semantics (for example cents) and rounding policy.

2. Limit parsing and buy-in semantics are underspecified

- `getLimitBuyIn` contains conflicting comments and an unreachable return statement.
- DomainSpec now documents intended formula, but implementation intent should be finalized.

3. Progression query period mapping is implicit

- API maps `MONTHLY -> 30`, default to 15; accepted values are not explicitly validated as enums at interface level.

4. Auth model is inconsistent

- Makeup routes have permission guards; player/player-stats/settlement/progression routes currently do not.
- Missing domain-level authorization policies for those slices.

## Medium Gaps

1. No explicit state machine implementation objects

- State behavior exists as implicit rules in use-cases; no explicit persisted status for many aggregates.

2. Event model is conceptual only

- Events listed in specs are not emitted via event bus yet.
- Downstream consumption exists as direct reads instead of asynchronous event flows.

3. Missing uniqueness rules in player creation

- No documented or enforced uniqueness on email and name collisions.

4. Missing date normalization policy

- Specs assume YYYY-MM-DD and UTC-safe behavior, but parsing/timezone rules are not codified.

## Testing Gaps Against Spec

1. Progression and player-management have no direct route-level contract tests.
2. Settlement has tests for generate use-case but limited negative-path coverage for malformed dates and idempotency collisions.
3. Daily-stats lacks property-based tests for bankroll reset invariants.
4. End-to-end cross-slice tests are missing for the flow: player-stats -> settlement -> makeup history.

## Recommended Next Steps

1. Introduce typed request validation (Zod or equivalent) at all external interfaces.
2. Add repository transaction boundaries for settlement and player-stats write sequences.
3. Create shared money value object under docs/shared and align all formulas.
4. Generate test specs from DomainSpec and reconcile with current unit/integration tests.
