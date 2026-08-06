# Findings — RWO Composition-Form Metamodel

- Dispatch: `refine-20260806T173343Z-rwo-composition-form-metamodel`
- Evidence closure: `ready`
- Ready for: findings and validation-first planning only
- Authority effect: `none`
- Claim ceiling: candidate design; no adoption, ontology migration, implementation, compiler/runtime conformance, authority, promotion, deployment, release, or production evidence

## Plain-language answer

RWO does not need a new universal expression language or a generic condition engine. It already has the right seven authored composition forms: `Sequence`, `FanOut`, `FanIn`, `Gate`, `Sidecar`, `BoundedRepeat`, and `ExplicitComposition`. The smallest coherent next design is to make each authored form an immutable instance of exactly one of those existing subtypes, give every subtype its own closed payload, and compile every accepted form—including explicit graph syntax—into a `WorkGraph` through a disjoint success result. A rejected form produces defects and no graph.

This keeps RWO structural. It may validate syntax, graph shape, selectors, mappings, declared references, and closed invariants. It may not decide what an approval means, whether recovery is appropriate, whether authority exists, whether an artifact is admitted, or whether an effect is safe. Those decisions remain with their existing owners. The candidate is internally coherent enough to plan exact schemas, fixtures, and validation, but there are no serialized fixtures, compiler bytes, runtime executions, or conformance receipts yet. [Observed basis: [`DESIGN.md` §§1–3, 5, 8, 10](../../../../DESIGN.md); [`ONTOLOGY.md` §§1, 3–6, 13](../../../../ontology/ONTOLOGY.md). Designed repair: [`synthesis-revised.md` §§1–12](synthesis-revised.md), exact-bound after [`review-precedent.md`](review-precedent.md), [`review-non-vacuity.md`](review-non-vacuity.md), and [`review-definitional.md`](review-definitional.md).]

## Evidence posture and traceability limit

“Observed” below means present in the current candidate sources that this writer was allowed to inspect. It does not mean implemented or freshly executed. “Designed” means the repaired, evidence-closed proposal in `synthesis-revised.md`. The closure hashes for that synthesis, all three reviews, and their receipts matched `evidence-closure.json` before this file was written.

The writer action did not admit the original explorer returns as direct inputs. Explorer reasoning is therefore cited indirectly through the exact-bound revised synthesis and reviewer chain; no row below claims direct explorer-return attribution. That narrowed traceability is sufficient for findings and validation-first planning, but not for implementation, conformance, adoption, or promotion.

## Current versus missing

| Surface | Current observed model | Missing or unresolved |
|---|---|---|
| Form taxonomy | `CompositionForm` with seven existing subtypes. [`ONTOLOGY.md` §3](../../../../ontology/ONTOLOGY.md); `ontology.json#/element_types` | Closed executable schemas for their authored payloads. |
| Composition output | Convenience forms compile to event-triggered graph structure; `rwo:r.compiles-to` currently runs directly from `CompositionForm` to `WorkGraph`. [`DESIGN.md` §5](../../../../DESIGN.md); [`ONTOLOGY.md` §5](../../../../ontology/ONTOLOGY.md); `ontology.json#/relations/rwo:r.compiles-to` | Result-mediated success/rejection lineage, compiler/profile schemas, canonical bytes, and conformance. |
| Structural owners | Existing `EventSelector`, `InputMapping`, `ReleasePolicy`, `SidecarLifecyclePolicy`, `WorkGraph`, `WorkNode`, and `EventTriggeredEdge`. [`ONTOLOGY.md` §§3–5](../../../../ontology/ONTOLOGY.md); `ontology.json#/element_types` and `#/relations` | Exact per-form use of those owners; Sequence minimum cardinality; quorum ownership; late-arrival behavior. |
| Runtime boundary | Root runtime consumes accepted events, evaluates declared edges, maps target input, checks command authority/idempotency, and issues commands. [`DESIGN.md` §§6.3, 7–8](../../../../DESIGN.md) | Compiler/runtime implementation and executed reducer, cursor, routing, and concurrency conformance. |
| Domain and authority boundary | Domain meaning stays with Work; authority is referenced and checked at external boundaries; structural facts do not imply approval, truth, or permission. [`DESIGN.md` §§1–3, 5.4, 6.3, 10](../../../../DESIGN.md); [`ONTOLOGY.md` §6](../../../../ontology/ONTOLOGY.md) | Exact typed authority, ACI, artifact-admission, ARE, budget, journal-acceptance, and effect-owner contracts. |
| Retry and recovery | Candidate-2 separates redelivery, Work retry, repeat rounds, replay, recovery decisions, and exact-effect handling. [Observed candidate design: recovery Candidate-2 §§5–10; adapter Candidate-2 §§1–6.] | Owner integration and runtime conformance; journal/domain truth; exact-effect schemas. |
| Ontology identity | Markdown declares `rwo-architecture@0.2.0`; machine JSON declares `rwo-architecture@0.1.0`. [`ONTOLOGY.md` §1](../../../../ontology/ONTOLOGY.md); `ontology.json#/ontology` | Owner-approved identity reconciliation and migration. This is not a compiler defect. |
| Validation | Existing candidate ontology reports graph-package validation and explicitly reports RWO implementation/runtime conformance unsupported. [`ONTOLOGY.md` §13](../../../../ontology/ONTOLOGY.md) | Serialized form fixtures, exact inputs/outputs/digests, compiler/validator commands, and current-run receipts. |

## Selected, rejected, and killed surfaces

Selected as the repaired candidate:

- immutable authored forms typed as exactly one existing subtype and enclosed by one `CompositeWorkDefinition`;
- closed per-form operand fields, with selectors, mappings, release, lifecycle, and owner references kept outside a universal operand union;
- exact opaque-label routing for `Gate`;
- finite definition-owned repeat bounds with debit/acceptance externally owned;
- immutable, non-authorizing `CompilerProfile`;
- disjoint `CompilationSuccess` and `CompilationRejection`;
- result-mediated compilation to `WorkGraph`;
- compiler-only structural defects;
- exact typed, non-authorizing references to external owners;
- a planned fixture contract as the first validation input.

Rejected or killed:

- a parallel `FormDefinition` type;
- runtime-shaped `FormInstance`;
- generic `OperandBinding.target` union;
- `ConditionBinding`, condition subtype nodes, and generic `evaluated-by`;
- generic policy, external-reference, decision, authority, or admission nodes;
- a unified cross-owner defect vocabulary;
- one receipt shape mixing success and rejection;
- `produces-explicit-composition`, because `ExplicitComposition` is authored source syntax, not compiler output;
- any claim that the planned scenario list is serialized, finite non-vacuity evidence, or executed proof.

[Designed disposition: [`synthesis-revised.md` §§1–2, 11–12](synthesis-revised.md). Precedent repair: [`review-precedent.md` “Type gate”, “Relation gate”](review-precedent.md). Definitional repair: [`review-definitional.md` “Candidate verdicts”, “Required non-collapse repairs”](review-definitional.md). Non-vacuity limit: [`review-non-vacuity.md`](review-non-vacuity.md).]

## Exact existing-subtype authored-form model

An authored form is one immutable source node under one existing subtype. The subtype is the sole discriminator; there is no duplicate `form_kind` or second version owner.

```text
authored_form {
  id: CanonicalSourceId
  type: Sequence | FanOut | FanIn | Gate |
        Sidecar | BoundedRepeat | ExplicitComposition
  schema_ref: ExactSchemaRef
  payload: ExactSubtypePayload
  provenance: NonEmpty<ImmutableSourceSelector>
}

CompositeWorkDefinition
  --encloses exactly one authored form source-->
authored_form
```

`schema_ref` owns exact schema/version identity. `provenance` identifies immutable source selectors. The source node is not a `WorkRun`, `Attempt`, `WorkNode`, or executing graph. No `FormInstance` is added. A compile-only `FormOccurrence { authored_form_ref, source_path }` is conditional: add it only if reused form diagnostics require independently addressable occurrences; otherwise put `source_path` directly on defects. It may never acquire runtime state, operands, lifecycle, authority, or compiler ownership. [Observed distinction: [`DESIGN.md` §§4.1–4.4](../../../../DESIGN.md); [`ONTOLOGY.md` §§2–3](../../../../ontology/ONTOLOGY.md). Designed repair: [`synthesis-revised.md` §2](synthesis-revised.md); [`review-definitional.md` `FormDefinition`/`FormInstance`](review-definitional.md).]

### Seven closed payloads

The following is the complete candidate payload surface. `WorkDefinitionRef` is the only work operand type. Typed external-owner references are configuration/gates, never operands. Every map key is unique within its exact field.

```text
SequencePayload {
  steps: OrderedList<WorkDefinitionRef>
  adjacent_transitions: OrderedList<{
    event_selector_ref: EventSelectorRef
    input_mapping_ref: InputMappingRef
  }>
}
```

The transition at index `i` connects `steps[i]` to `steps[i+1]`. Sequence order is semantic. The minimum allowed number of steps remains an owner gate; the compiler must not silently choose binary or n-ary semantics.

```text
FanOutPayload {
  source: WorkDefinitionRef
  branches: NonEmptyMap<BranchKey, WorkDefinitionRef>
  release_selector_ref: EventSelectorRef
  branch_input_mappings: ExactKeyMap<BranchKey, InputMappingRef>
  branch_delivery_requirement_refs: ExactKeyMap<BranchKey, DeliveryRequirementRef>
}
```

Branch keys are unique and canonical; key order is not branch meaning. Empty or duplicate branches reject.

```text
FanInPayload {
  sources: NonEmptyMap<SourceKey, WorkDefinitionRef>
  join: WorkDefinitionRef
  release_policy_ref: ReleasePolicyRef
  canonical_source_order: ExactPermutation<SourceKey>
  join_input_mapping_ref: InputMappingRef
}
```

No late-arrival policy is admitted until its behavior and owner are selected. Quorum shape/range remains owner-gated; structural release never means quality, consensus, truth, or approval.

```text
GatePayload {
  decision_work: WorkDefinitionRef
  route_targets: NonEmptyMap<OpaqueRouteLabel, WorkDefinitionRef>
  route_selectors: ExactKeyMap<OpaqueRouteLabel, EventSelectorRef>
  route_input_mappings: ExactKeyMap<OpaqueRouteLabel, InputMappingRef>
}
```

The decision Work owns label meaning. RWO performs exact equality against the declared map. Duplicate labels are compile-invalid; zero runtime match blocks; runtime multiple-match behavior exists only for explicit corrupt or migrated state.

```text
SidecarPayload {
  primary: WorkDefinitionRef
  companions: NonEmptyMap<CompanionKey, WorkDefinitionRef>
  lifecycle_policy_ref: SidecarLifecyclePolicyRef
  observation_selectors: ExactKeyMap<CompanionKey, NonEmptyList<EventSelectorRef>>
  companion_input_mappings: ExactKeyMap<CompanionKey, InputMappingRef>
  companion_command_requirement_refs:
    ExactKeyMap<CompanionKey, CommandRequirementRef>
}
```

Lifecycle configuration can request start/observe/await/detach/cancellation-request behavior. It cannot give a companion direct control over primary state.

```text
BoundedRepeatPayload {
  body: WorkDefinitionRef
  decision_work: WorkDefinitionRef
  exhaustion_target: WorkDefinitionRef
  continue_label: OpaqueRouteLabel
  stop_label: OpaqueRouteLabel
  max_rounds: PositiveInteger
  round_key_rule_ref: RoundKeyRuleRef
  route_input_mappings: {
    continue: InputMappingRef
    stop: InputMappingRef
    exhaustion: InputMappingRef
  }
  budget_debit_ref: BudgetDebitRef
  delivery_requirement_refs: NonEmptyList<DeliveryRequirementRef>
}
```

The definition declares the finite limit. The journal/budget owner decides and records debit. Repeat continuation requires an accepted opaque label and accepted debit; it is not a Work retry.

```text
ExplicitCompositionPayload {
  nodes: NonEmptyMap<NodeKey, WorkDefinitionRef>
  edges: List<EventTriggeredEdge>
  boundary_input_mappings: List<InputMappingRef>
  output_projection_ref: OutputProjectionRef
  finite_cycle_declarations: List<{
    cycle_ref: CycleRef
    bound_ref: BoundRef
    exhaustion_route_ref: RouteRef
  }>
}
```

`ExplicitComposition` remains authored source syntax. Accepted explicit syntax still compiles to a `WorkGraph`; bounded cycles are allowed only with declared finite bound and exhaustion route.

[Observed owners and semantics: [`DESIGN.md` §§5.1–5.7, 10](../../../../DESIGN.md); [`ONTOLOGY.md` §§3–6](../../../../ontology/ONTOLOGY.md); `ontology.json#/element_types`, `#/relations`, and `#/constraints/RWO-I03..I06`. Designed payloads: [`synthesis-revised.md` §§2–3](synthesis-revised.md). Reviewer constraints: [`review-precedent.md` “Type gate”](review-precedent.md), [`review-definitional.md` “Candidate verdicts”](review-definitional.md), [`review-non-vacuity.md` “Witness repairs”](review-non-vacuity.md).]

## No-generic-condition owner matrix

| Concern | Representation | Phase and deciding owner | RWO/compiler may do | Must not collapse into |
|---|---|---|---|---|
| Event selection | existing `EventSelector` on `EventTriggeredEdge` | Runtime; root RWO matches journal-accepted, correctly fenced events | Resolve selector declaration; runtime exact match | Domain meaning or success inference |
| FanIn readiness | existing `ReleasePolicy` | Runtime structural fold; quorum owner still open | Validate declaration; fold eligible structural arrivals after ownership closes | Quality, agreement, truth, or consensus |
| Gate routing | opaque label plus declared route map | Decision Work owns meaning; RWO owns exact equality | Validate unique labels; route one exact match | Approval evaluator or confirmation owner |
| Sidecar coupling | existing `SidecarLifecyclePolicy` | Definition policy plus target Work terminal response | Validate permitted direction and declared actions | Companion control of primary state |
| Repeat bound | definition limit plus `BudgetDebitRef` | Definition declares; journal/budget owner accepts and records debit | Validate positive finite declaration and reference shape | Capacity decision, retry, or recovery policy |
| Domain decision | exact domain-owner result reference | Domain Work/adapter | Check slot type and resolvability | Generic boolean predicate |
| Recovery | `RecoveryDecisionRef` | Recovery Candidate-2 classifier and journal/ACI acceptance | Consume an independently accepted decision reference | Treatment selection or recovery execution |
| Authority | `AuthorityVerificationRef` / existing `requires-authority` | Authority adapter/owner | Validate exact reference slot and declaration | Authority grant |
| Admission | `ACIAdmissionRef`, `ArtifactAdmissionRef` | ACI/admission owners | Validate typed reference presence/shape | Admission decision |
| ARE evidence | `AREEvidenceRef` | ARE entry, ACI, semantic/artifact admission owners | Carry admitted evidence reference only | Raw model output as accepted evidence |
| Effect permission | `EffectPermissionRef` | Exact-effect owner | Validate typed slot; wait for owner verdict | Effect safety or execution permission |
| Forbidden structure | compiler invariant | Compile time; compiler | Reject source and return compiler defect | Runtime/domain/external failure |

Release means structural eligibility only. Structural graph acceptance, journal acceptance, ARE evidence, ACI admission, authority verification, and effect permission are separate gates. [Observed: [`DESIGN.md` §§1–3, 5, 6.3, 8, 10](../../../../DESIGN.md); [`ONTOLOGY.md` §§4–6](../../../../ontology/ONTOLOGY.md); `ontology.json#/owner_routes` and `#/constraints`. Designed: [`synthesis-revised.md` §§4–5](synthesis-revised.md); [`review-definitional.md` “Required non-collapse repairs”](review-definitional.md).]

## Typed reference boundaries

Permitted external-owner slots are exact, not members of a generic reference union:

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

Each reference schema is owned externally. A form/compiler may check only that the exact slot permits that exact type, that its syntax and stable identity are valid, that its declared source owner is present, and that it resolves where resolution is available. A reference never performs acceptance, grants authority, admits an artifact, establishes truth, authorizes or executes an effect, or mints a decision. Delivery and effects remain blocked until the applicable owner has independently accepted the reference. Existing `requires-authority` is reused for authority rather than duplicated. [Observed: [`DESIGN.md` §§4.1, 8, 10](../../../../DESIGN.md); [`ONTOLOGY.md` §§3, 5–6](../../../../ontology/ONTOLOGY.md); `ontology.json#/relations/rwo:r.requires-authority` and `#/owner_routes`. Designed: [`synthesis-revised.md` §5](synthesis-revised.md); [`review-precedent.md` generic-external-reference and relation gates](review-precedent.md).]

Recovery Candidate-2 reinforces the boundary: admitted owner handles feed a structural classifier, but the accepted recovery decision has no authority effect and all ordinary entry, authority, ACI, and effect gates remain independent. Adapter Candidate-2 likewise separates capability claims, conformance evidence, scoped admission, journal acceptance, and effect permission. [Observed candidate design: [`RecoveryDecisionContract@candidate-2` §§1.3, 5, 8, 10](../../20260805T184601Z-rwo-domain-recovery-model/stages/08-distill-repair.md); [`TransportNeutralWorkProtocolAdapterContract@candidate-2` §§1, 4–6](../../20260806T032327Z-rwo-transport-neutral-adapters/stages/08-distill-repair.md).]

## Disjoint compilation to `WorkGraph`

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

A success has exactly one output graph and zero defects. A rejection has at least one compiler defect and no graph reference or output digest. Timestamps are excluded from semantic identity. Raw-source, canonical-input, dependency, and output-graph digests name separate byte domains. `CompilerProfile` is immutable canonicalization/desugaring configuration only—not a plugin surface, evaluator, policy, proof, authority, or promotion record.

```text
authored CompositionForm
  --compiles-to--> CompilationSuccess
  --produces-work-graph--> WorkGraph

authored CompositionForm
  --compilation-rejected-as--> CompilationRejection
  --rejects-with--> FormCompilationDefect
```

This repairs, rather than parallels, the existing `rwo:r.compiles-to`. Changing its current `CompositionForm -> WorkGraph` range is an ontology migration and remains blocked. [Observed current relation: [`ONTOLOGY.md` §5](../../../../ontology/ONTOLOGY.md); `ontology.json#/relations/rwo:r.compiles-to`. Designed result: [`synthesis-revised.md` §6](synthesis-revised.md); [`review-precedent.md` “Relation gate”](review-precedent.md); [`review-definitional.md` `CompilationReceipt`](review-definitional.md).]

### Deterministic compiler limits

The compiler may:

- resolve exact existing subtype, schema, profile, operand, selector, mapping, policy, and typed-reference declarations;
- validate closed syntax, reference shapes, decided cardinalities, and graph invariants;
- derive source paths and recursively expand convenience forms;
- emit nodes by canonical source path;
- emit edges by `(from_path, selector_ref, route_or_branch_key, to_path, mapping_ref)`;
- preserve semantically ordered lists and sort only key-defined sets;
- reject duplicate keys and divergent canonical identities; and
- return exactly one success or one rejection.

It may not accept journal events, fold runtime cursors, interpret domain labels, decide open quorum or late-arrival semantics, select recovery, mint attempts/rounds/decisions/admission/authority/permission, infer transport or effect success, migrate ontology, or promote any artifact. Rejection emits no graph, success, runtime state, journal record, cursor, command, attempt, round, debit, or external-owner verdict. Determinism is designed, not demonstrated: no compiler, canonical fixture bytes, duplicate compile receipt, or digest comparison exists. [Designed: [`synthesis-revised.md` §§6–7](synthesis-revised.md). Non-vacuity challenge: [`review-non-vacuity.md` deterministic compiler verdict and witness repairs](review-non-vacuity.md).]

## Defect owner split

Compiler-owned `FormCompilationDefect` is limited to source syntax and graph structure:

```text
FORM_SCHEMA_UNSUPPORTED
FORM_SOURCE_DIGEST_MISMATCH
FORM_OPERAND_MISSING
FORM_OPERAND_KEY_DUPLICATE
FORM_REFERENCE_UNRESOLVED
FORM_SELECTOR_UNDECLARED
FORM_MAPPING_INVALID
SEQUENCE_CARDINALITY_INVALID          # owner-gated
FANOUT_EMPTY
FANOUT_BRANCH_KEY_DUPLICATE
FANIN_EMPTY
FANIN_SOURCE_DUPLICATE
FANIN_ORDER_INCOMPLETE
FANIN_QUORUM_OUT_OF_RANGE             # owner-gated
GATE_ROUTE_LABEL_DUPLICATE
SIDECAR_CONTROL_DIRECTION_FORBIDDEN
REPEAT_BOUND_MISSING
REPEAT_BOUND_NON_POSITIVE
REPEAT_EXHAUSTION_MISSING
EXPLICIT_GRAPH_CYCLE_UNBOUNDED
CANONICAL_ID_BYTES_DIVERGENT
```

Runtime results are not compiler defects: ordinary selector no-match, stale-attempt ineligibility, unmatched Gate label, explicitly corrupted route ambiguity, frozen FanIn manifest, retained late arrival, repeat exhaustion, and stale reducer block. Journal owns duplicate/redelivery disposition, divergent-message quarantine, ordering, debit acceptance, and fences. Recovery, domain, authority, admission, ARE/ACI, adapter, and exact-effect owners retain their own typed results. Ontology identity divergence is a migration blocker, not a form defect. [Observed owner boundaries: [`DESIGN.md` §§7–11](../../../../DESIGN.md); `ontology.json#/owner_routes` and `#/constraints`. Designed split: [`synthesis-revised.md` §8](synthesis-revised.md); [`review-precedent.md` “Defect ownership”](review-precedent.md); [`review-non-vacuity.md` “Mutation boundaries”](review-non-vacuity.md).]

## Sidecar, retry, repeat, replay, and effect non-collapse

Sidecar lifecycle may translate primary observations into companion start, observe, await, detach, or cancellation-request actions. Companion state cannot directly fail, cancel, retry, or mutate primary state. Companion-to-primary influence requires an ordinary declared edge and every applicable decision, authority, and admission gate. Cancellation request is not terminal cancellation; nesting does not imply propagation. [Observed: [`DESIGN.md` §§5.5, 11](../../../../DESIGN.md); [`ONTOLOGY.md` §§4, 6](../../../../ontology/ONTOLOGY.md). Designed: [`synthesis-revised.md` §9](synthesis-revised.md).]

| Mechanism | Identity/state rule | Deciding owner |
|---|---|---|
| Transport redelivery | Same logical message, bytes, and Work attempt; a new transport delivery attempt is allowed | Adapter policy; journal deduplicates/quarantines |
| Work retry | New `work_attempt_id`; WorkRun and repeat round remain | Accepted recovery decision |
| Bounded repeat | New repeat-round identity, then child attempts after route gates and accepted debit | Definition plus decision Work plus journal/budget owner |
| Domain rework | Domain-owned decision/cycle; never inferred as redelivery, retry, or repeat | Domain owner |
| Replay/resume | Same semantic identities; rebuild from accepted history/version with zero external calls | Journal/reducer owner |
| Recovery classification | Owner-issued recovery decision reference; classification is not execution of treatment | Recovery owner plus journal/ACI acceptance |
| Effect reconciliation/retry | Original uncertain effect remains unknown; no Work retry or effect retry is inferred | Exact-effect owner |

These boundaries are directly consistent with Recovery Candidate-2’s identity transition table and Adapter Candidate-2’s retry/redelivery/replay table. [Observed candidate design: recovery Candidate-2 §§5–8; adapter Candidate-2 §§2, 5–6. Designed form rule: [`synthesis-revised.md` §9](synthesis-revised.md); [`review-definitional.md` repairs 3–5](review-definitional.md).]

## Planned fixture contract — explicitly unexecuted

Every future fixture must bind all of:

```text
fixture_id
owner_dependencies
phase
exact_input_bytes + input_byte_size + input_digest
compiler_version + reducer_version + profile_version, as applicable
initial_graph + journal + cursor + command state, as applicable
exactly_one_expected_result
exact_output_bytes + output_byte_size + output_digest, when applicable
allowed_mutations
forbidden_mutations
validation_command
validation_receipt
```

The planned compiler corpus includes one valid fixture per form; one nested all-seven form; byte-identical deterministic recompile; keyed FanOut permutation; Sequence order and selector negatives; FanOut empty and duplicate-key negatives; FanIn duplicate/order/quorum boundaries; Gate duplicate label; Sidecar forbidden control direction; repeat missing/non-positive bound and missing exhaustion; bounded and unbounded explicit cycles; unsupported selector/schema; raw-source digest mismatch; and divergent canonical-ID bytes.

The planned runtime/owner corpus includes ordinary selector no-match, stale attempt, unmatched Gate, explicit corrupt-route ambiguity, Sidecar companion failure, repeat exhaustion, transport redelivery, Work retry, bounded-repeat continuation, replay/resume, uncertain effect, raw ARE output presented as admission, divergent same-ID message bytes, and late arrival against a frozen join.

### Required discriminating groups

Every case below is **planned and unexecuted**. The owner dependencies are gates that must close before fixture bytes can be frozen; naming an expected result does not decide those gates.

#### 1. Quorum schedules after owner closure

| Planned case | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-FANIN-QUORUM-ZERO` with `source_count = N > 0`, `quorum = 0` | Structural quorum owner; exact `ReleasePolicy` schema; compiler defect owner | `CompilationRejection(FANIN_QUORUM_OUT_OF_RANGE)` | None; emit the rejection value only | No graph/success, journal append, cursor, command, frozen manifest, or external verdict |
| `FIX-FANIN-QUORUM-ABOVE-COUNT` with `source_count = N`, `quorum = N + 1` | Structural quorum owner; exact `ReleasePolicy` schema; compiler defect owner | `CompilationRejection(FANIN_QUORUM_OUT_OF_RANGE)` | None; emit the rejection value only | No graph/success, journal append, cursor, command, frozen manifest, or external verdict |
| `FIX-FANIN-QUORUM-POSITIVE-LOWER` with `quorum = 1` and the first eligible accepted source arrival | Structural quorum owner; journal acceptance/fence owner; reducer version; frozen-manifest rule | `FanInReleaseResult(released_at_quorum_1)` | Append the admitted arrival, fold its exact cursor transition, freeze the declared manifest, and emit exactly one join command | No pre-arrival release, second join command, manifest rewrite, domain-success inference, or late-arrival discard |
| `FIX-FANIN-QUORUM-POSITIVE-UPPER` with `quorum = N`, an ordered schedule of `N - 1` arrivals followed by arrival `N` | Structural quorum owner; journal acceptance/fence owner; reducer version; canonical source order; frozen-manifest rule | `FanInReleaseResult(released_at_quorum_N)` | Append the admitted arrivals, fold exact cursor transitions, freeze the declared manifest at arrival `N`, and emit exactly one join command | No release at `N - 1`, duplicate command, manifest rewrite, domain-success inference, or late-arrival discard |

#### 2. Domain rework round and recovery decision remain separate

| Planned case | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-DOMAIN-REWORK-ROUND` with one owner-admitted domain rework decision | Domain rework owner and schema; semantic/admission owner; journal acceptance; domain round identity rule | `DomainReworkRoundResult(accepted_new_domain_round)` | Append the owner-admitted rework record and allocate exactly one domain-owned round identity | No transport delivery attempt, Work retry attempt, `BoundedRepeat` round, recovery disposition, effect attempt, or RWO-minted domain decision |
| `FIX-RECOVERY-DECISION` with one atomically accepted `RecoveryDecisionRef` selecting `RETRY_NEW_ATTEMPT` | Recovery Candidate-2 owner; journal/ACI atomic acceptance; attempt budget/fence; exact typed reference schema | `RecoveryDecisionAcceptance(accepted_retry_new_attempt)` | Append the accepted recovery decision, consume its trigger, debit exactly one attempt budget, and allocate exactly one new Work attempt | No domain-rework round, repeat round, same-message redelivery identity, effect attempt, duplicate trigger consumption, or RWO-minted recovery decision |

#### 3. Distinct forbidden-owner-predicate structural defects

| Planned case | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-FORBIDDEN-DOMAIN-PREDICATE` embeds domain truth as a form predicate | Frozen condition-free form schemas; domain owner boundary; compiler defect owner | `CompilationRejection(FORM_DOMAIN_PREDICATE_FORBIDDEN)` | None; emit the rejection value only | No predicate evaluation, graph/success, domain fact, journal/cursor/command, or generic-condition fallback |
| `FIX-FORBIDDEN-RECOVERY-PREDICATE` embeds treatment selection as a form predicate | Frozen condition-free form schemas; recovery owner boundary; compiler defect owner | `CompilationRejection(FORM_RECOVERY_PREDICATE_FORBIDDEN)` | None; emit the rejection value only | No recovery classification/decision, graph/success, attempt/round allocation, or generic-condition fallback |
| `FIX-FORBIDDEN-AUTHORITY-PREDICATE` embeds authority approval as a form predicate | Frozen condition-free form schemas; authority owner boundary; compiler defect owner | `CompilationRejection(FORM_AUTHORITY_PREDICATE_FORBIDDEN)` | None; emit the rejection value only | No authority evaluation/grant, graph/success, command/effect, or generic-condition fallback |
| `FIX-FORBIDDEN-ADMISSION-PREDICATE` embeds ACI or artifact admission as a form predicate | Frozen condition-free form schemas; ACI/artifact-admission owners; compiler defect owner | `CompilationRejection(FORM_ADMISSION_PREDICATE_FORBIDDEN)` | None; emit the rejection value only | No admission verdict, artifact acceptance, graph/success, command/effect, or generic-condition fallback |
| `FIX-FORBIDDEN-EFFECT-PREDICATE` embeds effect safety or outcome as a form predicate | Frozen condition-free form schemas; exact-effect owner boundary; compiler defect owner | `CompilationRejection(FORM_EFFECT_PREDICATE_FORBIDDEN)` | None; emit the rejection value only | No permit, effect execution/retry/reconciliation, graph/success, or generic-condition fallback |

#### 4. Split stale-version defects

| Planned case | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-STALE-FORM-SCHEMA-VERSION` names a resolved but superseded authored-form schema | Form-schema owner; compatibility window; compiler defect owner | `CompilationRejection(FORM_SCHEMA_VERSION_STALE)` | None; emit the rejection value only | No implicit schema upgrade, graph/success, source rewrite, runtime state, or owner verdict |
| `FIX-STALE-COMPILER-PROFILE-VERSION` names a resolved but inactive immutable profile | Compiler-profile owner; activation/compatibility rule; compiler defect owner | `CompilationRejection(COMPILER_PROFILE_VERSION_STALE)` | None; emit the rejection value only | No profile fallback, graph/success, canonical-byte rewrite, runtime state, or promotion |
| `FIX-STALE-DEPENDENCY-VERSION` names a superseded selector, mapping, policy, or typed-reference schema | Exact dependency owner; version compatibility rule; compiler defect owner | `CompilationRejection(FORM_DEPENDENCY_VERSION_STALE)` | None; emit the rejection value only | No dependency substitution, graph/success, external-owner decision, journal/cursor/command, or migration |
| `FIX-STALE-REDUCER-VERSION` attempts resume with history bound to a different reducer version | Journal truth owner; reducer migration owner; replay compatibility receipt | `RuntimeBlock(STALE_REDUCER_VERSION)` | Retain accepted history and append the scoped block evidence if its owner contract permits | No cursor rewrite, route release, command, history reinterpretation, attempt/round/effect allocation, or silent reducer upgrade |

#### 5. Split digest defects

| Planned case | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-DIGEST-RAW-SOURCE` presents raw bytes inconsistent with the declared raw-source digest | Canonical byte-domain owner; source provenance owner; compiler defect owner | `CompilationRejection(FORM_SOURCE_DIGEST_MISMATCH)` | None; emit the rejection value only | No canonicalization, graph/success, source rewrite, runtime state, or external verdict |
| `FIX-DIGEST-CANONICAL-INPUT` presents canonical bytes inconsistent with the declared canonical-input digest | Canonicalization/profile owner; canonical byte-domain owner; compiler defect owner | `CompilationRejection(CANONICAL_INPUT_DIGEST_MISMATCH)` | None; emit the rejection value only | No graph/success, alternate canonicalization, source rewrite, runtime state, or external verdict |
| `FIX-DIGEST-DEPENDENCY` resolves one selector, mapping, policy, or typed-reference dependency to bytes divergent from its bound digest | Exact dependency owner; resolver/provenance owner; compiler defect owner | `CompilationRejection(FORM_DEPENDENCY_DIGEST_MISMATCH)` | None; emit the rejection value only | No dependency substitution, graph/success, external-owner decision, journal/cursor/command, or migration |
| `FIX-DIGEST-OUTPUT-GRAPH` observes emitted graph bytes divergent from the success result's output digest | Compiler/conformance owner; output byte-domain rule; validator version | `CompilerConformanceRejection(OUTPUT_GRAPH_DIGEST_MISMATCH)` | Retain the candidate compiler output and conformance rejection as non-runtime evidence only | No accepted success receipt, runtime admission, journal/cursor/command, graph repair, promotion, or deployment |
| `FIX-DIGEST-CANONICAL-ID-BYTES` supplies one canonical identity for two divergent byte sequences | Canonical identity/provenance owner; compiler defect owner | `CompilationRejection(CANONICAL_ID_BYTES_DIVERGENT)` | None; emit the rejection value only | No winner selection, merge, graph/success, quarantine outside the compiler result, runtime state, or owner verdict |

#### 6. Exact owner/admission missing-reference schemas

Each omission fixture uses an otherwise schema-valid source with exactly one required slot absent. Its owner must first publish the exact reference schema and the form-schema owner must declare the slot required; until then, the case remains gated and cannot be serialized.

| Planned case and exact omitted slot | Owner-gate dependencies | Exactly one expected result | Allowed mutations | Forbidden mutations |
|---|---|---|---|---|
| `FIX-MISSING-RECOVERY-DECISION-REF`: `RecoveryDecisionRef` | Recovery owner; exact reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_RECOVERY_DECISION_REF_MISSING)` | None; emit the rejection value only | No inferred/minted reference, recovery decision, graph/success, attempt/round, journal/cursor/command, or effect |
| `FIX-MISSING-AUTHORITY-VERIFICATION-REF`: `AuthorityVerificationRef` | Authority owner; exact reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_AUTHORITY_VERIFICATION_REF_MISSING)` | None; emit the rejection value only | No inferred/minted reference, authority grant, graph/success, command, admission, or effect |
| `FIX-MISSING-ACI-ADMISSION-REF`: `ACIAdmissionRef` | ACI owner; exact reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_ACI_ADMISSION_REF_MISSING)` | None; emit the rejection value only | No inferred/minted reference, ACI verdict, graph/success, command, artifact admission, or effect |
| `FIX-MISSING-ARTIFACT-ADMISSION-REF`: `ArtifactAdmissionRef` | Artifact-admission owner; exact reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_ARTIFACT_ADMISSION_REF_MISSING)` | None; emit the rejection value only | No inferred/minted reference, artifact acceptance, graph/success, command, ACI verdict, or effect |
| `FIX-MISSING-ARE-EVIDENCE-REF`: `AREEvidenceRef` | ARE entry and evidence owner; ACI/semantic/artifact admission owners; exact reference schema; compiler defect owner | `CompilationRejection(FORM_ARE_EVIDENCE_REF_MISSING)` | None; emit the rejection value only | No raw-model-output substitution, inferred/minted reference, graph/success, admission, authority, command, or effect |
| `FIX-MISSING-EFFECT-PERMISSION-REF`: `EffectPermissionRef` | Exact-effect owner; exact permit/reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_EFFECT_PERMISSION_REF_MISSING)` | None; emit the rejection value only | No inferred/minted permit, effect execution/retry/reconciliation, graph/success, command, or authority grant |
| `FIX-MISSING-BUDGET-DEBIT-REF`: `BudgetDebitRef` | Journal/budget owner; exact debit-reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_BUDGET_DEBIT_REF_MISSING)` | None; emit the rejection value only | No inferred/minted debit, counter mutation, graph/success, attempt/round, journal/cursor/command, or effect |
| `FIX-MISSING-JOURNAL-ACCEPTANCE-REF`: `JournalAcceptanceRef` | Journal acceptance owner; exact reference schema; form-slot declaration; compiler defect owner | `CompilationRejection(FORM_JOURNAL_ACCEPTANCE_REF_MISSING)` | None; emit the rejection value only | No inferred/minted acceptance, history append, graph/success, cursor/command, route release, or external verdict |

Each fixture must have one expected result and an exact mutation boundary. Compile rejection permits no graph, success receipt, runtime state, journal record, cursor, or command. Runtime negatives may retain accepted evidence but may not mutate the forbidden control surface: no edge/command on no-match; no frozen join rewrite; no route on unmatched Gate; no primary change from companion failure; no debit/round/attempt after exhaustion; no current release from stale attempt; no stale reducer cursor rewrite; quarantine only for divergent bytes; and no inferred owner reference.

None of these fixture bytes, commands, expected output digests, or validation receipts exists in the admitted writer evidence, and none has run. The list is a validation-first contract, not a witness package and not finite non-vacuity proof. [Designed plan: [`synthesis-revised.md` §10](synthesis-revised.md). Explicit challenge and required repairs: [`review-non-vacuity.md`](review-non-vacuity.md).]

## Minimal ontology delta

Only non-aliased candidate concepts survive:

- optional compile-only `FormOccurrence`, only if embedded `source_path` is insufficient;
- immutable, non-authorizing `CompilerProfile`;
- disjoint `CompilationSuccess`;
- disjoint `CompilationRejection`;
- compiler-owned `FormCompilationDefect`.

Existing form subtypes, `CompositeWorkDefinition`, `EventSelector`, `InputMapping`, `ReleasePolicy`, `SidecarLifecyclePolicy`, `WorkGraph`, `WorkNode`, `EventTriggeredEdge`, `references-work`, and `requires-authority` are reused. No form-definition supertype, generic condition/evaluator/policy/reference, or runtime form identity is added. `compiles-to` becomes success-mediated; rejection lineage is separate; one success produces exactly one `WorkGraph`; both result kinds bind one immutable profile; typed external references use owner-specific relations.

Required future ontology queries must distinguish:

- authored source syntax from compiled `WorkGraph`;
- success from rejection;
- compiler defects from runtime/journal/external-owner results;
- a reused owner relation from an ornamental alias;
- optional source occurrence, `WorkNode`, `WorkRun`, and `Attempt` identities;
- typed reference presence from owner acceptance; and
- semantic source, generated projection, validation evidence, and promotion authority.

This delta is designed only. It has not been applied to `ONTOLOGY.md`, `ontology.json`, generated nodes/relations/views, schemas, validators, or Inventory. [Observed current catalogs and projection boundary: [`ONTOLOGY.md` §§1–6, 13, 16](../../../../ontology/ONTOLOGY.md); `ontology.json#/ontology`, `#/element_types`, `#/relations`. Designed delta: [`synthesis-revised.md` §11](synthesis-revised.md); [`review-precedent.md`](review-precedent.md); [`review-definitional.md`](review-definitional.md).]

## Compatibility and migration posture

| Surface | Compatibility rule | Migration status |
|---|---|---|
| Existing seven subtype IDs | Preserve names and subtype ownership; extend only through exact versioned subtype schemas | Designed; not adopted |
| Authored bytes | Existing bytes remain identical only if an exact schema/profile proves the same byte domain and canonicalization | Unproven; no fixtures |
| `compiles-to` | Existing direct `CompositionForm -> WorkGraph` consumers require an explicit migration to success-mediated lineage | Blocked on ontology owner |
| Rejection | Add only a separate rejection lineage; never use a partial success or graph with defects | Designed only |
| `ExplicitComposition` | Preserve as source syntax; migrate any projection that treats it as compiler output | Owner review required |
| Runtime identity | Do not convert source forms into `WorkRun`, `Attempt`, or `WorkNode`; optional occurrences are compile-only | Non-collapse rule frozen |
| External references | Migrate generic authority/admission/effect carriage to exact owner-specific relations only after those owners publish contracts | Blocked on owner contracts |
| Journal/reducer | Never reinterpret accepted history silently; schema and reducer migration need explicit versioning and replay evidence | Blocked; `RWO-OQ-006` |
| Ontology identity | Reconcile Markdown `0.2.0` and machine JSON `0.1.0` before any delta | Blocked on ontology identity owner |
| Unknown versions | Fail closed; do not guess, default, or profile-fallback | Candidate invariant; unexecuted |

No migration may infer that previously generated graph bytes, receipts, runtime state, or external verdicts conform to this candidate. Roll-forward and rollback bytes, digests, commands, and owner receipts must be planned before mutation. [Observed: [`DESIGN.md` §§10, 15](../../../../DESIGN.md); [`ONTOLOGY.md` §§12–13](../../../../ontology/ONTOLOGY.md); `ontology.json#/ontology`, `#/constraints/RWO-I11..I12`, and `#/residue`. Designed: [`synthesis-revised.md` §12](synthesis-revised.md).]

## Verdict matrix

| Surface | Verdict | Evidence posture |
|---|---|---|
| Existing seven-form taxonomy | RETAIN | Observed candidate ontology |
| Authored form under exactly one existing subtype | RETAIN | Designed, source-backed |
| Parallel `FormDefinition` | KILL | Ornamental duplicate |
| Runtime-shaped `FormInstance` | KILL | Identity collapse |
| Optional compile-only `FormOccurrence` | CONDITIONAL | Add only for necessary path diagnostics |
| Closed per-form operands | RETAIN | Designed; Sequence cardinality gated |
| Existing selector/mapping/release/lifecycle owners | REUSE | Observed owners |
| Generic condition/evaluator layer | KILL | Universal policy/owner collapse |
| Typed external owner references | RETAIN AS REFERENCES ONLY | Exact schemas/owners unresolved |
| Disjoint results producing `WorkGraph` | RETAIN AS CANDIDATE | Designed; migration and conformance absent |
| `ExplicitComposition` as compiler output | KILL | It is source syntax |
| Unified defect vocabulary | KILL | Cross-owner collapse |
| Compiler structural defects | RETAIN AS CANDIDATE | Designed; no implementation |
| Scenario list as executed evidence | KILL | No serialized or executed corpus |
| Planned fixture contract | RETAIN | Validation-first input only |
| Findings and validation-first planning | READY | Exact-bound evidence closure |
| Adoption or ontology migration | BLOCKED | Owner decisions and migration evidence absent |
| Compiler/runtime conformance | UNSUPPORTED | No implementation or executions |
| Authority/promotion/deployment/release/production | NOT AUTHORIZED | `authority_effect: none` |

## Open gates

The package cannot advance to adoption or conformance until each gate has an explicit owner decision and evidence:

1. Sequence minimum cardinality.
2. Structural quorum ownership and exact admissible bounds.
3. Late-arrival behavior and owner, including frozen-manifest evidence retention.
4. Ontology identity reconciliation and owner-approved migration.
5. Journal truth, schema/reducer compatibility, and replay migration.
6. Exact typed authority, recovery, budget, journal-acceptance, and admission reference contracts.
7. ARE entry, ACI conformance, and artifact-admission owners/contracts.
8. Exact-effect permit, reconciliation, attempt, and conformance owner.
9. Serialized fixture corpus with canonical bytes, sizes, digests, expected outputs, and mutation boundaries.
10. Implemented compiler/validators plus executed compiler and runtime conformance receipts.
11. Canonical provenance representation and source-digest obligations.
12. A decision whether `FormOccurrence` is necessary or should be omitted.

The first planning units should therefore decide owner-gated schema questions, freeze schemas and byte domains, serialize the discriminating positive/negative fixtures, implement validators/compiler only within those frozen boundaries, bind exact digests, and execute validation. Planning must not treat fixture design as execution or a successful compiler check as runtime/owner conformance. [Closure posture: [`synthesis-revised.md` §§10–12](synthesis-revised.md); [`review-non-vacuity.md`](review-non-vacuity.md); recovery Candidate-2 §13; adapter Candidate-2 §10.]

## Claim ceiling

This findings package is **READY only for findings and validation-first planning**. It records a repaired candidate model whose definitions, owner boundaries, compilation lineage, non-collapse rules, and future validation contract are coherent at the design level.

It does **not** establish or authorize adoption, ontology migration, source-design modification, generated projection refresh, implementation, compiler conformance, runtime conformance, owner acceptance, authority, promotion, deployment, release, or production readiness. The exact evidence supports no broader claim.
