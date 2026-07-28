---
tags: [research, ontology, nodes, edges, provenance, lifecycle]
artifact_kind: research-initial-definitions
is_session: false
layer: ontology, architecture
nature: explanatory
status: draft
version: 0.1.0
last_updated: 2026-07-27
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

- A registered node must have at least one identifiable process that generates it.
- Registered nodes should carry meaningful edges when supported; an edge must not be invented
  merely to avoid an isolated node.
- The target should be minimal enough to apply across situations rather than becoming a special
  schema that works only for one research folder.
- `node_type` and `artifact_kind` are not separate dimensions. The canonical field name for the
  kind of a registered node is `artifact_kind`; this initial artifact therefore declares
  `artifact_kind: research-initial-definitions`.
- The producer, source, timing, allowed values, validation rule, authority, and mutability of each
  retained field must be understandable.
- The first bounded case is the research lifecycle. Connecting micro tasks to macro context is a
  subsequent problem that should consume, test, or extend the first result rather than silently
  replace it.
- Frontmatter tags remain topical labels; they must not silently encode epistemic role, maturity,
  authority, hierarchy, or relation semantics.
- Existing project hooks, dispatch confirmation, append-only telemetry, source-integrity controls,
  and claim-not-greater-than-proof discipline must not be weakened.
- Candidate research evidence may be stored under this research folder, but it is not canonical
  ontology or runtime authority merely because it has been recorded.

## Current Evidence Baseline

- `vault/ontology-conventions.md` defines seven frontmatter dimensions and a fourteen-value
  document-edge catalog expressed through a human-readable `Connections` section.
- The current repository corpus is inconsistent: seven `research-initial-definitions.md` artifacts
  include four with frontmatter and none with a `Connections` section; ten `research.md` artifacts
  include two with frontmatter and two with connections; sixteen `findings.md` artifacts include
  four with frontmatter and three with connections.
- Existing research artifacts already use values outside the current catalog, including
  `node_type: research-initial-definitions`, `status: proposed`, `related_plan`, and `stream_id`.
  Their presence is evidence of an unsettled contract, not evidence that those fields are valid or
  invalid.
- The governed research workflow distinguishes informational initial definitions, collected
  returns in `research.md`, and synthesized `findings.md`, but does not itself define a universal
  node schema for those artifacts.
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
