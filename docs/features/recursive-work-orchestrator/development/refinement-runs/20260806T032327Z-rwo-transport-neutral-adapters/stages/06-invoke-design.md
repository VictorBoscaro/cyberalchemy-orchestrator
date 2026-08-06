# Stage 06 — Invoke Design

Capability: `invoke`  
Mode: `design`  
Evidence state: `authored-complete`  
Runtime admission: BLOCKED

## Candidate

`TransportNeutralWorkProtocolAdapterContract@candidate-1`

This is a candidate contract, not an implemented interface, validated schema,
admitted adapter, ontology promotion, or runtime guarantee.

## Tournament Decision

| Candidate | Fidelity | Owner integrity | Portability | Testability | Decision |
| --- | --- | --- | --- | --- | --- |
| universal transport interface | low | low | apparent only | low | reject |
| core plus named profiles | medium | medium | medium | medium | reject alone |
| split ports only | medium | high | medium | medium | reject alone |
| canonical core + split ports + atomic capabilities + admission | high | high | high if proven per adapter/config | high | select |

The winner shares message identity and observation vocabulary. It does not
pretend that every transport has durability, acknowledgement, replay, fan-out,
ordering, settlement, or backpressure.

## View 1 — System And Owner Boundary

```text
domain-approved Work intent
  -> RWO kernel
  -> CanonicalCommand
  -> CommandDeliveryPort
  -> transport observation ------------------------------+
                                                           |
transport candidate event -> EventIngressPort              |
  -> CandidateEvent -> JournalAcceptancePort -> accepted record
                                               -> RWO reducer/recovery
                                               -> declared ARE/ACI route
```

The adapter owns transport translation and observation. RWO owns Work
lifecycle decisions under domain-approved policy. The journal owner decides
structural acceptance. The domain owner decides domain meaning. ARE reasons
only on admitted inputs. ACI executes only a separately admitted route. An
effect owner supplies exact-effect permits and reconciliation evidence. An
`authority_evidence_ref` locates evidence; it never authorizes an action.

## View 2 — Components And Ports

### Mandatory boundary components

```text
CommandDeliveryPort.submit(
  command: CanonicalCommand,
  context: DeliveryContext
) -> DeliveryObservation

EventIngressPort.receive(
  context: IngressContext
) -> IngressDelivery | NoDelivery | IngressObservation

JournalAcceptancePort.accept(
  event: CandidateEvent,
  expected_head: ExpectedJournalHead?
) -> AcceptedRecordRef | IdenticalDuplicateRef | Conflict | Reject

CapabilityDeclarationPort.describe(
  adapter_instance_ref: AdapterInstanceRef
) -> AdapterCapabilityManifest
```

`JournalAcceptancePort` is an independent RWO collaborator. A transport
adapter must not implement it merely because it exposes `ack`, `commit`,
`offset`, `receipt`, or `success`.

### Optional capability collaborators

`DeliverySettlementPort`, inbox, outbox, dead-letter routing, transport cursor,
request/response correlation, fan-out, and flow control exist only when the
admitted manifest declares the exact capability and configuration.

## View 3 — Information, Identity, And Evidence

### Canonical Work message

The canonical portion is immutable across redelivery:

| Field | Rule |
| --- | --- |
| `schema_version` | closed supported version |
| `message_kind` | `command` or `event` |
| `message_type` | declared WorkProtocol type |
| `work_ref` | stable Work identity |
| `root_work_run_id` | root execution tree identity |
| `work_run_id` | current Work Run identity |
| `node_path` | stable node position |
| `round_id` | recursive round identity when applicable |
| `work_attempt_id` | RWO execution attempt; transport cannot mint it |
| `logical_message_id` | stable across transport redelivery |
| `correlation_id` / `causation_id` | trace relationships, not authority |
| `actor_ref` | claimed actor evidence locator |
| `authority_evidence_ref` | evidence locator only |
| `idempotency_key` | scope declared by message type/effect contract |
| `payload_schema` / `payload` | typed canonical content |
| `canonical_digest` | digest of canonical bytes and schema identity |

An ingress adapter must preserve the received canonical bytes or a
deterministic canonical representation sufficient to recompute the digest.
The tuple `(logical_message_id, canonical_digest)` defines duplicate identity:
same ID and digest is an identical duplicate; same ID and different digest is
a divergent duplicate and must be rejected.

### Transport delivery metadata

Transport metadata is mutable and never enters canonical identity:

`transport_delivery_attempt_id`, adapter/config digest, provider message ID,
connection epoch, topic/stream/partition/group/offset, acknowledgement token,
delivery count, transport status, observed time, retry-after hint, and
dead-letter locator.

### Accepted history metadata

Only the journal may add `accepted_record_ref`, `accepted_sequence`,
`accepted_at_logical`, and `journal_head_digest`. Transport/provider metadata
cannot substitute for any of these fields.

## View 4 — Runtime Observation Algebra

The closed transport observation kinds are:

| Observation | Exact meaning |
| --- | --- |
| `submitted_local` | local adapter accepted the call/buffer entry |
| `accepted_by_transport` | named transport/provider accepted within a declared scope |
| `accepted_by_peer_application` | explicit peer application receipt was observed |
| `rejected_known` | named boundary rejected and no acceptance occurred there |
| `failed_known` | named operation failed with a known terminal transport outcome |
| `outcome_unknown` | acceptance or effect cannot be determined from available evidence |
| `flow_controlled` | progress is withheld by a declared pressure mechanism |
| `redelivered` | same logical message arrived in a new transport delivery attempt |
| `dead_lettered` | named transport moved delivery to a declared dead-letter location |
| `disconnected` | connection/session ended; delivery outcome is not inferred |

Every observation includes `scope`, `adapter_instance_ref`, configuration
digest, delivery-attempt identity, evidence locator, and observation time.
None means journal acceptance, Work success, domain truth, or business-effect
completion.

Recovery distinctions are mandatory:

- reconnect continues or replaces a transport connection;
- redelivery repeats a logical message with a new delivery-attempt identity;
- a new Work Attempt is created only by an RWO recovery decision;
- replay reduces accepted journal history with zero transport/effect calls;
- reconciliation asks the effect owner about an uncertain effect.

`outcome_unknown` never authorizes automatic effect retry.

## View 5 — Capability And Admission Model

### Closed manifest atoms

| Dimension | Allowed values / required qualification |
| --- | --- |
| durability | `none`, `process_lifetime`, `persistent(retention)` |
| redelivery | `none`, `provider_retry`, `consumer_redelivery` |
| acknowledgement | `none`, `local`, `provider`, `peer_application`, `consumer_settlement` |
| ordering | `none`, or `connection`, `stream`, `partition`, `key`, `target` with scope |
| replay | `none`, or `transport_cursor(retention)`; never journal replay |
| flow control | `none`, `block`, `credit`, `pull`, `throttle`, with buffer/overflow policy |
| fan-out | `single`, `competing_consumer`, `broadcast`, `per_target` |
| settlement | supported subset of `ack`, `nack`, `extend`, `claim` |
| transaction | exact named atomic boundary; never business-effect atomicity |
| correlation | `none`, `request_response`, `stream_messages` |

Unknown values fail closed. Named profiles are reusable requirement bundles,
not proof and not authority.

### Admission tuple

An `AdapterAdmissionVerdict` binds all of:

1. exact adapter implementation digest;
2. exact configuration digest;
3. manifest schema/version and declared atomic capabilities;
4. `TransportRequirementSet` for the route/message class;
5. an owner-issued, current `AdapterConformanceReceipt` for that exact tuple;
6. applicable journal, effect, authority, privacy, and route prerequisites;
7. owner and validity epoch.

Admission algorithm: validate schemas/digests and identity; compare every
requirement against manifest atoms; reject unknown, absent, ambiguous, or
prohibited values; validate the exact current conformance receipt; validate
external owner prerequisites; issue `pass` or `block`. Admission has
`authority_effect: none`.

Self-declaration, profile name, library choice, or transport documentation is
not admission evidence.

## View 6 — Transport Mappings And Assurance

| Transport arrangement | Honest mapping | Forbidden inference |
| --- | --- | --- |
| gRPC unary/streaming | connection/stream correlation, status and optional app receipt; flow control as configured | write/status is not journal acceptance; retry is not universally safe |
| raw/framed socket | connection epoch, frames, optional application ack | send success or reconnect is not recovery/durability |
| Redis Streams | stream/group/entry/PEL/claim/XACK transport evidence | XACK is not journal acceptance or business-effect truth |
| managed event bus | provider acceptance, configured retry/DLQ/fan-out scopes | provider receipt is not consumer or journal acceptance; no global ordering claim |
| in-memory | process-local submit/receive and declared buffer policy | no crash durability, cross-process delivery, or restart replay |

Planned conformance witnesses must cover canonical byte preservation,
identical/divergent duplicates, disconnect and outcome ambiguity, redelivery,
ordering scope, flow-control overflow, partial fan-out, stale admission,
unsupported capability, journal substitution attempts, replay zero-call, and
unknown-effect retry refusal.

## Design Evidence Ceiling And Open Gates

The six views are authored and internally composable. They have not been
materialized as schemas, fixtures, validator code, or transport adapters.
Therefore this stage is `authored-complete`, not `design-validator-pass`.

Open owner gates:

- G1: journal owner must define structural acceptance versus domain truth;
- G2: effect owner must define exact-effect permit/outcome/reconciliation;
- G3: ARE/ACI owners must define executable conformance and route admission;
- G4: ontology owner must approve candidate vocabulary and relations;
- G5: each adapter owner must provide implementation/config-bound conformance.

