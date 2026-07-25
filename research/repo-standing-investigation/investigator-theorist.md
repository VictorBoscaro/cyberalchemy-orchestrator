---
tags: [category-theory, residue, orchestration, anti-noise, vault]
node_type: audit
is_session: false
layer: domain, ontology
nature: explanatory
status: draft
veracity: medium
conviction: medium
version: 1.0.0
last_updated: 2026-07-21
---

# Investigator — Theorist / Architect (the formal GROUND)

*Vector: is the CT + decision-hygiene foundation coherent and load-bearing, or decoration?
One investigator of several; argues its axis hard.*

## Headline verdict

The ground is **coherent but currently cheap**. Every part of Front 2 that is
formalized and sorry-free is true *for free* — and buys almost nothing beyond what a
DAG scheduler plus an elementary variance argument already give. Every *surprising*,
load-bearing claim is **open or closed-negative**. The CT is load-bearing exactly on
the trivial/static fragment and decoration-or-unproven exactly on the dynamic fragment
the whole thesis is *about*. The repo's own collapse-tests for its two most important
claims are near-triggered.

## Coherent (survives) vs candidate-only

**Coherent, but "for free":**
- Sequential fragment = free category on a quiver (Mathlib `Paths`); assoc/identity
  come free — `OrchestrationCategory.lean` (sorry-free; the "sorry" at line 117 is a
  *comment* asserting `No sorryAx`). It types the DAG scheduler; nothing more.
- Yoneda embedding FF — `YonedaAsTranslation.lean:41/45/50/58`. But the repo already
  *self-deflated* this (FRAMINGS F6 status 2026-07-20): `y` is FF for free, the
  residue-0 endpoint is vacuous (`Knowledge.total`). Content survives only as the
  *ordered enrichment trajectory*, which is unformalized.
- Representables **separate** — `ProbeTypology.lean:38/49`. Separation ≠ reconstruction;
  the full-faithful *reconstruction* of the plural probe family is not anchored.
- `FunctorialResidueStructure` + `separation_is_functor_action` (`:120/:545`) +
  `functorial_strictly_dominates_count` (`:286`) — real, sorry-free.
- Covariance-knob unification (anti-noise §): `Var(ē)=σ²[1+(N−1)ρ̄]/N`; tension = engineered
  ρ̄<0, independence = ρ̄=0, one decorrelation axis. Elementary but **correct** — genuinely
  grounds Front 1's "one knob, two stages." Not merely named.
- `residue = shadow⊕structure` at the code layer (CONST-ENG EG-4/EG-5) and the
  ontology's mutual-information orthogonality (`ontology-conventions` App. A) — correct,
  tested formalizations of the same lever.

**Candidate-only / probably-false where it matters:**
- **ORCH beyond sequential is probably not a category.** zig-zag/feedback "never count
  as dependencies" → the repo's own honest guess (MAPPING §2, OBLIGATIONS named risk):
  2-cells / bicategory, **not** 1-morphisms. Collapse-test (a) — "CT is decoration for
  those edges" — is the likely outcome. The interesting connective structure is exactly
  what does not fit.
- **Synthesis-residue does not beat count on concrete agent outputs.** OBL-E3 sub-3 is
  dischargeable *only at the separation bar* — a third instance of an already-owned
  mechanism. The count-beating (invariant-factor) bar is **closed-NEGATIVE** over concrete
  `Ab`/Type-valued `AgentOut` (`DiamondResidueInvariantFactors.lean:408`
  `tierC_pigeonhole_not_injective`; the 2026-07-21 agentout-gate: "count-capped at the
  morphism level"; `PRIZES.md:67` OPEN only for a *non-concrete* codomain a real synthesis
  never reaches). So collapse-test (b) is *arguably already satisfied* for the substrate the
  orchestrator runs on. The categorical residue is decoration precisely where it must bite.
- **Enrichment convergence is unwitnessed.** The graded-convergence witness (sub-family
  fails to separate → adding the probe restores FF) is an **open obligation with no Lean
  decl** (PLAN §5, FRAMINGS F7). The sibling supplies only the *persistence* co-testimony
  (positive residue at every finite level — the *pessimistic* half). The engine's forward
  direction is unformalized: the foundation proves "you never finish," not "you progress."
- **bias⊕noise ⊥ split** holds only under a Legendre `F`; `F = MAP/anchored common scale`
  is **asserted by naming, not constructed** (OQ-10.1); it is **info-geometry, not CT**
  (the doc's own "non-native"); compositionality across stages is **OPEN** (DPI plausibly
  rotates residue out of ⊥ — = OBL-E3 one floor up). Only nudge↦coupling-fiber on `D(A^N)`
  is claimed native-categorical.
- **Provenance spine does not exist** — ids in four disjoint spaces (PLAN §5).

## Lean build status (sibling `domainspec-lean-formalization`)

Anchors are **"sorry-free per source," NOT build-verified** — the index (`lean-formalization/README.md`)
is explicit that `lake build` has **not** been re-run and warns of *caveat-lag*.
Confirmed on disk: repo present, OBL-E3 files present, `SynthesisResidue.lean` sorry-free.
**New risk found:** the build config is fragmented (`lean-formalization/files/`, `files/new/`,
`lean-engineer/`, `internal_tools/`), and `OrchestrationCategory.lean` sits in
`lean-formalization/` while the lakefile is under `.../files/` — it is **not evident the
OBL-E3 decls are in a compiled target**. Sorry-free-on-read ≠ in the dependency closure.

## Ranked: what to do next

1. **Provenance spine (BL-3 / cross-cutting) — logically prior to everything.** A category
   needs an equality predicate on objects to state composition (`cod f = dom g`). With ids
   in four disjoint spaces, ORCH's *objects are not even a well-defined set*, and "survival
   indexed by the family that tested it" (defeasible provenance) has no denotation. The
   spine is the shared referent three open things wait on (enrich step, freeze enforcement,
   self-reference typing). It is prior to a non-toy OBL-E3. Highest leverage.
2. **Lean build verification (`lake build` green + `#print axioms` clean).** Cheap, binary,
   and it converts the *entire* anchor table from "authoritative location" to "evidence" at
   once — and would surface the fragmented-target risk above. Ceiling: a green Lean object
   is still not evidence any orchestrator obeys it.
3. **OBL-E3 sub-3 discharge.** Worth doing to *bound* the claim, not raise it: as scoped it
   only confirms synthesis = a pushout that types-but-does-not-beat-count on real outputs.
   Informative (settles that the residue is decoration for concrete substrate); not a raise.
4. **EG-1 enum-drift trace** — small, empirical, unblocks the *code-layer* consistency
   invariant (single validated writer) the golden-graph loop needs; disabled write path
   depends on it.

## The single formal result that would most raise veracity

**The graded-convergence witness** (sub-family fails to separate → adding the missing probe
restores fully-faithful). It sits at the triple intersection: Front 2 (probe/Yoneda
dynamics), Front 1 (claim→refute→**enrich**→golden loop), Front 3 (the golden-connection
enrich step — the only place `omega_absorption_refuted` permits enrichment). Its absence is
the deepest hole: the repo has formalized the pessimistic *persistence* half and left the
constructive *convergence* half entirely un-witnessed. Landing it is what would make the CT
"not decoration" — converting F6's "anomaly→probe→enrich→shrink residue = the scientific
process" from framing into theorem. Second-best: the bias⊕noise **compositionality** result
(⊥ survives stage composition), but that needs `F` constructed first and is info-geom, not CT.

## Connections

| Document | Type | Description |
|---|---|---|
| `OBLIGATIONS.md` (OBL-E3) | `contextualizes` | The obligation this audit assesses; confirms sub-3 reaches only the separation bar, count-capped on concrete substrate. |
| `MAPPING.md` | `contextualizes` | The construct⟷CT table audited; concurs feedback = 2-cell, synthesis-residue count-capped. |
| `FRAMINGS.md` | `contextualizes` | F6/F7 dynamics assessed; flags graded-convergence witness as the un-witnessed keystone. |
| `lean-formalization/README.md` | `derives-from` | Source of the sibling build-status claims; this audit adds the fragmented-target risk. |
| [[anti-noise-orchestration]] | `contextualizes` | Front 1 thesis audited; covariance-knob coherent, bias⊕noise F-conditional and non-native. |
| [[engine-constitution]] | `contextualizes` | EG-1 enum-drift ranked as the code-layer consistency fix. |
| `plans/governed-agent-work-infrastructure/PLAN.md` | `contextualizes` | §2/§3.2/§5 assessed; provenance spine ranked as logically prior to OBL-E3. |
