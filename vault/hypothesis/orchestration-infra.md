---
hypothesis_id: HYP-ORCH-INFRA
title: "Thesis — The orchestrator's mediation made into an auditable substrate (bus, ids, retention, freeze)"
status: candidate
authority_level: exploratory
owner: Victor
created: 2026-07-20
last_updated: 2026-07-20
tags: [orchestration, bus, events, ids, retention, freeze, tagging, knowledge-taxonomy, residue, infra]
---

# Thesis — The orchestrator's mediation made into an auditable substrate

> **Status:** `candidate`, `exploratory`. This **does not legislate** — it reasons. It is the
> **infrastructure** sibling of [[anti-noise-orchestration]] (the *conceptual* thesis): that one
> asks *what* the orchestrator is (a noise-reduction machine); this one asks *what substrate*
> the machine runs on. `Claim ≤ proof`: each "you already do X" points to a real artifact;
> where there is none, it is marked **PENDING**. Its central design tension —
> *reuse-vendored vs. build-native* — is **kept open**, not resolved (see Open questions).

## Opening

Today the orchestrator's **mediation is an ephemeral act**: it reads a group's output and
composes the next group's prompt, in its own transcript, and nothing of that hand-off
survives except what the ledger incidentally stores (the composed `initial_prompt` in the
`groups` column; `feedback_prompts` verbatim in the close row). Agents never address each
other; `connections` (`sequential | zig-zag | feedback`) are **scheduling edges, not
transport** (register-dispatch SKILL). The orchestrator is a star whose center forgets.

This thesis proposes to make that mediation into a **written, addressable, auditable
substrate** — a bus, an id scheme, retention tiers, and a decision-science protocol — *without
breaking the two things the repo has earned*: the append-only ledger ([[engine-constitution]]
EG-1/EG-6) and the **one-shot agent** model. The claim in one line:

> **The bus is not a *duplicative* store: its lifecycle stream is a projection of the ledger's
> mediation, and its judgment stream is the one content the ledger has no home for — new, but
> written through the same validated appender (EG-1), never a second copy of anything.**

The thesis is falsifiable (see *Collapse-tests*) and, like its sibling, a **self-application**:
the substrate that records the orchestrator's judgments is itself governed by the anti-noise
discipline those judgments are meant to have (`freeze before the channel`).

## Context — what already exists

- **The ledger is already a two-event log** (EG-1): a dispatch row + a close row per dispatch,
  content nowhere re-validated (EG-6). Mediation is *partly* persisted already. **Caveat:** EG-1
  is itself `veracity: medium` and **promotion-blocked** by a live counterexample (the 2026-07-18
  enum-drift, [[engine-constitution]]); every argument below that leans on the one-writer spine
  inherits that unresolved risk.
- **`signature()`** ([ledger.py:790-808](../../implementations/server/ledger.py#L790-L808)) is a
  disk fingerprint (mtime_ns + size) that drives SSE change-detection — the **single
  integration point** for anything served live.
- **`expires`** (created + 60d, in session frontmatter) is the *only* time-retention vocabulary
  in the repo. There is **no** TTL/gc machinery (PENDING).
- **A sibling substrate exists.** `cyberAlchemyAI/knowledge-taxonomy` (KT) is a faceted
  **classification** substrate sharing this repo's DNA (orthogonal facets, residue calculus,
  the same dispatch model, JSONL event logs). It has reusable parts — the 5 closed facets, a
  system-tagging *interface contract*, two event envelopes, a two-kind residue model. See
  [[research]] / [[findings]] for the ground truth. **KT has no bus** (confirmed) and its
  tagging engine is a **spec, not shipped software**.
- **The independent-judgment primitive (P14, initial+final positions)** is named in
  `domainspec-subagents-strategy` but has **no persisted home** — PENDING. This is the gap the
  bus actually fills.

## The central thesis

### The bus is a two-stream projection of the ledger

Two streams, mirroring KT's own split (whose envelopes we may vendor — an open choice):

- a **lifecycle stream** — the mediated hand-offs, *projected* from dispatch/close rows.
  Candidate envelope reuses KT's `spec_hash` (a *proposed* idempotency key — undocumented in KT)
  and `parent_dispatch_id` (nesting). KT's **`corpus_hash_at_emit`** is a **candidate** witness of
  *what an agent saw when it emitted* — the enforcement handle freeze would need — but it is **null
  in 100% of KT's logged rows and undocumented there (PENDING)**; we would have to define and
  populate it ourselves;
- a **judgment stream** — the agent's **frozen independent judgment** (the ETE pre/post pair),
  which the ledger has no slot for today. A `proposal` with a `confidence` *is* a frozen
  judgment.

Because the lifecycle stream is a **projection, not a *duplicative* store**, a bus event whose
`spec_hash` disagrees with its ledger row is a **corruption signal** — EG-4 honesty, for free. The
*judgment* stream is genuinely new content, so to stay under the one-writer spine (EG-1) it must be
written through the same validated appender — never a second writer. What the orthogonality
principle ([[ontology-conventions]]) and EG-1 forbid is a second *authoritative and duplicative*
source of truth; a non-duplicative new tier, appended once through the one writer, is not that.

### "Listening all the time" is inversion, not a runtime change

The requirement "agents listen to the bus continuously" is satisfied by making the
**orchestrator** the listener (it is already the event loop) and handing each agent a **frozen
bus-snapshot at launch**. The one-shot agent constraint and the anti-noise *freeze before the
channel* rule point at the *same* design: read the bus once, frozen; register; only a later
re-invocation reads others. A continuously-listening agent would *be* the live anchoring
channel the freeze exists to kill. **This is untested by KT** (its dispatches are single-shot) —
so it is our claim, carried with its collapse-test.

### A three-level id hierarchy, minted per dispatch

`agent id ⊂ group id ⊂ dispatch id`. Two levels exist: `dispatch_id` (`YYYY-MM-DD-slug`, the
dedup key) and `group_id` (already a `connections` address). The **agent level does not exist**:
`agent_name` is a nullable, non-unique *persona* from the pool, not an identity. We **mint**
`dispatch_id:group_id:role#index` — assembled the same way KT's per-agent reports carry their
`agent_id`/`layer_id`/`dispatch_id` frontmatter (KT does not construct a literal joined id either),
dispatch-scoped, not a global identity.

### Retention is differentiated and legible in the tree

`subagents-dispatch.yaml` = **permanent** · `bus/` = **medium** (auditable, a TTL reusing
`expires`; duration open) · `live/` = **ephemeral** (a single current file, overwritten per
tick, served over SSE) · `pending/` = **pre-confirm** editable. The only code change for the
live view is teaching `signature()` about the new dirs.

### Tags are system-generated judgments, not agent-owned vocabulary

The agent does not *pick* a tag; it **emits `proposed`**, and an engine adjudicates
`accepted | withheld | unresolved`. The **method/framework** it applies is a-priori (predictable
at dispatch → feeds agent-pool name selection); the **domain** of its output is a-posteriori
(open — `domain` is an open string in KT, deliberately un-closed). The predicted↔produced
divergence is **first-class residue**, and it splits — per KT's Lean-proved M6 — into **instance
residue** (weak prediction rule → tighten) ⊥ **schema residue** (theme absent from the vocab →
enlarge). Two counters, not one divergence metric.

## The pipeline as a worked example

A `research` dispatch with an explorer group and a synthesizer:

1. **Dispatch.** The dispatcher predicts a *method/framework* theme; it feeds agent-pool name
   selection and lands on the dispatch row (permanent). The bus lifecycle stream emits
   `dispatched` with `corpus_hash_at_emit`.
2. **Frozen judgment.** Each explorer, at launch, reads a *frozen* bus-snapshot, forms its
   finding, and emits a `proposed` judgment (judgment stream) tagged with a corpus fingerprint
   (the field KT calls `corpus_hash_at_emit`, which we must define and populate) — *intended* as
   evidence it was formed *before* it saw peers.
3. **Channel opens.** Only now does the synthesizer read the explorers' judgments (a later
   invocation). Dispersion among the frozen `proposed` judgments *is* the noise measurement.
4. **Adjudication.** The tagging engine turns `proposed` → `accepted`/`withheld`/`unresolved`;
   `unresolved` that is real dissent escalates as `dissent_irreconcilable`.
5. **Close.** The close row (permanent) carries the convergence/dissent summary; the bus files
   for this `dispatch_id` age out under the medium-tier TTL; the `live/` view showed it all.

## Where each design lives

| Design element | Home | Tier |
|---|---|---|
| dispatch spec + outcome | the ledger | permanent |
| mediated hand-offs + frozen judgments | `telemetry/agents/bus/<dispatch_id>` (projection) | medium (TTL via `expires`) |
| the live "what is being said" view | `telemetry/agents/live/` over SSE (`signature()`, [ledger.py:790-808](../../implementations/server/ledger.py#L790-L808)) | ephemeral |
| pre-confirm sheets | `telemetry/agents/pending/` | pre-confirm |
| the closed facets + tagging contract | vendored from KT (open: vendor vs. couple) | reference |

## Open questions

1. **Coupling vs vendoring** — vendored KT schema vs a runtime dep; must be opt-in (portability
   principle: KT is not installed everywhere). **The central undecided axis — do not resolve it
   here.**
2. **Agent-level addressing** — mint `dispatch_id:group_id:role#index`; reconcile with the
   agent-pool MCP.
3. **Dual keying** — human `dispatch_id` (dedup) vs content-addressed `spec_hash`: keep both?
   Does `spec_hash` idempotency collide with dedup-on-`dispatch_id`?
4. **Open-`domain` dispersion** — inter-tagger agreement is unmeasurable on free strings until
   the engine's `edges-to-concrete-nodes` normalizes them. Re-opens BET-TAG.
5. **η^sch ⊥ η^ins vs bias ⊕ noise** — is KT's two-kind residue the same orthogonality as the
   conceptual thesis's, subsumed, or new? Routes to [[anti-noise-orchestration]].
6. **Live-listening under zig-zag/feedback** — does the inversion hold when a dispatch needs
   mid-flight cross-agent reaction, or is that always re-invocation?
7. **TTL duration for `bus/`** — the user flagged this as "to be defined"; `expires` gives the
   vocabulary, not the number.

## Collapse-tests (what falsifies this thesis)

- **Projection collapses to duplication.** If the *lifecycle* stream cannot be reconstructed as a
  projection of the ledger — if the transport must hold authoritative content the ledger does not —
  then it *is* a duplicative store and the "not a duplicative store" claim is false. (The *judgment*
  stream is new content by design; its distinct test is EG-1: it fails if written by anything other
  than the validated appender.)
- **The spine it leans on is itself unproven.** The projection argument assumes EG-1 (one writer)
  holds. EG-1 is currently `veracity: medium` and promotion-blocked by the 2026-07-18 enum-drift;
  if that drift proves the ledger *cannot* have a single writer, the projection's integrity
  guarantee falls with it.
- **Freeze is unenforceable.** If `corpus_hash_at_emit` (or our `signature()`) cannot actually
  witness that a judgment was formed before the channel was read, "freeze before the channel" is
  decoration and the anti-noise guarantee on the bus is empty.
- **Inversion fails.** If a real dispatch genuinely needs an agent to react to the live bus
  mid-run (not at a re-invocation boundary), the one-shot model is insufficient and the
  "listening = inversion" claim collapses into a runtime change we said we would not build.
- **The macro tag cannot be governed.** If an open `domain` string cannot be normalized enough
  to measure dispersion, "agents emit `proposed`, the engine adjudicates" yields no noise signal
  and the tag design reduces to the agent-owned vocabulary it was meant to replace.

## Registered bets

- **BET-BUS-PROJECTION** (`veracity: low`, `conviction: high`): the bus's lifecycle stream can be a
  projection of the ledger, and the judgment stream a non-duplicative tier appended through the one
  writer — no second authoritative *duplicate*. **Falsifier:** Collapse-test 1. **Depends on** EG-1
  holding (itself unproven).
- **BET-FREEZE-WITNESS** (`veracity: low`, `conviction: high`): a content/corpus hash at emit is a
  sufficient machine-checkable witness of freeze-before-the-channel. *(KT's `corpus_hash_at_emit` is
  null/undocumented today; this bet assumes we can define and populate it.)* **Falsifier:** if two
  agents can share a corpus hash yet one demonstrably read the other first, the hash is no witness.
- **BET-REUSE-PORTABLY** (`veracity: low`, `conviction: medium`): *if* we reuse KT's parts, it can
  be done portably (vendored or opt-in dep) without a hard runtime requirement. **Whether and how to
  reuse/couple is Open question 1 — explicitly undecided; this bet does not presume vendoring.**
  **Falsifier:** if the reusable parts cannot be used without KT installed at runtime.
- **BET-TWO-RESIDUES** (`veracity: low`, `conviction: medium`): predicted↔produced tag divergence
  *maps onto* KT's two residues (schema ⊥ instance) and is better modelled as two counters than one
  metric. KT's M6 proves *its* two residues independent; that our divergence **is** those residues is
  unproven (Open question 5). **Falsifier:** if a single repair reliably closes both counters, they
  were not independent here.

## Connections

| Document | Relationship | Description |
|---|---|---|
| [[anti-noise-orchestration]] | `sibling` | The *conceptual* thesis; this is the *infrastructure* one. Shares the residue calculus and the freeze-before-channel primitive (promoted here from PENDING). |
| [[engine-constitution]] | `depends-on` | EG-1 (one writer) and EG-6 (never re-validate history) constrain the bus to a projection; this thesis proposes a new retention/artifact-class axis for CONST-ENG to ratify if it survives. |
| [[ontology-conventions]] | `governed-by` | Orthogonality (no second store that duplicates the ledger); `veracity`/`conviction` on the bets. |
| [[findings]] | `derives-from` | The reuse map that grounds every "reuse" claim here. |
| [[research]] | `grounds` | The full two-party discussion trail. |
| `cyberAlchemyAI/knowledge-taxonomy` | `alternative-to` / reuse-source | The external substrate whose schema, envelopes, and residue model this thesis may vendor. Coupling is Open question 1. |
