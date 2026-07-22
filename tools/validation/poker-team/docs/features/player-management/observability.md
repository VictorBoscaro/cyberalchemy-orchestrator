---
id: player-management
feature: player-management
type: observability
title: "Player Management — Observability Spec"
summary: Observability contract for player lifecycle writes, coach assignment constraints, and player projection reads.
derived-from: OBSERVABILITY.md rules O4–O5, O7–O8, O11, O13
status: draft
pillar: operations
domain: player-management-observability
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

# Player Management — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: player-management`.
> No state machines, events, or workflows — CRUD-dominant feature with constraint-based rules.

---

## Domain Fidelity Metrics

### Operation Metrics (O4–O7)

#### CreatePlayer

**Base metrics (O4):**

*@source [operations.md#CreatePlayer](operations.md#CreatePlayer)*

```yaml
# Counts each call to CreatePlayer, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to CreatePlayer, grouped by success or error outcome"
  attributes:
    {
      feature: player-management,
      operation: CreatePlayer,
      result: success|error,
    }

# Measures execution time of CreatePlayer in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of CreatePlayer in seconds"
  attributes: { feature: player-management, operation: CreatePlayer }
```

**Rule violation rates (O5):**

| Rule | Expression                                        | Instrument                                                          | Alert Threshold                                     |
| ---- | ------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| R1   | `len(trim(name)) > 0`                             | `rule.violation` Counter `{rule_id="R1", operation="CreatePlayer"}` | rate > 5% → P2 (form validation gap)                |
| R2   | `len(trim(email)) > 0`                            | `rule.violation` Counter `{rule_id="R2", operation="CreatePlayer"}` | rate > 5% → P2                                      |
| R3   | `len(trim(currentLimit)) > 0`                     | `rule.violation` Counter `{rule_id="R3", operation="CreatePlayer"}` | rate > 5% → P2                                      |
| R4   | `count(Player where emailKey = canonical) = 0`    | `rule.violation` Counter `{rule_id="R4", operation="CreatePlayer"}` | track volume — high rate = re-registration attempts |
| R5   | `initialBankroll is null or initialBankroll >= 0` | `rule.violation` Counter `{rule_id="R5", operation="CreatePlayer"}` | rate > 1% → P2                                      |
| R6   | `currentLimit in {NL20,NL40,NL60,NL80,NL100}`     | `rule.violation` Counter `{rule_id="R6", operation="CreatePlayer"}` | any > 0 → P2 (API contract)                         |

**Postcondition verification (O7):**

| Postcondition                    | Instrument                                                                    | Alert                    |
| -------------------------------- | ----------------------------------------------------------------------------- | ------------------------ |
| Player record persisted          | `postcondition.check` Counter `{postcondition_id="player_persisted", result}` | any result=violated → P1 |
| Player returned by GetAllPlayers | `postcondition.check` Counter `{postcondition_id="player_queryable", result}` | any result=violated → P1 |

#### CreateCoach

**Base metrics (O4):**

*@source [operations.md#CreateCoach](operations.md#CreateCoach)*

```yaml
# Counts each call to CreateCoach, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to CreateCoach, grouped by success or error outcome"
  attributes:
    {
      feature: player-management,
      operation: CreateCoach,
      result: success|error,
    }

# Measures execution time of CreateCoach in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of CreateCoach in seconds"
  attributes: { feature: player-management, operation: CreateCoach }
```

**Rule violation rates (O5):**

| Rule | Expression                                             | Instrument                                                         | Alert Threshold             |
| ---- | ------------------------------------------------------ | ------------------------------------------------------------------ | --------------------------- |
| R4   | `count(Coach where principalId and status=ACTIVE) = 0` | `rule.violation` Counter `{rule_id="R4", operation="CreateCoach"}` | track (duplicate principal) |

#### AssignCoach

**Base metrics (O4):**

*@source [operations.md#AssignCoach](operations.md#AssignCoach)*

```yaml
# Counts each call to AssignCoach, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to AssignCoach, grouped by success or error outcome"
  attributes:
    {
      feature: player-management,
      operation: AssignCoach,
      result: success|error,
    }

# Measures execution time of AssignCoach in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of AssignCoach in seconds"
  attributes: { feature: player-management, operation: AssignCoach }
```

**Rule violation rates (O5):**

| Rule | Expression                                | Instrument                                                         | Alert Threshold                          |
| ---- | ----------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------- |
| R2   | Coach must be ACTIVE                      | `rule.violation` Counter `{rule_id="R2", operation="AssignCoach"}` | any > 0 → P2 (inactive coach assignment) |
| R4   | Player must not already have active coach | `rule.violation` Counter `{rule_id="R4", operation="AssignCoach"}` | track volume                             |

#### UnassignCoach

**Base metrics (O4):**

*@source [operations.md#UnassignCoach](operations.md#UnassignCoach)*

```yaml
# Counts each call to UnassignCoach, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to UnassignCoach, grouped by success or error outcome"
  attributes:
    {
      feature: player-management,
      operation: UnassignCoach,
      result: success|error,
    }

# Measures execution time of UnassignCoach in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of UnassignCoach in seconds"
  attributes: { feature: player-management, operation: UnassignCoach }
```

---

## Operational Health Metrics

### Endpoint SLOs (O8)

*@source [interfaces.md](interfaces.md)*

| Endpoint                              | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| ------------------------------------- | ------ | ---------------- | --------------- | ------------------- |
| `/players`                            | POST   | ≥ 99.9%          | ≤ 500ms         | ~10 req/day         |
| `/players`                            | GET    | ≥ 99.9%          | ≤ 300ms         | ~200 req/day        |
| `/players/overview`                   | GET    | ≥ 99.9%          | ≤ 500ms         | ~100 req/day        |
| `/coaches`                            | POST   | ≥ 99.9%          | ≤ 300ms         | ~2 req/day          |
| `/coaches`                            | GET    | ≥ 99.9%          | ≤ 200ms         | ~50 req/day         |
| `/coaches/:coachId/players/:playerId` | POST   | ≥ 99.9%          | ≤ 300ms         | ~5 req/day          |
| `/coaches/:coachId/players/:playerId` | DELETE | ≥ 99.9%          | ≤ 300ms         | ~2 req/day          |
| `/coaches/:coachId/players`           | GET    | ≥ 99.9%          | ≤ 300ms         | ~50 req/day         |

*@source [interfaces.md](interfaces.md)*

```yaml
# Measures HTTP request latency per endpoint using OTel semantic conventions
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: GET|POST|DELETE,
      url.path: /players*|/coaches*,
      http.response.status_code: int,
      feature: player-management,
    }
```

### Query Performance (O11)

*@source [interfaces.md](interfaces.md)*

| Query              | p95 Latency SLO | Max Result Size       | Cache TTL |
| ------------------ | --------------- | --------------------- | --------- |
| GetAllPlayers      | ≤ 200ms         | all rows              | 0         |
| GetPlayersOverview | ≤ 300ms         | all rows (aggregated) | 60s       |
| GetAllCoaches      | ≤ 100ms         | all rows              | 0         |
| GetCoachPlayers    | ≤ 200ms         | filtered rows         | 0         |

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

*@source [SPEC.md](SPEC.md) capabilities*

```yaml
- name: business.players_created
  instrument: Counter
  unit: "{player}"
  attributes: { feature: player-management, capability: CreatePlayer }
  business_question: "How many new players are being added?"
  healthy_range: "> 0 per week (growth indicator)"

- name: business.active_coaches
  instrument: Gauge
  unit: "{coach}"
  attributes: { feature: player-management }
  business_question: "How many coaches are currently active?"
  healthy_range: "> 0"

- name: business.coach_assignment_ratio
  instrument: Gauge
  unit: "1" # ratio
  attributes: { feature: player-management }
  formula: "players with active coach / total players"
  business_question: "What % of players have a coach assigned?"
  healthy_range: "≥ 80% (every active player should have a coach)"
  alert: ratio < 50% → P2 (players unmanaged)

- name: business.duplicate_email_attempts
  instrument: Counter
  unit: "{attempt}"
  attributes: { feature: player-management, capability: CreatePlayer }
  business_question: "How many duplicate player registrations are attempted?"
  purpose: "validates R4 uniqueness — high volume may indicate process issue"
```

---

## Metric Summary

| Rule                                                | Metric Count                          | Layer                  | Severity |
| --------------------------------------------------- | ------------------------------------- | ---------------------- | -------- |
| O4: Operation execution (4 operations)              | 8 (4 invocation + 4 duration)         | Operational            | P1       |
| O5: Rule violations (Create 6 + Coach 1 + Assign 2) | 1 (Counter, 9 rule_id attrs)          | Domain Fidelity        | P2       |
| O7: Postconditions (CreatePlayer)                   | 1 (Counter, 2 postcondition_id attrs) | Domain Fidelity        | P1       |
| O8: Endpoint SLOs                                   | 1 (OTel HTTP semconv)                 | Operational            | P1       |
| O11: Query performance                              | 1                                     | Operational            | P2       |
| O13: Business KPIs                                  | 4                                     | Business Effectiveness | P2       |
| **Total**                                           | **~16 OTel instruments**              |                        |          |
