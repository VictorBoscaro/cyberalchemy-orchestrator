---
title: "Findings — reuse map: KT × the agent-events infrastructure"
node_type: discovery
is_session: false
layer: architecture, domain
nature: reference
status: exploratory
veracity: medium
conviction: medium
last_updated: 2026-07-20
tags: [orchestration, bus, events, knowledge-taxonomy, residue, tagging, retention, reuse]
---

# Findings — what the agent-events infrastructure can reuse from `knowledge-taxonomy`

> Consolidated map from the two-party discussion in [[research]]. **Not a conclusion to
> legislate** — the leading candidate reading, with its central tension (*reuse-vendored vs.
> build-native*, and *how much to couple*) left **open**. Claim ≤ proof.

## The one firm finding

`cyberAlchemyAI/knowledge-taxonomy` (KT) is **not a tag list** — it is a **classification
substrate** sharing this repo's DNA: a faceted orthogonal schema (same shape as
[[ontology-conventions]]), a residue calculus (same `residue = shadow ⊕ structure` lever),
the same explorer/skeptic/synthesizer/writer/auditor dispatch model, and JSONL event logs.
It has **real reusable parts**. Whether and how much we reuse is what the hypothesis must
test — not assert.

## Reuse candidates (as vendored schema *or* opt-in dep — reuse/coupling is **Open question 3**, undecided)

| KT asset | What it gives | Caveat |
|---|---|---|
| `schema/v2.2.md` — the **5 closed facets** (`nature`, `normativity`, `temporality`, `source_confidence`, `content_certainty`) | The anchored common scale the noise axis needs. `source_confidence`/`content_certainty` → `veracity`/`conviction`. | `domain` is **NOT** reusable as a vocabulary — it is an open string (see below). |
| `docs/system-tagging-engine.md` | The **interface contract** for system-generated tagging: rule-layer ordering, `decision ∈ {accepted, proposed, withheld, unresolved}`, assertion-record shape, typed residue classes. | It is a **spec, not shipped software** — the classifier itself must be built. |
| `subagent-strategy.jsonl` envelope | The **bus transport** shape: `spec_hash` (a *proposed* idempotency key), `parent_dispatch_id` (nesting), `.closed` convergence/dissent metrics, and **`corpus_hash_at_emit`** — a *candidate* witness for *freeze-before-the-channel*. | No `agent_id`, no message content — a *lifecycle* log, not agent-to-agent transport. **`corpus_hash_at_emit` is null in 100% of KT's logged rows and undocumented (PENDING); `spec_hash`'s role is asserted, not documented in KT.** |
| `pipeline-signals.jsonl` envelope | The **frozen-judgment** shape: `type: proposal|decision`, `confidence`, `alternatives[]`, `rationale`. A `proposal`+`confidence` = a registered independent judgment. | — |
| The two-kind **residue model** (η^sch ⊥ η^ins; C7; `tower_tags`) | A richer residue model than a single divergence metric — Lean-proved independent (M6). | Whether it is the *same* orthogonality as `bias ⊕ noise` is an open question. |
| Dispatch-model overlap; `visualization/` graph explorer | External convergence evidence our dispatch model is right; a candidate live-view renderer. | Reuse as evidence / candidate, not blind import. |

## Build-native (no external owner — orchestration-internal)

- The **agent-level id** `dispatch_id:group_id:role#index` — KT addresses only to `dispatch_id`/`parent_dispatch_id`; `agent_name` is a nullable, non-unique *persona*, not an identity. Mint per dispatch (KT's per-agent reports carry `agent_id`/`layer_id`/`dispatch_id` as separate fields — a similar shape, not a literal joined id it constructs).
- The **ledger → bus projection** logic, keeping the ledger the authoritative permanent tier (CONST-ENG EG-1 one-writer, EG-6 never-re-validated). A bus event whose `spec_hash` ≠ its ledger row is a **corruption signal**. **Caveat:** EG-1 is itself `veracity: medium` and promotion-blocked by the enum-drift — the projection guarantee inherits that risk.
- The **retention tiers** (reuse `expires` + `signature()`), and the **ephemeral live-view file over SSE** — single integration point `signature()` ([ledger.py:790-808](../../implementations/server/ledger.py#L790-L808)).
- The **freeze-before-the-channel enforcement** — KT gives the *format* (`corpus_hash_at_emit`, `proposed` status); the *protocol* (when an agent may read others) is ours.

## The three corrected design moves

1. **"Agents listen to the bus all the time" → inversion.** The orchestrator listens (it is already the loop); each agent gets a *frozen bus-snapshot at launch*. The one-shot constraint and the anti-noise freeze point at the same design — they are allies, not a conflict. *(Untested by KT — its dispatches are single-shot batch; this is our claim.)*
2. **"Agents decide the macro tag" → agents emit `proposed`, the engine adjudicates.** `domain` is open, so the macro tag is not an enum pick. The **method/framework** an agent applies is a-priori (feeds name selection); the **domain** of the output is a-posteriori (open, registered from output). The vocabulary is the substrate's; the judgment is the agent's; the distribution is the noise axis.
3. **"One divergence metric" → two residue counters.** Predicted↔produced theme divergence splits into **instance residue** (weak a-priori rule — tighten it) and **schema residue** (theme absent from the vocabulary — enlarge it). M6 says fixing one does not fix the other.

## Open questions

1. **Agent-level addressing** — mint `dispatch_id:group_id:role#index`; reconcile with the agent-pool MCP.
2. **Dual keying** — human `dispatch_id` (`YYYY-MM-DD-slug`, dedup) vs content-addressed `spec_hash`. Keep both? Does `spec_hash` idempotency collide with register-dispatch's dedup-on-`dispatch_id`?
3. **Coupling vs vendoring** — KT as vendored schema (portability principle) vs runtime dep. Must be opt-in; the bus cannot hard-require KT present. **This is the central undecided axis — do not resolve it prematurely.**
4. **Open-`domain` dispersion** — inter-tagger agreement is not measurable on free strings; the engine's `edges-to-concrete-nodes` must normalize before dispersion is a signal. Re-opens BET-TAG.
5. **η^sch ⊥ η^ins vs bias ⊕ noise** — same orthogonality, subsumed, or a genuinely new axis? Routes to [[anti-noise-orchestration]].
6. **Live-listening under zig-zag/feedback** — does the inversion (orchestrator listens) hold when a dispatch genuinely needs mid-flight cross-agent reaction, or is that always re-invocation?

## Connections
| Document | Type | Description |
|---|---|---|
| [[research]] | `derives-from` | The full discussion trail this map distills. |
| [[orchestration-infra]] | `grounds` | The infra hypothesis these findings feed. |
| [[engine-constitution]] | `depends-on` | EG-1/EG-6 (ledger authority) constrain the projection; a new retention axis extends it. |
| [[anti-noise-orchestration]] | `contextualizes` | Freeze-before-channel and the residue calculus originate here. |
