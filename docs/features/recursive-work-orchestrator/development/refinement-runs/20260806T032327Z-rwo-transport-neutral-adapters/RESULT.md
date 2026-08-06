# Refined Model: Transport-Neutral RWO Command And Event Adapters

Status: candidate design complete; runtime admission blocked  
Selected handle: `TransportNeutralWorkProtocolAdapterContract@candidate-2`  
Implementation effect: none  
Authority effect: none

## Result In Plain Language

RWO should not have one adapter API that pretends gRPC, sockets, Redis,
managed event buses, and memory all behave alike. It should share only what is
actually common: a canonical Work message identity and a closed vocabulary for
what an adapter observed.

Everything else is declared as an exact capability and proven for a specific
adapter implementation plus configuration. A provider acknowledgement is
delivery evidence, not accepted Work history. The journal remains the gate
into RWO truth. The adapter never decides recovery, domain meaning, reasoning,
execution, effect authority, or success.

## Architecture

```text
RWO canonical command
  -> CommandDeliveryPort
  -> transport-specific adapter
  -> DeliveryObservation candidate
  -> JournalAcceptancePort
  -> accepted observation
  -> RWO reducer/recovery decision

transport delivery
  -> transport-specific adapter
  -> EventIngressPort
  -> canonical event candidate
  -> JournalAcceptancePort
  -> accepted event | identical duplicate | conflict | reject
```

An independent admission path checks:

```text
exact adapter implementation + exact configuration
  + closed capability manifest
  + route/message requirements
  + current conformance receipt
  + journal/effect/authority/ARE/ACI prerequisites
  -> AdapterAdmissionVerdict(pass | block)
```

## The Four Contracts

1. `CommandDeliveryPort` sends canonical commands and returns bounded transport
   observations.
2. `EventIngressPort` converts inbound transport data into canonical event
   candidates.
3. `JournalAcceptancePort` independently decides structural acceptance,
   identical duplicate, conflict, or rejection.
4. `CapabilityDeclarationPort` exposes closed atomic capabilities; it does not
   admit itself.

## Identity Rule

A redelivery keeps the canonical `logical_message_id`, canonical bytes,
digest, Work Run, and Work Attempt. It receives a new
`transport_delivery_attempt_id` and new transport metadata.

- same logical ID + same digest: identical duplicate;
- same logical ID + different digest: conflict and reject;
- delivery count never becomes Work Attempt count;
- provider message ID never becomes canonical identity.

## What An Adapter May Say

The closed observations are `submitted_local`, `accepted_by_transport`,
`accepted_by_peer_application`, `rejected_known`, `failed_known`,
`outcome_unknown`, `flow_controlled`, `redelivered`, `dead_lettered`, and
`disconnected`. Every observation names its exact scope and evidence.

None means journal acceptance, Work completion, domain truth, reasoning
approval, execution authority, or business-effect success.

## Retry And Recovery

“Retry” is split into five different situations:

| Situation | Treatment |
| --- | --- |
| reconnect | create a new connection epoch; do not change Work state |
| transport redelivery | keep logical identity, create a delivery-attempt ID, let the journal deduplicate |
| same-message retry | RWO may choose it only with admitted capability, convergence evidence, current fence, and budget |
| new Work Attempt | only RWO may create it from accepted history and domain-approved recovery policy |
| replay | rebuild from accepted journal records with zero transport/model/effect calls |
| uncertain external effect | effect owner reconciles; never automatically retry |

This makes recovery transport-independent without making it transport-blind.

## Capability Model

Each adapter/configuration declares closed, scoped atoms for durability,
redelivery, acknowledgement, ordering, replay cursor, flow control,
fan-out, settlement, transaction boundary, and correlation. Unknown or missing
capabilities fail closed. A profile is a convenient requirement bundle, not
proof or authority.

## How The Arrangements Fit

| Arrangement | Honest claim |
| --- | --- |
| gRPC | RPC/stream status, flow control, correlation, and optional peer receipt at declared scopes |
| socket | connection/frame/send/disconnect and optional application acknowledgement |
| Redis Streams | entry/group/pending/claim/redelivery/XACK transport evidence |
| managed event bus | provider acceptance, retry/DLQ/fan-out/target scopes |
| in-memory | process-local buffering/delivery with no crash or restart durability claim |

All five implement the same boundary contracts but receive different manifests
and admission outcomes.

## Ontology Integration Candidate

Later ontology review should consider eight nodes:

`CommandDeliveryPort`, `EventIngressPort`, `TransportDeliveryAttempt`,
`DeliveryObservation`, `AdapterCapabilityManifest`,
`TransportRequirementSet`, `AdapterConformanceReceipt`, and
`AdapterAdmissionVerdict`.

Candidate relations are `uses-adapter`, `declares-capability`,
`requires-capability`, `observed-by`, `evidenced-by`, and `admitted-by`.
Negative shields must explicitly prevent transport acknowledgement from
becoming journal truth, delivery from becoming recovery, a profile from
becoming authority, an authority reference from becoming a bearer permit,
transport replay from becoming journal replay, and transport atomicity from
becoming exactly-once business effects.

No ontology node or relation was changed by this run.

## Evidence And Open Gates

The governed three-role review completed and its action gate passed. The target
verdicts were FIX, FIX, and BLOCK; Candidate-2 incorporates all accepted
repairs. Those seats reviewed the frozen source/seed rather than the later
materialized candidate, so their returns are adversarial inputs—not independent
Candidate-2 validation. The 30-scenario matrix is internally single-valued but
design-only.

Runtime admission remains blocked on:

- G1 journal structural acceptance versus domain truth ownership;
- G2 exact-effect permit/outcome/reconciliation contracts;
- G3 ARE/ACI executable conformance and route schemas;
- G4 ontology owner review/promotion;
- G5 implementation/configuration-bound adapter conformance.

The next safe unit is the offline schema/fixture/validator Work Pack. No SWU was
selected or executed in this run.
