---
id: player-onboarding-observability-report
feature: player-onboarding
title: Player Onboarding Observability Alignment Report
summary: Static OTel coverage audit for player-onboarding against the feature observability contract.
status: in-progress
pillar: operations
domain: player-onboarding-observability
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

# Player Onboarding Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 19 | From [observability.md](observability.md) declarations |
| Instrumented in code | 14 | ✅ Found with matching type and required attributes |
| Partially instrumented | 2 | ⚠️ Found with type/attribute drift |
| Missing from code | 3 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 13 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 84.2% (16/19) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O1 | 2 | 2 | PASS | All declared obligations evidenced |
| O2 | 1 | 1 | PASS | All declared obligations evidenced |
| O3 | 1 | 1 | PASS | All declared obligations evidenced |
| O4 | 5 | 5 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O12 | 3 | 2 | FAIL | 1 missing |
| O13 | 4 | 3 | FAIL | 1 missing |
| O14 | 2 | 0 | PARTIAL | 1 missing, 1 partial |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `state.transition` | Counter | O1 | `backend/src/use-cases/onboarding/review-candidate-application.ts:63` | ✅ | — |
| `state.invalid_transition` | Counter | O1 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:105` | ✅ | — |
| `state.population` | UpDownCounter | O2 | `backend/src/use-cases/onboarding/review-candidate-application.ts:70` | ✅ | — |
| `invariant.violation` | Gauge | O3 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:131` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/onboarding/review-candidate-application.ts:205` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:246` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/onboarding/review-candidate-application.ts:205` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/onboarding/review-candidate-application.ts:210` | ✅ | — |
| `business.review_decision` | Counter | O4 | `backend/src/use-cases/onboarding/review-candidate-application.ts:126` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=player-onboarding |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/onboarding/review-candidate-application.ts:215` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:256` | ✅ | — |
| `workflow.step.duration` | Histogram | O12 | `—` | ❌ | No recording call found |
| `business.applications_submitted` | Counter | O13 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:175` | ✅ | — |
| `business.approval_rate` | Gauge | O13 | `—` | ❌ | No recording call found |
| `business.time_to_review` | Histogram | O13 | `backend/src/use-cases/onboarding/review-candidate-application.ts:132` | ✅ | — |
| `business.duplicate_blocked` | Counter | O13 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:220` | ✅ | — |
| `funnel.conversion_rate` | Gauge | O14 | `backend/src/use-cases/onboarding/submit-candidate-application.ts:186` | ⚠️ | type mismatch: expected Gauge, found Histogram |
| `funnel.drop_off` | Gauge | O14 | `—` | ❌ | No recording call found |

## Undeclared Metrics

- `calculation.drift`
- `event.consume`
- `event.consumer.lag`
- `event.emit`
- `funnel.step`
- `postcondition.check`
- `query.cache.hit`
- `query.cache.hit_ratio`
- `query.cache.lookup`
- `query.duration`
- `query.result_size`
- `rule.violation`
- `workflow.failed`

## Change Requests

| # | Priority | Action | Target File | Instrument | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=player-onboarding |
| 2 | P1 | Add | `backend/src/use-cases/onboarding/submit-candidate-application.ts` | `workflow.step.duration` | No recording call found |
| 3 | P2 | Add | `backend/src/use-cases/onboarding/submit-candidate-application.ts` | `business.approval_rate` | No recording call found |
| 4 | P2 | Fix | `backend/src/use-cases/onboarding/submit-candidate-application.ts` | `funnel.conversion_rate` | type mismatch: expected Gauge, found Histogram |
| 5 | P2 | Add | `backend/src/use-cases/onboarding/submit-candidate-application.ts` | `funnel.drop_off` | No recording call found |

## Next Actions

1. Run `domainspec-instrument-otel player-onboarding --change-requests docs/features/player-onboarding/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify player-onboarding` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
