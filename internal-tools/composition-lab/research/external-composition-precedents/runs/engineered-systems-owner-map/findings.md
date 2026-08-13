---
artifact_kind: bounded-engineered-systems-owner-map
track: external-composition-precedents
unit: engineered-systems-owner-map
status: collected
date: 2026-08-13
authority: evidence-only
---

# Engineered systems: bounded owner map

This is a source-bounded map. Each account remains separate. It does not define composition generally, compare the accounts as theories, or make a product recommendation.

## Source and search log

Effective web access was confirmed by opening and reading every admitted anchor. Access date for all sources: **2026-08-13**.

| Query / navigation step | Candidate | Decision | Reason |
|---|---|---|---|
| `Parnas On the Criteria To Be Used in Decomposing Systems into Modules PDF 1972` | D. L. Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* (1972) | Excluded | Primary modularity precedent, but the accessible passages foreground decomposition criteria rather than a sufficiently explicit operation for combining parts. |
| `David Parnas Designing Software for Ease of Extension and Contraction PDF uses relation modules interfaces` | D. L. Parnas, *Designing Software for Ease of Extension and Contraction* (ICSE 1978) | **Admitted (A1)** | Primary work by the owner; defines interfaces, the `uses` operation, admissibility conditions, preservation objective, and failure cases. |
| `site:docs.osgi.org osgi core specification bundle resolution requirements capabilities wiring` | OSGi Core Release 8, Resource API and Bundle Wiring chapters | **Admitted (A2)** | Official component/module specification; defines requirements, capabilities, namespaces, wires, resolution obligations, and invalid resolution. |
| `site:omg.org/spec/BPMN/2.0.2 PDF BPMN sequence flow process composition` | OMG BPMN 2.0.2 | Excluded | Official and relevant, but unnecessary after XProc satisfied the bounded workflow/dataflow slot with stronger pinpoint evidence. |
| `site:xproc.org/specification XProc 3.0 compound steps ports connections errors` | XProc Next Community Group, *XProc 3.0: An XML Pipeline Language* | **Admitted (A3)** | Primary/official specification for pipeline composition with ports, signatures, bindings, execution consequences, and named errors. |
| `site:developers.google.com/blockly/guides create custom blocks connection checks type checking official` | Blockly, *Custom connection checkers* | **Admitted (A4)** | Official documentation for a user-facing visual composition mechanism; defines compatibility checks and rejected connections. |
| `site:nasa.gov systems engineering handbook interface integration emergent behavior PDF` | NASA, *NASA Systems Engineering Handbook*, Rev. 2 | **Admitted (A5)** | Official institutional systems-engineering source; defines product integration activity, interface compatibility obligations, verification, and adverse emergent behavior. |
| `site:sei.cmu.edu software architecture components connectors composition primary paper pdf Allen Garlan Wright` | SEI technical reports / architecture material | Excluded | Search results did not yield a cleaner primary anchor than the five selected within the source bound. |
| `Standard ML modules signatures functors official specification PDF` | Standard ML materials | Excluded | Relevant module composition candidate, but not needed to satisfy coverage and the stable official-status chain was less direct than OSGi. |

Final anchor count: **5**.

## A1 — Parnas's `uses` structure and information-hiding interfaces

**Owner and citation.** David L. Parnas, “Designing Software for Ease of Extension and Contraction,” *Proceedings of the 3rd International Conference on Software Engineering (ICSE 1978)*, 1978, pp. 264–277. Accessible author paper via [MIT OpenCourseWare](https://ocw.mit.edu/courses/16-355j-software-engineering-concepts-fall-2005/1c68d0f98909a126ec5eb6a0ff358ec7_parnas_ease.pdf).

**Object.** A software family structured as callable programs, modules that isolate changeable decisions, and useful subsets or extensions. Parnas warns that module, subprogram, and level are not interchangeable units (pp. 274–275).

**Interface / contract.** Each callable program has a specification defining the effect of invocation; module interfaces should remain valid across versions while hiding anticipated changes (pp. 267–268). The relevant contract is therefore the program specification plus the assumptions exposed at the intermodule interface.

**Operation.** `A uses B` when correct execution of B may be necessary for A to satisfy A's specification; this is a correctness dependency, not merely a call relation (p. 268). The system structure is formed by selecting and constraining these `uses` relations; conflicts may be transformed by “sandwiching,” splitting a program so the resulting relations satisfy the stated conditions (p. 269).

**Conditions.** Parnas permits A to use B when A becomes essentially simpler, B is not substantially more complex from being barred from using A, there is a useful subset containing B without A, and no conceivably useful subset containing A without B (p. 269). A loop-free `uses` graph admits levels and usable/testable subsets (p. 269).

**Preservation / emergence.** The stated preservation target is an interface that remains valid across versions despite changes hidden inside a module (p. 267). A loop-free structure supports useful, testable subsets and minimal extensions; the paper does **not** characterize those effects as emergence.

**Failure / non-example.** Unrestrained mutual use makes parts highly interdependent, potentially leaving no usable subset until the whole system works (pp. 268–269). `Invokes` is a non-equivalent neighbor: A may invoke B without depending on B's correctness, and A may use B without invoking it (p. 268). A callable subprogram is not necessarily the module/unit of change (p. 275).

**Scope / limits.** The account targets software-family extensibility and contractibility through information hiding and a `uses` hierarchy. It does not give a general algebra of arbitrary composition, nor claim that all useful software dependencies must be hierarchical.

**Transfer risk (collector assessment, not source claim).** Transfer to skills, knowledge, work, agents, or lenses would require operational specifications precise enough to determine when one part's correctness depends on another. If “uses” is inferred from thematic relevance or observed invocation alone, the source's central distinction collapses.

**Pinpoint evidence.** Interface/change rule: pp. 267–268. Definition and distinction of `uses`: p. 268. Loop-free condition, allowed-use criteria, and sandwiching: p. 269. Module/subprogram/level distinction: p. 275.

## A2 — OSGi requirement–capability resolution and wiring

**Owner and citation.** OSGi Alliance, *OSGi Core Release 8*, Resource API Specification §6.3–6.5 and Bundle Wiring API Specification §7.1–7.2, Release 8 / Bundle Wiring API 1.2. Official HTML: [Resource API](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.resource.html) and [Bundle Wiring API](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.wiring.html).

**Object.** Resources/bundle revisions that declare requirements and capabilities, within an environment that has a current wiring state.

**Interface / contract.** A namespace types requirements and capabilities and defines their semantics. A requirement carries a filter over capability attributes; directives express mandatory/optional resolution, effectiveness, cardinality, mandatory attributes, and `uses` constraints (Resource API §§6.3–6.4.6).

**Operation.** Resolution finds wires from requirements to capabilities and adds the resulting wiring to the environment's existing state. A wire records the requirement, capability, requirer, and provider; bundle wiring is the selected runtime state rather than merely the declarations (Resource API §§6.4–6.5; Bundle Wiring §7.2.1).

**Conditions.** A basic match requires the same namespace, a matching filter, and support for mandatory attributes in `osgi.wiring.*` namespaces. Every mandatory requirement must be satisfied and all namespace constraints—including class-space consistency where applicable—must hold before the resource can provide its capabilities (Resource API §§6.3.1, 6.4, 6.4.6).

**Preservation / emergence.** The existing environment wiring is an explicit input and resolution returns an additive set of wires relative to that state. The source requires consistency of the resulting class space; it does not promise preservation of arbitrary component behavior. Capabilities are declared by resources and become available after valid resolution, so the source does **not** claim that capabilities emerge without being declared.

**Failure / non-example.** A same-namespace connection alone is insufficient: filters, mandatory attributes, transitive requirements, and namespace constraints must also hold. Unsatisfied mandatory requirements prevent resolution; an inconsistent transitive set fails with `ResolutionException` (Resource API §6.4.2; Resolver Service §58.1.3 in the same OSGi specification family).

**Scope / limits.** The model governs dependency resolution and runtime wiring for OSGi resources, with a generic requirement–capability layer. It explicitly leaves policy choices and potentially many valid solutions to the resolve context/environment; it is not a general account of semantic cooperation between components.

**Transfer risk (collector assessment, not source claim).** Transfer requires machine-checkable capabilities, requirements, namespaces, and a well-defined environment state. Applying the vocabulary to lenses or knowledge without decidable matching and consistency rules would reduce resolution to an informal analogy.

**Pinpoint evidence.** Entities and wire semantics: Bundle Wiring §§7.1.1, 7.2.1. Matching and resolution: Resource API §§6.3.1, 6.4–6.4.6. Transitive failure: Resolver Service §58.1.3.

## A3 — XProc 3.0 pipelines

**Owner and citation.** XProc Next Community Group; editors Norman Walsh, Achim Berndzen, Gerrit Imsieke, and Erik Siegel, *XProc 3.0: An XML Pipeline Language*, Community Group Report, 12 September 2022. [Stable specification PDF](https://spec.xproc.org/3.0/xproc/xproc_letter.pdf).

**Object.** Pipelines made of atomic and compound steps that consume and produce documents, with conditional, iterative, and error-handling constructs (Abstract; §2.1).

**Interface / contract.** A step's signature is its declared inputs, outputs, and options, fixed across instances. Steps participate through named input/output ports; ports declare whether they accept or produce one document or a sequence (§4).

**Operation.** A connection binds an input port to a data source. `p:pipe` explicitly connects an input to a readable output port of another step; compound steps expose outputs derived from contained subpipelines (§§4, 16.9). User-defined typed steps can be imported and invoked repeatedly (§2.1.2).

**Conditions.** Every declared input must be connected. Referenced ports must be readable in the relevant scope; defaults apply only when an explicit connection is absent. Runtime cardinality must agree when a sequence-producing port feeds a single-document input (§§4, 7.2.1, 16.2.1, 16.9).

**Preservation / emergence.** On fan-out, each destination receives a logically distinct document copy and changes to one copy must not be visible in another (§3). A compound step exposes selected outputs of its subpipeline (§4). The specification does **not** label resulting pipeline behavior as emergent.

**Failure / non-example.** An unconnected declared input is static error `err:XS0003`; an unreadable referenced port is static error `err:XS0022`; a sequence that produces other than exactly one document for a singleton input fails dynamically (§§4, 16.9). Mere textual adjacency is not necessarily composition: evaluation order of unconnected steps is implementation-dependent (§2.1).

**Scope / limits.** XProc specifies document-processing pipelines and their static/dynamic semantics. It does not explain composition of non-document knowledge, human judgments, or agents, and some ordering remains implementation-dependent when no connection establishes dependency.

**Transfer risk (collector assessment, not source claim).** Transfer requires identifiable ports, a notion of readable scope, compatible cardinality/content, and explicit data dependency. Treating chronological order or co-location as a port connection would violate the account's own neighbor distinction.

**Pinpoint evidence.** Purpose and pipeline structure: Abstract. Typed reusable steps: §2.1.2, pp. 21–23. Signatures, connections, cardinality, and errors: §4, pp. 34–36. Readable ports: §7.2.1, pp. 50–51. Explicit pipe validity: §16.9, pp. 175–176.

## A4 — Blockly connection checking

**Owner and citation.** Blockly project (Raspberry Pi Foundation, supported by Google), “Custom connection checkers,” official Blockly documentation, last updated 31 March 2026. [Official documentation](https://docs.blockly.com/guides/create-custom-blocks/inputs/connection_checker/).

**Object.** Visual programming blocks in a workspace whose value or statement connections may be joined by user interaction or programmatically.

**Interface / contract.** Block connections are the contact surface. The `ConnectionChecker` enforces safety, type, and drag checks; type information on connections states compatibility, while `IConnectionChecker` is the extension interface (“The Checks”; “Overriding the Connection Checker”).

**Operation.** A user or program connects compatible block connections. The checker mediates whether that connection is allowed; custom checkers may replace type or drag logic (“The Checks”; “Overriding the Connection Checker”).

**Conditions.** Safety checks require, among other things, that blocks share a workspace and the two connections belong to different blocks. Type checks reject values whose labeled type is incompatible with the receiving connection. Drag checks additionally restrict candidates during dragging, for example by proximity (“Safety checks”; “Type checks”; “Drag checks”).

**Preservation / emergence.** The documentation claims Blockly ensures generated code is syntactically correct. It does not specify semantic behavior preservation under block substitution, and it makes no emergence claim.

**Failure / non-example.** Connecting two `next` connections is a rejected nonsensical combination; connecting a string where a number is required is a rejected type mismatch. Spatial proximity during drag only determines which candidates are considered; it does not establish compatibility (“Safety checks”; “Type checks”; “Drag checks”).

**Scope / limits.** This page documents connection admissibility, not the full semantics of generated programs. Safety checks are presented as especially delicate and generally should not be overridden; the source does not provide a general contract theory for visual composition.

**Transfer risk (collector assessment, not source claim).** Transfer requires explicit connection kinds and validity predicates. Lenses, knowledge, or agent outputs usually lack a workspace identity, directional sockets, and type labels; inventing those after the fact could make the analogy unfalsifiable.

**Pinpoint evidence.** Page summary and “The Checks,” especially headings “Safety checks,” “Type checks,” “Drag checks,” and “Overriding the Connection Checker.”

## A5 — NASA product integration and interface management

**Owner and citation.** National Aeronautics and Space Administration, *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, 2016. [Official NASA PDF](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf).

**Object.** Validated lower-level products, enabling products, operators, environments, and documentation assembled into an integrated end product at a product layer (§5.2.1).

**Interface / contract.** Interfaces are the pathways of system interactions and may be mechanical, fluid, thermal, electrical, data, logical/software, or human. Interface requirements and Interface Control Documents/Drawings define and govern both sides of the boundary (§§5.0, 6.3.1.2.3–6.3.1.2.4; Appendix L).

**Operation.** The Product Integration Process obtains lower-level products, confirms validation, prepares the integration environment, and assembles/integrates the products in a planned sequence into the desired end product (§5.2.1, Figure 5.2-1).

**Conditions.** Received products must be validated; the integration environment and enabling products must be ready; configuration documentation must be adequate; interfaces must be properly marked and compatible with specifications and control documents (§§5.2.1.2.1–5.2.1.2.4, 6.3.1.2.3).

**Preservation / emergence.** Configuration and interface information are controlled work products, and the integrated product is checked for expected function. The handbook explicitly requires attention to interactions so there are no adverse emergent behaviors (§5.0); it does not state that a particular desirable capability necessarily emerges from every integration.

**Failure / non-example.** Incompatible or incorrectly marked interfaces, inadequate configuration documentation, unvalidated received products, and adverse emergent behavior are concrete invalidity/failure conditions (§§5.0, 5.2.1.2, 6.3.1.2.3). Configuration documents alone are inputs to integration, not the integrated product (Figure 5.2-1).

**Scope / limits.** This is lifecycle guidance for NASA systems engineering, not a formal composition calculus. It specifies process obligations and verification relationships but does not define substitutability or closure for arbitrary system elements.

**Transfer risk (collector assessment, not source claim).** Transfer requires an analog of validated lower-level products, controlled interfaces on both sides, an integration environment, and observable end-product verification. For agent or lens composition, those conditions may be unavailable or may turn an epistemic process into an unjustified assembly metaphor.

**Pinpoint evidence.** Interactions, interface kinds, and adverse emergence: §5.0, p. 84. Product Integration Process and sequence: §5.2.1–5.2.1.2.1, pp. 85–87. Interface compatibility and control: §6.3.1.2.3–6.3.1.2.4, pp. 137–138. Interface requirements by boundary side: Appendix L, pp. 236–239.

## Completion checklist

- [x] Exactly 5 admitted primary/official anchors.
- [x] Software modularity/information hiding: A1.
- [x] Official component/module model: A2.
- [x] Workflow/dataflow composition: A3.
- [x] User-facing visual composition: A4.
- [x] Systems-engineering boundary/failure account: A5.
- [x] All four substantive surfaces represented.
- [x] Every account records owner, object, interface/contract, operation, conditions, preservation/emergence, failure/non-example, scope/limits, transfer risk, and pinpoint evidence.
- [x] Unsupported preservation or emergence is marked as not claimed/not specified.
- [x] Concrete invalidity/failure cases appear in every account.
- [x] Source claims and collector transfer-risk assessments are visibly separated.
- [x] No internal corpus, sibling formal map, cross-domain synthesis, general definition, canonical verdict, or design recommendation used.
- [x] Only `findings.md` written by this run.

Unresolved gaps: Blockly's cited page governs connection validity but not whole-program semantic preservation; NASA gives process obligations rather than formal closure/substitution; Parnas provides dependency admissibility rather than a generic combining operator; XProc is limited to document pipelines; OSGi permits multiple valid resolutions and delegates policy to the environment.
