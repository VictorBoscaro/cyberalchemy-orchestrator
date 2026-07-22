---
id: player-onboarding
feature: player-onboarding
title: Player Onboarding Layering Alignment Report
summary: 2026-04-24 layering refresh for onboarding policy and handoff boundaries.
status: in-progress
pillar: operations
domain: onboarding-candidates-layering
audience:
  - developers
  - architecture
priority: p1
lang: en
owners:
  - backend-core
  - web-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - ALIGNMENT-REPORT.md
includes: []
auditor: domainspec-layering-auditor
auditedAt: 2026-04-24
domainspecVersion: 1.8.2
---

# Layering Alignment Report: player-onboarding

**Audited at:** 2026-04-24  
**Framework version:** DomainSpec 1.8.2

## Executive Summary

1. Grouping/version policy is now isolated in domain service code.
2. Review orchestration delegates approved handoff publication through an explicit gateway dependency.
3. Remaining layering drift is concentrated in UI-side status mapping and review presentation behavior.

## Findings

| ID | Status | Severity | Layering Issue | Evidence | Remediation Requirement |
| --- | --- | --- | --- | --- | --- |
| POB-LDR-01 | RESOLVED | HIGH | grouping policy hardcoded in use-case orchestration | `backend/src/domain/onboarding/rule-screen-grouping-policy.service.ts`, `backend/src/use-cases/onboarding/get-onboarding-flow.ts` | None. Policy is domain-owned and use-case now orchestrates only. |
| POB-LDR-02 | RESOLVED | MEDIUM | approved handoff path absent from domain boundary | `backend/src/domain/onboarding/player-intake-handoff.contract.ts`, `backend/src/use-cases/onboarding/review-candidate-application.ts` | None. Handoff side effect is mediated through gateway contract. |
| POB-LDR-03 | OPEN | LOW | admin UI status interpretation remains component-local | `apps/web/src/components/onboarding/AdminOnboardingReview.tsx`, [UI-REVIEW.md](UI-REVIEW.md) | Centralize view-model status mapping where needed to tighten UI boundary ownership. |

## Layer Verdict

**FLAG** - backend layering drift is resolved; UI layering evidence remains open.
