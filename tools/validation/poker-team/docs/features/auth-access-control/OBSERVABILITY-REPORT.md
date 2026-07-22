---
id: auth-access-control-observability-report
feature: auth-access-control
title: Auth & Access Control Observability Alignment Report
summary: Static OTel coverage audit for auth-access-control against the feature observability contract.
status: in-progress
pillar: platform
domain: auth-access-control-observability
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

# Auth & Access Control Observability Alignment Report

> Compares declared obligations in [observability.md](observability.md) against static code evidence under backend/src.
> Verification mode: static only (no live collector query).

## Summary

| Metric | Status | Detail |
| --- | --- | --- |
| Total declared instruments | 31 | From [observability.md](observability.md) declarations |
| Instrumented in code | 24 | ✅ Found with matching type and required attributes |
| Partially instrumented | 3 | ⚠️ Found with type/attribute drift |
| Missing from code | 4 | ❌ Declared but no recording evidence found |
| Extra (undeclared) | 10 | 🔄 Recorded in code but not declared in observability.md |

**Verdict:** FLAG

Coverage is 87.1% (27/31) including partials.

## Coverage by Rule

| Rule | Declared | Instrumented | Status | Notes |
| --- | --- | --- | --- | --- |
| O1 | 3 | 3 | PASS | All declared obligations evidenced |
| O2 | 2 | 2 | PASS | All declared obligations evidenced |
| O3 | 1 | 1 | PASS | All declared obligations evidenced |
| O4 | 10 | 10 | PASS | All declared obligations evidenced |
| O5 | 2 | 2 | PASS | All declared obligations evidenced |
| O8 | 1 | 0 | PARTIAL | 1 partial |
| O10 | 3 | 3 | PASS | All declared obligations evidenced |
| O12 | 5 | 3 | PARTIAL | 2 partial |
| O13 | 4 | 0 | FAIL | 4 missing |

## Instrument Detail

| Instrument Name | Type | Source Rule | Code Location | Status | Issue |
| --- | --- | --- | --- | --- | --- |
| `state.transition` | Counter | O1 | `backend/src/use-cases/auth-access-control/login.ts:228` | ✅ | — |
| `state.invalid_transition` | Counter | O1 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:76` | ✅ | — |
| `state.population` | UpDownCounter | O2 | `backend/src/use-cases/auth-access-control/login.ts:235` | ✅ | — |
| `state.transition` | Counter | O1 | `backend/src/use-cases/auth-access-control/login.ts:228` | ✅ | — |
| `state.population` | UpDownCounter | O2 | `backend/src/use-cases/auth-access-control/login.ts:235` | ✅ | — |
| `invariant.violation` | Gauge | O3 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:169` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/auth-access-control/login.ts:320` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/auth-access-control/login.ts:325` | ✅ | — |
| `security.login_denied` | Counter | O5 | `backend/src/use-cases/auth-access-control/login.ts:119` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:209` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/auth-access-control/login.ts:404` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:209` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:214` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:209` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/auth-access-control/authorize-request.ts:178` | ✅ | — |
| `security.access_denied` | Counter | O5 | `backend/src/use-cases/auth-access-control/authorize-request.ts:108` | ✅ | — |
| `operation.invocation` | Counter | O4 | `backend/src/use-cases/auth-access-control/logout.ts:266` | ✅ | — |
| `operation.duration` | Histogram | O4 | `backend/src/use-cases/auth-access-control/logout.ts:271` | ✅ | — |
| `http.server.request.duration` | Histogram | O8 | `backend/src/infrastructure/telemetry/metrics-plugin.ts:21` | ⚠️ | missing required attrs: feature=auth-access-control |
| `event.emit` | Counter | O10 | `backend/src/use-cases/auth-access-control/authorize-request.ts:130` | ✅ | — |
| `event.consume` | Counter | O10 | `backend/src/use-cases/auth-access-control/authorize-request.ts:134` | ✅ | — |
| `event.consumer.lag` | Histogram | O10 | `backend/src/use-cases/auth-access-control/authorize-request.ts:139` | ✅ | — |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:219` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:224` | ⚠️ | missing required attrs: workflow=EndToEndAuthFlow |
| `workflow.failed` | Counter | O12 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:200` | ✅ | — |
| `workflow.invocation` | Counter | O12 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:219` | ✅ | — |
| `workflow.duration` | Histogram | O12 | `backend/src/use-cases/auth-access-control/authenticate-request.ts:224` | ⚠️ | missing required attrs: workflow=AuthorizeRequestFlow |
| `business.login_success_rate` | Gauge | O13 | `—` | ❌ | No recording call found |
| `business.active_sessions` | Gauge | O13 | `—` | ❌ | No recording call found |
| `business.avg_session_duration` | Histogram | O13 | `—` | ❌ | No recording call found |
| `business.authorization_deny_rate` | Gauge | O13 | `—` | ❌ | No recording call found |

## Undeclared Metrics

- `business.authorization_decisions`
- `business.logins`
- `business.tokens_issued`
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
| 1 | P1 | Add | `backend/src/use-cases/auth-access-control/login.ts` | `business.active_sessions` | No recording call found |
| 2 | P1 | Add | `backend/src/use-cases/auth-access-control/login.ts` | `business.login_success_rate` | No recording call found |
| 3 | P1 | Fix | `backend/src/infrastructure/telemetry/metrics-plugin.ts` | `http.server.request.duration` | missing required attrs: feature=auth-access-control |
| 4 | P1 | Fix | `backend/src/use-cases/auth-access-control/authenticate-request.ts` | `workflow.duration` | missing required attrs: workflow=AuthorizeRequestFlow |
| 5 | P1 | Fix | `backend/src/use-cases/auth-access-control/authenticate-request.ts` | `workflow.duration` | missing required attrs: workflow=EndToEndAuthFlow |
| 6 | P2 | Add | `backend/src/use-cases/auth-access-control/login.ts` | `business.authorization_deny_rate` | No recording call found |
| 7 | P2 | Add | `backend/src/use-cases/auth-access-control/login.ts` | `business.avg_session_duration` | No recording call found |

## Next Actions

1. Run `domainspec-instrument-otel auth-access-control --change-requests docs/features/auth-access-control/OBSERVABILITY-REPORT.md`.
2. Re-run `domainspec-otel-verify auth-access-control` to confirm coverage.
3. If verdict is PASS, proceed to `domainspec-verify-feature`.
