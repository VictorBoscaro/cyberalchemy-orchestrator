# Operations: Agents Communication Infra

This file specifies the mutation side of the single-host runtime. It ratifies the
operator-designated [discovery v0.2.1](../discovery/feature-discovery/agents-communication-infra.md)
without authorizing runtime implementation. Commands request change; only committed events in the
[event journal](events.md#common-runtime-event-envelope) are facts; external work is represented by
durable effect intents and is never repeated by replay.

The canonical operation registry for this feature is limited to
`ConfirmRuntimeDispatch`, `AcceptRuntimeCommand`, `StartAgentAttempt`,
`PublishBusContribution`, `VerifyPublicationReceipt`, `CloseCollection`, `PublishRevealManifest`,
`MaterializeAuthorizedPeerInput`, `CommitGroupResult`, `CancelRun`, and
`RecordUsageObservation`. Named “internal transition” sections below decompose
those operations for testability; they are not additional registry operations.

## AcceptRuntimeCommand

**Type:** Operation (mutation)  
**Actor:** Authenticated command service, kernel policy reactor, adapter observer or materializer  
**Triggers:** Any requested runtime transition or accepted external observation

This is the common conditional-append boundary used by all specialized operations and internal
transition steps in this document. It does not grant adapters, agents or materializers direct journal
write access.

### Common command contract

Every operation receives a runtime command envelope in addition to its operation-specific input.

| Field | Required | Contract |
| --- | ---: | --- |
| `command_id` | yes | Stable command identity. Reuse with a different digest is a permanent conflict. |
| `idempotency_key` | yes | Dedupe key scoped to the operation and authenticated aggregate. |
| `command_digest` | yes | Hash of the canonical command envelope and operation input. |
| `aggregate_id` | yes | Runtime-derived aggregate identity; never trusted from agent-authored payload. |
| `expected_aggregate_version` | yes | Compare-and-set version observed by the caller. |
| `prerequisite_heads` | yes | Ordered `(aggregate_id, expected_version, state_hash)` dependencies checked in the same transaction as the target CAS. |
| `actor_principal_id` | yes | Derived from authenticated command or capability context. |
| `causation_id` | yes | Command/event/effect that caused this request. |
| `correlation_id` | yes | End-to-end run correlation identity. |

The journal applies the following order atomically: validate identity and policy; compare an existing
idempotency receipt and digest; load and compare the aggregate version and every prerequisite head;
reduce the command; append
events; update the aggregate head; enqueue newly requested effect intents; commit; then return the
stable command receipt. `same idempotency key + same digest` returns the original receipt without new
facts. `same idempotency key + different digest` returns `idempotency_conflict`. A stale expected
version or changed prerequisite head returns `aggregate_version_conflict` or
`prerequisite_head_conflict`. Neither rejection advances domain state. Start-vs-close/cancel races
therefore cannot pass validation using independently stale aggregate snapshots.

## ConfirmRuntimeDispatch

**Type:** Operation (mutation)  
**Actor:** Human operator through the command boundary  
**Triggers:** Explicit confirmation of an editable pending dispatch

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `pending_sheet_bytes` | bytes | yes | Exact confirmed bytes; mutable source data is not reread during replay. |
| `dispatch_id` | ID | yes | Official audit identity, unique for the confirmed version. |
| `execution_authority_mode` | enum | yes | Must already equal `runtime-managed`. |
| `dispatch_spec_ref` | artifact reference | yes | Immutable executable graph and participant/policy contract. |
| `dispatch_spec_digest` | SHA-256 | yes | Digest of the confirmed spec. |
| `schema_versions` | map | yes | Frozen command, event, recipe and payload schema versions. |
| `capability_resolution_ref` | artifact reference | yes | Exact accepted adapter/tool capability resolution. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-CONF-1 | Authority mode is selected before confirmation. | `mode = runtime-managed` |
| O-CONF-2 | An accepted runtime confirmation creates exactly one `ConfirmedDispatch` and one run; a legacy-selected proposal is rejected before either entity exists. | `acceptedConfirmRuntimeDispatch(d) => runtimeManaged(d) and existsUnique(confirmedDispatch(d)) and existsUnique(run(d))` |
| O-CONF-3 | The sheet bytes, spec, versions, policies and capability resolution are immutable after acceptance. | `accepted(d) => digest(authority(d)) = constant` |
| O-CONF-4 | The compatibility `.confirmed` marker has no execution authority for this run. | `runtimeManaged(d) => legacyWatcherMayExecute(d) = false` |
| O-CONF-5 | During the MVP, rerun means a new confirmed dispatch and a new run. | `rerun => new(dispatch_id) and new(run_id)` |

### State transition

[`RunLifecycle`](states.md#runlifecycle): `not_created -> confirmed -> opening_pending`

### Postconditions

- [`run.created`](events.md#runcreated) freezes the confirmed authority and establishes the 1:1
  MVP mapping between `dispatch_id` and `run_id`.
- [`audit_opening.requested`](events.md#audit_openingrequested) and its effect intent commit in the
  same local transaction as the run facts.
- No provider, tool or agent-start effect is eligible before verified audit opening.
- Marker/sheet cleanup, if requested, is a retryable compatibility effect after opening verification.

### Error states

| Condition | Result |
| --- | --- |
| Pre-confirmation routing choice is `legacy-managed` | Reject; preserve the legacy path and create no `ConfirmedDispatch`, runtime `Run`, journal fact or audit effect. |
| Existing dispatch/run identity has identical digest | Return the stable original receipt. |
| Existing identity has a different digest | Permanent identity conflict; no state change. |
| Capability combination changes semantics | Reject until a new spec version is explicitly reconfirmed. |

### OQ-ACI6 settlement

**Ratified.** `ExecutionAuthorityMode` is assigned before confirmation. Runtime-managed confirmation
freezes the source and makes the marker a compatibility projection ignored by legacy watchers;
a legacy-selected proposal never creates a runtime `ConfirmedDispatch` or
[`RunLifecycle`](states.md#runlifecycle). Routing to legacy is allowed only before runtime
confirmation; after runtime confirmation, change requires an explicit terminal/repair path and must
never transfer partial runtime state into a legacy success.

### Internal transition — VerifyAuditOpening

**Type:** Operation (mutation)  
**Actor:** Audit-ledger materializer  
**Triggers:** Opening effect claim or recovery reconciliation

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `run_id` | ID | yes | Runtime-derived run identity. |
| `dispatch_id` | ID | yes | Audit opening identity. |
| `canonical_row_digest` | SHA-256 | yes | Digest derived from frozen authority. |
| `observed_row` | absent or row | yes | Result of independent ledger read. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-OPEN-1 | Only the validated appender may physically append the audit row. | `writer(ledger) = validatedAppender` |
| O-OPEN-2 | Identical existing content is already applied. | `observed.digest = expected.digest => verified` |
| O-OPEN-3 | Absence invokes the appender once and requires post-append verification. | `absent => append; reread = expected` |
| O-OPEN-4 | Same identity with divergent content requires reconciliation and cannot release effects. | `sameId and differentDigest => reconciliation_required` |

### State transition

[`RunLifecycle`](states.md#runlifecycle): `opening_pending -> ready` or
`opening_pending -> reconciliation_required`

### Postconditions

- [`audit_opening.verified`](events.md#audit_openingverified) is persisted before execution effects
  become eligible.
- Recovery after append-before-ack converges by exact identity and content comparison.

### Internal transition — StartRun

**Type:** Operation (mutation)  
**Actor:** Protocol scheduler  
**Triggers:** Verified official opening

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-RUN-1 | Official opening is verified. | `run.state = ready and opening_verified = true` |
| O-RUN-2 | The frozen spec and capability resolution remain available by digest. | `hash(resolve(ref)) = frozen_digest` |

### State transition

[`RunLifecycle`](states.md#runlifecycle): `ready -> running`

### Postconditions

- [`run.started`](events.md#runstarted) is appended.
- The first dependency-free group may be started; provider choice never changes the group protocol.

### Internal transition — StartGroup

**Type:** Operation (mutation)  
**Actor:** Protocol kernel  
**Triggers:** Run start or a verified `ConnectionHandoff`

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `group_id` / `group_version` | ID / integer | yes | Immutable protocol revision within the run. |
| `group_spec_ref` | artifact reference | yes | Seats, schemas, phases, quorum and policy version. |
| `base_snapshot_ref` | artifact reference | yes | Content-addressed shared group context. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-GROUP-1 | All declared predecessor dependencies are committed and delivered. | `forall p in predecessors: delivered(p, group)` |
| O-GROUP-2 | Slice 0 has exactly two seats and the fixed `collect -> reveal -> vote -> commit` profile. | `slice0 => seats = 2 and deliberate = false` |
| O-GROUP-3 | Provider, adapter and model selections are per agent instance and do not alter the profile. | `protocol(group) independentOf provider(instance)` |

### State transition

[`GroupLifecycle`](states.md#grouplifecycle): `pending -> collecting`

### Postconditions

- [`group.started`](events.md#groupstarted) records the frozen group version and snapshot.
- Agent operations may be scheduled only for declared seats.

## StartAgentAttempt

**Type:** Operation (mutation)  
**Actor:** Scheduler; adapter materializer translates, and the sandboxed effect worker starts  
**Triggers:** A logical `operation_id` becomes eligible or a retry policy requests a new attempt

### Input and sealing pipeline

The scheduler first creates an [AgentInvocationPlan](domain.md#agentinvocationplan). The selected
[AgentAdapter](interfaces.md#internal-agentadapter) translates it into a
[MaterializedAgentInvocation](domain.md#materializedagentinvocation) and prepares the canonical
bytes and metadata for the [EffectiveInputArtifact](domain.md#effectiveinputartifact). The kernel
validates both digests and seals an [AgentExecutionRequest](domain.md#agentexecutionrequest); only
then may it atomically accept the Attempt, finalize the artifact metadata and commit the start
effect. An adapter can translate and report observations, but cannot accept state or write the
journal.

| Field | Source | Required contract |
| --- | --- | --- |
| `attempt_id`, `dispatch_id`, `operation_id`, `seat_id` | runtime | Authenticated identities; dispatch follows seat/group/run ownership, while retry keeps `operation_id` and creates a new `attempt_id`. |
| `provider_ref`, `adapter_ref`, `model_ref` | confirmed spec + scheduler | Exact selection for this agent instance; heterogeneous groups are valid. |
| `role_contract_ref`, `task_ref` | compiled profile | Local objective, allowed output and hashed role delta. |
| `base_snapshot_ref` | runtime | Same for peers unless the confirmed role contract declares `role_delta_ref`. |
| `effective_input_ref`, `provider_invocation_ref` | adapter materializer | Ordered content-addressed observable input and native request. |
| `response_schema_ref` | confirmed spec | Schema required before output can be a publication candidate. |
| `tool_profile_ref` | capability resolver | Exact tools; sealed collection includes publish but no peer-read capability. |
| `deadline`, `resource_budget` | confirmed policy | Typed time, token, tool, payload and storage limits. |
| `sandbox_policy` | confirmed policy | Explicit filesystem/network/process/credential isolation contract. |
| `authority_fence` | cutover verifier | Current runtime-owned epoch plus verified legacy-watcher-disable evidence. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-ATT-1 | Provider-specific CLI flags are not part of the canonical request. | `canonicalRequest hasNo providerFlags` |
| O-ATT-2 | Prepared canonical input bytes/hash exist before request sealing; finalized artifact metadata and request binding commit atomically with attempt acceptance. | `seal(request) => prepared(bytes,hash) and attempt.requested => atomic(finalizedArtifact,requestBinding,attempt.requested)` |
| O-ATT-3 | The manifest orders and hashes system/developer/user instructions, history, tool schemas, response schema, context and adapter wrappers. | `effective_input_ref = hash(orderedManifest)` |
| O-ATT-4 | Missing mandatory or semantics-changing capability rejects the combination unless a new spec is reconfirmed. | `missingSemanticsCapability => reject or reconfirm` |
| O-ATT-5 | Retry never creates a second logical seat contribution. | `retry => same(operation_id, seat_id) and new(attempt_id)` |
| O-ATT-6 | Plan, materialization and sealed request are distinct and digest-bound. | `sealedRequest = validate(planDigest, materializationDigest)` |
| O-ATT-7 | Start requires the sandbox launcher and a current execution-authority fence. | `startEffect => sandboxLaunched and fenceCurrent` |
| O-ATT-8 | Group/run heads used to establish eligibility are command prerequisites. | `start => prerequisiteHeadsUnchanged` |
| O-ATT-9 | Any Reference Scout bundle in the effective input is accepted only through an accepted [AgentReferenceDelivery](domain.md#agentreferencedelivery). | `reference_bundle in manifest => accepted(agents-communication-infra.AgentReferenceDelivery)` |

### State transition

[`AttemptLifecycle`](states.md#attemptlifecycle): `not_created -> requested`

### Postconditions

- [`attempt.requested`](events.md#attemptrequested) and a durable sandbox-launch/start effect intent
  commit atomically only after the sealed request exists.
- The effect worker passes the sealed request through [SandboxLauncher](interfaces.md#internal-sandboxlauncher)
  regardless of provider. Native translations remain artifacts/metadata, not kernel branches.

### Internal transition — RecordAttemptObservation

**Type:** Operation (mutation)  
**Actor:** Adapter worker or recovery reconciler  
**Triggers:** Provider start/status/events/result/cancel observation

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `attempt_id` | ID | yes | Existing physical attempt. |
| `worker_epoch` | integer | yes | Must match the durable claim epoch. |
| `observation_kind` | enum | yes | `started`, `running`, `waiting_tool`, `completed`, `failed`, `unknown`, `cancel_acknowledged`, or `cancelled`. |
| `provider_cursor` | opaque | no | Deduplicates incremental provider events. |
| `raw_output_ref` | artifact reference | terminal-dependent | Immutable provider-native output, separate from an accepted bus message. |
| `terminal_result` | [AgentTerminalResult](domain.md#agentterminalresult) | terminal-dependent | Versioned provider-neutral envelope parsed under common rules. |
| `observed_at` | timestamp | no | Diagnostic provider time; journal order remains authoritative. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-OBS-1 | A stale worker epoch cannot accept completion or renew a claim. | `epoch != current_epoch => reject` |
| O-OBS-2 | A valid terminal result is unique per attempt. | `count(terminal_result(attempt)) <= 1` |
| O-OBS-3 | Late observations remain journaled but cannot reverse a terminal aggregate transition. | `late => observed_ignored and state unchanged` |
| O-OBS-4 | Unknown non-retryable effects are not automatically repeated. | `unknown and non_retryable => no automatic start` |
| O-OBS-5 | Codex, Claude and later adapters use the same terminal-result version/parsing rules. | `protocol_equivalent(nativeResult, AgentTerminalResult)` |

### State transition

See the complete [`AttemptLifecycle`](states.md#attemptlifecycle).

### Postconditions

- The corresponding canonical attempt event is appended.
- Raw provider output remains distinct from a `BusPublication`, even when
  it contains a schema-valid candidate.

### Internal transition — DeliverReferenceScoutBundleToAgent

**Type:** Internal operation (atomic input-settlement transition owned by
[StartAgentAttempt](#startagentattempt); it has no standalone command or commit)
**Actor:** Runtime scheduler under an authenticated delivery capability
**Triggers:** A StartAgentAttempt plan includes one already lifecycle-delivered Reference Scout
bundle for the target [Attempt](domain.md#attempt) and its prepared
[EffectiveInputArtifact](domain.md#effectiveinputartifact)

**Contract status:** specified for the next bounded slice; not implemented. Stage G implements
Scout bundle commit and lifecycle delivery, but it does not settle a bundle into an agent attempt's
effective input.

### Input

| Field | Source | Required contract |
|---|---|---|
| `agent_reference_delivery_id`, `accepted_event_id` | runtime | Stable [AgentReferenceDelivery](domain.md#agentreferencedelivery) and event identities preallocated before manifest canonicalization. |
| `dispatch_id`, `target_attempt_id`, `target_seat_id`, `target_agent_instance_id` | authenticated capability + owning seat/group/run | Caller cannot self-assert recipient authority. |
| `scout_run_id`, `source_bundle_delivered_event_id` | capability-bound source | Existing lifecycle-delivered ScoutRun in the same dispatch. |
| `bundle_artifact_id`, `bundle_digest`, `recommendation_ids` | verified committed event + immutable artifact | Exact ordered bundle membership; never copied from the delivered event. |
| `effective_input_artifact_id`, `effective_input_entry_ordinal`, `effective_input_manifest_hash` | input materializer | Exact unique `reference_bundle` entry in the prepared manifest. |
| `visibility_policy_ref` | authenticated delivery capability | Frozen authorization for this one bundle/recipient pair. |
| `idempotency_key` | command envelope | Retry identity scoped to ScoutRun and target attempt. |

### Rules

| ID | Rule | Formal |
|---|---|---|
| O-ARD-1 | The preceding committed event owns ordered membership; the lifecycle-delivered event owns no recommendation list. | `recommendation_ids = committed.recommendation_ids = orderedIds(bundle.bytes) and delivered hasNo recommendation_ids` |
| O-ARD-2 | Source commit, lifecycle delivery and immutable artifact agree on run, artifact and digest. | `same(commit, source_delivered, scout_run_id, bundle_artifact_id, bundle_digest) and bundle_digest = hash(bundle.bytes) and commit.offset < source_delivered.offset` |
| O-ARD-3 | Source ScoutRun, delivery and recipient Attempt share one runtime-derived dispatch. | `ScoutRun.dispatch_id = delivery.dispatch_id = Attempt.dispatch_id` |
| O-ARD-4 | Recipient seat and agent instance equal the authenticated target Attempt. | `Attempt(target_attempt_id).(seat_id,agent_instance_id) = (target_seat_id,target_agent_instance_id)` |
| O-ARD-5 | The prepared manifest contains exactly one matching reference-bundle entry under the authenticated policy. | `entries[effective_input_entry_ordinal] = unique reference_bundle(bundle_artifact_id,bundle_digest,agent_reference_delivery_id,visibility_policy_ref) and effective_input_manifest_hash = hash(canonical(orderedManifest))` |
| O-ARD-6 | One ScoutRun may be delivered at most once to one target Attempt. | `unique(scout_run_id,target_attempt_id)` |
| O-ARD-7 | Retry returns the original canonical receipt; any source, membership, recipient, entry, policy or digest drift conflicts. | `scope=(scout_run_id,target_attempt_id); same(scope,key,command_digest) => same(command_receipt); same(scope,key) and different(command_digest) => conflict` |
| O-ARD-8 | The delivery commits only within the complete StartAgentAttempt acceptance unit. | `sealed(AgentExecutionRequest) and atomic(Attempt,EffectiveInputArtifact,requestBinding,AgentReferenceDelivery,accepted_event_id:reference_scout.bundle_delivered_to_agent@1,attempt.requested,sandboxLaunchEffectIntent) or atomic(none)` |
| O-ARD-9 | Lifecycle delivery and target-agent delivery are different accepted facts in strict journal order. | `accepted_event_id != source_bundle_delivered_event_id and source_delivered.journal_offset < target_delivered.journal_offset` |

### State transition

This operation has no independent lifecycle. Its accepted fact co-commits with
[`attempt.requested`](events.md#attemptrequested) when the target [Attempt](domain.md#attempt) is
accepted.

### Postconditions

- The committed
  [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent)
  event matches every identity,
  source, recipient, manifest, policy, idempotency and offset field of
  [AgentReferenceDelivery](domain.md#agentreferencedelivery).
- The accepted target-delivery event follows the accepted lifecycle-delivered event in journal
  order and remains distinct from it.
- The immutable effective-input manifest is never amended after acceptance.
- The accepted fact proves inclusion in observable input only; it does not prove access, reading,
  declared use or claim support.

### Error states

| Condition | Result |
|---|---|
| Source commit or lifecycle-delivery event is missing or not accepted | Reject; accept no attempt or target-delivery fact. |
| Commit, lifecycle delivery and artifact disagree on ScoutRun, artifact or digest | Integrity failure; reject. |
| Bundle digest or ordered recommendation membership does not match immutable bytes | Integrity failure; reject. |
| ScoutRun and recipient Attempt resolve to different dispatches | Authorization failure; reject. |
| Target seat or agent instance differs from the authenticated Attempt | Authorization failure; reject. |
| Manifest entry is missing, duplicated, at another ordinal or differs in artifact/digest/delivery/policy | Validation failure; reject. |
| `(scout_run_id,target_attempt_id)` already has a nonidentical delivery | Uniqueness conflict; return no new receipt. |
| Same scoped idempotency key carries another `command_digest` | Idempotency conflict; return no new receipt. |
| Aggregate or prerequisite head is stale | CAS conflict; recompute eligibility before retry. |
| Any member of the complete StartAgentAttempt transaction fails | Roll back all members; emit neither `attempt.requested` nor target-delivery event. |

## PublishBusContribution

**Type:** Operation (mutation)  
**Actor:** Agent as logical publisher through an authenticated bus capability  
**Triggers:** `bus_publish`

### Agent-authored BusPublication

| Field | Agent may supply | Validation |
| --- | ---: | --- |
| `idempotency_key` | yes | Non-empty; unique within authenticated run/group/version/seat scope. |
| `operation_id` | yes | Must equal the operation bound to the attempt capability. |
| `round_id` | yes | Must equal an active permitted round. |
| `message_type` | yes | Allowlisted by phase and schema (`position`, `critique`, `vote`, or declared type). |
| `reply_to_message_ids` | yes | Every referenced message is already visible to the principal. |
| `payload` or `payload_ref` | yes | Exactly one; schema-valid, size-bounded and content-hashed. |
| `run_id`, `dispatch_id`, `group_id/version`, `seat_id`, `agent_instance_id`, `attempt_id`, `actor_principal_id`, `phase` | **no** | Derived from authenticated capability context; conflicting supplied fields are rejected. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-PUB-1 | Publication authority is runtime-derived, never agent-asserted. | `authority(envelope) = authenticatedContext` |
| O-PUB-2 | Phase, message type, round and schema must agree with current journal state. | `allowed(group.state, round, message_type, schema)` |
| O-PUB-3 | One logical contribution exists per aggregate/seat/round/type despite physical retries. | `unique(aggregate_id, seat_id, round_id, message_type)` |
| O-PUB-4 | A reply may cite only visible messages. | `forall id in replies: visible(principal, id)` |
| O-PUB-5 | During collection, peer content is inaccessible; no generic peer-read tool exists in Slice 0. | `collecting => visible(peerContribution) = false` |
| O-PUB-6 | Receipt is returned only after the candidate event and artifact reference commit. | `return(receipt) => committed(publication.persisted)` |
| O-PUB-7 | Persisting a candidate does not make it official or quorum-eligible. | `publication.persisted and not receiptVerified => not official and not quorumEligible` |

### State transition

None. [`publication.persisted`](events.md#publicationpersisted) records a durable candidate without
advancing the group aggregate.

### PublicationReceipt

The only successful schema is [PublicationReceipt](domain.md#publicationreceipt), including
`receipt_version`, `status=persisted_candidate`, `event_id`, `message_id`, `journal_offset`,
`payload_hash` and `idempotency_key`. It is a projection of the committed candidate fact, not an
official contribution. The parent independently verifies every identity field and scope. A gateway
may return `transport_replayed` beside, but never inside, the canonical receipt; that transport flag
does not participate in receipt equality or verification.

### Postconditions

- [`publication.persisted`](events.md#publicationpersisted) exists before acknowledgement.
- The candidate stores content by hash/reference; provider output and effective input remain
  separate immutable records linked through the attempt.

### Error states

| Condition | Result |
| --- | --- |
| Retry with same key and same digest | Return the byte-identical stored `PublicationReceipt`; append nothing. The transport envelope may report `transport_replayed=true`. |
| Same key with different digest | Permanent `idempotency_conflict`. |
| Another active candidate owns the logical seat/round/type | `logical_contribution_conflict`; an abandoned historical candidate does not retain the active reservation. |
| Stale phase, round or capability | Reject and record an auditable security/protocol observation. |
| Agent supplies/conflicts with authority fields | Reject; do not reinterpret the payload. |
| Schema, size, budget or reply visibility fails | Reject; no contribution transition. |

## VerifyPublicationReceipt

**Type:** Operation (mutation)  
**Actor:** Parent/scheduler  
**Triggers:** Agent attempt returns a terminal structured result claiming a `PublicationReceipt`

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `attempt_id` | ID | yes | Attempt whose parent is evaluating completion. |
| `publication_receipt.event_id` | ID | yes | Claimed committed acceptance event. |
| `publication_receipt.message_id` | ID | yes | Claimed accepted logical message. |
| `publication_receipt.payload_hash` | SHA-256 | yes | Claimed hash of accepted publication content. |
| `publication_receipt.idempotency_key` | string | yes | Claimed publication dedupe key. |
| `publication_receipt.receipt_version/status/journal_offset` | scalar | yes | Complete canonical receipt schema; status must be `persisted_candidate`. |
| `operation_id` | ID | yes | Logical operation bound to the authenticated attempt. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-RECEIPT-1 | The parent resolves the receipt independently against the persisted journal; agent/provider claims are not evidence. | `verified(r) => existsUnique(e in journal): e.event_id = r.event_id` |
| O-RECEIPT-2 | Version, status, event, message, offset, payload hash and idempotency key match the same committed candidate event. | `matches(e,r) = allEqual(version,status,event_id,message_id,offset,payload_hash,key)` |
| O-RECEIPT-3 | The event's runtime-derived attempt, operation, seat and aggregate scope match authenticated parent context. | `scope(e) = authenticatedScope(attempt,operation)` |
| O-RECEIPT-4 | A valid provider result without a verified receipt is not an official contribution. | `official(result) => verified(receipt(result))` |
| O-RECEIPT-5 | Only one attempt result may satisfy a logical operation. | `count(acceptedResult(operation_id)) <= 1` |
| O-RECEIPT-6 | Verification recovery is idempotent by attempt, operation and logical message key. | `same(attempt,operation,logicalKey,receipt) => same verification outcome` |
| O-RECEIPT-7 | Official acceptance wins only by CAS on the owning active candidate. | `candidate.status = active -> officially_accepted`; `abandoned => never official` |

### Postconditions

- [`attempt.result_accepted`](events.md#attemptresult_accepted) and the message-type-specific
  [`position.accepted`](events.md#positionaccepted), [`critique.accepted`](events.md#critiqueaccepted)
  or [`vote.accepted`](events.md#voteaccepted) commit atomically and link the physical attempt to the
  earlier candidate.
- The same transaction CASes the authoritative candidate `active -> officially_accepted`, inserts
  the official `messages` row and preserves the candidate receipt bytes unchanged.
- The verified persisted contribution, not raw provider output, becomes the official result for the
  logical operation and may count toward quorum.
- Later attempt results for the same operation are preserved as superseded/ignored observations.
- If the process crashes after `publication.persisted` or after provider terminalization, recovery
  reloads the [AgentTerminalResult](domain.md#agentterminalresult) and candidate by
  `(attempt_id, operation_id, logical_message_key)`, repeats exact verification, and converges
  without another official acceptance.

### Error states

| Condition | Result |
| --- | --- |
| Receipt is missing from the terminal result | `publication_receipt_missing`; reject official result and do not count it toward quorum. |
| `event_id` does not resolve to one committed acceptance event | `publication_receipt_forged`; reject and record an auditable security observation. |
| Any receipt field differs from persisted event/message evidence | `publication_receipt_mismatch`; reject and identify only the mismatched field names in safe diagnostics. |
| Persisted event belongs to another attempt, operation, seat, group or run | `publication_receipt_scope_mismatch`; reject as cross-scope spoofing. |
| Another attempt already satisfied the logical operation | `operation_result_already_accepted`; preserve this result as superseded/ignored. |
| Candidate was abandoned | `publication_candidate_abandoned`; reject permanently even if late terminal evidence arrives. |

### Internal transition — AbandonPublicationCandidate

**Type:** Internal operation (mutation)  
**Actor:** Retry policy through the controlled journal writer  
**Triggers:** The candidate-owning attempt is terminal `unknown` and no terminal evidence can be
recovered through the adapter/status/artifact boundaries

The command identifies the candidate, its owning attempt/operation/logical key, the persisted
`attempt.unknown` event, a content-addressed no-recoverable-terminal-evidence determination and the
retry-authorization policy/version. It uses the current candidate version/status as a CAS
precondition.

| ID | Rule | Formal |
| --- | --- | --- |
| O-ABANDON-1 | Only an active candidate may be abandoned. | `CAS(active -> abandoned)` |
| O-ABANDON-2 | Unknown alone is insufficient; terminal evidence must be explicitly determined unrecoverable. | `abandon => attempt.unknown and noRecoverableTerminalEvidence` |
| O-ABANDON-3 | Retry policy must authorize another physical attempt for the same operation/seat. | `abandon => retryAuthorized(operation, seat)` |
| O-ABANDON-4 | Official acceptance and abandonment are mutually exclusive CAS winners. | `not(officiallyAccepted and abandoned)` |
| O-ABANDON-5 | A late result for an abandoned candidate remains evidence but cannot revive or accept it. | `abandoned + lateTerminal => observation_ignored` |

On success, [`publication.candidate_abandoned`](events.md#publicationcandidate_abandoned) commits
with the candidate status change and releases the partial active-key reservation. Only after that
commit may another authorized attempt publish a new candidate for the same logical contribution
key. Identical abandonment retry returns the stored command receipt; a concurrent verifier or
different abandonment digest produces the corresponding CAS/outcome conflict.

## CloseCollection

**Type:** Operation (mutation)  
**Actor:** Protocol kernel through a policy reactor command  
**Triggers:** All eligible contributions are present, or a persisted deadline/ceiling fact permits closure

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-CLOSE-1 | The eligible message set is frozen only from receipt-verified official acceptance facts. | `manifestInput = officialAcceptedMessages(at closeOffset)` |
| O-CLOSE-2 | Wall clock never closes collection during replay; a timeout must already be an event. | `timeoutAffectsState => exists(deadline.fired)` |
| O-CLOSE-3 | A missing or invalid second contribution in the fixed proof is `no_quorum`, never dissent. | `validContributions < 2 => no_quorum` |
| O-CLOSE-4 | A durable candidate without its official acceptance event is excluded. | `publication.persisted and not position.accepted => not eligible` |

### State transition

[`GroupLifecycle`](states.md#grouplifecycle): `collecting -> revealing`

### Postconditions

- [`collection.closed`](events.md#collectionclosed) freezes the eligible message IDs/hashes.
- Closing alone does not grant peer visibility.

## PublishRevealManifest

**Type:** Operation (mutation)  
**Actor:** Protocol kernel  
**Triggers:** Collection is closed and its frozen set is content-addressed

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `group_id` / `group_version` / `round_id` | IDs | yes | Exact reveal scope. |
| `message_entries` | ordered set | yes | Accepted `message_id` + `payload_hash` entries from the closed set. |
| `manifest_hash` | SHA-256 | yes | Hash of the canonical ordered manifest. |
| `authorized_principals` | principal set | yes | Derived from the confirmed group policy. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-REV-1 | Manifest content equals the frozen collection exactly. | `set(manifest) = set(collection.closed)` |
| O-REV-2 | Reveal is unique for group version and round. | `count(reveal(group, version, round)) <= 1` |
| O-REV-3 | Only `reveal.published`, not `collection.closed`, changes peer visibility. | `peerVisible(m) <=> m in publishedManifest and authorized` |
| O-REV-4 | Revealed content is delivered through a later turn/attempt input, not a generic peer-read channel. | `delivered(m, attempt) => m in effectiveInput(attempt)` |

### State transition

[`GroupLifecycle`](states.md#grouplifecycle): `revealing -> voting` for Slice 0, or
`revealing -> deliberating` when a later confirmed profile enables deliberation.

### Postconditions

- [`reveal.published`](events.md#revealpublished) commits the `RevealManifest`.
- Any authorized delivery is a content-addressed input to a new attempt/turn and is recorded in that
  turn's `EffectiveInputArtifact`.

## AuthorizeAgentInvocationPlan

**Type:** Operation (local authorization mutation)
**Actor:** Protocol-kernel scheduler through capability action `bus.plan`, phase `plan`
**Triggers:** One accepted running host-workflow binding selected for the next fixed-seat turn

This operation is the only admitted plan-registration boundary for
`SWU-ACI-BUS-DELIVERY-001`. The request carries `binding_id` and one complete
[AgentInvocationPlan](domain.md#agentinvocationplan). The capability context must equal the
binding-derived `binding_id`, `group_aggregate_id`, `target_attempt_id`, `target_seat_id`,
`provider_ref` and `adapter_ref`; the request cannot override any of them. The kernel recomputes
those six values from the immutable running binding before its first write, validates the complete
plan, derives `plan_digest`/`plan_ref`, and persists the byte-stable plan. Any attempt, seat, group,
provider or adapter substitution fails with no plan row.

This operation creates no Attempt, effective input, request, effect or provider/tool execution. It
exists only to provide the authenticated, digest-addressed plan prerequisite consumed by
[MaterializeAuthorizedPeerInput](#materializeauthorizedpeerinput).

## MaterializeAuthorizedPeerInput

**Type:** Operation (mutation)
**Actor:** Protocol kernel through a capability bound to the preallocated target identity
**Triggers:** An accepted [`reveal.published`](events.md#revealpublished) fact and one authorized
[StartAgentAttempt](#startagentattempt) plan whose target identity has not been accepted or started

This bounded operation proves reveal delivery without claiming or running a provider effect. It
does not expose a generic inbox or peer-read method.

**Authority:** the bounded promotion in
[SPEC.md](SPEC.md#bounded-spec-amendment-authorized-local-peer-input-materialization)
specializes discovery decision
[ACI-D8](../discovery/feature-discovery/agents-communication-infra.md#51-agent-input-bus-publication-and-reveal-delivery)
for `SWU-ACI-BUS-DELIVERY-001`; it does not promote dynamic Work Bus routing.

**Checked by:** [T-ACI-PEER1 through T-ACI-PEER7](../TEST-SPEC.md#bounded-authorized-peer-input-delivery).

### Input

| Field | Type | Required | Description |
|---|---|---:|---|
| `reveal_manifest_id` | string | yes | Exact accepted source manifest. |
| `visibility_policy_ref` | [VersionedReference](domain.md#versionedreference) | yes | Frozen policy controlling the peer filter. |
| `idempotency_key` | string | yes | Retry identity scoped to manifest plus target attempt. |

The authenticated runtime context, outside the request payload, supplies the exact
`agent_invocation_plan_ref`, `agent_invocation_plan_digest` and capability-bound
`target_attempt_id`/`target_seat_id`. The kernel resolves the plan by its reference, verifies its
digest, and requires its preallocated attempt/seat identities to equal the capability-bound
identities. The caller supplies no attempt ID, seat ID, message ID, artifact ID, hash, source seat
ID or ordering. The kernel derives those values from the authenticated plan/capability, accepted
manifest, official contributions and policy.

The kernel resolves the plan's authorized `base_snapshot_ref` and optional `role_delta_ref` into
ordered base entries, appends the derived reveal entries and preallocates the effective-input
artifact identity without finalizing it. It then invokes only the deterministic translation
surface of the plan-selected [AgentAdapter](interfaces.md#internal-agentadapter), passing that
preallocated identity and the prepared ordered entries. The translation returns observable wrapper
references plus a [MaterializedAgentInvocation](domain.md#materializedagentinvocation). The kernel
incorporates those wrapper references, hashes and finalizes the complete
[EffectiveInputArtifact](domain.md#effectiveinputartifact), verifies that the materialized
invocation binds its `effective_input_ref` to that artifact and its `plan_digest` to
`agent_invocation_plan_digest`, then seals the
[AgentExecutionRequest](domain.md#agentexecutionrequest). Adapter translation here is not an
external provider/tool effect.

For this exact SWU, `visibility_policy_ref` MUST equal
`aci.fixed-two-seat-peer-reveal@1`. Its closed predicate is:

```text
authorized(entry, target_seat_id) :=
  accepted(reveal.published(entry.reveal_manifest_id))
  AND entry.message_id IN RevealManifest(entry.reveal_manifest_id).message_entries
  AND official(Contribution(entry.message_id))
  AND Contribution(entry.message_id).group_aggregate_id =
      Seat(target_seat_id).group_aggregate_id
  AND Contribution(entry.message_id).seat_id != target_seat_id
```

No configurable principal list, dynamic route, inbox membership or policy extension is admitted by
this version.

### Rules

| ID | Rule | Formal |
|---|---|---|
| O-PEER-1 | Source and target share one group; recipient identity comes from the digest-verified [AgentInvocationPlan](domain.md#agentinvocationplan) and capability, not an existing Attempt row or agent payload. | `plan = resolve(agent_invocation_plan_ref) and hashCanonical(plan) = agent_invocation_plan_digest and plan.attempt_id/seat_id = capability.target_attempt_id/seat_id and Seat(plan.seat_id).group_aggregate_id = RevealManifest(reveal_manifest_id).group_aggregate_id` |
| O-PEER-2 | Only the unique accepted reveal for the exact manifest hash, group, round and ordered entries opens delivery. | `existsUnique accepted reveal.published where event.reveal_manifest_id = manifest.reveal_manifest_id = reveal_manifest_id and event.manifest_hash = manifest.manifest_hash = hashCanonical(manifest.group_aggregate_id,manifest.round_id,manifest.message_entries)` |
| O-PEER-3 | Entries preserve manifest order, pass policy and exclude the target seat's own contribution. | `entries = ordered(manifest.entries where authorized(entry,target_seat_id) and Contribution(entry.message_id).seat_id != target_seat_id)` |
| O-PEER-4 | Every entry binds one official contribution, immutable artifact and the exact payload hash recorded by its manifest entry. | `forall e in entries: official(e.message_id) and e.content_hash = manifest[e.message_id].payload_hash = Artifact(e.artifact_ref).content_hash` |
| O-PEER-5 | Acceptance uses the complete StartAgentAttempt unit after adapter wrappers are included in the finalized input, and is atomic with the requested attempt and unclaimed effect intent. | `preparedInput.artifact_id = MaterializedAgentInvocation.effective_input_ref = EffectiveInputArtifact.artifact_id and adapterWrapperRefs(MaterializedAgentInvocation) = EffectiveInputArtifact.adapter_wrapper_refs and MaterializedAgentInvocation.plan_digest = agent_invocation_plan_digest and sealed(AgentExecutionRequest) and atomic(Attempt,finalizedArtifactMetadata,MaterializedAgentInvocation,requestBinding,AgentExecutionRequest,PeerInputDelivery,peer_input.materialized,attempt.requested,unclaimedEffectIntent) or atomic(none)` |
| O-PEER-6 | Identical retry is byte-stable; any semantic drift conflicts. | `same(scope,key,digest) => same receipt and no append; same(scope,key) and different(digest) => conflict` |
| O-PEER-7 | At this operation's commit and receipt return, the effect remains unclaimed and this bounded SWU has performed no external execution. | `atReceiptReturn(accepted(peer_input.materialized)) => effect.status = pending and effect.claim_id = null and provider_start_count_by_this_operation = 0` |

### Calculations

| ID | Calculation | Formula |
|---|---|---|
| O-PEER-C1 | Authorized ordered peer entries | `peerEntries = preserveManifestOrder(manifest.message_entries where authorized(message_id,target_seat_id) and Contribution(message_id).seat_id != target_seat_id)` |
| O-PEER-C2 | Canonical effective input | `baseInputEntries = resolveAuthorizedInputEntries(plan.base_snapshot_ref,plan.role_delta_ref); preparedEntries = baseInputEntries ++ mapRevealEntries(peerEntries,manifest,policy); wrapperRefs = deterministicAdapterMaterialize(preallocatedArtifactId,preparedEntries).adapter_wrapper_refs; inputBytes = canonicalize(preparedEntries,wrapperRefs,plan.tool_profile_ref,plan.response_schema_ref); inputHash = sha256(inputBytes)` |
| O-PEER-C3 | Delivery semantic identity | `deliveryDigest = sha256(canonicalize(reveal_manifest_id,manifest.manifest_hash,target_attempt_id,target_seat_id,peerEntries,inputArtifactId,inputHash,visibility_policy_ref))` |
| O-PEER-C4 | Stable acknowledgement | `receiptBytes = canonicalize(PeerInputDeliveryReceipt(receipt_version="aci.peer-input-delivery-receipt/v1",status="materialized",event_id,peer_input_delivery_id,reveal_manifest_id,target_attempt_id,target_seat_id,effective_input_artifact_id,effective_input_manifest_hash,idempotency_key,journal_offset))` |

### State Transition

No independent [GroupLifecycle](states.md#grouplifecycle) transition occurs. The same complete
[StartAgentAttempt](#startagentattempt) acceptance transaction seals the
[AgentExecutionRequest](domain.md#agentexecutionrequest), finalizes artifact metadata and request
binding, creates the target [Attempt](domain.md#attempt), and co-commits
[`AttemptLifecycle`](states.md#attemptlifecycle) `not_created -> requested` through
[`attempt.requested`](events.md#attemptrequested).

### Postconditions

- One [PeerInputDelivery](domain.md#peerinputdelivery) and one
  [`peer_input.materialized`](events.md#peer_inputmaterialized) fact bind the exact target input.
- The operation returns one byte-stable
  [PeerInputDeliveryReceipt](domain.md#peerinputdeliveryreceipt).
- At operation commit and receipt return, its effect intent remains `pending` and unclaimed; this
  operation/SWU has performed no effect claim or provider/tool execution. Deterministic adapter
  translation is allowed only to produce the bound `MaterializedAgentInvocation`. A separately
  authorized later operation is not forbidden by this bounded proof.
- No agent-callable list, search, export, debug or generic peer-read capability is granted.
- This amendment neither satisfies nor relaxes the audit-ledger materializer, sole-writer/EG-1,
  runtime-authority cutover, administrator-hook or real-provider gates.

### Error States

| Condition | Result |
|---|---|
| Reveal event/manifest is missing or differs in hash, group, round or ordered entries | `REVEAL_MISMATCH`; atomically write nothing |
| `agent_invocation_plan_ref` is absent/unresolvable or its canonical digest differs from `agent_invocation_plan_digest` | `INVOCATION_PLAN_MISMATCH`; atomically write nothing |
| Capability-derived target identity or group differs | `TARGET_AUTHORITY_MISMATCH`; atomically write nothing |
| Finalized derived output contains an absent, self-authored, policy-denied, unaccepted or out-of-order entry that should have been filtered | `PEER_ENTRY_FORBIDDEN`; atomically write nothing |
| Contribution artifact or content hash differs from the manifest/finalized artifact | `PEER_ARTIFACT_MISMATCH`; atomically write nothing |
| Target attempt was already accepted, started or has a nonidentical delivery | `TARGET_ATTEMPT_CONFLICT`; atomically write nothing |
| Same scoped idempotency key or semantic identity has different canonical bytes/digest | `IDEMPOTENCY_CONFLICT`; atomically write nothing |
| Any caller requests claim/start/adapter/provider execution in this operation | `EFFECT_NOT_AUTHORIZED`; atomically write nothing |

### Internal transition — ComputeFixedProofVerdict

**Type:** Operation (mutation)  
**Actor:** Protocol kernel  
**Triggers:** Vote collection is ready for the fixed Slice-0 rule

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-VER-1 | Exactly two valid seat votes are required. | `validVotes = 2` |
| O-VER-2 | Matching votes compute a committable consensus result. | `v1 = v2 => verdict = consensus(v1)` |
| O-VER-3 | Conflicting valid votes compute explicit dissent. | `v1 != v2 => verdict = dissent({v1,v2})` |
| O-VER-4 | Missing or invalid contribution is no quorum, not dissent. | `validVotes < 2 => no_quorum and no verdict.computed` |
| O-VER-5 | The fixed rule is not generalized to later profiles. | `policy_version = fixed-two-seat-proof@1` |

### State transition

[`GroupLifecycle`](states.md#grouplifecycle): `voting -> committing` only when a verdict is computed.

### Postconditions

- [`verdict.computed`](events.md#verdictcomputed) records the policy version, both seat/message
  references and either `consensus` or `dissent`.
- No-quorum stays a distinct protocol condition and reaches a bounded terminal cause through the
  declared deadline/ceiling policy.

### OQ-ACI2 settlement

**Ratified exactly for the fixed proof.** Two valid logical contributions are mandatory. Matching
votes commit; two conflicting valid votes commit explicit dissent; fewer than two valid votes are
`no_quorum`, never dissent. Richer quorum, abstention, replacement and decision policies remain
outside this rule and require separately versioned confirmed profiles.

## CommitGroupResult

**Type:** Operation (mutation)  
**Actor:** Protocol kernel  
**Triggers:** A persisted verdict and a typed result payload are available

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `verdict_event_id` | ID | yes | Persisted result of the declared decision rule. |
| `result_payload_ref` | artifact reference | yes | Typed immutable result/envelope. |
| `participant_message_ids` | ID set | yes | Accepted evidence used by the result. |
| `dissent_refs` | ID set | yes | Preserved unresolved/minority evidence; may be empty. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-COMMIT-1 | One committed result exists per group version. | `count(commit(group_id, group_version)) <= 1` |
| O-COMMIT-2 | Result envelope records rule, participants, quorum, verdict and evidence references. | `complete(groupResultEnvelope)` |
| O-COMMIT-3 | Kernel never generates narrative synthesis implicitly. | `narrative != null => producedBy(declaredRole)` |
| O-COMMIT-4 | Replay reuses the committed payload and never calls an agent to reinterpret it. | `replay(commit) = reduce(event)` |

### State transition

[`GroupLifecycle`](states.md#grouplifecycle): `committing -> completed`

### Postconditions

- [`group.committed`](events.md#groupcommitted) publishes one immutable `GroupResult`.
- Explicit dissent remains a valid committed group result; its run-level classification is decided
  only by the internal `ElectRunTerminal` transition.

### Internal transition — PublishConnectionHandoff

**Type:** Operation (mutation)  
**Actor:** Connection handoff workflow  
**Triggers:** A source group commits and a declared downstream connection exists

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-HAND-1 | Delivery is deduplicated by source aggregate and connection identity. | `unique(source_aggregate_id, connection_id)` |
| O-HAND-2 | Handoff carries result, dissent and provenance, not narrative alone. | `payload includes result_ref, dissent_refs, provenance_refs` |
| O-HAND-3 | The downstream snapshot is immutable and content-addressed. | `target_snapshot_ref = hash(materializedHandoff)` |

### Postconditions

- [`handoff.published`](events.md#handoffpublished) and
  [`handoff.delivered`](events.md#handoffdelivered) make the downstream dependency observable.
- Delivery may enable the internal `StartGroup` transition; it never exposes a source group's internal bus.

## CancelRun

**Type:** Operation (mutation)  
**Actor:** Authorized human or runtime policy  
**Triggers:** Explicit cancellation command

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-CANCEL-1 | The command targets a current nonterminal run/group/attempt version. | `not terminal(target) and expectedVersion = currentVersion` |
| O-CANCEL-2 | Request, provider acknowledgement and terminal cancellation are distinct facts. | `requested != acknowledged != terminal` |
| O-CANCEL-3 | Completion/cancel races are ordered by the journal; only the first valid terminal transition wins. | `winner = minJournalOffset(validTerminalFacts)` |

### Postconditions

- Cancellation requests durable cancel effect intents for active attempts.
- Late results remain auditable and affect protocol state only if still valid at their journal order.

### Internal transition — ElectRunTerminal

**Type:** Operation (mutation)  
**Actor:** Protocol kernel through a policy reactor command  
**Triggers:** Final group result, irreconcilable dissent, bounded ceiling, explicit human abort, or technical prevention

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `terminal_cause` | enum | yes | Closed cause from the matrix below. |
| `cause_event_ids` | ID set | yes | Journal evidence supporting the cause. |
| `result_ref` | artifact reference | conditional | Required for committed result/dissent. |
| `exit_detail_ref` | artifact reference | no | Diagnostic detail separate from the enum. |

### Terminal cause matrix

| Winning run-level cause | `exit_reason` | Constraint |
| --- | --- | --- |
| Committed positive, negative, qualified or policy-approved partial result | `resolved` | Merit does not alter exit reason. |
| Committed irreconcilable dissent after allowed rounds | `dissent_irreconcilable` | Requires a committed dissent result, not missing quorum. |
| Round/protocol ceiling or timeout with no technical fault and no quorum/result | `loop_ceiling_reached` | Missing/invalid contribution remains no quorum. |
| Explicit human cancellation | `user_abort` | Requires an authorized human cancellation fact to win the terminal CAS. |
| Exhausted provider retries, corrupted state, resource/budget exhaustion preventing a valid outcome, or other technical prevention | `error` | Technical prevention is not reclassified as a protocol ceiling. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-TERM-1 | Attempt and group terminal facts never map directly to the audit ledger. | `ledgerExitReason = map(winningRunTerminal)` |
| O-TERM-2 | Exactly one valid run terminal wins by aggregate CAS and journal order. | `count(winningRunTerminal(run)) = 1` |
| O-TERM-3 | A partial result is resolved only when policy explicitly commits it as qualified. | `partial and not committedQualified => map(cause)` |
| O-TERM-4 | Later facts are preserved as ignored observations and cannot replace the winner. | `offset > winner.offset => no terminal mutation` |

### State transition

[`RunLifecycle`](states.md#runlifecycle): `running -> execution_terminal -> close_pending`

### Postconditions

- [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) freezes the run-level
  cause and `exit_reason`.
- [`audit_close.requested`](events.md#audit_closerequested) and the close materialization effect
  intent commit locally before worker execution.

### OQ-ACI3 settlement

**Ratified.** The closed matrix above is authoritative. Attempt/group terminal facts are evidence,
not audit mappings. The journal-ordered, CAS-protected run terminal alone selects one of
`resolved`, `dissent_irreconcilable`, `loop_ceiling_reached`, `user_abort`, or `error`. Negative,
falsified and `KILL` results remain `resolved` when validly committed.

### Internal transition — VerifyAuditClose

**Type:** Operation (mutation)  
**Actor:** Audit-ledger materializer  
**Triggers:** Close effect claim or recovery reconciliation

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-ACLOSE-1 | Close is derived from the unique run terminal and complete current audit schema. | `close.exit_reason = winningRunTerminal.exit_reason` |
| O-ACLOSE-2 | Existing identical close is applied; absent is appended then verified; divergent is reconciliation-required. | `identical => verified; absent => append+reread; divergent => reconciliation_required` |
| O-ACLOSE-3 | Only the validated appender physically writes the audit ledger. | `writer(ledger) = validatedAppender` |

### State transition

[`RunLifecycle`](states.md#runlifecycle): `close_pending -> closed` or
`close_pending -> reconciliation_required`

### Postconditions

- [`audit_close.verified`](events.md#audit_closeverified) is persisted only after the official close
  row exists with exact canonical content.
- `closed` is the only state claiming official close materialization.

## RecordUsageObservation

**Type:** Operation (mutation)  
**Actor:** Adapter worker  
**Triggers:** Provider reports usage for an attempt, turn, exchange or terminal result

### Input

| Field | Type | Required | Description |
| --- | --- | ---: | --- |
| `attempt_id`, `provider_ref`, `model_ref` | IDs | yes | Provenance of the observation. |
| `provider_record_id` | opaque ID | yes | Dedupe identity for the provider-reported record. |
| `input_units`, `cached_input_units`, `output_units`, `reasoning_units` | nullable numbers | yes | Preserve absence as `null`; provider semantics remain attributed. |
| `provider_unit_semantics` | map | yes | Names/units/version describing reported counters. |
| `pricing_ref` | nullable versioned reference | yes | Required only for a cost observation or derived cost. |
| `provider_metadata` | namespaced map | no | Nonportable detail; cannot govern protocol transitions. |

### Rules

| ID | Rule | Formal |
| --- | --- | --- |
| O-USAGE-1 | Each provider record is immutable and deduplicated without merging away provenance. | `unique(provider_ref, provider_record_id, attempt_id)` |
| O-USAGE-2 | Missing dimensions remain null, never synthesized as zero. | `not reported(x) => x = null` |
| O-USAGE-3 | Cost requires an explicit price/version source and compatible unit semantics. | `cost != null => pricing_ref != null and compatible(units, price)` |
| O-USAGE-4 | Rollups preserve provider attribution and nullability by attempt, operation, seat, group, run and dispatch. | `rollup(scope) = aggregate(observations, semantics)` |
| O-USAGE-5 | Usage cannot govern kernel transitions directly. | `providerMetadata notIn transitionGuards` |

### Postconditions

- [`usage.observed`](events.md#usageobserved) is appended with source provenance.
- Any rollup is a rebuildable projection over immutable observations, not billing truth.

### OQ-ACI10 settlement

**Observation and rollup semantics ratified; empirical completeness deferred.** Every reported record
is persisted as a nullable, provider-attributed [`UsageObservation`](events.md#usageobserved).
Missing counters and prices are never invented. Dispatch-level cost claims remain disabled until the
Slice-2 real-adapter conformance matrix proves completeness for tool-heavy, multi-turn, resumed and
retried execution; mixed-provider rollups must preserve each provider's semantics.

## Operation-to-event summary

| Operation | Principal produced events |
| --- | --- |
| [`AcceptRuntimeCommand`](#acceptruntimecommand) | Conditional append for opening/close verification, run/group start, attempt observations, deadlines, effects, handoffs and the unique run terminal |
| [`ConfirmRuntimeDispatch`](#confirmruntimedispatch) | [`run.created`](events.md#runcreated), [`audit_opening.requested`](events.md#audit_openingrequested) |
| [`StartAgentAttempt`](#startagentattempt) | [`attempt.requested`](events.md#attemptrequested), plus optional atomic target-agent delivery |
| Internal [`DeliverReferenceScoutBundleToAgent`](#internal-transition--deliverreferencescoutbundletoagent) | [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent), atomically within StartAgentAttempt |
| [`PublishBusContribution`](#publishbuscontribution) | [`publication.persisted`](events.md#publicationpersisted) candidate only |
| [`VerifyPublicationReceipt`](#verifypublicationreceipt) | [`attempt.result_accepted`](events.md#attemptresult_accepted) plus the message-type-specific official acceptance event |
| Internal [`AbandonPublicationCandidate`](#internal-transition--abandonpublicationcandidate) | [`publication.candidate_abandoned`](events.md#publicationcandidate_abandoned) |
| [`CloseCollection`](#closecollection) | [`collection.closed`](events.md#collectionclosed) |
| [`PublishRevealManifest`](#publishrevealmanifest) | [`reveal.published`](events.md#revealpublished) |
| [`MaterializeAuthorizedPeerInput`](#materializeauthorizedpeerinput) | [`peer_input.materialized`](events.md#peer_inputmaterialized) plus co-committed [`attempt.requested`](events.md#attemptrequested) |
| [`CommitGroupResult`](#commitgroupresult) | [`verdict.computed`](events.md#verdictcomputed), [`group.committed`](events.md#groupcommitted), and optional handoff facts |
| [`CancelRun`](#cancelrun) | [`cancellation.requested`](events.md#cancellationrequested), `attempt.cancel_requested`, and eventual [`group.cancelled`](events.md#groupcancelled) |
| [`RecordUsageObservation`](#recordusageobservation) | [`usage.observed`](events.md#usageobserved) |
