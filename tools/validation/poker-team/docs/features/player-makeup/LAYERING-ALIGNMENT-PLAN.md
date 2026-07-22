---
id: player-makeup
feature: player-makeup
title: Player Makeup Layering Alignment Plan
summary: Dependency-ordered remediation plan to complete domain layering alignment for player-makeup behavior.
status: implemented
pillar: finance
domain: player-makeup-layering-plan
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
  - LAYERING-ALIGNMENT-REPORT.md
includes: []
---

# Layering Alignment Plan: Player Makeup

## Scope

This plan remediates drift items PMK-LDR-01 and PMK-LDR-02 while preserving current behavior contracts for:

- player-makeup.AdjustPlayerMakeup
- player-makeup.MakeupAdjusted
- player-makeup.MakeupAdjustmentWorkflow

## Dependency-Ordered Remediation Waves

### Wave 1: Extract Audit Metadata Policy (PMK-LDR-01)

Objective:
- Move audit metadata validation out of use-case orchestration into domain-level policy module.

Tasks:
1. Add domain policy module:
- Create backend/src/domain/makeup/makeup-audit-metadata.service.ts
- Add `validateMakeupAuditMetadata` and `normalizeMakeupAuditMetadata`.

2. Add unit tests for domain policy:
- Create backend/src/domain/makeup/makeup-audit-metadata.service.test.ts
- Cover required fields, trimming, and error behavior.

3. Refactor use-case to consume domain policy:
- Update backend/src/use-cases/makeup/adjust-player-makeup.ts
- Replace inline metadata checks with domain policy call.

4. Keep API contract behavior unchanged:
- Validate route/use-case tests still assert `Invalid audit metadata` mapping where expected.

Acceptance target:
- No direct audit metadata rule checks remain in use-case body.

### Wave 2: Extract Effective Date Normalization (PMK-LDR-02)

Objective:
- Move mutation date defaulting/normalization to domain helper for deterministic policy location.

Tasks:
1. Extend makeup adjustment domain service:
- Update backend/src/domain/makeup/makeup-adjustment.service.ts
- Add `resolveAdjustmentDate(inputDate?: string, now?: Date)` with deterministic YYYY-MM-DD output and validation.

2. Add/extend unit tests:
- Update backend/src/domain/makeup/makeup-adjustment.service.test.ts
- Cover explicit date, fallback date, and invalid date semantics.

3. Refactor use-case date handling:
- Update backend/src/use-cases/makeup/adjust-player-makeup.ts
- Replace inline `new Date().toISOString().slice(0, 10)` with domain helper call.

Acceptance target:
- Use-case retains orchestration only; date policy is domain-owned.

### Wave 3: Enforcement and Documentation Lock

Objective:
- Ensure future player-makeup changes preserve layering guardrails.

Tasks:
1. Add explicit policy-ownership note in feature operations docs:
- Update docs/features/player-makeup/operations.md with domain policy ownership section.

2. Link plan/report from feature include set (optional but recommended):
- Update docs/features/player-makeup/SPEC.md `includes` list to reference layering artifacts when governance process adopts them.

3. Keep audit gate in workflow:
- Ensure future planning/implementation for this feature runs domainspec-audit-layering before edits.

Acceptance target:
- Layering constraints are visible in docs and repeatable in execution workflow.

## Verification Commands

Unit checks:
1. cd backend && npm test -- src/domain/makeup/makeup-adjustment.service.test.ts src/domain/makeup/makeup-audit-metadata.service.test.ts
2. cd backend && npm test -- src/use-cases/makeup/adjust-player-makeup.test.ts

Integration/contract checks:
1. cd backend && npm test -- src/infrastructure/http/routes/makeup.routes.contract.test.ts src/infrastructure/http/routes/makeup.routes.auth.test.ts
2. cd backend && npm test -- src/use-cases/settlement/generate-settlement.makeup-idempotency.test.ts src/use-cases/financial-settlement/generate-settlement.test.ts

Project checks:
1. cd backend && npm run typecheck
2. cd backend && npm test
3. cd . && npm run docs:index

## Completion Criteria

1. PMK-LDR-01 and PMK-LDR-02 are resolved in code and tests.
2. Player-makeup use-cases contain orchestration only (repo calls, transaction boundaries, DTO mapping).
3. Domain policy logic for audit metadata and mutation-date normalization is unit tested.
4. Docs index is regenerated and feature docs remain consistent with DomainSpec authority.
