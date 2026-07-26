# Research Initial Definitions

## Context

Cyberalchemy and DomainSpec are developing a governed way to turn human intent into recursive,
auditable agent work. The current subagent strategy already uses explicit roles, pairwise tension,
frozen prompt templates, source bindings, confirmation gates, runtime launch receipts, and
post-run observability to reduce correlated bias and keep local agent work aligned with a larger
objective.

The next local problem is finer control over both the prompts given to agents and the information
requested from different agents at selected points in their work. Prompt text currently appears in
dispatch records and selected workflow artifacts, while the project is beginning to bind
prompt-template digests and host-observable dynamic inputs at runtime. The intended capability is
to configure what information should be requested, why, from whom, and when. A coherent boundary
is needed before prompts and these configured requests can be deliberately authored, stored,
revised, selected, delivered, compared, and evaluated as governed project assets. The same problem
also requires understanding how a graph-oriented capability could represent the schemas of allowed
work structures and their concrete runtime instances without conflating structural representation,
execution, inference, provenance, or visualization.

## Purpose

This document establishes the informational baseline for research that will inform a later
discovery or architecture decision about governed control of agent prompts and requested
information. It separates already established constraints and evidence from the concepts and
boundaries that are still unknown.

## Research Question (Can be refined)

What minimum product and system boundaries would allow Cyberalchemy/DomainSpec to govern agent
prompts, configure ways of asking different agents for different information at selected points in
recursive work, and represent the resulting structures through governed graphs, while preserving
traceability to the relevant objectives, authority, evidence, schema revisions, and runtime
occurrences?

This wording is explicitly refinable. It does not assume that prompt management, request
configuration, runtime triggering, contribution capture, graph schema management, runtime graph
materialization, inference, projection, execution, and evaluation belong to one pipeline, service,
storage technology, or owner.

## Confirmed Product Constraints

- The immediate goal is finer control over agent prompts and requested information in support of
  bias reduction and better decisions, not prompt management as an isolated content-management
  feature.
- The architecture must remain minimal. Every proposed service, object, graph role, relation,
  property, event, index, or persisted artifact must have a named purpose, an actual consumer, and
  a consequence that would be lost if it did not exist. Concepts that cannot pass that necessity
  test must not be introduced.
- Existing mechanisms should be reused when they can satisfy the required purpose without hiding
  authority or provenance boundaries. A new service or durable object requires a responsibility
  and lifecycle that cannot be owned coherently by an existing capability.
- Important elements must not remain isolated: their connection to a relevant objective, runtime
  operation, decision, evidence chain, or explicitly named supporting purpose must be
  reconstructable. A connection alone is not sufficient when it cannot explain what the element
  contributes.
- Multiple agents working together must be composed so that their local positions help expose
  correlated bias and support the broader Cyberalchemy/DomainSpec objective.
- The system needs a structure for storing, versioning, measuring, and serving prompts.
- The first step is to make desired prompts and requests expressible and deliverable in controlled
  ways.
- The system must be able to request different information from different agents at selected
  points in their work.
- A configured request may carry an objective, metaprompt or instruction text, tags or other
  metadata, a trigger point or condition, and a description of the requested information or
  output. How these elements should be represented is not yet settled.
- Examples include, but are not limited to, tags, open questions, and decision-related
  information. These examples do not establish a taxonomy.
- The research must include the possible capability commonly described as a service that generates
  graphs, without assuming in advance that it is one service or that generation, validation,
  persistence, inference, execution, query, and visualization share an owner.
- It must preserve the distinction between a graph schema, which defines allowed structural forms,
  and a runtime graph, which contains concrete nodes and relations that claim conformance to a
  schema revision.
- Graph roles such as schema and runtime must not be treated as interchangeable with graph forms or
  restrictions such as DAGs, quivers, property graphs, trees, multigraphs, hypergraphs, or temporal
  graphs. Whether additional graph roles are needed remains open.
- A runtime node or relation may need identity, provenance, version, temporal validity, author or
  producer, state, confidence when applicable, and the schema revision to which it claims
  conformance. The minimum required metadata and its ownership remain unresolved.
- A declared graph relation does not by itself establish that a runtime operation is authorized or
  executed. The research must preserve the distinction between structural conformance and
  operational enforcement.
- Information produced in response does not automatically become accepted fact, project
  authority, authorization, or an accepted decision.
- A confirmed dispatch freezes each seat's prompt template; later dynamic slots carry data only
  and cannot introduce instructions, authority, lenses, source boundaries, or output contracts.
  Any request-specific instructional content must remain governed as instruction rather than
  enter through a data-only runtime slot.
- Runtime/provider claims must remain bounded to observable evidence. The current host bridge does
  not claim to capture hidden provider or system inputs.
- Dispatch lifecycle hooks, confirmation, append-only lineage, capability checks, exact source
  bindings, and close receipts remain mandatory.

## Current Evidence Baseline

- `.agents/skills/domainspec-subagents-strategy/SKILL.md` defines a two-projection proposal model,
  immutable per-seat prompt templates, separately materialized data-only workflow inputs, digest
  binding, invalidation rules, and the distinction between workflow evidence and ACI runtime
  authority.
- `.agents/skills/register-dispatch/SKILL.md` records the full `initial_prompt` per agent in the
  append-only dispatch ledger, but its row model is a dispatch record rather than a reusable prompt
  registry.
- `.agents/skills/anti-bias-vector-composition/SKILL.md` defines bias reduction as pairwise
  structural tension among agent micro-vectors, not merely diversity or additional agents.
- `docs/decisions/host-agent-dispatch-input-binding.md` records the accepted bounded host bridge:
  confirmed parent dispatch, group, seat, frozen prompt-template digest, workflow manifest, exact
  source/output hashes, and persisted turn binding. It explicitly stops short of the complete ACI
  invocation pipeline.
- `implementations/server/runtime/host_dispatch_hook.py` and
  `implementations/server/runtime/service.py` contain the implemented prompt-template and workflow
  manifest binding surface used by the host bridge.
- `.agents/skills/emit-topic-tags/SKILL.md` defines an existing activation-scoped mechanism for
  producing or depositing free topic observations. It does not establish a general configurable
  request model or a canonical tag registry.
- `experiments/skill-relationship-graph/` contains a static experiment that derives typed
  relationships from skill artifacts and explicitly distinguishes declared textual structure from
  runtime invocation evidence. It demonstrates an existing graph-generation mechanism but does not
  establish the required graph service, schema authority, runtime conformance, inference, or
  execution model.
- `docs/features/agents-communication-infra/experiments/bus-publication-probe/` demonstrates a
  bounded persist-before-acknowledge and receipt-verification mechanism for accepted agent
  publications. It is evidence relevant to a possible mutation or event acceptance boundary, not
  proof that a graph schema is enforced or executed at runtime.
- `docs/features/agent-provenance-telemetry/probes/` already separates raw agent emissions,
  deterministic normalization, vocabulary resolution, provenance, and later interpretation. These
  distinctions may constrain how tag assertions appear in runtime graphs, but they do not settle a
  graph data model or service boundary.
- `docs/architecture/agent-language-system-view.md` frames work descriptions as versioned,
  attributable hypotheses whose identity, authority, evidence, and history must remain
  reconstructable.
- Existing prompt text is distributed across dispatch rows, agent definition files, experiments,
  fixtures, and prompt-oriented context packs.

## Known Gaps

- There is no established canonical identity model for a reusable prompt asset versus a prompt
  template revision, a dispatch-local frozen copy, or a materialized invocation.
- There is no settled identity and provenance boundary connecting configured material, its
  revisions, a runtime occurrence, the targeted agent attempt, and the resulting information.
- The ownership boundary between authoring/version control, selection/resolution, runtime serving,
  request activation, contribution capture, measurement, and governance is not settled.
- It is not established what "the service that generates graphs" means in this system: whether it
  authors schemas, validates mutations, consumes events, materializes runtime state, performs
  inference, builds projections, serves queries, renders visualizations, or composes several of
  these capabilities.
- It is not known whether schema and runtime exhaust the graph roles the system needs. Provenance,
  history, evidence, inference, execution, projection, desired-state, and observed-state are
  possibilities to test and collapse, not a presumed list of separate graphs or components.
- The relationship between semantic graph roles and orthogonal mathematical or storage forms such
  as DAGs, quivers, property graphs, RDF graphs, trees, multigraphs, hypergraphs, and temporal
  graphs has not been established for this project.
- There is no settled machine-readable graph-schema contract for node types, relation types,
  source and target constraints, cardinalities, mandatory properties, forbidden relations,
  composable paths, invariants, inference rules, or validity conditions.
- It is unclear which paths are merely navigable, which relations may be composed, which
  compositions license an inference, and what evidence and authority a derived relation must
  retain.
- It is not established how a runtime node or relation proves conformance to an exact schema
  revision, how incompatible schema evolution is handled, or how historical instances remain
  interpretable.
- There is no agreed enforcement boundary that guarantees graph-schema constraints on accepted
  runtime mutations, including which checks belong in storage constraints, transaction-time
  validation, policy gates, rule engines, replay verification, or other mechanisms.
- It is unclear what additional mechanism is required for an execution-bearing graph to cause
  runtime behavior rather than merely describe it, and how authorization, scheduling, state
  transitions, idempotency, failure, and receipts would be connected to graph relations.
- It is not settled which graph is authoritative, which graphs are derived or disposable
  projections, how derived edges retain rule and premise provenance, or how they are invalidated
  and recomputed.
- There is no agreed necessity test for deciding when a graph role, service boundary, persisted
  record, property, or projection deserves to exist rather than being derived on demand, represented
  by an existing mechanism, or omitted.
- It is unclear how the system should detect and report important objects or relations that have no
  reconstructable purpose, consumer, objective connection, operational effect, or evidentiary role.
- It is unclear which prompt components should be reusable and composable without allowing hidden
  instruction or authority injection.
- There is no settled representation for the relationship among a request's objective, tags,
  instructional content, trigger point or condition, requested information, and targeted agent.
- It is not established how configured requests relate to prompt assets, dispatch configuration,
  agent activations, or the existing activation-scoped topic-observation mechanism.
- It is unclear whether instruction-bearing request content must always be frozen with the
  confirmed dispatch, should require reconfirmation when introduced later, or could eventually
  arrive through another explicit authority path.
- It is not established when requested information is best-effort and when its absence, refusal,
  invalidity, or failure has governed consequences.
- The status, interpretation, acceptance, and authority boundaries for information produced in
  response have not been defined.
- There is no agreed compatibility or migration rule for prompt changes, dynamic slot schemas,
  configured-request changes, model/provider changes, or changes in the larger project objective.
- There is no accepted metric model that separates prompt or request quality from model variance,
  task difficulty, source quality, topology, agent position, runtime timing, and evaluator bias.
- It is unclear which measurements should be offline, online, human-reviewed, adversarial,
  pairwise, outcome-based, or process-based.
- There is no established promotion lifecycle for candidate, tested, accepted, deprecated, or
  revoked prompt revisions.
- The relationship among prompt and request provenance, dispatch outcomes, agent outputs, dissent,
  decision quality, and objective traceability has not been defined.
- Existing external precedents and standards that should be reused rather than reinvented have not
  yet been identified for this bounded question.
