---
id: player-stats
feature: player-stats
title: Player Stats Alignment Report
summary: 2026-04-24 alignment refresh for stats UI contract fidelity and projection evidence.
status: in-progress
pillar: operations
domain: player-stats
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - TEST-SPEC.md
  - UI-REVIEW.md
includes: []
---

# Alignment Report: player-stats

**Audit date:** 2026-04-24
**Framework version:** DomainSpec 1.8.2
**Sources:** [SPEC.md](SPEC.md), [operations.md](operations.md), [queries.md](queries.md), [UI-REVIEW.md](UI-REVIEW.md)

## Executive Summary

1. Core record/history/window contracts remain implemented and deterministic.
2. UI review evidence is refreshed and now reflects current cursor pagination behavior.
3. Stats window query/UI data flow now aligns required `fromDate`/`toDate` input and canonical `winrateBbPer100` projection.
4. Remaining readiness risk is now observability hardening coverage (P1/P2), not missing P0 telemetry.

## Findings

| ID | Status | Severity | Gap Type | Evidence | Required Action |
| --- | --- | --- | --- | --- | --- |
| PST-ALG-01 | RESOLVED | MEDIUM | UI contract mismatch | [UI-REVIEW.md](UI-REVIEW.md), `apps/web/src/hooks/use-stats.ts`, `apps/web/src/components/stats/StatsWindowCard.tsx` | None. UI now sends required window params and renders canonical window metrics. |
| PST-ALG-02 | RESOLVED | MEDIUM | evidence freshness | [TEST-SPEC.md](TEST-SPEC.md), [UI-REVIEW.md](UI-REVIEW.md) | None. Evidence artifacts were refreshed for current implementation behavior. |
| PST-ALG-03 | PARTIAL | MEDIUM | observability coverage below full threshold | [observability.md](observability.md), [OBSERVABILITY-REPORT.md](OBSERVABILITY-REPORT.md), `backend/src/use-cases/player-stats/record-player-stats.ts` | Keep P0 telemetry regression-locked; complete remaining P1/P2 observability backlog (O8 semconv hardening and O13 KPI projection metrics). |

## Concept Coverage Snapshot

| Concept ID | Status | Notes |
| --- | --- | --- |
| player-stats.RecordPlayerStats | COMPLIANT | Operation contract and use-case behavior present. |
| player-stats.GetPlayerStatsHistory | COMPLIANT | Query and interface contracts present. |
| player-stats.GetPlayerStatsWindow | COMPLIANT | Query contract is implemented and UI mapping now uses canonical fields. |
| player-stats.PlayerStatsRecordLifecycle | COMPLIANT | State machine documented and linked in SPEC. |
| player-stats.ObservabilityCoverage | PARTIAL | P0 lifecycle telemetry is now instrumented; report verdict is FLAG with only non-blocking backlog items remaining. |

## Verdict

**FLAG** - behavior and contract alignment are stable and P0 observability gates are instrumented; remaining observability work is non-blocking hardening.
