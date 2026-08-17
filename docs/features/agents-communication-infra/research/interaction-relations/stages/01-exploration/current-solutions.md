---
tags: [agents-communication-infra, typed-graph, external-research, agent-orchestration]
node_type: research-explorer-return
is_session: false
layer: [architecture, application]
nature: [research, informational]
status: draft
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Current External Solutions Sweep

## Scope and evidence discipline

This sweep compares executable behavior, not product vocabulary. It covers five systems for which
current official evidence shows active maintenance: OpenAI Agents SDK, LangGraph, Google ADK,
Microsoft Agent Framework, and CrewAI. AutoGen is retained as an adjacent precedent but is not
counted: Microsoft now declares it in maintenance mode and directs new users to Agent Framework.

All sources are official product documentation or official source repositories, accessed on
2026-08-17. “Documented” below means an official contract or example exists. “GA”, “stable”,
“experimental”, and “production-ready” preserve the publisher's own maturity language. Repository
activity demonstrates maintenance, not real-world adoption. **Actual adoption is not established
for any system by this corpus**; vendor case studies, star counts, certification counts, or product
claims were not treated as adoption evidence.

## One-line result

Current systems converge on generic execution graphs, state, routing, joins, loops, interruption,
and durability, but none of the five active systems demonstrates a minimal algebra of
semantically typed interaction relations: semantic differences such as control transfer,
delegation-with-return, review authority, and approval are usually encoded by distinct higher-level
patterns, node logic, messages, state, or policy rather than by a rich edge type alone.

## Status and maturity

| System | Version/date evidence | Publisher-declared maturity | Maintenance evidence | Adoption evidence |
|---|---|---|---|---|
| OpenAI Agents SDK | Docs accessed 2026-08-17; release contract remains `0.Y.Z` and says the leading zero means the SDK is evolving rapidly | No GA/stable claim found for the Python SDK; non-beta public interfaces may still break on minor releases | Current official docs and releases; [release policy](https://github.com/openai/openai-agents-python/blob/main/docs/release.md) | Not established |
| LangGraph | Official repository showed the 1.x line and a `1.2.9` release dated 2026-07-10 | v1 public line; official release notes describe LangGraph v1 | Current releases and v1 docs; [repository](https://github.com/langchain-ai/langgraph), [v1 notes](https://docs.langchain.com/oss/python/releases/langgraph-v1) | Not established |
| Google ADK | Python `2.1.0` released 2026-05-23; graph workflows supported from Python/Go `2.0.0` | ADK Python 2.0 GA since 2026-05-19 and Go 2.0 GA since 2026-06-30 | Current 2.x releases; [ADK 2.0](https://github.com/google/adk-docs/blob/main/docs/2.0/index.md), [releases](https://github.com/google/adk-python/releases) | Not established |
| Microsoft Agent Framework | Docs accessed 2026-08-17; official Python metadata observed on the 1.x line (`1.12.1` in the inspected snapshot), while checkpoint docs already describe behavior “starting in 1.13.0” | Python package classifier says `Production/Stable`; Agent Framework 1.0 is presented as the production successor to AutoGen | Active 1.x releases and docs; [package metadata](https://github.com/microsoft/agent-framework/blob/main/python/pyproject.toml), [repository](https://github.com/microsoft/agent-framework) | Not established |
| CrewAI | Versioned official docs resolved to `1.15.16` on access | “Production ready” is a vendor claim, not independently verified maturity | Current versioned docs and releases; [Flows docs](https://docs.crewai.com/v1.15.16/en/concepts/flows), [repository](https://github.com/crewAIInc/crewAI) | Not established |
| AutoGen (adjacent, not counted) | Latest official release page identifies the 0.7.x line | `GraphFlow` is experimental; repository declares the overall project in maintenance mode | Maintenance only; no new features promised | Not established |

The Microsoft version discrepancy is itself a warning: consumers should pin and verify the
installed package rather than assume the continuously updated documentation matches a deployed
minor version.

## Behavioral comparison

| System | Core executable primitives | Graph/orchestration model | Handoff / control transfer | Sequence, parallel, condition, loop |
|---|---|---|---|---|
| OpenAI Agents SDK | `Agent`, `Runner`, tools, agents-as-tools, handoffs, guardrails, sessions, `RunState` | No general graph DSL in the core orchestration guide; runner loop plus ordinary Python orchestration | Handoff is an LLM-visible tool whose target becomes the active agent and normally receives conversation history; agent-as-tool returns a bounded result while the manager retains control | Handoffs route dynamically; sequence, fan-out, evaluator loops, and joins are explicitly shown as application Python (`asyncio`, `while`, output transforms) |
| LangGraph | Shared `State`, nodes, edges, reducers/channels, `Command`, `Send`, subgraphs, checkpointers | Pregel-like state graph executing active nodes in supersteps | A handoff is normally a state update plus `Command(goto=...)`; `Command.PARENT` crosses a subgraph boundary | Native fixed and conditional edges, multi-destination parallel activation, fan-in through state/reducers, cycles, recursion limits |
| Google ADK | Workflow nodes (agents, tools, functions, human input), edges/routes, `Event.Output`, `JoinNode`, nested and dynamic workflows | Declarative graph runtime in ADK 2.0; dynamic workflows use code for recursion or control too complex for a static graph | Collaborative agent routing exists, but graph control is primarily route/event-driven; control transfer is not a separate rich edge contract | Native chains, conditional routes, fan-out/fan-in, and conditional back-edges; prebuilt sequential/parallel/loop agents remain higher-level templates |
| Microsoft Agent Framework | Executors, typed messages, direct/conditional/switch/fan-out/fan-in edges, workflow events, shared state, sub-workflows | Functional and graph APIs share a workflow run model; graph execution uses supersteps | Built-in handoff orchestration is a mesh with allowed transfers; receiver takes task ownership and full conversation context, unlike agent-as-tool where manager retains control | Native graph sequence, conditions, switch, and fan-out/fan-in; repeated turns and termination are documented in handoff/group-chat orchestrations, but a generic cyclic-graph contract was not established in this sweep |
| CrewAI | Flow methods, `@start`, `@listen`, `@router`, `and_`, `or_`, Flow state, Crews/Agents | Event-driven Flow projected as a directed execution graph; methods emit outputs/labels that activate listeners | Delegation is primarily inside Crews or ordinary method calls; Flow does not expose a first-class ownership-transfer relation analogous to handoff | Chaining, multiple starts/broadcast, `and_`/`or_` joins, conditional labels, and code/routing-based loops; no minimal typed edge vocabulary |
| AutoGen (adjacent) | Agents, teams, messages, termination conditions, `DiGraphBuilder`, `GraphFlow` | Conversational teams plus experimental directed graph execution | `Swarm` uses `HandoffMessage`; group chats use a manager/speaker selector | Experimental `GraphFlow` supports sequence, parallel, conditional edges, activation groups, and cycles |

## System findings

### OpenAI Agents SDK

The core distinction is semantic and useful: **agents-as-tools** preserves a manager's control and
final-answer ownership, whereas a **handoff** changes the active agent and gives the receiver the
conversation. Input filters may narrow what crosses the handoff, and typed `input_type` can validate
handoff metadata. This is a genuine difference in authority/control, but it is represented by two
different primitives and runner behavior, not by two types on a general graph edge. The SDK's
[orchestration guide](https://openai.github.io/openai-agents-python/multi_agent/) explicitly leaves
deterministic sequencing, parallel calls, evaluator loops, and output composition to normal Python;
the [handoff contract](https://openai.github.io/openai-agents-python/handoffs/) says handoffs remain
inside one run.

State has several layers: session history across runs, the current runner history, application
context, and serializable `RunState`. A default handoff exposes prior conversation; an input filter
can make the recipient's view private or reduced. `RunState` is the durable pause/resume boundary
for pending approvals and captures model responses, generated items, approval state, and optional
server conversation identifiers ([RunState](https://openai.github.io/openai-agents-python/ref/run_state/)).

Termination is a final output with no outstanding tool call, or a `max_turns` failure. Human
approval is tool-scoped: approval-required tools interrupt the outer run even when called after a
handoff or inside an agent-as-tool, and the original run resumes after approve/reject
([HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/)). Model-call retries have
explicit replay-safety boundaries and policies; process-level durable recovery is delegated to
documented Dapr, Temporal, Restate, or DBOS integrations rather than supplied as a generic workflow
graph checkpoint engine ([running and recovery](https://openai.github.io/openai-agents-python/running_agents/),
[model retry](https://openai.github.io/openai-agents-python/models/)).

Types cover structured agent outputs and handoff inputs through Pydantic-compatible schemas, not
semantic compatibility of arbitrary agent-to-agent relations. Built-in tracing records model
generations, tools, handoffs, guardrails, and custom spans
([tracing](https://openai.github.io/openai-agents-python/tracing/)). Extension is ordinary code,
custom tools, hooks, guardrails, handoff filters, and custom session/durable orchestration adapters.

**Left to application code:** graph topology, join/quorum, convergence, reviewer authority,
cross-run workflow scheduling, and the meaning of repeated feedback.

### LangGraph

LangGraph provides the clearest general execution substrate in the sample. Its three base concepts
are shared state, nodes, and routing edges. Nodes and edges are ordinary functions; fixed edges,
conditional edges, `Command`, and `Send` determine activation. Multiple outgoing destinations run
in the next superstep, and cycles are valid. The graph ends at `END` or when no work remains; a
recursion limit/`RemainingSteps` bounds cycles
([Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)).

Graph state may be declared with `TypedDict`, dataclasses, or Pydantic and merged with per-field
reducers. This types the data plane, not the semantic intent of an edge. Handoffs are a documented
pattern implemented as state mutation plus routing—often a tool returns `Command`—and therefore
do not add an irreducible runtime relation type
([handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)). Subgraphs can
retain per-invocation or per-thread state, enabling private or persistent agent context, but the
designer chooses the visibility boundary.

Checkpointers save graph state at every step and enable resume, time travel, HITL, and recovery from
the last successful superstep. Successful parallel writes can be retained when a sibling fails
([persistence](https://docs.langchain.com/oss/python/langgraph/persistence)). `interrupt()` pauses
with a serializable payload and resumes with `Command(resume=...)`, making approval only one of many
possible external-input protocols
([interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)). Per-node retry policies
are stable across Python and TypeScript; newer timeout/error-handler additions in `langgraph>=1.2`
are explicitly marked alpha in the docs
([fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)). LangSmith is
the documented tracing/inspection path.

**Left to application code:** the distinction between advice, review, approval, delegation, and
evidence transfer; authority; quorum/convergence; payload privacy; compensating effects; and most
domain-level termination predicates.

### Google ADK 2.x

ADK 2.0 moves its workflow runtime to graphs whose nodes can be agents, tools, functions, human
input, or nested workflows. Edges establish execution routes, node output travels through
`Event.Output`, route values select branches, and `JoinNode` provides an all-upstream barrier.
Back-edges implement loops and re-activate a node with a fresh lifecycle
([graph workflows](https://adk.dev/graphs/), [routes](https://adk.dev/graphs/routes/)). Dynamic
workflows deliberately use code when loops, recursion, or branching are too dynamic for a static
graph. The older `SequentialAgent`, `ParallelAgent`, and `LoopAgent` are retained as templates but
are superseded by graph/dynamic workflows for Python and Go 2.x.

ADK supports typed agent input/output schemas; Go additionally exposes generic typed agent nodes,
and successors receive typed `Event.Output`
([data handling](https://adk.dev/graphs/data-handling/)). Session state is serializable key/value
data with explicit session, user, app, and invocation-temporary scopes; persistence depends on the
selected `SessionService` ([state](https://adk.dev/sessions/state/)). This is richer state scoping,
but it still does not make an edge mean “review” or “transfer authority.”

HITL is a first-class node: `RequestInput` pauses execution and can require a response schema; Go's
node reruns on resume and passes the reply as typed output
([human input](https://adk.dev/graphs/human-input/)). Resumability is opt-in at the application
configuration boundary, and the 2.0 migration contract references `RetryConfig`; this sweep did not
establish a universal checkpoint-per-node or exactly-once effect guarantee
([resume](https://adk.dev/runtime/resume/), [ADK 2.0](https://github.com/google/adk-docs/blob/main/docs/2.0/index.md)).
Tracing follows OpenTelemetry GenAI conventions and exports OTLP
([traces](https://adk.dev/observability/traces/)). Extension is through function/tool/agent nodes,
nested workflows, custom agents, route functions, and fully dynamic code.

**Left to application code:** semantic relation labels, authority and evidence rules, convergence,
failure compensation, non-all join policies, and the distinction between a protocol loop and a
mere control-flow cycle. A documented `JoinNode` can stall if any upstream emits no output, showing
that failure semantics cannot be inferred from fan-in topology alone.

### Microsoft Agent Framework

Agent Framework exposes the strongest code-level message typing in the sample. Executors receive
and emit typed messages; edges may be direct, conditional, switch-case, fan-out, or fan-in, and the
runtime can report delivery failures such as type mismatch, false condition, or buffered fan-in.
These are type and control guarantees, not domain-semantic edge types
([workflow concepts](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/),
[edges](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/edges),
[observability](https://learn.microsoft.com/en-us/agent-framework/workflows/observability)).

Its built-in handoff orchestration provides a particularly valuable semantic witness. Handoff is a
mesh without a central orchestrator: the receiver takes full task ownership and full conversation
context. Agent-as-tool instead returns to a primary agent that retains responsibility. Allowed
handoffs constrain who may take over next, even though all participants remain context-connected
([handoff](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)).
Sequential, concurrent, group-chat, handoff, and Magentic are higher-level orchestration builders
over workflow mechanisms, not evidence that each is a primitive edge kind.

Maturity must be read per surface: the core Python package declares production/stable, while
official release notes still mark particular orchestration surfaces such as Magentic experimental.
The stable core label therefore does not promote every included pattern to the same contract level.

Workflow checkpoints capture executor state, pending messages, pending requests/responses, and
shared state at superstep boundaries; durable file and Cosmos stores allow cross-process recovery.
Rehydration requires the same topology and stable executor/agent identities
([checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)). HITL uses
request/response events and tool-approval requests, both checkpointable
([HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)). The
framework supports shared workflow state and per-agent threads, but its docs warn that reused
executor or workflow instances can leak mutable state across runs unless instances are isolated or
reset ([state](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/state)).

The official checkpoint and core workflow pages establish resume, not a single generic retry
policy for every executor/effect. Application executors remain responsible for effect idempotency
and domain recovery unless a more specific provider contract says otherwise. Extension is through
custom executors, edge predicates and transforms, sub-workflows, orchestration builders, checkpoint
stores, middleware, and agent/provider adapters.

**Left to application code:** the semantics of evidence, review/acceptance authority,
convergence/quorum, compensation, privacy beyond context/state configuration, and whether two
topologically identical edges express different obligations.

### CrewAI

CrewAI separates autonomous `Crews` from event-driven `Flows`. A Flow marks entry points with
`@start`, activates downstream methods with `@listen`, combines triggers with `and_`/`or_`, and
routes on labels with `@router`. Multiple satisfied starts may execute in parallel. The resulting
structure can be plotted as a directed execution graph, but the public API is a decorator/event
model rather than a graph with semantically typed relations
([Flows](https://docs.crewai.com/v1.15.16/en/concepts/flows)).

Flow state may be an unstructured dictionary or a Pydantic model. `@persist` saves state, uses
SQLite by default, supports resume/fork by state ID, and allows a custom `FlowPersistence`
implementation. The documentation claims failed/restarted flows can reload state, but does not in
the inspected core contract establish checkpointing of every external effect or a graph-wide
exactly-once guarantee. Generic flow-step retry behavior was not established in this sweep.

`@human_feedback` pauses a Flow and can emit routing labels after interpreting free-form feedback;
without routing it simply collects feedback. The docs explicitly distinguish the local synchronous
decorator from managed webhook-based asynchronous HITL
([HITL](https://docs.crewai.com/v1.15.16/en/learn/human-in-the-loop)). This is a useful warning:
an LLM-collapsed feedback label is a routing decision, not proof of human authority unless the
application preserves the actual actor and decision evidence.

Observability in the inspected OSS Flow contract includes streamed execution, usage metrics, state
inspection, and graph plotting; detailed managed traces/logs are an AMP product claim and should
not be attributed automatically to the OSS runtime. Extension is ordinary Python Flow methods,
custom agents/Crews, custom decorators/providers, and custom persistence.

**Left to application code:** explicit control-transfer semantics, relation-level payload and
authority constraints, bounded/convergent loops, retry policy, effect recovery, and typed
compatibility between arbitrary listener outputs and downstream methods beyond normal Python and
Pydantic validation.

### AutoGen: adjacent transition evidence

AutoGen remains technically instructive but no longer satisfies the dispatch's “actively
maintained” requirement. The official repository says it is in maintenance mode and will receive
no new features, while recommending Agent Framework
([repository notice](https://github.com/microsoft/autogen)). Its `GraphFlow` executes directed
graphs with sequential, parallel, conditional, and cyclic paths, plus `all`/`any` activation
groups, but is explicitly experimental
([GraphFlow](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html)).
AgentChat also supplies round-robin/selector group chats, `Swarm` handoff messages, state save/load,
composable termination conditions, and OpenTelemetry tracing. Blocking `UserProxyAgent` input is
documented as unstable and non-resumable; persisted HITL is instead modeled by terminating, saving
team state, and starting another run
([HITL](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)).

AutoGen therefore demonstrates both a useful graph vocabulary and a maturity failure mode: a
feature can be expressively relevant while remaining an unsafe foundation for a new local contract.

## Cross-system behavior map

| Behavior needed locally | External witness | What the witness actually guarantees | What it does not settle |
|---|---|---|---|
| Dependency / sequence | Fixed edge or chain in LangGraph, ADK, Agent Framework; listener chain in CrewAI; Python chaining in OpenAI | B starts after A's activation/completion under that runtime | Whether A's output is accepted evidence, merely available input, or authoritative |
| Fan-out / fan-in | Supersteps and reducers (LangGraph), `JoinNode` (ADK), fan-in barrier edges (Agent Framework), multiple starts and `and_` (CrewAI), `asyncio.gather` (OpenAI) | Parallel activation and some barrier/merge rule | Quorum, partial failure, cancellation, ordering, dissent preservation |
| Conditional routing | Conditional edge/`Command`, routes, switch predicates, router labels, handoff tool choice | Selects one or more next activations from runtime data | Who is authorized to decide, whether the decision is evidence, and how it is audited |
| Control transfer | OpenAI and Agent Framework handoff; AutoGen `HandoffMessage` | Active specialist/task ownership changes, with defined context behavior | Whether all future protocols should encode this as an edge type, node, message, or subgraph |
| Delegation with return | Agent-as-tool in OpenAI and Agent Framework | Manager retains responsibility while a specialist returns a bounded result | Review/acceptance semantics and whether the result becomes canonical evidence |
| Review / approval | LangGraph interrupt, ADK human node, Agent Framework request/tool approval, OpenAI tool approval, CrewAI human feedback | Execution can pause and receive an external decision/input | Reviewer identity, authority scope, independence, quorum, and convergence are application contracts |
| Feedback loop / zig-zag | Back-edges in LangGraph/ADK, workflow loops in Agent Framework, routers/code in CrewAI, Python `while` in OpenAI | Repeated activation until a supplied predicate or limit ends it | Whether feedback is advisory or binding, who must respond, what changed, and what counts as convergence |
| Shared conversation | OpenAI default handoff, Agent Framework handoff mesh, AutoGen group chat | Participants receive a common or transferred history under the documented pattern | Selective disclosure, provenance, canonical artifact ownership, and least-privilege evidence flow |
| Durable pause/recovery | LangGraph checkpointer, Agent Framework checkpoints, OpenAI `RunState` plus durable integrations, ADK resumability, CrewAI persistence | Some state can be restored after interruption/restart | Exactly-once external effects, compensation, schema migration, and semantic validity after code/prompt changes |

## Implications for a local typed-relation basis

1. **Use graph mechanics as the substrate, not as the semantic answer.** Fixed, conditional,
   fan-out, fan-in, loop, and interrupt are well-supported execution behaviors. They say when work
   may run; they do not by themselves say what obligation or authority crosses the edge.

2. **Control transfer is the strongest externally witnessed semantic distinction.** OpenAI and
   Agent Framework independently distinguish handoff from agent-as-tool using task ownership,
   context, and return-of-control. Collapse test: if receiver ownership and return-of-control do not
   affect execution or evidence, the distinction disappears into ordinary routing.

3. **Type the data plane and the relation contract separately.** Frameworks commonly validate
   state/message/output schemas. That prevents malformed payloads but does not distinguish
   `advises`, `reviews`, `approves`, `delegates`, or `transfers-control`. A local relation candidate
   needs both endpoint/payload compatibility and a semantic effect.

4. **Treat named collaboration patterns as compiled subgraphs until necessity is shown.** No
   external system requires `zig-zag`, debate, group chat, or evaluator loop to be one primitive
   edge. They are normally compositions of activation, message/state transfer, choice, repetition,
   and termination plus an authority policy.

5. **Keep policy outside the edge unless it changes the relation's meaning.** Quorum, maximum
   rounds, convergence predicates, retry, timeout, and checkpoint frequency vary independently in
   current systems. Encoding all of them as edge types would multiply nominal types without
   demonstrating new interaction semantics.

6. **Model interruption and authority as distinct concerns.** An interrupt proves only that the
   runtime paused for input. Human approval additionally needs actor identity, decision scope,
   evidence, and authority. CrewAI's optional LLM classification of human feedback makes this
   distinction especially visible.

7. **Durability belongs to runtime ownership.** The external systems locate retry, checkpoints,
   replay safety, and idempotency in runners/checkpointers/storage/integrations. A typed relation may
   declare required delivery or evidence semantics, but should not silently appropriate recovery
   ownership from the runtime.

8. **Minimum external witness set for the next synthesis:** a candidate basis should at least
   distinguish (a) activation dependency, (b) payload/evidence delivery, (c) delegation with return,
   (d) transfer of control/ownership, and (e) authoritative gate/decision—unless the local corpus
   shows one can be compiled from the others without erasing observable behavior. Fan-out/fan-in,
   choice, repetition, quorum, convergence, retry, and interruption remain composition/runtime/policy
   candidates until their own necessity witnesses are produced.

This is a cautious implication, not a verdict on the final basis. The external corpus supplies
precedents and counterexamples; it does not prove minimality or sufficiency for the local patterns.
