---
tags: [plans, orchestration, authority, identity]
node_type: conceptual
is_session: true
layer: ontology, architecture
nature: explanatory
status: active
created: 2026-07-25
timestamp: 2026-07-25T00:28:38-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated:
  - plans/README.md
  - docs/architecture/agent-language-system-view.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session establishes a proposed vocabulary and coherent storage shape for Plans while preserving unresolved identity, authority, and hierarchy questions."
---

# Plan Governance and Structure

## Summary

The session began by reconstructing the recent repository context and making the current bet on
governed infrastructure for agent work legible. It distinguished Lean's logical kernel and TCB
from domain contract kernels, an invariant metamodel, and a composition checker rather than
collapsing all of them into a “kernel of kernels.” Plan semantics were centralized in
`plans/README.md` as a named, versioned proposal that searches for authority but never creates
execution authority merely by existing. A descriptive name now precedes identity, with `plan_id`
left null until a later admission event derives it from the accepted name. Existing Plan material
was consolidated under one descriptively named root directory, with the language research,
launcher workstream, candidate invariants, and archived roadmap represented in their current
roles. Signals of lifecycle independence now cause the infrastructure to suggest a subplan rather
than compel the user to split one. The infrastructure owns slugs, IDs, metadata, authority search,
relations, and validation instead of requiring the user to perform that bookkeeping. A local
README was added as a navigation surface that explicitly creates no authority, promotion, or
identity. A read-only red-team review corrected one unsupported claim about the next SWU and one
stale structure tree, after which hashes, links, obsolete paths, and the diff check passed without
adding another architectural decision.

## Open questions

- What exact admission event assigns `plan_id`, and what deterministic normalization and collision
  rule derives it from an accepted descriptive name?
- What degree of objective, lifecycle, evidence, and authority independence should make the
  infrastructure recommend representing related work as a subplan rather than inline work?
- Is Plan the only route-bearing object allowed to remain durable while governing authority is
  unresolved?

## Files touched

- README.md
- docs/PLAN.md
- docs/archive/PLAN-v0.3-detailed-roadmap.md
- docs/features/agent-provenance-telemetry/integration/stage-d/PLAN.md
- docs/architecture/agent-language-system-view.md
- docs/discovery/agent-assertion-capture/README.md
- docs/discovery/external-tools/README.md
- docs/essays/decision-hygiene-hypothesis/README.md
- docs/features/agents-communication-infra/README.md
- docs/features/ui-studio/README.md
- plans/README.md
- plans/agent-language-research-program/PLAN.md
- plans/agent-language-research-program/CANDIDATE-INVARIANTS.md
- plans/governed-agent-work-infrastructure/README.md
- plans/governed-agent-work-infrastructure/PLAN.md
- plans/governed-agent-work-infrastructure/archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md
- plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
- plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/CANDIDATE-INVARIANTS.md
- plans/governed-agent-work-infrastructure/workstreams/brokered-agent-launcher-capability-bootstrap.md
- research/agent-invocation-and-collaboration-topology/research-initial-definitions.md
- research/agent-language-mathematical-formalization/research-initial-definitions.md
- research/agent-language-mathematical-formalization/research.md
- research/agent-language-mathematical-formalization/findings.md
- research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md
- research/foundational-kernel-and-formalization/research-initial-definitions.md
- research/repo-standing-investigation/investigator-builder.md
- research/repo-standing-investigation/investigator-theorist.md
- sessions/2026-07-24-1056-dispatch-cutover-launcher-recovery.md
- sessions/2026-07-24-2000-agent-language-research-program.md
- sessions/2026-07-24-2329-agent-language-formalization.md
- telemetry/agents/subagents-dispatch.yaml
- vault/axioms/axioms.md

## User direction preserved

- Subplan criteria are advisory signals for the infrastructure, not compulsory work for the user.
- The final pass must describe and validate the current state without deciding the remaining
  hierarchy and identity questions.
