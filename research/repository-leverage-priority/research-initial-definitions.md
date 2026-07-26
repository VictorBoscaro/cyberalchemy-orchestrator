# Repository Leverage Priority — Initial Definitions

## Context

Cyberalchemy is building governed infrastructure for agent work: a system in which purpose,
authority, context, execution, results, and evidence remain inspectably connected. The repository
now contains several partially implemented infrastructure lines and several research or discovery
lines whose dependencies overlap.

The immediate local problem is choosing the next bounded advance that will create the most reusable
construction capability for subsequent work. A poor choice could deepen one conceptual branch
without removing recurring friction elsewhere; a strong choice should shorten or strengthen many
future build cycles.

## Purpose

This document establishes the informational baseline for a repository-wide leverage assessment.
The resulting evidence will inform the owner's prioritization of the next infrastructure advance
and any later planning or implementation decision.

## Research Question (Can be refined)

Which currently available, unfinished, or narrowly creatable repository capability would produce
the greatest near-term leverage for continuing to build Cyberalchemy, considering reuse across
workstreams, dependency unlocks, validation strength, time to usable value, and risk?

## Confirmed Product Constraints

- The recommendation should maximize reusable tooling and construction leverage, not merely finish
  the most recent document or research thread.
- Existing lifecycle hooks, ACI authorization, append-only dispatch telemetry, and source-integrity
  controls must not be bypassed or weakened.
- Components should remain minimal and justified by a real purpose, consumer, and verifiable
  consequence.
- Claims of authority, effective enforcement, mathematical rigor, or runtime behavior must not
  exceed available evidence.
- The user explicitly authorized scouts and a repository fan-out for this assessment and does not
  require another conversational confirmation before the bounded read-only dispatch.

## Current Evidence Baseline

- The latest closed sessions identify four connected lines: governed multiagent execution; prompt,
  request, tag, and graph control; macro-to-micro system explanation; and Plan/formalization/Lean.
  See `sessions/2026-07-25-*.md`.
- Parent dispatch workflow binding and bounded host-workflow input binding have been implemented and
  exercised, while the general ACI invocation pipeline remains incomplete.
- Research and experiment workflows now require initial-definition artifacts before governed
  execution.
- Prompt-control research was invalidated after its confirmed baseline changed materially, so it
  has no accepted findings yet.
- The work-context companion identifies a first falsifiable macro-to-micro vertical slice, but its
  fixture corpus, thresholds, and maintenance-cost ceiling remain undefined.
- Repository work is currently concurrent and the worktree contains unrelated in-progress changes;
  this assessment must be read-only outside its own research and governance artifacts.

## Known Gaps

- The actual dependency centrality of the candidate capabilities across current plans, specs,
  work-packs, experiments, runtime code, tests, and open questions has not been compared.
- It is unclear which candidate removes the most repeated manual work rather than only advancing
  one feature.
- The relative time-to-value and implementation risk of the leading candidates are not yet
  normalized.
- It is unclear whether the best next move is a runtime primitive, a workflow compiler/profile, an
  observability/context-selection tool, or a narrow vertical experiment.
- The degree to which current dirty-worktree changes already advance or invalidate a candidate is
  not yet understood.
