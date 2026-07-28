---
tags: [agent-events, prompts, structured-responses, event-bus, provenance, open-tags]
artifact_kind: research-initial-definitions
layer: capability
version: 0.1.1
last_updated: 2026-07-27
---

# Agent Event Prompted Requests - Initial Definitions

## Context

Cyberalchemy is developing governed infrastructure in which human intent, agent work, runtime
events, contributions, evidence, and later decisions remain inspectably connected. The repository
has an implemented local journal and host lifecycle-hook path currently bounded by a
reload-and-smoke blocker, a bounded local-pilot publication slice, candidate bus and replay
architecture, frozen dispatch-prompt rules, host-observable input bindings, and exploratory
contracts for capturing attributed agent observations. These surfaces have different
implementation and authority status.

The immediate local problem is enabling a user to configure requests that reach selected agents at
specific moments in a research activity. A user may, for example, require every participating
agent to receive a particular prompt before and after the research and to return a validated
structured payload. The exact lifecycle occurrences denoted by "before" and "after" remain
unsettled. Open, non-enumerated tags are the first bounded case: several agents
may separately describe the same work, and their raw emissions may contribute longitudinal
evidence from which better classifications and artifact-schema rules are later proposed. Raw
recurrence alone is not sufficient to license those rules.
Resolving this boundary matters because prompt ownership, lifecycle events, agent-produced content,
validation, persistence, and bus delivery carry different authority and failure semantics even
when they appear as one user-configurable behavior.

## Purpose

This document establishes the informational baseline for research that will inform a later
discovery or architecture decision about configurable event-triggered requests to agents. It
records the already confirmed product boundaries, current repository evidence, and unresolved
questions that must be understood before deciding service ownership, durable record shapes,
runtime integration, or implementation sequencing.

## Research Question (Can be refined)

What is the smallest governed capability that lets a user configure which agents receive which
versioned prompt at which configured moments associated with the research, validate the structured
payload each agent returns, and publish attributable results through the existing communication
infrastructure or another explicitly governed destination, while retaining open-tag emissions as
evidence that may inform future schema development?

This question is explicitly refinable. It does not assume that prompt management, event
definition, trigger resolution, agent selection, payload validation, persistence, bus delivery,
projection, and later schema promotion belong to one service, artifact, runtime component, or
authority.

## Confirmed Product Constraints

- A user must be able to configure that all agents in a selected research context receive a
  specified prompt before and after the research. The exact runtime moments represented by those
  terms remain to be established.
- The configuration must be able to select which agents participate rather than assuming that
  every agent in every workflow receives every request.
- The request must identify the prompt to present and the structured payload expected in response.
- Agent-produced payloads require validation against an explicitly defined response shape.
- Each agent-produced payload must remain attributable to its producer.
- More than one agent may emit tags for the same task, research activity, or artifact.
- The initial tags are open strings without a closed enum. Their purpose is to retain inexpensive
  descriptive evidence that can improve the system and inform later artifact-schema rules.
- Open tags do not automatically become accepted classifications, artifact kinds, authority,
  permissions, truths, or schema constraints.
- The initial capability must support targeted tag prompts, such as asking for knowledge domains
  and their relevant branches, as well as broader prompts asking for any tags that materially
  represent the target.
- The intended capability must not be implemented as an invocable tagging skill.
- Markdown frontmatter and `Connections` are not assumed to be the final application,
  persistence, or enforcement mechanism for this capability.
- Prompt content, response shape, trigger moment, and selected agents must remain attributable and
  configurable without becoming hidden instructions or untracked runtime state.
- Information supplied after a dispatch has been confirmed must not bypass the existing boundary
  between frozen instructions and authorized data-only runtime inputs.
- Existing lifecycle hooks, append-only lineage, host-observable launch binding, and
  claim-not-greater-than-proof discipline must not be weakened.
- The work must not prematurely introduce a canonical tag vocabulary, final artifact schema, or
  general ontology.

## Current Evidence Baseline

- `research/prompt-control-plane-foundations/research-initial-definitions.md` already establishes
  the broader need to store, version, serve, select, and evaluate prompts and to configure what
  information is requested, from whom, and when. It leaves the service and runtime boundaries
  unsettled.
- `.agents/skills/domainspec-subagents-strategy/SKILL.md` requires confirmed prompt templates to
  remain frozen and distinguishes instruction-bearing prompt content from separately materialized
  data-only inputs. It also records that changing instructions, lenses, source boundaries, or
  output contracts invalidates confirmation.
- `docs/decisions/host-agent-dispatch-input-binding.md` records an accepted bounded host bridge
  that binds a confirmed parent dispatch, group, seat, frozen prompt-template digest, workflow
  manifest, exact source/output hashes, and host-agent turn. It explicitly does not claim the
  complete provider-side effective input.
- `docs/features/agents-communication-infra/WORK-PACK.md` records the implemented local journal and
  the locally passing host-hook path together with a reload-and-smoke gate for resuming governed
  code and review dispatches. Production enablement remains separately blocked.
  `docs/features/agents-communication-infra/experiments/bus-publication-probe/README.md` records a
  bounded persist-before-acknowledge probe, while
  `docs/features/agents-communication-infra/README.md` presents the broader draft architecture for
  bus delivery, receipts, replay, and agent publication. These surfaces have different authority
  and do not by themselves define a combined contract for configurable lifecycle moments, prompt
  revisions, selected agent audiences, response schemas, validation outcomes, and governed
  destinations.
- The current draft direction in `docs/features/agent-provenance-telemetry/discovery.md`
  distinguishes free agent topic emissions from system resolution and later interpretation. It
  preserves raw attributed strings and does not require tag IDs, equivalence mapping, or a
  canonical registry; older registry-bearing contracts under that feature are superseded.
- `.agents/skills/emit-topic-tags/SKILL.md` demonstrates an activation-scoped prompt and a bounded
  free-tag payload shape. Its deposit mode runs as a close epilogue after work finishes, suspends,
  or fails; it does not establish configurable before-and-after occurrences. It is evidence about
  elicitation and response constraints, not the intended service boundary for this work.
- `plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md` treats tags
  as low-cost descriptions that may precede stronger types and rules, while keeping assertions,
  evidence, acceptance, and operational authority distinct.
- `plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md` frames
  runtime events and attributed records as part of the path connecting local agent activity to
  broader work context, without treating a recorded event as sufficient proof of meaning or
  authority.
## Known Gaps

- The ownership boundary among prompt management, event definition, trigger matching, request
  configuration, agent selection, response validation, bus publication, and downstream projection
  is not settled.
- The service, module, and runtime ownership of the capability is not settled, nor is it known
  whether the bounded behavior should reuse one existing mechanism or require a new component.
- It is not established what owns the highest-level user configuration or how its prompt,
  lifecycle, audience, validation, and delivery concerns are divided.
- The identity and versioning boundaries among reusable prompt content, a response schema, a
  configured request, one runtime request occurrence, and one agent response are unsettled.
- The subject of a configured request lacks a settled typed identity, revision, and snapshot
  boundary: "the same task, research activity, or artifact" is not yet an executable target model.
- It is not established which authorized target and context material each occurrence presents to
  an agent, how that material is produced, or which path, revision, and digest evidence must bind
  it to the request and response.
- The authoritative vocabulary and semantics for before-work, after-work, completion, failure,
  cancellation, retry, resumption, group, dispatch, logical seat, and agent-activation moments are
  not settled.
- It is unclear which lifecycle occurrences must be emitted deterministically by the host and
  which records contain agent-authored assertions produced in response.
- It is not established when a configured request becomes part of the authorized instructions for
  a dispatch, or what re-confirmation is required when its prompt or response contract changes.
- The operational meaning and acceptable evidence for an agent "receiving" a prompt are not
  defined. Host-observable selection, materialization, and dispatch must remain distinguishable
  from provider- or model-side states that the current boundary cannot prove.
- The agent-selection model is unsettled, including selection by exact seat, role, group,
  capability, workflow scope, or a policy resolved at runtime.
- It is not known whether "every agent" refers to every logical seat, every physical activation,
  retries, replacements, helpers, reviewers, or only a declared subset.
- The response-schema language, registry, versioning, compatibility rules, and validation owner
  are not settled.
- Failure semantics remain open for missing, refused, invalid, late, duplicate, partially
  persisted, or unrecoverably ambiguous agent responses.
- Schema-valid response, durably accepted publication, delivered contribution, and semantically
  promoted knowledge are distinct states whose owners and transitions have not been defined.
- The configured destination, persistence boundary, delivery obligation, and meaning of
  "accepted" remain unsettled; use of the existing bus is a candidate rather than a confirmed
  requirement. It is also unsettled whether routing is configured per request or fixed by the
  runtime architecture.
- The required delivery guarantee and idempotency boundary are not settled, including how replay
  avoids presenting the prompt twice or accepting duplicate responses.
- The minimum provenance that must accompany an agent-authored payload, and which boundary is
  trusted to supply it, are unsettled.
- The relationship between one before emission and one after emission from the same logical agent
  is not defined, especially across retry, replacement, resumption, or prompt revision changes.
- It is not established whether raw emissions are stored independently, how aggregation preserves
  provenance, or whether any consensus view should exist without replacing the source emissions.
- The responsibilities and representations of persistence and transport have not been
  distinguished for this capability.
- The downstream tracking, query, comparison, and interpretation needs are not settled.
- It is unclear how sensitive or private observations are detected, retained, disclosed, redacted,
  or removed without corrupting provenance.
- The process by which accumulated open emissions may justify candidate vocabularies, fields,
  artifact kinds, relations, or schema rules is not defined.
- Prompt wording, examples, and revisions can induce agreement or selection bias in open tags. It
  is not known which additional agent or model conditions create correlated emissions. Agreement
  among seats or repeated strings must not be treated as independent evidence, semantic
  equivalence, consensus, or sufficient evidence for a schema rule without controlling for those
  conditions.
- The existing close-epilogue tagging telemetry must not be confused with the new capability. The
  boundary between their records and cadences across configurable occurrences, retries, and
  resumptions remains unsettled.
- It is not established what capability boundary should own tagging-specific behavior versus
  behavior shared with other configured agent requests.
- The appropriate breadth of configuration and event reaction remains unsettled.
- It is not known which parts of the existing agent communication runtime can support the bounded
  use case without introducing a second runtime, duplicate journal, or competing authority.
- The reload-and-smoke gate recorded by the cited work pack must be reconciled with current runtime
  evidence before the lifecycle-hook path is treated as operationally ready.
- The required durability guarantee and the boundary that owns and proves it remain unsettled.

## Connections

| Document | Type | Description |
|---|---|---|
| [`../prompt-control-plane-foundations/research-initial-definitions.md`](../prompt-control-plane-foundations/research-initial-definitions.md) | `refines` | Narrows the broader prompt-control problem to event-triggered requests, structured responses, and governed result routing. |
