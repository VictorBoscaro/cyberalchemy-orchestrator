---
tags: [workflow-graph, orchestration, dispatch, agents, scheduling, communication, completion]
node_type: readme
is_session: false
layer: [architecture, domain, application]
nature: reference
status: draft
version: 0.1.0
created: 2026-08-04
last_updated: 2026-08-04
---

# Workflow Graph — Discovery Brief

> **Status:** `draft`, unreviewed investigation brief. This README defines what a future discovery
> must understand. It is not the discovery, a proposed schema, a decision record, a SPEC, or an
> implementation plan. The name “workflow graph” is provisional: the investigation must determine
> whether the executable model is one graph or a composition of multiple structures.

## 1. Purpose

Prepare a repository-wide discovery that determines how work is represented from reusable protocol
intent through confirmed execution and terminal outcome.

The immediate question came from the candidate decomposition of `DispatchSpec`: an agent is a
configured participant, while a node may represent agent work, deterministic work, a human gate or
a terminal state. That distinction is plausible but not yet governed by one coherent model across
protocol compilation, confirmation, scheduling, communication and runtime state.

The future discovery should make that model explicit before a closed `DispatchSpec` schema is
designed.

## 2. Central Investigation Question

What is the smallest explicit and executable model that represents work, dependencies, executors,
coordination, communication and completion without collapsing distinct authorities or creating a
second source of truth?

“Smallest” must be evaluated rather than asserted. A candidate is smaller only when it minimizes
canonical authorities and duplicated state while still providing total deterministic mappings,
representing every required counterexample, preventing implicit grants, reconstructing runtime
state from authoritative facts and preserving the meaning of prior versions.

One hypothesis to test is that “the workflow graph” is not one universal graph, but a composition:

```text
reusable protocol topology
        ↓ compilation
concrete candidate topology
        ↓ confirmation and resolution
confirmed executable topology
        ↓ runtime reduction
workflow state and terminal facts

alongside, but not implied by it:
communication authorization + collective coordination
```

This is an investigation frame, not a selected architecture.

The investigation must keep five semantic dimensions separate until evidence proves that any of
them share one representation:

1. **Structure:** obligations, ordering and dependency.
2. **Authority:** what has been confirmed and may execute.
3. **Allocation:** which logical or concrete executor performs an obligation.
4. **Coordination and communication:** participation, observation, sending, reveal and collective
   decision rules.
5. **State:** readiness, attempts, generations, results, cancellation and closure.

Separate dimensions do not imply five graphs. A policy, binding relation, state machine or derived
projection may be the smaller representation for a dimension.

## 3. Why This Discovery Is Needed

Relevant semantics currently exist in several places:

- [`ProtocolRecipe`](../../features/agents-communication-infra/specs/protocol-compilation.md#protocolrecipe)
  defines a bounded reusable DAG with typed nodes and edges.
- [`DispatchCandidate`](../../features/agents-communication-infra/specs/protocol-compilation.md#dispatchcandidate)
  preserves the concrete candidate nodes, edges and terminal-node IDs without granting execution
  authority or assigning executors.
- [`DispatchSpec`](../../features/agents-communication-infra/specs/domain.md#dispatchspec) carries a
  `group_graph` typed only as `object`; it does not yet close the executable graph schema.
- [`AgentInvocationPlan`](../../features/agents-communication-infra/specs/domain.md#agentinvocationplan)
  binds runtime execution to a `seat_id`, role/task references, budget, sandbox and authority fence.
- [Bus Contracts](../../features/agents-communication-infra/discovery/bus-contracts/README.md) owns
  routing, visibility, reveal and delivery semantics.
- [Agents Communication Protocols](../../features/agents-communication-infra/discovery/agents-communication-protocols/README.md)
  now records candidate questions about participant identity, workflow nodes, communication and
  completion, but should consume rather than incidentally define the resulting graph model.
- [`subagents-dispatch.yaml`](../../../telemetry/agents/subagents-dispatch.yaml) supplies a useful
  legacy precedent for dispatch envelopes, groups, agents and connections, but is an audit surface,
  not the normative executable model.

Because these artifacts answer different parts of the problem, using the word “graph” without a
layer qualifier can silently conflate reusable design, confirmed authority, scheduler state,
communication permission and UI projection.

There is also an ownership tension to resolve rather than inherit: Bus Contracts describes a
confirmed `RoutingPlan` containing a work graph, responsibilities, release gates and visibility
policy. The discovery must determine whether that plan is a projection of executable workflow
authority, a component of `DispatchSpec`, or an overextended communication contract. It must not
allow both `group_graph` and `RoutingPlan` to become competing owners of the same fact.

## 4. Current Evidence Baseline

The future discovery starts from these bounded observations:

1. Protocol compilation v1 admits node kinds `work`, `review`, `decision`, `integration`,
   `projection` and `terminal`, and edge kinds `depends_on`, `review_of`, `feeds` and `gates`.
2. The v1 protocol graph is a finite DAG: terminal nodes have no outgoing edges and all nodes must
   reach a terminal node.
3. The canonical fixture contains `work -> done`; it contains no executor field, so it does not
   prove either `node == agent` or that `done` has no executor.
4. The runtime domain distinguishes `Group`, `Seat`, `Attempt`, `AgentInvocationPlan`, terminal run
   facts and audit close state.
5. Workflow dependency does not, by itself, authorize communication.
6. Agent/attempt completion does not, by itself, prove semantic workflow success.
7. The current `DispatchSpec` does not provide a closed destination schema for mapping all these
   concerns into executable authority.

These are starting constraints, not proof that the current partition is optimal.

“One source of truth” does not require one global artifact. The candidate model must instead name
one canonical authority for each fact at each lifecycle stage. Multiple immutable artifacts are
acceptable only when their ownership does not overlap and their lineage and allowed derivations are
explicit.

## 5. Questions the Discovery Must Answer

The WGQ identifiers express coverage, not execution order. Evidence should normally be developed
in this dependency order: node semantics; identity and executor; topology and edge kinds;
compilation and authority; runtime state, retry and rework; communication; collective coordination;
completion; and simplified projections. WGQ-1 is answered from the resulting model rather than by
choosing a graph count in advance.

### WGQ-1 — How many graphs or state structures exist?

Determine whether reusable protocol topology, confirmed executable topology, runtime state,
communication authorization and collective coordination are revisions or projections of one
canonical graph, distinct graphs connected by total mappings, or a graph plus policies/state
machines. The answer must identify the canonical authority at every lifecycle stage.

### WGQ-2 — What does a node mean?

Define whether a node represents an obligation, task, invocation, gate, deterministic operation,
artifact transformation, state, outcome or some closed union of these. Test at least agent work,
review, deterministic work, human approval, fan-out/fan-in, integration and terminal behavior.
For a terminal node in particular, determine whether it is an executable obligation, derived
condition, named outcome, template marker or runtime fact, and therefore whether it can have an
executor, readiness, retry or output contract.

### WGQ-3 — How do nodes relate to agents and runtime identities?

Define the relationships among `node_id`, logical agent identity, `agent_name`, role contract,
`Group`, `Seat`, provider/runtime agent instance, `Attempt` and retry. Decide which relations are
one-to-one, one-to-many, optional or forbidden without assuming universally that one node equals
one agent.

### WGQ-4 — Which node and edge kinds are required?

Evaluate the existing protocol-compilation taxonomies and determine whether they are sufficient for
execution. For every admitted kind, define identity, required fields, valid endpoints, readiness,
input/output contracts, executor requirements, failure/retry behavior, ordering and equality.

### WGQ-5 — What belongs to workflow versus communication?

Determine whether communication authorization remains a separate topology and, if so, how it binds
to stable participants and workflow phases without duplicating workflow edges. Cover default deny,
sender/recipient identity, message schemas, visibility, reveal, delivery and phase restrictions.
Resolve the current `RoutingPlan` ownership tension explicitly: workflow dependency, release gate,
responsibility and visibility may be compiled together for convenience without acquiring the same
canonical owner.

### WGQ-6 — How is collective coordination represented?

Determine when parallel agents are merely independent ready nodes and when collective semantics
require an explicit scope such as a group. Cover quorum, eligible membership, independent
submission, reveal barriers, aggregation rules, dissent preservation, group budgets and collective
results, mapping any proposal to existing `Group`, `Seat` and `GroupResult` concepts.

### WGQ-7 — What is the completion model?

Define the relationship among terminal nodes, outcome definitions, convergence predicates, gates,
loop ceilings, rework, the unique winning terminal fact of a `Run`, `audit_close.verified` and
official closure. Preserve the distinction between attempt end, workflow outcome and dispatch
closure.

### WGQ-8 — How do rework and loops coexist with a DAG?

Determine whether rework uses executable cycles, repeated traversal of an acyclic template, new
generations, explicit state-machine transitions or another bounded mechanism. Replay, retry,
reconsideration and semantic rework must remain distinguishable.

### WGQ-9 — How is the graph compiled and confirmed?

Define a total, versioned and fail-closed mapping across:

```text
ProtocolRecipe
  -> DispatchCandidate
  -> ConfirmationProjection
  -> DispatchSpec
  -> Run / AgentInvocationPlan / Work Bus projections
```

Every source and destination path must have an explicit disposition and rule reference. Capability
requirements must not become grants implicitly, and runtime facts must not be inserted into frozen
authority retroactively.

For this discovery, a **total mapping** means that every admitted source path has exactly one
declared disposition such as copied, transformed, resolved, rejected, intentionally omitted or
retained only as lineage. Total does not imply reversible or lossless. Every transformation must
identify its authority, preconditions and destination owner.

The discovery must close what confirmation may do to candidate topology. At minimum, decide whether
confirmation may assign executors, resolve capabilities, specialize parameters, insert system
operations or gates, remove inapplicable nodes, or change edges. Any admitted transformation must
preserve attributable lineage; a forbidden transformation must fail closed rather than silently
rewrite the candidate.

The result must include an authority matrix with, for every lifecycle stage, the canonical facts,
immutability boundary, ability to grant execution, permitted derivations and successor. It should
test at least `ProtocolRecipe`, `DispatchCandidate`, confirmation input/projection, `DispatchSpec`,
`Run` facts and audit closure.

### WGQ-10 — Which views may simplify the canonical model?

Determine how authoring tools, confirmation UI, Mermaid diagrams, telemetry and control-center views
may hide or aggregate nodes without changing meaning. In particular, establish whether a UI may
show only agent nodes while omitting system operations, gates and terminal nodes.

## 6. Required Counterexamples

A candidate model is incomplete unless it can represent and distinguish at least:

1. One agent performs one task and reaches a terminal outcome.
2. Two independent reviewers feed one synthesizer.
3. One agent executes multiple sequential tasks.
4. One task is retried without creating a new logical agent.
5. A deterministic operation runs without an agent.
6. A human gate blocks subsequent work.
7. Agents are parallel but cannot communicate.
8. Agents communicate without a dependency edge between them.
9. A quorum and reveal barrier produce a collective result with preserved dissent.
10. Rework creates a new attributable generation and loop exhaustion does not imply approval.
11. The workflow reaches an unresolved or awaiting-human terminal outcome.
12. The run reaches a terminal fact while audit close remains pending or requires reconciliation.
13. Cancellation occurs while nodes are ready or attempts are active, and late results cannot
    regain authority.
14. A conditional branch is not selected without its nodes being misclassified as failed.
15. Fan-in receives a partial failure, timeout or escalation to a human.
16. One logical operation requires multiple executors, or one reusable subworkflow is invoked from
    multiple nodes, without identity collision.
17. A policy or topology change requires new confirmation while the prior run remains interpretable
    under its frozen version.

## 7. Scope Boundaries

### In scope

- Conceptual and lifecycle model for workflow topology and state.
- Node, edge, executor, identity, coordination and completion semantics.
- Boundaries with capability resolution, Work Bus and runtime facts.
- Canonicalization, versioning, mapping and projection requirements.
- Small canonical examples and counterexamples.

### Out of scope for the initial discovery

- Implementing a scheduler or provider adapter.
- Changing the promoted protocol-compilation v1 contract.
- Promoting a new `DispatchSpec` schema.
- Enabling mutating workflows.
- Selecting a graph database or visualization library.
- Treating the telemetry YAML as executable authority.

Those may become downstream work only after the conceptual model survives review.

## 8. Evidence Needed

| Question area | Minimum evidence before recommendation |
|---|---|
| Existing model | Field- and invariant-level inventory of protocol, domain, workflow, bus and runtime contracts. |
| Semantic dimensions | Explicit disposition of structure, authority, allocation, coordination/communication and state as graph, relation, policy, state machine or projection. |
| Identity | Explicit cardinality table for node, agent, seat, instance and attempt across retries and reuse. |
| Node/edge taxonomy | Closed candidate schemas exercised against every required counterexample. |
| Communication | At least one case where dependency and permission differ in each direction. |
| Coordination | Independent-review/quorum case proving that parallel layout alone is insufficient. |
| Completion | State-transition examples distinguishing attempt end, workflow outcome, run terminal fact and audit close. |
| Mapping | Total source-path-to-destination-path matrix with negative tests for omissions and implicit grants. |
| Authority | Lifecycle matrix naming the sole canonical owner of each fact, admitted transformations and lineage evidence. |
| Projection | Two views with different visual simplification that remain derivably equal to the same authority. |

## 9. Expected Outputs

If the investigation proceeds, this folder should evolve toward:

```text
docs/discovery/workflow-graph/
  README.md          # this investigation brief
  workflow-graph.md  # discovery, including provisional glossary and authority/mapping matrices
```

The discovery may recommend later decision records, experiments, SPEC amendments or work-pack
tasks. This brief authorizes none of them.

## 10. Non-Decisions Preserved by This Brief

- “Workflow graph” is a working name, not a ratified canonical concept.
- One node is not declared equal to one agent.
- Terminal nodes are neither removed nor mandated as the final representation.
- Communication is not yet declared inside or outside the workflow graph.
- Groups are not removed; their irreducible semantics remain under investigation.
- No `DispatchSpec` field, schema version or migration is selected.
- No current runtime capability is claimed.

## Connections

| Document | Edge | Why |
|---|---|---|
| [Agents Communication Protocols](../../features/agents-communication-infra/discovery/agents-communication-protocols/README.md) | `refines-question-from` | Supplies OQ-ACP3.B and OQ-ACP3.G and the candidate `DispatchSpec` decomposition that exposed the missing graph model. |
| [Protocol Compilation](../../features/agents-communication-infra/specs/protocol-compilation.md) | `starts-from` | Owns the promoted reusable recipe DAG and non-authoritative candidate projection. |
| [ACI Domain](../../features/agents-communication-infra/specs/domain.md) | `must-align-with` | Owns `DispatchSpec`, `Group`, `Seat`, `Attempt`, invocation plans and run terminal facts. |
| [Bus Contracts](../../features/agents-communication-infra/discovery/bus-contracts/README.md) | `boundary-with` | Owns communication authorization, visibility, reveal and delivery. |
| [ACI-PG-001](../../decisions/aci-protocol-governance-ownership.md) | `governed-by` | Fixes the authority boundary at non-authoritative `DispatchCandidate`; confirmation and runtime retain downstream ownership. |
| [Dispatch telemetry](../../../telemetry/agents/subagents-dispatch.yaml) | `compares-with` | Provides a legacy structural precedent without becoming a normative source. |
