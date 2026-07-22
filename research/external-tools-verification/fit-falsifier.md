---
tags: [external-tools, verification, falsify-fit, I1, I2, octopus-runtime, eve, pydantic-ai]
node_type: audit
is_session: false
layer: research
nature: adversarial-verification
status: complete
version: 0.1
last_updated: 2026-07-21
veracity: high
conviction: medium
---

# Fit-Falsifier — Adversarial Verification (read-only, first-hand)

Disposition: falsify-fit. Each tool assumed WRONG until its own source proves otherwise.
Invariants: **I1** no second source of truth (durable store subordinate-able to an external
event journal, never a competing canonical authority); **I2** freeze-before-channel (one-shot on a
frozen snapshot, no shared conversation history).
Verdicts: RESOLVES = failure hunt came up empty (source genuinely satisfies) · PARTIAL · FAILS.
Verified 2026-07-21 against live source/docs.

## octopus-runtime — `github.com/octoryn/octopus-runtime` (v0.7.0, Apache-2.0)

| Check | Verdict | Evidence (path / URL / quote) |
|---|---|---|
| (a) execute guard bypassable vs structural | **PARTIAL** | `src/gate.ts`: guard is advisory — `routeExecutes(route) => route === "autonomous"` and `routeFor(decision)` return values, not a capability barrier. Nothing stops a caller importing a connector and calling `.execute()` directly; the "unreachable except on Autonomous/Draft path" property holds only *on the runtime path* (`test/render-execute-split.test.ts`). Structural within the engine, not an unbypassable seal. |
| (b) octopus-evidence insists on canonical authority (I1) | **RESOLVES** | Falsification fails. `github.com/octoryn/octopus-evidence` README "Boundaries": *"Evidence is a **primitive**, not a system. It has no storage, no query, no network, no derivation."* Storing/timelining/gating are "the jobs of the other repos." It is a hash/serialization atom, fully subordinate — cannot be a competing authority. |
| (c) governTool admits wrapping our appender / imposes own store | **RESOLVES** | `src/ports.ts`: `Store`, `AuditSink` (`append(record)`/`query(filter)`), `ApprovalGateway`, `Transactor` etc. are caller-implemented interfaces — *"Dependency arrows always point inward: the core depends on these interfaces; adapters depend on the core. The core never imports an adapter."* `examples/govern-tool.ts` wraps *"any async function."* Our appender can be dropped in as the `AuditSink`/`Store` adapter → subordinable to an external journal. |
| (d) maturity red flags / false dep claims | **PARTIAL** | "No tests / no releases / false deps" is **FALSE**: `package.json` has one real dep `octopus-evidence ^0.2.0` (peer `better-sqlite3`), 3 releases, ~22 test files / 83 `node --test` cases, CI workflows. Genuine risk remains: single author (`Ran Tao <ran@octopusos.ai>`), 1 star, commercially captured (`octopusos.ai`, "patents in flight"), version drift (repo page cites v0.3.2, `package.json` says 0.7.0), 2026-nascent. |

**I1 → RESOLVES** (ports invert dependency; evidence is a subordinate primitive). **I2 → RESOLVES/NA** — trigger→result execution runtime, one-shot per run, holds no conversation history to share.

## Eve — `eve.dev` / `github.com/vercel/eve` + Workflow SDK (Apache-2.0, GA 2026-06)

| Check | Verdict | Evidence |
|---|---|---|
| (a) Workflow SDK insists on durable source of truth (I1) | **FAILS** | `vercel.com/docs/eve/concepts` §Durability: *"eve sessions run on top of Vercel Workflows. Workflows persist progress as an event log and deterministically replay it to reconstruct state."* The Vercel-managed event log **is** the canonical state authority (state is *reconstructed from it*), platform-bound (Functions/Fluid Compute/AI Gateway). Not subordinable to our appender — it competes as canonical truth. |
| (b) shared conversation history mandatory (I2) | **PARTIAL** | Sessions are *"the durable conversation"* persisting `history: ModelMessage[]`; history is core to the session model. But §Subagents: a subagent *"runs as a separate agent with **fresh conversation history and state**."* So freeze/no-shared-history is *achievable* via the subagent path — mandatory-history falsification only partly lands. |
| (c) fails to drive claude-code-cli/codex-cli on 5-op contract | **FAILS** | Eve is the agent, not a driver of external CLIs. `defineAgent({ model: 'openai/gpt-5.4-mini' })` resolves via AI Gateway; `workflow-sdk.dev/docs/ai`: WorkflowAgent *"runs the agent loop inside a workflow, persists state across step boundaries."* HTTP surface = `POST /eve/v1/session` (start) + `GET /eve/v1/session/<id>/stream` (events); no external-agent start/events/result/cancel/status contract wrapping claude-code-cli/codex-cli. Wrong role shape. |
| (d) license / maturity red flags | **PARTIAL** | Apache-2.0, Vercel-backed (not single-author) — but GA 2026-06 (brand new) and deeply Vercel-platform-coupled (Workflows, Functions, Fluid Compute, AI Gateway, Sandbox), colliding with the repo's portability/repo-local principle. |

**I1 → FAILS** (competing platform-owned canonical event log). **I2 → PARTIAL** (suppressible via fresh-history subagents). Role fit → FAILS (model-runner, not a CLI-agent driver).

## PydanticAI — `ai.pydantic.dev` (Python)

| Check | Verdict | Evidence |
|---|---|---|
| (a) output_type falls short of sealed versioned judgment record | **PARTIAL** | `pydantic.dev/docs/ai/core-concepts/output/`: `output_type` yields a validated plain Pydantic model / dataclass / TypedDict via Tool/Native/Prompted modes. Docs contain **no** native versioning, schema-version field, immutability, or sealing/hashing guarantee. A sealed+versioned record is hand-buildable (`model_config frozen=True` + version literal + external hash) but is not what `output_type` *is* — it falls short natively. |
| (b) pydantic-graph claims durable authority (I1) | **RESOLVES** | Falsification fails. `pydantic.dev/docs/ai/graph/graph/` describes state as an in-memory object *"passed along the line and built up by each node"* — no `persistence`/`durable`/`snapshot`/authority claims on the core graph. Persistence is a separate optional, pluggable module (in-memory default); does not assert canonical truth → subordinable. |
| (c) Python split unavoidable & costly beside TS/JS runtime | **FAILS** | PydanticAI is Python-only; no JS/TS port. Adopting it forces a Python process alongside the TS/JS appender + `agent-pool-mcp`, adding a cross-language IPC/serialization boundary and a second dependency toolchain — an unavoidable, load-bearing fit cost. |

**I1 → RESOLVES** (output is inert data; graph persistence optional/pluggable — both subordinable). Cost: mandatory Python split.

## Roll-up

- **octopus-runtime** — I1 RESOLVES, I2 RESOLVES/NA; only soft holes: advisory (not sealed) execute guard, and single-author/1-star/commercially-captured immaturity. No I1/I2 disqualifier found.
- **Eve** — I1 FAILS (Vercel-owned event log is a competing canonical authority; platform-locked) and role FAILS (runs its own model loop; does not drive claude-code/codex CLIs on the 5-op contract). I2 only PARTIAL (subagents give fresh history).
- **PydanticAI** — I1 RESOLVES (subordinable); but `output_type` is not a sealed/versioned record natively (PARTIAL) and imposes an unavoidable Python split (FAILS on fit-cost).

## Connections

| edge | target | note |
|---|---|---|
| tests | invariant I1 (no second source of truth) | falsify-fit probe per tool; octopus & pydantic-ai subordinable, Eve competes |
| tests | invariant I2 (freeze-before-channel) | octopus one-shot; Eve suppressible-via-subagents; pydantic-ai N/A |
| contradicts | (confirmer verdict, if it clears Eve on I1) | Eve's Vercel-owned event log falsifies subordinability |
| grounds | external-tool selection decision-gate | supplies adversarial evidence for adopt/reject |
| derives-from | vault/ontology-conventions.md | veracity⊥conviction; verdicts carry inline evidence/URL |
| relates-to | Portability / install principle (MEMORY) | Eve platform-lock red flag; PydanticAI Python-split cost |

