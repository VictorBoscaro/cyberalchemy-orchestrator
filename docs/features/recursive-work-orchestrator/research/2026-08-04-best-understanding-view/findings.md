# Findings — the Typed Coordinated Work Atlas

## Recommendation and claim ceiling

**Recommend one primary explanatory architecture: a typed coordinated Work Atlas.** Its landing view is **Structure**. **Flow** and **Ownership/Proof** are synchronized lenses over the same selected source or occurrence identity, and one shared **Inspector** exposes source, kind, owner, evidence stage, forbidden inference, and claim ceiling. A source outline and relation table are co-equal access paths into that same Inspector, not another semantic truth.

> **RESEARCH RECOMMENDATION ONLY.** No view, projection compiler, semantic graph, browser artifact, runtime, replay, accessibility evaluation, assistive-technology result, or human-comprehension study has been implemented or run. Nothing here is publication, promotion, authority, release, deployment, production, or effect evidence.

The recommendation is bound to the frozen proposal sources: [`DESIGN.md`](../../DESIGN.md) at SHA-256 `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`, and the candidate, non-promoting [`ONTOLOGY.md`](../../ontology/ONTOLOGY.md) at SHA-256 `1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`.

## Compact wireframe and one-image overview

```text
┌ PROPOSAL ONLY · NO IMPLEMENTATION / RUNTIME / ACCESSIBILITY / HUMAN PROOF ┐
│ WHAT IS WORK? uniform typed executable boundary; pipeline is also Work    │
│ One root OrchestratorKernel expands all composite definitions             │
├────────────────────────────────────────────────────────────────────────────┤
│ [Structure — landing] [Flow] [Ownership/Proof] [Source outline/table]     │
│                                                                            │
│ semantic outline │ selected definition graph / run plan │ shared Inspector│
│ KIND + OWNER text │ stable source/occurrence identity    │ source · stage │
│                                                                            │
├ user-paced illustrative paper trace ─── immutable text transcript ────────┤
│ PERSISTENT LEGEND: ENTITY · RELATION · LANE · STATE · CEILING · FORBIDDEN │
├────────────────────────────────────────────────────────────────────────────┤
│ invariants · source conflicts · unsupported evidence · all open residue    │
└────────────────────────────────────────────────────────────────────────────┘
```

This is the one-image overview contract: one root authority is visible above one reusable typed-Work topology; the three lenses and Inspector surround the same stable selection; the paper trace is visibly illustrative; and the legend plus proposal ceiling never disappear. The Structure view uses **C4-inspired decomposition/zoom discipline**—explicit types, labels, relationships, legends, and bounded zoom—not C4 semantics or an imported claim of interactive behavior ([C4 notation](https://c4model.com/diagrams/notation); [`DESIGN.md` lines 87–220](../../DESIGN.md#4-the-uniform-work-contract); [`ONTOLOGY.md` lines 63–180](../../ontology/ONTOLOGY.md#3-element-type-catalog)).

## Persistent Work card

```text
WHAT IS WORK?

Work is the uniform typed executable boundary.

Its immutable, versioned WorkDefinition declares input/output schemas,
command/event contracts, authority requirements, limits, and exactly one body:
  LEAF      -> executor binding
  COMPOSITE -> WorkGraph

WorkRun is one invocation of one WorkDefinition. Attempts belong to a WorkRun;
they do not change its definition, graph, or authority basis.

Every composition operator returns the same outer Work contract. A pipeline is
therefore also Work and can be nested where a leaf can be used. It does not
become an orchestrator: exactly one root OrchestratorKernel expands and schedules it.

Same outer contract; different body. Structural recursion; shallow authority.
```

The card remains reachable from every lens. Semantic entities stay explicitly typed as `WorkDefinition`, `WorkRun`, or `Attempt`; “Work” is the explanatory contract name, not an ambiguous generic node ([`DESIGN.md` lines 87–220 and 304–318](../../DESIGN.md#4-the-uniform-work-contract); [`ONTOLOGY.md` lines 42–90 and 172–180](../../ontology/ONTOLOGY.md#2-ontology-thesis); [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1), definition/instance notation precedent only).

## Why this architecture wins

| Candidate | What it preserves | Why it is not the primary view | Disposition |
|---|---|---|---|
| **Typed coordinated Work Atlas** | Structure, causality, ownership, evidence, residue, exact source selectors, and static/non-visual access without merging them | Requires future stable-ID and projection machinery, but its contract keeps that absence visible | **KEEP — primary** |
| Formal UML suite | Definition/instance and interaction distinctions | Several diagram families and imported notation create high learner cost and conformance risk | **DEFER as future export**, not current evidence |
| BPMN-like scenario-first view | Branch, join, gate, repetition, and finite walkthrough | Scenario primacy hides ontology, ownership, and residue and can look like observed behavior | **MERGE into Flow**; BPMN is a visualization precedent only ([OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2)) |
| Annotated document first | Source completeness and linear text | Makes the learner assemble cross-section structure, causality, and ownership unaided | **MERGE as outline/table/Inspector path** |
| Universal graph | Nominal inclusion of everything | Collapses definition, occurrence, ownership, evidence, and layout; overload becomes accidental meaning | **KILL as primary** |

The Atlas wins because it answers three different questions without pretending they are one: **what is composed**, **what causally occurs**, and **who owns or may establish each state**. Linked selection supplies cross-view continuity ([North and Shneiderman, coordinated multiple views](https://www.cs.umd.edu/users/ben/papers/North2000Snapa.pdf)); overview, focus, and details-on-demand supply orientation ([Shneiderman, “The Eyes Have It”](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)). Those sources inform the proposed interaction grammar only; their results are not evidence that this Atlas is implemented, accessible, or understood.

## Exact visual grammar and persistent minimal legend

The legend is always visible in every lens and in every static export. Shape, position, lane, color, fill, arrow style, and motion may reinforce meaning but never replace textual labels.

| Class | Required textual vocabulary |
|---|---|
| Entities | `KIND: WorkDefinition`, `KIND: WorkRun`, `KIND: Attempt`, named owner/boundary, derived projection, evidence finding, residue. `Work Atlas` is an interface title, never a semantic-node type. |
| Relations | `RELATION: STRUCTURAL TRIGGER`, `TEMPORAL CAUSATION`, `TRANSPORT/DELIVERY`, `JOURNAL ACCEPTANCE`, `PROJECTION DERIVATION`, `OWNED BY`, `REQUIRES AUTHORITY`. |
| Lanes | `OWNER: ROOT/CURSOR`, `COMMAND PROTOCOL`, `WORK/ADAPTER`, `EVENT PROTOCOL`, `JOURNAL`, plus scenario-specific `GATE`, `EXTERNAL EFFECT`, and `SIDECAR`. |
| Separate states | `JOURNAL ACCEPTANCE DISPOSITION`, work-owned `DOMAIN STATUS`, work/gate-owned `CONFIRMATION`, root-owned `CURSOR STATE`, `ADAPTER ADMISSION`, `ATTEMPT FRESHNESS`, and `FINDING STATUS`. |
| Journal disposition | `journal-accepted/new event record`; `journal-accepted/duplicate event record—no new cursor transition`; `quarantined/divergent`; `rejected/not recorded`. This is persistence disposition, never confirmation. |
| Effect boundary | `AUTHORITY REFERENCE: present/absent/unsupported`; `ADAPTER ADMISSION: admitted/rejected/not observed`; `EXTERNAL EFFECT OCCURRENCE: observed/not observed/unsupported`. No field implies another. |
| Claim ceiling | Persistent `PROPOSAL ONLY`, source layer, evidence stage, and `cannot establish` text. |
| Forbidden inference | Same outer contract ≠ same body; containment ≠ orchestrator or inherited authority; command ≠ journal-accepted event record; journal acceptance ≠ confirmation; terminal ≠ success/approval/effect permission; protocol/journal ≠ decision/execution; authority-reference presence ≠ adapter admission ≠ effect occurrence; projection ≠ domain state or authority. |

The text-first requirement is a design contract informed by [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and the [ARIA tree-view pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/); it is not accessibility-conformance evidence ([`DESIGN.md` lines 19–32 and 70–302](../../DESIGN.md#status-and-claim-ceiling); [`ONTOLOGY.md` lines 63–187 and 220–253](../../ontology/ONTOLOGY.md#3-element-type-catalog)).

## Synchronized-view contract

1. **Source precedence:** `DESIGN.md` is the primary proposal source. `ONTOLOGY.md` is its candidate, non-promoting structured mapping. Learner, navigation, layout, focus, highlight, and scenario records are removable projections. A conflict is shown with both selectors and preserved as open residue; the view does not silently choose or repair it.
2. **One identity:** every graph node, outline row, table row, occurrence card, and Inspector selection carries the same full source or occurrence identity. View-local duplicate identities are forbidden.
3. **Structure responsibility:** show the one-root overview, reusable `WorkDefinition` topology, selected composite body, and a separately labelled flattened run-plan projection. Recursion appears as shared type contract, definition nesting, and root-owned graph expansion—never nested authority.
4. **Flow responsibility:** show immutable text-labelled `COMMAND` and `EVENT` occurrence cards, explicit causal links, and declared release edges. Causation, transport, per-run sequence, journal acceptance, wall time, and cursor fold remain separate. OpenTelemetry is a visualization precedent only; it does not define RWO causation or prove delivery, replay, or runtime behavior ([OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/), [messaging spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/), [Lamport’s ordering paper](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/)).
5. **Ownership/Proof responsibility:** show named owners and separate rows for domain status, confirmation, journal acceptance, routing cursor, authority-reference presence, adapter admission, effect occurrence, evidence stage, profile, finding, and residue.
6. **Inspector responsibility:** show exact semantic or occurrence ID, `KIND`, `OWNER`, source layer, exact selector and digest, properties, relations, shields, journal disposition, reducer/freshness where relevant, evidence stage, claim ceiling, and `cannot establish` warning.
7. **Removal test:** deleting every projection record must leave design and ontology bytes, digests, semantic IDs, relation IDs, selectors, and source-conflict records unchanged. No projection writes back, resolves a conflict, creates authority, manufactures state/confirmation, or claims freshness without lineage.

No stable-ID policy, machine semantic graph, projection compiler, synchronized interface, or removal test presently exists. This is the proposed contract only ([`DESIGN.md` lines 19–32 and 430–460](../../DESIGN.md#status-and-claim-ceiling); [`ONTOLOGY.md` lines 21–40 and 255–327](../../ontology/ONTOLOGY.md#1-ontology-identity-and-boundary)).

## Named-element atlas

| Element | Visible treatment and non-collapse rule | Exact local selector |
|---|---|---|
| `WorkDefinition`, `WorkRun`, `Attempt` | Separate text-labelled definition card, run card, and attempt rows; never place runtime state on a definition | [`DESIGN.md` 87–128](../../DESIGN.md#4-the-uniform-work-contract); [`ONTOLOGY.md` 63–76](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Leaf/composite substitutability | Same outer frame plus `BODY: LEAF` or `BODY: COMPOSITE`; same contract, different body | [`DESIGN.md` 130–146](../../DESIGN.md#43-leaf-work); [`ONTOLOGY.md` 65–72, 144–149](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Sequence, fan-out, fan-in | Text-labelled edges with selector and input mapping; fan-in names release policy and canonical manifest | [`DESIGN.md` 148–188](../../DESIGN.md#5-the-composition-algebra); [`ONTOLOGY.md` 77–89, 145–159](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Gate | Decision-work entity plus `RELATION: ROUTE LABEL MATCH`; zero or multiple matches block; confirmation stays work-owned | [`DESIGN.md` 189–197](../../DESIGN.md#54-gate); [`ONTOLOGY.md` 85–86, 174–184](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Sidecar | `KIND: SIDECAR WORK`, owner, lifecycle policy, detached lane; no control without an explicit edge | [`DESIGN.md` 198–209](../../DESIGN.md#55-sidecar); [`ONTOLOGY.md` 87–88, 157–158, 180–181](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Bounded repetition | Back-edge names decision work, round/max, exhaustion edge, and no-next-attempt result | [`DESIGN.md` 210–215, 376–377](../../DESIGN.md#56-bounded-repetition); [`ONTOLOGY.md` 89–90, 125–126, 201–205](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Explicit composition | Operator and primitive graph are separately inspectable; compilation does not imply execution | [`DESIGN.md` 216–220](../../DESIGN.md#57-escape-hatch-explicit-graph-composition); [`ONTOLOGY.md` 90, 153–156, 225–228](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Root, protocol, journal, adapter | Distinct `KIND` and `OWNER`: one root schedules; protocol transports; journal records; adapter executes/translates | [`DESIGN.md` 54–68, 222–302](../../DESIGN.md#2-thesis); [`ONTOLOGY.md` 91–104, 160–187](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Command and event | Every occurrence says `KIND: COMMAND` or `KIND: EVENT`; lanes and styles are redundant cues only | [`DESIGN.md` 222–285](../../DESIGN.md#6-work-protocol-commands-events-and-the-bus); [`ONTOLOGY.md` 91–96, 119–126](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Journal acceptance | Labelled disposition attached to the event record, distinct from confirmation | [`DESIGN.md` 227–232, 259–271, 304–322, 385–390](../../DESIGN.md#6-work-protocol-commands-events-and-the-bus); [`ONTOLOGY.md` 96–100, 123–126, 164–166, 182–185](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Cursor, domain status, confirmation | Three separately owned cards; journal acceptance never creates confirmation | [`DESIGN.md` 287–302](../../DESIGN.md#7-state-and-ownership); [`ONTOLOGY.md` 99–108, 127–130, 166–187](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| External effects | Three separate text fields: authority-reference presence, adapter admission, effect occurrence | [`DESIGN.md` 104–113, 368–381](../../DESIGN.md#41-workdefinition); [`ONTOLOGY.md` 101–104, 167–185, 204–205](../../ontology/ONTOLOGY.md#3-element-type-catalog) |
| Invariants, failures, residue | `RWO-I01–I12`, evidence stage, failure posture, abnormal identity, and every unresolved record | [`DESIGN.md` 368–460](../../DESIGN.md#10-validation-invariants); [`ONTOLOGY.md` 189–218, 235–327](../../ontology/ONTOLOGY.md#7-architecture-profiles) |

## Complete section coverage

### All 16 design sections

| Design section | Atlas treatment |
|---|---|
| [§1 Purpose](../../DESIGN.md#1-purpose) | Overview promise and scope; operator palette; kernel does/does-not-own card; no-domain-judgment boundary. |
| [§2 Thesis](../../DESIGN.md#2-thesis) | Work/event-response thesis, four kernel responsibilities, and one-root expansion. |
| [§3 Non-goals](../../DESIGN.md#3-non-goals) | Out-of-scope ring and owner matrix; authority and UI projection remain outside the kernel. |
| [§4 Uniform Work contract](../../DESIGN.md#4-the-uniform-work-contract) | Persistent Work card, definition/run/attempt anatomy, leaf/composite body distinction. |
| [§5 Composition algebra](../../DESIGN.md#5-the-composition-algebra) | Composition catalog, typed event-triggered graph, operator desugaring, bounded cycles. |
| [§6 Protocol/bus](../../DESIGN.md#6-work-protocol-commands-events-and-the-bus) | Separate command/event rails, envelope, delivery, and journal dispositions; bus neither decides nor executes. |
| [§7 State and ownership](../../DESIGN.md#7-state-and-ownership) | Domain/journal/cursor ownership ledger, reducer lineage, and freshness. |
| [§8 Runtime flow](../../DESIGN.md#8-runtime-flow) | Illustrative accepted-event paper stepper, with `proposed—not observed` on every step. |
| [§9 Minimal API example](../../DESIGN.md#9-minimal-api-example) | Composite thumbnail and finite scenario selector; illustrative syntax only. |
| [§10 Validation invariants](../../DESIGN.md#10-validation-invariants) | `RWO-I01–I12` matrix with evidence stage and failure posture; no runtime pass implied. |
| [§11 Failure/recovery](../../DESIGN.md#11-failure-and-recovery-semantics) | Duplicate, divergent, delayed, stale-attempt, restart, cancellation, compensation, and sidecar overlays. |
| [§12 Existing architecture](../../DESIGN.md#12-relationship-to-existing-architecture) | Provenance neighborhood and source relationship; no supporting discovery promotion. |
| [§13 Honest “any pipeline” claim](../../DESIGN.md#13-what-any-pipeline-can-honestly-mean) | Bounded claim and excluded counterexamples; no universal expressiveness claim. |
| [§14 Ontology handoff](../../DESIGN.md#14-ontology-handoff) | Design-to-ontology bridge, required types/relations, and no-redefinition/no-promotion notice. |
| [§15 Open questions](../../DESIGN.md#15-open-questions) | Open-residue ledger; every unresolved question stays unresolved. |
| [§16 Connections](../../DESIGN.md#16-connections) | Typed, source-bound candidate links with provenance in the Inspector. |

### All 14 ontology sections

| Ontology section | Atlas treatment |
|---|---|
| [§1 Identity/boundary](../../ontology/ONTOLOGY.md#1-ontology-identity-and-boundary) | Source-precedence and claim-ceiling card; `authority_effect: none`. |
| [§2 Thesis](../../ontology/ONTOLOGY.md#2-ontology-thesis) | One-root semantic anatomy and shallow-authority closure rule. |
| [§3 Element types](../../ontology/ONTOLOGY.md#3-element-type-catalog) | Filtered outline/graph with explicit local type labels and stable selection. |
| [§4 Typed properties](../../ontology/ONTOLOGY.md#4-typed-property-catalog) | Subject/property/inference table with required evidence stage. |
| [§5 Allowed relations](../../ontology/ONTOLOGY.md#5-allowed-relation-catalog) | Directed relation table with cardinality, cycle policy, evidence, and non-transitivity. |
| [§6 Forbidden relations/shields](../../ontology/ONTOLOGY.md#6-forbidden-relations-and-inference-shields) | Negative-control ledger with selected prohibited inference. |
| [§7 Architecture profiles](../../ontology/ONTOLOGY.md#7-architecture-profiles) | Definition/runtime evidence comparison and invariant table; runtime profile remains unwitnessed. |
| [§8 Observation projections](../../ontology/ONTOLOGY.md#8-observation-projections) | `may observe` / `cannot establish alone` matrix; observation never authority. |
| [§9 Finding shape](../../ontology/ONTOLOGY.md#9-explainable-finding-shape) | Evidence-chain Inspector; missing evidence is unsupported or indeterminate, never pass. |
| [§10 Evidence/confidence](../../ontology/ONTOLOGY.md#10-evidence-and-confidence-ledger) | Evidence versus commitment display; no confidence promotion. |
| [§11 Source ledger](../../ontology/ONTOLOGY.md#11-source-ledger) | Precedence-aware provenance; supporting sources cannot promote the ontology. |
| [§12 Residue](../../ontology/ONTOLOGY.md#12-residue) | All fourteen unresolved records with open status and impact. |
| [§13 Validation](../../ontology/ONTOLOGY.md#13-validation-status) | `pass` / `unsupported` / `not granted` matrix; document mapping is not runtime conformance. |
| [§14 Connections](../../ontology/ONTOLOGY.md#14-connections) | Typed, non-promoting links and exact target selector. |

## Three finite illustrative paper traces

Every row below is one occurrence and explicitly provides `KIND`, `PRODUCER`, `CONSUMER`, `CAUSE`, and `OWNER`, plus journal/cursor and effect-boundary fields. These are paper walkthroughs of proposed semantics, not replay or runtime observations. BPMN and OpenTelemetry are visualization precedents only.

### A. Sequence with a gate

| Step | `KIND` | `PRODUCER` | `CONSUMER` | `CAUSE` | `OWNER` | Journal disposition / cursor | Effect boundary |
|---|---|---|---|---|---|---|---|
| M01 | `COMMAND: invoke A` | Root kernel | A run/adapter | Scenario invocation input | Root owns command issuance/cursor; A owns its domain status | No event record; proposed delivery only | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| M02 | `EVENT: A.release` | A run/adapter | Work protocol → journal/root reducer | M01 | A owns event/domain meaning; journal owns persistence disposition | `journal-accepted/new event record`; cursor satisfies A→G | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| M03 | `COMMAND: invoke G` | Root kernel | Gate work G | M02 | Root owns issuance/cursor; G owns decision and confirmation | No gate result event record; proposed delivery only | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| M04 | `COMMAND: confirmation-provided` | Confirmation adapter | Gate work G | Illustrative external confirmation input correlated with M03 | Confirmation adapter owns delivery evidence; G owns confirmation meaning/state | No gate event record; cursor unchanged | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; command receipt is not confirmation |
| M05 | `EVENT: route.approved` | Gate work G | Work protocol → journal/root reducer | M04 | G owns decision/confirmation; journal owns persistence disposition | `journal-accepted/new event record`; exactly one route becomes eligible | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| M06 | `COMMAND: invoke B` | Root kernel | B run/adapter | M05 | Root owns issuance/cursor; B owns its domain status | No B result event record; proposed delivery only | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; route label implies none of these outcomes |

### B. Fan-out followed by fan-in

| Step | `KIND` | `PRODUCER` | `CONSUMER` | `CAUSE` | `OWNER` | Journal disposition / cursor | Effect boundary |
|---|---|---|---|---|---|---|---|
| F01 | `EVENT: source.release` | Source work A | Work protocol → journal/root reducer | Scenario seed command outside this bounded trace | A owns event/domain meaning; journal owns persistence disposition | `journal-accepted/new event record`; two declared edges become eligible | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| F02 | `COMMAND: invoke B1` | Root kernel | Branch B1 run/adapter | F01 | Root owns issuance/cursor; B1 owns its domain status | Separate proposed delivery; no B1 event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| F03 | `COMMAND: invoke B2` | Root kernel | Branch B2 run/adapter | F01 | Root owns issuance/cursor; B2 owns its domain status | Separate proposed delivery; no B2 event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| F04 | `EVENT: B2.release` | Branch B2 | Work protocol → journal/root reducer | F03 | B2 owns event/domain meaning; journal owns persistence disposition | `journal-accepted/new event record`; fan-in `all` remains false | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| F05 | `EVENT: B1.release` | Branch B1 | Work protocol → journal/root reducer | F02 | B1 owns event/domain meaning; journal owns persistence disposition | `journal-accepted/new event record`; fan-in `all` becomes true | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; F04 does not cause F05 |
| F06 | `COMMAND: invoke J` | Root kernel | Join work J | F04 and F05 as explicit causes | Root owns issuance/cursor; J owns reconciliation/domain meaning | Canonical input manifest; fan-in fires once; no J event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |

### C. Primary, non-controlling sidecar, one retry, and exhaustion

| Step | `KIND` | `PRODUCER` | `CONSUMER` | `CAUSE` | `OWNER` | Journal disposition / cursor | Effect boundary |
|---|---|---|---|---|---|---|---|
| S01 | `COMMAND: invoke P/A1` | Root kernel | Primary P attempt A1/adapter | Scenario invocation input | Root owns issuance/cursor; P owns primary domain status | Proposed delivery; no P event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| S02 | `COMMAND: invoke sidecar S` | Root kernel | Sidecar S run/adapter | Same declared `start: with-primary` trigger as S01; S01 is not its cause | Root owns issuance/cursor; S owns sidecar domain status and has no primary authority | Separate proposed delivery; no S event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| S03 | `EVENT: diagnostic observation` | Sidecar S | Work protocol → journal/root reducer | S02 | S owns diagnostic meaning; journal owns persistence disposition | `journal-accepted/new event record`; no release by default | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; S cannot advance or stop P |
| S04 | `EVENT: P/A1 terminal failure` | Primary P attempt A1 | Work protocol → journal/root reducer | S01 | P owns failure meaning; journal owns persistence disposition | `journal-accepted/new event record`; retry decision work D becomes eligible | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; the event record does not itself retry |
| S05 | `COMMAND: invoke D` | Root kernel | Retry decision work D | S04 | Root owns issuance/cursor; D owns retry decision/confirmation | Proposed delivery; no D result event record | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| S06 | `EVENT: route.retry` | Retry decision work D | Work protocol → journal/root reducer | S05 | D owns retry decision/confirmation; journal owns persistence disposition | `journal-accepted/new event record`; cursor sets round 2 and enables A2 | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; journal acceptance is not D’s confirmation |
| S07 | `COMMAND: invoke P/A2` | Root kernel | Primary P attempt A2/adapter | S06 | Root owns issuance/cursor; P owns domain status across its new attempt | Proposed delivery; A1 remains history; A2 has a new attempt ID | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| S08 | `EVENT: P/A2 release` | Primary P attempt A2 | Work protocol → journal/root reducer | S07 | P owns outcome meaning; journal owns persistence disposition | `journal-accepted/new event record`; primary successor becomes eligible | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |
| S09 | `EVENT: sidecar terminal` | Sidecar S | Work protocol → journal/root reducer | S02 and the declared sidecar finish policy; S08 does not grant control | S owns sidecar outcome; journal owns persistence disposition | Separate `journal-accepted/new event record`; finish policy applies | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; S still cannot control the primary successor |
| **C-X1 exhaustion** | `EVENT: P/A2 terminal failure` (counterfactual replacing S08) | Primary P attempt A2 | Work protocol → journal/root reducer | S07 | P owns failure meaning; journal owns persistence disposition | `journal-accepted/new event record`; cursor observes `round=2=maxRounds` | No effect inferred: `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported`; another retry is ineligible |
| **C-X2 exhaustion** | `COMMAND: invoke exhaustion target` through the named `RELATION: EXHAUSTION EDGE` | Root kernel | Declared exhaustion target | C-X1 plus the declared max-round condition and exhaustion edge | Root owns issuance/cursor; exhaustion target owns any subsequent domain meaning | Cursor records exhaustion route; no target result event record; **no A3 may be created** | `AUTHORITY REFERENCE: unsupported`; `ADAPTER ADMISSION: not observed`; `EXTERNAL EFFECT OCCURRENCE: unsupported` |

Identical duplicates receive `journal-accepted/duplicate event record—no new cursor transition`; divergent same-key bytes are `quarantined/divergent`; delayed records retain occurrence and journal times; stale-attempt records remain visible but cannot release current edges ([`DESIGN.md` lines 148–215, 222–399](../../DESIGN.md#5-the-composition-algebra); [`ONTOLOGY.md` lines 77–100, 119–205](../../ontology/ONTOLOGY.md#3-element-type-catalog); [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2); [OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/)).

## Candidate protocol and failure/recovery ledger

This ledger makes the frozen proposal’s protocol and recovery semantics inspectable without claiming that any transport, journal, reducer, adapter, or recovery path exists.

| Topic | Candidate meaning the Atlas must display | Non-collapse and proof ceiling |
|---|---|---|
| At-least-once delivery | A command or event may be delivered more than once under the same stable key. | Delivery multiplicity is proposed; no runtime delivery result exists. |
| Idempotency | Commands and event acceptance require stable idempotency keys; identical repeats must converge. | A key does not prove the adapter’s external effect is idempotent. |
| Ordering scope | Events are ordered only within one `work_run_id`; no global ordering is claimed. | Arrival time, wall time, journal position, and causality remain distinct. |
| Append-only journal acceptance | Accepted event history is append-only and each record carries an explicit acceptance disposition. | A journal-accepted event record is persistence evidence, not confirmation, authorization, execution, or domain-state ownership. |
| Outbox/inbox reconciliation | The candidate boundary uses outbox/inbox or an equivalent atomic delivery boundary; pending commands are reconciled after restart. | This is a proposed delivery boundary, not an implemented transaction or exactly-once guarantee. |
| Replayable reducers | Versioned reducers fold accepted history into the rebuildable routing cursor; the same ordered history plus reducer version is expected to rebuild the same cursor. | Replay derives cursor state only; it does not recreate unobserved domain facts or prove runtime determinism. |
| No exactly-once external-effect claim | The design explicitly does not claim exactly-once business effects. | Authority-reference presence, adapter admission, and external-effect occurrence remain distinct, separately evidenced fields. |
| Lost delivery | Redelivery uses the same idempotency key. | Recovery is not proof that the original or repeated delivery produced an effect. |
| Identical duplicate | An identical repeat converges and is shown as `journal-accepted/duplicate event record—no new cursor transition`. | Duplicate persistence disposition is not a second confirmation or release. |
| Divergent duplicate | The same key with different bytes is `quarantined/divergent`. | The view retains both identity and conflict; it does not choose a winner or advance the cursor. |
| Root restart | Rebuild the cursor from accepted journal history, then reconcile pending commands through the outbox/inbox boundary. | Restart recovery is candidate semantics; no restart or replay test has run. |
| Stale attempt | Retain the occurrence and attempt identity, but do not let it release current edges. | Historical visibility does not make the stale attempt current. |
| Cancellation | Cancellation is an addressed request; each work owns how it reaches and reports terminal state, and propagation needs explicit edges. | A cancellation command is not cancellation completion or implicit parent/child propagation. |
| Compensation | Compensation is another declared Work graph. | It is not an implicit rollback or restoration promise. |
| Sidecar failure | Follow the declared sidecar lifecycle policy. | No universal fatality rule exists, and sidecar failure does not control the primary without an explicit edge. |

Exact bindings: [`DESIGN.md` §6](../../DESIGN.md#6-work-protocol-commands-events-and-the-bus) and [§11](../../DESIGN.md#11-failure-and-recovery-semantics); [`ONTOLOGY.md` typed properties, lines 119–130](../../ontology/ONTOLOGY.md#4-typed-property-catalog), [message and projection relations, lines 160–170](../../ontology/ONTOLOGY.md#5-allowed-relation-catalog), [inference shields, lines 172–187](../../ontology/ONTOLOGY.md#6-forbidden-relations-and-inference-shields), and [evidence profiles, lines 189–218](../../ontology/ONTOLOGY.md#7-architecture-profiles).

## Learner journeys

**Novice: “What is this system, and who owns what?”**

1. Read the proposal ceiling and persistent Work card.
2. Distinguish `WorkDefinition`, `WorkRun`, `Attempt`, leaf/composite body, and one-root kernel.
3. Use Ownership/Proof to compare work-owned domain state and confirmation, journal acceptance, and the root-owned cursor.
4. Step through M01–M06 with the persistent legend.
5. Step through S01–S09 and C-X1/C-X2; deny sidecar control and deny A3.
6. Finish at unsupported evidence, source conflicts, and all open residue.

**Expert: “How does this concrete composite route and recover?”**

1. Filter definitions, runs, graphs, edges, messages, journal, cursor, adapters, and authority references.
2. Inspect one edge’s selector, mapping, source precedence, cycle policy, and shields.
3. Compare causation, delivery, journal acceptance, and cursor fold in Flow.
4. Inspect authority-reference presence, adapter admission, and effect occurrence independently.
5. Cross-check profiles and invariants, then inspect every source conflict and residue before treating a conclusion as settled.

These are proposed journeys and finite acceptance tasks. No person has attempted them.

## Stable selection, Inspector, and equivalent access

- **Stable selection:** graph, outline, relation table, occurrence transcript, and ownership ledger select the same full identity. Focus and selection remain distinct. Changing a lens does not invent, shorten, or remap identity.
- **Inspector:** one card renders the exact source selector and digest, source precedence, `KIND`, `RELATION`, `OWNER`, properties, evidence stage, finding status, shields, freshness/reducer when applicable, claim ceiling, and forbidden inference.
- **Static equivalent:** every overview and scenario has a linear text export containing the persistent ceiling, Work card, legend, ownership rows, trace steps, source selectors, and residue.
- **Table equivalent:** every structural or temporal edge appears as a row with source, target, relation kind, selector/causes, input mapping or disposition, owner, evidence stage, and cannot-establish field.
- **Keyboard path:** the proposed focus order is ceiling → Work card → lens/outline → selected record → Inspector → scenario controls/transcript → invariants/residue → source links. If a tree widget is built, it must implement the ARIA pattern fully; native disclosures and links are preferred where sufficient.
- **Reduced-motion equivalent:** scenario progression is user-paced, stepwise, and transcript-backed. No autoplay causality or moving structural topology. Motion may be removed without losing ordering, selection, state, or ownership.
These are future artifact requirements, not proof of accessibility ([WCAG 2.2](https://www.w3.org/TR/WCAG22/); [ARIA tree-view pattern](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/); [`DESIGN.md` lines 430–460](../../DESIGN.md#14-ontology-handoff); [`ONTOLOGY.md` lines 220–253](../../ontology/ONTOLOGY.md#8-observation-projections)).

## Ownership, source authority, and claim ceilings

- The root kernel owns only validation/expansion/scheduling and the rebuildable routing cursor proposed by the design.
- Each work unit or adapter owns its domain status; a gate/work unit owns confirmation. The journal owns its persistence disposition. The protocol transports. The adapter executes or translates. None silently inherits another owner’s meaning.
- A journal-accepted event record is distinct from confirmation. It may record an event that reports confirmation, but persistence does not create the confirmation state.
- Authority-reference presence is distinct from adapter admission and external-effect occurrence. None entails either of the others.
- `DESIGN.md` is primary proposal meaning; `ONTOLOGY.md` is candidate mapping; projections explain or navigate only. Inventory was discovery only and grants no authority.
- Definition/source/graph evidence can support only its named stage. Runtime, browser, accessibility, and comprehension claims require their own later evidence.

## MVP contract and future work

**Smallest honest MVP contract:** pinned design and ontology fixtures with independent digests and precedence; persistent proposal ceiling, Work card, and text-first legend; Structure landing view plus outline and relation table; mandatory `KIND`, `RELATION`, and `OWNER`; shared stable selection and Inspector; the three immutable paper transcripts including exhaustion/no-A3; explicit journal dispositions; separate authority-reference/admission/effect fields; Ownership/Proof matrix; invariants, source conflicts, and all residue; keyboard, reduced-motion, static, and text/table access contracts; projection-removal byte-identity and complete-section-coverage tests.

**Future work, not current capability:** live journal replay, telemetry ingestion, runtime-derived state, formal notation exports, accessibility-conformance evaluation, and human-comprehension study. Each requires later implementation and independent evidence. This is the evidence-closure deferred row, not an MVP promise.

## Negative controls

These killed forms are retained only as tests that the recommendation must reject:

| Mutant | Required result |
|---|---|
| Remove Ownership/Proof or show ownerless status | **KILL:** ownership collapse. |
| Draw a kernel inside a composite or infer authority from containment | **KILL:** recursion/authority collapse. |
| Merge command and event rails or omit textual kinds | **KILL:** protocol-kind collapse. |
| Style journal disposition as confirmation or call it an “accepted decision” | **KILL:** persistence/confirmation collapse. |
| Merge authority-reference presence, adapter admission, and effect occurrence | **KILL:** effect-boundary collapse. |
| Autoplay causality, move structural nodes, or order by wall/arrival time | **KILL:** timeline spectacle. |
| Use the universal graph as landing view | **KILL:** graph overload. |
| Use universal green terminal/success or projection-authored status | **KILL:** status inflation. |
| Draw a cycle without decision owner, bound, exhaustion edge, and no-next-attempt result | **KILL:** finite-bound loss. |
| Let ontology override design or let a projection write back | **KILL:** source collapse. |

These are negative controls, not implemented tests ([Tversky, Morrison, and Betrancourt on animation](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf); [WCAG 2.2](https://www.w3.org/TR/WCAG22/); [`DESIGN.md` lines 19–32, 210–302, 368–399](../../DESIGN.md#status-and-claim-ceiling); [`ONTOLOGY.md` lines 172–187](../../ontology/ONTOLOGY.md#6-forbidden-relations-and-inference-shields)).

## Separate validation lanes

| Lane | Proposed checks | May establish if run and passed | Must not claim |
|---|---|---|---|
| Agent/structural | Frozen digests, source precedence, all 16+14 section bindings, stable-ID consistency, projection removability, finite trace conformance, legend completeness, negative-control rejection | Source/selector coverage and internal contract consistency | Runtime behavior or learner understanding |
| Browser | Rendering, direct links, synchronized selection, persistent legend/card, controls, transcript parity, reduced-motion and no-JavaScript behavior | Behavior of the built browser artifact | Accessibility conformance or comprehension |
| Accessibility | Keyboard, focus, names, contrast, zoom/reflow, motion, reading order, and assistive-technology evaluation | Results for the tested artifact/configuration | General comprehension or universal accessibility |
| Human comprehension | Preregistered novice/expert locate, trace, distinguish, retell, and boundary tasks | Results for the tested people, tasks, and stimulus | Runtime conformance, authority, or universal usability |

**None of these validation lanes has run.**

## Direct source trace

| Decision | Frozen local source | Direct external source and bounded use |
|---|---|---|
| Atlas with coordinated Structure, Flow, Ownership/Proof, Inspector | [`DESIGN.md` 19–460](../../DESIGN.md); [`ONTOLOGY.md` 21–337](../../ontology/ONTOLOGY.md) | [C4 notation](https://c4model.com/diagrams/notation), [overview/detail](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf), and [coordinated views](https://www.cs.umd.edu/users/ben/papers/North2000Snapa.pdf): explanatory precedents only |
| Work card and definition/run separation | [`DESIGN.md` 87–220, 304–318](../../DESIGN.md#4-the-uniform-work-contract); [`ONTOLOGY.md` 42–90, 172–180](../../ontology/ONTOLOGY.md#2-ontology-thesis) | [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1): definition/instance notation precedent only |
| C4-inspired discipline | [`DESIGN.md` 87–220](../../DESIGN.md#4-the-uniform-work-contract); [`ONTOLOGY.md` 63–180](../../ontology/ONTOLOGY.md#3-element-type-catalog) | [C4 notation](https://c4model.com/diagrams/notation): decomposition/zoom discipline only |
| Causal occurrence ledger | [`DESIGN.md` 222–330](../../DESIGN.md#6-work-protocol-commands-events-and-the-bus); [`ONTOLOGY.md` 119–170](../../ontology/ONTOLOGY.md#4-typed-property-catalog) | [OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/), [messaging spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/), [Lamport](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/): occurrence/ordering visualization precedents only |
| Legend and equivalent access contract | [`DESIGN.md` 19–32, 70–302, 430–460](../../DESIGN.md#status-and-claim-ceiling); [`ONTOLOGY.md` 63–187, 220–253](../../ontology/ONTOLOGY.md#3-element-type-catalog) | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [ARIA tree view](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/): future design requirements only |
| Three finite paper traces and exhaustion/no-A3 | [`DESIGN.md` 148–215, 222–399](../../DESIGN.md#5-the-composition-algebra); [`ONTOLOGY.md` 77–100, 119–205](../../ontology/ONTOLOGY.md#3-element-type-catalog) | [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2), [OpenTelemetry trace API](https://opentelemetry.io/docs/specs/otel/trace/api/): visualization precedents only; no BPMN conformance or replay proof |

## Open residue

All ten design questions `RWO-OQ-001` through `RWO-OQ-010` and ontology residues `rwo:residue.001` through `.014` remain open. In particular: journal versus work-owned state authority, dynamic graph extension, cross-host delivery, cancellation/compensation combinators, quorum meaning, schema/reducer migration, minimal authority reference, counterexample sufficiency, long-lived streams, promotion ownership, event-classification form, mapping purity, adapter ownership, and relation transitivity are not resolved by a view recommendation ([`DESIGN.md` §15](../../DESIGN.md#15-open-questions); [`ONTOLOGY.md` §12](../../ontology/ONTOLOGY.md#12-residue)).

The absence of implementation/runtime evidence remains `unsupported`, and ontology promotion remains `not granted`; neither is converted into a failure or a pass by this research artifact.

## Final reviewer verdict matrix

| Gate | Verdict | What the final review established within research scope | What it did not establish |
|---|---|---|---|
| Precedent and ownership | **PASS** | Local meaning stays owned by `DESIGN.md`; the ontology stays candidate/non-promoting; Inventory is discovery only; C4-inspired discipline and OpenTelemetry/BPMN visualization precedents are bounded | Novel owned implementation, runtime, browser, accessibility, or comprehension evidence |
| Non-vacuity | **PASS** | Persistent Work card answers what Work is and why a pipeline is Work without nested authority; the three traces distinguish routing/ownership; retry reaches `round=2=maxRounds`, fires exhaustion, and creates no A3; required mutants are rejectable | Human task performance or runtime execution |
| Definitional and authority non-collapse | **PASS** | Persistent legend; source precedence; textual `KIND`, `RELATION`, `OWNER`; journal-accepted event record distinct from confirmation; authority-reference presence distinct from adapter admission and effect occurrence | Authority, confirmation, admission, effect, conformance, or promotion itself |

## Research conclusion

The typed coordinated Work Atlas is the clearest evidence-backed recommendation because it gives the reader one stable place to orient and three deliberately separate ways to reason: Structure for recursive typed composition, Flow for finite causal occurrences, and Ownership/Proof for state, authority boundaries, evidence, and residue. The shared identity and Inspector keep those lenses synchronized without creating a second source of truth. Its MVP is a precise future artifact contract; its traces are finite paper examples; its negative controls expose semantic collapse; and its validation lanes keep structural, browser, accessibility, and human evidence separate.

That conclusion is the ceiling. The view has not been built, run, browser-tested, accessibility-tested, or human-validated.
