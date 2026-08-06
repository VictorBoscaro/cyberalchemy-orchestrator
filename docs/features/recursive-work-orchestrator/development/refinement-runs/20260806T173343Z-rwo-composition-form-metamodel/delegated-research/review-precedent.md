# Review Return — Precedent And Existing Owners

- Agent: Tetlock, Philip
- Action: `spawn-0005`
- Target verdict: `FLAG — REPAIR BEFORE EVIDENCE CLOSURE`
- Action execution: completed read-only
- Claim ceiling: candidate design review only; no implementation, adoption, compiler/runtime conformance, or ontology promotion.

Exact local search found no current declarations for the proposed new names, but most proposed semantics already have direct owners under different names. Absence of an exact name is not precedent-clean ownership.

## Type gate

| Candidate | Existing owner | Verdict / repair |
|---|---|---|
| `FormDefinition` | Existing `CompositionForm` taxonomy and seven subtypes; enclosing `WorkDefinition` | Build from owned. Use a concrete authored form definition under the current form taxonomy; do not create an ornamental parallel type. |
| Seven form payloads | `Sequence`, `FanOut`, `FanIn`, `Gate`, `Sidecar`, `BoundedRepeat`, `ExplicitComposition` | Already present as candidate ontology types; extend closed schemas only. |
| `FormInstance` | `WorkGraph`, `WorkNode`, edges, `composition_form` | Retain only if renamed/defined as one source-form occurrence before compilation; never alias `WorkRun`, `WorkNode`, or executing graph. |
| `OperandBinding` | `WorkNode`, `EventTriggeredEdge`, `EventSelector`, `InputMapping`, existing policies | Build from owned; closed role/domain only, with no substitute selector, mapping, policy, authority, or decision owner. |
| `ConditionBinding` | existing selector/policy/edge relations | Repair/remove generic wrapper; prefer typed fields and existing relations. |
| event-selection subtype | `EventSelector` | Already present; do not alias. |
| structural-readiness subtype | `ReleasePolicy` | Already present; quorum owner remains open. |
| route-selection subtype | decision Work plus declared selector/edge | Build from owned; do not create an approval evaluator. |
| bound-availability subtype | `WorkDefinition.limits`, `BoundedRepeat`, journal/recovery debit mechanics | Build from owned; definition declares, accepted-history/budget owner debits. |
| `LateArrivalPolicy` | no exact type; FanIn release and join reconciliation are distinct | Precedent-clean but blocked pending exact behavior and owner. |
| `CompilationReceipt` | existing `compiles-to` requirement and composition-compiler observation | Build from owned; addressable gap, not new authority. |
| `FormValidationDefect` | invariants and current validators | Build from owned and restrict to compiler/schema rejection. |
| `CompilerProfile` | no exact type; `ArchitectureProfile` is not compiler configuration | Precedent-clean if immutable and explicitly non-authorizing. |
| generic external reference | authority, recovery, journal, adapter admission, ARE/ACI, effects each have distinct owners | Do not add generic owner; use exact typed references. |

## Relation gate

- `defines-form`: unnecessary if an authored definition is already a typed existing form node; add only with a distinct endpoint/cardinality.
- `instantiates-form`: admissible only for a source `FormOccurrence -> definition`, never `WorkRun -> WorkDefinition`.
- `binds-operand`: retain with closed role/domain/range.
- `operand-references-work`: reuse/extend existing `references-work`, not an alias.
- `binds-condition`, `condition-specializes`, generic `evaluated-by`: repair or remove; use existing selector/policy relations and exact owners.
- `uses-late-arrival-policy`: blocked with the unresolved policy owner.
- `compiled-under`: precedent-clean immutable compiler-configuration link.
- `compiles-definition` and `produces-explicit-composition`: repair existing `compiles-to` into receipt-mediated lineage; do not add parallel compilation owners.
- `rejects-with`: compiler result to compiler-owned defect only.
- `cites-source`: choose one canonical existing provenance representation.
- `carries-external-reference`: too generic; use exact owner-specific relations, retaining `requires-authority` for authority.

## Defect ownership

Compiler/definition defects may refine current invariants. Runtime selector/route blocks and journal identity conflicts remain runtime/journal owned. Recovery, authority, admission, ARE/ACI, adapter, and exact-effect failures must remain typed external-owner results. `ONTOLOGY_IDENTITY_DIVERGENT` belongs to ontology migration, not form compilation.

## Required repairs

1. Remove parallel aliases and express the model through existing form, selector, mapping, release, lifecycle, graph, and owner surfaces.
2. Preserve recovery/admission/authority/effect ownership unchanged.
3. Repair existing `compiles-to` through a compilation result; do not add a second direct relation.
4. Bind each defect to one deciding owner and phase.
5. Keep late-arrival, quorum, ontology migration, journal truth, authority, artifact admission, ARE/ACI, exact effects, and runtime conformance blocked on their existing residues.

Exact selectors: `DESIGN.md#5.1–5.7`, `#6.3`, `#10`, runtime flow; `ontology/ONTOLOGY.md` type/relation catalogs and validation status; `ontology/ontology.json` owner routes; recovery Candidate-2 identity/concurrency/owner sections; adapter Candidate-2 identity/admission/retry sections. Proof posture: observed candidate sources, designed/unimplemented metamodel, prior ontology validation not rerun.
