---
artifact_kind: research-initial-definitions
status: active
date: 2026-08-17
subject: experiment-recommendation-trigger
---

# Experiment Recommendation Trigger — Initial Definitions

## Context

Cyberalchemy Orchestrator exists to keep agent work connected to the objectives, decisions,
assumptions, actions, and evidence that give it meaning. Its append-only dispatch ledger preserves
governed work across research, review, experiment, and implementation, while related artifacts hold
the substantive results that the ledger references only indirectly.

The local problem is a recurring transition failure: a person may conduct several research efforts,
reduce uncertainty, and accumulate usable evidence without turning any surviving claim into a
constructed artifact or an empirical test. A well-timed recommendation of a bounded validation
experiment could reconnect accumulated knowledge to action. A premature or unjustified
recommendation could instead interrupt legitimate research, misread missing telemetry as lack of
progress, or silently replace the person's intention.

## Purpose

This document establishes the informational context for research that will inform a later decision
about whether Cyberalchemy Orchestrator should recommend a validation experiment, what evidence
would justify such a recommendation, and whether the current ledger can support that judgment.

## Research Question (Can be refined)

Under what observable and governable conditions should Cyberalchemy Orchestrator recommend—without
imposing—a bounded validation experiment after a sequence of research work appears to have advanced
understanding without producing a constructed artifact?

## Confirmed Product Constraints

- The recommendation is intended to validate what already exists in the accumulated research, not
  to manufacture novelty or force implementation.
- The system must recommend at an appropriate moment rather than merely after an arbitrary count of
  research dispatches.
- The recommendation remains a suggestion to the person; it does not itself authorize, preregister,
  run, or adjudicate an experiment.
- Claims must not be stronger than the evidence available from the ledger and its governed
  artifacts.
- Research, experiment, and code are distinct live dispatch types in the current registry.
- The current audit ledger is append-only; its opening and closing records use a fixed validated
  schema.
- The person's intention and autonomy must remain attributable, contestable, and reversible when
  the system suggests a next step.

## Current Evidence Baseline

- The current dispatch registry exposes `research`, `code`, `review`, and `experiment` as live,
  routable types (`implementations/contracts/dispatch-type-registry.v1.json`).
- A current dispatch opening can record its type, goal, context, parent dispatch, working folder,
  groups, connections, and creation time. Its closing record contains a closed exit vocabulary,
  agent counts, feedback prompts, and close time (`.codex/skills/register-dispatch/SKILL.md`).
- The ledger reader can join opening and closing rows, distinguish open and closed work, and
  aggregate dispatches by type (`implementations/server/ledger.py`).
- A local audit concluded that a close row cannot introduce a new typed distinction; it only fills
  fields fixed by the current schema (`vault/audit/close-row-enrich-c.md`).
- DomainSpec precedent treats experiment selection as decision-relative and asks for a linked
  hypothesis, decision owner, disconfirming outcome, feasibility blockers, and recommended next
  step (`../domainspec-core/implementation/mars/templates/experiment-candidates-template.md`).
- Superinterviewer research treats suggestion as one candidate intervention among asking,
  informing, reframing, waiting, stopping, and testing. It states that suggestion is appropriate
  when a reversible candidate could unlock learning and that intervention episodes should preserve
  before/after state, signal, contestability, consequence, and alternative explanation
  (`../superinterviewer/research/foundation-game-framing/research.md`).

## Known Gaps

- “Several researches,” “advanced understanding,” and “nothing was built” do not yet have accepted
  operational meanings for this decision.
- It is unknown which of those conditions can be established from the ledger alone and which require
  reading linked artifacts or collecting additional signals.
- It is unknown how reliably parent relationships and working folders connect research about the
  same objective across dispatches or repositories.
- It is unknown how to distinguish productive continued research from research inertia.
- It is unknown which missing decision, surviving claim, or unresolved uncertainty makes an
  experiment preferable to implementation, another research step, a question, waiting, or stopping.
- It is unknown how the system should represent uncertainty, abstention, user refusal, or a previous
  declined recommendation.
- It is unknown whether existing historical episodes are sufficient to evaluate a candidate trigger
  without first changing the ledger or instrumentation.

