---
tags: [docs, temps, working-notes, unratified, index]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/temps

## 1. What is this?

Working notebooks. Each subfolder holds evolving design notes for something not yet ratified —
material that is being thought through in the open, before it earns a discovery document, a SPEC,
or a runtime contract.

## 2. Business Context

This repository draws a hard line between an artifact that carries authority and one that does
not: a discovery, a SPEC, a decision record, and a constitution each bind downstream work, and
the promotion path into them is gated. `temps/` is the holding area on the far side of that gate.
Its current occupant, the Agent Dispatch Protocol notebook, states the boundary in its own
opening line — "working notes; not a ratified discovery, SPEC, recipe, or runtime contract."

## 3. Why it matters

The folder name is misleading in a way that has a cost. "temps" reads as scratch or disposable,
but the contents are active, dated, and being worked on — the dispatch-protocol notebook was
started 2026-07-25. Deleting this folder as cleanup, or conversely citing anything inside it as
authority, are both errors this README exists to prevent: nothing here binds, and nothing here is
abandoned.

## 📁 Navigation

- **`agent-dispatch-protocol/`**: Design notebook for compiling a reusable per-skill protocol into
  a concrete, deterministically executable multi-agent dispatch. Started 2026-07-25; explicitly
  not ratified. See its own [README](agent-dispatch-protocol/README.md).

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| feeds | [`../discovery/`](../discovery/) — the promotion target once notes earn a discovery |
| relates-to | [`../../.claude/skills/domainspec-subagents-strategy/SKILL.md`](../../.claude/skills/domainspec-subagents-strategy/SKILL.md), [`../../.claude/skills/register-dispatch/SKILL.md`](../../.claude/skills/register-dispatch/SKILL.md) — the dispatch machinery the notebook is designing against |
