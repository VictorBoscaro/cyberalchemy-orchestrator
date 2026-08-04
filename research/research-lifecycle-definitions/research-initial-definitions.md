---
tags: [research, ontology, nodes, edges, provenance, lifecycle]
artifact_kind: research-initial-definitions
layer: project
status: draft
version: 0.2.1
created_at: 2026-07-28T02:02:50-03:00
updated_at: 2026-08-04T17:44:30-03:00
---

# Research Lifecycle Definitions — Initial Definitions

## Context

Cyberalchemy is developing governed infrastructure in which purpose, authority, context,
execution, results, and evidence remain inspectably connected. Documents, tasks, dispatches,
decisions, and other objects need stable identities and meaningful relations without forcing every
domain into one rigid hierarchy.

The immediate local problem is that the research lifecycle already produces distinct artifacts —
initial definitions, collected research, and findings — but their identities, classifications,
relations, field producers, valid values, and lifecycle transitions are not governed by one
minimal contract. Resolving that boundary matters because research artifacts are a bounded,
repeated case in which the repository can test node registration and edge semantics before
extending them to task-to-task, document-to-document, and task-to-document context.

## Purpose

This document establishes the informational baseline for research into the smallest useful
node-and-relation contract for research lifecycle artifacts. The resulting evidence will inform a
later discovery or design decision about research artifact registration, frontmatter, relation
representation, generation responsibility, validation, and compatibility with broader work-context
modeling.

## Research Question (Can be refined)

What is the smallest auditable and extensible contract that lets the repository register research
lifecycle artifacts as nodes, explain how every field is generated and validated, and relate
initial definitions, research records, findings, and their surrounding context without storing
redundant or manufactured information?

## Confirmed Product Constraints

Each constraint below is owner-confirmed or carried by the linked governing artifact; the research
must not silently strengthen it.

- A registered node must have at least one identifiable process that generates it.
  ([Artifact Schema and Context Edges](../../sessions/2026-07-27-1253-artifact-schema-and-context-edges.md))
- Registered nodes should carry meaningful edges when supported; an edge must not be invented
  merely to avoid an isolated node.
  ([Frontmatter & Connections](../../.claude/skills/custom/frontmatter.md))
- The target should be minimal enough to apply across situations rather than becoming a special
  schema that works only for one research folder.
  ([Prompt, Tags and Graph Research Scope](../../sessions/2026-07-25-2159-prompt-tags-and-graph-research-scope.md))
- `node_type` and `artifact_kind` are not separate dimensions. The canonical field name for the
  kind of a registered node is `artifact_kind`; this initial artifact therefore declares
  `artifact_kind: research-initial-definitions`.
  ([Artifact Schema and Context Edges](../../sessions/2026-07-27-1253-artifact-schema-and-context-edges.md))
- The producer, source, timing, allowed values, validation rule, authority, and mutability of each
  retained field must be understandable.
  ([Artifact Schema and Context Edges](../../sessions/2026-07-27-1253-artifact-schema-and-context-edges.md))
- The first bounded case is the research lifecycle. Connecting micro tasks to macro context is a
  subsequent problem that should consume, test, or extend the first result rather than silently
  replace it.
  ([Artifact Schema and Context Edges](../../sessions/2026-07-27-1253-artifact-schema-and-context-edges.md))
- Frontmatter tags remain topical labels; they must not silently encode epistemic role, maturity,
  authority, hierarchy, or relation semantics.
  ([Frontmatter & Connections](../../.claude/skills/custom/frontmatter.md))
- Existing project hooks, dispatch confirmation, append-only telemetry, source-integrity controls,
  and claim-not-greater-than-proof discipline must not be weakened.
  ([Repository agent policy](../../AGENTS.md))
- Candidate research evidence may be stored under this research folder, but it is not canonical
  ontology or runtime authority merely because it has been recorded.
  ([Evidence workspace](evidence/README.md))

## Current Evidence Baseline

- `vault/ontology-conventions.md` defines seven frontmatter dimensions and a fourteen-value
  document-edge catalog expressed through a human-readable `Connections` section.
- A repository-wide filename scan on 2026-08-04 using `rg --files` with the exact include names
  `research-initial-definitions.md`, `research.md`, and `findings.md` found inconsistent structural
  adoption: respectively 14/10/5, 13/3/4, and 19/5/5 for total files/files beginning with
  frontmatter/files containing an exact `## Connections` heading. These are a dated corpus
  observation, not a stable invariant.
- Existing research artifacts already use values outside the current catalog, including
  `node_type: research-initial-definitions`, `status: proposed`, `related_plan`, and `stream_id`.
  Their presence is evidence of an unsettled contract, not evidence that those fields are valid or
  invalid.
- The governed research workflow distinguishes informational initial definitions, collected
  returns in `research.md`, and synthesized `findings.md`, but does not itself define a universal
  node schema for those artifacts.
- Artifact-specific writing references already prescribe reciprocal `Connections` for
  `research.md` and `findings.md`, but the root `research` skill does not route to those references
  and their `derives` relation no longer belongs to the current frontmatter guide's starting
  vocabulary. This is evidence of contract fragmentation and vocabulary drift, not an accepted
  relation model.
- The governed-Markdown hook recognizes only structural presence of frontmatter and a
  `## Connections` heading. It does not select an artifact schema, populate fields or relations,
  resolve targets, or block acceptance of a nonconforming output.
- The current protocol compiler represents profile outputs through `output_id`, scalar
  `content_schema`, and `required`; it does not bind an output to a Markdown artifact kind, path
  template, field producer, or relation rule. `DispatchSpec.schema_refs` and the effective-input
  materialization boundary are existing integration seams whose suitability remains to be tested.
- Canonical Vault Reads already specifies non-mutating projections of frontmatter, raw connection
  declarations, and logical edges, including inverse folding for `derives-from` and `grounds`, but
  its blocked staged delivery plan is not an authoring or output-acceptance authority.
- The sibling repository `../domainspec-core` contains `CANONICAL-KINDS.md`,
  `ALLOWED-EDGES.yaml`, `EDGES.yaml`, related sessions, and an authority review concerning
  canonical kinds. Their relevance to this repository has not yet been evaluated.

## Known Gaps

- The identity boundary among a research topic, a research run, a document, and a document version
  is not settled.
- The valid `artifact_kind` vocabulary, per-kind required fields, generation processes, and
  compatibility rules remain unsettled.
- There is no accepted rule for which fields are authored by a human, proposed by an agent,
  generated by a tool, derived from Git or runtime history, or accepted by a governance gate.
- The canonical representation and direction of relations are unsettled, including whether inverse
  edges are persisted or derived.
- There is no accepted compatibility matrix for source node kind, edge kind, and target node kind.
- The current edge catalog does not express evidence, assertion authority, currentness,
  contestation, or supersession uniformly.
- It is unknown which parts of `domainspec-core`'s canonical-kind model are reusable, already
  deployed, context-specific, or incompatible with this repository's requirements.
- The boundary between universal node/edge envelope fields and kind-specific payload fields is not
  settled.

## Connections

| Document | Type | Description |
|---|---|---|
| [`vault/ontology-conventions.md`](../../vault/ontology-conventions.md) | `derives-from` | Supplies the current frontmatter dimensions and document-edge vocabulary that motivate this research. |
| [`plans/governed-agent-work-infrastructure/PLAN.md`](../../plans/governed-agent-work-infrastructure/PLAN.md) | `derives-from` | Supplies the broader objective of keeping governed agent work and its provenance inspectably connected. |
| [`domainspec-core/CANONICAL-KINDS.md`](../../../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md) | `contextualizes` | Identified sibling-repository evidence whose applicability remains to be established by the research. |
| [Research Lifecycle Definitions — Evidence Workspace](evidence/README.md) | `grounds` | This initial scope governs the evidence index and its separation from accepted findings. |
| [Current authoring contracts and ACI integration seams](evidence/current-authoring-and-aci-seams.md) | `grounds` | This initial scope grounds the bounded evidence record that separates observed repository behavior from the owner-proposed direction. |
| [Artifact Contract Evidence and Review session](../../sessions/2026-08-04-1744-artifact-contract-evidence-and-review.md) | `contains` | This research context contains the session that added and independently reviewed the current authoring-contract evidence. |
