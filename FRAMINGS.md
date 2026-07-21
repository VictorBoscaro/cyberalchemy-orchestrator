# FRAMINGS — framing ledger (session 2026-07-18)

> Status: brainstorm/candidate, **unreviewed**. Each entry is a hypothesis, not a result.
> Distinct from the normative definitions (§3 of PLAN) and from Lean results — **nothing here is
> proven**. Anchors verified by probe 2026-07-18; where the anchor is weak (memory /
> uncommitted Lean / own synthesis), it is **labeled**.

---

## F1 — Residue = shadow ⊕ structure

- **Typed form:** The residue decomposes into two faces — the *shadow* (object-level
  scalar invariant: count/entropy/magnitude) and the *structure* (categorical object:
  morphisms/types/rules). The structure strictly dominates the shadow when the codomain is not thin.
- **Anchor:** `FunctorialResidueStructure.lean:97` `structure FunctorialResidueStructure`,
  `:513` `separation_is_functor_action`; entropy = log-cardinality in
  `SecondLawDiscrete.lean:288` `entropy_nondecreasing_under_temporal_coarsening`.
- **Collapse-test:** If the structure were recoverable from the shadow, the faces collapse into one —
  but decategorifying is irreversible (the "beats count" wall).

## F2 — Battery of shadows + ceiling

- **Typed form:** Each scalar metric is a functor into a thin category — a distinct
  projection direction (count < entropy < magnitude in how much they see). Projection separates
  but does not reconstruct; ascending = swapping the codomain `C` for a non-thin one, not clarifying the shadow.
- **Anchor:** `FunctorialResidueStructure.lean:162` `ofAntitoneSet` (§2, `C = (Set O, ⊆)` =
  degenerate thin instance, "the wall"); thin collapse in `ThinCodomainCollapse.lean:98`
  `thin_codomain_noise_hom_subsingleton` and `BeatsCountCriterion.lean:196`
  `thin_hom_readout_not_beatsCount`.
  — *Weak anchor:* magnitude-as-shadow = memory `magnitude-owns-four-base-invariant` +
  **uncommitted** Lean (`MagnitudeEnriched.lean`), not a committed theorem.
- **Collapse-test:** The battery is non-empty only if different shadows **disagree** on some
  pair. If every metric ordered the same way, it collapses to a single functor — but count and magnitude disagree.

## F3 — Count presupposes separation

- **Typed form:** The bottom of the ladder is not count, it is separation/individuation: without
  an individuating signal there is no count (indiscernible = identical). Two levels of signal —
  individuating (enables counting, object-level) vs relational (enables seeing morphisms, beats count).
- **Anchor:** `BeatsCountCriterion.lean:111` `CountCapped`, `:118` `BeatsCount`, `:140`
  `not_countCapped_of_beatsCount`.
  — *Weak anchor:* "separation IS count" **has no Lean decl** — it is a memory-level lesson
  (`separation-is-count-two-routes-closed`, four closed-negative routes). The physical instance
  (identical QM particles not countable as individuals) is an illustration, not a theorem of the repo.
- **Collapse-test:** If count could exist without prior separation, the precedence falls and
  F3 becomes circular.

## F4 — Active-probe / passive-signal duality

- **Typed form:** The residue emits indirect signals (shadows received involuntarily,
  lossy) **and** admits active probes — test-maps `A → X` that we choose (Yoneda). The
  complete family of probes reconstructs (Yoneda fully faithful); a single passive shadow does not.
  Active/passive = choosing the screen vs being stuck with the projection = the thin/non-thin lever.
- **Anchor:** covariant (probe-inward) `YonedaAsTranslation.lean:41` `y`, `:45`
  `Faithful`, `:50` `Full`, `:58` `schema_residue_vanishes`; functor-of-points `Probe.lean:8-13`
  (it is an `example`, not a named lemma — thin); contravariant (observe-outward)
  `files/new/YonedaBridge.lean:65` `coyonedaUnit`.
  — *Label:* the covariant/contravariant **split** is real in the repo; the **duality** that
  pairs them (probe ⟷ observable) is **this session's synthesis**, not an existing claim of the repo.
- **Collapse-test:** If probing by all representables were not faithful, the active face would not
  have an advantage — but Yoneda FF guarantees that it does.

## F5 — Verb-rule

- **Typed form:** A verb (`implements`/`validates`/`refines`/…) is a morphism **plus** the
  condition under which it preserves the object's symmetry; outside that condition, it generates residue —
  making the residue measurable per-verb.
- **Anchor:** memory `symmetry-invertible-lever-is-enrichment` (morphism ≠ symmetry; only
  iso/Aut preserves). — *Weak anchor:* memory-level, no dedicated Lean decl.
- **Collapse-test:** If every verb preserved symmetry, there would be no residue per-verb —
  but the general morphism is not iso.

## F6 — The Yoneda point as target, the anomaly as engine (the dynamics)

- **Typed form:** The **Yoneda point** (fully faithful, residue 0, total individuation) is
  the target — crystalline knowledge. In domains with operative self-modeling it is **unreachable
  by construction** (the residue is structural). You *know* you haven't arrived because you receive a
  **discriminating signal**: a detected FF-failure (two things the model had identified
  turn out to be distinct under a new probe = a separator that the current lens is blind to). Hunting
  that anomaly → sending an active probe there → enriching `C` → shrinking the residue. This is the
  **scientific process**.
- **Anchor:** Yoneda point = `YonedaAsTranslation.lean:58` `schema_residue_vanishes`
  (residue vanishes iff `Full ∧ Faithful`); the anomaly = `BeatsCountCriterion.lean:118`
  `BeatsCount` (separator invisible at the current resolution). — *Weak anchor:* unreachability
  in rich domains is gradient A3 (BACKLOG / memory), not a Lean theorem.
- **Collapse-test:** Falls if, in rich domains, the Yoneda point is reachable (the engine stops);
  or if every "anomaly" is always re-expressible at the current resolution (signal without a new
  separator) — then there is no structure to extract, only noise.
- **Status (2026-07-20):** partially deflated by the 3-probes debate — the *unreachable*
  face survives (the persistence lemma agrees: positive residue at every finite level),
  but the framing "Yoneda point = target that gets *reached*" falls: `y` is FF for free
  and the residue-0 endpoint is vacuous (`Knowledge.total`). The content is the **ordered trajectory of
  enrichment** — see F7 and memory `yoneda-ascension-thesis-verdict`.

## F7 — Two probe species = the two independent axes, with presentation order

- **Typed form:** The two **species** of the probe (normed in DEF-ORCH-004) align with the two
  *independent* axes of discovery: **recognition** ↔ `¬EssSurj → NewObjects` (which
  objects exist) and **linking** ↔ `¬Full → NewRelations` (the relations, Yoneda's
  test-maps). What F7 adds is this *alignment* and the *order*. The axes are independent, but the
  **recon→linking order is not arbitrary**: it is a **type-formation dependency** — a
  link lives in `Hom(A,B)`, whose type is ill-formed while `A,B` do not yet exist. Hence the
  structure is a **graded poset** (well-founded object→relation stratification; the name "Reedy"
  is an analogy, not the homonymous structure), not a linear ladder nor a logical necessity. The
  shallow→deep reading ("search on top, then deep research") is the **resolution β-axis**
  (coarse sub-family that does not yet separate → enrich until it separates), which composes
  with the object→relation axis.
- **Anchor:** axes = `distilled-knowledge/knowledge-evolution-typing.md` in
  `domainspec-lean-formalization` (`¬EssSurj→NewObjects` ⊥ `¬Full→NewRelations`); the linking
  family **separates** (parallel morphisms) = `ProbeTypology.lean:38` `representables_separate`,
  `:49` `representables_isSeparating` — the complete *reconstruction* is Yoneda FF (see F4). —
  *Label:* the "two operational species = the two rungs", the well-founded stratification and the
  β-axis are **synthesis** (debate 2026-07-20), **with no Lean decl** — the witness of graded
  convergence (sub-family fails → adding a probe restores FF) is an **open obligation**. Also: the
  recon/linking subdivision is a *new* partition of the DEF-ORCH-004 probe (which covered only the
  *linking* half, `A→X`) and uses "recognition" in a narrower scope than the "(recon)" of
  MAPPING §1 — **reconciled (2026-07-20):** species normed in DEF-ORCH-004 (species axis +
  triple disambiguation of "recon") and partition in MAPPING §2.
- **Collapse-test:** Falls if the species are not independent (a probe that is recon *and*
  linking at the same time undoes the product of axes), or if the order is not forced by the
  typing of `Hom` (a universal object that lets you link before finding).

---

## Common thread

F1–F5 are the **static anatomy**; F6 is the **dynamics**; **F7 refines F4's linking axis
(the test-maps `A→X`) and adds a new recognition axis (object/EssSurj), ordering
the two by presentation (recon→linking)**. All circle the same lever —
**thin vs non-thin, the choice of `C`**. The scalar shadow (F1) and each metric (F2) are the
thin codomains where structure is lost; F3 shows that even count, the floor of that regime,
already presupposes an individuating signal that it does not manufacture; F4 names the way out — swapping the
passive projection for the active family of probes (Yoneda FF) is *choosing a non-thin `C`*; F5 locates
where the residue appears in that richer `C` (the per-verb symmetry defect); and F6 sets it all
in motion: the work is **climbing `C` toward the unreachable Yoneda point, driven by
discriminating signals**. The common bet, and the one point where they all fall together: that ascending
always means **enriching the codomain, never clarifying the shadow**.
