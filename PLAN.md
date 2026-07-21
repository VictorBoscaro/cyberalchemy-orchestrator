# PLAN — Knowledge Machine / Agent Orchestrator (seed)

> **Repo name:** provisional (`cyberalchemy-orchestrator`). Rename.
> **Status:** PLAN / brainstorm. Unreviewed. Local, no push. Claim ≤ proof.
> This is the **lean object** — just the plan. The vault grows on top of it later.
> Origin: 2026-07-18 session with Victor, after recon of 5 probes.

---

## 0. What this object is (and isn't)

**Is:** the minimal plan to start building a vault that models **knowledge**
(what it is, properties, relations, effects, who acts on it) and, as the first
concrete piece, an **agent orchestrator**.

**Isn't:** the vault. Isn't code. Isn't a claim that something already works. Nothing
here is typed in Lean yet; where I say "it's a category / it's Yoneda," read
**candidate to type**, not a result.

---

## 1. Problem

Model knowledge with enough structure to **produce systems** — including
itself, using itself. The first executable slice of this ambition is an
agent orchestrator that investigates, synthesizes, and critiques knowledge.

**Thesis (recorded, not inflated).** The work itself is an *instance* of the
epistemological framework it studies. This is **already named** in the parent repo
(BACKLOG A6, "framework as its own instance") — it's not a new claim, it's the
self-application pointed at the process of knowledge production. Honesty: a *declared*
instance is not proof that the process obeys the framework; it's a candidate,
falsifiable description.

---

## 2. Map — raw material that ALREADY exists (the 1st job is to consolidate, not create)

| Source | What it provides | Where | Access |
|---|---|---|---|
| robot-talks | parallel investigation by *concern* + confrontation on the tension axis | `.claude/skills/robot-talks/` (Arcanum + lean-formalization) | local/public |
| subagents-strategy | router: trigger, human-gate, invariants (tension, claim≤proof) | `Arcanum` skills + `ARCANUM-SUBAGENT-STRATEGY.md` | local |
| DISPATCH-COMPOSITION-MODEL | dispatch ontology in 4 levels, **typed edges**, retry-bounded | `Arcanum/TO-VLAD/DISPATCH-COMPOSITION-MODEL.md` | public |
| MOGT | multi-objective decision layer {quality,cost,latency,safety,escalation}; "decision receipt"; Nash-bargaining regime | `Arcanum/research/mogt-agentic-conversation/` | public — **experiments not started** |
| CT track | monoidal categories / multicategories as formal framing | `Arcanum/research/monoidal-categories-multicategories/` | public |
| Pulse Orchestration | Descent/Execution/Ascent cycles, ephemeral buses, cost function (entropy/tokens/latency/fidelity) | `business-philosopher/assuntos/orquestracao-multi-agente/` | local |
| Attention economy | tokens as currency; charge by reduction-of-uncertainty-per-token | `business-philosopher/assuntos/agents-optimization/` | local |
| domainspec-language | the "system language," already CT-oriented (objects/morphisms, presheaf/Lan, FDM) | `domainspec-core/.../domainspec-language/` | local |
| definitions protocol | single-source-of-truth + per-term structure + drift-audit | `Arcanum/definitions/DEFINITIONS.md` | public |
| Lean CT anchors | residue, Yoneda-as-translation, comma-connected (zig-zag) | `domainspec-lean-formalization/lean-formalization/` | local |

**Resolved (2026-07-20):** the "micro-economy" is **MOGT**, at
`Arcanum/research/mogt-agentic-conversation/` (public), not a separate doc. It is not
an access pending item; it's the orchestrator's decision layer (see E4). Honest
correction: the name "game theory" overstates it — it's **multi-objective optimization**
(objectives {quality, cost, latency, safety, escalation_risk}, Pareto dominance, optional
`bargaining_guided` regime). Status: **design + dry-run, 0% empirical** — it inherits
"claim ≤ proof" (all claims "insufficient evidence," experiments "not started").
The greater value for us is in the surrounding **research scaffolding** (catalog/ledger/inventory/
receipt), not in the decision model itself.

---

## 3. Definitions protocol (adopted from `Arcanum/definitions/DEFINITIONS.md`)

Rule flagged by Victor as necessary. We adopt it, with one extra field.

- **Single source of truth.** A term is normatively defined in ONE place; downstream
  only explains/applies/references, never redefines.
- **Per-term structure:** Status · Term+Aliases · Scientific/Formal Voice · Operational
  Interpretation · Colloquial Voice · Domain Context · **Boundary** (what's left out) ·
  Consumers (paths) · Related.
- **Namespaced IDs** (e.g., `DEF-ORCH-*` for this repo vs. inherited `DS-*`/`DEF-ARC-*`).
- **Drift-audit:** a file that tracks divergence between the normative definition and its uses.
- **NEW FIELD — Categorical type:** each definition carries its **CT mapping + anchor**
  (see §4). A definition without a categorical type is a candidate, not closed.

---

## 4. Categorical mapping discipline (the vault's spine)

**Rule.** Every construct of the agent-language → its type in category theory +
anchor in a real file (rule inherited from the parent repo's CLAUDE.md). Probe and zig-zag
are just the first two examples.

**The table lives in [MAPPING.md](MAPPING.md)** (single source of the mapping, protocol §3): §1 = the
seed table (7 inherited constructs), §2 = the parallels derived from the base skill
`domainspec-subagents-strategy` (concat/synthesis, feedback-as-2-cell, plural-probe,
meta/A6, …). Do not duplicate here — edit there.

**Verb-rule (from Victor's direction).** A verb (implements/validates/
refines/…) is an **action on an object that should preserve the object's symmetry under
certain premises**. Honest correction from the parent repo: an *arbitrary* morphism does NOT preserve
symmetry — only isos/automorphisms preserve it, and **the loss of symmetry IS the residue**
(memory `symmetry-invertible-lever-is-enrichment`). Hence the type of a verb is:

> **verb = morphism + the condition under which it is symmetry-preserving.**
> Victor's "premises" = exactly this condition. Outside it, the verb generates residue —
> and this makes the residue **measurable per verb**, which is what gives the discipline its value.

**Strong claim (downgraded to candidate, with collapse-test).** If `groups`=objects and
typed `connections` compose associatively, the agent-language **is** a
category (not *seems like*), and the residue of an orchestration is the same object the parent repo
studies — closing the A6 loop. **Collapses the decoration** if (a) zig-zag/feedback don't compose
associatively (it's just an annotated DAG), or (b) the synthesis-residue is not the same object
as `FunctorialResidueStructure` (and not just count-shaped). Typing (a) or (b) is the **first
real obligation** — see E3.

---

## 5. Step-by-step plan (each one carries its own collapse-test)

- **E0 — this PLAN.** Done. Collapse: if it doesn't survive the consistency review, redo it.
- **E1 — minimal vault + vocabulary of moves.** README + this plan + the §4 table
  as the initial doc, anchored in `DISPATCH-COMPOSITION-MODEL.md`. *Collapse:* if the table
  doesn't close a mapping per construct, it's a glossary, not a language.
- **E2 — first definitions in protocol §3.** ~5 terms (probe, zig-zag, verb,
  residue, dispatch) written with the 9 fields + categorical type. *Collapse:* if two
  definitions need to mutually redefine each other, the boundary is wrong.
- **E3 — test the strong claim (§4).** Type (a) category laws OR (b) residue=same-object.
  *Collapse-test already built in:* if it can only be "proven" by re-displaying the diamond, it's decoration.
  This is the slice that decides whether the repo is mathematics or metaphor.
- **E4 — decision layer (MOGT) as the orchestrator's "physics."** Adopt the "decision
  receipt" and the multi-criteria objectives. *Blocked* by: (i) Vladimir's doc (access),
  (ii) MOGT having zero experiments run — inherits the same "no evidence yet."

---

## Pending items / open questions

- **P-NOME.** definitive name and location of the repo (today: provisional local sibling folder).
- **P-CT.** feedback and robot-talks still without a CT type — resolve in E2/E3.

*(Resolved: the "micro-economy" is MOGT — game theory — at
`Arcanum/research/mogt-agentic-conversation/`, not a separate doc from Vladimir. The Towers
game is a different project, outside this one.)*
