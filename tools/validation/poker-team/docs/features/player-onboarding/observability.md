---
id: player-onboarding
feature: player-onboarding
type: observability
title: "Player Onboarding — Observability Spec"
summary: Observability contract for candidate onboarding lifecycle, review transitions, and onboarding flow reliability.
derived-from: OBSERVABILITY.md rules O1–O14
status: draft
pillar: operations
domain: player-onboarding-observability
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - operations-core
  - web-core
updatedAt: 2026-04-17
dependencies:
  - SPEC.md
  - operations.md
includes: []
---

# Player Onboarding — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: player-onboarding`.

---

## Domain Fidelity Metrics

### State Machine Monitors (O1–O3)

#### CandidateApplication State Machine

**Transition counters (O1):**

| From         | To           | Event                               | Attributes                                                                                    |
| ------------ | ------------ | ----------------------------------- | --------------------------------------------------------------------------------------------- |
| [new]        | SUBMITTED    | SubmitCandidateApplication          | `{entity: CandidateApplication, from: new, to: SUBMITTED, event: SubmitCandidateApplication}` |
| SUBMITTED    | UNDER_REVIEW | StartManualReview                   | `{..., from: SUBMITTED, to: UNDER_REVIEW, event: StartManualReview}`                          |
| SUBMITTED    | APPROVED     | ReviewCandidateApplication(APPROVE) | `{..., from: SUBMITTED, to: APPROVED, event: ReviewApprove}`                                  |
| SUBMITTED    | REJECTED     | ReviewCandidateApplication(REJECT)  | `{..., from: SUBMITTED, to: REJECTED, event: ReviewReject}`                                   |
| UNDER_REVIEW | APPROVED     | ReviewCandidateApplication(APPROVE) | `{..., from: UNDER_REVIEW, to: APPROVED, event: ReviewApprove}`                               |
| UNDER_REVIEW | REJECTED     | ReviewCandidateApplication(REJECT)  | `{..., from: UNDER_REVIEW, to: REJECTED, event: ReviewReject}`                                |

*@source [states.md#CandidateApplicationLifecycle](states.md#CandidateApplicationLifecycle)*

```yaml
# @rule O1: Transition Counter
# Counts each valid state transition in the CandidateApplication lifecycle
- name: state.transition
  instrument: Counter
  unit: "{transition}"
  description: "Counts each valid state transition in the CandidateApplication lifecycle"
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
  alert: any increment → P0
```

**State distribution (O2):**

```yaml
# @rule O2: State Distribution
# Tracks how many entities are currently in each CandidateApplication state
- name: state.population
  instrument: UpDownCounter
  unit: "{entity}"
  description: "Tracks how many entities are currently in each CandidateApplication state"
  attributes:
    {
      feature: player-onboarding,
      entity: CandidateApplication,
      state: SUBMITTED|UNDER_REVIEW|APPROVED|REJECTED,
    }
  monitors:
    - accumulation: "SUBMITTED count growing without APPROVED/REJECTED → review backlog"
      alert: SUBMITTED > 50 AND no review in 48h → P2
    - terminal_ratio: "REJECTED / (APPROVED + REJECTED) over 30d"
      alert: rejection rate > 80% → P2 (funnel quality issue or overly strict criteria)
```

**Invariant monitors (O3):**

| ID  | Invariant                                           | Check                                                                            | Alert              |
| --- | --------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------ |
| I1  | Closed apps cannot transition back to active states | Periodic: query apps where status IN (APPROVED, REJECTED) AND updated_at changed | any violation → P0 |
| I2  | Every submitted app includes rules acceptance       | Periodic: count apps where status != 'new' AND ruleAcceptance.acceptedAt IS NULL | any count > 0 → P0 |
| I3  | Every submitted app includes LGPD consent           | Periodic: count apps where status != 'new' AND lgpdConsentAccepted != true       | any count > 0 → P0 |

```yaml
# Detects domain invariant violations that should never occur in correct code
- name: invariant.violation
  instrument: Gauge
  unit: "{entity}"
  description: "Detects domain invariant violations that should never occur in correct code"
  attributes:
    {
      feature: player-onboarding,
      entity: CandidateApplication,
      invariant_id: I1|I2|I3,
      expression: string,
    }
  frequency: hourly
  alert: any value > 0 → P0
```

### Operation Metrics (O4–O7)

#### SubmitCandidateApplication

**Base metrics (O4):**

*@source [operations.md#SubmitCandidateApplication](operations.md#SubmitCandidateApplication)*

```yaml
# Counts each call to SubmitCandidateApplication, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to SubmitCandidateApplication, grouped by success or error outcome"
  attributes:
    {
      feature: player-onboarding,
      operation: SubmitCandidateApplication,
      result: success|error,
    }

# Measures execution time of SubmitCandidateApplication in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of SubmitCandidateApplication in seconds"
  attributes:
    { feature: player-onboarding, operation: SubmitCandidateApplication }
```

**Rule violation rates (O5):**

| Rule | Expression                                                         | Instrument                                | Alert Threshold                              |
| ---- | ------------------------------------------------------------------ | ----------------------------------------- | -------------------------------------------- |
| R1   | `acceptedRegulationVersion != '' and acceptedRegulationAt != null` | `rule.violation` Counter `{rule_id="R1"}` | rate > 5% → P2 (UI not enforcing acceptance) |
| R2   | `lgpdConsentAccepted = true`                                       | `rule.violation` Counter `{rule_id="R2"}` | rate > 5% → P2 (UI not enforcing consent)    |
| R3   | all required fields present                                        | `rule.violation` Counter `{rule_id="R3"}` | rate > 10% → P2 (form validation gap)        |
| R4   | email format valid                                                 | `rule.violation` Counter `{rule_id="R4"}` | informational                                |
| R5   | no duplicate by WhatsApp or email                                  | `rule.violation` Counter `{rule_id="R5"}` | track volume — high rate = bot/spam          |
| R6   | at least one time window                                           | `rule.violation` Counter `{rule_id="R6"}` | rate > 5% → P2 (form validation gap)         |
| R7   | tracker detail when required                                       | `rule.violation` Counter `{rule_id="R7"}` | informational                                |
| R8   | city/state format                                                  | `rule.violation` Counter `{rule_id="R8"}` | rate > 10% → P2 (UX issue)                   |
| R9   | age >= 18                                                          | `rule.violation` Counter `{rule_id="R9"}` | informational                                |

> **Key insight:** High R1/R2 violation rates indicate the frontend is not properly enforcing mandatory acceptance before submission. High R5 (duplicate) rates may indicate bot traffic or a returning candidate without proper messaging.

**Calculation drift (O6):**

| Calc | Formula                                   | Instrument                                            | Frequency          | Alert                                       |
| ---- | ----------------------------------------- | ----------------------------------------------------- | ------------------ | ------------------------------------------- |
| C1   | `canonicalEmail = lowercase(trim(email))` | `calculation.drift` Histogram `{calculation_id="C1"}` | On each submission | drift > 0 → P1 (email normalization broken) |

**Postcondition verification (O7):**

| Postcondition                       | Instrument                                                                           | Alert                    |
| ----------------------------------- | ------------------------------------------------------------------------------------ | ------------------------ |
| App persisted with SUBMITTED status | `postcondition.check` Counter `{postcondition_id="persisted_submitted", result}`     | any result=violated → P1 |
| ruleAcceptance stored               | `postcondition.check` Counter `{postcondition_id="rule_acceptance_stored", result}`  | any result=violated → P0 |
| App available for screening         | `postcondition.check` Counter `{postcondition_id="available_for_screening", result}` | any result=violated → P1 |

#### ReviewCandidateApplication

**Base metrics (O4):**

*@source [operations.md#ReviewCandidateApplication](operations.md#ReviewCandidateApplication)*

```yaml
# Counts each call to ReviewCandidateApplication, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to ReviewCandidateApplication, grouped by success or error outcome"
  attributes:
    {
      feature: player-onboarding,
      operation: ReviewCandidateApplication,
      result: success|error,
    }

# Measures execution time of ReviewCandidateApplication in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of ReviewCandidateApplication in seconds"
  attributes:
    { feature: player-onboarding, operation: ReviewCandidateApplication }
```

**Decision distribution:**

```yaml
- name: business.review_decision
  instrument: Counter
  unit: "{decision}"
  attributes:
    {
      feature: player-onboarding,
      operation: ReviewCandidateApplication,
      decision: APPROVE|REJECT,
    }
  business_question: "What is the approval vs rejection ratio?"
```

---

## Operational Health Metrics

### Endpoint SLOs (O8)

| Endpoint                             | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| ------------------------------------ | ------ | ---------------- | --------------- | ------------------- |
| `/onboarding/flow`                   | GET    | ≥ 99.9%          | ≤ 200ms         | ~500 req/day        |
| `/onboarding/candidates`             | POST   | ≥ 99.9%          | ≤ 1000ms        | ~20 req/day         |
| `/onboarding/candidates/{id}/review` | PATCH  | ≥ 99.9%          | ≤ 500ms         | ~10 req/day         |

*@source [interfaces.md#external-publiconboardingapi-rest](interfaces.md#external-publiconboardingapi-rest)*

```yaml
# Uses OTel HTTP semantic conventions with custom `feature` attribute:
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: GET|POST|PATCH,
      url.path: /onboarding/*,
      http.response.status_code: int,
      feature: player-onboarding,
    }
```

### Query Performance (O11)

| Query                     | p95 Latency SLO | Max Result Size     | Cache TTL                         |
| ------------------------- | --------------- | ------------------- | --------------------------------- |
| GetOnboardingFlow         | ≤ 100ms         | 1 payload           | 3600s (regulation rarely changes) |
| ListCandidateApplications | ≤ 200ms         | 50 rows (paginated) | 0                                 |

### Workflow Completion (O12)

*@source [workflows.md#CandidateOnboardingFlow](workflows.md#CandidateOnboardingFlow)*

```yaml
# Counts end-to-end CandidateOnboardingFlow executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end CandidateOnboardingFlow executions, grouped by outcome"
  attributes:
    {
      feature: player-onboarding,
      workflow: CandidateOnboardingFlow,
      result: completed|abandoned,
    }

# Measures total wall-clock time for CandidateOnboardingFlow execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  description: "Time from rules reading to submission"
  attributes: { feature: player-onboarding, workflow: CandidateOnboardingFlow }

- name: workflow.step.duration
  instrument: Histogram
  unit: "s"
  attributes:
    {
      feature: player-onboarding,
      workflow: CandidateOnboardingFlow,
      step_name: rules_reading|acceptance|form_submission,
    }
```

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

#### Onboarding Conversion

*@source [SPEC.md](SPEC.md) overview — "ensure each submitted application has confirmed acknowledgment"*

```yaml
- name: business.applications_submitted
  instrument: Counter
  unit: "{application}"
  attributes:
    { feature: player-onboarding, capability: SubmitCandidateApplication }
  business_question: "How many candidates are applying daily?"
  healthy_range: "> 0 (growth indicator)"
  alert: 0 submissions for 7 consecutive days → P2

- name: business.approval_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes:
    { feature: player-onboarding, capability: ReviewCandidateApplication }
  formula: "APPROVED / (APPROVED + REJECTED) over 30d rolling"
  business_question: "What percentage of candidates pass screening?"
  healthy_range: "30%–70% (too high = low bar, too low = bad funnel)"
  alert: rate < 10% or > 90% → P2

- name: business.time_to_review
  instrument: Histogram
  unit: "s" # hours in practice, recorded as seconds
  attributes:
    { feature: player-onboarding, capability: ReviewCandidateApplication }
  formula: "reviewedAt - submittedAt"
  business_question: "How long do candidates wait for a decision?"
  healthy_range: "p50 < 24h, p95 < 72h"
  alert: p50 > 48h → P2 (review backlog growing)
```

#### Duplicate Detection Effectiveness

```yaml
- name: business.duplicate_blocked
  instrument: Counter
  unit: "{application}"
  attributes: { feature: player-onboarding, match_field: whatsapp|email }
  business_question: "How many duplicate applications are we catching?"
  purpose: "validates R5 is working — high volume may indicate bot traffic"
```

### Funnel Metrics (O14)

#### Candidate Onboarding Funnel

*@source [STORIES.md](STORIES.md) — onboarding journey: rules → accept → form → submit*

```yaml
# @rule O14: Funnel Metrics
```

| Step                     | Instrument                                                                     | Expected Conversion      |
| ------------------------ | ------------------------------------------------------------------------------ | ------------------------ |
| 1. Page loaded           | `funnel.step` Counter `{journey: onboarding, step_name: page_loaded, outcome}` | —                        |
| 2. Rules reading started | `funnel.step` Counter `{..., step_name: rules_started, outcome}`               | ≥ 90%                    |
| 3. All rules read        | `funnel.step` Counter `{..., step_name: rules_completed, outcome}`             | ≥ 70%                    |
| 4. Terms accepted        | `funnel.step` Counter `{..., step_name: terms_accepted, outcome}`              | ≥ 95% of rules_completed |
| 5. Form filled           | `funnel.step` Counter `{..., step_name: form_filled, outcome}`                 | ≥ 80% of terms_accepted  |
| 6. Submitted             | `funnel.step` Counter `{..., step_name: submitted, outcome}`                   | ≥ 90% of form_filled     |

**Conversion rate:**

```yaml
# Measures end-to-end conversion rate for the user journey
- name: funnel.conversion_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes: { feature: player-onboarding, journey: onboarding }
  formula: step_6_submitted / step_1_page_loaded
  window: 7d rolling
  alert: rate drops > 10% from 30d baseline → P2
  business_question: "What % of visitors complete the full onboarding?"
  healthy_range: "≥ 40%"
```

**Drop-off analysis:**

```yaml
- name: funnel.drop_off
  instrument: Gauge
  unit: "1" # ratio
  attributes:
    {
      feature: player-onboarding,
      journey: onboarding,
      from_step: string,
      to_step: string,
    }
  formula: "1 - (to_step_count / from_step_count)"
  purpose: "identifies which step loses the most candidates"
  alert: any step drop-off > 50% → P2 (UX friction point)
```

---

## Metric Summary

| Rule                                      | Metric Count                                                                         | Layer                  | Severity       |
| ----------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------- | -------------- |
| O1: Transition counters                   | 2 (transition + invalid)                                                             | Domain Fidelity        | P0 for invalid |
| O2: State distribution                    | 1 (UpDownCounter, 4 states)                                                          | Domain Fidelity        | P2             |
| O3: Invariant monitors                    | 1 (Gauge, 3 invariants)                                                              | Domain Fidelity        | P0             |
| O4: Operation execution (Submit + Review) | 4 (2 invocation + 2 duration)                                                        | Operational            | P1             |
| O5: Rule violations (R1–R9)               | 1 (Counter, 9 rule_id attrs)                                                         | Domain Fidelity        | P2             |
| O6: Calculation drift (C1)                | 1                                                                                    | Domain Fidelity        | P1             |
| O7: Postconditions                        | 1 (Counter, 3 postcondition_id attrs)                                                | Domain Fidelity        | P0–P1          |
| O8: Endpoint SLOs                         | 1 (OTel HTTP semconv)                                                                | Operational            | P1             |
| O11: Query performance                    | 1                                                                                    | Operational            | P2             |
| O12: Workflow completion                  | 3                                                                                    | Operational            | P1             |
| O13: Business KPIs                        | 4                                                                                    | Business Effectiveness | P2             |
| O14: Funnel metrics                       | 3 (step + conversion + drop-off)                                                     | Business Effectiveness | P2             |
| **Total**                                 | **~23 OTel instruments** (covering same behavioral breadth as before via attributes) |                        |                |
