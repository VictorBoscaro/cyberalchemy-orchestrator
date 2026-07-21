---
title: "Research trail — KT reuse discussion for the agent-events infra hypothesis"
node_type: discovery
is_session: false
layer: architecture, domain
nature: explanatory
status: exploratory
last_updated: 2026-07-20
tags: [orchestration, bus, events, knowledge-taxonomy, residue, tagging, retention, reuse]
---

# Research trail — Can the agent-events infrastructure reuse `knowledge-taxonomy`?

> Verbatim-substance record of a two-party design discussion held to answer: *what of
> `cyberAlchemyAI/knowledge-taxonomy` (KT) can the orchestrator's new event/communication/
> tagging/retention system reuse, and what must be built?* This is the **evidence trail**
> the infra hypothesis ([[orchestration-infra]]) cites — not the hypothesis itself. Medium
> retention: it lives in `research/`, never in `vault/`.

## Method

Two agents, **independent first** (each formed its position before seeing the other's —
practicing the very "freeze before the channel" rule under study), then **one exchange
round**. Anti-bias axis: *ground-truth reader* (what KT actually is) ⊥ *orchestrator-need
holder* (what our system needs). KT was read from a real clone of the private repo
(`git` cached credentials worked where `gh` was unauthenticated).

- **Reader** (KT ground truth): agent_name Kahneman-side not used here — a general reader over the clone.
- **Infra** (orchestrator side): held the design of the infra hypothesis without reading KT first.

> **Editor's corrections (post-review, 2026-07-20).** Two claims in the agents' words below were
> downgraded by the independent evidence review and corrected in [[findings]] / [[orchestration-infra]],
> but are left verbatim here as the record: (1) `corpus_hash_at_emit` called "the gift / a
> machine-checkable witness" — in KT's actual log it is **null in 100% of rows and undocumented**, so
> it is a *candidate* field we must define, not a working witness; (2) the "dispatch model" section
> below pools `exit_reason` enum values partly from `experiments/E11-domainspec-adoption-pilot/validation/dispatch.yaml`,
> a different dispatch than the `discoveries/domain-hierarchy-standards/` one otherwise cited. The
> coherence review separately flagged that "bus = pure projection *plus* new content" was self-contradictory;
> the hypothesis now says **non-*duplicative*** store, with the judgment stream written through the one appender.

---

## Round 1 — KT ground truth (the reader)

Read from a full clone of `cyberAlchemyAI/knowledge-taxonomy`.

### 1. The faceted schema (v2.2)
- **8 upper types** (`schema/v2.2.md`): Entity, Event, Process, Quality, Role, Disposition, InformationObject, Proposition — chosen because they behave differently in a graph, not as philosophy.
- **6 facet axes**, orthogonal: `domain` (**open string — NOT a closed enum, NOT a hierarchy**, required), `nature` (concrete|abstract|symbolic|subjective), `normativity` (descriptive|normative), `temporality` (atemporal|instant|durative|cyclic), `source_confidence` (asserted|derived|speculative), `content_certainty` (definite|probabilistic|contested|unknown|refuted).
- **5 of 6 facets are closed controlled vocabularies; only `domain` is open.** `decisions/09-facet-value-enumeration.md` mandates enumerating closed values inline (an IRR test showed catalogers invent their own vocab otherwise — a *documentation* failure, not an ontology one).
- **Domain-hierarchy stance:** `discoveries/domain-hierarchy-standards/` ran a full dispatch asking whether to build a deep frozen domain tree. Verdict **`closed-negative`** — (a) fusing per-field standards (MSC/ACM-CCS/PhilPapers/PhySH) that classify different *kinds* of things creates edges with no semantics; (b) ~70% of a real corpus are cross-domain bridges ("framework F applied to domain D") a disciplinary tree discards. Constructive replacement: **method/framework as primary axis × domain-as-flat-facet**; per-field standards kept as independent gold, never fused. A separate live signal proposes a lighter `domain.top` (closed 10-class DDC-derived) + `domain.sub` (open) two-tier — still unshipped (v2.3+ work queue).
- Everything but `domain` is claimed to generalize everywhere; domain specificity is absorbed at the Claim layer (edges + external-authority URNs), not by growing types/facets.

### 2. The system-tagging engine
- Load-bearing constitutional stance (`README.md` §3, `docs/system-tagging-engine.md`): **"Tagging is system-generated, never hand-assigned."** Humans design/review/amend the rule set (governance); the system applies rules, records evidence, emits edges, preserves residue. Closing residue requires a *governance action* (amend a rule/catalog, register a target, declare scoped-out) — never writing the desired tag directly into one artifact.
- **Pipeline (ordered rule layers):** deterministic metadata → structural document → content-semantic (embeddings/classifiers) → graph-consistency → residue. Output contract: frontmatter tags + edges to concrete nodes/URNs (never free text) + audit trace. Assertion record: `rule_id`, `rule_version`, `rule_layer`, `confidence`, `confidence_basis`, `decision ∈ {accepted, proposed, withheld, unresolved}`.
- **Residue** = what the system could not honestly assign — typed (`unresolved.field_low_confidence`, `.field_conflict`, `.edge_needed`, `.schema_gap`, `.instance_residue`, …), each with evidence, blocking rule, severity, repair_path. E11 falsification explicitly includes "the pilot requires humans to decide tags case by case" and "accepted tags lack rule traces."
- **C7 (declared-scope-with-named-residue)**, `decisions/11`: no finite stack of classifiers saturates (`persistence_lemma`, proved in sister repo); KT stops by *declaring* a written enumeration of residues it chooses not to climb (v2.1 positivist scope + 5 humanities failure modes H1–H5 + decisions 01/06). `tower_tags.c7_declared` makes the declaration a computable set query (decision-12).

### 3. Event/telemetry format (two JSONL logs)
- `internal_tools/vault_telemetry/events/subagent-strategy.jsonl` — **dispatch lifecycle log**: `{event_name: subagent-strategy.dispatched|.closed, spec_hash, corpus_hash_at_emit, mode (robot-talks|ping-pong), dispatch_kind, dispatch_id, parent_dispatch_id (nullable), timestamp}`; `.closed` adds `{exit_reason, passes_total, convergence_passes, final_validator_verdict, residual_dissents}`. An open/close pair per multi-agent run, content-addressed by `spec_hash`.
- `docs/signals/pipeline-signals.jsonl` — **decision/ADR-lite signal log**: `{id(uuid), timestamp, session, feature, type: decision|pattern|proposal, severity, category, data{…}}`; decision-data has `{step, description, alternatives[], rationale, confidence}`; proposal-data has `{targetFile, changeDescription, rationale, priority, evidenceFrom}`.

### 4. Dispatch/agent model
- `dispatch.yaml` + `LEDGER.md` + per-agent `agents/NN-role-N.md`. Roles **explorer → skeptic → synthesizer → writer → auditor/reviewer**; each explorer a distinct `angle`, each skeptic an `attack_vector`. Inline `validator_block` checks goal-singularity, typed metric, role ordering, anti-bias pairing, `max_loops<=5`, slug format before the dispatch is trusted. `exit_reason` enum includes `dissent_irreconcilable`; `mode: zig-zag`; `executors: emulated` (Explore/general-purpose). Per-agent frontmatter carries `agent_id`, `layer_id`, `dispatch_id`, `role`, `model`, `decision`, `dissent[]`, `closure_mark` — i.e. `dispatch_id:layer_id:agent_id` compound addressing already exists, dispatch-scoped.

### 5. Residue & emergence
- Two-layer residue framework (from sister `domainspec-theorem`, `meta/framework-connection.md`): classification is a functor Δ: L1→L2 inducing **schema residue η^sch** (concepts L2 can't name — fixed by enlarging schema) ⊥ **instance residue η^ins** (round-trips that lose/hallucinate data — fixed by tightening Δ). The **M6 refutation** (Lean, no `sorry`) proves the two are *independent* — tightening schema does not buy instance discipline.
- `tower_tags` (decision-12): `residue_type`, `residue_status`, `tower_level_surfaced`, `surfaced_by`, `c7_declared`, `note` — makes the residue/C7 apparatus queryable off the corpus.
- **Emergence (E11→E12):** E11 ingest test (numeric gates: coverage ≥90%, ≥2 schema-gap witnesses, 0 free-text edges, 100% rule-trace, 0 submodule edits) → E12 emergence: does Type A residue *crystallize* into a new KT concept? Confirmed only under a non-relabeling condition (≥2 structurally distinct witnesses from ≥2 domains collapse to one concept no existing type/facet/edge expresses) — weak emergence only (Bedau–Chalmers).
- `meta/four-repos-residue-unification.md` names four repos as instances of one residue object: `domainspec-theorem`, `domainspec`, `arcanum`, `knowledge-taxonomy`. Marked `[position]`/`[open]`, not proved. **This orchestrator is not among the four.**

### 6. Reusable assets
- `schema/v2.2.md` (standalone faceted-classification spec), `docs/system-tagging-engine.md` (rule-driven residue-preserving pipeline — a spec, not shipped software), the two event JSONL formats, the dispatch model, `visualization/` (a graph explorer), and the `tower_tags`/C7 apparatus. Not reusable as-is: the 8 upper types / domain content (tuned to KT's problem), and the emergence machinery (coupled to the sister Lean repo, still `[open]`).

---

## Round 1 — Orchestrator freeze position (the infra holder)

Formed before reading KT. Load-bearing claims:

1. **The one-shot "listening" tension is resolved by inversion, not a runtime change.** The agent does NOT listen; the *orchestrator* listens (it's already the event loop); the agent gets a **frozen bus-snapshot at launch**. This is the only resolution that (a) preserves the star topology (`connections` are scheduling edges, not transport), (b) satisfies "freeze before the channel" — a continuously-listening agent is a live anchoring channel, exactly what the freeze kills, and (c) doesn't detonate the ledger discipline (a stateful always-on agent has no `close_of`, no `agents_spawned`). "Listening all the time" is a category error to correct, not a requirement to engineer.
2. **The bus should be a PROJECTION of the ledger, not a second store.** The ledger already holds every composed `initial_prompt` (groups JSON column) and `feedback_prompts` verbatim (close row) — mediation is already partly persisted. A second authoritative store violates orthogonality and risks drift from the ledger (the EG-1 one-writer spine exists to stop exactly this). The bus's real new content is the **independent-judgment ETE pre/post pairs**, which today have no home.
3. **"Agents decide their own tags" is incoherent for the MACRO tag, guarded for the THEME tag.** The macro tag must be system-generated against a governed vocabulary (letting each agent freely pick fights the substrate's convergence evidence). A **temporal contradiction**: the theme tag is meant to feed agent-pool name selection (a-priori, at dispatch, before output) AND be attached to every research (a-posteriori, from output). Resolution: dispatcher assigns an a-priori theme (a prediction) for name selection; the agent registers an a-posteriori theme from output; the predicted↔produced divergence is first-class residue.
4. **Needs from an external substrate:** a controlled `domain` vocabulary (stable ids, versioned); a deterministic classification engine; confidence facets (`source_confidence`/`content_certainty` → `veracity`/`conviction`); a bibliographic dedup key. **Event schema: only if it has one — predicted NO** (KT is a *classification* substrate, not an *event* one; conflating the two is the main failure mode).
5. **IDs:** `dispatch_id` and `group_id` exist (group_id is already a connection address); **`agent_name` is nullable and non-unique — a persona, not an identity.** No stable agent-level id today; addressing an agent requires *minting* one (`dispatch_id:group_id:role#index`). Ours to build.

---

## Round 2 — the exchange

### KT reader, reacting to the orchestrator's needs
- **(a) `domain` — "half-satisfiable" is generous; closer to a quarter.** `schema/v2.2.md:61` is explicit: `domain: <string>`, open, no enum, no ids, no versioning. Two attempts to close it both unshipped; the hierarchy attempt got `closed-negative`. What KT hands over is **a stance with teeth**: don't fuse a closed domain tree; make method/framework primary and `domain` a flat open facet; **budget a residue channel from day one**. This *contradicts* the orchestrator's stated need for "a controlled domain vocabulary" — KT tried that twice and backed off. What is cleanly reusable: the **5 closed facets**, esp. `source_confidence`/`content_certainty` as ready-made `veracity`/`conviction`.
- **(b) Bus store — the prediction is right for the need, wrong about why.** `subagent-strategy.jsonl` is a dispatch-lifecycle log (no `agent_id`, no message content, no agent-to-agent addressing); `pipeline-signals.jsonl` is session-keyed research-decision capture. **KT has no bus, confirmed.** But the `.closed` shape (`residual_dissents`, `convergence_passes`) is a validated precedent for "close-row carries the convergence evidence" — the orchestrator persisting the ETE pairs themselves (not just a count) is the natural refinement one level down. Use as confirmation, not code.
- **(c) System-tagging engine — validates the principle, does not supply the engine.** `README.md` §3 is a word-for-word precedent for "system assigns, humans govern the ruleset," backed by falsifiable E11. But `docs/system-tagging-engine.md` is a **spec, not shipped software** (the 90-artifact corpus was tagged by iteration/LLM/human-review, not a running engine). The orchestrator gets an **interface contract** (rule-layer ordering, decision classes, assertion-record shape, residue-class taxonomy) to build against; the classifier itself must be built (KT never built it either).
- **Direct improvement:** the a-priori/a-posteriori theme split *is* KT's **instance-residue vs schema-residue** distinction. Predicted↔produced divergence from a weak prediction rule = instance residue (tighten the rule); divergence because the produced theme isn't in the a-priori vocab = schema residue (enlarge the vocab). M6: fixing one doesn't fix the other → **encode two separate residue counters, not one "divergence" metric.**
- **Corroborations:** bus-as-projection — `schema/v2.2.md`: "hierarchy is a projection, not a stored tree; the graph is ground truth, the hierarchy is a view computed on demand." IDs — KT agents already carry `dispatch_id:layer_id:agent_id` (dispatch-scoped, not global) — confirms mint-per-dispatch. Frozen-snapshot inversion — KT never solved live-listening (single-shot batch), so **untested by KT, not validated.**

### Infra holder, reacting to KT ground truth
- **Concessions:** prediction "(b) KT has no events" is **wrong** (KT ships two JSONL logs); assumption "reuse a *closed* domain enum" is **wrong** (`domain` is open). But the deeper §3 claim ("agents don't own the vocabulary; production is governed") gets **stronger**.
- **(a) The event JSONL doesn't kill "bus = projection" — it gives it an envelope, split in two.** Reuse KT's two envelope shapes: **lifecycle stream** (`subagent-strategy.jsonl`) = bus transport projected from dispatch/close rows — `spec_hash` = message idempotency/dedup key, `parent_dispatch_id` = the dispatch level of the ID hierarchy, `.closed` metrics = aggregation + fork-guard telemetry, and **`corpus_hash_at_emit` is the machine-checkable witness for "freeze before the channel"** (reconcile with our `signature()`). **Signal/judgment stream** (`pipeline-signals.jsonl`) = the new frozen-judgment content (a `proposal` with `confidence` = a frozen judgment). Constraint: **vendor the schema, do not write into KT's files** (portability). A bus event whose `spec_hash` ≠ its ledger row = a corruption signal (EG-4 honesty, free).
- **(b) MACRO tag, restated with `domain` open:** not "pick from a closed enum." Reuses three things: (1) method/framework × domain-as-facet = the pre/post boundary exactly (method/framework a-priori → name selection; domain a-posteriori, open, from output); (2) the **5 closed facets** as the anchored common scale (`source_confidence`/`content_certainty` → `veracity`/`conviction` confirmed); (3) the **system-tagging engine as production governance** — `decision ∈ {proposed|accepted|withheld|unresolved}` + audit trace *is* the ETE + fork-guard lifecycle (`proposed` = frozen judgment, `accepted` = validated, `unresolved` = fork → `dissent_irreconcilable`). "Agents don't own the vocabulary" becomes "agents emit `proposed`; the engine adjudicates."
- **(c) Corrected reuse-vs-build split** — see [[findings]] for the consolidated version.
- **New open questions raised:** dual keying (`dispatch_id` vs `spec_hash`); open-`domain` dispersion (can't measure inter-tagger agreement on free strings — the engine's `edges-to-concrete-nodes` must normalize first); η^sch⊥η^ins vs bias⊕noise (same axis, subsumed, or new? routes to HYP-ORCH-NOISE).

## Connections
| Document | Type | Description |
|---|---|---|
| [[findings]] | `resolves` | The consolidated reuse/build map + open questions distilled from this trail. |
| [[orchestration-infra]] | `grounds` | The infra hypothesis this trail is evidence for. |
| [[anti-noise-orchestration]] | `contextualizes` | The conceptual thesis; the residue/freeze primitives promoted here originate there. |
