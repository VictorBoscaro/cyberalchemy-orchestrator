---
tags: [schema-governance, artifact-modeling, knowledge-representation]
artifact_kind: readme
layer: project
version: 0.1.0
updated_at: 2026-08-17T14:02:26-03:00
---

# Schema Service

Status: bootstrap.

This README describes the intended boundary of Schema Service; it does not claim that the service
is implemented. The project will provide shared machinery for governing reusable artifact types,
their schema definitions, and concrete artifacts such as documents, folders, skills, tools,
research results, and, where useful, code artifacts.

## Intent

Schema is used here in a general structural sense, not only as a database schema. A **type** is a
reusable semantic distinction, such as a kind of artifact or another governed concept. An immutable
**schema-definition revision** expresses a contract for a type: the information instances may
carry, the relations they may form, and optional invariants, path constraints, or composition laws.
A schema revision is not the type itself, and a concrete artifact does not receive its own schema
merely by existing.

The service is intended to make repository artifacts identifiable, discoverable, interpretable by
agents and humans, and progressively governable. Every artifact admitted to a governed boundary
receives a stable identity and a manifest revision that references a resolvable, revision-exact
schema — specific or fallback. More specific types and schemas may be introduced over time, but
their absence must not prevent a useful artifact from existing.

An artifact is the durable governed subject, not necessarily one file or path. Structured manifest
data, human-readable documents, files, directories, and other carriers may represent or describe
that artifact. The exact physical arrangement — embedded metadata, sidecar, registry record, or
another form — remains open.

## Design principles

- **Low-cost admission.** Creating or discovering an artifact should automatically produce its
  minimum manifest and observation. Users must not repeat information already known by the
  producing skill, tool, parent context, or repository.
- **Progressive formalization.** A candidate schema may begin with only a type name, a base type, and
  an objective. Properties, relations, constraints, and composition laws are optional refinements.
- **Open-world extension.** Base schemas do not enumerate every future type or subtype. The registry
  derives the known type and refinement graph from independently published schema definitions.
- **Total, non-exhaustive classification.** Every governed artifact can use the fallback schema of
  its nearest known family when no specific category applies. A fallback keeps the artifact valid
  and governable without pretending that the registry enumerates every category users may need.
- **Domain ownership.** The service owns common schema machinery and the universal minimum. Domain
  owners define what makes a research document, folder, skill, or other category meaningful.
- **Evidence before obligation.** Repeated structure may justify a proposed refinement, but observed
  coincidence must not silently become a normative rule.
- **Explicit authority.** Open tags and inferred classifications may aid discovery, but they must not
  control behavior unless promoted into an owned schema rule.
- **Separate semantic identity from revision identity.** A type is the reusable distinction; a
  revision-exact `SchemaId` identifies one immutable normative expression of it. The exact stable
  identity contract for `Type` remains an open design question.
- **Immutable revisions.** Publishing a new schema revision never changes what an existing
  `SchemaId` means.
- **Representation is not identity.** Path, format, and digest describe representations or
  observations; they are not sufficient as enduring artifact identity.

## Conceptual layers

```text
Domain
    -> defines or governs Type
        -> is expressed by SchemaDefinitionRevision

MetaSchema
    -> validates SchemaDefinitionRevision
        -> resolves an EffectiveSchema

Artifact
    -> is described by ManifestRevision
        -> references SchemaDefinitionRevision or fallback
    -> is made accessible by Representation
        -> is observed as RepresentationSnapshot

EffectiveSchema + ManifestRevision + RepresentationSnapshot
    -> produces ValidationReport
        -> is interpreted by EnforcementProfile
```

These are logical roles. They do not require separate files, tables, or runtime services during
bootstrap.

### Domain and type

A domain is currently understood as a boundary of meaning and governance: it determines which
distinctions, relations, rules, owners, and validation concerns belong together for some purpose.
Domains may overlap. A type may participate in more than one domain, although the mechanism for
multiple typing, imported capabilities, and ownership conflicts remains open.

A type has semantic identity across time. A schema-definition revision is an immutable contract
that expresses that type at one point in its evolution. This distinction permits the system to say
that two schema revisions concern the same reusable type without pretending that the revisions have
the same guarantees. Whether `TypeId` is serialized separately or derived from another stable
identity source is not yet decided.

`DomainPackage` is not a kernel primitive at bootstrap. It may later become a versioned unit for
publishing or importing type, property, relation, and rule definitions if evidence demonstrates an
independent owner, lifecycle, or interface.

### MetaSchema

The metaschema is the schema of schema-definition revisions. It defines how a revision declares the
type it expresses, its own identity, objective, bases, properties, relations, constraints,
composition laws, and expressivity. It also gives agents enough meaning and filling guidance to
determine whether a value should be derived, inherited, observed, generated, or explicitly
declared.

The metaschema does not define what research or folders mean. It defines the language in which the
owners of those domains publish their schemas. It is a versioned part of the service kernel and the
bootstrap root of the schema system.

### Schema-definition revision

A schema-definition revision is an instance of the metaschema. A minimal candidate can name its
reusable distinction with only a stable type identity, a revision-exact schema identity, a base,
and an objective:

```yaml
id: document/lab-note@0
type: document/lab-note
name: Lab note
extends: document/base@0
objective: Capture observations produced during an experiment.
```

The exact serialization of the separate type and schema-revision identities remains open. Later
revisions may add properties, relations, constraints, or composition laws. A refinement may add or
strengthen guarantees from its base schemas; it must not silently remove them. The registry, rather
than `document/base`, answers which document types and subtypes currently exist.

Publishing is an authorized registry operation, not merely writing a definition file. The
publication record must identify the owning domain, the publishing authority, the immutable
definition revision, and its lifecycle state. Open-world extension permits independently published
subtypes; it does not permit an unowned definition to acquire normative authority.

Creating a descriptive label, authoring a candidate definition, publishing a normative schema, and
activating enforcement are distinct acts. The exact `candidate` or `draft` lifecycle is not yet
defined, including whether an artifact may reference a non-published schema for local validation.

### Effective schema

The effective schema is the resolved closure of a definition and its bases or reusable
capabilities. It is a derived validation surface, not another independently authored source of
truth. Resolution must detect cycles, incompatible definitions, and attempts to weaken inherited
guarantees.

During bootstrap, weakening detection is guaranteed only for a deliberately monotonic constraint
core: refinements conjoin constraints and cannot override or delete inherited ones. Multiple
inheritance, reusable capabilities with conflicts, and richer constraint languages require their
own explicit compatibility semantics before the resolver may claim to decide weakening.

### Fallback classification

An admitted artifact must always carry a resolvable schema reference, but it does not need to match
a specific domain type. A governed family may publish an explicit fallback such as
`document/other@0`; the universal `artifact/other@0` remains available when even a more specific
family is not known. Which families require their own fallback remains open.

For example, a Markdown document that is neither a discovery, research report, nor specification
can remain governed without inventing a new normative type:

```yaml
id: artifact/design-memo
schema: document/other@0

values:
  classification_label: design-memo
```

`other` is a valid, intentionally broad classification. It is not equivalent to a missing or
unresolvable `schema`, which is a conformance error. A free-form `classification_label` and open
tags may preserve the user's vocabulary for discovery, but they confer no validation or behavioral
authority. The user may select `other` even when specific categories exist.

Repeated labels or structures may supply evidence for proposing a new owned schema. They never
publish one automatically. Reclassifying an artifact later creates a new manifest observation or
revision while preserving the artifact identity and earlier classification provenance; it does not
rewrite the artifact or mutate either `SchemaId`.

The intended novelty path is:

```text
fallback + descriptive classification
    -> candidate type/schema definition
        -> authorized publication
            -> new manifest revision referencing the published schema
```

Only the first step is required for admission. The later steps introduce reusable meaning and
normative authority; they must not be forced merely because an artifact is locally unusual.

### Instance and manifest revision

An instance is a concrete artifact considered under a type contract. A manifest revision records
the schema-dependent property and relation assertions made about that artifact at a particular
point. For example:

```yaml
id: artifact/schema-service-research
schema: document/research@0
objective_ref: objective/design-schema-service

values:
  research_question: How should repository schemas mature over time?

relations:
  uses:
    - reference/spivak-functorial-data-migration
```

The schema-definition revision says what may or must be present; the manifest revision supplies the
property values and relation targets for the concrete instance. Property and relation definitions
are intensional; the values and links in a manifest are extensional assertions. The manifest
remains logically distinct from the artifact itself, although it may share a serialization with a
representation and some values may be projections derived from artifact content.

An authored manifest revision and a new system observation are not necessarily the same event. An
inference must preserve its provenance and must not silently appear as a declaration made by the
artifact's author. The exact temporal model for observations, authorial revisions, reclassification,
and reconciliation remains open.

Relations and reclassification require stable artifact identity independent of location. That
identity is a semantic requirement; whether it is serialized as `id` or derived from another stable
identity source remains a conformance question. Path and content digest identify an observation or
revision, not the enduring artifact by themselves.

### Artifact

The artifact is the durable governed subject. A document, folder, skill, tool, code unit, or other
repository object may be an artifact in its own right, a representation of another artifact, or
both through explicit identities and relations. Path, digest, and carrier format are insufficient
as the artifact's enduring identity.

Schema definitions are themselves artifacts: they have identity, objective, provenance, and
immutable revisions, and they conform to the metaschema. This does not require an infinite tower;
the metaschema is the explicitly governed bootstrap foundation.

### Representation and snapshot

A representation makes an artifact accessible in some form, such as a human-readable document,
structured record, file, directory, skill package, or tool descriptor. A representation snapshot
records an observed state of that representation with the provenance necessary to scope later
validation. The snapshot mechanism may differ by artifact family; a path and content digest are not
a sufficient universal model for folders, remote tools, compound skills, or multiple synchronized
representations.

Manifest and representation are logical roles, not mandatory separate files. Front matter,
sidecars, registry records, and generated views remain candidate serializations. When the same datum
appears in structured and narrative forms, the system must know which occurrence is authored,
derived, inherited, observed, or generated. It cannot guarantee semantic agreement mechanically in
general; canonicality, provenance, and reconciliation must be explicit.

## Progressive schema expressivity

A schema can stop at any useful level of structural expressivity:

```text
observed/fallback -> classified -> structured -> relational -> path-constrained -> compositional
```

- **Observed/fallback:** the artifact exists under `artifact/other` or the fallback of its nearest
  known family.
- **Classified:** it has a more specific, owned category schema.
- **Structured:** the schema defines category-specific properties.
- **Relational:** it defines possible relations to other typed objects.
- **Path-constrained:** it defines invariants that inspect paths or reachability without claiming a
  semantic composition operation.
- **Compositional:** a domain defines an operation over composable relations plus the identities,
  laws, or path equations that make the operation meaningful.

This sequence is not a universal maturity scale. Expressivity, evidential confidence, publication
authority, instance conformance, and enforcement strength are independent dimensions. Validation
produces findings against an immutable schema revision; a separately versioned enforcement profile
owned by the governing operation decides whether a finding is advice, a warning, an obligation, or
a blocking violation. Changing that operational decision does not require publishing a new schema
revision.

## Relations, path constraints, and composition

Mature schemas may declare relations when the domain benefits from them. Examples include:

```text
ResearchDocument -> uses        -> Reference
ResearchDocument -> produces    -> Finding
Finding          -> supportedBy -> Evidence
Folder           -> contains    -> Artifact
SkillInvocation  -> produces    -> Artifact
Artifact         -> serves      -> Objective
```

Path constraints may express requirements such as "an accepted finding must reach supporting
evidence" or "a research folder must contain an initial definition." They do not by themselves
establish categorical composition. Composition is present only when the owning domain defines an
operation over composable relations and the laws or equations that a consumer observes. Neither
path constraints nor composition are required for a schema to exist. Relations with multiplicity,
recursion, or many-to-many structure may require explicit relation objects or a richer constraint
language; the exact representation remains an open design question.

Folder schemas govern both folder metadata and allowed or required relations to their contents.
They constrain contained artifacts without taking ownership of those artifacts' category schemas.

## Artifact producers

Humans, skills, and tools are first-class artifact producers. A skill may declare an expected output
schema:

```yaml
produces:
  schema: document/research@0
```

When an invocation creates an artifact, the creation event should carry the producer, invocation,
objective, and declared output schema already known to the runtime. Schema Service then enrolls the
artifact, creates its minimum manifest and observation, applies the declared schema, and validates
the observed representation. If no specific output schema is known or chosen, the producer uses a
resolvable fallback rather than inventing a schema or leaving the reference empty. An inferred
classification remains an attributed observation or proposal until an authorized operation adopts
it. The user should be asked only for information that cannot be derived, inherited, observed, or
generated.

A producer may propose a new schema or refinement after encountering a reusable distinction.
Repeated structure can support that proposal, but it is not required when a genuinely new type has
a distinct contract and owner. The producer must not silently publish a normative schema without
the owning domain's decision. Likewise, only the owner of a governed operation may strengthen its
enforcement profile.

## Candidate minimum manifest envelope

The exact universal serialization remains to be demonstrated through conformance cases. Current
semantic requirements and field candidates are:

| element | bootstrap status | note |
|---|---|---|
| resolvable, revision-exact `schema` | required | a specific or fallback schema is valid; an unknown reference is not |
| stable artifact identity | required capability | the `id` field is required only when no trusted source can derive it |
| `objective_ref` | candidate | admit only if a consumer cannot reliably inherit or derive it |
| `tags` | optional | open discovery vocabulary without behavioral authority |
| `classification_label` | optional | descriptive vocabulary for fallback instances only |
| representation reference, digest, producer, observation time | derived candidates | provenance of an observation, not user-authored minimum fields |

The objective of a schema revision and the objective of an artifact instance are different. A
schema revision's objective explains why the type contract and its distinctions exist. An
instance's objective explains why the concrete artifact exists or which larger objective it serves.
Instance objectives should be inherited or referenced where possible rather than duplicated as
stale prose.

Open tags and fallback labels are discovery surfaces, not behavioral authority.

The minimum is a semantic contract, not yet a frozen field list. In particular, the system still
needs a rule for the canonical source and acquisition mode of each property or relation when
manifest, representation, producer context, and inherited project context disagree.

## Validation, obligations, and reconciliation

The operating lifecycle is broader than one validation call:

```text
create or discover artifact
    -> establish or resolve durable identity
        -> create minimum manifest revision
            -> apply a specific or fallback classification
                -> observe a representation snapshot
                    -> validate manifest + snapshot
                        -> interpret the report under an enforcement profile
                            -> observe change and re-evaluate when required
```

Structural freshness, such as path, digest, or declared-schema conformance, may be checked
automatically. Semantic freshness, such as whether an objective still describes reality, cannot be
proven mechanically in general. Validation reports must identify the artifact, observed revision or
digest, exact `SchemaId`, and validator version so their scope is not mistaken for current truth.
Suspected semantic staleness is a finding for an enforcement profile to interpret, not proof that
the artifact is incorrect.

## Boundary

Schema Service will own:

- the metaschema, universal fallback artifact schema, and generic minimum-manifest semantics;
- stable type identity, revision-exact `SchemaId`, authorized immutable revision publication,
  registry, and resolution, once their exact identity contract is defined;
- refinement and reusable-capability relationships between schemas;
- effective-schema calculation and generic validation;
- the generic manifest-revision envelope and immutable validation-report format.

Domain owners will own category semantics, schemas, and domain-specific validators. For example, a
document domain may publish `document/research`, while a folder domain may publish
`folder/project`. Schema Service registers and applies those contracts without redefining them.

The runtime or operation governing an artifact will own admission boundaries, the source of stable
artifact identity, enforcement profiles, obligation creation, and when reconciliation runs. Shared
enrollment, inventory, provenance, or reconciliation implementations may later belong under this
project, but only after conformance cases demonstrate common rather than domain-specific mechanics.
Artifact-family owners will also own observation and snapshot mechanics that cannot be made generic
without erasing meaningful differences between files, folders, compound packages, and remote tools.

These responsibilities remain conceptual boundaries during bootstrap. They must not become runtime
services or internal subdirectories until implementation evidence demonstrates separate ownership,
lifecycle, or interface needs.

## Candidate project-local ledger

Schema Service is accumulating decisions, assumptions, open questions, evidence, and superseded
models across its README, research, sessions, and Robot-Talks. A project-local append-only knowledge
ledger may be useful as a compact index of that evolution and as an early governed artifact for the
service to dogfood.

Such a ledger must not duplicate the global subagent-dispatch ledger, runtime telemetry, the schema
registry, or the full content of research reports. Its candidate responsibility would be to assign
stable identifiers to project-local decisions, assumptions, open questions, and evidence links;
record status and authority; and preserve `supersedes` or resolution relationships. No ledger is
created yet because its owner, entry schema, append authority, and relationship to canonical source
documents remain open.

## Experiment program

The current bootstrap is being exercised through the
[`artifact-types-v0` experimentation plan](experimentation-plans/artifact-types-v0/experimentation-plan.md).
It sequences three gated experiments — `analysis`, skill, then folder — and prepares only the first
one. Candidate definitions in that package are experiment-local and non-normative; they do not
constitute a registry or implementation of this service.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Schema Service artifact model session](../../sessions/2026-08-17-1400-schema-service-artifact-model.md) | `contains` | This project context contains the session that established the current bootstrap artifact model and open questions. |

## Open questions

The following questions are intentionally unresolved. They are part of the bootstrap boundary, not
implicit implementation decisions.

### Identity, domains, and typing

- What stable identity does a `Type` retain across schema-definition revisions, and how is it
  serialized or derived?
- Is a domain primarily a semantic boundary, an authority boundary, or both?
- Can one artifact instantiate several types or participate in several domains simultaneously, or
  does it have one primary schema plus reusable capabilities or profiles?
- What distinguishes subtype, substitutability, monotonic refinement, imported capability, and
  descriptive classification?
- When does a versioned `DomainPackage` become justified as an artifact with independent ownership
  and lifecycle?

### Admission and schema lifecycle

- What exact fields belong to the universal minimum manifest envelope?
- Which governed families require their own `other` schema beyond `artifact/other`, and which
  information may a fallback preserve without becoming normative?
- Which repository objects are governed artifacts, and which generated, vendored, cached, or
  internal objects are excluded or represented only through derived records?
- What stable identity source survives movement, duplication, and content revision for each
  artifact family?
- What states, permissions, and validation behavior distinguish a descriptive label, schema
  candidate or draft, published schema, deprecated schema, and active enforcement?
- What evidence or conformance gate justifies promoting a candidate without requiring multiple
  instances or blocking a genuinely new reusable distinction?
- How are instances reclassified or migrated without mutating earlier manifest and schema meaning?

### Manifest, representation, and canonicality

- When is a file, folder, skill, or tool the governed artifact, a representation of another
  artifact, or both through explicit identities and relations?
- Is a manifest embedded, stored as a sidecar, held in a registry, or projected through more than
  one of these forms, and how is atomicity preserved?
- What is the canonical source of each datum when structured fields, human narrative, producer
  context, and inference disagree?
- How are authored manifest revisions distinguished from system observations and inferred
  classifications?
- What constitutes a representation snapshot for folders, compound skills, remote tools, or an
  artifact with multiple representations?
- When should an embedded property become a locally identified value or an independently governed
  related artifact?

### Relations, rules, and composition

- How are relation identity, multiplicity, recursion, n-ary structure, and many-to-many relations
  represented?
- Which path constraints can generic validation express without claiming semantic composition?
- Which domains have an observable composition operation, identities, and laws, and which constraint
  language should express them?
- Which changes are monotonic refinements, and how are corrections, supersession, and incompatible
  knowledge evolution represented without rewriting history?

### Operations and project memory

- What contract carries identity, producer, provenance, objective, and output-schema information
  from skills, tools, runtimes, and human creation flows?
- Which changes can be reconciled automatically, and which create semantic review obligations?
- How are enforcement profiles selected for each governed operation?
- Should Schema Service create a project-local knowledge ledger, and if so, what are its entry
  schema, append authority, canonical sources, and non-overlap with research, sessions, telemetry,
  and the schema registry?
