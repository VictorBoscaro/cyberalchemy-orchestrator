# Candidate Adapter Contract — Implementation Layering

Status: non-executed, validation-first plan  
Complexity: medium  
Evidence prerequisite: Candidate-2 authored-complete

## Dependency Rule

Higher layers may consume only accepted receipts from lower layers. No layer
may silently fill an owner decision or infer stronger guarantees from a
transport family name.

```text
L0 candidate schemas and vocabularies
  -> L1 offline fixtures and deterministic validator
  -> L2 owner contracts and executable design validation
  -> L3 candidate ontology proposal
  -> L4 one reference adapter and conformance harness
  -> L5 additional transport adapters and RWO integration
```

## L0 — Candidate Contract Artifacts

Materialize closed candidate schemas for:

- `CanonicalWorkMessage` and `TransportDeliveryAttempt`;
- `DeliveryObservation`;
- `AdapterCapabilityManifest` and `TransportRequirementSet`;
- `AdapterConformanceReceipt` and `AdapterAdmissionVerdict`.

L0 has no runtime, network, authority, or ontology effect. Its acceptance is
schema closure, stable canonicalization, and field-owner documentation.

## L1 — Offline Evidence Harness

Convert all Stage 08 cases into immutable fixtures. Add mutation cases for
unknown capability atoms, digest drift, scope weakening, divergent duplicate,
stale validity epochs, journal substitution, and authority-ref misuse. The
validator must be deterministic and offline. A replay spy must prove zero
adapter/model/allocation/effect calls.

## L2 — Owner Contracts And Design Validation

Journal/domain owners decide structural acceptance versus domain truth. Effect
owners define permits, outcomes, convergence, and reconciliation. ARE/ACI
owners define admitted evidence and route schemas. Candidate schemas are then
reconciled and the full suite rerun. Only this layer can yield
`design-validator-pass`.

## L3 — Ontology Candidate

After L2, propose the eight candidate nodes, relations, and six negative
semantic shields to the ontology owner. Promotion is separate authority; this
plan does not mutate the ontology.

## L4 — Reference Adapter

Only after L2 and a separately approved work pack, implement one in-memory
reference adapter. It must truthfully declare process-local durability, prove
buffer/overflow behavior, and pass the same conformance suite. It is a contract
probe, not portability proof.

## L5 — Real Transports And RWO Integration

Each gRPC, socket, Redis Streams, or managed-bus adapter gets its own exact
implementation/configuration manifest, transport-specific adversarial
fixtures, conformance receipt, and admission verdict. Cross-process RWO and
ARE/ACI integration occur only after applicable owner gates pass.

## Prohibited Layer Skips

- no adapter before closed schemas and validation;
- no ontology promotion before owner reconciliation;
- no named-profile admission without atomic capability evidence;
- no runtime retry policy inferred from a transport library;
- no production/release claim from reference-adapter conformance.

