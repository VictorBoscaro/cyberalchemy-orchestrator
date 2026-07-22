---
id: auth-access-control
feature: auth-access-control
type: observability
title: "Auth & Access Control — Observability Spec"
summary: Observability contract for authentication and authorization lifecycle, policy decisions, and security-critical request flow.
derived-from: OBSERVABILITY.md rules O1–O13
status: draft
pillar: platform
domain: auth-access-control-observability
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
updatedAt: 2026-04-17
dependencies:
  - SPEC.md
  - operations.md
includes: []
---

# Auth & Access Control — Observability Spec

> Derived from feature docs using [OBSERVABILITY.md](../../../domainspec/OBSERVABILITY.md) derivation rules.
> Instrumented via OpenTelemetry API. Meter scope: `poker-team`. All instruments carry `feature: auth-access-control`.
> Platform-pillar feature — security-critical. Every protected request flows through AuthenticateRequest + AuthorizeRequest.

---

## Domain Fidelity Metrics

### State Machine Monitors (O1–O3)

#### SessionLifecycle State Machine

**Transition counters (O1):**

| From   | To         | Event           | Attributes                                                        |
| ------ | ---------- | --------------- | ----------------------------------------------------------------- |
| [new]  | ACTIVE     | LoginSucceeded  | `{entity: Session, from: new, to: ACTIVE, event: LoginSucceeded}` |
| ACTIVE | TERMINATED | LogoutCompleted | `{..., from: ACTIVE, to: TERMINATED, event: LogoutCompleted}`     |
| ACTIVE | EXPIRED    | SessionExpired  | `{..., from: ACTIVE, to: EXPIRED, event: SessionExpired}`         |

*@source [states.md#SessionLifecycle](states.md#SessionLifecycle)*

```yaml
# @rule O1: Transition Counter
# Counts each valid state transition in the Session lifecycle
- name: state.transition
  instrument: Counter
  unit: "{transition}"
  description: "Counts each valid state transition in the Session lifecycle"
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
  alert: any increment → P0 (terminal states leaking back to active)
```

**State distribution (O2):**

```yaml
# @rule O2: Session State Distribution
# Tracks how many entities are currently in each Session state
- name: state.population
  instrument: UpDownCounter
  unit: "{entity}"
  description: "Tracks how many entities are currently in each Session state"
  attributes:
    {
      feature: auth-access-control,
      entity: Session,
      state: ACTIVE|TERMINATED|EXPIRED,
    }
  monitors:
    - active_sessions: "count of ACTIVE sessions"
      alert: sudden spike > 10x baseline → P1 (possible session flood / attack)
    - expired_backlog: "ACTIVE sessions where now >= expiresAt but not yet reaped"
      alert: backlog > 100 → P2 (expiry reaper lagging)
```

#### TokenLifecycle State Machine

**Transition counters (O1):**

| From   | To      | Event        | Attributes                                                         |
| ------ | ------- | ------------ | ------------------------------------------------------------------ |
| [new]  | ACTIVE  | TokenIssued  | `{entity: AccessToken, from: new, to: ACTIVE, event: TokenIssued}` |
| ACTIVE | EXPIRED | TokenExpired | `{..., from: ACTIVE, to: EXPIRED, event: TokenExpired}`            |
| ACTIVE | REVOKED | TokenRevoked | `{..., from: ACTIVE, to: REVOKED, event: TokenRevoked}`            |

*@source [states.md#TokenLifecycle](states.md#TokenLifecycle)*

```yaml
# Counts each valid state transition in the AccessToken lifecycle
- name: state.transition
  instrument: Counter
  unit: "{transition}"
  description: "Counts each valid state transition in the AccessToken lifecycle"
  attributes:
    { feature: auth-access-control, entity: AccessToken, from, to, event }
```

**State distribution (O2):**

```yaml
# Tracks how many entities are currently in each AccessToken state
- name: state.population
  instrument: UpDownCounter
  unit: "{entity}"
  description: "Tracks how many entities are currently in each AccessToken state"
  attributes:
    {
      feature: auth-access-control,
      entity: AccessToken,
      state: ACTIVE|EXPIRED|REVOKED,
    }
  monitors:
    - active_tokens: "count of ACTIVE tokens"
      alert: sudden spike > 5x baseline → P1 (token flood)
```

**Invariant monitors (O3):**

| ID  | Entity  | Invariant                         | Check                                                                                          | Alert                                  |
| --- | ------- | --------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------- |
| I1  | Session | Terminal states remain terminal   | Periodic: query sessions where status IN (TERMINATED, EXPIRED) AND updated_at recently changed | any violation → P0                     |
| I2  | Session | Active session has future expiry  | Periodic: count sessions where status = ACTIVE AND expiresAt <= now                            | count > 0 → P2 (expiry reaper lagging) |
| I1  | Token   | Terminal states remain terminal   | Periodic: query tokens where status IN (EXPIRED, REVOKED) AND updated_at recently changed      | any violation → P0                     |
| I2  | Token   | ACTIVE tokens must not be revoked | Periodic: count tokens where status = ACTIVE AND revokedAt IS NOT NULL                         | any count > 0 → P0                     |
| I3  | Token   | EXPIRED tokens are not accepted   | Monitor: AuthenticateRequest returns success for expired token                                 | any occurrence → P0                    |

```yaml
# Detects domain invariant violations that should never occur in correct code
- name: invariant.violation
  instrument: Gauge
  unit: "{entity}"
  description: "Detects domain invariant violations that should never occur in correct code"
  attributes:
    {
      feature: auth-access-control,
      entity: Session|AccessToken,
      invariant_id: string,
      expression: string,
    }
  frequency: every 5 minutes
  alert: any value > 0 → P0
```

### Operation Metrics (O4–O7)

#### Login

**Base metrics (O4):**

*@source [operations.md#Login](operations.md#Login)*

```yaml
# Counts each call to Login, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to Login, grouped by success or error outcome"
  attributes:
    { feature: auth-access-control, operation: Login, result: success|error }

# Measures execution time of Login in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of Login in seconds"
  attributes: { feature: auth-access-control, operation: Login }
```

**Rule violation rates (O5):**

| Rule | Expression                                    | Instrument                                | Alert Threshold                          |
| ---- | --------------------------------------------- | ----------------------------------------- | ---------------------------------------- |
| R1   | `principal(identifier).status = ACTIVE`       | `rule.violation` Counter `{rule_id="R1"}` | informational (disabled accounts)        |
| R2   | `verifyCredential(identifier, secret) = true` | `rule.violation` Counter `{rule_id="R2"}` | **rate > 20% in 5m → P1** (brute force)  |
| R3   | `riskPolicy(context) = ALLOW`                 | `rule.violation` Counter `{rule_id="R3"}` | track by deny reason — volume spike → P1 |

> **Security insight:** R2 (invalid credentials) and R3 (risk policy denial) are the primary brute-force indicators. High R2 rate from a single IP + R3.failedAttemptsLast15m >= 5 = active attack.

**Risk policy denial breakdown:**

```yaml
# Counts login denials grouped by reason — primary brute-force detection signal
- name: security.login_denied
  instrument: Counter
  unit: "{denial}"
  attributes:
    {
      feature: auth-access-control,
      operation: Login,
      deny_reason: IP_BLOCKED|RATE_LIMITED|NO_USER_AGENT|INVALID_CREDENTIALS|PRINCIPAL_DISABLED,
    }
  purpose: "granular breakdown of why logins fail — security signal"
```

**Postcondition verification (O7):**

| Postcondition                       | Instrument                                                                            | Alert                    |
| ----------------------------------- | ------------------------------------------------------------------------------------- | ------------------------ |
| Session created and persisted       | `postcondition.check` Counter `{postcondition_id="session_created", result}`          | any result=violated → P1 |
| Access token issued for new session | `postcondition.check` Counter `{postcondition_id="token_issued_for_session", result}` | any result=violated → P1 |

#### IssueAccessToken

**Base metrics (O4):**

*@source [operations.md#IssueAccessToken](operations.md#IssueAccessToken)*

```yaml
# Counts each call to IssueAccessToken, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to IssueAccessToken, grouped by success or error outcome"
  attributes:
    {
      feature: auth-access-control,
      operation: IssueAccessToken,
      result: success|error,
    }

# Measures execution time of IssueAccessToken in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of IssueAccessToken in seconds"
  attributes: { feature: auth-access-control, operation: IssueAccessToken }
```

**Rule violation rates (O5):**

| Rule | Expression                       | Instrument                                                              | Alert Threshold            |
| ---- | -------------------------------- | ----------------------------------------------------------------------- | -------------------------- |
| R1   | `session.status = ACTIVE`        | `rule.violation` Counter `{rule_id="R1", operation="IssueAccessToken"}` | rate > 5% → P2             |
| R2   | `minTtl <= ttlSeconds <= maxTtl` | `rule.violation` Counter `{rule_id="R2", operation="IssueAccessToken"}` | rate > 0 → P2 (API misuse) |

#### AuthenticateRequest

**Base metrics (O4):**

*@source [operations.md#AuthenticateRequest](operations.md#AuthenticateRequest)*

```yaml
# Counts each call to AuthenticateRequest, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to AuthenticateRequest, grouped by success or error outcome"
  attributes:
    {
      feature: auth-access-control,
      operation: AuthenticateRequest,
      result: success|error,
    }

# Measures execution time of AuthenticateRequest in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  attributes: { feature: auth-access-control, operation: AuthenticateRequest }
  description: "CRITICAL — this runs on every protected request. p99 must be minimal."
```

> **Performance note:** AuthenticateRequest is the hottest path in the system. p99 latency directly impacts every API call. Target: p99 < 5ms.

**Rule violation rates (O5):**

| Rule | Expression                                 | Instrument                                                                 | Alert Threshold                                       |
| ---- | ------------------------------------------ | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| R1   | `authorizationHeader startsWith 'Bearer '` | `rule.violation` Counter `{rule_id="R1", operation="AuthenticateRequest"}` | rate > 10% → P2 (missing header)                      |
| R2   | `verifySignature(token) = true`            | `rule.violation` Counter `{rule_id="R2", operation="AuthenticateRequest"}` | **any > 0 → P1** (tampered tokens)                    |
| R3   | `now < token.expiresAt`                    | `rule.violation` Counter `{rule_id="R3", operation="AuthenticateRequest"}` | informational (normal expiry)                         |
| R4   | `token.revokedAt = null`                   | `rule.violation` Counter `{rule_id="R4", operation="AuthenticateRequest"}` | track volume — high rate = logout propagation working |
| R5   | `token.sid != null`                        | `rule.violation` Counter `{rule_id="R5", operation="AuthenticateRequest"}` | **any > 0 → P0** (malformed token)                    |
| R6   | `session(token.sid).status = ACTIVE`       | `rule.violation` Counter `{rule_id="R6", operation="AuthenticateRequest"}` | informational (session terminated)                    |

> **Security insight:** R2 (invalid signature) is the strongest signal of token tampering. Any non-zero rate warrants investigation.

#### AuthorizeRequest

**Base metrics (O4):**

*@source [operations.md#AuthorizeRequest](operations.md#AuthorizeRequest)*

```yaml
# Counts each call to AuthorizeRequest, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to AuthorizeRequest, grouped by success or error outcome"
  attributes:
    {
      feature: auth-access-control,
      operation: AuthorizeRequest,
      result: ALLOW|DENY,
    }

# Measures execution time of AuthorizeRequest in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of AuthorizeRequest in seconds"
  attributes: { feature: auth-access-control, operation: AuthorizeRequest }
```

**Rule violation rates (O5):**

| Rule | Expression                                          | Instrument                                                              | Alert Threshold                                 |
| ---- | --------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------- |
| R1   | `requiredPermission matches permissionKeyPattern`   | `rule.violation` Counter `{rule_id="R1", operation="AuthorizeRequest"}` | any > 0 → P2 (bad permission key in code)       |
| R2   | `decision(permissions, requiredPermission) = ALLOW` | `rule.violation` Counter `{rule_id="R2", operation="AuthorizeRequest"}` | track by permission — per-permission spike → P2 |
| R3   | `exists denyMatch => decision = DENY`               | `rule.violation` Counter `{rule_id="R3", operation="AuthorizeRequest"}` | informational (deny rules working)              |

**Access denied breakdown:**

```yaml
# Counts authorization denials per permission — privilege escalation detection signal
- name: security.access_denied
  instrument: Counter
  unit: "{denial}"
  attributes:
    {
      feature: auth-access-control,
      operation: AuthorizeRequest,
      required_permission: string,
      reason_code: string,
    }
  purpose: "per-permission denial tracking — identifies misconfigured roles or privilege escalation attempts"
  alert: sudden spike for a single permission → P2
```

#### Logout

**Base metrics (O4):**

*@source [operations.md#Logout](operations.md#Logout)*

```yaml
# Counts each call to Logout, grouped by success or error outcome
- name: operation.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts each call to Logout, grouped by success or error outcome"
  attributes:
    { feature: auth-access-control, operation: Logout, result: success|error }

# Measures execution time of Logout in seconds
- name: operation.duration
  instrument: Histogram
  unit: "s"
  description: "Measures execution time of Logout in seconds"
  attributes: { feature: auth-access-control, operation: Logout }
```

**Postcondition verification (O7):**

| Postcondition                 | Instrument                                                                        | Alert                                    |
| ----------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------- |
| Session marked TERMINATED     | `postcondition.check` Counter `{postcondition_id="session_terminated", result}`   | any result=violated → P1                 |
| Active tokens revoked         | `postcondition.check` Counter `{postcondition_id="tokens_revoked", result}`       | any result=violated → P0 (security leak) |
| Revocation evidence persisted | `postcondition.check` Counter `{postcondition_id="revocation_persisted", result}` | any result=violated → P0                 |

---

## Operational Health Metrics

### Endpoint SLOs (O8)

*@source [interfaces.md](interfaces.md)*

| Endpoint            | Method | Availability SLO | Latency p99 SLO | Throughput Baseline |
| ------------------- | ------ | ---------------- | --------------- | ------------------- |
| `/auth/login`       | POST   | ≥ 99.9%          | ≤ 500ms         | ~100 req/day        |
| `/auth/token`       | POST   | ≥ 99.9%          | ≤ 100ms         | ~100 req/day        |
| `/auth/logout`      | POST   | ≥ 99.9%          | ≤ 300ms         | ~50 req/day         |
| `/auth/introspect`  | GET    | ≥ 99.9%          | ≤ 50ms          | ~500 req/day        |
| `/auth/permissions` | GET    | ≥ 99.9%          | ≤ 100ms         | ~20 req/day         |

*@source [interfaces.md](interfaces.md)*

```yaml
# Measures HTTP request latency per endpoint using OTel semantic conventions
- name: http.server.request.duration # OTel semconv
  instrument: Histogram
  unit: "s"
  attributes:
    {
      http.request.method: POST|GET,
      url.path: /auth/*,
      http.response.status_code: int,
      feature: auth-access-control,
    }
```

### Event Flow (O10)

| Event           | Producer         | Consumers                          | Lag SLO |
| --------------- | ---------------- | ---------------------------------- | ------- |
| LoginSucceeded  | Login            | audit subsystem, session tracker   | ≤ 2s    |
| TokenIssued     | IssueAccessToken | audit subsystem, session tracker   | ≤ 2s    |
| TokenRevoked    | Logout           | audit subsystem, cache invalidator | ≤ 1s    |
| LogoutCompleted | Logout           | audit subsystem, session tracker   | ≤ 2s    |
| AccessDenied    | AuthorizeRequest | security analytics, alerting       | ≤ 1s    |

*@source [events.md](events.md)*

```yaml
# Counts domain events published by this feature
- name: event.emit # Counter {feature: auth-access-control, event_type: LoginSucceeded|TokenIssued|TokenRevoked|LogoutCompleted|AccessDenied}
# Counts domain events consumed by downstream listeners
- name: event.consume # Counter {feature: auth-access-control, event_type, consumer}
# Measures delay in seconds between event publish time and consumer processing
- name: event.consumer.lag # Histogram (s) {feature: auth-access-control, event_type, consumer}
```

> **Security note:** AccessDenied event lag SLO is ≤ 1s — security analytics must react quickly to privilege escalation attempts.

### Query Performance (O11)

*@source [interfaces.md](interfaces.md)*

| Query                | p95 Latency SLO | Max Result Size | Cache TTL                   |
| -------------------- | --------------- | --------------- | --------------------------- |
| IntrospectToken      | ≤ 20ms          | 1 row           | 0 (always fresh — security) |
| GetPermissionCatalog | ≤ 50ms          | full catalog    | 300s                        |

### Workflow Completion (O12)

*@source [workflows.md#EndToEndAuthFlow](workflows.md#EndToEndAuthFlow)*

```yaml
# Counts end-to-end EndToEndAuthFlow executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end EndToEndAuthFlow executions, grouped by outcome"
  attributes:
    {
      feature: auth-access-control,
      workflow: EndToEndAuthFlow,
      result: completed|failed,
    }

# Measures total wall-clock time for EndToEndAuthFlow execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  description: "Measures total wall-clock time for EndToEndAuthFlow execution"
  attributes: { feature: auth-access-control, workflow: EndToEndAuthFlow }

# Counts EndToEndAuthFlow failures, tagged by the step where failure occurred
- name: workflow.failed
  instrument: Counter
  unit: "{failure}"
  description: "Counts EndToEndAuthFlow failures, tagged by the step where failure occurred"
  attributes:
    {
      feature: auth-access-control,
      workflow: EndToEndAuthFlow,
      failed_at_step: credential_validation|session_creation|token_issuance|auth_check|authorization|logout,
    }
```

*@source [workflows.md#AuthorizeRequestFlow](workflows.md#AuthorizeRequestFlow)*

```yaml
# Counts end-to-end AuthorizeRequestFlow executions, grouped by outcome
- name: workflow.invocation
  instrument: Counter
  unit: "{invocation}"
  description: "Counts end-to-end AuthorizeRequestFlow executions, grouped by outcome"
  attributes:
    {
      feature: auth-access-control,
      workflow: AuthorizeRequestFlow,
      result: completed|failed,
    }

# Measures total wall-clock time for AuthorizeRequestFlow execution
- name: workflow.duration
  instrument: Histogram
  unit: "s"
  attributes: { feature: auth-access-control, workflow: AuthorizeRequestFlow }
  description: "Measures total auth middleware overhead per request"
```

---

## Business Effectiveness Metrics

### Capability KPIs (O13)

#### Authentication Health

```yaml
- name: business.login_success_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes: { feature: auth-access-control, capability: Login }
  formula: "successful_logins / total_login_attempts over 1h"
  business_question: "What percentage of login attempts succeed?"
  healthy_range: "≥ 80% (lower may indicate UX issue or attack)"
  alert: rate < 50% in 15m → P1 (possible brute force or system issue)

- name: business.active_sessions
  instrument: Gauge
  unit: "{session}"
  attributes: { feature: auth-access-control }
  business_question: "How many users are actively using the system?"
  healthy_range: "within historical daily pattern"
  alert: 0 active sessions during business hours → P1

- name: business.avg_session_duration
  instrument: Histogram
  unit: "s"
  attributes: { feature: auth-access-control, capability: Login }
  formula: "terminatedAt - createdAt for sessions that reached TERMINATED"
  business_question: "How long do user sessions typically last?"
  healthy_range: "1h–8h (session max is 8h)"
```

#### Authorization Effectiveness

```yaml
- name: business.authorization_deny_rate
  instrument: Gauge
  unit: "1" # ratio
  attributes: { feature: auth-access-control, capability: AuthorizeRequest }
  formula: "DENY / (ALLOW + DENY) over 1h"
  business_question: "What percentage of authorization checks are denied?"
  healthy_range: "< 5% (higher may indicate role misconfiguration)"
  alert: rate > 20% → P2 (systematic permission issue)
```

---

## Metric Summary

| Rule                                                                  | Metric Count                                     | Layer                  | Severity       |
| --------------------------------------------------------------------- | ------------------------------------------------ | ---------------------- | -------------- |
| O1: Session + Token transitions                                       | 2 (transition + invalid, 2 entities)             | Domain Fidelity        | P0 for invalid |
| O2: State distribution                                                | 2 (UpDownCounter, 2 entities)                    | Domain Fidelity        | P1–P2          |
| O3: Invariant monitors                                                | 1 (Gauge, 5 invariants across 2 entities)        | Domain Fidelity        | P0             |
| O4: Operation execution (5 operations)                                | 10 (5 invocation + 5 duration)                   | Operational            | P1             |
| O5: Rule violations (Login 3 + Issue 2 + Auth 6 + Authz 3 + Logout 0) | 1 (Counter, 14 rule_id attrs)                    | Domain Fidelity        | P0–P2          |
| O7: Postconditions (Login + Logout)                                   | 1 (Counter, 5 postcondition_id attrs)            | Domain Fidelity        | P0–P1          |
| O8: Endpoint SLOs                                                     | 1 (OTel HTTP semconv)                            | Operational            | P1             |
| O10: Event flow                                                       | 3 (emit + consume + lag)                         | Operational            | P1             |
| O11: Query performance                                                | 1                                                | Operational            | P2             |
| O12: Workflow completion                                              | 5 (2 workflows × invocation+duration + 1 failed) | Operational            | P1             |
| O13: Business KPIs                                                    | 4                                                | Business Effectiveness | P1–P2          |
| Security-specific                                                     | 2 (login_denied + access_denied breakdowns)      | Domain Fidelity        | P1             |
| **Total**                                                             | **~33 OTel instruments**                         |                        |                |
