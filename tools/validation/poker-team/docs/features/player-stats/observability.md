---
id: player-stats
feature: player-stats
type: observability
title: "Player Stats — Observability Spec"
summary: Observability contract for player stats ingestion quality, aggregate windows, and downstream data trust.
derived-from: OBSERVABILITY.md rules O1–O13
status: draft
pillar: operations
domain: player-stats-observability
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

# Player Stats — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: player-stats`.
> Stats ingestion is the data backbone — financial-settlement and player-progression depend on accurate stats.

---

## Domain Fidelity Metrics

### State Machine Monitors (O1–O3)

#### PlayerStatsRecordLifecycle

**Transition counters (O1):**

| From      | To        | Event                | Attributes                                                                           |
| --------- | --------- | -------------------- | ------------------------------------------------------------------------------------ |
| [new]     | RECORDED  | PlayerStatsRecorded  | `{entity: PlayerStatsSnapshot, from: new, to: RECORDED, event: PlayerStatsRecorded}` |
| RECORDED  | CORRECTED | PlayerStatsCorrected | `{..., from: RECORDED, to: CORRECTED, event: PlayerStatsCorrected}`                  |
| CORRECTED | CORRECTED | PlayerStatsCorrected | `{..., from: CORRECTED, to: CORRECTED, event: PlayerStatsCorrected}`                 |

*@source [states.md#PlayerStatsRecordLifecycle](states.md#PlayerStatsRecordLifecycle)*

```yaml
# @rule O1: Transition Counter
# Counts each valid state transition in the PlayerStatsRecord lifecycle
- name: state.transition
  instrument: Counter
  unit: "{transition}"
  description: "Counts each valid state transition in the PlayerStatsRecord lifecycle"
  attributes: [feature, entity, from, to, event]
```

**Invalid transition counter:**

```yaml
# Counts rejected state transitions — any increment indicates a domain logic bug
- name: state.invalid_transition
  instrument: Counter
  unit: "{attempt}"
  description: "Counts rejected state transitions — any increment indicates a domain logic bug"
  attributes: [feature, entity, from, attempted_event, error_code]
  alert: any increment → P1
```

**Invariant monitors (O3):**

| ID  | Invariant                     | Check                                               | Alert                                |
| --- | ----------------------------- | --------------------------------------------------- | ------------------------------------ |
| I1  | One snapshot per day identity | `unique(playerId, statDate)` — periodic count check | any violation → P0 (data corruption) |
| I2  | Hands are always non-negative | `hands >= 0` after every record/correction          | any violation → P1                   |

```yaml
# Detects domain invariant violations that should never occur in correct code
- name: invariant.violation
  instrument: Gauge
  unit: "{entity}"
  description: "Detects domain invariant violations that should never occur in correct code"
  attributes:
    {
      feature: player-stats,
      entity: PlayerStatsSnapshot,
      invariant_id: I1|I2,
      expression: string,
    }
  frequency: hourly
  alert: I1 violation → P0, I2 violation → P1
```

### Operation Metrics (O4–O7)

#### RecordPlayerStats

**Base metrics (O4):**

*@source [operations.md#RecordPlayerStats](operations.md#RecordPlayerStats)*

```yaml
# Counts each call to RecordPlayerStats, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to RecordPlayerStats, grouped by success or error outcome"
  attributes:
    {
      feature: player-stats,
      operation: RecordPlayerStats,
      result: success|error,
      source_type: MANUAL|IMPORT|API,
    }

# Measures execution time of RecordPlayerStats in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of RecordPlayerStats in seconds"
  attributes:
    {
      feature: player-stats,
      operation: RecordPlayerStats,
      source_type: MANUAL|IMPORT|API,
    }
```

**Rule violation rates (O5):**

| Rule | Expression                                            | Instrument                                | Alert Threshold                                      |
| ---- | ----------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------- |
| R1   | `exists(Player.id == playerId)`                       | `rule.violation` Counter `{rule_id="R1"}` | rate > 5% → P2 (bad caller data)                     |
| R2   | `isValidDate(statDate)`                               | `rule.violation` Counter `{rule_id="R2"}` | rate > 1% → P2                                       |
| R3   | `isInteger(hands) and hands >= 0`                     | `rule.violation` Counter `{rule_id="R3"}` | rate > 1% → P2 (upstream validation gap)             |
| R4   | `sourceType in {MANUAL, IMPORT, API}`                 | `rule.violation` Counter `{rule_id="R4"}` | any > 0 → P2 (API contract violation)                |
| R5   | `unique(playerId, statDate)`                          | `rule.violation` Counter `{rule_id="R5"}` | track volume — high rate from IMPORT = ingestion bug |
| R6   | `existing != null => atLeastOneFieldChanged`          | `rule.violation` Counter `{rule_id="R6"}` | informational (no-op corrections)                    |
| R7   | `rake >= 0`                                           | `rule.violation` Counter `{rule_id="R7"}` | rate > 1% → P2                                       |
| R8   | `isInteger(sessionDuration) and sessionDuration >= 0` | `rule.violation` Counter `{rule_id="R8"}` | rate > 1% → P2                                       |

> **Data integrity insight:** R5 (uniqueness) violations from IMPORT source type indicate the ingestion pipeline is sending duplicates. R6 (no change) from MANUAL indicates operators submitting identical corrections.

**Calculation drift (O6):**

| Calc | Formula                                                | Instrument                                            | Frequency      | Alert                                     |
| ---- | ------------------------------------------------------ | ----------------------------------------------------- | -------------- | ----------------------------------------- |
| C1   | `snapshotKey = playerId + ':' + statDate`              | `calculation.drift` Histogram `{calculation_id="C1"}` | On each record | drift > 0 → P1 (key generation broken)    |
| C2   | `status = RECORDED if existing == null else CORRECTED` | `calculation.drift` Histogram `{calculation_id="C2"}` | On each record | drift > 0 → P1 (status derivation broken) |

**Postcondition verification (O7):**

| Postcondition                           | Instrument                                                                           | Alert                    |
| --------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| Snapshot exists for playerId + statDate | `postcondition.check` Counter `{postcondition_id="snapshot_persisted", result}`      | any result=violated → P1 |
| New records emit PlayerStatsRecorded    | `postcondition.check` Counter `{postcondition_id="recorded_event_emitted", result}`  | any result=violated → P1 |
| Corrections emit PlayerStatsCorrected   | `postcondition.check` Counter `{postcondition_id="corrected_event_emitted", result}` | any result=violated → P1 |

---

## Operational Health Metrics

### Endpoint SLOs (O8)

*@source [interfaces.md](interfaces.md)*

| Endpoint                          | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| --------------------------------- | ------ | ---------------- | --------------- | ------------------- |
| `/player-stats`                   | POST   | ≥ 99.9%          | ≤ 500ms         | ~200 req/day        |
| `/player-stats/:playerId/history` | GET    | ≥ 99.9%          | ≤ 300ms         | ~100 req/day        |
| `/player-stats/:playerId/window`  | GET    | ≥ 99.9%          | ≤ 200ms         | ~300 req/day        |

*@source [interfaces.md](interfaces.md)*

```yaml
# Measures HTTP request latency per endpoint using OTel semantic conventions
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: POST|GET,
      url.path: /player-stats*,
      http.response.status_code: int,
      feature: player-stats,
    }
```

### Event Flow (O10)

| Event                | Producer          | Consumers                                        | Lag SLO |
| -------------------- | ----------------- | ------------------------------------------------ | ------- |
| PlayerStatsRecorded  | RecordPlayerStats | player-management overview, financial-settlement | ≤ 5s    |
| PlayerStatsCorrected | RecordPlayerStats | player-management overview, analytics            | ≤ 5s    |

*@source [events.md](events.md)*

```yaml
# Counts domain events published by this feature
- name: event.emit # Counter {feature: player-stats, event_type: PlayerStatsRecorded|PlayerStatsCorrected}
# Counts domain events consumed by downstream listeners
- name: event.consume # Counter {feature: player-stats, event_type, consumer}
# Measures delay in seconds between event publish time and consumer processing
- name: event.consumer.lag # Histogram (s) {feature: player-stats, event_type, consumer}
```

> **Cross-feature impact:** PlayerStatsRecorded feeds financial-settlement and player-progression. Lag or missing events cause downstream calculation errors.

### Query Performance (O11)

*@source [interfaces.md](interfaces.md)*

| Query                 | p95 Latency SLO | Max Result Size     | Cache TTL |
| --------------------- | --------------- | ------------------- | --------- |
| GetPlayerStatsHistory | ≤ 200ms         | 50 rows (paginated) | 0         |
| GetPlayerStatsWindow  | ≤ 100ms         | aggregated result   | 60s       |

### Workflow Completion (O12)

*@source [workflows.md#RecordStatsWorkflow](workflows.md#RecordStatsWorkflow)*

```yaml
# Counts end-to-end RecordStatsWorkflow executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end RecordStatsWorkflow executions, grouped by outcome"
  attributes:
    {
      feature: player-stats,
      workflow: RecordStatsWorkflow,
      result: completed|failed,
    }

# Measures total wall-clock time for RecordStatsWorkflow execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  description: "Measures total wall-clock time for RecordStatsWorkflow execution"
  attributes: { feature: player-stats, workflow: RecordStatsWorkflow }

# Counts RecordStatsWorkflow failures, tagged by the step where failure occurred
- name: workflow.failed
  instrument: Counter
  unit: "{failure}"
  description: "Counts RecordStatsWorkflow failures, tagged by the step where failure occurred"
  attributes:
    {
      feature: player-stats,
      workflow: RecordStatsWorkflow,
      failed_at_step: authorize|validate|persist|emit_event,
    }
```

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

#### Stats Ingestion

*@source [SPEC.md](SPEC.md) capabilities*

```yaml
- name: business.stats_recorded
  instrument: Counter
  unit: "{snapshot}"
  attributes:
    {
      feature: player-stats,
      capability: RecordPlayerStats,
      source_type: MANUAL|IMPORT|API,
    }
  business_question: "How many stat records are ingested daily by source?"
  healthy_range: "> 0 on days with play sessions"
  alert: 0 records for 3 consecutive days → P2

- name: business.correction_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes: { feature: player-stats, capability: RecordPlayerStats }
  formula: "CORRECTED events / total events over 7d"
  business_question: "How often are stats being corrected after initial entry?"
  healthy_range: "< 10% (lower is better)"
  alert: rate > 25% → P2 (data quality issue at ingestion)

- name: business.ingestion_latency
  instrument: Histogram
  unit: "s"
  attributes: { feature: player-stats, capability: RecordPlayerStats }
  formula: "time from play session end to stat record creation"
  business_question: "How quickly do stats become available after play?"
  healthy_range: "p50 < 1h, p95 < 24h"

- name: business.active_players_with_stats
  instrument: Gauge
  unit: "{player}"
  attributes: { feature: player-stats }
  business_question: "How many players have recent stat records?"
  healthy_range: "stable or growing"
```

---

## Metric Summary

| Rule                              | Metric Count                          | Layer                  | Severity |
| --------------------------------- | ------------------------------------- | ---------------------- | -------- |
| O1: PlayerStatsRecord transitions | 2 (transition + invalid)              | Domain Fidelity        | P0–P1    |
| O3: Invariant monitors            | 1 (Gauge, 2 invariants)               | Domain Fidelity        | P0–P1    |
| O4: RecordPlayerStats execution   | 2 (invocation + duration)             | Operational            | P1       |
| O5: Rule violations (R1–R8)       | 1 (Counter, 8 rule_id attrs)          | Domain Fidelity        | P2       |
| O6: Calculation drift (C1–C2)     | 1 (Histogram, 2 calculation_id attrs) | Domain Fidelity        | P1       |
| O7: Postconditions                | 1 (Counter, 3 postcondition_id attrs) | Domain Fidelity        | P1       |
| O8: Endpoint SLOs                 | 1 (OTel HTTP semconv)                 | Operational            | P1       |
| O10: Event flow                   | 3 (emit + consume + lag)              | Operational            | P1       |
| O11: Query performance            | 1                                     | Operational            | P2       |
| O12: Workflow completion          | 3                                     | Operational            | P1       |
| O13: Business KPIs                | 4                                     | Business Effectiveness | P2       |
| **Total**                         | **~20 OTel instruments**              |                        |          |
