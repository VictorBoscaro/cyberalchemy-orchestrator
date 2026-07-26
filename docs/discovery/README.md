---
tags: [docs, discovery, index, orchestration-runtime, knowledge-bus]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/discovery

## 1. What is this?

Discovery documents that belong to the repository at large rather than to any one feature
package. Each subfolder is one discovery, authored as a `README.md` carrying full ontology
frontmatter, and each is currently `status: draft`.

## 2. Business Context

A discovery is the artifact that precedes a SPEC: it establishes what a problem actually is,
what already exists, and what remains open, before anything is designed or committed to. Most
discoveries in this repository are owned by a feature and live under
[`../features/<feature>/discovery/`](../features/). This folder holds the exceptions — discoveries
whose subject spans the whole orchestration runtime and would be mis-filed under any single
feature. Both current occupants sit at `layer: architecture, application` and were created
2026-07-21, when the runtime's source layer and its build-vs-adopt question were being worked
out in parallel.

## 3. Why it matters

Both documents are drafts about foundational choices — where agent assertions enter the knowledge
bus, and which parts of the orchestration runtime should be adopted rather than built. Reading
them as settled would be an error; so would missing that they exist and re-deriving their content
inside a feature package. This index states their status so neither happens.

## 📁 Navigation

- **`agent-assertion-capture/`**: "Agent assertion capture — the source layer of the knowledge
  bus." `node_type: discovery`, `status: draft`, v0.2.0, created 2026-07-21. The discovery is the
  folder's own [README.md](agent-assertion-capture/README.md).
- **`external-tools/`**: "External tools — build-vs-adopt for the orchestration runtime (Front 3)."
  `node_type: readme`, `status: draft`, v0.1.0, created 2026-07-21. The discovery is the folder's
  own [README.md](external-tools/README.md). Related investigation:
  [`../../research/external-tools-verification/`](../../research/external-tools-verification/).

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| sibling-of | [`../features/`](../features/) — feature-owned discoveries live under each feature |
| authored-via | `.claude/skills/discovery-writing/SKILL.md` — the discovery-authoring workflow |
| governed-by | [`../../vault/ontology-conventions.md`](../../vault/ontology-conventions.md) — frontmatter conventions both documents carry |
