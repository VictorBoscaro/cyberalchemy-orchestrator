---
tags: [plans, governance, dispatch, research]
node_type: plans-index
is_session: false
status: proposed
version: 0.1.0
last_updated: 2026-07-24
---

# Plans

This directory is the proposed canonical home for durable plan artifacts.

A plan is neither research nor execution:

- `research/` contains research inputs, collected evidence, and findings;
- `plans/` contains a proposed route for future work;
- a confirmed Dispatch or runtime TaskRun authorizes execution.

Each substantial plan should live at `plans/<plan-id>/PLAN.md`, carry a stable identity and status,
name its inputs and expected outputs, expose dependencies and decision gates, and preserve the
user request or other entry point that caused it to be proposed.

## Intended `dispatch_type: plan` convention

When `domainspec-subagents-strategy` eventually supports a LIVE `plan` type, its persisted output
should land under `plans/`. That convention is not active yet: the router currently marks
`dispatch_type: plan` as RESERVED and no plan-type skill owns its judgment, artifact contract, or
promotion gate.

The first manually authored plan in this directory is therefore a bootstrap artifact and a design
input for the future skill. It does not authorize subagents, research runs, implementation, or
automatic scheduling.
