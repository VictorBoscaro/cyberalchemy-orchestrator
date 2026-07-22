---
canonical_kind: discovery
node_type: readme
is_session: false
layer: architecture, application
nature: reference
status: draft
version: 0.1.0
last_updated: 2026-07-21
created: 2026-07-21
title: External tools — build-vs-adopt for the orchestration runtime (Front 3)
description: >
  Orientation index for a discovery area that evaluates external, off-the-shelf runtimes against
  the already-specified communication/deliberation infrastructure (Front 3 / HYP-ORCH-INFRA),
  to decide — per layer — what to build and what to adopt. Three candidates are on the table:
  Eve (durable TS agent runtime), PydanticAI (typed Python agent framework), and octopus-runtime
  (governed-execution TS gate). This README says what the area is and how to proceed; it is not a
  verdict and not a commitment. Every characterization here is conversation-derived and awaits
  first-hand verification.
evidence_for: [Research, Discovery]
tags: [external-tools, build-vs-adopt, orchestration-infra, runtime, bus, eve, pydantic-ai, octopus-runtime, portability]
question: >
  For each layer of the Front-3 runtime (deliberation kernel, runtime host + adapters, effect
  governance, schemas), is there an off-the-shelf tool that can be adopted without breaking the
  design's hard invariants — and where does building remain irreducible?
---

# External tools — build-vs-adopt for the orchestration runtime

> **Status:** `draft`, unreviewed orientation index. This is a **landing area**, not a decision:
> it parks the tool-scouting done in conversation so it can be verified, tensioned, and turned into
> a real research + discovery. `Claim ≤ proof`: every tool characterization below was drawn from a
> single web page read by a small model — it is **second-hand** and **must be re-verified
> first-hand** before any discovery rests on it. Nothing here selects a tool, and nothing here is
> built.

## What this is

Front 3 of [`docs/PLAN.md §3.3`](../../PLAN.md) — the **communication / deliberation
infrastructure** — is already specified on paper:
[`docs/features/agents-communication-infra/README.md`](../../features/agents-communication-infra/README.md)
and [`vault/hypothesis/orchestration-infra.md`](../../../vault/hypothesis/orchestration-infra.md)
(HYP-ORCH-INFRA). It is a governed, event-sourced runtime with a deterministic kernel, a
reveal barrier (freeze-before-the-channel), disjoint-authority stores, and a single validated
writer — **not** a generic message broker.

The question this area answers is narrower than "which agent framework": it is **build-vs-adopt,
per layer**. The design decomposes into layers with very different shapes, and an off-the-shelf
tool that fits one layer may actively fight another. This folder exists to test each candidate
against the layer it claims to serve **and** against the design's hard invariants — before a line
of runtime is written.

## The organizing lens — four layers

Worked out in conversation (2026-07-21); the map, not the verdict:

| Layer | What it is | Adoptable? |
|---|---|---|
| **Deliberation kernel** | phase machine `collect → reveal → deliberate → vote → commit`, the **reveal barrier**, the event journal (CAS / idempotent / replay-pure), disjoint authority | **Irreducibly custom.** No agent framework provides the barrier or the disjoint-authority journal; this is the anti-noise core. Gated by Wave W0 / EG-1. |
| **Runtime host + adapters** | drives `codex-cli` / `claude-code-cli` (the §4.4 5-op `AgentAdapter`), durability/recovery, channels, sandbox, schedules | **Candidate: adopt.** |
| **Effect governance** | the write-boundary + human gate (Phase-2 `confirm` → Fire = Draft → Autonomous), effect dedup, approval TTL | **Candidate: adopt.** |
| **Schemas** | `DispatchSpec`, event envelope, sealed judgment records (§5.3) | **Adopt a schema lib** (Pydantic if Python, zod if TS). |

## Candidates on the table

⚠ **All rows are second-hand** (one small-model web read each) and carry the magnifying-glass caveat
of [`docs/features/ui-studio/README.md`](../../features/ui-studio/README.md): they are the *reason to
verify*, not the verification. First-hand confirmation is the first task (see "How to proceed").

| Tool | What it claims to be | Layer it fits | Standing so far (unverified) |
|---|---|---|---|
| **octopus-runtime** (github.com/octoryn) | governed execution; autonomy levels Observe/Shadow/Draft/Autonomous; TS/Node, zero-dep, tamper-evident audit | **Effect governance** | Best-scoped of the three. Maps almost 1:1 onto the deliberately-`disabled` Phase-2 gate; could make **EG-1 structural** instead of by-discipline — directly targeting the enum-drift (Collapse-test 2). Explicitly **out of scope**: bus, orchestration, adapters, structured output. |
| **Eve** (eve.dev) | durable TS agent runtime; filesystem-first; subagents, tools, skills, channels, sandbox, schedules, MCP | **Runtime host + adapters** | Strong on the host/adapter layer; TS matches the appender/pool/MCP and the portability principle. Two risks: its Workflow SDK durability must be **subordinated** to the journal (not a second source of truth); its default conversation-history sharing fights the reveal barrier. |
| **PydanticAI** (ai.pydantic.dev) | typed Python agent framework; structured outputs, model-agnostic, pydantic-graph, Logfire | **Schemas + judgment stream** (and API adapter) | Strong on typed sealed judgments (noise-measurement substrate) and API adapters. Cost: Python — re-introduces a language split beside a TS runtime; its distinctive value (typed evals) is refoldable into zod if the host is TS. |

## Two invariants every candidate must survive

These are cross-cutting; they are why "it's a nice agent framework" is not enough:

1. **No second source of truth.** The design's spine is disjoint authority + one validated writer
   (EG-1) + *bus-as-projection*. A tool with its own durable store or audit primitive (Eve's
   Workflow SDK, octopus's `octopus-evidence`) must be **subordinated** to the event journal /
   appender, never allowed to become a competing authority — else it fails
   [HYP-ORCH-INFRA](../../../vault/hypothesis/orchestration-infra.md) **Collapse-test 1** (authorities
   overlap) or **2** (write boundary bypassed).
2. **Freeze before the channel.** Generic agent frameworks default to sharing conversation history
   — which is exactly the anchoring channel the reveal barrier exists to kill. Any adopted tool runs
   **deliberately de-featured** in the `collect` phase (one-shot, frozen snapshot, no shared
   history).

## The gate (non-negotiable)

Nothing here is adopted **as a writer** before Wave W0 clears the single-writer boundary and the live
enum-drift ([`vault/audit/ledger-enum-drift-finding.md`](../../../vault/audit/ledger-enum-drift-finding.md),
[`vault/constitution/engine-constitution.md`](../../../vault/constitution/engine-constitution.md) EG-1
at `veracity: medium`). Until then this area produces **research, verification, and read-side probes
only** — the same discipline the [agent-assertion-capture](../agent-assertion-capture/README.md)
discovery follows.

## Scope

- **In scope:** first-hand verification of the three tools' real capabilities; mapping each to the
  layer it serves; testing each against the two invariants + the gate; a build-vs-adopt
  recommendation per layer.
- **Out of scope:** building the kernel/journal/barrier (irreducibly custom); choosing a tool as a
  ledger writer (gated); the categorical thesis (Fronts 1–2).

## How this folder will be organized

```text
docs/discovery/external-tools/
  README.md                     ← this orientation index
  <tool>/                       ← one first-hand verification note per candidate (planned)
  external-tools.md             ← the landing discovery, once the tools are verified (planned)
```

The paired research (if run) lands under
[`research/external-tools-verification/`](../../../research/) and is cited here, mirroring how the
UI-studio discovery cited its verification sweep.

## Connections

| Document | Edge | Why |
|---|---|---|
| [HYP-ORCH-INFRA](../../../vault/hypothesis/orchestration-infra.md) | `evaluates-tools-for` | The specified Front-3 runtime whose layers these tools are measured against. |
| [`docs/features/agents-communication-infra/`](../../features/agents-communication-infra/README.md) | `depends-on` | The bus/kernel/adapter contract (§4.4, §5) each candidate is tested against. |
| [`vault/constitution/engine-constitution.md`](../../../vault/constitution/engine-constitution.md) | `governed-by` | EG-1 (single validated writer) — the invariant octopus could make structural and that every candidate must not violate. |
| [`vault/audit/ledger-enum-drift-finding.md`](../../../vault/audit/ledger-enum-drift-finding.md) | `blocked-by` | The live counterexample gating any adopted writer (Wave W0). |
| [`docs/PLAN.md §3.3`](../../PLAN.md) | `derives-from` | Front 3, the substrate this area shops for. |
| [agent-assertion-capture](../agent-assertion-capture/README.md) | `sibling` | The other open discovery under the same gate and the same disjoint-authority design. |
