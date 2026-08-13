# Transfer skeptic: formal structures versus engineered systems

## Scope and evidence status

This adversarial comparison uses only the accepted [formal and structural owner map](../runs/formal-structural-owner-map/findings.md) and its [review](../runs/formal-structural-owner-map/review.md), plus the accepted [engineered-systems owner map](../runs/engineered-systems-owner-map/findings.md) and its [review](../runs/engineered-systems-owner-map/review.md). Both reviews dispose their source artifacts as `PASS / KEEP`. Acceptance establishes fidelity to each bounded collection contract; it does not establish that the two maps share a theory or that concepts may be transported between them.

Severity means risk to a cross-domain generalization:

- **BLOCKER:** the proposed generalization is not licensed without new evidence or an explicit model.
- **MAJOR:** a qualified transfer may be possible, but a material distinction must first be represented and tested.
- **MINOR:** wording or scope discipline can prevent the error.

## Adversarial findings

### T1 — “Interface” is a same-word trap

**Severity: BLOCKER**

The formal map uses several non-equivalent boundary notions: equality of domain/codomain objects, a shared cospan foot used in a pushout, typed operadic ports, imports/exports in an operational semantics, and assumptions/guarantees about environments. The engineered map uses callable-program specifications, OSGi requirement/capability namespaces, XProc ports, Blockly sockets, and controlled physical/logical/human interfaces. Calling all of these “interfaces” hides differences in both type and authority.

In the formal accounts, an interface can be part of the mathematical data that determines whether an operation is defined. In the engineered accounts, it may instead be a declared contract, resolver input, user-interaction guard, controlled document, or organizational responsibility. A NASA interface document does not play the same role as equality of categorical boundaries; a Blockly checker does not prove a pushout exists.

**Minimal legitimate transfer condition:** state a domain-specific boundary object or contract, identify who or what has authority to declare it, define a checkable compatibility relation, and show what operation compatibility licenses. The generic word “interface” alone transfers nothing.

### T2 — Composition, integration, configuration, resolution, dependency, and coordination are not interchangeable operations

**Severity: BLOCKER**

The formal map distinguishes typed arrow chaining, pushout gluing, operadic substitution, syntax construction with transition rules, a distributive compatibility law, and logical conjunction under an assume/guarantee rule. The engineered map distinguishes Parnas's correctness dependency, OSGi resolution into a wiring state, XProc dataflow connection, Blockly connection admission, and NASA's planned product integration process.

Several engineered cases are not “composition” in the same operational sense. `A uses B` classifies a correctness dependency; it does not itself build a composite object. OSGi resolution selects a valid configuration relative to an environment. NASA integration is a governed causal process involving validation, sequencing, people, environments, and verification. Blockly checks whether a local connection is allowed but does not establish whole-program semantics. Collapsing these into one operation would confuse relation, selection, assembly, execution, and proof.

**Minimal legitimate transfer condition:** name the operation actually performed and its output kind. A transfer is legitimate only if source and target agree on whether the operation constructs, connects, selects, executes, proves, or merely constrains a whole—or if an explicit mapping between those operation kinds is supplied and tested.

### T3 — Typing and admissibility have different sources of authority

**Severity: MAJOR**

Formal admissibility is fixed by definitions, signatures, categorical structure, rule formats, or proof hypotheses. Engineered admissibility may be fixed by standards, specifications, mutable resolver policy, configured checkers, design authority, lifecycle governance, or operational context. OSGi explicitly allows policy and multiple valid resolutions; Blockly permits custom checking; NASA relies on controlled interface artifacts and verification. These are revisable socio-technical authorities, not merely discovered mathematical constraints.

Therefore, “well-typed composition” cannot be transferred to engineered or epistemic work merely by labeling parts with types. The labels may encode a designer's current policy rather than an invariant, and different authorities may disagree.

**Minimal legitimate transfer condition:** record the authority and version that owns each admissibility rule, distinguish invariant constraints from policy choices, and expose how rule changes alter accepted compositions.

### T4 — Preservation claims do not transport across the maps

**Severity: BLOCKER**

The formal map's preservation results are theorem-local: associativity and identities, categorical or hypergraph structure, operadic substitution laws, proved transition properties, congruence with respect to a chosen behavioral equivalence, or refinement under explicit assumptions. The engineered map preserves or checks different things: stable module interfaces, class-space consistency, document-copy isolation, syntactic correctness, configuration control, and expected end-product function.

These are not instances of a demonstrated common preservation law. In particular, local connection validity does not imply semantic preservation; validated components do not imply a validated integrated whole; and an interface stable across software versions is not categorical identity or associativity.

**Minimal legitimate transfer condition:** name one observable or formal property, define it on parts and wholes, specify the assumptions under which the operation should preserve it, and provide either a proof or a controlled test. “Composition preserves meaning/correctness” remains blocked.

### T5 — Emergence is not the common result of composition

**Severity: BLOCKER**

Most accounts in both maps make no emergence claim. The formal accounts derive closure, coherence, behavior, or refinement under stated hypotheses. The engineered accounts explicitly avoid attributing emergence to Parnas, OSGi, XProc, and Blockly. NASA warns about adverse emergent behavior and requires verification; it does not promise beneficial novelty from integration.

Using “emergence” for any whole-level effect would erase causality: an effect might be constructed by definition, selected by a resolver, produced during execution, proven from rules, observed only after integration, or merely attributed by an evaluator.

**Minimal legitimate transfer condition:** specify a baseline prediction from isolated parts, the interaction mechanism, the whole-level observable, the measurement procedure, and a counterfactual or ablation that distinguishes interaction-produced effect from selection, aggregation, or observer redescription.

### T6 — Observability and evidence differ before and after execution

**Severity: MAJOR**

Formal validity may be established intensionally from types, axioms, rule formats, and proofs before any empirical run. Engineered composition distributes evidence across static checking, resolution, runtime execution, integration procedure, inspection, and end-product verification. XProc has both static and dynamic errors; OSGi resolution depends on environment state; NASA explicitly separates validated inputs from verification of the integrated result.

A single “composition succeeded” flag would therefore conflate admissibility, construction, execution, and achieved effect. It would also make failures incomparable: a type mismatch, unresolved dependency, stuck transition, circular proof, integration defect, and adverse observed behavior occur at different stages and carry different evidence.

**Minimal legitimate transfer condition:** model at least four distinct statuses—admitted, formed/configured, executed or realized, and evaluated—and attach evidence and failure conditions to the stage that owns them.

### T7 — The identity of parts and wholes is not stable across accounts

**Severity: MAJOR**

Formal owners stipulate what counts as an object, morphism, operation, syntax term, behavior, or specification. Engineered owners distinguish modules from subprograms and levels, bundle declarations from runtime wiring, steps from pipelines, blocks from generated programs, and configuration documents from integrated products. The same material can occupy different roles, and the result of an operation need not be the same kind of thing as its inputs.

Without explicit object typing, a study may silently switch between composing artifacts, capabilities, behaviors, judgments, and descriptions of those things. That makes closure and decomposition claims unfalsifiable.

**Minimal legitimate transfer condition:** declare the unit of composition, the result type, the identity criterion for both, and whether the operation is closed over that type. If the result changes level or kind, represent that transition rather than calling it generic composition.

### T8 — Associativity and order-independence are especially unsafe transfers

**Severity: MAJOR**

Some formal operations are associative up to the relevant equality or isomorphism because the owner proves or axiomatizes that fact. Engineered integration can depend on resolver state, pipeline dependencies, planned assembly order, environment preparation, and human control. Even where a graphical or declarative representation looks reorderable, execution or policy may not be.

The existence of one associative formal precedent cannot justify regrouping skills, agents, lenses, or integration steps without changing results.

**Minimal legitimate transfer condition:** define the equality notion for outcomes and test at least two parenthesizations or orders under controlled inputs. Until then, order and grouping remain causal variables.

## Composition versus neighboring relations

| Neighbor | What it establishes | What it does not establish | Evidence needed before calling it composition |
|---|---|---|---|
| Aggregation | Parts are collected or counted together | Interaction, admissibility, or a new operational whole | A relation or operation whose result depends on how parts are combined |
| Configuration / resolution | A compatible selection or wiring state exists under constraints | Execution, semantic cooperation, or preserved behavior | Explicit result state plus evidence of any claimed downstream behavior |
| Integration | Parts were assembled through a governed process | Formal closure, substitutability, or order-independence | Interface compatibility, process trace, and whole-level verification |
| Coordination | Activities or actors are aligned over time | Formation of one object or semantic unit | A declared composite result and identity criterion, if one is claimed |
| Dependency | One part's correctness or availability relies on another | A combining operation or composite artifact | An operation beyond the dependency relation, if whole formation is claimed |
| Connection | A local join is admitted | Global correctness or meaningful whole behavior | Global constraints and an evaluation of the connected result |

## Surviving convergences

The attacks do not erase every cross-map regularity. The following survive, but only as bounded research hypotheses or design cautions—not as a general theory:

1. **Co-presence is insufficient.** Both maps provide explicit non-examples in which adjacency, collection, invocation, proximity, or shared naming does not establish composition.
2. **Admissibility is relational.** Every accepted account requires some relation among parts, boundaries, contracts, environments, or rules. The representation and authority of that relation remain domain-specific.
3. **Failure boundaries are constitutive evidence.** Type mismatch, missing colimits, disallowed wiring, stuck states, circular proof, unresolved requirements, invalid ports, and incompatible interfaces help identify what each owner means by its operation.
4. **Whole-level claims require additional obligations.** Neither local part validity nor local connection validity generally proves a whole-level property. Formal accounts add laws and proofs; engineered accounts add resolution, execution, process control, or verification.
5. **The environment can be part of the composition condition.** Assume/guarantee reasoning, OSGi resolution, XProc scope, Blockly workspace checks, and NASA integration environments all resist a context-free parts-only account. What “environment” means is not shared.
6. **Preservation must name its object.** Both maps become precise only when they state what remains invariant or is established—structure, behavioral equivalence, refinement, interface validity, consistency, copy isolation, syntax, or verified function.

## Minimal legitimate cross-domain transfer protocol

A concept should move from either owner map into a broader composition model only when the proposed transfer records:

1. source owner and exact local claim;
2. source and target object types;
3. source and target operation kinds;
4. boundary or contract representation;
5. authority for admissibility rules;
6. environment and state assumptions;
7. claimed invariant or whole-level effect;
8. observation, proof, or test method;
9. explicit failure and non-example;
10. which source laws are *not* being transferred.

Without these fields, shared vocabulary is evidence of resemblance only. It is not evidence that the same composition mechanism is present.

## Disposition

**BLOCK** any generalization that treats the two owner maps as converging on a single operation, interface type, preservation law, emergence mechanism, or evaluation method.

**ALLOW, as provisional hypotheses,** the weaker convergences above: composition-like practices are distinguishable from co-presence by explicit relational admissibility; their meaning is sharpened by failures; and whole-level claims require obligations beyond validity of the parts. These hypotheses remain to be tested against the internal corpus and other external domains.
