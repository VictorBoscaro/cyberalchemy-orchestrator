# Linguagem Operacional do Conhecimento - caderno editorial e conceitual

> Status: working notes; not a ratified discovery, ontology, specification, plan, or formal model.
>
> Started: 2026-08-11
>
> Claim discipline: every statement below is marked as an editorial decision, working definition,
> hypothesis, heuristic, observation, or open question. Nothing here has runtime or governance
> authority.

## Purpose

Preserve the current editorial and conceptual state of the inquiry provisionally called
**Linguagem Operacional do Conhecimento**. The notebook exists so the argument can become clearer
without silently converting an emerging vocabulary into a canonical ontology.

The immediate editorial objective is modest: explain how systems thinking, category theory, and
operational epistemology contribute different but composable operations. The larger research
objective remains open: determine whether a small typed grammar can describe how knowledge is
proposed, represented, transported, tested, revised, and realized.

## How this inquiry began

**Observation.** This thread began as an editorial revision of *Entre Sistemas e Categorias*, not
as an ontology project. The requested changes were a warmer paper field, the CyberAlchemy mark,
visible and invisible attribution, and a richer opening diagram.

The opening diagram presents three contributory traditions. In v0.2, its title and caption use
"três tradições" consistently:

```text
systems thinking       -> dynamics of the phenomenon
category theory        -> structure and transport
operational epistemology -> discovery and revision
                         ↓
             operational language of knowledge
```

Adding analogy to the epistemological box exposed a deeper issue: analogy, composition, boundary,
residue, lens, intervention, and probe do not belong exclusively to one tradition. Some are
structures, some operations, some judgments, and some witnesses of failure. The editorial problem
therefore became a typing problem.

The immutable rendered baseline for the patch pipeline is
[`entre_sistemas_e_categorias_revisado.pdf`](../../../output/pdf/entre_sistemas_e_categorias_revisado.pdf).
The current publication snapshot is
[`entre_sistemas_e_categorias_v0.2.pdf`](../../../output/pdf/entre_sistemas_e_categorias_v0.2.pdf).
Version 0.2 resolves the earlier *registros/tradições* ambiguity rather than silently
reinterpreting the baseline.

### Current editorial handoff

**Observed artifact.** The edited figure is the opening figure on page 1. The current visible
vocabulary is:

| Box | Current terms |
|---|---|
| Pensamento sistêmico | feedback; estoques/fluxos; atrasos; fronteiras; causalidade; intervenção |
| Teoria das categorias | objetos/morfismos; composição; funtores/transporte; equivalência; invariantes/preservação; construções universais |
| Epistemologia operacional | lentes/probes; sinais; analogias; hipóteses; reframing; resíduos/revisão |
| Linguagem operacional do conhecimento | tipos/schemas; regras de composição; provenance; grounding; instanciação/generatividade; governança |

Bridge concepts remain deliberately non-exclusive. Analogy crosses epistemology and transport;
composition crosses all boxes; boundary crosses systems, epistemology, and possible formalization;
residue crosses interpretation and representation; lens crosses epistemology and representation;
intervention/probe crosses observation and alteration of a phenomenon. The current figure expresses
these bridges through convergence, not by duplicating every bridge label.

No full Writer/ODT source model for the revised publication is currently retained. The repository
does retain a versioned PyMuPDF patch pipeline at
[`tools/pdf/entre_sistemas_e_categorias_v02.py`](../../../tools/pdf/entre_sistemas_e_categorias_v02.py),
with its immutable PDF input, output contract, and pinned source hash documented in
[`tools/pdf/README.md`](../../../tools/pdf/README.md). This is a durable semantic-visual patch
source, not a substitute for reconstructing the document in a complete editable authoring format.
The v0.2 output is explicitly untagged; a tagged accessible edition requires that full-source
reconstruction.

## Editorial thesis

**Hypothesis.** The three traditions are most useful here as complementary repertoires rather than
as equivalent theories:

- systems thinking supplies descriptions of dynamics, boundary, feedback, causality, and
  intervention;
- category theory supplies disciplines of typing, composition, transport, equivalence, and
  preservation;
- operational epistemology supplies lenses, probes, hypotheses, analogy, reframing, and revision;
- an operational language would make the interfaces, judgments, evidence, provenance, and
  residues among them explicit.

**Editorial decision for the current figure.** Keep the opening diagram panoramic. It may mix
structures, operations, and properties for orientation, but it must not be cited as the detailed
taxonomy of the theory.

## A correction that must survive

**Working definitions.** Composition, compatibility, equivalence, and compression are distinct:

| Term | Current working meaning |
|---|---|
| Composition | Connecting typed differences through a valid interface or rule. |
| Compatibility | A judgment that a proposed connection is admissible. |
| Equivalence | A judgment that substitution preserves the structure relevant to a stated context. |
| Compression | Identifying or discarding distinctions under an explicit preservation criterion. |

Composition does not require similarity, symmetry, equivalence, or compression. Different things
may compose precisely because their interfaces are compatible. Equivalence becomes relevant when
one thing is to stand in for another; compression becomes relevant when distinctions are to be
collapsed.

> Compor é conectar diferenças por interfaces válidas. Equivaler é julgar quando uma diferença
> pode ser ignorada. Algumas tarefas exigem ambas as operações, sem que uma se reduza à outra.

## Candidate typing map

**Hypothesis.** A single hierarchy is unlikely to type the vocabulary adequately. The material
currently suggests several *classificatory perspectives*, not yet proven to be orthogonal:

1. what kind of thing an occurrence is;
2. in which register it occurs or is represented;
3. what it operates on recursively;
4. relative to which intention, question, or task it matters;
5. which transversal properties or judgments apply to it.

The fifth perspective is explicit because the source notes alternated between treating intention
and transversal properties as the fourth coordinate. That instability is preserved here as an
open modeling issue rather than hidden by the word "orthogonal".

### Kinds of occurrence

| Candidate kind | Examples | Boundary that remains open |
|---|---|---|
| Orienter | intention, question, objective, constraint | External index, internal structure, or normative content? |
| Semantic/structural element | distinction, type, relation, state, transformation | Which are primitive and which require prior carriers or criteria? |
| Structure | lens, frame, schema, model, theory, system | When does a local organization become stable enough to change kind? |
| Operation | distinguish, compose, transport, probe, abstract, instantiate, reframe | Which operations are primitive, partial, or families of operations? |
| Readout or witness | signal, evidence, counterexample, rupture, residue, obstruction | Event, interpretation, judgment, or persisted artifact? |
| Judgment | relevance, compatibility, equivalence, preservation, sufficiency | Relation, predicate, proof obligation, or contextual decision? |
| Realization | experiment, action, workflow, implementation, behavior | Representation of an effect versus the effect itself? |

Multiple classification may be legitimate. The table is a diagnostic vocabulary, not a closed
sum type.

One live differentiation inside the aggregate "readout or witness" row is:

- **signal:** a readout;
- **evidence:** a signal interpreted relative to a hypothesis or frame;
- **witness:** evidence that establishes a specific judgment;
- **rupture:** an event in which a structural expectation fails;
- **residue:** a representation of what did not close;
- **obstruction:** a residue that blocks a specified construction.

**Hypothesis.** This differentiation may be useful, but it is not a settled hierarchy. In
particular, whether every residue must be persistent and typed remains contested.

### Candidate registers

**Hypothesis.** The notes distinguish phenomenal/systemic, interactional/observational,
epistemic, representational, operational/realizational, and normative/governance registers. These
are not stages and must not be treated as layers of reality merely because they can be listed.

The status of "meta/reflexive" is unresolved. Two live alternatives must remain visible:

- **meta as register:** the subject matter is the knowledge mechanism itself;
- **meta as recursive order:** an operation is applied to a representation or mechanism that
  itself produces representations.

A future case must discriminate these alternatives; the notebook does not merge them.

### Recursive order

**Working distinction.** First-order operations concern a domain; higher-order operations concern
representations, policies, or mechanisms that produce representations. Reflexivity is stronger
than merely being higher-order: the language represents elements of its own language and can
operate on those representations.

Non-commutativity alone does not establish temporal path dependence. Temporal and historical
claims additionally require state, ordering, and dependence on the traversed path.

## Em busca do kernel mínimo

The three traditions may be more than three boxes to be combined. **Risky, strong hypothesis:**
they are distinct repertoires with which to investigate a grammar that may sit beneath all three.
Category theory stresses composition, transformation, equivalence, and preservation; systems
thinking stresses the behavior and interaction of the domain; operational epistemology stresses
orientation, probes, evidence, and revision. The proposed kernel is the object of their joint
investigation, not a fourth tradition and not a conclusion already established.

The guiding question is:

> What must be fixed, and what may remain free, relative to a task and lens?

This gives minimalism a provisional epistemic form: seek structure that is minimally sufficient
under an explicit task, risk, and preservation criterion. It does not require a unique minimum or
a maximum amount of freedom; several incomparable, Pareto-relevant solutions may exist.

> **Hypothesis of a candidate kernel.** An operational language may refine its distinctions and
> transformations when specified contacts with a domain produce mismatches relevant to a task.
> This is one strong and risky hypothesis of the inquiry, not a definition of knowledge.

### Four provisional components

The current architecture separates four components that must not be collapsed:

| Component | Provisional role | What it must not silently import |
|---|---|---|
| **Kernel (K)** | orientation/context; distinction; relation/transformation; composition | observation, truth, agency, or a complete ontology |
| **Ground (G)** | the target, process, or situation about which the language operates | the claim that the domain is intrinsically or absolutely "resistant" |
| **Contact (C)** | interpretations/actions from language to ground and readouts from ground to language | transparent access, neutral observation, or automatic evidential force |
| **Enrichments (E)** | removable/addable structures such as time, probability, causality, agency, normativity, logic, modality, and geometry | universal necessity or monotonic improvement |

"Resistance" names a mismatch observed under a specified contact, expectation, and judgment; it
is not the definition of ground. Contact is not thereby promoted into the kernel, but without it
probe, signal, evidence, and empirical residue cannot be reconstructed.

The kernel itself remains a dependency hypothesis:

1. **orientation or context** - what makes a difference relevant;
2. **distinction** - what may differ;
3. **relation or transformation** - how differentiated terms connect or change;
4. **composition** - how typed local structures may connect.

Relation and transformation stay paired but distinct. Reducing a static, symmetric, or n-ary
relation to transformations can require additional carriers, truth values, products, spans,
typing, or direction. The reduction is not available for free.

| Candidate | Possible hidden dependency |
|---|---|
| Orientation/context | agent, value, norm, question, task, or evaluation criterion |
| Distinction | a carrier or alternatives and a criterion of discrimination |
| Relation | relata, arity, typing, and admissibility |
| Transformation | source, target, identity conditions, and preserved structure |
| Composition | partial typed interfaces, compatibility and formation judgments, closure, identity, and possibly associativity |

Calling these notions "minimal", "sufficient", "independent", or "primitive" remains prohibited
until dependency analysis and counterexamples support the claim. In particular, composition must
first be expressible as a partial typed operation with formation judgments; it cannot rely on an
already complete schema that the kernel is supposed to help reconstruct.

### Minimal contact and readout contract

At least the following roles must be expressible outside the kernel:

```text
representation -> expectation
interpretation/action/probe -> ground
ground -> readout
expectation x readout x relevance criterion -> situated judgment
```

An interpretation says what kernel distinctions address in the ground; an action or probe may
observe, perturb, or intervene; a readout carries a response back; a comparison under a criterion
can then judge whether something failed to close. These arrows are roles, not yet a commitment to
deterministic functions, lossless channels, or a single observer.

### Reconstruction sketches and imported dependencies

The following are proposed sketches, not formal derivations. A successful reconstruction must
state its formation and judgment rules and account for the dependencies named here.

| Candidate | Sketch | Dependencies that must remain visible |
|---|---|---|
| Lens | contextual selection and organization of distinctions, relations, probes, and necessary enrichments | orientation, selection criterion, contact |
| Probe | action intended to produce a discriminating readout | channel/contact, observability, readout rule |
| Signal | available readout | observability and channel |
| Evidence | signal interpreted relative to a claim or frame | claim, interpretation, warrant/judgment |
| Analogy | typed correspondence or transport followed by preservation and rupture tests | correspondence, typing, preservation criterion |
| Schema | stabilized types, relations, constraints, and permitted realizations | formation rules, satisfaction/realization, composition |
| Instance | realization satisfying a schema or constraint set | carrier, realization map/relation, satisfaction judgment |
| Reframing | transformation of the distinctions and relations organizing a local problem | source frame, target frame, relevance criterion |

### From emergent mismatch to represented residue

**Working distinction.** A rupture or mismatch is a situated occurrence: an expectation of
closure, preservation, composition, or adequacy meets a relevant difference. It is *emergent* only
in the stricter case where parts satisfy their local obligations and the failure becomes visible
only through interaction or at another level. A residue is a representation derived after that
occurrence has been read, compared, judged, and typed. Derivability as a representation therefore
does not exclude emergence as an occurrence, and not every residue is emergent.

This preserves adjacent but non-identical roles:

```text
mismatch/rupture -> readout/signal -> interpreted evidence -> witness -> represented residue
                                                               -> obstruction, if it blocks a specified construction
```

A witness establishes a particular judgment; evidence may support without establishing it. A
residue records what did not close; it is not automatically the event, signal, evidence, or
witness from which it was formed.

Residual descriptions should use multiple axes rather than exclusive species:

- **locus:** internal; transport/transformation; composition/globalization; contact with ground;
- **recursive order:** ordinary; reflexive.

"Internal" means an invariant fails without an external map; "transformation" means preservation
fails under a map; "composition/globalization" means locally admissible parts or interfaces fail
jointly; "contact" means prediction or expectation diverges from a readout. "Reflexive" modifies
any locus when the object includes the representing or evaluating mechanism itself. Multiple
labels are allowed when mechanisms coexist.

### A first operational model in `Set`

Let `X` be a declared carrier or observable population, `R: X -> S` a schema/representation, and
`L: X -> Y` the readout required by one fixed task or lens. Taking `S = im(R)`, `R` is sufficient
for `L` exactly when there is a function `L_bar: S -> Y` such that:

```text
L = L_bar o R
```

Equivalently, `L` must be constant on every fiber of `R`. A pair `x, y` with
`R(x) = R(y)` but `L(x) != L(y)` is a witness that this representation is not sufficient for that
`L`: it collapsed a distinction the declared readout needs. The pair becomes a represented
residue only after an expectation, relevance criterion, contact/readout, and judgment interpret
it as such.

This is deliberately a model in `Set`, not a general categorical theorem. Using all of `S` rather
than `im(R)`, stochastic or approximate lenses, multiple lenses, empirical populations, or richer
categories adds conditions. Every application must therefore declare at least the task, lens or
family of lenses, population/cases, obligation to preserve, tolerance or metric, risk, and horizon.

The fiber `R^-1(s)` is an admissible space of realizations only when `X`, `R`, and the schema's
constraints have been defined that way. Multiplicity in a fiber expresses underdetermination or
latent freedom; generativity additionally requires operations or rules that construct, sample, or
transform realizations. Indistinguishability under `R` is not automatically a symmetry in a
stronger structural sense.

**Hypothesis.** Structural freedom may be a common condition behind both generativity and some
residues. Freedom calibrated to the relevant equivalences permits diverse realizations while
preserving what the task needs. Freedom that crosses a distinction exposed by a finer lens *may*
produce residue. This is not the only source of residue: even a deterministic translation can
lose relevant information.

Composition, recursion, order, lens enrichment, local-global passage, and reflexivity can expose
previously hidden differences. Diagonalization belongs only to the special reflexive regime in
which the language can represent a sufficiently rich family of transformations and apply
representations to themselves. Any use of Lawvere-style fixed-point results requires a later
technical investigation with its hypotheses stated precisely; interpreting a fixed point as
"zero residue" is at most a task-relative candidate reading.

### Diagnostic flow, not an enrichment ratchet

The tempting sequence `kernel -> domain -> residue -> enrichment` is too linear. A safer working
flow is:

```text
kernel + ground + contact (+ enrichments)
    -> application/probe
    -> situated mismatch
    -> represented and typed residue
    -> diagnosis
    -> {repair probe/readout; revise expectation/lens; change boundary;
        repair interface; enrich; de-enrich; accept uncertainty; abstain/escalate}
```

A mismatch may result from insufficient language, a poor probe or lens, false expectation, noise,
drift, a bad boundary, or incompatible composition. It does not select its own remedy. Enrichment
may also be justified prospectively by known risk, safety, norm, or omitted mechanism before a
residue occurs. Conversely, structure should be removed when it contributes no exclusive
discriminability or preservation across declared probes/cases, removal violates no risk or norm,
and the reversible removal is retested.

## Live transversal-property candidates

These candidates were present in the source inquiry and remain deliberately unratified:

| Candidate | Question it raises |
|---|---|
| Compositionality | Can larger structures be formed from smaller ones under controlled rules? |
| Preservation | What remains invariant under a stated transformation? |
| Fidelity | Does a transport preserve or reflect the distinctions and relations it claims to carry? |
| Invariance | Which features remain unchanged, and is this distinct from or subordinate to preservation? |
| Symmetry/equivalence | Which differences may be ignored relative to a structure and task? |
| Discriminability | Which differences can a lens or family of probes detect? |
| Recoverability | What can be reconstructed after transport, abstraction, or compression? |
| Minimality | What is the least structure sufficient for a bounded task? |
| Generativity | Which coherent realizations remain possible under constraints? |
| Robustness | What survives perturbation, enrichment, scale, or context change? |
| Locality | Which judgments and operations depend only on bounded context, and which require wider structure? |
| Globalizability | When do locally compatible structures admit a joint realization? |
| Reflexivity | To what extent can the language represent and operate on itself? |
| Temporality/path dependence | Which results depend on order, state, and traversed history? |

The list is an inventory of questions, not proof that every item is a property, independent axis,
or universal feature of one grammar.

## Proposed recurring motifs

The source inquiry also proposed recurring motifs. They are neither mandatory workflows nor
derived constructs:

- **discovery:** candidate structure + contact -> probe -> signal/evidence -> situated mismatch ->
  represented residue -> diagnosis -> justified response;
- **analogy:** transport -> explore -> tension -> delimit -> abstract;
- **composition:** decompose -> establish interfaces/compatibility -> compose -> test -> inspect
  residue;
- **generation:** schema -> degrees of freedom -> instantiate -> select/test -> refine;
- **reframing:** frame -> anomaly or new lens -> transform distinctions -> new frame;
- **local-global:** local conditions -> compatibility -> attempted globalization -> witness or
  obstruction;
- **reflexive:** represent -> represent the representation mechanism -> self-apply -> fixed point
  or limit -> revise.

**Open question.** These sequences may be explanatory projections over richer activity rather than
stable motifs. Their value must be tested by whether they improve reconstruction or decision, not
by how many concepts they accommodate.

## Heuristics under investigation

The earlier notes called the following statements "laws". That name is not warranted. They are
conditional heuristics whose domains, costs, exceptions, and falsifiers remain to be specified.

### Relevant compression

Compress only relative to an orienter and an explicit preservation criterion. "Collapse as much
as possible" is undefined until an ordering or objective function is supplied, and it is unsafe
when future uses or irreversible harms are not bounded.

### Useful composition

Connect structures through valid interfaces and state what the composition preserves. Compression
or equivalence may enable reuse, but neither is a universal precondition of composition.

### Residue-guided refinement

Prefer added distinctions when an observable mismatch shows that the current representation is
insufficient. This is a cost-control heuristic, not a rule to wait for failure in preventive,
safety-critical, or irreversible contexts.

Residue guides diagnosis rather than dictating enrichment. The smallest justified response may
instead repair a probe, revise an expectation or lens, move a boundary, repair an interface,
remove structure, accept bounded uncertainty, or abstain. Prospective obligations based on risk,
safety, norm, or known omitted mechanisms may justify enrichment before any observed residue.

## Predictive investigation - accepted negative result

**Research question.** Under what conditions, if any, can the provisional grammar anticipate
distinctions, ruptures, residues, useful probes, or structural consequences before the relevant
observation, in a way distinguishable from retrospective reinterpretation and simpler
alternatives?

**Accepted research result: `confirmed-kill early-stop`.** No candidate was both witnessed and
definitionally sound. The grammar is therefore, in its current state, an **integrating and
heuristic language, not an incremental predictive theory**. This result narrows the status of the
claims; it does not erase the grammar's editorial or investigative value.

The result is grounded in three durable artifacts:

- [initial definitions](research/predictive-epistemic-grammar/research-initial-definitions.md),
  SHA-256 `a49e355fcacf6495cbba3664810a3ac975470f28d4a9fc7efa088a123608ace6`;
- [integral research returns](research/predictive-epistemic-grammar/research.md), SHA-256
  `ca8d7b48b4fa682b3b04d2067ee013371237107877db9efcb1fd1979460692a6`;
- [accepted findings](research/predictive-epistemic-grammar/findings.md), SHA-256
  `a2e289cedc7e29b55d9489eb3f4f54a600b736c9f3e390ae23d7d61c66737e2d`.

The mechanisms remain reusable as `build-from-owned`, with explicit attribution to their existing
owners. They do not establish novelty or predictive power merely by being connected through the
grammar.

| Candidate family | Why it did not survive | Relevant owners / use-mode |
|---|---|---|
| Residual-profile-guided probe selection | Definitionally distinct, but `no-witness` under information parity | Bayesian experimental design; active learning; Blackwell comparison; restricted reopening only |
| Enrichment / expressivity discriminator | Witnessed the familiar phenomenon of forgotten structure, but supplied no independent rule for choosing the enrichment | reduct/expansion; forgetful structure; invariants; definability; ablation |
| Compositional or local-global failure | Witnessed local adequacy with global failure, but only renamed the problem already expressed by the owners | assume-guarantee; CSP; compositional verification; sheaf obstructions; system dynamics |
| Analogy rupture | Witnessed a preservation failure, but added no rule beyond declared mappings and metamorphic obligations | structure-mapping; metamorphic/property testing |
| Minimality-generativity-residuality frontier | Had no frozen witness and reduced to a familiar complexity-loss trade-off | MDL; rate-distortion; information bottleneck; Pareto/bias-variance |
| Prospective enrichment by risk | Witnessed a temporal separation, but duplicated ordinary prospective risk analysis | FMEA; hazard analysis; causal risk assessment |
| Residual diagnosis and repair class | Witnessed loss under a transformation, but supplied no transportable residual-to-cause-to-repair map | differential diagnosis; root-cause analysis; fault trees; ablation |
| Reflexive limit / diagonalization | Had no system satisfying the required hypotheses and only restated classical fixed-point limits | Lawvere; Goedel; Turing; applicable fixed-point schemas |
| Prediction ledger | Survived only as methodological control; preregistration does not itself confer predictive power | preregistration; Registered Reports; the repository's frozen criterion machinery |

**Central typed negative.** Let `D` contain the same frozen hypotheses, information, admissible
probes, costs, and decision budget available to the baseline, and let `rho(D)` be the residual
profile. If `rho` is derivable from `D`, every policy `pi(D, rho(D))` can be reproduced by a policy
`pi'(D)`; if it is not derivable, the treatment received additional information and the comparison
does not isolate the grammar. The current probe candidate therefore cannot demonstrate incremental
advantage under information parity.

**Only legitimate reopening.** Freeze an explicit computational, representational, or sampling
constraint under which `rho` is an operational compression of `D`; give treatment and baseline
the same raw inputs, hypotheses, admissible probes, costs, and budget; then require a replicable
gain that disappears when `rho` is ablated. Renaming a killed candidate or relaxing parity is not
a reopening.

**Editorial boundary.** This accepted negative belongs to the non-ratified notebook. It promotes
no claim to *Entre Sistemas e Categorias* v0.2 and authorizes no PDF or builder change.

## What remains unestablished

- whether there is one grammar or a family of task-relative grammars;
- whether the classificatory perspectives are independent, dependent, or partly redundant;
- whether intention is a primitive, an external index, or a governed structure;
- whether distinction can be primitive without a domain and discrimination criterion;
- whether analogy is one transport operation, a workflow, or a family of operations and
  judgments;
- whether residues are necessarily persistent and typed;
- whether compression versus distinction is the central tension or one tension among several;
- whether the candidate kernel is expressive, minimal, independent, or operationally useful;
- whether kernel, ground, contact, and enrichments can be specified without circular dependencies;
- whether a useful partial order of sufficiency exists for a task, or only incomparable tradeoffs;
- which conditions license adding or removing a particular enrichment;
- which uses of category theory are formal constructions and which remain heuristic analogies;
- whether the project's history supports the claimed epistemological continuity from June onward.

The historical claim requires a separate evidence table of date, artifact, quotation, and allowed
inference. Conversation memory alone is not sufficient evidence.

## Smallest discriminating investigations

These are research questions, not an implementation plan.

1. **Dependency test.** Can the kernel be expressed without importing its own proposed derivatives
   as undeclared prerequisites?
2. **Reconstruction test.** Can lens, probe, analogy, schema, residue, and reframing be reconstructed
   with explicit formation and judgment rules?
3. **Counterexample test.** Which first important phenomenon - likely agency, normativity,
   temporality, evidence, or reflexivity - cannot be expressed by the kernel?
4. **Operational test.** Does using the grammar change a real decision, probe, or revision compared
   with an ordinary analysis of the same case?
5. **Register/order test.** Is a meta-level case better explained as a register change or as an
   increase in recursive order?
6. **Historical test.** Which repository artifacts actually establish continuity of the
   epistemological framing, and what weaker history survives if some do not?
7. **Contact test.** Hold a representation fixed and vary the readout/contact; if residue judgments
   change, contact is indispensable and cannot remain implicit.
8. **Relation-reduction test.** Represent static, symmetric, and n-ary relations using only
   transformations; any extra carriers, products, truth values, spans, direction, or typing count
   as imported structure.
9. **Prospective-risk test.** Find an irreversible case with known risk and no prior mismatch; if
   enrichment is still required, a strictly residue-reactive principle fails.
10. **Residue-classification test.** Independently label cases by locus and recursive order; low
    agreement or systematic multilabel ambiguity defeats a supposedly discriminating taxonomy.
11. **De-enrichment test.** Remove one enrichment and repeat the retained probes/cases; if all
    declared judgments and obligations survive within tolerance, the prior structure was not
    minimal for that scope.
12. **Factorization test.** Construct `x, y` with `R(x) = R(y)` and run the declared lenses; any
    `L(x) != L(y)` refutes sufficiency of the compression for that lens.
13. **Compositional-emergence test.** Verify local parts and interfaces before composing; if the
    failure was already internal to a part, it is not evidence of compositional emergence.

## Editorial separation

The next publication-oriented text should contain the argument, examples, and only the minimum
vocabulary needed by a reader. This notebook should retain the taxonomic alternatives,
dependencies, counterexamples, and failed names. Editorial clarity must not be purchased by
erasing epistemic uncertainty.

The opening figure may remain a compact map. A detailed typing table, if eventually published,
belongs in a later chapter or exploratory appendix and must preserve status labels.

## Promotion conditions

This notebook may feed a different artifact only when that artifact earns its own contract:

- **research:** one discriminating question, bounded sources or cases, method, evidence standard,
  and explicit output;
- **discovery:** a verified problem, baseline, scope, stable owner handle, and downstream design
  boundary;
- **essay:** a sustained thesis with evidence and a deliberate publication voice;
- **hypothesis node:** one atomic falsifiable claim with a collapse test;
- **Plan:** a named route toward an outcome, with lifecycle, authority search, and stopping gates.

Promotion copies or derives only the supported claims. It does not promote the notebook wholesale.

## Source basis and limitations

Repository precedents consulted:

- [`research-initial-definitions.md`](../../../research/agent-language-mathematical-formalization/research-initial-definitions.md)
  - confirms that carriers, relation kinds, composition, judgments, and the minimal falsifier set
    remain open;
- [`SEED.md`](../../../research/meta-ontology/SEED.md)
  - demonstrates the repository's "exploration, not a decision" and collapse-test discipline;
- [`essay.md`](../../../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md)
  - supplies the proposal-only work-context view and its explicit deferral of ontology terms;
- [`docs/temps`](../README.md)
  - owns this notebook's non-ratified status.

Three retained conversation attachments supplied immediate conceptual material. Some contain
localized corrupted character sequences; all remain non-durable conversation provenance, and
their historical or mathematical claims were not independently sourced. An earlier kernel note
discussed in the conversation is no longer present at its attachment path; its surviving claims
enter here only through the bounded review handoffs and are not assigned a fabricated source hash.
This notebook preserves the current argument while keeping those limits visible.

| Source | SHA-256 | Captured | Supports | Limitation |
|---|---|---|---|---|
| `attachment:4b4011de-f2e1-4e37-926a-9b8535feed2c/pasted-text.txt` | `2aed70ec0096bdf83a670281d891bf074e96e90eb74f158d07df548cf3437828` | 2026-08-11 | epistemological continuity claim; first typing separation | conversation attachment; historical evidence not cited |
| `attachment:c0cd6f7c-7bdc-4ace-a2e2-12d81afdcddb/pasted-text.txt` | `9c133a44ef3ce16359190b0dc105eae88f5987e71fc4ca24fae6a16c43a094a2` | 2026-08-11 | expanded typing map, registers, recursion, kernel, properties, motifs | localized corrupted sequences; hypotheses not independently tested |
| `attachment:012248bd-b397-408a-a5bc-af2c732e8473/pasted-text.txt` | `4bd7f135690e71746c6765ce467a781523af6917b038bf68d8d1297d681e0864` | 2026-08-11 | freedom, generativity, residuality, `Set` factorization, fibers, reflexive regime | localized corrupted sequences; categorical and fixed-point claims require separate technical verification |
| external source PDF `entre_sistemas_e_categorias.pdf` | `68fcd25046e1623022d5bd36d92e9864d1dcd6ae79f6caf18bff8de20c9bbe89` | 2026-08-11 | editorial baseline | external `Downloads` path; no editable source found |
| repository revised baseline PDF linked above | `d29e78998a12697b2fdcdebfab598439cca1a096251b069d65ac134446f8ecd8` | 2026-08-11 | immutable v0.2 patch input | PDF snapshot, not a full editable authoring model |
| repository v0.2 PDF linked above | `e66d5a82db2adcbeaed891f410661696daa2f8d6b75a7c40b0c71446196a25f5` | 2026-08-11 | current rendered v0.2 release | semantic-visual patch output; explicitly untagged; no full Writer/ODT source |
| [`research-initial-definitions.md`](research/predictive-epistemic-grammar/research-initial-definitions.md) | `a49e355fcacf6495cbba3664810a3ac975470f28d4a9fc7efa088a123608ace6` | 2026-08-11 | predictive research question, evidence baseline, and constraints | initial framing; not a research outcome |
| [`research.md`](research/predictive-epistemic-grammar/research.md) | `ca8d7b48b4fa682b3b04d2067ee013371237107877db9efcb1fd1979460692a6` | 2026-08-11 | integral returns on candidates, owners, non-vacuity, and soundness | bounded precedent search; no novelty certification |
| [`findings.md`](research/predictive-epistemic-grammar/findings.md) | `a2e289cedc7e29b55d9489eb3f4f54a600b736c9f3e390ae23d7d61c66737e2d` | 2026-08-11 | accepted `confirmed-kill` and typed negatives | supports current negative result, not impossibility in every future formulation |

## Revision notes

### 2026-08-11 - predictive investigation accepted negative

- Recorded the accepted `confirmed-kill early-stop`: no candidate was both witnessed and
  definitionally sound.
- Classified the current grammar as integrating and heuristic rather than incrementally predictive.
- Preserved the nine candidate-family failures, their owners, the information-parity negative, and
  the single restricted reopening condition without promoting claims to the PDF.

### 2026-08-11 - v0.2 same-text publication revision

- Published the 64-page v0.2 artifact with SHA-256
  `e66d5a82db2adcbeaed891f410661696daa2f8d6b75a7c40b0c71446196a25f5`.
- Preserved the baseline text while adding the approved editorial material: enriched opening boxes,
  chapter 17, the provisional kernel and residue distinctions, attribution, CyberAlchemy marks, and
  the warmer paper field.
- Corrected the opening terminology to *tradições*, completed the outline destinations, and repaired
  the glossary presentation without ratifying the kernel's minimality or sufficiency.
- Recorded the reproducible PyMuPDF patch pipeline with a pinned input hash and atomic publication.
  Its guarantee is semantic-visual rather than byte-for-byte identity; PDF trailer `/ID` values may
  vary between equivalent builds.
- Declared the release honestly untagged. A tagged accessible edition remains dependent on a full
  Writer/ODT-style source reconstruction.

### 2026-08-11 - kernel, contact, and residuality revision

- Reframed the three traditions as repertoires used to investigate a possible underlying grammar.
- Added the strong but unratified `kernel / ground / contact / enrichments` hypothesis and a
  minimal contact/readout contract.
- Preserved relation and transformation as an unresolved pair rather than reducing one to the
  other.
- Separated emergent mismatch from represented residue, and evidence from a judgment-establishing
  witness.
- Added the multiaxial residue labels, the bounded factorization model in `Set`, and the distinction
  between fibers, latent freedom, and actual generative operations.
- Replaced the enrichment ratchet with a diagnostic branch that includes repair, de-enrichment,
  prospective prevention, uncertainty, and abstention.
- Added falsifiers and the new attachment provenance without ratifying minimality or formal claims.

### 2026-08-11 - initial notebook

- Preserved the editorial origin of the inquiry.
- Separated composition, compatibility, equivalence, and compression.
- Converted the proposed ontology and laws into a candidate typing map, kernel hypothesis, and
  conditional heuristics.
- Recorded circularities, competing classifications, and smallest discriminating investigations.
- Preserved the live transversal-property candidates and recurring motifs without promoting them.
- Added the exact page-1 editorial handoff and non-durable source hashes.
