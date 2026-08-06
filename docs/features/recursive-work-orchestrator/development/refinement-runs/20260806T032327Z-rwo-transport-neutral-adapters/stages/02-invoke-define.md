# Stage 02 — Invoke Define

Capability: `invoke`  
Mode: `define`  
Template selection: candidate architecture definition within the Refine run  
Phase status: PASS

## Problem Definition

RWO has a logical command/event protocol boundary and an independent journal,
but its present candidate delivery clause overstates one deployment posture as
universal. gRPC, sockets, Redis consumer groups, managed buses, and memory do
not share one truthful durability, acknowledgement, replay, ordering, fan-out,
or backpressure contract.

The adapter problem is therefore not “wrap any transport.” It is:

> Preserve one RWO message and ownership model while requiring every adapter to
> state, prove, and stay within its actual transport capabilities.

## Exact Terms

| Term | Definition | Not equivalent to |
| --- | --- | --- |
| `CanonicalWorkMessage` | Immutable command/event bytes and RWO-owned identity submitted to or received from a transport boundary. | broker record or socket frame |
| `TransportDeliveryAttempt` | One transport-level attempt to move a canonical message. | RWO `Attempt` |
| `DeliveryObservation` | Scoped fact the adapter can report about a delivery attempt. | journal acceptance or recovery decision |
| `CommandDeliveryPort` | Outbound port that submits an addressed command and reports transport observations. | command execution or acceptance |
| `EventIngressPort` | Inbound port that exposes candidate event messages and transport observations for validation/acceptance. | accepted event or route release |
| `JournalAcceptancePort` | Independent boundary that accepts structural history and returns accepted record identity. | acknowledgement, inbox, outbox, or offset |
| `AdapterCapabilityManifest` | Closed declaration of supported, unsupported, and prohibited semantics for one implementation/configuration digest. | admission proof |
| `TransportRequirementSet` | Capabilities and limits required by one deployment/Work binding. | preference or transport name |
| `AdapterConformanceReceipt` | Immutable results for profile-specific positive and negative fixtures. | self-declaration |
| `AdapterAdmissionVerdict` | Owner-issued pass/block for an exact adapter/configuration/manifest/requirement/evidence tuple. | registration or authority for effects |

## Falsifiable Hypothesis

`TransportNeutralWorkProtocolAdapterContract@candidate-1` is sufficient if and
only if:

1. command delivery, event ingress, and journal acceptance are separate ports;
2. command/event ports share canonical message identity and return only closed
   observations;
3. optional transport behavior is declared in a closed capability manifest;
4. admission compares required capabilities against proven capabilities and
   fails closed on absent, unknown, expired, or prohibited behavior; and
5. no transport observation can select RWO recovery, domain meaning, ARE/ACI
   admission, or exact-effect authority.

## Candidate Families

- A — universal lowest-common-denominator port;
- B — one protocol port plus optional profiles;
- C — split command/event/journal ports without a shared admission model;
- D — hybrid split ports, canonical identity, capability manifest, and
  owner-issued admission verdict.

No candidate is selected by this stage.

## Dispatch Technique Trace

- `sequence`: consumes stage 01 and feeds stage 03.
- `frame_handoff`: the strict context pack bounds sources.
- `mandatory_component`: all ten terms above are required definition handles.
- `owner_boundary_check`: each term names what it cannot authorize or prove.
- Full dispatch: `../REFINE-DISPATCH.json`, validated PASS.

## Layering

Define records a layering gap rather than inventing implementation structure.
The later Plan stage must create the required implementation-layering artifact.

## Evidence Ceiling

Definition is authored. No template, term, profile, adapter, ontology node,
runtime behavior, admission, or authority is promoted.

