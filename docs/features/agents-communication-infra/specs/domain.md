---
tags: [agents-communication-infra, spec, domain]
node_type: spec
is_session: false
layer: domain
nature: [technical, reference]
status: draft
version: 0.6.4
last_updated: 2026-09-01
---

# Domain: Agents Communication Infra

This model assigns stable identities to confirmed intent, protocol aggregates, physical attempts,
accepted publications and immutable artifacts. It does not make projections, adapters or the audit
ledger co-owners of runtime state.

## Entities

### ConfirmationObservation

One immutable trusted-host entity proving that a human approved one presented dispatch revision.
Chat and a future UI are equivalent transport surfaces: both must produce this same closed
canonical value through an admitted issuer. Its persistent identity is the issuer-scoped pair
`(issuer_ref, observation_id)`; its complete canonical bytes and digest are immutable integrity
evidence rather than an alternate identity.

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema` | string | yes | Must equal `aci.confirmation-observation@1`. |
| `observation_id` | string | yes | Stable issuer-scoped evidence identifier; retries reuse it. |
| `action` | string | yes | Must equal `approve_runtime_dispatch`. |
| `channel` | [ConfirmationChannel](#confirmationchannel) | yes | Surface on which the approval was observed. |
| `issuer_ref` | [VersionedReference](#versionedreference) | yes | Admitted host adapter identity and digest. |
| `issuer_evidence_ref` | [ArtifactId](#artifactid) | yes | Immutable evidence that the admitted issuer observed the interaction. |
| `issuer_evidence_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 digest of the exact issuer-evidence bytes. |
| `human_principal_id` | string | yes | Human principal derived from authenticated host context. |
| `dispatch_id`, `dispatch_revision` | string | yes | Exact approved presentation. |
| `presented_pending_sheet_digest` | [ContentDigest](#contentdigest) | yes | Digest of the exact canonical bytes shown for approval. |
| `presented_dispatch_spec_digest` | [ContentDigest](#contentdigest) | yes | Digest produced by the trusted preview compilation shown before approval. |
| `observed_at` | timestamp | yes | Issuer-recorded observation time; not event-ordering authority. |

The command boundary dereferences the observation, verifies its artifact digest, issuer,
authenticated principal, dispatch/revision and both presented digests, then recompiles the same
pending bytes. A mismatched principal, scope or preview digest rejects before runtime authority
exists.

**Identity:** `(issuer_ref, observation_id)`; immutable after first acceptance. Equal identities
with different canonical bytes are an integrity conflict.

**Created by:** the admitted trusted-host confirmation issuer; accepted and persisted only by
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).

### ConfirmedDispatch

The immutable authorization accepted from one verified
[ConfirmationObservation](#confirmationobservation). It names each authority layer explicitly;
neither a pending sheet, a compiled spec, a compatibility marker nor a transport receipt is the
whole authorization by itself. A rerun, new observation or material change creates another
dispatch rather than mutating this entity.

| Field | Type | Required | Description |
|---|---|---:|---|
| `dispatch_id` | string | yes | Stable audit identity. |
| `dispatch_revision` | string | yes | Exact revision presented to and approved by the human. |
| `pending_sheet_artifact_id` | [ArtifactId](#artifactid) | yes | Exact approved source bytes. |
| `pending_sheet_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the exact approved canonical bytes; BOM, newline and insignificant transport whitespace are rejected rather than admitted or repaired. |
| `dispatch_spec_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical server-compiled [DispatchSpec](#dispatchspec) bytes. |
| `dispatch_spec_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of those canonical spec bytes. |
| `confirmation_observation_artifact_id` | [ArtifactId](#artifactid) | yes | Immutable [ConfirmationObservation](#confirmationobservation) bytes from an admitted issuer. |
| `confirmation_observation_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the canonical observation bytes. |
| `capability_resolution_artifact_id` | [ArtifactId](#artifactid) | yes | Frozen effective semantic capability resolution. |
| `capability_resolution_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the canonical capability-resolution bytes. |
| `confirmed_turn_graph_artifact_id` | [ArtifactId](#artifactid) | yes | Server-derived [ConfirmedTurnGraph](#confirmedturngraph) artifact. |
| `confirmed_turn_graph_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the canonical confirmed graph bytes. |
| `continuation_mapping_set_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical ordered set of the two confirmation-frozen continuation mappings. |
| `continuation_mapping_set_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of that canonical mapping-set artifact. |
| `confirmed_authority_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical [ConfirmedAuthorityEnvelope](#confirmedauthorityenvelope) bytes. |
| `confirmed_authority_digest` | [ContentDigest](#contentdigest) | yes | Identity-level digest of the complete frozen authority envelope. |
| `execution_authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | yes | Must equal `runtime-managed`; preserves the pre-confirmation cutover choice as accepted runtime evidence. |
| `confirmed_by` | string | yes | Authenticated human principal. |
| `confirmed_at` | timestamp | yes | Observation time copied from the verified observation for indexed query only. |

**Identity:** `dispatch_id`; immutable after acceptance. An accepted
[ConfirmedDispatch](#confirmeddispatch) creates exactly one [Run](#run); choosing
`legacy-managed` routes the dispatch away from
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch) and creates neither entity. The
closed confirmation semantics are governed by
[Runtime Confirmation Authority v1](confirmation-authority.md).

**Identity and replay:** A deliberate rerun uses a new `dispatch_id`. A retry with the same
`dispatch_id` and the same `confirmed_authority_digest` returns the byte-identical first receipt,
including when it uses a new idempotency key, and creates no rows, events or effects. The same
`dispatch_id` with a different authority digest is a permanent `confirmed_authority_conflict` with
no mutation. Key/command-digest replay remains an additional transport-level check, not the
identity of the confirmed authority.

### ConfirmedTurnGraph

The server-derived, finite expansion of the confirmed logical workflow. The first admitted graph is
exactly `author:0 -> reviewer:0 -> author:1`: three turn identities, two ordered edges, one
continuation binding, two source-message identities and exactly two ordered
[ContinuationInputMapping](#continuationinputmapping) records. Callers may provide the logical
pending workflow but never this expanded authority or its identities.

| Field | Type | Required | Description |
|---|---|---:|---|
| `graph_id` | string | yes | Deterministically derived graph identity. |
| `dispatch_id`, `run_id` | string | yes | Owning confirmed authority and run. |
| `dispatch_spec_digest` | [ContentDigest](#contentdigest) | yes | Binds the projection to the exact confirmed canonical spec. |
| `graph_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical expanded graph bytes. |
| `graph_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the canonical graph bytes. |
| `continuation_id` | string | yes | Sole preallocated author-turn continuation boundary. |
| `mapping_set_artifact_id` | [ArtifactId](#artifactid) | yes | Canonical two-mapping set. |
| `mapping_set_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of that mapping set. |
| `node_count`, `edge_count`, `mapping_count` | integer | yes | Must equal `3`, `2` and `2`. |
| `identity_derivation_ref` | [VersionedReference](#versionedreference) | yes | Exact algorithm contract used for all preallocated IDs. |

For this bounded version, each declared `operation_id` is the stable turn identity and is paired
with its seat, group, round, role and turn ordinal. The bound [DispatchSpec](#dispatchspec).`group_graph` contains
`loop_ceiling=1`; any extra/missing node, edge, mapping or continuation binding rejects
confirmation.

**Identity:** `graph_id`; immutable after confirmation.

**Created by:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).

### Run

The lifecycle aggregate for one [ConfirmedDispatch](#confirmeddispatch). It owns runtime progress
but not the official audit-ledger row.

| Field | Type | Required | Description |
|---|---|---:|---|
| `run_id` | string | yes | Runtime aggregate identity. |
| `dispatch_id` | string | yes | Frozen authorization source. |
| `dispatch_spec_digest` | [ContentDigest](#contentdigest) | yes | Exact canonical confirmed spec. |
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

### AgentContinuation

One bounded opportunity to resume a terminal agent turn after declared input dependencies become
satisfied. It preserves an exact reconstruction path whether or not the host retains a
provider-native session. A continuation is not a running [Attempt](#attempt), a generic peer inbox,
or authority for the agent to poll the bus.

**Authority:** [ACI-CONT-001](../../../decisions/aci-resumable-agent-continuation.md).

| Field | Type | Required | Description |
|---|---|---:|---|
| `continuation_id` | string | yes | Stable identity preallocated by the confirmed turn graph for one wait/resume boundary. |
| `dispatch_id` | string | yes | Runtime-derived parent scope. |
| `seat_id` | [SeatId](#seatid) | yes | Logical seat that may continue. |
| `agent_instance_id` | string | yes | Instance eligible for same-session resume while its handle remains valid. |
| `source_attempt_id` | string | yes | Terminal attempt whose work and context are being continued. |
| `source_turn_ordinal` | integer | yes | Completed turn; non-negative. |
| `target_turn_ordinal` | integer | yes | Exactly `source_turn_ordinal + 1` in the bounded slice. |
| `input_mapping_ids` | ordered list<string> | yes | Exactly two confirmed [ContinuationInputMapping](#continuationinputmapping) identities: prior author output, then review output. |
| `awaited_mapping_ids` | ordered list<string> | yes | Non-empty subset of `input_mapping_ids` whose official contributions were absent at suspension. |
| `context_snapshot_ref` | [ArtifactId](#artifactid) | yes | Immutable reconstruction base accepted before suspension. |
| `provider_continuation_ref` | string | no | Opaque, access-controlled adapter handle; never execution authority. |
| `provider_continuation_ref_digest` | [ContentDigest](#contentdigest) | no | Equality/correlation digest without exposing the opaque handle. |
| `resume_policy_ref` | [VersionedReference](#versionedreference) | yes | Bounded policy frozen at confirmation. |
| `deadline` | timestamp | yes | Time after which no resume may be authorized. |
| `state` | string | yes | Current [AgentContinuationLifecycle](states.md#agentcontinuationlifecycle) state. |
| `resume_mode` | string | no | Set at authorization to `same_session` or `reconstruct`; absent before authorization. |
| `version` | integer | yes | Aggregate compare-and-set version. |

```text
Attempt(source_attempt_id).dispatch_id = dispatch_id
Attempt(source_attempt_id).seat_id = seat_id
Attempt(source_attempt_id).agent_instance_id = agent_instance_id
Attempt(source_attempt_id).state in {completed, failed, cancelled, unknown}
target_turn_ordinal = source_turn_ordinal + 1
resume_mode = same_session => provider_continuation_ref exists
                            and target_attempt.agent_instance_id = agent_instance_id
resume_mode = reconstruct => definitive_provider_continuation_loss_event exists
                           and target_attempt.seat_id = seat_id
                           and target_attempt.agent_instance_id != agent_instance_id
unknown_resume_effect_outcome => no reconstruction_start_effect
```

The provider handle may improve continuity, but correctness derives from
`context_snapshot_ref`, the confirmed continuation input mappings and the newly materialized
[EffectiveInputArtifact](#effectiveinputartifact). Definitive handle loss may select the confirmed
reconstruction branch. An unknown resume outcome cannot silently start a replacement because that
could duplicate physical work.

**Lifecycle:** [AgentContinuationLifecycle](states.md#agentcontinuationlifecycle).
**Operations:** [SuspendAgentContinuation](operations.md#suspendagentcontinuation),
[ResumeAgentContinuation](operations.md#resumeagentcontinuation),
[ReconstructAgentContinuation](operations.md#reconstructagentcontinuation), and
[CancelAgentContinuation](operations.md#cancelagentcontinuation).

### ContinuationInputMapping

One confirmation-frozen authorization for an official bus contribution from an exact producer turn
to occupy one slot in a later continuation input. It is runtime-managed and is not a bus read grant
for either agent.

| Field | Type | Required | Description |
|---|---|---:|---|
| `mapping_id`, `mapping_version` | string, integer | yes | Immutable mapping identity and frozen schema/version marker; this slice fixes `mapping_version=1`. |
| `dispatch_id`, `continuation_id` | string | yes | Exact parent and confirmation-preallocated continuation scope. |
| `source_group_id`, `source_seat_id`, `source_operation_id` | string, [SeatId](#seatid), string | yes | Exact authenticated producer selector. |
| `source_turn_ordinal`, `source_round_id` | integer, string | yes | Exact logical turn and protocol round bound to `source_operation_id` by the confirmed turn graph. |
| `source_message_id`, `source_message_type` | string | yes | Deterministically preallocated logical publication identity and allowlisted official contribution type. |
| `target_seat_id`, `target_turn_ordinal` | [SeatId](#seatid), integer | yes | Exact continuation consumer. |
| `slot_name`, `slot_ordinal` | string, integer | yes | Canonical target slot; the bounded slice fixes author output before review output. |
| `visibility_policy_ref` | [VersionedReference](#versionedreference) | yes | Authorizes delivery of the exact contribution artifact to the target turn. |
| `confirmed_binding_digest` | [ContentDigest](#contentdigest) | yes | Proves selector, order and policy were frozen at confirmation. |

The bounded workflow contains exactly two such mappings. The `continuation_id` and each
`source_message_id` are deterministically preallocated at confirmation from the frozen dispatch and
turn graph; suspension must consume that same continuation identity. Each message resolves only
to the unique official [Contribution](#contribution) whose message, group, seat, operation, round and
type all match. The same message's [PublicationCandidate](#publicationcandidate) identifies the
owning attempt; that attempt must match the mapped operation/seat/dispatch and be terminal
`completed`. Zero or multiple matching chains reject. A candidate, raw provider output, path or
agent-supplied identifier cannot satisfy the mapping.

**Identity:** `mapping_id`; immutable after confirmation.

**Created by:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).

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
| `command_id` | string | yes | Accepted command that requested the effect. |
| `requested_event_id` | string | yes | Committed event that made the intent durable. |
| `effect_type` | string | yes | Adapter, tool, audit materialization or other declared kind. |
| `payload_ref` | [ArtifactId](#artifactid) | yes | Finalized immutable requested-input artifact. |
| `payload_digest` | [ContentDigest](#contentdigest) | yes | Immutable requested input. |
| `retry_class` | [RetryClass](#retryclass) | yes | Retry safety. |
| `status` | [EffectStatus](#effectstatus) | yes | Durable outbox state. |
| `attempt_count` | integer | yes | Starts at zero and advances only through the fenced claim/attempt protocol. |
| `claimed_by` | nullable string | yes | Current worker identity; `null` means the intent has never been claimed. |
| `claim_epoch` | nullable integer | yes | Current single-host claim fence; `null` means no claim epoch has been allocated. |
| `outcome_event_id` | nullable string | yes | Terminal accepted outcome fact; `null` means no outcome has been accepted. |
| `outcome_digest` | nullable [ContentDigest](#contentdigest) | yes | Immutable outcome comparison digest; `null` means no outcome has been accepted. |

For the confirmation-opening intent, acceptance fixes `effect_type=audit_opening`,
`retry_class=retryable`, `status=pending`, `attempt_count=0`, `claimed_by=null`,
`claim_epoch=null`, `outcome_event_id=null` and `outcome_digest=null`. These required nullable fields
make the closed initial projection explicit: `null` means never claimed and no accepted outcome. Its
payload requests audit-appender contract `0.6.4`; the confirmation writer never claims or executes
it.

**Identity:** `effect_id`; immutable after acceptance.

**Created by:** Operation-specific command acceptance. The confirmation-opening intent is created
by [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).

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

### ExecutionPolicySyntheticLineageReceipt

The closed, test-only persistence receipt for the exact seven POLICY-000 oracle members. It proves
only which non-executable synthetic unit committed with its ordered member content identities. The
transactional tests and post-close reopen observations, not the receipt alone, prove all-or-none
atomicity, durability and exact byte reproduction. It is not a [ConfirmedDispatch](#confirmeddispatch),
[Run](#run), [AgentInvocationPlan](#agentinvocationplan),
[AgentExecutionRequest](#agentexecutionrequest), [RuntimeEventEnvelope](#runtimeeventenvelope),
[EffectIntent](#effectintent), provider, opening or current-fence fact and cannot satisfy any
production authority parser or gate.

Its exact schema literal is `aci.execution-policy-synthetic-lineage-receipt@1`, and it has only the
fields below:

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema` | string | yes | Exactly `aci.execution-policy-synthetic-lineage-receipt@1`. |
| `authority` | string | yes | Exactly `test-only-non-executable`. |
| `synthetic_key` | string | yes | Caller-selected idempotency key scoped only to this isolated test seam. |
| `lineage_identity` | string | yes | Immutable logical identity for the synthetic unit; never an execution identity. |
| `members` | ordered list<[ExecutionPolicySyntheticLineageMember](#executionpolicysyntheticlineagemember)> | yes | Exactly seven closed bindings in the fixed order defined below. |
| `unit_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the exact canonical lineage-unit preimage defined below. |

The member list is exactly:

| Ordinal | Name | Exact POLICY-000 member |
|---:|---|---|
| 0 | `budget_policy` | `aci.budget-policy@1` reference target. |
| 1 | `sandbox_enforcement_policy` | `aci.sandbox-enforcement-policy@1` reference target. |
| 2 | `resource_budget` | [ResourceBudget](#resourcebudget). |
| 3 | `sandbox_policy` | [SandboxPolicy](#sandboxpolicy). |
| 4 | `combined_oracle` | [ExecutionPolicyOracleFixture](#executionpolicyoraclefixture). |
| 5 | `harness_fence_preimage` | Exact `aci.execution-authority-fence-harness-preimage@1` bytes. |
| 6 | `harness_fence_document` | [ExecutionAuthorityFenceHarness](#executionauthorityfenceharness). |

The lineage-unit preimage is the closed object with exact schema
`aci.execution-policy-synthetic-lineage-unit@1` and exactly `schema`, `authority`,
`lineage_identity` and `members`. `unit_digest` is
`sha256(aci-cjson-1(lineage_unit_preimage))`; `synthetic_key` is excluded so transport replay cannot
redefine the persisted content identity. Every member's artifact bytes must reproduce its stored
content digest before acceptance and after reopen.

**Identity:** `lineage_identity`. `synthetic_key` and `lineage_identity` are separately unique.
An identical key or identity with the same `unit_digest` converges on the first receipt; either one
with a different `unit_digest` is a permanent conflict.

**Created by:** only the isolated test-only synthetic-lineage harness. The receipt and its seven
member bindings commit with the seven finalized artifacts in one SQLite transaction or none do.

### ExecutionPolicyFakeDenialReceipt

The closed, durable result of one POLICY-002 test-only launch-admission probe over an exact
[ExecutionPolicySyntheticLineageReceipt](#executionpolicysyntheticlineagereceipt). It proves only
that the reviewed all-zero [ResourceBudget](#resourcebudget) and deny-all
[SandboxPolicy](#sandboxpolicy) produced the mandatory `denied` decision without crossing an
external boundary. It is not an [EffectIntent](#effectintent), runtime event,
[AgentExecutionRequest](#agentexecutionrequest), provider observation, production
[ExecutionAuthorityFence](#executionauthorityfence) or host-enforcement result.

Its exact schema literal is `aci.execution-policy-fake-denial-receipt@1`, and it has only these
fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema` | string | yes | Exactly `aci.execution-policy-fake-denial-receipt@1`. |
| `authority` | string | yes | Exactly `test-only-non-executable`. |
| `denial_key` | string | yes | Caller-selected transport idempotency key scoped only to the isolated test seam. |
| `lineage_identity` | string | yes | Exact persisted POLICY-001 lineage identity; never a Run, Attempt or effect identity. |
| `lineage_unit_digest` | [ContentDigest](#contentdigest) | yes | Exact `unit_digest` reproduced by reopening the persisted lineage. |
| `resource_budget_digest` | [ContentDigest](#contentdigest) | yes | Exact all-zero POLICY-000 ResourceBudget digest. |
| `sandbox_policy_digest` | [ContentDigest](#contentdigest) | yes | Exact deny-all POLICY-000 SandboxPolicy digest. |
| `decision` | string | yes | Exactly `denied`; no success, unknown or attempted variant exists in v1. |
| `reason_codes` | ordered list<string> | yes | Exactly `resource.max_wall_time_ms.zero`, then `sandbox.process.no-executable-grant`. |
| `denial_digest` | [ContentDigest](#contentdigest) | yes | SHA-256 of the exact canonical denial preimage defined below. |

The denial preimage has exact schema `aci.execution-policy-fake-denial@1` and every receipt field
except `denial_key` and `denial_digest`. For the reviewed POLICY-001 fixture, its canonical bytes
and digest are:

```text
{"authority":"test-only-non-executable","decision":"denied","lineage_identity":"policy-lineage-oracle-001","lineage_unit_digest":"sha256:f702b9d2954307a91039cd3ea92285cb464c2c997c2166c0d68c446513a2801d","reason_codes":["resource.max_wall_time_ms.zero","sandbox.process.no-executable-grant"],"resource_budget_digest":"sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836","sandbox_policy_digest":"sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a","schema":"aci.execution-policy-fake-denial@1"}
sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399
```

With `denial_key=policy-denial-command-001`, the complete canonical receipt bytes and content digest
are:

```text
{"authority":"test-only-non-executable","decision":"denied","denial_digest":"sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399","denial_key":"policy-denial-command-001","lineage_identity":"policy-lineage-oracle-001","lineage_unit_digest":"sha256:f702b9d2954307a91039cd3ea92285cb464c2c997c2166c0d68c446513a2801d","reason_codes":["resource.max_wall_time_ms.zero","sandbox.process.no-executable-grant"],"resource_budget_digest":"sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836","sandbox_policy_digest":"sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a","schema":"aci.execution-policy-fake-denial-receipt@1"}
sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11
```

**Identity:** `lineage_identity`. `denial_key` and `lineage_identity` are independent uniqueness
axes. Reuse with the same `denial_digest` returns the first persisted receipt; reuse with a changed
digest is a permanent conflict with no second denial row.

**Created by:** only the POLICY-002 test-only fake-denial harness after reopening and revalidating
the exact POLICY-001 lineage. One canonical receipt row commits or none does; no artifact, runtime
aggregate, event, effect or external action is created.

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

### ConfirmedAuthorityEnvelope

The closed canonical value whose digest is the identity-level meaning of one accepted confirmation.
It contains frozen semantic authority digests, not transport-attempt metadata; client idempotency
keys, command IDs, aggregate versions, journal offsets, receipts and writer timestamps are excluded
so a transport retry cannot redefine what the human approved.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Must equal `aci.confirmed-authority@1`. |
| `dispatch_id`, `dispatch_revision` | string | Must match the verified presentation and observation. |
| `execution_authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | Must equal `runtime-managed`. |
| `pending_sheet_digest` | [ContentDigest](#contentdigest) | Exact approved source bytes. |
| `dispatch_spec_digest` | [ContentDigest](#contentdigest) | Canonical server-compiled spec bytes. |
| `confirmation_observation_digest` | [ContentDigest](#contentdigest) | Verified human-approval observation bytes. |
| `capability_resolution_digest` | [ContentDigest](#contentdigest) | Frozen semantic capability resolution bytes. |
| `confirmed_turn_graph_digest` | [ContentDigest](#contentdigest) | Server-derived bounded graph bytes. |
| `mapping_set_digest` | [ContentDigest](#contentdigest) | Ordered two-mapping-set bytes. |
| `derivation_schema` | string | Must equal `aci.confirmed-dispatch-id-preimage@1`. |
| `identity_derivation_digest` | [ContentDigest](#contentdigest) | Canonical digest of the complete `aci.confirmed-dispatch-identity-derivation-contract@1` document used to derive every runtime identity. |
| `payload_schema_bundle_digest` | [ContentDigest](#contentdigest) | Canonical digest of the closed `aci.runtime-confirmation-payload-schemas@1` bundle containing the exact event, effect and stable-receipt schemas. |
| `schema_versions` | map | Complete command/event/payload/recipe/identity version set. |

**Equality:** canonical `aci-cjson-1` bytes and their SHA-256 digest are equal. All referenced
artifacts verify before the envelope can be accepted.

### ConfirmedDispatchIdentitySeed

The acyclic input to the versioned ID derivation calculation. It is constructed after the pending
source compiles to a verified spec and before graph, mapping, event, effect and receipt artifacts
are built.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Must equal `aci.confirmed-dispatch-id-preimage@1`. |
| `kind` | string | One closed derivation kind with a fixed output prefix. |
| `dispatch_id` | string | Exact approved dispatch identity. |
| `dispatch_spec_digest` | [ContentDigest](#contentdigest) | Canonical compiled spec bytes. |
| `coordinates` | ordered list<string> | Closed kind-specific coordinates; integers use shortest base-10 strings. |

**Equality:** canonical `aci-cjson-1` bytes. The seed never contains an ID it is being used to
derive and never contains `confirmed_authority_digest`, which prevents a digest/identity cycle.

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

### ExecutionPolicySyntheticLineageMember

One closed ordered content binding inside an
[ExecutionPolicySyntheticLineageReceipt](#executionpolicysyntheticlineagereceipt). It has exactly
`ordinal`, `name`, `artifact_id` and `content_digest`; no member carries authority, a producer,
runtime coordinates or an effect claim.

| Field | Type | Constraint |
|---|---|---|
| `ordinal` | integer | Exactly one value in `0..6`, contiguous and equal to the fixed member order on the receipt. |
| `name` | string | Exact name assigned to that ordinal by the receipt's seven-member table. |
| `artifact_id` | [ArtifactId](#artifactid) | Finalized content-addressed artifact in the isolated test database. |
| `content_digest` | [ContentDigest](#contentdigest) | Digest reproduced from the exact artifact bytes. |

**Equality:** all four fields compare by canonical value. Reordering, renaming, removal, addition,
artifact substitution or byte/digest drift changes the containing lineage-unit preimage and must
reject or conflict.

### ResourceBudget

The closed one-[Attempt](#attempt) resource document. Its exact schema literal is
`aci.resource-budget@1`; no field is optional and no omitted value means unlimited, inherited or a
host default.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exactly `aci.resource-budget@1`. |
| `max_wall_time_ms`, `max_input_tokens`, `max_output_tokens` | integer | Closed int64 range `0..9223372036854775807`. |
| `max_tool_calls` | integer | Closed int64 range `0..9223372036854775807`; exactly `0` when the confirmed tool profile is `tool.none`. |
| `max_payload_bytes`, `max_artifact_bytes` | integer | Closed int64 range `0..9223372036854775807`, attributable to this Attempt. |
| `budget_policy_ref` | [VersionedReference](#versionedreference) | Exact enforcement and accounting semantics; referenced bytes must resolve and reproduce the digest. |

The object is recursively closed: extra, missing, duplicate or misspelled fields reject. JSON
booleans, numeric strings, floats, negative values, values above `9223372036854775807`, `null`,
non-finite values, overflow/wraparound representations and implicit coercion reject for every integer. Zero is valid and means explicit
denial. `resource_budget_digest = sha256(aci-cjson-1(resource_budget))`; the digest is metadata or an
enclosing-contract field and is never inserted into this object.

The referenced `aci.budget-policy@1` document is also closed and has exactly `schema`, `scope`,
`exhaustion_action` and `unknown_usage_action`. The POLICY-000 oracle target is limited to
`scope=attempt`, `exhaustion_action=deny-new-work` and `unknown_usage_action=deny-new-work`; it is a
synthetic test reference, not a product selection.

**Equality:** exact canonical `aci-cjson-1` bytes. The separately computed content digest names
those complete bytes and is not a field of the value.

The confirmed dispatch limits `max_attempts_per_turn`, `max_total_turns` and `wall_clock_seconds`
govern [Run](#run) scheduling and are not [ResourceBudget](#resourcebudget) fields. The Run deadline
is `confirmed_at + wall_clock_seconds`; each [Attempt](#attempt) has its own explicitly authorized budget and a
deadline no later than that Run deadline. An implementation must not divide, copy or reinterpret a
dispatch limit into an Attempt budget. Retry consumes dispatch ceilings, receives a separately
authorized [Attempt](#attempt) budget and never resets the Run deadline. Missing provider counters are
observations with unknown values, not zero usage or permission for more work.

### SandboxPolicy

The closed launcher-isolation document. Its exact schema literal is `aci.sandbox-policy@1`; every
nested scope is closed and all grants are explicit.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exactly `aci.sandbox-policy@1`. |
| `policy_ref` | [VersionedReference](#versionedreference) | Exact launcher/enforcement semantics; referenced bytes must resolve and reproduce the digest. |
| `filesystem_scope` | object | Exactly `default`, `read_roots`, `write_roots`, `link_policy`. |
| `network_scope` | object | Exactly `default`, `allowed_endpoints`. |
| `process_scope` | object | Exactly `default`, `allowed_executables`, `max_child_processes`. |
| `credential_refs` | ordered list<[VersionedReference](#versionedreference)> | Duplicate-free opaque grants; the list may be non-empty, while secret bytes are forbidden. |

The v1 nested grammar is exact:

```json
{
  "filesystem_scope": {
    "default": "deny",
    "read_roots": [],
    "write_roots": [],
    "link_policy": "deny"
  },
  "network_scope": {
    "default": "deny",
    "allowed_endpoints": []
  },
  "process_scope": {
    "default": "deny",
    "allowed_executables": [],
    "max_child_processes": 0
  }
}
```

All three `default` fields and `link_policy` are exactly `deny` in v1. POLICY-000 performs lexical root
validation only: repository roots use canonical relative `/` paths and reject empty components,
`.`, `..`, drives, UNC paths and wildcards. Physical symlink, junction/reparse-point and resolved-path
containment checks are launcher/target-host enforcement obligations deferred to POLICY-003/L3.
Non-empty endpoint or executable lists reject until a separate closed, digest-pinned entry definition
is ratified. `max_child_processes` uses the closed int64 range `0..9223372036854775807` and the same
strict JSON primitive rules as [ResourceBudget](#resourcebudget).

Non-empty `credential_refs` remain valid L0 values. For every reference, the pure parser receives
the exact target bytes keyed to that reference, performs no I/O, and verifies its digest under the
reference owner's contract. POLICY-000 does not invent or require a universal credential-target
schema. Whether a launcher can resolve and isolate the referenced credential is deferred to
POLICY-003/L3. Unsupported host enforcement rejects before process creation; it never narrows or
widens a policy silently.

`sandbox_policy_digest = sha256(aci-cjson-1(sandbox_policy))`; the digest is outside the object.
The referenced `aci.sandbox-enforcement-policy@1` document is closed and has exactly `schema`,
`enforcement_mode` and `unsupported_control_action`. POLICY-000 admits only the synthetic
`enforcement_mode=deny-all`, `unsupported_control_action=deny` reference target.

**Equality:** exact canonical `aci-cjson-1` bytes. The separately computed content digest names
those complete bytes and is not a field of the value.

### ExecutionAuthorityFence

The production cutover fact accepted by effect claim and rechecked immediately before physical
start. The exact schema literal is `aci.execution-authority-fence@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exactly `aci.execution-authority-fence@1`. |
| `dispatch_id`, `run_id` | string | Exact runtime-owned execution. |
| `authority_mode` | [ExecutionAuthorityMode](#executionauthoritymode) | Must equal `runtime-managed`. |
| `cutover_epoch` | integer | Closed int64 range `1..9223372036854775807`; current monotonic epoch for the target host. |
| `legacy_watcher_disabled_evidence_ref` | [ArtifactId](#artifactid) | Finalized independently readable target-host evidence. |
| `fence_digest` | [ContentDigest](#contentdigest) | Digest of the exact preimage below, checked at claim and start. |

The fence is recursively closed. Its digest preimage contains the same fields except
`fence_digest`, and changes `schema` to `aci.execution-authority-fence-preimage@1`:

```text
fence_digest = sha256(aci-cjson-1(fence_preimage))
```

Acceptance requires exact frozen dispatch, Run and authority mode; a current matching host cutover
head; readable evidence that binds that host, epoch, disabled legacy watcher, writer inventory and
configuration digests; independently verified audit opening, prerequisite heads and sandbox; and a
launcher that can enforce every control. Drift, revocation, unreadable evidence or unsupported
enforcement denies before process creation. Product input cannot supply the epoch or evidence.

Product authority selects the exact [ResourceBudget](#resourcebudget),
[SandboxPolicy](#sandboxpolicy), tool profile and any opaque credential grants presented for a later
CONF v2. It does not select `cutover_epoch` or watcher-disable evidence. Those fence fields are
operational facts supplied by the cutover verifier only after target-host evidence exists; their
absence cannot be filled with a product preference or harness fixture.

**Equality:** exact canonical `aci-cjson-1` bytes. The embedded `fence_digest` validates only the
`aci.execution-authority-fence-preimage@1` bytes; equality of the complete fence remains whole-value
canonical-byte equality.

### ExecutionAuthorityFenceHarness

A structurally parallel, test-only fence for POLICY-000 pure oracle tests. It uses exact schema
`aci.execution-authority-fence-harness@1`; its preimage uses exact schema
`aci.execution-authority-fence-harness-preimage@1`. All other fields and strict type rules match
[ExecutionAuthorityFence](#executionauthorityfence), but the two values are different types and
authority domains.

The harness parser may validate harness structure and preimage digest. The production parser must
reject the harness schema literal before resolving its synthetic evidence reference. A harness
fence cannot satisfy confirmation, cutover, an invocation plan/request, an opening gate, an effect
claim or a [Run](#run) transition.

**Equality:** exact canonical `aci-cjson-1` bytes. Its embedded `fence_digest` validates only the
harness-preimage bytes and never identifies a production preimage or the complete harness document.

### ExecutionPolicyOracleFixture

The test-only aggregate of one all-zero [ResourceBudget](#resourcebudget), one deny-all
[SandboxPolicy](#sandboxpolicy) and their separately supplied content digests. It has exactly the
fields `schema`, `resource_budget`, `resource_budget_digest`, `sandbox_policy` and
`sandbox_policy_digest`, with schema literal `aci.execution-policy-oracle-fixture@1`.

This value is oracle data, never executable authority. POLICY-000 may use it only to prove strict
parsing, canonicalization, digest lineage, mutations and denial semantics. Production policy
package parsers, confirmation, plan/request acceptance and effect workers reject this schema. The
golden bytes and digests are fixed by the reviewed
[TECH-POLICY-D0](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md#fake-deny-all-lane),
not regenerated from host defaults.

**Equality:** exact canonical `aci-cjson-1` bytes. The two member digests independently bind their
complete member documents; they do not turn the combined fixture into authority.

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
| `schema_ref`, `schema_digest` | string, [ContentDigest](#contentdigest) | Exact versioned payload-schema identifier plus the digest of its closed definition; the two fields are separate journal columns. |
| `aggregate_type` | string | Closed aggregate kind; confirmation events require `run`. |
| `aggregate_id` | string | Owning stream. |
| `aggregate_version` | [AggregateVersion](#aggregateversion) | Contiguous within aggregate. |
| `journal_offset` | [JournalOffset](#journaloffset) | Globally increasing committed order. |
| `recorded_at` | timestamp | Journal observation; governs ordering only through offset. |
| `observed_at` | timestamp | Optional/nullable external observation; never orders transitions. |
| `run_id`, `dispatch_id` | string | Contextual runtime authority; both are required for the two confirmation events. |
| `actor_principal_id` | string | Required authenticated actor; never copied from agent-authored payload. |
| `command_id`, `idempotency_key` | string | Required accepted command and first transport-deduplication identities. |
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

The object has exactly these three fields. A pure parser receives an exact target-byte map keyed to
every reference and performs no filesystem, artifact-store, network or credential-provider I/O. A
reference is accepted only when the supplied bytes reproduce `digest` under the reference owner's
contract. Missing, extra, duplicate or misspelled fields, absent target bytes, a target that
violates its owner's contract or a digest mismatch reject; there are no defaults or coercions. A
reference owner may require a closed target schema, but POLICY-000 does not invent one universal
schema for credential references.

### ManifestEntry

| Field | Type | Constraint |
|---|---|---|
| `message_id` | string | Accepted contribution. |
| `payload_hash` | [ContentDigest](#contentdigest) | Matches accepted event. |

**Equality:** Ordered pair equality; manifests additionally compare canonical entry order and hash.

## Enums

### ConfirmationChannel

| Value | Description |
|---|---|
| `chat` | An admitted chat-host adapter observed the approval. |
| `ui` | An admitted future UI adapter observed the same semantic approval contract. |

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
| OQ-RESOURCE-LIMITS / OQ-SANDBOX | **L0 grammar ratified; L1 synthetic-lineage contract specified by this amendment and implementation separately gated** | Product must select exact [ResourceBudget](#resourcebudget), [SandboxPolicy](#sandboxpolicy), tool and opaque credential-reference values. The cutover verifier separately supplies production [ExecutionAuthorityFence](#executionauthorityfence) epoch/evidence as operational facts. [ExecutionAuthorityFenceHarness](#executionauthorityfenceharness), [ExecutionPolicyOracleFixture](#executionpolicyoraclefixture) and [ExecutionPolicySyntheticLineageReceipt](#executionpolicysyntheticlineagereceipt) remain test-only. POLICY-000 proves pure parsing/canonicalization; POLICY-001 may prove only transactional synthetic lineage after the complete DomainSpec amendment, work-pack readiness and independent review pass. Physical link resolution and L2-L3 denial/target-host enforcement remain separate work. |

## Connections

| Document | Type | Description |
|---|---|---|
| [Discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md) | `derives-from` | Source decisions and OQ dispositions. |
| [Rules](rules.md) | `governed-by` | Cross-entity invariants and authority rules. |
| [Persistence and replay](persistence-and-replay.md) | `maps` | Candidate storage ownership and transaction contract. |
| [TECH-POLICY-D0](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md) | `refines` | Reviewed closed POLICY-000 schema, digest-domain and layering source. |
| [POLICY-001 persistence pattern inventory](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md) | `refines` | Digest-pinned (`sha256:d8eae9829069631caaef769635b3748b5440d5bfab4aacaf682f736eb546d84e`) test-only receipt identity, one-transaction persistence and reopen boundary for POLICY-001. |
