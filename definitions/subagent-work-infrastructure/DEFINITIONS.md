# Subagent Work Infrastructure

Normative candidate definitions for the product model that governs structured work performed by
subagents.

These definitions specify conceptual boundaries, not final schemas, service boundaries, or runtime
implementations. Existing repository mechanisms are precedents and evidence; they are not binding
definitions of the target system.

---

<a id="def-swi-001"></a>

## Workflow Graph

- **ID:** DEF-SWI-001
- **Status:** candidate
- **Purpose:** Define the complete topology and authority envelope within which one task may be
  executed by agents.
- **Scientific/formal voice:** A Workflow Graph is a typed, attributed graph `G = (N, E, C)` where
  `N` is a finite set of Agent Nodes, `E` is a set of Typed Relations among those nodes, and `C` is
  the set of workflow-wide conditions, limits, and invariants. A concrete execution trace conforms
  to `G` only if every participating agent is declared in `N`, every inter-agent interaction is
  authorized by `E`, and every activation, repetition, effect, and terminal transition satisfies
  the applicable node authority and `C`. The graph defines the permitted execution space; it does
  not prescribe one deterministic trace through that space.
- **Plain-language voice:** It is the map of which agents may participate, what each one is there to
  do, and the allowed ways their work may move and interact.
- **Domain-context voice:** In the subagent-work infrastructure branch, a task may originate from a
  skill, a registered protocol, a free-form user request, or a combination of these. A workflow
  construction mechanism may propose the topology, including reviewers, synthesizers, bounded
  interaction, and conditional rework, but the runtime may execute only the topology and variation
  already authorized by the resulting Dispatch.
- **Boundary:** A Workflow Graph is not a Run: it defines permitted executions rather than recording
  one actual execution. It is also not a Dispatch: the Dispatch is the compiled, versioned contract
  that resolves the graph and the additional configuration required by a runtime.
- **Related:** DEF-SWI-002, DEF-SWI-003, DEF-SWI-004, DEF-SWI-006.

### Open questions

- Which workflow-wide conditions belong in `C`, and which belong on nodes or relations?
- Are collective interactions such as robot-talks represented by n-ary relations, interaction
  groups, or policies over a subgraph?
- Which conditional branches may be selected at runtime without requiring a new confirmation?

---

<a id="def-swi-002"></a>

## Agent Node

- **ID:** DEF-SWI-002
- **Status:** candidate
- **Purpose:** Represent one authorized agent participant in a Workflow Graph.
- **Scientific/formal voice:** An Agent Node is a node `n ∈ N` whose attributes define one agent's
  stable workflow identity and bounded authority. Its minimum attribute classes are identity;
  responsibility and completion criteria; prompt origin and materialized instructions; required,
  discoverable, upstream, and forbidden inputs; required, selectable, and forbidden skills and
  tools; read, mutation, creation, deletion, and external-effect scopes; execution budgets and
  retry limits; and an output contract. The node's authorized communication adjacency is derived
  from the graph's Typed Relations and must not be independently redefined by node-local data.
- **Plain-language voice:** It is one agent seat, together with what that agent must do, what it may
  see and use, what it may change, and what it must return.
- **Domain-context voice:** Each agent receives a `role` and `agent_name`, both structurally recorded
  and included in its materialized prompt. Inputs may combine mandatory files with bounded
  discovery scopes. A writing agent may be allowed to modify named files and create new files only
  within declared directories without requiring every future filename to be known in advance.
  Skills and tools may likewise be required, selected from an allowed set, or forbidden.
- **Boundary:** An Agent Node is always an agent participant in this product model. Scheduler,
  artifact, gate, join, and human-confirmation concepts are not silently treated as Agent Nodes.
  Their representation remains a workflow-model decision. An Agent Node describes authority; an
  agent invocation during a Run is an exercise of that authority.
- **Related:** DEF-SWI-001, DEF-SWI-003, DEF-SWI-004.

### Open questions

- What is the minimum required node attribute set for every workflow?
- Which model, provider, credential, and sandbox values are fixed on the node, and which may be
  resolved later by trusted infrastructure policy?
- How are discovery scopes expressed so optional search remains useful but enforceably bounded?
- Which completion criteria are declared by the workflow and which may be evaluated by another
  agent or infrastructure component?

---

<a id="def-swi-003"></a>

## Typed Relation

- **ID:** DEF-SWI-003
- **Status:** candidate
- **Purpose:** Give every connection among Agent Nodes an explicit executable meaning.
- **Scientific/formal voice:** A Typed Relation is an attributed connection `e ∈ E` whose type and
  parameters determine its allowed endpoints, direction, readiness effect, payload or message
  movement, visibility and release rules, activation condition, interaction or repetition limit,
  convergence or stopping rule, and failure behavior. Multiple relations of different types may
  connect the same Agent Nodes. Runtime scheduling and bus authorization must be derived from the
  applicable relation semantics rather than from an untyped notion of connectivity.
- **Plain-language voice:** An edge does not merely say that two agents are connected; its type says
  what the connection permits and how it behaves.
- **Domain-context voice:** Current repository precedents use `sequential`, `zig-zag`, and
  `feedback` connection types. `zig-zag` and `feedback` admit a loop limit, while `sequential` does
  not. Parallel execution is currently implicit within a group, and `robot_talks` is currently a
  group property rather than a connection type. These are inputs to the target design, not a
  commitment to preserve the existing taxonomy or group-centric representation.
- **Boundary:** A Typed Relation is not a generic permission list duplicated on its endpoint nodes.
  It is the authoritative source from which permitted inter-agent communication is compiled. Data
  dependency, scheduling order, communication, review, feedback, and release must not be assumed to
  have the same semantics merely because they connect the same agents.
- **Related:** DEF-SWI-001, DEF-SWI-002, DEF-SWI-004.

### Open questions

- What is the minimum closed set of relation types for the first executable version?
- Is `robot_talks` a relation type, an n-ary interaction, or a policy over a selected subgraph?
- Is parallelism represented explicitly or derived from the absence of a blocking dependency?
- Which relation types authorize messages, transfer data, affect readiness, or do more than one of
  these things?

---

<a id="def-swi-004"></a>

## Dispatch

- **ID:** DEF-SWI-004
- **Status:** candidate
- **Purpose:** Bind a confirmed workflow to one immutable executable contract.
- **Scientific/formal voice:** A Dispatch is a persistable, versioned executable contract produced
  by compiling a Workflow Graph with the bindings, prompts, input manifests, permissions, budgets,
  policies, output contracts, and authority provenance required by a runtime. Each material field
  has one named authority source: human confirmation, skill or protocol, trusted infrastructure
  policy, or compiler derivation. A Dispatch is valid for launch only when its Confirmation View is
  bound to the user's confirmation and the complete compiled contract is durably registered.
- **Plain-language voice:** It is the complete package the runtime can execute after the user has
  approved the meaningful shape and limits of the work.
- **Domain-context voice:** The user does not need to confirm every prompt or internal binding. The
  user confirms the human-governed projection of the workflow; other fields may come from a
  versioned skill, protocol, policy, or compiler. Once registered, the runtime must execute the
  Dispatch without using the chat agent as an implicit scheduler, message relay, or synthesizer and
  without inventing new topology or authority.
- **Boundary:** A Dispatch is not the user's original request, the visual confirmation surface, or
  mutable runtime state. It may contain information visible but not human-confirmed, provided that
  the authority for that information is explicit. Runtime facts belong to a Run and do not rewrite
  the Dispatch.
- **Related:** DEF-SWI-001, DEF-SWI-002, DEF-SWI-003, DEF-SWI-005, DEF-SWI-006.

### Open questions

- Which changes to a compiled Dispatch are material enough to require a new confirmation?
- Which fields are confirmed by the human, supplied by a protocol, resolved by policy, or derived
  by the compiler?
- What transaction boundary atomically binds confirmation, Dispatch registration, and launch
  eligibility?

---

<a id="def-swi-005"></a>

## Confirmation View

- **ID:** DEF-SWI-005
- **Status:** candidate
- **Purpose:** Present the human-governed projection of a proposed workflow for inspection,
  permitted modification, and confirmation.
- **Scientific/formal voice:** A Confirmation View is a versioned projection `V_h(D)` of a proposed
  Dispatch `D` containing the fields over which the human is the authority. Confirmation binds the
  user's decision to one exact version of `V_h(D)` and to the Dispatch compiled from it. A change
  to any human-governed field invalidates the prior confirmation and requires recompilation and
  renewed confirmation before launch eligibility is restored.
- **Plain-language voice:** It is the inspect-and-confirm view where the user sees the meaningful
  shape of the agent workflow and approves the version that may run.
- **Domain-context voice:** The intended product surface may be an interactive HTML view where the
  user can inspect the topology, open an agent to see its responsibility and received context,
  inspect relation types, and modify an allowed subset of agent and Dispatch parameters. A first
  version may limit editing to topology, agent parameters, interaction limits, anti-bias, and
  important effect boundaries. Informational fields must be visually distinguishable from fields
  the user is confirming.
- **Boundary:** A Confirmation View is a logical projection, not HTML itself. HTML is one possible
  rendering. Visibility does not imply confirmation: a prompt may be inspectable while its
  authority remains a versioned skill or trusted policy rather than the human.
- **Related:** DEF-SWI-004.

### Open questions

- What is the exact first-version set of human-governed fields?
- Which edits may the user perform directly, and which require returning to workflow construction?
- How are derived consequences and the diff from the previously confirmed version shown before
  reconfirmation?

---

<a id="def-swi-006"></a>

## Run

- **ID:** DEF-SWI-006
- **Status:** candidate
- **Purpose:** Represent one concrete execution of exactly one Dispatch.
- **Scientific/formal voice:** A Run is a durable execution instance associated with one immutable
  Dispatch. It records runtime state and the actual conforming trace, including activated nodes,
  agent invocations and attempts, relation traversals, messages, outputs, gate decisions, effects,
  failures, repetitions, and terminal state. Runtime facts extend the history of the Run and must
  not retrospectively mutate the Dispatch that authorized it.
- **Plain-language voice:** It is what actually happened during one execution of the approved
  package.
- **Domain-context voice:** A Run may take one of several paths permitted by the Workflow Graph: a
  review may converge after one exchange or continue up to its declared limit. Both may conform to
  the same Dispatch. Detailed Run lifecycle, recovery, event, and persistence semantics remain work
  for later design.
- **Boundary:** A Run is not the reusable workflow definition or its executable configuration. It
  records actual choices and outcomes under one Dispatch. A retry may be an attempt within a Run or
  a new Run only when the later lifecycle model says so explicitly.
- **Related:** DEF-SWI-001, DEF-SWI-004.

### Open questions

- Which states and terminal outcomes form the Run lifecycle?
- When is a retry another attempt in the same Run versus a new Run?
- Which runtime facts are authoritative state, events, evidence, or derived projections?

---

## Boundary table

| Term | Sharpest separating trait |
|---|---|
| **Workflow Graph** | Defines the permitted topology and execution space; it is not yet a runtime-ready contract or an observed execution. |
| **Agent Node** | Represents exactly one bounded agent participant; it is not a gate, artifact, scheduler, or invocation attempt. |
| **Typed Relation** | Gives a connection executable semantics; mere adjacency conveys no authority. |
| **Dispatch** | Is the immutable compiled contract eligible for runtime execution; it is not mutable execution state. |
| **Confirmation View** | Is the human-governed projection of a proposed Dispatch; visibility and confirmation are distinct. |
| **Run** | Records one actual execution of one Dispatch; it does not redefine what was authorized. |
