---
tags: [agents-communication-infra, spec, domain]
node_type: spec
is_session: false
layer: domain
nature: [technical, reference]
status: draft
version: 0.2.0
last_updated: 2026-07-21
---

# Domain: Agents Communication Infra

This model assigns stable identities to confirmed intent, protocol aggregates, physical attempts,
accepted publications and immutable artifacts. It does not make projections, adapters or the audit
ledger co-owners of runtime state.

## Entities

### ConfirmedDispatch

The immutable authorization captured from the human-approved pending sheet. A rerun or material
change creates another dispatch rather than mutating this entity.

| Field | Type | Required | Description |
|---|---|---:|---|
| `dispatch_id` | string | yes | Stable audit identity. |
| `source_bytes_artifact_id` | [ArtifactId](#artifactid) | yes | Exact approved bytes. |
| `dispatch_spec` | [DispatchSpec](#dispatchspec) | yes | Compiled executable contract. |
| `digest` | [ContentDigest](#contentdigest) | yes | Digest over the canonical frozen authority. |
| `authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | yes | Exclusive legacy/runtime owner chosen before confirmation. |
| `confirmed_by` | string | yes | Authenticated human principal. |
| `confirmed_at` | timestamp | yes | Recorded confirmation observation. |

**Identity:** `dispatch_id`; immutable after acceptance. During compatibility, one
[ConfirmedDispatch](#confirmeddispatch) creates at most one [Run](#run).

### Run

The lifecycle aggregate for one [ConfirmedDispatch](#confirmeddispatch). It owns runtime progress
but not the official audit-ledger row.

| Field | Type | Required | Description |
|---|---|---:|---|
| `run_id` | string | yes | Runtime aggregate identity. |
| `dispatch_id` | string | yes | Frozen authorization source. |
| `spec_digest` | [ContentDigest](#contentdigest) | yes | Exact confirmed spec. |
| `aggregate_version` | [AggregateVersion](#aggregateversion) | yes | Current contiguous CAS version. |
| `state_hash` | [ContentDigest](#contentdigest) | yes | Hash of canonical reduced state. |
| `opening_state` | [ReconciliationState](#reconciliationstate) | yes | Cross-store opening status. |
| `terminal_event_id` | string | no | Unique winning run terminal fact. |

**Lifecycle:** See [RunLifecycle](states.md#runlifecycle).

### Group

A versioned protocol aggregate within a [Run](#run). The aggregate identity is the tuple
`(run_id, group_id, group_version)`; revision creates a new immutable version.

| Field | Type | Required | Description |
|---|---|---:|---|
| `run_id` | string | yes | Owning run. |
| `group_id` | string | yes | Stable logical group identity. |
| `group_version` | integer | yes | Immutable protocol revision. |
| `aggregate_version` | [AggregateVersion](#aggregateversion) | yes | Current CAS version. |
| `policy_ref` | [VersionedReference](#versionedreference) | yes | Decision and visibility policy. |
| `eligible_seat_ids` | list<[SeatId](#seatid)> | yes | Frozen participation set when collection closes. |
| `reveal_manifest_id` | string | no | Manifest authorized for peer delivery. |
| `committed_result_id` | string | no | Unique result for this version. |

**Lifecycle:** See [GroupLifecycle](states.md#grouplifecycle).

### Seat

A logical quorum slot, independent of the model instance or retry that occupies it.

| Field | Type | Required | Description |
|---|---|---:|---|
| `seat_id` | [SeatId](#seatid) | yes | Logical participation identity. |
| `group_aggregate_id` | string | yes | Owning group version. |
| `role_contract_ref` | [VersionedReference](#versionedreference) | yes | Local objective and allowed output. |
| `agent_instance_id` | string | yes | Current selected provider/model instance. |
| `role_delta_ref` | [ArtifactId](#artifactid) | no | Declared, hashed deviation from the common base snapshot. |

**Invariant:** Retry never creates another seat. Replacement creates a new `agent_instance_id` and
inherits this identity only by an explicit accepted policy event.

### Attempt

One physical execution of a logical `operation_id`. Every retry creates a new `attempt_id` while
preserving the operation identity.

| Field | Type | Required | Description |
|---|---|---:|---|
| `attempt_id` | string | yes | Physical execution identity. |
| `operation_id` | string | yes | Stable logical operation. |
| `seat_id` | [SeatId](#seatid) | yes | Authorized logical contributor. |
| `agent_instance_id` | string | yes | Selected instance. |
| `provider_ref` | [VersionedReference](#versionedreference) | yes | Provider identity. |
| `adapter_ref` | [VersionedReference](#versionedreference) | yes | Adapter identity and version/digest. |
| `model_ref` | [VersionedReference](#versionedreference) | yes | Exact effective model. |
| `effective_input_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical input manifest actually materialized. |
| `request_digest` | [ContentDigest](#contentdigest) | yes | Idempotent adapter-start digest. |
| `worker_epoch` | integer | no | Durable single-host claim fence. |

**Lifecycle:** See [AttemptLifecycle](states.md#attemptlifecycle).

### Contribution

One receipt-verified message accepted as the official logical contribution for a seat, round and
message type. It is distinct from provider output, from the durable publication candidate, and from
the event that made the candidate eligible for protocol/quorum use.

| Field | Type | Required | Description |
|---|---|---:|---|
| `message_id` | string | yes | Logical publication identity. |
| `group_aggregate_id` | string | yes | Owning group version. |
| `seat_id` | [SeatId](#seatid) | yes | Authenticated logical author. |
| `operation_id` | string | yes | Capability-bound operation. |
| `round_id` | string | yes | Active protocol round. |
| `message_type` | string | yes | Phase/schema allowlisted type. |
| `payload_artifact_id` | [ArtifactId](#artifactid) | yes | Immutable content. |
| `accepted_event_id` | string | yes | Journal fact authorizing this contribution. |
| `publication_event_id` | string | yes | Earlier `publication.persisted` candidate fact verified by the parent. |
| `reply_to_message_ids` | list<string> | yes | Only messages already visible to the principal. |

**Uniqueness:** At most one accepted contribution per
`(group_aggregate_id, seat_id, round_id, message_type)`.

### PublicationCandidate

A schema-valid bus publication durably committed before acknowledgement. It is evidence eligible
for receipt verification, but is not an official [Contribution](#contribution) and cannot count
toward close, quorum, reveal or verdict until [VerifyPublicationReceipt](operations.md#verifypublicationreceipt)
accepts it.

| Field | Type | Required | Description |
|---|---|---:|---|
| `message_id` | string | yes | Stable candidate message identity. |
| `publication_event_id` | string | yes | Committed `publication.persisted` event. |
| `group_aggregate_id`, `attempt_id`, `operation_id`, `seat_id` | string | yes | Runtime-derived authenticated scope. |
| `round_id`, `message_type` | string | yes | Candidate logical key. |
| `payload_artifact_id` | [ArtifactId](#artifactid) | yes | Immutable candidate bytes. |
| `payload_hash` | [ContentDigest](#contentdigest) | yes | Canonical candidate digest. |
| `idempotency_key` | string | yes | Scoped retry identity. |
| `journal_offset` | [JournalOffset](#journaloffset) | yes | Committed candidate position. |
| `status` | string | yes | `active`, `officially_accepted`, or `abandoned`; transitions only by journal-writer CAS. |
| `official_accepted_event_id` | string | no | Set only by successful parent verification. |
| `abandoned_event_id` | string | no | Set only after the owning attempt is terminal `unknown`, no terminal evidence is recoverable and retry is authorized. |

**Lifecycle and uniqueness:** The authoritative candidate record owns one active reservation for
`(group_aggregate_id, seat_id, round_id, message_type)`. A receipt verifier may CAS
`active -> officially_accepted`. A retry-policy command may CAS `active -> abandoned` only after a
persisted terminal-unknown fact, a persisted no-recoverable-terminal-evidence determination and
authorization to retry. An abandoned candidate remains immutable evidence but releases the active
reservation; it can never later become official.

### EffectIntent

A durable request to execute an external or cross-store effect. Replay observes this entity but
never performs the effect directly.

| Field | Type | Required | Description |
|---|---|---:|---|
| `effect_id` | string | yes | Stable effect identity. |
| `effect_type` | string | yes | Adapter, tool, audit materialization or other declared kind. |
| `payload_digest` | [ContentDigest](#contentdigest) | yes | Immutable requested input. |
| `retry_class` | [RetryClass](#retryclass) | yes | Retry safety. |
| `claim_epoch` | integer | no | Current single-host claim fence. |
| `status` | [EffectStatus](#effectstatus) | yes | Durable outbox state. |

### Artifact

Immutable, content-addressed evidence metadata. Payload bytes live behind `storage_ref`; journal
events refer only to a finalized artifact whose digest, size and classification were validated.

| Field | Type | Required | Description |
|---|---|---:|---|
| `artifact_id` | [ArtifactId](#artifactid) | yes | Stable content-addressed identity. |
| `content_hash` | [ContentDigest](#contentdigest) | yes | Verified bytes digest. |
| `media_type` | string | yes | Validated media type. |
| `schema_ref` | [VersionedReference](#versionedreference) | no | Payload schema when structured. |
| `classification` | [ArtifactClassification](#artifactclassification) | yes | Access/redaction category. |
| `size_bytes` | integer | yes | Validated non-negative byte count. |
| `storage_ref` | string | yes | Opaque location controlled by the artifact boundary. |
| `tombstoned_at` | timestamp | no | Payload removal marker; provenance survives. |

### EffectiveInputArtifact

The immutable, content-addressed manifest of what an adapter actually presented to one
[Attempt](#attempt). It specializes the [Artifact](#artifact) evidence contract without claiming
visibility into provider-side transformations the runtime cannot observe.

| Field | Type | Required | Description |
|---|---|---:|---|
| `artifact_id` | [ArtifactId](#artifactid) | yes | Manifest artifact identity. |
| `attempt_id` | string | yes | Exactly one owning attempt. |
| `base_snapshot_ref` | [ArtifactId](#artifactid) | yes | Common peer context. |
| `role_delta_ref` | [ArtifactId](#artifactid) | no | Explicit hashed role-specific delta. |
| `entries` | ordered list<[EffectiveInputEntry](#effectiveinputentry)> | yes | Typed instructions, history, context, reveal and wrapper entries in presented order. |
| `tool_contract_refs` | ordered list<[VersionedReference](#versionedreference)> | yes | Tool names, descriptions and input schemas. |
| `response_schema_ref` | [VersionedReference](#versionedreference) | yes | Expected structured provider output. |
| `context_artifact_refs` | ordered list<[ArtifactId](#artifactid)> | yes | Context bodies and hashes. |
| `adapter_wrapper_refs` | ordered list<[ArtifactId](#artifactid)> | yes | Observable adapter-generated wrappers/flags. |
| `manifest_hash` | [ContentDigest](#contentdigest) | yes | Digest over canonical order and all component hashes. |

### RawProviderOutput

The immutable provider-native output for one attempt or exchange. It is evidence, not an accepted
[Contribution](#contribution), and provider-specific metadata cannot directly govern kernel state.

| Field | Type | Required | Description |
|---|---|---:|---|
| `artifact_id` | [ArtifactId](#artifactid) | yes | Output artifact identity. |
| `attempt_id` | string | yes | Source physical execution. |
| `exchange_id` | string | no | Provider exchange/turn when applicable. |
| `provider_ref` | [VersionedReference](#versionedreference) | yes | Exact provider source. |
| `model_ref` | [VersionedReference](#versionedreference) | yes | Exact effective model. |
| `provider_run_id` | string | no | Provider-native correlation identity. |
| `payload_hash` | [ContentDigest](#contentdigest) | yes | Verified immutable bytes. |
| `provider_metadata` | object | yes | Namespaced, non-authoritative metadata. |

### RevealManifest

The frozen set of contributions authorized for reveal after the collection barrier closes.

| Field | Type | Required | Description |
|---|---|---:|---|
| `reveal_manifest_id` | string | yes | Manifest identity. |
| `group_aggregate_id` | string | yes | Exact group version. |
| `round_id` | string | yes | Collection round. |
| `message_entries` | ordered list<[ManifestEntry](#manifestentry)> | yes | Accepted IDs and hashes only. |
| `manifest_hash` | [ContentDigest](#contentdigest) | yes | Canonical ordered-set digest. |
| `collection_closed_event_id` | string | yes | Barrier fact. |
| `reveal_event_id` | string | yes | Fact that grants delivery/read authority. |

**Invariant:** `collection.closed` freezes membership but does not grant peer-read. Only the
persisted `reveal.published` event does.

### GroupResult

The unique protocol commitment for one group version, separate from any narrative synthesis.

| Field | Type | Required | Description |
|---|---|---:|---|
| `group_result_id` | string | yes | Result identity. |
| `group_aggregate_id` | string | yes | Source group version. |
| `verdict` | string | yes | Schema-valid protocol outcome. |
| `decision_rule_ref` | [VersionedReference](#versionedreference) | yes | Applied deterministic rule. |
| `participant_seat_ids` | list<[SeatId](#seatid)> | yes | Participants counted. |
| `dissent_message_ids` | list<string> | yes | Preserved objections. |
| `result_payload_artifact_id` | [ArtifactId](#artifactid) | yes | Typed immutable envelope or synthesis. |
| `committed_event_id` | string | yes | Unique commit fact. |

## Value Objects

### DispatchSpec

| Field | Type | Constraint |
|---|---|---|
| `recipe_ref` | [VersionedReference](#versionedreference) | Digest-pinned. |
| `schema_refs` | ordered list<[VersionedReference](#versionedreference)> | Every executable input/output schema included. |
| `group_graph` | object | Finite and valid before confirmation. |
| `decision_policies` | object | Versioned and frozen. |
| `prompt_snapshot_refs` | ordered list<[ArtifactId](#artifactid)> | Content-addressed. |
| `capability_resolution` | object | Adapter/model/tool decisions and digests fixed. |
| `budgets` | object | Explicit finite limits. |

**Equality:** Canonical bytes and [ContentDigest](#contentdigest) are equal. This ratifies
**OQ-ACI4**: confirmed bytes, schema/recipe/profile versions, policies, prompt/snapshot references,
adapter version and capability resolution are frozen; clock/provider/tool observations arrive as
later events.

### AgentInvocationPlan

The provider-neutral scheduler decision before adapter materialization.

| Field | Type | Constraint |
|---|---|---|
| `attempt_id`, `operation_id`, `seat_id` | string | Runtime-authenticated identities. |
| `provider_ref`, `adapter_ref`, `model_ref` | [VersionedReference](#versionedreference) | Frozen selection. |
| `role_contract_ref`, `task_ref` | [VersionedReference](#versionedreference) | Compiled local contract. |
| `base_snapshot_ref`, `role_delta_ref` | [ArtifactId](#artifactid) | Shared base and optional declared delta. |
| `response_schema_ref`, `tool_profile_ref` | [VersionedReference](#versionedreference) | Frozen output/tool contracts. |
| `deadline` | timestamp | Frozen execution deadline. |
| `resource_budget` | [ResourceBudget](#resourcebudget) | Finite typed limits. |
| `sandbox_policy` | [SandboxPolicy](#sandboxpolicy) | Required launch isolation contract. |
| `authority_fence` | [ExecutionAuthorityFence](#executionauthorityfence) | Concrete legacy/runtime cutover fence. |

### MaterializedAgentInvocation

The adapter's deterministic translation of an [AgentInvocationPlan](#agentinvocationplan). It
references the exact observable input artifact and provider-native invocation controls, but does
not authorize execution or accept kernel state.

| Field | Type | Constraint |
|---|---|---|
| `plan_digest` | [ContentDigest](#contentdigest) | Exact source plan. |
| `effective_input_ref` | [ArtifactId](#artifactid) | Finalized [EffectiveInputArtifact](#effectiveinputartifact). |
| `provider_invocation_ref` | [ArtifactId](#artifactid) | Content-addressed native request/flags. |
| `materializer_ref` | [VersionedReference](#versionedreference) | Exact adapter materializer. |
| `materialization_digest` | [ContentDigest](#contentdigest) | Canonical equality identity. |

### AgentExecutionRequest

The sealed, immutable execution authority consumed by the effect worker after materialization.

| Field | Type | Constraint |
|---|---|---|
| `attempt_id`, `operation_id`, `seat_id` | string | Runtime-authenticated identities. |
| `provider_ref`, `adapter_ref`, `model_ref` | [VersionedReference](#versionedreference) | Confirmed selection; no provider-specific kernel branch. |
| `plan_digest`, `materialization_digest` | [ContentDigest](#contentdigest) | Bind the accepted plan and materialization. |
| `effective_input_ref`, `provider_invocation_ref` | [ArtifactId](#artifactid) | Exact finalized observable/native inputs. |
| `response_schema_ref`, `tool_profile_ref` | [VersionedReference](#versionedreference) | Frozen output/tool contracts. |
| `deadline` | timestamp | Frozen execution deadline. |
| `resource_budget` | [ResourceBudget](#resourcebudget) | Typed finite limits. |
| `sandbox_policy` | [SandboxPolicy](#sandboxpolicy) | Launcher-enforced isolation. |
| `authority_fence` | [ExecutionAuthorityFence](#executionauthorityfence) | Must remain current at effect claim/start. |
| `sealed_request_digest` | [ContentDigest](#contentdigest) | Equality identity for idempotent start. |

**Equality:** All fields compare by canonical value. Provider-specific invocation flags are adapter
materialization details recorded in the effective input, not fields that alter kernel semantics.

### BusPublication

| Field | Type | Constraint |
|---|---|---|
| `idempotency_key` | string | Non-empty; scoped to authenticated run/group/version/seat. |
| `operation_id` | string | Must equal the capability-bound operation. |
| `round_id` | string | Must equal an active allowed round. |
| `message_type` | string | Phase and schema allowlisted. |
| `reply_to_message_ids` | list<string> | All visible to the principal. |
| `payload` or `payload_ref` | object or [ArtifactId](#artifactid) | Exactly one; schema-valid, bounded and hashed. |

**Excluded authority fields:** `run_id`, `dispatch_id`, `group_id`, `group_version`, `seat_id`,
`agent_instance_id`, `attempt_id`, `actor_principal_id` and `phase`. The authenticated capability
supplies them; a conflicting payload field is rejected.

### PublicationReceipt

| Field | Type | Constraint |
|---|---|---|
| `receipt_version` | string | Supported receipt schema version. |
| `status` | string | Exactly `persisted_candidate`; never claims official acceptance. |
| `event_id` | string | Existing committed `publication.persisted` event. |
| `message_id` | string | Existing durable publication candidate. |
| `payload_hash` | [ContentDigest](#contentdigest) | Equals persisted payload hash. |
| `idempotency_key` | string | Equals persisted scoped key. |
| `journal_offset` | [JournalOffset](#journaloffset) | Committed global position. |

**Equality:** `receipt_version`, `status`, `event_id`, `message_id`, `journal_offset`, `payload_hash`
and `idempotency_key` must all match. The canonical serialized receipt is persisted and returned
byte-identically for an identical retry. Replay metadata is transport metadata outside this value
object. Verification requires a supported version, `status=persisted_candidate`, exact field
equality against one committed event, and authenticated attempt/operation/logical-key scope.

### AgentTerminalResult

Provider-neutral terminal envelope parsed under common rules for Codex, Claude and future adapters.

| Field | Type | Constraint |
|---|---|---|
| `result_version` | string | Supported terminal-result schema version. |
| `attempt_id`, `operation_id` | string | Must match the sealed request. |
| `completion_kind` | string | One of `completed`, `failed`, `cancelled`, `unknown`. |
| `raw_output_ref` | [ArtifactId](#artifactid) | Immutable provider-native evidence when observable. |
| `publication_receipt` | [PublicationReceipt](#publicationreceipt) | Required for an official bus result; nullable for non-publication terminals. |
| `provider_metadata` | object | Namespaced and non-authoritative. |

**Parsing:** Adapters may parse different native encodings, but must produce this envelope using the
same version/field/nullability rules. Unknown versions, ambiguous multiple receipts, prose-only
receipts, or a receipt inconsistent with `completion_kind` fail closed.

### EffectiveInputEntry

| Field | Type | Constraint |
|---|---|---|
| `entry_type` | string | `instruction`, `history`, `context`, `reveal_message`, `tool_contract`, `response_schema`, or `adapter_wrapper`. |
| `artifact_ref` | [ArtifactId](#artifactid) | Exact delivered bytes. |
| `content_hash` | [ContentDigest](#contentdigest) | Verified artifact digest. |
| `author_principal_id` | string | Required for authored/revealed messages; otherwise nullable. |
| `message_id` | string | Required for message/reveal entries; otherwise nullable. |
| `reveal_manifest_id` | string | Required for `reveal_message`; otherwise nullable. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | Policy authorizing delivery. |

### ResourceBudget

| Field | Type | Constraint |
|---|---|---|
| `max_wall_time_ms`, `max_input_tokens`, `max_output_tokens` | integer | Non-negative finite limits. |
| `max_tool_calls`, `max_payload_bytes`, `max_artifact_bytes` | integer | Non-negative finite limits. |
| `budget_policy_ref` | [VersionedReference](#versionedreference) | Frozen enforcement semantics. |

### SandboxPolicy

| Field | Type | Constraint |
|---|---|---|
| `policy_ref` | [VersionedReference](#versionedreference) | Frozen launcher policy. |
| `filesystem_scope`, `network_scope`, `process_scope` | object | Explicit allow/deny rules; default deny outside declared scope. |
| `credential_refs` | list<[VersionedReference](#versionedreference)> | Opaque launcher-resolved grants; secrets never enter durable payloads. |

### ExecutionAuthorityFence

| Field | Type | Constraint |
|---|---|---|
| `dispatch_id`, `run_id` | string | Exact runtime-owned execution. |
| `authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | Must equal `runtime-managed`. |
| `cutover_epoch` | integer | Monotonic authority epoch. |
| `legacy_watcher_disabled_evidence_ref` | [ArtifactId](#artifactid) | Concrete verified cutover evidence. |
| `fence_digest` | [ContentDigest](#contentdigest) | Equality identity checked before every external start. |

### SoleWriterEvidenceBundle

The immutable, host-scoped proof submitted to close EG-1 for one authoritative store and writer
version. It records evidence; it does not grant write authority by itself.

| Field | Type | Constraint |
|---|---|---|
| `store_ref`, `writer_ref`, `host_profile_ref` | [VersionedReference](#versionedreference) | Exact store, validated writer and host enforcement profile. |
| `writer_process_identity_ref` | [ArtifactId](#artifactid) | Evidence of the only process identity allowed to write. |
| `filesystem_acl_evidence_ref` | [ArtifactId](#artifactid) | File/directory permissions and effective-access inspection. |
| `writer_inventory_ref` | [ArtifactId](#artifactid) | Repository and deployed-path inventory, including legacy writers. |
| `negative_bypass_results_ref` | [ArtifactId](#artifactid) | Direct file access, alternate-process and legacy-path attempts must fail. |
| `auxiliary_lint_result_ref` | [ArtifactId](#artifactid) | Nullable defense-in-depth evidence; never sufficient alone. |
| `evidence_digest` | [ContentDigest](#contentdigest) | Canonical digest over the complete bundle manifest. |

**Acceptance:** all mandatory references must be verified for the target host and writer version;
an import scan or lint result alone leaves EG-1 open.

### RuntimeCommand

| Field | Type | Constraint |
|---|---|---|
| `command_id` | string | Globally unique. |
| `idempotency_key` | string | Unique in declared command scope. |
| `command_digest` | [ContentDigest](#contentdigest) | Canonical semantic request digest. |
| `aggregate_id` | string | Existing target aggregate. |
| `expected_version` | [AggregateVersion](#aggregateversion) | Required CAS expectation. |
| `prerequisite_heads` | ordered list<object> | Exact `(aggregate_id, expected_version, state_hash)` heads required atomically with target CAS. |
| `causation_id`, `correlation_id` | string | Stable provenance. |

### RuntimeEventEnvelope

| Field | Type | Constraint |
|---|---|---|
| `event_id`, `event_type` | string | Immutable identity and past-tense type. |
| `schema_ref`, `schema_digest` | [VersionedReference](#versionedreference), [ContentDigest](#contentdigest) | Exact payload contract. |
| `aggregate_id` | string | Owning stream. |
| `aggregate_version` | [AggregateVersion](#aggregateversion) | Contiguous within aggregate. |
| `journal_offset` | [JournalOffset](#journaloffset) | Globally increasing committed order. |
| `recorded_at` | timestamp | Journal observation; governs ordering only through offset. |
| `observed_at` | timestamp | Nullable external observation; never orders transitions. |
| `causation_id`, `correlation_id` | string | Provenance. |
| `payload_ref`, `payload_hash` | [ArtifactId](#artifactid), [ContentDigest](#contentdigest) | Immutable payload evidence. |

### AggregateVersion

Positive integer contiguous within one aggregate. Version zero means no accepted event. Equality is
integer equality.

### JournalOffset

Positive integer assigned by the one journal writer and globally ordered within the local database.
Equality is integer equality. This ratifies the offset part of **OQ-ACI1**.

### ContentDigest

Algorithm-qualified digest such as `sha256:<hex>`. Equality requires the same algorithm and bytes.

### ArtifactId

Opaque stable identity for one [Artifact](#artifact). Equality is exact string equality.

### SeatId

Opaque logical participation identity. Equality is exact string equality.

### VersionedReference

| Field | Type | Constraint |
|---|---|---|
| `name` | string | Namespaced identifier. |
| `version` | string | Explicit immutable version. |
| `digest` | [ContentDigest](#contentdigest) | Required where executable behavior or schema is selected. |

### ManifestEntry

| Field | Type | Constraint |
|---|---|---|
| `message_id` | string | Accepted contribution. |
| `payload_hash` | [ContentDigest](#contentdigest) | Matches accepted event. |

**Equality:** Ordered pair equality; manifests additionally compare canonical entry order and hash.

## Enums

### ExecutionAuthorityMode

| Value | Description |
|---|---|
| `legacy-managed` | Legacy session owns execution; no runtime Run exists. |
| `runtime-managed` | Runtime owns execution; compatibility marker cannot authorize a watcher. |

### ReconciliationState

| Value | Description |
|---|---|
| `pending` | Cross-store projection not yet verified. |
| `applied` | Canonical row was appended and verified. |
| `already_applied` | An identical canonical row already existed. |
| `divergent` | Same identity has different canonical content. |
| `reconciliation_required` | Effects/closure remain blocked pending explicit repair. |

### RetryClass

| Value | Description |
|---|---|
| `retryable` | May execute at least once with stable identity and reconciliation. |
| `non_retryable` | Must not repeat after unknown outcome. |

### EffectStatus

| Value | Description |
|---|---|
| `pending` | Durable and unclaimed. |
| `claimed` | Owned by the current claim epoch. |
| `succeeded` | Completion observation accepted. |
| `failed` | Known failure accepted. |
| `unknown` | External outcome cannot be safely reconciled. |

### ArtifactClassification

| Value | Description |
|---|---|
| `runtime-internal` | Runtime evidence with operator access. |
| `sensitive-input` | Effective input requiring restricted access. |
| `sensitive-output` | Raw provider output requiring restricted access. |
| `reveal-authorized` | Payload visible only through a persisted reveal manifest/policy. |
| `public` | Explicitly safe for general projection. |

## Ratified and deferred discovery questions

| Question | Disposition | Domain consequence |
|---|---|---|
| OQ-ACI4 | **Ratified** | [DispatchSpec](#dispatchspec) freezes reproducibility inputs; external observations are events. |
| OQ-ACI8 | **Ratified** | One content-addressed [EffectiveInputArtifact](#effectiveinputartifact) per [Attempt](#attempt) orders/hashes exact system, developer and user instructions, history, tool descriptions/schemas, response schema, context artifacts and adapter wrappers. Unobservable provider transformations remain named limitations. |
| OQ-ACI9 | **Boundary ratified; parameters deferred** | [EffectiveInputArtifact](#effectiveinputartifact) and [RawProviderOutput](#rawprovideroutput) are sensitive immutable [Artifact](#artifact) records; runtime-operator access and audited break-glass are the default, secrets are forbidden in durable payloads, and encryption becomes mandatory beyond local development. Concrete TTL, crypto-erasure periods and key management remain blocked on Slice-1 retention/credential ADRs. |

## Connections

| Document | Type | Description |
|---|---|---|
| [Discovery v0.2.1](discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Source decisions and OQ dispositions. |
| [Rules](rules.md) | `governed-by` | Cross-entity invariants and authority rules. |
| [Persistence and replay](persistence-and-replay.md) | `maps` | Candidate storage ownership and transaction contract. |
