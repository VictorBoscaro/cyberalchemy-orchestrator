---
id: player-progression
feature: player-progression
type: observability
title: "Player Progression — Observability Spec"
summary: Observability contract for promotion eligibility evaluation accuracy, latency, and decision outcomes.
derived-from: OBSERVABILITY.md rules O4–O6, O8, O13
status: draft
pillar: operations
domain: player-progression-observability
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-17
dependencies:
  - SPEC.md
  - operations.md
includes: []
---

# Player Progression — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: player-progression`.
> Single read-only evaluation operation — minimal surface but calculations matter for fair promotion decisions.

---

## Domain Fidelity Metrics

### Operation Metrics (O4–O6)

#### CheckProgression

**Base metrics (O4):**

*@source [operations.md#CheckProgression](operations.md#CheckProgression)*

```yaml
# Counts each call to CheckProgression, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to CheckProgression, grouped by success or error outcome"
  attributes:
    {
      feature: player-progression,
      operation: CheckProgression,
      result: eligible|not_eligible|error,
      period: BI_WEEKLY|MONTHLY,
    }

# Measures execution time of CheckProgression in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of CheckProgression in seconds"
  attributes:
    {
      feature: player-progression,
      operation: CheckProgression,
      period: BI_WEEKLY|MONTHLY,
    }
```

**Rule violation rates (O5):**

| Rule | Expression                           | Instrument                                | Alert Threshold                       |
| ---- | ------------------------------------ | ----------------------------------------- | ------------------------------------- |
| R1   | `exists(Player.id == playerId)`      | `rule.violation` Counter `{rule_id="R1"}` | rate > 5% → P2                        |
| R2   | `periodDays in {15, 30}`             | `rule.violation` Counter `{rule_id="R2"}` | any > 0 → P2 (API contract)           |
| R3   | `avgHands >= 1000`                   | `rule.violation` Counter `{rule_id="R3"}` | informational (not enough volume)     |
| R4   | `periodDays == 15 => winrate >= 7.5` | `rule.violation` Counter `{rule_id="R4"}` | informational (not meeting threshold) |
| R5   | `periodDays == 30 => winrate >= 5.0` | `rule.violation` Counter `{rule_id="R5"}` | informational (not meeting threshold) |

> **Business insight:** R3–R5 are not "violations" in a failure sense — they represent players who checked progression but didn't qualify. Tracking their rates tells us how realistic the promotion thresholds are.

**Calculation drift (O6):**

| Calc | Formula                                    | Instrument                                            | Frequency     | Alert                                        |
| ---- | ------------------------------------------ | ----------------------------------------------------- | ------------- | -------------------------------------------- |
| C1   | `stats where date >= now - periodDays`     | `calculation.drift` Histogram `{calculation_id="C1"}` | On each check | drift > 0 → P1 (window filter broken)        |
| C2   | `avgHands = sum(hands) / periodDays`       | `calculation.drift` Histogram `{calculation_id="C2"}` | On each check | drift > 0 → P1 (average calculation broken)  |
| C3   | `winrate = (profit/bbValue) / (hands/100)` | `calculation.drift` Histogram `{calculation_id="C3"}` | On each check | drift > 0 → P1 (bb/100 normalization broken) |

> C1–C3 drift impacts promotion fairness. A broken winrate calculation could promote or hold back players incorrectly.

---

## Operational Health Metrics

### Endpoint SLOs (O8)

*@source [interfaces.md](interfaces.md)*

| Endpoint                   | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| -------------------------- | ------ | ---------------- | --------------- | ------------------- |
| `/players/:id/progression` | GET    | ≥ 99.9%          | ≤ 300ms         | ~50 req/day         |

*@source [interfaces.md](interfaces.md)*

```yaml
# Measures HTTP request latency per endpoint using OTel semantic conventions
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: GET,
      url.path: /players/*/progression,
      http.response.status_code: int,
      feature: player-progression,
    }
```

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

*@source [SPEC.md](SPEC.md) capabilities*

```yaml
- name: business.eligibility_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes:
    {
      feature: player-progression,
      capability: CheckProgression,
      period: BI_WEEKLY|MONTHLY,
    }
  formula: "eligible / total checks over 30d"
  business_question: "What % of progression checks result in eligibility?"
  healthy_range: "10%–40% (too high = thresholds too easy, too low = thresholds too hard)"
  alert: rate > 60% or rate = 0% → P2 (threshold review needed)

- name: business.checks_per_day
  instrument: Counter
  unit: "{check}"
  attributes:
    {
      feature: player-progression,
      capability: CheckProgression,
      period: BI_WEEKLY|MONTHLY,
    }
  business_question: "How often is progression being evaluated?"
  healthy_range: "> 0 on business days"

- name: business.avg_hands_at_check
  instrument: Histogram
  unit: "{hand}"
  attributes: { feature: player-progression, capability: CheckProgression }
  formula: "avgHands from each CheckProgression evaluation"
  business_question: "How many hands are players averaging when checking progression?"
  purpose: "calibrate R3 threshold (currently 1000)"

- name: business.avg_winrate_at_check
  instrument: Histogram
  unit: "{bb_per_100}"
  attributes: { feature: player-progression, capability: CheckProgression }
  formula: "winrate from each CheckProgression evaluation"
  business_question: "What winrates are players achieving?"
  purpose: "calibrate R4/R5 thresholds (currently 7.5 / 5.0 bb/100)"
```

---

## Metric Summary

| Rule                           | Metric Count                          | Layer                  | Severity |
| ------------------------------ | ------------------------------------- | ---------------------- | -------- |
| O4: CheckProgression execution | 2 (invocation + duration)             | Operational            | P1       |
| O5: Rule violations (R1–R5)    | 1 (Counter, 5 rule_id attrs)          | Domain Fidelity        | P2       |
| O6: Calculation drift (C1–C3)  | 1 (Histogram, 3 calculation_id attrs) | Domain Fidelity        | P1       |
| O8: Endpoint SLOs              | 1 (OTel HTTP semconv)                 | Operational            | P1       |
| O13: Business KPIs             | 4                                     | Business Effectiveness | P2       |
| **Total**                      | **~9 OTel instruments**               |                        |          |
