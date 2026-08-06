# Revised Synthesis Return

- Agent: Mac Lane, Saunders
- Feedback loop: 1/1, exhausted
- Target verdict: `READY_FOR_FINDINGS_AND_VALIDATION_FIRST_PLANNING_ONLY`
- Claim ceiling: not ready for adoption, ontology migration, compiler/runtime conformance, promotion, deployment, release, or production.

## 1. Exact disposition

Survives:

- the existing `CompositionForm` taxonomy and seven subtypes;
- an immutable authored form as one concrete instance of an existing subtype, enclosed by `CompositeWorkDefinition`;
- closed per-form operand fields;
- existing `EventSelector`, `InputMapping`, `ReleasePolicy`, and `SidecarLifecyclePolicy` owners;
- exact opaque-label Gate routing;
- definition-owned finite repeat limits with debit/acceptance externally owned;
- immutable non-authorizing `CompilerProfile`;
- disjoint `CompilationSuccess` and `CompilationRejection`;
- result-mediated compilation from source syntax to `WorkGraph`;
- compiler-owned structural defects;
- typed references to external owners;
- planned fixture contracts as validation-first inputs;
- every owner and migration gate.

Killed:

- parallel `FormDefinition` ontology type;
- runtime-shaped `FormInstance`;
- generic `OperandBinding.target` union;
- `ConditionBinding` and all proposed condition subtype nodes;
- generic `evaluated-by`;
- generic condition/evaluator/policy/external-reference/decision/authority/admission nodes;
- unified defect vocabulary across unrelated owners;
- one `CompilationReceipt` shape mixing success and rejection;
- `produces-explicit-composition`, because `ExplicitComposition` is source syntax rather than compiler output;
- any claim that a scenario checklist is finite or executed non-vacuity evidence.

Still blocked: Sequence cardinality, structural quorum ownership, late-arrival behavior/owner, ontology identity/migration, journal truth/reducer migration, exact typed authority/admission references, ARE/ACI entry and artifact admission, exact-effect ownership, and conformance.

## 2. Repaired source model

An authored definition is not a new ontology type. It is one immutable node typed as exactly one existing subtype:

```text
Sequence | FanOut | FanIn | Gate |
Sidecar | BoundedRepeat | ExplicitComposition
```

It is enclosed by one `CompositeWorkDefinition`:

```text
authored_form {
  id: CanonicalSourceId
  type: one existing CompositionForm subtype
  schema_ref: ExactSchemaRef
  payload: ExactSubtypePayload
  provenance: NonEmpty<ImmutableSourceSelector>
}
```

The subtype is the discriminator; no duplicate `form_kind` is present. `schema_ref` owns the exact version/schema identity; the candidate does not create a second version authority.

No `FormInstance` is added. An optional compile-time-only `FormOccurrence { authored_form_ref, source_path }` is permitted only if a reused authored form needs addressable path diagnostics. It has no runtime identity, state, operands, lifecycle, authority, or compiler ownership. If a defect can carry `source_path` directly, the occurrence object is omitted.

## 3. Closed per-form operands

There is no universal target union and external owner references are not operands.

| Existing subtype | Closed operand surface | Non-operand configuration |
|---|---|---|
| `Sequence` | `steps: OrderedList<WorkDefinitionRef>` | Existing `EventSelector` and `InputMapping` per adjacent transition. Minimum cardinality remains an owner gate. |
| `FanOut` | `source`; `branches: NonEmptyMap<BranchKey, WorkDefinitionRef>` | One existing release selector; per-branch mappings and typed delivery requirements. |
| `FanIn` | `sources: NonEmptyMap<SourceKey, WorkDefinitionRef>`; `join` | Existing `ReleasePolicy`; canonical source order; no late-arrival policy until its owner is chosen. |
| `Gate` | `decision_work`; `route_targets: NonEmptyMap<OpaqueRouteLabel, WorkDefinitionRef>` | Existing selectors/mappings; decision Work owns label meaning. |
| `Sidecar` | `primary`; `companions: NonEmptyMap<CompanionKey, WorkDefinitionRef>` | Existing lifecycle policy, observation selectors, mappings, typed command requirements. |
| `BoundedRepeat` | `body`; `decision_work`; `exhaustion_target` | Opaque continue/stop labels, finite definition limit, round-key rule, mappings, typed requirements. |
| `ExplicitComposition` | `nodes: NonEmptyMap<NodeKey, WorkDefinitionRef>`; `edges: List<EventTriggeredEdge>` | Boundary mappings, output projection, declared finite-cycle data. It remains authored source syntax. |

Operand keys are unique within their exact closed field. Existing `references-work`, selector, mapping, release, lifecycle, and graph relations are reused or narrowed. Sequence remains `steps`; binary versus n-ary minimum is not silently decided.

## 4. No generic condition/evaluator layer

| Structural concern | Reused representation | Deciding owner |
|---|---|---|
| Event selection | Existing `EventSelector` on `EventTriggeredEdge` | RWO matches journal-accepted, correctly fenced events. |
| FanIn readiness | Existing `ReleasePolicy` | RWO folds eligible structural arrivals; quorum is owner-gated. |
| Gate route | Opaque label in declared route map | Decision Work owns meaning; RWO performs exact equality only. |
| Sidecar coupling | Existing `SidecarLifecyclePolicy` | Policy states permitted direction; target Work owns terminal response. |
| Repeat bound | Definition limit plus typed debit reference | Definition declares; journal/budget owner decides/records debit. |
| Domain/recovery/authority/admission/effect | Exact typed external reference | External owner accepts/rejects it; RWO never evaluates its meaning. |
| Forbidden composition | Compiler invariant | Compiler rejects source structure before graph output. |

Release means structural eligibility only—not success, approval, truth, permission, agreement, admission, or effect safety.

## 5. Typed external-owner references

Permitted slots reference exact owner contracts, for example:

```text
RecoveryDecisionRef
AuthorityVerificationRef
ACIAdmissionRef
ArtifactAdmissionRef
AREEvidenceRef
EffectPermissionRef
BudgetDebitRef
JournalAcceptanceRef
```

Their schemas remain external-owner concerns. A form/compiler checks only the exact permitted reference type for that slot, syntactic shape, declared source owner, stable identity, and resolvability where available. A reference does not perform acceptance, grant authority, authorize an effect, admit an artifact, or establish truth. Delivery/effect execution requires the independently accepted owner verdict. Existing `requires-authority` is reused for authority.

## 6. Disjoint compilation results

Every accepted source form—including `ExplicitComposition`—compiles to a `WorkGraph`.

```text
CompilationSuccess {
  result_kind: "success"
  source_form_ref
  source_occurrence_path?
  compiler_profile_ref
  compiler_version
  raw_source_bytes_domain
  raw_source_digest
  canonical_input_bytes_domain
  canonical_input_digest
  dependency_digests: [{ref, version, byte_domain, digest}]
  output_work_graph_ref
  output_graph_bytes_domain
  output_graph_digest
}
```

```text
CompilationRejection {
  result_kind: "rejection"
  source_form_ref
  source_occurrence_path?
  compiler_profile_ref
  compiler_version
  raw_source_bytes_domain
  raw_source_digest
  canonical_input_bytes_domain?
  canonical_input_digest?
  defects: NonEmpty<FormCompilationDefect>
}
```

A success has one output graph and no defects. A rejection has non-empty compiler defects and no graph/output digest. Timestamps stay outside semantic identity. Raw-source and canonical-input digests name different byte domains. `CompilerProfile` is immutable canonicalization/desugaring configuration—not plugin surface, evaluator, policy, proof, authority, or promotion.

Candidate repair of existing lineage:

```text
authored CompositionForm
  --compiles-to--> CompilationSuccess
  --produces-work-graph--> WorkGraph

authored CompositionForm
  --compilation-rejected-as--> CompilationRejection
  --rejects-with--> FormCompilationDefect
```

Changing the current `compiles-to` range is an ontology migration and remains blocked.

## 7. Deterministic compiler boundary

The compiler may resolve exact existing subtype/schema/profile/operands/selectors/mappings/policies/reference declarations; validate closed syntax/reference shapes/closed cardinalities/graph invariants; derive source paths; recursively expand convenience forms; emit nodes by canonical source path; emit edges by `(from_path, selector_ref, route_or_branch_key, to_path, mapping_ref)`; preserve semantic lists and sort key-defined sets; reject duplicate keys/divergent canonical identities; and return exactly one success or rejection.

It may not accept journal events, match runtime events, fold cursors, interpret domain labels, decide open quorum semantics, select recovery, mint attempts/rounds/decisions/admission/authority/permission, infer transport success, migrate ontology, or promote anything.

Compile rejection may emit a rejection result only. It emits no graph, success, runtime state, journal record, cursor, command, attempt, round, debit, or external-owner verdict.

## 8. Defects split by owner and phase

Compiler-owned `FormCompilationDefect` is restricted to source syntax and graph structure:

`FORM_SCHEMA_UNSUPPORTED`, `FORM_SOURCE_DIGEST_MISMATCH`, `FORM_OPERAND_MISSING`, `FORM_OPERAND_KEY_DUPLICATE`, `FORM_REFERENCE_UNRESOLVED`, `FORM_SELECTOR_UNDECLARED`, `FORM_MAPPING_INVALID`, `SEQUENCE_CARDINALITY_INVALID` (owner-gated), `FANOUT_EMPTY`, `FANIN_EMPTY`, `FANIN_SOURCE_DUPLICATE`, `FANIN_ORDER_INCOMPLETE`, `FANIN_QUORUM_OUT_OF_RANGE` (owner-gated), `GATE_ROUTE_LABEL_DUPLICATE`, `SIDECAR_CONTROL_DIRECTION_FORBIDDEN`, `REPEAT_BOUND_MISSING`, `REPEAT_BOUND_NON_POSITIVE`, `REPEAT_EXHAUSTION_MISSING`, `EXPLICIT_GRAPH_CYCLE_UNBOUNDED`, `CANONICAL_ID_BYTES_DIVERGENT`.

Runtime outcomes are not compiler defects: selector no-match, stale-attempt ineligibility, unmatched Gate label, corruption-detected route ambiguity, frozen FanIn manifest, retained late arrival, repeat exhausted, stale reducer block.

Journal owns duplicate/redelivery, divergent-message quarantine, debit acceptance/rejection, ordering, and fences. Recovery, authority, admission, ARE/ACI, adapter, and exact-effect owners keep their typed results. Ontology identity divergence is a migration blocker, not a form defect.

## 9. Frozen non-collapse rules

Sidecar lifecycle may couple primary observations to companion start/observe/await/detach/cancellation-request actions. Companion state cannot directly fail, cancel, retry, or mutate the primary. Companion-to-primary influence uses an ordinary declared edge plus the applicable decision and accepted authority/admission gates. Cancellation request is not terminal cancellation, and nesting never implies propagation.

| Mechanism | Identity/state boundary |
|---|---|
| Transport redelivery | Same logical message and Work attempt; journal deduplicates/quarantines. |
| Work retry | New Work attempt under recovery owner. |
| BoundedRepeat | New declared repeat-round identity, then child attempts; requires accepted opaque label and finite-bound debit. |
| Domain rework | Domain-owned cycle/decision; never inferred as transport retry or repeat. |
| Replay/resume | Recompute from accepted history/version; no new semantic acceptance or external calls. |
| Recovery classification | Owner-issued recovery decision reference; not the treatment itself. |
| Effect reconciliation/retry | Effect-owner controlled; uncertain outcome cannot infer Work retry. |

## 10. Planned fixture contract, not evidence

Every future fixture must bind: fixture ID, owner dependencies, phase, exact input bytes/size/digest, compiler/reducer/profile versions, initial graph/journal/cursor/command state, exactly one expected result, exact output bytes/size/digest where applicable, allowed/forbidden mutations, validation command, and validation receipt.

Planned compiler fixtures include one valid fixture per form; nested all-seven form; deterministic recompile; keyed FanOut permutation; Sequence order/selector negatives; FanOut empty/duplicate; FanIn duplicate/order/quorum boundaries; Gate duplicate label; Sidecar control direction; Repeat missing/non-positive/exhaustion; bounded/unbounded Explicit cycle; unsupported selector/schema; source digest mismatch; and divergent canonical ID bytes.

Planned runtime/owner fixtures include ordinary selector no-match, stale attempt, unmatched Gate, explicit corrupted-route ambiguity, Sidecar companion failure, Repeat exhaustion, transport redelivery, Work retry, bounded repeat continuation, replay/resume, uncertain effect, raw ARE-as-admission, divergent message bytes, and late arrival with frozen join.

Each fixture gets one result and an explicit mutation boundary. None exists or has run; this list is a validation-first contract only.

## 11. Minimal ontology delta

Candidate additions are limited to genuinely non-aliased concepts:

- optional compile-only `FormOccurrence`, only if path diagnostics cannot stay embedded;
- immutable non-authorizing `CompilerProfile`;
- disjoint `CompilationSuccess`;
- disjoint `CompilationRejection`;
- compiler-owned `FormCompilationDefect`.

No form-definition supertype, condition/evaluator taxonomy, generic reference/policy, or runtime identity is added. Existing form subtype, enclosing composite, selector, mapping, release, lifecycle, references-work, graph, and authority relations are reused. `compiles-to` is repaired into success-mediated lineage; rejection lineage is separate; success targets exactly one `WorkGraph`; both result kinds bind one immutable profile; external references use exact owner-specific relations only.

Queries must distinguish source syntax/output graph, success/rejection, compiler defect/runtime or external result, owner relation/alias, optional occurrence/WorkNode/runtime identities, typed reference presence/owner acceptance, and semantic source/generated projection/validation/promotion.

## 12. Preserved gates and verdict matrix

Before an adoption proposal: decide Sequence cardinality; quorum owner; late-arrival owner/behavior; ontology identity/migration; schema/reducer compatibility and journal truth; exact typed owner-reference contracts; exact-effect conformance; canonical provenance; and whether `FormOccurrence` is needed. Then implement schemas, serialized fixtures, compiler/validators, canonical bytes/digests, commands, and receipts.

| Surface | Revised verdict |
|---|---|
| Existing seven-form taxonomy | RETAIN |
| Authored form under existing subtype | RETAIN |
| Parallel `FormDefinition` | KILL |
| Runtime-shaped `FormInstance` | KILL |
| Optional compile-only `FormOccurrence` | CONDITIONAL |
| Closed per-form operands | RETAIN, Sequence cardinality gated |
| Existing selectors/release/lifecycle owners | REUSE |
| Generic condition/evaluator layer | KILL |
| Typed external owner references | RETAIN AS REFERENCES ONLY |
| Disjoint compilation results to `WorkGraph` | RETAIN AS CANDIDATE |
| `ExplicitComposition` as compiler output | KILL; source only |
| Unified defects | KILL |
| Compiler structural defects | RETAIN AS CANDIDATE |
| Scenario list as executed evidence | KILL |
| Planned fixture contracts | RETAIN |
| Findings/validation-first planning | READY |
| Adoption/ontology migration | BLOCKED |
| Compiler/runtime conformance | UNSUPPORTED |
| Promotion/deployment/release/production | NOT AUTHORIZED |

Evidence ceiling: this revision repairs definitions, owners, compilation lineage, and validation planning. It supplies no implementation, serialized fixture corpus, executed validation, compiler/runtime conformance, ontology acceptance, authority, promotion, deployment, release, or production evidence.
