# Seam feasibility — bias⊕noise (Kahneman×CT) and nudge (Thaler×CT)

> **Question:** do the paper's two central seams type formally, or are they analogy?
> **Method:** tensioned dispatch `2026-07-20-costura-feasibility` (ledger) — two pairs
> constructor⊥collapser (one per seam), independent positions frozen before
> synthesizing; `check-tension` gate passed (both PASS) before firing. Self-application A6.
> **Status:** completed, `resolved`. Provisional source: `vault/hypothesis/orquestracao-anti-ruido.md`
> (HYP-ORCH-NOISE, candidate/exploratory — this research revises it). Created 2026-07-20.

## Global verdict

**The thesis does NOT break.** The **design layer survives whole and metric-free** (both
collapsers concede this explicitly). The **formal/quantitative layer needs two
re-typings** — and both land in the **same house: categorical probability** (Markov
categories with extra statistical structure), *outside* naked optics and Euclidean orthogonality.
This co-location is the strongest structural result the dispatch produced.

## Seam 1 — Kahneman×CT: `residue = bias ⊕ noise`

**Verdict: `real-under-conditions X`.** Neither analogy (the Bregman route closes that exit), nor
unconditionally real (metric-free Euclidean orthogonality is false).

**Constructor↔collapser convergence** (Fritz and Leinster, without seeing each other, on the same object — low
noise): the decomposition is a **real theorem** via Bregman divergence / dually flat
geometry (Amari's generalized Pythagoras), **without the Fisher metric** — only the Legendre
primal–dual pairing. Mean = unique minimizer of expected Bregman (Banerjee 2005) ⇒ mechanical aggregation
= provably optimal noise minimizer (the √N lever with justification, not rhetoric).

**Condition X, in three pieces:**
1. **Add exactly one Legendre potential `F`** (generalized entropy/free-energy).
   From it come `D_F`, dual coords `η=∇F`, pairing-as-orthogonality, the e-affine connection.
   The split is **exclusive** to Bregman (arXiv 2501.18581). *Golden finding:* this `F` **is** the
   "anchored common scale / MAP" that the thesis already uses — it pays the toll without naming it.
2. **Slot-lock:** exact annihilation of the cross term only with randomization on the **first**
   argument of `D_F(a,s)` (M-projection / reverse-KL orientation). Flip it → Jensen gap ≠ 0.
3. **Compositionality — OPEN, and it is the real frontier.** It decomposed *one* game; whether bias⊕noise
   is functorial along the composition of lenses is unproven (composition mixes the two
   `D_F` slots). Fritz boundary-2 ≡ Leinster OBS2 (the DPI contracts KL, rotates the residue
   out of ⊥) — the two name the same frontier from both sides.

**Strength:** deep but taxed and pointwise (exact theorem given `F` and slot; non-native; status
compositionally open). Does not discharge OBL-E3 — it lives in the loss functional, not in the composition
of dispatch.

## Seam 2 — Thaler×CT: `nudge = process ≠ content`

**Verdict: `real-under-conditions X`,** X = **re-type outside the single-judgment optic.**

**Adjudication of the Myers⊥Jacobs fork → "vacuous in the optic, real in the coupling fiber"
(endorsed).** Myers's 2-cell (`φ:M→M'`) is *verbatim* the generator of the coend relation → a
dichotomy with no middle: **coherent** nudge = identity in the optic (vacuous); **incoherent** = changes
`get/put` = touched content. Since `M` is bound by `∫^M`, there is no functor `Optic→C` that returns
"the residue" — "acts on M, not on A/B" **does not typecheck**. Myers concedes exactly this gap
(the missing residue fibration); Jacobs supplies it.

**The same teeth, relocated:** both agree that process≠content *has* teeth, in a
content-preserving/residue-moving morphism. Jacobs **subsumes** Myers: the real nudges (freeze,
independence-then-aggregate) act on the **joint law** `D(A^N)`. The independence-nudge
`J ↦ ⊗_i(π_i∗ J)` is **identity on every marginal** (content intact) and **non-identity on the
joint** (kills correlation), detected by the variance drop under aggregation (the √N-over-ρ claim).
Natively well-defined because **marginalization `D(A^N)→∏D(A)` is non-monic**.

**Strength:** natively well-typed (non-monicity is a Markov fact, no imported `F`), but
positive payload thinner than Seam 1. **Jacobs > Myers.**

## Cross-seam meta — one house only

The two houses converge tightly and **substantively**: the barycenter `ā=E[a]` (Seam 1) **is** the
aggregation; the variance drop of the mean-pushforward (Seam 2) **is** the same aggregation acting on the
joint. The `F` that Seam 1 imports = the anchored scale that makes judgments commensurable
enough to marginalize/aggregate in Seam 2. **Seam 1 gives the optimality theorem of the lever
(under `F`); Seam 2 gives the well-typed action of that lever on the joint law (native).** The
variance-under-aggregation of one is the detector of the other. They do not dominate — **they compose**.

## Implication for the source thesis (HYP-ORCH-NOISE) — three re-typings

1. **`bias ⊕ noise` / `bias ⊥ noise` → promote "anchored common scale" from heuristic to
   FORMAL CARRIER.** Name it as the Legendre potential `F` / dually flat coordinate;
   state that orthogonality and √N are *licensed by it*, not by CT alone. Without `F`,
   the honest form is `residue = bias * noise` (two entropic contributions, not orthogonal
   legs). Answers OQ-2 (rubric by `dispatch_type` = choice of `F`) and OQ-4 (the 6
   facets = dual coords `η=∇F`).
2. **`√N` → regime revision.** L2/CLT fact under `F=‖·‖²`; outside the CLT, concentration is
   Sanov/large-deviation, **not 1/N**. State √N as the special Gaussian case; the general guarantee
   = "aggregation = m-projection onto the flat family, monotone under independence," conditional exponent.
3. **Nudge process≠content → re-type (does not break).** Split the nudge vocabulary into two
   typed classes: (a) **coupling-fiber nudges** on `D(A^N)` for aggregation
   (independence, freeze-before-channel, blinding); (b) **optic/lens nudges** only for the
   per-agent explorer→reviewer pipeline (compressor≠judge). Sharpens fix 1 (freeze = kill a
   coupling of anchoring before it forms) and OQ-3 (persona = correlated prior = a
   coupling at the judging stage → neutralize = ⊗ marginalize).

## Fork guard

Both seams are **dispersion, not dissent** (`resolved`, not `dissent_irreconcilable`):
Fritz-b2 ≡ Leinster-OBS2; Jacobs subsumes Myers and both converge on the marginal-preserving morphism.
**The genuine fork to escalate is COMPOSITIONALITY** — are bias⊕noise and the nudge re-type
functorial along the composition of stages/dispatch, or only pointwise per stage? This must
become the thesis's **4th collapse-test**: *does the decomposition survive functorial composition of the
stages, or only pointwise within each stage?* Separation-by-stage is the *design*
answer; the *formal* guarantee across composition is unproven.

## Audit

Ledger `telemetry/agents/subagents-dispatch.yaml` — dispatch `2026-07-20-costura-feasibility`
(4 tensioned explorers: Fritz⊥Leinster, Myers⊥Jacobs; synthesizer Riehl). `check-tension` gate
by Loregian+Capucci (infrastructure, unregistered). Technical sources: Banerjee JMLR 2005;
Pfau arXiv 2511.08789; arXiv 2501.18581; Amari (info geometry); Smithe arXiv 2306.17009 /
2109.04461; Riley arXiv 1809.00738; Clarke et al. arXiv 2001.07488; non-monicity of
marginalization (Fritz-style Markov categories).
