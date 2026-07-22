---
id: player-stats-observability-report
feature: player-stats
title: Player Stats Observability Alignment Report
summary: Static OTel coverage audit for player-stats against the feature observability contract.
status: in-progress
pillar: operations
domain: player-stats-observability
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

# Player Stats Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 16 | From [observability.md](observability.md) declarations |
| Instrumented in code | 11 | ✅ Found with matching type and required attributes |
| Partially instrumented | 3 | ⚠️ Found with type/attribute drift |
| Missing from code | 2 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 5 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 87.5% (14/16) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O1 | 2 | 2 | PASS | All declared obligations evidenced |
| O3 | 1 | 1 | PASS | All declared obligations evidenced |
| O4 | 2 | 2 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O10 | 3 | 1 | FAIL | 2 missing |
| O12 | 3 | 3 | PASS | All declared obligations evidenced |
| O13 | 4 | 2 | PARTIAL | 2 partial |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `state.transition` | Counter | O1 | `backend/src/use-cases/player-stats/record-player-stats.ts:194` | ✅ | — |
| `state.invalid_transition` | Counter | O1 | `backend/src/use-cases/player-stats/record-player-stats.ts:330` | ✅ | — |
| `invariant.violation` | Gauge | O3 | `backend/src/use-cases/player-stats/record-player-stats.ts:340` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/player-stats/record-player-stats.ts:358` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/player-stats/record-player-stats.ts:365` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=player-stats |
| `event.emit` | Counter | O10 | `backend/src/use-cases/player-stats/record-player-stats.ts:246` | ✅ | — |
| `event.consume` | Counter | O10 | `—` | ❌ | No recording call found |
| `event.consumer.lag` | Histogram | O10 | `—` | ❌ | No recording call found |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/player-stats/record-player-stats.ts:371` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/player-stats/record-player-stats.ts:377` | ✅ | — |
| `workflow.failed` | Counter | O12 | `backend/src/use-cases/player-stats/record-player-stats.ts:348` | ✅ | — |
| `business.stats_recorded` | Counter | O13 | `backend/src/use-cases/player-stats/record-player-stats.ts:282` | ✅ | — |
| `business.correction_rate` | Gauge | O13 | `backend/src/use-cases/player-stats/record-player-stats.ts:293` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.ingestion_latency` | Histogram | O13 | `backend/src/use-cases/player-stats/record-player-stats.ts:305` | ✅ | — |
| `business.active_players_with_stats` | Gauge | O13 | `backend/src/use-cases/player-stats/record-player-stats.ts:311` | ⚠️ | type mismatch: expected Gauge, found Histogram |

## Undeclared Metrics

- `calculation.drift`
- `postcondition.check`
- `query.duration`
- `query.result_size`
- `rule.violation`

## Change Requests

| # | Priority | Action | Target File | Instrument | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | Add | `backend/src/use-cases/player-stats/record-player-stats.ts` | `event.consume` | No recording call found |
| 2 | P1 | Add | `backend/src/use-cases/player-stats/record-player-stats.ts` | `event.consumer.lag` | No recording call found |
| 3 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=player-stats |
| 4 | P2 | Fix | `backend/src/use-cases/player-stats/record-player-stats.ts` | `business.active_players_with_stats` | type mismatch: expected Gauge, found Histogram |
| 5 | P2 | Fix | `backend/src/use-cases/player-stats/record-player-stats.ts` | `business.correction_rate` | type mismatch: expected Gauge, found Histogram |

## Next Actions

1. Run `domainspec-instrument-otel player-stats --change-requests docs/features/player-stats/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify player-stats` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
