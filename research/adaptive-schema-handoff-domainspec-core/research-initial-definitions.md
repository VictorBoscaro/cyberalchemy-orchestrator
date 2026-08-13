# Adaptive schema handoff to domainspec-core

## Context

Cyberalchemy Orchestrator governs how agent work remains connected to its objectives, decisions, assumptions, actions, and evidence. The immediate concern is how work is handed to Vlad in the sibling `domainspec-core` repository without imposing a single fixed level of ceremony on every kind of change.

The target system needs to admit useful objects at a minimal schema while allowing those objects to be progressively worked into stronger, category-level forms. It also needs extension points so later learning can introduce additional classifications or information without invalidating the initial representation.

## Purpose

This document establishes the informational baseline for a repository-grounded proposal about the first handoff to Vlad. The resulting research will inform the shape, permission level, requirements, and extensibility expectations of that handoff and provide a reusable basis for later handoffs.

## Research Question (Can be refined)

How should Cyberalchemy Orchestrator frame a first, risk-proportionate handoff to Vlad in `../domainspec-core` so that a domain object can exist with a minimal schema, mature toward category-level treatment, and remain extensible as new knowledge appears?

## Confirmed Product Constraints

- The handoff target is Vlad in the sibling repository `../domainspec-core`.
- Permission level and requirements must vary with the risk and work level of the requested change.
- A valid object must be able to exist using a minimal schema.
- The same object must be able to mature toward category-level treatment.
- The design must leave room for later additions as the system learns, including mechanisms such as tags, an `other` option, and open fields where appropriate.
- The first handoff should establish a reusable pattern because more handoffs are expected later.
- Scouts operate in pairs.
- This initial cycle is read-only with respect to source trees and produces research evidence and a proposal, not an implementation in `domainspec-core`.

## Current Evidence Baseline

- Repository policy requires work to remain tied to objective, assumptions, decisions, and evidence (`AGENTS.md`).
- The installed subagent strategy routes synthesis and multi-perspective repository inspection through the `research` capability (`.codex/skills/domainspec-subagents-strategy/SKILL.md`).
- Governed research requires a typed dispatch, explicit confirmation, parent-bound launches, and append-only open/close receipts (`.codex/skills/subagents-dispatch-lifecycle/SKILL.md`; `.codex/skills/register-dispatch/SKILL.md`).
- Invoke advertises a handoff mode whose role is to select bounded, obligation-linked context rather than forwarding an entire session (`.codex/skills/invoke/SKILL.md`; `.codex/skills/context-builder/SKILL.md`).

## Known Gaps

- Which existing artifacts and conventions in `domainspec-core` already express minimal schemas, progressive refinement, categories, extensibility, permissions, risk, or handoffs.
- Whether a Vlad-specific handoff convention or skill already exists in `domainspec-core`.
- Where the authoritative `invoke handoff` mode contract lives, because the installed Invoke root references a companion file that is not present beside the generated skill copy.
- Which artifacts in Cyberalchemy Orchestrator are both relevant and safe to include in the first handoff.
- What the smallest reusable handoff packet should contain, and which requirements should be gated by risk rather than mandatory in every case.
