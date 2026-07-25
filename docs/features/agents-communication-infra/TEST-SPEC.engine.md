# Test Spec (engine-derived): agents-communication-infra

<!-- ENGINE-PROVENANCE
format_version: 1
feature: agents-communication-infra
engine_commit: 5cc5a4e
inputs:
  domain.md: sha256:4efcf238eb9b82114a684886aac3e245fde77bbdb1632587fed2fe38d4c208e4
  events.md: sha256:c6c340dd0466eb307ce33715eb73b4bc8588ca3a56bb83cc701c1f66705c757c
  interfaces.md: sha256:d4c5f0ee8981f48bb6e4033303df59a8d3110f18632544dcb86b5984b950c525
  mappings.md: sha256:5ced0b93e8bf5b2defe8eefe13ac5bfb9fef506a8ca40faef94e90bc16b2d989
  operations.md: sha256:51aceee25dc4de7ed732ce7a9658b686c7221a32451a0d5c2729df1bd372ca22
  queries.md: sha256:6702da6a8637130f1094c426e63ea4409bdcbf63994f8c5f339ce031d6c410bd
  rules.md: sha256:18ddc0d50d697bc645a03ba7e1ee89c6ca8a271473e042519bf494901d35d36e
  states.md: sha256:290311e3819f2390b7c6ec75b3a56322f51d88081aba88fbb82b93ec38b4172d
  workflows.md: sha256:f99e2ad7008003d8ca11cce06f955a909f48d5dcafb69c1f2ca408edcc3bc4f1
note: the ENGINE-REGION below is deterministic δ output, replaced wholesale on
      re-derive. Do not hand-edit it. Run `check` to detect drift.
-->

<!-- ENGINE-REGION-START — deterministic δ output; overwritten on re-derive, do not hand-edit -->

## Source Completeness Gate

| Doc | Status |
| --- | --- |
| states.md | present |
| operations.md | present |
| interfaces.md | present |
| events.md | present |
| workflows.md | present |
| queries.md | present |
| mappings.md | present |
| domain.md | present |
| rules.md | present |

## Coverage Summary

Total obligations: 831
Spec-formalization metric (pure / (pure + needs_formal)): 20.2%

| Tier | Count |
| --- | --- |
| derivable-needs-harness | 707 |
| derivable-pure | 25 |
| needs-formal | 99 |

| Rule class | Count |
| --- | --- |
| contract | 4 |
| domain-enum | 5 |
| domain-field | 253 |
| error-obligation | 26 |
| event-obligation | 52 |
| invalid-transition | 321 |
| invariant | 12 |
| mapping-row | 8 |
| needs-formal | 99 |
| query-behavior | 3 |
| rule-validation | 13 |
| valid-transition | 35 |

## Suite Partition

- Unit (derivable-pure): 25
- Integration (derivable-needs-harness): 707
- Unresolved (needs-formal): 99

## Obligations

| ID | Key | Rule | Tier | Source | Obligation |
| --- | --- | --- | --- | --- | --- |
| ACI-EVT-001 | 00056527 | event-obligation | derivable-needs-harness | events.md#usage.observed | Event usage.observed is emitted with valid payload |
| ACI-TR-001 | 002446b4 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-DOM-001 | 003b35f2 | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:6 | PublicationReceipt.journal_offset: [JournalOffset](#journaloffset) (Committed global position.) |
| ACI-DOM-235 | 0097b5bf | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:2 | AgentReferenceDelivery.scout_run_id: string |
| ACI-NF-001 | 00c34350 | needs-formal | needs-formal | operations.md#ConfirmRuntimeDispatch:rule:3 | Rule O-CONF-4: needs_formal (prose Formal) |
| ACI-TR-002 | 010169dd | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-NF-002 | 0146c46b | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:6 | Rule O-RECEIPT-7: needs_formal (prose Formal) |
| ACI-TR-003 | 0208c4b1 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `closed` is rejected (no valid transition) |
| ACI-DOM-236 | 025995d3 | domain-field | derivable-needs-harness | domain.md#Attempt:field:8 | Attempt.effective_input_artifact_id: [ArtifactId](#artifactid) |
| ACI-NF-003 | 02bf4044 | needs-formal | needs-formal | operations.md#RecordUsageObservation:rule:1 | Rule O-USAGE-2: needs_formal (prose Formal) |
| ACI-DOM-237 | 033a94ad | domain-field | derivable-needs-harness | domain.md#Attempt:field:7 | Attempt.model_ref: [VersionedReference](#versionedreference) |
| ACI-TR-004 | 03a3b92e | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `opening_pending` is rejected (no valid transition) |
| ACI-TR-005 | 051cdc42 | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:8 | Transition `starting`, `running`, `waiting_tool`, or `cancel_requested` --[`attempt.failed`](events.md#attemptfailed)--> `failed` succeeds when guarded |
| ACI-DOM-002 | 05424ad3 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:3:0 | AgentInvocationPlan.base_snapshot_ref: [ArtifactId](#artifactid) (Shared base and optional declared delta.) |
| ACI-DOM-003 | 0546abba | domain-field | derivable-needs-harness | domain.md#Group:field:2 | Group.group_version: integer |
| ACI-TR-006 | 0572a3d5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `completed` is rejected (no valid transition) |
| ACI-NF-004 | 05b0521f | needs-formal | needs-formal | operations.md#ComputeFixedProofVerdict:rule:3 | Rule O-VER-4: needs_formal (prose Formal) |
| ACI-DOM-004 | 05d25936 | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:0 | RevealManifest.reveal_manifest_id: string |
| ACI-TR-007 | 0639ce4b | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `cancelling` is rejected (no valid transition) |
| ACI-EVT-002 | 066b2f30 | event-obligation | derivable-needs-harness | events.md#run.started | Event run.started is emitted with valid payload |
| ACI-TR-008 | 066ff124 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-NF-005 | 06e229e0 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:4 | Rule O-ATT-5: needs_formal (prose Formal) |
| ACI-DOM-005 | 06ef0df5 | domain-field | derivable-needs-harness | domain.md#SandboxPolicy:field:1:2 | SandboxPolicy.process_scope: object (Explicit allow/deny rules; default deny outside declared scope.) |
| ACI-DOM-006 | 078441c3 | domain-field | derivable-needs-harness | domain.md#VersionedReference:field:2 | VersionedReference.digest: [ContentDigest](#contentdigest) (Required where executable behavior or schema is selected.) |
| ACI-TR-009 | 080e6ada | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `close_pending` is rejected (no valid transition) |
| ACI-TR-010 | 08761593 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `completed` is rejected (no valid transition) |
| ACI-TR-011 | 08aa3bff | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state none is rejected (no valid transition) |
| ACI-DOM-007 | 0a7ae9f9 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:3 | RuntimeEventEnvelope.aggregate_version: [AggregateVersion](#aggregateversion) (Contiguous within aggregate.) |
| ACI-NF-006 | 0ae11f2b | needs-formal | needs-formal | operations.md#CancelRun:rule:2 | Rule O-CANCEL-3: needs_formal (prose Formal) |
| ACI-TR-012 | 0b5a2f6e | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `execution_terminal` is rejected (no valid transition) |
| ACI-NF-007 | 0b7e1fa3 | needs-formal | needs-formal | operations.md#VerifyAuditClose:rule:0 | Rule O-ACLOSE-1: needs_formal (prose Formal) |
| ACI-DOM-008 | 0b7e739a | domain-field | derivable-needs-harness | domain.md#Artifact:field:6 | Artifact.storage_ref: string |
| ACI-DOM-009 | 0bab8892 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:8 | AgentInvocationPlan.authority_fence: [ExecutionAuthorityFence](#executionauthorityfence) (Concrete legacy/runtime cutover fence.) |
| ACI-TR-013 | 0bc4194b | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:10 | Transition any nonterminal --[`cancellation.requested`](events.md#cancellationrequested)--> `cancelling` succeeds when guarded |
| ACI-DOM-010 | 0c079ac7 | domain-field | derivable-needs-harness | domain.md#Contribution:field:2 | Contribution.seat_id: [SeatId](#seatid) |
| ACI-NF-008 | 0c6cf0b5 | needs-formal | needs-formal | operations.md#VerifyAuditClose:rule:2 | Rule O-ACLOSE-3: needs_formal (prose Formal) |
| ACI-NF-009 | 0ccf30f5 | needs-formal | needs-formal | operations.md#RecordUsageObservation:rule:4 | Rule O-USAGE-5: needs_formal (prose Formal) |
| ACI-NF-010 | 0cdeebef | needs-formal | needs-formal | states.md#RunLifecycle:invariant:6 | Invariant RUN-I7: needs_formal (prose Formal) |
| ACI-TR-014 | 0d9541d9 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-015 | 0e158080 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `pending` is rejected (no valid transition) |
| ACI-TR-016 | 0e7aff3f | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:3 | Transition `running` --[`attempt.waiting_tool`](events.md#attemptwaiting_tool)--> `waiting_tool` succeeds when guarded |
| ACI-DOM-011 | 0eae5912 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:4:0 | AgentExecutionRequest.response_schema_ref: [VersionedReference](#versionedreference) (Frozen output/tool contracts.) |
| ACI-TR-017 | 0ed9bd79 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `cancelling` is rejected (no valid transition) |
| ACI-EVT-003 | 0f7e3d44 | event-obligation | derivable-needs-harness | events.md#reconciliation.retry_requested | Event reconciliation.retry_requested is emitted with valid payload |
| ACI-NF-011 | 0f933499 | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:5 | Invariant GRP-I6: needs_formal (prose Formal) |
| ACI-TR-018 | 0f963b71 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-NF-012 | 0fd41550 | needs-formal | needs-formal | operations.md#CancelRun:rule:1 | Rule O-CANCEL-2: needs_formal (prose Formal) |
| ACI-DOM-013 | 0fd93508 | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:2 | ConfirmedDispatch.dispatch_spec: [DispatchSpec](#dispatchspec) |
| ACI-NF-013 | 1094b5d9 | needs-formal | needs-formal | operations.md#ConfirmRuntimeDispatch:rule:1 | Rule O-CONF-2: needs_formal (prose Formal) |
| ACI-ERR-017 | 10e76feb | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:3 | Error mapping for DeliverReferenceScoutBundleToAgent: "ScoutRun and recipient Attempt resolve to different dispatches" -> Authorization failure; reject. |
| ACI-DOM-014 | 10f17bca | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:0 | ConfirmedDispatch.dispatch_id: string |
| ACI-TR-019 | 113212a2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `voting` is rejected (no valid transition) |
| ACI-DOM-015 | 11647554 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:0 | PublicationCandidate.message_id: string |
| ACI-TR-020 | 11778efe | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `running` is rejected (no valid transition) |
| ACI-NF-014 | 11e29da9 | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:3 | Rule O-PUB-4: needs_formal (prose Formal) |
| ACI-TR-021 | 11fa1e87 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `waiting_tool` is rejected (no valid transition) |
| ACI-ENUM-001 | 1204d7c4 | domain-enum | derivable-needs-harness | domain.md#ReconciliationState:enum | ReconciliationState vocabulary is exactly {pending,applied,already_applied,divergent,reconciliation_required} |
| ACI-TR-022 | 1232a3f1 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state none is rejected (no valid transition) |
| ACI-MAP-001 | 127ba33d | mapping-row | derivable-needs-harness | mappings.md#RawProviderOutputToCanonicalObservations | Mapping RawProviderOutputToCanonicalObservations ([RawProviderOutput](domain.md#rawprovideroutput) -> [Attempt](domain.md#attempt) observations, [BusPublication](domain.md#buspublication) candidate) maps all fields correctly |
| ACI-EVT-004 | 12b9fb00 | event-obligation | derivable-needs-harness | events.md#attempt.cancel_requested | Event attempt.cancel_requested is emitted with valid payload |
| ACI-EVT-005 | 130b0249 | event-obligation | derivable-needs-harness | events.md#publication.rejected | Event publication.rejected is emitted with valid payload |
| ACI-EVT-006 | 132881fc | event-obligation | derivable-needs-harness | events.md#audit_close.verified | Event audit_close.verified is emitted with valid payload |
| ACI-DOM-016 | 13938ff7 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:3 | SoleWriterEvidenceBundle.writer_inventory_ref: [ArtifactId](#artifactid) (Repository and deployed-path inventory, including legacy writers.) |
| ACI-TR-023 | 13db37a9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `waiting_tool` is rejected (no valid transition) |
| ACI-TR-024 | 13e768f4 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `failed` is rejected (no valid transition) |
| ACI-EVT-007 | 140bf843 | event-obligation | derivable-needs-harness | events.md#verdict.computed | Event verdict.computed is emitted with valid payload |
| ACI-TR-025 | 14179cc6 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `committing` is rejected (no valid transition) |
| ACI-TR-026 | 149ec19c | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `committing` is rejected (no valid transition) |
| ACI-NF-089 | 157fb0d2 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:7 | Rule O-ARD-8: needs_formal (prose Formal) |
| ACI-NF-015 | 15abca65 | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:3 | Rule O-RECEIPT-4: needs_formal (prose Formal) |
| ACI-TR-027 | 15aff3ff | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `pending` is rejected (no valid transition) |
| ACI-NF-016 | 15d3ba38 | needs-formal | needs-formal | operations.md#RecordAttemptObservation:rule:0 | Rule O-OBS-1: needs_formal (prose Formal) |
| ACI-DOM-017 | 15daa71c | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:2 | EffectiveInputEntry.content_hash: [ContentDigest](#contentdigest) (Verified artifact digest.) |
| ACI-NF-017 | 16011af7 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:6 | Rule O-ATT-7: needs_formal (prose Formal) |
| ACI-TR-028 | 165f2d95 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-029 | 17970d1b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `unknown` is rejected (no valid transition) |
| ACI-INV-001 | 17acef82 | invariant | derivable-pure | states.md#GroupLifecycle:invariant:3 | Invariant GRP-I4: duplicate-capped (count cap) |
| ACI-TR-030 | 17d8c3ad | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `cancel_requested` is rejected (no valid transition) |
| ACI-ERR-001 | 17dd98be | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:1 | Error mapping for PublishBusContribution: "Same key with different digest" -> Permanent `idempotency_conflict`. |
| ACI-TR-031 | 18af92cc | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `committing` is rejected (no valid transition) |
| ACI-TR-032 | 194be8bb | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `failed` is rejected (no valid transition) |
| ACI-TR-033 | 19c7946b | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `opening_pending` is rejected (no valid transition) |
| ACI-TR-034 | 1ab0a198 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `completed` is rejected (no valid transition) |
| ACI-TR-035 | 1ab907ad | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `running` is rejected (no valid transition) |
| ACI-EVT-008 | 1b3de7fb | event-obligation | derivable-needs-harness | events.md#handoff.delivered | Event handoff.delivered is emitted with valid payload |
| ACI-DOM-020 | 1bbbafbd | domain-field | derivable-needs-harness | domain.md#Group:field:3 | Group.aggregate_version: [AggregateVersion](#aggregateversion) |
| ACI-RULE-001 | 1bd69d3d | rule-validation | derivable-pure | operations.md#PublishRevealManifest:rule:1 | Rule O-REV-2: duplicate-capped (count cap) |
| ACI-DOM-021 | 1be1cb13 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:7:0 | RuntimeEventEnvelope.causation_id: string (Provenance.) |
| ACI-DOM-022 | 1c302609 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:5 | RuntimeEventEnvelope.recorded_at: timestamp (Journal observation; governs ordering only through offset.) |
| ACI-DOM-023 | 1c97147a | domain-field | derivable-needs-harness | domain.md#Run:field:5 | Run.opening_state: [ReconciliationState](#reconciliationstate) |
| ACI-TR-036 | 1d30540e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `completed` is rejected (no valid transition) |
| ACI-TR-037 | 1d69516a | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `execution_terminal` is rejected (no valid transition) |
| ACI-TR-038 | 1e0496bd | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state none is rejected (no valid transition) |
| ACI-NF-018 | 1e06fd2c | needs-formal | needs-formal | operations.md#ConfirmRuntimeDispatch:rule:0 | Rule O-CONF-1: needs_formal (prose Formal) |
| ACI-NF-019 | 1e3c0ff0 | needs-formal | needs-formal | operations.md#StartGroup:rule:2 | Rule O-GROUP-3: needs_formal (prose Formal) |
| ACI-ERR-002 | 1e3f000a | error-obligation | derivable-needs-harness | operations.md#ConfirmRuntimeDispatch:errorstate:0 | Error mapping for ConfirmRuntimeDispatch: "Pre-confirmation routing choice is `legacy-managed`" -> Reject; preserve the legacy path and create no `ConfirmedDispatch`, runtime `Run`, journal fact or audit effect. |
| ACI-TR-039 | 1e8bf001 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `completed` is rejected (no valid transition) |
| ACI-TR-040 | 1e960e11 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `voting` is rejected (no valid transition) |
| ACI-DOM-024 | 1edb434f | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:1:1 | ResourceBudget.max_payload_bytes: integer (Non-negative finite limits.) |
| ACI-NF-020 | 206f5c87 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:7 | Invariant ATT-I8: needs_formal (prose Formal) |
| ACI-TR-041 | 209dcfb8 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `completed` is rejected (no valid transition) |
| ACI-DOM-025 | 20feb1dc | domain-field | derivable-needs-harness | domain.md#Artifact:field:2 | Artifact.media_type: string |
| ACI-DOM-238 | 21cc9269 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:16 | AgentReferenceDelivery.journal_offset: [JournalOffset](#journaloffset) |
| ACI-NF-021 | 22277f2e | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:6 | Rule O-PUB-7: needs_formal (prose Formal) |
| ACI-TR-042 | 22fcc7f9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-026 | 23600d8e | domain-field | derivable-needs-harness | domain.md#BusPublication:field:0 | BusPublication.idempotency_key: string (Non-empty; scoped to authenticated run/group/version/seat.) |
| ACI-DOM-027 | 23a89aa7 | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:6 | ConfirmedDispatch.confirmed_at: timestamp |
| ACI-TR-043 | 23bf00a4 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `waiting_tool` is rejected (no valid transition) |
| ACI-DOM-028 | 2438f87a | domain-field | derivable-needs-harness | domain.md#SandboxPolicy:field:2 | SandboxPolicy.credential_refs: list<[VersionedReference](#versionedreference)> (Opaque launcher-resolved grants; secrets never enter durable payloads.) |
| ACI-DOM-029 | 2476fa89 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:1:0 | RuntimeEventEnvelope.schema_ref: [VersionedReference](#versionedreference), [ContentDigest](#contentdigest) (Exact payload contract.) |
| ACI-TR-044 | 24776696 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `running` is rejected (no valid transition) |
| ACI-TR-045 | 2489312d | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `running` is rejected (no valid transition) |
| ACI-ERR-003 | 249153f5 | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:5 | Error mapping for VerifyPublicationReceipt: "Candidate was abandoned" -> `publication_candidate_abandoned`; reject permanently even if late terminal evidence arrives. |
| ACI-EVT-009 | 24caef16 | event-obligation | derivable-needs-harness | events.md#group.cancelled | Event group.cancelled is emitted with valid payload |
| ACI-DOM-030 | 254a1ba7 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:5 | SoleWriterEvidenceBundle.auxiliary_lint_result_ref: [ArtifactId](#artifactid) (Nullable defense-in-depth evidence; never sufficient alone.) |
| ACI-DOM-031 | 255688aa | domain-field | derivable-needs-harness | domain.md#Artifact:field:4 | Artifact.classification: [ArtifactClassification](#artifactclassification) |
| ACI-ERR-004 | 25e34801 | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:1 | Error mapping for VerifyPublicationReceipt: "`event_id` does not resolve to one committed acceptance event" -> `publication_receipt_forged`; reject and record an auditable security observation. |
| ACI-DOM-032 | 26da62bf | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:5 | EffectIntent.status: [EffectStatus](#effectstatus) |
| ACI-DOM-033 | 270a750f | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:0:2 | AgentExecutionRequest.seat_id: string (Runtime-authenticated identities.) |
| ACI-TR-046 | 2749cb82 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `waiting_tool` is rejected (no valid transition) |
| ACI-DOM-034 | 28097a43 | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:0:1 | ExecutionAuthorityFence.run_id: string (Exact runtime-owned execution.) |
| ACI-TR-047 | 28221ca2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `completed` is rejected (no valid transition) |
| ACI-DOM-035 | 282677d5 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:4:0 | AgentInvocationPlan.response_schema_ref: [VersionedReference](#versionedreference) (Frozen output/tool contracts.) |
| ACI-NF-022 | 286dbd68 | needs-formal | needs-formal | operations.md#VerifyAuditOpening:rule:3 | Rule O-OPEN-4: needs_formal (prose Formal) |
| ACI-DOM-036 | 28cab90d | domain-field | derivable-needs-harness | domain.md#Group:field:4 | Group.policy_ref: [VersionedReference](#versionedreference) |
| ACI-TR-048 | 28fae33f | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-TR-049 | 2a64741d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-050 | 2a693efa | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `running` is rejected (no valid transition) |
| ACI-DOM-037 | 2abd7890 | domain-field | derivable-needs-harness | domain.md#Run:field:1 | Run.dispatch_id: string |
| ACI-TR-051 | 2afd3675 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `unknown` is rejected (no valid transition) |
| ACI-DOM-038 | 2ba58210 | domain-field | derivable-needs-harness | domain.md#Artifact:field:0 | Artifact.artifact_id: [ArtifactId](#artifactid) |
| ACI-TR-052 | 2c1a799d | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `failed` is rejected (no valid transition) |
| ACI-TR-053 | 2c1e9992 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `close_pending` is rejected (no valid transition) |
| ACI-INV-002 | 2c242026 | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:1 | Invariant ATT-I2: present (existence) |
| ACI-IF-001 | 2d24171b | contract | derivable-needs-harness | interfaces.md#POST /dispatches/{dispatch_id}/confirm:response:1 | POST /dispatches/{dispatch_id}/confirm -> 200 (identical idempotent replay) |
| ACI-NF-090 | 2d4ef614 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:2 | Rule O-ARD-3: needs_formal (prose Formal) |
| ACI-TR-054 | 2d6cfdec | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `collecting` is rejected (no valid transition) |
| ACI-NF-023 | 2e4ccfa7 | needs-formal | needs-formal | operations.md#ElectRunTerminal:rule:2 | Rule O-TERM-3: needs_formal (prose Formal) |
| ACI-DOM-039 | 2e900b97 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:5 | AgentTerminalResult.provider_metadata: object (Namespaced and non-authoritative.) |
| ACI-TR-055 | 2ed71a1d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `revealing` is rejected (no valid transition) |
| ACI-DOM-040 | 2edf6c23 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:4 | EffectiveInputEntry.message_id: string (Required for message/reveal entries; otherwise nullable.) |
| ACI-TR-056 | 2efff95e | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `closed` is rejected (no valid transition) |
| ACI-EVT-010 | 2f57ec10 | event-obligation | derivable-needs-harness | events.md#audit_close.requested | Event audit_close.requested is emitted with valid payload |
| ACI-RULE-002 | 2fa1cb3c | rule-validation | derivable-pure | operations.md#RecordAttemptObservation:rule:1 | Rule O-OBS-2: duplicate-capped (count cap) |
| ACI-DOM-041 | 2ffe835a | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:0:0 | AgentInvocationPlan.attempt_id: string (Runtime-authenticated identities.) |
| ACI-DOM-042 | 301db0e0 | domain-field | derivable-needs-harness | domain.md#VersionedReference:field:0 | VersionedReference.name: string (Namespaced identifier.) |
| ACI-EVT-011 | 3041c42d | event-obligation | derivable-needs-harness | events.md#critique.accepted | Event critique.accepted is emitted with valid payload |
| ACI-TR-057 | 309fb68c | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:9 | Transition `starting`, `running`, `waiting_tool`, or `cancel_requested` --[`attempt.unknown`](events.md#attemptunknown)--> `unknown` succeeds when guarded |
| ACI-EVT-012 | 30a10984 | event-obligation | derivable-needs-harness | events.md#attempt.running | Event attempt.running is emitted with valid payload |
| ACI-DOM-043 | 30c0a888 | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:5 | RawProviderOutput.provider_run_id: string |
| ACI-DOM-044 | 3119a3db | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:3 | EffectiveInputArtifact.role_delta_ref: [ArtifactId](#artifactid) |
| ACI-TR-058 | 314b38f7 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `confirmed` is rejected (no valid transition) |
| ACI-TR-059 | 31612bc7 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `committing` is rejected (no valid transition) |
| ACI-TR-060 | 31c8ffb5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-045 | 32037278 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:0:0 | SoleWriterEvidenceBundle.store_ref: [VersionedReference](#versionedreference) (Exact store, validated writer and host enforcement profile.) |
| ACI-MAP-002 | 32eaf4f6 | mapping-row | derivable-needs-harness | mappings.md#UsageObservationToRollups | Mapping UsageObservationToRollups (immutable [UsageObservation](events.md#usageobserved) -> rebuildable usage rollups) maps all fields correctly |
| ACI-DOM-046 | 32fdd12e | domain-field | derivable-needs-harness | domain.md#GroupResult:field:6 | GroupResult.result_payload_artifact_id: [ArtifactId](#artifactid) |
| ACI-TR-061 | 33084112 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:9 | Transition `committing` --[`group.committed`](events.md#groupcommitted)--> `completed` succeeds when guarded |
| ACI-ERR-018 | 33594d19 | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:4 | Error mapping for DeliverReferenceScoutBundleToAgent: "Target seat or agent instance differs from the authenticated Attempt" -> Authorization failure; reject. |
| ACI-EVT-013 | 335d8b9d | event-obligation | derivable-needs-harness | events.md#effect.unknown | Event effect.unknown is emitted with valid payload |
| ACI-DOM-239 | 33e05c3c | domain-field | derivable-needs-harness | domain.md#Attempt:field:5 | Attempt.provider_ref: [VersionedReference](#versionedreference) |
| ACI-TR-062 | 3428d97f | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `committing` is rejected (no valid transition) |
| ACI-TR-063 | 346bb344 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `voting` is rejected (no valid transition) |
| ACI-DOM-240 | 347dbd71 | domain-field | derivable-needs-harness | domain.md#Attempt:field:3 | Attempt.seat_id: [SeatId](#seatid) |
| ACI-TR-064 | 34bbb2f8 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-065 | 34ef6fc5 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-048 | 353250c0 | domain-field | derivable-needs-harness | domain.md#GroupResult:field:3 | GroupResult.decision_rule_ref: [VersionedReference](#versionedreference) |
| ACI-ERR-019 | 35a5a523 | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:9 | Error mapping for DeliverReferenceScoutBundleToAgent: "Any member of the complete StartAgentAttempt transaction fails" -> Roll back all members; emit neither `attempt.requested` nor target-delivery event. |
| ACI-EVT-014 | 35c710fb | event-obligation | derivable-needs-harness | events.md#effect.failed | Event effect.failed is emitted with valid payload |
| ACI-TR-066 | 35c7ff01 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `execution_terminal` is rejected (no valid transition) |
| ACI-TR-067 | 35f3a56c | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `opening_pending` is rejected (no valid transition) |
| ACI-TR-068 | 36624718 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `opening_pending` is rejected (no valid transition) |
| ACI-NF-024 | 367b6392 | needs-formal | needs-formal | operations.md#ConfirmRuntimeDispatch:rule:2 | Rule O-CONF-3: needs_formal (prose Formal) |
| ACI-DOM-049 | 3694a01c | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:5 | RevealManifest.collection_closed_event_id: string |
| ACI-DOM-241 | 373d422b | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:14 | AgentReferenceDelivery.idempotency_key: string |
| ACI-TR-069 | 37461b04 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `pending` is rejected (no valid transition) |
| ACI-DOM-050 | 377cb18e | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:3:1 | AgentExecutionRequest.provider_invocation_ref: [ArtifactId](#artifactid) (Exact finalized observable/native inputs.) |
| ACI-DOM-242 | 37861398 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:7 | AgentReferenceDelivery.target_attempt_id: string |
| ACI-TR-070 | 37a773bc | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `cancelling` is rejected (no valid transition) |
| ACI-DOM-051 | 37af732f | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:2:0 | PublicationCandidate.group_aggregate_id: string |
| ACI-DOM-052 | 380d0295 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:0:1 | SoleWriterEvidenceBundle.writer_ref: [VersionedReference](#versionedreference) (Exact store, validated writer and host enforcement profile.) |
| ACI-TR-071 | 38209eaa | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state none is rejected (no valid transition) |
| ACI-EVT-015 | 3879c18f | event-obligation | derivable-needs-harness | events.md#position.accepted | Event position.accepted is emitted with valid payload |
| ACI-NF-025 | 388360d5 | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:2 | Rule O-RECEIPT-3: needs_formal (prose Formal) |
| ACI-NF-026 | 38a96287 | needs-formal | needs-formal | operations.md#PublishRevealManifest:rule:0 | Rule O-REV-1: needs_formal (prose Formal) |
| ACI-NF-027 | 38cc4d76 | needs-formal | needs-formal | operations.md#PublishConnectionHandoff:rule:0 | Rule O-HAND-1: needs_formal (prose Formal) |
| ACI-DOM-053 | 38ea153d | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:2:3 | PublicationCandidate.seat_id: string |
| ACI-TR-072 | 3923d50f | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state none is rejected (no valid transition) |
| ACI-TR-073 | 3944ac94 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `completed` is rejected (no valid transition) |
| ACI-TR-074 | 39562e0b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `failed` is rejected (no valid transition) |
| ACI-DOM-054 | 39cef3df | domain-field | derivable-needs-harness | domain.md#GroupResult:field:0 | GroupResult.group_result_id: string |
| ACI-TR-075 | 3a8d151a | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `pending` is rejected (no valid transition) |
| ACI-NF-028 | 3b025ca1 | needs-formal | needs-formal | operations.md#VerifyAuditOpening:rule:1 | Rule O-OPEN-2: needs_formal (prose Formal) |
| ACI-RULE-004 | 3b5a8125 | rule-validation | derivable-pure | operations.md#PublishRevealManifest:rule:1 | Rule O-REV-2: first-allowed (count cap) |
| ACI-TR-076 | 3b7da99b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `failed` is rejected (no valid transition) |
| ACI-ENUM-002 | 3bb099c4 | domain-enum | derivable-needs-harness | domain.md#ExecutionAuthorityMode:enum | ExecutionAuthorityMode vocabulary is exactly {legacy-managed,runtime-managed} |
| ACI-TR-077 | 3cf18805 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `ready` is rejected (no valid transition) |
| ACI-DOM-055 | 3d2ab336 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:1:1 | RuntimeEventEnvelope.schema_digest: [VersionedReference](#versionedreference), [ContentDigest](#contentdigest) (Exact payload contract.) |
| ACI-TR-078 | 3d5593ef | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state any nonterminal is rejected (no valid transition) |
| ACI-TR-079 | 3d675132 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `revealing` is rejected (no valid transition) |
| ACI-TR-080 | 3d8b8473 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `failed` is rejected (no valid transition) |
| ACI-NF-091 | 3d957d74 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:1 | Rule O-ATT-2: needs_formal (prose Formal) |
| ACI-TR-081 | 3db1ec5c | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `opening_pending` is rejected (no valid transition) |
| ACI-DOM-056 | 3dcecb85 | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:6 | RawProviderOutput.payload_hash: [ContentDigest](#contentdigest) |
| ACI-EVT-016 | 3deceaec | event-obligation | derivable-needs-harness | events.md#attempt.observation_ignored | Event attempt.observation_ignored is emitted with valid payload |
| ACI-TR-082 | 3e427701 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `collecting` is rejected (no valid transition) |
| ACI-RULE-005 | 3e821081 | rule-validation | derivable-pure | operations.md#VerifyPublicationReceipt:rule:4 | Rule O-RECEIPT-5: duplicate-capped (count cap) |
| ACI-DOM-057 | 3eace821 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:8 | EffectiveInputArtifact.adapter_wrapper_refs: ordered list<[ArtifactId](#artifactid)> |
| ACI-DOM-058 | 3ebb40b5 | domain-field | derivable-needs-harness | domain.md#Artifact:field:1 | Artifact.content_hash: [ContentDigest](#contentdigest) |
| ACI-TR-083 | 3f0ad9ea | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state none is rejected (no valid transition) |
| ACI-DOM-243 | 3f3b3f90 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:4 | AgentReferenceDelivery.bundle_artifact_id: [ArtifactId](#artifactid) |
| ACI-TR-084 | 3fa0e151 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-085 | 3fca8ce7 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:4 | Transition `reconciliation_required` --`reconciliation.retry_requested`--> `opening_pending` succeeds when guarded |
| ACI-TR-086 | 3fcc9d40 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `pending` is rejected (no valid transition) |
| ACI-NF-029 | 40243696 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:2 | Invariant ATT-I3: needs_formal (prose Formal) |
| ACI-INV-003 | 4036bcc4 | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:4 | Invariant ATT-I5: first-allowed (count cap) |
| ACI-EVT-017 | 40746b6c | event-obligation | derivable-needs-harness | events.md#run.execution_terminal_elected | Event run.execution_terminal_elected is emitted with valid payload |
| ACI-RULE-006 | 414bd86e | rule-validation | derivable-pure | operations.md#VerifyPublicationReceipt:rule:4 | Rule O-RECEIPT-5: first-allowed (count cap) |
| ACI-TR-087 | 4225ce8e | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `ready` is rejected (no valid transition) |
| ACI-NF-030 | 42648cd4 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:8 | Invariant ATT-I9: needs_formal (prose Formal) |
| ACI-NF-092 | 42f45ca9 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:8 | Rule O-ARD-9: needs_formal (prose Formal) |
| ACI-ERR-020 | 4380021d | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:6 | Error mapping for DeliverReferenceScoutBundleToAgent: "`(scout_run_id,target_attempt_id)` already has a nonidentical delivery" -> Uniqueness conflict; return no new receipt. |
| ACI-DOM-061 | 441b19ec | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:3 | PublicationReceipt.message_id: string (Existing durable publication candidate.) |
| ACI-DOM-062 | 4489ca95 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:0:1 | AgentInvocationPlan.operation_id: string (Runtime-authenticated identities.) |
| ACI-TR-088 | 449853f7 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `running` is rejected (no valid transition) |
| ACI-RULE-007 | 44a29150 | rule-validation | derivable-pure | operations.md#CloseCollection:rule:1 | Rule O-CLOSE-2: absent (existence) |
| ACI-RULE-008 | 44c16902 | rule-validation | derivable-pure | operations.md#CloseCollection:rule:1 | Rule O-CLOSE-2: present (existence) |
| ACI-TR-089 | 44c2d4df | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `closed` is rejected (no valid transition) |
| ACI-TR-090 | 44f480a0 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state any nonterminal is rejected (no valid transition) |
| ACI-TR-091 | 4594ec87 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `collecting` is rejected (no valid transition) |
| ACI-TR-092 | 45ba4051 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `requested` is rejected (no valid transition) |
| ACI-TR-093 | 4638b44d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `voting` is rejected (no valid transition) |
| ACI-DOM-063 | 463b1f7c | domain-field | derivable-needs-harness | domain.md#BusPublication:field:4 | BusPublication.reply_to_message_ids: list<string> (All visible to the principal.) |
| ACI-TR-094 | 46544a8f | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `starting` is rejected (no valid transition) |
| ACI-TR-095 | 475036cf | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `running` is rejected (no valid transition) |
| ACI-TR-096 | 481e40d9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `waiting_tool` is rejected (no valid transition) |
| ACI-IF-002 | 484d5787 | contract | derivable-needs-harness | interfaces.md#POST /dispatches/{dispatch_id}/confirm:response:2 | POST /dispatches/{dispatch_id}/confirm -> 409 (key reused with another digest, stale aggregate version or authority mode already assigned) |
| ACI-TR-097 | 487aa714 | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:5 | Transition any applicable nonterminal --[`attempt.cancel_requested`](events.md#attemptcancel_requested)--> `cancel_requested` succeeds when guarded |
| ACI-TR-098 | 48b63cbe | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:11 | Transition `cancelling` --[`group.cancelled`](events.md#groupcancelled)--> `cancelled` succeeds when guarded |
| ACI-DOM-064 | 4a34bc94 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:0 | DispatchSpec.recipe_ref: [VersionedReference](#versionedreference) (Digest-pinned.) |
| ACI-TR-099 | 4a3a8e08 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `execution_terminal` is rejected (no valid transition) |
| ACI-TR-100 | 4af55dd2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state any nonterminal is rejected (no valid transition) |
| ACI-DOM-065 | 4b754bbe | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:0 | PublicationReceipt.receipt_version: string (Supported receipt schema version.) |
| ACI-EVT-018 | 4bd86728 | event-obligation | derivable-needs-harness | events.md#effect.succeeded | Event effect.succeeded is emitted with valid payload |
| ACI-DOM-066 | 4bf62e95 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:1:1 | AgentExecutionRequest.adapter_ref: [VersionedReference](#versionedreference) (Confirmed selection; no provider-specific kernel branch.) |
| ACI-TR-101 | 4c3f7e2d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `pending` is rejected (no valid transition) |
| ACI-TR-102 | 4c4f32c7 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `cancelling` is rejected (no valid transition) |
| ACI-QRY-001 | 4c78b680 | query-behavior | derivable-needs-harness | queries.md#GetRunStatus | Query GetRunStatus returns its projected read model without side effects |
| ACI-DOM-244 | 4dca0cf7 | domain-field | derivable-needs-harness | domain.md#Attempt:field:4 | Attempt.agent_instance_id: string |
| ACI-DOM-245 | 4dcfeaae | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:9 | AgentReferenceDelivery.target_agent_instance_id: string |
| ACI-NF-031 | 4de5e8b0 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:3 | Rule O-ATT-4: needs_formal (prose Formal) |
| ACI-TR-103 | 4e67deff | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:5 | Transition `ready` --[`run.started`](events.md#runstarted)--> `running` succeeds when guarded |
| ACI-TR-104 | 4edeb2cf | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state none is rejected (no valid transition) |
| ACI-ERR-005 | 4eeb4285 | error-obligation | derivable-needs-harness | operations.md#ConfirmRuntimeDispatch:errorstate:1 | Error mapping for ConfirmRuntimeDispatch: "Existing dispatch/run identity has identical digest" -> Return the stable original receipt. |
| ACI-INV-004 | 4f149290 | invariant | derivable-pure | states.md#RunLifecycle:invariant:0 | Invariant RUN-I1: absent (existence) |
| ACI-MAP-003 | 4f7ecb98 | mapping-row | derivable-needs-harness | mappings.md#RuntimeTerminalToExitReason | Mapping RuntimeTerminalToExitReason (unique run-level terminal cause -> audit-ledger `exit_reason`) maps all fields correctly |
| ACI-TR-105 | 4f7f52ec | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `requested` is rejected (no valid transition) |
| ACI-TR-106 | 4f87d5ad | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state any nonterminal is rejected (no valid transition) |
| ACI-TR-107 | 4fb1ee73 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `deliberating` is rejected (no valid transition) |
| ACI-NF-032 | 4fdd3641 | needs-formal | needs-formal | operations.md#RecordAttemptObservation:rule:3 | Rule O-OBS-4: needs_formal (prose Formal) |
| ACI-DOM-068 | 50430116 | domain-field | derivable-needs-harness | domain.md#Run:field:2 | Run.spec_digest: [ContentDigest](#contentdigest) |
| ACI-DOM-069 | 50d76254 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:2 | SoleWriterEvidenceBundle.filesystem_acl_evidence_ref: [ArtifactId](#artifactid) (File/directory permissions and effective-access inspection.) |
| ACI-TR-108 | 50e5da2d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-109 | 51790543 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-DOM-070 | 5226ef68 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:1:2 | AgentInvocationPlan.model_ref: [VersionedReference](#versionedreference) (Frozen selection.) |
| ACI-TR-110 | 5245c567 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-111 | 528eca8e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-TR-112 | 52c8bbdc | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `failed` is rejected (no valid transition) |
| ACI-NF-093 | 546cf481 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:1 | Rule O-ARD-2: needs_formal (prose Formal) |
| ACI-TR-113 | 55a94fef | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `collecting` is rejected (no valid transition) |
| ACI-DOM-246 | 55bac2db | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:8 | AgentReferenceDelivery.target_seat_id: [SeatId](#seatid) |
| ACI-TR-114 | 55c0bdea | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `collecting` is rejected (no valid transition) |
| ACI-TR-115 | 55c2f813 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `completed` is rejected (no valid transition) |
| ACI-TR-116 | 56139b13 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `opening_pending` is rejected (no valid transition) |
| ACI-DOM-071 | 56342934 | domain-field | derivable-needs-harness | domain.md#BusPublication:field:2 | BusPublication.round_id: string (Must equal an active allowed round.) |
| ACI-TR-117 | 56a94610 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `opening_pending` is rejected (no valid transition) |
| ACI-DOM-072 | 57968a7a | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:5 | ConfirmedDispatch.confirmed_by: string |
| ACI-TR-118 | 57d3ed27 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `close_pending` is rejected (no valid transition) |
| ACI-TR-119 | 580d1db1 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `ready` is rejected (no valid transition) |
| ACI-TR-120 | 5816be1e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `completed` is rejected (no valid transition) |
| ACI-RULE-009 | 58273721 | rule-validation | derivable-pure | operations.md#RecordAttemptObservation:rule:1 | Rule O-OBS-2: first-allowed (count cap) |
| ACI-DOM-073 | 587dbc7e | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:2 | DispatchSpec.group_graph: object (Finite and valid before confirmation.) |
| ACI-NF-033 | 58821502 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:6 | Invariant ATT-I7: needs_formal (prose Formal) |
| ACI-DOM-074 | 58df11c1 | domain-field | derivable-needs-harness | domain.md#Artifact:field:3 | Artifact.schema_ref: [VersionedReference](#versionedreference) |
| ACI-ERR-006 | 590321d3 | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:2 | Error mapping for VerifyPublicationReceipt: "Any receipt field differs from persisted event/message evidence" -> `publication_receipt_mismatch`; reject and identify only the mismatched field names in safe diagnostics. |
| ACI-TR-121 | 591dec1c | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:4 | Transition `waiting_tool` --[`attempt.running`](events.md#attemptrunning)--> `running` succeeds when guarded |
| ACI-TR-122 | 598ee0a0 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state none is rejected (no valid transition) |
| ACI-INV-005 | 59e284b3 | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:3 | Invariant ATT-I4: duplicate-capped (count cap) |
| ACI-DOM-075 | 5a45f12b | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:6 | EffectiveInputArtifact.response_schema_ref: [VersionedReference](#versionedreference) |
| ACI-TR-123 | 5a768d41 | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:1 | Transition `requested` --[`attempt.starting`](events.md#attemptstarting)--> `starting` succeeds when guarded |
| ACI-TR-124 | 5ac0a636 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `running` is rejected (no valid transition) |
| ACI-IF-003 | 5af67426 | contract | derivable-needs-harness | interfaces.md#POST /dispatches/{dispatch_id}/confirm:response:3 | POST /dispatches/{dispatch_id}/confirm -> 422 (draft, digest, schema or confirmation authority invalid, including `legacy-managed` routing) |
| ACI-TR-125 | 5b033ce3 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `committing` is rejected (no valid transition) |
| ACI-TR-126 | 5c460784 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `collecting` is rejected (no valid transition) |
| ACI-TR-127 | 5c665234 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-076 | 5cd82802 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:6 | PublicationCandidate.idempotency_key: string |
| ACI-TR-128 | 5d13b002 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:5 | Transition `deliberating` --[`critique.accepted`](events.md#critiqueaccepted)--> `deliberating` succeeds when guarded |
| ACI-INV-006 | 5d18a13e | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:4 | Invariant ATT-I5: duplicate-capped (count cap) |
| ACI-TR-129 | 5de3bc25 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `voting` is rejected (no valid transition) |
| ACI-TR-130 | 5e52b786 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `close_pending` is rejected (no valid transition) |
| ACI-QRY-002 | 5eca1910 | query-behavior | derivable-needs-harness | queries.md#GetVisibleGroupMessages | Query GetVisibleGroupMessages returns its projected read model without side effects |
| ACI-TR-131 | 5eebcd57 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `committing` is rejected (no valid transition) |
| ACI-TR-132 | 5ef48ccc | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-133 | 5f07b20f | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:2 | Transition `opening_pending` --[`audit_opening.verified`](events.md#audit_openingverified)--> `ready` succeeds when guarded |
| ACI-TR-134 | 5f2cf91d | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `close_pending` is rejected (no valid transition) |
| ACI-TR-135 | 5f5918c9 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:4 | Transition `revealing` --[`reveal.published`](events.md#revealpublished)--> `deliberating` succeeds when guarded |
| ACI-TR-136 | 5fdf2204 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `starting` is rejected (no valid transition) |
| ACI-ERR-007 | 60163b2e | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:5 | Error mapping for PublishBusContribution: "Schema, size, budget or reply visibility fails" -> Reject; no contribution transition. |
| ACI-DOM-077 | 60a7cf13 | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:2 | RevealManifest.round_id: string |
| ACI-TR-137 | 60c2b009 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `starting` is rejected (no valid transition) |
| ACI-NF-034 | 60d78b0f | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:5 | Rule O-RECEIPT-6: needs_formal (prose Formal) |
| ACI-TR-138 | 6113a9b5 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `committing` is rejected (no valid transition) |
| ACI-TR-139 | 61356881 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-TR-140 | 61366bd7 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:1 | Transition `confirmed` --[`audit_opening.requested`](events.md#audit_openingrequested)--> `opening_pending` succeeds when guarded |
| ACI-DOM-078 | 61852087 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:4:1 | AgentExecutionRequest.tool_profile_ref: [VersionedReference](#versionedreference) (Frozen output/tool contracts.) |
| ACI-MAP-004 | 61bbc90b | mapping-row | derivable-needs-harness | mappings.md#RevealManifestToEffectiveInput | Mapping RevealManifestToEffectiveInput ([RevealManifest](domain.md#revealmanifest) and authorized message artifacts -> later [EffectiveInputArtifact](domain.md#effectiveinputartifact)) maps all fields correctly |
| ACI-TR-141 | 61cf04dd | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `close_pending` is rejected (no valid transition) |
| ACI-TR-142 | 621ce602 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `completed` is rejected (no valid transition) |
| ACI-DOM-079 | 629c7732 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:1 | EffectiveInputArtifact.attempt_id: string |
| ACI-ERR-021 | 6308bff7 | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:8 | Error mapping for DeliverReferenceScoutBundleToAgent: "Aggregate or prerequisite head is stale" -> CAS conflict; recompute eligibility before retry. |
| ACI-TR-143 | 630e1ccd | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `deliberating` is rejected (no valid transition) |
| ACI-NF-035 | 6317ecd9 | needs-formal | needs-formal | operations.md#StartGroup:rule:1 | Rule O-GROUP-2: needs_formal (prose Formal) |
| ACI-DOM-080 | 63f9a4bc | domain-field | derivable-needs-harness | domain.md#GroupResult:field:5 | GroupResult.dissent_message_ids: list<string> |
| ACI-DOM-081 | 64208193 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:5 | EffectiveInputEntry.reveal_manifest_id: string (Required for `reveal_message`; otherwise nullable.) |
| ACI-DOM-082 | 64332a29 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:1:1 | AgentInvocationPlan.adapter_ref: [VersionedReference](#versionedreference) (Frozen selection.) |
| ACI-TR-144 | 64d9b225 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-EVT-019 | 64eadaea | event-obligation | derivable-needs-harness | events.md#attempt.cancel_acknowledged | Event attempt.cancel_acknowledged is emitted with valid payload |
| ACI-DOM-083 | 65650415 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:4 | AgentTerminalResult.publication_receipt: [PublicationReceipt](#publicationreceipt) (Required for an official bus result; nullable for non-publication terminals.) |
| ACI-TR-145 | 6567a6ee | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state none is rejected (no valid transition) |
| ACI-DOM-247 | 659fc3e6 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:6 | EffectiveInputEntry.agent_reference_delivery_id: string (Required only for `reference_bundle`; identifies the accepted target-agent delivery.) |
| ACI-DOM-084 | 65de3e4c | domain-field | derivable-needs-harness | domain.md#MaterializedAgentInvocation:field:3 | MaterializedAgentInvocation.materializer_ref: [VersionedReference](#versionedreference) (Exact adapter materializer.) |
| ACI-TR-146 | 66971256 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `running` is rejected (no valid transition) |
| ACI-NF-036 | 66c9761b | needs-formal | needs-formal | operations.md#RecordAttemptObservation:rule:4 | Rule O-OBS-5: needs_formal (prose Formal) |
| ACI-DOM-248 | 67202c58 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:13 | AgentReferenceDelivery.visibility_policy_ref: [VersionedReference](#versionedreference) |
| ACI-DOM-249 | 67495055 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:0 | AgentReferenceDelivery.agent_reference_delivery_id: string |
| ACI-NF-037 | 675e4a01 | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:7 | Invariant GRP-I8: needs_formal (prose Formal) |
| ACI-TR-147 | 67b75bdf | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-085 | 67c10718 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:2:0 | AgentInvocationPlan.role_contract_ref: [VersionedReference](#versionedreference) (Compiled local contract.) |
| ACI-TR-148 | 681eba7d | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `closed` is rejected (no valid transition) |
| ACI-NF-038 | 685b2928 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:0 | Invariant ATT-I1: needs_formal (prose Formal) |
| ACI-DOM-086 | 68785af5 | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:1 | RawProviderOutput.attempt_id: string |
| ACI-DOM-087 | 69776a2c | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:3 | ExecutionAuthorityFence.legacy_watcher_disabled_evidence_ref: [ArtifactId](#artifactid) (Concrete verified cutover evidence.) |
| ACI-TR-149 | 69826795 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `ready` is rejected (no valid transition) |
| ACI-ERR-008 | 69c2c499 | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:3 | Error mapping for PublishBusContribution: "Stale phase, round or capability" -> Reject and record an auditable security/protocol observation. |
| ACI-TR-150 | 6a5a0a78 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-088 | 6ad345de | domain-field | derivable-needs-harness | domain.md#Group:field:5 | Group.eligible_seat_ids: list<[SeatId](#seatid)> |
| ACI-TR-151 | 6b185201 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `completed` is rejected (no valid transition) |
| ACI-TR-152 | 6b4ff2c2 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-TR-153 | 6b77dd05 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `running` is rejected (no valid transition) |
| ACI-TR-154 | 6b826e90 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `cancelling` is rejected (no valid transition) |
| ACI-TR-155 | 6b827771 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `revealing` is rejected (no valid transition) |
| ACI-TR-156 | 6c2c6c71 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-089 | 6d2d43cc | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:3:0 | PublicationCandidate.round_id: string |
| ACI-DOM-090 | 6dfa6d9c | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:2 | ExecutionAuthorityFence.cutover_epoch: integer (Monotonic authority epoch.) |
| ACI-DOM-091 | 6e685f17 | domain-field | derivable-needs-harness | domain.md#BusPublication:field:3 | BusPublication.message_type: string (Phase and schema allowlisted.) |
| ACI-TR-157 | 6ecb11ff | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `cancelling` is rejected (no valid transition) |
| ACI-TR-158 | 6f03623e | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `collecting` is rejected (no valid transition) |
| ACI-DOM-092 | 6f047629 | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:5 | PublicationReceipt.idempotency_key: string (Equals persisted scoped key.) |
| ACI-TR-159 | 7015118b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `unknown` is rejected (no valid transition) |
| ACI-NF-039 | 7052fea2 | needs-formal | needs-formal | operations.md#ElectRunTerminal:rule:0 | Rule O-TERM-1: needs_formal (prose Formal) |
| ACI-DOM-093 | 70a3cdb7 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:1:0 | AgentTerminalResult.attempt_id: string (Must match the sealed request.) |
| ACI-TR-160 | 70bf2b5e | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `failed` is rejected (no valid transition) |
| ACI-NF-040 | 70f267da | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:0 | Rule O-ATT-1: needs_formal (prose Formal) |
| ACI-TR-161 | 7129e690 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `requested` is rejected (no valid transition) |
| ACI-DOM-094 | 71836045 | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:1 | ConfirmedDispatch.source_bytes_artifact_id: [ArtifactId](#artifactid) |
| ACI-DOM-096 | 71bac184 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:2 | RuntimeEventEnvelope.aggregate_id: string (Owning stream.) |
| ACI-DOM-097 | 71e53cfa | domain-field | derivable-needs-harness | domain.md#Group:field:6 | Group.reveal_manifest_id: string |
| ACI-TR-162 | 7255bd9a | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-098 | 72b195d5 | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:4 | RevealManifest.manifest_hash: [ContentDigest](#contentdigest) |
| ACI-TR-163 | 732e910a | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:6 | Transition `deliberating` --[`round.closed`](events.md#roundclosed)--> `voting` succeeds when guarded |
| ACI-TR-164 | 7336e366 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:6 | Transition `running` --[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected)--> `execution_terminal` succeeds when guarded |
| ACI-TR-165 | 733c7c82 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `failed` is rejected (no valid transition) |
| ACI-TR-166 | 734efeb3 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `cancelled` is rejected (no valid transition) |
| ACI-NF-041 | 73ca7c5f | needs-formal | needs-formal | operations.md#CommitGroupResult:rule:3 | Rule O-COMMIT-4: needs_formal (prose Formal) |
| ACI-TR-167 | 7451dfc4 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `close_pending` is rejected (no valid transition) |
| ACI-TR-168 | 7453fde5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-099 | 74709eec | domain-field | derivable-needs-harness | domain.md#GroupResult:field:4 | GroupResult.participant_seat_ids: list<[SeatId](#seatid)> |
| ACI-DOM-100 | 7470d89a | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:1 | PublicationReceipt.status: string (Exactly `persisted_candidate`; never claims official acceptance.) |
| ACI-TR-169 | 74a3b693 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `confirmed` is rejected (no valid transition) |
| ACI-TR-170 | 7527031b | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `execution_terminal` is rejected (no valid transition) |
| ACI-DOM-101 | 753f979b | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:4 | RuntimeCommand.expected_version: [AggregateVersion](#aggregateversion) (Required CAS expectation.) |
| ACI-TR-171 | 75616a68 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `cancel_requested` is rejected (no valid transition) |
| ACI-NF-042 | 757543ff | needs-formal | needs-formal | operations.md#StartRun:rule:0 | Rule O-RUN-1: needs_formal (prose Formal) |
| ACI-TR-172 | 7575b0da | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `running` is rejected (no valid transition) |
| ACI-TR-173 | 759cc227 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `pending` is rejected (no valid transition) |
| ACI-NF-043 | 75ac252e | needs-formal | needs-formal | operations.md#RecordUsageObservation:rule:0 | Rule O-USAGE-1: needs_formal (prose Formal) |
| ACI-EVT-020 | 7634838e | event-obligation | derivable-needs-harness | events.md#attempt.unknown | Event attempt.unknown is emitted with valid payload |
| ACI-TR-174 | 76652357 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `execution_terminal` is rejected (no valid transition) |
| ACI-TR-175 | 7687fdac | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `requested` is rejected (no valid transition) |
| ACI-DOM-102 | 76ae136e | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:3 | ConfirmedDispatch.digest: [ContentDigest](#contentdigest) |
| ACI-TR-176 | 76d08606 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `committing` is rejected (no valid transition) |
| ACI-ERR-009 | 76f6745c | error-obligation | derivable-needs-harness | operations.md#ConfirmRuntimeDispatch:errorstate:2 | Error mapping for ConfirmRuntimeDispatch: "Existing identity has a different digest" -> Permanent identity conflict; no state change. |
| ACI-DOM-103 | 76fd1a35 | domain-field | derivable-needs-harness | domain.md#GroupResult:field:7 | GroupResult.committed_event_id: string |
| ACI-DOM-104 | 770725e2 | domain-field | derivable-needs-harness | domain.md#SandboxPolicy:field:1:1 | SandboxPolicy.network_scope: object (Explicit allow/deny rules; default deny outside declared scope.) |
| ACI-DOM-105 | 7791046a | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:5 | AgentInvocationPlan.deadline: timestamp (Frozen execution deadline.) |
| ACI-DOM-106 | 78fc3006 | domain-field | derivable-needs-harness | domain.md#Group:field:7 | Group.committed_result_id: string |
| ACI-TR-177 | 7a1125e0 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `completed` is rejected (no valid transition) |
| ACI-DOM-107 | 7a1a2f63 | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:1 | RuntimeCommand.idempotency_key: string (Unique in declared command scope.) |
| ACI-DOM-108 | 7a9c3e30 | domain-field | derivable-needs-harness | domain.md#SandboxPolicy:field:1:0 | SandboxPolicy.filesystem_scope: object (Explicit allow/deny rules; default deny outside declared scope.) |
| ACI-DOM-109 | 7ac43f4a | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:2 | EffectIntent.payload_digest: [ContentDigest](#contentdigest) |
| ACI-TR-178 | 7addb77a | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `failed` is rejected (no valid transition) |
| ACI-DOM-110 | 7b253e3d | domain-field | derivable-needs-harness | domain.md#Seat:field:2 | Seat.role_contract_ref: [VersionedReference](#versionedreference) |
| ACI-DOM-111 | 7b3e3d90 | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:3 | RuntimeCommand.aggregate_id: string (Existing target aggregate.) |
| ACI-TR-179 | 7b4a96b7 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `unknown` is rejected (no valid transition) |
| ACI-TR-180 | 7ba9d1c6 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state any nonterminal is rejected (no valid transition) |
| ACI-DOM-112 | 7c7b593b | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:8:1 | RuntimeEventEnvelope.payload_hash: [ArtifactId](#artifactid), [ContentDigest](#contentdigest) (Immutable payload evidence.) |
| ACI-DOM-113 | 7cc23474 | domain-field | derivable-needs-harness | domain.md#Seat:field:1 | Seat.group_aggregate_id: string |
| ACI-TR-181 | 7d1d3835 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-114 | 7d4d5d43 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:4 | EffectiveInputArtifact.entries: ordered list<[EffectiveInputEntry](#effectiveinputentry)> |
| ACI-INV-007 | 7d84ad1d | invariant | derivable-pure | states.md#RunLifecycle:invariant:0 | Invariant RUN-I1: present (existence) |
| ACI-TR-182 | 7d9984e4 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-ERR-022 | 7dbedd0b | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:5 | Error mapping for DeliverReferenceScoutBundleToAgent: "Manifest entry is missing, duplicated, at another ordinal or differs in artifact/digest/delivery/policy" -> Validation failure; reject. |
| ACI-NF-044 | 7e9d6661 | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:1 | Rule O-RECEIPT-2: needs_formal (prose Formal) |
| ACI-DOM-115 | 7efad2ad | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:3 | AgentTerminalResult.raw_output_ref: [ArtifactId](#artifactid) (Immutable provider-native evidence when observable.) |
| ACI-TR-183 | 7f151382 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-TR-184 | 7f2f3957 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `unknown` is rejected (no valid transition) |
| ACI-NF-094 | 7f6ac55e | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:8 | Rule O-ATT-9: needs_formal (prose Formal) |
| ACI-TR-185 | 7f7e21a5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `requested` is rejected (no valid transition) |
| ACI-MAP-005 | 7f80544e | mapping-row | derivable-needs-harness | mappings.md#FrozenAuthorityToAuditLedgerRow | Mapping FrozenAuthorityToAuditLedgerRow ([ConfirmedDispatch](domain.md#confirmeddispatch) plus the unique terminal [Run](domain.md#run) -> canonical audit-ledger schema `0.6.1` opening or close row) maps all fields correctly |
| ACI-RULE-010 | 81054d6f | rule-validation | derivable-pure | operations.md#CommitGroupResult:rule:0 | Rule O-COMMIT-1: first-allowed (count cap) |
| ACI-TR-186 | 81428df1 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-187 | 81531126 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `requested` is rejected (no valid transition) |
| ACI-ERR-010 | 8172141e | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:2 | Error mapping for PublishBusContribution: "Another active candidate owns the logical seat/round/type" -> `logical_contribution_conflict`; an abandoned historical candidate does not retain the active reservation. |
| ACI-DOM-116 | 81d0a6f7 | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:4 | PublicationReceipt.payload_hash: [ContentDigest](#contentdigest) (Equals persisted payload hash.) |
| ACI-TR-188 | 8227795f | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `confirmed` is rejected (no valid transition) |
| ACI-DOM-117 | 82a77edc | domain-field | derivable-needs-harness | domain.md#BusPublication:field:5 | BusPublication.payload` or `payload_ref: object or [ArtifactId](#artifactid) (Exactly one; schema-valid, bounded and hashed.) |
| ACI-DOM-118 | 82c6ada1 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:0:0 | AgentExecutionRequest.attempt_id: string (Runtime-authenticated identities.) |
| ACI-TR-189 | 83225cb7 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state any nonterminal is rejected (no valid transition) |
| ACI-DOM-119 | 8379a8dc | domain-field | derivable-needs-harness | domain.md#MaterializedAgentInvocation:field:0 | MaterializedAgentInvocation.plan_digest: [ContentDigest](#contentdigest) (Exact source plan.) |
| ACI-DOM-120 | 839030ef | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:4 | RawProviderOutput.model_ref: [VersionedReference](#versionedreference) |
| ACI-ERR-011 | 83a21701 | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:4 | Error mapping for PublishBusContribution: "Agent supplies/conflicts with authority fields" -> Reject; do not reinterpret the payload. |
| ACI-TR-190 | 83f1ed1e | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:7 | Transition `starting`, `running`, `waiting_tool`, or `cancel_requested` --[`attempt.completed`](events.md#attemptcompleted)--> `completed` succeeds when guarded |
| ACI-EVT-021 | 849d1e4d | event-obligation | derivable-needs-harness | events.md#Run events | Event Run events is emitted with valid payload |
| ACI-TR-191 | 84acf89d | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:9 | Transition `close_pending` --[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required)--> `reconciliation_required` succeeds when guarded |
| ACI-DOM-121 | 8541e638 | domain-field | derivable-needs-harness | domain.md#ConfirmedDispatch:field:4 | ConfirmedDispatch.authority_mode: [ExecutionAuthorityMode](#executionauthoritymode) |
| ACI-TR-192 | 85b5b34e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `requested` is rejected (no valid transition) |
| ACI-NF-045 | 85f7a629 | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:2 | Rule O-PUB-3: needs_formal (prose Formal) |
| ACI-DOM-122 | 86899fca | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:0:2 | AgentInvocationPlan.seat_id: string (Runtime-authenticated identities.) |
| ACI-TR-193 | 8689a392 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `requested` is rejected (no valid transition) |
| ACI-DOM-123 | 86b29e15 | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:4 | EffectIntent.claim_epoch: integer |
| ACI-EVT-022 | 86d73be1 | event-obligation | derivable-needs-harness | events.md#audit_opening.reconciliation_required | Event audit_opening.reconciliation_required is emitted with valid payload |
| ACI-TR-194 | 871ae06e | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:10 | Transition `cancel_requested` --[`attempt.cancelled`](events.md#attemptcancelled)--> `cancelled` succeeds when guarded |
| ACI-EVT-023 | 871eafc2 | event-obligation | derivable-needs-harness | events.md#collection.closed | Event collection.closed is emitted with valid payload |
| ACI-TR-195 | 877f88ee | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:0 | Transition none --[`run.created`](events.md#runcreated)--> `confirmed` succeeds when guarded |
| ACI-DOM-124 | 87db5e36 | domain-field | derivable-needs-harness | domain.md#Run:field:4 | Run.state_hash: [ContentDigest](#contentdigest) |
| ACI-TR-196 | 882fa414 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-197 | 888dfe56 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state any nonterminal is rejected (no valid transition) |
| ACI-DOM-250 | 88a15cc1 | domain-field | derivable-needs-harness | domain.md#Attempt:field:1 | Attempt.dispatch_id: string |
| ACI-TR-198 | 88da44e6 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:0 | Transition `pending` --[`group.started`](events.md#groupstarted)--> `collecting` succeeds when guarded |
| ACI-TR-199 | 894eec19 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-DOM-251 | 896ed1d6 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:12 | AgentReferenceDelivery.effective_input_manifest_hash: [ContentDigest](#contentdigest) |
| ACI-EVT-024 | 8a7bba88 | event-obligation | derivable-needs-harness | events.md#run.created | Event run.created is emitted with valid payload |
| ACI-TR-200 | 8a93501e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state none is rejected (no valid transition) |
| ACI-EVT-025 | 8b123d74 | event-obligation | derivable-needs-harness | events.md#attempt.requested | Event attempt.requested is emitted with valid payload |
| ACI-DOM-252 | 8b649808 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:1 | AgentReferenceDelivery.dispatch_id: string |
| ACI-TR-201 | 8bbd01c5 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `failed` is rejected (no valid transition) |
| ACI-NF-046 | 8bc5d749 | needs-formal | needs-formal | operations.md#VerifyAuditOpening:rule:2 | Rule O-OPEN-3: needs_formal (prose Formal) |
| ACI-TR-202 | 8c33fc4d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-203 | 8c65f695 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state none is rejected (no valid transition) |
| ACI-TR-204 | 8cf0febe | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `unknown` is rejected (no valid transition) |
| ACI-DOM-125 | 8cfac596 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:0:0 | RuntimeEventEnvelope.event_id: string (Immutable identity and past-tense type.) |
| ACI-NF-047 | 8d681ad8 | needs-formal | needs-formal | operations.md#ConfirmRuntimeDispatch:rule:4 | Rule O-CONF-5: needs_formal (prose Formal) |
| ACI-NF-048 | 8d903ad3 | needs-formal | needs-formal | operations.md#ComputeFixedProofVerdict:rule:1 | Rule O-VER-2: needs_formal (prose Formal) |
| ACI-NF-049 | 8dd364db | needs-formal | needs-formal | operations.md#VerifyPublicationReceipt:rule:0 | Rule O-RECEIPT-1: needs_formal (prose Formal) |
| ACI-DOM-126 | 8ded6354 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:7 | EffectiveInputArtifact.context_artifact_refs: ordered list<[ArtifactId](#artifactid)> |
| ACI-NF-095 | 8dfa79ae | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:4 | Rule O-ARD-5: needs_formal (prose Formal) |
| ACI-INV-008 | 8e1169a3 | invariant | derivable-pure | states.md#GroupLifecycle:invariant:3 | Invariant GRP-I4: first-allowed (count cap) |
| ACI-DOM-127 | 8e17854d | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:5 | AgentExecutionRequest.deadline: timestamp (Frozen execution deadline.) |
| ACI-TR-205 | 8e7a27f2 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-DOM-128 | 8e8ea1db | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:6 | AgentExecutionRequest.resource_budget: [ResourceBudget](#resourcebudget) (Typed finite limits.) |
| ACI-DOM-129 | 8e98e4fd | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:2:1 | AgentExecutionRequest.materialization_digest: [ContentDigest](#contentdigest) (Bind the accepted plan and materialization.) |
| ACI-TR-206 | 8ee165b3 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `ready` is rejected (no valid transition) |
| ACI-TR-207 | 8f2c426d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `completed` is rejected (no valid transition) |
| ACI-DOM-253 | 8f355396 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:6 | AgentReferenceDelivery.recommendation_ids: ordered list<string> |
| ACI-TR-208 | 8f602172 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-209 | 8f86796c | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:1 | Transition `collecting` --[`position.accepted`](events.md#positionaccepted)--> `collecting` succeeds when guarded |
| ACI-TR-210 | 9030f0e7 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:3 | Transition `revealing` --[`reveal.published`](events.md#revealpublished)--> `voting` succeeds when guarded |
| ACI-TR-211 | 9075beaa | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `revealing` is rejected (no valid transition) |
| ACI-DOM-130 | 908c0e8d | domain-field | derivable-needs-harness | domain.md#ManifestEntry:field:0 | ManifestEntry.message_id: string (Accepted contribution.) |
| ACI-TR-212 | 90b3c35f | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `completed` is rejected (no valid transition) |
| ACI-ENUM-003 | 90b6d195 | domain-enum | derivable-needs-harness | domain.md#ArtifactClassification:enum | ArtifactClassification vocabulary is exactly {runtime-internal,sensitive-input,sensitive-output,reveal-authorized,public} |
| ACI-TR-213 | 90c9b708 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state any nonterminal is rejected (no valid transition) |
| ACI-TR-214 | 9157d5b5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `waiting_tool` is rejected (no valid transition) |
| ACI-TR-215 | 91770f87 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `completed` is rejected (no valid transition) |
| ACI-DOM-131 | 91ba8444 | domain-field | derivable-needs-harness | domain.md#Seat:field:3 | Seat.agent_instance_id: string |
| ACI-TR-216 | 920b609b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-DOM-132 | 9210b4fb | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:8 | AgentExecutionRequest.authority_fence: [ExecutionAuthorityFence](#executionauthorityfence) (Must remain current at effect claim/start.) |
| ACI-TR-217 | 9261c6da | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `waiting_tool` is rejected (no valid transition) |
| ACI-TR-218 | 932285fa | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `unknown` is rejected (no valid transition) |
| ACI-NF-096 | 9333a921 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:3 | Rule O-ARD-4: needs_formal (prose Formal) |
| ACI-DOM-133 | 933b0b1c | domain-field | derivable-needs-harness | domain.md#ManifestEntry:field:1 | ManifestEntry.payload_hash: [ContentDigest](#contentdigest) (Matches accepted event.) |
| ACI-DOM-134 | 93dafc9f | domain-field | derivable-needs-harness | domain.md#Contribution:field:9 | Contribution.reply_to_message_ids: list<string> |
| ACI-NF-050 | 93f557ec | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:0 | Invariant GRP-I1: needs_formal (prose Formal) |
| ACI-NF-051 | 940402d4 | needs-formal | needs-formal | operations.md#ElectRunTerminal:rule:1 | Rule O-TERM-2: needs_formal (prose Formal) |
| ACI-TR-219 | 943aa67f | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `unknown` is rejected (no valid transition) |
| ACI-TR-220 | 943bddf9 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `collecting` is rejected (no valid transition) |
| ACI-TR-221 | 9457c748 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `revealing` is rejected (no valid transition) |
| ACI-TR-222 | 94a173b0 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `revealing` is rejected (no valid transition) |
| ACI-TR-223 | 94ba7e02 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-EVT-026 | 94c18146 | event-obligation | derivable-needs-harness | events.md#audit_opening.requested | Event audit_opening.requested is emitted with valid payload |
| ACI-TR-224 | 950ee964 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:8 | Transition `close_pending` --[`audit_close.verified`](events.md#audit_closeverified)--> `closed` succeeds when guarded |
| ACI-TR-225 | 955d1a1c | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `unknown` is rejected (no valid transition) |
| ACI-TR-226 | 96169d2e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `starting` is rejected (no valid transition) |
| ACI-DOM-135 | 963a261a | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:1:2 | AgentExecutionRequest.model_ref: [VersionedReference](#versionedreference) (Confirmed selection; no provider-specific kernel branch.) |
| ACI-EVT-052 | 9669531a | event-obligation | derivable-needs-harness | events.md#reference_scout.bundle_delivered_to_agent@1 | Event reference_scout.bundle_delivered_to_agent@1 is emitted with valid payload |
| ACI-EVT-027 | 96c12cf3 | event-obligation | derivable-needs-harness | events.md#attempt.completed | Event attempt.completed is emitted with valid payload |
| ACI-MAP-008 | 96cd87c3 | mapping-row | derivable-needs-harness | mappings.md#ReferenceScoutBundleToEffectiveInput | Mapping ReferenceScoutBundleToEffectiveInput (accepted -> [AgentReferenceDelivery](domain.md#agentreferencedelivery), one typed) maps all fields correctly |
| ACI-TR-227 | 96faf49e | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state none is rejected (no valid transition) |
| ACI-NF-052 | 9731a09d | needs-formal | needs-formal | operations.md#CloseCollection:rule:0 | Rule O-CLOSE-1: needs_formal (prose Formal) |
| ACI-TR-228 | 976eebcc | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`opening_pending`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `opening_pending` is rejected (no valid transition) |
| ACI-DOM-136 | 9777d16c | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:3 | RawProviderOutput.provider_ref: [VersionedReference](#versionedreference) |
| ACI-DOM-137 | 97c686a6 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:5 | DispatchSpec.capability_resolution: object (Adapter/model/tool decisions and digests fixed.) |
| ACI-TR-229 | 981ceaf2 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `completed` is rejected (no valid transition) |
| ACI-NF-053 | 99621185 | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:5 | Invariant ATT-I6: needs_formal (prose Formal) |
| ACI-EVT-028 | 99b326f9 | event-obligation | derivable-needs-harness | events.md#publication.candidate_abandoned | Event publication.candidate_abandoned is emitted with valid payload |
| ACI-DOM-138 | 99f42129 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:8 | PublicationCandidate.status: string |
| ACI-DOM-139 | 9a176631 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:0:1 | AgentExecutionRequest.operation_id: string (Runtime-authenticated identities.) |
| ACI-TR-230 | 9a25a915 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `committing` is rejected (no valid transition) |
| ACI-TR-231 | 9a48c1f2 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `confirmed` is rejected (no valid transition) |
| ACI-TR-232 | 9a78cf80 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state `execution_terminal` is rejected (no valid transition) |
| ACI-TR-233 | 9b1147b9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-141 | 9b6be8a3 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:1 | EffectiveInputEntry.artifact_ref: [ArtifactId](#artifactid) (Exact delivered bytes.) |
| ACI-NF-054 | 9cdfd11c | needs-formal | needs-formal | operations.md#StartRun:rule:1 | Rule O-RUN-2: needs_formal (prose Formal) |
| ACI-EVT-029 | 9dfb25f1 | event-obligation | derivable-needs-harness | events.md#Common runtime event envelope | Event Common runtime event envelope is emitted with valid payload |
| ACI-DOM-142 | 9e53a357 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:1 | PublicationCandidate.publication_event_id: string |
| ACI-TR-234 | 9f08cc34 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `failed` is rejected (no valid transition) |
| ACI-TR-235 | 9f5b0b31 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `execution_terminal` is rejected (no valid transition) |
| ACI-DOM-143 | 9f721012 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:5 | EffectiveInputArtifact.tool_contract_refs: ordered list<[VersionedReference](#versionedreference)> |
| ACI-DOM-144 | 9f9d9a52 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:4 | DispatchSpec.prompt_snapshot_refs: ordered list<[ArtifactId](#artifactid)> (Content-addressed.) |
| ACI-DOM-145 | 9ff527ca | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:3:1 | AgentInvocationPlan.role_delta_ref: [ArtifactId](#artifactid) (Shared base and optional declared delta.) |
| ACI-TR-236 | 9ffbfbaa | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `cancelled` is rejected (no valid transition) |
| ACI-NF-055 | a028f649 | needs-formal | needs-formal | operations.md#CommitGroupResult:rule:1 | Rule O-COMMIT-2: needs_formal (prose Formal) |
| ACI-TR-237 | a03ccd68 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `starting` is rejected (no valid transition) |
| ACI-TR-238 | a16132d9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state none is rejected (no valid transition) |
| ACI-INV-009 | a1adc156 | invariant | derivable-pure | states.md#RunLifecycle:invariant:2 | Invariant RUN-I3: duplicate-capped (count cap) |
| ACI-TR-239 | a1d09ed5 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `waiting_tool` is rejected (no valid transition) |
| ACI-DOM-146 | a2271703 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:2:0 | AgentExecutionRequest.plan_digest: [ContentDigest](#contentdigest) (Bind the accepted plan and materialization.) |
| ACI-TR-240 | a243a00a | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `cancelling` is rejected (no valid transition) |
| ACI-TR-241 | a25b3675 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `failed` is rejected (no valid transition) |
| ACI-ERR-012 | a27cc4cf | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:0 | Error mapping for VerifyPublicationReceipt: "Receipt is missing from the terminal result" -> `publication_receipt_missing`; reject official result and do not count it toward quorum. |
| ACI-NF-056 | a3a11a91 | needs-formal | needs-formal | operations.md#VerifyAuditClose:rule:1 | Rule O-ACLOSE-2: needs_formal (prose Formal) |
| ACI-EVT-030 | a3fb9cda | event-obligation | derivable-needs-harness | events.md#attempt.cancelled | Event attempt.cancelled is emitted with valid payload |
| ACI-DOM-147 | a46870a0 | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:0 | EffectIntent.effect_id: string |
| ACI-DOM-148 | a51ebeb5 | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:1:0 | AgentInvocationPlan.provider_ref: [VersionedReference](#versionedreference) (Frozen selection.) |
| ACI-ERR-013 | a5badb7c | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:4 | Error mapping for VerifyPublicationReceipt: "Another attempt already satisfied the logical operation" -> `operation_result_already_accepted`; preserve this result as superseded/ignored. |
| ACI-TR-242 | a616f47b | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `failed` is rejected (no valid transition) |
| ACI-DOM-149 | a646e019 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:0:1 | RuntimeEventEnvelope.event_type: string (Immutable identity and past-tense type.) |
| ACI-TR-243 | a6744ace | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `voting` is rejected (no valid transition) |
| ACI-NF-057 | a6a02bc0 | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:4 | Rule O-PUB-5: needs_formal (prose Formal) |
| ACI-DOM-150 | a6dabf45 | domain-field | derivable-needs-harness | domain.md#Contribution:field:1 | Contribution.group_aggregate_id: string |
| ACI-TR-244 | a7380a78 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `closed` is rejected (no valid transition) |
| ACI-DOM-254 | a7f51864 | domain-field | derivable-needs-harness | domain.md#Attempt:field:6 | Attempt.adapter_ref: [VersionedReference](#versionedreference) |
| ACI-INV-010 | a8433c36 | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:3 | Invariant ATT-I4: first-allowed (count cap) |
| ACI-TR-245 | a8f3f0e6 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:7 | Transition `execution_terminal` --[`audit_close.requested`](events.md#audit_closerequested)--> `close_pending` succeeds when guarded |
| ACI-TR-246 | a9268d39 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state none is rejected (no valid transition) |
| ACI-TR-247 | a9678daf | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-151 | a9a9f359 | domain-field | derivable-needs-harness | domain.md#Run:field:3 | Run.aggregate_version: [AggregateVersion](#aggregateversion) |
| ACI-NF-058 | a9d5c61c | needs-formal | needs-formal | operations.md#ComputeFixedProofVerdict:rule:0 | Rule O-VER-1: needs_formal (prose Formal) |
| ACI-DOM-152 | aa01a95e | domain-field | derivable-needs-harness | domain.md#Artifact:field:7 | Artifact.tombstoned_at: timestamp |
| ACI-NF-059 | aa8813a8 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:2 | Rule O-ATT-3: needs_formal (prose Formal) |
| ACI-TR-248 | aab0692a | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`requested`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `requested` is rejected (no valid transition) |
| ACI-DOM-153 | aabac99d | domain-field | derivable-needs-harness | domain.md#Group:field:0 | Group.run_id: string |
| ACI-TR-249 | aabc3af2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-250 | aad6b109 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`waiting_tool`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `waiting_tool` is rejected (no valid transition) |
| ACI-EVT-031 | ab540f77 | event-obligation | derivable-needs-harness | events.md#group.failed | Event group.failed is emitted with valid payload |
| ACI-TR-251 | ab85fe30 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-154 | ab9116ec | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:7 | PublicationCandidate.journal_offset: [JournalOffset](#journaloffset) |
| ACI-DOM-155 | abc8f2ef | domain-field | derivable-needs-harness | domain.md#Group:field:1 | Group.group_id: string |
| ACI-TR-252 | ac185002 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.waiting_tool`](events.md#attemptwaiting_tool) | Event [`attempt.waiting_tool`](events.md#attemptwaiting_tool) in state `completed` is rejected (no valid transition) |
| ACI-DOM-156 | ac470bea | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:10 | PublicationCandidate.abandoned_event_id: string |
| ACI-TR-253 | ac599b34 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.cancel_requested`](events.md#attemptcancel_requested) | Event [`attempt.cancel_requested`](events.md#attemptcancel_requested) in state `starting` is rejected (no valid transition) |
| ACI-TR-254 | ac7ff329 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state none is rejected (no valid transition) |
| ACI-TR-255 | ad3a60b2 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:7 | Transition `voting` --[`vote.accepted`](events.md#voteaccepted)--> `voting` succeeds when guarded |
| ACI-EVT-032 | ad470a0b | event-obligation | derivable-needs-harness | events.md#group.committed | Event group.committed is emitted with valid payload |
| ACI-DOM-255 | ad47d91d | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:0 | EffectiveInputEntry.entry_type: string (`instruction`, `history`, `context`, `reveal_message`, `reference_bundle`, `tool_contract`, `response_schema`, or `adapter_wrapper`.) |
| ACI-DOM-157 | ad50b0e7 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:1:0 | AgentExecutionRequest.provider_ref: [VersionedReference](#versionedreference) (Confirmed selection; no provider-specific kernel branch.) |
| ACI-NF-060 | ad5c07c6 | needs-formal | needs-formal | operations.md#VerifyAuditOpening:rule:0 | Rule O-OPEN-1: needs_formal (prose Formal) |
| ACI-EVT-033 | ad621464 | event-obligation | derivable-needs-harness | events.md#attempt.result_accepted | Event attempt.result_accepted is emitted with valid payload |
| ACI-TR-256 | adaa8b44 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:none:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state none is rejected (no valid transition) |
| ACI-TR-257 | adb30c22 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `pending` is rejected (no valid transition) |
| ACI-DOM-158 | aea1fe96 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:3 | DispatchSpec.decision_policies: object (Versioned and frozen.) |
| ACI-TR-258 | aecdcf45 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `starting` is rejected (no valid transition) |
| ACI-DOM-159 | aed44127 | domain-field | derivable-needs-harness | domain.md#MaterializedAgentInvocation:field:2 | MaterializedAgentInvocation.provider_invocation_ref: [ArtifactId](#artifactid) (Content-addressed native request/flags.) |
| ACI-DOM-160 | af54bc60 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:2:2 | PublicationCandidate.operation_id: string |
| ACI-TR-259 | afb37168 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`completed`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `completed` is rejected (no valid transition) |
| ACI-TR-260 | b0a52d6b | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `revealing` is rejected (no valid transition) |
| ACI-NF-061 | b0bb7557 | needs-formal | needs-formal | operations.md#ComputeFixedProofVerdict:rule:2 | Rule O-VER-3: needs_formal (prose Formal) |
| ACI-TR-261 | b1822651 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `running` is rejected (no valid transition) |
| ACI-TR-262 | b1c1e8d3 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `cancelling` is rejected (no valid transition) |
| ACI-DOM-161 | b23c35ef | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:7 | AgentInvocationPlan.sandbox_policy: [SandboxPolicy](#sandboxpolicy) (Required launch isolation contract.) |
| ACI-DOM-162 | b2534246 | domain-field | derivable-needs-harness | domain.md#Contribution:field:6 | Contribution.payload_artifact_id: [ArtifactId](#artifactid) |
| ACI-NF-062 | b29bdd1f | needs-formal | needs-formal | states.md#RunLifecycle:invariant:3 | Invariant RUN-I4: needs_formal (prose Formal) |
| ACI-NF-063 | b2a67fa9 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:5 | Rule O-ATT-6: needs_formal (prose Formal) |
| ACI-TR-263 | b31740ae | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `running` is rejected (no valid transition) |
| ACI-DOM-163 | b3475e3b | domain-field | derivable-needs-harness | domain.md#Contribution:field:3 | Contribution.operation_id: string |
| ACI-DOM-164 | b376cbb1 | domain-field | derivable-needs-harness | domain.md#Seat:field:0 | Seat.seat_id: [SeatId](#seatid) |
| ACI-NF-064 | b5210e70 | needs-formal | needs-formal | operations.md#RecordUsageObservation:rule:3 | Rule O-USAGE-4: needs_formal (prose Formal) |
| ACI-TR-264 | b5681350 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-265 | b575d19b | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-266 | b65e0be9 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `closed` is rejected (no valid transition) |
| ACI-DOM-165 | b686fcbf | domain-field | derivable-needs-harness | domain.md#VersionedReference:field:1 | VersionedReference.version: string (Explicit immutable version.) |
| ACI-TR-267 | b75d553d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state any nonterminal is rejected (no valid transition) |
| ACI-NF-065 | b7914642 | needs-formal | needs-formal | operations.md#PublishConnectionHandoff:rule:1 | Rule O-HAND-2: needs_formal (prose Formal) |
| ACI-NF-066 | b7fa622f | needs-formal | needs-formal | states.md#AttemptLifecycle:invariant:9 | Invariant ATT-I10: needs_formal (prose Formal) |
| ACI-NF-067 | b81da157 | needs-formal | needs-formal | operations.md#StartGroup:rule:0 | Rule O-GROUP-1: needs_formal (prose Formal) |
| ACI-DOM-256 | b837ac90 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:7 | EffectiveInputEntry.visibility_policy_ref: [VersionedReference](#versionedreference) (Policy authorizing delivery.) |
| ACI-EVT-034 | b83cabb7 | event-obligation | derivable-needs-harness | events.md#Deferred event families | Event Deferred event families is emitted with valid payload |
| ACI-ERR-014 | b8639efe | error-obligation | derivable-needs-harness | operations.md#VerifyPublicationReceipt:errorstate:3 | Error mapping for VerifyPublicationReceipt: "Persisted event belongs to another attempt, operation, seat, group or run" -> `publication_receipt_scope_mismatch`; reject as cross-scope spoofing. |
| ACI-TR-268 | b8f9c1a3 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `confirmed` is rejected (no valid transition) |
| ACI-TR-269 | b8fc2990 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-270 | b94f8f53 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-TR-271 | b987402c | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:0 | Transition none --[`attempt.requested`](events.md#attemptrequested)--> `requested` succeeds when guarded |
| ACI-DOM-166 | b9ce32b5 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:4 | RuntimeEventEnvelope.journal_offset: [JournalOffset](#journaloffset) (Globally increasing committed order.) |
| ACI-DOM-167 | ba0889d4 | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:1 | ExecutionAuthorityFence.authority_mode: [ExecutionAuthorityMode](#executionauthoritymode) (Must equal `runtime-managed`.) |
| ACI-NF-097 | ba3f5c9b | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:5 | Rule O-ARD-6: needs_formal (prose Formal) |
| ACI-DOM-168 | ba9b2dce | domain-field | derivable-needs-harness | domain.md#Contribution:field:7 | Contribution.accepted_event_id: string |
| ACI-DOM-169 | bac06965 | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:5 | RuntimeCommand.prerequisite_heads: ordered list<object> (Exact `(aggregate_id, expected_version, state_hash)` heads required atomically with target CAS.) |
| ACI-NF-068 | bae59535 | needs-formal | needs-formal | states.md#RunLifecycle:invariant:4 | Invariant RUN-I5: needs_formal (prose Formal) |
| ACI-TR-272 | baed2ce3 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `cancelling` is rejected (no valid transition) |
| ACI-NF-069 | bb13a995 | needs-formal | needs-formal | operations.md#PublishRevealManifest:rule:2 | Rule O-REV-3: needs_formal (prose Formal) |
| ACI-DOM-170 | bc035563 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:1 | DispatchSpec.schema_refs: ordered list<[VersionedReference](#versionedreference)> (Every executable input/output schema included.) |
| ACI-NF-070 | bc10cb7c | needs-formal | needs-formal | operations.md#PublishConnectionHandoff:rule:2 | Rule O-HAND-3: needs_formal (prose Formal) |
| ACI-DOM-171 | bcb8b37e | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:6:1 | RuntimeCommand.correlation_id: string (Stable provenance.) |
| ACI-TR-273 | bce7b308 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `pending` is rejected (no valid transition) |
| ACI-EVT-035 | bd40c45b | event-obligation | derivable-needs-harness | events.md#reveal.published | Event reveal.published is emitted with valid payload |
| ACI-TR-274 | bd746071 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `voting` is rejected (no valid transition) |
| ACI-TR-275 | bd7ca95b | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:3 | Transition `opening_pending` --[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required)--> `reconciliation_required` succeeds when guarded |
| ACI-TR-276 | bd997039 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`close_pending`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `close_pending` is rejected (no valid transition) |
| ACI-EVT-036 | bdd944bb | event-obligation | derivable-needs-harness | events.md#audit_opening.verified | Event audit_opening.verified is emitted with valid payload |
| ACI-DOM-257 | bdded285 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:3 | AgentReferenceDelivery.source_bundle_delivered_event_id: string |
| ACI-TR-277 | bde7d3e9 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-DOM-172 | be293b0c | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:0 | EffectiveInputArtifact.artifact_id: [ArtifactId](#artifactid) |
| ACI-DOM-173 | be4bceb2 | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:6 | RevealManifest.reveal_event_id: string |
| ACI-EVT-037 | be76d5eb | event-obligation | derivable-needs-harness | events.md#audit_close.reconciliation_required | Event audit_close.reconciliation_required is emitted with valid payload |
| ACI-EVT-038 | be86eb43 | event-obligation | derivable-needs-harness | events.md#attempt.failed | Event attempt.failed is emitted with valid payload |
| ACI-TR-278 | bea49f66 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `confirmed` is rejected (no valid transition) |
| ACI-DOM-174 | becca793 | domain-field | derivable-needs-harness | domain.md#SandboxPolicy:field:0 | SandboxPolicy.policy_ref: [VersionedReference](#versionedreference) (Frozen launcher policy.) |
| ACI-DOM-175 | c0244458 | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:1 | EffectIntent.effect_type: string |
| ACI-ERR-023 | c0d0b2fc | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:2 | Error mapping for DeliverReferenceScoutBundleToAgent: "Bundle digest or ordered recommendation membership does not match immutable bytes" -> Integrity failure; reject. |
| ACI-DOM-176 | c16fdf27 | domain-field | derivable-needs-harness | domain.md#PublicationReceipt:field:2 | PublicationReceipt.event_id: string (Existing committed `publication.persisted` event.) |
| ACI-TR-279 | c1a9694a | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`, `running`, `waiting_tool`, or `cancel_requested`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `starting`, `running`, `waiting_tool`, or `cancel_requested` is rejected (no valid transition) |
| ACI-TR-280 | c2400242 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state `running` is rejected (no valid transition) |
| ACI-EVT-039 | c2ea0399 | event-obligation | derivable-needs-harness | events.md#Receipt and reveal guarantees | Event Receipt and reveal guarantees is emitted with valid payload |
| ACI-NF-071 | c36d32fc | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:5 | Rule O-PUB-6: needs_formal (prose Formal) |
| ACI-RULE-011 | c39462a2 | rule-validation | derivable-pure | operations.md#RecordUsageObservation:rule:2 | Rule O-USAGE-3: conjunct 1 missing |
| ACI-RULE-012 | c3ab4217 | rule-validation | derivable-pure | operations.md#RecordUsageObservation:rule:2 | Rule O-USAGE-3: conjunct 0 missing |
| ACI-TR-281 | c417eafd | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-282 | c57aadf5 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `confirmed` is rejected (no valid transition) |
| ACI-TR-283 | c5e5f062 | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:6 | Transition `cancel_requested` --[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged)--> `cancel_requested` succeeds when guarded |
| ACI-DOM-177 | c63d2ae0 | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:9 | EffectiveInputArtifact.manifest_hash: [ContentDigest](#contentdigest) |
| ACI-TR-284 | c662ccc4 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`committing`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `committing` is rejected (no valid transition) |
| ACI-TR-285 | c6766d17 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `completed` is rejected (no valid transition) |
| ACI-TR-286 | c6b30307 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `completed` is rejected (no valid transition) |
| ACI-TR-287 | c7df1078 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-DOM-258 | c81064af | domain-field | derivable-needs-harness | domain.md#Attempt:field:10 | Attempt.worker_epoch: integer |
| ACI-NF-072 | c862cb58 | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:0 | Rule O-PUB-1: needs_formal (prose Formal) |
| ACI-DOM-178 | c86b10d9 | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:3 | RevealManifest.message_entries: ordered list<[ManifestEntry](#manifestentry)> |
| ACI-DOM-179 | c8b4265a | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:3:0 | AgentExecutionRequest.effective_input_ref: [ArtifactId](#artifactid) (Exact finalized observable/native inputs.) |
| ACI-EVT-040 | c8ec2ed1 | event-obligation | derivable-needs-harness | events.md#handoff.published | Event handoff.published is emitted with valid payload |
| ACI-DOM-180 | c93018e8 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:6 | RuntimeEventEnvelope.observed_at: timestamp (Nullable external observation; never orders transitions.) |
| ACI-IF-004 | c9a6232b | contract | derivable-needs-harness | interfaces.md#POST /dispatches/{dispatch_id}/confirm:response:0 | POST /dispatches/{dispatch_id}/confirm -> 202 (command transaction committed) |
| ACI-DOM-181 | ca637bb9 | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:2 | ResourceBudget.budget_policy_ref: [VersionedReference](#versionedreference) (Frozen enforcement semantics.) |
| ACI-DOM-182 | cab59adf | domain-field | derivable-needs-harness | domain.md#Contribution:field:5 | Contribution.message_type: string |
| ACI-DOM-183 | caea72a8 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:0:2 | SoleWriterEvidenceBundle.host_profile_ref: [VersionedReference](#versionedreference) (Exact store, validated writer and host enforcement profile.) |
| ACI-DOM-184 | caeffd2e | domain-field | derivable-needs-harness | domain.md#Contribution:field:8 | Contribution.publication_event_id: string |
| ACI-NF-073 | cb8cc4c8 | needs-formal | needs-formal | operations.md#CloseCollection:rule:3 | Rule O-CLOSE-4: needs_formal (prose Formal) |
| ACI-TR-288 | cb96727f | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `collecting` is rejected (no valid transition) |
| ACI-TR-289 | cbf63a83 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `failed` is rejected (no valid transition) |
| ACI-TR-290 | cc1734bd | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:any applicable nonterminal:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state any applicable nonterminal is rejected (no valid transition) |
| ACI-TR-291 | ce1c1eb1 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:`reconciliation.retry_requested` | Event `reconciliation.retry_requested` in state none is rejected (no valid transition) |
| ACI-ERR-015 | ce39cc33 | error-obligation | derivable-needs-harness | operations.md#PublishBusContribution:errorstate:0 | Error mapping for PublishBusContribution: "Retry with same key and same digest" -> Return the byte-identical stored `PublicationReceipt`; append nothing. The transport envelope may report `transport_replayed=true`. |
| ACI-DOM-185 | ce9507f0 | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:0 | RawProviderOutput.artifact_id: [ArtifactId](#artifactid) |
| ACI-DOM-186 | cf15da8e | domain-field | derivable-needs-harness | domain.md#Run:field:0 | Run.run_id: string |
| ACI-INV-011 | cf16e53d | invariant | derivable-pure | states.md#RunLifecycle:invariant:2 | Invariant RUN-I3: first-allowed (count cap) |
| ACI-DOM-187 | cf5a9ab7 | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:1:2 | ResourceBudget.max_artifact_bytes: integer (Non-negative finite limits.) |
| ACI-DOM-188 | d1192658 | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:2 | RuntimeCommand.command_digest: [ContentDigest](#contentdigest) (Canonical semantic request digest.) |
| ACI-TR-292 | d157750e | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:8 | Transition `voting` --[`verdict.computed`](events.md#verdictcomputed)--> `committing` succeeds when guarded |
| ACI-DOM-259 | d1b74c9a | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:10 | AgentReferenceDelivery.effective_input_artifact_id: [ArtifactId](#artifactid) |
| ACI-DOM-189 | d2049b0d | domain-field | derivable-needs-harness | domain.md#EffectiveInputArtifact:field:2 | EffectiveInputArtifact.base_snapshot_ref: [ArtifactId](#artifactid) |
| ACI-EVT-041 | d286f301 | event-obligation | derivable-needs-harness | events.md#Usage and effect events | Event Usage and effect events is emitted with valid payload |
| ACI-DOM-190 | d2890d41 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:1 | SoleWriterEvidenceBundle.writer_process_identity_ref: [ArtifactId](#artifactid) (Evidence of the only process identity allowed to write.) |
| ACI-DOM-191 | d2b8dd69 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:7:1 | RuntimeEventEnvelope.correlation_id: string (Provenance.) |
| ACI-DOM-192 | d387707e | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:0:0 | ExecutionAuthorityFence.dispatch_id: string (Exact runtime-owned execution.) |
| ACI-TR-293 | d3df9858 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`execution_terminal`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `execution_terminal` is rejected (no valid transition) |
| ACI-DOM-193 | d4ba2540 | domain-field | derivable-needs-harness | domain.md#EffectiveInputEntry:field:3 | EffectiveInputEntry.author_principal_id: string (Required for authored/revealed messages; otherwise nullable.) |
| ACI-DOM-194 | d5138a35 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:9 | PublicationCandidate.official_accepted_event_id: string |
| ACI-NF-074 | d51fa27a | needs-formal | needs-formal | operations.md#RecordAttemptObservation:rule:2 | Rule O-OBS-3: needs_formal (prose Formal) |
| ACI-TR-294 | d58bcd97 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`group.failed`](events.md#groupfailed) | Event [`group.failed`](events.md#groupfailed) in state `revealing` is rejected (no valid transition) |
| ACI-DOM-195 | d5e420eb | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:2 | RawProviderOutput.exchange_id: string |
| ACI-DOM-196 | d604c92d | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:5 | PublicationCandidate.payload_hash: [ContentDigest](#contentdigest) |
| ACI-NF-075 | d61dc8a9 | needs-formal | needs-formal | states.md#RunLifecycle:invariant:1 | Invariant RUN-I2: needs_formal (prose Formal) |
| ACI-TR-295 | d67d676b | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`collecting`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `collecting` is rejected (no valid transition) |
| ACI-TR-296 | d6d5ef05 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-297 | d77a6086 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-DOM-197 | d7844a59 | domain-field | derivable-needs-harness | domain.md#GroupResult:field:2 | GroupResult.verdict: string |
| ACI-TR-298 | d86a81dc | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `cancelling` is rejected (no valid transition) |
| ACI-NF-098 | d884c957 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:0 | Rule O-ARD-1: needs_formal (prose Formal) |
| ACI-DOM-198 | d892d897 | domain-field | derivable-needs-harness | domain.md#RuntimeEventEnvelope:field:8:0 | RuntimeEventEnvelope.payload_ref: [ArtifactId](#artifactid), [ContentDigest](#contentdigest) (Immutable payload evidence.) |
| ACI-TR-299 | d8d8276c | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`group.committed`](events.md#groupcommitted) | Event [`group.committed`](events.md#groupcommitted) in state `voting` is rejected (no valid transition) |
| ACI-RULE-014 | d9196601 | rule-validation | derivable-pure | operations.md#CommitGroupResult:rule:2 | Rule O-COMMIT-3: conjunct 0 missing |
| ACI-DOM-199 | d91f1d2e | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:0 | RuntimeCommand.command_id: string (Globally unique.) |
| ACI-ENUM-004 | d962b023 | domain-enum | derivable-needs-harness | domain.md#EffectStatus:enum | EffectStatus vocabulary is exactly {pending,claimed,succeeded,failed,unknown} |
| ACI-DOM-200 | d97cbc20 | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:1:0 | ResourceBudget.max_tool_calls: integer (Non-negative finite limits.) |
| ACI-TR-300 | d9894db2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `pending` is rejected (no valid transition) |
| ACI-DOM-201 | da17aecb | domain-field | derivable-needs-harness | domain.md#RuntimeCommand:field:6:0 | RuntimeCommand.causation_id: string (Stable provenance.) |
| ACI-TR-301 | da3142a0 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `confirmed` is rejected (no valid transition) |
| ACI-DOM-202 | dab32097 | domain-field | derivable-needs-harness | domain.md#DispatchSpec:field:6 | DispatchSpec.budgets: object (Explicit finite limits.) |
| ACI-EVT-042 | db51c9fd | event-obligation | derivable-needs-harness | events.md#group.started | Event group.started is emitted with valid payload |
| ACI-TR-302 | db58a4a2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `voting` is rejected (no valid transition) |
| ACI-TR-303 | db5f76a0 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-NF-076 | db92c383 | needs-formal | needs-formal | operations.md#ComputeFixedProofVerdict:rule:4 | Rule O-VER-5: needs_formal (prose Formal) |
| ACI-NF-077 | dc891226 | needs-formal | needs-formal | operations.md#StartAgentAttempt:rule:7 | Rule O-ATT-8: needs_formal (prose Formal) |
| ACI-TR-304 | dcbca3e2 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `ready` is rejected (no valid transition) |
| ACI-EVT-043 | dcc44d52 | event-obligation | derivable-needs-harness | events.md#Group and bus events | Event Group and bus events is emitted with valid payload |
| ACI-EVT-044 | dcc93926 | event-obligation | derivable-needs-harness | events.md#attempt.starting | Event attempt.starting is emitted with valid payload |
| ACI-TR-305 | dd7cd52d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state any nonterminal is rejected (no valid transition) |
| ACI-NF-078 | dfe2cb87 | needs-formal | needs-formal | operations.md#PublishBusContribution:rule:1 | Rule O-PUB-2: needs_formal (prose Formal) |
| ACI-INV-012 | e09aa30e | invariant | derivable-pure | states.md#AttemptLifecycle:invariant:1 | Invariant ATT-I2: absent (existence) |
| ACI-ERR-024 | e0d414ed | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:0 | Error mapping for DeliverReferenceScoutBundleToAgent: "Source commit or lifecycle-delivery event is missing or not accepted" -> Reject; accept no attempt or target-delivery fact. |
| ACI-TR-306 | e0d61ffd | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `closed` is rejected (no valid transition) |
| ACI-NF-079 | e112065c | needs-formal | needs-formal | operations.md#PublishRevealManifest:rule:3 | Rule O-REV-4: needs_formal (prose Formal) |
| ACI-DOM-203 | e1262187 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:4 | PublicationCandidate.payload_artifact_id: [ArtifactId](#artifactid) |
| ACI-TR-307 | e147a394 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-204 | e189f44d | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:0:0 | ResourceBudget.max_wall_time_ms: integer (Non-negative finite limits.) |
| ACI-DOM-260 | e1b89b99 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:15 | AgentReferenceDelivery.accepted_event_id: string |
| ACI-TR-308 | e1c392b8 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state any nonterminal is rejected (no valid transition) |
| ACI-TR-309 | e24431d4 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.cancelled`](events.md#attemptcancelled) | Event [`attempt.cancelled`](events.md#attemptcancelled) in state `running` is rejected (no valid transition) |
| ACI-DOM-261 | e26af315 | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:5 | AgentReferenceDelivery.bundle_digest: [ContentDigest](#contentdigest) |
| ACI-NF-080 | e26bb9db | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:2 | Invariant GRP-I3: needs_formal (prose Formal) |
| ACI-DOM-205 | e2c46767 | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:0:2 | ResourceBudget.max_output_tokens: integer (Non-negative finite limits.) |
| ACI-ERR-025 | e31d4f46 | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:7 | Error mapping for DeliverReferenceScoutBundleToAgent: "Same scoped idempotency key carries another `command_digest`" -> Idempotency conflict; return no new receipt. |
| ACI-DOM-206 | e331df5c | domain-field | derivable-needs-harness | domain.md#GroupResult:field:1 | GroupResult.group_aggregate_id: string |
| ACI-TR-310 | e3f2c473 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`pending`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `pending` is rejected (no valid transition) |
| ACI-DOM-207 | e42d2809 | domain-field | derivable-needs-harness | domain.md#EffectIntent:field:3 | EffectIntent.retry_class: [RetryClass](#retryclass) |
| ACI-TR-311 | e4cbc166 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `ready` is rejected (no valid transition) |
| ACI-DOM-208 | e5271dbe | domain-field | derivable-needs-harness | domain.md#RevealManifest:field:1 | RevealManifest.group_aggregate_id: string |
| ACI-DOM-209 | e53a15dd | domain-field | derivable-needs-harness | domain.md#ExecutionAuthorityFence:field:4 | ExecutionAuthorityFence.fence_digest: [ContentDigest](#contentdigest) (Equality identity checked before every external start.) |
| ACI-TR-312 | e566b76a | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `deliberating` is rejected (no valid transition) |
| ACI-DOM-262 | e5672b61 | domain-field | derivable-needs-harness | domain.md#Attempt:field:9 | Attempt.request_digest: [ContentDigest](#contentdigest) |
| ACI-EVT-045 | e5b4c93e | event-obligation | derivable-needs-harness | events.md#publication.persisted | Event publication.persisted is emitted with valid payload |
| ACI-EVT-046 | e64b523d | event-obligation | derivable-needs-harness | events.md#attempt.waiting_tool | Event attempt.waiting_tool is emitted with valid payload |
| ACI-TR-313 | e64b95a0 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:2 | Transition `collecting` --[`collection.closed`](events.md#collectionclosed)--> `revealing` succeeds when guarded |
| ACI-DOM-210 | e67d9ea7 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:3:1 | PublicationCandidate.message_type: string |
| ACI-NF-081 | e68c7aeb | needs-formal | needs-formal | operations.md#CancelRun:rule:0 | Rule O-CANCEL-1: needs_formal (prose Formal) |
| ACI-ERR-026 | e69cd175 | error-obligation | derivable-needs-harness | operations.md#DeliverReferenceScoutBundleToAgent:errorstate:1 | Error mapping for DeliverReferenceScoutBundleToAgent: "Commit, lifecycle delivery and artifact disagree on ScoutRun, artifact or digest" -> Integrity failure; reject. |
| ACI-TR-314 | e8301b92 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `revealing` is rejected (no valid transition) |
| ACI-TR-315 | e8dea1a2 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-316 | e8e4d3c8 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`unknown`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `unknown` is rejected (no valid transition) |
| ACI-EVT-047 | e90bdf32 | event-obligation | derivable-needs-harness | events.md#Attempt events | Event Attempt events is emitted with valid payload |
| ACI-EVT-048 | e94eb48b | event-obligation | derivable-needs-harness | events.md#vote.accepted | Event vote.accepted is emitted with valid payload |
| ACI-TR-317 | ea16bfaf | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state `failed` is rejected (no valid transition) |
| ACI-TR-318 | ea687925 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `failed` is rejected (no valid transition) |
| ACI-TR-319 | ea82e711 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelling`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `cancelling` is rejected (no valid transition) |
| ACI-TR-320 | eab5f732 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.running`](events.md#attemptrunning) | Event [`attempt.running`](events.md#attemptrunning) in state `running` is rejected (no valid transition) |
| ACI-TR-321 | eaf5eed5 | valid-transition | derivable-needs-harness | states.md#RunLifecycle:transition:10 | Transition `reconciliation_required` --`reconciliation.retry_requested`--> `close_pending` succeeds when guarded |
| ACI-DOM-211 | eb1fcbfd | domain-field | derivable-needs-harness | domain.md#Attempt:field:0 | Attempt.attempt_id: string |
| ACI-TR-322 | eb7ae41b | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`collection.closed`](events.md#collectionclosed) | Event [`collection.closed`](events.md#collectionclosed) in state `deliberating` is rejected (no valid transition) |
| ACI-TR-323 | eb976e81 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) | Event [`run.execution_terminal_elected`](events.md#runexecution_terminal_elected) in state `ready` is rejected (no valid transition) |
| ACI-TR-324 | ebf1a525 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`voting`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `voting` is rejected (no valid transition) |
| ACI-TR-325 | ec40afec | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-326 | ec4e3f88 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `cancel_requested` is rejected (no valid transition) |
| ACI-TR-327 | ecf3d006 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:none:[`audit_opening.requested`](events.md#audit_openingrequested) | Event [`audit_opening.requested`](events.md#audit_openingrequested) in state none is rejected (no valid transition) |
| ACI-ERR-016 | ecfb157b | error-obligation | derivable-needs-harness | operations.md#ConfirmRuntimeDispatch:errorstate:3 | Error mapping for ConfirmRuntimeDispatch: "Capability combination changes semantics" -> Reject until a new spec version is explicitly reconfirmed. |
| ACI-TR-328 | ed08bae5 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_close.requested`](events.md#audit_closerequested) | Event [`audit_close.requested`](events.md#audit_closerequested) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-TR-329 | ed5a85c9 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_opening.verified`](events.md#audit_openingverified) | Event [`audit_opening.verified`](events.md#audit_openingverified) in state `closed` is rejected (no valid transition) |
| ACI-DOM-212 | ed8e5fff | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:2:1 | AgentInvocationPlan.task_ref: [VersionedReference](#versionedreference) (Compiled local contract.) |
| ACI-DOM-213 | edb508d4 | domain-field | derivable-needs-harness | domain.md#Contribution:field:0 | Contribution.message_id: string |
| ACI-TR-330 | ee570beb | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `revealing` is rejected (no valid transition) |
| ACI-NF-099 | ee7fa730 | needs-formal | needs-formal | operations.md#DeliverReferenceScoutBundleToAgent:rule:6 | Rule O-ARD-7: needs_formal (prose Formal) |
| ACI-NF-082 | eebc0bb6 | needs-formal | needs-formal | states.md#RunLifecycle:invariant:5 | Invariant RUN-I6: needs_formal (prose Formal) |
| ACI-TR-331 | eed74953 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state `failed` is rejected (no valid transition) |
| ACI-NF-083 | eef45d75 | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:6 | Invariant GRP-I7: needs_formal (prose Formal) |
| ACI-TR-332 | ef1faec3 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `closed` is rejected (no valid transition) |
| ACI-DOM-214 | ef8f0cf4 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:6 | SoleWriterEvidenceBundle.evidence_digest: [ContentDigest](#contentdigest) (Canonical digest over the complete bundle manifest.) |
| ACI-TR-333 | efd04371 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`running`:[`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) | Event [`attempt.cancel_acknowledged`](events.md#attemptcancel_acknowledged) in state `running` is rejected (no valid transition) |
| ACI-RULE-015 | f012b8f1 | rule-validation | derivable-pure | operations.md#CommitGroupResult:rule:0 | Rule O-COMMIT-1: duplicate-capped (count cap) |
| ACI-DOM-215 | f083435e | domain-field | derivable-needs-harness | domain.md#Seat:field:4 | Seat.role_delta_ref: [ArtifactId](#artifactid) |
| ACI-NF-084 | f0885055 | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:4 | Invariant GRP-I5: needs_formal (prose Formal) |
| ACI-TR-334 | f092f659 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`verdict.computed`](events.md#verdictcomputed) | Event [`verdict.computed`](events.md#verdictcomputed) in state `failed` is rejected (no valid transition) |
| ACI-TR-335 | f0d598df | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`run.created`](events.md#runcreated) | Event [`run.created`](events.md#runcreated) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-DOM-216 | f1939ee6 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:1:1 | AgentTerminalResult.operation_id: string (Must match the sealed request.) |
| ACI-EVT-049 | f1a6996f | event-obligation | derivable-needs-harness | events.md#deadline.fired | Event deadline.fired is emitted with valid payload |
| ACI-TR-336 | f24c8402 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`deliberating`:[`position.accepted`](events.md#positionaccepted) | Event [`position.accepted`](events.md#positionaccepted) in state `deliberating` is rejected (no valid transition) |
| ACI-DOM-263 | f2e0596e | domain-field | derivable-needs-harness | domain.md#Attempt:field:2 | Attempt.operation_id: string |
| ACI-DOM-217 | f2e9a3fd | domain-field | derivable-needs-harness | domain.md#MaterializedAgentInvocation:field:1 | MaterializedAgentInvocation.effective_input_ref: [ArtifactId](#artifactid) (Finalized [EffectiveInputArtifact](#effectiveinputartifact).) |
| ACI-NF-085 | f30019e8 | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:8 | Invariant GRP-I9: needs_formal (prose Formal) |
| ACI-DOM-218 | f312b4af | domain-field | derivable-needs-harness | domain.md#Run:field:6 | Run.terminal_event_id: string |
| ACI-TR-337 | f3aed3d2 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`running`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `running` is rejected (no valid transition) |
| ACI-TR-338 | f3c91c81 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.failed`](events.md#attemptfailed) | Event [`attempt.failed`](events.md#attemptfailed) in state `starting` is rejected (no valid transition) |
| ACI-DOM-220 | f4616f89 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:2 | AgentTerminalResult.completion_kind: string (One of `completed`, `failed`, `cancelled`, `unknown`.) |
| ACI-QRY-003 | f4bd361f | query-behavior | derivable-needs-harness | queries.md#GetRuntimeProjection | Query GetRuntimeProjection returns its projected read model without side effects |
| ACI-TR-339 | f5e401b6 | valid-transition | derivable-needs-harness | states.md#GroupLifecycle:transition:12 | Transition any nonterminal except `cancelling` --[`group.failed`](events.md#groupfailed)--> `failed` succeeds when guarded |
| ACI-TR-340 | f62f1b54 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`round.closed`](events.md#roundclosed) | Event [`round.closed`](events.md#roundclosed) in state `failed` is rejected (no valid transition) |
| ACI-NF-086 | f6325344 | needs-formal | needs-formal | operations.md#ElectRunTerminal:rule:3 | Rule O-TERM-4: needs_formal (prose Formal) |
| ACI-ENUM-005 | f6969962 | domain-enum | derivable-needs-harness | domain.md#RetryClass:enum | RetryClass vocabulary is exactly {retryable,non_retryable} |
| ACI-TR-341 | f6acf250 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) | Event [`audit_opening.reconciliation_required`](events.md#audit_openingreconciliation_required) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-TR-342 | f6d2829e | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`failed`:[`attempt.starting`](events.md#attemptstarting) | Event [`attempt.starting`](events.md#attemptstarting) in state `failed` is rejected (no valid transition) |
| ACI-TR-343 | f732105d | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`cancelled`:[`cancellation.requested`](events.md#cancellationrequested) | Event [`cancellation.requested`](events.md#cancellationrequested) in state `cancelled` is rejected (no valid transition) |
| ACI-DOM-221 | f7858a31 | domain-field | derivable-needs-harness | domain.md#MaterializedAgentInvocation:field:4 | MaterializedAgentInvocation.materialization_digest: [ContentDigest](#contentdigest) (Canonical equality identity.) |
| ACI-DOM-222 | f7d95581 | domain-field | derivable-needs-harness | domain.md#PublicationCandidate:field:2:1 | PublicationCandidate.attempt_id: string |
| ACI-MAP-006 | f7e41369 | mapping-row | derivable-needs-harness | mappings.md#BusPublicationToContribution | Mapping BusPublicationToContribution ([BusPublication](domain.md#buspublication) + authenticated capability context -> durable [PublicationCandidate](domain.md#publicationcandidate),) maps all fields correctly |
| ACI-EVT-050 | f82532dd | event-obligation | derivable-needs-harness | events.md#round.closed | Event round.closed is emitted with valid payload |
| ACI-NF-087 | f834138a | needs-formal | needs-formal | states.md#GroupLifecycle:invariant:1 | Invariant GRP-I2: needs_formal (prose Formal) |
| ACI-TR-344 | f85ddeed | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancel_requested`:[`attempt.unknown`](events.md#attemptunknown) | Event [`attempt.unknown`](events.md#attemptunknown) in state `cancel_requested` is rejected (no valid transition) |
| ACI-DOM-223 | f8677a28 | domain-field | derivable-needs-harness | domain.md#AgentTerminalResult:field:0 | AgentTerminalResult.result_version: string (Supported terminal-result schema version.) |
| ACI-TR-345 | f8e23851 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`revealing`:[`critique.accepted`](events.md#critiqueaccepted) | Event [`critique.accepted`](events.md#critiqueaccepted) in state `revealing` is rejected (no valid transition) |
| ACI-TR-346 | f94affd4 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`reconciliation_required`:[`run.started`](events.md#runstarted) | Event [`run.started`](events.md#runstarted) in state `reconciliation_required` is rejected (no valid transition) |
| ACI-DOM-224 | f9551703 | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:7 | AgentExecutionRequest.sandbox_policy: [SandboxPolicy](#sandboxpolicy) (Launcher-enforced isolation.) |
| ACI-DOM-264 | f9de72de | domain-field | derivable-needs-harness | domain.md#AgentReferenceDelivery:field:11 | AgentReferenceDelivery.effective_input_entry_ordinal: integer |
| ACI-DOM-225 | f9e0d96d | domain-field | derivable-needs-harness | domain.md#ResourceBudget:field:0:1 | ResourceBudget.max_input_tokens: integer (Non-negative finite limits.) |
| ACI-TR-347 | fa0e8be1 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`group.cancelled`](events.md#groupcancelled) | Event [`group.cancelled`](events.md#groupcancelled) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-348 | fa211e02 | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`closed`:[`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) | Event [`audit_close.reconciliation_required`](events.md#audit_closereconciliation_required) in state `closed` is rejected (no valid transition) |
| ACI-TR-349 | fa234297 | valid-transition | derivable-needs-harness | states.md#AttemptLifecycle:transition:2 | Transition `starting` --[`attempt.running`](events.md#attemptrunning)--> `running` succeeds when guarded |
| ACI-TR-350 | fae36007 | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`starting`:[`attempt.requested`](events.md#attemptrequested) | Event [`attempt.requested`](events.md#attemptrequested) in state `starting` is rejected (no valid transition) |
| ACI-TR-351 | faf9a1d5 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`failed`:[`vote.accepted`](events.md#voteaccepted) | Event [`vote.accepted`](events.md#voteaccepted) in state `failed` is rejected (no valid transition) |
| ACI-MAP-007 | fb66707c | mapping-row | derivable-needs-harness | mappings.md#AgentInvocationPlanToMaterializedInvocation | Mapping AgentInvocationPlanToMaterializedInvocation ([AgentInvocationPlan](domain.md#agentinvocationplan) -> [MaterializedAgentInvocation](domain.md#materializedagentinvocation),) maps all fields correctly |
| ACI-DOM-226 | fb9945b9 | domain-field | derivable-needs-harness | domain.md#RawProviderOutput:field:7 | RawProviderOutput.provider_metadata: object |
| ACI-TR-352 | fba28a2c | invalid-transition | derivable-needs-harness | states.md#AttemptLifecycle:invalid:`cancelled`:[`attempt.completed`](events.md#attemptcompleted) | Event [`attempt.completed`](events.md#attemptcompleted) in state `cancelled` is rejected (no valid transition) |
| ACI-TR-353 | fc858f28 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:any nonterminal except `cancelling`:[`reveal.published`](events.md#revealpublished) | Event [`reveal.published`](events.md#revealpublished) in state any nonterminal except `cancelling` is rejected (no valid transition) |
| ACI-TR-354 | fce40c7a | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`ready`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `ready` is rejected (no valid transition) |
| ACI-DOM-228 | fd02c81b | domain-field | derivable-needs-harness | domain.md#BusPublication:field:1 | BusPublication.operation_id: string (Must equal the capability-bound operation.) |
| ACI-DOM-229 | fd70c9cc | domain-field | derivable-needs-harness | domain.md#AgentExecutionRequest:field:9 | AgentExecutionRequest.sealed_request_digest: [ContentDigest](#contentdigest) (Equality identity for idempotent start.) |
| ACI-DOM-230 | fe1deb7d | domain-field | derivable-needs-harness | domain.md#Contribution:field:4 | Contribution.round_id: string |
| ACI-DOM-231 | fe6d567c | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:6 | AgentInvocationPlan.resource_budget: [ResourceBudget](#resourcebudget) (Finite typed limits.) |
| ACI-TR-355 | fe72dc2a | invalid-transition | derivable-needs-harness | states.md#RunLifecycle:invalid:`confirmed`:[`audit_close.verified`](events.md#audit_closeverified) | Event [`audit_close.verified`](events.md#audit_closeverified) in state `confirmed` is rejected (no valid transition) |
| ACI-DOM-232 | fe821ccc | domain-field | derivable-needs-harness | domain.md#AgentInvocationPlan:field:4:1 | AgentInvocationPlan.tool_profile_ref: [VersionedReference](#versionedreference) (Frozen output/tool contracts.) |
| ACI-EVT-051 | fe999885 | event-obligation | derivable-needs-harness | events.md#cancellation.requested | Event cancellation.requested is emitted with valid payload |
| ACI-DOM-233 | ff8c6257 | domain-field | derivable-needs-harness | domain.md#Artifact:field:5 | Artifact.size_bytes: integer |
| ACI-DOM-234 | ff988669 | domain-field | derivable-needs-harness | domain.md#SoleWriterEvidenceBundle:field:4 | SoleWriterEvidenceBundle.negative_bypass_results_ref: [ArtifactId](#artifactid) (Direct file access, alternate-process and legacy-path attempts must fail.) |
| ACI-NF-088 | ffaa08a5 | needs-formal | needs-formal | operations.md#CloseCollection:rule:2 | Rule O-CLOSE-3: needs_formal (prose Formal) |
| ACI-TR-356 | fffe47e5 | invalid-transition | derivable-needs-harness | states.md#GroupLifecycle:invalid:`completed`:[`group.started`](events.md#groupstarted) | Event [`group.started`](events.md#groupstarted) in state `completed` is rejected (no valid transition) |

## Unresolved Formal Gaps

needs_formal (un-formalized — no closed checkable expression): 99

- `ACI-NF-001` operations.md#ConfirmRuntimeDispatch:rule:3 — Rule O-CONF-4: needs_formal (prose Formal)
- `ACI-NF-002` operations.md#VerifyPublicationReceipt:rule:6 — Rule O-RECEIPT-7: needs_formal (prose Formal)
- `ACI-NF-003` operations.md#RecordUsageObservation:rule:1 — Rule O-USAGE-2: needs_formal (prose Formal)
- `ACI-NF-004` operations.md#ComputeFixedProofVerdict:rule:3 — Rule O-VER-4: needs_formal (prose Formal)
- `ACI-NF-005` operations.md#StartAgentAttempt:rule:4 — Rule O-ATT-5: needs_formal (prose Formal)
- `ACI-NF-006` operations.md#CancelRun:rule:2 — Rule O-CANCEL-3: needs_formal (prose Formal)
- `ACI-NF-007` operations.md#VerifyAuditClose:rule:0 — Rule O-ACLOSE-1: needs_formal (prose Formal)
- `ACI-NF-008` operations.md#VerifyAuditClose:rule:2 — Rule O-ACLOSE-3: needs_formal (prose Formal)
- `ACI-NF-009` operations.md#RecordUsageObservation:rule:4 — Rule O-USAGE-5: needs_formal (prose Formal)
- `ACI-NF-010` states.md#RunLifecycle:invariant:6 — Invariant RUN-I7: needs_formal (prose Formal)
- `ACI-NF-011` states.md#GroupLifecycle:invariant:5 — Invariant GRP-I6: needs_formal (prose Formal)
- `ACI-NF-012` operations.md#CancelRun:rule:1 — Rule O-CANCEL-2: needs_formal (prose Formal)
- `ACI-NF-013` operations.md#ConfirmRuntimeDispatch:rule:1 — Rule O-CONF-2: needs_formal (prose Formal)
- `ACI-NF-014` operations.md#PublishBusContribution:rule:3 — Rule O-PUB-4: needs_formal (prose Formal)
- `ACI-NF-089` operations.md#DeliverReferenceScoutBundleToAgent:rule:7 — Rule O-ARD-8: needs_formal (prose Formal)
- `ACI-NF-015` operations.md#VerifyPublicationReceipt:rule:3 — Rule O-RECEIPT-4: needs_formal (prose Formal)
- `ACI-NF-016` operations.md#RecordAttemptObservation:rule:0 — Rule O-OBS-1: needs_formal (prose Formal)
- `ACI-NF-017` operations.md#StartAgentAttempt:rule:6 — Rule O-ATT-7: needs_formal (prose Formal)
- `ACI-NF-018` operations.md#ConfirmRuntimeDispatch:rule:0 — Rule O-CONF-1: needs_formal (prose Formal)
- `ACI-NF-019` operations.md#StartGroup:rule:2 — Rule O-GROUP-3: needs_formal (prose Formal)
- `ACI-NF-020` states.md#AttemptLifecycle:invariant:7 — Invariant ATT-I8: needs_formal (prose Formal)
- `ACI-NF-021` operations.md#PublishBusContribution:rule:6 — Rule O-PUB-7: needs_formal (prose Formal)
- `ACI-NF-022` operations.md#VerifyAuditOpening:rule:3 — Rule O-OPEN-4: needs_formal (prose Formal)
- `ACI-NF-090` operations.md#DeliverReferenceScoutBundleToAgent:rule:2 — Rule O-ARD-3: needs_formal (prose Formal)
- `ACI-NF-023` operations.md#ElectRunTerminal:rule:2 — Rule O-TERM-3: needs_formal (prose Formal)
- `ACI-NF-024` operations.md#ConfirmRuntimeDispatch:rule:2 — Rule O-CONF-3: needs_formal (prose Formal)
- `ACI-NF-025` operations.md#VerifyPublicationReceipt:rule:2 — Rule O-RECEIPT-3: needs_formal (prose Formal)
- `ACI-NF-026` operations.md#PublishRevealManifest:rule:0 — Rule O-REV-1: needs_formal (prose Formal)
- `ACI-NF-027` operations.md#PublishConnectionHandoff:rule:0 — Rule O-HAND-1: needs_formal (prose Formal)
- `ACI-NF-028` operations.md#VerifyAuditOpening:rule:1 — Rule O-OPEN-2: needs_formal (prose Formal)
- `ACI-NF-091` operations.md#StartAgentAttempt:rule:1 — Rule O-ATT-2: needs_formal (prose Formal)
- `ACI-NF-029` states.md#AttemptLifecycle:invariant:2 — Invariant ATT-I3: needs_formal (prose Formal)
- `ACI-NF-030` states.md#AttemptLifecycle:invariant:8 — Invariant ATT-I9: needs_formal (prose Formal)
- `ACI-NF-092` operations.md#DeliverReferenceScoutBundleToAgent:rule:8 — Rule O-ARD-9: needs_formal (prose Formal)
- `ACI-NF-031` operations.md#StartAgentAttempt:rule:3 — Rule O-ATT-4: needs_formal (prose Formal)
- `ACI-NF-032` operations.md#RecordAttemptObservation:rule:3 — Rule O-OBS-4: needs_formal (prose Formal)
- `ACI-NF-093` operations.md#DeliverReferenceScoutBundleToAgent:rule:1 — Rule O-ARD-2: needs_formal (prose Formal)
- `ACI-NF-033` states.md#AttemptLifecycle:invariant:6 — Invariant ATT-I7: needs_formal (prose Formal)
- `ACI-NF-034` operations.md#VerifyPublicationReceipt:rule:5 — Rule O-RECEIPT-6: needs_formal (prose Formal)
- `ACI-NF-035` operations.md#StartGroup:rule:1 — Rule O-GROUP-2: needs_formal (prose Formal)
- `ACI-NF-036` operations.md#RecordAttemptObservation:rule:4 — Rule O-OBS-5: needs_formal (prose Formal)
- `ACI-NF-037` states.md#GroupLifecycle:invariant:7 — Invariant GRP-I8: needs_formal (prose Formal)
- `ACI-NF-038` states.md#AttemptLifecycle:invariant:0 — Invariant ATT-I1: needs_formal (prose Formal)
- `ACI-NF-039` operations.md#ElectRunTerminal:rule:0 — Rule O-TERM-1: needs_formal (prose Formal)
- `ACI-NF-040` operations.md#StartAgentAttempt:rule:0 — Rule O-ATT-1: needs_formal (prose Formal)
- `ACI-NF-041` operations.md#CommitGroupResult:rule:3 — Rule O-COMMIT-4: needs_formal (prose Formal)
- `ACI-NF-042` operations.md#StartRun:rule:0 — Rule O-RUN-1: needs_formal (prose Formal)
- `ACI-NF-043` operations.md#RecordUsageObservation:rule:0 — Rule O-USAGE-1: needs_formal (prose Formal)
- `ACI-NF-044` operations.md#VerifyPublicationReceipt:rule:1 — Rule O-RECEIPT-2: needs_formal (prose Formal)
- `ACI-NF-094` operations.md#StartAgentAttempt:rule:8 — Rule O-ATT-9: needs_formal (prose Formal)
- `ACI-NF-045` operations.md#PublishBusContribution:rule:2 — Rule O-PUB-3: needs_formal (prose Formal)
- `ACI-NF-046` operations.md#VerifyAuditOpening:rule:2 — Rule O-OPEN-3: needs_formal (prose Formal)
- `ACI-NF-047` operations.md#ConfirmRuntimeDispatch:rule:4 — Rule O-CONF-5: needs_formal (prose Formal)
- `ACI-NF-048` operations.md#ComputeFixedProofVerdict:rule:1 — Rule O-VER-2: needs_formal (prose Formal)
- `ACI-NF-049` operations.md#VerifyPublicationReceipt:rule:0 — Rule O-RECEIPT-1: needs_formal (prose Formal)
- `ACI-NF-095` operations.md#DeliverReferenceScoutBundleToAgent:rule:4 — Rule O-ARD-5: needs_formal (prose Formal)
- `ACI-NF-096` operations.md#DeliverReferenceScoutBundleToAgent:rule:3 — Rule O-ARD-4: needs_formal (prose Formal)
- `ACI-NF-050` states.md#GroupLifecycle:invariant:0 — Invariant GRP-I1: needs_formal (prose Formal)
- `ACI-NF-051` operations.md#ElectRunTerminal:rule:1 — Rule O-TERM-2: needs_formal (prose Formal)
- `ACI-NF-052` operations.md#CloseCollection:rule:0 — Rule O-CLOSE-1: needs_formal (prose Formal)
- `ACI-NF-053` states.md#AttemptLifecycle:invariant:5 — Invariant ATT-I6: needs_formal (prose Formal)
- `ACI-NF-054` operations.md#StartRun:rule:1 — Rule O-RUN-2: needs_formal (prose Formal)
- `ACI-NF-055` operations.md#CommitGroupResult:rule:1 — Rule O-COMMIT-2: needs_formal (prose Formal)
- `ACI-NF-056` operations.md#VerifyAuditClose:rule:1 — Rule O-ACLOSE-2: needs_formal (prose Formal)
- `ACI-NF-057` operations.md#PublishBusContribution:rule:4 — Rule O-PUB-5: needs_formal (prose Formal)
- `ACI-NF-058` operations.md#ComputeFixedProofVerdict:rule:0 — Rule O-VER-1: needs_formal (prose Formal)
- `ACI-NF-059` operations.md#StartAgentAttempt:rule:2 — Rule O-ATT-3: needs_formal (prose Formal)
- `ACI-NF-060` operations.md#VerifyAuditOpening:rule:0 — Rule O-OPEN-1: needs_formal (prose Formal)
- `ACI-NF-061` operations.md#ComputeFixedProofVerdict:rule:2 — Rule O-VER-3: needs_formal (prose Formal)
- `ACI-NF-062` states.md#RunLifecycle:invariant:3 — Invariant RUN-I4: needs_formal (prose Formal)
- `ACI-NF-063` operations.md#StartAgentAttempt:rule:5 — Rule O-ATT-6: needs_formal (prose Formal)
- `ACI-NF-064` operations.md#RecordUsageObservation:rule:3 — Rule O-USAGE-4: needs_formal (prose Formal)
- `ACI-NF-065` operations.md#PublishConnectionHandoff:rule:1 — Rule O-HAND-2: needs_formal (prose Formal)
- `ACI-NF-066` states.md#AttemptLifecycle:invariant:9 — Invariant ATT-I10: needs_formal (prose Formal)
- `ACI-NF-067` operations.md#StartGroup:rule:0 — Rule O-GROUP-1: needs_formal (prose Formal)
- `ACI-NF-097` operations.md#DeliverReferenceScoutBundleToAgent:rule:5 — Rule O-ARD-6: needs_formal (prose Formal)
- `ACI-NF-068` states.md#RunLifecycle:invariant:4 — Invariant RUN-I5: needs_formal (prose Formal)
- `ACI-NF-069` operations.md#PublishRevealManifest:rule:2 — Rule O-REV-3: needs_formal (prose Formal)
- `ACI-NF-070` operations.md#PublishConnectionHandoff:rule:2 — Rule O-HAND-3: needs_formal (prose Formal)
- `ACI-NF-071` operations.md#PublishBusContribution:rule:5 — Rule O-PUB-6: needs_formal (prose Formal)
- `ACI-NF-072` operations.md#PublishBusContribution:rule:0 — Rule O-PUB-1: needs_formal (prose Formal)
- `ACI-NF-073` operations.md#CloseCollection:rule:3 — Rule O-CLOSE-4: needs_formal (prose Formal)
- `ACI-NF-074` operations.md#RecordAttemptObservation:rule:2 — Rule O-OBS-3: needs_formal (prose Formal)
- `ACI-NF-075` states.md#RunLifecycle:invariant:1 — Invariant RUN-I2: needs_formal (prose Formal)
- `ACI-NF-098` operations.md#DeliverReferenceScoutBundleToAgent:rule:0 — Rule O-ARD-1: needs_formal (prose Formal)
- `ACI-NF-076` operations.md#ComputeFixedProofVerdict:rule:4 — Rule O-VER-5: needs_formal (prose Formal)
- `ACI-NF-077` operations.md#StartAgentAttempt:rule:7 — Rule O-ATT-8: needs_formal (prose Formal)
- `ACI-NF-078` operations.md#PublishBusContribution:rule:1 — Rule O-PUB-2: needs_formal (prose Formal)
- `ACI-NF-079` operations.md#PublishRevealManifest:rule:3 — Rule O-REV-4: needs_formal (prose Formal)
- `ACI-NF-080` states.md#GroupLifecycle:invariant:2 — Invariant GRP-I3: needs_formal (prose Formal)
- `ACI-NF-081` operations.md#CancelRun:rule:0 — Rule O-CANCEL-1: needs_formal (prose Formal)
- `ACI-NF-099` operations.md#DeliverReferenceScoutBundleToAgent:rule:6 — Rule O-ARD-7: needs_formal (prose Formal)
- `ACI-NF-082` states.md#RunLifecycle:invariant:5 — Invariant RUN-I6: needs_formal (prose Formal)
- `ACI-NF-083` states.md#GroupLifecycle:invariant:6 — Invariant GRP-I7: needs_formal (prose Formal)
- `ACI-NF-084` states.md#GroupLifecycle:invariant:4 — Invariant GRP-I5: needs_formal (prose Formal)
- `ACI-NF-085` states.md#GroupLifecycle:invariant:8 — Invariant GRP-I9: needs_formal (prose Formal)
- `ACI-NF-086` operations.md#ElectRunTerminal:rule:3 — Rule O-TERM-4: needs_formal (prose Formal)
- `ACI-NF-087` states.md#GroupLifecycle:invariant:1 — Invariant GRP-I2: needs_formal (prose Formal)
- `ACI-NF-088` operations.md#CloseCollection:rule:2 — Rule O-CLOSE-3: needs_formal (prose Formal)

needs-harness (derivable, requires a runtime/effect to test): 707

<!-- ENGINE-REGION-END -->
