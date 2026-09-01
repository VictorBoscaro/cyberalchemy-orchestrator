---
title: RWO Architecture 1.0.0
status: lifecycle-neutral-architecture-content
version: 1.0.0
private: true
authority_effect: none
promotion_effect: none
publication_effect: none
implementation_effect: none
ontology_effect: none
semantic_contract: RWO-SEMANTIC-CONTRACT/1.0.0
semantic_contract_sha256: 8da8959770733ac4a3f0936f5cb2a8175a0786c909822a141f10670409610740
supersedes_for_architecture_guidance: DESIGN.md@0.1.0
last_updated: 2026-08-08
---

# RWO Architecture 1.0.0

## Architecture decision

RWO is a deterministic structural compiler and reducer. It owns the meaning of
its registered semantic values and two pure operations:

1. compile an admitted `ExplicitComposition` into a normalized `WorkGraph`; and
2. reduce one `AcceptedEventView` against a compatible `WorkGraph` and
   `OrchestrationCursor` into one closed `ReduceOutcome`.

RWO does not execute work. It emits at most one immutable `CommandIntent` for an
external delivery owner. It does not accept events into a journal, decide domain
truth, schedule retries, authorize effects, or own a transport.

This document owns the structural architecture. The accepted
`RWO-SEMANTIC-CONTRACT/1.0.0` remains normative for exact value admission,
normalization, identities, bytes, defects, compilation, and reduction. If this
document conflicts with that contract, the contract wins and this architecture
must be revised through a versioned successor.

## View 1: context

### System boundary

~~~text
Composition author                         Accepted-history owner
       |                                            |
       | ExplicitComposition                        | AcceptedEventView
       v                                            v
  +----------------------------------------------------------------+
  |                  RWO semantic kernel                           |
  |                                                                |
  |  compile composition -> WorkGraph                              |
  |  reduce graph + cursor + accepted event -> ReduceOutcome       |
  +----------------------------------------------------------------+
                         |
                         | optional immutable CommandIntent
                         v
                  Command-delivery owner
~~~

### RWO owns

- exact semantic-profile admission;
- schema-owned semantic normalization;
- canonical payload bytes and typed semantic digests;
- explicit-composition validation and graph compilation;
- accepted-event replay classification;
- deterministic cursor evolution;
- structural readiness and at-most-one command-intent derivation; and
- closed structural defect and outcome ordering.

### RWO explicitly does not own

- why an event is accepted or whether it is true;
- the authoritative event journal or domain state;
- work execution or result quality;
- command delivery, acknowledgements, retry timing, or dead-letter storage;
- clocks, leases, backoff, jitter, circuit breakers, or concurrency control;
- credentials, authorization decisions, effect execution, or compensation;
- transport serialization, service hosting, or deployment; or
- product policy, user interface, publication, or promotion.

## View 2: high-level structure

~~~text
RWO-SEMANTIC-CONTRACT/1.0.0
  |
  +-- Admission and schema registry
  +-- Semantic normalizer
  +-- Canonical payload encoder
  +-- Typed semantic digest
  +-- Composition compiler
  +-- Accepted-event reducer
  +-- Structural defect ordering
  `-- Conformance manifest and detached review

Pure kernel boundary
  |
  +-- compile(ExplicitComposition) -> CompileOutcome
  `-- reduce(WorkGraph, Cursor, AcceptedEventView) -> ReduceOutcome

External integration boundary
  |
  +-- composition source adapter
  +-- accepted-event projection adapter
  +-- command-delivery adapter
  `-- derived-cursor persistence adapter
~~~

The contract and kernel are logically portable. An implementation language,
process boundary, binary interface, RPC mechanism, queue, or storage engine may
vary only behind an adapter that preserves the registered semantic tuple and
passes the same conformance observations.

## View 3: low-level components

### Semantic-profile components

| Component | Input | Output | Forbidden responsibility |
|---|---|---|---|
| Raw admission | raw UTF-8 JSON, exact tuple, closed schema | admitted value or ordered defects | transport acceptance or domain authorization |
| Semantic normalizer | admitted value and schema metadata | normalized semantic value | language iteration order |
| Canonical payload encoder | normalized value | RFC 8785 JCS bytes | domain identity by bare payload alone |
| Typed digest framer | contract/profile/schema/type tuple and payload bytes | domain-separated SHA-256 identity | wire-format identity |
| Composition compiler | admitted `ExplicitComposition` | `Compiled` or `Rejected` | scheduling or execution |
| Event reducer | graph, compatible cursor, accepted event | closed `ReduceOutcome` | journal acceptance or delivery retry |
| Defect comparator | structural defects | one total order | exception text or host ordering |
| Conformance package | exact inputs and expected observations | language-neutral test oracle | implementation or owner self-approval |

### First-slice values

| Value | Architectural role |
|---|---|
| `ExplicitComposition/1.0.0` | admitted source form presented to compilation |
| `WorkGraph/1.0.0` | normalized structural graph produced only by compilation |
| `AcceptedEventView/1.0.0` | accepted-event identity and semantic payload presented by an external owner |
| `OrchestrationCursor/1.0.0` | derived reducer state for one graph identity and stream |
| `CommandIntent/1.0.0` | immutable structural request derived by reduction |
| `StructuralDefect/1.0.0` | deterministic failure description ordered by the contract comparator |
| `CompileOutcome` | `Compiled` or `Rejected` |
| `ReduceOutcome` | `Applied`, `Duplicate`, `DivergentDuplicate`, or `Rejected` |

### Identity model

Canonical payload bytes identify a representation. A typed semantic digest
identifies a value only after binding the exact contract, profile, schema,
version, and value type. Graph, accepted-event, payload, command-intent, command
payload, cursor, and defect-detail identities therefore cannot alias merely
because their bare JSON payload bytes happen to match.

Delivery identifiers, attempts, timestamps, traces, broker offsets, leases, and
adapter metadata never participate in these semantic identities.

## View 4: workflow process

### Compilation

~~~text
raw ExplicitComposition
  -> admit exact contract/profile/schema/type tuple
  -> normalize schema-owned collections
  -> validate identifiers, endpoints, schemas, and first-slice cardinality
  -> construct normalized WorkGraph
  -> derive canonical bytes and typed graph identity
  -> Compiled(graph, bytes, identity)

any defect
  -> deterministic ordered defects
  -> Rejected(defects), no graph
~~~

Compilation is total over admitted input: it returns a closed result rather than
partially constructing a graph. The graph identity is derived and is not stored
inside the graph whose identity it names.

### Reduction

~~~text
WorkGraph + original cursor + AcceptedEventView
  -> validate exact versions, graph identity, and stream binding
  -> derive accepted-event identity and payload digest
  -> classify new, exact duplicate, or divergent duplicate
  -> for a new event, record it and select matching unsatisfied edges
  -> derive zero or one immutable CommandIntent
  -> return one closed outcome
~~~

- `Duplicate` returns the byte-identical original cursor and no command.
- `DivergentDuplicate` returns the byte-identical original cursor and no command.
- `Rejected` returns the byte-identical original cursor and no command.
- `Applied` returns a normalized next cursor and zero or one command intent.
- A new non-matching event is still recorded in the next cursor.

The cursor is a rebuildable structural projection. It is not a second journal
and cannot establish domain truth or external-effect completion.

## View 5: decision and recovery flow

~~~text
exact tuple and raw input admitted?
  no  -> Rejected(ordered defects)
  yes -> normalize and derive typed identity

event identity already present?
  same payload digest      -> Duplicate(original cursor)
  different payload digest -> DivergentDuplicate(original cursor)
  absent                    -> record event and evaluate graph

matching unsatisfied edge count?
  0 -> Applied(next cursor, no command)
  1 -> Applied(next cursor, immutable command intent)
 >1 -> Rejected(original cursor)
~~~

### Retry boundary

RWO classifies semantic situations; it never schedules attempts. A separately
owned service or adapter may map a declared `RetrySituation` to
`DoNotRetry`, `RetrySame`, `ReconcileThenDecide`, `DeadLetter`, or `Escalate`.

`RetrySame` preserves the complete command intent, command-intent identity, and
command-payload digest. A new physical delivery attempt does not create new
semantic work. Unknown delivery does not default to retry. Schema rejection,
divergent replay, invalid commands, authority denial, and failed
acceptance-critical validation are terminal for the same request.

Structural repetition is different: it is new graph-authorized work represented
by an explicit bounded edge. RWO does not convert operational retries into graph
cycles or graph cycles into delivery attempts.

## View 6: dependency and interface boundaries

| From | To | Allowed | Forbidden |
|---|---|---|---|
| Semantic contract | Unicode and canonicalization standards | pinned rules and data | host serializer defaults |
| Kernel | schema registry and contract values | exact registered tuples | transport, storage, clock, or credential dependency |
| Composition adapter | compiler | admitted `ExplicitComposition` | bypassing compilation with a claimed graph |
| Accepted-event adapter | reducer | exact `AcceptedEventView` supplied after external acceptance | claiming that delivery equals acceptance |
| Cursor store adapter | reducer caller | byte-preserving derived cursor persistence | becoming authoritative history or domain state |
| Command adapter | delivery target | immutable `CommandIntent` plus separate delivery context | changing semantic identity or payload |
| Any implementation | conformance manifest | read-only expected observations | regenerating or self-approving accepted expectations |

### Serialization boundary

JSON under the accepted JCS/I-JSON-safe-integer profile owns canonical semantic
payload bytes for contract version 1. A transport may use another encoding only
if its adapter proves a lossless mapping to and from the registered logical
value. Transport bytes do not replace canonical semantic bytes.

Large or transport-specific artifacts remain outside the first-slice control
values unless a future versioned schema admits an exact reference contract.

## Architecture invariants

| ID | Invariant |
|---|---|
| RWO-A01 | Equal admitted inputs under one exact tuple produce byte-identical normalized values, payload bytes, identities, defects, and outcomes. |
| RWO-A02 | Compilation is the only path from `ExplicitComposition` to a valid `WorkGraph`. |
| RWO-A03 | Reduction consumes an externally accepted event; it never performs journal acceptance. |
| RWO-A04 | One reducer call emits at most one immutable command intent. |
| RWO-A05 | Duplicate, divergent-duplicate, and rejected outcomes preserve the original cursor bytes. |
| RWO-A06 | The cursor is derived structural state and never a journal or domain-state authority. |
| RWO-A07 | Delivery metadata and attempts remain outside semantic identity. |
| RWO-A08 | `RetrySame` preserves semantic identity; structural repetition is explicit new work. |
| RWO-A09 | Unknown versions, schemas, owners, mappings, and identities fail closed. |
| RWO-A10 | A command intent is a request, not authorization or proof of an external effect. |
| RWO-A11 | Transport and implementation language cannot redefine contract meaning. |
| RWO-A12 | Accepted fixtures are immutable inputs to ordinary conformance tests. |

## Compatibility and evolution

Version 1 accepts only exact registered contract, profile, schema, and value-type
tuples. Compatibility is never inferred from semantic-version numbering. A
future compatibility projection must name source and target tuples, direction,
total algorithm, loss posture, conformance vectors, and owner acceptance.

The smallest extension boundaries are new schemas, a new semantic-contract
version, or separately proven adapters. Adding service policy, a transport, a
provider, a domain lifecycle, or an effect gate to the kernel would violate the
current architecture rather than extend it.

## Risks and required treatments

| Risk | Required treatment |
|---|---|
| Canonicalization differs by language | execute the same positive and negative vectors independently |
| Bare payload digests alias across types | use the accepted typed digest preimage |
| Duplicate keys collapse during parsing | preserve name occurrences until decoded-equivalent duplicate rejection |
| Cursor becomes hidden authority | rebuild from accepted inputs and retain the non-authority invariant |
| Retry mutates commands | separate semantic identity from delivery-attempt metadata |
| Adapter leaks transport semantics inward | dependency and lossless-mapping checks |
| Fixtures self-bless | detached independent review and explicit update acceptance |
| Documentation drifts from the contract | digest pinning, link checks, and versioned successor review |

## Evidence and claim ceiling

The accepted semantic contract and its frozen schemas/vectors establish a
normative language-neutral target. This architecture candidate establishes a
selected document boundary only after its Design selection passes. Neither
surface proves that any implementation conforms, that any runtime is integrated,
that performance is sufficient, or that any external effect occurred.

Canonical creation of this document requires exact owner acceptance of its
staged digest and post-creation byte validation. Such creation has authority,
promotion, publication, implementation, ontology, deployment, and production
effects all `none`.
