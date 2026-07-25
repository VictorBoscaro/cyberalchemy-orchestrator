---
tags: [agent-language, orchestration, progressive-typing, tagging, invariants, governance, recursive-relations, provenance]
node_type: conceptual
is_session: true
layer: [ontology, architecture, domain]
nature: [explanatory, technical]
status: active
created: 2026-07-24
timestamp: 2026-07-24T20:00:37-03:00
expires: 2026-09-22
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "Redefines cross-cutting language, governance, and ontology concepts that constrain future implementations."
---

# Agent Language Research Program

## Summary

The session began with an architectural reading of the repository and turned a broad agent-language
vision into initial research and planning artifacts. It recorded events, actions, obligations,
scheduling, multi-agent tasks, Plans as independent sessions, and progressive evaluation before
user notification. Scout and Interviewer became configurable constructs under progressive typing
without premature ontological classification. Tags became a cross-cutting property: any
addressable thing may be tagged, and authorized sources may generate declared, inferred, imported,
or proposed assignments with provenance. The architecture now distinguishes a finite kernel
invariant set per version from additional user-configurable invariants, with seven unratified
kernel candidates. The plan added the hypothesis that invariants must compose coherently and
participate in governed, observable feedback loops without acquiring implicit authority.
Hierarchy expanded into typed recursive relations for containment, classification, generation,
review, delegation, and provenance, separating lineage from authority and direct relations from
derived closure. A multi-level dashboard and declarative rules such as open-question sessions for
every document of a type were parked as explicit next steps. A two-agent review passed its
preparatory gates but was canceled by the owner before registration or execution, so the research
program remains proposed rather than executed.

## Contradictions

- questions `vault/ontology-conventions.md` — its current tag contract is limited to domain
  keywords and a fixed seven-label orthogonality model, while this session proposes generated,
  provenance-bearing tag assignments and progressively extensible classifications.

## Open questions

- What is the smallest independent kernel invariant set whose composition is jointly satisfiable,
  closed under primitive transformations, and sufficient for safe extensibility?
- Which recursive relation kinds require tree, DAG, or cyclic semantics, and how should inheritance,
  override, transitive closure, and termination differ among them?
- What common lifecycle can govern user-defined invariants and tag assignments without turning
  projections or generated classifications into authority?

## Next steps

1. Run the R1 language-kernel and typed-ontology research before hardening schemas or runtime types.
2. Resolve the tag and label tension with `vault/ontology-conventions.md` through explicit ontology
   governance.
3. Design the future `dispatch_type: plan` artifact contract and skill from the bootstrap plan
   before promoting the router entry from RESERVED to LIVE.
4. Create stream-specific research proposals for event envelopes, configurable constructs,
   recursive relations, feedback coherence, observability, and Git/GitOps boundaries.

## Recommendation

Prioritize the kernel-invariant, recursive-relation, and tag-governance questions before runtime
implementation, because they determine whether the later research streams can compose without
freezing premature classifications.

## Files touched

- `BACKLOG.md`
- `plans/README.md`
- `plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md`
- `plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/CANDIDATE-INVARIANTS.md`
- `research/agent-invocation-and-collaboration-topology/research-initial-definitions.md`
- `research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md`

## Owner directions registered

- Keep the system usable without event-driven automation while allowing events and actions to be
  attached modularly at selected pipeline points.
- Make dashboard views readable across multiple detail levels and preserve hierarchy, provenance,
  authority, and observability during drill-down.
- Permit rules over typed sets, including attaching an independently identifiable open-questions
  session to every document of a selected type.
- Preserve partial definitions: constructs may exist before their complete classification is known.
- Make tags universal and generatable while retaining assignment origin, evidence, and acceptance
  status.
- Represent multiple recursive hierarchies explicitly; child lineage must not imply inherited
  authority.
