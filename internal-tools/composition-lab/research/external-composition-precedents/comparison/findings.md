---
artifact_kind: provisional-external-synthesis
track: external-composition-precedents
status: candidate
date: 2026-08-13
authority: evidence-only
inputs: accepted-owner-maps-and-bounded-comparison-only
---

# Provisional external synthesis

## One-line answer

The accepted external sources establish several domain-owned ways of forming, licensing, connecting, resolving, interpreting, or verifying wholes, but they do not yet establish one shared operation or a general account of composition. ([formal map, F1–F6](../runs/formal-structural-owner-map/findings.md); [engineered map, E1–E5](../runs/engineered-systems-owner-map/findings.md); [correspondence matrix](correspondences.md); [transfer-skeptic analysis, T1–T8](transfer-skeptic.md))

## What the sources establish separately

The formal owners make different operations precise under different assumptions: typed arrow chaining (F1), pushout gluing of open decorated systems (F2), typed many-to-one substitution (F3), behavior of constructor-built syntax through transition rules (F4), compatibility between syntax and behavior through a distributive law (F5), and conjunction plus assume/guarantee proof obligations (F6). Their associativity, closure, preservation, refinement, or behavioral results remain local to those formalisms and hypotheses. ([formal map, F1–F6](../runs/formal-structural-owner-map/findings.md); [formal review](../runs/formal-structural-owner-map/review.md))

The engineered owners establish another heterogeneous set: correctness dependencies and stable information-hiding interfaces (E1), environment-relative requirement/capability resolution (E2), explicit document-pipeline connections with static and dynamic conditions (E3), local visual-connection admissibility (E4), and governed product integration followed by whole-product verification (E5). These accounts do not jointly supply an algebra, and several do not claim to construct a composite object at all. ([engineered map, E1–E5](../runs/engineered-systems-owner-map/findings.md); [engineered review](../runs/engineered-systems-owner-map/review.md); [transfer-skeptic analysis, T2](transfer-skeptic.md))

## Weak convergences that survived

**Corpus-construction caveat:** the recurrences below are selection- and schema-conditioned. The formal inquiry asked each account for its operation/interface, formation conditions, and failure boundaries; the engineered map required every admitted account to record operation, conditions, and failure/non-example, and excluded a candidate that lacked a sufficiently explicit combining operation. Their recurrence is therefore diagnostically useful inside this comparison, but it is not independent evidence that these features prevail across composition domains. ([formal map, question and boundary](../runs/formal-structural-owner-map/findings.md); [engineered map, source and search log and completion checklist](../runs/engineered-systems-owner-map/findings.md))

Under that limitation, the comparison exposes these weak candidate constraints:

- **Co-presence is insufficient in the admitted cases:** collection, adjacency, invocation, proximity, or shared naming does not by itself satisfy the owners' operation-specific conditions. ([correspondence matrix, failure/non-example rows](correspondences.md); [transfer-skeptic analysis, surviving convergence 1](transfer-skeptic.md))
- **Admissibility is represented relationally in the admitted cases:** each constrains a proposed combination through some relation among boundaries, types, contracts, requirements, rules, authorities, or environments; the relation itself is not shared. This is a schema-conditioned comparison result, not evidence of independent cross-domain prevalence. ([correspondence matrix, bounded observation 1](correspondences.md); [transfer-skeptic analysis, surviving convergences 2 and 5](transfer-skeptic.md))
- **Recorded failures help discriminate the admitted operations:** mismatched boundaries, missing structure, invalid wiring, stuck execution, circular proof, unresolved requirements, bad ports, and incompatible interfaces mark different formation boundaries. Because failure/non-example was a required field, this supports diagnostic use only, not an unconditioned recurrence claim. ([formal map, coverage record](../runs/formal-structural-owner-map/findings.md); [engineered map, E1–E5 failure/non-example fields](../runs/engineered-systems-owner-map/findings.md); [transfer-skeptic analysis, surviving convergence 3](transfer-skeptic.md))
- **Whole-level claims need extra evidence in these accounts:** valid parts or valid local connections do not alone establish whole behavior; the owners add proofs, resolution, execution semantics, process controls, or verification. ([correspondence matrix, laws and whole-behavior rows](correspondences.md); [transfer-skeptic analysis, T4, T6 and surviving convergence 4](transfer-skeptic.md))
- **Preservation is property-specific in these accounts:** precise accounts name what is preserved or established and under which assumptions; “meaning” or “correctness” without an observable, equivalence, proof, or test remains unsupported. ([formal map, F1–F6 laws/preservation fields](../runs/formal-structural-owner-map/findings.md); [engineered map, E1–E5 preservation/emergence fields](../runs/engineered-systems-owner-map/findings.md); [transfer-skeptic analysis, T4 and surviving convergence 6](transfer-skeptic.md))

These are candidate research constraints, not elements of a general definition. That restraint is required by the external research brief and the broader program. ([external initial definitions, constraints and gaps](../research-initial-definitions.md); [research program, limits](../../../research-program.md))

## Rejected transfers and same-word traps

- **“Interface” is not one object:** categorical boundaries, cospan feet, typed ports, imports/exports, specifications, resolver declarations, visual sockets, and controlled engineering documents differ in type, authority, and function. ([transfer-skeptic analysis, T1](transfer-skeptic.md))
- **Composition is not interchangeable with dependency, connection, configuration, resolution, integration, or coordination:** these may constrain, select, connect, assemble, execute, or prove different result kinds. ([transfer-skeptic analysis, T2 and neighboring-relations table](transfer-skeptic.md))
- **Formal laws do not transfer by resemblance:** no accepted engineered correspondence demonstrates associativity, identities, closure, structure preservation, or staging independence. ([correspondence matrix, bounded observations 2–3 and final paragraph](correspondences.md); [transfer-skeptic analysis, T4 and T8](transfer-skeptic.md))
- **“Emergence” is not a common output:** NASA treats adverse emergent behavior as an integration risk, while the formal owners mostly derive or preserve behavior under specified rules; no shared emergence mechanism is evidenced. ([correspondence matrix, emergence row and bounded observation 4](correspondences.md); [transfer-skeptic analysis, T5](transfer-skeptic.md))
- **Typing and compatibility are authority-dependent:** mathematical signatures and hypotheses are not equivalent to mutable standards, policies, checkers, configuration, or design authority. ([transfer-skeptic analysis, T3](transfer-skeptic.md))
- **Formation, execution, and evaluation are not one event:** a structure may be admitted or formed yet fail during realization or fail a later whole-level check. ([formal map, F4](../runs/formal-structural-owner-map/findings.md); [engineered map, E2, E3 and E5](../runs/engineered-systems-owner-map/findings.md); [transfer-skeptic analysis, T6](transfer-skeptic.md))

## Candidate vocabulary — explicitly provisional

The following terms are useful only as comparison fields to test in further external work; they are not definitions or required components of every case:

| candidate field | bounded use | current limit |
|---|---|---|
| participating unit | what an owner treats as input to an operation or relation | input identity may change by level or role ([transfer-skeptic analysis, T7](transfer-skeptic.md)) |
| result kind | the object, state, behavior, proof, or product claimed after the operation | some accounts constrain or select rather than construct ([transfer-skeptic analysis, T2](transfer-skeptic.md)) |
| operation kind | constructs, glues, substitutes, connects, resolves, executes, proves, or integrates | no shared operation has been shown ([correspondence matrix](correspondences.md)) |
| admissibility relation | the check or obligation that licenses a proposed operation | representation and authority remain domain-specific ([transfer-skeptic analysis, T1 and T3](transfer-skeptic.md)) |
| environment / state | context on which admission, behavior, or verification depends | its meaning differs across assume/guarantee, OSGi, XProc, Blockly, and NASA ([transfer-skeptic analysis, surviving convergence 5](transfer-skeptic.md)) |
| stage status | admitted, formed/configured, realized/executed, evaluated | the four stages are a comparison discipline, not an established universal lifecycle ([transfer-skeptic analysis, T6](transfer-skeptic.md)) |
| claimed invariant or effect | the named property proved, preserved, produced, or observed | requires owner-specific proof or measurement ([transfer-skeptic analysis, T4](transfer-skeptic.md)) |
| failure boundary | the condition making an operation undefined, invalid, stuck, unresolved, or unsuccessful | failure types are not interchangeable ([transfer-skeptic analysis, T6](transfer-skeptic.md)) |
| residue / recoverability | what remains visible, reusable, provable, or reconstructable after composing or decomposing | currently under-owned and unresolved ([correspondence matrix, decomposition/residue rows and bounded observation 5](correspondences.md)) |

## Implications for the next external research

1. Add domains in which composition is situated, epistemic, expressive, or material, because the accepted corpus is limited to formal structures and engineered systems; this is a coverage need, not evidence that those domains will converge. ([external initial definitions, known gaps](../research-initial-definitions.md); [research program, external line](../../../research-program.md))
2. Search specifically for owners of decomposition, reversibility, residue, loss, and recovery; the current comparison cannot support an inverse or recoverability account. ([correspondence matrix, decomposition/residue rows and bounded observation 5](correspondences.md))
3. Require each new owner map to separate operation, result kind, admissibility authority, environment, stage of evidence, named invariant/effect, and failure. This directly tests the candidate constraints without presuming they are universal or independently prevalent. ([transfer-skeptic analysis, minimal transfer protocol](transfer-skeptic.md))
4. Test order and grouping rather than importing associativity: compare outcomes under controlled reorderings or parenthesizations using an explicit equality criterion. ([transfer-skeptic analysis, T8](transfer-skeptic.md))
5. Treat any emergence claim as a causal hypothesis requiring an isolated-parts baseline, interaction mechanism, whole-level observable, measurement, and ablation or counterfactual. ([transfer-skeptic analysis, T5](transfer-skeptic.md))

## What remains unknown

It remains unknown whether the external cases form one family, several incompatible families, or only a useful comparison set; whether part identities precede or are transformed by composing; whether any admissibility structure transfers beyond its owner; when order matters; what is lost or recoverable; and whether any whole-level novelty is interaction-produced rather than selected, aggregated, executed, or attributed by an observer. ([external initial definitions, known gaps](../research-initial-definitions.md); [correspondence matrix, bounded observations](correspondences.md); [transfer-skeptic analysis, T5, T7 and T8](transfer-skeptic.md))

No external evidence in this bounded synthesis authorizes a general definition of composition, a repository classification, or a product or architecture decision. ([external initial definitions, purpose and constraints](../research-initial-definitions.md); [research program, limits](../../../research-program.md))
