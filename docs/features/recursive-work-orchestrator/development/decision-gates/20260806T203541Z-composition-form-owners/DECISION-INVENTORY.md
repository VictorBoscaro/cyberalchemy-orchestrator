# RWO composition-form owner decisions

Status: decision selections complete; consequential mutation blocked by protected ontology-owner route  
Target: `CompositionFormSourceContract@candidate-2`  
Source result: `../../refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/RESULT.md`

This gate resolves design choices only. It does not mutate `DESIGN.md`, ontology sources, schemas, implementations, generated projections, or authority state. Accepted records may enter `docs/decisions/` only after the user selects a real option and the gate closes; that folder's owner contract admits accepted decisions only.

## Blocker decisions requiring human selection

| Order | Decision ID | Question | Current state |
|---|---|---|---|
| 1 | `DG-RWO-CFM-001` | What authored cardinality does `Sequence` permit? | accepted: `SEQ-NARY-MIN2` |
| 2 | `DG-RWO-CFM-002` | Does RWO own structural `quorum(n)`, or must a Decision Work produce a release label? | accepted: `QUORUM-RWO-STRUCTURAL` |
| 3 | `DG-RWO-CFM-003` | What happens to an eligible arrival after a FanIn release manifest freezes? | accepted: `LATE-RETAIN-NONCONTRIBUTING` |
| 4 | `DG-RWO-CFM-004` | Which ontology identity is canonical, and what migration posture follows? | selected: `ONTOLOGY-ROLLFORWARD-0.2`; protected owner route still required |
| 5 | `DG-RWO-CFM-005` | Is provenance embedded as immutable selectors or referenced through one canonical provenance record? | accepted: `PROVENANCE-EMBEDDED-SELECTORS` |
| 6 | `DG-RWO-CFM-006` | Is compile-only `FormOccurrence` necessary, or are diagnostic source paths sufficient? | accepted: `OCCURRENCE-OMIT-USE-SOURCE-PATH` |

## Direct owner routes, not preference questions yet

- Journal truth, reducer compatibility, and replay migration already fail closed on version mismatch; their owner must publish an exact compatibility/migration contract before another meaningful choice can be prefiltered.
- Authority, recovery, budget, journal-acceptance, ARE, ACI, artifact-admission, and exact-effect reference schemas belong to their exact owners. Decision Gate cannot invent structurally valid schema options for them.
- Serialized fixtures, compiler/validator implementation, and conformance receipts are downstream work, not architectural preferences.

## Claim ceiling

Until all required blocker decisions are selected or explicitly deferred/stopped, the gate result is `BLOCK`. No plan refresh, schema freeze, implementation, or ontology mutation is admitted.
