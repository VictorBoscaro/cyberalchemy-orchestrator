---
id: player-makeup-observability-report
feature: player-makeup
title: Player Makeup Observability Alignment Report
summary: Static OTel coverage audit for player-makeup against the feature observability contract.
status: in-progress
pillar: finance
domain: player-makeup-observability
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

# Player Makeup Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 33 | From [observability.md](observability.md) declarations |
| Instrumented in code | 28 | ✅ Found with matching type and required attributes |
| Partially instrumented | 5 | ⚠️ Found with type/attribute drift |
| Missing from code | 0 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 8 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 100.0% (33/33) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O1 | 2 | 2 | PASS | All declared obligations evidenced |
| O2 | 1 | 1 | PASS | All declared obligations evidenced |
| O3 | 1 | 1 | PASS | All declared obligations evidenced |
| O4 | 4 | 4 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O9 | 2 | 2 | PASS | All declared obligations evidenced |
| O10 | 3 | 3 | PASS | All declared obligations evidenced |
| O12 | 5 | 4 | PARTIAL | 1 partial |
| O13 | 5 | 2 | PARTIAL | 3 partial |
| O15 | 3 | 3 | PASS | All declared obligations evidenced |
| O16 | 6 | 6 | PASS | All declared obligations evidenced |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `state.transition` | Counter | O1 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:258` | ✅ | — |
| `state.invalid_transition` | Counter | O1 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:334` | ✅ | — |
| `state.population` | UpDownCounter | O2 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:267` | ✅ | — |
| `invariant.violation` | Gauge | O3 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:343` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:453` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:458` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:453` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/makeup/set-player-makeup-policy.ts:98` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=player-makeup |
| `idempotency.violation` | Gauge | O9 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:282` | ✅ | — |
| `idempotency.dedup` | Counter | O9 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:291` | ✅ | — |
| `event.emit` | Counter | O10 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:317` | ✅ | — |
| `event.consume` | Counter | O10 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:321` | ✅ | — |
| `event.consumer.lag` | Histogram | O10 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:326` | ✅ | — |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:463` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:468` | ✅ | — |
| `workflow.failed` | Counter | O12 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:441` | ✅ | — |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:463` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:468` | ⚠️ | missing required attrs: workflow=SettlementMakeupApplication |
| `business.adjustments_executed` | Counter | O13 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:401` | ✅ | — |
| `business.total_makeup_outstanding` | Gauge | O13 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:406` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.avg_debt_per_player` | Gauge | O13 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:409` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.players_in_debt` | Gauge | O13 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:412` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `business.policy_changes` | Counter | O13 | `backend/src/use-cases/makeup/set-player-makeup-policy.ts:83` | ✅ | — |
| `reconciliation.mismatch` | Gauge | O15 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:376` | ✅ | — |
| `transaction.duplicate` | Counter | O15 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:287` | ✅ | — |
| `exposure.amount` | Gauge | O15 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:295` | ✅ | — |
| `makeup.cycle.adjustments` | Counter | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:384` | ✅ | — |
| `makeup.cycle.total_increase` | Counter | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:388` | ✅ | — |
| `makeup.cycle.total_decrease` | Counter | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:393` | ✅ | — |
| `makeup.cycle.net_change` | Gauge | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:397` | ✅ | — |
| `makeup.cycle.error_rate` | Gauge | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:436` | ✅ | — |
| `makeup.recalculation.drift` | Gauge | O16 | `backend/src/use-cases/makeup/adjust-player-makeup.ts:243` | ✅ | — |

## Undeclared Metrics

- `calculation.drift`
- `postcondition.check`
- `query.cache.hit`
- `query.cache.hit_ratio`
- `query.cache.lookup`
- `query.duration`
- `query.result_size`
- `rule.violation`

## Change Requests

| # | Priority | Action | Target File | Instrument | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=player-makeup |
| 2 | P1 | Fix | `backend/src/use-cases/makeup/adjust-player-makeup.ts` | `workflow.duration` | missing required attrs: workflow=SettlementMakeupApplication |
| 3 | P2 | Fix | `backend/src/use-cases/makeup/adjust-player-makeup.ts` | `business.avg_debt_per_player` | type mismatch: expected Gauge, found Histogram |
| 4 | P2 | Fix | `backend/src/use-cases/makeup/adjust-player-makeup.ts` | `business.players_in_debt` | type mismatch: expected Gauge, found Histogram |
| 5 | P2 | Fix | `backend/src/use-cases/makeup/adjust-player-makeup.ts` | `business.total_makeup_outstanding` | type mismatch: expected Gauge, found Histogram |

## Next Actions

1. Run `domainspec-instrument-otel player-makeup --change-requests docs/features/player-makeup/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify player-makeup` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
