# lean-formalization — what the sibling Lean proves, and why it matters here

> **What this is.** An index of the theorems and design notes in the **sibling** repo
> `domainspec-lean-formalization` that anchor the category-theory constructs used in this project.
> It holds **no Lean of its own** — only pointers, each with a plain-language reading of *what the
> file says* and *why it matters to the orchestrator*. Nothing in *this* repo is typed in Lean.
>
> **How to read a pointer.** Anchors are `path:line` relative to the sibling repo root
> (`../domainspec-lean-formalization/`). The canonical Lean is in that repo's `lean-formalization/`
> folder.
>
> **What "sorry-free" means, and does not.** "sorry-free (per source)" = we read the file and the
> sibling's own axiom-check session (`AxCheckSessions.lean`) and found no live `sorry`/`admit`. We
> have **not** re-run the full `lake build` gate; the sibling warns of *caveat-lag* — honest scoping
> present at the proof, often dropped at the citation (`README.md:55`, `GLOSSARY.md:375`). Treat a
> pointer as an authoritative **location**, not a build-verified clean claim.
>
> **The load-bearing caveat, in one line.** These are **formalized Lean objects, not evidence that
> any orchestrator behaves this way**. The sibling states it: *"The gap between 'the math is
> formalized' and 'the framework obeys it' is real and is preserved everywhere"* (`OBJECT-MAP.md:10-19`).
> A pointer buys a typed candidate, not a discharged claim.
>
> Verified 2026-07-21 by a three-agent recon (dispatch `2026-07-21-sibling-lean-pointer-index`),
> which also corrected line anchors that had drifted in our own docs (§4).

---

## 1. The constructs, and the Lean that grounds them

Grouped by the idea each supports in this project. Every entry: **Says** (plain reading) ·
**Matters** (why it is load-bearing for us) · the anchor · sorry-free?

### A. The probe — why *opposed, complete* families of agents buy something a single one cannot

This is the formal core of Front 2, and the reason the whole project bets on *structurally
different* agents rather than more of them.

**`YonedaAsTranslation.lean`** — the Yoneda embedding as translation.
`:41` `abbrev y := yoneda` · `:45`/`:50` anonymous `Faithful`/`Full` instances · `:58`
`theorem schema_residue_vanishes`. *(sorry-free.)*
- **Says:** an object is fully determined, up to isomorphism, by the *totality* of maps (probes)
  into it — the embedding into its "functor of points" is full and faithful. `schema_residue_vanishes`
  states the residue between a thing and its probe-image is zero exactly when that embedding is full
  and faithful.
- **Matters:** this is the theorem behind our claim that a *complete family of probes reconstructs*
  what a single passive reading loses. For the orchestrator it separates "more agents" from "the
  right agents": one scalar read-back of an object is lossy, but the complete family of active,
  opposed probes pins it down. It is also the target picture of Front 2's dynamics — the (usually
  unreachable) "Yoneda point" where residue is zero.

**`Probe.lean`** — the functor-of-points probe. `:8`, `:12` (two anonymous `example`s, by `rfl`).
*(sorry-free.)*
- **Says:** a "probe into `X`" is literally a morphism `A → X`; these two computations just confirm
  the functor-of-points bookkeeping (a probe *is* an element of a hom-set).
- **Matters:** it pins the *definition* of "probe" we use throughout (an active map you choose, not
  a passive signal you receive), grounding `DEF-ORCH-004`. Modest by design — it is an `example`, a
  computation, not a deep theorem; do not cite it as more.

**`files/new/YonedaBridge.lean:65`** — `def coyonedaUnit`. *(sorry-free; separate lake sub-package.)*
- **Says:** the co-Yoneda unit — the *contravariant* companion to `y`, i.e. observing an object
  from the outside rather than probing it from within.
- **Matters:** it is the formal pair behind our F4 "active-probe ⟷ passive-signal" duality — the
  choice between picking the screen (active) and being stuck with a projection (passive). Caveat: it
  builds in a separate sub-package, not the main target.

### B. The residue — what a synthesis actually loses

The object our entire "residue" vocabulary points at, and the reason `robot_talks` synthesis is
modeled as a pushout that *loses* something rather than a concatenation that keeps everything.

**`FunctorialResidueStructure.lean`** — the residue as a functor.
`:120` `structure FunctorialResidueStructure` · `:189` `def ofAntitoneSet` · `:286`
`functorial_strictly_dominates_count` · `:545` `theorem separation_is_functor_action`.
*(all sorry-free.)*
- **Says:** the residue is a functor from schemas (ordered by refinement) into a codomain `C` —
  "what fails to cross when a rich reality is compiled to a leaner schema." `ofAntitoneSet` is the
  degenerate thin instance (`C = sets ordered by ⊆`, "the wall"). `separation_is_functor_action`
  exhibits two *distinct* residue elements that a refinement map collapses to one — refining a
  schema genuinely *identifies* previously-distinct things, and that identification is a functor's
  action. `functorial_strictly_dominates_count` proves the structured residue carries information no
  scalar count sees.
- **Matters:** this is the single object OBL-E3 sub-3 asks a synthesis's residue to *be*. It is why
  a synthesis is a pushout (identifies overlaps, generates residue) and a bare `concat` is only a
  coproduct (keeps everything, count-shaped). `functorial_strictly_dominates_count` is also the
  formal backing for the engine constitution's EG-4 (a derived number must never claim more than the
  rows under it) and for the anti-noise thesis's "aggregate ≠ one scalar."

### C. Beats-count — the formal meaning of "an anomaly the current lens cannot see"

Why our noise/aggregation must not collapse to a single number, and why "climbing the codomain"
is the only way to detect a distinction a scalar is blind to.

**`BeatsCountCriterion.lean`** — count-capped vs. beats-count.
`:111` `CountCapped` · `:118` `BeatsCount` · `:140` `not_countCapped_of_beatsCount` · `:196`
`thin_hom_readout_not_beatsCount`. *(sorry-free.)*
- **Says:** a readout is *count-capped* when it factors through the count/fiber data, and *beats
  count* when it distinguishes two inputs that every count identifies. `not_countCapped_of_beatsCount`
  is the dichotomy; `thin_hom_readout_not_beatsCount` proves a thin (scalar-like) codomain can never
  beat count.
- **Matters:** this is the exact statement of "an anomaly is a separator the current resolution is
  blind to." For the orchestrator: a scalar score is count-capped, so it *provably cannot* detect a
  distinction a richer readout can — the formal reason a panel of judgments must keep its structure
  (distribution, disagreement), not collapse to a mean, and the reason detecting a fork or a bias
  needs a non-thin codomain.

**`ThinCodomainCollapse.lean:98`** — `thin_codomain_noise_hom_subsingleton`. *(sorry-free.)*
- **Says:** in a thin codomain the residue's hom-set is a subsingleton — every morphism-level
  distinction collapses.
- **Matters:** the floor. It proves that insisting on a scalar-like codomain *guarantees* you cannot
  see morphism-level residue — so the way up is to enrich `C`, never to "clarify the shadow." This is
  the wall our F6 dynamics climb away from.

**`ProbeTypology.lean`** — the separating family. `:38` `representables_separate` · `:49`
`representables_isSeparating`. *(sorry-free.)*
- **Says:** a family of representable probes *jointly* separates parallel morphisms — if every probe
  in the family agrees on `f` and `g`, then `f = g`.
- **Matters:** the formal form of check-tension's *separating family* (P5): a plural, orthogonal set
  of probes is jointly faithful where any single axis is blind. It is the theorem under "opposed
  angles cancel correlated bias" — the family separates what one probe cannot.

**`SecondLawDiscrete.lean:284`** — `entropy_nondecreasing_under_temporal_coarsening`. *(sorry-free.)*
- **Says:** entropy, defined as the log-cardinality of the noise set, does not decrease under
  temporal coarsening — a discrete second-law analogue.
- **Matters:** it makes one of the *scalar* faces of residue (entropy, F2) a real, computable
  quantity — with the honest caveat that it is a shadow (it sees magnitude, not structure). It grounds
  the entropic regime of the anti-noise thesis; use it knowing it is count-side, not structure-side.

### D. The ceiling — where count-beating provably stops

The honest upper bound on what OBL-E3 may claim.

**`DiamondResidueInvariantFactors.lean`** — `:257` `invariantFactorResidue` (ℤ/4 vs ℤ/2⊕ℤ/2) ·
`:408` `tierC_pigeonhole_not_injective`. *(sorry-free.)*
- **Says:** `invariantFactorResidue` exhibits a separator invisible even to *output cardinality*
  (two groups of the same size, non-isomorphic). `tierC_pigeonhole_not_injective` proves that for
  finite equal-order non-isomorphic abelian groups no injective homomorphism exists — closing the
  strongest "count-invisible separator" bar **negatively** over concrete `Ab`.
- **Matters:** this is the ceiling that keeps us honest. The strongest prize — a separator invisible
  to a count on the residue object itself — is closed-negative for concrete codomains. So a synthesis
  over concrete agent outputs can reach the *separation* bar (Group B) but **not** this one; it bounds
  what OBL-E3 sub-3 is allowed to assert (see §2).

### E. Zig-zag — the shape of the back-and-forth connection

**`P1Positive.lean`** + **`LanFaithfulFailureFamilyCommaConnected.lean`** — comma-connectedness.
`P1Positive.lean:303` `def CommaConnected` · `LanFaithfulFailureFamilyCommaConnected.lean:158`
`commaConnected_Δ2` · `P1Positive.lean:564` `lanUnit_mono_of_cocycle_torsionFree_noFarComma`.
*(sorry-free.)*
- **Says:** `CommaConnected Δ` holds when, for every target `d`, the comma category
  `CostructuredArrow Δ d` is connected — any two lifts are joined by a zig-zag of arrows.
  `commaConnected_Δ2` is a verified instance; the positive result derives a mono where the comma has
  no "far" object.
- **Matters:** this is the formal home of our `zig-zag` connection type — a back-and-forth between
  groups, read as connectedness of a comma category. Honest limit: it anchors the *shape*, but our
  MAPPING already suspects `zig-zag`/`feedback` are 2-cells, not 1-morphisms — so this does **not**
  settle the OBL-E3 risk that the "it's a category" claim narrows to the sequential fragment.

> **Do not cite `probe_zigzag_nf.lean`.** It looks like a zig-zag anchor and our older docs pointed
> near it, but it is a **refuted probe** with live `sorry` tactics (`:159`, `:178`, `:187`); its own
> header records the route as dead. The real zig-zag anchor is the `CommaConnected` entry above.

---

## 2. OBL-E3 — the direct bridge (synthesis-residue)

The one place the sibling points *back* at us: a design note whose stated target is this repo's
[`OBLIGATIONS.md`](../OBLIGATIONS.md) OBL-E3 (*is the orchestration language a category, and is a
synthesis's residue the same object as `FunctorialResidueStructure`?*).

- **`TO-ME/oble3-synthesis-as-second-residue-instance/`** (`00-motivation-and-business-context.md`,
  `01-technical-approach.md`). **Says:** maps `concat` (no robot-talks) → coproduct; `synthesis`
  (`robot_talks:true`) → pushout/colimit; robot-talks overlap-identification → the span apex map;
  synthesis-residue → a `synthesisResidue` mirroring the diamond. **Matters:** it is the written plan
  for discharging OBL-E3 sub-3 — the concrete route from our dispatch vocabulary to the residue object.
- **`OrchestrationCategory.lean`** — **Says:** `ORCH` is a category on the *sequential* fragment
  (associativity + identity free from Mathlib's `CategoryTheory.Paths`; builds clean per
  `TO-ME/README.md:80-90`). **Matters:** it settles sub-1/sub-2 of OBL-E3 for the sequential fragment
  only — exactly the fragment our named risk says might be all we get.
- **`SynthesisResidue.lean:408`** — `separation_is_functor_action` (in the `SynthesisResidue`
  namespace). **Says:** the sub-3 payload — a synthesis's residue clears the separation bar.
  **Matters:** it is the closest thing to a discharge of OBL-E3 sub-3 — but see the honest reading.
- **`PRIZES.md:67`** — **Says:** the "second morphism-level count-beating residue" prize is **OPEN**,
  but closed-negative over concrete `Ab`; the 2026-07-21 *agentout-gate* verdict finds the
  tension-synthesis residue over Type-valued `AgentOut` **count-capped at the morphism level**.
  **Matters:** it tells us the prize our synthesis might have won is not winnable over concrete agent
  outputs.

**Honest reading of OBL-E3's status.** Sub-3 is dischargeable only at the **separation bar** — a
genuine third instance of a mechanism already owned there ("build-from-owned bookkeeping"), **not**
a new count-beater. The stronger **invariant-factor bar** stays open only for a *non-concrete*
codomain, which a synthesis over concrete agent outputs does not reach. Do not record sub-3 as
settling fractality or the zig-zag/feedback question. (`STRONG-UNIFICATION-STATUS.md:59`: *"the
diamond remains the repo's sole morphism-level count-beating witness."*)

---

## 3. Connections worth following (surfaced by the recon, not yet in our docs)

These touch Fronts 1 and 3 more directly than the pure-CT anchors — leads, not claims:

- **Decision gates (Front 1 ↔ Front 3).** `ReconstructionGate.lean` — a literal `GateDecision` with
  **pass / flag / block** (`reconstructionGate_eq_{block,pass,flag}_iff`); `ForgetNodeResidue.lean` —
  an entropy gate. *Why it matters:* a formalized decision gate is exactly the shape of our
  check-tension / human-confirm gate; whether the two gates measure the *same object* is a banked open
  question there.
- **The agentout gate (Front 1 ↔ Front 3).** `research/oble3-agentout-gate/` +
  `theorem/sessions/2026-07-21-0500-synthesis-residue-agentout-gate.md`. *Why it matters:* it is the
  synthesis-residue admission gate for **agent outputs** specifically — the live counterpart to the
  OBL-E3 note, and the closest existing work to our Front 3 bus admitting judgments.
- **Dialogical co-construction (multi-agent).** `DialogicalCoConstruction.lean` — a
  three-residues-of-dialogue conjecture on a Lorenzen–Lorenz substrate (Tier-A closed sorry-free).
  *Why it matters:* a typed model of two agents co-constructing a result — the deliberation phase of
  our per-group bus.
- **Bias as untracked residue (Front 1).** `EPISTEMIC-POSITION.md:207-211` reads Kahneman's
  tracked-vs-untracked distinction as the precedent for typed residue: *"a bias is precisely a residue
  object the schema lacks the type to register."* *Why it matters:* this is the sharpest existing link
  between the decision-hygiene front and the categorical one — our "anomaly the lens can't see", stated
  as cognitive hygiene.
- **Good Regulator (self-modeling).** `EPISTEMIC-POSITION.md:193-196` — Conant–Ashby: *"any honest
  model is a regulator over the iteration that produced it."* *Why it matters:* relevant to an
  orchestrator that regulates its own dispatch process (the A6 self-instance idea).
- **Knowledge as a functor.** `KnowledgeAsFunctor.lean` — `Sound = Faithful`, `Complete = Full`,
  `Learning := Hom K K'` (sorry-free). *Why it matters:* a typed vocabulary for "what an agent knows /
  learns." The "= knowledge" gloss is an explicit **stipulation, not a theorem**.
- **The two discovery axes.** `distilled-knowledge/knowledge-evolution-typing.md` — recognition
  (`¬EssSurj → NewObjects`) ⊥ linking (`¬Full → NewRelations`) ⊥ forgetting (`¬Faithful`), pointing at
  `SchemaInstance.lean`, `SchemaRuleCollapse.lean`, `ResidueEssSurjFunctor.lean`. *Why it matters:* it
  is the formal version of our F7 recon→linking axes. The doc itself flags these residues as thin /
  count-capped and **not** `lake build`-verified — a caveat we inherit.

---

## 4. Anchor drift to fix in our own docs

The recon found line/name drift between our citations and the sibling source — to correct in
[`FRAMINGS.md`](../FRAMINGS.md), [`OBLIGATIONS.md`](../OBLIGATIONS.md)
(follow-up, not yet applied):

- `separation_is_functor_action` → `FunctorialResidueStructure.lean:545` (not `:513`; `:120` is the
  `structure`).
- `tierC_pigeonhole_not_injective` → `DiamondResidueInvariantFactors.lean:408` (not `:386`, the docstring).
- `entropy_nondecreasing_under_temporal_coarsening` → `SecondLawDiscrete.lean:284` (not `:288`).
- The zig-zag anchor must move off `probe_zigzag_nf.lean` (refuted, has `sorry`) onto
  `P1Positive.lean:303` + `LanFaithfulFailureFamilyCommaConnected.lean:158`.
- `y`, `Faithful`, `Full` in `YonedaAsTranslation.lean` are an `abbrev` and two **anonymous
  instances** — citable by line only, not by name.

---

## 5. The sibling's own epistemic stance (for honesty)

`EPISTEMIC-POSITION.md` is labeled `[position]`, not theorem, and is **stale** (`last_updated:
2026-05-27`) with parts retracted in place (its `StrangeLoop` "colimit strictly less than the
structure" claim is demoted to *claim > proof* — what is actually proved is only one named functor
failing to be an equivalence). Its durable stance: **categorical structuralism + Peircean
fallibilism + Lakatos iteration** — *"what is discovered is universal-property structure
(presentation-invariant, Yoneda); what is created is each particular presentation"* (`:38-44`). For
anything load-bearing, cite the Lean, not the position paper.
</content>
