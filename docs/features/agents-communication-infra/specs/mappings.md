---
id: agents-communication-infra
feature: Agents Communication Infra
type: mappings
title: "Agents Communication Infra — Mappings"
status: draft
version: 0.1.0
derived-from: ../discovery/feature-discovery/agents-communication-infra.md@0.2.1
---

# Mappings: Agents Communication Infra

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

## RevealManifestToEffectiveInput

**From:** [RevealManifest](domain.md#revealmanifest) and authorized message artifacts  
**To:** later [EffectiveInputArtifact](domain.md#effectiveinputartifact)  
**Direction:** internal delivery

Only IDs/hashes frozen by `collection.closed` and authorized by `reveal.published` are resolved. Their
order, schema, authorship, source message IDs and manifest digest are preserved. Closing collection
without a reveal event maps to no peer input. The first proof provides no generic peer-read mapping.

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
| receipt field differs from persisted event | reject official contribution |
| candidate exists but parent verification/terminalization was interrupted | recover by attempt/operation/logical key; append official pair at most once |
| provider pair is not `protocol_equivalent` | reject adapter/capability combination |
| sandbox policy or authority fence cannot be enforced | reject start effect; preserve Slice-1 blocker |
| ledger identity matches but canonical row differs | `reconciliation_required` |
| usage dimension absent | preserve `null`; do not synthesize zero/cost |
| artifact bytes/hash/type mismatch | reject reference; no authoritative event may cite incomplete payload |
