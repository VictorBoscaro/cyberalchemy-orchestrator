---
tags: [plans, subagents, agent-work, infrastructure, target-model]
node_type: branch-intent
is_session: false
status: draft
last_updated: 2026-08-03
---

# Subagent Work Infrastructure

## Product overview

Work performed by subagents is difficult to trust, control, and understand as it grows beyond a
single conversation. Tasks, decisions, prompts, intermediate outputs, reviews, messages, artifacts,
and execution state become distributed across chat history, files, temporary processes, and
unrelated logs. An artifact may exist without a reliable explanation of which work produced it,
which inputs were used, which decisions authorized it, or which later work depends on it.

This fragmentation makes basic questions unnecessarily difficult to answer. It may be unclear which
work is currently active, which tasks are blocked, which decisions remain unresolved, what the
current accepted state is, why a particular action occurred, or whether a produced result followed
the workflow that was approved. A successful output alone does not establish that the process was
authorized, reviewed, reproducible, or safe.

This product aims to provide a unified infrastructure for governed work with subagents. It connects
the definition, authorization, execution, communication, validation, artifacts, and history of
subagent work so that they can be controlled and inspected as parts of one system.

The product should make complex delegated work more trustworthy without requiring a human or chat
agent to manually coordinate every interaction. It should preserve enough structure and evidence to
explain both the current state of work and the path that produced it.

Its value is not limited to running multiple agents. The intended outcome is a platform where
subagent work can be organized, constrained, validated, observed, recovered, and related to the
objectives, features, decisions, inputs, and artifacts that give it meaning.

## Purpose of this branch

This branch exists to design the intended final form of that infrastructure from first principles.
We will first establish a small, coherent high-level product and system model and only then
introduce detailed contracts, schemas, state machines, persistence, APIs, migration, or
implementation plans.

The work in this branch does not begin by adapting the current implementation or preserving its
existing concepts. Existing repository artifacts may later be examined as evidence, constraints,
or reusable mechanisms, but they do not define the target model in advance.

## What the product should enable

### Structured subagent work

The product should enable tasks such as research, discovery, specification, implementation, review,
and custom application workflows to be represented as organized collaboration among subagents.

The collaboration should be explicit enough to distinguish responsibilities, dependencies,
communication, validation, rework, integration, and completion. This is useful because multi-agent
quality depends not only on the quality of individual agents, but also on how their work is divided,
combined, challenged, and accepted.

### Controlled delegation

The product should enable precise control over what delegated agents are allowed to read, modify,
create, communicate, and execute.

Work involving files, tools, network access, credentials, messages, or external effects should
remain inside explicit boundaries. This allows the platform to support consequential work without
depending on prompt instructions as the only protection against unauthorized behavior.

### Governed quality and validation

The product should enable validation gates, independent judgments, producer-reviewer separation,
anti-bias perspectives, sealed review, structured deliberation, bounded rework, integration, and
approval where they are appropriate.

These mechanisms make quality requirements part of the work definition. They reduce the risk that
an output is accepted merely because an agent produced it or because no independent challenge was
performed.

### Configurable agent behavior

The product should enable agent responsibilities, skills, prompts, inputs, tools, models,
permissions, budgets, and output formats to be configured and reused.

It should support both natural-language outputs and structured outputs governed by schemas. This
makes specialized workers, reviewers, observers, classifiers, and event-producing agents reusable
without requiring a new implementation for every workflow.

### Autonomous execution of confirmed work

The product should enable a confirmed subagent workflow to be executed by the infrastructure
without requiring the chat agent to coordinate transitions or relay messages.

The infrastructure should persist the confirmed Dispatch, initialize the declared subagents,
materialize their prompts and authorized inputs, schedule ready work, transport messages, apply
gates and limits, collect outputs, manage artifacts, and drive the work to an explicit terminal
state. The chat agent may still participate when the confirmed workflow explicitly requires it.

### Visible work state

The product should enable the current state of work to be understood across tasks, features,
workflows, agents, gates, and artifacts.

It should be possible to distinguish work that is proposed, awaiting confirmation, ready, active,
waiting, blocked, failed, cancelled, unresolved, or complete. This allows incomplete and blocked
work to remain visible instead of disappearing into chat history or being mistaken for completion.

### Recoverable history and decisions

The product should enable decisions, confirmations, revisions, rejections, reviews, messages,
attempts, and execution outcomes to remain attributable and recoverable.

This is useful because the current state alone cannot explain why it exists. Earlier decisions,
failed approaches, rejected outputs, and unresolved disagreements may all constrain later work and
should not be lost when the system advances.

### Artifact and result provenance

The product should enable every official artifact and result to be traced to the work that produced
it.

That trace should connect the artifact to its Dispatch, Run, agents, prompts, inputs, messages,
outputs, reviews, decisions, and effects. This makes it possible to evaluate whether the artifact
was produced under the expected authority, evidence, workflow, and validation conditions.

### Relational observability

The product should enable work to be inspected through its relationships, not only through isolated
logs or chronological events.

A feature should remain connected to its tasks; a task to its Dispatches; a Dispatch to its Runs and
agents; an agent output to the inputs and messages it consumed; an artifact to the reviews that
accepted it; and a decision to the evidence and later work that depend on it.

This provides an account of how the system's current state was formed, rather than only a list of
things that happened.

### Reuse and evolution

The product should enable successful workflows, prompts, agent configurations, validation policies,
and collaboration patterns to be reused and evolved through explicit versions.

Reuse reduces repeated coordination work, while versioning preserves the ability to explain and
compare earlier executions.

### Capability summary

| ID | Product capability |
|---|---|
| PC-1 | Represent complex work as structured collaboration among subagents. |
| PC-2 | Constrain delegated access, communication, mutation, and effects. |
| PC-3 | Apply explicit validation, review, independence, anti-bias, and rework. |
| PC-4 | Configure and reuse skills, prompts, tools, inputs, models, and structured outputs. |
| PC-5 | Execute confirmed workflows without implicit chat-agent supervision. |
| PC-6 | Expose the current state of tasks, workflows, agents, gates, and artifacts. |
| PC-7 | Preserve attributable decisions, messages, reviews, attempts, and outcomes. |
| PC-8 | Trace artifacts and results to their complete production context. |
| PC-9 | Observe typed relationships across features, tasks, Dispatches, Runs, inputs, and outputs. |
| PC-10 | Reuse and version successful workflow and agent configurations. |

## High-level system properties

### SP-1 — Conformance to confirmed workflow authority

Every Run must conform to the topology, authority, limits, and permitted variation declared by its
Dispatch. The Dispatch must remain bound to the exact version of the human-governed workflow
projection that the user confirmed.

This does not require one deterministic execution trace. Retries, rework, bounded loops,
conditional transitions, and early convergence may produce different valid Runs when the Workflow
Graph authorizes them. It does require that the runtime introduce no undeclared agent, relation,
permission, recipient, effect, or terminal behavior.

Without this property, confirmation becomes decorative: the user approves one structure while the
runtime executes authority or topology that was never present in the confirmed proposal.

### SP-2 — Autonomous execution

Once a Dispatch is confirmed, the infrastructure must be able to execute it to an explicit terminal
state without depending on the chat agent as an implicit scheduler, message relay, or synthesizer.

Without this property, the persisted workflow is only documentation and the actual orchestration
continues to live in unrecorded chat behavior.

### SP-3 — Bounded agent authority

Every agent must operate within enforceable boundaries over tools, inputs, messages, network access,
workspace paths, artifacts, budgets, and effects.

Without this property, prompt instructions such as "do not modify this file" are behavioral hopes,
not infrastructure guarantees.

### SP-4 — Governed communication

Every official agent-to-agent exchange must pass through a bus that authenticates the sender,
validates the payload, determines authorized recipients, applies visibility and release conditions,
preserves content, and records delivery.

Without this property, communication can bypass the confirmed workflow and provenance cannot
reliably explain who said what to whom.

### SP-5 — Explicit validation and artifact promotion

Reviews, validation gates, acceptance decisions, rework, and artifact promotion must be explicit
parts of the workflow.

Without this property, an agent producing a file can be mistaken for the system accepting that file
as an official result.

### SP-6 — Configurable and versioned agent behavior

Skills, prompt templates, input bindings, structured-output schemas, collaboration patterns, and
agent configurations must be reusable, versioned, and attributable.

Without this property, each Dispatch reinvents its behavior and earlier Runs cannot explain which
instructions or contracts produced their outputs.

### SP-7 — Durable execution history

The system must preserve the confirmed Dispatch and the accepted facts of its Runs, attempts,
messages, prompts, inputs, outputs, decisions, events, artifacts, and terminal states.

Without this property, recovery and audit depend on reconstructing execution from incomplete logs
and surviving files.

### SP-8 — Relational observability

The system must preserve typed relationships among objectives, features, tasks, Dispatches, Runs,
agents, inputs, messages, outputs, reviews, decisions, artifacts, and effects.

Without this property, the user can see isolated activity but cannot explain how an artifact was
produced, which work served a feature, or what depends on a particular result.

### SP-9 — Recoverable and honest lifecycle

Retries, crashes, duplicate requests, partial delivery, cancellation, unresolved work, and unknown
external outcomes must remain explicit and recoverable without silently repeating effects.

Without this property, the runtime may produce duplicate work or report completion when the actual
outcome is unknown.

### SP-10 — Entry-point and provider independence

The execution infrastructure must not depend on `subagents-strategy`, one chat surface, or one model
provider. Different entry points should submit the same work contract, and provider adapters should
not alter workflow semantics.

Without this property, the platform remains an extension of one current workflow rather than a
general subagent-work infrastructure.

## Capability-to-property direction

The architecture will be derived rather than assumed. Each product capability must be supported by
one or more system properties; each property must later have an owning service boundary, contracts,
and evidence that it is enforced.

```text
product problem
      |
      v
product capability (PC-N)
      |
      v
system property (SP-N)
      |
      v
service responsibility
      |
      v
contract
      |
      v
test and operational evidence
```

An initial, non-exhaustive relationship is:

| Product capability | Required system properties |
|---|---|
| PC-1 — Structured collaboration | SP-1, SP-2, SP-4, SP-5 |
| PC-2 — Controlled delegation | SP-3, SP-4, SP-5 |
| PC-3 — Governed quality | SP-1, SP-4, SP-5, SP-6 |
| PC-4 — Configurable behavior | SP-3, SP-6, SP-7 |
| PC-5 — Autonomous execution | SP-1, SP-2, SP-4, SP-9 |
| PC-6 — Visible work state | SP-7, SP-8, SP-9 |
| PC-7 — Recoverable history | SP-7, SP-8, SP-9 |
| PC-8 — Artifact provenance | SP-3, SP-5, SP-7, SP-8 |
| PC-9 — Relational observability | SP-7, SP-8 |
| PC-10 — Reuse and evolution | SP-1, SP-6, SP-10 |

Service ownership and contract mappings remain work for the detailed target model.

## Target system shape

The system receives a task that may be expressed as a plain-language description, an invocation of
a known skill, or a description accompanied by inputs, constraints, and an explicitly selected
protocol.

It produces a concrete proposed Workflow Graph. Every participating agent is represented as an
Agent Node. Typed Relations define the permitted dependencies and interactions among those nodes;
workflow-wide conditions define limits, conditional behavior, and terminal structure. The graph
describes the permitted execution space rather than one predetermined execution trace.

The proposal also contains the information needed to compile an executable Dispatch: prompts,
inputs, capabilities, budgets, effect boundaries, artifact boundaries, and output contracts. Every
material value must identify whether its authority comes from the human, a skill or registered
protocol, trusted infrastructure policy, or compiler derivation.

The user inspects a Confirmation View: the human-governed projection of the proposed workflow. The
view exposes the topology, participating agents, roles and responsibilities, relation types and
limits, anti-bias configuration, and important permission and effect boundaries. It may also expose
informational fields, such as materialized prompts, without treating those fields as human-authored
or human-confirmed. A trusted infrastructure boundary binds the user's decision to the exact
Confirmation View version and to the Dispatch compiled from it.

Persisting the Dispatch is not the terminal responsibility of the infrastructure. The
infrastructure must execute it: initialize the declared subagents, materialize their prompts and
authorized inputs, mediate communication through the bus, apply gates and limits, record runtime
facts, collect and validate outputs, manage artifact promotion, and return an explicit terminal
result. This execution must not depend on the chat agent acting as an implicit message relay or
scheduler.

## Intended interaction model

```text
task, optional skill, inputs, and constraints
                      |
                      v
          proposed Workflow Graph
                      |
                      v
          interactive Confirmation View
                      |
                      v
       compile + validate + confirm + register
                      |
                      v
          immutable executable Dispatch
                      |
                      v
 scheduler + launcher + agents + work bus + state
                      |
                      v
      messages + events + outputs + artifacts
                      |
                      v
        official terminal result for the caller
```

The initial access path may be `subagents-strategy`, but the system must not depend on that entry
point. A CLI, API, another skill, a workflow, or a future product surface should be able to submit
the same work contract.

## Core conceptual model

The canonical candidate definitions live under
[`definitions/subagent-work-infrastructure`](../../definitions/subagent-work-infrastructure/DEFINITIONS.md).
This README applies those definitions to the product direction rather than creating a second
definition authority.

| Concept | Role in the product |
|---|---|
| [Workflow Graph](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-001) | Defines the typed agent topology and permitted execution space for one task. |
| [Agent Node](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-002) | Defines one agent participant, its responsibility, inputs, capabilities, effects, limits, and output contract. |
| [Typed Relation](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-003) | Gives an inter-agent connection explicit scheduling, interaction, data, limit, and failure semantics. |
| [Dispatch](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-004) | Compiles the graph and its resolved configuration into one immutable executable contract. |
| [Confirmation View](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-005) | Presents the human-governed projection for inspection, bounded editing, and confirmation. |
| [Run](../../definitions/subagent-work-infrastructure/DEFINITIONS.md#def-swi-006) | Records one concrete execution and actual trace of one Dispatch. |

### Workflow Graph and Agent Nodes

Every node in the Workflow Graph represents one agent. Scheduler, artifact, gate, join, and human
confirmation concepts are not silently treated as agent nodes; the model must represent their
behavior through relations, workflow conditions, contracts, or other explicitly selected
mechanisms.

An Agent Node must be able to express at least:

- stable node identity, role, agent name, and requested execution configuration;
- local objective, responsibility, completion criteria, and output contract;
- prompt origin, bindings, and materialized instructions;
- mandatory inputs, bounded optional discovery, upstream inputs, and forbidden inputs;
- required, selectable, and forbidden skills and tools;
- permitted reads, modifications, creation locations, deletions, and external effects;
- budgets, timeouts, retry limits, and failure behavior.

Mandatory inputs and optional discovery are distinct authorities. An agent may be required to read
specific files while also being permitted to discover additional files within a declared scope. A
writing agent may be allowed to modify named files and create new files within declared directories
without requiring every filename to be predicted in advance.

### Typed Relations and bus authority

Relations are typed because connectivity alone does not explain how work moves. Multiple relations
of different types may connect the same agents when, for example, one relation controls readiness
and another authorizes messages. Each relation type must eventually define its endpoints, direction,
readiness effect, information movement, visibility and release rules, activation condition, limits,
stopping behavior, and failure behavior.

The current repository provides `sequential`, `zig-zag`, and `feedback` as connection precedents.
It currently treats parallel work as implicit within a group and `robot_talks` as a group property.
The target model does not adopt that group-centric representation in advance. It must decide whether
parallelism is explicit or derived and whether collective interaction such as robot-talks is a
relation type, an n-ary interaction, or a policy over a selected subgraph.

An agent's authorized senders and recipients are derived from Typed Relations. The Agent Node must
not carry a second independent communication list that can drift from the graph. The runtime
compiles the relations into the effective bus policy.

### Confirmation and atomic launch eligibility

The Confirmation View is a logical projection and may be rendered as an interactive HTML surface.
The user should be able to inspect the topology, open an agent to see what it will receive, inspect
relation behavior, modify allowed parameters, and confirm the resulting version. The first version
may deliberately restrict editing to agent parameters, workflow topology and interaction limits,
anti-bias, Dispatch-wide parameters, and important effect boundaries.

Any edit to a human-governed field requires recompilation and validation before confirmation. The
confirmation and its corresponding Dispatch registration must become durable as one atomic
eligibility decision; runtime launch may begin only afterward. The execution itself is not one
atomic transaction.

## Central boundaries

The target model must preserve these separations:

1. The caller states the task and may provide inputs or narrower constraints.
2. A protocol or workflow-construction mechanism determines how the work should be decomposed.
3. A workflow-construction mechanism produces one closed Workflow Graph for the task, where closed
   means that the permitted topology, authority, variation, limits, and terminal behavior are
   declared rather than that one execution trace is predetermined.
4. A Confirmation View presents the human-governed projection of that workflow.
5. A trusted confirmation boundary binds the user's decision to the exact Confirmation View version
   and the immutable Dispatch compiled from it.
6. Confirmation and Dispatch registration establish launch eligibility atomically.
7. The runtime executes the Dispatch but does not invent new topology or authority.
8. Agents produce typed work; they do not select unauthorized recipients or runtime transitions.
9. The bus derives effective communication authority from Typed Relations.
10. Runtime facts belong to a Run and do not rewrite the Dispatch.
11. Artifact and result boundaries determine which produced outputs become official.

## Working method

We will develop the model in deliberate layers:

1. Define the high-level product, capabilities, system properties, flow, and boundaries.
2. Maintain the smallest coherent conceptual model in this README and its normative vocabulary under
   `definitions/`.
3. Derive candidate service responsibilities from the accepted system properties.
4. Walk representative tasks through the model: research, review, implementation, specification,
   and discovery.
5. Identify the minimum authoritative payloads and the producer of every field.
6. Define workflow graph semantics, communication, lifecycle, and failure behavior.
7. Define versioned schemas and interfaces only after the concepts stabilize.
8. Define persistence, recovery, security, observability, migration, and implementation slices last.

At each layer, we will distinguish:

- values supplied by the caller;
- values supplied by a skill or registered protocol;
- values derived by the compiler;
- values confirmed by the user;
- values resolved by infrastructure policy;
- values produced by agents;
- values observed or generated by the runtime.

No field should enter a contract without a named producer, consumer, meaning, authority, and
mutation rule.

## What this README does not decide

This document intentionally does not decide:

- final names for domain objects and services;
- the final number or shape of JSON payloads;
- whether workflow construction is deterministic, model-assisted, or hybrid;
- how free-form tasks obtain a protocol when no skill is present;
- how workflow templates, concrete Dispatches, and runtime state are persisted;
- the final closed taxonomy and schemas for Typed Relations;
- whether robot-talks is a relation, n-ary interaction, or policy over a subgraph;
- the detailed Run lifecycle and the boundary between retry attempts and new Runs;
- exact bus operations or message schemas;
- exact prompt, semantic-agent-event, and runtime-event contracts;
- provider, model, sandbox, filesystem, credential, or artifact-store implementations;
- migration from the current repository architecture;
- compatibility with existing runtime or ledger formats;
- implementation phases, estimates, or file-level tasks.

Those decisions will be developed here and promoted to canonical definitions only when their
conceptual boundaries stabilize. Later contract artifacts may encode them after the design gate.

## Open questions

The branch must answer the following without relying on unstated runtime behavior:

- What enters the system?
- How does a description or skill become a confirmable workflow?
- What exact fields belong to the first-version Confirmation View, and which editable fields does it
  expose?
- Which visible fields are human-confirmed, protocol-supplied, policy-resolved, compiler-derived, or
  merely informational?
- Which changes invalidate confirmation and require a new version?
- What minimum attributes are required on every Agent Node?
- How are gates, joins, artifacts, and human decisions represented while every graph node remains an
  agent?
- What is the minimum closed relation taxonomy for the first executable version?
- Is robot-talks a relation, an n-ary interaction, or a policy over a selected subgraph?
- Is parallelism explicit or derived from the absence of a blocking relation?
- Which relation types affect readiness, authorize messages, transfer data, or combine those
  responsibilities?
- How are prompts, context, models, tools, permissions, and budgets resolved?
- How does an agent publish work without choosing unauthorized recipients?
- What is the minimum agent-message payload, and what does the bus add to it?
- How does the bus determine delivery, visibility, and release?
- How does the scheduler determine what is ready?
- How are configurable prompts and structured semantic events represented?
- Which events are produced by infrastructure, and which are agent-authored candidates?
- How are retries, cancellation, exhaustion, unresolved work, and terminal states represented?
- When is a retry another attempt within one Run, and when does it create a new Run?
- How are concurrent writes, artifact ownership, validation, and promotion controlled?
- What is returned to the caller, and who determines that it is the official result?
- Which information is configuration, which is runtime state, and which is durable evidence?
- Which relations must be preserved to answer provenance and current-state questions?

## Gate before detailed design

We should not begin JSON Schema or implementation design until the high-level target model can
explain, with one consistent vocabulary:

- the product problem and intended outcome;
- the accepted product capabilities and system properties;
- the trace from every capability to the properties that support it;
- the path from task to confirmed Dispatch to official result;
- the responsibility of each candidate subsystem;
- the boundary between workflow construction and execution;
- the trusted human-confirmation boundary;
- the relationship among agent nodes, messages, events, state, outputs, and artifacts;
- the authority and isolation boundaries for agent effects;
- the relational-observability questions the system must answer;
- one complete example each for a read-only task and an artifact-producing task;
- the important unresolved choices without disguising them as settled design.

This README is both the branch charter and the evolving high-level product model. Canonical term
boundaries live under `definitions/`; schemas and implementation artifacts remain gated until this
model is coherent.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Product-model framing session](../../sessions/2026-08-03-1558-subagent-infrastructure-product-model.md) | `contains` | Records the session that established and refined this branch charter. |
