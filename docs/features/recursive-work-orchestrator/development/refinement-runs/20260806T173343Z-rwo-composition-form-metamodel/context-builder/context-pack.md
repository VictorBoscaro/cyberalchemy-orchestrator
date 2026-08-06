# Context Pack: RWO Composition-Form Metamodel

Pack kind: runtime handoff session evidence  
Mode: standard, strict, emit both  
Run ID: `20260806T173343Z-rwo-composition-form-metamodel`  
Claim ceiling: candidate research, design, ontology delta, and non-executed plan

## Obligations

| ID | Obligation | Evidence | Status |
|---|---|---|---|
| O1 | Preserve the seven named form meanings while finding the smallest common model. | `DESIGN.md` §§5.1–5.7; seed | covered |
| O2 | Separate immutable form definition, structural placement, and runtime Work identities. | `DESIGN.md` §§4–5, 9; seed | covered; exact model is candidate |
| O3 | Define closed operand roles and form-specific cardinalities. | seed §Forms; current ontology type catalog | covered as research obligation |
| O4 | Separate structural predicates, selectors, policies, limits, external decisions, and prohibitions. | `DESIGN.md` §§5–8, 10–11; recovery result | covered |
| O5 | Prevent domain, recovery, ARE/ACI, admission, authority, and effect owner collapse. | `DESIGN.md` purpose/non-goals and RWO-I10; recovery result | covered |
| O6 | Preserve redelivery, Work retry, repeat round, replay, and effect reconciliation distinctions. | recovery and adapter results | covered |
| O7 | Define deterministic desugaring to `ExplicitComposition` and compiler lineage. | `DESIGN.md` §5.7, RWO-I07/I11; seed | covered as candidate requirement |
| O8 | Define fan-in ordering, quorum, frozen manifest, and late-arrival behavior. | `DESIGN.md` §5.3; seed; recovery concurrency | covered; owner choices retained |
| O9 | Define versioning, compatibility, migration, and extension posture. | ontology sources and seed | covered; identity mismatch retained |
| O10 | Define ontology nodes, relations, constraints, queries, and non-collapse shields. | `ontology/ONTOLOGY.md`, `ontology.json`, graph validators | covered as candidate delta |
| O11 | Provide finite positive fixtures and discriminating negative controls. | seed required output and ontology validator precedents | covered as planned witnesses |
| O12 | Produce an owner-gated, non-executed implementation Work Pack. | Refine and Invoke Plan contracts | covered |

Strict coverage: PASS. Open ownership choices are retained as explicit gates, not hidden context omissions.

## Selected evidence

| Source | Selectors | Obligations | Why included |
|---|---|---|---|
| `../../../DESIGN.md` | Purpose, Non-goals, §§4–11, RWO-I01–I12, open questions | O1–O9 | current RWO candidate semantics and ownership boundaries |
| `../../../ontology/ONTOLOGY.md` | §§1, 3, 5, 6, 12, 13 | O3, O9–O11 | current semantic vocabulary, shields, residue, and claim limits |
| `../../../ontology/ontology.json` | ontology identity, form/property/relation/constraint sections | O3, O9–O11 | current machine-readable projection and version mismatch evidence |
| `../../../ontology/scripts/build-graph.mjs` and `validate-graph.mjs` | canonical generation, closed schema, endpoint/source checks | O7, O10–O11 | current deterministic-validation precedents |
| `../../../ontology/examples/all-operators.pipeline.json` | all-form example | O1, O7, O11 | current concrete composition surface |
| `../20260805T184601Z-rwo-domain-recovery-model/RESULT.md` | architecture, treatments, identities, concurrency, domain/ARE, claim ceiling | O4–O8 | recovery-owner and identity separation |
| `../20260806T032327Z-rwo-transport-neutral-adapters/RESULT.md` | architecture, identity, observations, retry/recovery, evidence | O4–O7 | delivery-versus-execution boundary |
| `../REFINE-SEED-PROPOSAL.md` | problem, candidates, forms, outputs, ceiling | O1–O12 | user-confirmed refinement scope |

## Evidence versus inference

Evidence establishes the named form vocabulary, structural compilation intent, existing owner boundaries, partial ontology, and lack of generic runtime/compiler conformance. The exact envelope, closed payload schemas, condition taxonomy, receipt-mediated compilation lineage, ontology delta, fixtures, and plan are designed candidates to be attacked and validated; no source already adopts them.

## Authority precedence

1. User-confirmed seed and exact run scope.
2. Current RWO `DESIGN.md` for candidate architecture boundaries.
3. Recovery and adapter candidate results for identity and owner consistency.
4. Semantic ontology source; machine/generated ontology surfaces are projections.
5. Delegated research is advisory until parent evidence closure.
6. Validation proves only the named candidate artifact, never promotion or runtime readiness.

## Constraints and non-goals

- Writes stay inside this run folder except the registered and eventually closed append-only dispatch ledger rows.
- `DESIGN.md`, ontology sources/projections, implementations, `cyberAlchemy-v2`, definitions, Inventory, authority, deployment, release, and production state remain unchanged.
- A form may carry accepted external references but may not evaluate their semantics or manufacture permission.
- No proposed schema, defect code, compiler rule, ontology node, fixture, or work-pack task is represented as implemented.

## Fallback exploration rule

Unsupported details become explicit owner gates or planned witnesses. Do not broaden sources, invent authority, or convert candidate consistency into implementation proof.
