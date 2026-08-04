---
tags: [docs, discovery, index, orchestration-runtime, knowledge-bus]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.2.0
last_updated: 2026-08-04
---

# docs/discovery

## 1. What is this?

Repository-wide discovery areas that do not belong to one feature package. A subfolder may begin
with a `README.md` investigation brief or orientation index and later contain a distinct discovery
artifact. Each README must state explicitly whether it is the discovery or only prepares one.

## 2. Business Context

A discovery is the artifact that precedes a SPEC: it establishes what a problem actually is,
what already exists, and what remains open, before anything is designed or committed to. Most
discoveries in this repository are owned by a feature and live under
[`../features/<feature>/discovery/`](../features/). This folder holds the exceptions — discovery
areas whose subject spans the whole orchestration runtime and would be mis-filed under any single
feature. The areas here remain draft and must not be read as settled architecture merely because
they have a repository-wide home.

## 3. Why it matters

These documents address foundational choices: where agent assertions enter the knowledge bus,
which runtime layers should be adopted rather than built, and how executable work should be
represented. Reading them as settled would be an error; so would missing that they exist and
re-deriving their content inside a feature package. This index states their status so neither
happens.

## 📁 Navigation

- **`agent-assertion-capture/`**: "Agent assertion capture — the source layer of the knowledge
  bus." `node_type: discovery`, `status: draft`, v0.2.0, created 2026-07-21. The discovery is the
  folder's own [README.md](agent-assertion-capture/README.md).
- **`external-tools/`**: "External tools — build-vs-adopt for the orchestration runtime (Front 3)."
  `node_type: readme`, `status: draft`, v0.1.0, created 2026-07-21. The planned discovery is
  `external-tools.md`; its [README.md](external-tools/README.md) is the orientation index. Related investigation:
  [`../../research/external-tools-verification/`](../../research/external-tools-verification/).
- **`workflow-graph/`**: repository-wide investigation of whether executable work is one graph or a
  composition of protocol topology, confirmed workflow, runtime state, communication and
  completion. Its [README.md](workflow-graph/README.md) is an investigation brief; the actual
  `workflow-graph.md` discovery is planned.

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| sibling-of | [`../features/`](../features/) — feature-owned discoveries live under each feature |
| authored-via | `.claude/skills/discovery-writing/SKILL.md` — the discovery-authoring workflow |
| governed-by | [`../../vault/ontology-conventions.md`](../../vault/ontology-conventions.md) — frontmatter conventions both documents carry |
