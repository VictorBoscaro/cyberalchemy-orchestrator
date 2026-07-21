---
tags: [permguard, lean-kernel, reference-monitor, tool-call-confinement, portability, architecture]
node_type: discovery
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-07-20
timestamp: 2026-07-20T23:07:29-03:00
expires: 2026-09-18
conversation_id: unknown
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 6
importance_rationale: "Closes a live architecture question with a load-bearing skeptic correction and sets an explicit null hypothesis for any future permguard reconsideration, but changes no code and blocks nothing in flight."
---

# permguard-kernel fit — DEFER-as-disproof-attempt

## Summary

The session evaluated whether the permguard / "Lean kernel" in the sibling repo
domainspec-lean-formalization could integrate with the orchestrator. A reactive Explore agent
established that "lean-kernel" is a Lean 4 + Mathlib verified reference monitor (a PDP) for agent
tool-calls, shipped as an off-path CLI binary (`permguard`). The question was formalized as a
governed research — not an experiment first — scoped to internal repo + sibling repo + bounded
literature and required to end in a go/no-go. A research brief was authored at
research/permguard-kernel/README.md as a discovery node deriving from
research/agent-name-selection-arch. After the user flagged that no research/findings artifacts
existed, the dispatch (2026-07-20-permguard-kernel-fit) was actually run: three corpus-isolated
explorers → synthesizer → skeptic, registered and closed in the ledger. The synthesizer concluded
DEFER→fire-experiment, but the skeptic materially corrected it by finding the incumbent
enforce-append-only hook is machine-global, not repo-local, invalidating the "generalize what we
already run" framing. The final verdict, written to findings.md, is DEFER-as-disproof-attempt: keep
permguard out of the portable substrate and out of OBL-PORT. The null hypothesis the Lean kernel
must beat is "the existing JS deny PDP, once made repo-local, is sufficient." The grounding: the
kernel does zero canonicalization, so all residual risk (realpath/symlink/TOCTOU/Windows case-fold
+ a proven bash-egress bypass) is unverified caller-side code we would own, and the win32 Mathlib
build is the practical adoption blocker. Prior art (Cedar/AgentCore, OPA Guardrails, ScopeGate,
XACML) already owns the pattern except the thin verified-PDP × PreToolUse-PEP seam.

## Open questions

- Whether the verified-PDP × PreToolUse-PEP seam is a thin-but-real contribution worth building an
  artifact around, or too thin to justify any Lean/Mathlib cost at all — the research kept the probe
  alive but did not decide it is worth pursuing.

## Recommendation

Keystone: the cheapest discriminator, not the biggest build. If a future session pursues permguard,
write the caller-side Windows path canonicalizer and diff its guarantee against
enforce-append-only-dispatch.cjs *before* any Lean/Mathlib build — if the kernel protects nothing the
JS hook cannot, that is learned in an afternoon without touching Lean. Licensed by findings.md's
verdict and the skeptic's grounded correction that the incumbent hook is machine-global, not
repo-local (so the "generalize what we run" onramp does not exist yet); the outcome — kernel earns
its build cost, or DROP-kernel/KEEP-JS — remains undecided.

## Files touched

- research/permguard-kernel/README.md
- research/permguard-kernel/research.md
- research/permguard-kernel/findings.md
- telemetry/agents/subagents-dispatch.yaml
