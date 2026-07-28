---
tags: [codex-hooks, agent-provenance, host-runtime, telemetry-ledger]
artifact_kind: session
layer: task
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
timestamp: 2026-07-27T12:55:18-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agent-provenance-telemetry/integration/stage-f/codex-namespaced-hook-matcher-repair-receipt.md
  - docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md
  - docs/features/agents-communication-infra/WORK-PACK.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session identifies a host-runtime coverage defect that blocks trustworthy subagent provenance and records the staged remediation plus its proof gate."
---

# Codex hook host-binary remediation

## Summary

The session began by running the required read-only Codex hook smoke before resuming Phase A. The helper returned its marker, but no new hook state, ledger open/close pair, `dispatch_links` row, or workflow binding appeared; the ledger hash and counts remained unchanged. Trust configuration, hook feature enablement, matcher normalization, and the pilot process were checked and did not explain the missing event. Host logs instead showed the embedded Codex `0.146.0-alpha.3.1` executing `collaborationspawn_agent` without entering the generic `PreToolUse` hook path. This contradicts the prior handoff's working assumption that a fresh trusted session was the only remaining condition. Official later source and the upstream function-tool hook-default correction support treating the embedded host binary as the defective boundary. Codex `0.146.0-alpha.10.1` was installed at user scope, selected through VS Code's `chatgpt.cliExecutable`, and passed strict configuration diagnostics. Phase A remains blocked until VS Code reloads that binary and a fresh smoke proves matching state, ledger, and SQLite evidence.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Host-hook repair and Phase A handoff](2026-07-26-1506-host-hook-repair-and-phase-a-handoff.md) | `contradicts` | The observed fresh-session smoke refutes the handoff's assumption that session freshness, rather than host function-tool hook coverage, was the remaining blocker. |
| [Mandatory host wrapper](../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md) | `validates` | The missing provenance evidence demonstrates why a host must prove that multi-agent tool calls traverse the fail-closed hook boundary. |
| [Agents communication infrastructure work pack](../docs/features/agents-communication-infra/WORK-PACK.md) | `is-part-of` | This bounded remediation is part of the work pack's host-bus integrity prerequisite for Phase A. |

## Open questions

- After the VS Code window reloads, does Codex `0.146.0-alpha.10.1` emit `PreToolUse` for `collaboration.spawn_agent` and complete the matching close lifecycle?

## Next steps

1. Reload the VS Code window so the configured replacement Codex binary becomes the active extension host.
2. In a fresh trusted session, run exactly one read-only `collaboration.spawn_agent` smoke.
3. Verify a new hook-state record, matching YAML ledger open and close, the expected `dispatch_links` delta, and no lingering open state; require a workflow binding only when the smoke is workflow-bound.
4. If the smoke passes, update the host-runtime status and resume Phase A; if it fails, keep Phase A stopped and treat multi-agent hook coverage as an upstream host blocker.

## Recommendation

Reload the VS Code window and make the single read-only smoke the next action. Do not resume Phase A or perform additional dispatches until its hook, ledger, and database evidence agree.

## Files touched

- `docs/features/agent-provenance-telemetry/integration/stage-f/codex-namespaced-hook-matcher-repair-receipt.md`
- `docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md`
- `docs/features/agents-communication-infra/WORK-PACK.md`
- `C:\Users\victo\AppData\Roaming\Code\User\settings.json`
- `sessions/2026-07-27-1255-codex-hook-host-binary-remediation.md`
