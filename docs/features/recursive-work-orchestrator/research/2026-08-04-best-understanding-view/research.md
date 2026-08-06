# Raw explorer returns — Recursive Work Orchestrator best understanding view

These are the explorer returns preserved verbatim before synthesis. The enclosing headings are indexing metadata only. Explorer recommendations are independent research inputs, not accepted conclusions.

## Agent 1 — Structure explorer

action_id: `spawn-0001`  
role: `structure-explorer`  
status: `pass`  
validation: `pass`  
started_at: `2026-08-04T17:17:00-03:00`  
finished_at: `2026-08-04T17:23:59-03:00`  
artifacts: `[]`

## Research body

### Local evidence boundary

The recommendation treats both local documents as proposal-only candidate semantics, not runtime truth:

- `DESIGN.md:19-32` separates required recursive composition from forbidden recursive orchestration authority.
- `DESIGN.md:87-146` defines the uniform `Work` boundary, immutable `WorkDefinition`, invocation-specific `WorkRun`, leaf binding, and composite substitutability.
- `DESIGN.md:148-220` defines the composition algebra and its primitive event-triggered graph encoding.
- `DESIGN.md:222-285` separates command/event lanes and limits event classifications to structural meanings.
- `DESIGN.md:287-302` assigns domain state, accepted history, and the orchestration cursor to different owners.
- `DESIGN.md:304-330` describes one-root expansion and event-driven routing.
- `DESIGN.md:368-383` supplies twelve invariants suitable for structural badges and negative controls.
- `DESIGN.md:385-399` preserves explicit failure/recovery forms.
- `DESIGN.md:418-428` bounds the expressiveness claim.
- `DESIGN.md:447-460` preserves ten unresolved design questions.
- `ONTOLOGY.md:21-40` declares candidate, non-promoting, non-runtime status.
- `ONTOLOGY.md:42-61` gives the compact type/relation thesis and shallow-authority closure rule.
- `ONTOLOGY.md:63-109` supplies stable element types.
- `ONTOLOGY.md:111-135` supplies typed properties plus forbidden inferences.
- `ONTOLOGY.md:137-170` supplies directed, generally non-transitive relations and their evidence requirements.
- `ONTOLOGY.md:172-187` supplies the hard non-collapse shields.
- `ONTOLOGY.md:189-218` separates definition-only evidence from unavailable runtime evidence.
- `ONTOLOGY.md:220-233` defines bounded observation projections.
- `ONTOLOGY.md:235-253` requires explainable findings and makes missing evidence non-passing.
- `ONTOLOGY.md:281-305` preserves fourteen residue items.
- `ONTOLOGY.md:307-327` explicitly marks implementation/runtime conformance unsupported.

### Compared grammars

| Grammar | Fit | Benefits | Failure modes / cognitive burden | Disposition |
|---|---|---|---|---|
| C4-style hierarchical zoom with a project-specific legend | Strong for orientation and stable cross-view identity. C4 defines context/container/component/code static views, supports selective zoom, and allows alternative interactive visualizations over the same abstractions. Its notation guidance requires explicit element types, descriptions, directional labelled relationships, and legends. [C4 diagrams](https://c4model.com/diagrams), [C4 notation](https://c4model.com/diagrams/notation), [C4 abstractions](https://c4model.com/abstractions) | Small learning surface; naturally supports overview → kernel/components → selected composite internals; compatible with removable projections. | Native C4 abstractions do not distinguish `WorkDefinition`, `WorkRun`, structural graph position, ownership, or typed trigger semantics. Calling a `Work` a C4 component would be misleading because C4’s component has a specific software-structure meaning. C4 alone also cannot show recursive type closure. | **Adapt as the zoom discipline, not as the semantic vocabulary.** |
| ArchiMate 3.2 | Moderate-to-strong semantic fit. The Open Group describes it as an open language for visualizing relationships across architecture domains; its standardized relationship vocabulary includes structural and dynamic relationships, and the exchange format provides model identity usable across projections. [Open Group overview](https://www.opengroup.org/archimate-forum/archimate-overview), [ArchiMate 3.2 status](https://www.opengroup.org/archimate-licensed-downloads), [official model-exchange format](https://www.opengroup.org/open-group-archimate-model-exchange-file-format), [official exchange schema](https://www.opengroup.org/xsd/archimate/3.0/html-model/) | Typed relations can separate composition, assignment/responsibility, triggering, flow, specialization, and realization. Good basis for owner overlays and cross-view model identity. | Full notation is too large for the primary learner view. Generic triggering/flow cannot encode event selector, input mapping, release policy, or authority evidence without profiles. Composition notation may visually suggest lifecycle/authority inheritance unless explicitly shielded. | **Use its relation discipline selectively; reject full ArchiMate as the primary surface.** |
| UML 2.5.1 composite structure + activity + instance notation | Highest formal expressive ceiling. UML’s normative specification and machine-readable metamodel cover composition/generalization, components/interfaces, activity fork/join/decision/control flows, instances, interactions, and state machines. [OMG UML specification](https://www.omg.org/spec/UML/2.5.1) | Can represent definition/instance separation, composite internals, typed ports/contracts, fork/join/gate patterns, and runtime occurrences precisely. | Requires several diagram families, stereotypes, and substantial legend knowledge. A UML composite structure can be misread as runtime containment; an activity diagram can collapse structural edge definitions into occurrences; multiple attempts and owner boundaries become cluttered. | **Keep as an expert/export mapping, not the primary explanatory grammar.** |
| One unfiltered property graph / DOT compound graph | Strong machine projection, weak primary explanation. DOT supports graphs, nodes, edges, subgraphs, clusters, and compound edges. [Graphviz language documentation](https://graphviz.org/documentation/), [DOT guide](https://graphviz.org/pdf/dotguide.pdf) | Directly accommodates ontology entities and relations; clusters can show selected composite bodies. | A giant graph mixes types, runtime occurrences, ownership, evidence, and residue. Cluster nesting alone falsely suggests nested orchestrator authority and makes stable identity hard to perceive. Layout is a projection, not semantics. | **Reject as primary; keep as removable expert projection.** |

### Full component-to-encoding matrix

| Required component | Primary structural encoding | Inspector / secondary encoding | Guardrail |
|---|---|---|---|
| `WorkDefinition` | Solid rounded rectangle labelled `Definition`, stable `work_ref@version`; same geometry for leaf and composite | Contract fields, schemas, commands, events, authority requirements, limits | Never use run-state color on a definition |
| `WorkRun` | Separate outlined instance chip linked by `instantiates` to its definition | `work_run_id`, node address, attempts | Never place it inside the definition as though identical |
| Leaf/composite substitutability | Identical outer `Work` frame; body-kind badge `leaf` or `composite` | Contract comparison table | Shape equality means outer-contract substitutability only |
| Recursive composition | Composite body has a drill-in affordance and a bounded inner graph preview | Breadcrumb retains the same definition identity | Nesting communicates body containment, not authority |
| Sequence | Directed typed edge labelled `release selector → input mapping` | Desugared primitive edge | Do not label merely “next” or infer success |
| Fan-out | One source edge expanding to distinct target edges, each with mapping/authority markers | Branch manifest | No implication of equal authority or shared input |
| Fan-in | Explicit join node/rule badge `all`, `any`, or `quorum(n)` followed by join work | Canonical input-order manifest | Structural readiness does not mean quality or consensus |
| Gate | Ordinary work node with diamond route-selector attached to its emitted route label | Owner/evidence, zero-or-multiple-match failure | Diamond routes; it does not own the gate’s decision |
| Sidecar | Parallel companion node attached by a dashed lifecycle-policy bracket | Start/observe/finish/output contribution policy | Dashed bracket is not a control or authority edge |
| Bounded repetition | Back-edge labelled decision work, `maxRounds`, and exhaustion route | Bound and residue | Never render an unlabeled/unbounded loop |
| Explicit graph composition | Expanded typed node-edge canvas | Operator-to-graph compilation record | Same primitive semantics as convenience forms |
| Root orchestrator | Single top-level kernel node outside all composite body frames | Validate/expand/derive/issue responsibilities | Exactly one root; never repeat it inside composites |
| Bus / `WorkProtocol` | Boundary rail with visibly separate command and event lanes | Delivery semantics and ordering scope | Transport neither decides, authorizes, nor executes |
| Journal | Append-only store adjacent to event lane | Recorded event lineage/replay inputs | Persistence is not execution or necessarily domain-state authority |
| Work units | Definition node plus selected run instance; leaf adapter boundary when applicable | Owned contracts and domain-state declaration | Kernel observes but does not own domain meaning |
| Commands | Solid arrow on command lane, arrowhead toward addressed run/adapter | Envelope, idempotency and authority refs | Request may be rejected; not an accepted fact |
| Events | Hollow/double-line arrow on event lane toward protocol/journal | Producer, event type/classification, causation | Event is a fact, not permission or approval |
| Routing cursor | Small derived-projection card owned by root orchestrator | reducer version, history watermark, enabled nodes | Derived control state, not domain state |
| Domain status | Owner-tagged state badge inside/adjacent to the owning work unit | source event and owner | Never aggregate into an ownerless universal color |
| Confirmation | Gate/work-owned badge and evidence reference | confirmation contract/state | Orchestrator can deliver/observe but cannot mark confirmed |
| External effects | Adapter boundary with authority-reference checkpoint before effect icon | accepted authority reference and effect owner | No direct kernel-to-effect arrow |
| Invariants | Selectable `RWO-Ixx` badges attached to affected types/relations | Expected condition, evidence stage, failure posture | A design-only badge is not a runtime pass |
| Residue | Numbered open-question markers, visually distinct from warnings/errors | Exact `RWO-OQ-*` / `rwo:residue.*`, impact, open status | Residue remains unresolved; no implied repair |
| Attempt | Instance sub-row under `WorkRun`, keyed by `attempt_id` | stale/current classification | Attempts do not change definition or authority basis |
| Event selector | Label capsule on each routing edge | event type, structural class, version | Never infer by event-name sentiment |
| Input mapping | Small transform glyph after selector | declared source/target fields | Mapping validity does not prove semantic fitness |
| Output projection | Boundary arrow from selected child outputs to composite output | projection declaration | Does not manufacture child facts |
| Authority reference | Checkpoint glyph on command/effect boundary | evidence locator and required stage | A reference is not itself the authority decision |
| Status projection | Removable view-layer card with reducer/freshness labels | provenance and observed child events | Cannot create status, confirmation, authority, or freshness |
| Observation projections/findings | Toggleable evidence layer, never base semantic edges | profile, expectation, observation, stage, status, evidence refs | Absence of evidence is unsupported/indeterminate |

### Recursion test

Recursion should appear in three different ways, never collapsed into one glyph:

1. **Type identity at overview zoom:** leaf and composite use the same outer `WorkDefinition` frame, preserving closure and substitutability (`DESIGN.md:87-99,138-146`; `ONTOLOGY.md:69-76`).
2. **Nesting at definition-detail zoom:** selecting a composite reveals its contained `WorkGraph`, with breadcrumbs and the same stable definition ID. Nesting denotes `has-body` and `contains-node`, not runtime authority (`ONTOLOGY.md:144-149,178-179`).
3. **Graph expansion at run-plan zoom:** a separate “expanded plan” projection flattens nested definition bodies into one addressed plan beneath exactly one root orchestrator (`DESIGN.md:121-128,144-146,304-318`; `ONTOLOGY.md:163`).

Showing only nesting invites the false “orchestrators inside orchestrators” reading. Showing only a flattened plan loses reusable composite boundaries. Showing only common shape hides how a composite is operationally expanded.

## Recommended structural grammar

Use a **typed zoomable Work atlas**: C4’s hierarchical zoom discipline, a deliberately small ArchiMate-like typed relation vocabulary, and UML-like definition/instance separation, all projected from one immutable semantic model.

Its primary path is:

`System boundary → one root kernel and owned boundaries → Work-definition topology → selected composite body → optional expanded run plan`

Required primitive vocabulary:

- Entity forms: `WorkDefinition`, `WorkRun`, `Attempt`, root kernel, protocol, journal, adapter, derived projection, residue.
- Relations: `specializes`, `has-body/contains`, `references-work`, `event-triggered invoke`, `instantiates`, `owns`, `records`, `derives-from`, `requires-authority`.
- Stable selection: every projection carries the same ontology or run identifier; no view-local duplicate identity.
- Removable projections: ownership, evidence, learner annotations, and layout coordinates may be removed without changing semantic nodes, relations, identifiers, or source bindings.
- Explicit edge labels: source event selector, target, and input mapping are always inspectable, aligning with C4’s guidance that every directional relationship be labelled.
- Mandatory legend: distinguishes definition/run, structural/temporal, command/event, ownership/observation, candidate/runtime, and containment/authority.
- Claim ceiling always visible: `proposal-only`; definition-level evidence may support structural analysis but not runtime behavior.

This grammar is smaller than full ArchiMate or UML, while retaining their most valuable disciplines. A plain C4 model is insufficient because its native abstraction hierarchy does not correspond to this design’s `Work` algebra. The proposed atlas therefore borrows C4 navigation, not C4 semantics.

## What the structural view cannot explain alone

A structural atlas cannot show:

- the exact causal order of one accepted event, cursor fold, authority check, and resulting command;
- duplicate, delayed, divergent, or stale-attempt handling;
- which attempt was current at a particular moment;
- how a bounded retry unfolds over time;
- whether a command or external effect was actually delivered;
- whether a human understands the model.

Those require a synchronized causal trace, evidence inspector, and later validation. Structural edges must not be animated as if they were observed occurrences.

## Limitations

- No implementation or runtime evidence exists; all encodings are recommendations over proposal-only sources.
- UML and ArchiMate offer richer semantics than used here; the comparison evaluates explanatory fitness for this design, not general language superiority.
- The recommendation has not been browser-tested, accessibility-tested, or human-tested.
- Dynamic topology, streams, migration semantics, quorum meaning, journal authority, and adapter ownership remain unresolved local residue.
- A typed atlas reduces—but cannot eliminate—graph overload. Large expanded plans still require filtering, outline/table equivalents, and stable selection.
- Color cannot carry type, ownership, status, or claim ceiling alone.
- The local Inventory consequence was used only as a hypothesis: stable shared identity and removable learner projections remain recommended because they preserve a single semantic source, not because Inventory grants authority.

## Blockers

None for the bounded research return. Implementation selection is intentionally blocked by scope, and runtime/comprehension claims remain unsupported rather than failed.

## Agent 2 — Flow explorer

{
  "action_id": "spawn-0002",
  "role": "flow-explorer",
  "status": "pass",
  "started_at": "2026-08-04T17:18:00-03:00",
  "finished_at": "2026-08-04T17:24:16-03:00",
  "research_body": {
    "claim_ceiling": "Design analysis and paper-executable walkthrough only. No recursive-work runtime, replay UI, browser artifact, or human-comprehension result was observed.",
    "local_evidence": [
      {
        "selector": "DESIGN.md:19-32",
        "finding": "Recursive composition is required, but recursive orchestration authority is forbidden; a trace must show one root scheduler even when a composite is expanded."
      },
      {
        "selector": "DESIGN.md:54-68",
        "finding": "The kernel validates and expands a graph, responds to events with idempotent commands, and rebuilds only its routing cursor; domain judgment stays outside it."
      },
      {
        "selector": "DESIGN.md:116-128",
        "finding": "WorkRun, node path, and attempt are distinct stable identities. A structural address does not convey authority or parent status."
      },
      {
        "selector": "DESIGN.md:148-220",
        "finding": "Sequence, fan-out, fan-in, gate, sidecar, and bounded repetition compile to event-triggered edges; the temporal view must preserve each operator's distinct release semantics."
      },
      {
        "selector": "DESIGN.md:222-285",
        "finding": "Commands and events are separate lanes. The envelope already supplies message, run, node, attempt, correlation, causation, authority, sequence, and idempotency identities. Ordering is per work_run_id, not global."
      },
      {
        "selector": "DESIGN.md:287-330",
        "finding": "The journal owns accepted history, the root owns the rebuildable routing cursor, and each work owns domain state. The accepted-event fold and resulting command publication are the causal spine."
      },
      {
        "selector": "DESIGN.md:368-399",
        "finding": "The trace needs explicit duplicate, conflict, stale-attempt, restart, cancellation, compensation, and sidecar-failure representations; it must not silently normalize these cases away."
      },
      {
        "selector": "ONTOLOGY.md:63-109",
        "finding": "The element catalog distinguishes WorkRun, Attempt, messages, protocol, journal, cursor, projection, adapter, authority reference, domain state, and confirmation state, supplying stable cross-view selection identities."
      },
      {
        "selector": "ONTOLOGY.md:137-170",
        "finding": "Structural relations and temporal relations are separately typed. receives, emits, issues, delivered-by, and recorded-by should become occurrence edges without rewriting contains-node or references-work edges."
      },
      {
        "selector": "ONTOLOGY.md:172-187",
        "finding": "Hard inference shields prohibit bus authority, kernel domain-state ownership, terminal-success collapse, projection authority, parent authority inheritance, and unsupported idempotency claims."
      },
      {
        "selector": "ONTOLOGY.md:189-233",
        "finding": "Runtime profiles require evidence not yet present. A definition map, graph map, journal replay, delivery trace, authority audit, and status view each have different proof ceilings."
      },
      {
        "selector": "ONTOLOGY.md:281-327",
        "finding": "Replay migrations, delivery guarantees, authority references, sidecar ownership, and runtime conformance remain open or unsupported."
      }
    ],
    "external_evidence": [
      {
        "source": "OMG UML 2.5.1 specification",
        "url": "https://www.omg.org/spec/UML/2.5.1",
        "use": "Primary standard for lifelines, messages, execution occurrences, interaction fragments, and state-machine notation."
      },
      {
        "source": "OMG BPMN 2.0.2 specification",
        "url": "https://www.omg.org/spec/BPMN/2.0.2",
        "use": "Primary standard for explicit sequence flow, parallel divergence/convergence, events, gateways, and token-oriented workflow semantics."
      },
      {
        "source": "W3C SCXML 1.0 Recommendation",
        "url": "https://www.w3.org/TR/scxml/",
        "use": "Primary event-based state-machine standard with run-to-completion processing; useful for a selected work unit's local transition view."
      },
      {
        "source": "OpenTelemetry tracing specification overview",
        "url": "https://opentelemetry.io/docs/specs/otel/overview/",
        "use": "Official specification describing a trace as a span DAG and links for causal relationships that do not fit one parent-child tree."
      },
      {
        "source": "OpenTelemetry tracing API",
        "url": "https://opentelemetry.io/docs/specs/otel/trace/api/",
        "use": "Official definitions for span context, parentage, links, events, status, and producer/consumer span kinds."
      },
      {
        "source": "OpenTelemetry messaging span conventions",
        "url": "https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/",
        "use": "Official producer/consumer model; recommends span links for asynchronous and batch correlation because a span has only one parent."
      },
      {
        "source": "W3C Trace Context Recommendation",
        "url": "https://www.w3.org/TR/trace-context/",
        "use": "Primary propagation standard for trace-id and parent-id. It supports correlation but does not establish domain authority or complete causality."
      },
      {
        "source": "Lamport, Time, Clocks, and the Ordering of Events in a Distributed System",
        "url": "https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/",
        "use": "Original paper establishing happens-before as a partial order; justifies refusing to interpret wall-clock or arrival order as causality."
      }
    ],
    "temporal_grammars": [
      {
        "name": "UML interaction plus state-machine drill-down",
        "encoding": "Lifelines for root kernel, bus, journal, each work/adapter, authority adapter, and effect boundary; command/event arrows; combined fragments for alt, par, loop, and optional sidecar; a linked state machine for the selected work.",
        "benefits": "Strong actor/owner visibility and readable gate, retry, and request/response walkthroughs. UML provides standardized interaction and state-machine vocabularies.",
        "failure_modes": "A sequence diagram's vertical order is easily mistaken for a global clock; fan-in causality and duplicate deliveries become cluttered; lifeline nesting can falsely suggest nested orchestrators.",
        "fit": "Good static explanation and printable equivalent, but insufficient as the sole replay grammar."
      },
      {
        "name": "BPMN token and gateway flow",
        "encoding": "Tasks as work occurrences, parallel gateways for fan-out/fan-in, exclusive gateways for declared gate labels, boundary/event constructs for signals, and bounded loop annotations.",
        "benefits": "Most immediately legible grammar for sequence, branch, join, and bounded repetition. Token advancement makes release conditions concrete.",
        "failure_modes": "A token can be mistaken for domain status, approval, or authority; pools/lanes invite organizational ownership readings; sidecar non-control and message identity are awkward; runtime occurrence and immutable definition can collapse.",
        "fit": "Excellent structural-temporal overview, unsafe unless every token is explicitly labeled 'derived routing eligibility, not work status'."
      },
      {
        "name": "Causal event DAG with distributed-trace lanes",
        "encoding": "Immutable occurrence cards keyed by message_id; solid causation edges keyed by causation_id; dashed same-run correlation; producer/consumer spans or intervals; multi-parent links for joins; independent wall-clock axis; per-run sequence shown as scoped evidence rather than universal order.",
        "benefits": "Best match for asynchronous commands/events, fan-out, multi-cause fan-in, delayed and duplicate delivery, retries, and sidecars. Lamport's partial order and OpenTelemetry links prevent a false single parent tree.",
        "failure_modes": "Raw tracing conventions do not model graph definition, work-owned status, confirmation, or authority. Span status must never substitute for domain status. A trace is an observation/projection, not proof that an external effect occurred exactly once.",
        "fit": "Best primary causal grammar when augmented by explicit owner/state/effect fields and linked back to the structure view."
      },
      {
        "name": "SCXML-style local transition projection",
        "encoding": "One selected WorkRun/Attempt displayed as work-owned states and event-triggered transitions, with command receipts as inputs and emitted events as outputs.",
        "benefits": "Clarifies that domain and confirmation status belong to the selected work and that one event may trigger a bounded set of transitions.",
        "failure_modes": "Run-to-completion semantics would be false if projected onto the whole asynchronous system; it hides graph topology and cross-work causality.",
        "fit": "Inspector drill-down only, not the global temporal view."
      }
    ],
    "recommended_causal_grammar": {
      "name": "Causal occurrence ledger with synchronized lane replay",
      "core_rule": "The authoritative visual order is a partial order induced by explicit causation_id edges and declared graph-release edges. Per-work-run sequence, persisted acceptance order, and occurred_at are separate sortable attributes; none may silently create causality.",
      "lanes": [
        "Root orchestrator/cursor",
        "Command lane",
        "Target work or executor adapter",
        "Event lane",
        "Journal acceptance",
        "Gate/confirmation owner when selected",
        "Authority adapter and external-effect boundary",
        "Sidecar lane, visually detached from primary control"
      ],
      "occurrence_card": [
        "message_id and kind",
        "message_type and structural event class",
        "work_ref, work_run_id, node_path, attempt_id",
        "producer and intended consumer",
        "correlation_id and causation_id",
        "idempotency_key",
        "journal acceptance disposition",
        "cursor delta and reducer version",
        "domain-status owner plus explicitly reported status, if any",
        "confirmation owner plus explicit evidence state, if any",
        "authority_ref and effect disposition",
        "claim ceiling: definition walkthrough, fixture, runtime trace, or telemetry"
      ],
      "edge_styles": {
        "solid_arrow": "explicit causation",
        "double_incoming_solid": "fan-in release with named policy and canonical manifest",
        "dashed_line": "correlation only",
        "thin_gray_line": "transport/delivery occurrence",
        "blue_fold_marker": "journal event folded into cursor",
        "red_quarantine": "same idempotency key with divergent bytes",
        "hollow_duplicate": "identical duplicate accepted as no new causal fact",
        "faded_stale": "retained stale-attempt observation that cannot release current edges"
      },
      "controls": [
        "step by causal frontier, not frame time",
        "play/pause and previous/next accepted fact",
        "jump to cause, consequences, work run, attempt, or graph edge",
        "toggle wall-clock, journal acceptance order, and causal partial order without conflating them",
        "show duplicate/delayed/out-of-order/terminal overlays",
        "reduced-motion mode where highlighting changes but geometry does not move",
        "text/table export preserving the exact occurrence and edge identities"
      ],
      "stable_selection": "Use semantic source identities (`work_ref`, graph node/edge IDs) for definition selection and occurrence identities (`work_run_id`, `attempt_id`, `message_id`) for replay selection. A view may synchronize these IDs but must never replace them with screen coordinates or transient animation objects.",
      "cannot_explain_alone": "The event trace cannot establish the complete reusable Work contract, recursive substitutability, all graph constraints, ontology type hierarchy, or why a missing event is impossible rather than merely unobserved. It must be paired with a structure view and ownership/inspector projection."
    },
    "paper_traces": [
      {
        "scenario": "sequence with a gate",
        "identities": "correlation_id=C-GATE; work runs R-A, R-G, R-B; every row has a unique message_id Mnn; each emitted event causation_id points to the command it answers, and each new command points to the accepted release event that caused it.",
        "steps": [
          {
            "n": 1,
            "command_or_event": "M01 command invoke A",
            "producer": "root orchestrator",
            "consumer": "A adapter",
            "correlation_causation": "C-GATE / root invocation",
            "persisted_fact": "No domain fact; command delivery is cursor/outbox evidence, not a journal-emitted work fact.",
            "derived_cursor": "A invocation delivered under its idempotency key.",
            "domain_status_owner": "A",
            "confirmation_owner": "gate G, not yet active",
            "external_effect_permitted": "Only if A's command authority_ref is accepted by its adapter."
          },
          {
            "n": 2,
            "command_or_event": "M02 event A.release",
            "producer": "A",
            "consumer": "journal then root reducer",
            "correlation_causation": "C-GATE / M01",
            "persisted_fact": "Accepted A release event; terminal/release does not mean approved.",
            "derived_cursor": "sequence edge A->G satisfied; G enabled.",
            "domain_status_owner": "A",
            "confirmation_owner": "G",
            "external_effect_permitted": "No; an event is not effect permission."
          },
          {
            "n": 3,
            "command_or_event": "M03 command invoke G",
            "producer": "root orchestrator",
            "consumer": "gate G",
            "correlation_causation": "C-GATE / M02",
            "persisted_fact": "No confirmation fact.",
            "derived_cursor": "G invocation delivered.",
            "domain_status_owner": "G",
            "confirmation_owner": "G",
            "external_effect_permitted": "No downstream effect."
          },
          {
            "n": 4,
            "command_or_event": "M04 command confirmation-provided",
            "producer": "authorized confirmation adapter",
            "consumer": "G",
            "correlation_causation": "C-GATE / external confirmation interaction",
            "persisted_fact": "Command receipt is not confirmation state.",
            "derived_cursor": "No route enabled until G emits an accepted route event.",
            "domain_status_owner": "G",
            "confirmation_owner": "G",
            "external_effect_permitted": "No."
          },
          {
            "n": 5,
            "command_or_event": "M05 event G.route.approved",
            "producer": "G",
            "consumer": "journal then root reducer",
            "correlation_causation": "C-GATE / M04",
            "persisted_fact": "G's accepted decision event with evidence reference.",
            "derived_cursor": "Exactly one approved edge matched; B enabled. Zero/multiple would block.",
            "domain_status_owner": "G",
            "confirmation_owner": "G",
            "external_effect_permitted": "Still no effect until B command authority is checked."
          },
          {
            "n": 6,
            "command_or_event": "M06 command invoke B",
            "producer": "root orchestrator",
            "consumer": "B adapter",
            "correlation_causation": "C-GATE / M05",
            "persisted_fact": "No result fact.",
            "derived_cursor": "B delivery recorded.",
            "domain_status_owner": "B",
            "confirmation_owner": "G remains owner of its decision",
            "external_effect_permitted": "Yes only at B's adapter after accepted authority_ref; the gate label alone is insufficient."
          }
        ]
      },
      {
        "scenario": "fan-out followed by fan-in",
        "identities": "correlation_id=C-FAN; branch runs R-B1 and R-B2; join run R-J; branch events E1/E2 are concurrent unless an explicit causal edge says otherwise.",
        "steps": [
          {
            "n": 1,
            "command_or_event": "F01 event source.release",
            "producer": "source work",
            "consumer": "journal/root reducer",
            "correlation_causation": "C-FAN / source invoke",
            "persisted_fact": "Accepted source release.",
            "derived_cursor": "Two declared fan-out edges become eligible.",
            "domain_status_owner": "source work",
            "confirmation_owner": "none",
            "external_effect_permitted": "No."
          },
          {
            "n": 2,
            "command_or_event": "F02/F03 commands invoke B1 and B2",
            "producer": "root orchestrator",
            "consumer": "B1/B2 adapters",
            "correlation_causation": "C-FAN / both caused by F01",
            "persisted_fact": "No shared status or authority fact.",
            "derived_cursor": "Both deliveries recorded independently.",
            "domain_status_owner": "B1 and B2 separately",
            "confirmation_owner": "none unless branch contracts name one",
            "external_effect_permitted": "Independently checked per command and adapter."
          },
          {
            "n": 3,
            "command_or_event": "F04 event B2.release arrives before F05 event B1.release",
            "producer": "B2 then B1",
            "consumer": "journal/root reducer",
            "correlation_causation": "C-FAN / F03 and F02 respectively; neither branch event causes the other",
            "persisted_fact": "Two accepted branch facts, each with its own scoped sequence.",
            "derived_cursor": "After F04, all-policy unsatisfied; after F05, all-policy satisfied.",
            "domain_status_owner": "Each branch",
            "confirmation_owner": "none",
            "external_effect_permitted": "No."
          },
          {
            "n": 4,
            "command_or_event": "F06 command invoke join J",
            "producer": "root orchestrator",
            "consumer": "J",
            "correlation_causation": "C-FAN / multi-cause links to F04 and F05",
            "persisted_fact": "No reconciliation result yet.",
            "derived_cursor": "Fan-in fired once with canonically ordered input manifest.",
            "domain_status_owner": "J owns reconciliation meaning",
            "confirmation_owner": "J or a separate gate if declared",
            "external_effect_permitted": "Only after J command authority check."
          }
        ]
      },
      {
        "scenario": "primary with non-controlling sidecar and one bounded retry",
        "identities": "correlation_id=C-RETRY; primary WorkRun R-P has attempts A1 and A2; sidecar WorkRun R-S is distinct; max_rounds=2 with exhaustion route.",
        "steps": [
          {
            "n": 1,
            "command_or_event": "S01/S02 commands invoke primary A1 and sidecar",
            "producer": "root orchestrator",
            "consumer": "P adapter and S adapter",
            "correlation_causation": "C-RETRY / common composite invocation; sibling commands do not cause each other",
            "persisted_fact": "No shared state.",
            "derived_cursor": "Primary and sidecar deliveries recorded.",
            "domain_status_owner": "P and S separately",
            "confirmation_owner": "retry decision work D",
            "external_effect_permitted": "Checked independently; sidecar has no primary authority."
          },
          {
            "n": 2,
            "command_or_event": "S03 diagnostic sidecar.observed",
            "producer": "S",
            "consumer": "journal/observer",
            "correlation_causation": "C-RETRY / selected primary observation",
            "persisted_fact": "Diagnostic fact only.",
            "derived_cursor": "No primary release edge unless explicitly selected.",
            "domain_status_owner": "S",
            "confirmation_owner": "D",
            "external_effect_permitted": "No control effect on P."
          },
          {
            "n": 3,
            "command_or_event": "S04 event P.A1.failed terminal",
            "producer": "P attempt A1",
            "consumer": "journal/root reducer",
            "correlation_causation": "C-RETRY / S01",
            "persisted_fact": "A1 terminal failure; retained under attempt A1.",
            "derived_cursor": "Declared edge enables retry decision D; does not itself retry.",
            "domain_status_owner": "P",
            "confirmation_owner": "D",
            "external_effect_permitted": "No."
          },
          {
            "n": 4,
            "command_or_event": "S05 invoke D; S06 event D.route.retry",
            "producer": "root then D",
            "consumer": "D then journal/root reducer",
            "correlation_causation": "C-RETRY / S04 then S05",
            "persisted_fact": "Accepted bounded retry decision.",
            "derived_cursor": "Round increments to 2; A2 enabled because bound remains.",
            "domain_status_owner": "D owns its decision; P owns primary status",
            "confirmation_owner": "D",
            "external_effect_permitted": "No primary effect yet."
          },
          {
            "n": 5,
            "command_or_event": "S07 command invoke P attempt A2",
            "producer": "root orchestrator",
            "consumer": "P adapter",
            "correlation_causation": "C-RETRY / S06",
            "persisted_fact": "A1 remains history; it is not overwritten.",
            "derived_cursor": "A2 delivery recorded with new attempt_id and stable WorkRun identity.",
            "domain_status_owner": "P",
            "confirmation_owner": "D",
            "external_effect_permitted": "Only after A2 authority/idempotency check."
          },
          {
            "n": 6,
            "command_or_event": "S08 event P.A2.release; S09 sidecar terminal",
            "producer": "P then S",
            "consumer": "journal/root reducer",
            "correlation_causation": "C-RETRY / S07; sidecar termination follows its lifecycle policy, not control of P",
            "persisted_fact": "A2 release and sidecar terminal are separate facts.",
            "derived_cursor": "Primary successor enabled; sidecar awaited/detached/cancel-requested exactly as policy states.",
            "domain_status_owner": "P and S separately",
            "confirmation_owner": "D retains ownership of retry decision",
            "external_effect_permitted": "Only through the successor's authority adapter."
          }
        ]
      }
    ],
    "abnormal_event_display": {
      "duplicate": "Render a second hollow occurrence linked to the first by idempotency_key, labeled 'no new cursor transition' when bytes match.",
      "divergent_duplicate": "Render red quarantine with both digests; do not merge or advance.",
      "delayed": "Keep occurred_at and accepted_at separately; position causally by explicit edges and optionally show wall-clock skew.",
      "out_of_order": "Show arrival/acceptance rank separately from per-run sequence. Never drag nodes into an invented global order.",
      "stale_attempt": "Retain as faded evidence under its attempt; place a barrier on any release edge.",
      "terminal": "Use terminal shape plus the emitted domain label; never use a universal green success color."
    },
    "misleading_animations_to_reject": [
      "A single token visibly flowing through the bus as though transport owns or decides the workflow.",
      "Automatically advancing from a command to a domain state before an accepted event exists.",
      "Sorting every event by occurred_at or arrival time and animating that order as causality.",
      "Drawing fan-out branches as causally ordered siblings.",
      "Animating fan-in after the visually last branch rather than after the named release policy is satisfied.",
      "Turning a composite into an expanding nested orchestrator or nested scheduler lane.",
      "Coloring terminal as green/success, or treating it as approval or effect permission.",
      "Showing a confirmation-provided command as confirmed before the gate emits its own accepted route event.",
      "Letting a sidecar's warning, failure, or completion stop or advance the primary without an explicit edge/policy.",
      "Reusing one node identity for multiple attempts, thereby erasing failed-attempt history.",
      "Collapsing identical and divergent duplicates into the same visual treatment.",
      "Replaying a journal as if it proves truth, completeness of external work, or exactly-once effects.",
      "Moving nodes during playback so cross-view identity depends on screen position.",
      "Animating an unbounded retry loop or omitting the round counter and exhaustion route."
    ],
    "limitations": [
      "The walkthrough uses illustrative message names; exact command/event vocabularies remain candidate contracts.",
      "The design leaves journal authority versus copied work-owned evidence unresolved (DESIGN.md:451-452; ONTOLOGY.md:287-288).",
      "Cross-host guarantees, reducer/schema migration, and minimal authority-reference semantics are unresolved.",
      "OpenTelemetry supplies correlation and causal-link patterns, not the orchestrator's domain semantics, authority model, or accepted-history contract.",
      "UML, BPMN, and SCXML are compared as explanatory grammars; no conformance claim or implementation-stack recommendation is made.",
      "No runtime fixture, replay reducer, UI prototype, accessibility test, or learner study exists."
    ]
  },
  "blockers": [],
  "artifacts": [],
  "validation": "pass"
}

## Agent 3 — Learning explorer

{
  "action_id": "spawn-0003",
  "role": "learning-explorer",
  "status": "pass",
  "started_at": "2026-08-04T17:00:00-03:00",
  "finished_at": "2026-08-04T17:24:26-03:00",
  "artifacts": [],
  "research_body": {
    "local_evidence": [
      {
        "selector": "DESIGN.md:19-32,34-85",
        "finding": "The visible explanation must begin with an explicit proposal-only ceiling and distinguish recursive composition from prohibited recursive orchestration authority; it must not make UI projection, approval, domain meaning, or runtime existence appear kernel-owned."
      },
      {
        "selector": "DESIGN.md:87-220",
        "finding": "The structural view needs a stable Work/WorkDefinition/WorkRun/graph anatomy, plus composition forms whose common primitive is an event-triggered connection."
      },
      {
        "selector": "DESIGN.md:222-330; DESIGN.md:368-399",
        "finding": "A causal view must preserve command/event lane separation, journal versus cursor versus domain-state ownership, and the proposal’s fail-closed/recovery distinctions."
      },
      {
        "selector": "DESIGN.md:332-366; DESIGN.md:418-460",
        "finding": "The illustrative composite is the right finite walkthrough, but must be labelled illustrative and proposed; bounded expressiveness and all open questions remain inspectable residue."
      },
      {
        "selector": "ONTOLOGY.md:21-40,42-61,63-187",
        "finding": "The ontology is candidate-local and non-authoritative. Its type, property, relation, and shield catalogs supply an inspectable semantic source, including the non-collapse rules learner views must never override."
      },
      {
        "selector": "ONTOLOGY.md:189-233,235-279,281-327",
        "finding": "Profiles, observations, finding shape, evidence ledger, source ledger, residue, and validation status define the needed ownership/proof view. Runtime evidence and promotion are explicitly unsupported/not granted."
      },
      {
        "selector": ".arcanum/inventory/entries/interactive-ontology-learning-map-strategy-result-synthesis.md:81-160; .arcanum/inventory/entries/iolm-workable-example-research-strategy-result-synthesis.md:104-185",
        "finding": "Use one immutable, revision-pinned semantic snapshot with separately stored semantic, learner, and navigation projections. Graph, outline, and table are co-primary, share full stable-ID selection, and feed one provenance inspector."
      },
      {
        "selector": ".arcanum/inventory/entries/body-war-business-view-novice-comprehension-review-result-synthesis.md:77-145; .arcanum/inventory/entries/learning-graph-next-route-guide-research-strategy-result-synthesis.md:73-145",
        "finding": "Learner aids are removable and cannot create semantics, status, or route execution. Browser evidence can establish a stimulus’s structure and interaction, never learner comprehension."
      },
      {
        "selector": ".arcanum/inventory/entries/cyberalchemy-orchestrator-reasoning-engine-purpose-strategy-result-synthesis.md:77-123",
        "finding": "The explanation must not depict the repository as a reasoning engine or imply that an explanatory view derives new semantic conclusions."
      }
    ],
    "external_evidence": [
      {
        "source": "[Shneiderman, The Eyes Have It (1996)](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)",
        "use": "Supports the learner sequence overview → zoom/filter → details on demand. Apply it as orient → focus → inspect, not as a claim that a graphic itself proves understanding."
      },
      {
        "source": "[North & Shneiderman, Snap-Together Visualization (2000)](https://www.cs.umd.edu/users/ben/papers/North2000Snapa.pdf)",
        "use": "Supports coordinated multiple views with linked selection. Its reported overview-detail performance evidence is not transferable as evidence that this proposed RWO view will be comprehended."
      },
      {
        "source": "[Tversky, Morrison & Betrancourt, Animation: Can It Facilitate? (2002)](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf)",
        "use": "Use discrete, user-paced scenario steps with visible state rather than autoplay animation; animation can overload perception when fast or complex."
      },
      {
        "source": "[Mayer, Segmenting Principle (2009)](https://www.cambridge.org/core/books/abs/multimedia-learning/segmenting-principle/37240877DDA0362355ADB39936027982)",
        "use": "Supports learner-paced segmentation of the composite walkthrough and pre-training of Work, event, command, journal, cursor, and gate vocabulary."
      },
      {
        "source": "[W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [Focus Order understanding](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)",
        "use": "Requires meaningful keyboard focus order, text alternatives/equivalent structure, visible focus, non-text contrast, reflow considerations, and an option to disable non-essential interaction animation."
      },
      {
        "source": "[WAI-ARIA APG Tree View pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/)",
        "use": "Supplies a concrete keyboard contract if the semantic outline is implemented as a tree; selection and focus must remain distinguishable."
      },
      {
        "source": "[CAST UDL Guidelines](https://udlguidelines.cast.org/static/udlg3-graphicorganizer-digital-numbers-a11y.pdf)",
        "use": "Supports multiple representations and navigation paths, but is a design rationale rather than a completed accessibility or learning evaluation."
      }
    ],
    "interaction_architectures": [
      {
        "name": "Annotated-document-first",
        "shape": "A linear DESIGN/ONTOLOGY reader with expandable diagrams and deep links.",
        "strength": "Lowest semantic translation risk; naturally exposes all prose and residue.",
        "weakness": "Poor at connecting composition, event flow, and ownership across sections; forces novices to construct the system model unaided.",
        "verdict": "Retain as the text/table equivalent and source inspector, not as the sole learner experience."
      },
      {
        "name": "Single universal graph canvas",
        "shape": "One force-directed graph containing every design and ontology entity, relation, evidence, and learner cue.",
        "strength": "Can expose topology and support expert free exploration.",
        "weakness": "Conflates structural, temporal, ownership, and learner relations; visually overloads novices; risks implying unstated edges and hides prose-only boundaries.",
        "verdict": "Reject as the primary grammar. A graph may be a focused structural projection only."
      },
      {
        "name": "Synchronized Structure, Flow, Ownership views",
        "shape": "Three co-primary projections over an immutable semantic snapshot: structural graph/outline, finite scenario playback, and ownership/proof ledger; one shared selected stable ID and one inspector.",
        "strength": "Separates what exists in the candidate model, how a declared composite would route, and who may claim/decide what. It matches the source’s explicit non-collapse boundaries and permits novice progressive disclosure plus expert cross-checking.",
        "weakness": "Requires a projection compiler, strict stable-ID binding, and a text/table equivalent to avoid making the visual view privileged.",
        "verdict": "Recommended."
      },
      {
        "name": "Guided scenario-first explainer",
        "shape": "A narrated, stepwise walkthrough of the minimal API composite, with a later jump to source sections.",
        "strength": "Strong orientation for the novice’s concrete question.",
        "weakness": "A single scenario can make illustrative syntax or proposed behavior look implemented and can underrepresent ontology shields, residue, and alternative forms.",
        "verdict": "Use as one mode inside the synchronized system, never as the whole explanation."
      }
    ],
    "recommended_learner_grammar": {
      "name": "Orient → Focus → Inspect → Trace → Bound → Compare",
      "rules": [
        "Orient: show a compact claim-ceiling banner, one-root-authority rule, and three selectable lenses: Structure, Flow, Ownership/Proof.",
        "Focus: selecting an item in graph, semantic outline, or relation table selects the same immutable stable ID in every projection; navigation edges are display-only.",
        "Inspect: a single inspector card shows source heading/line selector, semantic fields, allowed relations, forbidden inferences, evidence stage, owner, and claim ceiling.",
        "Trace: scenario playback is a finite, user-paced declared-event walkthrough of DESIGN §9; each step marks proposed/illustrative state and has a static previous/next transcript.",
        "Bound: every view exposes what it cannot establish—especially no implementation/runtime evidence, no promotion, no authority decision, and no human-comprehension claim.",
        "Compare: expert mode permits side-by-side graph/outline/table and profile/finding comparison without creating relations or changing source bytes."
      ],
      "semantic_integrity_contract": "Semantic nodes, relations, source digests, and source selectors are read-only inputs. Learner routes, layout coordinates, labels, focus state, scenario sequencing, and navigation links live in removable projections. Deleting them leaves semantic bytes unchanged."
    },
    "novice_journey": [
      "Enter on the proposal-only banner and answer: this is a candidate architecture, not a runtime.",
      "Read the one-sentence thesis, then choose “Who owns what?”",
      "Use the Ownership lens to compare Work unit/adapter domain state, Journal accepted history, and root orchestrator cursor; inspect the no-kernel-domain-state shield.",
      "Choose the illustrated composite and advance one user-paced event step at a time: research → fan-out reviews → fan-in synthesis → approval gate → implement/revise/reject, with the sidecar visible but non-authoritative.",
      "Open the boundary notice to distinguish a gate decision from routing, a terminal event from success, and a status projection from authority.",
      "Finish at the residue panel: implementation, runtime conformance, promotion, and human comprehension remain unsupported."
    ],
    "expert_journey": [
      "Open Structure with the semantic outline/table and filter to WorkDefinition, WorkRun, graph, edge, command, event, journal, cursor, and authority reference.",
      "Select an EventTriggeredEdge and inspect exact selector, input mapping, source/design selector, allowed relations, cycle policy, and no-inheritance shield.",
      "Switch to Flow, scrub the illustrative composite’s declared event path, and compare command versus event lanes, idempotency, journal append, cursor reduction, and fail-closed gate matching.",
      "Switch to Ownership/Proof to test each assertion against evidence stage and profile; inspect RWO-I01–I12 and the runtime-evidence profile’s missing witness.",
      "Use graph/outline/table equivalence to detect projection-only differences, then inspect source ledger and all fourteen residue entries before treating an implication as settled."
    ],
    "section_mapping": {
      "DESIGN.md": [
        ["§1 Purpose", "overview: bounded-pipeline promise and scope", "focused: operator palette", "inspector: kernel does/does-not-own", "scenario: orient", "boundary: no domain judgment"],
        ["§2 Thesis", "overview: Work and event-response thesis", "focused: four kernel responsibilities", "inspector: root expansion", "scenario: expand", "boundary: no semantic judgment"],
        ["§3 Non-goals", "overview: explicit out-of-scope ring", "focused: owner matrix", "inspector: non-goal rationale", "scenario: gate versus kernel", "boundary: UI/projection and authority excluded"],
        ["§4 Uniform Work contract", "overview: Work anatomy", "focused: contract schema", "inspector: fields and versions", "scenario: invoke", "boundary: contract is proposed"],
        ["§5 Composition algebra", "overview: composition catalog", "focused: event-triggered edge graph", "inspector: operator desugaring", "scenario: composite path", "boundary: syntax is not authority"],
        ["§6 Protocol/bus", "overview: two-lane diagram", "focused: envelope and delivery", "inspector: command/event fields", "scenario: delivery", "boundary: bus neither decides nor executes"],
        ["§7 State and ownership", "overview: three-state owner matrix", "focused: cursor lineage", "inspector: freshness/reducer", "scenario: replay", "boundary: projection cannot manufacture facts"],
        ["§8 Runtime flow", "overview: flow diagram", "focused: accepted-event steps", "inspector: each step’s input/output", "scenario: six-step trace", "boundary: proposed flow, not observed runtime"],
        ["§9 Minimal API example", "overview: composite thumbnail", "focused: nested composition tree", "inspector: each operator", "scenario: full walkthrough", "boundary: illustrative syntax only"],
        ["§10 Validation invariants", "overview: 12 invariant checklist", "focused: selected invariant", "inspector: failure posture/profile", "scenario: failing branch", "boundary: no runtime pass implied"],
        ["§11 Failure/recovery", "overview: recovery categories", "focused: selected failure", "inspector: declared policy", "scenario: duplicate/restart/stale attempt", "boundary: no universal retry/rollback"],
        ["§12 Existing architecture", "overview: provenance neighborhood", "focused: source relationship", "inspector: source selector", "scenario: none", "boundary: does not promote discovery"],
        ["§13 Honest any-pipeline claim", "overview: bounded claim", "focused: excluded counterexamples", "inspector: claim conditions", "scenario: unsupported topology", "boundary: not universal expressiveness"],
        ["§14 Ontology handoff", "overview: design-to-ontology bridge", "focused: required types/relations", "inspector: source mapping", "scenario: none", "boundary: no redefinition/promotion"],
        ["§15 Open questions", "overview: residue count", "focused: question category", "inspector: why it matters", "scenario: unresolved branch", "boundary: unresolved remains unresolved"],
        ["§16 Connections", "overview: source links", "focused: relation type", "inspector: target provenance", "scenario: none", "boundary: candidate connection only"]
      ],
      "ONTOLOGY.md": [
        ["§1 Identity/boundary", "overview: ontology posture", "focused: identity card", "inspector: authority_effect none", "scenario: none", "boundary: no canonical/runtime/promotion effect"],
        ["§2 Thesis", "overview: semantic anatomy", "focused: root/graph/cursor diagram", "inspector: closure and shallow-authority rules", "scenario: expand", "boundary: one root only"],
        ["§3 Element-type catalog", "overview: type groups", "focused: filtered type graph", "inspector: type definition/source", "scenario: typed participant", "boundary: local namespace only"],
        ["§4 Typed-property catalog", "overview: property groups", "focused: subject/property table", "inspector: required stage/forbidden inference", "scenario: message/property", "boundary: properties do not create authority"],
        ["§5 Allowed relations", "overview: relation families", "focused: directed relation graph", "inspector: cardinality/cycle/evidence", "scenario: edge firing", "boundary: non-transitivity unless stated"],
        ["§6 Forbidden relations/shields", "overview: shield ledger", "focused: selected counterexample", "inspector: prohibited inference", "scenario: rejected implication", "boundary: hard non-collapse"],
        ["§7 Architecture profiles", "overview: profile comparison", "focused: RWO-I01–I12 table", "inspector: minimum evidence", "scenario: definition-only versus runtime", "boundary: runtime profile unfulfilled"],
        ["§8 Observation projections", "overview: observation menu", "focused: input-to-observable map", "inspector: cannot-establish field", "scenario: proposed replay", "boundary: observation never authority"],
        ["§9 Explainable finding shape", "overview: finding template", "focused: evidence chain", "inspector: status/evidence-stage", "scenario: unsupported finding", "boundary: missing evidence never pass"],
        ["§10 Evidence/confidence ledger", "overview: candidate claim ledger", "focused: one claim", "inspector: evidence and commitment confidence", "scenario: counterexample need", "boundary: no confidence promotion"],
        ["§11 Source ledger", "overview: source hierarchy", "focused: selected source", "inspector: authority/use", "scenario: provenance jump", "boundary: supporting sources do not promote"],
        ["§12 Residue", "overview: 14 unresolved items", "focused: one residue", "inspector: ontology impact", "scenario: unresolved decision", "boundary: preserve open status"],
        ["§13 Validation status", "overview: status matrix", "focused: selected check", "inspector: evidence", "scenario: unsupported runtime check", "boundary: FLAG is not conformance/promotion"],
        ["§14 Connections", "overview: ontology links", "focused: connection type", "inspector: target selector", "scenario: none", "boundary: does-not-promote retained"]
      ]
    },
    "measurable_unexecuted_acceptance_tasks": [
      "Projection integrity: compile a pinned semantic fixture with learner/navigation projections; delete all learner/navigation records and assert semantic graph bytes, digests, node IDs, and relation IDs are identical. NOT RUN.",
      "Cross-view selection: for every semantic node/relation, select it from graph, outline, and table; assert the same full stable ID, inspector source selector, and claim ceiling appear in all views. NOT RUN.",
      "Section coverage: machine-check that all 16 DESIGN sections and 14 ONTOLOGY sections have at least one linked overview/focus/inspector/scenario/boundary treatment and no dangling selector. NOT RUN.",
      "Novice protocol: preregister locate/trace/retell/distinguish/boundary/vocabulary tasks for the two novice questions; use a pinned visual stimulus and compare answer accuracy, time, and stalls against document-only. No human study is authorized or run.",
      "Expert protocol: ask experts to trace a gate/repeat/recovery path, identify each owner and forbidden inference, and locate evidence-stage limits; score against exact source selectors. No human study is authorized or run.",
      "Scenario fidelity: compare every playback transition against DESIGN.md:320-327 and the §9 illustrative composite; assert no step creates a runtime event, authority decision, or unmentioned causal edge. NOT RUN.",
      "Keyboard/accessibility: test complete lens, outline, table, inspector, scenario, and source-link operation with keyboard only; test focus order, focus visibility, screen-reader names, reduced motion, 200–400% zoom/reflow, contrast, and no-JavaScript text/table access. NOT RUN.",
      "Claim-ceiling test: inject strings such as implemented, verified runtime, approved, or understood into a candidate projection and assert the build/validation rejects them unless source-bound evidence permits them. NOT RUN."
    ],
    "accessibility_risks": [
      "A graph-only canvas is not an equivalent information structure for screen-reader, magnification, cognitive, or keyboard users; provide source-linked outline and relation table as co-primary views.",
      "Linked selection can create disorienting focus moves or announce excessive changes. Keep focus and selection distinct, preserve meaningful DOM order, and announce only deliberate inspector updates.",
      "Custom graph/tree widgets impose substantial keyboard obligations; prefer native disclosure/links where possible, or implement the relevant ARIA pattern fully rather than applying roles cosmetically.",
      "Color, arrow direction, and motion cannot be the only carriers of event class, ownership, or proposal status; use text labels, patterns, and sufficient contrast.",
      "Autoplay or fast flow animation can obscure discrete causal steps and violates reduced-motion expectations; provide stepper controls, pause/stop, and static transcript.",
      "Dense ontology tables can fail reflow and reading order at zoom; preserve headings, linearizable rows, sticky labels only when non-obscuring, and downloadable/plain text equivalents.",
      "Claim-ceiling notices must be programmatically associated with the related scenario/finding, not be a distant visual disclaimer."
    ],
    "blockers": [
      "No machine-readable semantic graph, immutable snapshot schema, stable-ID policy, or projection compiler exists yet; a view cannot truthfully claim synchronization until those are owned and built.",
      "The RWO design and ontology are proposal-only; there is no implementation, runtime trace, replay, browser artifact, or conformance evidence.",
      "No human-comprehension or accessibility evaluation has been authorized or executed; the architectures are evidence-informed hypotheses, not demonstrated outcomes.",
      "Exact ownership of any future projection schema, learner-task protocol, and accessibility acceptance is not established by these candidate documents."
    ]
  },
  "validation": {
    "status": "pass",
    "checks": [
      "Read-only constraint respected; no files changed.",
      "All 16 DESIGN sections and all 14 ONTOLOGY sections mapped.",
      "Recommendation preserves one immutable semantic source, removable learner/navigation projections, stable cross-view selection, inspector, scenario, text/table equivalent, keyboard path, and visible claim ceilings.",
      "No claim of human comprehension, runtime implementation, or learner-edge semantic authority."
    ]
  }
}

