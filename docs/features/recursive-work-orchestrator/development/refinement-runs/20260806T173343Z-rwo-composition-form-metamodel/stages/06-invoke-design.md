# Stage 06 — Invoke Design

Capability: `invoke`  
Mode: `design`  
Candidate: `CompositionFormSourceContract@candidate-2`  
Evidence state: `authored-complete`  
Design-validator/runtime/ontology admission: BLOCKED

This is a repaired candidate architecture, not a schema, compiler, ontology migration, implementation, or runtime guarantee.

## Tournament decision

| Candidate | Shared mechanics | Owner integrity | Testability | Decision |
|---|---:|---:|---:|---|
| universal expression tree | high | failed | superficial | kill |
| seven unrelated schemas | low | high | fragmented | reject |
| common generic envelope | high | failed | medium | kill |
| existing subtype + closed payload + disjoint compilation result | sufficient | high | high when materialized | select |

## View 1 — Context and owners

```text
author/source owner
  -> CompositeWorkDefinition
  -> one existing CompositionForm subtype with closed payload
  -> definition/compiler owner
  -> CompilationSuccess -> WorkGraph
  -> root RWO runtime matches structural events only

domain/recovery/journal/ARE/ACI/authority/effect owners
  -> exact typed verdict/reference
  -> separately accepted boundary
  -> never interpreted or minted by the form compiler
```

Ontology semantic source, generated graph/view projections, validation evidence, and promotion authority remain separate strata.

## View 2 — Components

- existing seven form subtype schemas;
- direct per-form operand fields and existing relations;
- existing selector/mapping/release/lifecycle surfaces;
- typed external owner-reference slots;
- immutable `CompilerProfile`;
- `CompilationSuccess` and `CompilationRejection`;
- compiler-only `FormCompilationDefect`;
- deterministic canonical compiler;
- future serialized fixture corpus and validator.

`FormOccurrence` is optional compile-time diagnostic data and omitted unless path-addressable reuse proves necessary.

## View 3 — Information and identity

Source identity is `CanonicalSourceId + exact subtype + schema_ref + source bytes/provenance`. Compiled identity is `WorkGraph` bytes/digest. Runtime identity is `WorkRun`, `Attempt`, and repeat round. Transport delivery, journal acceptance, recovery decision, admission, authority, and effect identities remain external. No field or object aliases these domains.

Compilation results bind compiler/profile/version, raw-source byte domain/digest, canonical-input byte domain/digest, dependency byte domains/digests, and success-only graph byte domain/digest. Rejection binds non-empty structural defects and no graph.

## View 4 — Workflow

1. resolve subtype, schema, profile, owned references, and typed requirements;
2. validate closed syntax/cardinality/reference shape/graph invariants;
3. derive canonical paths and recursively expand forms;
4. order nodes by source path and edges by the fixed key tuple;
5. preserve semantic lists and sort key-defined sets;
6. return one success or rejection;
7. only after separate runtime admission may accepted history drive structural matching.

Compilation never accepts events, folds cursors, chooses recovery, debits budgets, mints attempts/rounds, interprets labels, or authorizes anything.

## View 5 — Decisions and failures

Compile defects are limited to exact structural codes. Runtime selector no-match, stale fences, route mismatch, frozen join, late arrival, exhaustion, and reducer version are runtime outcomes. Duplicate/quarantine/debit are journal outcomes. Recovery/admission/authority/ARE/ACI/effect failures remain their owner’s typed results. Ontology identity divergence is a migration blocker.

Every future fixture has one result and one mutation boundary. Runtime evidence may be retained while control mutation remains forbidden.

## View 6 — Dependencies and interfaces

| Interface | Consumed by candidate | What remains external |
|---|---|---|
| `CompositeWorkDefinition` / subtype | source enclosure and discriminator | executable Work contract ownership |
| `EventSelector` / `InputMapping` | direct references | their schemas and semantic source |
| `ReleasePolicy` | FanIn structural readiness | quorum owner decision |
| `SidecarLifecyclePolicy` | directed companion coupling | target Work response and primary authority |
| journal/budget | typed accepted debit/history refs | acceptance, ordering, debit, truth |
| recovery/domain | opaque accepted decision refs | treatment/meaning |
| ARE/ACI/admission/authority/effect | typed reference slots | verification, admission, permission, conformance |
| ontology owner | candidate delta proposal | identity migration and promotion |

## Design selection and evidence ceiling

The six views and planned witness contracts are authored. No closed schemas, compiler, serialized fixtures, denominator/selection fixed-point receipt, or executed validators exist. Therefore the design is `authored-complete`, not `design-validator-pass`. Normal implementation planning is blocked; only a validation-first remediation Plan is allowed.

## Dispatch technique trace

- `sequence`: define → research → repair → design → validation-first plan.
- `owner_boundary_check`: external decisions and promotion stay outside compiler/runtime.
- `artifact_contract_bridge`: source syntax maps to graph/result/fixture/ontology candidate surfaces.
- `recomposition_proof`: the minimal source/compile unit rebuilds the six views.
- `validation_loop`: future fixtures require exact bytes, mutations, commands, and receipts.
- `residue_ledger`: owner/migration gates remain explicit.
- Full dispatch: `../REFINE-DISPATCH.json`, validation PASS.

## Next route

Proceed only to Stage 07 review synthesis and a remediation Plan that materializes executable design evidence. Do not route to source/ontology mutation.
