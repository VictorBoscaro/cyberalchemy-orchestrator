---
module: agent-provenance-telemetry
version: 0.1.0
status: draft
updatedAt: 2026-07-23
docType: observability
specAuthoringGate: in-review
runtimeGate: block
derivedFrom: SPEC.md@0.1.0
---

# Observability: Agent Provenance Telemetry

This aspect defines the minimum operational signals needed to diagnose APT Operations, its local
ACI adapter, deterministic reads/projections, Session workflow and reference-probe ingestion. It
derives from the [APT concept registry](SPEC.md#concept-registry), the
[persistence/replay boundary](persistence-and-replay.md#authority-boundary) and the existing
[ACI observability contract](../../agents-communication-infra/specs/observability.md).

It specifies signal shape and safety obligations only. It does not claim that collectors,
exporters, dashboards, alerts, storage, deployment or instrumentation exist. It introduces no new
Domain Event, bus, store or control-plane concept, and does not lift the
[WORK-PACK mutation gate](../WORK-PACK.md#mutation-gate-authority-and-evidence).

## Non-Authority Contract

APT operational logs, traces, metrics, dashboards and alerts are retention-limited observations.
They are never:

- proof that an APT command/event was accepted;
- a substitute for an ACI receipt, journal prefix, semantic key or aggregate head;
- an input to an Operation, domain Rule, replay reducer or projection hash;
- a retry/idempotency lookup, recovery ledger or reverse-join authority;
- evidence that an artifact, profile or probe recommendation was committed;
- permission to append, retry, roll over, link, publish, rebuild or repair; or
- a trigger that directly changes workflow control flow.

Only the verified ACI result described by
[Atomic Commands, Results and Receipts](persistence-and-replay.md#atomic-commands-results-and-receipts)
determines an append outcome. An alert may prompt an authorized operator to inspect authoritative
state and separately invoke an existing control surface; the signal itself cannot perform that
action.

```text
telemetry_signal ∉ command_inputs ∪ replay_inputs ∪ projection_hash_inputs
emit_failure ⇒ no_change(operation_result)
alert_fired ⇒ no_automatic_APT_command
```

## Signal Inventory

All signal names use the `apt.` namespace and the resource attribute
`feature=agent-provenance-telemetry`.

| Signal family | Purpose | Minimum instruments | Source contract |
|---|---|---|---|
| Operation outcome | Observe all six mutation calls and closed append branches | structured completion log, root span, invocation/duration counters | [Operations](operations.md) |
| ACI adapter | Observe submit, receipt/group verification and typed failures | adapter child span/log, outcome/conflict counters | [ACICommandAdapter](interfaces.md#acicommandadapter) |
| Accepted event flow | Count only receipt-verified accepted event groups | group-completion log, accepted-event counter, projection-lag histogram | [Events](events.md), [States](states.md#atomic-command-receipt-and-read-grouping) |
| Replay/projection | Observe input binding, pure fold, historical boundary and integrity failures | query span/log, result/failure/fallback counters, duration/lag histograms | [Queries](queries.md), [Persistence and Replay](persistence-and-replay.md#replay-checkpoints-and-projections) |
| Session workflow | Distinguish ensure reuse, new Session, rollover and optional link | workflow span/log and result counter | [StartOrReuseSession](workflows.md#startorreusesession) |
| Research workflow | Distinguish capture status and independent enrichment outcomes | workflow span/log and item result counter | [CaptureAndEnrichResearch](workflows.md#captureandenrichresearch) |
| Probe lineage | Distinguish delivery verification and zero/mixed/all-new transactional partitions | workflow span/log and partition counters | [IngestReferenceProbeLineage](workflows.md#ingestreferenceprobelineage) |
| Contract/security health | Surface profile, evidence, CAS, atomic-group, replay and redaction failures | closed failure counters and restricted diagnostic logs | [Rules](rules.md), [Interfaces](interfaces.md) |

Operational observation of an accepted APT Domain Event happens only after the adapter verifies the
durable ACI receipt/group. It does not append an “observed” Event and cannot fill a missing journal
member.

## Common Signal Envelope

Every structured log record and span carries this closed envelope:

| Field | Cardinality | Classification | Rule |
|---|---:|---|---|
| `signal_schema` | exactly 1 | internal | Exact schema ID from this document |
| `signal_version` | exactly 1 | internal | `1` |
| `feature` | exactly 1 | internal | Constant `agent-provenance-telemetry` |
| `signal_name` | exactly 1 | internal | Closed name |
| `observed_at` | exactly 1 | internal | Operational observation time; never event ordering authority |
| `severity` | exactly 1 | internal | `debug`, `info`, `warn` or `error` |
| `operation` | exactly 1, nullable | internal | One of the six registered Operation names or canonical null |
| `workflow` | exactly 1, nullable | internal | One of the three registered Workflow names or canonical null |
| `operation_outcome` | exactly 1, nullable | internal | Closed Operation outcome or canonical null |
| `adapter_outcome` | exactly 1, nullable | internal | Closed adapter outcome or canonical null |
| `workflow_result` | exactly 1, nullable | internal | `completed`, `partial`, `failed` or canonical null |
| `error_code` | exactly 1, nullable | restricted | Exact closed [InterfaceError](interfaces.md#interfaceerror) code or canonical null; never free text |
| `error_family` | exactly 1, nullable | internal | Closed bounded family or canonical null |
| `retryability` | exactly 1, nullable | internal | `never`, `same-command`, `refresh-owner-evidence` or canonical null; derived from InterfaceError |
| `correlation` | exactly 1 object | restricted | Closed opaque-ID/causation shape below; fields may be canonical null |
| `duration_ms` | exactly 1, nullable | internal | Non-negative operational duration or canonical null; not semantic time |

Every common-envelope slot is present. Non-applicable values are encoded only as canonical null;
omission is invalid.

Unknown fields are dropped before export and count as a schema violation. Free-form `message`,
payload, exception text or serialized input/output fields are forbidden.

### Correlation and Causation

Logs and spans may carry the following exact opaque identifiers under restricted access:

```text
correlation = {
  trace_id,
  span_id,
  parent_span_id,
  correlation_id,
  causation_id,
  command_identity,
  receipt_id,
  event_id,
  session_id,
  session_dispatch_link_id,
  dispatch_id,
  research_capture_id,
  fact_id,
  probe_id,
  journal_first_offset,
  journal_last_offset,
  requested_o,
  effective_as_of,
  source_through_offset
}
```

Every slot is present and either an opaque value or canonical null. Applicable values must be exact;
they are never reconstructed from text similarity. `correlation_id` directly preserves the trusted
invocation correlation ref. For a submitted/accepted command, `causation_id` is only the
owner-bound ACI envelope encoding/reference of `command_identity(op)` required by
[APTFactToACIEvent](mappings.md#aptfacttoacievent); there is no caller-selected causation value.
For a non-command observation without such an envelope it is canonical null. `receipt_id` and
`event_id` remain in their own slots and are never chosen as substitute causation IDs.
`command_identity` is the one normalized command identity:

```text
command_identity =
  capture_operation_id  when operation = AppendResearchCapture
  operation_id          for the other five Operations
  canonical null        when no command identity applies
```

There is no generic `operation_id` slot for `AppendResearchCapture`. A submitted operation span
carries exactly this normalized identity; a post-acceptance signal may add verified
receipt/event/offset IDs.

These identifiers are forbidden as metric attributes. They are correlation aids, not acceptance
evidence, and are retained only under the restricted log/trace policy.

## Data Classification and Redaction

| Class | Permitted examples | Surfaces | Treatment |
|---|---|---|---|
| `internal_bounded` | operation/workflow/event enums, outcome branch, error family, status class, counts, durations | logs, spans, metrics | Allowlisted exactly |
| `restricted_correlation` | opaque IDs, offsets, command/receipt/payload digests, registered profile ID/version | protected logs and spans only | Access-controlled, finite retention, never metric labels |
| `prohibited_content` | raw research/artifact/checkpoint bodies, selectors or selector offsets/digests, session names, questions, answers, claims, problems, notation/LaTeX/legend/reading, locators, reference text, prompts, credentials, authorization evidence, stack traces containing values | none | Drop before signal creation; record only bounded violation reason |

Artifact IDs and content digests, where operationally necessary, are
`restricted_correlation`; artifact storage locators are prohibited. `method_ref`, `policy_ref`,
`producer_ref`, actor display names and arbitrary owner evidence are not metric attributes and may
enter a protected trace/log only as an opaque pre-classified reference, never as user-controlled
text.

Redaction is allowlist-first:

1. construct a typed signal from known fields only;
2. map detailed errors to a closed metric `error_family`;
3. preserve every closed schema slot and encode non-applicable values as canonical null;
4. drop prohibited content and unknown keys before formatter/exporter invocation;
5. emit only the finite `error_code/error_family` representation; exception type, class, message
   and stack are never signal fields; and
6. increment `apt.telemetry.schema_violation` without copying the offending value.

A redaction/export failure cannot change the Operation result or cause an automatic retry.

## Structured Log Schemas

### `apt.operation.completed@1`

One record is attempted after each ProvenanceAppendPort invocation reaches a typed outcome.

| Field | Required | Closed values / rule |
|---|---:|---|
| common envelope | yes | All common slots present; `operation_outcome` is non-null, `adapter_outcome/workflow_result` are canonical null |
| `operation` | yes | `EnsureSession`, `StartNewSession`, `LinkSessionDispatch`, `AppendResearchCapture`, `AppendResearchFact`, `AppendReferenceProbeLineage` |
| `operation_outcome` | yes | `accepted_new`, `submitted_retry`, `semantic_existing`, `conflict`, `error` |
| `error_code` | yes, nullable | Non-null for `conflict/error`; canonical null otherwise |
| `error_family` | yes, nullable | Closed family for `conflict/error`; canonical null otherwise |
| `retryability` | yes, nullable | Exact value derived by [InterfaceError](interfaces.md#interfaceerror) for `conflict/error`; canonical null otherwise |
| `event_count` | yes | Non-negative; zero for no-command branches |
| `receipt_present` | yes | Boolean consistent with verified result |
| `duration_ms` | yes | Non-negative |

`semantic_existing` includes ensure reuse and zero-new semantic results without claiming a new
receipt. The record never contains an Entity/capture/event payload.

### `apt.adapter.submit.completed@1`

| Field | Required | Closed values / rule |
|---|---:|---|
| common envelope | yes | All common slots present; `adapter_outcome` is non-null, `operation_outcome/workflow_result` are canonical null |
| `submission_kind` | yes | `single`, `atomic` |
| `adapter_outcome` | yes | `accepted_new`, `submitted_retry`, `semantic_existing`, `conflict`, `error`, `unknown_response` |
| `error_code` / `error_family` / `retryability` | yes, nullable | For `unknown_response`, exactly `APPEND_FAILED` / `internal` / `same-command`; other errors use their exact InterfaceError mapping; all three are canonical null for accepted/retry/existing |
| `receipt_verification` | yes | `verified`, `not_applicable`, `failed`, `unknown` |
| `group_verification` | yes | `verified`, `not_applicable`, `failed`, `unknown` |
| `existing_exact_count` | yes | Non-negative |
| `submitted_new_count` | yes | Non-negative |
| `accepted_new_count` | yes | Non-negative |

When the adapter response is unknown, the log uses only `adapter_outcome=unknown_response`,
`error_code=APPEND_FAILED`, `error_family=internal` and `retryability=same-command`. It invents no
additional error code and never says accepted based on a projection, prior log or artifact. A retry
is permitted only as the same command identity/digest through the authoritative ACI boundary.

### `apt.event.group.accepted@1`

Exactly one record may be emitted for a newly accepted, receipt-verified ACI command group. Retry
and semantic-existing branches emit no accepted-group record.

| Field | Required | Closed values / rule |
|---|---:|---|
| common envelope | yes | All common slots present; `operation_outcome=accepted_new`; `adapter_outcome/workflow_result/error_code/error_family/retryability` are canonical null |
| `group_kind` | yes | `single`, `atomic` |
| `journal_first_offset` | yes | Exact verified integer `≥1`; also present in restricted correlation |
| `journal_last_offset` | yes | Exact verified integer `≥journal_first_offset`; also present in restricted correlation |
| `event_count` | yes | `last-first+1`, positive |
| `event_type_counts` | yes | Closed object with all six event-type slots present and non-negative |
| `ordered_payload_digest` | yes | Restricted exact verified digest; never a metric attribute |

```text
event_type_counts = {
  SessionStarted,
  SessionContextRebound,
  SessionDispatchLinked,
  ResearchCaptureAppended,
  ResearchFactAppended,
  ReferenceProbeLineageAppended
}

sum(event_type_counts.values) = event_count
journal_first_offset ≥ 1
journal_last_offset ≥ journal_first_offset
```

Offset `0` is reserved only for the logical genesis/empty-reducer boundary and can never identify an
accepted group.

The `apt.event.accepted` Counter is incremented from this verified record by each newly accepted
event-type count only. `submitted_retry`, `semantic_existing`, `conflict`, `error` and
`unknown_response` increment it by zero.

### `apt.replay.completed@1`

| Field | Required | Closed values / rule |
|---|---:|---|
| common envelope | yes | All common slots present; Operation/adapter/workflow outcome slots are canonical null; correlation includes exact `requested_o`; `effective_as_of` is exact after boundary verification and canonical null on pre-boundary rejection |
| `projection` | yes | `session_record`, `dispatch_scope`, `research_record` |
| `input_source` | yes, nullable | `checkpoint`, `empty_state`, `materialized_projection` only after verified source selection; canonical null on rejection before selection |
| `result` | yes | `success`, `rejected`, `pure_replay_fallback` |
| `replay_reason` | yes, nullable | Closed replay reason below; required when `result=rejected`, canonical null for `success/pure_replay_fallback` |
| `groups_folded` | yes | Non-negative |
| `events_folded` | yes | Non-negative |
| `boundary_lag_offsets` | yes, nullable | Exact non-negative `requested_o-effective_as_of` only after that boundary verifies; canonical null on pre-boundary rejection |
| `materialization_lag_offsets` | yes, nullable | For verified `input_source=materialized_projection`, correlation has exact `source_through_offset` and this field is exact non-negative `effective_as_of-source_through_offset`; both are canonical null for pre-boundary rejection and for `checkpoint/empty_state` |

The log is emitted outside `pure_reducer`; logging is not reducer I/O. A Query never rebuilds a
projection. `pure_replay_fallback` means newly owner-bound verified input, as specified in
[Projection Persistence](persistence-and-replay.md#projection-persistence).
The common-envelope `error_family` is exactly `replay_integrity` when `result=rejected` and
canonical null for `success/pure_replay_fallback`; `retryability=never` on rejection and canonical
null on success/fallback. Detailed replay classification exists only in `replay_reason`.
A rejection after boundary verification may retain the verified `effective_as_of` and derived
boundary lag. A rejection before boundary verification must keep both canonical null; telemetry
never invents a boundary or lag.
The same closed source matrix applies to the replay log and input-binding span:

```text
verified_source_selected ⇒ input_source∈{checkpoint,empty_state,materialized_projection}
rejected_before_source_selection ⇒ input_source=canonical null
```

A rejection after a source was verified may retain that exact source. Telemetry never infers one
from an intended query path, checkpoint presence or projection cache.

### Workflow Completion Logs

Every workflow record carries the common envelope with `workflow/workflow_result` non-null and
`operation/operation_outcome/adapter_outcome` canonical null. It also carries every workflow detail
slot below; slots not applicable to that workflow are canonical null.
`error_code/error_family` are canonical null for `completed`, and may be non-null closed values for
`partial/failed`; both slots remain present in every branch.

```text
workflow_result = {completed, partial, failed}
ensure_branch = {reused, created, failed}
rollover_branch = {not_requested, accepted, failed}
link_branch = {not_requested, accepted, failed}
capture_status = {captured, partial, missing}
capture_result = {accepted_new, submitted_retry, semantic_existing, failed}
fact_result = {not_attempted, all_accepted, partially_accepted, all_failed}
partition = {zero_new, mixed, all_new}
probe_result = {accepted_new, submitted_retry, semantic_existing, failed}

workflow_count_slots = {
  fact_attempt_count,
  fact_accepted_count,
  fact_failed_count,
  existing_exact_count,
  submitted_new_count,
  accepted_new_count
}
```

These sets list every permitted non-null value. A phase-specific slot is canonical null when that
phase was not reached or its value was not validly bound; `not_requested` is used only after a valid
decision explicitly skips the phase.

| Schema | Required applicable fields | Canonical-null workflow detail fields |
|---|---|---|
| `apt.session.workflow.completed@1` | `workflow=StartOrReuseSession`, `workflow_result`; each Session branch slot is a finite enum when reached and canonical null otherwise | `capture_status`, `capture_result`, `fact_result`, `fact_attempt_count`, `fact_accepted_count`, `fact_failed_count`, `partition`, `probe_result`, `existing_exact_count`, `submitted_new_count`, `accepted_new_count` |
| `apt.research.workflow.completed@1` | `workflow=CaptureAndEnrichResearch`, `workflow_result`, `capture_result`, `fact_result`, non-negative integer `fact_attempt_count`, `fact_accepted_count`, `fact_failed_count`; `capture_status` is finite after valid binding and canonical null otherwise | Session branches, `partition`, `probe_result`, `existing_exact_count`, `submitted_new_count`, `accepted_new_count` |
| `apt.probe.workflow.completed@1` | `workflow=IngestReferenceProbeLineage`, `workflow_result`, `probe_result`; after verified partitioning, finite `partition` plus non-negative integer `existing_exact_count`, `submitted_new_count`, `accepted_new_count`; before partitioning, all four are canonical null | Session branches, `capture_status`, `capture_result`, `fact_result`, `fact_attempt_count`, `fact_accepted_count`, `fact_failed_count` |

Research count arithmetic is exact:

```text
fact_attempt_count = fact_accepted_count + fact_failed_count
fact_result = not_attempted       iff fact_attempt_count = 0
fact_result = all_accepted        iff fact_attempt_count > 0
                                      ∧ fact_accepted_count = fact_attempt_count
fact_result = partially_accepted iff fact_accepted_count > 0 ∧ fact_failed_count > 0
fact_result = all_failed          iff fact_attempt_count > 0
                                      ∧ fact_failed_count = fact_attempt_count
```

Probe count arithmetic applies only after verified partitioning:

```text
0 ≤ accepted_new_count ≤ submitted_new_count
partition = zero_new iff submitted_new_count = 0 ∧ existing_exact_count > 0
partition = mixed    iff submitted_new_count > 0 ∧ existing_exact_count > 0
partition = all_new  iff submitted_new_count > 0 ∧ existing_exact_count = 0
probe_result ∈ {accepted_new,submitted_retry}
  ⇒ accepted_new_count = submitted_new_count
probe_result = semantic_existing
  ⇒ submitted_new_count = accepted_new_count = 0 ∧ existing_exact_count > 0
```

Counts summarize a request; the logger does not emit one record per selector or raw item.

## Trace Contract

Every span uses the common closed envelope plus the exact finite result attribute declared here:

```text
evidence_bind_result = {verified, not_required, rejected}
validation_result = {valid, rejected}
replay_bind_result = {bound, rejected}
replay_reduce_result = {success, rejected}
```

| Span name | Parent | Required safe attributes | Status rule |
|---|---|---|---|
| `apt.operation` | host span or root | `operation`, final `operation_outcome`; restricted correlation in span fields | Error only for `conflict/error`; semantic reuse is success |
| `apt.owner_evidence.bind` | operation | `evidence_kind`, `evidence_bind_result` | Never record evidence value |
| `apt.domain.validate` | operation | `operation`, `validation_result`, bounded `error_family` or canonical null | No payload or selector |
| `apt.aci.submit` | operation | `submission_kind`, final `adapter_outcome` | Acceptance only after verified ACI result; `unknown_response` is adapter-only |
| `apt.aci.receipt.verify` | `apt.aci.submit` | `receipt_verification`, `group_verification` | Failed verification is error |
| `apt.replay.input_bind` | query span | `projection`, present nullable `input_source`, `replay_bind_result` | Same source matrix as `apt.replay.completed@1`: verified selection gives the exact enum; pre-selection rejection gives canonical null |
| `apt.replay.reduce` | query span | `projection`, `groups_folded`, `events_folded`, `replay_reduce_result` | Pure reducer span timing is measured externally; reducer code performs no telemetry I/O |
| `apt.workflow.session` | host span or root | bounded Session branch enums, `workflow_result` | No session name |
| `apt.workflow.research` | host span or root | capture status/counts, `workflow_result` | No research content |
| `apt.workflow.probe` | committed-ingress span or root | partition/counts, `workflow_result` | No locator/recommendation text |

Sampling/export decisions occur after the business result and cannot suppress or alter journal
acceptance. Trace continuity is not replay continuity.

## Metric Schemas

Metric attributes are exactly those listed. Opaque IDs, digests, timestamps, offsets, names and
free text are forbidden labels.

| Metric | Instrument/unit | Exact attributes | Meaning |
|---|---|---|---|
| `apt.operation.invocations` | Counter / `{invocation}` | `operation`, `operation_outcome` | One increment per typed Operation result; `unknown_response` is impossible |
| `apt.operation.duration` | Histogram / `ms` | `operation` | End-to-end port duration |
| `apt.adapter.submissions` | Counter / `{submission}` | `submission_kind`, `adapter_outcome` | Adapter request outcomes, including `unknown_response` |
| `apt.adapter.duration` | Histogram / `ms` | `submission_kind` | Submit plus result verification duration |
| `apt.append.conflicts` | Counter / `{conflict}` | `operation`, `error_family` | Idempotency, semantic identity, CAS and evidence/profile conflict trends |
| `apt.profile.verification_failures` | Counter / `{failure}` | `profile_kind`, `reason` | Missing, mismatched or unregistered binding/receipt |
| `apt.aci.receipt_verification_failures` | Counter / `{failure}` | `submission_kind`, `reason` | Receipt/range/count/order/digest mismatch |
| `apt.event.accepted` | Counter / `{event}` | `event_type` | Add only newly accepted event counts from `apt.event.group.accepted@1`; retry/semantic-existing add zero |
| `apt.projection.reads` | Counter / `{read}` | `projection`, `result` | Query success/rejection/fallback, including rejection before source selection |
| `apt.projection.duration` | Histogram / `ms` | `projection`, `input_source` | Emitted only after verified source selection; input binding plus fold/build duration |
| `apt.projection.boundary_lag_offsets` | Histogram / `{offset}` | `projection` | Emit only after both `requested_o/effective_as_of` verify; exact difference, including post-boundary rejection |
| `apt.projection.materialization_lag_offsets` | Histogram / `{offset}` | `projection` | Emit only for verified `materialized_projection` boundary/source pairs; exact `effective_as_of-source_through_offset` |
| `apt.replay.integrity_failures` | Counter / `{failure}` | `projection`, `replay_reason` | Atomic group, prefix, checkpoint, schema or hash failure, including pre-source rejection without a duration series |
| `apt.workflow.results` | Counter / `{workflow}` | `workflow`, `workflow_result` | Closed completion outcome for all three Workflows |
| `apt.probe.partition` | Counter / `{ingestion}` | `partition`, `probe_result` | Emitted only after a verified finite zero/mixed/all-new partition; pre-partition failure has no partition series |
| `apt.telemetry.schema_violation` | Counter / `{violation}` | `signal_kind`, `reason` | Unknown/prohibited/invalid telemetry field attempts |

Closed metric enums:

```text
operation = {
  EnsureSession, StartNewSession, LinkSessionDispatch,
  AppendResearchCapture, AppendResearchFact, AppendReferenceProbeLineage
}
workflow = {StartOrReuseSession, CaptureAndEnrichResearch, IngestReferenceProbeLineage}
event_type = {
  SessionStarted, SessionContextRebound, SessionDispatchLinked,
  ResearchCaptureAppended, ResearchFactAppended, ReferenceProbeLineageAppended
}
projection = {session_record, dispatch_scope, research_record}
operation_outcome = {accepted_new, submitted_retry, semantic_existing, conflict, error}
adapter_outcome = {
  accepted_new, submitted_retry, semantic_existing, conflict, error, unknown_response
}
error_family = {
  authentication, authorization, schema, evidence, artifact, profile, idempotency,
  semantic_identity, cas, atomic_group, replay_integrity, not_found, internal
}
```

`result`, `reason`, `profile_kind`, `partition`, `submission_kind`, `input_source` and `signal_kind`
use these metric-specific closed values:

```text
submission_kind = {single, atomic}
partition = {zero_new, mixed, all_new}
input_source = {checkpoint, empty_state, materialized_projection}
profile_kind = {
  atomic_grouping, semantic_registry, reference_probe, event_schema_canonicalizer
}
profile_verification_reason = {
  missing, mismatched_id, mismatched_version, mismatched_digest,
  unregistered, invalid_registration_receipt
}
receipt_verification_reason = {
  missing, command_identity, range, count, event_order, payload_digest
}
replay_reason = {
  atomic_group, prefix_integrity, checkpoint_integrity, future_checkpoint,
  profile, schema, canonicalizer, projection_hash
}
projection_result = {success, rejected, pure_replay_fallback}
workflow_result = {completed, partial, failed}
probe_result = {accepted_new, submitted_retry, semantic_existing, failed}
signal_kind = {log, span, metric}
telemetry_violation_reason = {
  unknown_field, missing_required, invalid_enum, prohibited_field,
  high_cardinality_label
}
```

Each metric accepts only its semantically named result/reason enum above. An exporter cannot promote
the detailed `error_code` into a metric label.

## Required Failure Signals

| Failure seam | Log/trace outcome | Metric | Correctness alert |
|---|---|---|---|
| Same command identity, changed digest | `conflict`, exact restricted `error_code` | `apt.append.conflicts{error_family=idempotency}` | Any accepted changed-digest replacement is critical |
| Global `fact_id` divergent collision | `conflict` | `apt.append.conflicts{error_family=semantic_identity}` | Any duplicate accepted semantic owner is critical |
| Stale capture/fact/aggregate/delivery head | `conflict` | `apt.append.conflicts{error_family=cas}` | Accepted stale CAS is critical; rejection rate is trend-only |
| Required profile absent/mismatched | `error` | `apt.profile.verification_failures` | Any mutation accepted without exact profile is critical |
| Receipt/group mismatch | `error` | `apt.aci.receipt_verification_failures` | Any success returned after mismatch is critical |
| Incomplete/forked/digest-invalid replay | `rejected` | `apt.replay.integrity_failures` | Any projection value returned after integrity failure is critical |
| Future checkpoint selected for historical read | `rejected` | `apt.replay.integrity_failures{replay_reason=future_checkpoint}` | Any future-state leak is critical |
| Stale projection | `rejected` or `pure_replay_fallback` | `apt.projection.reads` | Query-side rebuild is critical |
| Prohibited content presented to telemetry | bounded schema violation only | `apt.telemetry.schema_violation` | Any exported prohibited content is security-critical |

Alerts evaluate observations but never authorize automatic APT control flow. Performance and volume
alerts require measured pilot thresholds; this spec does not invent production SLOs.

## Cardinality and Volume Budgets

| Surface | Budget | Enforcement obligation |
|---|---|---|
| Metric attributes | Only closed enums above; `operation≤6`, `workflow≤3`, `event_type≤6`, `projection≤3`, `submission_kind≤2`, `partition≤3`, `error_family≤13` | Unknown values map to no series and increment the bounded schema-violation counter |
| Metric instrument shape | Only the exact attribute columns declared per metric | Exporters may not add resource IDs, host paths, digests or error messages as labels |
| Completion logs | At most one operation completion and one adapter completion per port invocation; at most one workflow completion per workflow invocation | Retries are separate invocations but share restricted command correlation |
| Accepted-group logs | At most one summary record per verified command group | Use bounded counts; do not log every fact payload/member |
| Root traces | At most one Operation or Query root span per invocation plus only the bounded child-span kinds above | Sampling cannot affect business execution |
| Diagnostic detail | Opaque IDs/digests only in restricted logs/spans | Never copy them into metrics or dashboards as dimensions |

When a closed enum evolves, its schema version and series budget must be reviewed before emission.
Cardinality overflow is a telemetry defect, not permission to collapse distinct domain outcomes or
drop authoritative ACI data.

## Retention and Access

| Signal class | Retention contract | Access |
|---|---|---|
| Aggregated metrics | Finite owner-approved operational metrics retention policy; no per-ID dimensions | Operational readers |
| Internal bounded logs | Finite owner-approved operational log retention policy | Operational readers |
| Restricted correlation logs/spans | Shortest finite owner-approved incident/debug retention compatible with the pilot | Explicit restricted role; access itself auditable by the owning platform |
| Alert state/runbook notes | Must not outlive the source signal's permitted classification/retention without a separately governed incident record | Incident responders |
| Prohibited content | Zero telemetry retention | None |

Every configured sink must bind an exact retention-policy reference/version and classification
before readiness can pass. This documentation does not choose a deployment backend or duration.
Expiry/deletion of telemetry never deletes or changes ACI journal events, receipts, artifacts,
semantic keys, heads or APT projections. Conversely, ACI retention does not authorize copying
content into telemetry for longer retention.

## Dashboard and Runbook Views

| View | Minimum panels | Non-authority warning |
|---|---|---|
| Append health | invocation outcomes/duration, adapter outcomes, idempotency/semantic/CAS conflicts, receipt failures | Counts are diagnostic; inspect ACI receipt/journal for truth |
| Session wiring | ensure reused/created, rollover/link results and duration | Cannot infer current Session/link from metrics |
| Research capture | capture status counts and independent fact outcomes | Contains no question/answer/problem/notation text |
| Probe lineage | zero/mixed/all-new partitions, profile failures, atomic-group failures | Cannot infer source access/support from delivery count |
| Replay/projection | query results/duration/source lag, fallback and integrity failures | Cannot repair/rebuild or select a future checkpoint |
| Privacy/schema | redaction/schema violations by bounded reason | Never displays offending values |

First investigation steps:

| Alert | Severity | Read-only investigation |
|---|---|---|
| Accepted changed digest, divergent fact ID or stale CAS | critical | Compare authoritative command receipt, semantic key and aggregate head through ACI owner surfaces |
| Receipt/group verification failure | critical | Compare registered profile, receipt range/order/digest and journal prefix; do not repair from telemetry |
| Replay integrity/future-state leak | critical | Preserve requested/effective boundaries and verify prefix/checkpoint bindings; return no projection value |
| Profile verification failure | high | Verify exact ACI registration receipt and digest; do not emulate profile |
| Exported prohibited content | critical/security | Stop the affected telemetry sink through its owner process, preserve redacted metadata and review allowlist; do not alter APT facts |
| Sustained CAS/profile/replay rejection rate | warning/high by owner policy | Correlate restricted invocation IDs with authoritative failures; do not auto-retry from alert |

## Observability Invariants

| ID | Invariant | Formal |
|---|---|---|
| APT-OBS-I1 | Telemetry is never authority. | `telemetry∩authority_inputs=∅` |
| APT-OBS-I2 | Signal failure cannot change a result. | `emit_failure⇒Δ(operation_result,journal,projection)=0` |
| APT-OBS-I3 | Alerts cause no automatic APT command. | `alert⇒¬automatic_append∧¬automatic_retry∧¬automatic_rebuild` |
| APT-OBS-I4 | Accepted-event signals require verified durable acceptance. | `emit(accepted_event_signal)⇒verified(ACI_receipt_and_group)` |
| APT-OBS-I5 | Unknown adapter response has the sole closed InterfaceError mapping and only same-command retryability. | `adapter_outcome=unknown_response⇒operation_outcome=null ∧ error_code=APPEND_FAILED ∧ error_family=internal ∧ retryability=same-command ∧ ¬accepted_new` |
| APT-OBS-I6 | Raw and sensitive content never enters telemetry. | `prohibited_content∩(logs∪spans∪metrics∪alerts)=∅` |
| APT-OBS-I7 | Selectors never enter telemetry. | `selector_fields∩telemetry=∅` |
| APT-OBS-I8 | Metric labels are bounded. | `metric_attributes⊆declared_closed_enums` |
| APT-OBS-I9 | Correlation IDs never become metric labels. | `opaque_ids∩metric_attributes=∅` |
| APT-OBS-I10 | Replay reducer performs no telemetry I/O. | `IO(pure_reducer)=0` |
| APT-OBS-I11 | Query fallback is observed, never caused by a metric/alert. | `fallback⇒authoritative_projection_check∧¬telemetry_decision` |
| APT-OBS-I12 | Telemetry expiry changes no authoritative state. | `expire(telemetry)⇒Δ(ACI_authority)=0` |
| APT-OBS-I13 | Detailed errors remain restricted and bounded in metrics. | `metric_error=error_family(closed_error_code)` |
| APT-OBS-I14 | Probe telemetry does not assert use/support. | `observed(delivery)⇏access∨consulted∨support` |
| APT-OBS-I15 | Correlation uses the normalized command identity and never invents a capture `operation_id`. | `command_identity=AppendResearchCapture?capture_operation_id:operation_id` |
| APT-OBS-I16 | Every common and workflow-detail slot is present; non-applicable means canonical null. | `closed_signal⇒all_declared_slots_present ∧ nonapplicable(slot)⇒slot=null` |
| APT-OBS-I17 | Accepted event signals count only newly accepted, verified group members. | `Δapt.event.accepted=event_type_counts(verified_group) iff operation_outcome=accepted_new; retry∨semantic_existing⇒Δ=0` |
| APT-OBS-I18 | Workflow results and branches use only their finite enums. | `workflow_result∈{completed,partial,failed} ∧ workflow_details∈declared_closed_enums∪{null}` |
| APT-OBS-I19 | Replay rejection uses the common family plus one separate finite reason. | `replay.result=rejected⇒error_family=replay_integrity ∧ replay_reason∈closed_replay_reason; success∨fallback⇒error_family=null ∧ replay_reason=null` |
| APT-OBS-I20 | Accepted group offsets are positive; zero is logical genesis only. | `accepted_group⇒1≤first_offset≤last_offset ∧ offset(0)=logical_genesis_only` |
| APT-OBS-I21 | Causation preserves the owner-bound event-envelope mapping. | `causation_id=ACI_ref(command_identity(op)) ∧ receipt_id/event_id use own slots` |
| APT-OBS-I22 | Each span result and Workflow span result is finite and schema-specific. | `span_result∈{evidence_bind_result,validation_result,replay_bind_result,replay_reduce_result,workflow_result}` |
| APT-OBS-I23 | Lag exists only from verified operands; pre-boundary rejection invents neither boundary nor lag, and materialization lag is absent outside verified materialized input. | `verified(requested_o,effective_as_of)⇒boundary_lag_offsets=requested_o-effective_as_of; ¬verified(effective_as_of)⇒effective_as_of=null∧boundary_lag_offsets=null; verified(materialized_source)⇒materialization_lag_offsets=effective_as_of-source_through_offset; otherwise materialization_lag_offsets=null` |
| APT-OBS-I24 | Workflow count slots obey the per-schema null matrix and exact arithmetic. | `research⇒attempted=accepted+failed ∧ probe_counts=null; session⇒all_count_slots=null; probe_partitioned⇒0≤accepted_new≤submitted_new ∧ fact_counts=null; probe_prepartition⇒partition=null∧probe_counts=null` |
| APT-OBS-I25 | Replay log/span source exists only after verified selection, and source-labeled duration is absent before selection. | `verified_source_selected⇒same_exact(input_source_log,input_source_span) ∧ emit(projection.duration); rejected_before_source_selection⇒input_source_log=null ∧ input_source_span=null ∧ ¬emit(projection.duration) ∧ emit(projection.reads,rejected)` |

## Planned Test Derivation

The planned [TEST-SPEC](../TEST-SPEC.md) must derive at least:

1. schema tests for every required log, span and metric with missing/unknown/invalid fields;
2. one Operation outcome fixture for each of the six Operations and all applicable
   `accepted_new/submitted_retry/semantic_existing/conflict/error` branches, plus adapter-only
   `unknown_response` mapped exactly to `APPEND_FAILED/internal/same-command`;
3. correlation propagation from trusted invocation through adapter and verified receipt using
   normalized `command_identity`, including `capture_operation_id` for capture and no invented
   capture `operation_id`, without using IDs as metric labels;
4. raw artifact, checkpoint body, selector, question, answer, claim, problem, notation, locator,
   credential and free-form exception leak attempts across every signal surface;
5. allowlist redaction and bounded schema-violation behavior without recursion or copied value;
6. profile missing/mismatch, idempotency conflict, semantic collision, CAS conflict and atomic-group
   verification signals;
7. replay incomplete/forked/digest/hash/future-checkpoint failure signals with no returned
   authoritative projection; canonical-null effective/boundary lag on pre-boundary rejection,
   verified lag on post-boundary rejection, and materialization-lag formula/presence only for
   verified materialized input; replay log/span source parity, canonical-null source on
   pre-selection rejection, no source-labeled duration in that branch, and retained
   reads/integrity failure signals;
8. `apt.event.group.accepted@1` closed-shape/range/count/digest tests and proof that
   `apt.event.accepted` increments only for newly accepted verified members, never retry/existing,
   and rejects accepted-group offset zero as logical-genesis-only;
9. all common/workflow slots present with canonical null for every non-applicable branch;
10. finite result enums for evidence binding, domain validation, replay binding/reduction and all
    Workflow spans; Session ensure/reuse/rollover/link branch signals with all six count slots
    canonical null and without Session names;
11. research finite captured/partial/missing capture/fact results, exact
    attempted=accepted+failed arithmetic and three probe count slots canonical null, without
    research text;
12. probe finite zero/mixed/all-new partitions, exact partition/result arithmetic, pre-partition
    canonical-null probe counts, three fact count slots canonical null, and proof delivery
    telemetry asserts no use/support;
13. telemetry exporter/logging/tracing failure injection proving unchanged Operation result and no
    retry/control-flow effect;
14. cardinality-budget tests rejecting opaque IDs, digests and unknown values as metric labels;
15. retention/classification configuration checks and zero-retention handling for prohibited
    content; and
16. dashboard/runbook queries proving all operational views are read-only and non-authoritative.

All derivation links remain planned/not-run. This aspect does not modify TEST-SPEC and does not
authorize implementation or deployment.

## Connections

| Document | Type | Description |
|---|---|---|
| [SPEC.md](SPEC.md) | `derives-from` | Supplies the feature scope and exact concept registry. |
| [Operations](operations.md) | `observes` | Supplies the six mutation contracts and outcomes. |
| [Interfaces](interfaces.md) | `observes` | Supplies append/query/adapter and closed error boundaries. |
| [Events](events.md) | `observes-after-acceptance` | Supplies exact accepted event types; telemetry creates no new Event. |
| [Workflows](workflows.md) | `observes` | Supplies Session, research and probe orchestration branches. |
| [Queries](queries.md) | `observes` | Supplies projection names and historical read outcomes. |
| [Persistence and Replay](persistence-and-replay.md) | `constrained-by` | Keeps telemetry outside authority, reducer I/O and recovery. |
| [Rules](rules.md) | `governed-by` | Supplies privacy, telemetry non-authority, idempotency and profile rules. |
| [ACI observability](../../agents-communication-infra/specs/observability.md#trace-and-log-correlation) | `aligns-with` | Supplies cross-feature correlation and operational-plane separation. |
| [WORK-PACK](../WORK-PACK.md) | `planned-by` | Keeps runtime mutation and deployment blocked. |
