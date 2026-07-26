# Category Theory Parallels

Normative candidate definitions for the repository's category-theoretic parallels.

*Unreviewed. Claim ≤ proof: nothing here is a proven result; where the anchor is weak
(memory-level, uncommitted Lean, or our own synthesis) this is labeled inline.*
*Adopts the definitions protocol from `Arcanum/definitions/DEFINITIONS.md` — single source of
truth: each term is defined normatively in exactly ONE place; boundaries do not collide.*

---

<a id="def-orch-001"></a>

## Residue

- **ID:** DEF-ORCH-001
- **Status:** candidate
- **Term + Aliases:** **residue** (*residue*, "what is lost in translation")
- **Scientific/formal voice:** The categorical object that measures what a morphism/translation
  fails to preserve, typed against `FunctorialResidueStructure` — the separation action as a
  functorial action, not as a set of losses. It has two faces decomposed as a sum: **shadow ⊕
  structure** (scalar object-level face ⊕ morphism-level face).
- **Operational interpretation:** When an agent/verb transforms a knowledge artifact
  (schema → instance, merge, coarsening), the residue is *the object* that carries the
  surviving distinction — not the textual report of the loss, but the thing against which
  "beating the count" is even definable.
- **Colloquial voice:** It's what the translation lost, kept as a thing instead of a lament.
- **Boundary:** EXCLUDES the **shadow** (DEF-ORCH-003): the residue is the two-faced object;
  the shadow is *only one* of them (the scalar one). A residue whose only non-trivial face is
  the shadow is *count-capped* and does not beat the count. Residue ≠ the verb that generates
  it (DEF-ORCH-005).
- **Categorical type + anchor:** `structure FunctorialResidueStructure` —
  `lean-formalization/FunctorialResidueStructure.lean:120`; action `separation_is_functor_action` — `:545`.
  Anchor pinned: `domainspec-lean-formalization @ 6edb664` — reported **sorry-free** by source
  inspection + that repo's own audit (`COUNT-WALL.md`, `ROOT-CONTRADICTIONS.md`); **not**
  re-verified against the build gate in this session (`lake build` + `#print axioms` pending).
  **Reading ceiling:** this anchor witnesses residue only at the *separation* bar
  (output-cardinality-visible, as the diamond does), **not** the stronger *invariant-factor* bar;
  the scope + the closing mechanism live once in OBL-E3 sub-3.
- **Related:** DEF-ORCH-002, DEF-ORCH-003, DEF-ORCH-005.

---

<a id="def-orch-002"></a>

## Separation

- **ID:** DEF-ORCH-002
- **Status:** candidate
- **Term + Aliases:** **separation** (*separation*, "to distinguish")
- **Scientific/formal voice:** The primitive: to distinguish two objects. It precedes counting
  — without an individuating signal there is nothing to count; indiscernible = identical.
  Formally, the criterion that separates an action that merely *caps* the count (`CountCapped`)
  from one that *beats* it (`BeatsCount`).
- **Operational interpretation:** Before the orchestrator counts, groups, or scores anything,
  some map had to distinguish two artifacts. Separation is that prior operation; the count is
  derived from it, never the reverse.
- **Colloquial voice:** First you distinguish two things; only then does counting them make
  sense.
- **Boundary:** EXCLUDES counting and the shadow: separation is *prior* — it is the condition
  for counting, not a case of it. (weak) label: the lesson "separation IS count" (within CIC)
  is memory-level — `separation-is-count-two-routes-closed` — and **has no Lean declaration**;
  it is an observed ceiling, not a theorem here.
- **Categorical type + anchor:** `CountCapped` — `lean-formalization/BeatsCountCriterion.lean:111`;
  `BeatsCount` — `:118`; `not_countCapped_of_beatsCount` — `:140`.
- **Related:** DEF-ORCH-001, DEF-ORCH-003.

---

<a id="def-orch-003"></a>

## Shadow

- **ID:** DEF-ORCH-003
- **Status:** candidate
- **Term + Aliases:** **shadow** (*shadow*, count/entropy/magnitude)
- **Scientific/formal voice:** The scalar, object-level face of the residue: a functor to a
  *thin* category. It separates but does not reconstruct (lossy). Cases: entropy =
  log-cardinality; magnitude; any invariant numerical reading.
- **Operational interpretation:** Orchestrator metrics — number of nodes, entropy of a
  partition, size of a merge. Useful for ordering, useless for inverting: given the shadow,
  the object cannot be recovered.
- **Colloquial voice:** It's the number that summarizes the object and throws the object away.
- **Boundary:** EXCLUDES the morphism-level face of the residue (DEF-ORCH-001): over a thin
  category, no morphism-level reading beats the count — the collapse is structural. The
  shadow is *one* face; never both.
- **Categorical type + anchor:** entropy = log-cardinality,
  `entropy_nondecreasing_under_temporal_coarsening` — `lean-formalization/SecondLawDiscrete.lean:288`;
  thin collapse `thin_codomain_noise_hom_subsingleton` — `ThinCodomainCollapse.lean:98`;
  `thin_hom_readout_not_beatsCount` — `BeatsCountCriterion.lean:196`. (weak) label:
  magnitude-as-shadow is memory + uncommitted Lean.
- **Related:** DEF-ORCH-001, DEF-ORCH-002.

---

<a id="def-orch-004"></a>

## Probe

- **ID:** DEF-ORCH-004
- **Status:** candidate
- **Term + Aliases:** **probe** (*probe/recon*, test-map)
- **Scientific/formal voice:** The active interrogation of an object by test-maps `A → X` that
  *we* choose (Yoneda). The complete family of these maps reconstructs the object: the Yoneda
  embedding is fully faithful.
- **Species axis:** the probe has two species, one per *independent* axis of discovery —
  **linking** (establishes relations, `¬Full` axis; these are the test-maps `A→X`) and
  **recognition** (discovers *which objects/types exist*, `¬EssSurj` axis). **This entry
  covers both normatively**; the *framing* (species ≅ axes, ordering, β-axis) is F7. Full
  **reconstruction** (FF) is the limit of the family of linkings, while the **separation** of
  parallel morphisms by a sub-family is the graded step (open obligation). The order
  recon→linking is not arbitrary: it is the type-formation dependency (`Hom(A,B)` needs
  `A,B`). Collapse-test: F7.
- **Operational interpretation:** The orchestrator knows an artifact not by internal
  inspection, but by the set of questions `A → X` it can address to it; the totality of the
  answers *is* the artifact. At the agent-tool boundary, `ProbeTool` is the reusable capability and
  `ProbeRun` is one execution applying an explicit, versioned `lens_ref`; that run owns
  `observations[]`. **Sonda** is the pt-BR UI label for the same Probe concept, not a third entity.
- **Colloquial voice:** You know the thing by the complete set of questions you can ask it.
- **Boundary:** mandatory DISAMBIGUATION — **three** senses of "recon" that do NOT collapse:
  (1) **active-probe/Yoneda** (THIS entire term — interrogation by test-maps, the broad
  "recon" alias from MAPPING §1) ≠ (2) **probe-experiment** (Popperian falsification, NOT
  this term, lives in `experiment/SKILL.md`); and, *within* this term, (3) the **recognition
  species** (object axis/`¬EssSurj`) is **narrower** than (1) — **never** use bare "recon" for
  the species; write "recognition" (the probe is the *recognition-probe*). EXCLUDES the
  **verb** (DEF-ORCH-005): the probe *reads* the object without transforming it; the verb
  *acts* on it. EXCLUDES **Reference Scout**: `ReferenceScoutTool -> ScoutRun ->
  recommendations[]` discovers paths and references, while `ProbeTool -> ProbeRun(lens_ref) ->
  observations[]` observes through a lens. Shared runtime infrastructure does not establish a
  subtype relation, and neither recommendation nor observation is automatically promoted to fact.
  Frozen Scout v1 spellings (`reference-probe`, `probe_id`, `probe.*`) are compatibility identifiers,
  not uses of this general Probe concept.
- **Categorical type + anchor:** `y` — `lean-formalization/YonedaAsTranslation.lean:41`;
  `Faithful` — `:45`; `Full` — `:50`; `schema_residue_vanishes` — `:58`; functor-of-points
  identity (this sense) `Probe.lean:8-13` (it is an `example`, thin). **Recognition species
  (F7):** `¬EssSurj→NewObjects` in `domainspec-lean-formalization/distilled-
  knowledge/knowledge-evolution-typing.md`; **separation** (parallel morphisms) by family =
  `ProbeTypology.lean:38` `representables_separate`, `:49` `representables_isSeparating`.
  (weak) label: the active-probe / passive-signal duality **and** the species subdivision are
  our own synthesis (2026-07-20 debate), **not** a repo claim — no Lean decl for the
  partition.
- **Related:** DEF-ORCH-001, DEF-ORCH-005; framing in F7 (FRAMINGS).

---

<a id="def-orch-005"></a>

## Verb

- **ID:** DEF-ORCH-005
- **Status:** candidate
- **Term + Aliases:** **verb** (*verb/action*, action on object)
- **Scientific/formal voice:** An action on an object = a morphism **plus** the condition
  under which it preserves the object's symmetry. Within the condition, it is preserving
  (iso/Aut); outside it, it generates residue. Morphism ≠ symmetry: only isomorphisms/Aut
  preserve distinctions.
- **Operational interpretation:** Each orchestrator verb (merge, refine, forget, translate) is
  a morphism with a declared safety zone; applying it outside that zone produces residue —
  and that is *where* there is information to formalize.
- **Colloquial voice:** An action that, once it leaves the range where it's reversible, starts
  losing things.
- **Boundary:** EXCLUDES the **residue** (DEF-ORCH-001): the verb is the *cause* (the
  morphism applied), the residue is the *effect* (the lost object). EXCLUDES the **probe**
  (DEF-ORCH-004): the probe reads, the verb transforms. (weak) label: the characterization
  "verb = morphism + preservation condition" is memory-level
  (`symmetry-invertible-lever-is-enrichment`), **with no Lean declaration**.
- **Categorical type + anchor:** memory `symmetry-invertible-lever-is-enrichment` (morphism ≠
  symmetry; only iso/Aut preserves). No dedicated Lean decl — weak label assumed.
- **Related:** DEF-ORCH-001, DEF-ORCH-004.

---

## Boundary table

For each term, the ONE trait that separates it most sharply from its closest neighbor
(demonstrates that the boundaries do not collide):

| Term | Sharpest separating trait (vs. neighbor) |
|---|---|
| **residue** (001) | Has TWO faces (shadow ⊕ structure); neighbor *shadow* has only one. It is the *effect* of a verb, not the verb. |
| **separation** (002) | Is *prior* to counting — a condition, not a case; neighbor *shadow* is already a derived numerical reading. |
| **shadow** (003) | Functor to a *thin* category, lossy, does not reconstruct; neighbor *probe* (full Yoneda) reconstructs. |
| **probe** (004) | *Reads* the object without transforming it (Yoneda FF); neighbor *verb* *acts* and can generate residue. |
| **verb** (005) | Is the applied morphism + symmetry condition (the *cause*); neighbor *residue* is the lost object (the *effect*). |
