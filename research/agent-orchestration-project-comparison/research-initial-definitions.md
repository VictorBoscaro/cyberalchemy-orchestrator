---
title: Agent-orchestration project comparison
status: initial-definitions
created: 2026-09-01
---

# Agent-orchestration project comparison

## Context

Cyberalchemy develops infrastructure intended to keep agent work connected to the objectives,
decisions, authority, assumptions, actions, and evidence that give the work meaning. Its currently
implemented orchestration stratum organizes, dispatches, and observes LLM subagents through a local
control surface, append-only records, operational skills, host integrations, and an opt-in local
runtime pilot. That delivered surface is narrower than the broader project objective and must not be
treated as equivalent to the complete intended system.

Eight public projects have been identified as potentially relevant precedents for agent dispatch,
durable execution, governance, approvals, audit, and observability. A grounded comparison matters
because their capabilities may expose useful mechanisms, unconsidered product territory, deliberate
boundary differences, or reuse opportunities. Without a shared informational baseline, however,
implemented behavior, documentation claims, proposals, and product aspirations could be compared as
if they had the same evidentiary standing.

## Purpose

This document establishes the informational starting point for comparative research that will
inform later discovery, target-model design, and bounded adoption decisions for Cyberalchemy. It
does not select features, grant external projects design authority, authorize code adoption, or
authorize implementation.

## Research Questions (Can be refined)

### Required program question

- **RQ0.** What do the eight selected projects demonstrably provide that could strengthen
  Cyberalchemy; what territory do they cover that Cyberalchemy is not currently proposing; what
  does Cyberalchemy demonstrably provide that they do not; which differences are intentional
  boundaries rather than gaps; and which concepts, patterns, or license-compatible implementations
  may be reusable?

### Comparison objects and evidence standing

- **RQ1.** Which Cyberalchemy capabilities are built, local-pilot, proposed, open, or contested, and
  what exact scope does each status cover?
- **RQ2.** Which capabilities does each selected external project demonstrably implement, and what
  are their evidenced completeness and operational standing?
- **RQ3.** Where do documentary claims, implementation artifacts, executable behavior, and
  independently verified results materially diverge for Cyberalchemy or any selected project?
- **RQ4.** Which project state or revision does each material capability claim describe, and beyond
  what temporal boundary does the claim cease to apply?

### Comparative boundaries and differentiation

- **RQ5.** Which selected projects are peers of Cyberalchemy's implemented orchestration stratum,
  and which are references from a different system layer or product boundary?
- **RQ6.** Which evidenced external capabilities are outside Cyberalchemy's current implemented and
  proposed surfaces?
- **RQ7.** Which evidenced Cyberalchemy capabilities are not evidenced within the inspected public
  surfaces of the selected projects?
- **RQ8.** Which material differences represent a deficiency, which represent a deliberate product
  boundary, and which remain undecidable from current authority?
- **RQ9.** What scope and uncertainty must qualify any negative claim that a project lacks a
  capability?
- **RQ10.** Which aspects of repository-local operation and governance/evidence-first behavior are
  confirmed product commitments, current implementation properties, or revisable design choices?

### Reuse, authority, and downstream decisions

- **RQ11.** Which externally evidenced concepts or patterns fit Cyberalchemy's objective and
  accepted boundaries without making precedent the authority for its target model?
- **RQ12.** Which externally evidenced implementations are technically compatible with
  Cyberalchemy's current or intended architecture?
- **RQ13.** What licensing constraints apply to any possible code reuse, including the unresolved
  receiving license for Cyberalchemy?
- **RQ14.** Which later discovery, target-model, or bounded-adoption decisions can this comparison
  inform, and what authority remains required before any result changes the project?

## Confirmed Product Constraints

- The comparison concerns these eight public repositories:
  `builderz-labs/mission-control`, `boundflow/boundflow`,
  `open-multi-agent/open-multi-agent`, `OrlojHQ/orloj`,
  `temporal-community/temporal-agent-harness`,
  `LF-Decentralized-Trust-labs/gitmesh`, `Chorus-AIDLC/Chorus`, and
  `chankov/agent-fleet`.
- Capability claims must not be stronger than their supporting evidence. A README statement alone
  does not establish that a capability is implemented, complete, or operational.
- Cyberalchemy must be represented through distinct evidence states rather than as one delivered
  object: built, local pilot, proposed, open, and contested.
- External projects are evidence and precedent. They do not define Cyberalchemy's target model or
  carry authority to change it.
- A capability difference does not by itself establish a product deficiency. An absence may reflect
  a deliberate boundary.
- Reuse may concern concepts, patterns, or code. Actual code adoption additionally requires a
  compatible receiving license, implementation fit, and a later adoption decision.
- This research supplies information to later decisions; it does not authorize implementation or
  automatically promote comparative findings into requirements.

## Current Evidence Baseline

- The root project objective is to preserve the warranted connection from low-level agent work to
  its objective, authorization, and evidence. Governed multi-agent dispatch is one implemented
  stratum of that broader objective (`README.md:23-38`).
- The runnable local baseline includes the reader/control plane and its UIs, an append-only YAML
  dispatch ledger, the agent-pool selector, operational skills, host-hook integrations, and an
  opt-in loopback ACI/APT pilot (`README.md:70-98`; `implementations/README.md:53-84`).
- UI confirmation currently writes a validated marker. It does not itself append the dispatch
  ledger or launch an agent; the later orchestration reaction remains separate
  (`implementations/server/main.py:311-353`; `implementations/README.md:13-22`).
- Structural dispatch enforcement exists through validated append and close operations, but that
  enforcement is narrower than the broader governance objective. Some lifecycle and decision
  properties remain outside deterministic enforcement
  (`.claude/skills/register-dispatch/SKILL.md:37-50,116-142`).
- Host-hook launch enforcement is implemented but host-dependent. Current project evidence records
  a Codex hook-bypass condition whose reload and live-smoke closure remain unresolved
  (`docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md:99-112`;
  `docs/features/agents-communication-infra/WORK-PACK.md:21-29`).
- The broader work language, full production write-side/runtime authority, formal typing, and parts
  of the decision and knowledge architecture remain proposed, open, or contested rather than
  delivered (`README.md:100-119`; `plans/governed-agent-work-infrastructure/PLAN.md:293-360`).
- The eight external repositories were selected through a preliminary GitHub and README-level
  relevance sweep. This establishes an oriented shortlist, not proof of their implementations. The
  preliminary basis is preserved in
  `robot-talks/2026-09-01-initial-definitions/dialogue.md:108-131`.
- An existing draft target-model branch requires the intended system to be derived from the
  project's own objective and constraints rather than predefined by existing mechanisms
  (`plans/autonomous-agent-graph-system/README.md:37-46`).
- Cyberalchemy currently declares no repository license, so compatibility with future distribution
  terms cannot yet be concluded (`README.md:14-16`).

## Known Gaps

- It is not yet established whether the eight repositories form one peer class or represent
  references from different system layers and product boundaries.
- Their implemented capabilities, completeness, operational status, and differences from their
  documented claims are not yet known at the evidence level required for comparison.
- It is unclear which external capabilities fall outside Cyberalchemy's current proposals and which
  apparently unique Cyberalchemy properties are absent from the inspected public surfaces of the
  other projects.
- The distinction between a useful external mechanism, a missing Cyberalchemy capability, and a
  capability that would violate an intentional product boundary remains unresolved.
- Repository-local operation is a current implementation property and portability intent, but its
  status as a lasting product constraint is undecided.
- The long-term boundary of governance/evidence-first behavior is not yet separated into immutable
  product commitments, current implementation properties, and revisable design choices.
- No single downstream decision, owning artifact, or decision authority has been designated as the
  sole consumer of the comparison.
- The public evidence needed to support a negative claim that another project lacks a capability is
  not yet established; absence from inspected material is not proof of absence.
- The relevant revision and time boundary for state-bearing comparisons across the nine evolving
  repositories has not been fixed.
- Cyberalchemy's receiving licensing posture is undecided, so code-level compatibility and adoption
  cannot presently be concluded even when an external repository has a declared license.
