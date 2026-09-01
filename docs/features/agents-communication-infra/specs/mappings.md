---
id: agents-communication-infra
feature: Agents Communication Infra
type: mappings
title: "Agents Communication Infra — Mappings"
status: draft
version: 0.4.0
derived-from: ../discovery/feature-discovery/agents-communication-infra.md@0.2.1
---

# Mappings: Agents Communication Infra

## PendingRuntimeDispatchToConfirmedAuthority

**From:** exact canonical `aci.pending-runtime-dispatch@1` bytes, one admitted
[ConfirmationObservation](domain.md#confirmationobservation), and the server's immutable capability
resolution
**To:** [ConfirmedDispatch](domain.md#confirmeddispatch),
[ConfirmedTurnGraph](domain.md#confirmedturngraph), exactly two
[ContinuationInputMapping](domain.md#continuationinputmapping) records and one
[Run](domain.md#run) in `opening_pending`
**Direction:** inbound confirmation projection and local acceptance

| Source | Target | Transform / rule |
|---|---|---|
| exact pending bytes | pending-sheet artifact/digest | Finalize the bytes without normalization or reread; `pending_sheet_digest = SHA-256(exact bytes)`. |
| pending `recipe_ref`, ordered `schema_refs`, prompt refs and budgets | canonical `aci.dispatch-spec@1` | Project exactly after closed-shape validation; no default, clock, random value or environment discovery. |
| pending logical requirements + server resolution | spec `capability_resolution` and immutable resolution artifact/digest | Resolve server-side; reject a caller-expanded effective grant or any difference from the trusted preview. |
| pending `workflow` | spec `group_graph` | Replace only the schema label; preserve the exact ordered three nodes, two edges, workflow kind and loop ceiling. |
| pending policy refs | spec `decision_policies` | Preserve exact pinned policy refs, freeze `same_session_preferred`, and freeze source types `[author.output, reviewer.output]`. |
| trusted observation | observation artifact/digest plus `confirmed_by`/`confirmed_at` | Require exact issuer evidence, principal, channel, action, dispatch/revision and displayed pending/spec digests; project principal/time without a writer-clock replacement. |
| verified spec graph + dispatch/spec digest | confirmed graph, continuation, source messages, events, effect and receipt IDs | Derive only through the manifest-pinned `aci.confirmed-dispatch-id-preimage@1` contract; supplied runtime IDs are invalid. |
| the author and reviewer source selectors | two continuation mappings in slot order | Map author output to `prior_author_output` at ordinal `0` and reviewer output to `review_feedback` at ordinal `1`; both target author turn `1`. |
| each closed `aci.continuation-input-binding@1` value | `confirmed_binding_digest` | Hash the complete canonical binding while excluding only `mapping_id` and `mapping_version`; then derive `mapping_id` independently. |
| pending, spec, observation, capability, graph, mapping-set, complete identity-derivation-contract and closed payload-schema-bundle digests plus frozen versions/mode | canonical [ConfirmedAuthorityEnvelope](domain.md#confirmedauthorityenvelope) | Construct the exact closed `aci.confirmed-authority@1` value; hash it as `confirmed_authority_digest`; exclude command/key/offset/receipt/writer-clock transport data. |
| confirmed authority + derived identities | accepted domain rows, two event payloads and one audit-opening effect payload | Finalize artifacts, then commit every CONF-000 acceptance member atomically; no audit row, external call, Attempt or continuation lifecycle transition is produced. |

The normative source, target bytes, field-level projection, derivation inputs and expected IDs are
frozen by [Runtime Confirmation Authority v1](confirmation-authority.md) and its
[`confirmed-dispatch-v1`](fixtures/confirmed-dispatch-v1/manifest.json) package. A different source
revision, observation or semantic resolution requires a new confirmation authority; it is never
silently normalized into the old mapping.

## AgentInvocationPlanToMaterializedInvocation

**From:** [AgentInvocationPlan](domain.md#agentinvocationplan)  
**To:** [MaterializedAgentInvocation](domain.md#materializedagentinvocation),
[EffectiveInputArtifact](domain.md#effectiveinputartifact), then sealed
[AgentExecutionRequest](domain.md#agentexecutionrequest)  
**Direction:** outbound to provider boundary

| Source | Target | Transform / rule |
|---|---|---|
| role/task/base snapshot/role delta refs | ordered instruction/context entries | resolve exact bytes; retain order, role, digest and source ref |
| tool profile | tool declarations | capture exact names, descriptions and input schemas presented |
| response schema ref | response schema entry | capture exact schema bytes/digest |
| adapter/provider/model refs | materialization metadata | record resolved identities, versions/digests and namespaced wrapper metadata |
| history/reveal inputs | typed [EffectiveInputEntry](domain.md#effectiveinputentry) values | preserve entry type, manifest ID, message ID, author, content hash and visibility-policy reference |
| deadline/resource budget | invocation controls | canonical values plus observable provider-native translation |
| sandbox policy/authority fence | sealed launch controls | preserve policy/fence digest; launcher revalidates both before start |

Unobservable provider-side transformations are recorded as limitations, not reconstructed. Equal
base snapshots are proven by hash; role differences require a confirmed `role_delta_ref`.

## RawProviderOutputToCanonicalObservations

**From:** [RawProviderOutput](domain.md#rawprovideroutput)  
**To:** [Attempt](domain.md#attempt) observations, [BusPublication](domain.md#buspublication) candidate
and [UsageObservation](events.md#usageobserved)  
**Direction:** inbound from provider boundary

Raw bytes/native events are stored first with provider/model/attempt provenance. Canonical status is
mapped to `queued`, `running`, `waiting_tool`, `completed`, `failed`, `cancelled` or `unknown`.
Structured output is schema-validated before becoming a publication candidate. Provider usage fields
map only when explicitly reported; missing input/cache/output/reasoning counters remain `null`.
Provider prose, terminal status and usage metadata never substitute for a verified bus receipt.
Codex and Claude native terminals use provider-specific parsers only at the boundary and must yield
the same versioned [AgentTerminalResult](domain.md#agentterminalresult); ambiguous receipt extraction
or unknown result versions fail closed.

## BusPublicationToContribution

**From:** [BusPublication](domain.md#buspublication) + authenticated capability context  
**To:** durable [PublicationCandidate](domain.md#publicationcandidate),
[RuntimeEventEnvelope](domain.md#runtimeeventenvelope) and [PublicationReceipt](domain.md#publicationreceipt),
then an official [Contribution](domain.md#contribution) only after parent verification  
**Direction:** inbound

| Source | Target | Rule |
|---|---|---|
| capability context | dispatch/run/group/version/seat/agent/attempt/principal/phase | derived; never trusted from payload |
| authored operation/round/type | logical message key | must equal capability/active policy |
| payload or payload ref | immutable payload ref/hash | validate schema, size, classification and digest |
| idempotency key + canonical digest | command/message dedupe | identical retry returns original receipt; mismatch conflicts |
| committed `publication.persisted` | canonical receipt version/status/event/message/offset/hash/key | receipt returned only after commit; optional `transport_replayed` remains outside the byte-stable receipt |
| verified receipt + authenticated attempt/operation/logical key | `attempt.result_accepted` + type-specific official acceptance | commit atomically; only this contribution is quorum-eligible |

Candidate persistence and official acceptance are deliberately separate. Recovery resolves the
same candidate and terminal result by `(attempt_id, operation_id, logical_message_key)`, repeats
exact verification and returns the prior outcome without duplicating official events.

## ContinuationContributionsToEffectiveInput

**From:** exactly two confirmed [ContinuationInputMapping](domain.md#continuationinputmapping)
records plus their official [Contribution](domain.md#contribution) artifacts
**To:** one target-turn [EffectiveInputArtifact](domain.md#effectiveinputartifact)
**Direction:** internal runtime materialization

| Source | Target | Rule |
|---|---|---|
| reconstruction snapshot | base context entry | exact finalized artifact/hash from the suspended continuation |
| author-turn mapping + official contribution | prior-output history entry | preallocated message, group, operation, seat, round, turn binding, type, dispatch, receipt and completed attempt must match uniquely |
| reviewer-turn mapping + official contribution | review-feedback context entry | preallocated message, group, operation, seat, round, turn binding, type, dispatch, receipt and completed attempt must match uniquely |
| confirmed revision task | final instruction entry | exact versioned task artifact/digest frozen at confirmation |
| mapping order and visibility policies | complete manifest order and policy refs | canonical order is base, author output, review, revision instruction |

The kernel resolves sources from accepted journal facts; no agent or host binding supplies a path or
artifact selector. Finalization occurs only inside
[ResumeAgentContinuation](operations.md#runtime-continuation-input-materialization-contract) or the
corresponding [ReconstructAgentContinuation](operations.md#reconstructagentcontinuation)
transaction, atomically with the target execution unit.
Missing, candidate-only, raw, cross-dispatch, nonterminal, reordered or policy-invalid sources map
to rejection and no authoritative write.

## RevealManifestToEffectiveInput

**From:** [RevealManifest](domain.md#revealmanifest) and authorized message artifacts  
**To:** later [EffectiveInputArtifact](domain.md#effectiveinputartifact)  
**Direction:** internal delivery

Only IDs/hashes frozen by `collection.closed` and authorized by `reveal.published` are resolved. Their
order, schema, authorship, source message IDs and manifest digest are preserved. Closing collection
without a reveal event maps to no peer input. The first proof provides no generic peer-read mapping.

## ReferenceScoutBundleToEffectiveInput

**From:** accepted
[`reference_scout.bundle_committed@1`](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle),
the immutable bundle artifact and the distinct accepted lifecycle fact
[`reference_scout.bundle_delivered@1`](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle)

**To:** [AgentReferenceDelivery](domain.md#agentreferencedelivery), one typed
[EffectiveInputEntry](domain.md#effectiveinputentry) in the target
[EffectiveInputArtifact](domain.md#effectiveinputartifact), and
[`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent)

**Direction:** internal target-agent delivery

**Contract status:** specified for the next bounded slice; not implemented.

**Authority and ownership:** this bounded mapping formalizes
[OQ-ACI8](../discovery/feature-discovery/agents-communication-infra.md#oq-aci8--canonical-effective-input)
under [ACI-R19](rules.md#aci-r19--reference-bundle-delivery-is-source-bound-and-attempt-atomic).
ACI owns the accepted Scout commit/lifecycle facts, target-agent delivery and effective input. The
host alone may later produce source-access observations; APT consumes the independent facts for
declared-use, lineage and claim-support views.

| Source | Target | Transform / rule |
|---|---|---|
| authenticated target capability + target [Attempt](domain.md#attempt) | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`dispatch_id/target_attempt_id/target_seat_id/target_agent_instance_id`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`dispatch_id/target_attempt_id/target_seat_id/target_agent_instance_id` | derive identities; require the same `dispatch_id` on source [ScoutRun](../../agent-provenance-telemetry/probes/reference-scout-tool.md#naming-boundary), delivery and target Attempt |
| accepted [`reference_scout.bundle_committed@1`](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle) | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`scout_run_id/bundle_artifact_id/bundle_digest/recommendation_ids`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`scout_run_id/bundle_artifact_id/bundle_digest/recommendation_ids` | copy source identity and membership/order from this commit fact, then verify all bundle values against the exact immutable bytes |
| immutable bundle artifact | [EffectiveInputEntry](domain.md#effectiveinputentry).`entry_type=reference_bundle/artifact_ref/content_hash`; [AgentReferenceDelivery](domain.md#agentreferencedelivery).`bundle_artifact_id/bundle_digest`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`bundle_artifact_id/bundle_digest` | require `bundle_digest = hash(bundle_bytes)` and preserve artifact identity without rewriting the bundle |
| accepted lifecycle [`reference_scout.bundle_delivered@1`](../../agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md#reference-scout-lifecycle) | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`source_bundle_delivered_event_id`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`source_bundle_delivered_event_id` | copy the lifecycle event identity and require only its `scout_run_id`, artifact and digest to equal the commit/delivery values; this event has no recommendation-membership field |
| command envelope `idempotency_key` | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`idempotency_key`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent) payload and envelope `idempotency_key` | preserve the authenticated scoped retry key exactly |
| stable preallocated delivery identity | [EffectiveInputEntry](domain.md#effectiveinputentry).`agent_reference_delivery_id`; [AgentReferenceDelivery](domain.md#agentreferencedelivery).`agent_reference_delivery_id`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`agent_reference_delivery_id` | use one identity so manifest canonicalization does not depend on a post-commit identifier |
| stable preallocated target-event identity | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`accepted_event_id`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent) envelope `event_id` | assign one identical event identity before canonicalization and commit |
| accepted target-delivery journal append | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`journal_offset`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent) envelope `journal_offset` | record the same authoritative committed offset on both |
| authenticated visibility policy | [EffectiveInputEntry](domain.md#effectiveinputentry).`visibility_policy_ref`; [AgentReferenceDelivery](domain.md#agentreferencedelivery).`visibility_policy_ref`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`visibility_policy_ref` | freeze the same versioned policy reference into all three targets |
| finalized ordered [EffectiveInputArtifact](domain.md#effectiveinputartifact) manifest | [AgentReferenceDelivery](domain.md#agentreferencedelivery).`effective_input_artifact_id/effective_input_entry_ordinal/effective_input_manifest_hash`; target [`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).`effective_input_artifact_id/effective_input_entry_ordinal/effective_input_manifest_hash`; [EffectiveInputEntry](domain.md#effectiveinputentry) at that ordinal | require exactly one matching `entry_type=reference_bundle` entry and preserve its zero-based ordinal |

**Defaults:** none. Missing source facts, identities, policy, artifact bytes, manifest fields or
idempotency evidence fail closed; the mapping never synthesizes a target-agent delivery.

### Validation

| Input condition | Required result |
|---|---|
| Matching accepted commit is absent or differs in ScoutRun, artifact or digest | reject the target-agent delivery and accept no Attempt |
| Committed order/membership differs from immutable bundle bytes, or `bundle_digest != hash(bundle_bytes)` | integrity failure; reject |
| Lifecycle-delivered fact is absent, differs in ScoutRun/artifact/digest, or is treated as carrying `recommendation_ids` | reject; membership remains owned only by commit plus bytes |
| Source ScoutRun, delivery and target Attempt dispatches differ, or capability recipient differs from the Attempt | authorization failure; reject |
| Effective input contains zero, duplicate or mismatched `reference_bundle` entries | validation failure; reject |
| Stable delivery/event identity, scoped idempotency key or any source/recipient/policy/manifest field drifts on retry | conflict; return no new receipt |
| Any member of the [StartAgentAttempt](operations.md#startagentattempt) acceptance unit fails | atomically accept none of the delivery, artifact metadata, request binding, Attempt, events or launch effect intent |

The delivery entity, finalized effective-input metadata, sealed request binding,
`reference_scout.bundle_delivered_to_agent@1`, `attempt.requested` and sandbox-launch effect intent
commit as one [StartAgentAttempt](operations.md#startagentattempt) acceptance unit or none commits.
This mapping establishes delivery, not access, declared use or claim support.

**Checked by:** [T-ACI-R22](../TEST-SPEC.md#t-aci-r22--reference-bundle-target-delivery)
and [T-ACI-ARD1 through T-ACI-ARD5](../TEST-SPEC.md#t-aci-ard1--exact-reference-bundle-delivery).

## FrozenAuthorityToAuditLedgerRow

**From:** [ConfirmedDispatch](domain.md#confirmeddispatch) plus the unique terminal [Run](domain.md#run)
fact  
**To:** canonical audit-ledger schema `0.6.1` opening or close row  
**Direction:** outbound cross-store

Opening identity uses `dispatch_id`; close identity uses `close_of`. Every required row value derives
from frozen spec/authority or accepted terminal facts, including `agents_spawned`. Reconciliation
compares identity and complete canonical content. Identical means already applied; absent invokes the
validated appender and verifies afterward; divergent maps to `reconciliation_required` and releases
neither provider effects nor official closure. This ratifies OQ-ACI5.

## RuntimeTerminalToExitReason

**From:** unique run-level terminal cause  
**To:** audit-ledger `exit_reason`

| Run-level cause | `exit_reason` |
|---|---|
| committed positive, negative or policy-qualified result | `resolved` |
| committed irreconcilable dissent | `dissent_irreconcilable` |
| bounded round/protocol ceiling, including non-technical timeout/no-quorum | `loop_ceiling_reached` |
| explicit human cancellation | `user_abort` |
| exhausted provider retries, corruption, resource/budget exhaustion preventing outcome, other technical prevention | `error` |

Attempt/group terminal facts never map directly. A partial result is `resolved` only when policy
explicitly commits it as the qualified result.

## UsageObservationToRollups

**From:** immutable [UsageObservation](events.md#usageobserved)  
**To:** rebuildable usage rollups

| Rollup level | Key | Semantics |
|---|---|---|
| attempt | `attempt_id` | provider-reported records for one physical execution/exchange |
| operation | `operation_id` | all retries retained; accepted-attempt subset separately labeled |
| seat | `seat_id` | physical usage attributable to one logical participant |
| group | group aggregate identity | all attributable seat/adapter observations |
| run | `run_id` | all groups/effects in one immutable run |
| dispatch | `dispatch_id` | compatibility 1:1 today; remains distinct dimension |

Aggregation preserves provider/model, counter semantic/version and nullability. Missing is not zero.
Costs are calculated only with an explicit immutable pricing source/version and currency; otherwise
cost remains unknown. These rollups are projections and never billing truth. OQ-ACI10 remains an
empirical adapter-completeness gate.

## Candidate SQLite Logical Table Boundary

The W0 persistence ADR may normalize/merge projection tables but MUST preserve these authorities and
constraints.

| Logical table | Authority | Minimum columns / constraint |
|---|---|---|
| `command_receipts` | authoritative dedupe | command ID, scoped idempotency key, command digest, status, stable receipt; unique scoped key |
| `events` | authoritative journal | global integer offset, event ID/type/schema, aggregate ID/version, causation/correlation, payload ref/hash; unique event ID and aggregate version |
| `aggregate_heads` | authoritative CAS | aggregate ID, current contiguous version, state hash |
| `effect_intents` | authoritative outbox | effect ID/type, payload digest, retry class, claim epoch, status/outcome; unique effect ID |
| `artifacts` | authoritative metadata | artifact ID, content hash, media/schema type, classification, size, storage ref |
| `attempts` | rebuildable projection | operation/attempt/agent/provider/adapter/model identities, canonical lifecycle status |
| `publication_candidates` | authoritative logical reservation | candidate ID/status, attempt/operation/logical key, candidate event, payload ref/hash, idempotency key, CAS version, accepted/abandoned event; unique candidate identity and at most one active reservation per logical key |
| `messages` | rebuildable constrained projection | logical key, seat/round/type, official accepted event, source candidate event, payload ref/hash, visibility; unique logical key |
| `publication_receipts` | rebuildable projection | receipt version/status/event/message/offset/payload hash/idempotency key/canonical receipt bytes and digest; transport replay metadata is not persisted in the receipt |
| `reveal_manifests` | rebuildable constrained projection | group/version/round, manifest digest, frozen message IDs/hashes, reveal event |
| `usage_observations` | immutable event projection | source event, attempt/provider/model, nullable counters, semantic/version and pricing ref |
| `runtime_projections` | disposable read model | projection key, source cursor, state payload/hash |

`command_receipts`, appended `events`, updated `aggregate_heads` and newly requested
`effect_intents` commit in one SQLite transaction. Audit-ledger rows remain outside this database and
become acknowledged facts only after exact verification through
[AuditLedgerMaterializer](workflows.md#auditledgermaterializer).

## Mapping Validation Matrix

| Failure | Required result |
|---|---|
| provider-specific field would control kernel transition | reject mapping/spec combination |
| authority field arrives from agent payload | reject and audit |
| reveal message absent from manifest | deny delivery |
| target-agent bundle has no preceding matching commit and lifecycle-delivery facts | reject target-agent delivery |
| source ordering is not `bundle_committed.journal_offset < bundle_delivered.journal_offset < bundle_delivered_to_agent.journal_offset` | reject target-agent delivery |
| commit membership/order differs from immutable bundle bytes | reject target-agent delivery |
| ScoutRun, delivery and target Attempt do not share one dispatch | reject target-agent delivery |
| effective input has zero, duplicate or mismatched `reference_bundle` entries | reject target-agent delivery |
| receipt field differs from persisted event | reject official contribution |
| candidate exists but parent verification/terminalization was interrupted | recover by attempt/operation/logical key; append official pair at most once |
| provider pair is not `protocol_equivalent` | reject adapter/capability combination |
| sandbox policy or authority fence cannot be enforced | reject start effect; preserve Slice-1 blocker |
| ledger identity matches but canonical row differs | `reconciliation_required` |
| usage dimension absent | preserve `null`; do not synthesize zero/cost |
| artifact bytes/hash/type mismatch | reject reference; no authoritative event may cite incomplete payload |
