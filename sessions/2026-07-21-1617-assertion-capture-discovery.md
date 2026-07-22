---
tags: [assertion-capture, knowledge-bus, provenance, hooks, anti-bias, orchestration, claim-graph, orchestration-infra]
node_type: discovery
is_session: true
layer: architecture, application
nature: explanatory, reference
status: active
created: 2026-07-21
timestamp: 2026-07-21T16:17:32-03:00
expires: 2026-09-19
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Root-cause design for the provenance-spine gap PLAN §5 names as blocking three problems, tri-angle-reviewed with defects corrected — but still an unbuilt, gated draft."
---

# Agent assertion capture — the source layer of the knowledge bus

## Summary

The session set out to design how the orchestrator captures the epistemic decisions agents make
inside a session — decisions, premises, hypotheses, doubts, definitions — which today evaporate into
the transcript. It converged on a self-emission model: the working agent (including subagents) emits
its own assertions at the source through a judgment-free tool, because an agent grading its own
records would be the correlated-bias failure the project exists to counter (emitter = stenographer,
never judge). Trust is relocated from the agent's honesty to two mechanisms — every assertion carries
a type-specific withdrawal condition (its falsifier), and a declared↔produced cross-check catches
confabulation. Capture rides the agentic loop: since no thinking hook exists, the tool boundary is
treated as the think boundary (seed at SubagentStart + silent-triggered PostToolUse nudge + mandatory
Stop sweep), with cadence bookkeeping token-free. The source layer is framed as the coarsest-quality
but source-truest tier of a knowledge bus — valuable as immutable testimony (provenance), the root of
the missing provenance spine, and the K-only floor where enrichment happens only when refinement adds
relations. These decisions were parked in a new discovery rather than forced into HYP-CLAIM-GRAPH,
since the material spans claim-graph, orchestration-infra, a future feature, and experiments. Three
subagents reviewed it on opposed angles (falsifier ⊥ coherence ⊥ feasibility): the hook facts held,
but the review surfaced overclaims, citation errors, and real build gaps. Honesty and citation
defects were corrected inline (softened "provably", fixed the proposed→accepted→superseded
mis-attribution, AX-*→P-*, EG-6→EG-1, folder→file link, "answers"→"candidate answer", the
C4-immutable × OQ-3-editable contradiction, the token-free undercount). The keystone (that "form ≠
quality" rests on untested inter-tagger agreement, CT1) and build gaps G1–G8 were recorded in the
discovery's §6 as decisions, and a ledger registration of the review was left unregistered pending
the human confirm the register-dispatch discipline requires.

## Contradictions

- questions [`vault/hypothesis/claim-graph.md`](../vault/hypothesis/claim-graph.md) — the design
  makes CT1 / BET-CLAIM-TYPES (still open and untested there) the single load-bearing keystone of the
  whole capture architecture (the C1→C2→C3 cascade in the discovery's §6), and its answer to that
  node's Open Question #3 is explicitly a *candidate*, not a discharge — raising the stakes on an
  unresolved bet without resolving it.

## Open questions

- Can the declared↔produced cross-check on Codex (which has no context injection) recover enough to
  make the source layer more than Claude-only in practice, or is the "source-truest, well-formed
  assertion" structurally a Claude-only artifact (discovery G5)?
- Can capture bound its own contamination of the reasoning stream it means to record cleanly — the
  PostToolUse nudge injects between a tool result and the next thought (discovery G7)?

## Next steps

1. Design and run the OQ-1 experiment — inter-tagger agreement on assertion-type / edge-type — via
   the experiment-harness, before any build. It is the cheapest falsifier of the keystone.
2. Resolve build gaps G1–G4 before handing §3 to an implementation plan: lineage resolution path
   (`session_id`/`dispatch_id` for a subagent with no dispatch row yet), physical home (OQ-3),
   `agent_id`-keyed concurrency-safe counter, and the new store's own single-writer + authority-overlap
   review (OQ-5).
3. Once stabilized, promote the pieces to their homes: C1–C3 → HYP-CLAIM-GRAPH, C4–C5 → HYP-ORCH-INFRA
   (discovery OQ-6).

## Recommendation

Attack the keystone first. The entire capture design stands or falls on whether typing is reliable —
if independent runs cannot agree on an assertion's type and slots above chance, "form ≠ quality"
collapses and the emitter is judging under a new label, taking C1→C2→C3 and the anti-bias rationale
with it. Run OQ-1 as the cheapest test before investing in the tool, the hooks, or promotion; all
three reviewers and the discovery's own §6 isolate this as the load-bearing keystone.

## Files touched

- docs/discovery/agent-assertion-capture/README.md

## Extra section

Two mandates the user stated explicitly, to register verbatim in intent:
- **The emitter records but never judges quality** — *"esse agente não vai decidir nada sobre a
  qualidade do que ele está registrando, ele só vai registrar."* This is the stenographer principle
  and the anti-bias root: self-grading = the correlated-bias failure the project counters.
- **The source layer is the coarsest tier but valuable for being at the source** — it is refined
  downstream "both with other gates and comparing things, and with specific processes," never
  rewritten.
