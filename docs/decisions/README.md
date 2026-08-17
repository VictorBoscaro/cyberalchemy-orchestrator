---
tags: [docs, decisions, authority, governance, index]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/decisions

## 1. What is this?

Accepted decision records. Each file answers one settled question, carries `status: accepted` and
a date, and is written so that other artifacts can cite it by path as the authority for a choice
they depend on.

## 2. Business Context

In this repository a decision is not a note — it is a citable authority. Downstream artifacts
name the decision file that licenses them: the workstream
[`../../plans/governed-agent-work-infrastructure/workstreams/agent-reference-lineage-implementation-layering.md`](../../plans/governed-agent-work-infrastructure/workstreams/agent-reference-lineage-implementation-layering.md)
carries `authority.decision: docs/decisions/host-agent-dispatch-input-binding.md` together with
`selected_option: A`, and the Skill Control Center's `SPEC.md`, `queries.md` and `operations.md`
each cite [`skill-control-center-phase-1-scope.md`](skill-control-center-phase-1-scope.md) as
their scope authority. A decision landing here is what unblocks the work that references it.

## 3. Why it matters

Because these files are cited by path, they cannot be renamed, merged, or silently superseded
without breaking the authority chain of everything pointing at them. A reader arriving here needs
to know that this folder is a set of load-bearing references rather than a discussion log, and
that the option a record selects (not merely the question it raises) is the part downstream
artifacts bind to.

## 📁 Navigation

- **[host-agent-dispatch-input-binding.md](host-agent-dispatch-input-binding.md)**: `accepted`,
  2026-07-25. Which implementation boundary makes downstream host-agent inputs durable enough to
  run the planned multi-stage research topology. Option A is the selected option cited by the
  agent-reference-lineage implementation-layering workstream.
- **[phase-a-output-evidence-and-implementation-baseline.md](phase-a-output-evidence-and-implementation-baseline.md)**:
  `accepted`, updated 2026-08-10. Only the exact host-observed terminal response artifact may be
  producer-attributed `binding-output`, and the bounded repair uses the current Python + SQLite
  runtime baseline.
- **[repository-leverage-priority.md](repository-leverage-priority.md)**: `accepted`, 2026-07-25.
  Sequences the two leading capabilities — first repair and ratify the Host Binding → BUS
  reveal/materialized-input dogfood seam, then prepare and implement ACI-005, the opening
  materializer.
- **[skill-control-center-phase-1-scope.md](skill-control-center-phase-1-scope.md)**: 2026-07-25,
  gate result `PASS`. Bounds Skill Control Center Phase 1 to read-only/draft-only. Cited as scope
  authority across the `skill-control-center` feature package.
- **[typed-interaction-graph-research-execution.md](typed-interaction-graph-research-execution.md)**:
  2026-08-17, `accepted`. Executes the typed-relation research as governed stages because the
  current compiler cannot materialize downstream sequential handoffs before upstream agents run.

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| grounds | [`../../plans/governed-agent-work-infrastructure/workstreams/`](../../plans/governed-agent-work-infrastructure/workstreams/) — workstreams cite decisions as `authority.decision` |
| grounds | [`../features/skill-control-center/`](../features/skill-control-center/) — the Phase 1 scope decision bounds that package |
| authored-via | `.claude/skills/decision-gate/SKILL.md` — the decision-gate skill |
