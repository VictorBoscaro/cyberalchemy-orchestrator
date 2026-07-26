---
tags: [docs, navigation, index, features, decisions, discovery, essays]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs

## 1. What is this?

`docs/` is the repository's documentation root. It holds the long-lived written artifacts of the
knowledge machine — feature packages, accepted decisions, discovery documents, essays, and emitted
pipeline signals — as distinct from the executable machinery (`.claude/skills/`,
`implementations/`, `tools/`) and from the governed knowledge store (`vault/`).

## 2. Business Context

This repository builds a governed agent orchestrator, and its work products are documents before
they are code: a feature is discovered, specified, decided, and only then implemented. `docs/`
is where that chain lives. Two of its subfolders are load-bearing for that pipeline —
`decisions/`, which records accepted choices that later artifacts cite as their authority (for
example [`decisions/host-agent-dispatch-input-binding.md`](decisions/host-agent-dispatch-input-binding.md),
cited as `authority.decision` by
[`../plans/governed-agent-work-infrastructure/workstreams/agent-reference-lineage-implementation-layering.md`](../plans/governed-agent-work-infrastructure/workstreams/agent-reference-lineage-implementation-layering.md)),
and `features/`, where each in-flight build keeps its own spec, discovery, and work-pack tree.

## 3. Why it matters

Without an index here, the eight subfolders below give no signal about which are active, which
are empty, and which are scratch. Two of them (`architecture/`, `archive/`) currently hold no
files at all, and one is named `temps/` while containing active working notes — a reader
navigating by folder name alone will draw the wrong conclusion in three of eight cases. This
file states the actual status of each.

## 📁 Navigation

- **`architecture/`**: Currently empty on disk. It held `agent-language-system-view.md` and a
  `pdf-versions/` set; that essay now lives at
  [`../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/`](../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/).
  Documents elsewhere still point at the old path — see the note in
  [`../plans/governed-agent-work-infrastructure/essays/README.md`](../plans/governed-agent-work-infrastructure/essays/README.md).
- **`archive/`**: Currently empty. Reserved for retired documents.
- **`decisions/`**: Accepted decision records that other artifacts cite as governing authority.
  Has its own [README](decisions/README.md).
- **`discovery/`**: Standalone discovery documents not owned by any single feature package.
  Has its own [README](discovery/README.md).
- **`essays/`**: Long-form argumentative pieces and their supporting research, at
  `authority: proposal-only`. Has its own [README](essays/README.md).
- **`features/`**: One subfolder per feature build, each holding its own discovery, specs,
  work-pack and reviews. The deepest tree in the repository.
  Has its own [README](features/README.md).
- **`signals/`**: Machine-emitted pipeline signal records. Has its own [README](signals/README.md).
- **`temps/`**: Working notebooks that are explicitly not ratified artifacts. Despite the name,
  the contents are active. Has its own [README](temps/README.md).

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the repository root README |
| sibling-of | [`../plans/README.md`](../plans/README.md) — owns the canonical Plan contract |
| governed-by | [`../vault/ontology-conventions.md`](../vault/ontology-conventions.md) — frontmatter and node-type conventions |
| conforms-to | `.claude/skills/custom/readme-pattern.md` — the four-section README contract |
