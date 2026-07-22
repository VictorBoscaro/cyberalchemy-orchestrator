---
tags: [external-tools, verification, adopt-case, constructor, octopus-runtime, eve, zod, pydantic-ai]
node_type: decision-input
is_session: false
layer: research
nature: constructor disposition (smallest-adoption case)
status: draft
version: 0.1.0
last_updated: 2026-07-21
veracity: high
conviction: medium
depends_on: [fit-confirmer.md, fit-falsifier.md]
---

# Adopt-Case — Constructor / Smallest Adoption

Disposition: **CONSTRUCTOR / ADOPT**. Per layer, the smallest adoption that satisfies **I1** (no second source of truth), **I2** (freeze-before-channel), **EG-1** (single validated writer of the audit ledger). claim≤proof: every line cites confirmer (CF) or falsifier (FL). Where a check FAILS I concede it; I do not adopt around it. Frozen independently of any build case.

## Layer 1 — effect-governance: **octopus-runtime** (adopt, narrow)

**Adopt:** `governTool` + the caller-implemented `ports.ts` interfaces (`Store`, `AuditSink.append/query`, `ApprovalGateway`) + the `octopus-evidence` primitive.

- **I1 — RESOLVES (both notes agree).** Ports invert the dependency: "the core depends on these interfaces; adapters depend on the core" (FL c); octopus-evidence "has no storage, no query, no network … subordinate to an external event journal" (CF b, FL b). Our appender drops in as the `AuditSink`/`Store` adapter, staying subordinate. This is the whole reason to adopt: a ready-made subordinable audit port + a zero-dep trace atom.
- **EG-1.** `governTool` wrapping our appender as `fn` makes one governed path the writer (CF c). But I adopt the **falsifier's** reading of the guard, not the confirmer's: it is **advisory, not a sealed capability barrier** — "nothing stops a caller importing a connector and calling `.execute()` directly" (FL a, PARTIAL). Conceded. Therefore EG-1's single-writer property is **not** delivered by octopus; it must be enforced by us — the governTool-wrapped appender is the *only* module permitted to import the ledger writer (single-import lint), and octopus supplies structure, not the seal.
- **Would NOT build:** our own draft/approval routing, our own evidence hashing atom, our own inward-pointing port set. **Would NOT claim:** that octopus's guard is an unbypassable seal (FL a).

## Layer 2 — runtime-host + adapters: **do NOT adopt Eve**; build a repo-local subprocess adapter

- **I1 — FAILS for Eve. Conceded, not worked around.** "Workflows persist progress as an event log and deterministically replay it to reconstruct state" — the Vercel-managed log **is** the canonical state authority, platform-bound, "not subordinable to our appender" (FL a, FAILS). The confirmer's RESOLVES rests only on the softer eve.dev checkpoint framing and self-notes "subordination is architectural, not enforced" (CF a). Between an enforced-competing-authority quote and an unenforced-architectural hope, the falsifier's direct §Durability quote governs. I adopt FL.
- **Role — FAILS.** Eve "is the agent, not a driver of external CLIs" (FL c); no native start/events/result/cancel/status contract over claude-code-cli/codex-cli. Even the confirmer concedes the adapter "must be app-built inside a tool" with "no first-hand cancel" (CF c, PARTIAL). Both notes agree the adapter is not provided.
- **Smallest adoption = none.** Build the thin 5-op subprocess adapter ourselves against the two CLIs. This is the one place a build is unavoidable *and* correct: a local subprocess emits **no** competing event log (satisfies I1) and a one-shot `spawn` on a frozen snapshot satisfies **I2** directly (no Vercel replay, no shared history). Aligns with the repo's portability/repo-local principle; Eve's Vercel platform-lock collides with it (FL d).
- **Would NOT build:** a durable session-replay log of our own — that would re-import the very I1 violation we rejected Eve for.

## Layer 3 — schemas + judgment: **adopt zod, not PydanticAI**

- **I1 — RESOLVES for both candidates** (output is inert data; pydantic-graph/zod state in-memory, persistence opt-in — CF b, FL b). Not the deciding axis.
- **Deciding axis = fit-cost.** PydanticAI is Python-only; adopting it "forces a Python process alongside the TS/JS appender + agent-pool-mcp … an unavoidable, load-bearing fit cost" (FL c, FAILS). Conceded. The runtime is TS, so zod is the native choice — and the confirmer itself says the typed cases/evaluators "reimplement cleanly in TS/zod" (CF c) and that version/digest is "caller-supplied … not a native pydantic-ai primitive" (CF a). PydanticAI's `output_type` is "not a sealed/versioned record natively" (FL a, PARTIAL) — so its one edge over zod is illusory: **either** tool needs a hand-built freeze wrapper.
- **Adopt:** a zod schema for the judgment record + a thin frozen wrapper = zod parse ⊕ version literal ⊕ external digest. The digest atom is **octopus-evidence** (Layer 1) — the record→trace binding I1 wants, subordinate to the journal.
- **Would NOT build/adopt:** a Python bridge, pydantic-graph, pydantic-evals. **Would NOT claim:** that any `output_type`/schema tool gives sealing for free (FL a).

## Roll-up

Adopt octopus (ports + evidence atom, guard treated as advisory) · reject Eve, build a repo-local one-shot subprocess adapter · adopt zod with a hand-built freeze+digest wrapper. EG-1's single writer = the governTool-wrapped, single-import appender receiving a zod-validated, evidence-sealed record, invoked one-shot by the local adapter.

## Connections

| edge | target | note |
|---|---|---|
| adopts | octopus-runtime governTool + ports + octopus-evidence | narrow: subordinable AuditSink + zero-dep trace atom (CF b/c, FL b/c) |
| concedes | FL a (octopus guard advisory) | guard is not the EG-1 seal; single-import lint is |
| rejects | Eve | I1 FAILS (Vercel event log = competing authority) + role FAILS (FL a/c) |
| builds | repo-local 5-op subprocess adapter | the app-built adapter both notes concede is absent (CF c, FL c) |
| adopts | zod + freeze/digest wrapper | over PydanticAI; Python-split FAILS on fit-cost (FL c) |
| binds | Layer-3 record digest ↔ Layer-1 octopus-evidence | record→trace seal, journal-subordinate (I1) |
| enforces | EG-1 single writer | governTool-wrapped, single-import appender |
| relates-to | Portability / install principle (MEMORY) | repo-local adapter over Vercel platform-lock |
| pairs-with | fit-confirmer, fit-falsifier | takes FL on Eve-I1 and octopus-guard; takes CF+FL agreement on I1 subordinability |
| grounds | external-tool selection decision-gate | constructor input alongside the two audits |
