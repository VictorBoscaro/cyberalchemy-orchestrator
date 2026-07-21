# research.md — permguard-kernel fit (explorer transcripts)

Dispatch `2026-07-20-permguard-kernel-fit`. Three explorers, isolated corpus (none saw the
other's corpus). Transcripts preserved; the reconciliation and the verdict live in
[`findings.md`](./findings.md).

---

## Explorer A — INTERNAL corpus (`cyberalchemy-orchestrator`)

**Where the hooks actually live (the load-bearing surprise).** The repo **has no
`.claude/settings.json` nor `.claude/settings.local.json`** — they do not exist. Every hook lives in the
**user-global** file `C:\Users\victo\.claude\settings.json`, pointing to absolute-path scripts
in `C:\Users\victo\.claude\hooks\`. The four are `PreToolUse`:

| Hook (matcher) | Script | Role |
|---|---|---|
| `^Agent$` | `remind-register-dispatch.cjs` | register-dispatch reminder |
| `^(Edit\|MultiEdit\|Write\|NotebookEdit\|Bash\|PowerShell)$` | `enforce-append-only-dispatch.cjs` | append-only ledger guard |
| `^(Write\|Edit\|MultiEdit)$` | `remind-create-skill.cjs` | skill reminder |
| `^Workflow$` | `block-workflow.cjs` | hard tool block |

**Candidate attachment points:**

| Point | Pros | Cons |
|---|---|---|
| **PreToolUse hook (user-global settings)** — where `enforce-append-only-dispatch` already runs | Exact mechanism permguard needs; a path-scoped deny PDP over Bash/Edit/Write **is already proven working here** | Machine-global, absolute Win paths, does not ship with the repo; runs in the caller's process, not confined per-subagent |
| **`.claude/settings.json` repo-local** (does not exist) | Would make the hook opt-in + repo-local (`portability-install-principle`) | Net-new integration surface; nothing repo-local exists today |
| **Dispatch schema / `append-dispatch.cjs`** | Could carry a per-agent capabilities manifest at confirm | Strictly closed schema (unknown-key → exit 2); governs *composition*, not *runtime* |
| **`agent-pool-mcp`** | Already the repo's "border guard" — thematic parent | MCP is off-path; does not intercept the bash/edit path |
| **Control plane `implementations/server/`** | Central, multi-repo | Read-only by design; making it enforce would break read-only |

**Capability gating already exists:** `enforce-append-only-dispatch.cjs` is a working content-inspecting
PreToolUse PDP (blocks writes to the ledger); `block-workflow.cjs` is a general block;
`~/.claude/settings.json` `permissions.deny` denies `PowerShell` and ~18 `Agent(gsd-*)` subagents
by name. A permguard **generalizes a pattern the repo already runs**.

**Per-portability-hypothesis verdict:**
- **H-PORT-1 (Substrate ⊥ domain): SURVIVES.** Domain-independent hook; does not touch vault/FRAMINGS/definitions.
- **H-PORT-2 (schema is the only contract): SURVIVES with an asterisk.** Observation still keys on `telemetry/agents/` + `schema_version`, but enforcement introduces a *second* contract (policy file) that is not the ledger schema — orthogonal, does not break, but it is no longer "just the schema".
- **H-PORT-3 (read-only = zero-integration): BREAKS.** Enforcement is inherently on-path: a PreToolUse hook needs to run *on the target* to intercept and emit allow/deny. That is instrumentation on the target — the opposite of disk-only observation.
- **H-PORT-4 (single vocabulary, N consumers): SURVIVES.** Permguard's 6 tools are disjoint from the `agent_name` pool.
- **H-PORT-5 (skills copy-in, config-free): BREAKS.** The current hooks already falsify config-free for enforcement — they need entries in the user-global `settings.json` with absolute paths + pre-built `.cjs`; they are not copy-in today. permguard adds `settings.json` wiring + per-platform binary → needs an installer, exactly the `OQ-PORT`.

**Honest fit:** it fits the border-guard lineage and reuses a mechanism the repo already operates,
but it directly contradicts the "read-only / zero-integration / copy-in config-free" pillar —
enforcement is on-path by nature (breaks H-PORT-3) and cannot be pure copy-in (breaks
H-PORT-5). Viable framing = the brief's own guess: an **opt-in, repo-local** hook, not a
default substrate capability.

---

## Explorer B — KERNEL corpus (`domainspec-lean-formalization/lean-engineer/`)

Ground truth. All theorems close with `#print axioms` (no `sorry`).

**PROVEN:** `decidePolicy_sound` (soundness); `deny_precedence` (any layer that forbids ⇒
`.deny`); `add_layer_restricts` (more layers only narrow — no-escalation); `layered_not_flattenable`
(∃ P r where it differs from Cedar flatten — "not a re-skin of Cedar"); `decidePolicy_append_allow`
(`allow(P++Q) ⇔ allow(P) ∧ allow(Q)`); `normalize_clean` + `normalize_idempotent` (`..` defense
as a theorem); `read_confined`/`write_confined`/`edit_confined` (confinement); egress
`hostMatchesSuffix` label-granular + scheme-equality.

**The machine-checked NEGATIVE (honesty exhibit):** `bash_egress_bypass` — `∃ S P hist r,
traceTaint = .secret ∧ r.tool = .bash ∧ egressGuard = .allow`. A `curl` via bash **provably**
bypasses the egress/taint guard; `webfetch_still_denied` shows the identical `webFetch` being denied.
"Protection is exactly as wide as the `isEgress` catalog, not one tool more."

**DECLARED holes (trusted, not proven):** URL-parse (`https://api.github.com@attacker.com/`),
IDNA/punycode, percent-encoding, DNS-rebinding/IP-literal (`169.254.169.254`), bash-routed curl;
content-based secret classification **explicitly NOT done** (secret sources are a
declared path-prefix in the policy); realpath/symlink, TOCTOU, case-fold+NFC, shell quoting.

**Build:** toolchain `leanprover/lean4:v4.30.0-rc2`; Mathlib pinned `rev 388f44f…`. `lake exe
cache get` then `lake build`; binary at `.lake/build/bin/permguard`.

**Canonicalization / trust border:** the kernel **does no canonicalization at all**. The CALLER
pre-computes everything; the guarantee only holds for what the parser produces (banner "UNVERIFIED TRUST
BORDER"). Path → pre-sliced into segments, `parseStringList` rejects `/` inside a segment;
host → pre-sliced into labels, `parseHostLabels` rejects an embedded `.`. realpath/URL/DNS never
done, never verified. "The only bug ever found was a fail-open at the border."

**CLI contract:** `permguard [--explain] <policy.json> <request.json> [<history.json>]`. Fail-closed
exit: **0 allow, 1 deny, 2 parse/border error** (never default allow). The 3rd arg + `secretSources`
in the policy turns on the `egressGuard` trace mode (Rung 5). An empty `layers` is REJECTED (`decidePolicy []
= allow` would be fail-open).

| Concern | KERNEL guarantees | YOUR (caller) responsibility |
|---|---|---|
| Deny precedence / layer composition | theorems | — |
| `..` traversal | `normalize_clean` (theorem) | pre-slice path into segments, no `/` in the segment |
| Path confinement | `read/write_confined` | realpath/symlink, TOCTOU, case-fold/NFC |
| Egress host | `hostMatchesSuffix`, scheme-eq | URL parse, IDNA/punycode, DNS-rebind/IP-literal |
| Bash curl egress | PROVEN to BYPASS | catalog/block bash sinks yourself |
| Secret classification | none (only declared prefixes) | label content, no laundering, faithful trace |
| Bad input | fail-closed exit 2 | the JSON parser is the unverified trust border |

**Biggest build/win32 risk:** the pinned Mathlib `388f44f…` over `lean4:v4.30.0-rc2` — if
`lake exe cache get` has no pre-built oleans for Windows, `lake build` compiles Mathlib from
scratch (an hours-long build): the primary practical blocker to adoption. No win32 guards in
`IO.FS.readFile`; the kernel treats path segments abstractly (no OS-path awareness),
so all Windows path/case-fold/separator concerns are pushed onto the caller
as declared unverified holes.

---

## Explorer C — PRIOR-ART corpus (literature, bounded)

**PDP/PEP split** → owned outright by **XACML/ABAC** (origin of the PEP/PDP/PAP/PIP vocabulary;
NIST SP 800-204B is the modern restatement). 20-year-old terminology; **cite, do not mint**.

**Reference monitor mediating an agent tool-call via pre-tool hook:**
- **Cedar / Amazon Bedrock AgentCore Policy** — Cedar (AWS, Rust, CNCF) applied to agent tool
  authorization; Gateway PEP between agent and tools, default-deny; + **Cedar Analysis** (symbolic /
  automated-reasoning validation of the policy). The closest owned incumbent.
- **OPA / Rego sidecar** — the modern de facto PDP; **OPA Guardrails (TrueFoundry)** already wires OPA to
  **MCP pre-tool hooks**. "OPA as PDP for agent tool-call via pre-tool hook" already exists named.
- **ScopeGate** — a named 5-stage PDP/PEP for agent tool-calls (scope, authz,
  money-ceiling, idempotency, default-deny), out-of-band before side effects. Nearly identical framing.
- **Microsoft "Authorization Fabric" / Securing MCP** — agent calls PEP/PDP before executing →
  ALLOW/DENY/REQUIRE_APPROVAL/MASK.
- **"Capability Gates Are Not Authorization"** — confused-deputy in LangChain/LlamaIndex; argues
  for a per-call fail-closed deterministic gate.

**Capability confinement / reference monitor of agent effects:** **seL4** (formally verified
capability microkernel, being pitched as a substrate "for agents"); **Agent libOS**
("acts as a **reference monitor** for agent effects"); a containment proof line
(formal-skill-verification, revocable capabilities, PARseL).

**Explorer VERDICT:** *mostly owned, not a naming gap — with one genuinely
open seam.* (1) PDP/PEP → owned by XACML. (2) Reference monitor mediating a tool-call via pre-tool hook
→ already named and shipped several times (Cedar/AgentCore, OPA Guardrails, ScopeGate, MS Authorization
Fabric) — **adopt/cite**, do not reinvent. (3) Capability confinement → owned by seL4/Agent-libOS.
**The one un-owned combination:** a *formally **verified** decision kernel (proof-carrying
PDP)* wired to a **PreToolUse-style PEP**, *specifically for agent tool-calls*. The pieces
exist separately (Cedar Analysis gives symbolic validation but AgentCore's enforcement is not a verified
kernel; seL4/PARseL give verified confinement at the OS/skill level, not at the tool-call PDP).
No one has clearly nailed the intersection "verified PDP ⋈ PreToolUse PEP for LLM tool-calls".

> **Strategist note (not the explorer's):** several arXiv IDs in the prior-art return have
> implausible/future dates (e.g.: `2606.*`, `2605.*`). The anchors that carry the argument — Cedar,
> XACML/NIST, OPA — are solid and verifiable; the specific arXiv papers are marked
> **to-verify** and must not, on their own, sustain any load-bearing claim of the findings.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| `./findings.md` | `derives` | the findings reconcile these three transcripts into a go/no-go verdict |
| `./README.md` | `derives-from` | the brief that specified this research |
