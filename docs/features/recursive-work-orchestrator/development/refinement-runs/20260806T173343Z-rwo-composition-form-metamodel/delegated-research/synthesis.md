# Synthesis Return

- Agent: Mac Lane, Saunders
- Role: synthesizer
- Verdict: `PASS` as evidence-bounded candidate research
- Claim ceiling: nothing here is implemented, adopted, promoted, or proven at runtime.

## 1. Baseline and candidate selection

Current sources provide seven named composition forms, event-triggered-edge expansion, typed-edge and fail-closed invariants, partial ontology vocabulary, and partial graph validation. They do not provide an exact common envelope, form-instance distinction, typed operand bindings, closed condition algebra, deterministic compiler receipt, full cardinalities, or finite compiler-conformance witnesses. No generic recursive compiler or RWO runtime is evidenced. The ontology identity also diverges: semantic/current-state surfaces identify `rwo-architecture@0.2.0`, while `ontology.json#/ontology` identifies `0.1.0`. [Eilenberg §§1,9; Riehl §§1,8; direct: `DESIGN.md#5-the-composition-algebra`, `#10-validation-invariants`, `RWO-I01–I12`; `ontology/ONTOLOGY.md#1`, `#3-element-type-catalog`, `#5-allowed-relation-catalog`, `#13`; `ontology/ontology.json#/ontology`; `ontology/evidence/CURRENT-STATE-2026-08-05.json#/findings/rwo:finding.current.graph-expansion`; observed]

| Candidate | Verdict | Basis |
|---|---|---|
| Universal expression tree / generic policy evaluator | KILL | Cannot prevent structural evaluation from absorbing domain, recovery, ARE/ACI, authority, admission, or effect decisions. |
| Seven unrelated schemas | REJECT | Preserves local fidelity but duplicates identity, provenance, compiler lineage, defects, and validation mechanics. |
| Common envelope plus seven closed discriminated payloads | RETAIN WITH CONTROLS | Shares only structural mechanics; form-specific operands, conditions, policies, and limits remain closed. |

## 2. Exact common model

```text
FormDefinition {
  form_ref: CanonicalRef
  form_kind: Sequence | FanOut | FanIn | Gate |
             Sidecar | BoundedRepeat | ExplicitComposition
  form_version: ExactVersion
  boundary_contract_ref: WorkContractRef
  payload: ClosedKindPayload
  provenance: {
    source_refs: NonEmpty<ImmutableSourceSelector>
    source_digest: Digest
  }
}

FormInstance {
  form_instance_id: CanonicalId
  form_ref: CanonicalRef
  enclosing_graph_ref: GraphRef
  structural_path: CanonicalPath
  operand_bindings: NonEmpty<OperandBinding>
  compiler_profile_ref: CompilerProfileRef
}

OperandBinding {
  role: KindClosedRole
  key: StableLocalKey
  target:
    WorkRef | NodeRef | EdgeRef | MappingRef |
    ExistingPolicyRef | AcceptedExternalRef
  requirement_refs: [AuthorityOrAdmissionRequirementRef]
}
```

`FormDefinition` is immutable schema and provenance. `FormInstance` is structural placement under an exact compiler profile. Neither is a run, attempt, repeat round, decision, recovery treatment, evidence acceptance, authority bearer, or promotion record. Generic `conditions`, arbitrary policies, free-form limits, and executable extension bags are forbidden. [Eilenberg §3; Riehl §§2–4; direct: `DESIGN.md#Purpose`, `#Non-goals`; designed]

## 3. Closed condition taxonomy and owners

| Family | Kind | Evaluator/state owner | RWO-visible effect |
|---|---|---|---|
| Event selection | Evaluable selector | RWO matcher over journal-accepted, exact-version/current-attempt events conforming to the source `EventContract` | Satisfy one declared edge selector once. |
| Structural readiness | Closed predicate | RWO cursor reducer | Determine declared arrival readiness; `all`, `any`, or provisionally `quorum(n)` has no semantic-quality meaning. |
| Route selection | Exact-match selector | Decision Work owns label meaning; RWO matches the accepted opaque label | Select exactly one declared route. |
| Lifecycle coupling | Closed policy | Existing `SidecarLifecyclePolicy`; target Work owns cancellation response and terminal state | Start, observe, detach, await, or request cancellation. |
| Boundedness | Finite limit plus accepted debit reference | Definition/policy owner defines limit; journal/budget owner atomically records consumption | Permit or reject another declared round. |
| Recovery | Accepted-decision reference | `RecoveryDecisionContract@candidate-2` owner | Follow an accepted treatment; never infer one. |
| Authority/admission/effect | Accepted external reference or requirement | Authority, ACI, admission, or effect owner | Gate delivery only; never manufacture permission. |
| Domain/ARE | Opaque accepted result/reference | Domain Work and evidence/admission owners | Supply mapping data or route label without interpretation. |
| Prohibition | Compile-time constraint | Schema/compiler validator | Reject before graph/runtime mutation. |

Only event selection, structural readiness, exact route matching, and bound availability are RWO-evaluable. Selectors, policies, limits, accepted-decision references, and prohibitions remain distinct objects. [Hewitt §§1–3; Riehl §§2,5; designed taxonomy grounded in the direct design, recovery, and adapter sources]

## 4. Admissibility by form and phase

Legend: `V` compile validation, `E` runtime structural evaluation, `M` exact match, `P` closed policy/limit, `R` accepted external reference, `—` forbidden.

| Form | Compile | Runtime |
|---|---|---|
| Sequence | Event/structural `V`; authority/admission `R` | Event/structural `E`; recovery and authority `R`; domain data opaque |
| FanOut | Event/structural `V`; per-branch authority `R` | Event/structural `E`; per-command recovery/authority `R` |
| FanIn | Event/structural/bound `V`; authority `R` | Event/structural `E`; late-arrival `P`; recovery/authority `R`; reconciliation join-owned |
| Gate | Event and closed labels `V`; decision Work and authority `R` | Event `E`; route `M`; recovery/authority `R`; meaning decision-owned |
| Sidecar | Event/structural/lifecycle `V`; authority `R` | Event/structural `E`; lifecycle `P`; recovery/authority `R`; no implicit primary control |
| BoundedRepeat | Event/structural/labels/bound `V`; recovery/authority `R` | Event/structural `E`; route `M`; finite bound and atomic debit `P`; recovery/authority `R` |
| ExplicitComposition | Every edge, mapping, lifecycle policy, and cycle bound `V`; external owners `R` | Declared event/structural `E`; routes `M`; lifecycle/bounds `P`; external decisions remain `R` |

No cell admits a general boolean expression over domain payloads, recovery state, ARE conclusions, admission, authority, or effect outcome. [Hewitt §3; Riehl §5; designed]

## 5. Seven exact payloads

- `Sequence`: ordered, at least two `steps`; each adjacent transition binds one declared release selector, mapping, and requirement references. Order is semantic; “success” is never inferred.
- `FanOut`: exactly one source release and at least one uniquely keyed branch. Branches canonicalize by key; each retains independent authority requirements.
- `FanIn`: at least one uniquely keyed source, exactly one join Work, complete canonical source order, `all | any | quorum(n)` release policy, and exactly one closed late-arrival policy. `1 <= n <= source_count`; join Work owns reconciliation.
- `Gate`: exactly one decision Work and at least one unique opaque-label-to-target route. Runtime must match exactly one route; zero or multiple matches block without creating a decision.
- `Sidecar`: exactly one primary and at least one uniquely keyed companion, existing lifecycle policy, declared start/observe/finish behavior, and explicit output-contribution behavior. No implicit failure or cancellation control.
- `BoundedRepeat`: exactly one body, decision Work, distinct continue/stop labels, positive `max_rounds` or admitted finite-budget reference, stable round-key rule, and exactly one exhaustion target. Repeat, redelivery, Work retry, and recovery are distinct.
- `ExplicitComposition`: non-empty uniquely keyed nodes, typed edges, boundary mappings, output projection, selectors/mappings, and explicitly bounded cycles; no convenience-form residue.

Recursive operands expand beneath one root orchestrator; nesting does not create nested orchestrators or new authority. [Eilenberg §4; Hewitt §§2–4; Riehl §§3–5; designed]

Disagreement preserved: Eilenberg models Sequence as a non-empty ordered list, while Riehl’s minimum ontology cardinality uses predecessor/successor. Retain the ordered-list surface with a minimum of two steps and compile each adjacent pair; this preserves n-ary ergonomics while satisfying binary-edge realization. This synthesis choice requires owner confirmation.

## 6. Deterministic compilation and receipt

1. Resolve exact form, schema, compiler profile, source digest, Work contracts, selectors, mappings, policies, and external-reference requirements.
2. Validate the closed payload and admissibility matrix without emitting runtime state.
3. Assign paths from parent path, form kind, and stable operand key.
4. Recursively expand child forms.
5. Emit nodes ordered by canonical structural path.
6. Emit edges ordered by `(from_path, selector_ref, route_or_branch_key, to_path, mapping_ref)`.
7. Sort mathematical sets by declared key; preserve only semantic sequences, including Sequence order and FanIn manifest order.
8. Reject duplicate keys or equal canonical IDs with divergent bytes.
9. Serialize an `ExplicitComposition`, compute digests, and emit receipt-mediated lineage.

```text
CompilationReceipt {
  compiler_ref
  compiler_version
  compiler_profile_ref
  canonicalization_profile
  form_ref
  form_version
  source_digest
  input_canonical_digest
  dependency_digests: [{ref, version, digest}]
  explicit_composition_ref
  output_canonical_digest
  defects: []
}
```

Identical canonical input, dependencies, compiler, and profile must yield byte-identical graph and semantic receipt bytes. Observation timestamps, if any, are outside semantic identity. Compilation cannot interpret labels, accept journal facts, mint attempts or rounds, select recovery, infer transport success, or satisfy authority/admission/effect gates. [Eilenberg §5; Hewitt §4; Riehl §§3–4; designed]

## 7. Identity, concurrency, late arrival, versioning, and extension

- Runtime predicate input is accepted, deduplicated history fenced by graph version, run, node, round, and current attempt.
- Each edge transitions from unsatisfied to satisfied at most once per scope.
- `any` uses the first eligible accepted event in journal per-run order; no global-clock claim.
- `quorum(n)` freezes the first eligible distinct-source set, stored in canonical source order.
- A materialized join command and manifest are immutable. Late arrivals remain evidence and may drive only separately declared edges.
- Identical redelivery converges; divergent bytes under one identity quarantine.
- Stale-attempt events remain evidence but cannot release current edges.
- Cancellation request and cancellation terminal observation are distinct.
- Repeat continuation needs both accepted decision label and atomically accepted bound debit.
- Unknown major version, kind, operand role, condition family, or compiler profile rejects.
- Optional minor additions are compatible only when canonical defaults produce identical output when absent.
- New roles, conditions, edge behavior, ordering, identity rules, or form kinds require a new version, compiler rule, owner route, fixtures, and migration declaration.
- Historical receipts are never reinterpreted. Migration creates a new candidate definition and receipt.
- Extension bags and executable predicates are forbidden.

## 8. Unified defect vocabulary

Compile-time rejection with no runtime-state mutation:

`FORM_KIND_UNKNOWN`, `FORM_VERSION_UNSUPPORTED`, `FORM_SOURCE_DIGEST_MISMATCH`, `FORM_OPERAND_ROLE_INVALID`, `FORM_OPERAND_MISSING`, `FORM_OPERAND_DUPLICATE_KEY`, `FORM_REFERENCE_UNRESOLVED`, `FORM_RELEASE_SELECTOR_INVALID`, `FORM_MAPPING_INVALID`, `FORM_CONDITION_FAMILY_FORBIDDEN`, `FORM_CONDITION_PHASE_FORBIDDEN`, `DOMAIN_PREDICATE_IN_KERNEL`, `FANOUT_EMPTY`, `FANIN_EMPTY`, `FANIN_SOURCE_DUPLICATE`, `FANIN_QUORUM_OUT_OF_RANGE`, `FANIN_ORDER_INCOMPLETE`, `FANIN_LATE_ARRIVAL_POLICY_MISSING`, `GATE_ROUTE_DUPLICATE`, `SIDECAR_IMPLICIT_CONTROL`, `REPEAT_BOUND_NON_POSITIVE`, `REPEAT_EXHAUSTION_MISSING`, `EXPLICIT_GRAPH_UNBOUNDED_CYCLE`, `FORM_CANONICAL_ID_COLLISION`, `COMPILATION_DIGEST_DIVERGENCE`, `ONTOLOGY_IDENTITY_DIVERGENT`.

Runtime block/quarantine without fabricated decisions:

`EVENT_SELECTOR_UNDECLARED`, `EVENT_ATTEMPT_STALE`, `ROUTE_LABEL_UNMATCHED`, `ROUTE_LABEL_AMBIGUOUS`, `FANIN_LATE_ARRIVAL_MUTATION`, `CANCELLATION_STATE_COLLAPSE`, `REPEAT_BOUND_EXHAUSTED`, `RECOVERY_DECISION_REFERENCE_MISSING`, `AUTHORITY_REFERENCE_MISSING`, `ADMISSION_REFERENCE_MISSING`, `REDELIVERY_RETRY_REPEAT_COLLAPSE`, `EFFECT_OUTCOME_RETRY_FORBIDDEN`, `ARE_EVIDENCE_UNADMITTED`, `MESSAGE_IDENTITY_DIVERGENT`, `REDUCER_VERSION_STALE`.

Names are candidate vocabulary, not implemented codes.

## 9. Candidate ontology delta

Add only:

- Nodes: `FormDefinition`, `FormInstance`, `OperandBinding`, `ConditionBinding`, four closed structural condition subtypes, `LateArrivalPolicy`, `CompilationReceipt`, `FormValidationDefect`, and `CompilerProfile`.
- Properties: exact form/kind/version, operand key/role, condition family, phase, evaluator owner, canonical order key, compiler profile, source/output/canonical digests, defect code/path, compatibility mode, and fixed `authority_effect: none`.
- Relations: `defines-form`, `instantiates-form`, `binds-operand`, `operand-references-work`, `binds-condition`, `condition-specializes`, `evaluated-by`, `uses-late-arrival-policy`, `compiled-under`, `compiles-definition`, `produces-explicit-composition`, `rejects-with`, `cites-source`, and `carries-external-reference`.
- Repair existing direct `compiles-to` into receipt-mediated lineage.
- Retain existing `EventSelector`, `InputMapping`, `ReleasePolicy`, `SidecarLifecyclePolicy`, `AuthorityReference`, and graph types; do not create aliases.
- Enforce acyclic containment/evidence relations, form-specific cardinalities, explicit bounded graph cycles, unique keys/routes, closed condition admissibility, non-transitivity, source lineage, projection non-authority, and all proposed non-collapse shields.
- Queries must expose operands/roles, RWO-evaluable conditions, external owner references, bounded cycles/exhaustion, invalid quorum/order/routes, prohibited sidecar paths, source-to-output receipts, missing provenance, ontology-version divergence, non-none authority effects, and fixture coverage.

## 10. Acceptance witnesses and scenario matrix

Positive witnesses: a minimal valid fixture per form; one nested all-seven-form compilation; byte-identical recompilation and receipt digest; permuted unordered FanOut input yielding identical output; preserved Sequence order and canonical FanIn manifest order; FanIn `all`, `any`, `quorum(1)`, and `quorum(source_count)`; late arrival retained without join mutation; Gate opaque labels with exactly one match; Sidecar observation without control inference; Repeat continuation with accepted label plus atomic debit; explicit bounded cycle with exhaustion; and generated graph/view coverage plus query fixtures.

| Negative scenario | Expected defect/effect |
|---|---|
| Wrong/undeclared Sequence release event | `FORM_RELEASE_SELECTOR_INVALID` or `EVENT_SELECTOR_UNDECLARED`; no release |
| Empty/duplicate FanOut branch | `FANOUT_EMPTY` / `FORM_OPERAND_DUPLICATE_KEY`; no graph |
| `quorum(0)` or above source count | `FANIN_QUORUM_OUT_OF_RANGE`; no graph |
| Late arrival rewrites frozen join | `FANIN_LATE_ARRIVAL_MUTATION`; original invocation unchanged |
| Gate zero/multiple match | `ROUTE_LABEL_UNMATCHED` / `ROUTE_LABEL_AMBIGUOUS`; no route |
| Sidecar failure implicitly controls primary | `SIDECAR_IMPLICIT_CONTROL`; no primary mutation |
| Repeat zero/unbounded/missing exhaustion | repeat bound/exhaustion defect; no graph |
| Repeat used for redelivery/retry/recovery | `REDELIVERY_RETRY_REPEAT_COLLAPSE`; reject |
| Undeclared explicit cycle | `EXPLICIT_GRAPH_UNBOUNDED_CYCLE`; no graph |
| Domain/recovery/authority/effect predicate | condition-family/domain-predicate defect; reject |
| Stale attempt or reducer version | stale defect; evidence retained, no edge release |
| Same identity, divergent bytes | identity/digest divergence; quarantine |
| Raw ARE used as admission | `ARE_EVIDENCE_UNADMITTED`; command blocked |
| Missing owner/admission reference | matching missing-reference defect; command blocked |
| Ontology `0.1.0`/`0.2.0` mismatch | `ONTOLOGY_IDENTITY_DIVERGENT`; migration blocked |

## 11. Compatibility, migration, and owner gates

Use an additive `rwo-composition-form-metamodel@candidate-1` namespace. Before migration:

1. Resolve ontology `0.1.0` versus `0.2.0`.
2. Decide whether `quorum(n)` remains kernel-owned or requires a Decision Work (`RWO-OQ-005` / `rwo:residue.005`).
3. Select exact late-arrival policy and owner.
4. Decide schema/reducer migration (`RWO-OQ-006` / `rwo:residue.006`).
5. Define minimal accepted authority reference (`rwo:residue.007`).
6. Close condition/event classification representation (`rwo:residue.011`).
7. Resolve journal truth ownership (`RWO-OQ-001`).
8. Resolve reasoning-entry, artifact-admission, and exact-effect owners (`rwo:residue.025–029`).
9. Freeze digests and byte sizes for semantic sources, machine ontology, schemas, compiler/profile, generators, validators, fixtures, projections, evidence, and receipts.
10. Implement and validate schemas/compiler/fixtures before any adoption or conformance claim.
11. Require semantic-source owner acceptance before projection regeneration; passing generation remains non-authoritative.

## 12. Candidate verdict matrix

| Surface | Verdict | Ceiling |
|---|---|---|
| Closed common envelope | RETAIN WITH CONTROLS | Candidate design |
| Seven closed payloads | RETAIN WITH SEQUENCE-CARDINALITY OWNER GATE | Candidate design |
| Four RWO-evaluable structural families | RETAIN WITH QUORUM OWNER GATE | Candidate design |
| Generic predicates/policies/evaluators | KILL | Forbidden owner collapse |
| Accepted external references | RETAIN | Reference carriage only |
| Receipt-mediated compilation lineage | RETAIN | Candidate ontology/compiler design |
| Direct `compiles-to` without receipt | REPAIR | Existing relation observed; replacement unimplemented |
| Ontology migration | BLOCKED | Identity divergence and owner gates unresolved |
| Compiler/runtime conformance | UNSUPPORTED | No implementation or finite executed witness |
| Ontology promotion/authority | NOT AUTHORIZED | `authority_effect: none` |
| Deployment/release/production | NOT IN SCOPE | No evidence |

This package is coherent enough for adversarial review and implementation planning. It does not establish adoption, schema validity, compiler execution, ontology acceptance, promotion, runtime conformance, deployment, release, or production readiness.
