# Work Pack — Executable Evidence For Composition Form Source Contract

Status: candidate remediation plan; not admitted, selected, or executed  
Source design: `CompositionFormSourceContract@candidate-2`  
Objective: turn the repaired authored design into executable offline evidence before any runtime or ontology migration proposal.

## Control fields

| Field | Value |
|---|---|
| complexity | high |
| output mode | compact planning snapshot; mutation handoff blocked pending split execution contracts |
| design evidence | `authored-complete` |
| plan evidence | `plan-evidence-pending` |
| implementation layering | `IMPLEMENTATION-LAYERING.md` |
| admission timing | selected unit at a future Task Session |
| selected unit | none |
| execution entry | blocked; no machine route projection authored |
| authority effect | none |

This Refine run does not authorize any SWU. Before execution, Invoke Plan must be refreshed into split task/wave contracts, exact allowed routes, closeout synchronization, baseline hashes, and an Implementation Readiness-valid execution-entry projection.

## Boundaries

Future L0–L3 candidate artifacts must live in a separately approved RWO development/evidence folder. Existing `DESIGN.md`, ontology, implementations, definitions, `cyberAlchemy-v2`, authority state, Git, deployment, and production remain read-only until their exact owner route separately authorizes them. L4 ontology targets are never automatic.

## SWU-CFM-001 — Disjoint compilation-result contracts

Primary behavior: prove that success and rejection cannot be confused.

Deliverables: closed candidate schemas for `CompilerProfile`, `CompilationSuccess`, `CompilationRejection`, and `FormCompilationDefect`; byte-domain definitions; positive and schema-negative vectors.

Acceptance: success requires one graph/no defects; rejection requires non-empty defects/no graph; raw/canonical/output domains cannot alias; unknown fields reject; fixtures and deterministic schema receipt pass.

Dependencies: none.  
Future write scope: new candidate-only evidence folder; exact path must be approved.  
Split analysis: schemas and vectors are inseparable because neither independently proves disjointness.  
Execution: not selected; recommended first.

## SWU-CFM-002 — Owner decision pack

Primary behavior: obtain one explicit owner verdict for every semantic that blocks closed schemas.

Deliverables: requests/receipts for Sequence cardinality, quorum, late arrival, journal truth/reducer migration, typed authority/admission/ARE/ACI/artifact/effect/budget references, provenance, ontology identity, and optional occurrence need.

Acceptance: every choice has one named owner, exact selected value or explicit defer/block, source selectors, version, applicability epoch, and no permissive default.

Dependencies: none; required before affected L1 schema fields.  
Future write scope: owner decision artifacts only.  
Split analysis: this is a closure-only manual pack; individual owners may answer independently, but schema admission requires the full required subset.  
Execution: manual, not selected.

## SWU-CFM-003 — Seven closed source schemas

Primary behavior: accept only the exact common metadata plus one existing subtype payload.

Deliverables: common source schema and seven discriminated subtype schemas that reuse existing selectors, mappings, release/lifecycle policies, graph types, and exact owner-reference schemas.

Acceptance: generic `conditions`, evaluators, policies, limits, external references, extension bags, duplicate discriminators, and cross-form fields reject; every form has one minimal valid and one cardinality/role negative.

Dependencies: SWU-001 and applicable SWU-002 owner receipts.  
Future write scope: candidate schemas/fixtures only.  
Split analysis: each subtype may be a child implementation unit, but the independent acceptance boundary is the closed one-of family and cross-subtype rejection.  
Execution: not selected.

## SWU-CFM-004 — Serialized fixture corpus

Primary behavior: turn Stage 08’s plan into exact finite inputs/outputs/mutation assertions.

Deliverables: nested all-seven source and expected graph; one exact file per planned case; initial/final state snapshots; expected single result; byte sizes/digests; allowed/forbidden mutation declarations.

Acceptance: every case is complete and schema-valid; no `or`/unnamed defect; blocked-owner cases remain non-runnable until receipts exist; corpus manifest binds every byte.

Dependencies: SWU-003.  
Future write scope: fixtures/manifest only.  
Split analysis: individual fixtures can be authored separately, but the corpus acceptance boundary is total coverage with one manifest.  
Execution: not selected.

## SWU-CFM-005 — Deterministic compiler and validator

Primary behavior: compile/reject exact sources deterministically without external side effects.

Deliverables: canonicalizer, recursive desugarer to `WorkGraph`, structural validator, compilation-result emitter, test harness, and machine receipt.

Algorithm: resolve exact versions/dependencies; validate closed source; derive canonical paths; recursively expand; order nodes/edges by the frozen rules; preserve semantic lists/sort keyed sets; reject collision/divergence; emit exactly one result.

Acceptance: nested golden passes; two runs are byte-identical; keyed permutation is invariant; every compile negative yields one defect; spy proves zero journal/runtime/model/network/effect calls.

Dependencies: SWU-001, 003, 004.  
Future write scope: candidate compiler/validator/tests only.  
Split analysis: canonicalizer, compiler, and result emitter are candidate child units, but the selected acceptance boundary must be split further before execution unless a task contract proves their atomicity.  
Execution: blocked pending Plan refresh/split.

## SWU-CFM-006 — Runtime and owner-boundary harness

Primary behavior: prove structural reducer behavior without owner collapse.

Deliverables: accepted-history schedules and spies for selector no-match, stale attempt, FanIn freeze/late arrival, Gate mismatch/corruption, Sidecar failure, repeat exhaustion, redelivery/retry/repeat/replay/effect distinctions, and raw ARE/admission misuse.

Acceptance: permitted evidence retention occurs; every forbidden control mutation remains absent; replay is zero-call; exact owner references fail closed when stale/missing/mismatched.

Dependencies: SWU-005 and all applicable journal/recovery/authority/ARE/ACI/effect owner receipts.  
Future write scope: candidate runtime test harness only; production runtime read-only.  
Split analysis: each owner boundary is independently testable and must become its own execution task during Plan refresh.  
Execution: blocked-owner and blocked-split.

## SWU-CFM-007 — Ontology migration candidate

Primary behavior: propose the smallest non-aliased, source-backed graph delta after executable evidence.

Deliverables: identity reconciliation; candidate semantic source updates for result/profile/defect concepts and relation repair; queries, shields, provenance, fixtures, generated projections, validation receipt, and independent owner review.

Acceptance: current semantic/machine identity agrees first; no generic form/condition/reference nodes; source/graph/result/runtime/projection/validation/promotion strata stay distinct; graph validators and negatives pass; ontology owner explicitly decides acceptance/promotion.

Dependencies: SWU-002, 005, 006 and ontology owner gate.  
Future write scope: exact ontology targets only after separate approval.  
Split analysis: semantic source, projection, validation, and promotion are separate lifecycle units and must not be bundled in execution.  
Execution: blocked-promotion.

## Validation strategy

| Slice | Evidence |
|---|---|
| L0 result contract | closed-schema negatives, disjoint-union assertions, golden digests |
| L1 source schema | per-form positives/negatives, cross-kind rejection, owner receipts |
| L2 compiler | nested golden, repeat compile, permutation, collision, zero-call spy |
| L3 runtime boundaries | before/after state schedules, no-control-mutation assertions, owner substitution negatives |
| L4 ontology | identity reconciliation, semantic validation, deterministic projections, queries, negative shields, owner receipt |

## Stop conditions

Stop on unresolved semantic choice, generic extension seam, ambiguous defect, missing byte binding, failed acceptance-critical case, external call during offline compile/replay, authority/promotion/deployment request, destructive scope, or any attempt to combine semantic source, generated projection, runtime implementation, validation, and promotion in one SWU.

## Dispatch technique trace

- `sequence`: 001 → owner-gated 003 → 004 → split 005 → owner-gated 006 → 007.
- `scu_swu_reduction`: each SWU states one primary behavior and split pressure.
- `recomposition_proof`: the seven units rebuild source, compiler, evidence, runtime boundaries, and ontology candidate without owner collapse.
- `validation_loop`: every layer has exact future evidence.
- `owner_boundary_check`: 002, 006, and 007 stop on external owners.
- `execution_receipt_handoff`: every future unit requires an exact receipt, but no execution route is admitted here.
- `residue_ledger`: all semantic/migration/conformance gaps remain visible.

## Plan verdict

This Work Pack is sufficient as a dependency-ordered remediation map. It is intentionally insufficient for mutation-capable handoff until a later Invoke Plan refresh supplies split task/wave artifacts, exact targets, closeout contracts, allowed routes, a selected SWU, and an Implementation Readiness-valid execution entry.
