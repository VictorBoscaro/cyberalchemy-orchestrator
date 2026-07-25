---
tags: [plans, infrastructure, navigation]
node_type: plan-index
is_session: false
status: active
last_updated: 2026-07-25
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Governed Agent Work Infrastructure

This directory contains the current root Plan for the repository's governed agent-work
infrastructure and the material organized beneath it. This README is a navigation surface: it
does not create authority, approve the proposed route, promote a workstream, assign a `plan_id`, or
change the status of any artifact.

## Start here

Read [PLAN.md](PLAN.md) for the objective, boundary, current hypothesis, child registry, and
relationship between what runs today and what remains proposed.

The repository-wide definition of `Plan`, including naming, identity, authority search, user
burden, and storage rules, remains owned by the [`/plans` README](../README.md). This local README
does not redefine that contract.

## Contents

| Name | Path | Current role |
|---|---|---|
| Governed Agent Work Infrastructure | [PLAN.md](PLAN.md) | Root Plan; named, with ID pending |
| Agent Work Language Research | [subplans/agent-work-language-research/PLAN.md](subplans/agent-work-language-research/PLAN.md) | Research subplan recorded by the root Plan |
| Candidate System Invariants | [subplans/agent-work-language-research/CANDIDATE-INVARIANTS.md](subplans/agent-work-language-research/CANDIDATE-INVARIANTS.md) | Candidate invariant set belonging to the research subplan |
| Brokered Agent Launcher Capability Bootstrap | [workstreams/brokered-agent-launcher-capability-bootstrap.md](workstreams/brokered-agent-launcher-capability-bootstrap.md) | Workstream recorded by the root Plan; not an independent Plan |
| Knowledge Machine and Agent Orchestrator Seed Roadmap | [archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md](archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) | Archived predecessor retained for provenance |

## Directory meaning

- `subplans/` contains work currently represented as a child Plan.
- `workstreams/` contains bounded work represented inside the root Plan without an independent Plan
  identity.
- `archive/` contains predecessor material retained for provenance rather than treated as a live
  sibling Plan.

These descriptions report the current repository state. They are not general criteria for deciding
how future work must be organized.

## Identity and authority status

The root Plan and research subplan have descriptive names and currently retain `plan_id: null`.
Their files record resolved repository-owner authority for maintaining proposal-only Plans. That
authority does not itself authorize execution.

The launcher workstream records unresolved governing authority. The archived roadmap is historical
material and does not govern the active Plan.
