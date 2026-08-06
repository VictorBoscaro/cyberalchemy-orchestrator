# Explorer transcript

This file is the parent-preserved explorer-return transcript for dispatch `2026-08-06-rwo-composition-form-metamodel`. Candidate statements remain research; source observations retain their stated proof status.

## Agent 1 — Eilenberg, Samuel

EXPLORER RETURN

Agent: Eilenberg, Samuel  
Role: explorer-form-semantics  
Verdict: PASS as candidate research; no implementation or runtime claim.

### 1. Current versus missing

Observed current model:

- The source proposes seven closed composition forms and says every convenience form compiles to event-triggered edges. Nested composites expand under one root orchestrator. [DESIGN.md SHA-256 `28b6fca…9419`, selectors `#5-the-composition-algebra` through `#57-escape-hatch-explicit-graph-composition`; observed]
- Existing invariants require typed edges, single-valued gate routes, declared fan-in ordering/release policy, bounded cycles, stable idempotency, and fail-closed unknown versions/operators. [DESIGN.md, selectors `#10-validation-invariants`, `RWO-I01`–`RWO-I12`; observed]
- The candidate ontology names `CompositionForm` and all seven subtypes, but only materially types `release-mode` and `max-rounds`; it does not provide a common form envelope, operand bindings, form instances, compilation receipts, or complete form-specific constraints. [ontology.json SHA-256 `bd0bf759…d7503`, selectors `/element_types[id=rwo:CompositionForm|Sequence|FanOut|FanIn|Gate|Sidecar|BoundedRepeat|ExplicitComposition]`, `/properties[id=rwo:p.release-mode|rwo:p.max-rounds]`; observed]
- The all-operators fixture represents forms through graph edges and auxiliary arrays, not through independently validated form definitions. [all-operators.pipeline.json SHA-256 `fb91a4b9…eb31`, selectors `/graphs/*/edges`, `/graphs/*/fan_in_policies`, `/graphs/*/sidecars`, `/graphs/*/bounded_cycles`; observed]
- The current validator checks references, required form coverage, fan-in membership, sidecar references, positive repeat bounds, and cycle declaration. It does not prove deterministic desugaring or canonical receipt equality. [validate.mjs SHA-256 `b30cde18…1be3`, selectors `lines 341-402`; observed]

Missing:

- exact `FormDefinition`/`FormInstance` distinction;
- closed operand-role schemas and cardinalities;
- deterministic ID, ordering, desugaring, and receipt rules;
- exact form-version compatibility and extension rules;
- negative defects for duplicate operands, ambiguous routes, invalid quorum, sidecar control leakage, stale versions, and divergent recompilation;
- a finite nested all-forms compilation witness.

### 2. Candidate comparison

| Candidate | Verdict | Reason |
|---|---|---|
| Universal expression tree | KILL | One evaluator would permit structural matching to absorb domain decisions, recovery choices, or authority checks. |
| Seven unrelated schemas | REJECT | Preserves local typing but duplicates identity, provenance, validation, and compiler mechanics and prevents uniform inspection. |
| Common envelope plus closed discriminated payloads | RETAIN WITH CONTROLS | Smallest model that shares structural mechanics while keeping each form’s operands and permitted structural conditions closed. |

This selection is candidate design, supported by the confirmed seed at `REFINE-SEED-PROPOSAL.md` SHA-256 `d37d3cd2…0da7`, selectors `#candidate-under-test` and `#candidate-comparisons`; it is not adopted source architecture.

### 3. Exact candidate model

```text
FormDefinition = {
  form_ref: CanonicalRef,
  form_kind: ClosedFormKind,
  form_version: ExactVersion,
  boundary_contract_ref: WorkContractRef,
  payload: KindSpecificPayload,
  provenance: {
    source_refs: [ImmutableSourceSelector...],
    source_digest: Digest
  }
}

FormInstance = {
  form_instance_id: CanonicalId,
  form_ref: CanonicalRef,
  enclosing_graph_ref: GraphRef,
  structural_path: CanonicalPath,
  operand_bindings: [OperandBinding...]
}

OperandBinding = {
  role: KindClosedRole,
  key: StableLocalKey,
  work_ref | node_ref | edge_ref | mapping_ref | policy_ref,
  authority_requirement_refs: [Reference...]
}
```

`FormDefinition` is immutable schema/provenance. `FormInstance` is structural placement. Neither is a `WorkRun`, attempt, accepted decision, recovery decision, or authority bearer.

Common fields exclude generic boolean `conditions`, arbitrary `policies`, and free-form `limits`. Those belong only in closed kind payloads or external references. This repairs the seed’s overly permissive initial envelope.

### 4. Closed per-form payloads and laws

- `Sequence`: ordered non-empty `steps`; each adjacent transition has one declared release selector, input mapping, and authority/admission references. Law: preserve declared step order; no inferred “success.”
- `FanOut`: one source release plus non-empty, uniquely keyed branches sorted by branch key during compilation. Law: permutation of serialization is immaterial after canonicalization; branch authority remains independent.
- `FanIn`: uniquely keyed non-empty sources, join Work, canonical source order, structural release policy `all | any | quorum(n)`, and closed late-arrival handling. Constraint: `1 <= n <= source_count`; reconciliation remains join-owned.
- `Gate`: decision Work and non-empty unique route-label map. Each accepted label compiles to exactly one edge; zero/multiple matches reject. Labels are opaque tokens, never interpreted as approval.
- `Sidecar`: primary plus non-empty uniquely keyed companions; closed start mode, observation selectors, finish behavior, and output-contribution flag. No implicit control edge; cancellation remains a request.
- `BoundedRepeat`: body, decision Work, distinct continue/stop labels, positive `max_rounds` or admitted budget reference, stable round-key rule, and exhaustion route. Repeat round is distinct from transport redelivery and new Work Attempt. [Recovery RESULT.md SHA-256 `da368117…e4b`, selectors `#treatment-semantics`, `#concurrency-rule`; observed owner boundary]
- `ExplicitComposition`: uniquely keyed nodes and edges, boundary mappings, output projection, typed selectors/mappings, and declared bounded cycles. It contains no convenience-form residue.

All forms are recursively nestable because operands reference `WorkDefinition`s; compilation recursively expands them into one root graph. This preserves DESIGN §4.4 and RWO-I02 without creating nested orchestrators.

### 5. Deterministic compilation

Canonical procedure:

1. Resolve exact `form_ref`, exact version, source digest, and referenced Work contracts.
2. Validate the kind-specific payload before expansion.
3. Assign structural paths from parent path plus kind and stable operand key.
4. Recursively compile child composites.
5. Emit nodes ordered lexicographically by canonical structural path.
6. Emit edges ordered by `(from_path, selector_ref, route_or_branch_key, to_path, mapping_ref)`.
7. Normalize sets by canonical key; preserve only semantically ordered lists such as Sequence steps and FanIn input order.
8. Reject duplicate canonical keys or canonical-ID collisions with divergent bytes.
9. Serialize canonical `ExplicitComposition`, calculate its digest, and emit a receipt.

```text
CompilationReceipt = {
  compiler_ref,
  compiler_version,
  form_ref,
  form_version,
  source_digest,
  input_canonical_digest,
  explicit_composition_ref,
  output_canonical_digest,
  dependency_digests: [{ref, version, digest}],
  canonicalization_profile,
  defects: []
}
```

Recompiling identical canonical inputs with the same compiler/profile must yield byte-identical explicit composition and receipt content except a separately excluded observation timestamp. A timestamp must not participate in semantic identity.

Compilation may create structural nodes, selectors, mappings, and edges only. It may not:

- interpret route labels;
- decide domain correctness;
- select recovery treatment;
- mint Work Attempts or repeat rounds;
- accept journal facts;
- satisfy ACI, authority, or effect gates;
- infer success from transport acknowledgement.

The adapter Candidate-2 explicitly preserves journal acceptance and recovery separation. [Transport adapter RESULT.md SHA-256 `0c5a44ae…c82`, selectors `#architecture`, `#identity-rule`, `#retry-and-recovery`; observed owner boundary]

### 6. Version and extension posture

- Exact major version is mandatory; unknown major or kind rejects.
- Minor additions may only add optional fields with canonical defaults that compile identically when absent.
- Any new operand role, condition family, emitted edge behavior, ordering rule, or identity rule requires a new version.
- New form kinds require a new closed discriminator and compiler implementation; extension bags and executable predicates are forbidden.
- Stored instances bind exact form, compiler, canonicalization-profile, and dependency digests.
- Historical receipts are never reinterpreted under a newer compiler; migration produces a new candidate definition and receipt.

### 7. Defect vocabulary

- `FORM_KIND_UNKNOWN`
- `FORM_VERSION_UNSUPPORTED`
- `FORM_SOURCE_DIGEST_MISMATCH`
- `FORM_OPERAND_ROLE_INVALID`
- `FORM_OPERAND_MISSING`
- `FORM_OPERAND_DUPLICATE_KEY`
- `FORM_REFERENCE_UNRESOLVED`
- `FORM_RELEASE_SELECTOR_INVALID`
- `FORM_MAPPING_INVALID`
- `FANOUT_EMPTY`
- `FANIN_EMPTY`
- `FANIN_QUORUM_OUT_OF_RANGE`
- `FANIN_ORDER_INCOMPLETE`
- `GATE_ROUTE_DUPLICATE`
- `GATE_ROUTE_UNMATCHED`
- `SIDECAR_IMPLICIT_CONTROL`
- `REPEAT_BOUND_NONPOSITIVE`
- `REPEAT_EXHAUSTION_MISSING`
- `EXPLICIT_GRAPH_UNBOUNDED_CYCLE`
- `FORM_FORBIDDEN_SEMANTIC_PREDICATE`
- `FORM_CANONICAL_ID_COLLISION`
- `COMPILATION_DIGEST_DIVERGENCE`

All definition defects reject without runtime state mutation. Runtime zero/multiple gate matches block routing without manufacturing a decision.

### 8. Required finite fixtures

Positive:

1. One nested fixture containing every form.
2. Recompile it twice and compare canonical bytes and receipt digests.
3. Permute unordered FanOut serialization and prove identical output.
4. Preserve Sequence order and canonical FanIn manifest order.
5. Compile zero-domain-semantics route labels as opaque values.

Discriminating negatives:

1. wrong Sequence release selector;
2. empty or duplicate FanOut branch;
3. `quorum(0)` and quorum greater than source count;
4. duplicate Gate route label;
5. Sidecar implicit control of primary;
6. zero/unbounded Repeat and missing exhaustion;
7. undeclared ExplicitComposition cycle;
8. generic `approved == true` predicate;
9. recovery-treatment expression inside a form;
10. authority or ACI verdict synthesized by compilation;
11. stale form/compiler version;
12. same canonical identity with divergent bytes.

### 9. Evidence ceiling and residue

The source establishes proposal-level structural semantics and partial validators. The model above is a research candidate derived from those sources. It has not been encoded, executed, promoted, or independently validated.

Residue:

- exact late-arrival policy remains an owner decision;
- whether structural `quorum(n)` belongs in the kernel remains open at DESIGN `RWO-OQ-005`;
- schema/reducer migration remains open at `RWO-OQ-006`;
- journal truth ownership remains open at `RWO-OQ-001`;
- candidate schemas and compiler fixtures still need implementation and validation;
- child Inventory remains blocked and supplied no proof.

## Agent 2 — Hewitt, Carl

EXPLORER RETURN

Agent: Hewitt, Carl  
Role: `explorer-condition-boundaries`  
Verdict: `PASS` — a universal boolean-expression or generic-policy evaluator is inadmissible. The smallest defensible model is a closed family of structurally evaluable predicates plus references to decisions, policies, limits, admissions, and prohibitions owned elsewhere.

### 1. Condition taxonomy and ownership

| Family | Object kind | Evaluator / state owner | Permitted RWO effect | Boundary |
|---|---|---|---|---|
| Event selection | Evaluable selector | RWO matcher over journal-accepted events conforming to the source Work’s `EventContract` | Mark one declared edge selector satisfied | Cannot interpret labels such as `approved` or `success` |
| Structural readiness | Evaluable predicate | RWO cursor reducer over accepted current-attempt facts | Enable a declared edge once | `all`, `any`, and `quorum(n)` measure arrivals, not quality, agreement, or authority |
| Route selection | Selector over accepted decision output | Decision Work emits the label; RWO performs exact-match routing | Select exactly one declared route | RWO never evaluates approval or domain meaning |
| Lifecycle coupling | Closed policy, not a free predicate | Sidecar policy defines coupling; target Work owns cancellation response and terminal state | Start, observe, detach, await, or issue cancellation-request | Sidecar failure or observation cannot implicitly control the primary |
| Boundedness | Limit check plus accepted debit reference | Definition/policy owner defines ceiling; journal or budget owner atomically records consumption | Permit or reject another declared round | Does not choose recovery or prove termination inside a round |
| Recovery treatment | Accepted-decision reference | `RecoveryDecisionContract@candidate-2` classifier/authority path | Follow the referenced accepted treatment | Form must not infer redelivery, retry, repeat, reconcile, compensate, or stop |
| Authority/admission | Accepted-reference requirement | Authority, ACI, artifact-admission, or effect owner | Deliver only after required accepted reference is present | Presence of an event, selector match, or schema validity cannot manufacture permission |
| Domain decision | Accepted Work output/reference | Gate or domain Work and its evidence owner | Supply a route label or referenced result | Opaque to RWO |
| ARE/ACI evidence | Evidence/admission reference, never predicate truth | ARE produces optional evidence; entry, ACI, semantic/artifact admission owners accept it | Carry an accepted reference only | Raw ARE output is neither a route decision nor authority |
| Prohibition | Validation constraint | Compiler/schema validator | Reject the definition before execution | Never dynamically “evaluated” as business policy |

Evidence: observed in `DESIGN.md` §§2–3, 5.1–5.7, 6.2–6.3, 7–8, 10–11; `ontology/ONTOLOGY.md` §§3–6, 12–13; seed §§Problem, Candidate under test, Condition families, Forms; recovery `RESULT.md` §§Exact Architecture, Treatment Semantics, Concurrency Rule, Domain And ARE; adapter `RESULT.md` §§Architecture, Identity Rule, What An Adapter May Say, Retry And Recovery. Candidate classifications above are designed, not implemented.

### 2. Adversarial counterexamples

- `event.label == "approved"` cannot be a generic boolean predicate. The label is domain-owned; RWO may only match an accepted, contract-declared route label. Treating it as approval violates `DESIGN.md` §§5.1, 5.4, 6.3 and ontology shield `rwo:f.no-terminal-success-collapse`.
- `terminal(A) && terminal(B)` is not semantic success. It may be structural readiness only when those exact current-attempt events are selected by a declared fan-in policy.
- `quorum(2)` counts two eligible source arrivals. It cannot establish independent judgment, consensus, correctness, or admission; ontology shield `rwo:f.no-structural-quorum-quality` makes that inference forbidden.
- A late third arrival after `any` or `quorum(2)` fires cannot mutate the already materialized join invocation. It remains journal evidence and may feed an explicitly declared later edge; otherwise deterministic replay would be lost.
- Cancellation is an addressed request. `cancel-requested(primary)` does not mean the primary is canceled, and parent termination does not propagate cancellation absent an explicit edge (`DESIGN.md` §§5.5, 11).
- Sidecar failure has no universal fatal meaning. A generic `sidecar.failed => primary.failed` policy would give the sidecar implicit control expressly forbidden by `DESIGN.md` §§5.5, 11.
- Redelivery, retry, and repeat are distinct identity transitions: redelivery preserves logical message and Work Attempt; retry allocates a new Work Attempt; repeat allocates a new bounded round and later child attempts. A generic `retry(condition)` collapses adapter `RESULT.md` §§Identity Rule, Retry And Recovery and recovery `RESULT.md` §Treatment Semantics.
- A stale-attempt event is retained but ineligible to release current edges (`DESIGN.md` §11). Therefore event selection must include current run/node/round/attempt fencing.
- An uncertain external effect must be reconciled or escalated by the effect/recovery owner, never converted into Work retry by a form (`Recovery RESULT.md` §Treatment Semantics; adapter `RESULT.md` §Retry And Recovery).
- Admission failure blocks the command boundary; it is not a false branch of a gate and cannot be turned into an alternative route without an accepted owner decision.
- Raw ARE evidence cannot satisfy a gate, recovery treatment, admission, or authority condition. Recovery `RESULT.md` §Domain And ARE explicitly requires entry, ACI, and semantic/artifact admission before reference.

### 3. Admissibility matrix

Legend: `E` evaluable by RWO; `M` exact-match selector; `R` accepted external reference; `P` closed policy/limit; `V` compile-time validation only; `—` inadmissible.

| Form / phase | Event | Structural | Route | Lifecycle | Bound | Recovery | Authority / admission | Domain / ARE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sequence / compile | V | V | — | — | — | — | R | — |
| Sequence / runtime | E | E | — | — | — | R | R | R only as opaque mapping input |
| FanOut / compile | V | V | — | — | — | — | R per branch | — |
| FanOut / runtime | E | E | — | — | — | R | R per command | — |
| FanIn / compile | V | V | — | — | V | — | R | — |
| FanIn / runtime | E | E (`all/any/quorum`) | — | P late-arrival handling | — | R | R for join command | Join Work owns reconciliation |
| Gate / compile | V | — | V closed labels | — | — | — | R | R decision Work |
| Gate / runtime | E | — | M exactly one | — | — | R | R for selected command | Decision Work owns meaning |
| Sidecar / compile | V | V | — | V | — | — | R | — |
| Sidecar / runtime | E | E | — | P | — | R | R | Sidecar output remains ordinary Work output |
| Repeat / compile | V | V | V continue/stop | — | V positive finite limit | R only | R | R decision Work |
| Repeat / runtime | E | E | M | — | P plus atomic debit | R | R | Decision Work owns continue/stop meaning |
| Explicit / compile | V | V | V | V | V for every cycle | R only | R | — |
| Explicit / runtime | E | E | M | P | P | R | R | Opaque |

No form may embed a general boolean expression over domain payload, recovery state, ARE conclusions, admission state, authority, or effect outcome.

### 4. Deterministic concurrency rules

1. Predicate input is only accepted, deduplicated journal history fenced to the exact graph version, run, node, round, and current attempt.
2. Each compiled edge has a stable identity and transitions from unsatisfied to satisfied at most once per declared scope.
3. Fan-in source keys and join input ordering are canonical and definition-fixed.
4. `any` selects the first eligible accepted event by the journal’s per-run ordering. No global clock order is claimed.
5. `quorum(n)` selects the first canonical set reaching `n`; require `1 <= n <= distinct declared sources`.
6. The join command and its input manifest become immutable when readiness first fires. Late arrivals cannot rewrite them.
7. Identical redelivery converges under the same logical identity; divergent bytes under one key quarantine rather than re-evaluate.
8. Competing accepted recovery decisions require the recovery contract’s atomic compare-and-accept rule. Forms cannot break the tie.
9. Stale attempts remain evidence but cannot satisfy current selectors.
10. Cancellation-request issuance and cancellation terminal observation are distinct facts.
11. Repeat continuation requires both an accepted decision label and an available/debited bound. Neither fact substitutes for the other.
12. Replay with identical ordered history and reducer version must recreate the same cursor, selected quorum set, routes, and commands (`DESIGN.md` invariants RWO-I07 and RWO-I11).

### 5. Deterministic failure vocabulary

- `FORM_CONDITION_FAMILY_FORBIDDEN`
- `FORM_CONDITION_PHASE_FORBIDDEN`
- `DOMAIN_PREDICATE_IN_KERNEL`
- `RECOVERY_DECISION_REFERENCE_MISSING`
- `AUTHORITY_REFERENCE_MISSING`
- `ADMISSION_REFERENCE_MISSING`
- `EVENT_SELECTOR_UNDECLARED`
- `EVENT_ATTEMPT_STALE`
- `ROUTE_LABEL_UNMATCHED`
- `ROUTE_LABEL_AMBIGUOUS`
- `FANIN_SOURCE_DUPLICATE`
- `FANIN_QUORUM_OUT_OF_RANGE`
- `FANIN_LATE_ARRIVAL_MUTATION`
- `SIDECAR_IMPLICIT_CONTROL`
- `CANCELLATION_STATE_COLLAPSE`
- `REPEAT_BOUND_NON_POSITIVE`
- `REPEAT_BOUND_EXHAUSTED`
- `REDELIVERY_RETRY_REPEAT_COLLAPSE`
- `EFFECT_OUTCOME_RETRY_FORBIDDEN`
- `ARE_EVIDENCE_UNADMITTED`
- `MESSAGE_IDENTITY_DIVERGENT`
- `REDUCER_VERSION_STALE`

These are candidate defect names, not currently implemented codes.

### 6. Positive and negative traces

Positive:

1. Fan-in has sources `a,b,c`, `quorum(2)`, canonical order `a,b,c`.
2. Accepted current-attempt release for `b` arrives, then `a`.
3. RWO marks two structural arrivals and freezes manifest `[a,b]` in canonical order.
4. Required join-command admission reference is accepted.
5. Join Work is invoked once. Later `c` is retained but does not mutate that invocation.
6. Join Work—not RWO—reconciles semantic meaning.

Positive repeat:

1. Decision Work emits accepted route `continue`.
2. Round limit is three; journal atomically accepts debit from round one to round two.
3. RWO creates a new round identity, then new child attempts.
4. This is neither message redelivery nor Work retry.

Negative controls:

- `terminal(review) && payload.score > 0.8` as a Sequence condition → `DOMAIN_PREDICATE_IN_KERNEL`.
- Fan-in `quorum(0)` or `quorum(4)` over three sources → `FANIN_QUORUM_OUT_OF_RANGE`.
- Gate label matches two edges → `ROUTE_LABEL_AMBIGUOUS`; no route fires.
- Sidecar failure automatically fails/cancels primary → `SIDECAR_IMPLICIT_CONTROL`.
- Repeat without positive bound or accepted budget reference → `REPEAT_BOUND_NON_POSITIVE`.
- Stale attempt emits selected release → `EVENT_ATTEMPT_STALE`; retained, no edge release.
- Unknown effect outcome triggers new Work Attempt → `EFFECT_OUTCOME_RETRY_FORBIDDEN`.
- Raw ARE verdict is used as admission → `ARE_EVIDENCE_UNADMITTED`.
- Same idempotency key with divergent bytes → `MESSAGE_IDENTITY_DIVERGENT`, quarantine.

### 7. Claim ceiling and unresolved gates

Observed source semantics support strict owner separation and fail-closed behavior. The precise taxonomy, matrix, concurrency rules, and defect vocabulary above are candidate research output only.

Still unresolved:

- whether structural quorum should remain in RWO or always be represented by a decision Work (`ontology/ONTOLOGY.md` `rwo:residue.005`);
- exact schema/reducer migration (`rwo:residue.006`);
- minimal accepted authority reference (`rwo:residue.007`);
- condition/event-classification representation (`rwo:residue.011`);
- reasoning-entry and artifact-admission owners (`rwo:residue.025–026`);
- exact-effect owner and conformance evidence (`rwo:residue.027–029`);
- runtime compiler, fixtures, and RWO/ARE/ACI conformance remain unsupported (`ontology/ONTOLOGY.md` §13).

## Agent 3 — Riehl, Emily

EXPLORER RETURN

Identity: Riehl, Emily  
Role: `explorer-ontology-validation`  
Action: `spawn-0003`  
Result: `pass`  
Posture: read-only, candidate-only, no promotion or runtime claim.

### 1. Current model and exact gap

The current ontology already makes the seven forms addressable as subtypes of `rwo:CompositionForm`, alongside `ReleasePolicy`, `SidecarLifecyclePolicy`, `EventSelector`, `InputMapping`, and `EventTriggeredEdge`. It also defines `compiles-to`, `uses-release-policy`, and `uses-lifecycle-policy` relations. Evidence: `ontology/ONTOLOGY.md#3-element-type-catalog` lines 68–115 and `#5-allowed-relation-catalog` lines 146–180; observed.

That is a vocabulary, not an exact metamodel. It lacks:

- a distinction between immutable form definition and run-bound form instance;
- typed operand bindings and operand roles;
- condition bindings with evaluator ownership;
- compiler receipts and validation defects;
- addressable late-arrival, boundedness, and compilation policies;
- cardinalities and admissibility constraints specific to each form;
- queries and negative controls for owner collapse.

This gap is explicit in the seed, `REFINE-SEED-PROPOSAL.md#Problem` lines 5–9 and `#Required-output` lines 70–81; observed candidate requirement.

The current-state evidence confirms no generic recursive graph compiler or RWO runtime exists. `rwo:finding.current.graph-expansion` is `unsupported`, and the validation receipt says runtime conformance is unsupported. Evidence: `ontology/evidence/CURRENT-STATE-2026-08-05.json#/findings/rwo:finding.current.graph-expansion`; `ontology/receipts/CURRENT-STATE-2026-08-05-VALIDATION.json#/checks/rwo-runtime-conformance`; observed.

There is also a package identity migration defect: the Markdown and current-state evidence identify `rwo-architecture@0.2.0`, while `ontology.json#/ontology` still identifies `rwo-architecture@0.1.0`. This must fail any candidate migration until all semantic, generated, view, and receipt surfaces bind one ontology identity. Evidence: `ontology/ONTOLOGY.md#1` lines 21–45; `ontology/ontology.json#/ontology`; observed.

### 2. Smallest useful candidate ontology delta

Retain the existing seven form subtype nodes. Add only concepts that change compilation, validation, provenance, or query results.

#### New node types

| Candidate ID | Meaning | Status |
|---|---|---|
| `rwo:FormDefinition` | Immutable, versioned definition carrying one closed `form_kind` payload. | designed |
| `rwo:FormInstance` | Run-bound realization of one exact `FormDefinition`; never a new semantic authority. | designed |
| `rwo:OperandBinding` | A keyed binding between a form definition and a typed operand role/work reference. | designed |
| `rwo:ConditionBinding` | Binding of one admissible structural matcher to its evaluator and phase. | designed |
| `rwo:StructuralReadinessCondition` | Closed RWO predicate over accepted structural history only. | designed |
| `rwo:EventSelectionCondition` | Matcher over declared event type, classification, and payload shape. | designed |
| `rwo:RouteMatchCondition` | Exact equality between an accepted decision-work route label and one declared route. | designed |
| `rwo:BoundAvailabilityCondition` | Structural check that an accepted finite bound has capacity; debit remains journal-owned. | designed |
| `rwo:LateArrivalPolicy` | Closed handling policy for events arriving after fan-in release. | designed |
| `rwo:CompilationReceipt` | Immutable source-to-explicit-graph lineage record with canonical digests. | designed |
| `rwo:FormValidationDefect` | Typed, path-addressed rejection produced without graph mutation. | designed |
| `rwo:CompilerProfile` | Versioned set of canonicalization and desugaring rules. | designed |

Do not add generic `Condition`, `Policy`, `Evaluator`, `Decision`, or `Authority` supernodes that imply a universal evaluator. Domain decisions, recovery decisions, authority/admission results, and effect permissions remain external accepted references. The ontology may describe their reference slots, but must not model them as RWO-evaluable predicates. This follows `DESIGN.md#Purpose` lines 34–52, `#Non-goals` lines 70–85, and the seed condition-owner table lines 33–48; observed boundary, designed delta.

Do not duplicate existing `EventSelector`, `InputMapping`, `ReleasePolicy`, `SidecarLifecyclePolicy`, `AuthorityReference`, or graph types.

#### New properties

- `rwo:p.form-ref`: stable ID plus version; `FormDefinition`; exactly one.
- `rwo:p.form-kind`: closed seven-value discriminator; `FormDefinition`; exactly one.
- `rwo:p.form-version`: immutable schema/compiler compatibility version.
- `rwo:p.operand-key`: unique within a definition.
- `rwo:p.operand-role`: closed per-form role vocabulary.
- `rwo:p.condition-family`: `structural-readiness | event-selection | route-match | bound-availability`.
- `rwo:p.evaluation-phase`: `compile | accepted-event-fold | route`.
- `rwo:p.evaluator-owner`: stable owner reference; must resolve to the RWO compiler/runtime only for the four structural families.
- `rwo:p.canonical-order-key`: explicit ordering key, never source-document array position by inference.
- `rwo:p.compiler-profile-ref`.
- `rwo:p.source-digest`, `rwo:p.output-digest`, `rwo:p.canonical-bytes-digest`.
- `rwo:p.defect-code`, `rwo:p.instance-path`.
- `rwo:p.compatibility-mode`: `exact | declared-backward-compatible`; no implicit compatibility.
- `rwo:p.authority-effect`: fixed to `none` on every new node and relation.

### 3. Relations, domain/range, and cardinalities

| Relation | Domain → range | Cardinality | Cycle rule |
|---|---|---:|---|
| `defines-form` | `CompositeWorkDefinition → FormDefinition` | exactly 1 for form-backed composites | acyclic |
| `instantiates-form` | `FormInstance → FormDefinition` | exactly 1 | acyclic |
| `binds-operand` | `FormDefinition → OperandBinding` | form-specific minimum | acyclic containment |
| `operand-references-work` | `OperandBinding → WorkDefinition` | exactly 1 | graph cycles checked separately |
| `binds-condition` | `FormDefinition → ConditionBinding` | 0..many, admissibility constrained | acyclic containment |
| `condition-specializes` | `ConditionBinding → one closed structural condition subtype` | exactly 1 | acyclic |
| `evaluated-by` | structural condition → `CompilerProfile` or root `OrchestratorKernel` | exactly 1 | acyclic |
| `uses-late-arrival-policy` | `FanIn FormDefinition → LateArrivalPolicy` | exactly 1 | acyclic |
| `compiled-under` | `CompilationReceipt → CompilerProfile` | exactly 1 | acyclic |
| `compiles-definition` | `CompilationReceipt → FormDefinition` | exactly 1 | acyclic |
| `produces-explicit-composition` | `CompilationReceipt → ExplicitComposition FormDefinition` | exactly 1 | acyclic |
| `rejects-with` | compiler validation result → `FormValidationDefect` | 1..many only on reject | acyclic |
| `cites-source` | definition/receipt/defect → evidence source | 1..many | acyclic evidence lineage |
| `carries-external-reference` | binding → accepted owner-issued reference | 0..many | acyclic; zero authority effect |

Existing `rwo:r.compiles-to` should be repaired from a bare `CompositionForm → WorkGraph` assertion into receipt-mediated lineage. A direct edge hides compiler identity, source digest, output digest, and rejection evidence. Evidence for the current direct relation: `ONTOLOGY.md#5` line 164; observed. Receipt mediation is designed.

Per-form operand cardinalities:

- `Sequence`: exactly one `predecessor`, exactly one `successor`.
- `FanOut`: exactly one `source`, at least one uniquely keyed `branch`.
- `FanIn`: at least one uniquely keyed `source`, exactly one `join`.
- `Gate`: exactly one `decision-work`, at least one uniquely labelled `route-target`.
- `Sidecar`: exactly one `primary`, at least one uniquely keyed `companion`.
- `BoundedRepeat`: exactly one `body`, exactly one `decision-work`, exactly one `exhaustion-target`.
- `ExplicitComposition`: at least one node operand; edges are explicit typed graph members.

These follow the candidate schemas in `REFINE-SEED-PROPOSAL.md#Forms-that-must-receive-exact-schemas` lines 50–58; designed, not accepted.

### 4. Integrity constraints and prohibitions

Required constraints:

1. One `FormDefinition` has exactly one kind and the payload schema for that kind only.
2. Operand keys and route labels are unique within a definition.
3. Every referenced work, selector, mapping, policy, owner reference, and schema resolves.
4. Every convenience form compiles to `ExplicitComposition` with no convenience-form residue.
5. Canonical ordering uses declared keys; object insertion order and source array order cannot silently determine graph identity.
6. Recompiling the same canonical source under the same compiler profile yields byte-identical explicit graph bytes and receipt digest.
7. A changed source digest, compiler profile, schema version, or canonicalization rule produces a distinct receipt identity.
8. Graph containment is acyclic except cycles explicitly represented by `BoundedRepeat`; each such cycle has a positive finite bound and exhaustion route.
9. `FanIn quorum(n)` requires `1 <= n <= unique_source_count`.
10. Gate label matching has exactly one target; zero or multiple matches reject.
11. Sidecars have no control relation to their primary unless an explicit ordinary gate/edge exists.
12. A condition family is admissible only for its declared form and phase.
13. Domain-result meaning, recovery selection, authority/admission, reasoning approval, and effect permission cannot be targets of `evaluated-by` from RWO.
14. Generated nodes, relations, and views must remain projections of semantic source plus evidence; they cannot become promotion authority.
15. All new relations remain non-transitive except local subtype specialization.

Add explicit shields:

- `no-condition-domain-meaning`
- `no-condition-recovery-selection`
- `no-condition-authority-admission`
- `no-condition-effect-permission`
- `no-form-retry-collapse`
- `no-form-redelivery-collapse`
- `no-sidecar-control-inference`
- `no-compiler-promotion`
- `no-generated-source-reversal`
- `no-form-instance-definition-collapse`

These extend, rather than replace, the existing non-collapse shields in `ONTOLOGY.md#6` lines 181–200.

### 5. Candidate admissibility model

| Form | Compile-time structural bindings | Runtime structural evaluation | Forbidden as RWO predicates |
|---|---|---|---|
| Sequence | source, release selector, target, mapping | accepted-event match | “successful”, “approved”, recovery choice |
| FanOut | source and non-empty keyed branches | one release match enables declared branches | independence, equal authority |
| FanIn | keyed sources, ordering, release and late-arrival policies | accepted arrivals plus `all/any/quorum` | agreement, quality, reconciliation |
| Gate | decision work and closed unique routes | exact accepted label match | approval evaluation |
| Sidecar | primary, companions, lifecycle policy | declared start/observe/finish triggers | implicit primary control or fatality |
| BoundedRepeat | body, decision work, bound, labels, exhaustion | label match plus bound availability | retry, redelivery, recovery inference |
| ExplicitComposition | closed nodes, edges, mappings, boundaries | declared edge matching only | arbitrary boolean/domain policy |

The current design directly supports these separations in `DESIGN.md#5.1–5.7` lines 171–220 and `#Runtime-flow` lines 304–330; observed design, candidate exactness designed.

### 6. Query architecture

The candidate graph should answer, without inspecting prose:

- Which form definitions compile under compiler profile X?
- Which exact operands and roles belong to form Y?
- Which conditions may be evaluated by RWO at runtime?
- Which bindings carry external decision, recovery, admission, authority, or effect references?
- Which definitions contain bounded cycles, and where are their exhaustion routes?
- Which fan-ins lack canonical ordering or valid quorum bounds?
- Which gates have duplicate, missing, or unmatched route labels?
- Which sidecars have a prohibited implicit control path to a primary?
- Which receipts bind a given source digest to a given explicit graph digest?
- Which generated nodes lack semantic-source provenance?
- Which ontology identity/version appears across semantic source, projection, view, and receipt surfaces?
- Which candidate objects have `authority_effect != none` or imply promotion?
- Which defects and negative fixtures exercise each retained constraint?

The existing `views/current-state.json` covers all current nodes and relations exactly once but exposes no query collection; its `queries` surface is empty. Evidence: `ontology/views/current-state.json#/groups`, `#/sequences`, and absent/empty query surface; observed.

### 7. Fixtures and negative controls

Positive fixtures:

- one minimal valid fixture per form;
- one nested all-seven-form fixture;
- deterministic recompile fixture with identical graph and receipt digests;
- fan-in `all`, `any`, and boundary-valid quorum fixtures;
- explicit bounded cycle with exhaustion;
- generated graph/view coverage fixture.

Discriminating negatives:

- unknown form kind or payload field;
- zero operands or duplicate operand key;
- sequence selector absent or not declared by source contract;
- empty fan-out or duplicate branch key;
- fan-in `quorum(0)`, quorum above source count, duplicate source, missing order, and undeclared late-arrival policy;
- gate zero match, duplicate label, and multiple target match;
- sidecar implicit control edge or undeclared cancellation authority;
- repeat zero/unbounded bound, missing exhaustion route, redelivery/retry represented as repeat, or reused round identity;
- unbounded explicit graph cycle;
- domain/recovery/reasoning/authority/effect object attached as an RWO-evaluable condition;
- stale schema/compiler version;
- source digest mismatch or divergent output under identical inputs;
- missing owner/admission reference;
- generated node lacking source lineage;
- ontology identity mismatch across `ONTOLOGY.md`, `ontology.json`, evidence, views, and receipts;
- any `authority_effect` other than `none`.

The current validator already supplies useful precedents: closed schemas, unique IDs, endpoint resolution, source/residue resolution, deterministic regeneration, complete view coverage, source-hash checking, and two negative fixtures for authority effect and missing endpoints. Evidence: `ontology/scripts/validate-graph.mjs#validateClosedSchema`, `#validateEndpoint`, `#validateSourceHashes`, and `#validateGraph`; observed. It does not validate the proposed form metamodel; designed extension only.

### 8. Compatibility and migration

Use an additive candidate namespace/version first, such as `rwo-composition-form-metamodel@candidate-1`; do not silently rewrite `rwo-architecture@0.2.0`.

Migration gates:

1. Resolve the current `0.1.0` versus `0.2.0` ontology identity divergence.
2. Freeze digests for semantic ontology source, machine ontology, schemas, generator, validator, fixtures, generated nodes/relations/views, and validation receipt.
3. Map each existing seven-form node to the new `FormDefinition` model without changing its proposal-only posture.
4. Convert direct `compiles-to` assertions into receipt-mediated compilation lineage.
5. Preserve all existing source references, residue, forbidden inferences, and authority effect.
6. Reject unknown extensions by default. A new form or condition family requires a new metamodel version, explicit owner route, schema, compiler rule, fixtures, migration declaration, and validation receipt.
7. Regenerate projections only after semantic-source acceptance by the proper owner; successful generation and validation remain non-authoritative.

### 9. Source-digest obligations

Every candidate validation receipt must bind exact SHA-256 digests and byte sizes for:

- `DESIGN.md`;
- `ontology/ONTOLOGY.md`;
- `ontology/ontology.json`;
- every form/condition schema;
- compiler profile and compiler implementation;
- graph generator and validators;
- all positive and negative fixtures;
- generated nodes, relations, and views;
- current-state evidence inputs;
- the receipt itself through an externally anchored manifest.

Observed hashes relevant to this read-only exploration include:

- `DESIGN.md`: `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`
- `ONTOLOGY.md`: `b0b83ea540c0f805208b93e068816c45cb928d4f08eea50eca8ba4178843d9e1`
- `ontology.json`: `bd0bf759862e77032cf1ca62fceea2a785628626e48ea3b01b5caf47180d7503`
- `build-graph.mjs`: `0599bee98272c892e4457b5d1b22d46ff7430654e8ab824bbe5fdbdecda3507c`
- `validate-graph.mjs`: `76b315b898ca36f2c8cb31e4b329ff2fc35566cb0ca0e190e622852afd7c37b4`
- `all-operators.pipeline.json`: `fb91a4b91fdd80dfb0a723840dda49df58770b17d10b91e441b9e66d8a5beb31`

These identify observed bytes only; they do not accept or promote the candidate.

### 10. Verdict

Select the common closed envelope plus discriminated family payload, provided the candidate uses typed structural conditions and external owner references rather than a universal condition evaluator.

Reject:

- the universal boolean-expression tree, because it cannot prevent domain, recovery, reasoning, or authority evaluation;
- seven unrelated schemas, because they duplicate identity, provenance, compiler lineage, defects, and validation mechanics;
- ornamental aliases for existing selectors, mappings, policies, graph elements, receipts, or owner objects;
- any relation that lets compilation, graph containment, generated projections, or successful validation create authority or promotion.

The result is implementation-ready research architecture only. It proves neither implementation, ontology acceptance, promotion, runtime conformance, deployment, release, nor production readiness.
