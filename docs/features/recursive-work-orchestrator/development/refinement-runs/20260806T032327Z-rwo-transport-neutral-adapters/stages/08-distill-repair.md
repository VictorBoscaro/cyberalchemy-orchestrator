# Stage 08 — Distill Repair

Capability: `distill`  
Mode: `repair`  
Candidate exactness: PASS  
Runtime admission: BLOCKED

## Repaired Candidate

`TransportNeutralWorkProtocolAdapterContract@candidate-2`

Candidate-2 repairs every accepted review finding. It defines a transport-
neutral semantic boundary, not a universal transport implementation.

## 1. Normative Separation

The model has four independent contracts:

1. `CommandDeliveryPort` translates an already-authorized canonical command
   into transport operations and returns bounded delivery observations.
2. `EventIngressPort` translates inbound transport delivery into a candidate
   canonical event plus transport evidence.
3. `JournalAcceptancePort` alone converts a candidate event/observation into an
   accepted record, identical duplicate, conflict, or rejection.
4. `CapabilityDeclarationPort` describes an exact adapter/configuration; an
   independent admission owner compares it with requirements and conformance
   evidence.

An adapter is never the RWO scheduler, journal, domain owner, ARE, ACI, effect
owner, or authority selector.

## 2. Exact Message And Identity Model

`CanonicalWorkMessage` is the union of `CanonicalCommand` and
`CandidateEvent`. Its immutable identity is:

```text
schema_version
message_kind + message_type
work_ref
root_work_run_id + work_run_id + node_path + round_id?
work_attempt_id
logical_message_id
correlation_id? + causation_id?
actor_ref?
authority_evidence_ref?
idempotency_key + idempotency_scope
payload_schema + canonical_payload_bytes
canonical_digest
```

`canonical_digest` covers the schema identity and canonical bytes. Redelivery
must preserve every canonical field. The adapter adds a separate
`TransportDeliveryAttempt`:

```text
transport_delivery_attempt_id
adapter_implementation_digest + adapter_configuration_digest
provider_message_id?
connection_epoch?
topic/stream/partition/group/offset?
acknowledgement_or_settlement_token?
delivery_count?
observed_transport_status?
observed_at
retry_after_hint?
dead_letter_locator?
```

Only journal acceptance adds accepted-record identity and sequence. A
transport/provider ID cannot replace `logical_message_id`; a Work Attempt ID
cannot replace a transport delivery-attempt ID.

Duplicate rule:

- same `logical_message_id` + same `canonical_digest` -> identical duplicate;
- same `logical_message_id` + different `canonical_digest` -> conflict and
  fail closed;
- different logical IDs, even with equal payload -> distinct messages unless a
  domain-owned idempotency contract says otherwise.

## 3. Exact Observation Model

A `DeliveryObservation` is the tuple:

```text
observation_kind
observation_scope
logical_message_id
transport_delivery_attempt_id
adapter implementation/configuration digests
evidence_ref
observed_at
retry_after_hint?
```

The only observation kinds are `submitted_local`, `accepted_by_transport`,
`accepted_by_peer_application`, `rejected_known`, `failed_known`,
`outcome_unknown`, `flow_controlled`, `redelivered`, `dead_lettered`, and
`disconnected`. `observation_scope` must identify the exact local process,
connection, stream, provider, peer, target, partition, or group boundary.

These observations are candidates for journal acceptance before an RWO reducer
may use them. None directly advances Work lifecycle, accepted sequence, domain
truth, authority, or effect outcome.

## 4. Exact Capability Manifest

`AdapterCapabilityManifest` is closed and versioned. It binds exact
implementation and configuration digests and declares:

- durability: none, process-lifetime, or persistent with retention;
- redelivery: none, provider-retry, and/or consumer-redelivery;
- acknowledgement scopes: local, provider, peer-application, and/or consumer
  settlement;
- ordering scopes: connection, stream, partition, key, target, or none;
- replay: none or transport-cursor with retention;
- flow control: block, credit, pull, throttle, or none, plus buffer bound and
  overflow behavior;
- fan-out: single, competing-consumer, broadcast, and/or per-target;
- settlement operations: ack, nack, extend, claim, or none;
- transaction boundaries: exact named transport/storage operations only;
- correlation: none, request-response, and/or stream-messages.

Every scoped capability includes its limitations and prohibitions. Unknown
atoms, dynamic strings, missing scopes, and profile fallback fail closed. A
named profile is only a versioned `TransportRequirementSet` bundle.

## 5. Admission Contract

`AdapterAdmissionVerdict` is valid only for this atomic tuple:

```text
adapter implementation digest
adapter configuration digest
manifest digest and schema version
requirement-set digest and message/route scope
conformance-receipt digest
conformance owner
validity epoch
external prerequisite refs
```

The deterministic candidate admission procedure is:

1. validate closed schemas, canonical digests, and identity invariants;
2. compare every required capability, scope, limit, and prohibition with the
   manifest;
3. block on absent, unknown, ambiguous, incompatible, or silently degraded
   behavior;
4. validate a current owner-issued conformance receipt for the exact
   implementation/configuration/manifest/requirements tuple;
5. validate the required journal, effect, authority, privacy, and route owner
   prerequisites;
6. issue one result: `pass` or `block`, with reasons and evidence locators.

The manifest is a claim. The conformance receipt is evidence. The admission
verdict is a scoped eligibility decision. All have `authority_effect: none` and
none selects a Work transition or effect permit.

## 6. Retry, Redelivery, Replay, And Reconciliation

| Situation | Identity change | Decision owner | Allowed treatment |
| --- | --- | --- | --- |
| transport reconnect | new connection epoch | adapter/transport policy | reconnect only; no Work transition |
| transport redelivery | new delivery-attempt ID; same logical ID/digest | admitted delivery policy | accept as candidate; journal deduplicates |
| known pre-accept delivery failure | new delivery-attempt ID if retried | RWO recovery contract | same-message retry only within declared capability/budget/fence |
| unknown delivery outcome | none inferred | RWO + recipient/effect owner | reconcile or wait; no blind effect retry |
| new Work Attempt | new `work_attempt_id` | RWO recovery decision | only from accepted history and current policy |
| replay | no new identity | journal/reducer owner | route-free reconstruction; zero external calls |
| uncertain external effect | no retry inferred | effect owner | reconcile against effect contract and current permit |

Same-message retry requires all of: an admitted redelivery capability; stable
logical identity and bytes; recipient convergence/idempotency evidence for the
declared scope; a current authority/effect fence where applicable; and
remaining policy budget. If any condition is absent, the result is `block` or
`reconcile`, never silent fallback. `outcome_unknown` involving an external
effect always selects reconciliation, not automatic retry.

## 7. State Transitions

```text
PreparedCanonicalCommand
  -> SubmittedToAdapter
  -> DeliveryObservationCandidate
  -> JournalAcceptance
  -> AcceptedObservationRecord
  -> RWO recovery/reducer decision

TransportIngress
  -> ParsedCandidateEvent
  -> identity/schema/authority evidence validation
  -> JournalAcceptance
  -> AcceptedEventRecord | IdenticalDuplicate | Conflict | Reject
```

No edge exists from transport state directly to Work completion, new Work
Attempt, domain fact, ARE conclusion, ACI execution, or effect outcome.

Replay consumes only accepted journal records and produces reducer state. It
must make zero adapter, model, allocation, route, and effect calls.

## 8. Transport Arrangements

- gRPC maps status, headers, local buffering, stream/connection flow control,
  and explicit peer receipts to their exact observation scope. RPC success is
  not journal or business acceptance.
- sockets map frame identity, connection epoch, local send, disconnect, and an
  optional application-level receipt. Reconnect is not recovery.
- Redis Streams maps stream/group/entry, pending/claim/redelivery, and XACK to
  transport metadata and settlement evidence. Pending or acknowledged entries
  are not accepted Work history.
- managed event buses map provider acceptance, configured retry/DLQ, fan-out,
  target, and ordering scope. Partial target delivery remains per-target
  evidence.
- in-memory maps only process-local buffering and delivery. It truthfully
  declares no cross-process or crash durability and no restart replay.

New transports integrate by implementing the ports, closed manifest, and
conformance cases. They do not require changes to RWO lifecycle semantics.

## 9. Candidate Ontology Delta

No ontology is mutated in this run. Candidate nodes for later owner review:

- `CommandDeliveryPort`
- `EventIngressPort`
- `TransportDeliveryAttempt`
- `DeliveryObservation`
- `AdapterCapabilityManifest`
- `TransportRequirementSet`
- `AdapterConformanceReceipt`
- `AdapterAdmissionVerdict`

Candidate relations: `uses-adapter`, `declares-capability`,
`requires-capability`, `observed-by`, `evidenced-by`, and `admitted-by`.

Required negative semantic shields:

- transport acknowledgement is not journal acceptance;
- transport delivery/reconnect is not Work recovery;
- named profile is not admission or authority;
- `authority_evidence_ref` is not a bearer permit;
- transport replay is not journal replay;
- transport transaction is not exactly-once business effect.

## 10. Repair Closure And Remaining Gates

The scenario matrix gives one design-level decision for each admitted test
case. Candidate-2 therefore passes internal exactness and recomposition.

It does not clear these external gates:

- G1 journal structural acceptance versus domain truth ownership;
- G2 exact-effect permit, outcome, and reconciliation contracts;
- G3 ARE/ACI executable schemas and route conformance;
- G4 ontology review and promotion;
- G5 adapter implementation/configuration conformance evidence.

Until those owners act and executable fixtures pass, every runtime adapter
admission remains BLOCKED.

