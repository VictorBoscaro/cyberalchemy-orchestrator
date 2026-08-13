---
artifact_kind: research-findings
track: external
run: formal-structural-owner-map
status: complete
date: 2026-08-13
sources: 6
---

# Formal and structural owner map

## Question and boundary

How do specific formal traditions represent formation of a whole from parts; which
operations or interfaces license it; which laws or properties are preserved; and when is
composition undefined, invalid, or insufficient?

This is an owner map, not a unified theory. Each finding remains scoped to the formalism
that owns it. “Evidence” reports what the source establishes; “paraphrase” restates it for
this question; “inference” is a deliberately weaker interpretation that the source does not
itself establish.

## 1. Ordinary category composition

- **owner:** Tom Leinster, *Basic Category Theory*, Definition 1.1.1 and Remark 1.1.2(b),
  [§1.1, pp. 10–11 (PDF pp. 17–18)](https://arxiv.org/pdf/1612.09375).
- **composed_object:** Morphisms/arrows arranged as a typed chain
  `A₀ → A₁ → ... → Aₙ`; the composite is another morphism `A₀ → Aₙ`.
- **operation_or_interface:** Binary morphism composition. The codomain of the first arrow
  and domain of the second are the interface that must coincide.
- **formation_conditions:** For `f: A → B` and `g: B → C`, the category supplies
  `g ∘ f: A → C`. Identity morphisms supply neutral compositions.
- **laws_or_preservation:** Associativity and left/right identity are axioms. A typed chain
  therefore determines one composite independently of parenthesization.
- **failure_or_non_example:** The primitive operation is not defined by the category axioms
  for arrows whose adjoining boundary objects do not match. Merely collecting objects or
  parallel arrows is not morphism composition.
- **scope_and_limits:** This definition controls typed chaining and coherence. It does not say
  that objects are “parts,” explain the internal formation of an object, or assign empirical
  meaning to an arrow.
- **transfer_risk:** High if `A`, `B`, and `C` are replaced by informal labels without a
  justified notion of morphism and boundary equality; associativity would then be asserted by
  analogy rather than demonstrated.
- **epistemic separation:**
  - **Evidence:** Leinster defines the composition function only on
    `A(B,C) × A(A,B)` and requires associativity and identity laws (Definition 1.1.1).
  - **Paraphrase:** Category composition licenses chaining through an exactly shared typed
    boundary and makes regrouping irrelevant.
  - **Inference:** A project-level composition interface might need an analogue of typed
    boundaries and identity operations. The source does not establish what those analogues are.

## 2. Open systems as decorated cospans

- **owner:** Brendan Fong, “Decorated Cospans,”
  [§§1, 2.1, 3](https://arxiv.org/abs/1502.00872) (Theory and Applications of Categories
  30, 2015, 1096–1120).
- **composed_object:** Open, decorated networks represented by a cospan
  `X → N ← Y` plus a decoration on apex `N`; the resulting composite remains an open
  decorated network from `X` to `Z`.
- **operation_or_interface:** Sequential gluing by pushout over the shared foot `Y`;
  decorations combine via the monoidal product and are transported along the copairing into
  the pushout. Coproduct gives parallel/monoidal juxtaposition.
- **formation_conditions:** The base category must provide the needed finite colimits; the
  decorating assignment must be a lax braided monoidal functor; sequential inputs must share
  the boundary object used by the pushout.
- **laws_or_preservation:** Isomorphism classes of decorated cospans form a category;
  composition is well-defined, associative, and unital. Under the stronger stated structure,
  the result is symmetric monoidal and hypergraph, and the relevant functors preserve that
  structure (Proposition 3.2; Corollary 3.5; Theorem 4.1).
- **failure_or_non_example:** Without the required pushout there is no stated gluing operation;
  without the lax monoidal/coherence data there is no licensed rule for combining arbitrary
  decorations. Juxtaposition by coproduct and gluing over an interface are distinct operations.
- **scope_and_limits:** The construction applies to systems representable as cospans with
  explicit input/output feet and functorial apex decorations. It does not claim that every
  organized whole has this boundary shape.
- **transfer_risk:** Medium-high. “Interface” must support an actual gluing construction, and
  the extra content must transform coherently. Calling metadata a decoration is insufficient.
- **epistemic separation:**
  - **Evidence:** Fong states pushout composition for cospans (§2.1), defines the decorated
    form (Definition 3.1), and proves the category and preservation results (Proposition 3.2,
    Theorems 3.5 and 4.1).
  - **Paraphrase:** This owner separates boundary structure, internal system structure, and
    the law that carries internal structure through gluing.
  - **Inference:** That separation may be diagnostically useful for project artifacts, but no
    mapping from skills, lenses, or work products to cospans has been established here.

## 3. Operads and wiring diagrams

- **owner:** David I. Spivak, “The operad of wiring diagrams: formalizing a graphical
  language for databases, recursion, and plug-and-play circuits,”
  [§§1–2, 4.1, 6](https://arxiv.org/html/1305.0297).
- **composed_object:** Many input operations/entities inserted into a wiring diagram to
  produce one output entity; nested diagrams flatten to another wiring diagram. An algebra on
  the operad chooses what entities are and how each diagram acts on them.
- **operation_or_interface:** Multivariable operadic substitution. In the typed variant, ports
  carry value types and wiring identifies compatible ports/cables; the composition formula is
  built using a pushout.
- **formation_conditions:** An operad fixes colors/types, admissible wiring operations,
  symmetric actions, identities, and substitution. A chosen algebra must interpret every such
  operation coherently in a target domain.
- **laws_or_preservation:** Operadic associativity makes substitution of diagrams into diagrams
  independent of staging; units act neutrally; equivariance accounts for permutation. An
  operad algebra preserves this operation structure in its interpretation.
- **failure_or_non_example:** In the typed operad, wires to be connected must have matching
  types (§4.1). A picture is not yet a composition rule until an operad admits it, and an operad
  does not determine domain behavior until an algebra is chosen. The paper also finds that
  simple additive invariants for its relational algebra are generally uninformative (§3.1), a
  concrete warning that not every desired summary is preserved.
- **scope_and_limits:** The paper owns a particular family of wiring-diagram operads and
  algebras for relations, databases, circuits, recursion, and plug-and-play. It does not show
  that all hierarchy or collaboration is operadic.
- **transfer_risk:** High if a workflow sketch is treated as an operad without specifying
  admissible substitutions, typing, identities, and algebraic interpretation.
- **epistemic separation:**
  - **Evidence:** Spivak defines wiring diagrams as operadic morphisms, uses nested
    substitution as their composition, requires type agreement in the typed variant, and
    distinguishes the operad from an algebra interpreting it.
  - **Paraphrase:** The formalism makes “how parts may be plugged together” separate from
    “what the plugged-together thing does.”
  - **Inference:** This syntactic/semantic separation could guide experiments on composition,
    but the source supplies no evidence that repository compositions satisfy operad laws.

## 4. Structural operational semantics (SOS)

- **owner:** Gordon D. Plotkin, “A Structural Approach to Operational Semantics,”
  [§§3.3–3.5, pp. 34–41; §5.3, pp. 57–59](https://homepages.inf.ed.ac.uk/gdp/publications/sos_jlap.pdf).
- **composed_object:** Compound program phrases or definitions built from syntax constructors;
  their behavior is a transition relation derived from rules referring to component behavior
  and state/environment.
- **operation_or_interface:** Syntax constructors such as sequential command composition,
  conditionals, loops, and sequential/simultaneous/private definitions. For definitions,
  imports and exports form explicit dataflow interfaces.
- **formation_conditions:** A compound must be syntactically well-formed, and its premises must
  match an operational rule. Sequential definitions export from the first into the second;
  simultaneous definitions require no common defined variable in the presented language.
- **laws_or_preservation:** The rule format supports proofs by structural induction. Plotkin
  demonstrates properties such as determinism of expression transitions and preservation of a
  variable not assigned by a command (Facts 13 and 15); these are proved properties of this
  rule system, not generic consequences of having syntax.
- **failure_or_non_example:** A nonterminal configuration with no outgoing transition is
  “stuck” (Definition 11, p. 28). Conflicting exports make the presented simultaneous-definition
  form ill-formed. A syntactic constructor alone does not guarantee determinism, progress, or
  another semantic property; the rules and proof carry that burden.
- **scope_and_limits:** SOS explains behavior of structurally built language phrases. It is not
  by itself a theory of physical wholes, social coordination, or emergent novelty.
- **transfer_risk:** Medium-high. Treating a workflow as syntax is useful only if its steps,
  states, transition premises, and error/stuck conditions can be made explicit.
- **epistemic separation:**
  - **Evidence:** The source supplies structural rules, import/export accounts for compound
    definitions, a definition of stuckness, and structural-induction proofs of named properties.
  - **Paraphrase:** Composition here means that constructors plus rules determine whole-program
    transitions from component configurations.
  - **Inference:** Repository workflows might be tested for missing rules or stuck states, but
    this source does not license representing every work practice as a program semantics.

## 5. Bialgebraic compositional semantics

- **owner:** Daniele Turi and Gordon Plotkin, “Towards a Mathematical Operational Semantics,”
  [pp. 1–2 and §§7.1–7.3](https://homepages.inf.ed.ac.uk/gdp/publications/Math_Op_Sem.pdf).
- **composed_object:** Program syntax generated by a signature/monad, equipped with operational
  behavior represented coalgebraically; a bialgebra combines the algebraic and coalgebraic
  structures under one compatibility law.
- **operation_or_interface:** A distributive law of the syntax monad over the behavior comonad
  mediates the two structures. Abstract GSOS/tree-rule formats are represented by suitable
  natural transformations.
- **formation_conditions:** Syntax must freely generate the relevant monad, behavior must admit
  the stated coalgebraic/comonadic treatment, and rules must fit the natural-transformation or
  distributive-law form with the category providing the required structure.
- **laws_or_preservation:** Under those conditions the construction yields intended operational
  and canonical denotational models; the universal semantics is compositional and preserves
  behavioral distinctions up to the chosen coalgebraic bisimulation (§7.3).
- **failure_or_non_example:** The paper reports that attempting to fit simple negative tree rules
  exposed an inaccuracy and motivated the stricter “safe” subclass (p. 2). Thus an arbitrary set
  of structural-looking rules does not inherit the adequacy or congruence results. Changing the
  behavior functor changes the relevant equivalence (for example, bisimulation versus traces).
- **scope_and_limits:** The preservation theorem concerns specified syntax and behavioral
  equivalence under strong categorical hypotheses. It does not preserve every property and is
  not a domain-free definition of whole formation.
- **transfer_risk:** High. “Behavior,” “syntax,” and “compatibility” need mathematical carriers
  and a proven law; metaphorical bialgebra language would contribute no theorem.
- **epistemic separation:**
  - **Evidence:** Turi and Plotkin state the natural-transformation precondition, derive
    operational/denotational models, and prove preservation of behavioral distinctions; they
    also document a rule class that fails to fit.
  - **Paraphrase:** Whole-program meaning is compositional only when syntax-building and
    behavior interact through a disciplined compatibility law.
  - **Inference:** A composition experiment could look for an analogous compatibility
    obligation between assembly and evaluation, but the theorem cannot be transferred without
    reconstructing its formal assumptions.

## 6. Assume/guarantee composition of concurrent specifications

- **owner:** Martín Abadi and Leslie Lamport, “Composing Specifications,”
  [Introduction and §1.4, pp. 73–80; §5.3](https://lamport.azurewebsites.net/pubs/abadi-composing.pdf),
  ACM TOPLAS 15(1), 1993.
- **composed_object:** Specifications of interacting concurrent components; semantically a
  specification is a set of behaviors, and the composed specification is conjunction/
  intersection before proving implementation of a higher-level specification.
- **operation_or_interface:** Logical conjunction of component specifications plus an
  assume/guarantee proof rule. Each component’s environment consists of the external
  environment together with the other components.
- **formation_conditions:** Component guarantees must jointly imply the system guarantee; the
  external assumption plus other component guarantees must establish each component’s
  assumption; each component must meet its own guarantee under that assumption. The paper adds
  realizability and safety/liveness hypotheses to make the circular rule sound.
- **laws_or_preservation:** Under the paper’s hypotheses, satisfaction by components supports a
  proof that their composition implements the higher-level specification. The preserved object
  is the proved guarantee/refinement, not necessarily each component’s behavior in isolation.
- **failure_or_non_example:** The naïve composition principle is circular and is explicitly not
  always valid (p. 74): each guarantee may be invoked to establish the assumptions on which that
  guarantee depends. The authors’ later note also says their explicit realizable-part treatment
  was superseded, so this paper should not be imported as current TLA+ prescription
  ([publication note](https://www.microsoft.com/en-us/research/publication/composing-specifications/)).
- **scope_and_limits:** This is a semantic proof theory for interacting systems specified by
  safety/liveness properties and agent/environment distinctions. It does not describe how an
  arbitrary artifact acquires identity as a whole.
- **transfer_risk:** Medium-high. Informal “assumptions” and “guarantees” do not reproduce the
  result unless circular dependence, realizability, environment ownership, and refinement are
  represented and checked.
- **epistemic separation:**
  - **Evidence:** Abadi and Lamport define composition as conjunction in their semantic setting,
    formulate the three-part composition principle, show why it is circular, and develop the
    extra conditions needed for a valid proof rule.
  - **Paraphrase:** Component correctness does not automatically compose when components form
    one another’s environments.
  - **Inference:** Multi-agent or multi-skill arrangements may have the same circularity hazard,
    but this source does not show that their outputs are temporal behaviors or that its rule
    applies to them.

## Coverage record (not a synthesis)

| tradition / formal recut | owner source | operation represented | explicit local failure boundary |
|---|---|---|---|
| Ordinary categories | Leinster | Typed sequential arrow composition | Adjoining domain/codomain mismatch |
| Categorical open systems | Fong | Pushout gluing plus coherent decoration transport | Missing colimit or monoidal coherence |
| Operads | Spivak | Typed many-to-one substitution of wiring diagrams | Disallowed wiring, type mismatch, or absent algebra |
| Structural operational semantics | Plotkin | Syntax constructors interpreted by transition rules | Ill-formed interface or stuck configuration |
| Bialgebraic semantics | Turi–Plotkin | Distributive law joining syntax and behavior | Rule format or categorical hypotheses fail |
| Concurrent modular specification | Abadi–Lamport | Conjunction plus assume/guarantee proof rule | Circular reasoning without realizability/side conditions |

The table records coverage only. It does not establish that these operations are instances of one
mechanism, that their “interfaces” are interchangeable, or that any one should govern the
Composition Lab.

## Bounded answer

These owners each make composition conditional on explicit admissibility data—typed boundaries,
gluing colimits, operadic substitution, transition premises, compatibility laws, or environment
assumptions—and each derives only formalism-specific preservation results. The evidence does not
support a domain-general definition of composition or a direct transfer to repository artifacts.
