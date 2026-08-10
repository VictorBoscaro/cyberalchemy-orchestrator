---
tags: [agents-communication-infra, spec, domain]
node_type: spec
is_session: false
layer: domain
nature: [technical, reference]
status: draft
version: 0.4.1
last_updated: 2026-08-10
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
| `authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | yes | Must equal `runtime-managed`; preserves the pre-confirmation cutover choice as accepted runtime evidence. |
| `confirmed_by` | string | yes | Authenticated human principal. |
| `confirmed_at` | timestamp | yes | Recorded confirmation observation. |

**Identity:** `dispatch_id`; immutable after acceptance. An accepted
[ConfirmedDispatch](#confirmeddispatch) creates exactly one [Run](#run); choosing
`legacy-managed` routes the dispatch away from `ConfirmRuntimeDispatch` and creates neither entity.

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
| `dispatch_id` | string | yes | Runtime-derived dispatch scope inherited from the owning run. |
| `operation_id` | string | yes | Stable logical operation. |
| `seat_id` | [SeatId](#seatid) | yes | Authorized logical contributor. |
| `agent_instance_id` | string | yes | Selected instance. |
| `provider_ref` | [VersionedReference](#versionedreference) | yes | Provider identity. |
| `adapter_ref` | [VersionedReference](#versionedreference) | yes | Adapter identity and version/digest. |
| `model_ref` | [VersionedReference](#versionedreference) | yes | Exact effective model. |
| `effective_input_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical input manifest actually materialized. |
| `request_digest` | [ContentDigest](#contentdigest) | yes | Idempotent adapter-start digest. |
| `worker_epoch` | integer | no | Durable single-host claim fence. |

**Reference-lineage extension status:** `dispatch_id` as a persisted attempt field is specified for
the next bounded slice and is not implemented by the Stage G pilot.

**Dispatch provenance:**

```text
Attempt(attempt_id).dispatch_id =
  Run(Group(Seat(Attempt(attempt_id).seat_id).group_aggregate_id).run_id).dispatch_id
```

`Attempt.dispatch_id` is derived by the runtime from the authorized seat/group/run ownership path;
it is never accepted from an agent-authored payload.

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

### HostTerminalResponseArtifact

The immutable producer-turn evidence record for exact terminal response bytes observed by the host.
The bytes live in a separately content-addressed [Artifact](#artifact), so two turns may produce
identical bytes without collapsing their attribution. It is the bounded compatibility evidence selected
by the accepted Phase-A output decision; it is distinct from [RawProviderOutput](#rawprovideroutput),
which preserves provider-native evidence, and from [GroupResult](#groupresult), which is a protocol
commitment.

| Field | Type | Required | Description |
|---|---|---:|---|
| `terminal_response_id` | string | yes | Stable evidence identity derived from the producer-turn tuple, not from payload bytes. |
| `payload_artifact_id` | [ArtifactId](#artifactid) | yes | Content-addressed exact terminal response bytes. |
| `dispatch_id` | string | yes | Parent dispatch from the verified [HostWorkflowBindingRef](#hostworkflowbindingref); it need not identify a `ConfirmedDispatch`. |
| `group_id` | string | yes | Producing workflow group. |
| `seat_id` | [SeatId](#seatid) | yes | Producing seat. |
| `turn_ordinal` | integer | yes | Producing host workflow turn. |
| `completion_kind` | string | yes | Host-observed terminal kind; only `completed` satisfies a success-required slot. |
| `content_hash` | [ContentDigest](#contentdigest) | yes | SHA-256 of the exact host-observed bytes. |
| `size_bytes` | integer | yes | Exact byte count. |
| `committed_event_id` | string | yes | Accepted [`host_workflow.terminal_response_committed`](events.md#host_workflowterminal_response_committed) fact. |

**Identity and authority:** at most one terminal-response evidence record exists per
`(dispatch_id, group_id, seat_id, turn_ordinal)`. An identical retry returns its persisted receipt;
different bytes or completion kind conflict. A caller-supplied path, a terminal-state row without
this artifact, or a repository file attributed after completion cannot satisfy `binding-output`.

### HostTerminalResponseReceipt

The canonical verification value returned after the artifact bytes and their journal fact are both
durable.

| Field | Type | Constraint |
|---|---|---|
| `receipt_version` | string | Exactly `aci.host-terminal-response-receipt/v1`. |
| `terminal_response_id` | string | Resolves to the matching [HostTerminalResponseArtifact](#hostterminalresponseartifact) evidence record. |
| `payload_artifact_id` | [ArtifactId](#artifactid) | Resolves to exact content-addressed bytes. |
| `dispatch_id`, `group_id`, `seat_id`, `turn_ordinal` | identity tuple | Exact producing turn identity. |
| `completion_kind` | string | Equals the committed host terminal observation. |
| `content_hash` | [ContentDigest](#contentdigest) | Equals both artifact metadata and exact bytes. |
| `size_bytes` | integer | Equals artifact metadata and exact bytes. |
| `event_id` | string | Matching accepted commit event. |
| `journal_offset` | [JournalOffset](#journaloffset) | Durable event position. |

The receipt is not self-authenticating: consumers verify it against evidence metadata, payload artifact bytes,
the owning workflow turn and the accepted event.

### HostWorkflowBindingRef

Immutable authority reference produced by the Stage-F host binding bridge for one workflow turn.
It binds `dispatch_id`, `group_id`, `seat_id`, `turn_ordinal`, prompt digest and manifest digest.
Legacy-managed execution verifies this reference against the orchestration journal; it does not
pretend that a `ConfirmedDispatch` or `Run` exists.

### SourceToSlotMapping

The mapping frozen at human confirmation that authorizes one completed producer turn to populate
one required consumer slot in the L0/L1 sequential slice.

| Field | Type | Required | Description |
|---|---|---:|---|
| `mapping_id`, `mapping_version` | string, integer | yes | Immutable mapping identity and CAS version. |
| `dispatch_id` | string | yes | Shared verified parent binding scope. |
| `connection_id` | string | yes | Declared topology edge; topology alone supplies no bytes. |
| `source_group_id`, `source_seat_id` | string, [SeatId](#seatid) | yes | Exact producer selector for this slice. |
| `target_group_id`, `target_seat_id`, `target_turn_ordinal` | string, [SeatId](#seatid), integer | yes | Exact consumer turn. |
| `slot_name`, `slot_ordinal` | string, integer | yes | Required slot identity; L0 requires ordinal `0`. |
| `required_completion_kind` | string | yes | L0 requires `completed`. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | yes | Authorizes this consumer to receive these exact bytes. |
| `confirmed_binding_digest` | [ContentDigest](#contentdigest) | yes | Proves mapping/policy was frozen at confirmation. |

**L0 cardinality:** exactly one mapping, producer and required slot per consumer turn. Fan-in,
optional slots and non-success completion policies are deferred to L2.

### WorkflowInputManifest

The canonical ordered materialization for one host workflow consumer turn. L0 contains exactly one
entry: mapping identity/version, verified terminal-response receipt identity, payload artifact ID,
content hash, size, slot name/ordinal and visibility policy. `manifest_digest` hashes canonical
manifest bytes.

### HostWorkflowTurnBinding

The launch authorization candidate binding one target [HostWorkflowBindingRef](#hostworkflowbindingref)
to one [WorkflowInputManifest](#workflowinputmanifest). It carries `binding_id`, target tuple,
mapping version, manifest digest, prerequisite journal heads and `binding_digest`. It becomes
launchable only through [AuthorizeHostWorkflowTurnLaunch](operations.md#authorizehostworkflowturnlaunch).

### AgentReferenceDelivery

The immutable acceptance record that binds one already-delivered Reference Scout bundle to the
exact [EffectiveInputArtifact](#effectiveinputartifact) entry materialized for one target
[Attempt](#attempt). This record is distinct from the existing Scout lifecycle fact
`reference_scout.bundle_delivered@1`: that earlier fact says the committed bundle reached the
ScoutRun's terminal delivery state, while this entity proves a later, separately authorized
delivery into one agent attempt.

**Contract status:** specified for the next bounded slice; not implemented. The source Scout
lifecycle is evidenced by [Stage G](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle);
this target-agent binding extends the canonical-input settlement of
[OQ-ACI8](../discovery/feature-discovery/agents-communication-infra.md#oq-aci8--canonical-effective-input)
without claiming that Stage G already implements it.

| Field | Type | Required | Description |
|---|---|---:|---|
| `agent_reference_delivery_id` | string | yes | Stable delivery identity. |
| `dispatch_id` | string | yes | Runtime-derived dispatch scope shared by ScoutRun and recipient. |
| `scout_run_id` | string | yes | Source ScoutRun whose committed bundle is already terminal-delivered. |
| `source_bundle_delivered_event_id` | string | yes | Existing accepted `reference_scout.bundle_delivered@1` lifecycle fact. |
| `bundle_artifact_id` | [ArtifactId](#artifactid) | yes | Exact immutable ordered recommendation bundle. |
| `bundle_digest` | [ContentDigest](#contentdigest) | yes | Verified digest of the source bundle bytes. |
| `recommendation_ids` | ordered list<string> | yes | Exact accepted recommendation membership and order carried by the bundle. |
| `target_attempt_id` | string | yes | Recipient attempt derived from authenticated delivery capability. |
| `target_seat_id` | [SeatId](#seatid) | yes | Recipient seat derived from the same capability and attempt. |
| `target_agent_instance_id` | string | yes | Recipient agent instance derived from the same capability and attempt. |
| `effective_input_artifact_id` | [ArtifactId](#artifactid) | yes | Finalized target manifest containing the exact bundle entry. |
| `effective_input_entry_ordinal` | integer | yes | Zero-based position of the unique bundle entry in the target manifest. |
| `effective_input_manifest_hash` | [ContentDigest](#contentdigest) | yes | Finalized manifest digest after inserting the bundle entry. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | yes | Delivery policy derived from the authenticated capability and frozen into the input entry. |
| `idempotency_key` | string | yes | Retry identity scoped to source ScoutRun and capability-derived target attempt. |
| `accepted_event_id` | string | yes | Committed `reference_scout.bundle_delivered_to_agent@1` fact. |
| `journal_offset` | [JournalOffset](#journaloffset) | yes | Global append position committed before acknowledgement. |

**Identity and uniqueness:** `agent_reference_delivery_id`; at most one accepted delivery exists per
`(scout_run_id, target_attempt_id)`. An identical retry returns the original canonical receipt.
Bundle, artifact, membership, digest, recipient, entry, policy or manifest drift conflicts rather
than creating another delivery. Reuse of the scoped idempotency key with any such drift is also a
conflict.

**Relational invariants:**

```text
committed_event =
  preceding accepted reference_scout.bundle_committed@1 where
    committed_event.scout_run_id = scout_run_id
    and committed_event.bundle_artifact_id = bundle_artifact_id
    and committed_event.bundle_digest = bundle_digest
    and committed_event.recommendation_ids = recommendation_ids

source_bundle_delivered_event_id identifies
  accepted reference_scout.bundle_delivered@1 where
    delivered_event.scout_run_id = scout_run_id
    and delivered_event.bundle_artifact_id = bundle_artifact_id
    and delivered_event.bundle_digest = bundle_digest
    and committed_event.journal_offset < delivered_event.journal_offset

bundle_digest = hash(Artifact(bundle_artifact_id).bytes)
ordered_recommendation_ids(Artifact(bundle_artifact_id).bytes) = recommendation_ids
delivered_event has no recommendation_ids field
recommendation_ids derives only from committed_event and Artifact(bundle_artifact_id).bytes

ScoutRun(scout_run_id).dispatch_id = dispatch_id
Attempt(target_attempt_id).dispatch_id = dispatch_id
Attempt(target_attempt_id).seat_id = target_seat_id
Attempt(target_attempt_id).agent_instance_id = target_agent_instance_id
EffectiveInputArtifact(effective_input_artifact_id).attempt_id = target_attempt_id
EffectiveInputArtifact(effective_input_artifact_id).manifest_hash = effective_input_manifest_hash
entries[effective_input_entry_ordinal] =
  unique reference_bundle(
    artifact_ref = bundle_artifact_id,
    content_hash = bundle_digest,
    agent_reference_delivery_id,
    visibility_policy_ref)

accepted_event_id identifies
  reference_scout.bundle_delivered_to_agent@1 where
    accepted_event.agent_reference_delivery_id = agent_reference_delivery_id
    and accepted_event.dispatch_id = dispatch_id
    and accepted_event.scout_run_id = scout_run_id
    and accepted_event.source_bundle_delivered_event_id = source_bundle_delivered_event_id
    and accepted_event.bundle_artifact_id = bundle_artifact_id
    and accepted_event.bundle_digest = bundle_digest
    and accepted_event.recommendation_ids = recommendation_ids
    and accepted_event.target_attempt_id = target_attempt_id
    and accepted_event.target_seat_id = target_seat_id
    and accepted_event.target_agent_instance_id = target_agent_instance_id
    and accepted_event.effective_input_artifact_id = effective_input_artifact_id
    and accepted_event.effective_input_entry_ordinal = effective_input_entry_ordinal
    and accepted_event.effective_input_manifest_hash = effective_input_manifest_hash
    and accepted_event.visibility_policy_ref = visibility_policy_ref
    and accepted_event.idempotency_key = idempotency_key
    and accepted_event.journal_offset = journal_offset
    and delivered_event.journal_offset < accepted_event.journal_offset
```

As part of `StartAgentAttempt`, the runtime preallocates `attempt_id`,
`agent_reference_delivery_id` and `accepted_event_id`, then atomically accepts the Attempt,
finalized effective-input artifact metadata, this delivery record,
`reference_scout.bundle_delivered_to_agent@1` and `attempt.requested`. The preallocated delivery ID
may therefore be embedded in the manifest before any member becomes accepted. No accepted attempt
or delivery exists if any member of that transaction fails, so the manifest reference is not
circular acceptance evidence and an immutable manifest is never amended after acceptance.

**Evidence boundary:** This entity proves only that the exact accepted bundle bytes were included
in the observable input manifest for the named attempt. It does not prove that the provider
received an unobservable transformation, that the agent opened or consulted a recommended source,
that the agent declared use of it, or that it supports a claim.

**Operation boundary:** target-agent delivery is an optional, atomic input-settlement step of the
existing [StartAgentAttempt](operations.md#startagentattempt) operation through the
capability-derived [ArtifactBoundary](interfaces.md#internal-artifact-boundary). Its dedicated
event is `reference_scout.bundle_delivered_to_agent@1`; the event aspect and SPEC registry are
updated later in this same bounded spec-authoring pass.

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

### PeerInputDelivery

The authoritative binding of one published reveal to one preallocated local target attempt.
It proves only that exact permitted peer entries were materialized into immutable observable input;
it neither launches a provider nor creates a generic inbox/read grant.

**Contract status:** specified for `SWU-ACI-BUS-DELIVERY-001`; not implemented. It specializes
[discovery section 5.1](../discovery/feature-discovery/agents-communication-infra.md#51-agent-input-bus-publication-and-reveal-delivery)
without promoting routing, inbox or provider-launch proposals.

| Field | Type | Required | Description |
|---|---|---:|---|
| `peer_input_delivery_id` | string | yes | Stable delivery identity. |
| `reveal_manifest_id` | string | yes | Persisted source manifest with an accepted `reveal.published` fact. |
| `source_group_aggregate_id` | string | yes | Exact group version shared by manifest and target seat. |
| `source_round_id` | string | yes | Exact revealed round. |
| `target_attempt_id` | string | yes | Preallocated local attempt selected by trusted scheduler context; no provider start is implied. |
| `target_seat_id` | [SeatId](#seatid) | yes | Seat derived from the target attempt, never from agent-authored input. |
| `peer_message_entries` | ordered list<[EffectiveInputEntry](#effectiveinputentry)> | yes | Exactly authorized manifest entries whose source seat differs from `target_seat_id`. |
| `effective_input_artifact_id` | [ArtifactId](#artifactid) | yes | Finalized immutable [EffectiveInputArtifact](#effectiveinputartifact). |
| `effective_input_manifest_hash` | [ContentDigest](#contentdigest) | yes | Canonical digest of the complete target input. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | yes | Exact fixed-proof delivery policy. |
| `idempotency_key` | string | yes | Retry identity scoped to manifest plus target attempt. |
| `accepted_event_id` | string | yes | Committed [`peer_input.materialized`](events.md#peer_inputmaterialized) fact. |
| `journal_offset` | [JournalOffset](#journaloffset) | yes | Position committed before acknowledgement. |

**Identity and uniqueness:** `peer_input_delivery_id`; at most one accepted delivery exists per
`(reveal_manifest_id, target_attempt_id)`. The semantic identity is the canonical digest of source
manifest, target attempt/seat, ordered peer entries, effective-input artifact/hash and policy.
Reusing either the scoped idempotency key or semantic uniqueness key with different bytes is a
permanent conflict.

```text
Seat(Attempt(target_attempt_id).seat_id).group_aggregate_id = source_group_aggregate_id
RevealManifest(reveal_manifest_id).group_aggregate_id = source_group_aggregate_id
RevealManifest(reveal_manifest_id).round_id = source_round_id
exists accepted reveal.published(reveal_manifest_id)

peer_message_entries =
  preserveManifestOrder(
    RevealManifest(reveal_manifest_id).message_entries
    where authorized(message_id, target_seat_id)
    and Contribution(message_id).seat_id != target_seat_id)

forall entry in peer_message_entries:
  entry.entry_type = reveal_message
  and entry.reveal_manifest_id = reveal_manifest_id
  and entry.artifact_ref = Contribution(entry.message_id).payload_artifact_id
  and entry.content_hash = ManifestEntry(entry.message_id).payload_hash
  and Artifact(entry.artifact_ref).content_hash = entry.content_hash

no entry in peer_message_entries:
  Contribution(entry.message_id).seat_id = target_seat_id
```

Acceptance is one journal transaction over the preallocated target identity: finalized artifact
metadata, `Attempt`, this delivery, `peer_input.materialized`, `attempt.requested` and an unclaimed
effect intent are all accepted or none are. `SWU-ACI-BUS-DELIVERY-001` stops before effect claim or
provider start. The fixed two-seat fixture asserts the symmetric A-to-B/B-to-A policy; the domain
rule itself is the policy-authorized peer filter above. Nothing here authorizes an agent-callable
read query.

**Created by:** [MaterializeAuthorizedPeerInput](operations.md#materializeauthorizedpeerinput).

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
| `binding_id`, `group_aggregate_id` | string | Canonical host-workflow binding and group derived by the scheduler authority. |
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

### PeerInputDeliveryReceipt

The byte-stable acknowledgement returned only after [PeerInputDelivery](#peerinputdelivery), its
event and authoritative constrained records commit.

| Field | Type | Constraint |
|---|---|---|
| `receipt_version` | string | Exactly `aci.peer-input-delivery-receipt/v1`. |
| `status` | string | Exactly `materialized`. |
| `event_id` | string | Existing committed `peer_input.materialized` event. |
| `peer_input_delivery_id` | string | Existing authoritative delivery. |
| `reveal_manifest_id` | string | Exact accepted source manifest. |
| `target_attempt_id` | string | Exact authorized recipient attempt. |
| `target_seat_id` | [SeatId](#seatid) | Must equal the target attempt's seat. |
| `effective_input_artifact_id` | [ArtifactId](#artifactid) | Finalized target artifact. |
| `effective_input_manifest_hash` | [ContentDigest](#contentdigest) | Exact canonical target-input digest. |
| `idempotency_key` | string | Exact scoped retry key. |
| `journal_offset` | [JournalOffset](#journaloffset) | Committed event position. |

**Equality:** every field compares by canonical value. An identical retry returns persisted
canonical bytes without appending an event or creating another artifact. Verification resolves all
fields against one committed event and the authoritative delivery row; transport replay metadata
is outside this value object.

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

**Reference-lineage extension status:** `reference_bundle` and
`agent_reference_delivery_id` are specified for the next bounded slice and are not implemented by
the Stage G pilot.

| Field | Type | Constraint |
|---|---|---|
| `entry_type` | string | `instruction`, `history`, `context`, `reveal_message`, `reference_bundle`, `tool_contract`, `response_schema`, or `adapter_wrapper`. |
| `artifact_ref` | [ArtifactId](#artifactid) | Exact delivered bytes. |
| `content_hash` | [ContentDigest](#contentdigest) | Verified artifact digest. |
| `author_principal_id` | string | Required for authored/revealed messages; otherwise nullable. |
| `message_id` | string | Required for message/reveal entries; otherwise nullable. |
| `reveal_manifest_id` | string | Required for `reveal_message`; otherwise nullable. |
| `agent_reference_delivery_id` | string | Required only for `reference_bundle`; identifies the accepted target-agent delivery. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | Policy authorizing delivery. |

For `entry_type=reference_bundle`, `artifact_ref` and `content_hash` equal the source
[AgentReferenceDelivery](#agentreferencedelivery)'s bundle artifact and `bundle_digest`, and
`agent_reference_delivery_id` identifies that delivery. The entry carries the Scout's ordered
recommendation bundle as context; it is not a generic peer-read grant and creates no authority to
read any other bus payload or artifact. Its `visibility_policy_ref` equals the source delivery's
capability-derived `visibility_policy_ref`.

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
| `legacy-managed` | Pre-confirmation routing choice: the legacy session owns execution; no runtime `ConfirmedDispatch` or `Run` exists. |
| `runtime-managed` | Accepted runtime confirmation freezes `ConfirmedDispatch` and creates exactly one `Run`; the compatibility marker cannot authorize a watcher. |

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
| [Discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Source decisions and OQ dispositions. |
| [Rules](rules.md) | `governed-by` | Cross-entity invariants and authority rules. |
| [Persistence and replay](persistence-and-replay.md) | `maps` | Candidate storage ownership and transaction contract. |
