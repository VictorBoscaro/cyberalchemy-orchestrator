---
tags: [agents, architecture, kernel, interoperability, formalization, lean, research-brief]
node_type: research-initial-definitions
is_session: false
status: proposed
version: 0.4.0
last_updated: 2026-07-24
related_plan: plans/agent-language-research-program/PLAN.md
---

# Research Initial Definitions: Foundational Kernel and Formalization

## Context

The project is developing a compositional and governable environment in which people and agents
can create, relate, evaluate, execute, observe, and revise heterogeneous objects such as research,
plans, experiments, code, rules, tasks, sessions, and definitions. These objects must remain
interoperable and auditable even when their descriptions, classifications, locations, relations,
or surrounding organizational views change.

The first part of the research program needs to establish what minimum shared contracts, if any,
are necessary for that interoperability. Resolving this boundary matters because prematurely
centralizing domain semantics would constrain the system, while leaving identity, authority,
validity, provenance, composition, or historical interpretation implicit would make later
automation and recursive composition unreliable.

## Purpose

This document establishes the starting context for the first phase of the agent-language research
program. The research will inform later decisions about foundational contracts, the boundaries
among shared and specialized semantics, the role of formalization, and the readiness of subsequent
research into events, agents, plans, execution, evaluation, observability, and Git integration.

It is not a kernel specification, ontology, formal model, research plan, Dispatch, implementation
design, or source of runtime authority.

## Research Question (Can be refined)

What minimum shared contracts are necessary for independently evolving parts of the system to
remain interoperable, composable, revisable, and auditable, and what bounded role should Lean play
in defining, checking, evidencing, or explaining those contracts?

## Confirmed Product Constraints

- Kernel structure is a subject of the first research phase, not a preselected architectural
  answer.
- The research must consider whether the system needs one kernel, several specialized kernels, a
  microkernel with extensions, a kernel-of-kernels, another arrangement, or no artifact properly
  described as a kernel.
- Lean must be included because it is used extensively in the surrounding work, but its use must
  not silently confer product correspondence, runtime truth, operational authority, or promotion.
- Objects have identities that are not defined solely by their names, descriptions, physical
  paths, current classifications, or participation in a larger composition.
- Names, descriptions, properties, classifications, relations, validity claims, and architectural
  interpretations may be revised. Their accepted history and provenance must remain
  reconstructable.
- A person or agent must be able to create a construct and assert that it is valid. Such an
  assertion must remain distinguishable from accepted validity and from authority to cause an
  operational effect.
- Constructs and typed relations may recur at different declared levels and may compose new
  instances of the same language. Physical placement or level alone does not determine meaning.
- Relations may be composed. Accepted relations preserve their type, direction, origin,
  destination, scope, version, provenance, cardinality, transitivity, inheritance, and cycle
  policy.
- Different relation types may form trees, forests, DAGs, or controlled cyclic graphs.
- Loose tags and facets must permit inexpensive, incomplete description before all relevant
  properties or relation semantics have been settled.
- Layers and phases are not assumed to be universal kernel invariants. A phase is presently a
  revisable coordination view over a larger program rather than a fixed product layer.
- `Intent`, `Plan`, `Research`, `Discovery`, `Design`, `Spec`, `Code`, and `Verification` are
  candidate work kinds rather than an assumed universal linear pipeline. Their instances may recur
  at different scopes and relate recursively, including Research that investigates a Plan and a
  Plan that requests Research.
- A workflow may require a governed default progression among work kinds, but placement in that
  progression alone must not define an object's identity, meaning, authority, or physical
  location.
- Plans are revisable priors. Later evidence may revise their boundaries, sequence, assumptions,
  gates, or stopping points without erasing prior versions.
- Every governed artifact that communicates research, planning, discovery, design, specification,
  formalization, review, or a decision must expose an explicit `Open Questions` section and
  preserve later question dispositions in history.
- Recursive composition of objects does not authorize recursive orchestration. An invoked
  orchestrator must not invoke another orchestrator.
- Lineage does not automatically transmit authority, tools, budget, evidence, approval, or
  terminal state. Any relevant context or delegation must be explicit, attributable, and bounded.

## Current Evidence Baseline

- The current
  [agent-language research plan](../../plans/agent-language-research-program/PLAN.md) separates the
  broader program into language, event, agent, planning, evaluation, definition, observability,
  Git, and integration streams. It records kernel topology and Lean formalization as first-phase
  concerns.
- The
  [event-driven obligations definitions](../event-driven-obligations-and-task-orchestration/research-initial-definitions.md)
  already establish low-friction tags, typed relation metadata, derived physical placement, and
  authority-safe runtime facts as product constraints.
- The
  [agent invocation definitions](../agent-invocation-and-collaboration-topology/research-initial-definitions.md)
  already distinguish recursive object composition from nested orchestrator invocation and
  automatic inheritance.
- `../domainspec-lean-formalization` contains existing material on ontology conventions,
  composition, self-application, formal categorization, translation, and proof-bounded claims.
- `../domainspec-core` contains DomainSpec-v2 and CAV2 material on typed relationships,
  meta-types, axioms, invariants, authority, provenance, traceability, gates, promotion, recursive
  self-application, and distinctions between authoring and contract planes.
- The existing ACI material in this repository distinguishes accepted journal facts from derived
  projections and separates proposed configuration from executable authority.

## Known Gaps

- It is not established whether the word `kernel` names one useful product concept, several
  bounded concepts, only an architectural metaphor, or no necessary concept at all.
- The minimum interoperability boundary is not known, including which candidate constraints must
  be global, which may be local to a construct or subsystem, and which should remain configurable.
- It is unclear how multiple foundational contracts would declare ownership, compatibility,
  translation, composition, conflict, supersession, or conformance without recreating a universal
  kernel implicitly.
- A finite bootstrap boundary for checking foundational contracts has not been established.
- The interaction among identity, version, provenance, relative validity, authority, composition,
  history, and revision has not been tested for joint consistency or sufficiency.
- The system has not settled which aspects of names, descriptions, functions, objectives,
  classifications, properties, relations, rules, or types may change while preserving object
  identity.
- The boundary between a validity assertion, supporting evidence, accepted validity, contextual
  applicability, and operational authorization is not defined.
- It is unclear which rules are intrinsic to a construct, attached through relations, inherited
  through an explicitly declared policy, or evaluated only within a selected view or context.
- Composition semantics for edges and larger graph fragments are not defined, including how
  cardinality, transitivity, inheritance, validity, authority, and cycle policies interact.
- It is not known whether layers and levels should be represented as ordered structures, typed
  graphs, facets, projections, user-defined schemes, or several coexisting forms.
- The exact relationship among a program, phase, stream, plan, task, gate, and execution lifecycle
  remains unsettled.
- It is not settled which candidate work names denote durable artifact kinds, activity kinds,
  session kinds, contextual roles, stage instances, or overlapping classifications.
- The typed relation grammar among Plan, Research, Discovery, Design, Spec, Code, and Verification
  is not defined, including recursion, reopening, promotion, skipping, containment, production,
  challenge, evidence, cardinality, and cycle policies.
- The boundary between a configurable `WorkflowProfile` and any universally required promotion
  contract is not established.
- It is not known whether the minimal universal work contract should require only `Spec` and
  `Code`, while the route involving Plan, Research, Experiment, Discovery, Design, Verification,
  or other work kinds is selected and confirmed during installation or later per context.
- It is unclear whether `Object` is a useful common primitive or an overly broad addressability
  label that collapses materially different kinds such as Entity, Assertion, Event, Definition,
  Relation, and Execution.
- The relation contract may describe semantics owned by a relation type rather than metadata that
  every relation instance must repeat. The minimum cheap relation instance and the conditions that
  trigger stronger validation are not established.
- It is not known how loose tags avoid becoming a parallel informal ontology, including synonymy,
  contradiction, promotion, rejection, and later reclassification.
- The system has not distinguished semantic completeness from physical materialization: a complete
  authority and provenance model may not require every small interaction to persist every possible
  intermediate object.
- The user-confirmed prohibition on an invoked orchestrator invoking another orchestrator remains a
  product constraint, but its architectural consequences and the narrower failure it prevents
  have not yet been compared with bounded recursive-delegation models.
- `Plan as a revisable prior` has not been classified as an informal metaphor or a probabilistic
  model. If no Bayesian update semantics are intended, the vocabulary may need a less technically
  loaded description.
- The common Open Question contract is not settled, including stable identity, status, provenance,
  ownership, evidence, dependencies, closure, reopening, deferral, and cross-artifact projection.
- The high-level system view mixes confirmed constraints, candidate invariants, architectural
  hypotheses, and illustrative shapes. The presentation boundary among those modalities is not yet
  reliable enough to support a strong “decided nothing” claim.
- It is unclear which architectural claims are suitable for formalization, which require empirical
  evaluation, and which are primarily governance or product decisions.
- Lean's appropriate roles and limits are not established, including its relationship to runtime
  validators, generated artifacts, evidence, premises, authority, and versioned definitions.
- The reusable results in `../domainspec-lean-formalization`, DomainSpec-v2, and CAV2 have not yet
  been independently compared and reviewed for applicability to this research phase.
