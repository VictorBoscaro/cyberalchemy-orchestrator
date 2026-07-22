---
id: player-management
feature: player-management
title: Player Management Layering Alignment Report
summary: 2026-04-24 layering refresh for visibility and player identity boundaries.
status: in-progress
pillar: operations
domain: player-management-layering
audience:
  - developers
  - architecture
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - ALIGNMENT-REPORT.md
includes: []
auditor: domainspec-layering-auditor
auditedAt: 2026-04-24
domainspecVersion: 1.8.2
---

# Layering Alignment Report: player-management

**Audited at:** 2026-04-24  
**Framework version:** DomainSpec 1.8.2

## Executive Summary

1. Visibility authority is now centralized in domain policy (`player-visibility.service.ts`).
2. Identity linkage (`principalId`) is represented in domain entity and persistence layers.
3. Lifecycle event ownership boundaries are now explicit in player and coach use-cases.
4. `GetCoachPlayers` now treats permission checks as authorization preconditions without overriding domain visibility scope.

## Findings

| ID | Status | Severity | Layering Issue | Evidence | Remediation Requirement |
| --- | --- | --- | --- | --- | --- |
| PM-LDR-01 | RESOLVED | MEDIUM | visibility policy split between use-case and domain layers | `backend/src/domain/coach/player-visibility.service.ts`, `backend/src/use-cases/coach/get-coach-players.ts` | None. Domain service is authoritative for visibility decisions. |
| PM-LDR-02 | PARTIAL | LOW | validation and normalization still partly use-case-local | `backend/src/use-cases/player/create-player.ts` | Optional hardening: extract reusable normalization/value-object factories for shared player identity rules. |
| PM-LDR-03 | RESOLVED | MEDIUM | lifecycle event emission boundary not yet deterministic | [events.md](events.md), `backend/src/use-cases/player/create-player.ts`, `backend/src/use-cases/coach/create-coach.ts`, `backend/src/use-cases/coach/assign-coach.ts`, `backend/src/use-cases/coach/unassign-coach.ts` | None. Lifecycle events are emitted in canonical operation flows and covered by tests. |
| PM-LDR-04 | RESOLVED | HIGH | permission check overrode domain ownership boundary in coach query flow | `backend/src/use-cases/coach/get-coach-players.ts`, `backend/src/use-cases/coach/get-coach-players.test.ts` | None. Ownership scope remains domain-enforced; permissions no longer escalate data scope. |

## Layer Verdict

**FLAG** - core layering is stable; remaining low-severity hardening is optional normalization extraction.
