---
tags: [docs, essays, index, orchestration, noise, category-theory, context]
node_type: readme
is_session: false
layer: [ontology, architecture, epistemology]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/essays

## 1. What is this?

Long-form argumentative pieces about what this repository is building and why. Every item here is
`status: draft` and `authority: proposal-only` — an essay argues a position, it does not bind
anything. Three are folders (an essay plus its supporting material), two are single files.

## 2. Business Context

The orchestrator is being built alongside a claim about *why* it should exist, and the essays are
where that claim is developed before it is allowed to govern anything. They sit downstream of the
hypothesis nodes in [`../../vault/hypothesis/`](../../vault/hypothesis/) — the anti-noise essay
derives from `HYP-ORCH-NOISE`
([`../../vault/hypothesis/anti-noise-orchestration.md`](../../vault/hypothesis/anti-noise-orchestration.md))
— and upstream of the system views under
[`../../plans/governed-agent-work-infrastructure/essays/`](../../plans/governed-agent-work-infrastructure/essays/),
which name the two context essays here as their `predecessors`.

## 3. Why it matters

Two things here are easy to get wrong. First, the two hypothesis essays carry explicit
`veracity: low` / `conviction: medium` frontmatter — they are held with more confidence than
they have evidence for, and are marked that way on purpose; citing them as established would
invert their own stated status. Second, `anti-noise-orchestrator/` is the only essay with a
`research/` tree beneath it, so its supporting evidence is not where a reader would look for the
others.

## 📁 Navigation

- **`anti-noise-orchestrator/`**: "The Orchestrator as a Noise-Reduction Machine" — the thesis
  that an agent orchestrator is formally a judgment-error-reduction machine over the native lever
  `residue = bias ⊕ noise`. High-level draft, unreviewed. The essay is the folder's
  [README.md](anti-noise-orchestrator/README.md); its supporting work sits in
  `anti-noise-orchestrator/research/` across four subfolders — `critique-redteam/`,
  `frame-refine-review/`, `prior-art-ct-kahneman-thaler/` and `seam-feasibility/`.
- **`categorical-theory-hypothesis/`**: Category-theoretic reading of orchestration (residue,
  shadow, probe, Yoneda, pushout, colimit, enrichment, `OBL-E3`). `status: draft`,
  `veracity: low`, `conviction: medium`, v0.1.0. Essay is the folder's
  [README.md](categorical-theory-hypothesis/README.md).
- **`decision-hygiene-hypothesis/`**: Decision-hygiene reading of orchestration (Kahneman,
  Thaler, noise, bias, framing, nudge). `status: draft`, `veracity: low`, `conviction: medium`,
  v0.1.0. Essay is the folder's [README.md](decision-hygiene-hypothesis/README.md).
- **[from-context-to-governed-primitives.md](from-context-to-governed-primitives.md)**: Carries
  the macro/micro argument into graphs, ontologies, invariants and services. `status: draft`,
  v0.1.0, `authority: proposal-only`; declares `macro-to-micro-context.md` as related.
- **[macro-to-micro-context.md](macro-to-micro-context.md)**: "Linking the Macro to the Micro" —
  objectives, work lineage and hierarchy. `status: draft`, v0.1.0, `authority: proposal-only`.

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| derives-from | [`../../vault/hypothesis/`](../../vault/hypothesis/) — the hypothesis nodes the essays argue |
| precedes | [`../../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md`](../../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md) — names both context essays as `predecessors` |
| governed-by | [`../../vault/ontology-conventions.md`](../../vault/ontology-conventions.md) — the `veracity`/`conviction` convention |
