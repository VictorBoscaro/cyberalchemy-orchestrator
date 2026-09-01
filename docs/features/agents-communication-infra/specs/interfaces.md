---
id: agents-communication-infra
feature: Agents Communication Infra
type: interfaces
title: "Agents Communication Infra — Interfaces"
status: draft
version: 0.5.1
last_updated: 2026-09-01
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

## External dependency: Trusted confirmation observation issuer

The admitted chat host, and a future UI host, are external evidence issuers rather than ACI state
writers. Each exact versioned issuer integration:

| Receives | Produces | Required boundary behavior |
|---|---|---|
| Effect-free server presentation containing `dispatch_id`, `dispatch_revision`, `pending_sheet_digest` and `dispatch_spec_digest` | Canonical [ConfirmationObservation](domain.md#confirmationobservation) artifact/evidence | Derive principal, channel, issuer reference and evidence from authenticated host context; never copy those authority fields from user-authored message content. |

The observation tuple and both displayed digests must equal the tuple later revalidated by
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch). Any difference rejects. Issuer
admission is an exact versioned configuration check; v1 does not claim cryptographic attestation,
an expiry policy or a general presentation-lifecycle protocol.

## External: Runtime Command API (HTTP or equivalent command transport)

The command transport is replaceable. The semantics below are owned by the operations and journal,
not by HTTP status codes.

### POST /dispatches/{dispatch_id}/confirm

**Exposes:** [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch)  
**Auth:** authenticated human/operator principal authorized to confirm the exact presented dispatch
revision and both displayed digests.

Before this request, a trusted
[confirmation-observation issuer](#external-dependency-trusted-confirmation-observation-issuer)
must ask the runtime command boundary to resolve one authenticated server-known pending revision,
read its bytes and build an effect-free preview. The issuer presents exactly one
`dispatch_id`/revision plus the resulting `pending_sheet_digest` and `dispatch_spec_digest`, observes
the human decision, and finalizes a canonical [ConfirmationObservation](domain.md#confirmationobservation).
Chat and a future UI use this same sequence and differ only in admitted issuer/channel evidence.

**Request**

| Field | Type | Maps To |
|---|---|---|
| `dispatch_id` | opaque ID | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`dispatch_id` |
| `dispatch_revision` | non-empty string | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`dispatch_revision` |
| `pending_revision_selector` | authenticated server-known selector | Resolves once to [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`pending_sheet_bytes`; it is not an arbitrary path or artifact authority. |
| `pending_sheet_digest` | [ContentDigest](domain.md#contentdigest) | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`pending_sheet_digest` |
| `confirmation_observation_ref` | [ArtifactId](domain.md#artifactid) | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`confirmation_observation_ref` |
| `confirmation_observation_digest` | [ContentDigest](domain.md#contentdigest) | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`confirmation_observation_digest` |
| `execution_authority_mode` | [ExecutionAuthorityMode](domain.md#executionauthoritymode) | [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch).`execution_authority_mode`; must equal the finalized pending source and current cutover choice. |
| `idempotency_key` | non-empty string | Common command input `idempotency_key` in [operations.md](operations.md#common-command-contract). |
| `expected_aggregate_version` | integer `0` for creation | Common command input `expected_aggregate_version` in [operations.md](operations.md#common-command-contract). |

The command service resolves this transport shape into the complete
[ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch) input before command acceptance. The
resolution is part of the authenticated command boundary, not client-supplied runtime authority:

| Resolved operation input | Server-side resolution contract |
|---|---|
| `pending_sheet_bytes`, `pending_sheet_digest` | Authorize `pending_revision_selector` within the server-owned pending namespace, resolve its exact dispatch/revision, read it once, verify the submitted digest against those bytes, finalize them through [ArtifactBoundary](#internal-artifact-boundary), and bind the resulting artifact ID/digest. A client path, traversal, alias to another revision or mutable locator outside that namespace rejects. |
| `dispatch_id`, `dispatch_revision` | Use the authenticated path/body identity only after exact equality with the finalized source and verified observation. |
| `execution_authority_mode` | Require `request mode = finalized pending mode = current cutover choice = runtime-managed`. Any mismatch rejects before compilation; `legacy-managed` preserves the legacy/session path without creating `ConfirmedDispatch` or `Run`. |
| `confirmation_observation_ref`, `confirmation_observation_digest` | Dereference and validate the closed canonical observation; verify exact issuer/evidence, authenticated human, channel, action, time, dispatch/revision and both displayed digests. Request-body copies cannot satisfy this step. |
| `dispatch_spec_ref`, `dispatch_spec_digest` | Recompile the exact verified pending bytes with server-side resolution, finalize the immutable [DispatchSpec](domain.md#dispatchspec), and require byte/digest equality with the trusted preview and observation. A caller-supplied expanded spec or effective grant is rejected. |
| `schema_versions` | Resolve the complete command, event, recipe/profile and payload-schema version set referenced by the finalized dispatch spec; any missing or mutable version rejects confirmation. |
| `capability_resolution_ref`, `capability_resolution_digest` | Resolve adapter/model/tool capabilities server-side, persist the immutable resolution artifact and require equality with the trusted preview; reject any semantics-changing mismatch. |
| confirmed graph, mappings and IDs | Derive the exact bounded graph, mapping set and every ID through [Runtime Confirmation Authority v1](confirmation-authority.md); reject client-supplied values. |
| command envelope | Derive `aggregate_id=run_id`, require creation version `0`, and bind `idempotency_key`, authenticated principal, causation and correlation to the [RuntimeCommand](domain.md#runtimecommand); none are inferred from pending-sheet content. |

Failure to read, hash, compile, finalize or resolve any row above returns `422` and creates no
`ConfirmedDispatch`, run, journal fact or audit effect. A `legacy-managed` routing choice has this
same effect and preserves the legacy/session path. The server does not reread the mutable source
after acceptance.

**Responses**

| Status | Condition | Body |
|---|---|---|
| `202` | command transaction committed | first stable command receipt, [Run](domain.md#run).run_id, `confirmed_authority_digest`, [JournalOffset](domain.md#journaloffset) |
| `200` | identical key replay or new-key identity replay | the byte-identical first stable command receipt |
| `409` | key reused with another command digest | `idempotency_conflict`; original receipt/unit is preserved |
| `409` | existing dispatch has another `confirmed_authority_digest` | `confirmed_authority_conflict`; original receipt/unit is preserved |
| `409` | creation CAS or prerequisite head loses the race | `aggregate_version_conflict` or `prerequisite_head_conflict`; current version is disclosed only when authorized |
| `422` | `legacy-managed` routing reaches this runtime endpoint | `legacy_authority_mode`; legacy path is preserved |
| `422` | issuer/evidence or observation fields are not trusted | `untrusted_confirmation_issuer` or `untrusted_confirmation_observation` |
| `422` | observation dispatch/revision scope differs | `confirmation_observation_scope_mismatch` |
| `422` | pending or compiled/presented spec digest differs | `pending_sheet_digest_mismatch` or `dispatch_spec_digest_mismatch` |
| `422` | bounded graph, mapping projection or a derived ID differs | `invalid_bounded_graph`, `confirmation_projection_mismatch` or `derived_identity_mismatch` |
| `422` | identity-derivation contract or payload-schema bundle differs | `identity_derivation_mismatch` or `confirmation_payload_schema_mismatch` |
| `422` | confirmation attempts a forbidden materialization/effect | `forbidden_effect_boundary` |

Every `422` code above is pinned by the normative
[confirmation negative vectors](fixtures/confirmed-dispatch-v1/negative-vectors.json) and creates no
[ConfirmedDispatch](domain.md#confirmeddispatch), [Run](domain.md#run), journal fact or audit effect.

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
| `acceptConfirmedDispatch` | [RuntimeCommand](domain.md#runtimecommand), closed confirmation acceptance batch | first stable confirmation receipt and the two committed event identities | sole-writer persistence specialization for [ConfirmRuntimeDispatch](operations.md#confirmruntimedispatch); inside one `BEGIN IMMEDIATE`, evaluates key replay/conflict first, then `(dispatch_id, confirmed_authority_digest)` replay/conflict, validates the complete batch and commits it all-or-none |
| `verifyPublicationReceipt` | [PublicationReceipt](domain.md#publicationreceipt), authenticated parent/worker context | verified accepted event or rejection | all receipt fields and logical scope must match persisted facts |
| `readStream` | aggregate ID or global cursor | ordered [RuntimeEventEnvelope](domain.md#runtimeeventenvelope) records | never invokes commands, providers, tools or materializers |
| `claimEffect` | effect identity, worker epoch, expected status | claimed [EffectIntent](domain.md#effectintent) | single-host CAS; stale epochs cannot complete |
| `recordEffectObservation` | effect outcome observation, expected claim epoch and outcome digest | committed event/next intent | atomically updates effect status/epoch/outcome event with command receipt and aggregate event/head; unknown remains explicit |

Only the controlled journal writer performs physical writes. Logical publishers call command or bus
interfaces; they never receive a database connection.

### Confirmation acceptance batch

The `acceptConfirmedDispatch` input is a recursively closed writer-owned value. It names exactly:

- the nine newly authoritative artifact-metadata records for pending sheet,
  [DispatchSpec](domain.md#dispatchspec), confirmation observation,
  [ConfirmedTurnGraph](domain.md#confirmedturngraph), ordered mapping set,
  [ConfirmedAuthorityEnvelope](domain.md#confirmedauthorityenvelope), the
  [`run.created`](events.md#runcreated) payload, the
  [`audit_opening.requested`](events.md#audit_openingrequested) payload and the `audit_opening` effect
  payload;
- one immutable [ConfirmationObservation](domain.md#confirmationobservation), one
  [ConfirmedDispatch](domain.md#confirmeddispatch), one [Run](domain.md#run), the graph, its sole
  continuation binding and exactly two normalized
  [ContinuationInputMapping](domain.md#continuationinputmapping) records;
- [`run.created`](events.md#runcreated) at aggregate version `1` bound to its finalized payload
  artifact, [`audit_opening.requested`](events.md#audit_openingrequested) at aggregate version `2`
  bound to its finalized payload artifact, the version-`2`
  [`opening_pending`](states.md#runlifecycle) head, one generic `audit_opening`
  [EffectIntent](domain.md#effectintent)
  bound to its finalized payload requesting appender contract `0.6.4`, in `pending` state with
  `attempt_count=0`, `claimed_by=null`, `claim_epoch=null`, `outcome_event_id=null` and
  `outcome_digest=null`, and the first stable receipt. These fields are present in the closed batch;
  their null values mean never claimed and no accepted outcome.

The capability-resolution artifact is already finalized preview evidence. The writer verifies and
references it but it is not one of the nine acceptance metadata members. The static payload-schema
bundle and identity-derivation contract are digest-bound authority inputs, not newly accepted
artifact metadata. The writer derives or recomputes every server-owned ID and digest before
mutation; caller-supplied graph, mapping, event, effect or receipt identities cannot grant
authority.

For a new key, the identity check occurs after `BEGIN IMMEDIATE` and before creation CAS. Existing
same dispatch plus same `confirmed_authority_digest` returns the byte-identical first receipt with
zero new rows/events/effects, even under a new key. Divergent authority returns
`confirmed_authority_conflict`; same-key command drift returns `idempotency_conflict`. No unlocked
identity pre-read is conformant. Every named failpoint rolls back the complete batch, while a lost
response after commit converges through these same replay rules.

## Internal: AgentAdapter

**Concept:** [AgentAdapter](#internal-agentadapter)  
**Consumers:** effect worker and scheduler.

| Method | Input | Output | Required semantics |
|---|---|---|---|
| `materialize` | [AgentInvocationPlan](domain.md#agentinvocationplan) | [MaterializedAgentInvocation](domain.md#materializedagentinvocation) plus prepared effective-input bytes/metadata | deterministic native translation and canonical input preparation; no artifact, delivery or Attempt acceptance |
| `start` | sealed [AgentExecutionRequest](domain.md#agentexecutionrequest) | provider attempt identity/status observation | invoked only through SandboxLauncher; adapter cannot write state |
| `resume` | sealed [AgentExecutionRequest](domain.md#agentexecutionrequest), opaque continuation handle | provider attempt identity/status observation | same sandbox/fence rules as start; definitive no-start and unknown outcomes are distinct |
| `events` | [Attempt](domain.md#attempt).attempt_id, provider cursor | canonical incremental observations + next cursor | provider-native payload stays namespaced and content-addressed |
| `result` | [Attempt](domain.md#attempt).attempt_id | [AgentTerminalResult](domain.md#agentterminalresult) | common version/parsing rules; provider prose alone never becomes a contribution |
| `cancel` | [Attempt](domain.md#attempt).attempt_id, command ID | cancellation observation | idempotent request; acknowledgement is distinct from terminal state |
| `disposeContinuation` | opaque continuation handle, command ID | typed `acknowledged`, `disposed`, or `unknown` observation with command/handle-digest/adapter cursor | idempotent and correlated; only `disposed` is terminal, acknowledgement remains `cancel_requested`, and unknown requires reconciliation |
| `continuationStatus` | opaque continuation handle | `available`, `definitively_unavailable_no_start`, or `unknown` observation | used after restart or failed resume; only definitive no-start evidence can enter `reconstruction_eligible` |
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

The complete [ResourceBudget](domain.md#resourcebudget) and
[SandboxPolicy](domain.md#sandboxpolicy) values participate in the canonical
[AgentInvocationPlan](domain.md#agentinvocationplan) bytes and `plan_digest`. The sealed
[AgentExecutionRequest](domain.md#agentexecutionrequest) copies those values without defaulting,
coercion or reinterpretation. Provider-native translation is observation/materialization metadata
and cannot replace or weaken them. This binding is a later production contract: POLICY-000 parses
pure values only and creates no plan or request.

When the optional delivery context is present, the prepared manifest contains exactly one
[`reference_bundle`](domain.md#effectiveinputentry) entry produced by
[ReferenceScoutBundleToEffectiveInput](mappings.md#referencescoutbundletoeffectiveinput). The
capability-derived recipient, accepted source facts and immutable bytes are revalidated inside the
atomic StartAgentAttempt acceptance unit. No standalone endpoint or adapter method accepts
[`reference_scout.bundle_delivered_to_agent@1`](events.md#reference_scoutbundle_delivered_to_agent1).

For [AgentContinuation](domain.md#agentcontinuation), the adapter may return an opaque continuation
handle after a terminal turn and later consume it through `resume`. The runtime stores the handle
behind access control and journals only its digest. Resume still consumes a complete sealed request
and exact [EffectiveInputArtifact](domain.md#effectiveinputartifact); provider memory cannot add
undeclared authority or substitute for reconstruction evidence.

A provider that cannot resume must declare `resume=unsupported` in its immutable capability
declaration before dispatch confirmation. If the matching terminal source observation also returns
no handle, the runtime may derive typed `capability_absent_no_handle` evidence from that declaration,
the source attempt and adapter digest. This is canonical definitive-no-start evidence and may move a
suspended continuation to `reconstruction_eligible` only when the separately confirmed policy
allows it. A missing handle without that exact declaration/evidence is `unknown`, not definitive.

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

## Internal: ExecutionPolicyContractParser

**Consumers:** POLICY-000 pure contract-oracle tests. This is a pure implementation-facing module
contract subordinate to [CanonicalContractPolicy](rules.md#aci-r16--canonical-contract-policy), not
an execution or launcher authority.

These methods are pure. Each consumes exact raw JSON bytes, rejects duplicate keys before ordinary
object construction, validates recursively closed fields and strict JSON primitives, reproduces
exact `aci-cjson-1` bytes and returns either one complete typed value with its declared digests or a
typed rejection with no partial value. They perform no persistence, environment/host discovery,
clock, filesystem, network, credential, process, provider, journal, audit or effect call.

Integer handling is exact signed-64 validation, never host-language truncation or coercion. Every
`ResourceBudget` ceiling and `SandboxPolicy.max_child_processes` accepts only
`0..9223372036854775807`; production and harness `cutover_epoch` accept only
`1..9223372036854775807`.

| Method | Input | Output | Contract |
|---|---|---|---|
| `parseResourceBudget` | raw `aci.resource-budget@1` bytes, exact caller-supplied budget-policy target bytes, confirmed tool-profile literal | complete [ResourceBudget](domain.md#resourcebudget), canonical bytes and content digest, or rejection | binds and digest-verifies the supplied target bytes, then validates the closed budget-policy schema; no defaults/coercion; every ceiling is signed int64 `0..9223372036854775807`; `tool.none` requires `max_tool_calls=0`; does not accept dispatch ceilings or derive an Attempt budget |
| `parseSandboxPolicy` | raw `aci.sandbox-policy@1` bytes, exact caller-supplied sandbox-enforcement target bytes, exact caller-supplied credential target-byte map keyed to every `credential_refs` reference | complete [SandboxPolicy](domain.md#sandboxpolicy), canonical bytes and content digest, or rejection | validates the closed enforcement target and digest-verifies every credential target under its reference owner's contract, with no I/O and no universal credential-target schema; accepts non-empty duplicate-free opaque credential refs; `max_child_processes` is signed int64 `0..9223372036854775807`; roots receive lexical grammar checks only and `link_policy` must equal `deny`; non-empty endpoint/executable entries reject in v1 |
| `parseExecutionAuthorityFence` | raw `aci.execution-authority-fence@1` bytes | complete production [ExecutionAuthorityFence](domain.md#executionauthorityfence), canonical preimage/full-document bytes and their distinct digests, or rejection | accepts only the production schema/preimage literals, requires signed int64 `cutover_epoch` in `1..9223372036854775807` and verifies the embedded preimage digest; rejects the harness literal before evidence resolution |
| `parseExecutionAuthorityFenceHarnessForTest` | raw `aci.execution-authority-fence-harness@1` bytes | complete [ExecutionAuthorityFenceHarness](domain.md#executionauthorityfenceharness), canonical preimage/full-document bytes and their distinct digests, or rejection | test-only parser with signed int64 `cutover_epoch` in `1..9223372036854775807`; never returns a production fence or cutover evidence |
| `parseExecutionPolicyOracleFixtureForTest` | raw `aci.execution-policy-oracle-fixture@1` bytes plus exact member/reference-target bytes | complete [ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture), verified member bytes/digests, or rejection | test-only aggregate parser; output type is ineligible for confirmation, plan/request acceptance or effect authority |

The exact schemas, golden bytes/digests and negative-vector allocation come from reviewed
[TECH-POLICY-D0](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md).
Conformance is [T-ACI-POL0-1 through T-ACI-POL0-8](TEST-SPEC.md#policy-000-l0-test-matrix).

`parseSandboxPolicy` never inspects or resolves a host path. Physical symlink,
junction/reparse-point and resolved-path containment enforcement belongs exclusively to the
separate [SandboxLauncher](#internal-sandboxlauncher) at POLICY-003/L3.

## Internal: ExecutionPolicySyntheticLineageHarness (test-only)

**Concept:** [ExecutionPolicySyntheticLineageHarness](capabilities/execution-policy-authority.md#executionpolicysyntheticlineageharness-test-only)
**Consumers:** [T-ACI-POL1-1 through T-ACI-POL1-8](TEST-SPEC.md#policy-001-l1-test-matrix)
test code only.

This boundary may depend only on the pure
[ExecutionPolicyContractParser](#internal-executionpolicycontractparser), existing runtime database,
artifact and canonicalization helpers, and a temporary file-backed database path supplied by the
test. It is not exported from a production package and exposes no runtime service, journal command,
API, CLI, confirmation, run, plan, request, attempt, event, effect, audit, provider, launcher or
policy-resolution operation.

| Method | Input | Output | Contract |
|---|---|---|---|
| `persistSyntheticLineage` | temporary file-backed database, `synthetic_key`, `lineage_identity`, exact seven validated POLICY-000 member bodies in receipt order, optional named test failpoint | first closed [ExecutionPolicySyntheticLineageReceipt](domain.md#executionpolicysyntheticlineagereceipt), or typed rejection/conflict | Revalidate all member bytes/digests; call `ArtifactStore.prepare()` seven times before the transaction; inside one `RuntimeDatabase.write()` transaction resolve key/identity replay or conflict, call `ArtifactStore.finalize(conn, ...)` for all seven prepared artifacts and insert one receipt plus seven ordered bindings. Never call per-artifact `ArtifactStore.commit()`. |
| `reopenSyntheticLineage` | same file-backed database path and persisted `lineage_identity` | first receipt plus the exact seven ordered member bodies/digests, or typed rejection | Reopen through fresh database/artifact handles, reproduce every byte/digest/binding/receipt field and return no partial unit. It invokes no production parser as authority and performs no external effect. |

The only admitted failpoints are after transaction begin, after each artifact finalization, after
the receipt, after each member binding and immediately before commit. `after_commit` is a separate
lost-response observation fired only after the transaction exits; retry must converge on the first
receipt. A failure followed by reopen yields the complete unit or none. Key and lineage-identity
checks occur within the same writer transaction; an unlocked pre-read cannot establish replay.

The harness may create exactly two test-only tables in the temporary database: one receipt table
and one ordered-member table. They are absent from production migrations. On success and failure,
POLICY-001 rows exist only in finalized artifact metadata and those two tables. The production
tables enumerated by [ACI-R16](rules.md#aci-r16--canonical-contract-policy) remain empty, and
fail-on-call spies around every prohibited runtime/external dependency remain at zero.

Persistence never promotes bytes: production policy-document parsers still reject the combined
oracle structurally, and `parseExecutionAuthorityFence` still rejects the harness schema before
evidence resolution after reopen. Conformance is
[T-ACI-POL1-1 through T-ACI-POL1-8](TEST-SPEC.md#policy-001-l1-test-matrix).

## Internal: ExecutionPolicyFakeDenialHarness (test-only)

**Consumers:** [T-ACI-POL2-1 through T-ACI-POL2-8](TEST-SPEC.md#policy-002-l2-test-matrix)
test code only.

This boundary depends only on the exact persisted POLICY-001 test lineage, its harness, the pure
[ExecutionPolicyContractParser](#internal-executionpolicycontractparser), canonicalization/error
helpers and the same caller-supplied temporary file-backed database. It is not exported from a
production package and accepts no [AgentExecutionRequest](domain.md#agentexecutionrequest),
[EffectIntent](domain.md#effectintent), production fence, process/provider/tool/network/credential
callable, runtime service, journal, audit appender, host capability or workload path.

| Method | Input | Output | Contract |
|---|---|---|---|
| `denySyntheticAttempt` | temporary file-backed database, `denial_key`, exact persisted `lineage_identity`, one closed non-executable `action_attempt_label`, optional named test failpoint | first closed [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt), or typed rejection/conflict | Reopen and revalidate the exact POLICY-001 unit before transaction entry; require all-zero budget, deny-all sandbox and one of the twelve T-ACI-POL2-3 labels; resolve both uniqueness axes and insert one canonical receipt in one writer transaction. The label routes test coverage only and is excluded from preimage, receipt, identity and authority. |
| `reopenFakeDenial` | same temporary database path and persisted `lineage_identity` | first canonical fake-denial receipt plus its exact content digest, or typed rejection | Use fresh database/lineage/denial harness handles; reproduce the receipt, `denial_digest`, receipt digest and source lineage binding; return no partial or executable value. |

The admitted label set is exactly the twelve literals in
[T-ACI-POL2-3](TEST-SPEC.md#t-aci-pol2-3--decision-reasons-and-attempt-labels-are-closed).
Every label returns the same byte-identical first receipt because the receipt attests the package-
level deny-all decision, not an attempted effect. An unknown label rejects. The interface never
dispatches on a label to an external adapter.

The only failpoints are `policy_denial.after_begin`, `policy_denial.after_receipt`,
`policy_denial.before_commit` and the post-transaction lost-response observation
`policy_denial.after_commit`. A pre-commit failure reopens with no POLICY-002 row; a post-commit
retry returns the first receipt. The harness may create exactly one additional test-only receipt
table, absent from production migrations. It leaves the seven POLICY-001 artifacts, receipt and
member bindings unchanged and leaves every production authority/runtime/effect table empty.

Temporary SQLite persistence is the only admitted I/O. Each action label must be exercised while
fail-on-call spies for workload filesystem, network, process, credential, tool, provider, runtime,
journal, audit, clock and environment remain at zero. This is the POLICY-002/L2 fake lane only;
OpenAI/Codex CLI or any other real provider and all target-host enforcement remain POLICY-003 or
later work.

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

POLICY-000 does not exercise the operational methods above. POLICY-001/L1 owns synthetic fixture
lineage, POLICY-002/L2 owns fake deny-all behavior, and POLICY-003/L3 owns target-host sandbox and
current production-fence enforcement.

## Internal: Audit Ledger Appender Port

**Consumers:** [AuditLedgerMaterializer](workflows.md#auditledgermaterializer) only.

| Method | Input | Output | Contract |
|---|---|---|---|
| `readByIdentity` | `dispatch_id` or `close_of` | absent, identical candidate row or existing divergent row | tolerant read for reconciliation; never mutates history |
| `appendValidatedRow` | canonical schema `0.6.4` row | physical row reference | invokes the existing validated appender pinned by `dispatch-type-registry.v1.json`; no alternate ledger writer |
| `verifyExactRow` | frozen-authority-derived canonical row | identical, absent or divergent | field-for-field canonical comparison, not identity-only equality |

The journal and YAML audit ledger do not share a transaction. Opening is a release barrier and close
is official only after exact-row verification is recorded back through the journal.

## Internal: Artifact Boundary

**Consumers:** adapters, bus, journal and reveal materializer.

| Method | Input | Output | Contract |
|---|---|---|---|
| `commitArtifact` | bytes, media/schema type, classification | immutable artifact ID and content hash | validates size/hash/type before an event may reference it |
| `commitHostTerminalResponse` | active host-turn binding, terminal kind, exact host-observed bytes, idempotency key | [HostTerminalResponseReceipt](domain.md#hostterminalresponsereceipt) | atomically commits exact bytes, artifact metadata, producer attribution, terminal turn state and accepted event; never accepts a caller path as the artifact source |
| `verifyHostTerminalResponse` | receipt, expected parent/producer turn and optional required completion kind | verified [HostTerminalResponseArtifact](domain.md#hostterminalresponseartifact) or denial | resolves accepted event and exact bytes; rejects cross-dispatch, stale/superseded turn, digest/size/kind drift and missing bytes |
| `verifyHostWorkflowBinding` | [HostWorkflowBindingRef](domain.md#hostworkflowbindingref), expected parent/turn | verified journal-backed binding or denial | supports the bounded legacy-managed bridge without inventing `ConfirmedDispatch` or `Run` |
| `materializeHostWorkflowInput` | active [SourceToSlotMapping](domain.md#sourcetoslotmapping), verified terminal receipt, target binding | [WorkflowInputManifest](domain.md#workflowinputmanifest) and binding candidate | L0 admits exactly one completed producer and one required slot; verifies consumer visibility policy and canonical digest |
| `authorizeHostWorkflowTurnLaunch` | manifest, [HostWorkflowTurnBinding](domain.md#hostworkflowturnbinding), prerequisite heads | accepted launch intent or CAS denial | atomically checks workflow/consumer/mapping/manifest/binding/cancellation/supersession heads; never launches from projection state |
| `getAuthorized` | artifact ID + authenticated principal/action/phase | bytes or denial | applies the same sealing/redaction policy as API/SSE |
| `tombstonePayload` | retention/crypto-erasure authority | tombstone retaining allowed provenance | cannot rewrite the originating event or claim payload availability |

Effective inputs, raw outputs and host terminal responses are sensitive immutable artifacts. Concrete retention periods,
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
| IF-ACI-15 | Host terminal response attribution is not caller-authored | `binding-output(source) -> verifiedHostTerminalResponse(source) and sameDispatch(source,target) and sourceBytes = hostObservedBytes` |
| IF-ACI-16 | Connected topology cannot launch with incomplete dynamic input | `dynamicRequiredSlots(target) and not completeVerifiedManifest(target) -> no launchEffectIntent` |
| IF-ACI-17 | Content identity and producer attribution are separate | `payloadArtifactId = hash(bytes)` and `terminalResponseId = identity(producerTurn)` |
| IF-ACI-18 | L0 dynamic input is visibility-authorized and single-source | `launchable(target) => exactlyOne(activeMapping) and authorized(mapping.visibilityPolicy,target,payload)` |
| IF-ACI-19 | Execution-policy parsing is strict, pure and authority-separated | `policy000Accepted(x) => recursivelyClosed(x) and exactSchema(x) and aciCjson1(x) and signed64RangesValid(x) and everyReferenceHasCallerSuppliedBytes(x) and referencesVerified(x)`; `credentialReferenceVerified(x) => digestValidUnderReferenceOwnerContract(x) and noUniversalCredentialTargetSchema`; `sandboxL0(x) => lexicalRootsOnly(x) and linkPolicy(x)=deny`; `policy000ParserCall(x) => externalCalls = empty and effects = empty`; `physicalLinkResolution => POLICY-003/L3 SandboxLauncher`; `productionFenceParser(harness) => rejectBeforeEvidenceResolution`; `oracleFixture => notExecutionAuthority` |
| IF-ACI-20 | Synthetic policy lineage is test-only, atomic and non-authoritative | `acceptedPolicy001(u) => exactSevenOrderedMembers(u) and atomic(sevenFinalizedArtifacts,oneReceipt,sevenBindings) and replayOrConflictCheckedInsideWriterTransaction`; `reopen(u) => exactBytesAndDigests(u) and sameFirstReceipt(u)`; `policy001ProductionRows = empty`; `policy001ExternalEffects = empty`; `policy001L2Behavior = empty` |
| IF-ACI-21 | Fake-denial labels are test selectors, never attempted effects | `acceptedPolicy002(label,u) => label in closedTwelveLabelCorpus and exactReopenedPolicy001(u) and oneDurableDeniedReceipt(u) and label notIn receiptOrAuthority and externalCalls=empty`; `positiveBudgetOrGrant => rejectBeforeDenialTransaction`; `policy002ProductionRows=empty`; `policy002L3Evidence=empty` |

## Deferred Interface Decisions

- OQ-ACI9: concrete redaction, encryption, access escalation, retention and key-destruction periods.
- OQ-ACI10: empirical completeness of provider usage across tool-heavy, resumed, multi-turn and
  retried executions. Missing dimensions remain `null` until proven.
- Distributed leases, multi-host writers and a generic agent peer-read API are outside the current
  single-host W0 contract.
- Product-selected Attempt ceilings/grants and POLICY-003/L3 operational vectors are outside the
  POLICY-000 parser and POLICY-002 fake-denial surfaces. POLICY-001/L1 and POLICY-002/L2 use only
  their separate test-only harnesses above; neither adds parser authority, a production surface or
  a real-provider path.
