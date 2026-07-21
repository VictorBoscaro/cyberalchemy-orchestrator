# FRAMINGS — stratified CT ledger (framings · interpretation · join)

## Objective

This document is the **single stratified ledger** for the orchestrator's category-theory
thesis. It holds, in one place, three strata that answer three questions:

- **§1 — Theory:** *what the abstract types are* — the F1–F7 anatomy of the residue and the
  ascent, i.e. the codomain `C` and the thin/non-thin lever.
- **§2 — Interpretation functor** `I : AgentLang → CT`: *how the orchestration language
  instantiates that theory* — each construct of the agent-language ↦ its candidate CT type +
  a real-file anchor.
- **§3 — Join / soundness:** *whether the two agree* — the fibration (which framing each
  construct instantiates) and the bidirectional gaps (framings with no construct, constructs
  with no framing).

It is the **single source of truth** for the construct ⟷ CT-type mapping. Every entry is a
**candidate to be typed**, held under `claim ≤ proof` — nothing here is a result.

## Context

This ledger was formed on **2026-07-21** by merging two previously separate files:
`FRAMINGS.md` (the F1–F7 abstract anatomy) and `MAPPING.md` (the construct ⟷ CT-type
interpretation). The two referenced each other on nearly every entry, so the file boundary
did **negative work** — closing a single thought meant jumping between files. Merging
internalizes every cross-reference, states the shared discipline **once** (§0), and — the
payoff — puts the **bidirectional gaps** on one surface (§3): a framing with no operational
witness yet (F2), a framing that binds to a construct with no dedicated row (F5 ⟷ the edge
taxonomy), and constructs with no framing yet (`feedback = 2-cell`, `meta`/A6,
`final_approver = limit` → candidate F8/F9). Provenance: framings session 2026-07-18; mapping
created 2026-07-19; stratified merge 2026-07-21.

---

## §0 — Status and conventions

> Status: brainstorm/candidate, **unreviewed** / **not reviewed**. Each entry — framing or
> mapping row — is a hypothesis / a **candidate parallel to be typed**, not a result.
> **`claim ≤ proof`.** Distinct from the normative definitions (§3 of PLAN) and from Lean
> results — **nothing here is proven**; this merge is a reorganization, no row or framing is
> upgraded in strength.
> **Anchors.** Every claim is anchored to a real file. Framing anchors verified by probe
> 2026-07-18; where the anchor is weak (memory / uncommitted Lean / own synthesis), it is
> **labeled**.
> **Single source of truth for the mapping** (PLAN protocol §3): the mapping tables live
> **here** (§2); PLAN §4 points to them, does not duplicate them.
> **Inherited rule.** Every construct of the agent-language → its type in CT + anchor in a
> real file. The operational base is the skill `domainspec-subagents-strategy`
> (`domainspec/.claude/skills/domainspec-subagents-strategy/SKILL.md`) + constitution
> `subagents-strategy-constitution-proposal.md` (v0.6.3).
> **Provenance.** Framings session 2026-07-18; mapping created 2026-07-19; stratified merge 2026-07-21.

---

## §1 — Theory: the abstract types

### F1 — Residue = shadow ⊕ structure

- **Typed form:** The residue decomposes into two faces — the *shadow* (object-level
  scalar invariant: count/entropy/magnitude) and the *structure* (categorical object:
  morphisms/types/rules). The structure strictly dominates the shadow when the codomain is not thin.
- **Anchor:** `FunctorialResidueStructure.lean:120` `structure FunctorialResidueStructure`,
  `:545` `separation_is_functor_action`; entropy = log-cardinality in
  `SecondLawDiscrete.lean:288` `entropy_nondecreasing_under_temporal_coarsening`.
- **Collapse-test:** If the structure were recoverable from the shadow, the faces collapse into one —
  but decategorifying is irreversible (the "beats count" wall).

### F2 — Battery of shadows + ceiling

- **Typed form:** Each scalar metric is a functor into a thin category — a distinct
  projection direction (count < entropy < magnitude in how much they see). Projection separates
  but does not reconstruct; ascending = swapping the codomain `C` for a non-thin one, not clarifying the shadow.
- **Anchor:** `FunctorialResidueStructure.lean:189` `ofAntitoneSet` (§2, `C = (Set O, ⊆)` =
  degenerate thin instance, "the wall"); thin collapse in `ThinCodomainCollapse.lean:98`
  `thin_codomain_noise_hom_subsingleton` and `BeatsCountCriterion.lean:196`
  `thin_hom_readout_not_beatsCount`.
  — *Weak anchor:* magnitude-as-shadow = memory `magnitude-owns-four-base-invariant` +
  **uncommitted** Lean (`MagnitudeEnriched.lean`), not a committed theorem.
- **Collapse-test:** The battery is non-empty only if different shadows **disagree** on some
  pair. If every metric ordered the same way, it collapses to a single functor — but count and magnitude disagree.

### F3 — Count presupposes separation

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

### F4 — Active-probe / passive-signal duality

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

### F5 — Verb-rule

- **Typed form:** A verb (`implements`/`validates`/`refines`/…) is a morphism **plus** the
  condition under which it preserves the object's symmetry; outside that condition, it generates residue —
  making the residue measurable per-verb.
- **Anchor:** memory `symmetry-invertible-lever-is-enrichment` (morphism ≠ symmetry; only
  iso/Aut preserves). — *Weak anchor:* memory-level, no dedicated Lean decl.
- **Collapse-test:** If every verb preserved symmetry, there would be no residue per-verb —
  but the general morphism is not iso.

### F6 — The Yoneda point as target, the anomaly as engine (the dynamics)

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

### F7 — Two probe species = the two independent axes, with presentation order

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

### Common thread

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

---

## §2 — Interpretation functor

The interpretation functor is `I : AgentLang → CT` — each construct of the agent-language ↦ its
candidate CT type ↦ anchor ↦ strength. Its graph is the two tables below.

### 2.1 Seed table (inherited from PLAN §4)

| Construct | Candidate CT type | Anchor | Strength |
|---|---|---|---|
| probe (recon) | generalized element / functor-of-points (Yoneda) | `YonedaAsTranslation.y`, `Probe.lean` | strong candidate |
| probe (experiment) | Popperian falsification | `experiment/SKILL.md` | nominal rhyme (≠ Yoneda) |
| zig-zag | triangle identities / `EqvGen` back-and-forth | `P1Positive.CommaConnected`, `probe_zigzag_nf.lean` | strong candidate |
| sequential | composition `∘` | `connections` | structural |
| dispatch | typed diagram `J → Cat` | schema v0.6.x | candidate |
| feedback / robot-talks | ? (2-cell / (co)limit of perspectives) | — | open → see §2 |
| residue of a synthesis | `FunctorialResidueStructure` / non-iso Lan unit | `FunctorialResidueStructure.lean:120` (`domainspec-lean-formalization @ 6edb664`, sorry-free per source + repo audit; build-gate re-verify pending) | structural |

> **Note (F7):** the "(recon)" in the *probe* row above is the **broad** sense (active probe vs.
> experiment), **not** the recognition *species* from F7 (object axis/`¬EssSurj`). The partition
> by species is in §2, row `probe: species`. Single source of truth for the term: DEF-ORCH-004.

### 2.2 Parallels from the subagents-strategy skill

| Construct | Literal semantics in the skill | Candidate CT type | Strength / what it resolves |
|---|---|---|---|
| **concat vs. synthesis** (P7) | `robot_talks:true → synthesizes`; otherwise `concat`; "aggregation is **derived**, never a field"; "a bare concat is never the final deliverable" | **concat = coproduct** (thin, count-shaped) vs. **synthesis = pushout/colimit** (identifies overlaps in the tension; **generates residue**) | **strong.** Links directly to `FunctorialResidueStructure` (DEF-ORCH-001); halfway point of OBL-E3's sub-obligation 3. **Ceiling (2026-07-21):** dischargeable at the *separation* bar (second instance à la the diamond), **not** the *invariant-factor* prize (needs non-concrete `C`) — see OBL-E3 sub-3 + `TO-ME/oble3-synthesis-as-second-residue-instance/` |
| **feedback edge** | "`feedback` edges **never count as dependencies**"; conditional; back-edge to pull material | **NOT a 1-morphism** — 2-cell / extra structure (outside the 1-skeleton) | **positive evidence** for the OBLIGATIONS risk. Moves P-CT: feedback = 2-cell, not a morphism |
| **check-tension / anti-bias axes** (P5) | tensioned n≥2 pair; axis ∈ {methodology, source-corpus, attack-vector, temporal-prior}; 2 agents verify | **separating family of probes** (jointly-faithful); each axis = orthogonal probe direction; the gate = enriching non-thin `C` | **strong.** Gives the probe (DEF-ORCH-004) a *plural* form; ties together F4 + F6 (axis = separator/anomaly) |
| **meta + lineage** (P13) | `meta:true` = dispatch *about* dispatching; `parent_dispatch_id`; finite/acyclic chain | **endofunctor / free monad**; lineage = well-founded tree (operad of dispatches) | **strong.** Thesis A6 ("framework as its own instance") mechanized in a registry field |
| **final_approver** (P12) | dedicated auditor, never a group member (no self-approval); receives the entire `working_folder` | **terminal cone / limit** of the diagram; auditor = apex outside the diagram | candidate |
| **exit_reason** | closed vocabulary `resolved\|loop_ceiling_reached\|dissent_irreconcilable\|user_abort\|error` | classifying map to a finite **thin** object = the run's **shadow** | candidate — links to DEF-ORCH-003 (scalar reading, lossy; the real residue is the artifact) |
| **dependency scheduling / READY** (P4) | READY when every incoming `sequential`/`zig-zag` edge has produced; all READY launch concurrently; declared order is only a tiebreak | `J → Cat` diagram; scale = topological order of the dependency **poset** | reinforces §1's `dispatch = J → Cat` |
| **collapse-detection** (P14) | the synthesizer downstream of robot-talks **needs** both the **initial AND final** positions | keep the **morphism**, not just the object = *beats count* (do not decategorify) | candidate — live instance of F1/F3 |
| **probe: recon/connection species** (F7) | the two probe species (normed in DEF-ORCH-004) on the two axes: recon↔`¬EssSurj`, connection↔`¬Full` (the `A→X`); order = presentation dependency | **partition by independent axis** = graded poset (object→relation stratification) | **candidate** — anchor `knowledge-evolution-typing.md` + `ProbeTypology.lean:38,:49` (separates, does not reconstruct); distinct from the broad "(recon)" alias in §1; see F7 + DEF-ORCH-004 |

---

## §3 — Join and soundness

The interpretation functor (§2) and the abstract types (§1) are two views of one structure. This
stratum records the **join**: which framing each mapping row instantiates (the fibration), and —
the payoff of the merge — the **bidirectional gaps** where one side has no partner on the other.
Status of every claim below: **candidate, unreviewed** (`claim ≤ proof`).

### 3.1 Fibration — framing ⊣ the §2 rows that instantiate it

| Framing (§1) | Mapping rows that instantiate it (§2) | Strength |
|---|---|---|
| **F1** — residue = shadow ⊕ structure | concat/synthesis (§2.2); collapse-detection (§2.2); exit_reason (§2.2); residue-of-a-synthesis (§2.1) | candidate |
| **F3** — count presupposes separation | collapse-detection (§2.2); check-tension / anti-bias axes (§2.2, the *separation* face) | candidate |
| **F4** — active-probe / passive-signal duality | probe (recon, broad sense) (§2.1); check-tension / plural probe (§2.2) | candidate |
| **F6** — Yoneda point (target) / anomaly (engine) | check-tension / anti-bias axes (§2.2, axis = separator/anomaly) | candidate |
| **F7** — two probe species = two independent axes | probe: recon/connection species (§2.2); probe (recon) (§2.1) | candidate |

### 3.2 Gap map — the unmatched-on-both-sides (the merge payoff)

**(a) Framings with no / weak operational witness in §2:**

- **F5 (verb-rule)** has *no dedicated §2 row*, but it binds to the graph's **edge taxonomy**: the
  verbs are the edges (`sequential` / `zig-zag` / `feedback` / `dispatch`), and the §2 finding
  `feedback = 2-cell` is exactly F5's "a verb that does **not** preserve symmetry → generates
  residue." **Candidate join to author:** `F5 ⟷ edge-taxonomy + feedback-edge` (unwritten; worth a row).
- **F2 (battery of shadows + ceiling)** is only *grazed* by `exit_reason` (§2.2, the run's scalar
  shadow). It remains **theory with no operational witness** yet — flagged, not resolved.

**(b) §2 rows with no framing → candidate new framings F8/F9:**

- `feedback = 2-cell` (§2.2) — operational structure outside the 1-skeleton; the abstract theory has
  not absorbed 2-cells. → feeds the F5 candidate above and a possible **F8**.
- `meta + lineage = free monad (A6)` (§2.2) — self-application (`framework as its own instance`,
  thesis A6) has no framing. → candidate **F8: self-application / the endofunctor A6**.
- `final_approver = terminal cone / limit` (§2.2) — the auditor as an apex *outside* the diagram, the
  **dual** of the probe-colimit (F4/F7), has no framing. → candidate **F9: the auditor as the dual of
  the probe-colimit**.

> These are *candidates for new framings*, not framings — do not number them into §1 until reviewed.

### 3.3 Collapse-tests (folded from the former MAPPING §3)

- **concat/synthesis (the central finding).** *Collapse:* if the synthesis is, in practice, a
  count-shaped merge, it falls into the same collapse-test (b) as OBL-E3 — becomes an analogy, not a pushout.
- **feedback = 2-cell.** *Collapse:* if `feedback` composes associatively as a 1-level
  edge, it goes back to being a morphism and the OBLIGATIONS risk dissolves (unlikely given
  "never counts as a dependency").
- **plural probe.** *Collapse:* if the 4 axes are not jointly-faithful (some object
  indistinguishable across the whole family), the family does not reconstruct and the Yoneda-FF parallel weakens.
- **meta/A6.** *Collapse:* if the lineage admits a cycle, it stops being a well-founded tree / free
  monad — but the constitution requires it to be finite and acyclic.

---

## §4 — Open items and obligations

- **P-CT** (PLAN): feedback/robot-talks — **advanced** by §2 (feedback = 2-cell; synthesis
  = colimit). Still needs typing in Lean.
- **OBL-E3 sub-3** (synthesis-residue = same object): the concat/synthesis row is the
  concrete discharge route — type `synthesize` as a pushout whose non-iso unit IS `FunctorialResidueStructure`.
  **Scoped (2026-07-21):** reachable at the *separation* bar only; the *invariant-factor* prize
  (`domainspec-lean-formalization/PRIZES.md`, OPEN) needs a non-concrete codomain and is **not** closed by sub-3.
  Design brief: `TO-ME/oble3-synthesis-as-second-residue-instance/`.
