---
tags: [plans, orchestration, archived-roadmap]
node_type: plan
name: Knowledge Machine and Agent Orchestrator Seed Roadmap
plan_id: null
identity_status: archived-name-only
plan_role: archived-predecessor
related_root_plan: plans/governed-agent-work-infrastructure/PLAN.md
status: superseded
version: 0.3.0
authority: proposal-only
authority_resolution:
  status: unknown
  search_note: archived artifact; no durable governing-authority receipt was found in the artifact
last_updated: 2026-07-24
---

# Knowledge Machine and Agent Orchestrator Seed Roadmap

> **Repo name:** provisional (`cyberalchemy-orchestrator`). Rename (P-NOME, still open).
> **Status:** PLAN / brainstorm. Unreviewed. Local, no push. Claim ≤ proof.
> This is the **lean object** — the plan. Origin: 2026-07-18 session with Victor, after recon of 5 probes.
> **Re-anchored 2026-07-21 (v0.3).** After a deep read of the grown vault, the spine is no longer the
> old E0–E4 step list. It is now stated as what it actually is: **one engine (the T0 loop) with three
> faces**, a **binding spine that is still missing**, and **two roadmap tracks**. The framing (§0–§4) is
> mostly inherited unchanged; §5–§8 are the re-anchored spine. Everything stays under `claim ≤ proof`.

---

## 0. What this object is (and isn't)

**Is:** the minimal plan to build a vault that models **knowledge** (what it is, its
properties, relations, effects, who acts on it) and, as the first concrete piece, an
**agent orchestrator**. Read as a single **engine**: *state a falsifiable claim → probe it →
keep what survives → enrich the model from what breaks* (the **T0 root loop**, §5), whose
first executable slice is an orchestrator that counters bias and noise.

**Isn't:** the vault. Isn't (mostly) code — one read-only slice runs (§6), the rest is thesis.
Isn't a claim that something already works. Nothing here is typed in Lean; where it says "it's a
category / it's Yoneda," read **candidate to type**, not a result.

---

## 1. Problem

Model knowledge with enough structure to **produce systems** — including itself, using itself.
The first executable slice is an agent orchestrator that investigates, synthesizes, and critiques
knowledge.

**Thesis (recorded, not inflated).** The work itself is an *instance* of the epistemological
framework it studies (BACKLOG A6, "framework as its own instance"). Honesty: a *declared* instance
is not proof that the process obeys the framework; it's a candidate, falsifiable description. It has
since been split: the **stance** to self-record is fixed as a design posture (AX-3), while the
**reflexive content claim** (that building the repo *is* the same loop) was demoted to a private,
falsifiable hypothesis whose current-design instance is already **falsified** — see §5 and
[[framework-self-similarity]].

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
| Lean CT anchors | residue, Yoneda-as-translation, comma-connected (zig-zag) | `domainspec-lean-formalization/lean-formalization/` (**sibling repo — not in this repo**) | local |

**Resolved (2026-07-20):** the "micro-economy" is **MOGT**, at
`Arcanum/research/mogt-agentic-conversation/` (public), not a separate doc. Honest correction: the
name "game theory" overstates it — it's **multi-objective optimization** (objectives {quality, cost,
latency, safety, escalation_risk}, Pareto dominance, optional `bargaining_guided` regime). Status:
**design + dry-run, 0% empirical**. Its greater value for us is the surrounding **research
scaffolding** (catalog/ledger/inventory/receipt), not the decision model itself. It is the orchestrator's
future decision layer — parked, not on the critical path (§7, Track B).

---

## 3. Definitions protocol (adopted from `Arcanum/definitions/DEFINITIONS.md`)

- **Single source of truth.** A term is normatively defined in ONE place; downstream only
  explains/applies/references, never redefines.
- **Per-term structure:** Status · Term+Aliases · Scientific/Formal Voice · Operational
  Interpretation · Colloquial Voice · Domain Context · **Boundary** (what's left out) · Consumers ·
  Related.
- **Namespaced IDs** (`DEF-ORCH-*` here vs. inherited `DS-*`/`DEF-ARC-*`).
- **Drift-audit:** a file tracking divergence between the normative definition and its uses.
- **NEW FIELD — Categorical type:** each definition carries its **CT mapping + anchor** (§4). A
  definition without a categorical type is a candidate, not closed.

Terms live in [DEFINITIONS.md](../../../definitions/DEFINITIONS.md) (residue, separation, shadow, probe, verb, …).
Honest state: several anchors are **weak** — memory-level or own-synthesis, with no Lean declaration
(verb-rule, shadow-as-magnitude, the probe species). These are labeled inline; they are candidates, not results.

---

## 4. Categorical mapping discipline (one of the three faces, §5)

**Rule.** Every construct of the agent-language → its type in category theory + anchor in a real
file (inherited from the parent repo's CLAUDE.md).

**The table lives in [FRAMINGS.md §2](../../../FRAMINGS.md#2--interpretation-functor)** (single source, protocol §3): §1 = seed table (7
inherited constructs), §2 = parallels from the base skill `domainspec-subagents-strategy`
(concat=coproduct / synthesis=pushout, feedback-as-2-cell, plural-probe=separating-family, meta/A6).
Do not duplicate here — edit there.

**Verb-rule.** A verb is an **action on an object that preserves the object's symmetry under certain
premises**. Only isos/automorphisms preserve symmetry; **the loss of symmetry IS the residue**
(memory `symmetry-invertible-lever-is-enrichment`). Hence:

> **verb = morphism + the condition under which it is symmetry-preserving.**
> Outside the condition the verb generates residue — making the residue **measurable per verb**.

**Strong claim (candidate, with collapse-test).** If `groups`=objects and typed `connections`
compose associatively, the agent-language **is** a category, and the residue of an orchestration is
the same object the parent repo studies — closing the A6 loop. **Collapses to decoration** if (a)
zig-zag/feedback don't compose associatively (it's an annotated DAG), or (b) the synthesis-residue
is not the same object as `FunctorialResidueStructure` (and the discharge reaches only the
*separation* bar, not the invariant-factor prize). Typing (a) or (b) is [OBL-E3](../../../OBLIGATIONS.md) (§8).

---

## 5. The engine — the T0 loop and its three faces *(the re-anchored spine)*

Everything below is **one loop seen three ways**.

### 5.1 The T0 root loop
`state a falsifiable claim → probe it → keep what survives → enrich the model from what breaks`
(`vault/axioms/axioms.md`, T0 root; categorical form = [FRAMINGS.md](../../../FRAMINGS.md) **F6**: anomaly →
enrich `C` → shrink residue = "the scientific process"). The governing discipline — `claim ≤ proof`
and `veracity ⊥ conviction` — already runs through every doc and the code (EG-8). **But the loop
itself is NOT built.** The `enrich` step is *provably absent* from the current ledger: a close row
carries only a closed `exit_reason` enum + counts + verbatim strings — never a change to the model
`C` ([[close-row-enrich-c]]). What runs today is the *read* half of one face (§6); the enrich engine
is the thing to add (§7).

### 5.2 The three faces (P-FACES-INSTANCE — each a *candidate* faithful instance of T0)

| Face | The loop, in that language | Home | State |
|---|---|---|---|
| **Decision-science** | claim = a debiasing move; probe = tensioned/independent dispatch; residue = `bias ⊕ noise` | [[anti-noise-orchestration]] (`HYP-ORCH-NOISE`) | candidate, low veracity; `⊕`-orthogonality partially deflated (holds only under an imported Legendre `F`, else `bias × noise`) |
| **Categorical** | claim = a construct's CT type; probe = an active map `A→X`; residue = `FunctorialResidueStructure` | [FRAMINGS.md §2](../../../FRAMINGS.md#2--interpretation-functor) + [OBL-E3](../../../OBLIGATIONS.md) | OPEN; nothing typed *here* — anchors live in the **sibling** repo, build-gate unverified |
| **Engineering** | claim = a schema/invariant; probe = a dispatch; residue = what a synthesis merge loses | `implementations/` + the ledger + [[engine-constitution]] | Phase-1 read runs; the `enrich` op **has no correspondent** — partial fire ([[faces-instance-frozen-map]]) |

**A6 / self-reference.** Building the repo through dispatches recorded in the *same* ledger is real,
but its claim-content — that the build loop and the ascension loop are the **same structure** — is a
private, gated hypothesis whose current-design instance is **FALSIFIED** ([[framework-self-similarity]],
falsifier 1 fired 2026-07-21: no close row enriches `C`). It becomes runnable only after the missing
spine (§5.3) exists. The stance to self-record survives as design posture AX-3.

### 5.3 The binding spine that is still missing *(the crux)*
The three faces are only "the same loop" if a **provenance spine** ties them: `assertion → the
dispatch/research that generated it → its trail`. Today that spine is **absent** — four disjoint
id-spaces (documents, epistemic ledger, operational trace, domain) with no typed cross-link
([research/meta-ontology/](../../../research/meta-ontology/) SEED). The same gap explains three symptoms at once:
the missing `enrich` step (5.1), the falsified fractality (5.2), and the meta-ontology's non-convergence.
It has a name in the backlog: **BL-3 — the ledger as a typed, `enrich`/`supersede`-capable knowledge
graph**. BL-3 is the **pivot unlock**: it lands the enrich step, [[claim-graph]], fractality, and the
meta-ontology convergence in one move.

---

## 6. What runs today vs. what is thesis (2026-07-21)

"Runs" = built + tested, not proven-correct.

**Runs (the substrate — one read-only slice).**
- **Dispatch discipline** — agent groups, typed connections, the `check-tension` anti-bias gate
  (fires only for n≥2 investigate/evaluate groups), append-only ledger, strict Node appender.
- **Control plane — Phase 1 (read).** FastAPI + SSE (`implementations/server/`) with **10 UI variants**
  that live-read the pending sheet + the ledger. Serious test coverage (parser, endpoints w/ mutant
  checks, a Playwright UI-contract over all ten). Load-bearing design: **appender-strict ⊥ reader-lenient**.
- **agent-pool MCP** (`tools/agent-pool-mcp/`) — 414 entries, deterministic core + cheap Haiku frontier, cross-repo.

**Thesis (paper, not proven).** The categorical typing (§4, MAPPING, OBLIGATIONS) and the
decision-science loop (§5.2). Candidates under `claim ≤ proof`.

**The keystone blocker.** [[ledger-enum-drift-finding]]: two 2026-07-18 close rows carry an
out-of-enum `exit_reason: "success"` that could only have **bypassed** the validated appender —
despite the append-only hook. This holds [[engine-constitution]] **EG-1** ("one writer") at
`veracity: medium`, **promotion-blocked**, and it **blocks Phase 2** (the UI Dispatch button that
*writes* — present but `disabled` by contract). The infra hypothesis's "bus is a projection, not a
second store" leans on EG-1 and inherits the same hole. Repair path is documented and reviewer-verified.

**Portability caveat.** "Droppable into any repo" is true of the *architecture* (structural parser,
auto-discovery, canonical MCP), but the *substrate today* is hardwired to one Windows operator
(`C:/Users/victo`, PT labels, ported pool provenance). Asserted + partially engineered, **not
demonstrated** on a second machine (see memory `portability-install-principle`).

---

## 7. Roadmap — one ordered BUILD plan

> **ROADMAP ≠ BACKLOG.** This is the ordered, dependency-aware plan of *what to build and in what
> order* — not the candidate pool. Parked candidates live in [BACKLOG.md](../../../BACKLOG.md) (BL-1/H-META-1′,
> BL-2, BL-4, MOGT, de-hardwire portability, OQ-9/OQ-10, README-vs-AX-1) and graduate here only by
> becoming an `OBL-*`, a `vault/hypothesis/` doc, or a numbered step below — never by silent
> implementation. **BL-3** has graduated via its step here; its BACKLOG status line (still "IDEA/parked")
> is reconciled as a sub-task of D-1.
>
> **Tags.** `[BUILD]` writes/repairs a runnable artifact · `[PROOF]` discharges/falsifies a claim (Lean
> or reproduction) · `[PROOF/DIAG]` empirical reproduction, not CT-track proof capital · `[DESIGN]` a
> governed decision, no code.
>
> **Critical path:** `FT-1 → B-1 → B-3 → B-4`, with **D-1** running parallel from the start (only B-3
> consumes it). **Track B** (`TR-2 → FT-2 → P-1`) is fully parallel and gates only the categorical /
> fractality *claims* — never the engine.
>
> *Provenance: this roadmap was produced by a dogfooded dispatch (`2026-07-21-roadmap-build-order`) —
> two opposed drafters → synthesizer → two opposed reviewers (both FAIL) → one revision → final approver
> ACCEPT. A6 in practice.*

### Phase 0 — cheap falsification + transversals *(parallel, no build capital)*

- **FT-1 — Enum-drift causal trace.** `[PROOF/DIAG]` · **critical path.** Establish *how* the two
  2026-07-18 `exit_reason:"success"` close rows entered. Correct gate: `exit_reason` is validated by
  `validateClose` (`append-dispatch.cjs:242`, dispatched via `isClose`), **not** `validateDispatch`
  (`:137`, dispatch rows only). Three exhaustive outcomes: **(i)** a live out-of-band write path is
  reproduced; **(ii)** the rows were written by an *older* appender whose `validateClose` lacked the enum
  check, or with the append-only hook absent/disabled that day — **EG-1 intact, no re-adjudication**;
  **(iii)** proven impossible. Must inspect appender git history + hook state at 2026-07-18. *Done:* one
  of (i)/(ii)/(iii) established with evidence. *Deps:* none. *Collapse:* only (i) forces EG-1
  re-adjudication and scopes B-1; (ii)/(iii) leave EG-1 intact.
- **FT-2 — OBL-E3 sub-3.** `[PROOF]` · parallel (Track B). Type `synthesize` as a pushout clearing
  `separation_is_functor_action` (`FunctorialResidueStructure.lean:545`) on the ORCH substrate. *Done:*
  the separation-bar factorization type-checks + `#print axioms` clean + assoc/identity on the
  `sequential` fragment. *Deps:* TR-2. *Ceiling (binding):* the **separation** bar only — **not** the
  invariant-factor prize (`tierC_pigeonhole_not_injective` closed-negative over concrete `Ab`); do **not**
  record sub-3 as settling fractality or the zig-zag/feedback 1-morphism question. *Collapse:* (a)
  zig-zag/feedback don't compose → category only on the sequential fragment; (b) count-shaped residue → analogy → 0.
- **TR-1 — Verify + re-point the `TO-ME/` brief.** `[BUILD]` · parallel. *Done:* (1) confirm the brief
  exists at `../domainspec-lean-formalization/TO-ME/oble3-synthesis-as-second-residue-instance/` (it does);
  (2) every in-repo `TO-ME/…` citation resolves to that sibling path; (3) OBLIGATIONS.md's "physically
  absent" wording is corrected to match on-disk reality. *Deps:* none.
- **TR-2 — Verify sibling Lean build-gate.** `[PROOF]` · parallel. *Done:* `lake build` green +
  `#print axioms` clean @ `6edb664`; the build-unverified caveat is lifted or the anchors demoted. *Deps:*
  none. *Collapse:* gate fails → typed anchors revert to candidate → FT-2 blocked.

### Phase 1 — secure the spine *(critical path)*

- **B-1 — Enum-drift repair + EG-1 disposition.** `[BUILD]` · **keystone.** Scoped by FT-1's outcome —
  no step presupposes one. *Builds:* if FT-1=(i), close the reproduced write path; if (ii)/(iii), record
  the finding and re-promote or amend EG-1. Add the sole-writer guard the constitution names
  (`engine-constitution.md:132`), with its ceiling stated in-file **conditional on FT-1**: a Python check
  covers only the reader (`ledger.py` never writes) and cannot stop a manual edit — under (i) the hook
  exists yet was bypassed (identify + close the vector); under (ii) the vector is the hook-off window, not
  a bypass, and EG-1 is intact; under (iii) no vector exists. Fold in the **mis-anchor correction**:
  re-point `engine-constitution.md:120,132` and `ledger-enum-drift-finding.md:54` from `validateDispatch`
  to `validateClose` for the close-row path; the guard covers **both** row kinds. Extend `audit_enums.py`
  with grandfathering logic (today it flags all offenders indiscriminately). *Done:* `audit_enums.py`
  (with grandfather logic) shows **zero non-grandfathered** offenders; the two 2026-07-18 rows are
  explicitly annotated as known + quarantined (append-only — true removal deferred to BL-3 `supersede`);
  the mis-anchor is corrected in both docs; EG-1 is re-promoted above `veracity:medium` or formally
  amended. *Deps:* FT-1.

### Phase 2 — write path + ledger design

- **B-2 — Phase-2 confirm bridge.** `[BUILD]` · parallel with D-1/B-3. `POST /confirm` on the (currently
  GET-only) FastAPI server writes a pending-CONFIRM **signal file** — not a ledger row, not a second
  store; a separate agent session polls/`Monitor`s it and runs check-tension → register → agents → close
  through the validated appender. *There is no running-orchestrator wakeup primitive today* — the bridge
  is POST-writes-signal-file + agent-polls; do not assume a long-running Claude is present. Flip the
  disabled button. *Done:* a confirmed dispatch round-trips to exactly one validated close row; the
  server/button write only the signal file. *Deps:* B-1 (never enable a write trigger over an unsecured spine).
- **D-1 — BL-3 type-system + event-envelope decision.** `[DESIGN]` · critical-path feeder, **no dep on
  B-1.** Decide OQ-3 (event envelope), OQ-5 (node alphabet + edge catalog + per-type schema), OQ-2
  (governance labels), `supersede`/`amend` semantics + the provenance edge (`SEED.md:109-131`); reconcile
  BL-3's BACKLOG status line. *Done:* a `decision-gate` record fixing the alphabet/edges/envelope. *Deps:*
  none — the OQ set is orthogonal to the drift repair and runs parallel to FT-1/B-1.

### Phase 3 — build the pivot *(critical path)*

- **B-3 — BL-3 typed-graph ledger + `enrich`/`supersede` + provenance spine.** `[BUILD]` · **pivot.** The
  append-only typed knowledge graph (nodes = assertions/hypotheses/definitions/premises/decisions; typed
  edges) under System A's discipline; `supersede` **appends, never mutates** (this is what finally lets
  B-1's quarantined rows be superseded); the provenance spine links assertion → generating
  dispatch/research → trail across the four id-spaces. *Done:* every assertion resolves to a **non-empty
  provenance trail** terminating in a recorded dispatch/research event; `supersede` appends without
  mutating. *Deps:* B-1, D-1. *Collapse:* orphan assertions with no recoverable generating event → trail
  guarantee decorative → halt.

### Phase 4 — mechanize + conditional re-test

- **B-4 — Mechanize the T0 `enrich` loop on BL-3.** `[BUILD]` · the engine becomes an engine. *Done:* ≥1
  close **demonstrably adds a distinction/type the schema did not previously carry** (structure, not
  shadow), traceable to its triggering dispatch. *Deps:* B-3, B-2. *Collapse:* enrich reduces to
  annotation → engine stays read-half only.
- **P-1 — HYP-ORCH-FRACTAL re-test.** `[PROOF, conditional]` · parallel (Track B tail). *Deps:* **full
  OBL-E3 adjudication of the composition/1-morphism question** (not merely FT-2's separation bar) + B-3 +
  B-4. *Abort/narrow* if **either** OBL-E3 collapses to the sequential fragment (the likely outcome
  *falsifies* the full-loop ≡, leaving at most a narrowed sequential sub-claim to re-test) **or** FT-2
  collapses. *Retirement trigger:* if OBL-E3 is never adjudicated, retire the hypothesis when the
  substrate is declared stable (Phase 2 ships) — do not carry indefinitely. Fractality is already
  adjudicated-falsified at current design; P-1 only re-opens after the spine lands.

---

## 8. Obligations & open defects

- **OBL-E3** — is the orchestration language a category? OPEN, scoped 2026-07-21: dischargeable at the
  *separation* bar (genuine second instance), **not** the *invariant-factor* prize (count-invisible;
  closed-negative over concrete `Ab` by `tierC_pigeonhole_not_injective`; open only for a non-concrete
  codomain). Named risk: zig-zag/feedback are probably 2-cells, not 1-morphisms → the claim may narrow to
  the `sequential` fragment. Full statement + collapse-tests: [OBLIGATIONS.md](../../../OBLIGATIONS.md).
- **Enum-drift / EG-1** — the keystone defect (§6). Blocks Phase 2. [[ledger-enum-drift-finding]].
- **Missing provenance spine / BL-3** — the reason the loop can't `enrich` and fractality is falsified (§5.3).
- **`TO-ME/` citation path** — the OBL-E3 brief **exists** cross-repo (`../domainspec-lean-formalization/TO-ME/oble3-synthesis-as-second-residue-instance/`); in-repo citations use the bare path and OBLIGATIONS.md still calls it "absent" — reconcile (roadmap TR-1).
- **P-NOME** — the repo's definitive name + location, still open.
- **P-CT** — feedback/robot-talks CT type: **advanced** ([FRAMINGS.md §2](../../../FRAMINGS.md#2--interpretation-functor): feedback=2-cell,
  synthesis=colimit), still needs typing in Lean (that's OBL-E3).

## Open Questions

This Plan is superseded. The obligations and open defects above remain historical question records;
their current status must be resolved in active owning artifacts rather than by reviving this
archived route implicitly. The governing authority of this archived Plan remains unknown.
