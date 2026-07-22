---
id: player-onboarding
feature: player-onboarding
title: Player Onboarding Alignment Report
summary: 2026-04-24 alignment refresh for onboarding contracts and handoff behavior.
status: in-progress
pillar: operations
domain: onboarding-candidates
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - operations-core
  - backend-core
  - web-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - TEST-SPEC.md
  - interfaces.md
  - workflows.md
includes: []
---

# Alignment Report: player-onboarding

**Audit date:** 2026-04-24  
**Framework version:** DomainSpec 1.8.2  
**Sources:** [SPEC.md](SPEC.md), [operations.md](operations.md), [interfaces.md](interfaces.md), [TEST-SPEC.md](TEST-SPEC.md), [UI-REVIEW.md](UI-REVIEW.md)

## Executive Summary

1. Admin onboarding permissions are now split and enforced consistently for list, detail, and review actions.
2. Rule screen grouping and regulation version selection are now domain-policy driven and test-covered.
3. Approved candidate handoff to player-management is implemented through a dedicated gateway and persistence path.
4. Candidate dedupe is hardened with DB uniqueness constraints plus race-safe duplicate mapping.
5. UI review evidence was refreshed; stale BLOCK findings are resolved and remaining UI items are non-blocking flags.

## Findings

| ID | Status | Severity | Gap Type | Evidence | Required Action |
| --- | --- | --- | --- | --- | --- |
| POB-ALG-01 | RESOLVED | HIGH | permission-model drift | `backend/src/infrastructure/http/routes/onboarding.routes.ts`, `backend/src/domain/auth-access-control/role-definitions.ts`, `backend/src/infrastructure/http/routes/onboarding.routes.test.ts` | None. Split admin permissions are enforced and tested. |
| POB-ALG-02 | RESOLVED | HIGH | policy-wiring drift | `backend/src/domain/onboarding/rule-screen-grouping-policy.service.ts`, `backend/src/domain/onboarding/rule-screen-grouping-policy.service.test.ts`, `backend/src/use-cases/onboarding/get-onboarding-flow.ts` | None. Grouping policy is domain-owned and configurable. |
| POB-ALG-03 | RESOLVED | HIGH | spec-without-code | `backend/src/use-cases/onboarding/review-candidate-application.ts`, `backend/src/infrastructure/repositories/drizzle-onboarding-player-intake-handoff.repository.ts`, `backend/src/use-cases/onboarding/review-candidate-application.test.ts` | None. Approved review now emits deterministic intake handoff payload. |
| POB-ALG-04 | RESOLVED | HIGH | integrity gap | `backend/drizzle/0001_solid_intake_handoff.sql`, `backend/src/infrastructure/database/schema.ts`, `backend/src/use-cases/onboarding/submit-candidate-application.ts`, `backend/src/use-cases/onboarding/submit-candidate-application.test.ts` | None. DB-level dedupe and race-safe error mapping are implemented. |
| POB-ALG-05 | RESOLVED | MEDIUM | UI evidence freshness | [UI-REVIEW.md](UI-REVIEW.md) | None. UI review artifact is now current and blocker status is closed. |

## Concept Coverage Snapshot

| Concept ID | Status | Notes |
| --- | --- | --- |
| player-onboarding.ReviewCandidateApplication | COMPLIANT | Review operation enforces split permissions and deterministic transitions. |
| player-onboarding.RuleScreenGroupingPolicy | COMPLIANT | Runtime grouping strategy now resolves through domain policy module. |
| player-onboarding.CandidateOnboardingFlow | COMPLIANT | Approved candidate handoff is persisted for downstream intake. |
| player-onboarding.SubmitCandidateApplication | COMPLIANT | Duplicate protection now includes DB constraints and concurrent-write mapping. |

## Verdict

**FLAG** - backend and UI freshness blockers are closed; remaining UI improvements are non-blocking.
