---
hypothesis_id: HYP-ORCH-INFRA
title: "Thesis — The orchestrator's mediation made into an auditable substrate (bus, ids, retention, freeze)"
status: candidate
authority_level: exploratory
owner: Victor
created: 2026-07-20
last_updated: 2026-07-21
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
survives except what the audit ledger incidentally stores (the composed `initial_prompt` in the
`groups` column; `feedback_prompts` verbatim in the close row). Agents never address each
other; `connections` (`sequential | zig-zag | feedback`) are **scheduling edges, not
transport** (register-dispatch SKILL). The orchestrator is a star whose center forgets.

This thesis proposes to make that mediation into a **written, addressable, auditable
substrate** — a bus, an event journal, an id scheme, retention tiers, and a decision-science
protocol — while preserving append-only history and frozen independent judgment. The updated
claim in one line:

> **The bus is not a store: agents and the kernel publish through it; accepted publications and
> lifecycle transitions are persisted in the event journal. The audit ledger remains the
> highest-level record of authorization and outcome, written only by its appender. The knowledge
> store holds promoted epistemic content. These stores do not duplicate one another because each
> is authoritative for a different kind of fact.**

The thesis is falsifiable (see *Collapse-tests*) and, like its sibling, a **self-application**:
the substrate that records the orchestrator's judgments is itself governed by the anti-noise
discipline those judgments are meant to have (`freeze before the channel`).

## Context — what already exists

- **The audit ledger is already a two-event log** (EG-1): a dispatch row + a close row per dispatch,
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

### Bus, journal, audit ledger, and knowledge store have disjoint authority

The runtime carries two event families, mirroring KT's own split (whose envelopes we may vendor —
an open choice):

- a **lifecycle stream** — transitions, attempts, rounds, mediated hand-offs, delivery and commit;
- a **judgment stream** — each agent's **frozen independent judgment** (the ETE pre/post pair),
  including proposals, confidence, critiques and verdicts.

Both families are accepted through the bus contract and persisted in the **event journal**, which
is authoritative for reconstructing runtime state. Agents are logical publishers of their own
messages; they do not write journal files or tables directly. The kernel publishes lifecycle
events. A validated journal writer supplies ordering, idempotency and durable acceptance.

The **audit ledger** is deliberately coarser. It records the confirmed dispatch/spec reference,
authorization, and official terminal outcome. Only its appender writes it (EG-1). The
**knowledge store** is authoritative for promoted definitions, premises, decisions, claims and
typed relationships; agents may propose these through the bus, but promotion has its own governed
writer. Large immutable bodies live in an artifact store. Realtime is a projection and owns no
facts.

No stream is a duplicate merely because the same `run_id` links them. Duplication occurs only if
two stores claim authority for the same fact. Cross-store references and content hashes are
integrity witnesses; projections must remain reproducible from their authoritative sources.

Candidate envelopes may still reuse KT's `spec_hash` (a proposed idempotency key — undocumented in
KT), `parent_dispatch_id` (nesting), and `corpus_hash_at_emit`. The latter is null in 100% of KT's
logged rows and undocumented there (PENDING), so this runtime must define it or replace it with an
`input_snapshot_id` + content hash + visible event cursor. A hash alone does not prove that an agent
was prevented from reading peers; the bus ACL and reveal barrier must enforce that property.

### Agents publish; the kernel governs visibility and delivery

Agents publish positions, critiques, votes and contextual proposals through authorized bus tools.
Publishing does not grant access to peers' sealed content. The **kernel** owns the event loop,
persists accepted publications, applies the reveal barrier and builds a frozen snapshot for each
invocation. An adapter may implement a round as a new one-shot invocation or as a resumable provider
session; this is a capability difference, not a change in bus semantics.

The anti-noise rule remains: an agent must commit its initial judgment before it can read peers.
A continuously exposed peer feed would be the anchoring channel the freeze exists to kill. This is
untested by KT, so enforcement must be proved against every read surface (bus API, MCP, realtime and
debug endpoints), not inferred from prompt instructions or a corpus hash.

### Runtime identity is deeper than persona

`dispatch_id`, `run_id`, `group_id`, `agent_instance_id` and `attempt_id` are distinct. The existing
`agent_name` is a nullable, non-unique persona from the pool, not execution identity. A deterministic
display form such as `run_id:group_id:role#index` may be useful, but retries need their own
`attempt_id`, and provider sessions remain namespaced metadata. The exact minting scheme is open;
the non-conflation is not.

### Retention follows fact class, not transport directory

The audit ledger and promoted knowledge are **permanent**. Event-journal records follow a governed
durable-retention policy. Artifact retention depends on content class. Bus delivery state and
realtime connections are **ephemeral**. Drafts remain **pre-confirm** and editable; the confirmed
spec is immutable. The existing `expires` vocabulary is reusable, but no TTL/gc machinery exists
today (PENDING). Physical directories such as `bus/` or `live/` are implementation options, not
architectural authorities.

### Tags are system-generated judgments, not agent-owned vocabulary

The agent does not *pick* a tag; it **emits `proposed`**, and an engine adjudicates
`accepted | withheld | unresolved`. The **method/framework** it applies is a-priori (predictable
at dispatch → feeds agent-pool name selection); the **domain** of its output is a-posteriori
(open — `domain` is an open string in KT, deliberately un-closed). The predicted↔produced
divergence is **first-class residue**, and it splits — per KT's Lean-proved M6 — into **instance
residue** (weak prediction rule → tighten) ⊥ **schema residue** (theme absent from the vocab →
enlarge). Two counters, not one divergence metric.

### Dispatch types are governed registry entries, not a terminal enum

The current `0.6.1` appender validates a closed `dispatch_type` enum. That is the implemented
contract today, not the target ceiling. In the target runtime, system, organization, workspace and
user namespaces may register their own types and versioned recipes. A personal routine such as
`user.victor/monthly-knowledge-routine` is valid when its recipe compiles to the common finite graph,
message envelope, bounded-loop, permission, provenance and terminal-outcome contracts.

Strict-on-write survives this change: validation moves from membership in an enum embedded in the
appender to successful resolution of a namespaced type, installed recipe, schemas, capabilities and
allowed overrides. Historical rows keep their original raw type. A user-defined type must not add a
branch to the kernel; if it needs a new executable primitive, that primitive is installed separately
as a trusted extension.

## The pipeline as a worked example

A `research` dispatch with an explorer group and a synthesizer:

1. **Dispatch.** The dispatcher predicts a *method/framework* theme; it feeds agent-pool name
   selection. Confirmation appends the high-level dispatch row and the kernel records `run.started`
   in the event journal.
2. **Frozen judgment.** Each explorer, at launch, reads a *frozen* bus-snapshot, forms its
   finding, and publishes a sealed `proposed` judgment through the bus. The accepted message lands
   in the journal with `input_snapshot_id`, content hash and visible cursor; the ACL/barrier, not the
   hash alone, prevents peer reads.
3. **Channel opens.** Only after the barrier does the kernel reveal the explorers' judgments to an
   authorized synthesizer/aggregator. Dispersion among the frozen proposals is the noise measurement.
4. **Adjudication.** The tagging engine turns `proposed` → `accepted`/`withheld`/`unresolved`;
   `unresolved` that is real dissent escalates as `dissent_irreconcilable`.
5. **Close.** The journal commits the terminal group/run events; the audit-ledger appender writes the
   official close row. Realtime projects both without becoming authoritative. Promoted definitions,
   premises or decisions enter the knowledge store through its promotion writer.

## Where each design lives

| Design element | Home | Tier |
|---|---|---|
| confirmed dispatch/spec reference + official outcome | audit ledger | permanent |
| lifecycle events + accepted messages + frozen judgments | event journal | durable, policy-governed |
| message publication/delivery | bus | ephemeral transport; accepted content is journaled |
| promoted definitions, premises, decisions and claims | knowledge store | permanent/versioned |
| large outputs, patches, reports and snapshots | artifact store | content-class policy |
| live "what is being said" view | realtime projection over SSE | ephemeral/reconstructible |
| pre-confirm draft | draft store / current `pending/` compatibility surface | pre-confirm/editable |
| the closed facets + tagging contract | vendored from KT (open: vendor vs. couple) | reference |

## Open questions

1. **Coupling vs vendoring** — vendored KT schema vs a runtime dep; must be opt-in (portability
   principle: KT is not installed everywhere). **The central undecided axis — do not resolve it
   here.**
2. **Runtime identity** — define the minting and relationships among `dispatch_id`, `run_id`,
   `group_id`, `agent_instance_id`, `attempt_id` and provider-session ids; reconcile them with
   the agent-pool MCP without turning persona names into identities.
3. **Multiple keys** — human `dispatch_id`, execution `run_id`, versioned spec reference and
   content-addressed `spec_hash`: which operations deduplicate on which key?
4. **Open-`domain` dispersion** — inter-tagger agreement is unmeasurable on free strings until
   the engine's `edges-to-concrete-nodes` normalizes them. Re-opens BET-TAG.
5. **η^sch ⊥ η^ins vs bias ⊕ noise** — is KT's two-kind residue the same orthogonality as the
   conceptual thesis's, subsumed, or new? Routes to [[anti-noise-orchestration]].
6. **Invocation strategy** — when should an adapter use one-shot invocations versus resumable
   provider sessions, while preserving identical reveal and snapshot semantics?
7. **Journal and artifact retention** — `expires` gives a vocabulary, but duration, legal holds,
   compaction and garbage collection remain undefined.
8. **Cross-store commit** — how do journal terminal events, the official audit close and knowledge
   promotions recover from partial failure without pretending to be one transaction?
9. **Custom-type governance** — who may install, version, deprecate and revoke namespaced dispatch
   types and recipes at each scope?

## Collapse-tests (what falsifies this thesis)

- **Authorities overlap.** If two stores must independently decide the same canonical fact, then
  the separation is duplicative rather than orthogonal and the authority matrix must be redrawn.
- **A write boundary can be bypassed.** If the audit ledger, event journal or knowledge store can
  be mutated outside its designated validated physical path, provenance and replay cease to be
  trustworthy. The known audit-ledger enum drift is already a live warning for this test.
- **Freeze is unenforceable.** If an agent can read peer content through any surface before its
  sealed initial publication is accepted, a hash or timestamp cannot rescue the guarantee and
  "freeze before the channel" is decoration.
- **Provider mechanics leak into semantics.** If one-shot Codex and resumable Claude executions
  observe different visibility, ordering or commit rules, the adapter boundary has failed.
- **The macro tag cannot be governed.** If an open `domain` string cannot be normalized enough
  to measure dispersion, "agents emit `proposed`, the engine adjudicates" yields no noise signal
  and the tag design reduces to the agent-owned vocabulary it was meant to replace.
- **Custom types require kernel branches.** If each user-defined routine needs bespoke scheduling
  code instead of compiling to the common graph and policy primitives, `dispatch_type` is not
  actually extensible at the promised level.

## Registered bets

- **BET-DISJOINT-AUTHORITY** (`veracity: low`, `conviction: high`): event journal, audit ledger and
  knowledge store can coexist without duplication because each owns a disjoint class of canonical
  facts and all overlap is reference/projection. **Falsifier:** Collapse-test 1.
- **BET-FREEZE-ENFORCEMENT** (`veracity: low`, `conviction: high`): an ACL reveal barrier plus an
  accepted sealed publication and recorded input snapshot/cursor can make freeze-before-the-channel
  machine-checkable across providers. Hashes are integrity witnesses, not proof of unreadability.
  **Falsifier:** Collapse-test 3.
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
| [[engine-constitution]] | `depends-on` | EG-1 protects the current high-level audit ledger; its generalized write-boundary rule gives each future authoritative store one validated physical write path. EG-6 preserves historical records under schema evolution. |
| [[ontology-conventions]] | `governed-by` | Orthogonality (no overlapping authority between stores); `veracity`/`conviction` on the bets. |
| [[findings]] | `derives-from` | The reuse map that grounds every "reuse" claim here. |
| [[research]] | `grounds` | The full two-party discussion trail. |
| `cyberAlchemyAI/knowledge-taxonomy` | `alternative-to` / reuse-source | The external substrate whose schema, envelopes, and residue model this thesis may vendor. Coupling is Open question 1. |
