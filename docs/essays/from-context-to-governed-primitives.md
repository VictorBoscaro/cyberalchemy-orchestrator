---
tags: [agents, context, primitives, graphs, ontologies, invariants, services]
node_type: essay
status: draft
version: 0.1.0
last_updated: 2026-07-25
authority: proposal-only
related:
  - docs/essays/macro-to-micro-context.md
---

# From Macro-to-Micro Context to Governed Primitives

I want to link the macro to the micro.

Every local action should remain connected to the larger context that gives it purpose. A file
change may realize a task. The task may belong to a sprint, advance a feature, implement a Spec,
and remain inside the scope of a user approval. The feature may serve a project, the project an
application, and the application a company objective.

```text
company objective
→ application
→ project
→ feature
→ sprint
→ task
→ attempt
→ file change
```

The work happens near the bottom. Its reason usually exists above it.

As described in [Linking the Macro to the Micro](./macro-to-micro-context.md), this is not one
universal hierarchy. The same task may participate in several contexts at once:

```text
Task-T
├── part-of Sprint-S
├── realizes Feature-F
├── implements Spec-V3
├── uses Research-R
├── executed-by Agent-A
└── authorized-by Decision-D
```

These connections do not mean the same thing. They cannot be collapsed into one `parent_id`, one
folder tree, or one universal workflow stage.

The system therefore needs more than a place to store documents. It needs a small set of
composable primitives from which users can define their own ways of organizing, governing, and
observing work. It must allow those definitions to start incomplete and change as more is
discovered, without losing identity, provenance, authority, or history.

This essay develops that hypothesis. It does not select an implementation architecture or declare
a final universal kernel.

## Why primitives come before artifact kinds

It is tempting to begin with a list such as:

```text
Plan
Research
Discovery
Experiment
Spec
Code
Prompt
Skill
Agent
Tool
```

Those are useful names, but they are not necessarily the primitive substrate.

A Research can investigate a Plan. A Plan can request Research. Research can exist inside the
context of a Discovery, an Experiment, a Feature, or no settled work kind yet. A Prompt may be a
versioned asset, a component of a Skill, a frozen part of a Dispatch, or a materialized runtime
invocation. An Agent may be a durable definition, a selected role, or one concrete attempt.

If these names become universal primitives too early, the infrastructure will encode today's way
of working as if it were permanent. If they remain only loose text, the system cannot validate,
compose, query, or govern them.

The initial substrate should instead make it possible to:

- give something a stable identity before its final classification is known;
- make attributable assertions about it;
- place it in one or more graphs;
- define which relations are possible;
- record concrete relation instances;
- attach incomplete classifications and tags;
- preserve changes through events and versions;
- state invariants that must hold;
- derive views without turning those views into authority.

Plan, Research, Agent, Prompt, Skill, and Tool can then be defined as domain constructs composed
from the substrate. Some may later prove foundational. That remains an open question.

## A provisional separation of the primitives

The following terms are hypotheses. Their value comes from keeping responsibilities separate, not
from claiming that every term deserves its own database table or deployed service.

### Identity-bearing object

An object is something the system can address across time and across representations.

Its identity is not reducible to its:

- name;
- path;
- current type;
- description;
- tags;
- current relations;
- physical representation.

The same object may move between folders, receive a new name, acquire a more precise
classification, or appear in several graphs without becoming a different object.

`Object` may ultimately be too broad as a formal carrier. Entity, assertion, event, definition,
relation, and execution may require different sorts. For now, identity-bearing object is a useful
informal starting point, not an accepted universal type.

### Node

A node means only that an object appears in a graph.

It does not, by itself, say what the object is. The same object can appear as a node in several
graphs, at different levels and in different dimensions.

```text
Object: Research-R

Node in a work graph:
  Research-R ──supports──→ Discovery-D

Node in a feature graph:
  Research-R ──provides-evidence-for──→ Feature-F

Node in a knowledge graph:
  Research-R ──supports-claim──→ Hypothesis-H
```

The object's identity remains stable. Each graph contributes a contextual occurrence and a set of
claims about it.

### Relation assertion

A relation assertion states that two or more identified things are connected in a particular way,
under a declared context.

```text
Task-T ──realizes──→ Feature-F
```

The relation type carries meaning. `part-of`, `realizes`, `supports`, `authorized-by`,
`depends-on`, and `represented-by` are not interchangeable.

A relation assertion may need provenance, scope, validity, confidence, and a governing schema
version. These are candidate obligations, not a settled record format.

### Classification, type, role, facet, field, and tag

These concepts should not collapse into one generic metadata mechanism.

- A **type** states conformance to a structural contract.
- A **role** describes how an object participates in one context.
- A **classification** places an object under a concept or scheme.
- A **facet** supplies one declared dimension of description.
- A **field** carries a named value under a schema.
- A **tag** is a cheap, potentially incomplete assertion used for discovery and grouping.

For example, an object may:

```text
conform to type: Document
play role: EvidenceSource
be classified as: Research
have lifecycle facet: Proposed
have domain tag: agent-communication
have free tag: needs-rethinking
```

A tag should not silently become a type, a permission, an accepted fact, or an invariant. It may
later be promoted into a governed vocabulary or structural field, but that promotion should be
explicit and historical.

### Event

An event records that something happened:

```text
object-created
tag-proposed
relation-accepted
schema-version-published
file-changed
approval-revoked
dispatch-started
```

Events let the system reconstruct how a representation changed rather than merely overwrite the
current state. They also provide activation points for hooks.

An event is evidence that an occurrence was recorded. It is not automatically proof that the
occurrence was correct, authorized, or successfully enforced.

### Assertion

An assertion is an attributable claim.

Examples include:

```text
Agent-A proposes that Object-X is Research.
Validator-V reports that Graph-G conforms to Schema-S.
User-U approves Dispatch-D within Scope-C.
Test-T reports that Implementation-I satisfies Obligation-O.
```

Proposed, accepted, rejected, superseded, and derived assertions must remain distinguishable.
Validity, acceptance, and authority are different judgments.

### Graph

A graph is a structural arrangement of nodes and relations.

Graphs are arbitrarily definable: code, documents, work, authority, provenance, execution,
knowledge, and repository structure may all be projected as graphs. This does not mean that every
source is reduced to a graph. Code remains code; a document remains a document. The graph is a
governed structural representation of selected aspects.

Graphs may have different mathematical forms:

- trees and forests;
- directed acyclic graphs;
- cyclic directed graphs;
- quivers or directed multigraphs;
- hypergraphs;
- temporal graphs;
- typed or property graphs.

These forms are not interchangeable. A DAG expresses acyclicity. A quiver permits independently
identifiable arrows, including parallel arrows and, unless restricted, cycles. A hypergraph can
represent a relation involving more than two participants.

The graph's mathematical form is also independent of its function. A graph may be descriptive,
normative, executable, epistemic, authoritative, provenance-bearing, or merely a projection.

### Schema graph

A schema graph defines the space of possible graph instances:

- permitted node types;
- permitted relation types;
- relation origins and destinations;
- cardinalities;
- cycle policies;
- composition rules;
- constraints and invariants.

```text
Task ──realizes──→ Feature
Feature ──advances──→ Objective
Approval ──authorizes──→ Dispatch
Dispatch ──produces──→ Artifact
```

This schema does not assert that any concrete Task or Dispatch exists.

### Runtime graph

A runtime graph contains concrete instances:

```text
task-123 ──realizes──→ feature-search
feature-search ──advances──→ objective-retention
approval-987 ──authorizes──→ dispatch-456
```

Every runtime graph should declare the schema version against which it claims conformance. A
schema change must not silently reinterpret old runtime facts.

In an initial formal hypothesis, a runtime graph `G` conforms to a schema graph `S` through a
structure-preserving map:

```text
p : G → S
```

Runtime nodes and edges map to permitted schema elements, preserve source and destination, and
satisfy the constraints declared by `S`.

This remains a hypothesis. Different graph families may require different conformance models.

### Morphism

`Morphism` is presently overloaded and should be used carefully.

It might mean:

1. a possible arrow declared inside a schema;
2. a concrete relation instance in a runtime graph;
3. a transformation between graph schemas;
4. a structure-preserving map from a runtime graph to its schema;
5. a composable transformation among larger system constructs.

These are related but not identical. Until a formal model is selected, the system should name the
exact role rather than use `morphism` as a universal synonym for every edge or operation.

### Path and witness

A path connects several direct relations:

```text
Task-T
──part-of──→ Sprint-S
──realizes──→ Feature-F
──advances──→ Objective-O
```

The system may derive that `Task-T` contributes indirectly to `Objective-O`, but only if the
relevant composition rule permits that conclusion.

A witness records the direct relations, rule versions, and assumptions used to derive it. Derived
macro-to-micro connections should remain reconstructable from their witnesses.

### Ontology

An ontology is a governed semantic system that defines how the objects and relations of one or
more graphs are interpreted, composed, and constrained.

Graphs provide structure. An ontology provides meaning:

- the vocabulary used to interpret nodes and relations;
- the distinctions among concepts;
- mappings among graphs;
- valid and invalid compositions;
- semantic constraints;
- permitted inferences.

A collection of graphs does not automatically form an ontology. It becomes an ontological
composition when their meanings and mappings are explicit. One graph may also be interpreted by
an ontology; the number of graphs is not the defining property.

An initial hypothesis is:

```text
Ontology =
  graphs
  + semantic vocabulary
  + interpretations
  + cross-graph mappings
  + constraints
  + inference rules
```

### Invariant

An invariant is a property that must remain true across a declared set of states, transitions, or
compositions.

Examples might include:

- an object retains stable identity across projections;
- a runtime edge conforms to its declared schema version;
- a projection cannot manufacture authority;
- a derived path retains its direct witnesses;
- a tag cannot silently confer execution permission;
- a revoked approval cannot authorize later effects;
- an invoked orchestrator cannot invoke another orchestrator.

An invariant declaration is not proof that the property holds. It still requires an evaluator,
evidence, an applicability context, and, where effects matter, a real enforcement point.

### Kernel

A kernel owns or checks a bounded set of invariants.

There may be:

- a graph-schema kernel;
- a runtime-graph conformance kernel;
- a tag-governance kernel;
- an authority kernel;
- an event-history kernel;
- a prompt-composition kernel;
- an agent-invocation kernel.

If these kernels compose, a higher-level contract must say which global properties survive their
composition. That is the motivation for considering a kernel of kernels. It should not be assumed
to be one universal service or one artifact.

The kernel is not the starting point. The starting point is the property the user needs preserved.
The kernel is a candidate mechanism for making that preservation explicit and checkable.

### Projection and view

A projection selects and organizes part of a larger state for one purpose.

The same objects can be projected by:

- Feature;
- Plan;
- sprint;
- artifact kind;
- authority scope;
- unresolved question;
- agent;
- physical folder.

A folder hierarchy is one projection among many. A projection may be stale, partial, or optimized
for a particular query. It must not acquire semantic or operational authority merely because it is
convenient to inspect.

## Domain constructs are compositions, not necessarily primitives

Agents, Prompts, Skills, Tools, Plans, Research, Discoveries, and Experiments are important system
objects. The hypothesis is not that they are unimportant, but that their definitions should be
constructed from smaller distinctions.

For example:

```text
Agent
  identity
  + capabilities
  + roles
  + authority constraints
  + runtime attempts
  + provenance

Prompt
  identity
  + versioned content
  + instruction authority
  + composition rules
  + materialized invocation occurrences

Skill
  identity
  + invocation contract
  + instructions
  + allowed capabilities
  + validation and lifecycle

Tool
  identity
  + effect boundary
  + input/output contract
  + permission requirements
  + observations and receipts
```

These are preliminary decompositions. They make it possible to ask which invariants belong to all
constructs and which belong only to one domain.

## Invariants connect primitives without collapsing them

Primitives give the system distinguishable carriers. Invariants state what must remain true when
those carriers interact.

Consider this chain:

```text
User Decision-D
──authorizes──→ Workflow-W
──generates──→ Dispatch-X
──invokes──→ Agent Attempt-A
──produces──→ File Change-C
──realizes──→ Task-T
──advances──→ Feature-F
──serves──→ Objective-O
```

Several different kernels may participate:

- the authority kernel checks that `Dispatch-X` remains inside the scope of `Decision-D`;
- the invocation kernel checks that the chat agent may invoke an orchestrator, while that
  orchestrator and its subagents may not invoke another orchestrator;
- the runtime graph kernel checks that concrete edges conform to their schema;
- the provenance kernel preserves who or what produced `File Change-C`;
- the work-context kernel checks that the upward and downward paths remain reconstructable;
- the tag kernel prevents a loose classification from being treated as authority;
- the projection kernel prevents a generated folder view from becoming a new source of truth.

No single primitive performs all these checks. No one relation should inherit all the semantics of
the others.

The kernel-of-kernels problem appears when these local assurances are composed:

```text
valid authority relation
+ valid runtime graph
+ valid provenance record
+ valid work relation
≠ automatically valid total execution
```

The composition needs its own witness. Local validity must not be mistaken for global
compatibility.

## Example: graph services

Graph management naturally separates into at least two logical services.

### Graph Schema Service

The Graph Schema Service manages the space of possible graphs.

It may:

- register graph kinds and schema identities;
- define node and relation types;
- declare whether a graph is a DAG, quiver, hypergraph, or another form;
- define cardinality and cycle policies;
- register composition rules and path equations;
- version schemas;
- compare compatibility between schema versions;
- manage schema mappings and migrations;
- publish constraints for independent validators;
- preserve who proposed, accepted, superseded, or rejected a schema.

This service manages definitions. It does not own concrete runtime facts merely because they
conform to its schemas.

### Runtime Graph Service

The Runtime Graph Service manages concrete graph instances.

It may:

- create and address runtime nodes and edges;
- bind every graph instance to a schema version;
- preserve provenance and temporal validity;
- validate changes against the declared schema;
- record events and version history;
- expose traversal and query;
- build materialized projections;
- calculate diffs;
- emit events for hooks;
- retain derivation witnesses;
- distinguish authoritative, projected, derived, proposed, and cached graphs.

For example, a source-code projector may emit a call graph. A document projector may emit a graph
of claims and references. A Dispatch runtime may emit execution, authority, and provenance graphs.
The service manages these graph instances without claiming that every projection is complete or
authoritative.

### The boundary between them

```text
Ontology
  interprets
      ↓
Graph Schema
  defines possible structure
      ↓ conforms-to
Runtime Graph
  records concrete instances
```

The schema and runtime services should evolve independently but meet at a governed conformance
boundary.

If a schema changes:

- the old runtime graph retains its original interpretation;
- the new schema receives a new identity or version;
- compatibility is evaluated explicitly;
- migration produces a trace;
- failed or partial migration remains visible.

The current hypothesis names two logical services. They need not become two network processes.

## Example: tag service

Tags need their own management capability because they occupy the boundary between cheap
description and governed semantics.

A useful tag service should support both open and governed tags.

### Open tags

Open tags allow inexpensive description before the vocabulary is settled:

```text
needs-rethinking
probably-security-related
interesting-for-agent-memory
```

They may be proposed by users, agents, or deterministic extractors. They should retain provenance
and should not silently become accepted classifications.

### Governed tags

Governed tags belong to declared vocabularies or dimensions:

```text
knowledge-domain: formal-methods
lifecycle: proposed
risk: high
work-kind: research
```

Their definitions, allowed values, applicability, and lifecycle may be versioned.

### Responsibilities of the Tag Service

The service may:

- register tag identities and namespaces;
- preserve aliases without losing historical names;
- accept free tag proposals;
- manage controlled vocabularies;
- record who or what attached a tag;
- distinguish proposed, accepted, rejected, deprecated, and superseded tags;
- attach confidence and temporal validity where meaningful;
- detect incompatible or redundant tags;
- query objects through tag combinations;
- recommend consolidation without applying it silently;
- promote recurring open tags into governed vocabulary;
- project tags into views and search indexes;
- emit events when important classifications change.

The service should protect at least these boundaries:

- a tag does not define object identity;
- a tag does not automatically establish a structural type;
- a tag does not authorize an effect;
- an agent-generated tag is an assertion, not accepted truth;
- removing a tag from the current view does not erase its history;
- synonym resolution does not silently rewrite prior meaning.

### Example

Suppose an agent creates an unidentified artifact and tags it:

```text
open tag: maybe-research
domain tag: graph-theory
feature tag: agent-context
```

Later, a user accepts `Research` as its work classification and relates it to an Experiment:

```text
Artifact-X ──classified-as──→ Research
Artifact-X ──evidence-for──→ Experiment-E
```

The original `maybe-research` assertion remains in history. The accepted classification does not
need to depend on the folder where the artifact is stored.

## Other possible logical services

The graph and tag examples suggest a family of bounded management capabilities:

### Identity and Object Registry

Maintains stable identities, aliases, versions, and cross-representation references.

### Ontology and Definition Service

Maintains vocabulary, concept definitions, semantic relations, mappings among ontologies, naming
conflicts, and definition provenance.

### Invariant and Kernel Registry

Maintains invariant identities, scope, applicability, owners, evaluators, evidence requirements,
versions, and composition obligations.

### Conformance and Validation Service

Evaluates explicit judgments such as graph-to-schema conformance, invariant satisfaction, and
compatibility. Its verdict is evidence; it does not automatically authorize effects.

### Event and Hook Service

Records accepted events, resolves applicable triggers, schedules reactions, exposes which hooks
are active, and preserves why each hook ran.

Examples include:

- when more than a configured number of lines change, evaluate whether nearby README projections
  need refresh;
- when Research is placed under a forbidden Discovery projection, report or repair the
  inconsistency;
- when code changes without a corresponding Spec relation, open a reconciliation obligation.

### Authority and Decision Service

Records approvals, rejections, revocations, delegations, scopes, conditions, and the concrete work
that claims to operate under them.

### Provenance and Lineage Service

Preserves origin, transformations, dispatches, agent attempts, sources, generated artifacts, and
derivation witnesses without implying authority inheritance.

### Projection and View Service

Builds feature, Plan, sprint, folder, graph, and dashboard views over shared objects. It maintains
coherence between views while preserving their derivative status.

### Agent and Capability Registry

Maintains agent definitions, roles, capabilities, constraints, versions, and the distinction
between a durable agent definition and one runtime attempt.

### Prompt and Instruction Service

Maintains prompt identities, versions, components, metaprompts, composition constraints, frozen
dispatch bindings, and materialized invocation records.

### Skill and Tool Registry

Maintains invocable capabilities, contracts, effect boundaries, permission requirements,
dependencies, versions, and observations.

### Context Compiler

Selects and compiles the bounded context required for a task while preserving resolvable lineage
to the larger objective. It should not infer authority merely from relevance or ancestry.

These are logical responsibilities, not a proposal for a large collection of microservices.
Several may share one implementation. Their boundaries matter before their deployment topology.

## A possible minimum architecture

The emerging shape is:

```text
Human intent and decisions
            ↓
Identity-bearing objects and attributable assertions
            ↓
Ontologies and schema graphs define possible meaning and structure
            ↓
Runtime graphs, tags, events, and domain constructs record current work
            ↓
Kernels and validators check bounded invariants
            ↓
Hooks react to accepted changes
            ↓
Projections organize the same state for different users and purposes
```

The system remains configurable because users can define schemas, vocabularies, tags, hooks,
views, and bounded kernels. It remains governable because these definitions have identity,
version, provenance, authority, and explicit composition boundaries.

## What this would make possible

If this substrate works, a user could:

- define which work relationships are allowed without fixing one universal folder hierarchy;
- view the same project by Feature, Plan, objective, sprint, artifact kind, or authority scope;
- create new classifications before deciding whether they deserve a formal type;
- discover which tasks no longer connect to a live objective;
- trace a file change to the user decision that authorized it;
- see which schemas and hooks govern a Dispatch;
- distinguish a proposed tag from an accepted classification;
- change a schema without silently changing the meaning of historical runtime facts;
- detect when independently valid domain rules compose into an inconsistency;
- generate small agent context packages while preserving the path back to the macro objective.

The system does not need to know every future artifact kind in advance. It needs to preserve the
conditions under which new kinds, relations, and rules can be introduced safely.

## Candidate invariants

The following are hypotheses to investigate, not accepted universal laws:

- identity survives renaming, relocation, reclassification, and projection;
- accepted history remains reconstructable;
- every runtime graph declares the schema version it claims to instantiate;
- schema changes do not silently reinterpret historical instances;
- relations preserve type, direction, provenance, scope, and declared cycle policy;
- derived paths retain their direct witnesses and rule versions;
- projections cannot manufacture facts or authority;
- lineage does not automatically delegate authority, tools, evidence, or budget;
- tags do not silently become types, truths, permissions, or invariants;
- user approvals and rejections remain attributable and linked to their governed scope;
- revocation and supersession remain visible;
- local kernel validity does not imply global compositional validity;
- checker acceptance does not imply physical runtime enforcement;
- recursive composition of work objects does not authorize recursive orchestrator invocation.

## Open questions

- Which carriers are truly primitive, and which are convenient compositions?
- Is `Object` a useful shared abstraction or only a common addressing envelope around many sorts?
- Which graph families need first-class support?
- When should a relation be modeled as a binary edge, hyperedge, assertion object, or event?
- Which schema arrows admit path composition, and which explicitly do not?
- Does an ontology own schemas, interpret them, compose them, or perform all three in separate
  views?
- Can one runtime graph conform to several schemas or ontologies without ambiguous authority?
- Which tags remain open forever, and what evidence permits promotion into governed vocabulary?
- Which invariants are global, which belong to domain kernels, and which are configurable policy?
- What must a kernel-composition witness prove or record?
- Which logical services need independent persistence and authority boundaries?
- Which services should be one implementation even if their conceptual responsibilities remain
  distinct?
- What should be checked with deterministic validators, SMT solvers, Lean, empirical tests, or
  human judgment?
- How much of this structure can be maintained automatically before its maintenance costs exceed
  its value?

The purpose of these primitives is not to make the system abstract for its own sake.

It is to preserve one practical property:

> The smallest action should remain connected to the changing context, meaning, and authority that
> make it worth doing.
