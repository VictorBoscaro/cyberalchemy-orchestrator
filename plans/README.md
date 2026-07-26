---
tags: [plans, naming, identity, authority, governance]
node_type: plans-index-and-contract
is_session: false
status: active
version: 0.6.0
last_updated: 2026-07-25
authority_basis: repository-owner-direction
schema_status: proposed
---

# Plans

This `README.md` is the only file at the root of `/plans`. It owns the repository's canonical
definition, naming rule, authority boundary, storage convention, index, and open questions for
Plans. Every other direct child of `/plans` is a directory named after a Plan's descriptive
function or objective.

Current repository structure:

```text
plans/
├── README.md
└── governed-agent-work-infrastructure/
    ├── README.md
    ├── PLAN.md
    ├── subplans/  # legacy/transitional; awaiting migration to plans/
    │   └── agent-work-language-research/
    │       ├── PLAN.md
    │       └── CANDIDATE-INVARIANTS.md
    ├── workstreams/
    │   └── brokered-agent-launcher-capability-bootstrap.md
    └── archive/
        └── knowledge-machine-and-agent-orchestrator-seed-roadmap.md
```

The current `subplans/` path is a legacy storage shape retained temporarily so existing links
remain valid. It is not the active convention. The canonical recursive shape for a child Plan is:

```text
plans/
└── <root-plan>/
    ├── PLAN.md
    └── plans/
        └── <child-plan>/
            ├── PLAN.md
            └── plans/
                └── <grandchild-plan>/
                    └── PLAN.md
```

Every directory represented by `<root-plan>`, `<child-plan>`, or `<grandchild-plan>` contains a
Plan of the same kind. Being a child is a declared relationship to another Plan, not a lesser
object type. The repeated `plans/` directory expresses that relationship recursively in storage.

## Canonical definition

### Scientific/formal voice

A `Plan` is a named, versioned, attributable proposal for a possible route from an interpreted
current state toward a desired outcome. It may organize assumptions, dependencies, questions,
alternatives, resources, phases, decision gates, stopping conditions, and candidate downstream
work.

Let \(p\) be a Plan, \(N_p\) its descriptive name, \(R_p\) its proposed route, and \(A_p\) the
result of its authority search:

\[
\operatorname{Plan}(p)
\Rightarrow
\operatorname{DescriptiveName}(N_p)
\land
\operatorname{Proposal}(R_p)
\land
\operatorname{ProvenanceKnown}(p)
\land
\operatorname{AuthoritySearched}(A_p).
\]

The Plan may initially have no assigned durable ID:

\[
\operatorname{Draft}(p)
\Rightarrow
\operatorname{NameAssigned}(N_p)
\land
\operatorname{PlanId}(p)=\varnothing.
\]

Before admission into identity-bearing relations, promotion, or operational governance, an ID is
derived from the accepted name and then frozen:

\[
\operatorname{Admit}(p)
\Rightarrow
\operatorname{PlanId}(p)=
\operatorname{UniqueSlug}(\operatorname{Normalize}(N_p)).
\]

The derivation establishes an initial correspondence; it does not make the mutable name the
identity. A later rename preserves the assigned ID and records the new name and aliases as a
versioned description.

The authority result may be resolved, absent, unknown, or contested:

\[
A_p \in
\{\operatorname{resolved}(a),\operatorname{absent},
\operatorname{unknown},\operatorname{contested}(a_1,\ldots,a_n)\}.
\]

A Plan never supplies execution authority merely by existing or being accepted:

\[
\operatorname{Plan}(p)\not\Rightarrow
\operatorname{AuthorizedToExecute}(R_p).
\]

### Plain-language voice

Name the Plan for what it is trying to accomplish before assigning it a technical ID. “Governed
Agent Work Infrastructure” tells a reader what the Plan builds; `infrastructure-program` does not.
Once the name and scope are accepted, the system can derive a stable ID from that name.

A Plan says, “given what we currently know, this is a route we could take.” It may exist before an
authority agrees to own it, but unresolved authority must remain visible and cannot silently become
approval.

### Repository-context voice

The current root Plan is
[Governed Agent Work Infrastructure](governed-agent-work-infrastructure/PLAN.md). Its agent-language
research is a child Plan because it has its own question, gates, evidence, and review lifecycle.
That child still occupies the legacy `subplans/` path pending migration; its relationship and
Plan status do not depend on that path. The brokered-launcher bootstrap remains a workstream
because it has not yet earned an independent Plan identity and its governing authority is
unresolved.

## Naming before identity

Every Plan starts with:

1. a descriptive human-readable `name`;
2. a short statement of objective and boundary;
3. a descriptive folder slug derived from the name for navigation; and
4. `plan_id: null` until the identity-assignment gate is crossed.

A good name:

- describes the capability, transformation, or outcome;
- is understandable without repository history;
- distinguishes the Plan from siblings;
- avoids generic containers such as `infrastructure`, `program`, `roadmap`, `phase`, or `plan`
  unless qualified by the actual objective; and
- does not encode transient status, implementation technology, date, or sequence unless that
  distinction is intrinsic.

Examples:

| Weak name | Descriptive name |
|---|---|
| Infrastructure | Governed Agent Work Infrastructure |
| Agent Language Program | Agent Work Language Research |
| Stage D | Brokered Agent Launcher Capability Bootstrap |

The folder slug is a locator, not yet the durable ID. When an ID is assigned, its initial base is
the normalized descriptive name, with a deterministic collision suffix when necessary. The exact
ID algorithm remains a schema decision.

The conventional leaf filename `PLAN.md` is allowed because its descriptive parent directory
supplies the object's namespace. Other artifact filenames must describe their function or subject;
generic historical filenames should be renamed while their former paths remain recoverable from
version history.

## One root Plan, recursively nested Plans and work

A coherent objective should have one root Plan. Research programs, implementation slices,
migrations, experiments, and local routes belong inside that Plan as sections, workstreams,
evidence nodes, or child Plans. A new peer root still requires an independently accepted objective
and lifecycle boundary.

Work begins as a section or workstream. The following are signals that the infrastructure should
*suggest* extracting it as a child Plan:

- its own objective and completion criteria;
- its own authority search or sponsor;
- independent versioning, gates, blocking, cancellation, reopening, or supersession;
- a separately resumable evidence and decision history; or
- enough internal structure that keeping it inline obscures the parent route.

These are not user-facing admission requirements and no fixed number of signals forces a split.
The user may deliberately keep the work inline. The infrastructure should explain the expected
cost—such as readability, independent lifecycle, or authority ambiguity—record the choice, and
continue unless a true kernel invariant would be violated.

Physical separation into another file does not create a Plan, and placement under `plans/` does
not by itself establish parentage. When extraction is accepted, the infrastructure creates a Plan
under the parent's recursive `plans/` directory, declares its parent and role, proposes its
descriptive name, derives machine fields, migrates the relevant material, and checks links and
structural invariants. The child remains a full Plan with its own lifecycle; "child" names its
relationship to the parent, not a separate or inferior object type. Governing authority may
remain explicitly unresolved.

## Minimum user burden

Governance should constrain the system more than it burdens the user. The user need only express
the intended outcome, relevant boundaries, and any decision they actually want to make. They
should not have to manufacture IDs, folder slugs, frontmatter, relationship fields, authority
records, or validation evidence.

The infrastructure is responsible for:

- proposing a descriptive name from the stated objective and asking only when ambiguity would
  materially change the Plan;
- searching for authority and recording `resolved`, `absent`, `unknown`, or `contested` without
  inventing an authority;
- recommending inline work, a workstream, or a child Plan and honoring the user's explicit structural
  preference when kernel invariants permit it;
- deriving locators and, at the identity gate, a stable `plan_id`;
- maintaining parent, child, version, provenance, gate, and supersession relations; and
- validating storage shape, links, uniqueness, and machine-checkable invariants.

The small mandatory core should therefore be expressed as infrastructure-enforced postconditions,
not as a form the user must fill out:

\[
\operatorname{StoredPlan}(p)
\Rightarrow
\operatorname{DescriptiveName}(p)
\land
\operatorname{ObjectiveKnown}(p)
\land
\operatorname{ProvenanceKnown}(p)
\land
\operatorname{AuthoritySearchRecorded}(p)
\land
\operatorname{StructureValid}(p).
\]

If the available conversation does not determine one of these fields, the infrastructure records
an explicit unknown or asks one narrow question only when no safe representation is possible.

## Authority is searched, not inferred

Every Plan searches for governing authority. Candidate evidence includes:

1. authority explicitly supplied by the originating user or accepted entry point;
2. authority declared by the target repository, project, resource, or bounded domain;
3. an accepted constitution, specification, workflow profile, decision, or delegation covering
   the scope;
4. an attributable sponsor who can accept responsibility for the proposed route; or
5. an explicit unresolved result when no sufficient authority is found.

Authorship, parentage, folder placement, generation by an agent, completeness, or age do not
automatically supply authority.

Authority questions remain distinct:

- who may draft or revise the proposal;
- who may accept the route;
- which domain authorities constrain individual steps; and
- who may authorize concrete Dispatches and effects.

A Plan with absent, unknown, or contested authority may be stored, researched, revised, compared,
offered to a sponsor, superseded, or retired. It may not be described as binding, funded,
scheduled, or executable; allocate authoritative resources; confirm a Dispatch; or cross an effect
boundary.

`Plan` is not yet the only object allowed to lack governing authority. The narrower hypothesis is
that it is the primary route-bearing object allowed to remain durable while governing authority is
unresolved.

## Current index

| Name | Path | Role | ID state | Authority state |
|---|---|---|---|---|
| Governed Agent Work Infrastructure | [PLAN.md](governed-agent-work-infrastructure/PLAN.md) | Root Plan | Named; ID pending | Resolved repository owner; proposal-only |
| Agent Work Language Research | [PLAN.md](governed-agent-work-infrastructure/subplans/agent-work-language-research/PLAN.md) | Child research Plan; legacy path pending migration to `plans/` | Named; ID pending | Resolved repository owner; proposal-only |
| Brokered Agent Launcher Capability Bootstrap | [workstream](governed-agent-work-infrastructure/workstreams/brokered-agent-launcher-capability-bootstrap.md) | Workstream, not a Plan | No Plan ID | Unknown |
| Knowledge Machine and Agent Orchestrator Seed Roadmap | [archive](governed-agent-work-infrastructure/archive/knowledge-machine-and-agent-orchestrator-seed-roadmap.md) | Archived predecessor | Historical name only | Unknown |

## Collapse tests

The model fails if:

- a generic technical label is accepted as the Plan name;
- an ID is invented before the Plan's function or objective is understood;
- renaming silently changes an already assigned durable ID;
- a workstream becomes a Plan merely because it has its own file;
- child-Plan heuristics are enforced as a compulsory split against the user's preference;
- the user is required to hand-author IDs, metadata, authority states, or structural bookkeeping;
- a child Plan appears as a peer root because its parent relation or recursive `plans/` nesting was omitted;
- a Plan under `plans/` is treated as a lesser object type merely because it has a parent;
- the legacy `subplans/` path is used for newly created child Plans;
- an agent-authored or complete-looking Plan is treated as authorized;
- unresolved authority is normalized to the author or parent;
- Plan acceptance launches work without distinct execution authority; or
- `/plans` accumulates loose files other than this `README.md`.

## Intended `dispatch_type: plan` convention

`dispatch_type: plan` remains RESERVED. A future Plan workflow should first establish the
descriptive name and boundary, then decide whether the result is a section, workstream, child Plan, or
root Plan. Only a later identity gate derives and freezes `plan_id`.

## Open Questions

- What exact admission event assigns `plan_id`?
- What normalization and collision algorithm derives the ID from the accepted name?
- When does renaming justify a new Plan rather than a new description version?
- Which postconditions of workstream-to-child-Plan promotion must be machine-checkable?
- Who may conclude `authority: absent` rather than `unknown`?
- Is Plan the only route-bearing object allowed to remain durable with unresolved authority?
