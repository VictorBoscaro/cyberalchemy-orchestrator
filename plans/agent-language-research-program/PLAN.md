---
tags: [agents, research-plan, orchestration, events, actions, ontology, observability]
node_type: plan
plan_type: research-program
is_session: true
plan_id: agent-language-research-program
status: proposed
version: 0.12.0
created_at: 2026-07-24
last_updated: 2026-07-24
entry_point:
  kind: conversation
  summary: >
    The user asked for a research plan covering a modular agent language and its supporting
    infrastructure, including events, actions, schedules, agent modes, sessions, definitions,
    hierarchy, observability, dashboards, Git integration, and progressive validation.
authority: proposal-only
---

# Plan: Agent Language Research Program

## Why this plan exists

The product direction now spans several connected but independently researchable systems. Treating
them as one research question would mix language semantics, runtime authority, agent collaboration,
knowledge representation, observability, and product interaction into a single result that would
be difficult to falsify or implement.

This plan divides that space into research streams and integration gates. It proposes what should
be investigated and in what dependency order. It is not itself research, a Dispatch, a schedule,
or implementation authority.

The plan is a prior over the program rather than a frozen route. Its phases, stream boundaries,
dependency assumptions, and gates should be updated when findings, contradictions, or changed
objectives justify a revision. Earlier versions remain part of the program's provenance.

## Program question

What is the smallest coherent language and infrastructure that lets a user define, relate,
observe, evaluate, schedule, and evolve agent work—from events and actions through multi-agent
sessions and knowledge artifacts—without hiding authority, provenance, uncertainty, or cost?

## Inputs already available

- [Event-driven obligations and task orchestration](../../research/event-driven-obligations-and-task-orchestration/research-initial-definitions.md)
- [Agent invocation and collaboration topology](../../research/agent-invocation-and-collaboration-topology/research-initial-definitions.md)
- Existing ACI architecture, domain, workflow, capability, journal, projection, and host-hook
  artifacts under `docs/features/agents-communication-infra/`
- Existing subagent strategy, research, review, experiment, interrogation, observability, ontology,
  and definition-governance skills as evidence of recurring capability shapes
- Candidate precedents in `../ZefraHub`, `../maestro-trama`, Git/GitOps systems, and external
  research, each requiring explicit evidence and authority treatment when used

## Research streams

### R1 — Language kernel and typed ontology

Define the minimum common model for objects, classes, categories, properties, typed relationships,
containment, labels/tags, definitions, identity, version, provenance, and authority.

Key questions include whether labels are free annotations or governed definitions plus
assignments; how multiple hierarchies coexist; how things can be created under partial knowledge
and classified later; how a fixed kernel invariant set coexists with easily configurable
user-level invariants; and which semantics belong in the kernel rather than an extension.

Hierarchy must not be assumed to mean one containment tree. The same object may participate in
several typed recursive structures: physical or logical containment, class/subclass,
instance/classification, generated-by lineage, parent/child execution, plan/subplan,
dispatch/child-dispatch, review-of, definition-of, authority delegation, provenance, and temporal
succession. Research must establish which structures are trees, forests, DAGs, or general graphs
and which edge kinds permit or forbid cycles.

Every addressable thing must be taggable, including tags and invariant definitions themselves.
Any authorized source—user, agent, action, rule, observation, importer, or another object—must be
able to generate candidate tags or assignments easily. Each assignment must preserve whether it
was declared, generated, inferred, or imported; its generator and evidence; its confidence or
status when applicable; and the authority under which it becomes accepted. Capability and
where-used are initial examples of tag facets, not a closed taxonomy.

Physical location is one property or projection of an object, not the place where that object's
meaning is defined. A construct may appear at the repository root, under `internal_tools`, or in
another derived view without changing its identity or semantics. Folder trees, indexes, dashboards,
and task-oriented arrangements may therefore expose different navigational projections over the
same authoritative objects and relations. Research must establish how those projections are
generated, reconciled, versioned, and explained without making a path an implicit type or authority.

Expected output: a minimal candidate invariant kernel, progressive-definition semantics, and an
ontology/tag boundary with explicit collapse tests.

R1 must not assume in advance that the result is one universal kernel. It must compare a single
kernel, several specialized kernels connected by protocols, a microkernel plus extensions, and a
possible kernel-of-kernels that governs how kernels declare identity, contracts, compatibility,
translation, version, authority, and composition without absorbing their domain semantics.

Lean is an explicit part of this stream because the surrounding system already uses it extensively.
The research must keep three roles separate: Lean as a notation and reasoning aid, Lean as an
executable checker for selected contracts, and Lean artifacts as a possible source of governed
evidence. It must not assume that using Lean makes a theorem, model, generated artifact, or
architectural choice operationally authoritative. The existing `../domainspec-lean-formalization`
material is a starting evidence corpus for compositionality, bounded self-application, ontology
conventions, relations, and proof-bound claims.

The high-level system document must eventually end with a mathematical formalization appendix.
That appendix starts with explicit mathematical notation and only then translates the accepted
model into Lean. Category theory is a required lens, supplemented by whatever mathematics is
needed, but every categorical object, morphism, functor, law, or other construction must identify
the original infrastructure concept it models, the responsibility it carries, and the claims it
does not establish. Decorative or analogy-only formalization does not satisfy this requirement.

The appendix must separate definitions, assumptions, candidate axioms, invariants, propositions,
counterexamples, proof obligations, and machine-checked results. Each concept must link back to the
original infrastructure artifact and explain whether the formalization describes semantics,
authority, lifecycle, composition, projection, execution, or verification.

Every governed artifact that communicates research, planning, discovery, design, specification,
formalization, review, or a decision must expose an explicit `Open Questions` section. The section
may state that no questions are currently identified, but it must not be silently omitted.
Questions that are answered, superseded, deferred, rejected, or moved out of scope remain
historically traceable rather than disappearing.

### R2 — Events, actions, obligations, and parameter resolution

Research the common event envelope, universal `tags`, required-minimum versus optional payload
fields, defaults, templates, contextual resolution, enrichment, and effective-value provenance.
Define how pre-action and post-action obligations attach at different scopes and how conflicts,
failure, replay, and idempotency behave.

Acceptance probes include mandatory declarations around document reads and rules applying to all
documents of a selected type.

Expected output: event/action/obligation semantics and authority-safe extension points.

### R3 — Configurable agent constructs and sessions

Research whether persona, role, mode, capability, skill, tool, and session type are genuinely
distinct concepts, contextual views, or classifications that can overlap and be added later. Use
the following configurable constructs as probes without pre-classifying them:

- `Scout`: short, precise, bounded exploration;
- `Interviewer`: evidence-backed question selection, one answer at a time, configurable scope,
  mutable targets, stopping rules, and resumable session state;
- `Worker`, `Reviewer`, nested reviewer, orchestrator, synthesizer, skeptic, and approver shapes.

Expected output: a progressively typed configuration model and lifecycle for independently
observable agent-related constructs and sessions.

### R4 — Plans, task definitions, schedules, and execution

Define Plan as an independent proposal session with its own properties, entry-point provenance,
versions, decisions, and promotion state. Relate it to reusable task definitions, confirmed
Dispatches, TaskRuns, schedules, conditions, event triggers, retries, cancellation, and the minimum
worker-plus-reviewer topology.

`Intent -> Plan -> Research -> Discovery/Design -> Spec -> Code -> Verification` is a candidate
work grammar, not a universal linear pipeline. Its construct kinds may recur and relate
recursively: a Research may investigate or challenge a Plan; a Plan may request Research; a Spec
may contain a local Plan or expose a Research need; Code or Verification may reopen Discovery,
Research, or Spec. Research must distinguish construct kinds from stage instances, define the
typed relations that connect them, and establish which workflow profiles require which promotion
gates without making position in one sequence define an object's meaning.

Interactive action requests are an explicit acceptance case. When a user asks the system to do
something, the request may need to become a durable, independently identifiable work intent before
execution begins. Later acceptance, planning, attempts, progress observations, blockers,
completion, cancellation, or failure must be recorded as new attributable facts rather than edits
to the original request. Research must establish which utterances cross the durable-work boundary,
whether admission requires confirmation, and how conversational clarification remains distinct
from an accepted command, task, or run.

Unexecuted Dispatches are also an explicit acceptance case. As soon as the system identifies or
generates a meaningful Dispatch candidate, it must be possible to pre-register the candidate so it
is easy to find, inspect, and remind the user about. Pre-registration is not executable authority
and must remain distinct from the official confirmed-Dispatch ledger. If the candidate is never
launched, its history must still receive an attributable disposition such as declined, superseded,
expired, blocked, cancelled, or not-launched-with-reason rather than disappearing from memory.

Recursive object composition is an explicit acceptance case: plans, Dispatches, reviews, tasks,
sessions, definitions, and other language objects may contain, relate to, or produce objects of
their own kind. This does not authorize recursive orchestrator invocation. A delegated
orchestrator must not invoke another orchestrator; agents inside a Dispatch receive only the small,
task-specific tools resolved for their assignments. Every recursive object relation must preserve
stable identity, typed parent/child or generator/product relations, depth and cycle policy,
provenance, budgets, terminal state, and a distinction between lineage and authority inheritance.

Expected output: a lifecycle from user intent to plan, confirmation, dispatch generation, and
observable execution without conflating any of those authorities.

### R5 — Evaluation ladders and user-facing escalation

Research graduated evaluation in which cheap deterministic checks precede Scouts, reviewers,
tensioned groups, experiments, or human decisions. Define budgets, thresholds, dissent retention,
stop conditions, escalation evidence, and the rule that user notifications should usually be backed
by the appropriate validation level.

Acceptance probe: evaluate whether a new repository should be opened, escalate through bounded
review levels, and ask the user only when a consequential choice remains.

Expected output: a cost-aware evaluation and escalation protocol.

### R6 — Definitions, experiments, recommendations, and promotion

Research how user-created definitions for actions, skills, code, categories, or other language
objects enter an experiment; how evidence and review determine usefulness; and how accepted
definitions are registered, versioned, related, and retired.

Include recommendation without forced automation: repeated creation of similar artifacts may
produce a recommendation for a canonical document, while the base system remains able to create
and classify documents without an event rule.

Expected output: definition and recommendation lifecycles with human-governed promotion.

### R7 — Observability and the multi-level dashboard

Define the authoritative facts and derived read models required to see what the system is doing
across system, layer, pipeline, agent, task, plan, session, event, action, relationship, artifact,
and execution levels.

Research progressive disclosure, stable drill-down identity, visible provenance and freshness,
honest partial/error/unavailable states, replay, audit, and the division between bounded-cardinality
metrics and rich events or traces.

The operational view must make pending and live work legible: candidate Dispatches awaiting
confirmation, confirmed Dispatches not yet started, candidates deliberately not launched, intents
not yet admitted, admitted tasks not yet started, active and stalled runs, blockers, requested
decisions, recent progress, terminal outcomes, and work whose status is unknown because no fresh
observation exists. Reminders are derived from these accepted lifecycle facts; a reminder neither
confirms a Dispatch nor authorizes execution.

Expected output: an observability model and dashboard information architecture, not a UI
implementation.

### R8 — Git and GitOps integration

Research which parts of identity, versioning, review, branching, diffs, provenance, promotion,
rollback, and reconciliation should reuse Git; which require runtime or database authority; and how
GitOps can remain strong without making a repository commit the authority for every live action.

Expected output: a Git/GitOps responsibility boundary and staged adoption path.

### R9 — Integrated architecture and build strategy

Join the preceding findings into one architecture explained from product problem and conceptual
model through language semantics, control plane, data plane, knowledge plane, observability, and
candidate infrastructure. Compare extending this repository, forking it, and starting a new
repository while reusing selected assets.

Expected output: the high-level application document, paired architectural views, decision
inventory, and an implementation-readiness recommendation.

## Dependency shape

1. Run the first phase as a foundational inquiry over R1, including kernel topology and Lean
   formalization feasibility, without requiring that it end in one universal kernel.
2. Run R2 and R3 in parallel once their shared terms are stable enough.
3. Use R2 and R3 to constrain R4.
4. Run R5 and R6 against the R1–R4 candidate model.
5. Develop R7 across all streams, because observability is a cross-cutting contract rather than a
   final UI concern.
6. Run R8 once artifact, definition, event, and execution authorities can be distinguished.
7. Perform R9 only after the preceding streams expose their agreements, contradictions, and open
   decisions.

## Program phases as revisable coordination objects

A phase is a bounded coordination view over a larger program: it groups questions, evidence
requirements, dependencies, and decision gates that are useful to consider together. It is not a
product layer, a universal lifecycle state, or an invariant of every system object. A phase has its
own identity and version, may overlap another phase where dependencies require it, and may be
split, merged, reordered, or superseded without rewriting the history of work already performed.

Phase boundaries are therefore hypotheses recorded by the Plan. Passing a phase gate means that
the next work has enough explicit evidence and unresolved-risk visibility to begin; it does not
mean that every conclusion inside the phase is final or irreversible.

### Phase 1 — foundational contracts and formalization feasibility

The first phase investigates the minimum conditions under which heterogeneous parts of the system
can remain interoperable, evolvable, and auditable. `Kernel` is an object of this research, not its
assumed answer.

Its question families are:

- **kernel necessity and boundary:** what failure or ambiguity a kernel is meant to prevent; what
  must be shared globally; and what can remain local, translated, or extension-defined;
- **kernel topology:** one universal kernel, multiple specialized kernels, microkernel plus
  extensions, protocol federation, or a kernel-of-kernels, including hybrid forms;
- **candidate invariants:** identity, versioning, provenance, relative validity, typed relations,
  explicit authority, traceable composition, and history preservation, tested individually and in
  composition rather than accepted as a fixed list;
- **bootstrap and regress:** how conformance and compatibility can be checked without requiring an
  unbounded tower of metakernels, metavocabularies, or external authorities;
- **evolution:** how names, descriptions, properties, classifications, relations, rules, and even
  kernel contracts may change while claims remain attributable and old interpretations remain
  reconstructable;
- **recursive composition:** which constructs and relations remain closed under composition,
  which controlled forms of self-description are useful, and where cycles, depth, or authority
  must be bounded;
- **validity and promotion:** how a person or agent can create a construct and claim it is valid,
  how that claim differs from acceptance or operational authority, and what evidence or gate can
  promote it;
- **views and placement:** how layers, levels, folders, indexes, and dashboards arise as
  configurable projections without becoming hidden semantic or authority boundaries;
- **formalization boundary:** which claims are precise and stable enough to formalize, which remain
  hypotheses or empirical product questions, and what information is lost when translated into a
  formal model;
- **Lean fit:** which parts benefit from Lean definitions, propositions, proofs, countermodels,
  executable checks, or generated witnesses; how those artifacts relate to runtime validators;
  and where Lean would add coupling or proof cost without commensurate confidence.

The phase should compare at least three relationships between formalization and the running system:

1. Lean is explanatory only and informs human-reviewed specifications.
2. Lean produces or validates portable contracts and test artifacts consumed by implementations.
3. Selected Lean-checked claims become governed evidence at an explicit promotion boundary.

The phase must not collapse proof into authority. A Lean proof may establish a proposition relative
to definitions and premises; it does not by itself establish that those definitions match the
product, that the premises hold at runtime, or that an action is authorized.

Phase 1 is ready to yield downstream work when it has exposed the viable kernel topologies,
identified which candidate invariants are global, local, or still disputed, described a finite
bootstrap boundary, and assigned Lean a bounded role with explicit translation and authority
semantics. These are readiness conditions for continuing the program, not a requirement to freeze
the ontology permanently.

## Research execution shape

Each stream should eventually receive its own confirmed `dispatch_type: research` sheet rather
than being executed as one oversized dispatch. A typical substantial stream may use:

- tensioned explorers over distinct methodologies or source corpora;
- a synthesizer that preserves claims, dissent, and provenance;
- one or more named skeptic gates;
- bounded robot-talks or zig-zag only where confrontation can change the result;
- a parent or independent auditor as final approver.

Exact agents, prompts, sources, budgets, loops, tools, and write scopes are intentionally absent.
They belong to later concrete dispatch proposals and require the existing capability, tension, and
human confirmation gates.

The mathematical appendix uses staged review over frozen document revisions. Each review layer has
two independent reviewers. Two sequential layers compare their surviving conclusions; when they
do not agree, a third layer uses fresh reviewers against the resulting frozen revision. Because
downstream dynamic handoff is not yet durably bound by ACI, each layer is a separate confirmed
Review Dispatch rather than one opaque multi-layer invocation.

## Program gates

- **G1 — Invariant and vocabulary readiness:** the minimal global laws are explicit, shared terms
  have one canonical home, partial classification is representable, and unresolved collisions are
  visible.
- **G2 — Authority readiness:** proposal, definition, event, command, Dispatch, TaskRun, journal
  fact, projection, and recommendation cannot silently authorize one another.
- **G3 — Composition readiness:** event/action rules, agent modes, plans, and schedules compose
  without requiring bespoke runtime code for every case.
- **G4 — Observability readiness:** every accepted action and derived recommendation can be traced
  to effective configuration, evidence, and responsible actors.
- **G5 — Implementation readiness:** the integrated architecture identifies a bounded first slice,
  its invariants, migrations, tests, and explicit non-goals.

## Immediate next steps

1. Before dispatching research, author a high-level explanatory architecture brief that starts
   from the product problem and the compositional model, progressively introduces the kernel and
   its projections, then presents the candidate architecture and alternative tools for each
   responsibility without treating any option as selected implementation authority.
2. Review and amend the stream boundaries in this plan against that shared explanation.
3. Decide the minimal metadata and lifecycle required for Plan artifacts themselves.
4. Define the candidate recursive work grammar and its workflow profiles, including construct
   recurrence, admissible relation types, promotion gates, reopening, and explicit skip policies.
5. Define the minimum interactive work-intent, Dispatch-candidate pre-registration, reminder, and
   task-run envelopes, including dispositions for work that is never launched.
6. Prepare the first-phase research proposal around kernel alternatives, candidate invariants,
   bootstrap, evolution, composition, validity, projections, and the bounded role of Lean; challenge
   every candidate invariant before allowing the ontology to harden.
7. Research and author the mathematical appendix in notation-first order, with responsibility and
   source mappings for every formal concept, an explicit Open Questions section, and subsequent
   Lean translation obligations.
8. Run the staged two-reviewer mathematical and Lean correspondence reviews, using a fresh third
   layer when two sequential layers disagree.
9. Design the future `dispatch_type: plan` skill from this bootstrap example, then separately
   decide whether to promote that router entry from RESERVED to LIVE.
10. Only after that promotion, require plan-mode subagent outputs to be saved under `plans/`.

## Open questions about the future Plan type

- Is every Plan a session, or can a stable reusable PlanDefinition produce multiple PlanSessions?
- Which fields are common to research, implementation, migration, experiment, and operational
  plans?
- Does accepting a plan authorize only dispatch proposal generation, or any execution?
- How are entry prompts, later amendments, rejected alternatives, and user decisions preserved?
- What constitutes completion, supersession, cancellation, and reopening?
- Can plans contain nested plans, and how are their budgets and authority bounded?
- Can a Research target a Plan, can a Plan target a Research, and which relation expresses purpose,
  production, challenge, revision, containment, or promotion in each case?
- Which validations must occur before a plan can be offered, accepted, scheduled, or executed?
- Are `Spec` and `Code` the only universally required work kinds, with Research, Experiment,
  Discovery, Design, Plan, and Verification selected by a user-confirmed `WorkflowProfile`?
- Should installation establish that workflow profile, its required gates, and permitted skips, or
  would installation-time confirmation make later context-specific governance too rigid?

## Recursive work grammar hypothesis

The familiar progression:

```text
Intent
  -> Plan
  -> Research
  -> Discovery / Design
  -> Spec
  -> Code
  -> Verification
```

is useful as a default explanatory path, but it must not be mistaken for one irreversible global
state machine. These names are candidate construct or activity kinds that can be instantiated at
different scopes and connected through typed relations. For example:

- a Research can `investigates` or `challenges` a Plan;
- a Plan can `requests` a Research or `organizes` several Research objects;
- a Discovery can `synthesizes` Research and `proposes` Design decisions;
- a Spec can `governs` Code while containing a local Plan for one unresolved subsystem;
- Verification can `evaluates` Code against a Spec and `reopens` Research, Discovery, or Spec.

A `WorkflowProfile` may still require a default progression and prevent unauthorized skipping.
What must be invariant is not the universal order of the construct names, but the explicitness of
the applicable profile, the identities and versions of stage instances, the typed relations among
them, the evidence and authority required by each promotion, and the historical facts recording
reopening or bypass.

This structural recursion does not relax the execution boundary. The root orchestrator may compile
a recursively structured work graph into bounded WorkPackages, but an invoked orchestrator still
must not invoke another orchestrator. Leaf agents receive materialized task-specific context,
tools, budgets, output contracts, and gates rather than the full surrounding graph or a chain of
orchestrator authority.

## Closing architectural hypothesis: invariants as a coherent composition

Candidate kernel invariants cannot be treated as an unordered checklist, and the program must not
assume that they all belong to one kernel. Whether implemented by one kernel, several specialized
kernels, or a kernel-of-kernels, the governing contracts must define a coherent admissible region
in which the rest of the system can exist, vary, and compose. Their interactions therefore need
explicit composition semantics: compatibility, dependency, precedence, conflict, scope, and the
conditions under which preserving each invariant locally is sufficient to preserve the system
globally.

This coherence also requires feedback. Runtime observations, violations, unresolved classifications,
conflicting user invariants, failed effects, and semantic drift must be able to produce signals that
drive bounded responses such as rejection, repair, reconciliation, escalation, re-evaluation, or a
proposal to revise a definition. A feedback loop does not create authority by itself and must not
silently rewrite accepted history.

The resulting hypothesis is:

\[
\text{flexible system}
=
\text{minimal interoperability contract across one or more kernels}
+
\text{coherent composition laws}
+
\text{governed feedback loops}
+
\text{configurable local invariants}.
\]

Research must test not only whether each candidate invariant is necessary, but whether the set is
jointly satisfiable, sufficiently complete to support safe composition, and closed under the
primitive transformations exposed by the system. A set that is individually plausible but produces
contradiction, deadlock, unobservable failure, or uncontrolled feedback when composed is not an
adequate kernel.

## Kernel-of-kernels hypothesis

In this plan, `kernel` means a minimal architectural contract for one bounded responsibility, not
the operating-system kernel, a mathematical kernel of a morphism, or a machine-learning similarity
function. A semantic kernel, authority kernel, temporal kernel, composition kernel, or execution
kernel may each have a different internal vocabulary while still needing to interoperate.

A possible kernel-of-kernels would not contain the union of their domain logic. It would define how
a kernel:

- identifies and versions itself;
- declares the constructs and operations it owns;
- publishes invariants and compatibility requirements;
- binds authority and provenance;
- exposes translation and composition contracts; and
- records conformance, incompatibility, supersession, and unresolved residue.

This remains a hypothesis because it can reproduce the same problem one level higher or create an
infinite regress. Research must identify a bootstrap boundary: the smallest externally admitted
contract that lets kernel agreements be checked without requiring another kernel above it.

## Interactive work-intent, Dispatch candidates, and realtime state

The system may need a realtime operational substrate in which user requests and generated Dispatch
candidates are captured before execution:

```text
conversation statement
  -> candidate WorkIntent
  -> admitted WorkIntent
  -> pre-registered DispatchCandidate / Plan / TaskDefinition
  -> confirmed Dispatch
  -> TaskRun / AgentAttempt
  -> append-only lifecycle events
  -> current-work and reminder projections
```

Pre-registering a `DispatchCandidate` means preserving its identity, origin, proposed purpose,
current proposal revision, confirmation requirement, staleness, and disposition. It does not append
an official executable Dispatch row and does not bypass confirmation. A candidate that never runs
still receives a durable fact explaining what happened: `declined`, `superseded`, `expired`,
`blocked`, `cancelled`, or `not-launched`, with reason and responsible actor when known.

Candidate lifecycle facts may include `identified`, `proposal-prepared`,
`awaiting-confirmation`, `confirmed-not-started`, `launched`, `stale`, `reminder-emitted`, and the
terminal non-launch dispositions above. Execution lifecycle facts remain separate, such as
`started`, `progress-observed`, `blocked`, `waiting-for-decision`, `completed`, `cancelled`, and
`failed`.

The interface must make pending candidates easy to see and should remind the user when one remains
actionable or when a session would otherwise end with it forgotten. Reminder policy needs
deduplication, cadence, relevance, dismissal/snooze semantics, and an escalation ceiling so
visibility does not become notification spam. A reminder is a projection and communication effect,
not a confirmation or an execution command.

Not every utterance should automatically become work or a Dispatch candidate. Open questions
include the admission threshold, confirmation requirements, idempotency across repeated
instructions, reconciliation when a proposal changes, stale-candidate detection, retention of
deliberately abandoned candidates, and whether agents may propose new work without authorizing it.

## Recursive hierarchy and relation hypothesis

The system needs a first-class representation for recursive structure rather than relying on path
names, nested JSON, prompt history, or one nullable `parent_id`. A recursive relation should be
independently identifiable and observable. Every accepted relation records at least its type,
direction, origin, destination, scope, version, provenance, cardinality, transitivity, inheritance,
and cycle policy, plus a validity interval, lifecycle, and override semantics when relevant.
Different relation types may therefore form trees, forests, DAGs, or controlled cyclic graphs
without forcing all recursive structures into one global topology.

Different relations must remain distinguishable even when they connect the same objects. For
example:

- `dispatch-B generated-by dispatch-A` records operational lineage;
- `dispatch-B authorized-by confirmation-C` records execution authority;
- `dispatch-B reviews dispatch-A` records purpose;
- `dispatch-B contained-in plan-P` records organization.

None of those relations can be inferred safely from another. In particular, being a child does not
automatically grant the parent's capabilities, authority, budget, evidence visibility, or terminal
status. A parent may explicitly materialize the context needed by one child task, within its
authority, but that is a versioned and attributable input decision rather than inheritance from
lineage.

The representation must support direct and derived questions such as roots, ancestors,
descendants, depth, generating chain, effective inherited properties, cycles, orphaned objects,
cross-hierarchy conflicts, and the exact relation path that justified a projection or action.
Derived transitive closure may be indexed for navigation, but it remains a projection over
authoritative direct relations.

Research must decide how recursive rules compose with feedback loops. A feedback edge, a child
Dispatch, and a self-referential definition can all produce recursion, but they have different
termination, authority, and consistency requirements and must not collapse into one generic
`parent-child` mechanism.

## Compositional reflexivity and derived-location hypothesis

The provisional name for the broader property is **compositional reflexivity**: the language's
constructs and typed relations can reappear at different levels and can describe or contain new
instances of the same language. This is stronger than having many configuration options and weaker
than claiming unrestricted self-reference or runtime recursion.

The property combines three separable requirements:

- **closure under composition:** valid objects can be combined into larger valid objects through
  typed relations;
- **level recurrence:** the same construct kinds can participate at system, repository, workflow,
  task, session, agent, artifact, or other declared levels without gaining a different meaning
  merely because of their level;
- **derived placement:** physical paths and folder trees are materialized views over independently
  defined properties and relations, so the same knowledge graph can support multiple useful folder,
  index, dashboard, or task-oriented projections.

This hypothesis does not imply that every object may contain every other object, that every
relation is transitive, or that cycles are always legal. Admissible composition remains governed by
relation-specific cardinality, inheritance, depth, and cycle policies. It also does not permit an
invoked orchestrator to create another orchestrator: structural self-description and recursive
object lineage must remain distinct from recursive execution authority.
