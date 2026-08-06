# Stage 08 — Distill Repair And Exact Candidate

Capability: `distill`  
Mode: `repair`  
Candidate: `CompositionFormSourceContract@candidate-2`  
Verdict: PASS for smallest coherent authored model; executable validation BLOCKED

## Exact repaired model

The source surface is an immutable node of one existing form subtype inside `CompositeWorkDefinition`. Its subtype is the discriminator. It has one exact schema reference, one closed subtype payload, and immutable provenance. There is no parallel form-definition type or runtime form instance.

Per-form operands are direct typed fields. Selectors, mappings, release/lifecycle policies, graph relations, and authority relations reuse existing owners. Domain, recovery, journal, budget, ARE/ACI, admission, authority, and effect inputs appear only in exact typed owner-specific slots and remain non-authorizing references.

The compiler returns exactly one of:

- `CompilationSuccess` with exact input/dependency/profile/compiler byte domains and digests plus one output `WorkGraph`; or
- `CompilationRejection` with the same source/compiler binding and non-empty compiler structural defects, but no graph.

The compiler owns only structural desugaring and rejection. Runtime, journal, recovery, admission, authority, reasoning, effects, ontology validation, and promotion retain separate states and owners.

## Form rules

| Form | Exact structural rule | Preserved gate |
|---|---|---|
| Sequence | ordered `steps`, selectors/mappings for adjacent transitions | minimum cardinality |
| FanOut | one source, non-empty unique keyed branches | per-branch external requirements |
| FanIn | non-empty unique keyed sources, one join, canonical order, existing release policy | quorum and late arrival |
| Gate | one decision Work, non-empty unique opaque route map | decision meaning external |
| Sidecar | one primary, non-empty companions, directed lifecycle/observation configuration | no companion control of primary |
| BoundedRepeat | body, decision, exhaustion target, opaque labels, positive finite limit/debit ref | retry/repeat owner separation |
| ExplicitComposition | non-empty nodes, typed edges, mappings, output projection, bounded cycles | remains source syntax |

## Failure and mutation rules

Compiler defects are one-code structural rejections and produce no graph/runtime/journal mutation. Runtime outcomes may retain evidence but do not perform forbidden control mutation. Journal outcomes own deduplication, divergence quarantine, fencing, order, and debit. External owners produce their exact failures; the form model does not rename them.

## Scenario contract

`08-scenario-matrix.json` is a planned, unexecuted matrix. It gives each case exactly one expected result, allowed mutation, forbidden mutation, and gate dependency. Its `status` is deliberately `planned-unexecuted`; it is not evidence of non-vacuity or conformance.

## Recomposition and residue

The model recomposes into the existing RWO form/graph vocabulary without adding domain or authority semantics. It remains blocked on exact schemas, serialized fixtures, compiler/validator implementation, byte/digest bindings, executed receipts, owner decisions, and ontology migration.
