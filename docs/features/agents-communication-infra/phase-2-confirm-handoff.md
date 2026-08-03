---
feature: agents-communication-infra
title: "Phase 2 — the confirm handoff (control plane → orchestrator)"
status: draft
authority: candidate
created: 2026-07-21
last_updated: 2026-08-03
---

# Phase 2 — the confirm handoff (control plane → orchestrator)

> Status: **built for the `linear` UI only** (2026-07-21). The write verb and the
> reader flag are server-wide; the button is wired in `static/ui/linear/index.html`.
> The other nine variants still render the button disabled.

Phase 1 made the control plane a **reader**. Phase 2 adds exactly one write verb so a
human can confirm a pending sheet from the browser instead of typing "sim" into a
Claude session. It does **not** move dispatch execution into the server — the
orchestrator (Claude, in a session) still runs the chain. The seam between them is a
**marker file**, not a ledger write.

## The three layers

1. **Write verb — `POST /api/confirm`** (`server/main.py`). Body `{repo, file}`.
   Writes `telemetry/agents/pending/<sheet>.json.confirmed` — a marker in the pending
   dir, *"the only editable surface"*. It **never** touches the append-only ledger, so
   **EG-1** (one validated writer for `subagents-dispatch.yaml`) is untouched: the
   validated appender still writes the real dispatch row later. Guards: unknown repo →
   404, missing sheet → 404, path traversal / non-`.json` name → 400. Idempotent.

2. **Reader flag — `_confirmed`** (`server/ledger.read_pending`). Each pending entry
   carries `_confirmed: true|false` from the marker's existence. The marker ends in
   `.confirmed`, outside the `*.json` glob, so it never reads back as a sheet of its own.

3. **UI button** (`static/ui/linear/index.html`, `pendingCard`). Unconfirmed → enabled
   "Dispatch"; on click POSTs and optimistically flips to a disabled "Confirmed"
   (the SSE `signature()` globs only `*.json`, so a marker write does not itself wake the
   stream — the optimistic flip is the live feedback; a reload re-reads `_confirmed` from
   disk). Confirmed → disabled "Confirmed". Unreadable sheet → disabled.

## The orchestrator's side (the loop this closes)

When a Claude session is acting as orchestrator, the confirm marker is its trigger. On
seeing a new `<sheet>.json.confirmed`:

1. Read the sheet it names (`pending/<sheet>.json`).
2. Run the existing chain — the `domainspec-subagents-strategy` entry preserves the user's
   explicit `anti_bias_mode` choice, then **register-dispatch** validates and writes the dispatch
   row, the orchestrator spawns the agent groups, and **close** appends the close row. The default
   is `disabled`; `enabled` is accepted only with complete pairwise evidence produced at entry.
3. **Consume the queue entry:** once the dispatch is registered (it now lives in the
   ledger, the durable record), delete the pending sheet **and** its `.confirmed` marker
   so the pending dir stays a queue of *not-yet-dispatched* work. Registration in the
   ledger — not the marker — is the permanent fact (EG-1/EG-6).

The marker is transport, deliberately ephemeral; the accepted fact and its provenance
survive in the ledger. This is the same "bus is a projection, not a second source of
truth" discipline the infra hypothesis (HYP-ORCH-INFRA) states, applied to the smallest
possible surface.

### Arming the watch

The watch is a per-session behavior, not a daemon: in a live orchestrator session, the
assistant polls (or uses a Monitor) the pending dirs for `*.confirmed` markers and runs
the chain above. There is intentionally no background writer — keeping execution in the
session preserves the single human gate and the one-validated-writer boundary.

## What is NOT built yet

- The button in the other nine UI variants (share `pendingCard` shape; same three-line change).
- Any automatic marker consumption — today the orchestrator (or a human) deletes the
  marker after dispatch; there is no server-side reaper.
- A `consumed/` archive — deletion is the current convention; move-instead-of-delete is a
  future option if an audit trail of *what was queued* (distinct from *what dispatched*)
  is wanted.

## Connections

| Document | Type | Description |
|---|---|---|
| [`discovery/feature-discovery/agents-communication-infra.md`](discovery/feature-discovery/agents-communication-infra.md) | `grounds` | Supplies the implemented marker/session seam that the runtime migration discovery must preserve or replace explicitly. |
| `README.md` (this feature) | `refines` | The full Phase-1/Phase-2 proposal; this is the concrete Phase-2 slice that shipped. |
| `vault/constitution/engine-constitution.md` (EG-1) | `respects` | Confirm writes a pending-dir marker, never the ledger; the validated appender stays the sole ledger writer. |
| `vault/hypothesis/orchestration-infra.md` (HYP-ORCH-INFRA) | `instantiates` | "Transport is ephemeral, the accepted fact survives in the ledger" — applied to the smallest surface. |
| `implementations/server/main.py` · `ledger.py` | `implemented-by` | The write verb (`POST /api/confirm`) and the `_confirmed` reader flag. |
| `implementations/static/ui/linear/index.html` | `implemented-by` | The wired Dispatch button (this variant only). |
