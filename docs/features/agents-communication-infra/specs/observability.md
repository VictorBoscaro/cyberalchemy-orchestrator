---
id: agents-communication-infra
feature: Agents Communication Infra
type: observability
title: "Agents Communication Infra — Observability Spec"
derived-from: domainspec/OBSERVABILITY.md rules O1-O13
status: draft
version: 0.1.0
---

# Agents Communication Infra — Observability Spec

Observability is split into four non-interchangeable planes: permanent audit ledger, durable event
journal, retention-limited operational logs, and aggregate/sampleable traces and metrics. Logs,
metrics, traces and [RuntimeProjection](queries.md#getruntimeprojection) are never workflow authority.
All instruments use meter scope `cyberalchemy-orchestrator` and attribute
`feature=agents-communication-infra`.

This document specifies required signals and alerts; checked rows are specification coverage, not a
claim that collectors, dashboards, sandbox enforcement, credential controls or resource limiters are
already implemented. W0/EG-1 remain blocked until implementation and fault evidence satisfy their
gates.

## Domain Fidelity Metrics

### State and invariant monitors (O1-O3)

| Monitor | Instrument | Safe attributes | Alert |
|---|---|---|---|
| accepted transitions | `aci.state.transition` Counter | entity, from, to, event_type | trend |
| rejected transitions | `aci.state.invalid_transition` Counter | entity, from, attempted_event, error_code | any increment P0 for kernel defect; security rejection classified separately |
| state population | `aci.state.population` UpDownCounter | entity, state | non-terminal accumulation beyond policy deadline P1 |
| replay state-hash mismatch | `aci.replay.state_hash_mismatch` Gauge | reducer_version | any value > 0 P0 |
| duplicate logical terminal/commit | `aci.invariant.duplicate_terminal` Counter | aggregate_type | any increment P0 |
| effect released before verified opening | `aci.invariant.effect_before_opening` Counter | effect_type | any increment P0 |
| peer-content disclosure before reveal | `aci.invariant.sealing_violation` Counter | surface, phase | any increment P0/security |
| manifest/message digest mismatch | `aci.invariant.reveal_manifest_mismatch` Counter | phase | any increment P0 |

Run lifecycle monitoring distinguishes `confirmed`, `opening_pending`, `ready`, `running`,
`execution_terminal`, `close_pending`, `closed` and `reconciliation_required`. Attempt/group states
are separately labeled; they are never aggregated into a false run terminal.

### Operation metrics (O4-O7)

Every operation in [operations.md](operations.md) emits:

```yaml
- name: aci.operation.invocation
  instrument: Counter
  unit: "{invocation}"
  attributes: [feature, operation, result]
- name: aci.operation.duration
  instrument: Histogram
  unit: "s"
  attributes: [feature, operation]
- name: aci.operation.postcondition
  instrument: Counter
  unit: "{check}"
  attributes: [feature, operation, postcondition_id, result]
```

| Operation/rule | Additional instrument | Alert |
|---|---|---|
| [AcceptRuntimeCommand](operations.md#acceptruntimecommand) idempotent replay | `aci.command.deduplicated` Counter `{command_type}` | informational |
| conflicting idempotency digest | `aci.command.idempotency_conflict` Counter `{command_type}` | any unexpected rate P1/security |
| stale aggregate version | `aci.command.cas_conflict` Counter `{aggregate_type}` | trend; sustained saturation P1 |
| changed prerequisite head | `aci.command.prerequisite_conflict` Counter `{aggregate_type, prerequisite_type}` | unexpected start-vs-close/cancel/terminal rate P1; accepted stale start P0 |
| [PublishBusContribution](operations.md#publishbuscontribution) rejection | `aci.bus.publication_rejected` Counter `{reason, phase}` | forged/cross-scope P0; invalid/late trend P1 |
| [VerifyPublicationReceipt](operations.md#verifypublicationreceipt) failure | `aci.bus.receipt_verification_failed` Counter `{reason}` | forged/mismatch P0 |
| effect outcome acceptance | `aci.outbox.outcome_acceptance` Counter `{effect_type,result}` | digest conflict/stale epoch trend P1; partial acceptance P0 |
| [AuditLedgerMaterializer](workflows.md#auditledgermaterializer) exact-row divergence | `aci.ledger.reconciliation_divergence` Counter `{row_kind}` | any increment P0 |
| [RecordUsageObservation](operations.md#recordusageobservation) invalid semantics | `aci.usage.observation_rejected` Counter `{provider, reason}` | sustained rate P1 |

## Operational Health Metrics

### Interface SLO obligations (O8)

Numeric availability/latency thresholds require pilot measurement and ratification before Slice 1
exit; W0 does not invent production SLOs. The following correctness obligations apply immediately.

| Interface | Correctness SLO | Latency measure |
|---|---|---|
| confirm/runtime command API | 100% accepted responses have a committed stable command receipt | request-to-commit histogram |
| agent `bus_publish` | 100% returned receipts match committed journal evidence | request-to-commit histogram |
| run query/stream | no authorized cursor gap is silently skipped | snapshot/query and delta lag histograms |
| adapter operations | all started attempts reach terminal or explicit unknown/reconciliation state | start/status/cancel histograms by adapter |
| audit materializer | no provider effect before verified opening; no `closed` before verified close | intent-to-verification histogram |

### Idempotency and outbox monitors (O9)

| Constraint | Instrument | Alert |
|---|---|---|
| one command result per scoped key/digest | `aci.idempotency.violation` Gauge `{scope}` | any > 0 P0 |
| one contribution per logical seat/round/type | `aci.message.logical_duplicate` Counter `{message_type}` | any accepted duplicate P0 |
| one handoff per source aggregate/connection | `aci.handoff.logical_duplicate` Counter | any accepted duplicate P0 |
| effect claim fencing | `aci.outbox.stale_epoch_completion` Counter `{effect_type}` | any increment P0 |
| effect outcome digest conflict | `aci.outbox.outcome_digest_conflict` Counter `{effect_type}` | any increment P0/reconciliation |
| pending/unknown effects | `aci.outbox.population` UpDownCounter `{effect_type,status}` | beyond policy age P1 |

### Event flow (O10)

| Flow | Producer | Consumer | Metric/alert |
|---|---|---|---|
| command decision events | command service/kernel | reducers/outbox | `aci.event.consumer_lag`; sustained lag P1 |
| accepted bus events | deliberation bus | receipt verifier/group reducer | receipt without matching event P0 |
| collection/reveal events | group kernel | policy/read projections | reveal without frozen manifest P0 |
| attempt/usage observations | adapter worker | attempt/usage projections | missing required provider event at conformance gate P1 |
| opening/close acknowledgement | audit materializer | run reducer | pending beyond recovery budget P1; divergence P0 |

Common instruments are `aci.event.emitted`, `aci.event.consumed` and
`aci.event.consumer_lag` with bounded attributes `event_type`, `producer` and `consumer`. IDs belong
in correlated traces/logs, not metric labels.

### Query performance (O11)

| Query | Measures | Correctness fallback |
|---|---|---|
| [GetRuntimeProjection](queries.md#getruntimeprojection) | duration, result bytes/event count, projection lag | force consistent snapshot on expired/gapped cursor |
| [GetRunStatus](queries.md#getrunstatus) | duration, projection source lag | expose pending/reconciliation; never infer state |
| [GetVisibleGroupMessages](queries.md#getvisiblegroupmessages) | duration, authorized/denied count | fail closed on missing policy/manifest |

## Workflow Metrics (O12)

Each workflow in [workflows.md](workflows.md) emits started/completed/failed/duration counters. The
following additional measures preserve the important failure seams:

| Workflow | Metric | Meaning |
|---|---|---|
| [RunExecutionWorkflow](workflows.md#runexecutionworkflow) | `aci.run.time_to_verified_open`, `aci.run.time_to_verified_close` | cross-store convergence latency |
| [GroupDeliberationWorkflow](workflows.md#groupdeliberationworkflow) | `aci.group.collection_duration`, `aci.group.reveal_delivery_duration` | barrier and delivery latency |
| [ReceiptGatedPublicationWorkflow](workflows.md#receiptgatedpublicationworkflow) | `aci.bus.receipt_gate_result` Counter `{result,reason}` | official-result acceptance health |
| [AuditLedgerMaterializer](workflows.md#auditledgermaterializer) | `aci.ledger.materialization_result` Counter `{row_kind,result}` | absent/identical/divergent outcomes |
| [ExternalEffectReconciliationWorkflow](workflows.md#externaleffectreconciliationworkflow) | `aci.recovery.effect_result` Counter `{effect_type,result}` | converged/unknown/repair-required |
| [ExecutionAuthorityCutoverWorkflow](workflows.md#executionauthoritycutoverworkflow) | `aci.cutover.authority_conflict` Counter | dual-owner attempt; any increment P0 |

## Sandbox, Credential and Resource Observability

These are acceptance obligations for the implementation waves, not evidence that strong isolation
exists today. Values that could reveal secrets, prompts or tenant identity stay out of metric labels.

| Concern | Required signal | Safe attributes | Alert |
|---|---|---|---|
| sandbox policy | `aci.sandbox.launch` Counter and `aci.sandbox.denial` Counter | sandbox_profile, provider, reason | fallback/bypass any increment P0 security; denial trend P1 |
| sandbox escape/control failure | `aci.sandbox.violation` Counter | control, severity | any increment P0 security; stop affected worker |
| credential issuance | `aci.credential.lease` Counter and duration histogram | credential_class, provider, result | issuance outside allowed scope P0 |
| credential exposure | `aci.credential.leak_detected` Counter | detection_surface, credential_class | any increment P0 security; revoke/rotate |
| credential lifecycle | `aci.credential.active_leases` UpDownCounter | credential_class, provider | expired/stale lease P0; abnormal population P1 |
| resource budget | `aci.resource.consumed` Counter | resource_kind, provider, model | approaching configured budget P1 |
| resource enforcement | `aci.resource.limit_result` Counter | resource_kind, result | over-budget effect start P0; repeated denial P1 |
| worker pressure | `aci.resource.worker_saturation` Gauge | pool, resource_kind | threshold determined by pilot; sustained saturation P1 |

Resource metrics cover at least wall time, provider requests, tokens where reported, tool calls,
concurrency, artifact bytes and process memory/CPU where the sandbox can measure them. Budget alerts
use the applicable [ResourceBudget](domain.md#resourcebudget) policy; absence of an enforceable budget
is surfaced as `result=policy_missing`, never interpreted as unlimited authority.

## Usage and Cost Accountability (OQ-ACI10)

Every provider-reported record is persisted first as immutable nullable
[UsageObservation](events.md#usageobserved) with attempt, operation, seat, group, run, dispatch,
provider, adapter, model and source-event provenance. Storage-level rollups follow
[UsageObservationToRollups](mappings.md#usageobservationtorollups).

```yaml
- name: aci.model.usage
  instrument: Counter
  unit: "{token}"
  attributes: [feature, provider, adapter, model, counter_kind, semantics_version]
- name: aci.model.report_coverage
  instrument: Gauge
  unit: "1"
  attributes: [feature, provider, adapter, execution_shape, counter_kind]
- name: aci.model.cost_observed
  instrument: Counter
  unit: "{currency_minor}"
  attributes: [feature, provider, model, currency, pricing_version]
```

Rules:

- null/missing counters are excluded and reported through coverage; never converted to zero;
- retries count as physical consumption, while accepted-attempt usage is a separately labeled view;
- counters with incompatible provider semantics/versions are not summed into an unlabeled total;
- each rollup exports its `source_through_offset`, observation count and missing-count dimensions;
- cost exists only when an explicit immutable pricing source/version and pricing digest support a
  compatible completed calculation;
- calculated cost carries currency and pricing digest; no cost metric is emitted for missing or
  incompatible pricing;
- dashboards say “provider-reported” and never claim invoice/billing equivalence;
- Slice 2 validates single-provider tool-heavy, multi-turn, resumed and retried completeness; Slice 3
  validates second/mixed-provider rollups without schema/kernel forks.

## Business Effectiveness (O13)

| Question | KPI | Gate |
|---|---|---|
| Does recovery preserve one logical outcome? | recovery convergence rate and duplicate logical effect count | Slice 0/1 |
| Does sealing hold across controlled surfaces? | sealing violation count and denied cross-seat probes | Slice 1 |
| Does one provider satisfy the common contract? | adapter conformance pass rate by execution shape | Slice 2 |
| Does mixed-provider operation preserve the protocol? | mixed-run conformance pass rate and schema/kernel fork count | Slice 3 |
| Does multi-agent deliberation earn its cost? | preregistered rubric quality/dissent benefit versus latency and provider-reported usage/cost | product gate |

## Trace and Log Correlation

Traces/logs may carry `dispatch_id`, `run_id`, `group_id`, `operation_id`, `attempt_id`, `command_id`,
`event_id`, `message_id`, `effect_id`, `correlation_id` and journal offset under access controls.
Metrics must not use these unbounded identifiers as labels. Prompts, raw outputs, message payloads,
credentials and secrets are artifact references/digests only; operational logging does not grant
access to their content. Allow/deny, break-glass, spoof, stale capability and cross-run attempts are
security audit facts with redaction appropriate to OQ-ACI9.

## Alert Runbook Index

| Alert | Severity | First checks |
|---|---|---|
| replay state-hash mismatch / duplicate terminal / pre-opening effect | P0 | stop promotion; preserve DB/artifacts; compare journal transaction and reducer version |
| sealing/reveal/capability violation | P0 security | revoke capability, halt affected group, preserve manifest/access evidence |
| ledger exact-row divergence | P0 | block effects/closure; compare frozen authority, canonical mapping and existing row; no append retry |
| forged/mismatched receipt | P0 security | reject result; correlate capability, persisted event and raw provider output |
| prolonged pending/unknown effect or projection lag | P1 | inspect claim epoch, adapter status/reconciler and journal cursor |
| incomplete usage reports | P1 at adapter gate | compare execution-shape matrix and provider-native records; keep fields null |
| sandbox fallback/escape or credential exposure | P0 security | stop affected worker/effects; revoke credentials; preserve redacted security evidence |
| resource budget bypass | P0 | fence new effects; compare materialized invocation budget, measured consumption and limiter decision |
| stale usage rollup or pricing mismatch | P1 | compare `source_through_offset`, missing counts, pricing digest/currency and immutable observations |

## Coverage Checklist

- [x] Lifecycle transitions, invalid transitions and invariants have monitors (O1-O3).
- [x] Operation base metrics, violations and postconditions are specified (O4-O7).
- [x] Interface correctness SLOs and idempotency monitors are specified (O8-O9).
- [x] Journal/event flow and query performance obligations are specified (O10-O11).
- [x] Every workflow has completion/recovery measures (O12).
- [x] Capability/product gates have KPIs (O13).
- [x] Usage rollups preserve provenance, nullability and provider semantics (OQ-ACI10).
- [x] Sandbox, credential and resource observability requirements and alert semantics are specified.
- [ ] Sandbox, credential and resource collectors/enforcement await implementation evidence.
- [ ] Numeric latency/availability thresholds await measured pilot baselines before Slice 1 exit.
- [ ] Retention, encryption and key-management thresholds await the OQ-ACI9 ADR.
