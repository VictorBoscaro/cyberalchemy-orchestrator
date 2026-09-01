# Events: Agents Communication Infra

These are immutable accepted facts. Wire names are explicit and stable; replay reduces them without
reissuing commands, querying providers, consulting the wall clock, or repeating effects. A command
rejection may have a durable command receipt without becoming an aggregate transition event.

Each second-level wire heading below is a value of the versioned `RuntimeEventType` vocabulary. It
is not a DomainSpec registry concept. Likewise, internal transition labels in `operations.md` are
decompositions of registered operations, not additional registry Operations.

## Common runtime event envelope

| Field | Required | Contract |
| --- | ---: | --- |
| `event_id`, `event_type` | yes | Immutable fact identity and the exact wire name specified below. |
| `schema_ref`, `schema_digest` | yes | Exact versioned payload-schema identifier string and the content digest of its closed definition; these are separate journal fields. |
| `aggregate_type`, `aggregate_id`, `aggregate_version` | yes | Aggregate identity and contiguous CAS version allocated by the journal writer. |
| `journal_offset` | yes | Global integer ordering position in the declared local journal. |
| `recorded_at` | yes | Journal time; ordering authority remains `journal_offset`. |
| `observed_at` | no | Provider/external diagnostic time; never governs replay. |
| `run_id`, `dispatch_id` | contextual | Runtime-derived authority identities. |
| `group_id`, `group_version`, `seat_id`, `agent_instance_id` | contextual | Runtime-derived group/participant identities. |
| `operation_id`, `attempt_id`, `round_id` | contextual | Logical operation, physical attempt and declared round identities. |
| `message_id`, `reply_to_message_ids` | contextual | Logical publication and visible discourse references. |
| `actor_principal_id` | yes | Authenticated principal; never accepted from agent-authored content. |
| `command_id`, `idempotency_key` | yes | Accepted command identity/dedupe trace. |
| `causation_id`, `correlation_id` | yes | Immediate cause and end-to-end run trace. |
| `policy_version`, `input_snapshot_id` | contextual | Frozen decision/input provenance. |
| `payload_ref`, `payload_hash` | contextual | Immutable artifact reference and content hash. |

`group_version` is the immutable protocol revision; `aggregate_version` is only its event-stream CAS
version. `message_id` identifies a logical publication; `event_id` identifies the fact accepting,
rejecting or delivering it. Runtime authority fields are always populated from authenticated
context, not copied from agent payloads.

## Run events

## run.created

**Wire name:** `run.created`  
**Produced by:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `not_created -> confirmed`

**Payload schema:** `aci.run-created@1`, one exact member of the manifest-pinned
`aci.runtime-confirmation-payload-schemas@1` bundle.

| Field | Type | Required | Contract |
|---|---|---:|---|
| `schema` | string | yes | Exact `aci.run-created@1`. |
| `run_id`, `dispatch_id`, `dispatch_revision` | string | yes | Exact server-derived run identity and verified presentation scope. |
| `execution_authority_mode` | [ExecutionAuthorityMode](domain.md#executionauthoritymode) | yes | Exact literal `runtime-managed`. |
| `pending_sheet_ref`, `dispatch_spec_ref`, `confirmation_observation_ref` | [ArtifactId](domain.md#artifactid) | yes | Finalized source, spec and trusted-host observation artifacts. |
| `pending_sheet_digest`, `dispatch_spec_digest`, `confirmation_observation_digest` | [ContentDigest](domain.md#contentdigest) | yes | Digests of those three distinct byte domains. |
| `capability_resolution_ref`, `confirmed_turn_graph_ref`, `continuation_mapping_set_ref`, `confirmed_authority_ref` | [ArtifactId](domain.md#artifactid) | yes | Finalized server resolution, bounded graph, ordered mapping set and complete authority artifacts. |
| `capability_resolution_digest`, `confirmed_turn_graph_digest`, `continuation_mapping_set_digest`, `confirmed_authority_digest` | [ContentDigest](domain.md#contentdigest) | yes | Exact digest paired with each preceding artifact. |
| `identity_derivation_ref` | [VersionedReference](domain.md#versionedreference) | yes | Exact complete identity-derivation contract. |
| `identity_derivation_digest`, `payload_schema_bundle_digest` | [ContentDigest](domain.md#contentdigest) | yes | Canonical digests of the complete derivation contract and closed confirmation-payload-schema bundle. |
| `graph_id`, `continuation_id` | string | yes | Server-derived graph and continuation identities. |
| `mapping_ids`, `source_message_ids` | ordered list<string> | yes | Exactly two values each, in mapping/source-message order. |
| `schema_versions` | closed map<string,string> | yes | Complete frozen command/event/payload/recipe/identity version map; unknown or missing keys reject. |
| `confirmed_by` | string | yes | Authenticated human principal projected from the observation. |
| `confirmed_at` | RFC3339 millisecond UTC timestamp | yes | Issuer observation time; no writer-clock substitution. |

The payload contains exactly these fields. Unknown, missing, null or wrong-type values reject; list
order is semantic. Its envelope has `aggregate_type=run`, `aggregate_id=run_id`,
`aggregate_version=1`, `schema_ref=aci.run-created@1` and `schema_digest` equal to that member's
definition digest in the frozen bundle.

The event freezes the complete accepted authority; it is not itself a complete audit-ledger
opening row. Its `event_id` is the CONF-000 derived `event` identity for coordinates
`["run.created","1"]`, and its aggregate version is exactly `1`.

| Consumer | Action |
|---|---|
| Run reducer | Establish version-1 `confirmed` state from the exact authority digests and derived run identity. |
| Audit-opening materializer | Retain the frozen authority input but perform no append until the requested effect is claimed. |
| Runtime projection | Expose the confirmed identity/digests without granting execution readiness. |

## audit_opening.requested

**Wire name:** `audit_opening.requested`  
**Produced by:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `confirmed -> opening_pending`

**Payload schema:** `aci.audit-opening-requested@1`, one exact member of the manifest-pinned
`aci.runtime-confirmation-payload-schemas@1` bundle.

| Field | Type | Required | Contract |
|---|---|---:|---|
| `schema` | string | yes | Exact `aci.audit-opening-requested@1`. |
| `run_id`, `dispatch_id` | string | yes | Exact accepted run and audit-opening identity. |
| `confirmed_authority_ref` | [ArtifactId](domain.md#artifactid) | yes | Frozen authority artifact from which the materializer later derives the candidate opening row. |
| `confirmed_authority_digest` | [ContentDigest](domain.md#contentdigest) | yes | Digest of that exact authority artifact. |
| `appender_contract_version` | string | yes | Exact literal `0.6.4`. |
| `effect_id` | string | yes | CONF-000 server-derived effect identity. |
| `effect_type` | string | yes | Exact literal `audit_opening`. |
| `effect_payload_ref` | [ArtifactId](domain.md#artifactid) | yes | Finalized canonical `aci.audit-opening-effect@1` request. |
| `effect_payload_digest` | [ContentDigest](domain.md#contentdigest) | yes | Digest of that effect-payload artifact. |

The payload contains exactly these fields. Unknown, missing, null or wrong-type values reject. Its
envelope has `aggregate_type=run`, `aggregate_id=run_id`, `aggregate_version=2`,
`schema_ref=aci.audit-opening-requested@1` and `schema_digest` equal to that member's definition
digest in the frozen bundle.

The event and generic effect intent commit locally together. Confirmation does not pre-claim the
intent, append YAML or assert that a canonical audit row already exists. Its `event_id` is the
CONF-000 derived `event` identity for coordinates `["audit_opening.requested","2"]`, and its
aggregate version is exactly `2`.

The matching generic [EffectIntent](domain.md#effectintent) row is closed as:
`effect_id` above; `command_id` equal to the accepted command; `requested_event_id` equal to this
event; `effect_type=audit_opening`; exact payload ref/digest above; `retry_class=retryable`;
`status=pending`; `claim_epoch=null`; `claimed_by=null`; `attempt_count=0`;
`outcome_event_id=null`; and `outcome_digest=null`. The fixture uses the canonical domain name
`effect_id`, never `effect_intent_id`.

Both events, their two payload artifact-metadata records, the effect payload artifact metadata,
version-2 head, pending/unclaimed effect and first receipt are members of the same
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch) transaction as the remaining six
confirmation artifact-metadata records and authority rows. No event or payload becomes
authoritative in a partial commit.

| Consumer | Action |
|---|---|
| Audit-ledger materializer | When separately authorized to claim the effect, derive and reconcile a schema `0.6.4` opening row from the exact authority. |
| Run reducer | Advance version-1 `confirmed` to version-2 `opening_pending`; never to `ready`. |
| Effect outbox projection | Expose exactly one pending/unclaimed intent; projection does not claim or execute it. |

## audit_opening.verified

**Wire name:** `audit_opening.verified`  
**Produced by:** Audit opening reconciliation within [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `opening_pending -> ready`

**Payload:** `dispatch_id`, expected/observed canonical row digests, verification mode
(`already_identical` or `appended_then_verified`) and appender contract version.

**Consumers:** Run reducer; effect-release policy; runtime projection.

## audit_opening.reconciliation_required

**Wire name:** `audit_opening.reconciliation_required`  
**Produced by:** Audit opening reconciliation within [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `opening_pending -> reconciliation_required`

**Payload:** `dispatch_id`, expected digest, observed divergent digest and repair evidence reference.
No execution effect may be released.

**Consumers:** Run reducer; operator alert/projection; reconciler.

## run.started

**Wire name:** `run.started`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `ready -> running`

**Payload:** `run_id`, frozen spec/policy versions and first eligible group identities.

**Consumers:** Run reducer; group scheduler; runtime projection.

## run.execution_terminal_elected

**Wire name:** `run.execution_terminal_elected`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `running -> execution_terminal`

**Payload:** winning `terminal_cause`, mapped `exit_reason`, cause event IDs, nullable committed result
reference and exit-detail reference. Attempt/group terminals are evidence only; the event is the
unique run-level mapping authority.

**Consumers:** Run reducer; close materializer; audit/runtime projections.

## audit_close.requested

**Wire name:** `audit_close.requested`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `execution_terminal -> close_pending`

**Payload:** unique run-terminal event ID, `dispatch_id`, canonical close row reference/digest,
`exit_reason` and close effect identity.

**Consumers:** Audit-ledger materializer; effect outbox; run reducer.

## audit_close.verified

**Wire name:** `audit_close.verified`  
**Produced by:** Close reconciliation within [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `close_pending -> closed`

**Payload:** `dispatch_id`, `close_of`, expected/observed row digests and verification mode. It is
accepted only after the exact official close row exists.

**Consumers:** Run reducer; official-close projection; operator stream.

## audit_close.reconciliation_required

**Wire name:** `audit_close.reconciliation_required`  
**Produced by:** Close reconciliation within [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `close_pending -> reconciliation_required`

**Payload:** close identity, expected/observed divergent digests and repair evidence reference.

**Consumers:** Run reducer; operator alert/projection; reconciler.

## reconciliation.retry_requested

**Wire name:** `reconciliation.retry_requested`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `reconciliation_required -> opening_pending|close_pending`

**Payload:** target (`opening` or `close`), authorized disposition reference and prior divergence
event ID. It never treats divergence as applied.

**Consumers:** Run reducer; corresponding materializer.

## Group and bus events

## group.started

**Wire name:** `group.started`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `pending -> collecting`

**Payload:** group/version, frozen group spec and base snapshot references, seat set, phase profile,
decision-policy version and per-instance provider/adapter/model selections.

**Consumers:** Group reducer; scheduler; sealed bus projection.

## position.accepted

**Wire name:** `position.accepted`  
**Produced by:** [VerifyPublicationReceipt](operations.md#verifypublicationreceipt)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `collecting -> collecting`

**Payload:** runtime-derived run/group/seat/agent/attempt/principal identities; logical message key;
round; payload reference/hash; reply IDs; operation and idempotency identities. Content remains
sealed from peers.

**Consumers:** Group reducer; constrained `messages` projection; `publication_receipts` projection;
collection policy.

## publication.persisted

**Wire name:** `publication.persisted`  
**Produced by:** [PublishBusContribution](operations.md#publishbuscontribution)  
**Transition:** None; this is a durable candidate, not an official contribution

**Payload:** `receipt_version`, `status=persisted_candidate`, runtime-derived attempt/operation/
seat/group scope, logical message key, message type/round, payload reference/hash, idempotency key
and canonical receipt fields. The committed journal offset completes the receipt projection.

**Consumers:** Candidate/receipt projection; parent receipt verifier. It is ineligible for collection
close, quorum, reveal and verdict until the matching official acceptance event commits.

## publication.candidate_abandoned

**Wire name:** `publication.candidate_abandoned`  
**Produced by:** [Internal `AbandonPublicationCandidate`
transition](operations.md#internal-transition--abandonpublicationcandidate)  
**Transition:** None; atomically CASes one authoritative candidate `active -> abandoned`

**Payload:** candidate/message/publication event identity; owning attempt/operation/seat/group and
logical contribution key; persisted `attempt.unknown` event; no-recoverable-terminal-evidence
artifact/digest; retry-policy reference; expected candidate status/version and abandonment command
identity. It releases only the partial active-key reservation and never deletes candidate evidence.

**Consumers:** Candidate projection; retry scheduler; late-result auditor. A late provider terminal
for this candidate is retained as ignored evidence and cannot make the candidate official.

## critique.accepted

**Wire name:** `critique.accepted`  
**Produced by:** [VerifyPublicationReceipt](operations.md#verifypublicationreceipt)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `deliberating -> deliberating`

**Payload:** same canonical publication identity fields as `position.accepted`, plus visible
`reply_to_message_ids`. Deferred from Slice 0.

**Consumers:** Group reducer; deliberation projection; round policy.

## vote.accepted

**Wire name:** `vote.accepted`  
**Produced by:** [VerifyPublicationReceipt](operations.md#verifypublicationreceipt)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `voting -> voting`

**Payload:** canonical publication identity fields, schema-valid immutable vote and evidence
references. One logical vote is allowed per seat/round.

**Consumers:** Group reducer; fixed decision rule; `publication_receipts` projection.

## publication.rejected

**Wire name:** `publication.rejected`  
**Produced by:** [PublishBusContribution](operations.md#publishbuscontribution) security/audit path  
**Transition:** None

**Payload:** authenticated scope, safe rejection code, attempted message type/digest and conflicting
authority-field names if any; rejected payload content need not be persisted. It cannot yield a
`PublicationReceipt` or contribution.

**Consumers:** Security audit projection; adapter diagnostics.

## attempt.result_accepted

**Wire name:** `attempt.result_accepted`  
**Produced by:** [VerifyPublicationReceipt](operations.md#verifypublicationreceipt)  
**Transition:** None; links physical attempt to the already accepted logical message

**Payload:** `attempt_id`, `operation_id`, logical message key, complete receipt identity
(`receipt_version`, `status`, `event_id`, `message_id`, `journal_offset`, `payload_hash`,
`idempotency_key`), verification offset and parent principal. It commits atomically with the
message-type-specific official acceptance event, the candidate CAS to `officially_accepted` and the
official `messages` row. Exactly one attempt result may satisfy the logical operation.

**Consumers:** Attempt/operation projection; scheduler; quorum policy.

## collection.closed

**Wire name:** `collection.closed`  
**Produced by:** [CloseCollection](operations.md#closecollection)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `collecting -> revealing`

**Payload:** ordered receipt-verified official message IDs/hashes, close offset, expected/received
seat counts, quorum status and optional persisted deadline event. Candidate-only publications are
excluded. Closing freezes the set but does not open ACL.

**Consumers:** Group reducer; reveal-manifest builder; constrained bus projection.

## reveal.published

**Wire name:** `reveal.published`  
**Produced by:** [PublishRevealManifest](operations.md#publishrevealmanifest)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `revealing -> voting|deliberating`

**Payload:** reveal manifest ID/hash, group/version/round, exact ordered message ID/hash set,
authorized principals and target next phase. This is the only event that opens peer visibility.

**Consumers:** Group reducer; ACL projection; adapter input materializer. Delivered reveal content
must appear in the receiving turn's effective-input manifest.

## peer_input.materialized

**Wire name:** `peer_input.materialized`
**Produced by:** [MaterializeAuthorizedPeerInput](operations.md#materializeauthorizedpeerinput)
**Transition:** No independent transition; it co-commits with
[`attempt.requested`](#attemptrequested), which performs
[AttemptLifecycle](states.md#attemptlifecycle) `not_created -> requested`. No provider effect is claimed or
run by the bounded SWU.

**Payload:**

| Field | Type | Contract |
|---|---|---|
| `peer_input_delivery_id` | string | Exact [PeerInputDelivery](domain.md#peerinputdelivery) identity. |
| `reveal_manifest_id` | string | Existing accepted [RevealManifest](domain.md#revealmanifest). |
| `reveal_manifest_hash` | [ContentDigest](domain.md#contentdigest) | Exact canonical digest of the accepted manifest. |
| `reveal_event_id` | string | Existing accepted `reveal.published` fact for the manifest. |
| `source_group_aggregate_id` | string | Equals `PeerInputDelivery.source_group_aggregate_id`. |
| `source_round_id` | string | Equals `PeerInputDelivery.source_round_id`. |
| `target_attempt_id` | string | Equals `PeerInputDelivery.target_attempt_id`; derived from trusted scheduler context. |
| `target_seat_id` | [SeatId](domain.md#seatid) | Equals `PeerInputDelivery.target_seat_id`; derived from the target attempt. |
| `peer_message_entries` | ordered list<[EffectiveInputEntry](domain.md#effectiveinputentry)> | Equals `PeerInputDelivery.peer_message_entries` in authorized manifest order. |
| `effective_input_artifact_id` | [ArtifactId](domain.md#artifactid) | Equals `PeerInputDelivery.effective_input_artifact_id`. |
| `effective_input_manifest_hash` | [ContentDigest](domain.md#contentdigest) | Equals `PeerInputDelivery.effective_input_manifest_hash`. |
| `visibility_policy_ref` | [VersionedReference](domain.md#versionedreference) | Equals `PeerInputDelivery.visibility_policy_ref`. |
| `idempotency_key` | string | Equals `PeerInputDelivery.idempotency_key`; scoped to manifest plus target attempt. |

The event is accepted only with finalized artifact metadata, the bound
[MaterializedAgentInvocation](domain.md#materializedagentinvocation), request binding, sealed
[AgentExecutionRequest](domain.md#agentexecutionrequest), target [Attempt](domain.md#attempt),
authoritative [PeerInputDelivery](domain.md#peerinputdelivery),
[`attempt.requested`](#attemptrequested) and an unclaimed effect intent.
The ordered entries preserve reveal-manifest order, exclude the target seat's own contribution and
contain no message absent from the manifest. A same-key/same-semantic-digest retry returns the
stored receipt and emits nothing; drift conflicts.

```text
payload.peer_input_delivery_id = PeerInputDelivery.peer_input_delivery_id
payload.reveal_manifest_id = RevealManifest.reveal_manifest_id
payload.reveal_manifest_hash = RevealManifest.manifest_hash
payload.reveal_event_id = RevealManifest.reveal_event_id
accepted(payload.reveal_event_id, reveal.published)
reveal.published.reveal_manifest_id/hash =
  payload.reveal_manifest_id/reveal_manifest_hash
payload.source_group_aggregate_id = PeerInputDelivery.source_group_aggregate_id
payload.source_round_id = PeerInputDelivery.source_round_id
payload.target_attempt_id/seat_id = PeerInputDelivery.target_attempt_id/seat_id
Attempt(payload.target_attempt_id).seat_id = payload.target_seat_id
Seat(payload.target_seat_id).group_aggregate_id = payload.source_group_aggregate_id
payload.peer_message_entries = PeerInputDelivery.peer_message_entries
payload.effective_input_artifact_id/hash =
  PeerInputDelivery.effective_input_artifact_id/effective_input_manifest_hash
EffectiveInputArtifact(payload.effective_input_artifact_id).artifact_id =
  payload.effective_input_artifact_id
EffectiveInputArtifact(payload.effective_input_artifact_id).attempt_id =
  payload.target_attempt_id
EffectiveInputArtifact(payload.effective_input_artifact_id).manifest_hash =
  payload.effective_input_manifest_hash
payload.visibility_policy_ref = PeerInputDelivery.visibility_policy_ref
payload.idempotency_key = PeerInputDelivery.idempotency_key
envelope.event_id = PeerInputDelivery.accepted_event_id
envelope.journal_offset = PeerInputDelivery.journal_offset
PeerInputDeliveryReceipt.event_id/journal_offset =
  envelope.event_id/journal_offset
PeerInputDeliveryReceipt.peer_input_delivery_id/reveal_manifest_id =
  payload.peer_input_delivery_id/reveal_manifest_id
PeerInputDeliveryReceipt.target_attempt_id/target_seat_id =
  payload.target_attempt_id/target_seat_id
PeerInputDeliveryReceipt.effective_input_artifact_id/effective_input_manifest_hash =
  payload.effective_input_artifact_id/effective_input_manifest_hash
PeerInputDeliveryReceipt.idempotency_key = payload.idempotency_key
same(scoped_key, canonical_semantic_bytes, digest) => same receipt and no append
same(scoped_key) and changed(canonical_semantic_bytes or digest) => conflict
```

| Consumer | Action |
|---|---|
| Attempt reducer | Observe the co-committed requested attempt. |
| Internal input materializer | Return/verify the exact artifact binding. |
| Recovery verifier | Return byte-identical receipt or reject drift. |
| Audit projection | Expose delivery evidence without payload-wide read authority. |

This event grants no agent-callable query or generic peer-read capability.

## round.closed

**Wire name:** `round.closed`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `deliberating -> voting` (or a later declared round)

**Payload:** round identity, accepted message set/hash, close criterion and policy version.

**Consumers:** Group reducer; scheduler; runtime projection. Deferred from Slice 0.

## verdict.computed

**Wire name:** `verdict.computed`  
**Produced by:** Decision step of [CommitGroupResult](operations.md#commitgroupresult)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `voting -> committing`

**Payload:** `policy_version=fixed-two-seat-proof@1`, two seat/message references, quorum=2 and
verdict `consensus` or `dissent`. Fewer than two valid votes produce no event and remain
`no_quorum`.

**Consumers:** Group reducer; group-result commit; audit projection.

## group.committed

**Wire name:** `group.committed`  
**Produced by:** [CommitGroupResult](operations.md#commitgroupresult)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `committing -> completed`

**Payload:** unique group result ID, typed result payload reference, verdict event, decision rule,
participants, expected/received quorum, dissent and provenance references. Narrative exists only
when produced by a declared role.

**Consumers:** Group reducer; connection handoff; run terminal policy; runtime projection.

## handoff.published

**Wire name:** `handoff.published`  
**Produced by:** Connection-handoff step of [CommitGroupResult](operations.md#commitgroupresult)  
**Transition:** None in the source group

**Payload:** source aggregate, connection ID, group result/dissent/provenance references and target
group/version. Unique by `(source_aggregate_id, connection_id)`.

**Consumers:** Handoff materializer; downstream dependency projection.

## handoff.delivered

**Wire name:** `handoff.delivered`  
**Produced by:** Connection-handoff reconciliation within [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** May satisfy a downstream group's start guard

**Payload:** handoff event ID, target group/version and immutable target snapshot reference/hash.

**Consumers:** Downstream group scheduler; runtime projection.

## cancellation.requested

**Wire name:** `cancellation.requested`  
**Produced by:** [CancelRun](operations.md#cancelrun)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `nonterminal -> cancelling`

**Payload:** authorized principal, target run/group, reason/detail reference, active attempt IDs and
cancel command identity. Human cancellation may become run `user_abort` only if its terminal CAS wins.

**Consumers:** Group reducer; attempt cancellation scheduler; run terminal policy.

## group.cancelled

**Wire name:** `group.cancelled`  
**Produced by:** [CancelRun](operations.md#cancelrun) reconciliation step  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `cancelling -> cancelled`

**Payload:** cancellation request event, terminal/reconciled attempt set and optional persisted
cancellation deadline event.

**Consumers:** Group reducer; run terminal policy.

## group.failed

**Wire name:** `group.failed`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [GroupLifecycle](states.md#grouplifecycle) `nonterminal -> failed`

**Payload:** failure class (`protocol_ceiling`, `technical_prevention`, or declared class), cause
events, retry-policy version and detail reference. The run terminal policy, not this event alone,
maps an audit exit reason.

**Consumers:** Group reducer; run terminal policy; operator projection.

## Attempt events

## attempt.requested

**Wire name:** `attempt.requested`  
**Produced by:** [StartAgentAttempt](operations.md#startagentattempt)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `not_created -> requested`

**Payload:** operation/attempt/seat/agent identities; provider/adapter/model references;
`plan_digest`, `materialization_digest`, sealed request digest; effective-input and native-invocation
artifact references/hashes; response schema; tool profile; typed resource budget; sandbox policy;
execution-authority fence and prerequisite heads. A sandbox-launch/provider-start effect intent
commits in the same transaction.

**Consumers:** Attempt reducer; effect worker; runtime projection.

<a id="referencescoutbundledeliveredtoagent"></a>

## reference_scout.bundle_delivered_to_agent@1

**Wire name:** `reference_scout.bundle_delivered_to_agent@1`
**Produced by:** Internal
[DeliverReferenceScoutBundleToAgent](operations.md#internal-transition--deliverreferencescoutbundletoagent)
within [StartAgentAttempt](operations.md#startagentattempt)
**Transition:** No independent lifecycle; co-commits with `attempt.requested` when the target
[Attempt](domain.md#attempt) is accepted.

**Contract status:** specified for the next bounded slice; not implemented. The
[Stage G lifecycle](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle)
and [execution receipt](../../agent-provenance-telemetry/integration/stage-g/execution-receipt.md#live-local-pilot-proof)
evidence commit and terminal lifecycle delivery only. This target-agent delivery fact is distinct
from that implemented `reference_scout.bundle_delivered@1` fact.

**Payload:**

| Field | Type | Description |
|---|---|---|
| `agent_reference_delivery_id` | string | Stable preallocated identity of the accepted [AgentReferenceDelivery](domain.md#agentreferencedelivery). |
| `dispatch_id` | string | Runtime-derived scope; equals the source [ScoutRun](../../agent-provenance-telemetry/probes/reference-scout-tool.md#naming-boundary) and target [Attempt](domain.md#attempt) dispatches and the envelope `dispatch_id`. |
| `scout_run_id` | string | Source APT-owned ScoutRun with accepted commit and lifecycle-delivery facts. |
| `source_bundle_delivered_event_id` | string | Accepted `reference_scout.bundle_delivered@1` identity; never this event's `event_id`. |
| `bundle_artifact_id` | [ArtifactId](domain.md#artifactid) | Exact immutable ordered bundle. |
| `bundle_digest` | [ContentDigest](domain.md#contentdigest) | `hash(bundle_bytes)`, equal across source commit and lifecycle delivery. |
| `recommendation_ids` | ordered list<string> | Membership copied only from the preceding accepted `reference_scout.bundle_committed@1` and verified against bundle bytes; the lifecycle-delivered event has no such field. |
| `target_attempt_id` | string | Capability-derived recipient [Attempt](domain.md#attempt). |
| `target_seat_id` | [SeatId](domain.md#seatid) | Capability-derived recipient seat; equals Attempt and envelope seat. |
| `target_agent_instance_id` | string | Capability-derived recipient instance; equals Attempt and envelope instance. |
| `effective_input_artifact_id` | [ArtifactId](domain.md#artifactid) | Finalized [EffectiveInputArtifact](domain.md#effectiveinputartifact) accepted in the same transaction. |
| `effective_input_entry_ordinal` | integer | Zero-based location of the unique matching `reference_bundle` entry. |
| `effective_input_manifest_hash` | [ContentDigest](domain.md#contentdigest) | Canonical digest of the finalized ordered manifest. |
| `visibility_policy_ref` | [VersionedReference](domain.md#versionedreference) | Policy derived from the authenticated delivery capability and frozen into the matching input entry. |
| `idempotency_key` | string | Scoped retry key; equals the common-envelope key. |

**Formal invariants:**

```text
delivery = AgentReferenceDelivery(payload.agent_reference_delivery_id)

delivery.agent_reference_delivery_id = payload.agent_reference_delivery_id
delivery.dispatch_id = payload.dispatch_id = envelope.dispatch_id
delivery.scout_run_id = payload.scout_run_id
delivery.source_bundle_delivered_event_id = payload.source_bundle_delivered_event_id
delivery.bundle_artifact_id = payload.bundle_artifact_id
delivery.bundle_digest = payload.bundle_digest
delivery.recommendation_ids = payload.recommendation_ids
delivery.target_attempt_id = payload.target_attempt_id = envelope.attempt_id
delivery.target_seat_id = payload.target_seat_id = envelope.seat_id
delivery.target_agent_instance_id =
  payload.target_agent_instance_id =
  envelope.agent_instance_id
delivery.effective_input_artifact_id = payload.effective_input_artifact_id
delivery.effective_input_entry_ordinal = payload.effective_input_entry_ordinal
delivery.effective_input_manifest_hash = payload.effective_input_manifest_hash
delivery.visibility_policy_ref = payload.visibility_policy_ref
delivery.idempotency_key = payload.idempotency_key = envelope.idempotency_key
delivery.accepted_event_id = envelope.event_id
delivery.journal_offset = envelope.journal_offset
envelope.event_id != payload.source_bundle_delivered_event_id

committed_event =
  preceding accepted reference_scout.bundle_committed@1 where
    committed_event.scout_run_id = payload.scout_run_id
    and committed_event.bundle_artifact_id = payload.bundle_artifact_id
    and committed_event.bundle_digest = payload.bundle_digest

source_bundle_delivered_event =
  accepted reference_scout.bundle_delivered@1 where
    source_bundle_delivered_event.event_id = payload.source_bundle_delivered_event_id
    and source_bundle_delivered_event.scout_run_id = payload.scout_run_id
    and source_bundle_delivered_event.bundle_artifact_id = payload.bundle_artifact_id
    and source_bundle_delivered_event.bundle_digest = payload.bundle_digest

committed_event.journal_offset
  < source_bundle_delivered_event.journal_offset
  < envelope.journal_offset

ScoutRun(payload.scout_run_id).dispatch_id = payload.dispatch_id
Attempt(payload.target_attempt_id).dispatch_id = payload.dispatch_id
Attempt(payload.target_attempt_id).seat_id = payload.target_seat_id
Attempt(payload.target_attempt_id).agent_instance_id = payload.target_agent_instance_id
EffectiveInputArtifact(payload.effective_input_artifact_id).attempt_id = payload.target_attempt_id
EffectiveInputArtifact(payload.effective_input_artifact_id).manifest_hash =
  payload.effective_input_manifest_hash
EffectiveInputArtifact(payload.effective_input_artifact_id)
  .entries[payload.effective_input_entry_ordinal] =
  unique reference_bundle(
    artifact_ref = payload.bundle_artifact_id,
    content_hash = payload.bundle_digest,
    agent_reference_delivery_id = payload.agent_reference_delivery_id,
    visibility_policy_ref = payload.visibility_policy_ref)

payload.bundle_digest = hash(Artifact(payload.bundle_artifact_id).bytes)
payload.recommendation_ids =
  committed_event.recommendation_ids =
  ordered_recommendation_ids(Artifact(payload.bundle_artifact_id).bytes)
source_bundle_delivered_event hasNo recommendation_ids

atomic(
  accepted Attempt,
  finalized EffectiveInputArtifact metadata,
  sealed AgentExecutionRequest binding,
  accepted AgentReferenceDelivery,
  this event,
  attempt.requested,
  sandbox-launch effect intent)
or atomic(none)
```

**Consumers:** On implementation, the Attempt reducer MUST verify the atomic input settlement and
runtime projections MUST expose the accepted delivery evidence. APT-owned lineage/query consumers
may later correlate this fact but cannot reinterpret it as proof of source access, declared use or
claim support.

## attempt.starting

**Wire name:** `attempt.starting`  
**Produced by:** Provider-effect claim accepted through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `requested -> starting`

**Payload:** effect/claim ID, current `worker_epoch`, request digest and adapter reference.

**Consumers:** Attempt reducer; adapter worker; projection.

## attempt.running

**Wire name:** `attempt.running`  
**Produced by:** Adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `starting|waiting_tool -> running`

**Payload:** provider run identity, adapter cursor and namespaced provider metadata.

**Consumers:** Attempt reducer; runtime projection.

## attempt.waiting_tool

**Wire name:** `attempt.waiting_tool`  
**Produced by:** Adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `running -> waiting_tool`

**Payload:** authorized tool call identity, schema/input digest and tool-effect intent reference;
secrets and mutable effects remain outside durable payloads.

**Consumers:** Attempt reducer; tool worker; resource projection.

## attempt.completed

**Wire name:** `attempt.completed`  
**Produced by:** Adapter result through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `starting|running|waiting_tool|cancel_requested -> completed`

**Payload:** versioned [AgentTerminalResult](domain.md#agentterminalresult), immutable
raw-provider-output reference/hash, schema-validation status, provider result identity and current
worker epoch. Completion alone does not prove an official bus publication.

**Consumers:** Attempt reducer; parent receipt verifier; retry policy.

## host_workflow.terminal_response_committed

**Wire name:** `host_workflow.terminal_response_committed`
**Produced by:** [CommitHostTerminalResponse](operations.md#commithostterminalresponse)
**Transition:** bound host workflow turn `running -> completed|failed|cancelled|unknown`

**Payload:** `dispatch_id`, `group_id`, `seat_id`, `turn_ordinal`, `completion_kind`,
`artifact_id`, `content_hash`, `size_bytes`, receipt version, scoped idempotency key and current
binding identity. The artifact metadata and exact bytes are durable before this event is
acknowledged.

**Invariants:** the producer tuple resolves to the same confirmed parent dispatch and active turn;
the artifact is a [HostTerminalResponseArtifact](domain.md#hostterminalresponseartifact); an
identical retry returns the original event/receipt; identity, completion-kind, digest or size drift
conflicts. This event does not by itself grant a consumer visibility or launch authority.

**Consumers:** host workflow reducer; connection handoff workflow; downstream input materializer;
artifact/receipt verifier.

## host_workflow.terminal_outcome_recorded

**Wire name:** `host_workflow.terminal_outcome_recorded`
**Produced by:** [RecordHostWorkflowTerminalOutcome](operations.md#recordhostworkflowterminaloutcome)

**Payload:** bound producer tuple, one of `failed|cancelled|unknown`, reason/evidence reference and
current binding identity. It carries no response artifact and cannot satisfy an L0 required slot.

## host_workflow.input_materialized

**Wire name:** `host_workflow.input_materialized`
**Produced by:** [MaterializeHostWorkflowInput](operations.md#materializehostworkflowinput)

**Payload:** dispatch and target-turn tuple, mapping ID/version, source terminal-response ID,
payload artifact ID/hash/size, slot name/ordinal, visibility-policy reference, canonical manifest
digest and binding candidate digest. Unique by `(mapping_id,mapping_version,target_turn)`.

**Consumers:** host workflow scheduler; binding verifier; restart reducer.

## host_workflow.turn_launch_authorized

**Wire name:** `host_workflow.turn_launch_authorized`
**Produced by:** [AuthorizeHostWorkflowTurnLaunch](operations.md#authorizehostworkflowturnlaunch)

**Payload:** target turn, mapping/manifest/binding identities and digests, verified prerequisite
heads and unique launch-intent ID. It commits atomically with the unclaimed launch intent and is
unique per target turn. Reconciliation may claim the intent once; replay never creates another.

## host_workflow.turn_started

**Wire name:** `host_workflow.turn_started`

Accepted only as the observation of the unique authorized launch intent for the same target turn
and binding digest. It cannot exist without `host_workflow.turn_launch_authorized`.

## host_workflow.turn_superseded

**Wire name:** `host_workflow.turn_superseded`

Records authorized replacement of a nonterminal consumer turn or its confirmed mapping. It advances
the supersession head, invalidates stale materializations and prevents their launch CAS.

## continuation.suspended

**Wire name:** `continuation.suspended`
**Produced by:** [SuspendAgentContinuation](operations.md#suspendagentcontinuation)
**Transition:** [AgentContinuationLifecycle](states.md#agentcontinuationlifecycle) `none -> suspended`

**Payload:** continuation, dispatch, seat, agent instance, source attempt and turn, target turn,
ordered awaited mapping IDs, reconstruction snapshot artifact/hash, optional opaque-handle digest,
resume policy, deadline and aggregate version. The opaque handle itself is access-controlled adapter
state and is never published in the event.

## continuation.resume_requested

**Wire name:** `continuation.resume_requested`
**Produced by:** [ResumeAgentContinuation](operations.md#resumeagentcontinuation)
**Transition:** `suspended -> resume_requested`

**Payload:** continuation/version, `same_session` mode, complete source receipt
set, target attempt/input/request/effect identities and digests, deadline and prerequisite heads.
The event commits atomically with that target execution unit.

## continuation.resuming

**Wire name:** `continuation.resuming`
**Produced by:** accepted effect claim
**Transition:** `resume_requested -> resuming`

**Payload:** continuation, target attempt, effect, worker epoch, adapter reference and selected mode.

## continuation.resumed

**Wire name:** `continuation.resumed`
**Produced by:** adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)
**Transition:** `resuming|resume_unknown -> resumed`

**Payload:** continuation, target attempt, provider run identity, resulting agent instance, mode,
adapter cursor and worker epoch. Same-session mode must preserve the source agent instance.

## continuation.provider_lost

**Wire name:** `continuation.provider_lost`
**Produced by:** adapter reconciliation observation
**Transition:** `suspended|resuming|resume_unknown -> reconstruction_eligible`

**Payload:** continuation, optional failed-handle digest, typed definitive-no-start evidence
(`handle_definitively_unavailable_no_start` or `capability_absent_no_handle`), immutable adapter
capability reference/digest, source or target attempt, observation cursor when applicable, whether a
target existed, and the matching target attempt/effect terminal disposition when applicable. The
capability-absent form requires a preconfirmed `resume=unsupported` declaration and a matching
terminal source observation with no handle. An unknown start/resume outcome or unexplained missing
handle is not this event and cannot authorize reconstruction. Acceptance proves no provider work
started.

## continuation.resume_unknown

**Wire name:** `continuation.resume_unknown`
**Produced by:** adapter reconciliation observation
**Transition:** `resuming -> resume_unknown`

**Payload:** continuation, target attempt/effect, worker epoch, adapter cursor and typed uncertainty
evidence. It preserves the current target identity and grants no reconstruction authority.

## continuation.reconstruction_requested

**Wire name:** `continuation.reconstruction_requested`
**Produced by:** [ReconstructAgentContinuation](operations.md#reconstructagentcontinuation)
**Transition:** `reconstruction_eligible -> resume_requested`

**Payload:** continuation/version, `reconstruct` mode, definitive-loss event, failed claimed target when present,
replacement agent instance/attempt/input/request/effect identities and digests, and prerequisite
heads. The event commits atomically with the replacement execution unit.

## continuation.cancel_requested

**Wire name:** `continuation.cancel_requested`
**Produced by:** [CancelAgentContinuation](operations.md#cancelagentcontinuation)
**Transition:** `suspended|resume_requested|resuming|resume_unknown|reconstruction_eligible -> cancel_requested`

**Payload:** continuation/version, command ID and optional cancel/disposal effect ID.

## continuation.cancelled

**Wire name:** `continuation.cancelled`
**Produced by:** adapter/local disposal observation
**Transition:** `cancel_requested -> cancelled`

**Payload:** continuation, typed `disposed` or target-attempt terminal cancellation evidence,
matching command ID, handle digest when applicable, adapter cursor and worker epoch. An
`acknowledged` or `unknown` disposal observation remains nonterminal and cannot produce this event.

## continuation.expired

**Wire name:** `continuation.expired`
**Produced by:** journal-backed deadline reactor
**Transition:** `suspended|unclaimed resume_requested|reconstruction_eligible -> expired`

**Payload:** continuation/version, confirmed deadline and deadline effect identity. Wall-clock
observation proposes the command; journal order and aggregate CAS choose the winner.

## attempt.failed

**Wire name:** `attempt.failed`  
**Produced by:** Adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `starting|running|waiting_tool|cancel_requested -> failed`

**Payload:** failure class/code, retryability, provider evidence reference and worker epoch.

**Consumers:** Attempt reducer; retry/group terminal policy.

## attempt.unknown

**Wire name:** `attempt.unknown`  
**Produced by:** Recovery status reconciliation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `starting|running|waiting_tool|cancel_requested -> unknown`

**Payload:** effect retry class, last provider cursor/status evidence and reconciliation attempts.
Non-retryable unknown work is not automatically repeated.

**Consumers:** Attempt reducer; operator repair projection; run terminal policy.

## attempt.cancel_requested

**Wire name:** `attempt.cancel_requested`  
**Produced by:** [CancelRun](operations.md#cancelrun)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `nonterminal execution -> cancel_requested`

**Payload:** attempt, cancellation command and durable cancel effect IDs.

**Consumers:** Attempt reducer; adapter cancel worker.

## attempt.cancel_acknowledged

**Wire name:** `attempt.cancel_acknowledged`  
**Produced by:** Adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `cancel_requested -> cancel_requested`

**Payload:** adapter/provider acknowledgement identity and observation cursor. It is not terminal.

**Consumers:** Attempt reducer; cancellation projection.

## attempt.cancelled

**Wire name:** `attempt.cancelled`  
**Produced by:** Adapter observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `cancel_requested -> cancelled`

**Payload:** terminal provider/local cancellation evidence and worker epoch.

**Consumers:** Attempt reducer; group cancellation reconciliation.

## attempt.observation_ignored

**Wire name:** `attempt.observation_ignored`  
**Produced by:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** None

**Payload:** original attempt/event identity, reason (`late`, `stale_epoch`, `superseded_operation`
or `terminal_already_won`) and safe observation reference. Facts are retained without reversing state.

**Consumers:** Audit/debug projection; adapter conformance tests.

## Usage and effect events

## usage.observed

**Wire name:** `usage.observed`  
**Produced by:** [RecordUsageObservation](operations.md#recordusageobservation)  
**Transition:** None

**Payload:** attempt/operation/seat/group/run/dispatch, provider/adapter/model identities;
provider-record identity; nullable input, cached-input, output and reasoning counters; unit semantics;
nullable pricing reference; namespaced provider metadata and source cursor/event. Missing values are
`null`, never zero.

**Consumers:** Immutable usage projection; rollups by attempt, operation, seat, group, run and
dispatch. A rollup preserves provider attribution/nullability and is not billing truth. Empirical
completeness for tools, multi-turn, resume and retries is deferred to the Slice-2 adapter gate.

## deadline.fired

**Wire name:** `deadline.fired`  
**Produced by:** Authorized timer observation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** None by itself; a policy reactor may cause a later close/failure command

**Payload:** deadline identity, target aggregate, scheduled/observed times and policy version.

**Consumers:** Collection/round/cancellation policy. Replay uses this fact, never wall clock.

## effect.succeeded

**Wire name:** `effect.succeeded`  
**Produced by:** Effect reconciliation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** Effect-intent projection only

**Payload:** effect identity/type, claim epoch, external identity, outcome digest and source evidence.

**Consumers:** Outbox projection; the relevant policy reactor.

## effect.failed

**Wire name:** `effect.failed`  
**Produced by:** Effect reconciliation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** Effect-intent projection only

**Payload:** effect identity/type, claim epoch, retry class, failure code and evidence reference.

**Consumers:** Outbox retry policy; run/group/attempt policy.

## effect.unknown

**Wire name:** `effect.unknown`  
**Produced by:** Effect reconciliation through [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Transition:** Effect-intent projection only

**Payload:** effect identity/type, claim epoch, retry class and reconciliation evidence. For
`non_retryable`, it blocks automatic repetition.

**Consumers:** Outbox repair policy; operator projection; technical-terminal policy.

## Receipt and reveal guarantees

A successful [PublicationReceipt](domain.md#publicationreceipt) is returned only after
`publication.persisted` commits. It always contains the single canonical schema: `receipt_version`,
`status`, `event_id`, `message_id`, `journal_offset`, `payload_hash` and `idempotency_key`. An
identical retry returns those persisted canonical bytes unchanged; `transport_replayed`, if exposed,
belongs to an outer transport envelope. The parent independently verifies identity and authenticated
scope. Only that verification may atomically CAS the active candidate and append
`attempt.result_accepted` plus the message-type-specific official acceptance event; only official
events are eligible for close/quorum. Candidate and receipt projections are rebuildable from journal
facts, while the authoritative active reservation lives in `publication_candidates`.

`collection.closed` freezes eligible IDs/hashes but grants no visibility. Only `reveal.published`
commits a `RevealManifest` and changes authorized visibility. Revealed messages are delivered as a
content-addressed input to a later attempt/turn and must be listed in its effective-input artifact;
the initial proof exposes no unrestricted peer-read tool.

## Deferred event families

Pause/human-gate, replacement, abstention, sealed voting, multi-round deliberation, distributed
leases, second-provider conformance and generalized recipe events remain deferred. They require
versioned schemas and negative fixtures before their owning slice; they may not be inferred from
provider prose or added as provider-specific kernel branches.
