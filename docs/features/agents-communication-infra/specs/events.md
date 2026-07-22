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
| `schema_ref`, `schema_digest` | yes | Versioned payload contract and content digest. |
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
**Transition:** [RunLifecycle](states.md#runlifecycle) `none -> confirmed`

**Payload:** `run_id`, `dispatch_id`, `confirmed_dispatch_digest`, `dispatch_spec_ref/digest`,
`execution_authority_mode=runtime-managed`, schema/recipe/policy versions, capability-resolution
reference, and confirmation principal. The event freezes authority; it is not itself a complete
audit-ledger opening row.

**Consumers:** Run reducer; audit-opening materializer; runtime projection.

## audit_opening.requested

**Wire name:** `audit_opening.requested`  
**Produced by:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch)  
**Transition:** [RunLifecycle](states.md#runlifecycle) `confirmed -> opening_pending`

**Payload:** `dispatch_id`, canonical row reference/digest, appender contract version and effect
intent identity. It commits locally with the newly requested opening effect.

**Consumers:** Audit-ledger materializer; run reducer; effect outbox projection.

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
**Transition:** [AttemptLifecycle](states.md#attemptlifecycle) `none -> requested`

**Payload:** operation/attempt/seat/agent identities; provider/adapter/model references;
`plan_digest`, `materialization_digest`, sealed request digest; effective-input and native-invocation
artifact references/hashes; response schema; tool profile; typed resource budget; sandbox policy;
execution-authority fence and prerequisite heads. A sandbox-launch/provider-start effect intent
commits in the same transaction.

**Consumers:** Attempt reducer; effect worker; runtime projection.

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
