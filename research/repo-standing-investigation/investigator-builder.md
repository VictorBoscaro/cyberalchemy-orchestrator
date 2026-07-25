---
tags: [orchestration, control-plane, phase-2, dispatch-loop, builder, standing-investigation]
node_type: conceptual
is_session: false
layer: architecture, application
nature: explanatory
status: draft
veracity: medium
conviction: high
version: 1.0.0
last_updated: 2026-07-21
---

# Investigator — the Builder

*Vector: value = a loop that runs end-to-end and produces a usable result. Theory that types nothing buys nothing yet.*

## Headline finding: the loop already runs — it just isn't driven from the plane

The end-to-end orchestration loop **already executes today**, in-session:
propose → `check-tension` (anti-bias gate) → human confirm → `register-dispatch`
appender writes the ledger row → Claude spawns `Agent` subagents → close row →
SSE pushes it to the 10 UIs. This very investigation is an instance of it.
Evidence: `README.md` "what runs today", `plans/governed-agent-work-infrastructure/PLAN.md §4`,
`.claude/skills/register-dispatch/append-dispatch.cjs` (~26 KB, validated, wrote
this repo's ~30 dispatches), the ~49-row live ledger.

So the read-only substrate is **one verb short** of a control-plane-driven loop.
`implementations/server/main.py` is GET-only (its own docstring, lines 6-9, names
Phase 2 + `Monitor` as the plan). The button already exists and is inert:
`implementations/static/ui/terminal/index.html:548` (`data-testid="dispatch-button" disabled`),
`UI-CONTRACT.md:252-255`. The pending sheet
(`telemetry/agents/pending/2026-07-19-example-ui-control-plane.json`) is the
purpose-built pre-confirm editable surface — its own `_note` says "Delete it once
the real flow is up."

## What should be done next (ranked)

### 1. Wire Phase 2 confirm as a *pending-sheet marker*, not a ledger write. (smallest slice)
- `POST /api/confirm/{repo}/{dispatch_id}` writes a confirm marker into the pending
  sheet (already "the only editable surface, pre-confirm"). **It does not touch the ledger.**
- Enable the disabled button in **one** UI (terminal), not all ten.
- Claude in-session waits on `Monitor` (the deferred tool the README Phase 2 already
  names), sees the marker, runs the existing chain (`check-tension` →
  `register-dispatch` → `Agent` spawns → close row).
- Result: a person clicks a button in the browser and a real dispatch runs and
  streams back. That is the demonstrated loop. Est. ~1 endpoint + 1 button enable
  + 1 Monitor wait.

### 2. Phase 3-minimal: `POST` to create/edit the pending sheet from the UI.
Then propose + confirm + observe all happen in the plane; delete the example
fixture once a real sheet flows through. This makes the loop fully person-usable
without a session author hand-writing JSON.

## The "blocker" is mis-scoped — do not let it veto the loop

The enum-drift (`vault/audit/ledger-enum-drift-finding.md`) blocks **EG-1's
*promotion*** — a governance/veracity status — **not the appender's *operation***.
The appender works; it wrote ~30 dispatches. The 2 bad rows are ones that
**bypassed** it (manual YAML edit). Phase-2-as-marker writes a confirm signal, and
the row is still written by the validated appender — so wiring it **reinforces**
the single-writer invariant instead of threatening it. "Resolve enum-drift before
Phase 2" is only binding for a *button-writes-ledger-YAML* design; the README's own
design (Claude's `register-dispatch` writes the row) dissolves the gate. A Builder
ships slice #1 now and traces the 2-row drift in parallel, not as a precondition.

## Defer (big rebuilds that would sit unused)

All of Front 3 §3.3 as a *rewrite*: deterministic kernel, vendor adapters,
per-group deliberation bus, event journal, technical reveal barrier, knowledge
store (`docs/features/agents-communication-infra/README.md` — a 1254-line target
spec, explicitly "not a runtime"). Also Front 2 / OBL-E3 CT typing, and the
claim→refute→golden loop (`PLAN.md §5`). None is needed for a demonstrated loop;
each is multi-week and the session-as-runtime already covers the executor role
those pieces would fill. The correct cheap runtime is **the Claude session via
Monitor**, exactly as the README Phase 2 chose — reuse it, don't build a kernel yet.

## Already built, under-used

- `register-dispatch` appender + `check-tension` + `Agent` + `robot-talks` — a
  complete, executable dispatch discipline, driven only by hand.
- 10 UI variants + SSE — already observe the loop live; missing only the write-back verb.
- The pending sheet — designed as the pre-confirm surface for exactly this button.
- `agent-pool-mcp` (419 entries, cross-repo) — resolves `agent_name`, already runnable.
- `Monitor` — the single missing primitive; it exists as a tool, just isn't invoked.

**Bottom line:** the shortest path to a demonstrated end-to-end orchestration is not
new architecture — it is one POST endpoint + one enabled button + one Monitor wait,
closing the loop the substrate already runs by hand. Ship that before any Front-2/3 theory.

## Connections

| Document | Type | Description |
|---|---|---|
| `README.md` | `grounds` | "What runs today" — the in-session dispatch loop this finding says is one verb short of the plane. |
| `plans/governed-agent-work-infrastructure/PLAN.md` | `grounds` | §4 runs-vs-thesis; this doc argues the §3.3 rebuild is deferrable behind a Phase-2 slice. |
| `implementations/server/main.py` | `contextualizes` | The GET-only reader whose missing `POST /api/confirm` is build step #1. |
| `.claude/skills/register-dispatch/SKILL.md` | `grounds` | The validated appender that already writes the ledger — the loop's working write step. |
| `vault/audit/ledger-enum-drift-finding.md` | `contradicts` | This doc argues its "keystone before Phase 2" framing is mis-scoped: it blocks EG-1 promotion, not the appender's operation. |
| `docs/features/agents-communication-infra/README.md` | `contradicts` | The full Front-3 target spec; this doc argues it is deferrable, not the next step. |
