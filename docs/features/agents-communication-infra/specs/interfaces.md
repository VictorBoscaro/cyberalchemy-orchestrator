---
id: agents-communication-infra
feature: Agents Communication Infra
type: interfaces
title: "Agents Communication Infra — Interfaces"
status: draft
version: 0.3.0
derived-from: ../discovery/feature-discovery/agents-communication-infra.md@0.2.1
---

# Interfaces: Agents Communication Infra

These boundaries preserve one deterministic protocol while allowing command clients, providers and
models to vary. Runtime authority is always derived from authenticated context and accepted journal
facts; no request body, provider output or projection can grant itself authority.

## Capability Backlinks

- [Provider-neutral agent execution](SPEC.md#provider-neutral-agent-execution)
- [Receipt-gated deliberation](SPEC.md#receipt-gated-deliberation)
- [Recoverable runtime authority](SPEC.md#recoverable-runtime-authority)
- [Operator projection and usage accountability](SPEC.md#operator-projection-and-usage-accountability)

## External: Runtime Command API (HTTP or equivalent command transport)

The command transport is replaceable. The semantics below are owned by the operations and journal,
not by HTTP status codes.

### POST /dispatches/{dispatch_id}/confirm

**Exposes:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch)  
**Auth:** authenticated human/operator principal authorized to confirm the exact draft digest.

**Request**

| Field | Type | Maps To |
|---|---|---|
| `dispatch_id` | opaque ID | [ConfirmedDispatch](domain.md#confirmeddispatch).dispatch_id |
| `pending_sheet_ref` | artifact/file reference | [ConfirmedDispatch](domain.md#confirmeddispatch).source_bytes_artifact_id |
| `pending_sheet_digest` | SHA-256 digest | [ConfirmedDispatch](domain.md#confirmeddispatch).digest |
| `execution_authority_mode` | [ExecutionAuthorityMode](domain.md#executionauthoritymode) | Pre-confirmation routing choice; only `runtime-managed` maps to [ConfirmedDispatch](domain.md#confirmeddispatch).authority_mode, while `legacy-managed` preserves the legacy/session path and is rejected by this endpoint. |
| `idempotency_key` | non-empty string | [RuntimeCommand](domain.md#runtimecommand).idempotency_key |
| `expected_version` | non-negative integer or `null` for creation | [RuntimeCommand](domain.md#runtimecommand).expected_version |

The command service resolves this transport shape into the complete
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch) input before command acceptance. The
resolution is part of the authenticated command boundary, not client-supplied runtime authority:

| Resolved operation input | Server-side resolution contract |
|---|---|
| `pending_sheet_bytes` | Read `pending_sheet_ref` once, verify `pending_sheet_digest` against the exact bytes, finalize those bytes through [ArtifactBoundary](#internal-artifact-boundary), and bind the resulting artifact ID to `ConfirmedDispatch.source_bytes_artifact_id`. |
| `dispatch_id` | Use the authenticated path/body identity only after exact equality and authorization checks. |
| `execution_authority_mode` | Validate the submitted pre-confirmation choice against the current cutover state. `legacy-managed` returns the operation's typed rejection and preserves the legacy/session path without creating `ConfirmedDispatch` or `Run`; only `runtime-managed` is compiled into `ConfirmRuntimeDispatch`. |
| `dispatch_spec_ref`, `dispatch_spec_digest` | Compile the exact verified pending bytes with the operator-selected profile, finalize the immutable [DispatchSpec](domain.md#dispatchspec), and verify its digest before acceptance. |
| `schema_versions` | Resolve the complete command, event, recipe/profile and payload-schema version set referenced by the finalized dispatch spec; any missing or mutable version rejects confirmation. |
| `capability_resolution_ref` | Resolve adapter/model/tool capabilities against the finalized dispatch spec, persist the immutable resolution artifact and reject any semantics-changing mismatch. |
| command envelope | Bind `idempotency_key`, `expected_version`, authenticated principal, causation and correlation to the [RuntimeCommand](domain.md#runtimecommand); none are inferred from pending-sheet content. |

Failure to read, hash, compile, finalize or resolve any row above returns `422` and creates no
`ConfirmedDispatch`, run, journal fact or audit effect. A `legacy-managed` routing choice has this
same effect and preserves the legacy/session path. The server does not reread the mutable source
after acceptance.

**Responses**

| Status | Condition | Body |
|---|---|---|
| `202` | command transaction committed | stable command receipt, [Run](domain.md#run).run_id, [JournalOffset](domain.md#journaloffset) |
| `200` | identical idempotent replay | the original stable command receipt |
| `409` | key reused with another digest, stale aggregate version or authority mode already assigned | stable error code and current version where disclosure is authorized |
| `422` | draft, digest, schema or confirmation authority invalid, including `legacy-managed` routing | rule violations; no `ConfirmedDispatch`, run, journal fact or audit effect created |

The response confirms journal acceptance, not audit-ledger opening. Provider/tool work remains
blocked until the [AuditLedgerMaterializer](workflows.md#auditledgermaterializer) records verified
opening.

### POST /runs/{run_id}/commands

**Exposes:** [AcceptRuntimeCommand](operations.md#acceptruntimecommand)  
**Auth:** authenticated operator, policy reactor or runtime worker principal with command-specific
scope.

| Field | Type | Maps To |
|---|---|---|
| `command_id` | opaque ID | [RuntimeCommand](domain.md#runtimecommand).command_id |
| `command_type` | versioned allowlisted type | [RuntimeCommand](domain.md#runtimecommand).command_type |
| `idempotency_key` | non-empty string | [RuntimeCommand](domain.md#runtimecommand).idempotency_key |
| `expected_aggregate_version` | integer | [AggregateVersion](domain.md#aggregateversion) |
| `prerequisite_heads` | array of aggregate/version/state-hash triples | [RuntimeCommand](domain.md#runtimecommand).prerequisite_heads |
| `payload` or `payload_ref` | schema-valid object or artifact reference | [RuntimeCommand](domain.md#runtimecommand).payload_ref |
| `causation_id`, `correlation_id` | opaque IDs | [RuntimeCommand](domain.md#runtimecommand) causation/correlation fields |

The runtime derives `actor_principal_id`, dispatch/run scope and allowed aggregate from the
authenticated capability. Conflicting authority fields in the payload are rejected.

### POST /runs/{run_id}/cancel

**Exposes:** [CancelRun](operations.md#cancelrun)  
**Auth:** authenticated operator with cancel authority bound to the current confirmed run.

Cancellation acceptance, adapter acknowledgement and terminalization are distinct accepted facts.
An accepted request returns a command receipt; it does not claim that active attempts have stopped.

### GET /runs/{run_id}

**Exposes:** [GetRunStatus](queries.md#getrunstatus)  
**Auth:** runtime operator or authorized observer.

Returns a [RuntimeProjection](queries.md#getruntimeprojection) plus its source
[JournalOffset](domain.md#journaloffset). It never reads provider state to manufacture a lifecycle
transition.

### GET /runs/{run_id}/stream?after={journal_offset}

**Exposes:** [GetRuntimeProjection](queries.md#getruntimeprojection)  
**Auth:** runtime operator or authorized observer; redaction is identical to point queries.

| Outcome | Meaning |
|---|---|
| snapshot + cursor | consistent initial [RuntimeProjection](queries.md#getruntimeprojection) |
| ordered event | next authorized projection delta after the cursor |
| heartbeat | transport liveness only; never a domain fact |
| gap/expired cursor | client must request a new consistent snapshot |

## External: Agent Tool Gateway (MCP or equivalent)

An attempt receives a short-lived, audience-bound capability. During sealed collection, its
surface contains `bus_publish` and the declared non-peer tools only; it contains no list, search,
read, export or debug method for peer contributions.

### bus_publish

**Exposes:** [PublishBusContribution](operations.md#publishbuscontribution)  
**Auth:** capability scoped to `(run, group_version, seat, agent_instance, attempt, operation,
action, phase)` and revalidated against current journal state on every call.

**Agent-authored request**

| Field | Type | Required | Validation |
|---|---|---:|---|
| `idempotency_key` | non-empty string | yes | scoped uniqueness; identical digest replays, different digest conflicts |
| `operation_id` | opaque ID | yes | must match the sealed [AgentExecutionRequest](domain.md#agentexecutionrequest).operation_id |
| `round_id` | opaque ID | yes | must be active and allowed by the capability |
| `message_type` | schema-qualified allowlist value | yes | allowed by current group phase |
| `reply_to_message_ids` | message ID array | no | every ID must already be visible to this principal |
| `payload` or `payload_ref` | typed object or artifact reference | yes | schema, classification, hash and size checks pass |

The agent MUST NOT supply `dispatch_id`, `run_id`, `group_id`, `group_version`, `seat_id`,
`agent_instance_id`, `attempt_id`, `actor_principal_id` or `phase`. If any appears in the authored
payload as an authority claim, the gateway rejects the request rather than ignoring the conflict.

**Response: [PublicationReceipt](domain.md#publicationreceipt)**

| Field | Meaning |
|---|---|
| `receipt_version` | supported canonical receipt schema version |
| `status` | exactly `persisted_candidate`; does not claim official acceptance |
| `event_id` | committed `publication.persisted` [RuntimeEventEnvelope](domain.md#runtimeeventenvelope) identity |
| `message_id` | durable [PublicationCandidate](domain.md#publicationcandidate) identity |
| `journal_offset` | committed [JournalOffset](domain.md#journaloffset) |
| `payload_hash` | digest of the accepted canonical payload |
| `idempotency_key` | scoped key supplied by the agent |

A receipt is returned only after append commit. It is evidence to be independently checked by
[VerifyPublicationReceipt](operations.md#verifypublicationreceipt), not self-authenticating proof.
An outer transport envelope may add `transport_replayed`; it is never part of the canonical,
byte-stable `PublicationReceipt`.

## Internal: EventJournal

**Concept:** [EventJournal](#internal-eventjournal)  
**Consumers:** command service, protocol kernel, outbox workers, receipt verifier, projection reducers
and reconcilers.

| Method | Input | Output | Contract |
|---|---|---|---|
| `acceptCommand` | [RuntimeCommand](domain.md#runtimecommand), expected [AggregateVersion](domain.md#aggregateversion) | stable command receipt and committed event range | the sole public write path; compares idempotency digest, target CAS and prerequisite heads before atomically committing events, head changes and new effects |
| `verifyPublicationReceipt` | [PublicationReceipt](domain.md#publicationreceipt), authenticated parent/worker context | verified accepted event or rejection | all receipt fields and logical scope must match persisted facts |
| `readStream` | aggregate ID or global cursor | ordered [RuntimeEventEnvelope](domain.md#runtimeeventenvelope) records | never invokes commands, providers, tools or materializers |
| `claimEffect` | effect identity, worker epoch, expected status | claimed [EffectIntent](domain.md#effectintent) | single-host CAS; stale epochs cannot complete |
| `recordEffectObservation` | effect outcome observation, expected claim epoch and outcome digest | committed event/next intent | atomically updates effect status/epoch/outcome event with command receipt and aggregate event/head; unknown remains explicit |

Only the controlled journal writer performs physical writes. Logical publishers call command or bus
interfaces; they never receive a database connection.

## Internal: AgentAdapter

**Concept:** [AgentAdapter](#internal-agentadapter)  
**Consumers:** effect worker and scheduler.

| Method | Input | Output | Required semantics |
|---|---|---|---|
| `materialize` | [AgentInvocationPlan](domain.md#agentinvocationplan) | [MaterializedAgentInvocation](domain.md#materializedagentinvocation) plus prepared effective-input bytes/metadata | deterministic native translation and canonical input preparation; no artifact, delivery or Attempt acceptance |
| `start` | sealed [AgentExecutionRequest](domain.md#agentexecutionrequest) | provider attempt identity/status observation | invoked only through SandboxLauncher; adapter cannot write state |
| `events` | [Attempt](domain.md#attempt).attempt_id, provider cursor | canonical incremental observations + next cursor | provider-native payload stays namespaced and content-addressed |
| `result` | [Attempt](domain.md#attempt).attempt_id | [AgentTerminalResult](domain.md#agentterminalresult) | common version/parsing rules; provider prose alone never becomes a contribution |
| `cancel` | [Attempt](domain.md#attempt).attempt_id, command ID | cancellation observation | idempotent request; acknowledgement is distinct from terminal state |
| `status` | [Attempt](domain.md#attempt).attempt_id | canonical reconciliation observation | used after restart/unknown effect; must not invent completion |
| `capabilities` | adapter identity/digest | versioned capability declaration | classifies features as required, semantics-preserving emulation or semantics-changing |

### Invocation materialization and sealed request contract

The runtime creates one provider-neutral [AgentInvocationPlan](domain.md#agentinvocationplan) per
physical attempt. The selected adapter translates it to
[MaterializedAgentInvocation](domain.md#materializedagentinvocation) and prepares the canonical bytes
and metadata for the exact [EffectiveInputArtifact](domain.md#effectiveinputartifact). The kernel
validates both digests and, during [StartAgentAttempt](operations.md#startagentattempt), atomically
finalizes artifact metadata, accepts any [AgentReferenceDelivery](domain.md#agentreferencedelivery),
binds the sealed [AgentExecutionRequest](domain.md#agentexecutionrequest), accepts the Attempt and
commits `attempt.requested`; only a later claimed effect may ask the launcher to start it.

When an authorized Reference Scout bundle is included, the kernel preallocates the
[AgentReferenceDelivery](domain.md#agentreferencedelivery) identity and target-event identity and supplies
an immutable binding to the materializer. The adapter may place the exact authorized bundle only as
one typed `reference_bundle` entry; it cannot select the source ScoutRun, target identities,
recommendation membership/order or visibility policy. After materialization, the kernel verifies
the binding through
[ReferenceScoutBundleToEffectiveInput](mappings.md#referencescoutbundletoeffectiveinput) and accepts
the delivery only in the complete [StartAgentAttempt](operations.md#startagentattempt) transaction.
This boundary is specified for the next bounded slice and is not implemented.

| Field | Authority | Contract |
|---|---|---|
| `attempt_id`, `dispatch_id`, `operation_id`, `seat_id`, `agent_instance_id` | runtime | authenticated physical/logical identities |
| `provider_ref`, `adapter_ref`, `model_ref` | confirmed spec + scheduler | exact resolved destination and immutable version/digest where available |
| `role_contract_ref`, `task_ref` | compiled recipe/profile | local objective, visible inputs and allowed output type |
| `base_snapshot_ref` | runtime | content-addressed shared context |
| `role_delta_ref` | confirmed role contract | optional, content-addressed declared difference from the base snapshot |
| `agent_reference_delivery_id`, source Scout bundle ref/digest, target-event ID, `visibility_policy_ref` | kernel + authenticated target capability | optional preallocated immutable binding; when present it must yield exactly one matching `reference_bundle` entry and cannot be rewritten by the adapter |
| `effective_input_ref`, `provider_invocation_ref` | adapter materializer | ordered observable input and exact native invocation artifacts |
| `response_schema_ref` | confirmed spec | schema required before a raw result can become a publication candidate |
| `tool_profile_ref` | capability resolver | exact tools and permissions; collection has no peer-read capability |
| `deadline`, `resource_budget` | confirmed policy | explicit time, token, tool, payload and storage bounds |
| `sandbox_policy` | confirmed policy | filesystem/network/process/credential allowlists, default-deny elsewhere |
| `authority_fence` | cutover verifier | current runtime epoch and verified legacy-watcher-disable evidence |
| optional Reference Scout delivery context | runtime scheduler under authenticated delivery capability | preallocated delivery/event identities plus accepted source commit, lifecycle-delivery fact, immutable bundle and policy; source ScoutRun and target Attempt must share `dispatch_id`, and the adapter cannot author or accept any delivery field |

When the optional delivery context is present, the prepared manifest contains exactly one
[`reference_bundle`](domain.md#effectiveinputentry) entry produced by
[ReferenceScoutBundleToEffectiveInput](mappings.md#referencescoutbundletoeffectiveinput). The
capability-derived recipient, accepted source facts and immutable bytes are revalidated inside the
atomic StartAgentAttempt acceptance unit. No standalone endpoint or adapter method accepts
[`reference_scout.bundle_delivered_to_agent@1`](events.md#referencescoutbundledeliveredtoagent).

### Heterogeneous-provider conformance

Provider, adapter and model are resolved per `agent_instance_id`, not per run or group. Codex,
Claude and future adapters MAY occupy seats in one group when each satisfies the same frozen
capability profile. They MUST satisfy `protocol_equivalent(plan, materialized invocation, sealed
request, terminal result, events, states, decision result)` under that profile. Codex and Claude
native terminals are parsed with the same versioned [AgentTerminalResult](domain.md#agentterminalresult)
rules and emit the same canonical attempt and [UsageObservation](events.md#usageobserved) shapes. Provider-specific flags and
metadata remain namespaced in the [EffectiveInputArtifact](domain.md#effectiveinputartifact) or
[RawProviderOutput](domain.md#rawprovideroutput); the kernel, bus schemas and decision rule MUST NOT
branch on provider/model names.

## Provider Implementation and Admission Boundary

The first real provider implementation is repository-local Python integration that invokes a CLI
subprocess only through [SandboxLauncher](#internal-sandboxlauncher). Pydantic core validates the
decoded common request/result/receipt/event models; runtime-owned canonical projection and sealing
remain outside adapter and Pydantic serialization defaults.

Before registration as runnable, every real adapter must satisfy
[ProviderAdapterAdmissionGate](rules.md#aci-r18--provider-adapter-admission-gate) on its target host.
It receives no journal or audit-ledger writer and returns observations only. Octopus Runtime and Eve
are not kernel dependencies. PydanticAI is not part of this subprocess boundary and may enter only
as a future direct-API adapter behind the same interface and evidence gate.

A Node transport may validate a derived view with Zod only after it is inventoried as an ACI
consumer and shared Python-authority vectors pass. No current Node component is admitted on that
basis.

## Internal: DeliberationBus

**Concept:** [DeliberationBus](#internal-deliberationbus)  
**Consumers:** authenticated agent gateway, protocol kernel and reveal-delivery worker.

| Method | Input | Output | Contract |
|---|---|---|---|
| `publish` | agent-authored [BusPublication](domain.md#buspublication) + authenticated capability context | [PublicationReceipt](domain.md#publicationreceipt) | derives all authority fields and appends before acknowledgement |
| `closeCollection` | authorized command + expected aggregate version/prerequisite heads | accepted `collection.closed` event | counts only receipt-verified official acceptances; does not grant peer-read |
| `publishReveal` | frozen [RevealManifest](domain.md#revealmanifest) + expected version | accepted `reveal.published` event | manifest IDs/hashes exactly match the frozen eligible set |
| `authorizeInvocationPlan` | capability action `bus.plan`, phase `plan`, plus binding and complete [AgentInvocationPlan](domain.md#agentinvocationplan) | immutable `plan_ref` and `plan_digest` | derives target/group/provider/adapter from the running binding and rejects every caller substitution before write |
| `materializeRevealInput` | authorized attempt/turn + reveal manifest | content-addressed input artifact | delivered messages appear in that turn's [EffectiveInputArtifact](domain.md#effectiveinputartifact) |

The initial proof deliberately has no generic peer-read method. [GetVisibleGroupMessages](queries.md#getvisiblegroupmessages)
is an internal authorized query used by projection/reveal materialization and is not placed in an
agent capability during `collect`.

## Internal: SandboxLauncher

**Consumers:** provider-start effect worker only.

| Method | Input | Output | Contract |
|---|---|---|---|
| `validatePolicy` | [SandboxPolicy](domain.md#sandboxpolicy), host capabilities | validation result | fail closed if required filesystem/network/process/credential isolation cannot be enforced |
| `launch` | sealed [AgentExecutionRequest](domain.md#agentexecutionrequest), current [ExecutionAuthorityFence](domain.md#executionauthorityfence) | provider process/attempt observation | verifies request digest, fence epoch and policy before process creation; never writes journal state |
| `terminate` | attempt/process identity, authorized cancel command | termination observation | idempotent and evidence-producing; acknowledgement is not terminal state |

`OQ-SANDBOX` remains a real-provider admission blocker: no S-003/L2/W3 exit is allowed until
launcher isolation and negative escape fixtures pass on the target host. Fake-adapter Slice 1 work
does not claim or require this real-provider evidence.

## Internal: Audit Ledger Appender Port

**Consumers:** [AuditLedgerMaterializer](workflows.md#auditledgermaterializer) only.

| Method | Input | Output | Contract |
|---|---|---|---|
| `readByIdentity` | `dispatch_id` or `close_of` | absent, identical candidate row or existing divergent row | tolerant read for reconciliation; never mutates history |
| `appendValidatedRow` | canonical schema `0.6.1` row | physical row reference | invokes the existing validated appender; no alternate ledger writer |
| `verifyExactRow` | frozen-authority-derived canonical row | identical, absent or divergent | field-for-field canonical comparison, not identity-only equality |

The journal and YAML audit ledger do not share a transaction. Opening is a release barrier and close
is official only after exact-row verification is recorded back through the journal.

## Internal: Artifact Boundary

**Consumers:** adapters, bus, journal and reveal materializer.

| Method | Input | Output | Contract |
|---|---|---|---|
| `commitArtifact` | bytes, media/schema type, classification | immutable artifact ID and content hash | validates size/hash/type before an event may reference it |
| `getAuthorized` | artifact ID + authenticated principal/action/phase | bytes or denial | applies the same sealing/redaction policy as API/SSE |
| `tombstonePayload` | retention/crypto-erasure authority | tombstone retaining allowed provenance | cannot rewrite the originating event or claim payload availability |

Effective inputs and raw outputs are sensitive immutable artifacts. Concrete retention periods,
key management and post-local-development encryption remain deferred under OQ-ACI9 and must be
settled before Slice 1 exits.

## Interface Invariants

| ID | Invariant | Formal constraint |
|---|---|---|
| IF-ACI-01 | Append before acknowledgement | `PublicationReceipt returned -> matching accepted event committed` |
| IF-ACI-02 | Parent-side receipt gate | `official contribution -> VerifyPublicationReceipt = verified` |
| IF-ACI-03 | Authority is derived | `agent payload authority fields = empty` and effective authority comes from authenticated context |
| IF-ACI-04 | Collection stays sealed | `phase=collect and requester.seat != owner.seat -> peer payload denied on every controlled interface` |
| IF-ACI-05 | Reveal is manifest-bound | `peer message delivered -> message_id/hash in persisted RevealManifest and reveal.published accepted` |
| IF-ACI-06 | Provider neutrality | equal capability profile implies equal canonical protocol/interface shapes regardless of provider/model |
| IF-ACI-07 | Projection is non-authoritative | query/stream response cannot create a runtime transition |
| IF-ACI-08 | One physical writer per authoritative store | logical publisher never obtains journal/audit-ledger write access |
| IF-ACI-09 | Adapter is translation/observation only | adapter response becomes command input and never directly mutates state |
| IF-ACI-10 | Start is fenced and sandboxed | `providerProcessCreated -> sandboxPolicyEnforced and authorityFenceCurrent` |
| IF-ACI-11 | Candidate is not official | `publication.persisted and not verified -> not quorumEligible` |
| IF-ACI-12 | Adapter admission is evidence-gated | `real provider runnable -> ProviderAdapterAdmissionGate passed for adapter version and target host` |
| IF-ACI-13 | Boundary validation is subordinate | language-native boundary schema cannot define canonical bytes, digest or acceptance identity |
| IF-ACI-14 | Target-agent reference delivery is kernel-authorized and atomic | `reference_bundle in accepted input -> authenticatedDeliveryCapability and preallocated(delivery_id,target_event_id) and exactAcceptedSourceBinding and atomic(AgentReferenceDelivery,finalizedEffectiveInputMetadata,sealedRequestBinding,Attempt,reference_scout.bundle_delivered_to_agent@1,attempt.requested,launchEffectIntent)` |

## Deferred Interface Decisions

- OQ-ACI9: concrete redaction, encryption, access escalation, retention and key-destruction periods.
- OQ-ACI10: empirical completeness of provider usage across tool-heavy, resumed, multi-turn and
  retried executions. Missing dimensions remain `null` until proven.
- Distributed leases, multi-host writers and a generic agent peer-read API are outside the current
  single-host W0 contract.
