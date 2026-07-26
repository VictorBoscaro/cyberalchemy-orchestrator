---
tags: [plans, essays, system-view, agent-language, work-context, index]
node_type: readme
is_session: false
layer: [architecture, ontology]
nature: reference
status: active
version: 0.1.1
last_updated: 2026-07-26
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
authority: proposal-only
---

# Governed Agent Work Infrastructure — essays

## 1. What is this?

The system views for this Plan: long-form documents that explain the shape and stakes of the
proposed system to a reader who does not yet have its vocabulary. Both are `status: draft` and
`authority: proposal-only` — they argue for a design, they do not ratify one.

## 2. Business Context

This Plan proposes a common language for governed agent work, and that language cannot be
specified before it can be described. The two essays split that job: the **agent-language**
system view sets out the composable language itself and states plainly that its terms stay
provisional until an ontology view owns them and its load-bearing choices stay open until an
engineer view owns their verdicts; the **work-context** companion carries the macro-to-micro
context argument — objectives, work lineage, authority — into the same frame. Both name
[`../subplans/agent-work-language-research/PLAN.md`](../subplans/agent-work-language-research/PLAN.md)
as their `related_plan`, and the work-context essay names the two `docs/essays/` context pieces as
its `predecessors`.

## 3. Why it matters

These are the entry documents for the Plan — the readable account a newcomer needs before
`PLAN.md`, `CANDIDATE-INVARIANTS.md` or the workstreams make sense. Two conditions are worth
knowing before reading. First, `work-context-system-view/essay.md` used to point its
`companion_to` and two body references at `docs/architecture/agent-language-system-view.md`, a
path that stopped resolving when the agent-language essay moved here. All three now point at
[`agent-language-system-view/essay.md`](agent-language-system-view/essay.md) (repaired
2026-07-26, dispatch `2026-07-26-docs-defect-repair`) — this was the first of five
recommendations in the essay's own review; **the remaining four are still open**. Second, the review
found no section redundant across all 38 sections and recommended the essay stay one file, so
its length is a deliberate outcome rather than an unfinished edit.

## 📁 Navigation

- **`agent-language-system-view/`**: "A Composable Language for Governed Agent Work" — the
  high-level system view. `node_type: system-view`, `status: draft`, v0.8.1,
  `authority: proposal-only`, `root_plan: plans/governed-agent-work-infrastructure/PLAN.md`.
  - **[essay.md](agent-language-system-view/essay.md)**: the essay.
  - **`agent-language-system-view/pdf-version/`**: five rendered variants —
    `02-swiss.pdf`, `03-blueprint.pdf`, `04-academic.pdf`, `05-studio.pdf` and
    `agents-infrastructure-hypothesis.pdf`. The numbering starts at 02; there is no
    `01-editorial.pdf` in this folder.
- **`work-context-system-view/`**: The work-context companion to the system view.
  `node_type: essay`, `view_kind: system-view-companion`, `status: draft`, v0.2.0,
  `authority: proposal-only`.
  - **[essay.md](work-context-system-view/essay.md)**: the essay, 38 numbered sections.
  - **`work-context-system-view/review/`** → **[review.md](work-context-system-view/review/review.md)**:
    the review of that essay. Recommends keeping it as one file and making five navigational
    repairs, beginning with the broken canonical-companion reference.

## Connections

| Edge | Target |
|---|---|
| owned-by | [`../PLAN.md`](../PLAN.md) — the governing Plan |
| related-plan | [`../subplans/agent-work-language-research/PLAN.md`](../subplans/agent-work-language-research/PLAN.md) — both essays name it |
| derives-from | [`../../../docs/essays/macro-to-micro-context.md`](../../../docs/essays/macro-to-micro-context.md), [`../../../docs/essays/from-context-to-governed-primitives.md`](../../../docs/essays/from-context-to-governed-primitives.md) — declared `predecessors` |
| companion-of | [`agent-language-system-view/essay.md`](agent-language-system-view/essay.md) — the `companion_to` target of the work-context essay, repaired 2026-07-26 |
