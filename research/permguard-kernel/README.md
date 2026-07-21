---
tags: [orchestration, agents, permguard, lean, tool-call-confinement, portability, security]
node_type: discovery
is_session: false
session_ref: null
layer: architecture, external
nature: reference, technical
status: draft
veracity: low
conviction: low
version: 0.1.0
last_updated: 2026-07-20
---

# permguard-kernel — fit of the verified reference monitor into the orchestration substrate

> **Status:** research *brief*, pre-dispatch, **unreviewed**. This is the **plan** of the
> investigation — the framing, the lineage, and the agent structure — **not** the result.
> Nothing here has been dispatched: there is no `research.md` (explorer transcripts) nor `findings.md`
> (writer output) yet, and no ledger row. `Claim ≤ proof`: every assertion below
> about the kernel holds only as far as the sibling repo `domainspec-lean-formalization` proves; here it is
> a citation to an external source, not a local proof.

## Where this derived from

This research **derived from** [`../agent-name-selection-arch/findings.md`](../agent-name-selection-arch/findings.md)
— the only other research in the repo, and the direct thematic relative: that one decided the architecture of
a **border guard** (the agent can register a new tag, but only after deterministically
guaranteeing it does not yet exist; implemented in `tools/agent-pool-mcp/`). This one
asks about the guard of the layer below — **what each dispatched subagent may touch**
(path/host/command), which the orchestrator today does not govern in any way.

The external object of study is the **`permguard` / "Lean kernel"** in
`../../domainspec-lean-formalization/lean-engineer/`: a reference monitor verified in Lean 4
+ Mathlib (a PDP) that, given a layered policy and a tool call
(`read | write | edit | bash | webFetch | webSearch`), returns `allow`/`deny` with proven deny-precedence
and authority-intersection. It compiles to a `permguard` CLI binary (exit `0`=allow,
`1`=deny, `2`=error→**fail-closed**). Holes declared by the authors themselves: `curl` via bash
bypasses the egress guard (machine-checked negative), symlink/TOCTOU and content-based secret classification
are out of scope. There is **no** mediation layer, no MCP, no HTTP — it is an *off-path* CLI.

## The question

The orchestrator governs the **composition of the dispatch** (which agents run, with which angles, under
human confirm) but does **not** govern **capability confinement** (what each agent touches). The
`permguard` fills exactly that gap, and its six-tool vocabulary *is* the tool-set
that the subagents use. The question of this research:

> Should tool-call confinement à la `permguard` be a capability of the orchestrator's **portable**
> substrate — and, if so, what is the **minimal architecture that does not break** the read-only /
> zero-integration (H-PORT-1..5)?

The named friction the research has to resolve, not sidestep: (a) cost of building Lean+Mathlib
and a binary for **win32**; (b) head-on collision with the near-zero portability goal of the README;
(c) canonicalization (realpath, symlink, URL parsing into segments/labels) — the part that **actually**
provides security — is **unverified** and would be our own code; (d) the kernel is **not** the Lean anchor
of the categorical thesis (it is a different subpackage from `lean-formalization/`), so it discharges
nothing of OBL-E3.

## Research structure (proposed — becomes the pending sheet)

Fan-out of **3 explorers, one per corpus** (corpus-of-origin is the anti-bias axis) → **synthesizer**
(n:1, reconciles; every load-bearing assertion cites which explorer's return it came from) → **skeptic**
genuinely empowered to kill the conclusion against the collapse-tests.

| Explorer | Corpus (exclusive owner) | Angle — the question it carries |
|---|---|---|
| **internal** | `cyberalchemy-orchestrator` (hooks, dispatch schema, ledger, H-PORT-1..5) | Where would enforcement live in *our* architecture, and which portability hypothesis does it break? |
| **kernel** | `../../domainspec-lean-formalization/lean-engineer/` as **ground truth, not aspiration** | What the kernel guarantees vs. declared hole; win32 build reality + the unverified surface (canonicalization) that would be ours |
| **prior-art** | literature, **strictly bounded** | Cedar / XACML / OPA-sidecar / capability-confinement for LLM agents / "PreToolUse-hook-as-PDP" — is it already a *named* pattern? (so as not to reinvent, **not** a general survey) |

- **`anti_bias_global`:** *adoption-optimism vs. portability-conservatism* — the correlated bias
  to cancel is integration-enthusiasm ("it fits beautifully"); the skeptic is paid to
  oppose with "this violates zero-integration and the proven guarantees are conditional on our own
  unproven code".
- **`dispatch_type`:** `research`. **`final_approver`:** `parent`. **`working_folder`:**
  `research/permguard-kernel/`.

## Deliverable — a `findings.md` that answers a few sharp questions

1. Should tool-call confinement be a capability of the **portable** substrate, or does it stay outside it
   (opt-in per repo, respecting the `portability-install-principle`: repo-local, path-relative,
   env-secrets, opt-in)?
2. If so, what is the **minimal architecture that does not break read-only/zero-integration**? (a priori
   guess to falsify: opt-in `PreToolUse` hook + pre-built binary + a canonicalization
   contract.)
3. What exactly is the **unverified surface** we assume, and is it acceptable?
4. Is the pattern already **owned/named** in the literature?
5. **Go/no-go verdict:** pursue / defer / drop. If pursue, it becomes an adjacent `OBL-PORT`
   **or** it dispatches the already-specified *experiment* (the `PreToolUse` hook calling `permguard`
   blocks an out-of-policy `bash` in a real subagent, on win32, with acceptable latency, without
   breaking the read-only auto-discovery).

**Termination obligation:** the research ends in a go/no-go — not in open-ended essay. Do not collapse
research and experiment: this one answers *"is it well-posed and worth it, what is the minimal architecture?"*; the
experiment answers *"does it build on Windows and is the latency acceptable?"*.

## Out of scope

- The category mathematics (`lean-formalization/`) — a different subpackage, would only confuse.
- General "agent security" survey — the literature stays bound to prior-art-for-naming.
- Any actual build or binary — that belongs to the experiment, if the verdict is go.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| `../agent-name-selection-arch/findings.md` | `derives-from` | parent research; both are border guards — that one guards tag registration, this one guards tool-call |
| `../../domainspec-lean-formalization/lean-engineer/` | `depends-on` (external) | the verified `permguard` kernel — object of study; sibling repo, non-`[[wikilink]]` citation |
| [[ontology-conventions]] | `depends-on` | frontmatter and edge conventions this node follows |
| [[portability-install-principle]] | `depends-on` | any enforcement integration has to be opt-in / repo-local by this principle |
