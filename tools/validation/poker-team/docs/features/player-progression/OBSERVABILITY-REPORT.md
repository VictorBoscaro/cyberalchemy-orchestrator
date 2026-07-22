---
id: player-progression-observability-report
feature: player-progression
title: Player Progression Observability Alignment Report
summary: Static OTel coverage audit for player-progression against the feature observability contract.
status: in-progress
pillar: operations
domain: player-progression-observability
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

# Player Progression Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 7 | From [observability.md](observability.md) declarations |
| Instrumented in code | 5 | ✅ Found with matching type and required attributes |
| Partially instrumented | 2 | ⚠️ Found with type/attribute drift |
| Missing from code | 0 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 2 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 100.0% (7/7) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O4 | 2 | 2 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O13 | 4 | 3 | PARTIAL | 1 partial |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/progression/check-progression.ts:209` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/progression/check-progression.ts:215` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=player-progression |
| `business.eligibility_rate` | Gauge | O13 | `backend/src/use-cases/progression/check-progression.ts:185` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.checks_per_day` | Counter | O13 | `backend/src/use-cases/progression/check-progression.ts:180` | ✅ | — |
| `business.avg_hands_at_check` | Histogram | O13 | `backend/src/use-cases/progression/check-progression.ts:195` | ✅ | — |
| `business.avg_winrate_at_check` | Histogram | O13 | `backend/src/use-cases/progression/check-progression.ts:199` | ✅ | — |

## Undeclared Metrics

- `calculation.drift`
- `rule.violation`

## Change Requests

| # | Priority | Action | Target File | Instrument | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=player-progression |
| 2 | P2 | Fix | `backend/src/use-cases/progression/check-progression.ts` | `business.eligibility_rate` | type mismatch: expected Gauge, found Histogram |

## Next Actions

1. Run `domainspec-instrument-otel player-progression --change-requests docs/features/player-progression/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify player-progression` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
