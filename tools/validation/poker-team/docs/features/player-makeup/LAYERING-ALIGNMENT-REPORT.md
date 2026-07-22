---
id: player-makeup
feature: player-makeup
title: Player Makeup Layering Alignment Report
summary: Audit of domain layering fidelity for player-makeup concepts across domain and use-case layers.
status: implemented
pillar: finance
domain: player-makeup-layering
audience:
  - developers
  - finance
priority: p1
lang: en
owners:
  - backend-core
  - architecture-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - workflows.md
includes: []
---

# Layering Alignment Report: Player Makeup

## Current-Framework Constraints (from domainspec/CHANGELOG.md)

1. DomainSpec artifacts remain semantic source of truth for behavior and acceptance.
2. `gsd-phase` delegation can orchestrate execution, but cannot override DomainSpec semantics.
3. Layering audit gate is expected before planning/implementation for features with existing code.

## Concept-To-Code Map

| Concept ID | Primary spec anchor | Domain implementation | Use-case/application implementation |
| --- | --- | --- | --- |
| player-makeup.AdjustPlayerMakeup | operations.md#adjustplayermakeup | backend/src/domain/makeup/makeup-adjustment.service.ts | backend/src/use-cases/makeup/adjust-player-makeup.ts |
| player-makeup.GetPlayerMakeupHistory | queries.md#getplayermakeuphistory | backend/src/domain/makeup/makeup-history.service.ts | backend/src/use-cases/makeup/get-player-makeup-history.ts |
| player-makeup.SettlementMakeupApplicationContract | workflows.md#settlementmakeupapplicationcontract | backend/src/domain/settlement/settlement.service.ts | backend/src/use-cases/financial-settlement/generate-settlement.ts |
| player-makeup.MakeupApplied | events.md#makeupapplied | backend/src/domain/settlement/settlement.service.ts | backend/src/use-cases/financial-settlement/generate-settlement.ts |
| player-makeup.MakeupAdjusted | events.md#makeupadjusted | backend/src/domain/makeup/makeup-adjustment.service.ts | backend/src/use-cases/makeup/adjust-player-makeup.ts |

## Behavior Location Classification

| Behavior | Current location | Classification | Assessment |
| --- | --- | --- | --- |
| Makeup rounding and debt-floor math (C1-C5) | domain/makeup-adjustment.service.ts | domain | aligned |
| History filtering, ordering, cursor policy | domain/makeup-history.service.ts | domain | aligned |
| Settlement policy math (S1-S4) | domain/settlement.service.ts | domain | aligned |
| Settlement event decision logic (MAKEUP_APPLIED/PAYOUT emission gating) | domain/settlement.service.ts | domain | aligned |
| Transaction boundary and write orchestration | use-cases + financial unit-of-work | application | aligned |
| Audit metadata presence validation for adjustment mutation | use-cases/makeup/adjust-player-makeup.ts | misplaced | move candidate |
| Effective date defaulting (`now` when date missing) | use-cases/makeup/adjust-player-makeup.ts | misplaced | move candidate |

## Misplaced Items

| Drift ID | Severity | Concept linkage | Evidence | Why misplaced | Target destination |
| --- | --- | --- | --- | --- | --- |
| PMK-LDR-01 | medium | player-makeup.AdjustPlayerMakeup, player-makeup.MakeupAdjusted | backend/src/use-cases/makeup/adjust-player-makeup.ts validates actorId/requestId/reasonCode/sourceChannel directly | This is mutation-level policy validation that should be reusable and testable as domain policy/value-object logic, not embedded in orchestration flow. | backend/src/domain/makeup/makeup-audit-metadata.service.ts (or value object module) |
| PMK-LDR-02 | low | player-makeup.AdjustPlayerMakeup | backend/src/use-cases/makeup/adjust-player-makeup.ts derives fallback date from system clock | Domain-effective date normalization for mutation audit/event date should be deterministic in domain helper to avoid orchestration-level policy drift. | backend/src/domain/makeup/makeup-adjustment.service.ts (add date normalization helper) |

## No-Drift Confirmations

1. Domain policy calculations and thresholds are no longer in player-makeup use-cases.
2. Domain invariants for non-negative makeup and half-up normalization are centralized in domain services.
3. Settlement side-effect decisions are centralized in domain service and use-case remains orchestration.
4. Use-cases remain responsible for repository orchestration and transaction boundaries, which is allowed.

## Audit Verdict

- Overall status: partial alignment.
- Drift severity profile: 0 critical, 0 high, 1 medium, 1 low.
- Release risk impact: low for correctness, medium for long-term maintainability/reuse.
