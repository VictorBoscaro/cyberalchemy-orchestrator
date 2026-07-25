---
tags: [vault, anti-bias, anti-noise, orchestration, epistemology]
node_type: axiom
is_session: false
session_ref: null
layer: ontology, domain
nature: reference
status: draft
veracity: high
conviction: high
version: 0.4.0
last_updated: 2026-07-21
---

# Axioms — the commitments taken as given

> **Status:** `draft`, unreviewed. These are **assumed**, not discharged. Per
> [[ontology-conventions]], an `axiom` is challenged with *"revisiting it breaks everything
> built on it"* — not with *"show me evidence"* (that is a `premise`). Promoting a claim here
> **removes it from test on purpose**: the research program downstream stops asking *whether*
> and starts asking *what is the best way*. Each axiom states **exactly what it does and does
> not** axiomatize, so nothing evidence-revisable is smuggled in as settled.
>
> `Claim ≤ proof` is not violated by an axiom: the certainty is declared as **assumed**, and
> every claim *made within* the method stays falsifiable. What is fixed is the frame, not the
> findings.
>
> **Revised 2026-07-20** (`2026-07-20-review-claim-graph-axioms`): AX-1 re-cut as a value
> **commitment**; the untested **agent-transfer** demoted to **P-AGENT-TRANSFER**.
>
> **Revised 2026-07-21** (`2026-07-21-root-hypothesis-tension`): "the three faces are instances of
> T0" demoted to **P-FACES-INSTANCE**; AX-3's self-similarity demoted to [[framework-self-similarity]].
>
> **Restructured 2026-07-21** (from the axiom-layer red-team, `2026-07-21-axiom-redteam-review`): the
> layer had become a **grab-bag** — three different *kinds* wearing one `axiom` label. Partitioned
> below by kind; **AX-2 fixed** (it over-claimed falsifiability as the whole method); **AX-4 (independent
> check)** and **AX-5 (fallibilism)** added as the method invariants that were missing.

## The three kinds *(the restructure, and why)*

The axiom layer was fusing three different *kinds* of foundational thing under one label — the same
fusion [[BACKLOG]] **BL-2** names (a carrier-kind ⊕ a role smuggled into one label). Separated:

- **§1 — Method invariants (the floor).** Norms you cannot drop without losing the ability to
  *correct or build at all*. Foundational to **inquiry itself** — the true "there is nowhere to walk
  without them" layer. Their stability is not "slowest-moving" but **revision-cost ∝ how much they
  load-bear** (revising one breaks everything above it). Fixed **relative to the commitment to
  inquire honestly**, not cosmically (abandon inquiry and they lapse — but then it is a different
  enterprise).
- **§2 — Value commitment (the telos).** What *this project* is *for*. Foundational to this repo,
  **not** to inquiry — a different project could drop it and still know honestly.
- **§3 — Design stance.** A distinctive *choice* of how to work. Droppable without breaking the
  method. Foundational to this repo's *character*, not to its epistemics.

Only §1 is the floor. The old flat "AX-1/2/3 are all axioms" hid that AX-1 is a *value* and AX-3 a
*choice* — neither is a method invariant.

---

## §1 — Method invariants (the floor)

### AX-2 — Accountability: revision under type-appropriate warrant

**Assumed as the operating method.** The repo runs the loop **state a claim → probe it → keep what
survives → enrich the model from what breaks** — where "probe/keep" means holding the claim to the
**warrant appropriate to its type**, asserting no more than that warrant supports (`claim ≤ proof`).
This loop is the **T0 root**; the method is the substrate, not a hypothesis under test — it is what
lets a collapse-test *mean* something.

- **Correction (2026-07-21):** the warrant is **type-indexed**, not falsification alone —
  falsification is only the **empirical slice**. Its faces: **falsify** (empirical), **prove**
  (mathematical / a Lean anchor), **ground-by-use/coherence** (definitional), **owner + gate**
  (decisional). For an *applied* formalism the warrant **composes**: `proof ∘ falsification` — proof
  warrants internal consistency, falsification warrants that the formalism *represents* the real
  phenomenon (this repo is all-applied, so the composition is the rule; see [[axiom-layer-redteam]]).
- **Not axiomatized (kept open, not smuggled):**
  1. **Generation** — "state a claim" contains a creative act (conjecture/abduction) that is
     **pre-methodological** ("no logic of discovery"): the method *disciplines* which conjectures are
     admissible; it does not *produce* them. Governed by this layer, not a member of it.
  2. That the **three faces are instances** of T0 — evidence-revisable, lives as **P-FACES-INSTANCE**.
- `veracity: high` · `conviction: high`.

#### P-FACES-INSTANCE — *(premise, not axiom)* the three faces are instances of T0

`node_type: premise` · `veracity: low` · `conviction: medium`. **Working bet:** each face —
decision-science ([[anti-noise-orchestration]]), categorical (FRAMINGS / MAPPING / OBLIGATIONS),
engineering (dispatch / ledger / check-tension) — is a **faithful instance** of T0: a
structure-preserving map sending each root operation (state → probe → keep → enrich) to a **named**
operation of that face, preserving order and a **non-vacuous** falsification step. **Falsifier
(functor, not label):** false if ≥ 1 face has a root operation with no faithful correspondent, if a
correspondence is drawn only *post-hoc*, or if the shared root never **moves a design decision**. A
merely applicable label is not a survival (the [[anti-noise-orchestration]] `OQ-9` immunization guard
turned on ourselves). **Pre-registration (per `OQ-11`):** the correspondence map is frozen in
[[faces-instance-frozen-map]]. **Status (2026-07-21):** decision-science and categorical faces
complete; the **engineering face's `enrich` op has no correspondent at the current ledger design**
([[close-row-enrich-c]]) — a **partial fire** pending **BL-3**; the decision-moving disjunct is
pre-registered there but **binding was deferred by the owner** — so this premise rests on the map
falsifier alone.

### AX-4 — Independent check *(the anti-bias norm)* — new

**Assumed as a method norm.** Treat the knower as a **biased instrument**: every load-bearing
conclusion is subject to an **independent / adversarial check** before it is relied on. This is what
self-honesty (AX-2) cannot catch alone — an honest reading of your own evidence is still *your*
reading. It is the norm the machine's `check-tension` gate and opposed-reviewer dispatches
*implement*; "independent reviewers" is its operative face.

- **Distinct from AX-1 (deliberately).** AX-1 is the *goal* of reducing bias (what the project is
  for). AX-4 is the *method-norm* of checking, which holds **even if** debiasing were not the mission
  — you check because you are fallible, not because bias-reduction is your telos.
- **Not axiomatized:** any *particular mechanism*. "Ensemble independent LLM judgments cancel error"
  rests on Condorcet conditional-independence, which a **shared base model violates** (correlated
  errors cap what independence buys). The mechanism is content — the live premise **P-AGENT-TRANSFER**
  and the optimization handed to [[anti-noise-orchestration]] (`HYP-ORCH-NOISE`). The **norm** is the
  invariant; the **mechanism** is under test. Demoting the mechanism does not touch the norm.
- `veracity: high` (as a norm; not the operative dimension) · `conviction: high`.

### AX-5 — Fallibilism — new

**Assumed.** Everything **except these method invariants** is revisable by what survives testing —
the vocabulary, the schemas, the categorical framing, and the meta-ontology's **own levels** (no
fixed meta-level; the governance recursion, `H-META-1'`). The one thing not up for revision is
**that everything else is.** This is the "nothing is fixed" correction, self-applied — what
distinguishes a knowledge machine from a fixed ontology.

- **Not a contradiction with §1's fixedness:** the invariants are fixed *as the frame of the
  enterprise* (the rules of the game), not as a *level of content* (a move). F6 / `H-META-1'` forbid
  a terminal codomain of **content**; they do not govern the enterprise-constituting frame.
- `veracity: high` · `conviction: high`.

---

## §2 — Value commitment (the telos — **not** a method invariant)

### AX-1 — Debiasing is worth pursuing *(a value commitment)*

**A value/goal, not an empirical prediction and not a method invariant.** Reducing correlated
**bias** and **noise** in judgment is a goal worth building the orchestrator around. Challenged by
*"is this goal worth pursuing?"* — not by *"show me it works."* Held **regardless of proven
achievability**. This is *what the project is for*; a different project could drop it and still do
honest inquiry (that is why it is §2, not §1).

- **What this axiomatizes:** the *value*, grounded in decision science (Kahneman on bias/noise).
- **What this does NOT axiomatize:** (1) **Agent-transfer** — that the human value carries to
  *agents* — lives as **P-AGENT-TRANSFER**; (2) **Efficacy** — that any countermeasure cancels bias
  rather than relabels it — handed to [[anti-noise-orchestration]].
- `conviction: high`. Veracity is not the operative dimension for a commitment.

#### P-AGENT-TRANSFER — *(premise, not axiom)* the value transfers to agents

`node_type: premise` · `veracity: low` · `conviction: high`. **Working bet:** agent judgment
inherits enough of the human bias/noise structure that debiasing *agents* is worthwhile.
**Falsifier:** if agents' correlated bias on a shared base model is effectively irreducible — no
countermeasure measurably beats the single-agent baseline — the transfer fails and AX-1's *agent
applicability* collapses (the value survives; its relevance to this project would not). This is also
the **mechanism half of AX-4** under test.

---

## §3 — Design stance (a distinctive choice — **not** a method invariant)

### AX-3 — Framework as its own instance

**A design decision, not a method invariant.** Already named in the
[`archived roadmap §1`](../../plans/governed-agent-work-infrastructure/archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) (A6):
the work of building this repo is recorded in the same ledger it operates. You could drop
self-recording and still have an honest method — so this is §3, a *choice* that gives the repo its
character, not part of the floor. What AX-3 fixes is only the **stance/decision** to self-record. Its
**reflexive claims** — that the knowledge-ascension loop and the orchestration loop are the *same
structure* at different scales (self-similarity / fractality) — are evidence-revisable and live as
the falsifiable hypothesis [[framework-self-similarity]] (`HYP-ORCH-FRACTAL`), not here.

---

## Consequence — validation → optimization

Fixing §1 (and §2's value) **re-poses** the downstream program. *"Is debiasing / the scientific
method worth it?"* is closed by decree; *"what is the **best** architecture of dispatch, tension,
freeze, aggregation, and claim-typing to serve them?"* is the open work. Two efficacy conditions
survive as **collapse conditions, not assumptions**:

- **∀-method** (per-method): "best way" does **not** assume any *particular* method succeeds.
- **∃-method** (existential): "best way" **does** presuppose at least one countermeasure measurably
  beats the single-agent baseline. If **no** method clears baseline, the optimization is empty and
  AX-1's agent applicability (P-AGENT-TRANSFER) collapses. Stated so the existential assumption is
  explicit and falsifiable, not silent.

> **Reconciliation in progress (2026-07-21).** [`README.md`](../../README.md) now states the split
> explicitly — the **value** (debiasing is worth building around) as a commitment, and
> **agent-transfer + efficacy** as the falsifiable part — matching this axiom's partition; the same
> split is drawn as the method-vs-content distinction in
> [`plans/governed-agent-work-infrastructure/PLAN.md`](../../plans/governed-agent-work-infrastructure/PLAN.md)
> §2. The
> distinction is now named on both sides; what remains is the promotion decision itself — neither
> presupposed as the side that yields — before either moves up a level.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[anti-noise-orchestration]] | `grounds` | AX-1 hands it the "best way" optimization; the AX-4 *mechanism* (efficacy of independent checking on shared-base-model agents) is the open thesis here. |
| [`Knowledge Machine and Agent Orchestrator Seed Roadmap`](../../plans/governed-agent-work-infrastructure/archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) | `derives-from` | §1 already names A6; AX-3 records the *stance* in the axiom layer (§3). |
| [[claim-graph]] | `grounds` | AX-2 (the method root) is what the claim-graph mechanizes: veracity propagation + `contradicts` as the enrichment engine. |
| [[framework-self-similarity]] | `grounds` | AX-3's stance grounds it; the reflexive self-similarity claim was demoted here (`HYP-ORCH-FRACTAL`), which `depends-on` P-FACES-INSTANCE. |
| [[axiom-layer-redteam]] | `derives-from` | The three-kinds partition, AX-2's type-appropriate-warrant fix, and AX-4/AX-5 come from its reconciled landing. |
| [[BACKLOG]] (BL-2) | `exemplifies` | This restructure is BL-2 (de-fuse kinds under one label) applied to the axiom layer itself. |
| [`README.md`](../../README.md) | `contradicts` | ⚠️ Narrowed (2026-07-21): README now states the value/efficacy split explicitly; the residual is only the pending promotion decision (which side yields), still open before either moves up. |
| [[ontology-conventions]] | `depends-on` | Uses its `axiom` vs `premise` distinction and confidence dimensions. |
