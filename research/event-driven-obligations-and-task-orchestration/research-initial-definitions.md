---
tags: [agents, orchestration, research-brief, events, obligations, scheduling, task-recipes, labels]
node_type: research-initial-definitions
is_session: false
status: proposed
version: 0.5.0
last_updated: 2026-07-24
related_plan: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
stream_id: R2-R4
target_discovery: docs/features/agents-communication-infra/discovery/event-driven-obligations-and-task-orchestration.md
related_research:
  - research/agent-invocation-and-collaboration-topology/research-initial-definitions.md
---

# Research Initial Definitions: Event-Driven Obligations and Task Orchestration

## Context

This project is building infrastructure for governable, reproducible, and observable multi-agent
work. Its current local runtime can intercept supported host actions, authorize agent dispatches,
append lifecycle facts to an event journal, preserve input provenance, and rebuild read models
without granting authority to projections.

The next product need is to make that infrastructure programmable at more points in the pipeline.
The system must support mandatory behavior around selected actions and must also be able to start
specific multi-agent tasks in response to time, system state, or something that has happened.
Resolving the authority and composition boundaries matters because these capabilities must remain
modular without allowing automation, policies, or extensions to bypass the journal, capabilities,
dispatch governance, or review guarantees already present.

## Purpose

This document freezes the starting context for research that will inform the
`event-driven-obligations-and-task-orchestration` discovery. That later discovery will support
decisions about how mandatory action behavior, event- and time-originated execution, and reusable
multi-agent tasks relate to the existing ACI journal, host hooks, capabilities, Dispatch authority,
and invocation topology.

It is not a research plan, scheduler design, obligation schema, task recipe, executable
configuration, specification, or runtime authority.

## Research Question (Can be refined)

How should the orchestration substrate represent and govern modular obligations around actions, and
start reusable multi-agent tasks from time, event, condition, or manual origins, while preserving
explicit authority, idempotency, replay, provenance, and a minimum separation between worker and
reviewer?

## Confirmed Product Constraints

The following constraints were established directly by the user or by current authoritative
project boundaries. Research may expose tensions or consequences but must not silently weaken them.

- The system must be modular enough to add mandatory behavior at selected parts and levels of the
  orchestration pipeline.
- A mandatory behavior may require a typed event with a specific payload before an action and
  another typed event with a specific payload after it.
- Every event must expose a `tags` field so users and system components can attach multiple
  relevant labels without changing the event type. Tags are additive classification and discovery
  metadata; they do not replace event identity, provenance, authority, or the minimum payload
  required by that event's contract.
- Objects and relationships must also admit low-friction, progressively refinable tags or facets
  about concerns such as function, usability, relationship, and system level. An object may be
  recorded under partial knowledge before every relevant type or property is settled.
- Every accepted relationship must record its type, direction, origin, destination, scope, version,
  provenance, cardinality, transitivity, inheritance, and cycle policy. Relation-specific rules may
  form trees, DAGs, or controlled cyclic graphs rather than one universal hierarchy.
- Physical location is a derived property or view of an independently identified object; a path
  does not define the object's meaning, type, or authority. The same authoritative objects and
  relationships may support multiple folder or navigational projections.
- A caller must not always need to supply every event parameter explicitly. Event definitions may
  declare required minima, optional fields, defaults, templates, and fields resolvable from
  authorized context, provided the accepted event records the effective payload and the origin of
  every resolved value.
- For document reading, the system must be able to require a pre-read declaration and a post-read
  assessment that records whether the document remains worth using and what follows from that
  assessment.
- The system must support starting a specific task from a date or time, a condition, an occurrence,
  or an equivalent event-oriented origin.
- Scheduled and event-originated tasks must be easy to add without requiring bespoke orchestration
  code for every task.
- A meaningful generated or requested Dispatch candidate must be pre-registerable before it has
  executable authority so that it remains visible, inspectable, and recoverable across sessions.
  This pre-registration must not be confused with confirmation or with the official executable
  Dispatch ledger.
- Dispatch candidates awaiting a decision or launch must be easy for the user to see, and the
  system must be able to remind the user about actionable candidates so they are not silently
  forgotten.
- A Dispatch candidate that is never launched must still retain an attributable historical
  disposition and reason, such as declined, superseded, expired, blocked, cancelled, or
  not-launched, rather than disappearing.
- The minimum multi-agent task shape is two distinct agents with distinct responsibilities: one
  worker and one reviewer.
- Mandatory behavior and scheduled tasks must remain observable and attributable rather than
  depending only on prompt compliance.
- The system must support declarative rules over typed sets of objects, including rules such as
  “for every document of type X, establish an open-questions session.” The session must remain an
  independently identifiable object with its own properties, lifecycle, provenance, and typed
  relationship to each covered document.
- A future dashboard must make the system legible at multiple levels of detail. It must connect
  overview, layer, pipeline, agent, task, session, event, and artifact views without losing stable
  identity, relationships, provenance, or the distinction between authoritative facts and derived
  views.
- Dashboard detail must be progressively disclosed: essential context remains visible at first
  paint, while deeper operational, explanatory, and evidentiary detail remains navigable on demand.
- The existing ACI journal remains authoritative for accepted runtime facts; projections and
  telemetry do not independently authorize execution.
- Existing capability and append-before-ack boundaries must not be bypassed by a scheduler,
  trigger, obligation, task definition, host hook, or agent.
- The existing official audit-ledger authority and its validated write boundary remain in force
  until a separately governed cutover changes them.

## Current Evidence Baseline

- The current [ACI architecture](../../docs/features/agents-communication-infra/specs/architecture.md)
  separates commands, the event journal, effects, authenticated publication, artifacts,
  projections, and the official audit-ledger appender.
- The current [ACI workflows](../../docs/features/agents-communication-infra/specs/workflows.md)
  already use triggers in the local sense of starting a workflow from an accepted command, durable
  intent, restart, or state transition, and include recovery of worker effects.
- The [mandatory host wrapper](../../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md)
  demonstrates fail-closed interception before and after supported agent launches.
- The [dispatch ingestion integration](../../docs/features/agent-provenance-telemetry/integration/stage-g/reference-scout-and-ingestion.md)
  records supported tool use after execution and distinguishes exact file evidence,
  metadata-only observations, and opaque shell access.
- The [orchestration infrastructure hypothesis](../../vault/hypothesis/orchestration-infra.md)
  already proposes namespaced, versioned recipes that compile to common finite graph, permission,
  provenance, and terminal-outcome contracts, but does not establish scheduling or general
  obligation semantics.
- The related
  [invocation and collaboration topology research](../agent-invocation-and-collaboration-topology/research-initial-definitions.md)
  already covers compilation of a confirmed Dispatch into agent invocations, scheduling
  dependencies, message permissions, reviewer pairs, fan-in, and bounded rework.
- The executable slice has durable commands, idempotency keys, aggregate version checks,
  capabilities, events, artifacts, projections, Session-to-Dispatch linkage, and agent lifecycle
  hooks. It does not currently expose a general obligation registry, general trigger registry,
  calendar scheduler, or reusable task-recipe runtime.
- The sibling `maestro-trama` dashboard material provides non-authoritative reference patterns for
  progressive disclosure, self-explaining views, visible provenance and freshness, explicit
  unavailable or partial states, stable drill-down identity, and the separation of bounded-
  cardinality health metrics from rich per-occurrence events and traces. This evidence was
  inspected through an opaque read-only shell path and does not establish a design decision here.

## Known Gaps

- The boundary between an event, a condition over projected state, a temporal occurrence, and a
  command that requests execution is not yet settled for this product.
- It is unclear how a scheduled or event-originated run receives sufficient authority when the
  current model freezes executable authority through human confirmation of a Dispatch.
- The identity, minimum envelope, lifecycle, retention, and authority boundary of a pre-registered
  Dispatch candidate are not defined, including how it remains separate from an official
  confirmed Dispatch record.
- Reminder policy for pending Dispatch candidates is not defined, including relevance, cadence,
  deduplication, snooze/dismissal, staleness, escalation ceilings, and how reminders remain
  projections rather than confirmations or execution commands.
- The terminal disposition model for candidates that never launch is not settled, including who
  may classify the reason and when an inactive candidate is expired rather than merely pending.
- The product has not decided whether recurring authorization applies to a task definition, one
  schedule, one occurrence window, one generated Dispatch, or some combination of them.
- The inheritance and conflict rules for obligations attached at system, repository, workflow,
  Dispatch, agent, tool, resource, or individual-action level are not defined.
- The product has not settled which action phases are stable extension points or what happens when
  a required pre-action or post-action declaration is missing, invalid, late, or contradicted.
- The common event envelope and its minimum required fields are not defined, including tag
  identity, tag vocabulary governance, cardinality, namespacing, inheritance, and whether tags
  attach directly or through separately governed label assignments.
- The transition from loose tags or facets to accepted typed properties and relationships is not
  defined, including who may propose, validate, accept, supersede, or reject each refinement.
- The common relation envelope and the per-relation-type rules are not defined beyond the confirmed
  metadata dimensions, including which fields are always required, which are conditional, and how
  tree, DAG, and controlled-cycle policies are validated.
- It is unclear how physical folder trees and other navigational projections are generated from
  authoritative properties and relations, how several views coexist, and how path changes avoid
  rewriting object identity or semantic history.
- Parameter resolution precedence is not defined across caller input, event-definition defaults,
  templates, contextual derivation, and later enrichment. The system must still distinguish an
  omitted value from an unknown, unavailable, redacted, or intentionally empty value.
- The boundary between agent-authored judgments and kernel-observed facts is not yet defined for
  pre-action intent and post-action assessment events.
- It is unclear how obligation versions and their effective configuration are bound to an action
  so that later replay can establish which requirements applied at execution time.
- The relationship among a reusable task definition, a confirmed Dispatch, a TaskRun, agent
  attempts, and the existing audit-ledger opening and close rows is not settled.
- The worker-reviewer minimum does not yet define independence, visibility, review authority,
  revision limits, inconclusive outcomes, escalation, or terminal acceptance.
- Retry, missed schedule, overlap, backlog, cancellation, clock, timezone, and catch-up semantics
  are not defined.
- It is unclear which extensions may register new events, obligations, triggers, and task types,
  and how registration avoids creating a second schema, command, or journal authority.
- Selector semantics for rules over “all objects of type X” are not defined, including whether
  membership is evaluated continuously or from a frozen snapshot, whether rules apply
  retroactively, how exclusions and overrides work, and how reconciliation remains idempotent.
- The contract for an open-questions session is not yet defined: its ownership, status model,
  question identity, resolution and reopening semantics, relation to its source document, and
  behavior when the document changes all remain open.
- The dashboard's audiences, layer vocabulary, default altitude, navigation contracts, freshness
  guarantees, and authority-safe read models are not yet settled. It must not imply certainty,
  completeness, or causal conclusions that its underlying observations cannot support.
- The division of responsibility between host hooks, the runtime kernel, background workers, and
  provider adapters is not settled for actions that occur without an active interactive host
  session.
