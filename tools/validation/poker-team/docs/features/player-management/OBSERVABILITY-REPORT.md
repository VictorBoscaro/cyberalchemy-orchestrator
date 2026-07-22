---
id: player-management-observability-report
feature: player-management
title: Player Management Observability Alignment Report
summary: Static OTel coverage audit for player-management against the feature observability contract.
status: in-progress
pillar: operations
domain: player-management-observability
audience:
  - developers
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-30
dependencies:
  - observability.md
  - operations.md
includes: []
---

# Player Management Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 13 | From [observability.md](observability.md) declarations |
| Instrumented in code | 10 | ✅ Found with matching type and required attributes |
| Partially instrumented | 3 | ⚠️ Found with type/attribute drift |
| Missing from code | 0 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 5 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 100.0% (13/13) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O4 | 8 | 8 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O13 | 4 | 2 | PARTIAL | 2 partial |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/player/create-player.ts:230` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/player/create-player.ts:235` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/player/create-player.ts:230` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/coach/create-coach.ts:130` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/player/create-player.ts:230` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/coach/assign-coach.ts:152` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/player/create-player.ts:230` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/coach/unassign-coach.ts:80` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=player-management |
| `business.players_created` | Counter | O13 | `backend/src/use-cases/player/create-player.ts:177` | ✅ | — |
| `business.active_coaches` | Gauge | O13 | `backend/src/use-cases/coach/create-coach.ts:95` | ⚠️ | type mismatch: expected Gauge, found UpDownCounter |
| `business.coach_assignment_ratio` | Gauge | O13 | `backend/src/use-cases/coach/assign-coach.ts:126` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.duplicate_email_attempts` | Counter | O13 | `backend/src/use-cases/player/create-player.ts:219` | ✅ | — |

## Undeclared Metrics

- `business.coach_assignments`
- `postcondition.check`
- `query.duration`
- `query.result_size`
- `rule.violation`

## Change Requests

| # | Priority | Action | Target File | Instrument | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=player-management |
| 2 | P2 | Fix | `backend/src/use-cases/coach/create-coach.ts` | `business.active_coaches` | type mismatch: expected Gauge, found UpDownCounter |
| 3 | P2 | Fix | `backend/src/use-cases/coach/assign-coach.ts` | `business.coach_assignment_ratio` | type mismatch: expected Gauge, found Histogram |

## Next Actions

1. Run `domainspec-instrument-otel player-management --change-requests docs/features/player-management/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify player-management` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
