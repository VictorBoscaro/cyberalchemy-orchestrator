# Stage 05 — Distill Coherent Adapter Unit

Capability: `distill`  
Mode: `standard`  
Verdict: PASS

## Broad Layer

The broad layer is the RWO work protocol plus delivery, accepted history,
recovery, domain, reasoning, and authority collaborators.

## Candidate Reduction

| Track | Decision | Elimination condition |
| --- | --- | --- |
| A universal adapter | reject | cannot truthfully express heterogeneity or owner separation |
| B core plus profiles | reject alone | profile support does not prevent command/event/journal collapse |
| C split ports | reject alone | port split does not prevent identity drift or false capability claims |
| D hybrid | select and reduce | viable if the shared surface remains a message/observation contract, not a transport SDK |

## Smallest Coherent Unit

`TransportNeutralWorkProtocolAdapterContract@candidate-1` consists of exactly:

1. `CanonicalWorkMessage` with immutable RWO identity and a separate transport
   metadata carrier;
2. `CommandDeliveryPort` returning `DeliveryObservation`;
3. `EventIngressPort` returning candidate messages plus `IngressObservation`;
4. independent `JournalAcceptancePort` returning accepted/conflict/reject
   records;
5. `AdapterCapabilityManifest` plus `TransportRequirementSet`;
6. owner-issued `AdapterAdmissionVerdict` bound to a conformance receipt.

Inbox, outbox, dead-letter, replay, settlement, fan-out, ordering, and flow
control are capability-specific collaborators or operations. They are not
mandatory core methods.

## Closure Test

- Responsibility: translate canonical messages and transport mechanics without
  deciding lifecycle or authority.
- Inputs: canonical message, delivery/ingress context, exact admitted manifest.
- Outputs: closed observations or candidate messages; never accepted facts.
- Further split: removing any of the six items loses lane, identity, acceptance,
  capability, or admission integrity.
- Hidden glue: journal acceptance is named explicitly; inbox/outbox are not
  silently inferred.

## Recomposition Proof

```text
Work command intent
  -> canonical message
  -> CommandDeliveryPort
  -> DeliveryObservation
  -> journal-admitted recovery input
  -> RWO RecoveryDecisionContract

Transport candidate event
  -> EventIngressPort
  -> schema/identity/authority checks
  -> JournalAcceptancePort
  -> AcceptedRecordRef
  -> cursor/reducer/declared route
```

This recomposes into the current WorkProtocol/Journal architecture without
making the adapter a scheduler, journal, domain owner, ARE, ACI, or effect owner.

## Evolution Profile

Expected variants are new transports and new optional capabilities. The small
extension boundary is the closed capability vocabulary plus versioned profile
constraints. Dynamic arbitrary capability strings are rejected.

## Premortem

The most likely failure is a provider adapter claiming a broad named profile
while interpreting acknowledgement or ordering differently. Repair: admission
is atomic-capability based, configuration-bound, and negative-fixture backed.

## Next Handle

Start Design from `TransportNeutralWorkProtocolAdapterContract@candidate-1`.

