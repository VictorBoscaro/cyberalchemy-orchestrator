---
tags: [external-tools, verification, fit-confirm, octopus-runtime, eve, pydantic-ai]
node_type: audit
is_session: false
layer: research
nature: first-hand source verification (confirm-fit disposition)
status: draft
version: 0.1.0
last_updated: 2026-07-21
veracity: high
conviction: medium
---

# External Tools Fit-Confirmer

First-hand verification (source + official docs read directly). Disposition: **confirm-fit** — strongest honest case per check. Verdicts frozen independently.

Invariants: **I1** no second source of truth (a tool's durable store must be subordinable to an external event journal); **I2** freeze-before-channel (one-shot on a frozen snapshot, no shared conversation history).

## octopus-runtime (github.com/octoryn/octopus-runtime, v0.7.0)

| Check | Verdict | Evidence (path / URL / quote) |
|---|---|---|
| (a) structural guard on `execute` enforced in code | **RESOLVES** | `src/gate.ts`: `export function routeExecutes(route: GateRoute): boolean { return route === "autonomous"; }` — execute path returns true *only* for `"autonomous"`; `"draft"` = "render and create an approval; execute only once approved." Guard is code, not prose. |
| (b) octopus-evidence subordinate effect-audit plane (I1) | **RESOLVES** | `octopus-evidence` README (github.com/octoryn/octopus-evidence): *"Evidence is a primitive, not a system. It has no storage, no query, no network"* and is *"subordinate to an external event journal."* `src/decision-evidence.ts`: *"a pure mapping ... it only reads a decision that was already made and writes down a verifiable trace of it."* Audit, never authority. |
| (c) governTool wraps arbitrary async fn behind Draft-approval gate | **RESOLVES** | `src/tool.ts`: `governTool<Input,Output>(fn, options)` returns a governed async fn. `if (route === "autonomous") { ...await fn(input)... }` and `if (route === "draft") { const approved = await options.approve(...); if (approved) {...await fn(input)...} }`; else `{ executed:false }`. "fn is never called" off those paths. Our ledger appender = `fn`. |
| (d) real & usable | **RESOLVES** | `package.json`: `"license":"Apache-2.0"`, `"engines":{"node":">=22"}`, runtime deps = **only** `octopus-evidence ^0.2.0` (itself zero-dep). better-sqlite3 is a *devDependency*. README: 83 tests, v0.7.0 (3 releases, latest Jul 2026). |

## Eve (eve.dev + Vercel Workflow SDK)

| Check | Verdict | Evidence (URL / quote) |
|---|---|---|
| (a) Workflow SDK subordinable to external journal (I1) | **RESOLVES (honest note)** | vercel.com/docs/eve: *"Vercel Workflows persist session state and resume interrupted work."* eve.dev/docs: *"checkpoints each step so a session can pause, survive a crash, and resume."* This is a **runtime checkpoint/resume log**, not a domain source-of-truth — nothing claims it is canonical, so an external ledger stays authoritative. (Note: no explicit "external journal is canonical" statement; subordination is architectural, not enforced.) |
| (b) one-shot on frozen snapshot, no shared history (I2) | **RESOLVES** | vercel.com/docs/eve, "Start a session": `POST /eve/v1/session -d '{"message":"..."}'` starts a fresh session from a single message with no prior conversation attached; returns `x-eve-session-id` + `continuationToken`. A single-turn session = one-shot on frozen input; history is opt-in (only via continuationToken), so omit it. |
| (c) drive claude-code-cli/codex-cli as subprocess adapters vs start/events/result/cancel/status | **PARTIAL** | Session HTTP lifecycle maps the contract: **start**=`POST /eve/v1/session`; **events**=`GET /session/<id>/stream` (NDJSON lifecycle events); **result/status**=`continuationToken` + `x-eve-session-id`. Tools (`defineTool`, zod `inputSchema`, `async execute`, "full access to `process.env`") can spawn a CLI subprocess. But: no first-hand `cancel`, and no native CLI *adapter* — the start/events/result/cancel/status contract must be app-built inside a tool. |
| (d) real & usable | **RESOLVES (beta caveat)** | License Apache-2.0; TypeScript; `eve@0.11.4` (npm), Workflow SDK open-source (workflow-sdk.dev); backed by Vercel's production fleet. Caveat: vercel.com/docs/eve — *"eve is currently in beta ... APIs ... may change."* Some features lean on Vercel services (Sandbox/AI Gateway/Connect), though it runs locally (`npx eve init`, localhost:3000). |

## PydanticAI (ai.pydantic.dev → pydantic.dev/docs/ai)

| Check | Verdict | Evidence (URL / quote) |
|---|---|---|
| (a) output_type covers sealed judgment record bound to schema + digest | **RESOLVES** | .../core-concepts/output/: output_type accepts "dataclasses and Pydantic models ... type unions"; `{values:[{tag,confidence}], rationale}` = `class Output(BaseModel){ values:list[TagEntry]; rationale:str }`. *"Structured outputs use Pydantic to build the JSON schema ... and to validate the data returned by the model."* Record + schema binding native. (Note: version/digest is a caller-supplied field over the model, not a native pydantic-ai primitive — trivially composed.) |
| (b) pydantic-graph state in-memory (subordinable, I1) | **RESOLVES** | .../ai/graph/graph/: state is *"an optional way to access and mutate an object (often a dataclass or Pydantic model) as nodes run"*, *"initialized before the graph runs and then passed along ... built up by each node"* via `GraphRunContext`. In-memory during the run; durable persistence is opt-in, so it does not compete as an authority. |
| (c) pydantic-evals refoldable into zod if runtime is TS | **RESOLVES** | .../ai/evals/evals/: *"pydantic-evals does not depend on pydantic-ai"*; runtime-agnostic model `Dataset → Case → Evaluator` defined "in Python code, or as serialized data." Code-first + runtime-agnostic ⇒ the typed cases/evaluators/scoring model reimplements cleanly in TS/zod. |

## Roll-up

- **octopus-runtime**: 4/4 RESOLVES. Guard is real code; evidence plane is explicitly journal-subordinate; governTool fits the ledger appender.
- **Eve**: 3 RESOLVES (a,b,d) + 1 PARTIAL (c). Fits I1/I2; CLI-adapter contract exists in pieces but is app-built (no native cancel/adapter).
- **PydanticAI**: 3/3 RESOLVES.

## Connections

| Edge | Target | Note |
|---|---|---|
| grounds | I1 (no second source of truth) | octopus-evidence + Workflow SDK checkpoint + pydantic-graph state all shown subordinable, not canonical |
| grounds | I2 (freeze-before-channel) | Eve `POST /eve/v1/session` one-shot + PydanticAI one-shot output_type run on frozen input |
| derives-from | vault/ontology-conventions.md | veracity⊥conviction stance; first-hand-only evidence rule |
| pairs-with | (pending) fit-falsifier | opposing-disposition sibling; this node is confirm-fit and must not hedge toward the falsifier |
| informs | ledger appender / governTool integration | governTool wraps the appender behind the Draft-approval gate (check c) |

