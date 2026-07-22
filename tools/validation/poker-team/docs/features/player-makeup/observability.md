---
id: player-makeup
feature: player-makeup
type: observability
title: "Player Makeup — Observability Spec"
summary: Observability contract for makeup debt lifecycle, policy enforcement, and finance integrity controls.
derived-from: OBSERVABILITY.md rules O1–O16
status: draft
pillar: finance
domain: player-makeup-observability
audience:
  - developers
  - finance
priority: p1
lang: en
owners:
  - finance-core
  - backend-core
updatedAt: 2026-04-17
dependencies:
  - SPEC.md
  - operations.md
includes: []
---

# Player Makeup — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: player-makeup`.
> Finance-pillar features have mandatory integrity monitors (O15–O16).

---

## Domain Fidelity Metrics

### State Machine Monitors (O1–O3)

#### MakeupDebtState State Machine

**Transition counters (O1):**

| From    | To      | Event          | Attributes                                                                    |
| ------- | ------- | -------------- | ----------------------------------------------------------------------------- |
| Settled | InDebt  | MakeupAdjusted | `{entity: MakeupDebtState, from: Settled, to: InDebt, event: MakeupAdjusted}` |
| InDebt  | InDebt  | MakeupAdjusted | `{..., from: InDebt, to: InDebt, event: MakeupAdjusted}`                      |
| InDebt  | Settled | MakeupAdjusted | `{..., from: InDebt, to: Settled, event: MakeupAdjusted}`                     |
| InDebt  | Settled | MakeupApplied  | `{..., from: InDebt, to: Settled, event: MakeupApplied}`                      |

*@source [states.md#MakeupDebtState](states.md#MakeupDebtState)*

```yaml
# @rule O1: Transition Counter
# Counts each valid state transition in the MakeupDebt state lifecycle
- name: state.transition
  instrument: Counter
  unit: "{transition}"
  description: "Counts each valid state transition in the MakeupDebt state lifecycle"
  attributes: [feature, entity, from, to, event]
```

**Invalid transition counter:**

| From    | Attempted Event                    | Reason                                  |
| ------- | ---------------------------------- | --------------------------------------- |
| Settled | MakeupApplied                      | Cannot apply makeup when no debt exists |
| Settled | MakeupAdjusted (result == 0)       | No-op — delta is zero                   |
| InDebt  | MakeupApplied (applied < previous) | Partial application does not settle     |

```yaml
# Counts rejected state transitions — any increment indicates a domain logic bug
- name: state.invalid_transition
  instrument: Counter
  unit: "{attempt}"
  description: "Counts rejected state transitions — any increment indicates a domain logic bug"
  attributes: [feature, entity, from, attempted_event, error_code]
  alert: any increment → P1
```

**State distribution (O2):**

```yaml
# @rule O2: State Distribution
# Tracks how many entities are currently in each MakeupDebt state
- name: state.population
  instrument: UpDownCounter
  unit: "{entity}"
  attributes:
    { feature: player-makeup, entity: MakeupDebtState, state: Settled|InDebt }
  monitors:
    - debt_ratio: "InDebt / (Settled + InDebt) over 30d"
      alert: ratio > 80% → P2 (most players carrying debt — systemic issue?)
    - settling_trend: "rate of InDebt→Settled transitions per week"
      purpose: "debt is being resolved at healthy pace"
```

**Invariant monitors (O3):**

| ID  | Invariant                              | Check                                        | Alert              |
| --- | -------------------------------------- | -------------------------------------------- | ------------------ |
| I1  | Debt is never negative                 | `makeup >= 0` after every adjustment         | any violation → P0 |
| I2  | No adjustment event when delta is zero | `delta == 0 => no MAKEUP_ADJUSTMENT created` | any violation → P1 |

```yaml
# Detects domain invariant violations that should never occur in correct code
- name: invariant.violation
  instrument: Gauge
  unit: "{entity}"
  description: "Detects domain invariant violations that should never occur in correct code"
  attributes:
    {
      feature: player-makeup,
      entity: MakeupDebtState,
      invariant_id: I1|I2,
      expression: string,
    }
  frequency: hourly
  alert: any value > 0 → P0
```

### Operation Metrics (O4–O7)

#### AdjustPlayerMakeup

**Base metrics (O4):**

*@source [operations.md#AdjustPlayerMakeup](operations.md#AdjustPlayerMakeup)*

```yaml
# Counts each call to AdjustPlayerMakeup, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to AdjustPlayerMakeup, grouped by success or error outcome"
  attributes:
    {
      feature: player-makeup,
      operation: AdjustPlayerMakeup,
      result: success|error,
    }

# Measures execution time of AdjustPlayerMakeup in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of AdjustPlayerMakeup in seconds"
  attributes: { feature: player-makeup, operation: AdjustPlayerMakeup }
```

**Rule violation rates (O5):**

| Rule | Expression                             | Instrument                                | Alert Threshold                          |
| ---- | -------------------------------------- | ----------------------------------------- | ---------------------------------------- |
| R1   | `exists(Player.id == playerId)`        | `rule.violation` Counter `{rule_id="R1"}` | rate > 5% → P2 (bad caller data)         |
| R2   | `isFinite(amount) and amount >= 0`     | `rule.violation` Counter `{rule_id="R2"}` | rate > 1% → P2 (upstream validation gap) |
| R3   | `operation in {increase,decrease,set}` | `rule.violation` Counter `{rule_id="R3"}` | rate > 0 → P2 (API contract violation)   |

**Calculation drift (O6):**

| Calc | Formula                                              | Instrument                                            | Frequency             | Alert                            |
| ---- | ---------------------------------------------------- | ----------------------------------------------------- | --------------------- | -------------------------------- |
| C1   | `normalized = floor(amount + 0.5)`                   | `calculation.drift` Histogram `{calculation_id="C1"}` | After each adjustment | drift > 0 → P0 (rounding broken) |
| C2   | `current = previous + normalized` (increase)         | `calculation.drift` Histogram `{calculation_id="C2"}` | After each adjustment | drift > 0 → P0                   |
| C3   | `current = max(0, previous - normalized)` (decrease) | `calculation.drift` Histogram `{calculation_id="C3"}` | After each adjustment | drift > 0 → P0                   |
| C4   | `current = max(0, normalized)` (set)                 | `calculation.drift` Histogram `{calculation_id="C4"}` | After each adjustment | drift > 0 → P0                   |
| C5   | `delta = current - previous`                         | `calculation.drift` Histogram `{calculation_id="C5"}` | After each adjustment | drift > 0 → P0                   |

> C1–C5 drift is **P0** because incorrect rounding or arithmetic directly causes financial discrepancy.

**Postcondition verification (O7):**

| Postcondition                               | Instrument                                                                             | Alert                    |
| ------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------ |
| Makeup persisted with non-negative value    | `postcondition.check` Counter `{postcondition_id="makeup_non_negative", result}`       | any result=violated → P0 |
| MAKEUP_ADJUSTMENT created only when delta≠0 | `postcondition.check` Counter `{postcondition_id="adjustment_event_on_delta", result}` | any result=violated → P1 |

#### SetPlayerMakeupPolicy

**Base metrics (O4):**

*@source [operations.md#SetPlayerMakeupPolicy](operations.md#SetPlayerMakeupPolicy)*

```yaml
# Counts each call to SetPlayerMakeupPolicy, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to SetPlayerMakeupPolicy, grouped by success or error outcome"
  attributes:
    {
      feature: player-makeup,
      operation: SetPlayerMakeupPolicy,
      result: success|error,
    }

# Measures execution time of SetPlayerMakeupPolicy in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of SetPlayerMakeupPolicy in seconds"
  attributes: { feature: player-makeup, operation: SetPlayerMakeupPolicy }
```

**Rule violation rates (O5):**

| Rule | Expression                         | Instrument                                                                   | Alert Threshold                             |
| ---- | ---------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------- |
| R1   | `exists(Player.id == playerId)`    | `rule.violation` Counter `{rule_id="R1", operation="SetPlayerMakeupPolicy"}` | rate > 5% → P2                              |
| R2   | validate policy shape              | `rule.violation` Counter `{rule_id="R2", operation="SetPlayerMakeupPolicy"}` | rate > 1% → P2                              |
| R3   | `clamp(playerRakebackShare, 0, 1)` | `rule.violation` Counter `{rule_id="R3", operation="SetPlayerMakeupPolicy"}` | informational (clamping is auto-corrective) |

---

## Operational Health Metrics

### Endpoint SLOs (O8)

*@source [interfaces.md](interfaces.md)*

| Endpoint                      | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| ----------------------------- | ------ | ---------------- | --------------- | ------------------- |
| `/players/:id/makeup`         | GET    | ≥ 99.9%          | ≤ 200ms         | ~100 req/day        |
| `/players/:id/makeup`         | PATCH  | ≥ 99.9%          | ≤ 500ms         | ~20 req/day         |
| `/players/:id/makeup/history` | GET    | ≥ 99.9%          | ≤ 300ms         | ~50 req/day         |
| `/players/makeup/policy`      | GET    | ≥ 99.9%          | ≤ 100ms         | ~30 req/day         |
| `/players/:id/makeup/policy`  | PATCH  | ≥ 99.9%          | ≤ 500ms         | ~5 req/day          |

*@source [interfaces.md](interfaces.md)*

```yaml
# Uses OTel HTTP semantic conventions with custom `feature` attribute:
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: GET|PATCH,
      url.path: /players/*/makeup*,
      http.response.status_code: int,
      feature: player-makeup,
    }
```

### Idempotency Monitors (O9)

| Concern                   | Constraint                                       | Instrument                                                                                        | Alert            |
| ------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------- | ---------------- |
| MakeupApplied duplication | `unique(playerId, date)` per MakeupApplied event | `idempotency.violation` Gauge `{operation: SettlementMakeupApplication, rule_id: dedup_identity}` | **any > 0 → P0** |

*@source [events.md#MakeupApplied](events.md#MakeupApplied) — Idempotent per (playerId, date)*

```yaml
# @rule O9: Idempotency Monitor
# Detects duplicate operations that violate idempotency constraints
- name: idempotency.violation
  instrument: Gauge
  unit: "{violation}"
  description: "Detects duplicate operations that violate idempotency constraints"
  attributes:
    {
      feature: player-makeup,
      operation: SettlementMakeupApplication,
      rule_id: dedup_identity,
    }
  check: "periodic scan — group MakeupApplied events by (playerId, date), flag count > 1"
  frequency: every 15 minutes
  alert:
    condition: value > 0
    severity: P0
    runbook: |
      1. Query makeup events WHERE type=MakeupApplied GROUP BY (playerId, date) HAVING count > 1
      2. Identify which settlement execution created the duplicate
      3. Compare amounts — if identical, safe to soft-delete duplicate
      4. If amounts differ, escalate to finance lead

# Counts how many times dedup logic successfully prevented a duplicate
- name: idempotency.dedup
  instrument: Counter
  unit: "{dedup}"
  attributes: { feature: player-makeup, operation: SettlementMakeupApplication }
  purpose: "tracks how often dedup logic prevents a duplicate MakeupApplied"
```

### Event Flow (O10)

| Event          | Producer                                | Consumers            | Lag SLO |
| -------------- | --------------------------------------- | -------------------- | ------- |
| MakeupAdjusted | AdjustPlayerMakeup                      | finance audit        | ≤ 5s    |
| MakeupApplied  | financial-settlement.GenerateSettlement | makeup history query | ≤ 5s    |

*@source [events.md](events.md)*

```yaml
# Counts domain events published by this feature
- name: event.emit # Counter {feature: player-makeup, event_type: MakeupAdjusted|MakeupApplied}
# Counts domain events consumed by downstream listeners
- name: event.consume # Counter {feature: player-makeup, event_type, consumer}
# Measures delay in seconds between event publish time and consumer processing
- name: event.consumer.lag # Histogram (s) {feature: player-makeup, event_type, consumer}
```

### Query Performance (O11)

*@source [interfaces.md](interfaces.md)*

| Query                  | p95 Latency SLO | Max Result Size     | Cache TTL        |
| ---------------------- | --------------- | ------------------- | ---------------- |
| GetPlayerMakeup        | ≤ 50ms          | 1 row               | 0 (always fresh) |
| GetPlayerMakeupHistory | ≤ 200ms         | 50 rows (paginated) | 0                |
| GetMakeupPolicy        | ≤ 50ms          | 1 row               | 300s             |

### Workflow Completion (O12)

*@source [workflows.md#MakeupAdjustmentWorkflow](workflows.md#MakeupAdjustmentWorkflow)*

```yaml
# Counts end-to-end MakeupAdjustmentWorkflow executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end MakeupAdjustmentWorkflow executions, grouped by outcome"
  attributes:
    {
      feature: player-makeup,
      workflow: MakeupAdjustmentWorkflow,
      result: completed|failed,
    }

# Measures total wall-clock time for MakeupAdjustmentWorkflow execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  description: "Measures total wall-clock time for MakeupAdjustmentWorkflow execution"
  attributes: { feature: player-makeup, workflow: MakeupAdjustmentWorkflow }

# Counts MakeupAdjustmentWorkflow failures, tagged by the step where failure occurred
- name: workflow.failed
  instrument: Counter
  unit: "{failure}"
  description: "Counts MakeupAdjustmentWorkflow failures, tagged by the step where failure occurred"
  attributes:
    {
      feature: player-makeup,
      workflow: MakeupAdjustmentWorkflow,
      failed_at_step: authorization|validation|domain_execution|audit_persistence,
    }
```

*@source [workflows.md#SettlementMakeupApplicationContract](workflows.md#SettlementMakeupApplicationContract)*

```yaml
# Counts end-to-end SettlementMakeupApplication executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end SettlementMakeupApplication executions, grouped by outcome"
  attributes:
    {
      feature: player-makeup,
      workflow: SettlementMakeupApplication,
      result: completed|failed,
    }

# Measures total wall-clock time for SettlementMakeupApplication execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  description: "Measures total wall-clock time for SettlementMakeupApplication execution"
  attributes: { feature: player-makeup, workflow: SettlementMakeupApplication }
```

**Workflow invariant monitors:**

| ID  | Invariant                               | Check                            | Alert              |
| --- | --------------------------------------- | -------------------------------- | ------------------ |
| I1  | Debt is never negative after adjustment | `newMakeup >= 0`                 | any violation → P0 |
| I2  | No event when delta is zero             | `delta == 0 => no event emitted` | any violation → P1 |

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

#### Makeup Adjustments

*@source [SPEC.md](SPEC.md) capabilities*

```yaml
- name: business.adjustments_executed
  instrument: Counter
  unit: "{adjustment}"
  attributes:
    {
      feature: player-makeup,
      capability: AdjustPlayerMakeup,
      adjustment_operation: increase|decrease|set,
    }
  business_question: "How many makeup adjustments happen daily by type?"
  healthy_range: "> 0 on business days"

- name: business.total_makeup_outstanding
  instrument: Gauge
  unit: "{currency_minor}" # BRL cents
  attributes: { feature: player-makeup }
  business_question: "What is the total makeup debt across all players?"
  healthy_range: "trending stable or down"
  alert: sudden increase > 50% week-over-week → P2 (mass debt event?)

- name: business.avg_debt_per_player
  instrument: Gauge
  unit: "{currency_minor}" # BRL cents
  attributes: { feature: player-makeup }
  business_question: "What is the average makeup debt per indebted player?"
  healthy_range: "within historical range"

- name: business.players_in_debt
  instrument: Gauge
  unit: "{player}"
  attributes: { feature: player-makeup }
  business_question: "How many players currently carry makeup debt?"
  healthy_range: "stable or declining"
```

#### Makeup Policy

```yaml
- name: business.policy_changes
  instrument: Counter
  unit: "{change}"
  attributes: { feature: player-makeup, capability: SetPlayerMakeupPolicy }
  business_question: "How often are makeup policies being changed?"
  purpose: "frequent changes may indicate unclear policy"
```

---

## Financial Integrity Metrics (O15–O16)

### Transaction Integrity (O15)

*@source [operations.md#AdjustPlayerMakeup](operations.md#AdjustPlayerMakeup), [OBSERVABILITY.md rule O15](../../../domainspec/OBSERVABILITY.md)*

```yaml
# Mandatory for pillar: finance

# Detects discrepancies between computed (from event replay) and stored financial values
- name: reconciliation.mismatch
  instrument: Gauge
  unit: "{currency_minor}" # BRL cents
  description: "Detects discrepancies between computed (from event replay) and stored financial values"
  attributes: { feature: player-makeup, entity: Player }
  check: |
    For each player with makeup adjustments:
      computed_makeup = replay all MAKEUP_ADJUSTMENT + MAKEUP_APPLIED transactions
      stored_makeup = Player.makeup current value
      mismatch = |computed_makeup - stored_makeup|
  frequency: hourly
  alert: mismatch > 0 → P0
  runbook: |
    1. Identify affected player(s)
    2. Replay transaction log: sum(MAKEUP_ADJUSTMENT.delta) + sum(MAKEUP_APPLIED.amount)
    3. Compare with current stored makeup value
    4. If stored > computed: player debt is overstated (financial harm to player)
    5. If stored < computed: team is owed more than recorded (financial loss)
    6. Correct stored value and create reconciliation adjustment event

# Detects duplicate financial transactions that violate uniqueness constraints
- name: transaction.duplicate
  instrument: Counter
  unit: "{duplicate}"
  description: "Detects duplicate financial transactions that violate uniqueness constraints"
  attributes:
    {
      feature: player-makeup,
      transaction_type: MAKEUP_ADJUSTMENT|MAKEUP_APPLIED,
    }
  check: |
    For MAKEUP_APPLIED:
      SELECT player_id, date, COUNT(*)
      FROM makeup_events WHERE type = 'MAKEUP_APPLIED'
      GROUP BY player_id, date
      HAVING COUNT(*) > 1
  frequency: every 15 minutes
  alert: any increment → P0

# Estimates total monetary exposure from detected duplicate transactions
- name: exposure.amount
  instrument: Gauge
  unit: "{currency_minor}" # BRL cents
  description: "Estimates total monetary exposure from detected duplicate transactions"
  attributes: { feature: player-makeup }
  check: "sum of potentially duplicated MakeupApplied amounts"
  alert: exposure > 0 → P0 with R$ amount in alert body
```

### Makeup Adjustment Cycle Metrics (O16)

*@source [workflows.md](workflows.md), [OBSERVABILITY.md rule O16](../../../domainspec/OBSERVABILITY.md)*

```yaml
- name: makeup.cycle.adjustments # Counter {feature: player-makeup}
- name: makeup.cycle.total_increase # Counter {currency_minor} {feature: player-makeup}
- name: makeup.cycle.total_decrease # Counter {currency_minor} {feature: player-makeup}
- name: makeup.cycle.net_change # Gauge {currency_minor} {feature: player-makeup}
- name: makeup.cycle.error_rate # Gauge (ratio) {feature: player-makeup}

# Drift detection — verify rounding correctness:
- name: makeup.recalculation.drift
  instrument: Gauge
  unit: "{currency_minor}"
  attributes: { feature: player-makeup, calculation_id: C1|C2|C3|C4|C5 }
  check: |
    For recent adjustments:
      recompute C1 (half-up rounding) from raw input amount
      recompute C2/C3/C4 (arithmetic) from previous + normalized
      recompute C5 (delta) from current - previous
      compare with stored adjustment results
  frequency: after each adjustment batch
  alert: drift > 0 → P0 (rounding or arithmetic is broken)
```

---

## Metric Summary

| Rule                                              | Metric Count                                     | Layer                  | Severity |
| ------------------------------------------------- | ------------------------------------------------ | ---------------------- | -------- |
| O1: MakeupDebtState transitions                   | 2 (transition + invalid)                         | Domain Fidelity        | P0–P1    |
| O2: State distribution                            | 1 (UpDownCounter, 2 states)                      | Domain Fidelity        | P2       |
| O3: Invariant monitors                            | 1 (Gauge, 2 invariants)                          | Domain Fidelity        | P0–P1    |
| O4: Operation execution (Adjust + SetPolicy)      | 4 (2 invocation + 2 duration)                    | Operational            | P1       |
| O5: Rule violations (Adjust R1–R3 + Policy R1–R3) | 1 (Counter, 6 rule_id attrs)                     | Domain Fidelity        | P2       |
| O6: Calculation drift (C1–C5)                     | 1 (Histogram, 5 calculation_id attrs)            | Domain Fidelity        | P0       |
| O7: Postconditions                                | 1 (Counter, 2 postcondition_id attrs)            | Domain Fidelity        | P0–P1    |
| O8: Endpoint SLOs                                 | 1 (OTel HTTP semconv)                            | Operational            | P1       |
| O9: Idempotency (MakeupApplied)                   | 2 (violation + dedup)                            | Financial Integrity    | P0       |
| O10: Event flow                                   | 3 (emit + consume + lag)                         | Operational            | P1       |
| O11: Query performance                            | 1                                                | Operational            | P2       |
| O12: Workflow completion                          | 5 (2 workflows × invocation+duration + 1 failed) | Operational            | P1       |
| O13: Business KPIs                                | 5                                                | Business Effectiveness | P2       |
| O15: Transaction integrity                        | 3                                                | Financial Integrity    | P0       |
| O16: Makeup cycle                                 | 6                                                | Financial Integrity    | P0       |
| **Total**                                         | **~37 OTel instruments**                         |                        |          |
