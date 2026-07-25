---
tags: [agents, orchestration, category-theory, lean, formalization, architecture]
node_type: conceptual
is_session: true
layer: [architecture, domain]
nature: [explanatory, technical]
status: active
created: 2026-07-24
timestamp: 2026-07-24T23:29:59-03:00
expires: 2026-09-22
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "Establishes the program's canonical single-Plan organization and a mathematical model that will guide architecture and subsequent Lean implementation."
---

# Agent Language Mathematical Formalization

## Summary

This session consolidated the Agent Language Research Program around one Plan instead of treating
each research directory as an independent plan. Research directories became evidence nodes with
bidirectional plan and stream metadata across the foundational, formalization, invocation, and
event-driven briefs. Three independent formalization designers examined category-theoretic
structure, Lean mechanization, and infrastructure correspondence. They converged on a many-sorted,
proof-relevant typed multigraph, with category structure earned only by relation families that
have explicit composition laws. The resulting model separates semantic structure, accepted
runtime facts, derived projections, executable authority, and physical effects. The system view
received a mathematical-first appendix covering typed relations, witnessed derivations, history,
projections, authority, explicit context materialization, recursive work, finite bootstrap,
propositions, countermodels, a Lean roadmap, residue, and governed Open Questions. The Plan now
requires implementing the reviewed Lean subset, running a real build, auditing dependencies,
`sorry`, and axioms, and iterating until the selected obligations pass or evidence changes the
model. The formalization design dispatch closed as resolved, while staged mathematical and Lean
review and the actual Lean implementation remain pending. No new research directory was created;
the evidence and findings remain in the existing formalization node.

## Open questions

- What are the minimal primitive carriers, and can a shared `Object` abstraction avoid collapsing
  semantically distinct constructs?
- Which relation families admit categorical composition, partial composition, or no composition?
- What finite bootstrap roots and ownership contract can stop compatibility checking without
  pretending to provide absolute self-justification?
- Which formal claims should remain explanatory, generate validators, or become governed evidence?

## Next steps

1. Freeze the current appendix revision and run the first two-reviewer mathematical and
   categorical review layer.
2. Run the second two-reviewer Lean-mechanizability and infrastructure-correspondence layer on the
   resulting frozen revision.
3. If the sequential layers disagree materially, run a third layer with fresh reviewers.
4. Encode the accepted Lean dependency cone, run the real build, audit `sorry` and axioms, and
   iterate until the selected obligations pass or a documented blocker changes the model.

## Recommendation

Review and falsify the small typed-graph correspondence core before expanding its categorical
structure or implementing Lean, because the accepted countermodels now provide concrete tests for
whether each abstraction preserves the infrastructure's authority boundaries.

## Files touched

- `docs/architecture/agent-language-system-view.md`
- `plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md`
- `research/agent-invocation-and-collaboration-topology/research-initial-definitions.md`
- `research/agent-language-mathematical-formalization/research-initial-definitions.md`
- `research/agent-language-mathematical-formalization/research.md`
- `research/agent-language-mathematical-formalization/findings.md`
- `research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md`
- `research/foundational-kernel-and-formalization/research-initial-definitions.md`
- `telemetry/agents/subagents-dispatch.yaml`

## Owner direction registered

Research rounds, mathematical subtopics, and review layers that remain inside the same research
question must not create additional directories. They must stay connected to the single Plan and
reuse the existing research node so the repository does not accumulate disconnected folder noise.
