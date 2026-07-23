---
tags: [agent-telemetry, provenance, dispatch, topic-tags, source-observation, skills, orchestration]
node_type: discovery
is_session: true
layer: [architecture, domain]
nature: explanatory
status: active
veracity: medium
conviction: high
version: 1.0.0
last_updated: 2026-07-23
created: 2026-07-23
timestamp: 2026-07-23T00:15:43-03:00
expires: 2026-09-21
decisions_made: true
contradictions_found: false
specs_updated: [docs/features/agent-provenance-telemetry/discovery.md, .claude/skills/emit-topic-tags/SKILL.md, .claude/skills/emit-topic-tags/references/host-contract.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "Establishes the provenance contract, separates agent and host responsibilities, and creates the empirical basis for later ontology decisions."
---

# Agent provenance telemetry and topic emission

## Summary

The session began by comparing agent communication protocols and bus contracts to decide where integration with the specification should deepen. Instead of merging or implementing the whole infrastructure at once, it identified observational telemetry as the smallest feature capable of producing useful evidence: conversation and turn identity, dispatch lineage, logical-seat activations, and papers or sources observed through mediated tools. Static `agent-pool` profiles were separated from actual execution topics, while only Knowledge Taxonomy's open `domain` idea was reused as inspiration for broad tags. The first topic design—registry, tag IDs, equivalence mappings, confidence and residue—was discarded because it fixed semantics before runtime observations existed; the agent contract became a free JSON string array with lineage added by the host. Empirical probes were preserved and amended to operate on raw strings, measuring overlap, drift, cost, source capture and lens utility without promoting equivalences. The emission instruction became `emit-topic-tags` and passed repeated independent reviews covering materiality, authorization, safety, retries, Unicode, provenance, disclosure and testing. Those reviews exposed two audiences: the agent needs a compact observation-and-emission procedure, while the host needs detailed mechanical and governance contracts. The final structure applies progressive disclosure through a short agent-facing skill, a separate host contract, a conformance and semantic release suite, and discovery v0.3 with no canonical registry.

## Open questions

- Will accumulated raw vocabulary become stable and reusable enough to justify an equivalence layer or canonical registry?
- Can exact-string and mechanically normalized projections produce a useful multi-agent lens without erasing meaningful lexical divergence?

## Next steps

1. Implement the minimal host wiring for conversation/turn identity, untyped origin edges, activation lineage, source observations and the topic-deposit tool.
2. Run mechanical conformance and the frozen semantic forward-test before enabling automatic topic capture broadly.
3. Execute the preregistered probes on raw observations before designing semantic mapping or registry authority.

## Recommendation

Prioritize the minimal host wiring and empirical runs; let observed vocabulary behavior answer the two open questions before adding semantic authority.

## Design boundary

Abstractly, the system observes before it classifies. Concretely, an agent emits `string[]`; the host owns identity, envelope, validation, privacy, persistence, normalization and projections.

## Files touched

- .claude/skills/emit-topic-tags/SKILL.md
- .claude/skills/emit-topic-tags/agents/openai.yaml
- .claude/skills/emit-topic-tags/references/host-contract.md
- .claude/skills/emit-topic-tags/references/conformance.md
- docs/features/agent-provenance-telemetry/README.md
- docs/features/agent-provenance-telemetry/discovery.md
- docs/features/agent-provenance-telemetry/prompts/topic-emission.md
- docs/features/agent-provenance-telemetry/probes/README.md
- docs/features/agent-provenance-telemetry/probes/v0.3-raw-tag-execution-amendment.md
- docs/features/agent-provenance-telemetry/probes/APT-P001-inter-tagger-agreement.md
- docs/features/agent-provenance-telemetry/probes/APT-P002-topic-drift.md
- docs/features/agent-provenance-telemetry/probes/APT-P003-vocabulary-coverage.md
- docs/features/agent-provenance-telemetry/probes/APT-P004-capture-cost-noise.md
- docs/features/agent-provenance-telemetry/probes/APT-P005-source-capture.md
- docs/features/agent-provenance-telemetry/probes/APT-P006-lineage-replay.md
- docs/features/agent-provenance-telemetry/probes/APT-P007-emergent-lens.md
- docs/features/agent-provenance-telemetry/research/current-state-inventory.md
- docs/features/agent-provenance-telemetry/research/seed-registry-gate.md
- docs/features/agent-provenance-telemetry/research/tag-curation-pilot-v01.md
- docs/features/agent-provenance-telemetry/contracts/README.md
- docs/features/agent-provenance-telemetry/contracts/verify_contracts.py
- docs/features/agent-provenance-telemetry/contracts/fixtures/conformance-vectors.json
- docs/features/agent-provenance-telemetry/contracts/fixtures/seed-registry-candidates-v01.json
- docs/features/agent-provenance-telemetry/reviews/2026-07-22-system-tags-and-lens-review.md
