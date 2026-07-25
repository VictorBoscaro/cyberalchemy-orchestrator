---
tags: [plans, infrastructure, orchestration, decision-hygiene, category-theory]
node_type: plan
plan_type: infrastructure-program
name: Governed Agent Work Infrastructure
plan_id: null
identity_status: named-id-pending
status: active
version: 0.2.0
authority: proposal-only
authority_resolution:
  status: resolved
  authority_kind: repository-owner
  basis: explicit owner direction that the child work belongs to one infrastructure Plan
last_updated: 2026-07-25
---

# Governed Agent Work Infrastructure

## Plan boundary

This is the single root Plan for creating the repository's governed agent infrastructure.
Decision hygiene explains why the infrastructure exists; the agent-language research program,
runtime/ACI work, observability, control-center work, and bounded implementation slices are
children, evidence nodes, or projections of this Plan rather than peer root Plans.

Its current child-Plan registry is:

| Child | Role in the infrastructure Plan | Authority state |
|---|---|---|
| [Agent Work Language Research](subplans/agent-work-language-research/PLAN.md) | Research subplan for the common language, kernel, relations, authority, events, agents, plans, and observability | Resolved repository-owner authority; proposal-only |
| [Brokered Agent Launcher Capability Bootstrap](workstreams/brokered-agent-launcher-capability-bootstrap.md) | Bounded implementation workstream for the launcher capability bootstrap | Governing authority unknown; inert as a binding route |

The archived [Knowledge Machine and Agent Orchestrator Seed Roadmap](archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) is a predecessor
artifact retained for provenance, not a live sibling Plan.

## Orientation — orchestrating agents as a decision-making problem

> **Status:** orientation / brainstorm, **unreviewed**, local (no push).
> `Claim ≤ proof`: every statement holds only as far as the linked artifact supports it. Read
> "is a category" / "reduces noise" as *a claim we hope to show*, not as a result. **Nothing in
> *this* repo is typed in Lean**; the anchors point to theorems in the sibling repo
> `domainspec-lean-formalization`, indexed in [`lean-formalization/`](../../lean-formalization/README.md) —
> formalized and sorry-free per source, though we have not re-run their build gate, and a
> formalized Lean object is not evidence that any orchestrator obeys it.
>
> This is a high-level orientation — business → hypothesis → the three fronts → what runs vs.
> what is still thesis → what we are still gathering. It replaces the old dense root `PLAN.md`
> (retired to this Plan's [`archive/`](archive/), which keeps the detailed roadmap and its codes:
> OBL-E3, BL-3, EG-1, the FT/B/D phases). The codes live there; the shape lives here.

---

## 1. The business problem

When you fan a piece of work out to several LLM agents, what comes back is only as good as the
**judgment** behind it. Our hypothesis is that multi-agent judgment fails the way human judgment
fails — three failure modes we expect, and are trying to test rather than assume:

- **Correlated bias** — agents on the same base model may agree too readily and share blind spots,
  so N of them could be closer to one look repeated than to N independent looks.
- **Noise** — their answers scatter for reasons unrelated to the task (phrasing, ordering,
  sampling); that dispersion is invisible unless it is measured.
- **Framing** — how the question is posed may steer the downstream answers, so an ill-posed frame
  could poison the pipeline before any agent starts.

If those hold, a consequence we bet on (but have not shown) follows: what helps is not *more*
agents but *structurally different* ones — paired on deliberately opposed angles, kept blind to one
another, their independent judgments aggregated rather than fused.

**A ceiling we state up front.** Agents sharing a base model produce correlated errors, which
limits how much independence can buy — we do not yet know by how much. So the open question is not
only "do these failures occur" but "do the countermeasures actually *cancel* them, or only relabel
them." We think it is worth pursuing because each failure it names has a known countermeasure in
decision science, which at least turns "orchestrate agents well" into moves that can be stated and
falsified.

---

## 2. The hypothesis

> **Working hypothesis.** Treat the orchestrator's job as *decision hygiene*, try to give that
> hygiene *category-theoretic types* — and run both inside one *method*: hold every claim to the
> warrant its type supports, keep what survives, enrich from what breaks. The method is the frame,
> not a bet; the two theses inside it are the bets, and the second is the more speculative.

Three parts — and the first is the **frame** the other two run inside, not a third peer:

- **The method (the frame).** The repo operates one loop — **state a claim → probe it → keep what
  survives → enrich the model from what breaks** — holding each claim to no more than the warrant
  its *type* supports (`claim ≤ proof`). Falsification is the *empirical* slice of that warrant, not
  the whole: a claim can also be discharged by proof (a Lean anchor), by grounded use (a definition),
  or by an owner's gate (a decision). This is the **T0 root** — fixed *as the frame of the
  enterprise*, the one thing not itself under test, so that a collapse-test can *mean* something
  ([`vault/axioms/axioms.md`](../../vault/axioms/axioms.md), AX-2, with AX-4 *independent check* and
  AX-5 *fallibilism* as the other two method invariants). It is not aspirational: the discipline
  already runs (every construct below carries a collapse-test; every belief carries `veracity` held
  apart from `conviction`). What is **not** built is the *automated* form of this loop — see the coda.
- **Decision hygiene (the moves).** Borrowed from the science of judgment: **Kahneman** on *bias
  and noise* (two errors that may be independent, each calling for a different tool) and **Thaler**
  on *nudges* (making the hygienic path the default). This is where the concrete moves come from —
  opposed lenses, independence, aggregation-rather-than-fusion, freeze-before-you-discuss,
  fork-guard. Most of these are argued, not yet built (§3.1).
- **Category-theoretic types (the more speculative half).** The bet is that giving these moves
  types would let us say more precisely what a judgment loses and when aggregating a set of
  judgments adds information rather than noise. The candidate typings: a probe as a generalized
  element (Yoneda); a synthesis as a pushout whose non-invertible unit would be the **residue**
  (what the merge lost); feedback as a 2-cell rather than a plain edge. These are candidates to be
  checked, not results — see the open obligation in §3.2.

**The coda — the loop as a *machine*, still unbuilt.** The method above already runs *by hand*: the
scientific process is the frame we work inside, not a future feature. What is not built is its
*automated* form — a claim entering the ledger → surviving refutation attempts → connecting into a
"golden" graph of held-true nodes, reopenable when a sharper test family arrives. That machine is
**not built yet**. What already runs is the surrounding discipline (`claim ≤ proof`; every construct
paired with a collapse-test), not the machine.

**Two caveats we do not want to bury:**
1. The category-theoretic typing is **candidate for us, though partly formalized elsewhere**.
   Nothing is typed in Lean *in this repo*. The constructs it leans on (probe→Yoneda,
   residue→`FunctorialResidueStructure`, zig-zag→comma-connected) are formalized — and sorry-free
   per source — in the sibling repo `domainspec-lean-formalization`; the pointers are indexed in
   [`lean-formalization/`](../../lean-formalization/README.md). Two limits stay honest: we have not
   re-run the sibling's full build gate, and a formalized Lean object is not evidence that any
   orchestrator obeys it. In particular, the synthesis-residue instance closest to our OBL-E3
   reaches only a "separation bar" already owned there — not the count-beating prize.
2. The bias/noise split is **conditional, not free**. It separates cleanly only under a particular
   loss geometry (a Legendre potential `F`); without that assumption the honest form keeps a cross
   term (`bias + noise + interaction`). See
   [`anti-noise-orchestration`](../../vault/hypothesis/anti-noise-orchestration.md).

---

## 3. The three fronts

We do not treat the three as independent, parallel pieces. They share a floor that is *not* one of
them — the **method** of §2 (the T0 root: claim ≤ proof, keep what survives, enrich from what
breaks), which is what makes any front correctable rather than merely asserted. On that floor there
is an intended relationship between the three — and the relationship is itself part of what is
unproven, so we state it as intent, not as fact:

```text
      ┌─────────────────────────────────────────────────────┐
      │  FRONT 2 — Category theory                           │
      │  (the intended ground *for typing the other two*)   │
      │  would type what a judgment is, and what a merge     │
      │  loses  — OPEN, nothing typed here yet               │
      └───────────────┬─────────────────────┬───────────────┘
             (intends to type)      (intends to type)
                      ▼                     ▼
      ┌───────────────────────┐   ┌─────────────────────────┐
      │ FRONT 1 — Decision    │   │ FRONT 3 — System         │
      │ making (the WHY)      │◄──│ architecture (the HOW)   │
      │ principles the        │(intends to  enforce)         │
      │ judgments should obey │   │ mostly unbuilt           │
      └───────────────────────┘   └─────────────────────────┘
      ════════════════════════════════════════════════════════
       THE METHOD — the T0 root (AX-2 / AX-4 / AX-5): state a
       claim → probe it → keep what survives → enrich from what
       breaks. The floor all three fronts stand on — the frame,
       not under test. Its discipline runs today; its automated
       loop does not.
```

The intent: Front 2 would supply the types for both Front 1 and Front 3, and Front 3 would make
Front 1's principles enforceable in code rather than merely asked-for. Both are goals, not
results — Front 2's typing is an open obligation (§3.2) and most of Front 3 is unbuilt (§3.3). *If*
the shape holds, it matters for a plain reason: a principle the architecture does not enforce stays
aspirational, and a type with nothing to type buys nothing. Whether it holds is exactly what we do
not yet know. Two senses of "ground" must not be confused: Front 2 is the intended ground *for
typing* the fronts; the **method** is the ground *of the enterprise* — the floor that lets a
collapse-test mean something. Front 2 could collapse to the sequential fragment (§3.2) and the
method floor would stand untouched.

Each front below states what it is, where it already lives, and — as plainly as we can — its
current standing.

### 3.1 Front 1 — Decision-making *(the WHY: the principles)*

What we would like to be true of the judgments the orchestrator produces. The failure it targets,
the proposed tool, and how far each has actually gotten:

| Failure | Proposed tool | Current standing |
|---|---|---|
| **Bias** (correlated, directional) | **tension** — deliberately *opposed* angles, so one agent's bias is more likely surfaced by another | `check-tension` gate runs today; `anti-bias-vector-composition` |
| **Noise** (dispersion of the aggregate) | **independence + aggregation** — independent, producer-blind scorers on a common scale; aggregate the estimate, not the individual | PENDING — argued, not built |
| **Framing** (an ill-posed lens may poison what follows) | **opposed frames + frame-dispersion as a signal** | PENDING — proposed stage |
| **Anchoring** (peers may contaminate a judgment before it is committed) | **freeze before the channel** — seal your position before the discussion opens | the initial+final primitive exists; the freezing rule is PENDING |
| **Premature consensus** (a correct minority may be averaged away) | **fork-guard** — try to distinguish dispersion (average it) from a real fork (escalate as `dissent_irreconcilable`) | escalation channel exists; the detector is PENDING |

One idea the design leans on, offered as a claim to test: tension and independence may not be
opposites but two settings of a single decorrelation knob — negative error-correlation (opposed
probes) where it can be engineered, zero error-correlation (independent, blind scorers) where it
cannot — applied where each is cheaper (tension at the *generate* stage, independence at the
*judge* stage). We have not demonstrated this on data.

*Home:* [`vault/hypothesis/anti-noise-orchestration.md`](../../vault/hypothesis/anti-noise-orchestration.md)
(HYP-ORCH-NOISE) — a red-teamed thesis with registered bets and collapse-tests. **Standing:**
candidate, low veracity; the anti-bias half runs, the anti-noise half is mostly PENDING.

### 3.2 Front 2 — Category theory *(the intended GROUND: the formal language)*

The half that would give the other two a formal language. Probes, zig-zag, robot-talks — each is
assigned a *candidate* categorical type plus an anchor in a real file. None of these is typed in
Lean in this repo, so each is a candidate to be checked, not a result:

- **probe** → candidate: generalized element / functor-of-points (Yoneda); the conjecture is that
  a complete family of probes reconstructs (Yoneda fully faithful) where a single passive signal
  does not.
- **zig-zag** → candidate: back-and-forth / triangle identities (comma-connected).
- **robot-talks / synthesis** → candidate: a pushout / colimit whose non-invertible unit would be
  the **residue** — what the merge identified away. A bare `concat` would be a coproduct
  (count-shaped); a real synthesis would generate residue. This is the concrete thing OBL-E3 tests.
- **feedback** → candidate: a 2-cell rather than a 1-morphism (it "never counts as a dependency") —
  which, if right, is a reason the loop may live one level up, not in the base category.
- **dispatch** → candidate: a typed diagram `J → Cat`.

The picture this front works toward — a framing, not a theorem — is that knowledge advances by
enriching the codomain `C` toward a (likely unreachable) Yoneda point, driven by a discriminating
signal: an anomaly is a separator the current lens cannot see; find it, probe it, enrich `C`,
shrink the residue.

*Home:* [`FRAMINGS.md`](../../FRAMINGS.md) (the merged CT ledger — F1–F7 anatomy + construct ⟷ CT type + join; single source) + `OBL-E3` in
[`OBLIGATIONS.md`](../../OBLIGATIONS.md) — the open obligation: *is the orchestration language
actually a category?* + [`lean-formalization/`](../../lean-formalization/README.md) — the index of
where each construct is formalized in the sibling repo. **Standing:** OPEN *for the orchestration
claim*. The underlying CT constructs are formalized and sorry-free per source in the sibling repo
(not here, and not re-built by us); what is unproven is that the *orchestration language* is one of
their instances. Named risk (stated in the obligation): zig-zag and feedback are probably not
1-morphisms, so the claim may narrow to the sequential fragment only.

### 3.3 Front 3 — System architecture *(the HOW: the intended enforcement substrate)*

The machinery that would make Front 1's principles enforceable in code rather than left to a
prompt. *(This is what the earlier framing called "nudge" — but nudge is a Front-1 concept; this
front is the event/bus/journal substrate that a nudge would need to have any teeth.)* It is a
proposal, largely unbuilt. It pulls apart six responsibilities today conflated under
"orchestration":

1. a **deterministic kernel** — would own only the protocol (identity, phases, barriers,
   visibility, deadlines, idempotency, transitions), never deciding which answer is "better".
2. **vendor-independent agent adapters** — one `AgentAdapter` contract over Codex CLI, Claude Code
   CLI, and API models, so swapping the adapter would not change the protocol.
3. a **per-group deliberation bus** — phases `collect → reveal → deliberate → vote → commit`, with
   a **reveal barrier** an agent cannot read past before sealing its own position. This is the
   proposed code-level form of Front 1's "freeze before the channel".
4. **sealed private judgments + a deterministic aggregator** — tags/scores as individual sealed
   judgments; an `aggregator` role reads the full set only after the barrier and produces a
   reproducible aggregate (frequency/distribution/agreement, not a prose "average"), without
   editing the individual judgments.
5. **four planes of observability** — audit ledger (permanent business facts), event journal
   (durable, replayable transitions), operational logs (why a process failed), traces/metrics
   (latency/cost/tokens) — kept distinct rather than collapsed into one "log".
6. a **typed knowledge/provenance store** — definitions, premises, decisions, constraints, claims,
   evidence, each with a state (`proposed → accepted → superseded`) and provenance, so that a
   definition would not become canonical merely because an agent stated it.

The proposed discipline: the transport may be ephemeral, but the accepted fact and its provenance
must survive; the bus would be a **projection** of the ledger, not a second source of truth — its
lifecycle stream projecting the ledger's hand-offs, its judgment stream (new content the ledger has
no home for) written through the *same* validated appender, never a second writer.

**Governed by the engine constitution (CONST-ENG).** Whatever the kernel and bus become, the plan
is that they must not break the invariants the current ledger already earned: **EG-1** (one
validated writer), **EG-2** (strict on write, lenient on read), and **EG-6** (history is an
artifact, never re-validated). EG-1 is the binding constraint today — it stands at
`veracity: medium`, blocked by the enum-drift (§4), so the write path is disabled until that is
traced. The bus-as-projection claim leans on EG-1 and inherits the same unresolved hole.

*Home:* [`docs/features/agents-communication-infra/README.md`](../../docs/features/agents-communication-infra/README.md)
(the full proposal: responsibilities, invariants, MVP, open decisions) +
[`vault/hypothesis/orchestration-infra.md`](../../vault/hypothesis/orchestration-infra.md)
(HYP-ORCH-INFRA: bus-as-projection, id scheme, retention tiers, freeze-witness) +
[`vault/constitution/engine-constitution.md`](../../vault/constitution/engine-constitution.md)
(CONST-ENG: EG-1…EG-8) + [`research/agent-events-infra-hypothesis/`](../../research/agent-events-infra-hypothesis/).
**Standing:** proposal. What exists is a starting point — the scheduling edges, a read-only control
plane, SSE. The kernel, adapters, reveal barrier, durable journal, and store are not built.

---

## 4. What runs today vs. what is still thesis

"Runs" here means built and tested — **not** proven correct.

**Runs (a read-only slice of the substrate).**
- **Dispatch discipline** — agent groups, typed connections (`sequential`/`zig-zag`/`feedback`),
  the `check-tension` anti-bias gate (fires only for n≥2 investigate/evaluate groups), an
  append-only ledger, a strict Node appender.
- **Control plane — Phase 1 (read).** A FastAPI + SSE server with 10 UI variants that read the
  pending sheet and the ledger live, with test coverage. The design it rests on:
  appender-strict, reader-lenient.
- **agent-pool MCP** — 414 entries, a deterministic core plus a cheap Haiku frontier, cross-repo.

**Still thesis (argued, not proven).** All three fronts above, at the standings stated: the
candidate CT typing (Front 2), the anti-noise design (Front 1), and the bus/infra substrate
(Front 3).

**The one defect we treat as blocking.** An audit found two 2026-07-18 close rows carrying an
out-of-enum `exit_reason: "success"` that could only have bypassed the validated appender. It holds
the engine constitution's single-writer rule (EG-1) at `veracity: medium`, blocks its promotion,
and blocks the write path (the UI Dispatch button that writes is present but disabled by contract).
Front 3's "bus is a projection" claim leans on EG-1 and inherits the hole. See
[`vault/audit/ledger-enum-drift-finding.md`](../../vault/audit/ledger-enum-drift-finding.md).

**Portability caveat.** "Droppable into any repo" holds for the *architecture*, but the substrate
today is hardwired to one Windows operator. Asserted and partly engineered — not demonstrated on a
second machine.

---

## 5. What we are gathering next (information, not building)

Before building, the open items each front needs settled:

**Front 1 (decision-making).**
- The common-scale rubric: fixed global vs. per-`dispatch_type`, and its boundary with the
  knowledge-taxonomy facets (what a thing *is* vs. how *good* it is).
- The frame's noise arm: how many independent frames, how to measure dispersion of *questions*
  (which do not average), and what would separate "ill-posed" from "rich".
- Whether the CT operationalization ever changes a decision, or only relabels one (the CT bet is
  candidate, not yet survived).

**Front 2 (category theory).**
- Verify the sibling Lean build (`lake build` green, `#print axioms` clean); until then the anchors
  stay candidate.
- OBL-E3: do zig-zag/feedback compose associatively (a category), or are they 2-cells (narrowing
  the claim to the sequential fragment)?

**Front 3 (system architecture).**
- The open decisions in the infra proposal — persistence, group-closing rule, who proposes the
  synthesis, sealing policy, TTLs, reconciling the canonical schema with the historical ledger.
- Whether the reveal barrier can be a *technical* guarantee rather than a prompt convention.
- The vendor boundary: whether the same scenario runs through both a Codex-CLI and a
  Claude-Code-CLI adapter to an equivalent operational (not semantic) terminal state.

**The claim→refutation→golden loop (the scientific process of §2, still unbuilt).** The loop is
meant to run: a claim enters the ledger → survives refutation attempts → is connected into a
"golden" graph where the nodes are held true. The framing constraint that shapes all of it (a
*candidate* anchor in the sibling repo `domainspec-lean-formalization`'s reflection tower —
`omega_absorption_refuted`, **build unverified**): an append-only promotion is *K-only* and
provably never enriches the codomain `C`, **not even at the colimit** — enriching requires a
*relation-adding / quotient* step. So the **golden-connection step is the only place in the loop
where enrichment can happen**, and it is exactly what a BL-3 close-row would have to carry. Open
items, none built:
- *Refutation — survival criterion.* The minimal **separating** family (surviving one refuter
  proves almost nothing — F4's passive-signal collapse-test); when a claim counts as "survived";
  and survival as **defeasible and indexed by the family that tested it**, so a sharper family can
  reopen it (this index *is* provenance).
- *Golden — connection protocol.* How to compute a surviving claim's morphisms to existing nodes
  (`refines`/`contradicts`/`instantiates` — the F5 verbs), and the **contradiction protocol** when
  it clashes with a held node: refute the newcomer, retract the old (quotient), or split (the two
  were secretly distinct — `¬EssSurj`, add object).
- *Golden — moving frontier vs. the consistency invariant.* Reconcile "everything is true"
  (a consistency invariant with a single owner — **EG-1**) with "never residue-0" (the golden graph
  is always one probe from the next anomaly, never a fixed floor — the F6 correction). Gated under
  the enum-drift (§4), like the rest of EG-1.
- *Golden — node typing.* Whether to type nodes **rule vs. law** (contingent policy vs. structural
  law whose violation changes the system), carrying the vault's veracity⊥conviction rather than a
  boolean.
- *The graded-convergence witness* (sub-family fails to separate → adding the missing probe restores
  fully-faithful) remains an **open obligation with no Lean decl**; the sibling tower supplies only
  the *persistence* co-testimony (residue survives every level), not this.

**Cross-cutting.** A **provenance spine** — assertion → the dispatch/research that generated it →
its trail — does not exist today; ids live in four disjoint spaces. We suspect this single gap is
behind the missing `enrich` step (Front 1's loop), the unenforced freeze (Front 3), and the untyped
self-reference. Settling the node alphabet, edge catalog, and event envelope is the decision several
other things appear to wait on — a suspicion, to be confirmed as we design it.

---

## 6. Where the detail lives

| For… | Read |
|---|---|
| this root Plan and orientation | `plans/governed-agent-work-infrastructure/PLAN.md` |
| the detailed roadmap + codes (OBL/BL/FT/EG, phases) | [`archive/`](archive/) (retired root PLAN) |
| decision-making thesis | [`vault/hypothesis/anti-noise-orchestration.md`](../../vault/hypothesis/anti-noise-orchestration.md) |
| category-theory mapping | [`FRAMINGS.md`](../../FRAMINGS.md) · [`OBLIGATIONS.md`](../../OBLIGATIONS.md) |
| where the CT is actually formalized (sibling repo) | [`lean-formalization/`](../../lean-formalization/README.md) |
| system architecture | [`docs/features/agents-communication-infra/README.md`](../../docs/features/agents-communication-infra/README.md) · [`vault/hypothesis/orchestration-infra.md`](../../vault/hypothesis/orchestration-infra.md) · [`vault/constitution/engine-constitution.md`](../../vault/constitution/engine-constitution.md) |
| what runs today (substrate, control plane) | [`README.md`](../../README.md) |
| the blocking defect | [`vault/audit/ledger-enum-drift-finding.md`](../../vault/audit/ledger-enum-drift-finding.md) |

## Open Questions

- **Resolved:** the repository owner is the governing authority for this root Plan. The Plan remains
  proposal-only and supplies no execution authority.
- Which claims in the three fronts remain part of this Plan after the agent-language research
  program is reconciled with it?
- Should this orientation be revised, split, or superseded by Plans with separately resolved
  authorities for decision hygiene, mathematical formalization, and system architecture?
</content>
