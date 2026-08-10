---
description: Minimal, self-contained guide for authoring the frontmatter and typed Connections of governed Markdown documents in this repository.
---

# Frontmatter & Connections

This provisional guide is the compact authoring reference for governed Markdown. It keeps the
schema intentionally soft: use the starting vocabularies when they fit, and use the documented
fallback only after they do not. The creating agent chooses and writes the metadata and
connections; hooks must not invent values or targets.

The governed-Markdown `PostToolUse` hook only reminds the creating agent to apply this guide. It
does not populate frontmatter or select tags. Activation telemetry produced by `emit-topic-tags`
is a separate observational record and must not be copied into document frontmatter automatically.

## Structural obligations

Every `.md` must carry:

1. a YAML frontmatter block (`---` ... `---`); and
2. a `## Connections` section containing meaningful typed edges, or a one-line explanation
   when no real connection is known.

Excluded from this gate: `.claude/`, `node_modules/`, and any `templates/` directory.

## Starting vocabularies and fallbacks

The vocabularies below are starting sets, not closed enums. Prefer a listed value whenever it
fits. A new specific value may be proposed when it adds a distinction that existing values
cannot express.

Fallbacks are valid values, not automatic defaults:

- use `artifact_kind: others` only after no listed artifact kind fits;
- use the edge type `other` only when a real source-target relationship exists and no listed
  edge type fits.

Never fabricate a connection target merely to satisfy the structural obligation.

## Frontmatter schema

Use fields only where they apply. `artifact_kind` is the single document-kind discriminator;
do not use `node_type`, and do not repurpose a subsystem-specific `artifact_type`.

```yaml
---
tags: [topical labels only]
artifact_kind: axiom | premise | constitution | discovery | research-initial-definitions | plan | research | findings | research-evidence | implementation-plan | spec | audit | conceptual | essay | backlog | readme | session | others
layer: project | domain | capability | feature | task | others
version: 0.x.x
created_at: YYYY-MM-DDTHH:MM:SS±HH:MM
updated_at: YYYY-MM-DDTHH:MM:SS±HH:MM
---
```

### `artifact_kind` picker

Choose the kind by asking what contract the document presents to its reader.

| `artifact_kind` | Reader contract |
|---|---|
| `axiom` | Foundational commitment; revisiting it affects everything built on it. |
| `premise` | Revisable belief that should change when evidence changes. |
| `constitution` | Governed rules changed through an explicit governance process. |
| `discovery` | Exploration of a problem space, constraints, and candidate directions. |
| `research-initial-definitions` | Scope, questions, terms, and evidence rules established before research begins. |
| `plan` | A plan for a feature, a project, research, or any other bounded undertaking. Plans can be contained inside other plans. |
| `research` | Investigation and synthesis performed against research questions. |
| `findings` | Distilled claims, conclusions, and implications produced by research or review. |
| `research-evidence` | Source-grounded observation retained as evidence for later synthesis. |
| `implementation-plan` | Ordered implementation intent that can be executed or revised. |
| `spec` | Normative behavioral or structural contract an implementation must satisfy. |
| `audit` | Time-bound assessment whose conclusions can be checked again. |
| `conceptual` | Explanatory model or context that can be enriched or corrected. |
| `essay` | Committed argument whose reasoning should be engaged or countered. |
| `backlog` | Candidate work to prioritize, schedule, or close. |
| `readme` | Orientation to the contents and use of a directory or package. |
| `session` | Durable record of one bounded work or conversation session. |
| `others` | Valid fallback after none of the listed document contracts fits. Explain the intended contract in the document. |

### `layer`: primary contextual altitude

`layer` answers one question:

> At which contextual altitude does this artifact primarily operate?

Choose exactly one primary layer:

| `layer` | Meaning |
|---|---|
| `project` | Shapes the project as a whole: its mission, system-wide policy, or overall direction. |
| `domain` | Shapes one bounded problem or knowledge domain within the project. |
| `capability` | Shapes a reusable ability the system or team must provide across one or more features. |
| `feature` | Shapes a user- or system-visible outcome delivered through related work. |
| `task` | Shapes one bounded unit of execution or its immediate result. |
| `others` | Valid fallback after none of the listed contextual altitudes fits; explain the altitude in the document. |

Use the highest level whose decisions the document directly shapes, not every level it may
eventually affect. The field is singular so it remains useful for navigating macro-to-micro
context. Broader or narrower relationships belong in `## Connections`.

Topic, concern, and origin are different dimensions. Values such as `ontology` and
`architecture` describe subject matter or concern and belong in tags; `external` describes
origin and is not a layer.

### Other fields

- `tags` describe subject matter only, never document role or maturity. Use concrete topical
  labels.
- `version`, `created_at`, `updated_at`, and `private` provide lifecycle and publication metadata
  where the owning workflow needs them.

### Lifecycle timestamps

For a newly created governed Markdown document, include both `created_at` and `updated_at`. Produce
them as RFC 3339 timestamps in the `America/Sao_Paulo` civil timezone, with the UTC offset effective
at that instant written explicitly, for example `2026-07-27T15:26:46-03:00`.

- Set `created_at` when the artifact is first durably created and never change it.
- Set `updated_at` to the time of the latest durable content or applicable metadata revision.
  Reading, indexing, validating, or copying an unchanged artifact must not advance it.
- On a substantive update to a legacy document, replace `last_updated` with `updated_at`. Add
  `created_at` only from trustworthy repository or runtime evidence of the original creation; do
  not infer it from a filename or fabricate it. If no trustworthy evidence exists, leave the
  missing creation timestamp explicit for later migration rather than recording a false instant.

## `## Connections`: typed edges

```markdown
## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[other-doc]] | `derives-from` | One-line explanation of the actual relationship. |
```

Every row needs a real target, a type, and a description explaining why the edge exists. Link
with `[[slug]]` for a vault node or with a Markdown path. When the target is governed and the
relationship has a meaningful inverse, add the inverse row there as part of the same change.

The following edge types are the starting vocabulary:

| Type (A → B) | Meaning |
|---|---|
| `resolves` | A solves the problem B states. |
| `derives-from` | A was built upon or generated from B. |
| `grounds` | A is the foundation B rests on; inverse of `derives-from`. |
| `implements` | A concretely realizes specification or constitution B. |
| `validates` | A provides evidence that supports B. |
| `promotes-from` | A ratifies or formalizes the thesis stated in B. |
| `exemplifies` | A is a concrete instance of abstract B. |
| `refines` | A adds detail or precision to B while retaining its subject. |
| `contextualizes` | A supplies useful background for B without creating a functional dependency. |
| `depends-on` | A cannot function or remain valid without B. |
| `is-part-of` | A belongs structurally to the real context represented by B. |
| `contains` | A structurally contains B; inverse of `is-part-of`. |
| `alternative-to` | A is a competing or discarded alternative to B. |
| `contradicts` | A is materially in tension with or refutes B. |
| `supersedes` | A directly succeeds B and makes it obsolete. |
| `deprecates` | A partially or informally replaces B. |
| `other` | A real relationship exists, but none of the listed edge types fits; the description must name the missing semantics. |

`is-part-of` and `contains` require real context targets. Do not infer either edge only from
directory structure or from files read, mentioned, or touched. Their inverse relationship is
documented for authoring, but transitivity, composition, and acyclicity are not yet enforced.

If no real connection is known, keep the section and state that explicitly instead of creating
a placeholder edge. A future review may validate metadata and reciprocal edges; no automatic
review is required at this stage.
