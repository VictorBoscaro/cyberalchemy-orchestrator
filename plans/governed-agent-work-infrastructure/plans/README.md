---
tags: [plans, subplans, research-program, agent-work-language, index]
node_type: readme
is_session: false
layer: [architecture, ontology]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Governed Agent Work Infrastructure — subplans

## 1. What is this?

Plans subordinate to this Plan. A subplan is a full Plan in its own right — it owns a `PLAN.md`
and declares `parent_plan` — but its objective is scoped by the parent rather than standing
alone. There is currently one.

## 2. Business Context

[`../../README.md`](../../README.md) owns the repository's canonical definition of a Plan, its
naming rule, and its authority boundary; this folder is where that contract recurses one level.
The single subplan, Agent Work Language Research, is the research program behind the parent
Plan's central bet: that governed agent work needs one common language covering kernel,
relations, authority, events, agents, plans and observability. The parent Plan indexes it
directly at [`../PLAN.md`](../PLAN.md) with the note "Resolved repository-owner authority;
proposal-only."

## 3. Why it matters

The subplan is `status: proposed` at v0.16.0 — heavily revised but not accepted — and its
identity is deliberately unresolved: it carries `plan_id: null` with
`identity_status: named-id-pending`. Anything that cites it must cite it by path, because it does
not yet have a stable id to cite. Its companion invariant set is marked
`authority: research-input-only` and is explicitly *not* a ratified requirement set, a
distinction that matters because the file reads like a specification of system laws.

## 📁 Navigation

- **`agent-work-language-research/`**: The research subplan for the common agent-work language.
  - **[PLAN.md](agent-work-language-research/PLAN.md)**: the subplan. `node_type: plan`,
    `plan_type: research-program`, `plan_role: research-subplan`, `status: proposed`, v0.16.0,
    created 2026-07-24. `plan_id: null` / `identity_status: named-id-pending`;
    `parent_plan: plans/governed-agent-work-infrastructure/PLAN.md`.
  - **[CANDIDATE-INVARIANTS.md](agent-work-language-research/CANDIDATE-INVARIANTS.md)**:
    candidates for the finite global law set the language and its infrastructure would own.
    `node_type: candidate-invariant-set`, `status: proposed`, v0.4.1,
    `authority: research-input-only`. Explicitly not ratified requirements.

## Connections

| Edge | Target |
|---|---|
| owned-by | [`../PLAN.md`](../PLAN.md) — the parent Plan, which indexes this subplan |
| governed-by | [`../../README.md`](../../README.md) — the canonical Plan contract |
| grounds | [`../essays/`](../essays/) — both system-view essays name this subplan as `related_plan` |
| sibling-of | [`../workstreams/`](../workstreams/) — bounded execution artifacts under the same Plan |
