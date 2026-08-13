# KF-L1C-E2 — domainspec conceptual genealogy and formal-containment audit

## Decision and evidence boundary

The repository does **not** contain one proved account of knowledge formation. It contains a changing family of typed mathematical models, repo-local interpretations, proposed experiments, and explicit demotions. The most defensible native organization is not a sequence but a set of coupled distinctions:

1. schema/instance representation and its failures;
2. probe/readout/reconstruction and their non-equivalence;
3. structural residue versus its shadows;
4. observer-relative choice versus formally supplied data;
5. conservative learning versus probe-policy change;
6. reflection/promotion versus residue-derived repair;
7. mathematical construction versus real-process or epistemic interpretation.

This return is anchored to the fixed launch snapshot `main@2a7a5aecb2e3b06ca985f8f15fb7bb75fd0ea4f3`. That commit was also `HEAD` when inspected. The working tree had substantial pre-existing dirtiness. Current-only untracked artifacts are recorded separately and are not used as evidence of snapshot completion.

**Dispatch decision:** `complete-with-material-dissent; needs-review`.

## Native problem map

| Native problem | Repository question | Boundary that survives inspection | Claim type |
|---|---|---|---|
| Representation | Can a source-side object or schema fully represent behavior after translation? | Unrestricted representability fails; representation and preservation must be scoped to a functor, instance, and criterion. | proved + interpreted |
| Lens | What distinctions does a chosen theory/readout make available? | A “scientific lens” is a governing research hypothesis and task-relative discipline, not a constructed category of lenses or an empirically confirmed cycle. | interpreted + proposed |
| Probe | What family of tests separates, detects, or reconstructs? | Representables separate; reconstruction requires stronger density/full-faithfulness hypotheses; probe count alone is not reconstruction. | proved |
| Residue | What failed to survive or be reconstructed? | Structural residue is the functor `noise`; unit defects, entropy, cost, cardinality, and complements are scoped instances/readouts, not definitions. | implemented + proved + policy |
| Observer | Where does choice enter? | Lean types functors/register tags and narrow threshold separations; the choice, purpose, phenomenal status, and adequacy of an observer remain outside the theorem. | implemented + interpreted |
| Learning | What counts as a knowledge-changing step? | Two incompatible local meanings coexist: conservative morphism over a fixed theory and change of next-probe policy. Neither is proved to model empirical learning. | implemented + proved + interpreted |
| Reflection | How are failures promoted to a richer level? | The tower proves ladder/persistence facts for supplied or fixed carriers; it does not derive carrier content or justify ascent from residue alone. | proved + interpreted + demoted |
| Knowledge | What object is knowledge? | `Knowledge T` is explicitly a stipulation: an object over `T` (held schema plus encoding). Other “knowledge” files reuse thermodynamic, VC, or congruence models under stated analogical ceilings. | implemented + interpreted |

The map is native to the repository because its canonical policy already separates structural dock, component, readout, probe, reconstruction, and coverage. It should not be flattened into an ontological or psychological stage model.

## Repository protocol record

### Snapshot and mutation discipline

- `C:/Users/victo/cyberalchemy-orchestrator/research/knowledge-formation/research/dispatch-state.md`, heading **Repository baselines**, records `domainspec-lean-formalization`, branch `main`, commit `2a7a5aec…`, and 53 dirty entries at capture. It says dirty-tree presence is not evidence of authorship, authority, or completion. **Type: implemented protocol.**
- `AGENTS.md`, headings **MANDATORY FIRST STEP — Stop-and-Question Triggers**, **Subset rule (claim ≤ proof)**, and Route 3, requires claim demotion, owner/precedent labeling, no silent reversal of audits, and current-tree verification of registers. **Type: implemented repository policy.**
- `.agents/skills/research/SKILL.md`, headings **Purpose**, **Standing rules**, and **Output shape**, treats ownership as attribution rather than a kill and requires role-separated evidence, dissent, and typed outcomes. **Type: implemented research protocol.**
- No source-repository file was edited. Only this return and its R12 record were created.

### Search protocol

1. Verified `HEAD`, the launch commit object, and the dirty tree.
2. Used `git grep`, `git ls-tree`, and `git show <commit>:<path>` across tracked Markdown, Lean, YAML, and text for `knowledge`, `lens`, `probe`, `representation`, `residue`, `observer`, `learning`, and `reflection`.
3. Used path histories (`git log <commit> -- <path>`) to establish appearance and revision dates.
4. Read root policy/registers, conceptual histories, audit findings, canonical ontology, and relevant Lean headers/declarations.
5. Checked relevant working-tree-only paths and kept them outside the fixed-snapshot conclusions.

### Claim typing used here

- **implemented** — a definition, interface, file-level policy, or construction exists;
- **proved** — a named Lean theorem establishes the stated mathematical proposition (not its empirical gloss);
- **interpreted** — prose assigns epistemic, scientific, or philosophical meaning to formal structure;
- **proposed** — a hypothesis, experiment, candidate interface, or research target;
- **aspirational** — program direction without a closed construction or witness;
- **retracted/stale** — an audit demoted it, a later artifact contradicts its status claim, or current-tree verification makes the register outdated.

## Genealogy: how the vocabulary arose and changed

### 1. Translation and representation came before “knowledge”

`PROJECT-HISTORY.md`, heading **How We Got Here**, begins with the practical mismatch between a domain, specification, code, and runtime: compilation can succeed while failing to preserve the domain. Under **The First Turn: Prove Before Believing**, `Δ` is demoted from an entire stochastic generation process to a compilation contract. Under **M6, Or The Day The Bridge Broke**, the four-object counterexample forces schema residue and instance residue apart. **Evidence:** the narrative says the schema was clean while the Lan unit invented witnesses. **Type: interpreted history anchored to proved counterexample.**

`lean-formalization/M6Counter.lean`, declaration `M6Strong` and the file’s counterexample construction, gives the formal witness: faithful and object-injective schema behavior does not force the relevant Lan-unit isomorphism. `lean-formalization/M2Counter.lean`, theorem `M2_unrestricted_false`, separately proves that `(F.op ⋙ yoneda.obj b)` need not be representable. **Type: proved.**

This is the first durable representation lesson: the repository cannot treat a representation as a transparent copy. “Representable,” “faithful,” “full,” “unit isomorphism,” and “recoverable” become separate predicates.

### 2. Residue moved from metaphor to a typed, then partitioned, object

`PROJECT-HISTORY.md`, headings **Fully Faithful Became The Threshold** and **Residue Stopped Being One Word**, records two corrections. First, “fractal” becomes subordinate to the owned technical notion of full faithfulness. Second, collapse of distinctions (`Residue_FF`) is separated from objects outside an essential image (`Residue_EssSurj`). **Type: interpreted genealogy.**

`GLOSSARY.md`, heading **Residue**, defines typed residue as evidence classified by the failed translation and explicitly marks schema residue as prospective when the required right adjoint is unavailable. `RESIDUE-ONTOLOGY.md`, headings **The partition** and **Exact terminology**, later fixes canonical policy: structural residue is `noise : Schemaᵒᵖ ⥤ C`; `noiseObj S` is its component; `noise_anti` is functor action; unit defects, entropy, cost, and cardinality require explicit adapters. **Type: implemented normative policy, not theorem.**

`lean-formalization/FunctorialResidueStructure.lean`, structure `FunctorialResidueStructure`, implements that structural dock. `README.md`, heading **The one idea**, correctly says the older `ResidueStructure`/`universal_monotonicity` form is a Set-valued degenerate instance and that the functorial action is the stronger spine. **Type: implemented + proved for the functorial action; interpreted for “one idea.”**

The later count-wall work further changes the program. `BACKLOG.md`, B7 status paragraph under the second morphism-level witness target, says count-beating is dormant as a governing target under the 2026-07-23 scientific-lens frame. `GLOSSARY.md`, declarations **`CountCapped` / `BeatsCount`**, makes both relative to a declared baseline `fib`, task, and scope. **Type: interpreted policy grounded in implemented predicates.** The question changes from “escape counting absolutely” to “is this readout adequate for the declared task?”

### 3. The reflection tower arose from self-audit, then lost its causal reading

`PROJECT-HISTORY.md`, heading **The Tower Appeared Because The Project Started Looking At Itself**, says research itself leaves residue; a level observes the previous level and promotes what was missing into new vocabulary. `docs/reflection-tower.md`, heading **The problem in human terms**, expresses this as “rules need rules” and “audit needs audit.” Under **What the tower is, in one paragraph**, it analogizes the tower to Lean universes. **Type: interpreted orientation.**

`lean-formalization/ReflectionTower.lean`, heading **Conceptual reading**, explicitly separates its Lean content from that interpretation: Lean records a ladder, not self-application. Its `FreeExtension` interface and `persistence_lemma` are formal; Gödel/Lawvere and Hofstadter readings are conceptual parallels. **Type: implemented + proved; philosophical reading interpreted.**

`lean-formalization/ReflectionTowerAnchored.lean`, structure `AnchoredCarrier`, implements a supplied carrier plus anchor and builds the substantive K-only extension. `lean-formalization/ReflectionTowerFunctorial.lean`, declarations `F`, `Fmap`, `towerF`, and `persistence_F`, supplies a choice-free additive alternative by adjoining a fixed widget. The file labels itself a candidate replacement, not a hot swap, and originally omits a bona fide `Cat ⥤ Cat` functor law package. **Type: implemented + proved within stated scope; proposed migration.**

`lean-formalization/ReflectionTowerPromotion.lean`, heading **The modeling decision** and theorem `promotion_closes_iff_trivial_carrier`, proves a compatibility result for an already supplied carrier. Its header explicitly says it does **not** construct `A` from residue, select carrier content, or type the full `R_n → seed(L_{n+1})` step. **Type: proved mathematical biconditional; interpreted closure reading.**

The reversal is audit-certified in `research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md`, C11: demote `README.md:40` and causal “seeding” language because Lean fixes `Discrete PUnit` or receives `A`; nonemptiness/anchoring does not select content. **Type: retracted/stale narrative, proved formal boundary.**

### 4. The observer entered as a structural position, not as a proved subject

`PROJECT-HISTORY.md`, heading **The Observer Entered Through The Right Door**, says someone chooses the cut, schema, invariant, and residue. `research-philosophy/README.md`, headings **Objective**, **Tese**, and **Escopo explícito**, narrows the observer corpus to the structural positions of choosing schema, applying instance, and naming residue, excluding general philosophy of mind and qualia without a functor. **Type: interpreted research scope.**

`lean-formalization/ObserverAsSchemaChooser.lean`, structures `ObserverRegister` and `ObserverAct`, implements a functor plus register tag. `ObserverRefinement` is only `HEq` of underlying functors. The theorem `fullyFaithful_not_imp_essSurj` gives a one-directional threshold separator; its header refuses full independence and phenomenal claims. **Type: implemented + proved, with explicit interpretive ceiling.**

The same file’s **History (2026-07-13 repo audit)** is direct reversal evidence: it had been an undeclared orphan, had never elaborated, and the original “thresholds are distinct” theorem only showed both predicates inhabited by the same identity functor. The repaired theorem now exhibits one functor satisfying full faithfulness and refuting essential surjectivity. **Type: earlier state retracted/stale; repaired state proved.**

`lean-formalization/ObserverResidueCarrier.lean`, declaration `obstructionCarrier`, packages presheaves whose Lan unit is non-monic. Its header distinguishes this from Blackwell comparison-of-experiments and claims only Set-level packaging plus two boundary facts (`obstructionCarrier_inhabited_bicyclic`, `obstructionCarrier_empty_of_fullyFaithful`). **Type: implemented + proved; “observer” remains a mathematical functor, not a conscious subject.**

`lean-formalization/ObserverAdjunctionRefutation.lean`, heading **Honest outcome: B (not a hard refutation)**, is another correction: the restricted observer family has heterogeneous source categories, so the proposed adjunction is malformed in the attempted domain; it does not prove nonexistence of every possible left adjoint. **Type: proved diagnostic + proposed stronger refutation left open.**

### 5. Probes moved from ad hoc corepresentables to an explicit observation/reconstruction hierarchy

`lean-formalization/Probe.lean`, declaration `opFlip` and its examples, first fixes the corepresentable/hom-out variance. It supplies examples, not an epistemology. **Type: implemented.**

`lean-formalization/ProbeTypology.lean`, heading **Probe typology — build-from-owned**, defines a probe as a functor-of-points test and proves `representables_separate` and `representables_isSeparating`. The header attributes these to Yoneda/Mathlib and refuses novelty. **Type: proved, owner: Yoneda and Mathlib.**

`PROBES.md`, heading **PROBES — inventário preliminar**, is deliberately weaker: a preliminary inventory of where to search and why two surveys hypothesized relevance; it says relevance had not yet been audited. Its convergence list ranges from representables to empirical experiment proposals. **Type: proposed inventory, not validated ontology.**

`lean-formalization/ResidueObservationTheory.lean`, heading **Residue observation theory**, then makes the distinctions explicit:

- `Obs J R` is the complete presheaf of observations;
- `Separating J` is faithfulness of the restricted nerve;
- `Reconstructive J` is full faithfulness;
- `EquivalenceClosed J` adds essential surjectivity;
- `observedResidue R J` composes probes with structural residue;
- `reconstructive_of_isDense` is the owned density theorem.

The header states that its reconstruction full-faithfulness axis and the F11 Lan-unit axis are distinct and no theorem identifies them. **Type: implemented + proved.**

`RESIDUE-ONTOLOGY.md`, heading **The partition**, says the roles are not yet one inhabited Lean pipeline; no concrete restricted `Reconstructive` family has been applied to a declared `noiseObj`, and no inhabited `EquivalenceClosed` instance is present. **Type: aspirational gap, verified register statement.**

### 6. “Lens” widened into a scientific discipline and was then sharply demoted

`README.md`, heading **The one idea**, introduces the current scientific-lens cycle: people propose typed entities/laws; formalization checks consequences; theories guide probes; readouts retain observations; models face the world. The same paragraph explicitly calls this a **governing research hypothesis, not a theorem**. **Type: interpreted/proposed.**

`lean-formalization/ProbeLensAttacks.lean`, heading **Local algebraic attacks for the scientific-lens program**, proves bounded consequences: threshold stability, joint-readout kernel intersection/factorization, and small adaptive-identification results. Its header states that joint retention does not generate theory objects, laws, reconstruction rules, translations, or empirical adequacy. **Type: proved local algebra; scientific interpretation bounded.**

`research/audits/smithe-lens-fibration-observer/research/findings.md`, heading **First Lean target** and its final verdict, demotes “BayesLens factors through `Refines`”: the factoring is owned Blackwell/Markov-category material plus generic antitonicity, and a total-schema version is vacuous. The distinct surviving target is the non-statistical F11/Lan obstruction, explicitly **not a lens**. `others/SMITHE-2024-AUDIT.md`, update note dated 2026-06-02, preserves that demotion. **Type: retracted proposal; build-from-owned alternative.**

`research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md` is the binding reversal:

- C01: joint readouts can improve a fixed task, but “lens composition” is demoted;
- C02: “lens is/carries a category” is tautological or unwitnessed;
- C04: fibration-shaped ingredients exist, but no total category/cartesian lifts;
- C05: horizontal lens composition plus vertical tower is not a supported double structure;
- C09: the scientific-lens cycle remains an interpretive hypothesis, with no preregistered end-to-end losing case;
- C10: observation/residue/score alone do not determine or justify the next probe/schema/task/authority/tower step.

**Type: audit-certified demotions and typed negatives.**

### 7. “Knowledge” arrived in several non-equivalent formalizations

#### 7.1 Knowledge as a social corpus boundary — proposed experiment

`experiments/knowledge-entropy-over-time/proposal.md`, headings **The question**, **Hypothesis**, and **Subset-rule discipline**, operationalizes `known`, `known-unknowns`, and unmeasurable `unknown-unknowns`. `BridgeFFCognitive` is explicitly not built; H1 is conditional; no direction of the ratio is claimed. **Type: proposed experiment.**

`experiments/knowledge-entropy-over-time/prior-art.md`, headings **Headline finding** and **Required amendments**, reverses key framings: Rescher owns the Q-A-Q/expanding-boundary mechanism; Park–Lu–Fortunato undercut the original scalar H0; “expanding island, expanding shore” needs attribution; typed/domain-stratified structure must be preregistered or H1 collapses to categorical relabeling. Phase 2 remains pending. **Type: interpreted literature audit; proposed empirical work.**

#### 7.2 Knowledge as held schema over a theory — explicit stipulation

`lean-formalization/KnowledgeAsFunctor.lean`, heading **The definition, and exactly what kind of object it is**, introduces `Knowledge T` as `Held` plus `encode : Held ⥤ T`. The header repeats: “= knowledge” is a stipulation, not a theorem. Declarations `Knowledge.Sound`, `Knowledge.Complete`, `Knowledge.read`, `Knowledge.Hom`, `Learning`, and `Knowledge.total` give owned mathematical structure. `totalIsTerminal` proves the maximal “total knowledge” object is terminal; the social-colimit reading is explicitly not built. **Type: implemented + proved about the stipulated object; epistemic identification interpreted.**

`distilled-knowledge/knowledge-evolution-typing.md`, entry **2026-07-19 — Knowledge is a slice object**, accurately labels the slice/comma backbone owned by Mac Lane/Spivak and the knowledge gloss as stipulation. It also records the Frame Dilemma: maximal framing is vacuous; partial framing depends on free probe choice. **Type: interpreted synthesis with proved anchors.**

#### 7.3 Learning as conservative morphism versus learning as changed probe policy

In `KnowledgeAsFunctor.lean`, `Learning K K'` abbreviates a morphism of knowers over fixed `T`; theorem `Learning.conservative` says the encoding commutes, interpreted as nothing already known being lost. **Type: implemented + proved for this definition.**

In `lean-formalization/KnowledgeLoop.lean`, structure `KnowledgeLoop` bundles `G`, `observe`, schema-indexed `score`, and update `U`. Definition `learns` says `G (U l a) ≠ G l`; `H2_characterization` is definitional; the two-state witness proves the predicate has positive and negative cases. The header explicitly says this “learns” is orthogonal to the conservative morphism and does not import it. It also says `score` is indexed by residue schema but does not access `noiseObj` or a noise element. **Type: implemented + proved non-vacuity; empirical learning interpretation proposed.**

`lean-formalization/KnowledgeLoopUpdateUnderdetermination.lean`, theorem `same_pre_update_plumbing_opposite_learnsAlong`, holds residue, `G`, observation, and score fixed while varying `U`, obtaining opposite learning results. This is the exact formal obstruction to saying observation/residue determines learning. **Type: proved local underdetermination.**

#### 7.4 Knowledge as reverse thermodynamics, chain persistence, and VC floor

`lean-formalization/KnowledgeFirstLaw.lean`, heading **The conceptual finding**, proves antitone decay of `log |noise|` along a hypothesized refining chain. Its header labels the result count-side, build-from-owned, empirically uncommitted, and imperfectly named: a monotone law is second-law shaped, not physical first-law conservation. **Type: proved conditional mathematics; analogy interpreted.**

`lean-formalization/KnowledgeReverseThermo.lean`, heading **Collapse-test**, uses one congruence order in opposite directions and an `AddCommMonCat` separator. It explicitly refuses a physical “second law of knowledge” and says no real process is modeled by proof. **Type: proved local structural pairing; broader epistemic gloss rejected.**

`lean-formalization/KnowledgeFunctorialChain.lean`, heading **Verdict: OPTION (a)**, proves a count-invisible distinction survives composition, but also proves the intermediate depth adds no new residue: the composite reduces to endpoint action. **Type: proved; any “depth creates knowledge” reading retracted by its own ceiling.**

`lean-formalization/VCKnowledgeFloor.lean`, declarations `K`, `KU`, and theorem `two_pow_KU_le_K`, merely wrap family cardinality and VC dimension. The header says construction, not novelty; no general knowledge semantics follows. **Type: implemented + proved owned combinatorics; knowledge label interpreted.**

## Key findings with exact evidence and claim type

| Finding | Exact anchor | Precise evidence | State |
|---|---|---|---|
| The repo has no universal origin or sequence of knowledge. | `KnowledgeAsFunctor.lean`, **Honest scope**; `KnowledgeLoop.lean`, **Knowledge is a stipulation, not leaned on**; `experiments/knowledge-entropy-over-time/proposal.md`, **Subset-rule discipline** | Each artifact explicitly limits itself to a candidate definition/model/hypothesis; the models use different units (knower over theory, loop state, social corpus). | interpreted |
| Representation failure is constitutive evidence, not merely missing implementation. | `M2Counter.lean#M2_unrestricted_false`; `M6Counter.lean#M6Strong` and counterexample theorems | Unrestricted representability fails; schema-level faithfulness/object injection does not force Lan-unit recovery. | proved |
| Probe separation is weaker than reconstruction, which is weaker than closure. | `ResidueObservationTheory.lean#Separating`, `#Reconstructive`, `#EquivalenceClosed`, `#reconstructive_of_isDense` | The file assigns distinct formal predicates and proves only the stated implications. | implemented/proved |
| Structural residue is not a measurement value or a unit defect by definition. | `RESIDUE-ONTOLOGY.md`, **Exact terminology** and **Claim discipline**; `FunctorialResidueStructure.lean#FunctorialResidueStructure` | Canonical policy fixes `noise` as dock; adapters are required for readouts and scoped instances. | implemented policy |
| Observer-as-conscious-subject is not formalized. | `ObserverAsSchemaChooser.lean`, **What the separation theorem does and does not say**; `research-philosophy/README.md`, **Escopo explícito** | Lean proves only a functor/register threshold separation and refuses phenomenal equivalence; prose keeps conscious choice as a research question. | proved + interpreted gap |
| Learning has two local definitions that are not unified. | `KnowledgeAsFunctor.lean#Learning`; `KnowledgeLoop.lean#learns` and **Knowledge is a stipulation, not leaned on** | Conservative commuting morphism and next-probe inequality are explicitly called orthogonal. | implemented |
| Observation does not determine update. | `KnowledgeLoopUpdateUnderdetermination.lean#same_pre_update_plumbing_opposite_learnsAlong`; lens/reflexivity audit C10 | Same pre-update fields plus different `U` yield opposite outcomes; supplied policy is execution, not justification. | proved/audit-demoted |
| Reflection does not derive the next vocabulary’s content. | `ReflectionTowerPromotion.lean`, **What this does NOT claim**; lens/reflexivity audit C11 | The carrier is fixed/supplied; theorems concern essential surjectivity and nonemptiness, not content selection. | proved boundary; stale prose demoted |
| Scientific-lens support stops at local algebra and a research hypothesis. | `README.md`, scientific-lens paragraph; `ProbeLensAttacks.lean`, file header; lens/reflexivity audit C09 | No preregistered end-to-end case can lose; local theorems do not produce or validate a theory. | proposed + proved local + demoted |
| The repository itself acknowledges citation and registry drift in both directions. | `ROOT-CONTRADICTIONS.md`, **Root cause** and **The drift runs in both directions** | Caveat-lag lets narrative outrun proof; registries also understate or misreport current artifacts. | implemented audit finding |

## Owners and source types

| Content | Owner named by repository | Source type in this corpus | Repository use |
|---|---|---|---|
| Schema/instance and migration | David Spivak; Schultz–Spivak–Vasilakopoulou–Wisnesky | cited categorical database theory | implemented in `SchemaInstance.lean` |
| Representables/separation/density | Yoneda; Isbell/Kelly/Dubuc; Mathlib | owned category theory | probes and reconstruction criteria |
| Slice/comma object and terminality | Mac Lane / standard category theory | owned mathematics | backbone of stipulated `Knowledge T` |
| Fully faithful / essential-surjective thresholds | standard category theory; repo F11 instances | owned mathematics + repo witnesses | reconstruction/coverage separation |
| Comparison of experiments / Bayesian lenses | Blackwell–Sherman–Stein; Fritz; Cho–Jacobs; Smithe/Myers | owned statistical/category theory | explicitly not subsumed by observer residue carrier |
| Active perception and design | Friston; Lindley; MacKay | external theory cited in header | motivation for `KnowledgeLoop`, not theorem ownership of H2 |
| Concept revision | Lakatos | philosophical/historical interpretation | motivation for update/restructuring |
| Behavioral equivalence/finality | van Glabbeek; Rutten | owned process/coalgebra theory | local “stuck” and observation-carrier results |
| Knowledge-boundary growth | Rescher; Gleiser; scientometric sources | literature audit / proposal | owns mechanism or imagery; empirical phase incomplete |
| Reflection/diagonal reading | Lawvere; Gödel/Tarski/Hofstadter as parallels | interpreted philosophical lineage | not formal self-application theorem |
| Repository-specific semantic identifications | Boscaro/Rondelli and repo dispatches | local interpretation/proposal | must remain typed as such |

No owner is inferred where the repository does not name one. The lens/reflexivity audit C03 explicitly records the exact transport owner as unresolved in that bounded pass; this return preserves that status.

## Gaps, inconsistencies, and stale registers

### Formal gaps

1. **No end-to-end knowledge-formation pipeline.** `RESIDUE-ONTOLOGY.md`, **The partition**, says the roles are not one inhabited Lean pipeline. There is no concrete restricted reconstructive probe family applied to a declared residue object and no inhabited equivalence closure. **State: aspirational.**
2. **No observation-to-update justification.** `KnowledgeLoop.score` lacks access to a residue object element, and `KnowledgeLoopUpdateUnderdetermination` proves `U` can reverse the outcome with all pre-update plumbing fixed. **State: proved gap.**
3. **No social knowledge colimit.** `KnowledgeAsFunctor.lean#totalIsTerminal` proves the terminal reading only; the colimit of individual held schemas is explicitly not built. **State: proposed/aspirational.**
4. **No empirical knowledge-entropy result.** The experiment is phase-1 complete with amendments; operationalization/data remain pending. **State: proposed.**
5. **No category/fibration/double-category of project lenses.** Lens/reflexivity audit C02/C04/C05 finds only category-carrying packaging, reindexing ingredients, and separate axes. **State: typed negative/open future construction.**
6. **No residue-derived carrier content.** Promotion theorems consume a carrier. **State: proved limitation.**

### Contradictions and demotions

1. `EPISTEMIC-POSITION.md`, heading **StrangeLoop.lean / C_ω_absorption_refuted**, originally said the repo proves the colimit is “strictly less” than structure. Its inline 2026-07-19 demotion corrects this to one named promotion functor not being an equivalence. **State: retracted/stale inference.**
2. The same file’s **TowerColimit.lean — something exists in the limit** section withdraws an attempted inference that construction-default nonclosure makes colimit existence stipulative; it preserves only the narrower point that the tower is weak evidence for Peircean realism. **State: corrected interpretation.**
3. `ROOT-CONTRADICTIONS.md`, C13, records `ResidueFFfunctor.lean`’s header saying the morphism action had a `sorry` while its body had zero; the real defect was hollow identity action, not a missing proof. **State: stale register.**
4. `ROOT-CONTRADICTIONS.md`, C15, records `OPEN-PROBLEM-LOOP-CLOSURE.md` calling a session unstarted after `CoupledSkewTowerNonEquiv.lean` landed; it also preserves the caveat that the obtained `TraceDescends` instance is vacuous at that pair. **State: stale register with unresolved scope.**
5. `ROOT-CONTRADICTIONS.md`, **The drift runs in both directions**, corrects an earlier audit generalization that drift always inflates: registries can also understate proofs, as with the README’s stale “none of those invariants is in Lean” after `FCAConceptResidue.lean`. **State: retracted audit generalization.**
6. `ObserverAsSchemaChooser.lean`, **History**, corrects a theorem that formerly failed to separate its two thresholds and a file that had never elaborated. **State: repaired formal artifact; earlier claim stale.**

### Current-tree drift outside the fixed snapshot

The following were untracked at inspection and therefore excluded from snapshot conclusions:

- `lean-formalization/PerspectiveMark.lean`, heading **Perspective marks**, adds explicit distinctions among declaration, instantiation, execution, mark, operational influence, and causality, and says it does not define residue.
- `research/discipline-lens-observer-question-2026-08-13/`, including `research-initial-definitions.md` and `research/findings.md`, investigates discipline/lens/observer/question distinctions and preserves earlier lens-composition demotions.
- `research/residue-as-trace-imprint/`, a current-only research folder on mark/residue relations.
- `research/scientific-perspective-mark/`, whose research files distinguish detectable marks, causal attribution, and residue adapters.

These artifacts indicate active conceptual revision after launch, but not fixed-snapshot implementation or proof. **State: current-only/untracked.**

## Tensions and translation failures

### Formal structure ↔ epistemic meaning

`Knowledge T`, `ObserverAct`, `KnowledgeLoop`, and reflection-tower carriers are mathematically valid structures. Their names do not prove that real knowledge, observers, learning, or reflection instantiate them. The files themselves repeatedly say “model-of-math ≠ real-process-obeys-it.” Translation fails when a conditional theorem is narrated as an empirical or phenomenological account.

### Representation ↔ possession

A representable functor has an owned categorical meaning. A person “holding” a theory is stipulated as a functor into it. No theorem bridges representability or slice membership to human possession, understanding, skill, belief, or justification. The free lever `Held/encode` carries the conceptual residue.

### Probe separation ↔ reconstruction

Yoneda probes can separate parallel maps while reconstruction requires full faithfulness/density and closure adds essential surjectivity. A probe family can therefore improve distinctions without generating a theory or warranting that the observed object has been recovered.

### Residue ↔ readout

The repository historically moved among complement, unit defect, entropy, cost, count, carrier, and functor-action readings. `RESIDUE-ONTOLOGY.md` corrects this by making adapters mandatory. Translation fails whenever a scalar or observed mark is called residue merely because it records loss.

### Observer choice ↔ functor data

Formal artifacts can store a chosen functor and prove properties of it. They do not explain who chose it, under what purposes and authority, why its distinctions matter, or whether another observer would adopt it. The philosophical corpus names this residue; Lean does not contain it.

### Learning ↔ preservation

Conservative `Learning` preserves an earlier encoding. H2 learning changes next-probe policy. Discovery/regularization in `distilled-knowledge/knowledge-evolution-typing.md` instead changes schema via failures of Full/EssSurj/Faithful. These may interact, but the repository has not proved them equivalent or sequential.

### Reflection ↔ repair

The tower adds or receives carrier vocabulary and proves persistence/nonclosure. It does not infer a repair policy from an obstruction. Calling promotion “learning from residue” silently inserts a selection and authority mechanism not present in the formal artifact.

## Knowledge-formation coherence test

Treat a repository account as a coherent knowledge-formation account only if it answers all eight questions without defining the answer into the interface:

1. **Unit:** What changes — person, held schema, instance, probe policy, institution, or corpus?
2. **Phenomenon:** Is the change information receipt, distinction gain, skill, belief, understanding, justification, discovery, or retention?
3. **Lens:** Which distinctions/readouts are supplied, by whom, and for which task?
4. **Probe:** What is observed, and does the family merely separate or actually reconstruct?
5. **Residue:** Which structural dock/component is used, and what explicit adapter produces the reported readout?
6. **Update:** What rule changes the state, and is that rule derived, independently justified, or stipulated?
7. **Reflection:** What authorizes a new vocabulary or level, and is carrier content produced or merely supplied?
8. **Warrant:** What proves the mathematical proposition, and what separately warrants the real-process/epistemic interpretation?

**Result on the fixed snapshot:** the repository passes these questions locally in several files because it states its ceilings, but fails them as a single unified formation process. The relevant objects live at different scales and claim types. “Knowledge formation” is therefore a defensible research umbrella, not a currently coherent formal unit. **Type: interpreted audit conclusion from explicit artifact boundaries, not theorem.**

## Strongest conflict with a proof-only account

A proof-only account would retain the conditional mathematics but lose the repository’s central epistemic fact: **the semantic identifications and selection rules are not proved and are often the load-bearing content.**

The sharpest witness is the conjunction of:

- `KnowledgeAsFunctor.lean`, which proves facts about a slice-like structure while declaring “= knowledge” a stipulation;
- `KnowledgeLoopUpdateUnderdetermination.lean`, which proves that identical residue/probe/observation/score plumbing permits opposite learning outcomes through different supplied updates;
- `ReflectionTowerPromotion.lean`, which proves facts about a supplied carrier while refusing any residue-to-content derivation;
- `README.md` and lens/reflexivity audit C09, which keep the scientific-lens cycle at hypothesis status.

If only Lean conclusions are admitted, one cannot recover why the structures are epistemic, which probes matter, how an update is justified, or why a carrier should be added. If the prose is admitted without proof typing, the account inflates. The repository’s actual method is neither proof-only nor prose-first: it is a typed relation between proof, stipulation, interpretation, audit, and open residue.

## Reversal evidence

1. **One bridge → two audits:** M6 breaks the hope that schema discipline guarantees instance fidelity (`PROJECT-HISTORY.md`, **M6, Or The Day The Bridge Broke**; `M6Counter.lean`).
2. **Fractal slogan → owned threshold:** full faithfulness replaces the proprietary “fractal” reading (`PROJECT-HISTORY.md`, **Fully Faithful Became The Threshold**).
3. **One residue → typed partition:** FF loss and EssSurj coverage split (`PROJECT-HISTORY.md`, **Residue Stopped Being One Word**; `RESIDUE-ONTOLOGY.md`).
4. **Absolute count escape → task-relative lens test:** `BeatsCount` becomes baseline-relative, B7 dormant (`GLOSSARY.md`; `BACKLOG.md`).
5. **Tower reifies residue → carrier is supplied:** promotion prose is demoted by `ReflectionTowerPromotion.lean` and audit C11.
6. **Observer threshold “distinct” by coexistence → genuine one-way separator:** `ObserverAsSchemaChooser.lean`, **History** and `fullyFaithful_not_imp_essSurj`.
7. **Bayesian lens as repo contribution → owned re-export:** Smithe audit demotes factoring-through-refinement; F11 obstruction survives separately.
8. **Lens composition/integrated architecture → local fixed-task gain only:** lens/reflexivity audit C01–C05.
9. **Knowledge entropy directional story → conditional typed experiment:** proposal withholds direction; prior-art audit attributes mechanism to Rescher and demands H0 revision.
10. **Knowledge as theorem → explicit stipulation:** `KnowledgeAsFunctor.lean` centralizes and bounds the semantic bet.
11. **Observation causes learning → update underdetermination:** `KnowledgeLoopUpdateUnderdetermination.lean` and audit C10.
12. **Philosophical restatement as proof → marked inference:** `EPISTEMIC-POSITION.md` demotes “strictly less” and weakens its Peircean evidential claim.

## Rejected synthesis move

**Rejected:**

> A lens selects a probe; observation reveals residue; residue determines learning; learning refines representation; reflection promotes the residue into the next schema; repeated cycles form knowledge.

This is attractive but unsupported as a repository synthesis:

- no category or composition law for project lenses is built (audit C02/C05);
- probe separation is not reconstruction (`ResidueObservationTheory`);
- `KnowledgeLoop.score` need not access residue content;
- update is underdetermined with identical pre-update plumbing (`same_pre_update_plumbing_opposite_learnsAlong`);
- conservative learning and changed-probe learning are distinct definitions;
- promotion consumes a fixed/supplied carrier rather than deriving vocabulary content;
- the scientific-lens cycle lacks a losing end-to-end empirical case;
- the “knowledge” identification is stipulated.

The smallest surviving synthesis is non-sequential: **chosen representations enable probes; probes yield task-relative observations; explicit adapters may expose aspects of structural residue; independently justified updates may alter held schemas, instances, or probe policies; formalization checks consequences; audits keep the semantic interpretation from exceeding them.** This is an interpreted map, not a theorem or universal formation order.

## Material dissent fields

### strongest_claim_expected_to_conflict_and_why

The strongest conflict with the sibling proof-boundary position is: **formal containment is not sufficient evidence for the repository’s knowledge account because the semantic identifications, observer choices, task relevance, update laws, and promotion authority are explicitly outside the formal artifacts.** A proof-boundary reader can correctly restrict claims but may incorrectly treat the omitted material as disposable; here it is the conceptual residue that determines what the proofs are about.

### evidence_that_would_reverse_the_position

This position would reverse if the repository supplied one inhabited, non-vacuous, end-to-end construction in which: a declared knowledge object determines a probe family; the family is reconstructive for a named residue object; observation accesses that object through an explicit adapter; a uniquely or contractually justified update follows; the update changes the knowledge object; and a theorem plus preregistered external case connects the mathematical cycle to an empirical knowledge process. No such artifact exists at the fixed snapshot.

### synthesis_move_rejected

Reject the deterministic lens → probe → residue → learning → reflection → knowledge ladder. It collapses distinctions the repository worked to separate and reintroduces precisely the carrier-selection and update-justification claims that its August audit killed.

## References consulted

Primary repository anchors consulted at the fixed snapshot include:

- `AGENTS.md`; `.agents/skills/research/SKILL.md`; `README.md`; `PROJECT-HISTORY.md`; `GLOSSARY.md`; `EPISTEMIC-POSITION.md`; `PROBES.md`; `RESIDUE-ONTOLOGY.md`; `ROOT-CONTRADICTIONS.md`; `WEAK-WITNESSES.md`; `BACKLOG.md`; `OPEN-PROBLEM-LOOP-CLOSURE.md`.
- `docs/reflection-tower.md`; `docs/distilled/reflection-tower/reflection-tower.md`; `distilled-knowledge/knowledge-evolution-typing.md`; `distilled-knowledge/README.md`.
- `experiments/knowledge-entropy-over-time/{README.md,proposal.md,prior-art.md}`.
- `research-philosophy/README.md`; `research/audits/lens-reflexivity-bidirectional-refutation-2026-08-11/research/findings.md`; `research/audits/smithe-lens-fibration-observer/research/findings.md`; `others/SMITHE-2024-AUDIT.md`.
- Lean files cited by declaration throughout: `SchemaInstance`, `M2Counter`, `M6Counter`, `FunctorialResidueStructure`, `Probe`, `ProbeTypology`, `ResidueObservationTheory`, `ObserverAsSchemaChooser`, `ObserverResidueCarrier`, `ObserverAdjunctionRefutation`, `ReflectionTower`, `ReflectionTowerAnchored`, `ReflectionTowerFunctorial`, `ReflectionTowerPromotion`, `KnowledgeAsFunctor`, `KnowledgeFirstLaw`, `KnowledgeReverseThermo`, `KnowledgeFunctorialChain`, `KnowledgeLoop`, `KnowledgeLoopUpdateUnderdetermination`, `VCKnowledgeFloor`, `ProbeLensAttacks`, `CodensityUnitResidue`, and `ObservationResidueCarrier`.

