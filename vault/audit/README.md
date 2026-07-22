---
tags: [vault, audit, router]
node_type: readme
is_session: false
layer: domain
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-22
---

# vault/audit — router

> **What lives here.** *Audits* — honest checks of what the project's ledger and its
> claims actually hold up to **right now**, not plans or theories. An audit earns its
> authority by being reproducible: re-run it and see if the finding still stands.

The whole system runs on one **append-only ledger** — a log that records every batch of
agent work after a human confirms it. Two very different things get audited here: whether
that ledger is *trustworthy*, and whether the project's headline claim — that the way it
grows knowledge is the *same underlying structure* as the loop it runs to coordinate agents
("the framework as its own instance") — is actually true of the running system.

## The audits

| Audit | The question, in plain words | What it found | Why it matters to the project |
|---|---|---|---|
| [ledger-enum-drift-finding](ledger-enum-drift-finding.md) | Did every record in the ledger go through the one validated gate? | **No** — two records (2026-07-18) were added by hand, bypassing it. | Breaks the "single write path" rule that the next milestone (letting a UI button write) depends on. |
| [close-row-enrich-c](close-row-enrich-c.md) | When a batch of agent work closes, can that ever teach the system a genuinely *new distinction*? | **No** — provable from the ledger's schema, not just observed. | The "framework is its own instance" claim can't fully hold until the ledger is redesigned. |
| [faces-instance-frozen-map](faces-instance-frozen-map.md) | Do the project's three self-descriptions really share one core loop? | Two of three match; the running-system face is **missing** its "learn something new" step. | Same gap as above, reached independently — and it parks a design decision for that future redesign. |

## How they connect

- **Two are the same story from different angles.** `close-row-enrich-c` and
  `faces-instance-frozen-map` both find that today's orchestrator can *record* work but can't
  yet *learn a new distinction* from closing it — so the "same structure" claim only becomes
  testable once the ledger is rebuilt (the planned **BL-3** typed-graph ledger).
- **One stands apart.** `ledger-enum-drift-finding` is about the ledger's plain integrity,
  and it is the keystone to clear before the project lets anything write to the ledger
  automatically.

## Connections

| Document | Type | Description |
|---|---|---|
| [[ledger-enum-drift-finding]] | `contextualizes` | Indexes the ledger-integrity audit; routes readers to the live counterexample that blocks EG-1. |
| [[close-row-enrich-c]] | `contextualizes` | Indexes the "can a close enrich `C`?" audit — one half of the fractality story. |
| [[faces-instance-frozen-map]] | `contextualizes` | Indexes the frozen faces-instance map — the other half, breaking at the same joint. |
