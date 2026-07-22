---
canonical_kind: discovery
node_type: discovery
is_session: false
layer: architecture, application
nature: reference
status: draft
version: 0.2.0
last_updated: 2026-07-21
created: 2026-07-21
title: Agent assertion capture — the source layer of the knowledge bus
description: >
  A capture layer where every invoked agent (including subagents) self-emits the assertions it
  makes along a session — decisions, premises, hypotheses, doubts, definitions — as `proposed`,
  low-veracity records at the source, through a judgment-free `emit-assertion` tool plus
  hook-driven cadence. This is the coarsest-quality but source-truest layer of the knowledge bus;
  downstream gates, comparison, and per-type processes refine it. Emitter is a stenographer, never
  a judge. Landing document to decide what to build.
evidence_for: [Research, Spec, Feature]
tags: [knowledge-bus, assertion-capture, provenance, emit, hooks, anti-bias, claim-graph, orchestration-infra]
question: >
  How does every invoked agent cheaply record the decisions/premises/hypotheses/doubts/definitions
  it makes at the source, in a form that does not require trusting the agent, so that a later
  refinement layer can raise them — without the emitter ever judging their quality?
---

# Agent assertion capture — the source layer of the knowledge bus

> **Status:** `draft`, unreviewed landing document. This is where the design worked out in
> conversation is parked so the team can decide **what to do** (promote pieces to the vault, cut a
> feature, run experiments) — it is **not** an implementation plan and **not** a commitment to
> build. `Claim ≤ proof`: every mechanism below is a candidate with a collapse-test; nothing here
> is built yet, and anything that *writes* is gated (see Open Question OQ-5 / EG-1).

## Objective

Add a **capture layer** in which every invoked agent — including subagents — self-emits the
assertions it makes during a session (decisions, premises, hypotheses, doubts, definitions) as
`proposed`, `veracity: low` records **at the moment they are made**, through a judgment-free
`emit-assertion` tool plus hook-driven cadence. The end state is a running, **provenance-carrying
source layer** (the coarsest-quality but source-truest tier of the knowledge bus) plus a **defined
refinement path** by which downstream gates, comparison, and per-type processes raise those raw
records — the emitter never deciding anything about their quality.

---

## 1. Business Context

### Why now

The orchestrator already captures **dispatch-level** facts (the append-only audit ledger, written
post-confirm by `register-dispatch`). But the **epistemic** work an agent does *inside* a session
— the premises it adopts, the forks it resolves, the terms it defines, the doubts it hits —
evaporates into the transcript the moment the session ends. That is exactly the gap
[`docs/PLAN.md §5`](../../PLAN.md) names as the suspected **root** of three unsolved problems: the
missing `enrich` step in the claim→refutation→golden loop, the unenforced freeze, and the untyped
self-reference — "a provenance spine (assertion → the dispatch/research that generated it → its
trail) does not exist today; ids live in four disjoint spaces." This whole design was itself worked
out across a multi-turn session whose decisions live **only in a chat transcript** — a live
instance of the problem it addresses.

### What's broken

- **Assertion-level knowledge has no capture path.**
  [`vault/hypothesis/claim-graph.md`](../../../vault/hypothesis/claim-graph.md) (HYP-CLAIM-GRAPH)
  *types* assertions and their edges, but nothing *populates* the graph; its Open Question #3
  ("who runs the decompositor — a skill, an LLM pass, a human-in-the-loop?") is **open**.
- **The knowledge store is design-only.**
  [`vault/hypothesis/orchestration-infra.md`](../../../vault/hypothesis/orchestration-infra.md)
  (HYP-ORCH-INFRA) declares a knowledge store that holds **promoted** content behind a governed
  promotion writer (agents "may propose through the bus"), but there is **no writer and no capture
  path**, and the bus does not exist yet. *(The full `proposed → accepted → superseded` lifecycle is
  stated in [`docs/PLAN.md §3.3`](../../PLAN.md), not in HYP-ORCH-INFRA.)*
- **No provenance spine.** [`docs/PLAN.md §5`](../../PLAN.md) — assertions cannot be traced to the
  dispatch/session/agent that produced them; the ids are disjoint.
- **All new writes are gated.** [`vault/constitution/engine-constitution.md`](../../../vault/constitution/engine-constitution.md)
  EG-1 (single validated writer) stands at `veracity: medium`, blocked by the live enum-drift
  counterexample ([`vault/audit/ledger-enum-drift-finding.md`](../../../vault/audit/ledger-enum-drift-finding.md)).
  Any new writer — the `emit-assertion` appender included — inherits EG-1's **unpromoted status**
  (not the specific manual-edit bug), so it cannot ship until EG-1 clears **and** the new store
  passes its own single-writer + authority-overlap review (see OQ-5).

### What stays the same (scope boundary)

- The **audit ledger** and `register-dispatch` — dispatch granularity is unchanged; this layer sits
  *below* it, at assertion granularity.
- The **strict dispatch appender** and its `schema_version 0.6.1` contract.
- The **read-only control plane** (Phase 1) — no change to the reader.
- The **categorical thesis** (FRAMINGS / OBLIGATIONS / DEFINITIONS) and the **agent-pool MCP**.
- **Out of scope for this cut:** building the event-journal/bus runtime; changing promotion
  authority; and — the load-bearing boundary — the emitter deciding **anything** about the quality
  of what it records. Quality lives at the promotion bar, not here.

---

## 2. Core Concepts

### C1 — Emitter as stenographer (form ≠ quality)

The emitting agent **records, it does not judge**. It is responsible for the *form* of an assertion
(its content, type, and whatever slots are present) but **never** for its *quality* (true? strong?
promotable? high-veracity?). **Why this design:** an agent that graded the quality of its own
records would be marking its own homework — emitter-and-judge in the same party is precisely the
**correlated bias** the whole project exists to counter. Separating emit from judge is the same
invariant as dispatch ⊥ gate and producer ⊥ scorer (freeze-before-the-channel).

### C2 — Two bars: capture-lenient ⊥ promotion-strict

| Bar | Who | Judges quality? | Behavior |
|---|---|---|---|
| **Capture** | the working agent, via `emit-assertion` | **No** | Lenient: never rejects; stamps `proposed` + `veracity: low`; a missing slot is recorded as `<absent>`, not fixed or fabricated. |
| **Promotion** | gate: cross-check + human / governed writer + (for load-bearing) independent probe | **Yes** | Strict: applies well-formedness, measures the falsifier, decides whether to raise. |

A missing slot is **signal, not failure** — a decision emitted without its foregone alternatives is
recorded as `alternatives: <absent>`, which is exactly what the auditor flags downstream as inert.

### C3 — Per-type well-formedness: every assertion carries its withdrawal condition

The single rule: **an assertion is well-formed iff it carries the condition under which it would be
withdrawn.** The *type* only decides the **shape** of that condition. (This is the bar checked at
**promotion**, not enforced at capture.)

| Type | Content | Withdrawal condition (its falsifier) | Repo artifact it generalizes |
|---|---|---|---|
| **hypothesis** | claim P | **collapse-test** — the observation that refutes | `HYP-*` collapse-tests |
| **premise** | the assumption | **retraction trigger** + what it is *load-bearing* for | `vault/axioms/axioms.md` **`P-*`** nodes (P-AGENT-TRANSFER, P-FACES-INSTANCE) — **not** AX-* axioms, which are assumed and carry no evidence-retraction |
| **definition** | the term | **boundary** + a **discriminating membership test** | `definitions/DEFINITIONS.md` (Boundary field) |
| **decision** | chose X over Y | the **foregone alternatives** + criterion + **reopening condition** | (dispersed; no home) |
| **doubt / open question** | the question | **resolution criterion** + what is **blocked** on it | "Open questions" sections |

Two teeth: a **decision without a foregone alternative is not a decision, it is a default** (the
dangerous silent kind); a **doubt without a resolution criterion is just anxiety**, not a graph node.

### C4 — Source layer = witness (coarsest quality, finest granularity)

This layer is the two extremes at once: **finest granularity** (the individual assertion) and
**crudest quality** (`proposed`, `veracity: low`, unrefined). Its value is **not** quality — it is
**testimony**: it records that assertion X was made at time T, in context C, by agent A. That
witness is **irreducible** — it cannot be regenerated downstream. Therefore the source is
**immutable / append-only** — the write-boundary/single-writer integrity of **EG-1**, with **EG-6**
keeping the record un-re-validated under schema change: refinement **never rewrites** a source
record; it produces *new nodes and edges that point back* to it. The source stays `veracity: low` forever, permanently
linked.

> ⚠ **Terminology guard:** "coarse" here means crude *quality*, **not** low granularity. Earlier in
> the design "coarse" meant the task/decision *granularity* axis. They are orthogonal; do not
> conflate.

### C5 — K-only floor ⊥ enrich-by-relation (where knowledge actually advances)

Per [`docs/PLAN.md §5`](../../PLAN.md) — as a **candidate** anchor resting on an *unverified* Lean
decl (`omega_absorption_refuted`) in the sibling repo, **not** proven in-repo — append-only promotion
is *conjectured* to be **K-only** and to never enrich the codomain `C` ("not even at the colimit"),
so that enriching would require a **relation-adding / quotient** step.
[`vault/audit/close-row-enrich-c.md`](../../../vault/audit/close-row-enrich-c.md) proves only the
narrower in-repo fact: a close-row can't enrich `C` because the appender's schema is fixed
(enrichment only at a `schema_version` bump) — it does **not** make the K-only/colimit claim. So the source is the **K-only
floor** (append, never enriched); **enrichment happens only when refinement adds edges** (`refines`,
`contradicts`, or a *split*: two records secretly distinct → add object). "Refine what's there" is
therefore not a step among others — it is the **only place the knowledge can advance**, which is
exactly the golden-connection step BL-3 must carry. *(This maps onto the finding; it does not prove
it — and it stays behind the EG-1 gate.)*

### C6 — Capture mechanism: think-boundary = tool-boundary

There is no thinking/reasoning hook. But in the agentic loop the **tool boundary is the think
boundary**: `PreToolUse` fires right after a thought concluded in a decision to act (the freeze
point — before the next input contaminates it); `PostToolUse` rides the tool result, right before
the next thought; `Stop`/`SubagentStop` catch the final prose-only thought. So the capture model is:

- **Seed once** at `SubagentStart` / `SessionStart` (a fixed, cache-friendly reminder: "emit via
  `emit-assertion`, or say 'no decision'").
- **Mandatory consolidated sweep** at `Stop` / `SubagentStop`.
- **Silent-triggered nudge** on `PostToolUse` — fires *only* after N tool-boundaries with zero
  emission; doubles as the cheap **completeness auditor**.
- **Streaming per-decision** (`PreToolUse`) is **opt-in**, for long / high-stakes sessions only.

The **cadence bookkeeping** is token-free: a counter file incremented per `PostToolUse` — no
tokenizer, no transcript parse, **zero model tokens**. But capture itself is **not** free: the
injected reminder costs tokens when it fires; the seed occupies context all session (cache-friendly
≠ free); and the **mandatory `Stop`/`SubagentStop` sweep is a forced generation** — the single
largest token cost in the system, and non-optional. *(Build note: the counter must be **keyed by
`agent_id`** — subagents run in parallel and would race a single shared file — and reset on each
`emit-assertion`; the threshold `N` is unspecified. See §6.)*

### C7 — Trust without trusting: the declared ↔ produced cross-check

The hook buys **completeness** (fewer silent decisions), **not fidelity** (LLM self-reports can be
unfaithful). Fidelity is recovered by holding two sources against each other: the assertion the
agent **declared** vs. the **artifact it produced** (the ground truth of what it actually decided).
Divergence is **first-class residue** (the same η^sch ⊥ η^ins split HYP-ORCH-INFRA uses for tags).
The auditor checks *"does the declaration match the trace?"* (cheap, mechanical) — never *"is it
true?"* (impossible here).

---

## 3. Detailed Specifications

### 3.1 Emission record shape

Each `emit-assertion` call appends one record carrying:

- `type` — one of `decision | premise | hypothesis | doubt | definition` (extensible).
- `content` — the assertion itself.
- **type-specific slots** per C3 (collapse-test / retraction-trigger / boundary+test / foregone
  alternatives+reopening / resolution criterion), each `<absent>` if not stated.
- `status: proposed`, `veracity: low` — stamped by the writer, not settable by the agent.
- `conviction` — optional agent self-report; orthogonal, non-authoritative.
- **lineage (mandatory, writer-stamped — never agent-supplied)** — `session_id`, `agent_id`,
  `dispatch_id`, `timestamp`, context pointer. Stamped by the writer/hook from trusted context (the
  hook payload carries `agent_id`/`agent_type`), **not** produced by the model — otherwise it is
  self-reported and untrustworthy (C1/C7). Being writer-stamped, it is never "missing," so it never
  triggers a capture rejection (consistent with C2's "never rejects"). **Without lineage this is not
  a spine, it is litter** (see Why now); it roots the provenance spine PLAN §5 says is missing.
  *Open:* the resolution path for `session_id`/`dispatch_id` — a running subagent may have **no
  dispatch row yet** — is not defined (see §6).

Written through **one validated appender** (the `register-dispatch` pattern, one granularity down)
so EG-1's single-writer rule holds.

### 3.2 Capture model — Claude Code vs. Codex

*Hook facts below were verified against current Claude Code docs (`code.claude.com/docs/en/hooks.md`)
in-session, not from an in-repo artifact; `SubagentStart` and `PostToolUse` `additionalContext` and
subagent-payload `agent_id`/`agent_type` all exist as of that check. **Version floor unstated** — an
older Claude Code install predating `SubagentStart` silently falls back to sweep-only capture (see §6).*

| Capability | Claude Code | Codex |
|---|---|---|
| Emission tool (`emit-assertion`) | ✅ | ✅ (portable — it is just a tool) |
| Seed at spawn | ✅ `SubagentStart` / `SessionStart` (context injection) | ⚠ static `AGENTS.md` only (fires once) |
| Silent-triggered mid-flight nudge | ✅ `PostToolUse` `additionalContext`, throttled via state file | ❌ no context injection (hooks observe/block only, Bash-tool events only) |
| Reach into subagents | ✅ hooks fire inside Task subagents (`agent_id`/`agent_type` in payload) | n/a |

**Consequence:** on Codex the dynamic nudge does not exist — capture there leans on the static
reminder + the tool + a heavier reliance on the §3.4 close-time cross-check to recover what the
missing nudge did not catch.

### 3.3 Refinement path — two forces

- **Horizontal (gates + comparison):** the declared↔produced cross-check, the promotion gate,
  and cross-agent/cross-run comparison (dispersion → the anti-noise machinery). Refines by
  **tension and aggregation**.
- **Vertical (per-type processes):** a raw record is lifted by a process matched to its type — a
  hypothesis through `experiment-harness`, a definition through `definitions-governance`, a decision
  through a `decision-gate`. Each process tests exactly that type's **withdrawal condition** (C3).

### 3.4 Cross-check (declared ↔ produced)

Runtime-agnostic; runs at close over what landed on disk (so it also covers Codex, where the nudge
is absent). Emits a divergence record — itself a `proposed` assertion of type `doubt` when the
declaration and the artifact disagree — rather than silently trusting either side.

---

## 4. Open Questions

*(Each carries a recommendation, per the discovery skill.)*

- **OQ-1 — CT1, inter-tagger agreement.** Can two independent runs agree on an assertion's *type* /
  an edge's *type* above chance? If not, the layer measures noise, not structure.
  **Recommendation:** run this as an `experiment-harness` experiment *before* building the tool —
  it is the cheapest thing that can kill the whole idea.
- **OQ-2 — does the nudge degrade the task?** More frequent reminders may raise emission *volume*
  while lowering task quality or producing ritual/low-fidelity emission.
  **Recommendation:** register it as a collapse-test (measure task-success delta + declared↔produced
  divergence rate with the hook on vs. off); if net-negative, the hook is removed, emission stays.
- **OQ-3 — physical home of the source layer** *(build-blocker: no appender can be built without a
  path/format).* **Recommendation:** a per-session **append-only** file under a new
  `telemetry/knowledge/` path — **not** under `pending/`, to avoid the C4 contradiction: the
  assertion record is **immutable from the moment it is appended**; the *pre-confirm editability* of
  a pending sheet belongs to the dispatch layer, never to a source assertion.
- **OQ-4 — who owns the sweep vs. the streaming trade-off.** Capturing at decision-time maximizes
  fidelity but pollutes context; the close-sweep minimizes pollution but is post-hoc.
  **Recommendation:** default to seed + silent-net + mandatory close-sweep; make per-decision
  streaming opt-in for high-stakes sessions; lean on §3.4 to absorb the sweep's fidelity cost.
- **OQ-5 — EG-1 gate (necessary, not sufficient).** The `emit-assertion` writer is a **new
  authority** (the knowledge store, distinct from the audit ledger), so clearing the enum-drift does
  **not** by itself validate it — EG-1's own Validation clause requires *"equivalent contract tests
  and an authority-overlap review"* for any future store. **Recommendation:** gate *implementation*
  behind (a) the enum-drift trace **and** (b) a dedicated single-writer boundary + authority-overlap
  review for the new store (is a `proposed/veracity:low` source decision the *same canonical fact* as
  its later promoted counterpart? C4's point-back design answers *yes-by-reference*, but must pass the
  review, not assume it). The *discovery* and *experiments* (OQ-1/OQ-2) write no ledger and proceed now.
- **OQ-6 — promotion targets (where the pieces go).** This document is cross-cutting on purpose.
  **Recommendation:** once stabilized, promote C1–C3 to
  [HYP-CLAIM-GRAPH](../../../vault/hypothesis/claim-graph.md) (answering its OQ#3), C4–C5 to
  [HYP-ORCH-INFRA](../../../vault/hypothesis/orchestration-infra.md), and C6–C7 + §3 to a feature
  discovery when/if the experiments survive.

---

## 5. Connections

| Document | Edge | Why |
|---|---|---|
| [HYP-CLAIM-GRAPH](../../../vault/hypothesis/claim-graph.md) | `refines` | Offers a **candidate** answer to its Open Question #3 — the working agent self-emitting inline. This is **not** the generic decompositor (ingestion of an *arbitrary* process, gated on BET-DECOMP-CHEAP); it is a narrower, different mechanism and does **not** discharge that bet. |
| [HYP-ORCH-INFRA](../../../vault/hypothesis/orchestration-infra.md) | `depends-on` | Realizes its `proposed → promoted` knowledge store and the disjoint-authority split at the source. |
| [`vault/audit/close-row-enrich-c.md`](../../../vault/audit/close-row-enrich-c.md) | `grounds` | The K-only ⊥ enrich-by-relation finding that C5 rests on. |
| [`vault/constitution/engine-constitution.md`](../../../vault/constitution/engine-constitution.md) | `cites` | EG-1 (one validated writer) and EG-6 (history is an artifact) constrain the appender. |
| [`docs/PLAN.md §5`](../../PLAN.md) | `derives-from` | The provenance-spine gap this layer is the root of. |
| [`vault/audit/ledger-enum-drift-finding.md`](../../../vault/audit/ledger-enum-drift-finding.md) | `blocked-by` | The live counterexample that gates any new writer (OQ-5). |

---

## 6. Review findings & open design gaps (2026-07-21)

Reviewed by three subagents on opposed angles (falsifier ⊥ coherence ⊥ feasibility). The honesty and
citation defects they raised (overclaimed "provably"; the `proposed→accepted→superseded`
mis-attribution; the AX-* vs P-* category error; EG-6 vs EG-1; the folder-vs-file link; "answers"
vs "candidate answer" to OQ#3; the "verified" matrix's missing source; the C4-immutable vs
OQ-3-editable contradiction; the "token-free" undercount) are **corrected inline above**. What
remains are decisions, not edits:

### The keystone risk (all three converge here)

**"Form ≠ quality" (C1) depends on typing being reliable — and that is untested.** Choosing *which*
utterances are assertions, assigning each a **type**, and marking a slot `<absent>` are themselves
discriminations. If two independent runs cannot agree on them above chance (CT1 / BET-CLAIM-TYPES,
still open in HYP-CLAIM-GRAPH), then the emitter *is* judging, just relabeled — and the cascade is
total: C1 → C2's two-bar split → C3's per-type check → the whole anti-bias rationale. This is the
load-bearing keystone and the thing most likely to be false. **OQ-1 must run before any build.**

### Build gaps (each blocks handing §3 to an implementation plan)

- **G1 — lineage source.** Lineage is now writer-stamped (§3.1), but the **resolution path for
  `session_id`/`dispatch_id` is undefined**, and a running subagent may have no dispatch row yet.
  Without it every record risks `dispatch_id: <absent>` — the "litter" §3.1 warns against.
- **G2 — physical home (OQ-3).** No path/format/rotation decided → no appender can be built.
- **G3 — counter file.** Must be keyed by `agent_id`, concurrency-safe, with a defined reset and a
  concrete `N`. A single shared `.claude/emit-state.json` races across parallel subagents.
- **G4 — EG-1 scope (OQ-5).** The new store needs its **own** single-writer boundary +
  authority-overlap review; clearing the enum-drift is necessary, not sufficient.

### Honest limits to keep visible

- **G5 — Codex is not compensated.** §3.4's close-time cross-check recovers only a **presence/divergence
  flag**, never the in-context type-specific slots (the alternatives actually weighed, the collapse-test
  held in mind) — those are gone once the session closes. On Codex the "source-truest layer" degrades to
  low-fidelity flags; the "source-true, well-formed assertion" is **Claude-only in practice**. C4's
  irreducibility principle actually forbids downstream regeneration — so §3.4 must be framed as a *flag
  recovery*, not a substitute for capture.
- **G6 — think ≈ tool blind spot.** Reasoning-heavy, tool-light agents (e.g. a synthesizer) hit few
  tool boundaries → capture collapses onto the low-fidelity Stop sweep. Fidelity degrades exactly for the
  most decision-dense agents. Intermediate prose-only reasoning is invisible until the sweep.
- **G7 — the nudge contaminates the stream it means to capture cleanly.** C6 prizes `PreToolUse` capture
  as "before the next input contaminates it," yet the `PostToolUse` nudge **is** a contaminating injection
  between the tool result and the next thought. And the **always-on sweep means OQ-2's "hook on vs off"
  experiment cannot isolate the sweep's cost.** Needs agent-type scoping (hook matchers, already used in
  `.claude/settings.json` for `Write`, unused here) and a sweep-toggle for the experiment.
- **G8 — version floor.** The whole subagent-capture value rests on `SubagentStart`, a newer hook not
  guaranteed on every install (portability principle). State a version floor or a sweep-only fallback.
