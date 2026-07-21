# findings.md — permguard-kernel fit

**Verdict: DEFER-as-attempt-at-refutation (not DEFER-as-onramp).** Do not mint `OBL-PORT`;
do not make confinement a capability of the portable substrate. Keep a live probe **only** because the
seam "verified PDP ⋈ PreToolUse PEP for tool-calls" is genuinely un-owned — but running
with an explicit null hypothesis: *the JS deny PDP the repo already runs, once made repo-local, is
sufficient; the Lean kernel has to **earn** its build cost by protecting something the JS hook
provably cannot.* If it does not earn it, the honest outcome is **DROP-the-kernel / KEEP-the-JS-hook**.

Reconciliation of three explorers with isolated corpus (A=internal, B=kernel, C=prior-art), attacked by
a skeptic. Transcripts in [`research.md`](./research.md).

---

## The 5 questions

**Q1 — Capability of the portable substrate, or opt-in per repo?**
Opt-in per repo, **not** default capability. Confinement is *on-path* — it needs to run on the target to
intercept tool-calls, the opposite of disk-only read-only observation (A: **H-PORT-3 BREAKS**). And it is not
config-free: the current hooks themselves already falsify "skills copy-in config-free", requiring
`settings.json` + absolute-path `.cjs`; permguard adds wiring + per-platform binary (A:
**H-PORT-5 BREAKS** → needs an installer = `OQ-PORT`). H-PORT-1 and H-PORT-4 survive; H-PORT-2
survives with an asterisk (enforcement introduces a 2nd orthogonal contract, the policy file).

**Q2 — Minimal architecture that does not break read-only/zero-integration?**
Strictly additive and present only in repos that opt in: **PEP** = PreToolUse deny hook; **PDP** =
permguard CLI (`exit 0 allow / 1 deny`, fail-closed) (B); **placement** = a `.claude/settings.json`
**repo-local** (which **does not exist today**) so the wiring is opt-in and ships with the repo. Control plane
and schema/appender stay untouched. Zero-integration preserved *for those who do not opt in*; for those who opt in,
the read-only pillar is locally and consciously abdicated.

**Q3 — Unverified surface assumed, is it acceptable?**
The proven core is strong and `sorry`-free (deny-precedence, no-escalation, non-flattenable,
read/write/edit confinement, `..` as a theorem, egress by label) (B). But what is **assumed** is the *unverified
trust border*, and it is substantial: **the kernel does no canonicalization at all** — realpath/symlink,
TOCTOU, Windows case-fold/NFC are declared holes, pushed onto the caller; "the only bug ever
found was a fail-open at the border" — the residual risk lives **100%** exactly where we would integrate
(B). Machine-checked negative: `curl` via bash **provably** bypasses the egress guard, and this repo
dispatches subagents with Bash (B). **Acceptable only** if scoped to write/edit confinement **with a
Windows canonicalizer on our side**, and explicitly **not** sold as network control.

**Q4 — Is the pattern already owned/named?**
Mostly owned — **not a naming gap** (C). PDP/PEP = XACML/ABAC (cite, do not mint).
Reference monitor via pre-tool hook for agent tool-calls = already shipped: Cedar/Amazon Bedrock
AgentCore (+ Cedar Analysis), OPA Guardrails in MCP pre-tool hooks, ScopeGate, MS Authorization
Fabric. Capability confinement = seL4 / Agent libOS / PARseL. **The one un-owned seam:** a
*formally verified* decision kernel (proof-carrying PDP) wired to a PreToolUse-style PEP,
*specifically for LLM tool-calls* (C). *(Caution: several arXiv IDs in the return have implausible
future dates — to-verify; Cedar/XACML/OPA are solid.)*

**Q5 — Verdict.** DEFER demoted (below).

---

## The correction that changed the verdict (skeptic's finding)

The synthesizer framed the experiment as *"generalize the `enforce-append-only-dispatch.cjs` that the
repo already runs"*. **This is a factual error.** That hook **is not repo-local and does not ship with the repo** — the
repo has no `.claude/settings.json`; the four PreToolUse hooks live in the **machine-global** `settings.json`
pointing to absolute-path scripts in `~/.claude/hooks/` (A). So the
experiment secretly packages **two** net-new moves: (1) create a **repo-local** enforcement seam
that does not exist today, and (2) swap a working JS PDP for a Lean-kernel PDP.
The Lean question is hitching a ride on an unrelated portability refactor. By the
`portability-install-principle`, move (1) is the real, necessary and **build-free** work; the
kernel is a passenger.

**Why "verified" is decorative here, if nothing changes:** the kernel buys deny-precedence /
no-escalation / `..`-as-theorem — none of which is a risk we have evidence of losing in a
~250-line JS deny hook. All the residual risk (canonicalization + egress via bash) is **our own
unverified code** anyway. The adjective "verified" adds a per-platform binary
+ hours-long Mathlib build + a 2nd contract (policy file) to harden a component that
**is not where the breaches occur**. And `append-dispatch.cjs` already writes path canonicalization by hand
in JS (strip `./`, case-insensitive `vault/` guard) — we are already competent and responsible for the only
part that fails.

**Capability in search of a requirement:** minus egress (proven bypass), the only in-scope use is
write/edit confinement — and the repo's *demonstrated* need (append-only protection of the ledger)
is already solved, build-free, by the existing deny PDP. No dispatch artifact names a write-confinement
threat that the JS hook cannot express. An experiment with no falsifiable win condition
is not an experiment.

---

## Recommended action — the experiment, with gates reordered

If pursued, **reorder the gates** and make the null hypothesis explicit:

1. **Gate 1 (cheap, first):** write the **caller-side Windows canonicalizer** and
   **diff** its guarantee against the existing JS guard. If all the residual risk lives there and is
   unverified JS anyway, the kernel adds no guarantee — and you learn this in an afternoon,
   **without touching Lean/Mathlib**.
2. **Gate 2 (only if Gate 1 passes):** the win32 Mathlib build probe (`lake exe cache get`; if there are
   no pre-built oleans for Windows, an hours-long build — the primary practical blocker) (B).
3. **Scope:** write/edit confinement only, opt-in, repo-local, **excluding** any egress claim.
4. **Null hypothesis to refute:** *"the JS deny PDP, once repo-local, is sufficient; the Lean kernel
   must earn its build cost by protecting something the JS hook provably cannot."*

Ordering the build first spends the most (hours of Mathlib) to learn the least.

## Mandatory caveat

The incumbent `enforce-append-only-dispatch.cjs` is **machine-global, not repo-local, and does not ship with
the repo** — any "generalize what we already run" framing is invalid until a repo-local
enforcement seam exists. The kernel's proofs cover **none** of the residual risk: canonicalization
(realpath/symlink/TOCTOU/case-fold/Windows NFC) and egress via bash are unverified caller
code we own, and the only bug ever found in permguard was a fail-open at exactly that
border.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| `./research.md` | `derives-from` | the findings reconcile the three explorer transcripts |
| `./README.md` | `derives-from` | the brief that specified this research |
| [[portability-install-principle]] | `depends-on` | the verdict rests on: enforcement is opt-in/repo-local, never default substrate |
