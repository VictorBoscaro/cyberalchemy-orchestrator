---
tags: [orchestration, agents, dispatch, ledger, architecture, residue]
node_type: premise
is_session: true
layer: architecture, domain
nature: explanatory
status: active
created: 2026-07-20
timestamp: 2026-07-20T23:00:21-03:00
expires: 2026-09-18
conversation_id: d51af106-948f-4af6-ab5e-db42a184ae21
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Seeds the durable infra hypothesis (bus persists mediation, KT facet/tag-contract reuse, schema⊥instance residue-counter tagging) that downstream event/bus work builds on, and it passed a formal two-reviewer gate that forced correction of real over-claims."
---

# Engine constitution, then the infrastructure hypothesis for agent events

## Summary

The session opened with whether this repo should have a development constitution like
ZefraHub's, and produced **CONST-ENG** (`vault/constitution/engine-constitution.md`) — a
candidate constitution ratifying discipline the ledger code already earned, with **EG-1**
(one validated writer) left promotion-blocked by the live 2026-07-18 enum-drift. The user
then expanded scope to a complex event/agent-communication system: ephemeral artifacts with
differentiated retention, a message bus (agents never message directly — they publish to a
bus another consumes), a live view, a 3-level id hierarchy (agent ⊂ group ⊂ dispatch), and
independent agent tag decisions (a theme tag feeding agent-pool name selection, a macro tag
from an external knowledge-taxonomy). Reconnaissance established that today agents never talk
directly (the orchestrator mediates; `connections` are scheduling edges), there is no bus and
no TTL machinery, and `robot_talks` persists only as a flag. The user chose **option 1** (the
bus *persists* the mediation, not decoupled delivery) and that the governance be a
**hypothesis** linked to CONST-ENG, not a new constitution. After the user corrected me for
designing without reading the private `cyberAlchemyAI/knowledge-taxonomy` (KT) repo, I cloned
it via git and found it is a classification *substrate* sharing this repo's DNA — a faceted
orthogonal schema (v2.2), a residue calculus, the same explorer/skeptic/writer/auditor
dispatch model, and JSONL event logs — with `domain` an open string, five closed facets,
system-generated tagging, and no bus. A two-party reuse discussion (each side forming its
position independently first, practicing freeze-before-the-channel) reconciled to: reuse KT's
five closed facets, its system-tagging interface contract, and its two event envelopes; build
the agent-level id, the ledger→bus projection, the retention tiers, and freeze enforcement
ourselves. The tag design was corrected from "agents decide tags" to "agents emit `proposed`,
an engine adjudicates," with predicted↔produced divergence modelled as two independent residue
counters (schema ⊥ instance). I wrote the durable **HYP-ORCH-INFRA**
(`vault/hypothesis/orchestration-infra.md`) plus the medium-retention discussion trail
(`research/agent-events-infra-hypothesis/`), holding the reuse-vs-couple tension explicitly
open. A registered two-reviewer dispatch (coherence ⊥ evidence) returned NEEDS-REVISION /
ACCURATE-WITH-CORRECTIONS — catching EG-1 treated as settled, `corpus_hash_at_emit` presented
as a working witness though null/undocumented in KT, a smuggled vendor conclusion, and a
self-contradictory projection collapse-test — all incorporated before this node.

## Contradictions

- questions [[engine-constitution]] — the infra hypothesis's projection argument leans on EG-1 ("one validated writer"), but EG-1 is `veracity: medium` and promotion-blocked by the 2026-07-18 enum-drift; the review caught it being treated as settled. Unresolved.
- questions [[anti-noise-orchestration]] — whether KT's schema ⊥ instance residue split (η^sch ⊥ η^ins) is the *same* decomposition as HYP-ORCH-NOISE's `bias ⊕ noise`, or a distinct orthogonal pair. Unresolved.
- questions [[orchestration-infra]] — its two load-bearing open questions stay undecided: reuse-vs-couple (vendored KT schema vs. opt-in runtime dep, turning on KT's installability) and live-listening under `zig-zag`/`feedback` edges (is mid-flight cross-agent reaction always re-invocation?).

## Next steps

- Trace the 2026-07-18 enum-drift that blocks EG-1: reproduce how two `close_of` rows with an off-enum `exit_reason` reached `telemetry/agents/subagents-dispatch.yaml` without passing `append-dispatch.cjs` `validateDispatch`. Method is known; only labor remains. This gates Phase 2 and the whole bus-as-projection claim.

## Recommendation

Attack the enum-drift trace first. The infra hypothesis's load-bearing claim — the bus is a
*projection* of the ledger, not a second store — rests entirely on EG-1's one-writer spine, and
the licensing fact here is that EG-1 is a **documented promotion-block** ([[engine-constitution]])
that the evidence review independently re-flagged. Until that drift is traced and the single
writer is either enforced or amended, the projection's integrity guarantee is unfounded and the
reuse-vs-couple decision is premature — so the next session should resolve the blocker beneath the
hypothesis before elaborating the hypothesis itself.

## Files touched

- vault/constitution/engine-constitution.md
- vault/hypothesis/orchestration-infra.md
- research/agent-events-infra-hypothesis/research.md
- research/agent-events-infra-hypothesis/findings.md
- research/agent-events-infra-hypothesis/review-coherence.md
- research/agent-events-infra-hypothesis/review-evidence.md
- telemetry/agents/subagents-dispatch.yaml
