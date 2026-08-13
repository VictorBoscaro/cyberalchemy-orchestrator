# KF-L1C-E1 — Formal proof boundary in `domainspec-lean-formalization`

## Scope and snapshot

- **Agent / angle:** KF-L1C-E1, Samson Abramsky; machine-checked structure versus conceptual surplus.
- **Launch corpus:** `C:/Users/victo/domainspec-lean-formalization`, branch `main`, commit `2a7a5aecb2e3b06ca985f8f15fb7bb75fd0ea4f3` (HEAD exactly matched at inspection).
- **Dirty-tree boundary:** the launch tree already contained many modified and untracked files. None was changed. The only formal item relevant to this return that is outside the fixed commit is untracked `lean-formalization/PerspectiveMark.lean`, paired with a user modification registering `PerspectiveMark` in `lean-formalization/files/lakefile.toml`; it is reported separately as **current-only**, never blended into snapshot findings.
- **Verification strength:** direct source inspection at the fixed commit/current tree, exact declaration lookup, lake-library registration checks, `sorry`/`axiom` text sweep, and register-to-tree comparison. The selected modules are registered as `lean_lib`s and contain proof bodies; the only `sorry` matches in the selected corpus are historical prose. I did **not** run a new Lean build because the task required repository reading without modification; therefore “proved” below means “present as a Lean theorem with a proof term in the inspected source,” not a new build attestation.
- **Exclusions:** no other knowledge-formation explorer return or R12 record was read; no external-literature search was performed; no essay prose or work/knowledge bridge was drafted.

## Native problem map

The repository does not formalize one process called knowledge formation. It contains several native, only partly connected problems:

1. **Schema/instance typing:** categories as schemas, functors to `Type` as instances, and pullback by precomposition.
2. **Observation and reconstruction:** probes, restricted nerves, faithful/full-faithful thresholds, changing probe interpretations, and explicit non-monic coarse-graining witnesses.
3. **Lens-relative distinction:** deterministic readouts, joint kernels, task-relative factorization, observation budgets, and counterexamples showing that refinement or added probes do not by themselves imply reconstruction or learning.
4. **Residue:** a family of distinct constructions—probability-fibre objects, functorial schema-indexed noise, essential-image complements, merge/gluing surplus, automata minimization kernels, and open obligations. “Residue” is not a single Lean type across the repository.
5. **Reflection/promotion:** free-extension interfaces and two tower constructions; persistence and non-essential-surjectivity are formal, while metatheory, self-reference, and epistemic readings are commentary.
6. **Local/global:** a finite constraint-satisfaction quantifier gap and exact-record manifest gluing, not a general sheaf/descent or social-knowledge theorem.
7. **Provenance/authority:** source records, exact compatibility, lineage non-transmission, materialization, lifecycle obligations, and Myhill–Nerode collapse; these are bounded models, frequently labeled proposal-only or not system-wired.
8. **Epistemic stipulations:** `Knowledge`, `Learning`, “first law of knowledge,” “knowledge loop,” and “thermo leg” are interpretations placed on mathematical structures. The files themselves repeatedly deny that those interpretations are established by Lean.

## Repository protocol record

1. Confirmed branch, commit, and dirty status before substantive reading.
2. Enumerated all `.lean` files, then searched Lean and repository registers for observation, observer, lens, schema, instance, residue, reflection, preservation, local/global, provenance, ledger, lineage, learning, and knowledge.
3. Read the formal cores and their honesty/scope headers, then checked exact declaration lines.
4. Compared claims in `INSTANCE-MAP.md`, `OBJECT-MAP.md`, `README.md`, `PROJECT-HISTORY.md`, `RESIDUE-ONTOLOGY.md`, `STRONG-UNIFICATION-STATUS.md`, and the August 11 audits against the current tree.
5. Kept three evidential levels separate: theorem signature/proof body; in-file interpretation; external or local proposal cited by that interpretation.
6. Treated current-only `PerspectiveMark.lean` as post-snapshot evidence and checked that none of the tracked formal files discussed below differed from the fixed commit.

## Key findings and exact formal evidence

### 1. Schemas and instances are cleanly typed; their epistemic reading is not proved

**Implemented / proved.** `lean-formalization/SchemaInstance.lean` defines:

- `DomainSpec.SchemaInstance.Schema` (line 60): a sigma-packaged small category.
- `DomainSpec.SchemaInstance.Instance` (line 71): a functor from the schema carrier to `Type`.
- `DomainSpec.SchemaInstance.SchemaMorphism` (line 76): a functor between schema carriers.
- `DomainSpec.SchemaInstance.pullback` (line 83), with `pullback_id` (line 90) and `pullback_comp` (line 98).
- `Instance_T` (line 135) and corresponding `pullback_T_id` / `pullback_T_comp`: monad-algebra-valued attribution.

**Owner/source type.** The file explicitly identifies this as the Spivak categorical-database convention and Mathlib category/functor machinery: **owned external mathematics / formal-library implementation**, not a repository discovery.

**Interpreted / stipulated.** `lean-formalization/KnowledgeAsFunctor.lean` defines `DomainSpec.KnowledgeAsFunctor.Knowledge` (line 84) as `Held` plus `encode : Held ⥤ T`, then `Knowledge.Sound` (faithfulness, line 97), `Knowledge.Complete` (fullness, line 101), and `Knowledge.read` (pullback, line 111). It also implements `Knowledge.Hom` (line 122), a category of knowers (`instCategory`, line 148), `Learning := Knowledge.Hom` (line 171), the commuting equation `Learning.conservative` (line 176), `Knowledge.total` (line 186), identity readout `Knowledge.total_read` (line 201), and terminality `totalIsTerminal` (line 212).

The file’s binding qualification is correct and essential: **“knowledge = this functor” is a stipulation**, not a theorem. Likewise `Learning.conservative` proves the equation `transfer ⋙ K'.encode = K.encode`; the gloss “nothing already known is lost” is an interpretation. It does not prove psychological retention, truth, justification, memory, skill, evidence, or social acceptance. `Knowledge.total` also exposes the maximal-frame collapse: soundness/completeness are trivial at `Held = T`, and readout is the identity.

### 2. Observation is formalized as explicit maps and categorical thresholds, not as perception or experience

**Implemented / proved.** `lean-formalization/ResidueObservationTheory.lean` defines:

- `restrictedNerve` (line 39) and `Obs` (line 43).
- `ObjectIsoReflecting` (line 46), `Separating` = faithfulness (line 50), `Reconstructive` = nonempty full-faithfulness (line 53), and `EquivalenceClosed` = reconstruction plus essential surjectivity (line 57).
- `objectIsoReflecting_of_reconstructive` (line 61) and `reconstructive_of_isDense` (line 69).
- `observedResidue` (line 76), `observedNoiseAnti` (line 81), and `observed_not_mono_of_separating` (line 97): a faithful restricted nerve reflects failure of monicity.
- `entropy_readout_not_full` (line 175): the non-injective entropy readout induces a non-full functor between discrete categories.
- `diamond_observedNoiseAnti_not_mono` (line 224): every separating probe family continues to see the diamond refinement map as non-monic.
- A **separate** Lan-unit axis, `LanUnitReconstructive` (line 238) and `f11_fullyFaithful_implies_lanUnitReconstructive` (line 245). No theorem identifies this axis with restricted-nerve reconstruction.

**Owner/source type.** Restricted Yoneda/density and fully-faithful machinery are **owned external mathematics / Mathlib**. The diamond consumers are **repo-local wiring to earlier formal witnesses**. The file expressly denies that cardinality, entropy, cost, or `BeatsCount` defines residue.

**Lens thresholds.** `lean-formalization/ObserverAsSchemaChooser.lean` implements `ObserverRegister` (line 75), `ObserverAct` (line 81), and `ObserverRefinement` (line 95), but this “refinement” is currently just heterogeneous equality of the underlying functor. `fullyFaithful_not_imp_essSurj` (line 144), using `incl01`, proves only one directional separation: fully faithful does not imply essentially surjective. It proves neither full logical independence nor phenomenal equivalence.

### 3. Schema-relative revelation is inhabited, but remains external and relative

`lean-formalization/SchemaIndexedObservation.lean` implements:

- `SchemaProbeEvolution` (line 27), a functor from the residue schema into a functor category.
- `MorphismIndistinguishableAt` (line 33), `MorphismRevealedByRefinement` (line 43), and `ResidueMorphismRevealedByRefinement` (line 64).
- `residueMorphismRevealedByRefinement_of_comp_eq_of_separating` (line 74): if refined probes are separating and two distinct maps are collapsed after `noise_anti`, a revelation witness follows.
- `not_residueMorphismRevealedByRefinement_of_separating_of_mono` (line 90) and `not_morphismRevealedByRefinement_constantEvolution` (line 135): monicity/separating coarse probes or constant probe evolution block the corresponding revelation notions.

`lean-formalization/SchemaIndexedObservationWitness.lean` supplies the finite `MergeResidue` consumer: `mergeProbeEvolution` (line 80), `arm_maps_revealed_by_refinement` (line 163), actual gluing by the residue map `arm_maps_glued_by_noise_anti` (line 172), and structural revelation under constant identity or one-object `Unit` probes (`arm_maps_structurally_revealed_by_refinement`, line 191; `arm_maps_structurally_revealed_by_unit_probe`, line 206).

**Boundary.** These theorems establish relative distinguishability of two maps under stipulated probe families. The file explicitly does not prove that probes are internally expressible by the residue schema, low-information, psychologically available, or reconstructive beyond the displayed faithfulness calculation.

### 4. “Lens” results are factorization and budget results, not a theory of scientific perspective

`lean-formalization/ProbeLensAttacks.lean` proves deterministic statements including `joint_eq_iff`, `countCapped_iff_joint_kernel_eq_left`, `adaptiveTranscript_factorsThrough_observeBoth`, and the finite three-probe separation `ThreeProbeWitness.adaptive_injective` / `no_fixed_pair_injective`. `lean-formalization/ObservationBudget.lean` sharpens this with `adequate_of_jointlyInjective`, the converse `exists_task_not_factorsThrough_iff_not_jointlyInjective`, `QuerySchedule.run_eq_of_probe_eq`, and the concrete `budget_two_adaptive_gap`.

The current source has already demoted an earlier overstatement: its collapse test now says exactly budget `k = n`; it explicitly denies the unrestricted `k ≥ n` claim because `ReadableWithin` uses exact arity. The August 11 claim-audit document preserves the historical finding, but repeating it as a present defect would be stale.

`lean-formalization/TaskProbeFactorizationCollapse.lean` further proves:

- `no_task_relative_residue_of_decoded` (line 69): a decoder rules out task-relative residue.
- `c1_strict_relational_contraction` (line 131) together with `task_not_decoded_by_new_probe` (line 138): removing one residual collision does not entail global task decoding.
- `recipientTask_not_decoded_by_receivingReadout` (line 215): preserving a source invariant on an embedding does not imply recipient-wide task adequacy.

These are the strongest formal checks against treating “better lens” as automatic understanding.

### 5. The repository has multiple incompatible formal surrogates for learning

`lean-formalization/KnowledgeLoop.lean` defines `DomainSpec.KnowledgeLoop` (line 105) with abstract state `L`, observation `Obs`, score `A`, probe index `P`, a functorial residue, `G`, `observe`, schema-indexed `score`, and update `U`. It defines `learns` (line 135) as `G (U l a) ≠ G l`, `step` (line 144), `learnsAlong` (line 149), `stuck` (line 160), and a finite non-vacuity theorem `learns_nonvacuous` (line 221).

This is an **object-level policy-change predicate**. `score` can ignore `noiseObj`; `P` is an arbitrary type with no typed map into the residue category. The current header correctly retracts any stronger corepresentable/Tannaka reconstruction reading as external motivation only.

`lean-formalization/KnowledgeLoopUpdateUnderdetermination.lean` proves that identical pre-update residue, generator, observation, and score can coexist with opposite `learnsAlong` verdicts: `same_pre_update_plumbing` (line 78), `learningLoop_learnsAlong` (line 94), `inertLoop_not_learnsAlong` (line 101), aggregated in `same_pre_update_plumbing_opposite_learnsAlong` (line 131). Thus observation plus residue-indexed scoring does not determine learning; the choice of `U` is load-bearing.

`lean-formalization/ObservedRevisionUnderdetermination.lean` generalizes the same logical obstruction. `ObservedPolicy.fiberwise_compatible` (line 47) proves that a correct deterministic policy must be constant, up to the declared setoid, on observation fibres. The concrete `indistinguishableProblem_not_solvable` (line 116) and positive `separatingProblem_solvable` (line 135) concern fixed-domain functor extensions only, not learning or revision in general.

### 6. Residue has structural content, but its information/knowledge gloss is underdetermined

`lean-formalization/Residue.lean` defines `DomainSpec.Residue.ResidueObject`, entropy `H`, non-negativity, identity collapse, products, and `H_product_eq`. This is a finite probability-fibre object, not the same type as `FunctorialResidueStructure` or essential-image residue.

Two negative results control epistemic translation:

- `lean-formalization/ResidueWiringUnderdetermined.lean`, `H_wiring_underdetermined` (line 81), gives uniform and biased distributions on the same support with distinct entropy. The support alone does not canonically determine the entropy wiring.
- `lean-formalization/TwoFacesDecategorification.lean`, `card_and_H_are_distinct_shadows` (line 96) and `two_faces_decategorification` (line 141), proves within its stated carriers that cardinality and entropy are distinct shadows, entropy is lossy, and reconstruction is not forced. The “knowledge/information faces” wording is an interpretation of these formal non-injectivity and symmetry facts, not a definition of human knowledge.

`lean-formalization/EntropyStructureSplit.lean` similarly formalizes “entropy + structure” only as a kernel/non-factorization split (`beatsCount_countTrues_readPart`, `not_countCapped_countTrues_readPart`), explicitly not as a scalar sum and not at the morphism-level bar.

### 7. Reflection is a categorical extension phenomenon; its epistemic reading is actively delimited

`lean-formalization/ReflectionTower.lean` contains a real interface (`FreeExtension`) but also explicit status distinctions:

- `ResiduePair` is a deferred stub with only `tag : Unit` and no current consumers.
- `FreeExtension.disjointUnion` is a degenerate consistency inhabitant.
- the earlier `WithAnchor` stack is marked superseded by `ReflectionTowerAnchored.lean`.

`lean-formalization/ReflectionTowerPromotion.lean` proves, for an already supplied anchored carrier, `promotion_closes_iff_trivial_carrier` (line 143), `promotion_not_essSurj_iff_nonempty_carrier` (line 160), `residue_not_closable_forces_nontrivial_carrier` (line 169), and `tower_step_seeds_nontrivial_carrier` (line 226). It does **not** construct carrier content from residue; the input carrier is already chosen.

`lean-formalization/ReflectionTowerFunctorial.lean` defines `F` (line 90), `Fmap` (line 96), `towerF` (line 118), `persistence_F` (line 142), `incl_not_essSurj` (line 162), and `towerF_no_finite_closure` (line 181). Despite “endofunctor” prose, it explicitly says no bona-fide `Cat ⥤ Cat` object with on-the-nose `map_id`/`map_comp` is constructed; `F` is a function on objects plus an arrow operation. It is also labeled a candidate replacement, not a hot swap, and lacks the anchored tower’s anchor arrows.

Most decisively, `lean-formalization/TowerResidueDirection.lean` preserves the earlier negative rather than reversing it. `tower_residue_persists` (line 146), `tower_carriers_differ` (line 175), and `tower_is_thermo_leg` (line 201) show a fresh, nonempty, count-shaped essential-image residue on changing carrier types. The file states that reading this as a single-carrier, noise-shrinking knowledge dynamics is ill-typed. “Thermo leg” remains an interpretation of persistence/non-essential-surjectivity, not a physical or cognitive theorem.

### 8. Local/global results are bounded quantifier and exact-record theorems

`lean-formalization/FiniteLocalGlobalConstraintGap.lean` defines local consistency with a separately quantified colouring for each view and joint/global consistency with one shared colouring (`SatisfiesOn`, line 46; `Consistent`, 50; `LocallyConsistent`, 58; `HasGlobalWitness`, 62; `JointlyConsistent`, 66). `punctured_local_global_gap` (line 164) proves all three punctured views are independently satisfiable while the full Boolean two-colouring does not exist. `covered_same_witness_glues` (line 143) and `hasGlobalWitness_iff_full_consistent` (line 153) show that the gap disappears once the same witness is used across a covering family.

This is a finite CSP quantifier swap. The file expressly denies identification with sheaf cohomology, Selmer groups, Kochen–Specker contextuality, or a knowledge model.

In the engineering corpus, `lean-engineer/ContextManifestGluing.lean` gives an independent exact-record analogue: `Compatible` (line 72), `ConflictAt` (line 79), `not_common_extension_of_conflict_at` (line 97), `exists_unique_exact_extension_of_compatible` (line 153), and executable reflection `recompose_eq_some_union_iff_compatible` (line 241). Its header denies runtime, freshness, authority, and provenance-truth semantics. This is useful preservation structure, not epistemology.

### 9. Provenance and authority are represented as stored fields and bounded equivalences, not truth

Three distinct formalizations must not be merged:

1. **Source-record integrity.** `lean-engineer/ContextManifestIntegrity.lean` defines `SourceVersion` with a provenance list (line 42), `SourceVersion.covers` (line 113), and `CoverageAdequate` (line 131). `coverageAdequate_inputA` (line 232) and `not_coverageAdequate_inputWithoutAuthority` (line 237) are finite fixtures. Nonempty stored provenance is checked; provenance truth is outside the model.
2. **Authority lifecycle.** `lean-formalization/AuthorityLifecycleResidue.lean` implements `lifecycleResidue` (line 189) with thin `Set Obligation` noise. `promotion_discharges_residue` (line 211), `residue_empty_iff_projected` (line 220), `blocked_not_dischargeable` (line 251), and `dischargeability_splits` (line 262) prove obligation-set facts on a stipulated status preorder. The phrase “discharges to knowledge” is a local lifecycle reading; Lean proves empty obligations / `projected`, not epistemic knowledge or valid authority.
3. **Operational equivalence and lineage.** `lean-formalization/LedgerEventResidue.lean` defines `ledgerResidue` (line 147), `LedgerClass` as a left-quotient range (line 156), and `ledgerMinimalDFA` (line 160), with `ledgerMinimalDFA_accepts` (line 163). `leftQuotient_collapse` (line 187) and `minKernel_nonempty` (line 285) prove that distinct provenance-carrying prefixes/states can be operationally identified. This is Myhill–Nerode/FCA-owned machinery applied to a toy ledger; the file explicitly labels “provenance = automaton non-minimality” a scope decision and not system wiring.

`lean-engineer/cyberalchemy-orchestrator/agent-language/AgentLanguageLineage.lean` supplies a complementary negative in a proposal model: `lineage_not_implies_disjunction` (line 243) and `lineage_transmits_none_individually` (line 276) show that an ancestry edge alone transmits neither authority, tools, budget, nor evidence; `materialize_provides` (line 439) makes the explicit operation load-bearing. The entire agent-language suite labels itself a **model of a proposed invariant set with no product correspondence or execution authority**. `AgentLanguageCore.wellFormed_record_not_preserves` (line 252) also proves that a complete governance record does not entail the semantic `Preserves` predicate.

`lean-formalization/SourceLedgeredAmalgamationResidue.lean` is only a framework reading of `MergeResidue`: `amalgamation_count_blind` (line 105), `dedup_separates` (line 113), `amalgamation_dedup_beats_source_count` (line 134), and `spine_noise_anti_is_dedup` (line 158). It proves gluing distinctions in a span-colimit model; it explicitly does not prove that a running amalgamation implements that pushout or that source links are truthful.

## Claim-state ledger

| State | Supported examples | What must not be inferred |
|---|---|---|
| **implemented** | Schema/instance API; observation predicates; knowledge-loop fields; lifecycle preorder; manifests; tower constructors | that the implementation corresponds to a real knower, institution, observer, or runtime |
| **proved** | Pullback laws; faithful/full-faithful implications; concrete revelation/gluing witnesses; finite local/global gap; update underdetermination; tower non-closure; left-quotient collapse; lineage non-transmission | phenomenology, causality, truth, justification, social acceptance, empirical adequacy, universal learning laws |
| **interpreted** | functor = knowledge; commuting hom = conservative learning; probe-policy change = learning; persistent residue = thermo; empty obligations = knowledge | that Lean established the interpretation itself |
| **proposed** | cyberAlchemy lifecycle, ledger-event identity, source-ledgered amalgamation, agent-language invariant model | current product correspondence, runtime enforcement, or validated governance semantics |
| **aspirational/open** | internal schema-derived probes; content-sensitive residue→carrier rule; genuine categorical endofunctor version of `F`; non-thin provenance/obligation lifts; general orbit-space reconstruction; empirical/causal perspective validation | that an open seam has a witness or is uniquely highest leverage |
| **retracted/stale** | old observer “two inhabited thresholds” result; reconstruction gloss in old KnowledgeLoop prose; reflection tower as knowledge dynamics; unrestricted `k ≥ n` observation-budget prose; exhaustive instance-register claim | reassertion without checking the current source |

## Register verification and inconsistencies

1. **`INSTANCE-MAP.md` is stale as an exhaustive register.** It is dated 2026-07-15 and claims a 32-row exhaustive map. It contains no occurrences of `AuthorityLifecycleResidue`, `LedgerEventResidue`, `KnowledgeAsFunctor`, or `SchemaIndexedObservation`; those tracked files entered later (2026-07-18, 07-19, and 08-05). The table remains useful for its dated corpus but its current exhaustiveness claim is false.
2. **`OBJECT-MAP.md` is also incomplete for this question.** Its last change is 2026-07-20 and it has no exact entries for `KnowledgeAsFunctor`, `KnowledgeLoop`, `SchemaIndexedObservation`, `FiniteLocalGlobalConstraintGap`, `AuthorityLifecycleResidue`, or `LedgerEventResidue`, although it accurately lists `ReflectionTowerPromotion` as proved. It should not be treated as a current semantic inventory.
3. **Historical audit findings can be stale after fixes.** `research/audits/final-post-fix-claim-review-2026-08-11/review.md` records defects in earlier `KnowledgeLoop`, lakefile, and observation-budget prose. The current source/lakefile at the launch commit already contains the requested demotions: arbitrary `P`, no `noiseObj` access, “two loops yield,” and exact-budget-only wording.
4. **`ReflectionTower.lean` is internally status-layered, not a single live construction.** Its header accurately distinguishes a degenerate interface inhabitant, a superseded early anchored stack, the substantive anchored tower, and a separate choice-free tower. Any register row saying simply “reflection tower proved” loses material implementation differences.
5. **Formal family fragmentation:** `ResidueObject`, `ResidueStructure`, `FunctorialResidueStructure`, essential-image residues, task-relative residues, and prose “residue” are not definitionally unified. Cross-file narratives sometimes use one word across these carriers; no theorem supplies a universal conversion.

## Translation failures

1. **Functor → knower:** `Knowledge` is mathematically coherent but epistemically underconstrained. Faithful/full encodings do not type belief, truth, warrant, salience, embodiment, memory, skill, testimony, or error correction.
2. **Commutation → preservation:** `Learning.conservative` is a commuting triangle. Without a chosen semantics for objects/morphisms and an adequacy relation, “nothing known is lost” is stronger than the theorem.
3. **Probe change → learning:** `KnowledgeLoop.learns` detects a changed next probe, not improved truth, stable capacity, understanding, or warranted revision. The update-underdetermination witness makes the free `U` explicit.
4. **Observation → reconstruction:** faithfulness separates morphisms; full faithfulness reconstructs homs; essential surjectivity covers objects. These are distinct thresholds. The repo correctly proves some implications and counterexamples but no general epistemic equivalence.
5. **More probes → better understanding:** joint injectivity gives task adequacy, but budget and scheduling can still separate methods; removing a collision need not decode a task; preserving a source invariant need not ensure recipient-wide adequacy.
6. **Residue → information/knowledge:** entropy requires a chosen probability wiring; cardinality and entropy have different kernels; structural residue and scalar shadows live in different codomains. No canonical global “information from knowledge” map is forced.
7. **Residue → revision:** neither functorial residue nor observed failure chooses an update. The repository has counterexamples showing observation-fibre collisions and update choice remain decisive.
8. **Reflection → self-knowledge:** the towers prove categorical adjunction/non-closure patterns. They do not implement self-reference, metatheory, or a learner; one current theorem explicitly rejects the noise-shrinking knowledge reading on typing grounds.
9. **Stored provenance → truthful provenance:** all manifest and ledger models can inspect fields, exact equality, and operational futures, but do not establish that records are accurate, authoritative, independent, or socially accepted.
10. **Local witnesses → shared knowledge:** the finite local/global gap is exactly the difference between separate witnesses and one shared witness. It gives no theorem about testimony, consensus, institutional knowledge, or sheaf semantics without additional structure.

## Knowledge-formation coherence test

**Test.** A repository-level account would count as one coherent formal unit only if it supplied typed adapters connecting, on a shared or explicitly transported subject/unit:

1. observation/probe outcome;
2. evidence or residue consumed by an update;
3. revision/learning;
4. preservation and loss across that revision;
5. local-to-global aggregation or reconstruction;
6. provenance/authority conditions under which the result may be called knowledge;
7. non-vacuity witnesses and collapse-tests for every adapter.

**Result: fails as a unified formation process; passes as a constraint atlas.** No inspected declaration composes all seven. The strongest breaks are explicit: `KnowledgeLoop.score` cannot inspect `noiseObj`; update is freely chosen; `KnowledgeAsFunctor.Learning` is a different notion from `KnowledgeLoop.learns`; observation reconstruction has two nonidentified full-faithfulness axes; the reflection tower changes carrier types and is placed away from the knowledge reading; provenance truth and system correspondence are outside the models; local/global results use independently quantified finite witnesses. The formal corpus is therefore evidence for distinctions and non-implications that a future account must preserve, not evidence for a single origin, sequence, subject, or definition of knowledge.

## Material dissent fields

### Strongest claim expected to conflict and why

**Claim:** the conceptual genealogy and unformalized residue are necessary evidence for a knowledge account, so bounding the repository contribution by Lean declarations omits the phenomena that motivated them.

**Response:** that claim is plausible as a research-method statement, but it cannot change the type of the evidence. The formal corpus itself repeatedly labels its epistemic moves as stipulations, candidate models, external motivations, or scope decisions. Conceptual surplus may guide questions; it cannot be reported as a theorem or as confirmation that knowledge forms by these mechanisms. This should conflict directly with any synthesis that treats recurrence of the vocabulary as corroboration.

### Evidence that would reverse this position

A machine-checked, non-vacuous adapter chain would reverse the “constraint atlas only” verdict: an observation whose result is demonstrably consumed from a structural residue; an independently justified update law; a proved preservation/loss statement under that update; a local/global reconstruction theorem on the same typed carrier; and provenance/authority predicates connected to the formal state without assuming the desired conclusion as fields. Empirical or scholarly evidence validating the interpretations could also license a cross-corpus **possible constraint**, but not turn prose into Lean proof.

### Rejected synthesis move

Reject the sequence **schema refinement → more observation → less residue → learning → reflection → promoted knowledge**. Every arrow is either conditional, uses a different carrier/notion, or is refuted as automatic: constant probes cannot reveal merely by schema refinement; more probes can be budget-limited; entropy wiring is free; update is underdetermined; the tower’s knowledge reading is ill-typed; projected status is only empty stipulated obligations. The sequence would be narrative order masquerading as a proved epistemology.

## Current-only post-snapshot note

Untracked `lean-formalization/PerspectiveMark.lean` is not part of commit `2a7a5ae…`. In the current dirty tree it implements `PerspectiveProtocol` (line 39), `RunLedger` (line 70), `IsRecordedExecution` (line 98), `IsRecordedConformingExecution` (line 107), `is_executed_iff_exists_recorded_eq_conforming` (line 128), and `discrepant_recorded_run_witness` (line 463). Its finite fixtures separate declaration, realization, recorded occurrence, equality conformance, predicted mark, observed mark, and operational difference; the header denies causality and any residue adapter. The paired untracked session record claims a successful build, but because this material is outside the fixed launch snapshot and user-owned, it is **current-only provisional evidence**, not a launch-corpus finding.

## Bottom line

The repository’s strongest machine-checked contribution to knowledge formation is negative and architectural: it precisely separates schemas from instances, probes from reconstruction, observation from revision, preservation from adequacy, local witnesses from a shared witness, stored provenance from truth, lineage from transmitted capability, and mathematical models from their epistemic readings. It does not machine-check a general account of how knowledge forms. Any later synthesis should preserve these non-implications and classify cross-corpus relations as constraints, analogies, or non-comparabilities unless a typed adapter and matching warrant are explicitly present.
