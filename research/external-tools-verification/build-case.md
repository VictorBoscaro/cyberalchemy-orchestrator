---
tags: [external-tools, verification, build-case, collapser, I1, I2, EG-1, octopus-runtime, eve, pydantic-ai]
node_type: audit
is_session: false
layer: research
nature: adversarial-synthesis (collapser / build disposition)
status: complete
version: 0.1.0
last_updated: 2026-07-21
veracity: high
conviction: medium
---

# Build-Case — Collapser (BUILD)

Disposition: **collapse toward custom code**. Thesis: the two invariants —
**I1** no second source of truth, **I2** freeze-before-channel — plus the **EG-1**
single-writer gate FORCE building at every layer. Each tool's adoptable value is
either (a) exactly the interface we'd implement anyway, or (b) a feature whose
removal (to satisfy I1/I2) leaves nothing to adopt. Frozen independently; no hedge
toward adopt. Evidence cites the confirmer/falsifier notes by check.

---

## Layer 1 — effect-governance (octopus-runtime)

**Attack.** The one thing we cannot cheaply build — an *unbypassable* single-writer
seal (EG-1) — is exactly the thing octopus does **not** give. Falsifier (a):
`routeExecutes` is a boolean return, *"not a capability barrier … nothing stops a
caller importing a connector and calling `.execute()` directly"* — structural only
*on the runtime path*. That is advisory, and EG-1 promises structural. Confirmer (a)
calls it "code, not prose," but code that returns `true` is not a seal.

Everything genuinely adoptable is the interface we own regardless: falsifier (c) —
`Store`/`AuditSink`/`ApprovalGateway` are *"caller-implemented interfaces … the core
never imports an adapter."* Our appender **is** the adapter. And the subordinate
audit atom, `octopus-evidence`, is by its own README *"a primitive, not a system … no
storage, no query, no network"* (confirmer b / falsifier b) — a hash+serialize
function, ~zero code to inline. De-featuring to preserve I1 collapses octopus to that
atom; adopting the atom buys nothing a `sha256(canonical(record))` helper doesn't.

Cost side: single author, 1 star, `octopusos.ai` "patents in flight," version drift
(repo v0.3.2 vs `package.json` 0.7.0), 2026-nascent (falsifier d). Coupling EG-1 — a
constitutional gate — to a commercially-captured infant dep is the anti-pattern.

**FALSIFIER (L1):** proof that octopus's `execute` guard is a **capability barrier**
— connectors physically unreachable without a token minted by the gate, not a boolean
— *and* that the seal survives a direct connector import. That would deliver the EG-1
structural single-writer property we otherwise must build. Neither note found it;
falsifier (a) found the opposite.

## Layer 2 — runtime-host + adapters (Eve)

**Attack.** Eve fails I1 by construction. Falsifier (a): *"Workflows persist progress
as an event log and deterministically replay it to reconstruct state … the
Vercel-managed event log **is** the canonical state authority,"* platform-bound —
**FAILS**, not subordinable. Confirmer (a) can only reach RESOLVES by admitting *"no
explicit 'external journal is canonical' statement; subordination is architectural,
not enforced"* — a hedge, not enforcement. Adopt Eve and our journal + Vercel's replay
log are two canonical stores: I1 violated the moment durability is on.

De-featuring to save I1 means disabling Workflow durability — but durability/replay
**is** what Eve is. Strip it and you hold a bare `POST /session` HTTP surface, i.e.
the thing we'd build. Role also fails: confirmer (c) is **PARTIAL** — *"no native
cancel, no native CLI adapter; the start/events/result/cancel/status contract must be
app-built inside a tool."* Falsifier (c): Eve *"is the agent, not a driver of external
CLIs … wrong role shape."* We need a driver for claude-code-cli/codex-cli; Eve runs
its own model loop via AI Gateway. The adapter is custom either way. Plus platform
lock (Workflows/Fluid Compute/Sandbox) collides with the repo-local portability
principle (falsifier: relates-to Portability).

I2 is the only near-miss: subagents give *"fresh conversation history and state"*
(falsifier b, PARTIAL) — but a freeze we get by *avoiding* Eve's core session model is
not a reason to adopt it.

**FALSIFIER (L2):** proof that Eve runs with Workflow durability **disabled or
replaced** by our journal as the canonical replay source (I1 held), *and* exposes a
**native external-CLI adapter with cancel** on the 5-op contract. Then host+adapter
adopt wins. Falsifier found I1 FAILS + role FAILS; confirmer found adapter PARTIAL —
both deny it.

## Layer 3 — schemas + judgment (PydanticAI vs zod)

**Attack.** The judgment artifact we need is a **sealed, versioned, digest-bound**
record. That is not what `output_type` *is*: falsifier (a), PARTIAL — *"no native
versioning, schema-version field, immutability, or sealing/hashing guarantee … a
sealed+versioned record is hand-buildable but not what output_type is."* Confirmer (a)
concurs: *"version/digest is a caller-supplied field … not a native pydantic-ai
primitive."* So the sealing is custom whether we adopt or not.

Adopting to get the un-custom remainder costs a **Python split**: falsifier (c),
**FAILS** — Python-only, *"forces a Python process alongside the TS/JS appender +
agent-pool-mcp, a cross-language IPC/serialization boundary … an unavoidable,
load-bearing fit cost."* The runtime is TS (octopus/Eve are TS). Paying a language
boundary to obtain a validated model — when the sealing is custom anyway — is negative
value. The subordinable wins (graph state in-memory, confirmer b) only prove pydantic
is *harmless*, not *needed*. And confirmer (c) concedes the eval layer is *"runtime-
agnostic … reimplements cleanly in TS/zod"* — an admission that reimplementation is
the cheap path. Build in zod: `schema + frozen + versionLiteral + externalDigest` =
exactly the pieces both notes say you bolt onto pydantic, minus Python.

**FALSIFIER (L3):** proof that either (i) the target runtime is actually Python (Python
split is free), or (ii) `output_type` natively emits a sealed+versioned+hashed
immutable record with **no** caller composition. Then adopt is justified. Both notes
deny both: Python-only + no native sealing.

---

## Roll-up

- **EG-1 across all three:** the single-writer seal is delivered by none — octopus
  advisory (falsifier a), Eve *introduces a second writer* (its event log, falsifier
  a), pydantic inert. The writer gate is custom at every layer.
- **I1 forces build** at L2 (Eve's competing canonical log) and forces the sealing at
  L3; **I2** is satisfiable only by paths that route *around* each tool's core.
- Adoptable surface = caller-implemented ports (L1) and reimplement-in-TS admissions
  (L3) — build, by the tools' own docs.

## Connections

| edge | target | note |
|---|---|---|
| collapses | fit-confirmer (confirm-fit sibling) | inverts its RESOLVES: octopus (a) code≠seal; Eve (a) hedge≠enforcement; pydantic (a) digest is caller-supplied |
| grounds | EG-1 single-writer gate | seal delivered by none; octopus advisory, Eve adds a 2nd writer, pydantic inert |
| tests | I1 (no second source of truth) | Eve's Vercel-owned replay log = competing canonical authority (falsifier a) |
| tests | I2 (freeze-before-channel) | freeze reachable only by routing around each tool's core (Eve subagents; one-shot) |
| relates-to | Portability / install principle (MEMORY) | Eve platform-lock + octopus commercial capture vs repo-local |
| grounds | external-tool selection decision-gate | supplies the BUILD pole opposite the adopt case |
| derives-from | vault/ontology-conventions.md | veracity⊥conviction; claim≤proof, inline citation |
