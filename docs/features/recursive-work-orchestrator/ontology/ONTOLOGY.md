---
tags: [orchestrator, recursive-work, ontology, architecture-properties, event-bus]
node_type: conceptual
is_session: false
session_ref: null
layer: [ontology, architecture, application]
nature: [reference, technical]
status: draft
veracity: low
conviction: high
version: 0.2.0
last_updated: 2026-08-05
private: true
authority: proposal-only
ontology_type: architecture-property
branch: system
---

# Recursive Work Orchestrator — Candidate Ontology

## 1. Ontology identity and boundary

| Field | Value |
|---|---|
| Ontology ID | `rwo-architecture@0.2.0` |
| Reusable archetype | `architecture-property` |
| Project-local alias | `recursive-work-orchestrator` |
| Branch | `system` |
| Source | [`../DESIGN.md`](../DESIGN.md) |
| Source posture | candidate design; proposal-only |
| Authority effect | none |
| Runtime conformance effect | none |
| Promotion status | not requested; not granted |

This ontology describes the proposed architecture of a thin recursive work orchestrator. It is a
candidate semantic model, not a canonical definition store, executable schema, implementation
claim, runtime observation, or authorization decision.

Repository-wide terms remain owned by [`definitions/`](../../../../definitions/). Terms in this
document are scoped to `rwo-architecture@0.2.0` until an explicit owner promotes or maps them.

Version 0.2.0 adds evidence-bound observations from the accepted 2026-08-05 current-state
research. Those observations classify implementation precedents, proposal gaps, and a conditional
Agent Reasoning Engine boundary. They do not turn a precedent into an RWO realization, make the
untracked design implemented, or satisfy any cross-owner integration gate.

## 2. Ontology thesis

```text
LeafWorkDefinition       ┐
                         ├─ specializes ─> WorkDefinition ─instantiated-by─> WorkRun
CompositeWorkDefinition  ┘                         │
        │                                          ├─ receives ─> Command
        └─ has-body ─> WorkGraph                    └─ emits ────> Event
                           │
                           ├─ contains ─> WorkNode ─references─> WorkDefinition
                           └─ contains ─> EventTriggeredEdge

OrchestratorKernel ─expands─> WorkGraph
OrchestratorKernel ─derives─> OrchestrationCursor <─derived-from─ Journal
OrchestratorKernel ─issues─> Command ─delivered-by─> WorkProtocol
Event ─recorded-by─> Journal ─projected-by─> StatusProjection
```

The closure rule is structural: every composition produces another `WorkDefinition`. The authority
rule is shallow: only one root `OrchestratorKernel` expands and schedules a run graph.

## 3. Element-type catalog

All identifiers use the local `rwo:` namespace.

| ID | Label | Parent type | Definition | Source |
|---|---|---|---|---|
| `rwo:ArchitectureElement` | Architecture Element | — | Any typed element in this local architecture model. | DESIGN §4–§8 |
| `rwo:WorkDefinition` | Work Definition | `rwo:ArchitectureElement` | Immutable, versioned outer contract that can describe a leaf or composite. | DESIGN §4.1 |
| `rwo:LeafWorkDefinition` | Leaf Work Definition | `rwo:WorkDefinition` | Work definition whose body binds to an executor adapter. | DESIGN §4.3 |
| `rwo:CompositeWorkDefinition` | Composite Work Definition | `rwo:WorkDefinition` | Work definition whose body is a work graph and whose boundary remains substitutable for a leaf. | DESIGN §4.4 |
| `rwo:WorkRun` | Work Run | `rwo:ArchitectureElement` | One invocation of one immutable work definition. | DESIGN §4.2 |
| `rwo:Attempt` | Attempt | `rwo:ArchitectureElement` | One execution attempt belonging to a work run. | DESIGN §4.2 |
| `rwo:WorkGraph` | Work Graph | `rwo:ArchitectureElement` | Typed graph that composes addressed work nodes through event-triggered edges. | DESIGN §4.4, §5.7 |
| `rwo:WorkNode` | Work Node | `rwo:ArchitectureElement` | Structural position in a graph that references one work definition. | DESIGN §4.2, §5 |
| `rwo:EventTriggeredEdge` | Event-Triggered Edge | `rwo:ArchitectureElement` | Routing rule from a source event selector to one target invocation and input mapping. | DESIGN §5 |
| `rwo:EventSelector` | Event Selector | `rwo:ArchitectureElement` | Versioned matcher over an event type and structural classification. | DESIGN §5, §6.3 |
| `rwo:InputMapping` | Input Mapping | `rwo:ArchitectureElement` | Declared transformation from selected source data to a target input contract. | DESIGN §4.4, §8 |
| `rwo:OutputProjection` | Output Projection | `rwo:ArchitectureElement` | Declared mapping from selected child outputs into a composite boundary output. | DESIGN §4.4 |
| `rwo:WorkContract` | Work Contract | `rwo:ArchitectureElement` | Input, output, command, event, authority, and limit declarations for a work definition. | DESIGN §4.1 |
| `rwo:EventContract` | Event Contract | `rwo:WorkContract` | Declares event types, schemas, and structural classifications a work may emit. | DESIGN §4.1, §6.3 |
| `rwo:CommandContract` | Command Contract | `rwo:WorkContract` | Declares addressed commands a work may receive. | DESIGN §4.1, §6 |
| `rwo:CompositionForm` | Composition Form | `rwo:ArchitectureElement` | Declarative graph pattern compiled into event-triggered edges. | DESIGN §5 |
| `rwo:Sequence` | Sequence | `rwo:CompositionForm` | Releases a successor from a declared predecessor event. | DESIGN §5.1 |
| `rwo:FanOut` | Fan-Out | `rwo:CompositionForm` | Releases multiple explicitly mapped branches from one declared event. | DESIGN §5.2 |
| `rwo:FanIn` | Fan-In | `rwo:CompositionForm` | Waits for a structural release condition and invokes a join work. | DESIGN §5.3 |
| `rwo:Gate` | Gate | `rwo:CompositionForm` | Routes one decision-work label to exactly one declared outgoing edge. | DESIGN §5.4 |
| `rwo:Sidecar` | Sidecar | `rwo:CompositionForm` | Attaches ordinary work to a primary under a declared lifecycle policy. | DESIGN §5.5 |
| `rwo:BoundedRepeat` | Bounded Repeat | `rwo:CompositionForm` | Repeats a graph under a decision work, bound, and exhaustion route. | DESIGN §5.6 |
| `rwo:ExplicitComposition` | Explicit Composition | `rwo:CompositionForm` | Direct typed graph form underlying the convenience operators. | DESIGN §5.7 |
| `rwo:ReleasePolicy` | Release Policy | `rwo:ArchitectureElement` | Structural readiness rule such as all, any, or bounded quorum. | DESIGN §5.3 |
| `rwo:SidecarLifecyclePolicy` | Sidecar Lifecycle Policy | `rwo:ArchitectureElement` | Declares start, observation, termination, and output contribution behavior for a sidecar. | DESIGN §5.5 |
| `rwo:WorkMessage` | Work Message | `rwo:ArchitectureElement` | Versioned message in the common work-protocol envelope. | DESIGN §6.1 |
| `rwo:Command` | Command | `rwo:WorkMessage` | Addressed request that a target or authority adapter may reject. | DESIGN §6 |
| `rwo:Event` | Event | `rwo:WorkMessage` | Accepted fact emitted by a work unit or trusted runtime adapter. | DESIGN §6 |
| `rwo:EventClassification` | Event Classification | `rwo:ArchitectureElement` | Structural event role: progress, release, terminal, or diagnostic. | DESIGN §6.3 |
| `rwo:WorkProtocol` | Work Protocol | `rwo:ArchitectureElement` | Logical command/event delivery boundary; not itself a decision-maker or executor. | DESIGN §6 |
| `rwo:Journal` | Journal | `rwo:ArchitectureElement` | Append-only accepted message history used for replay and audit. | DESIGN §6.2, §7 |
| `rwo:OrchestratorKernel` | Orchestrator Kernel | `rwo:ArchitectureElement` | Root graph interpreter that validates, expands, observes, and issues declared commands. | DESIGN §2, §8 |
| `rwo:OrchestrationCursor` | Orchestration Cursor | `rwo:ArchitectureElement` | Rebuildable control projection of deliveries, satisfied edges, and enabled nodes. | DESIGN §7 |
| `rwo:StatusProjection` | Status Projection | `rwo:ArchitectureElement` | Rebuildable user or operator view over accepted child events. | DESIGN §7 |
| `rwo:ExecutorAdapter` | Executor Adapter | `rwo:ArchitectureElement` | Boundary that translates the work protocol to an external executor and reports events. | DESIGN §4.3 |
| `rwo:AuthorityReference` | Authority Reference | `rwo:ArchitectureElement` | Reference to accepted authority evidence required for command delivery or an external effect. | DESIGN §4.1, §10 |
| `rwo:DomainState` | Domain State | `rwo:ArchitectureElement` | Work-owned meaning and lifecycle state that remains opaque to the orchestrator. | DESIGN §3, §7 |
| `rwo:ConfirmationState` | Confirmation State | `rwo:DomainState` | Confirmation meaning and state owned by an individual gate or work unit. | DESIGN §3, §5.4 |
| `rwo:ArchitectureProfile` | Architecture Profile | `rwo:ArchitectureElement` | Named set of constraints evaluated over this ontology. | DESIGN §10 |
| `rwo:ObservationProjection` | Observation Projection | `rwo:ArchitectureElement` | Typed transformation of source, graph, journal, runtime, or audit evidence into observed facts. | DESIGN §10, §13 |
| `rwo:PropertyFinding` | Property Finding | `rwo:ArchitectureElement` | Explainable result containing subject, expectation, observation, profile, evidence, and owner route. | Ontology Vault architecture-property contract |

## 4. Typed-property catalog

Properties describe elements; they do not create authority. `required_stage` names the earliest
stage at which a value may be evidenced.

| Property ID | Valid subject | Value domain | Required stage | Forbidden inference |
|---|---|---|---|---|
| `rwo:p.work-ref` | `WorkDefinition` | stable ID + version | definition | Same label or path means same identity. |
| `rwo:p.body-kind` | `WorkDefinition` | `leaf \| composite` | definition | Composite body grants nested orchestration authority. |
| `rwo:p.input-schema` | `WorkDefinition` | schema reference | definition | Schema validity proves semantic fitness. |
| `rwo:p.output-schema` | `WorkDefinition` | schema reference | definition | Schema validity proves result correctness. |
| `rwo:p.event-class` | `EventContract`, `Event` | `progress \| release \| terminal \| diagnostic` | definition/event | Terminal means approved or successful. |
| `rwo:p.release-mode` | `ReleasePolicy` | `all \| any \| quorum(n)` | definition | Structural quorum proves quality or independent judgment. |
| `rwo:p.max-rounds` | `BoundedRepeat` | positive integer | definition | A finite bound proves agent termination within a round. |
| `rwo:p.sidecar-finish` | `SidecarLifecyclePolicy` | `detach \| await \| cancel-requested` | definition | Sidecar may control primary without an edge. |
| `rwo:p.message-kind` | `WorkMessage` | `command \| event` | message | A command is an accepted fact; an event is permission for an effect. |
| `rwo:p.delivery-semantics` | `WorkProtocol` | `at-least-once` | architecture | Exactly-once business effects. |
| `rwo:p.ordering-scope` | `WorkProtocol`, `Journal` | `per-work-run` | architecture/runtime | Global ordering across runs. |
| `rwo:p.idempotency-key` | `Command`, `Event` | non-empty stable key | message/runtime | Duplicate delivery is harmless without adapter evidence. |
| `rwo:p.reducer-version` | `OrchestrationCursor`, `StatusProjection` | version reference | projection | A view without a reducer version is replayable. |
| `rwo:p.freshness` | `StatusProjection` | cursor/time watermark | projection | A displayed state is current when freshness is absent. |
| `rwo:p.authority-effect` | any local ontology element | `none` | ontology | Ontology membership grants authority. |
| `rwo:p.authoritative-for` | `DomainState`, `Journal`, `OrchestrationCursor` | owned state class | architecture | One owner class silently owns the other two. |
| `rwo:p.evidence-stage` | `PropertyFinding` | `definition \| source \| graph \| runtime \| test \| telemetry` | finding | Earlier-stage evidence proves a later-stage property. |
| `rwo:p.finding-status` | `PropertyFinding` | `pass \| fail \| unsupported \| indeterminate` | finding | Missing evidence means pass. |
| `rwo:p.proof-status` | `PropertyFinding` | `freshly-executed \| observed \| execution-unverified \| proposal \| hypothesis` | finding | Observed or previously executed evidence is fresh execution in this ontology update. |
| `rwo:p.correspondence` | `PropertyFinding` | `direct-realization \| precedent \| partial-analogue \| gap \| forbidden` | finding | A precedent or analogue is an implementation of the RWO contract. |
| `rwo:p.source-posture` | `PropertyFinding` | `tracked \| untracked-proposal \| private-evidence` | finding | Tracked bytes are promoted architecture or runtime conformance. |
| `rwo:p.promotion-effect` | `PropertyFinding` | `none` | finding | A finding can promote its subject, evidence, or vocabulary. |

## 5. Allowed-relation catalog

Relations are directed and non-transitive unless a row says otherwise.

| Relation ID | Source type | Target type | Cardinality | Cycle policy | Evidence requirement | Meaning |
|---|---|---|---|---|---|---|
| `rwo:r.specializes` | element type | element type | many-to-one | acyclic | ontology row | Local subtype relation. Transitive only within this type hierarchy. |
| `rwo:r.has-body` | `WorkDefinition` | `WorkGraph` or leaf binding | exactly one | acyclic | definition | Selects composite graph or leaf binding. |
| `rwo:r.instantiates` | `WorkRun` | `WorkDefinition` | exactly one | acyclic | accepted invocation | Binds a run to an immutable definition. |
| `rwo:r.has-attempt` | `WorkRun` | `Attempt` | one-to-many | acyclic | accepted attempt record | Associates attempts without changing run identity. |
| `rwo:r.contains-node` | `WorkGraph` | `WorkNode` | one-to-many | acyclic containment | graph definition | Gives a node structural membership. |
| `rwo:r.contains-edge` | `WorkGraph` | `EventTriggeredEdge` | one-to-many | acyclic containment | graph definition | Gives an edge structural membership. |
| `rwo:r.references-work` | `WorkNode` | `WorkDefinition` | exactly one | graph cycles governed separately | graph definition | Selects the reusable work at a structural position. |
| `rwo:r.from-node` | `EventTriggeredEdge` | `WorkNode` | exactly one | bounded cycles only | graph definition | Declares edge source. |
| `rwo:r.to-node` | `EventTriggeredEdge` | `WorkNode` | exactly one | bounded cycles only | graph definition | Declares edge target. |
| `rwo:r.selects-event` | `EventTriggeredEdge` | `EventSelector` | exactly one | follows edge | graph definition | Names the event trigger. |
| `rwo:r.maps-input-with` | `EventTriggeredEdge` | `InputMapping` | exactly one | follows edge | graph definition | Names the target-input mapping. |
| `rwo:r.projects-output-with` | `CompositeWorkDefinition` | `OutputProjection` | exactly one | acyclic | definition | Declares composite boundary output. |
| `rwo:r.compiles-to` | `CompositionForm` | `WorkGraph` | exactly one | acyclic | deterministic compiler receipt | Desugars convenience syntax into the primitive graph. |
| `rwo:r.uses-release-policy` | `FanIn` | `ReleasePolicy` | exactly one | acyclic | definition | Declares fan-in structural readiness. |
| `rwo:r.uses-lifecycle-policy` | `Sidecar` | `SidecarLifecyclePolicy` | exactly one | acyclic | definition | Declares sidecar lifecycle coupling. |
| `rwo:r.bound-to` | `LeafWorkDefinition` | `ExecutorAdapter` | exactly one | acyclic | definition | Selects the external executor boundary. |
| `rwo:r.receives` | `WorkRun` | `Command` | many | temporal | accepted delivery | Records an addressed request received by a run. |
| `rwo:r.emits` | `WorkRun` or trusted adapter | `Event` | many | temporal | accepted event | Attributes an event to its producer. |
| `rwo:r.delivered-by` | `WorkMessage` | `WorkProtocol` | exactly one | acyclic | delivery receipt | Identifies the protocol boundary used. |
| `rwo:r.recorded-by` | `Event` | `Journal` | exactly one | append-only | journal receipt | Records accepted event persistence. |
| `rwo:r.expands` | `OrchestratorKernel` | `WorkGraph` | many | structural recursion; runtime invocation acyclic | validated plan | Expands nested definitions into one root plan. |
| `rwo:r.issues` | `OrchestratorKernel` | `Command` | many | temporal | outbox receipt | Issues a declared addressed command. |
| `rwo:r.derived-from` | `OrchestrationCursor` or `StatusProjection` | `Journal` | exactly one per version | acyclic | reducer + cursor | Makes projection lineage explicit. |
| `rwo:r.observes` | `StatusProjection` | `Event` | many | acyclic | event reference | Exposes an accepted fact without owning it. |
| `rwo:r.requires-authority` | `WorkDefinition` or `Command` | `AuthorityReference` | zero-to-many | acyclic | accepted reference | Names required authority evidence without deciding it. |
| `rwo:r.owned-by` | `DomainState` | work unit or adapter | exactly one | acyclic | owner declaration | Places domain-state semantics outside the kernel. |
| `rwo:r.evaluates` | `ArchitectureProfile` | property or relation constraint | one-to-many | acyclic | profile definition | Selects constraints for a profile. |
| `rwo:r.supported-by` | `PropertyFinding` | evidence reference | one-to-many | acyclic | direct evidence | Grounds an observed finding. |

## 6. Forbidden relations and inference shields

These are hard non-collapse rules for this ontology.

| Shield ID | Forbidden inference |
|---|---|
| `rwo:f.no-nested-orchestrator-invocation` | `CompositeWorkDefinition` or graph containment must not imply an orchestrator-to-orchestrator invocation edge. |
| `rwo:f.no-parent-authority-inheritance` | Parentage, containment, or node path must not imply inherited tools, context, budget, evidence, confirmation, or authority. |
| `rwo:f.no-kernel-domain-state` | Observing an event or maintaining a cursor must not imply that `OrchestratorKernel` owns `DomainState` or `ConfirmationState`. |
| `rwo:f.no-bus-authority` | Delivering or recording a message must not imply that `WorkProtocol` or `Journal` authorized, decided, or executed it. |
| `rwo:f.no-terminal-success-collapse` | `terminal` must not imply success, approval, acceptance, truth, or downstream permission. |
| `rwo:f.no-projection-authority` | A `StatusProjection` must not manufacture confirmation, authority, freshness, or domain facts. |
| `rwo:f.no-structural-quorum-quality` | `quorum(n)` must not imply independent evidence, quality, correctness, or consensus. |
| `rwo:f.no-schema-correctness` | Schema-valid input, output, command, or event must not imply semantic correctness. |
| `rwo:f.no-idempotency-effect-proof` | A stable message key must not imply an external effect is idempotent without adapter evidence. |
| `rwo:f.no-ontology-promotion` | Inclusion in this ontology must not promote a term, constraint, source, or architecture claim. |
| `rwo:f.no-precedent-realization-collapse` | A selected precedent or partial analogue must not be described as an RWO implementation without direct contract and conformance evidence. |
| `rwo:f.no-observed-fresh-collapse` | Source inspection or prior executable evidence must not be reported as fresh execution in the current run. |
| `rwo:f.no-cross-owner-bridge-authority` | A bridge projection must not select owners, accept schemas, register a host binding, authorize an effect, or create a second scheduler or integrated journal. |

## 7. Architecture profiles

### `rwo:profile.core-v0`

The core profile evaluates all twelve invariants from DESIGN §10:

| Constraint | Ontology expression | Minimum evidence |
|---|---|---|
| `RWO-I01` uniform outer contract | every `LeafWorkDefinition` and `CompositeWorkDefinition` specializes `WorkDefinition` and has one `WorkContract` | definition parse |
| `RWO-I02` shallow runtime authority | composite graphs may be expanded; orchestrator-invocation edges are absent | graph validation |
| `RWO-I03` complete routing edge | every edge has one source, target, selector, and input mapping | graph validation |
| `RWO-I04` single-valued gate route | each admitted gate label resolves to exactly one edge | graph validation + fixture |
| `RWO-I05` explicit fan-in policy | every `FanIn` uses one release policy and canonical input ordering | definition parse + fixture |
| `RWO-I06` bounded cycles | every cyclic component has a positive bound and exhaustion route | graph validation |
| `RWO-I07` idempotent acceptance | commands and events have stable keys; divergent duplicate is rejected | runtime test |
| `RWO-I08` non-authoritative projection | projection retains reducer, freshness, and event lineage; cannot emit authority facts | schema + negative test |
| `RWO-I09` no parent inheritance | child materialization names explicit tools, context, budget, evidence, and authority | runtime manifest test |
| `RWO-I10` effect authority boundary | every effectful command names accepted authority evidence | runtime trace + authority audit |
| `RWO-I11` deterministic cursor replay | identical ordered history and reducer version rebuild identical cursor bytes | replay test |
| `RWO-I12` fail-closed extensibility | unknown operator, command, event, schema, or capability is rejected | negative fixtures |

### `rwo:profile.definition-only`

Evaluates only definition and graph properties. It may establish structural validity but cannot
claim delivery, replay, adapter, authority, or runtime conformance.

### `rwo:profile.runtime-evidence`

Adds message delivery, replay, idempotency, stale-attempt, and authority-boundary observations. It
requires an implementation and test evidence that do not yet exist for this design.

### `rwo:profile.current-state-evidence-v0`

Classifies current orchestrator bytes as precedents, partial analogues, gaps, or forbidden
topologies against the candidate RWO model. It preserves proof status separately from
correspondence status. Passing this profile means only that a finding is traceable and correctly
bounded; it cannot establish `rwo:profile.core-v0` or `rwo:profile.runtime-evidence` conformance.

## 8. Observation projections

Each projection produces evidence, never architecture authority.

| Projection ID | Input | May observe | Cannot establish alone |
|---|---|---|---|
| `rwo:obs.definition-map` | versioned work definitions | identity, body kind, schema refs, declared contracts and limits | runtime behavior or semantic correctness |
| `rwo:obs.graph-map` | expanded graph | nodes, edges, selectors, mappings, cycles, structural bounds | delivered commands or completed work |
| `rwo:obs.composition-compiler` | operator expression + compiler receipt | deterministic desugaring into a graph | that the graph executed |
| `rwo:obs.journal-replay` | accepted journal + reducer version | reconstructed cursor and deterministic digest | truth or completeness of unobserved external work |
| `rwo:obs.delivery-trace` | outbox/inbox and adapter receipts | delivery attempts, deduplication, ordering within scope | exactly-once external effects |
| `rwo:obs.authority-audit` | effect command + accepted authority reference + adapter trace | evidence that the declared boundary was used | correctness of the authority decision itself |
| `rwo:obs.status-view` | journal + projection reducer | current derived display, provenance, freshness | ownership of child domain state |
| `rwo:obs.counterexample-suite` | bounded pipeline fixtures | unsupported operators, ambiguous routes, unbounded cycles, collapse violations | universal “any pipeline” expressiveness |
| `rwo:obs.current-target-precedent-map` | pinned target commit + accepted evidence closure | implementation precedents, partial analogues, absent generic capabilities, forbidden topology | RWO implementation, recursive execution, host adoption, or production operation |
| `rwo:obs.rwo-are-boundary-map` | pinned RWO/ARE/ACI sources + reviewed documentation contract | conditional stages, owner seams, fail-closed rules, planned witnesses, open residue | owner selection, schema acceptance, runtime compatibility, artifact admission, effect authority, or executable integration |

## 9. Explainable finding shape

Every architecture-property finding must retain:

```yaml
finding_id: "rwo:finding:..."
subject_ref: "rwo:..."
profile_ref: "rwo:profile.core-v0"
constraint_ref: "RWO-I.."
expected: "..."
observed: "..."
status: pass | fail | unsupported | indeterminate
evidence_stage: definition | source | graph | runtime | test | telemetry
proof_status: freshly-executed | observed | execution-unverified | proposal | hypothesis
correspondence: direct-realization | precedent | partial-analogue | gap | forbidden
source_posture: tracked | untracked-proposal | private-evidence
promotion_effect: none
evidence_refs: []
owner_route: "..."
forbidden_inferences: []
```

Absence of evidence yields `unsupported` or `indeterminate`, never `pass`.

## 10. Evidence and confidence ledger

| Claim | Evidence | Evidence confidence | Commitment confidence | Current action |
|---|---|---|---|---|
| composites share the leaf `Work` boundary | DESIGN §4 | low: design only | high | keep as candidate architecture constraint |
| one root expands nested graphs | DESIGN status boundary, §4.4, RWO-I02 | low: design plus prior candidate architecture | high | keep; requires graph fixtures and runtime enforcement |
| commands/events are sufficient for thin orchestration | DESIGN §2, §6, §8 | low | high | test with counterexamples |
| work units own confirmation and domain status | DESIGN §3, §5.4, §7 | low | high | keep with projection non-authority shield |
| at-least-once plus idempotency is the delivery baseline | DESIGN §6.2 | low | medium | keep as a candidate; compare implementation constraints |
| bounded event-triggered graphs cover almost any bounded pipeline | DESIGN §5.7, §13 | low | medium | preserve as falsifiable premise, not a universal claim |
| current dispatch identity, protocol lanes, fan-out shape, gate routing, and one accepted journal are useful precedents | accepted findings E1; current-target evidence projection | medium: direct source inspection; compiler slice freshly executed | low | retain as precedents only; require RWO schemas and conformance before realization claims |
| generic recursive graph expansion, projection of composite boundaries, sidecar lifecycle, and a routing cursor are implemented | accepted findings E1/E2 | low: gaps were observed; no RWO runtime exists | low | keep unsupported; do not infer from specialized dispatch/APT surfaces |
| ARE may integrate as a gate-adjacent, ACI-subordinate leaf boundary | accepted findings E3/C1/K1; private bridge profile | medium for source correspondence; low for compatibility | low | documentation-only; owners, schemas, conformance, artifact admission, and exact-effect evidence remain blocking |

No confidence promotion is recommended. The design remains proposal-only and has no RWO
implementation witness. The newly bound implementation evidence supports only the correspondence
classification recorded in the current-state projection.

## 11. Source ledger

| Source | Kind | Authority in this ontology | Use |
|---|---|---|---|
| [`../DESIGN.md`](../DESIGN.md) | candidate architecture design | primary semantic source; proposal-only | element types, properties, relations, constraints, residue |
| [`../../agents-communication-infra/discovery/bus-contracts/README.md`](../../agents-communication-infra/discovery/bus-contracts/README.md) | discovery | supporting context only | bus, routing, journal, idempotency, command/control separation |
| [`../../../../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md`](../../../../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md) | proposal-only system view | supporting context only | recursive work, shallow authority, history and projections |
| [`../../../essays/from-context-to-governed-primitives/from-context-to-governed-primitives.md`](../../../essays/from-context-to-governed-primitives/from-context-to-governed-primitives.md) | proposal-only essay | constraint context only | recursive composition does not authorize recursive invocation |
| `domainspec-core:ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/findings.md` | accepted delegated research | evidence only | current implemented state, RWO deltas, topology verdicts, open residue |
| `domainspec-core:ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/receipts/evidence-closure.json` | immutable evidence closure | evidence binding only | source identities E1, E2, E2-WG, E3, C1, and K1; claim ceiling |
| `domainspec-core:ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/audit-final.md` | final research audit | validation evidence only | confirms accepted documentation claim boundaries |
| [`evidence/CURRENT-STATE-2026-08-05.json`](evidence/CURRENT-STATE-2026-08-05.json) | candidate ontology projection | non-authoritative read model | machine-readable findings and bridge summary |
| [`nodes/nodes.json`](nodes/nodes.json) | generated candidate node graph | non-authoritative read model | addressable architecture elements, precedents, sources, findings, residue, stages, gates, witnesses, and prohibited topologies |
| [`relations/relations.json`](relations/relations.json) | generated candidate relation graph | non-authoritative read model | typed structural, evidence, finding, contradiction, integration, governance, validation, and prohibition edges |
| [`views/current-state.json`](views/current-state.json) | generated current-state view | non-authoritative read model | grouped nodes, queryable trace paths, RWO-to-ARE sequence, and forbidden authority moves |

The supporting sources do not independently promote this model. Their distinctions are carried
through the design; this ontology must not outrank them.

## 12. Residue

The ontology preserves every open question from DESIGN §15 as unresolved:

| Residue ID | Design question | Ontology impact |
|---|---|---|
| `rwo:residue.001` | `RWO-OQ-001` journal versus work-owned source of state | ownership and reconciliation relations remain unsettled |
| `rwo:residue.002` | `RWO-OQ-002` dynamic graph extension and confirmation | graph version and authority relations remain incomplete |
| `rwo:residue.003` | `RWO-OQ-003` cross-host delivery guarantees | protocol properties remain candidate |
| `rwo:residue.004` | `RWO-OQ-004` standard cancellation/compensation forms | composition catalog may need extension |
| `rwo:residue.005` | `RWO-OQ-005` structural versus decision-work quorum | release-policy semantic boundary remains open |
| `rwo:residue.006` | `RWO-OQ-006` schema/reducer migration | version and replay relations remain incomplete |
| `rwo:residue.007` | `RWO-OQ-007` minimal authority reference | effect-boundary property remains incomplete |
| `rwo:residue.008` | `RWO-OQ-008` counterexample suite | bounded expressiveness claim remains unsupported |
| `rwo:residue.009` | `RWO-OQ-009` long-lived streams | uniform `Work` closure remains unproven |
| `rwo:residue.010` | `RWO-OQ-010` promotion owner | ontology remains proposal-only |

Additional ontology residue:

| Residue ID | Question | Status |
|---|---|---|
| `rwo:residue.011` | Is `EventClassification` metadata on an event contract, an independent controlled vocabulary, or both? | open |
| `rwo:residue.012` | Should `InputMapping` be pure and deterministic, or may it invoke a mapping work unit? | open |
| `rwo:residue.013` | Is an executor adapter a work-owned component or an independently governed runtime boundary? | open |
| `rwo:residue.014` | Which relation types, if any, may compose transitively beyond local subtype relations? | open |

Workflow-graph hypothesis residue imported from the accepted research remains unresolved:

| Residue ID | Source question | Ontology impact |
|---|---|---|
| `rwo:residue.015` | `WGQ-1` graph/state structure count | canonical lifecycle and state partition remains unsettled |
| `rwo:residue.016` | `WGQ-2` meaning of a workflow node | `WorkNode` cannot be collapsed into `AgentNode` |
| `rwo:residue.017` | `WGQ-3` node/agent/seat/attempt cardinalities | retry, reuse, and identity relations remain incomplete |
| `rwo:residue.018` | `WGQ-4` node and edge taxonomy | executable closed schemas are not selected |
| `rwo:residue.019` | `WGQ-5` workflow versus communication | routing and permission ownership remain separate and unsettled |
| `rwo:residue.020` | `WGQ-6` collective coordination | quorum, dissent, budgets, and collective result semantics are unowned |
| `rwo:residue.021` | `WGQ-7` completion model | attempt end, outcome, terminal fact, and audit close remain distinct candidates |
| `rwo:residue.022` | `WGQ-8` rework under a DAG | bounded loop, generation, and replay semantics remain unsettled |
| `rwo:residue.023` | `WGQ-9` compilation and confirmation | total mapping, lineage, and fail-closed authority remain unproven |
| `rwo:residue.024` | `WGQ-10` simplified views | projections must remain derivable and non-authoritative |

Cross-owner integration residue:

| Residue ID | Blocker | Status |
|---|---|---|
| `rwo:residue.025` | reasoning-entry owner and typed verdict contract are unselected | open |
| `rwo:residue.026` | artifact-admission owner and contract are absent (`GAP-ARE-ART-001`) | blocked |
| `rwo:residue.027` | exact-effect owner, accepted effect schema, and effect evidence are absent | open |
| `rwo:residue.028` | cross-repository command, cut, artifact, effect, and compatibility schemas lack owner receipts and conformance evidence | open |
| `rwo:residue.029` | discriminating witnesses F1–F8 are planned but unexecuted | open |

## 13. Validation status

This v0.2.0 ontology can be checked at the document, design-correspondence, and delegated-evidence
traceability levels. RWO runtime and cross-repository integration conformance remain unsupported.

| Check | Result | Evidence |
|---|---|---|
| ontology type selected before mapping | pass | `architecture-property`, inferred with high confidence |
| branch selection | pass | derived `system` branch |
| source authority stated | pass | §1, §10, §11 |
| architecture element types mapped | pass | §3 |
| typed properties and forbidden inferences mapped | pass | §4 |
| allowed relations and cycle policies mapped | pass | §5 |
| architecture profiles mapped | pass | §7 |
| observation projections bounded | pass | §8 |
| explainable finding shape present | pass | §9 |
| open residue preserved | pass | §12 |
| delegated evidence traceability | pass | accepted evidence rows E1, E2, E2-WG, E3, C1, K1 projected without exceeding their claim ceilings |
| current target precedent classification | pass | `evidence/CURRENT-STATE-2026-08-05.json`; proof and correspondence axes remain separate |
| node materialization | pass | 137 unique nodes across 10 node kinds; every accepted finding, evidence source, residue item, stage, gate, witness, and killed topology is addressable |
| relation integrity | pass | 220 directed zero-authority relations; all endpoints and evidence references resolve |
| current-state view coverage | pass | the view covers every node and relation exactly once and exposes three bounded trace sequences |
| negative graph fixtures | pass | authority-producing relation and missing-endpoint relation both reject |
| RWO implementation/runtime conformance | unsupported | no RWO runtime, recursive compiler, full fixtures, or conformance receipt |
| RWO-to-ARE executable integration | unsupported | documentation-only bridge; owners, schemas, compatibility, F1–F8, and effect evidence remain open |
| ontology promotion | not granted | no owner decision or promotion record |

Overall result: **FLAG** — structurally mapped and evidence-bound, with RWO realization,
cross-repository integration, runtime conformance, and promotion explicitly unsupported.

## 14. Connections

| Edge | Target |
|---|---|
| derived-from | [`Thin Recursive Work Orchestrator — Design`](../DESIGN.md) |
| informed-by | [`Bus Contracts — Discovery`](../../agents-communication-infra/discovery/bus-contracts/README.md) |
| constrained-by | [`A Composable Language for Governed Agent Work`](../../../../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md) |
| evidenced-by | [`Current-state evidence projection`](evidence/CURRENT-STATE-2026-08-05.json) |
| materialized-as | [`Node graph`](nodes/nodes.json) |
| connected-by | [`Typed relation graph`](relations/relations.json) |
| projected-by | [`Current-state graph view`](views/current-state.json) |
| bounded-by | `cyberAlchemy-v2:development/agent-reasoning-engine/design/rwo-integration/ONTOLOGY-BRIDGE.md` |
| governed-by | [`Vault Conventions`](../../../../vault/ontology-conventions.md) |
| does-not-promote | [`Repository Definitions`](../../../../definitions/DEFINITIONS.md) |

## 15. Convention update record

| Field | Record |
|---|---|
| Current rule in v0.1.0 | architecture-property findings carried status and evidence stage but did not distinguish proof freshness, source posture, or correspondence to the proposed architecture |
| Proposed rule in v0.2.0 | every imported current-state finding records orthogonal `proof_status`, `correspondence`, `source_posture`, and `promotion_effect` fields |
| Rationale | prevents observed implementation precedent, proposal state, and executable conformance from collapsing into one claim |
| Migration note | v0.1.0 prose remains valid; projection consumers must treat the four new fields as required and must not infer later-stage proof from them |
| Affected files | this ontology; `evidence/CURRENT-STATE-2026-08-05.json`; private RWO-to-ARE bridge profile; validation receipt |
| Rollback strategy | remove the v0.2.0 projection and bridge, restore the v0.1.0 ontology bytes identified by E2, and leave the accepted research closure unchanged |

This convention change is local to `rwo-architecture@0.2.0`. It does not change the repository-wide
Ontology Vault convention or any canonical definition.

### Graph materialization extension

| Field | Record |
|---|---|
| Current rule before this extension | current-state findings existed as JSON records, while architecture elements, residue, integration stages, gates, and witnesses were addressable only through Markdown sections |
| Proposed rule | materialize every governed object as a typed node and every supported connection as a directed, evidence-bound, zero-authority relation; generate the focused view from the same inputs |
| Rationale | makes the ontology queryable without treating explanatory Markdown or naming similarity as graph truth |
| Migration note | consumers should use stable `node_id` and `relation_id` values; the evidence projection and Markdown remain upstream explanatory inputs, while generated graph bytes must pass `scripts/validate-graph.mjs` |
| Affected files | `nodes/`, `relations/`, `views/`, `schemas/`, `scripts/`, `fixtures/`, evidence projection, validation receipt, and this ontology |
| Rollback strategy | remove the graph package directories and graph links, restore the previous evidence projection and receipt hashes, and retain all v0.2.0 Markdown findings and accepted research unchanged |

## 16. Machine-readable graph package

| Surface | Count | Contract |
|---|---:|---|
| [`nodes/nodes.json`](nodes/nodes.json) | 137 | every node has a kind, branch, sources, owner route, status, runtime posture, confidence, properties, residue, forbidden inferences, and `authority_effect: none` |
| [`relations/relations.json`](relations/relations.json) | 220 | every directed edge resolves both endpoints, cites evidence nodes, declares cycle/runtime posture, and retains zero authority effect |
| [`views/current-state.json`](views/current-state.json) | 1 | covers all nodes and relations, groups ten node kinds, and exposes three bounded trace sequences |
| [`schemas/`](schemas/) | 3 | closed node, relation, and view contracts |
| [`fixtures/`](fixtures/) | 2 | negative authority-effect and missing-endpoint controls |

The graph is generated with `node scripts/build-graph.mjs` and checked with
`node scripts/validate-graph.mjs`. Generation is deterministic over this ontology, the accepted
evidence projection, and the private RWO-to-ARE bridge. Generated adjacency remains a projection;
it cannot resolve residue, select an owner, promote a source, or prove runtime conformance.
