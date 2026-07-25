---
tags: [agents, communication-infra, research-brief, invocation, collaboration-topology, task-orchestration]
node_type: research-initial-definitions
is_session: false
status: proposed
version: 0.9.0
last_updated: 2026-07-24
related_plan: plans/governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md
stream_id: R3-R4
target_discovery: docs/features/agents-communication-infra/discovery/agent-invocation-and-collaboration-topology.md
related_research:
  - research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md
---

# Research Initial Definitions: Agent Invocation and Collaboration Topology

## Context

This project is building infrastructure to manage subagents with defined properties—such as their
identity, objective, responsibilities, information, tools, and relationships with other agents.
The broader goal is to make multi-agent work reproducible, governable, and observable instead of
depending only on informal prompt coordination.

This research focuses on how subagents will use that infrastructure. It will define how a generated
dispatch becomes a set of concrete agent invocations and collaborations while preserving the
project's authority, communication, and evidence boundaries.

The creation of a Dispatch or task run from time, events, conditions, and reusable task
definitions, plus mandatory behavior attached around arbitrary actions, is separated into the
related `event-driven-obligations-and-task-orchestration` research. This document begins after a
Dispatch has executable authority and focuses on compiling its agent topology.

## Purpose

This document freezes the starting point for research that will inform the
`agent-invocation-and-collaboration-topology` discovery. It defines the question, boundaries,
known constraints, current evidence, and unresolved gaps before new evidence is collected or
conclusions are synthesized.

It is not a findings document, an executable dispatch configuration, a specification, or runtime
authority.

## Research Question (Can be refined)

How should one generated Dispatch, composed of groups, named reasoning agents, typed tools, source
responsibilities, and communication connections, compile into each agent's actual invocation,
effective tool access, scheduling dependencies, message permissions, and later mediated inputs
without creating a second authority beside the human-confirmed runtime Dispatch?

## Confirmed Product Constraints

The following are user-set constraints. Research may identify implementation consequences or
contradictions, but it must not silently weaken them.

- Humans do not hand-author the dispatch configuration; an orchestrator generates it.
- Human confirmation freezes the generated Dispatch as the single executable authority. Any change
  to topology, responsibility, capability, visibility policy, or other executable semantics requires
  a newly versioned and confirmed Dispatch.
- A generated Dispatch candidate may exist durably before confirmation so it can be found,
  inspected, reminded, declined, superseded, or otherwise dispositioned. Only a confirmed
  executable Dispatch may compile into agent invocations; candidate registration alone grants no
  invocation authority.
- Every dispatched reasoning agent has a canonical persona name selected from the agent-pool MCP
  path and receives that name in its invocation prompt.
- Typed tools such as Reference Scout do not receive reasoning-agent personas.
- An agent assignment directly carries its concise objective, context, references to check, tools,
  and expected output.
- Being listed under an agent's references means that agent is responsible for checking that
  source. A shared source may appear in multiple agents' lists.
- Scout supplies candidate references. The assigned agent may choose which candidates to inspect
  and may inspect a directly known additional source only within its effective source/folder
  authority.
- Every reasoning subagent should normally have Scout access. An orchestrator agent additionally
  needs governed subagent-dispatch capability and the strategy skill.
- Interviewer must exist as a configurable construct, but its classification as a mode,
  capability, skill, agent kind, session kind, or another concept must remain open until research
  establishes the useful boundaries. Its configuration must be able to define the interview target
  and scope, question-formation strategy, evidence available to it, mutable artifact boundaries,
  stopping conditions, and the properties and state carried by the resulting interview session.
- The system must permit progressive definition: a construct may be created with stable identity,
  provenance, and only the properties currently known, without requiring an exhaustive declaration
  of everything it is. Later classification or enrichment must preserve the earlier history and
  distinguish added knowledge from retroactively asserted fact.
- Interview sessions must be independently identifiable and observable. Their questions, answers,
  decisions, unresolved ambiguities, artifact changes, and terminal readiness assessment must
  remain attributable rather than surviving only in chat history.
- Delegated agents may have different tool profiles; a child does not automatically receive every
  tool available to its parent.
- Agents inside a Dispatch receive small, task-specific tool profiles rather than the
  orchestrator's general tool surface. Internal Scout-like research and a bounded Interviewer are
  candidate tools, but their exact inclusion remains assignment-specific.
- A delegated orchestrator must not invoke another orchestrator. Recursive object lineage and
  nested Dispatch relationships must not become recursive chains of orchestration authority.
- The root orchestrator may compile a recursively structured graph of Plans, Research,
  Discovery/Design, Specs, Code, Verification, and other WorkPackages into bounded leaf
  assignments. Structural nesting does not grant any leaf agent orchestration authority.
- A parent may explicitly select and materialize whatever context a child task needs within the
  parent's accepted authority. That context transfer is versioned, attributable input
  materialization; it is not automatic inheritance from a parent/child or generated-by relation.
- At every model turn, the model-visible boundary is the exact runtime-materialized effective input,
  the authorized tool schemas, and the mediated observations made available to that attempt. Later
  turns may therefore include authorized tool results, revealed peer contributions, downstream
  handoff inputs, rework instructions, or other policy-authorized observations; all must remain
  attributable to persisted authority and evidence.
- Static topology, mutable execution state, content visibility, and command authority are distinct.
  Compiled connections express scheduling and release relationships; they do not automatically
  create free-form message channels or grant visibility.
- Agents do not freely choose recipients or mutate routing. Runtime routing derives from the
  confirmed Dispatch, and command/control effects remain behind governed capabilities.
- Communication must support more than a linear pipeline, including reviewer pairs, fan-in to a
  summarizer, downstream reviewers, discussions, and bounded zig-zag/rework loops.
- Invocation and collaboration objects may participate in recursive typed structures. Dispatches
  and other agent-related constructs may contain, review, generate, or classify constructs of their
  own kind, while the no-nested-orchestrator boundary still applies to execution. These
  relationships must be typed, attributable, navigable, and observable rather than recoverable
  only from paths, prompts, or naming conventions.
- Parent/child or generated-by lineage does not automatically transfer authority, capabilities,
  budgets, evidence visibility, lifecycle state, or approval. Any inheritance must be explicit,
  scoped, and reconstructible from accepted authority.
- Feedback and zig-zag/rework create explicit new rounds, generations, or operations under finite
  limits. They do not rewrite accepted history.
- Fan-in and downstream handoff must preserve the dissent, provenance, source responsibility, and
  policy decisions needed by the consumer; synthesized prose alone is not sufficient evidence.

## Current Evidence Baseline

The prior [identity and tool-access findings](../agent-identity-and-tool-access/findings.md) establish
the initial implementation baseline:

- the agent-pool MCP recommends canonical names but does not yet issue durable selection authority;
- the current wrapper does not compile proposal JSON into an invocation;
- `task_name` is routing data and must not substitute for persona identity;
- ACI's confirmed capability resolution is the candidate single grant authority;
- per-attempt tool profiles and provider-visible persona binding are not operational yet; and
- Scout is operational as a typed lifecycle but is not automatically injected into every reasoning
  agent's profile.

The associated [collected returns](../agent-identity-and-tool-access/research.md) are evidence, not
ratified design.

Existing communication and routing work is also prior art for this research:

- the [bus-contracts discovery](../../docs/features/agents-communication-infra/discovery/bus-contracts/README.md)
  separates an immutable `RoutingPlan` compiled into the confirmed `DispatchSpec` from mutable,
  journal-derived `RoutingState`;
- that discovery also separates the Work Bus, command/control plane, kernel-generated handoff
  workflow, and realtime projection, and makes recipient resolution a runtime responsibility rather
  than an agent choice;
- the current [ACI domain model](../../docs/features/agents-communication-infra/specs/domain.md)
  already defines the provider-neutral `DispatchSpec`, `AgentInvocationPlan`,
  `MaterializedAgentInvocation`, `AgentExecutionRequest`, and `EffectiveInputArtifact` seams;
- the current [ACI workflows](../../docs/features/agents-communication-infra/specs/workflows.md)
  already require persisted reveal manifests before peer content becomes visible and materialize
  authorized revealed content into a later effective input; and
- the DomainSpec
  [subagent-topologies discovery](../../../domainspec/vault/discovery/subagents-topologies/discovery.md)
  supplies an epistemic topology taxonomy and a boundary: deliberate tension can address correlated
  bias, but topology alone cannot repair a loaded question, thin source coverage, or a biased single
  synthesizer.
- the related
  [event-driven obligations and task orchestration initial definitions](../event-driven-obligations-and-task-orchestration/research-initial-definitions.md)
  own the upstream questions of time/event/condition triggers, reusable task definitions, and
  mandatory behavior around actions; their eventual authority boundary constrains which Dispatch
  this invocation research may compile.

These sources constrain and narrow the research question; they must be cited and tested rather than
rediscovered. They remain evidence at their declared maturity levels and do not supersede the
human-confirmed runtime Dispatch as execution authority.

## Known Gaps

- The authority and maturity of the relevant ACI contracts are not yet settled consistently across
  discovery, specification, and implementation artifacts.
- The boundary between generated dispatch information and runtime-owned invocation evidence is not
  yet fully defined.
- The relationship among source responsibility, source access, observed ingestion, and citation is
  not yet fully defined.
- The inheritance rules for reasoning-agent, orchestrator, and typed-tool capabilities are not yet
  settled.
- The enforceable boundary between a delegated orchestrator and leaf agents is not yet settled,
  including how the runtime prevents an orchestrator from invoking another orchestrator and how it
  restricts leaf agents to small assignment-specific tools.
- The context materialization contract is not yet settled, including how a parent selects inputs
  for a child, proves source authority, records omissions and transformations, and binds the
  effective context to one attempt without calling it inherited state.
- Whether agent persona, role, mode, capability, skill, tool, and session type are distinct,
  overlapping, contextual, or derived classifications is not yet settled for configurable
  constructs such as Scout and Interviewer.
- The minimum creation contract for a partially defined construct is not settled, nor are the
  rules for later classification, contradictory classifications, removal, supersession, and the
  point at which execution requires a fully resolved effective contract.
- The Interviewer's configuration schema, question-selection policy, user-answer authority,
  resumability, branching, artifact-mutation permissions, and exit verdicts are not yet defined.
- The canonical compilation from declared groups and connections into immutable routing edges,
  release gates, responsibility mappings, visibility policies, and per-attempt inputs is not yet
  settled.
- The runtime semantics for fan-out, fan-in, reviewer pairs, discussions, and bounded
  feedback/zig-zag generations are not yet settled consistently across the candidate discoveries
  and the current executable slice.
- The mechanism that preserves independent judgment and dissent through fan-in, including review of
  a single synthesizer's output where required, is not yet settled.
- The representation of recursive invocation and collaboration is not settled, including relation
  identity and types, tree versus DAG versus cyclic graph semantics, depth and cycle limits,
  transitive projections, inheritance and override rules, orphan handling, and child terminal
  behavior.
- The compilation boundary from a recursively related work grammar into small agent assignments is
  not settled, including which context, stage obligations, promotion gates, and neighboring
  relations each leaf must see.
- The boundary between schedulable connections, authorized content delivery, agent-authored work,
  and command/control effects is conceptually established in prior work but not yet compiled into
  one verified invocation-and-collaboration contract.
- The exact handoff from an authorized scheduled or event-originated TaskRun into one immutable
  Dispatch is not yet established by the related research.
- The handoff from a pre-registered Dispatch candidate to a confirmed immutable Dispatch is not
  settled, including identity continuity, proposal-version binding, stale confirmation, terminal
  non-launch dispositions, and the projection that shows pending candidates without implying that
  they are executable.
