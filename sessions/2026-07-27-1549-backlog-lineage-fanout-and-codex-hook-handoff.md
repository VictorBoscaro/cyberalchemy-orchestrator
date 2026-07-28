---
tags: [agent-reference-lineage, workflow-input-lineage, codex-hooks, host-workflow-binding, backlog-skills]
artifact_kind: session
layer: capability
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
timestamp: 2026-07-27T15:49:01-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "This session established the exact execution-lineage gap, promoted the backlog skill, and isolated the live Codex host boundary that must pass before governed subagent work resumes."
---

# Backlog, lineage fan-out, and Codex hook handoff

## Summary

The session completed a governed zig-zag review of the new backlog skill with two independent reviewers and one separate writer. The first review round found seven governance and usability defects, the writer corrected them, and both reviewers returned PASS on the second frozen revision. The approved package was promoted to `.claude/skills/backlog` as the canonical source and `.codex/skills/backlog` as a verified mirror, while the local `.agents` mirror remained byte-identical. A structured read-only fan-out then mapped AgentReferenceLineage across specifications, runtime persistence, hooks, and tests without using the research workflow. The scouts confirmed that AgentReferenceLineage is a reference-specific APT query, while AgentReferenceDelivery bounded L0 is already implemented despite stale implementation-status prose. They also established that declared input is bound by attempt, observed reads are only dispatch-scoped, semantic use remains research/reference-specific, and no authoritative attempt-to-output relation exists. The same live run reproduced the host-control contradiction: collaboration launches succeeded while the policy-selected database retained zero host workflow turn bindings and no new Codex hook state. Process inspection proved that the active VS Code extension still runs embedded `codex-cli 0.146.0-alpha.3.1`, although `chatgpt.cliExecutable` correctly points to installed `0.146.0-alpha.10.1`. No repository bridge code was changed because the defective binary bypasses `PreToolUse` before repository hooks can execute. Governed subagent work remains paused until a VS Code reload and one fresh read-only smoke produce hook state, YAML/ACI lifecycle evidence, and a terminal workflow binding.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agent lineage, dispatch, and backlog handoff](2026-07-27-1457-agent-lineage-dispatch-and-backlog-handoff.md) | `derives-from` | This session executed the backlog promotion and lineage investigation handed off by the earlier session. |
| [Codex hook host-binary remediation](2026-07-27-1255-codex-hook-host-binary-remediation.md) | `validates` | The active-process evidence reproduced the documented stale embedded-binary boundary. |
| [Mandatory host wrapper](../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md) | `validates` | The failed live binding demonstrates the wrapper's requirement that host support be proven by a real smoke rather than configuration alone. |
| [Agent provenance telemetry queries](../docs/features/agent-provenance-telemetry/specs/queries.md) | `contextualizes` | The fan-out distinguished the reference-specific AgentReferenceLineage query from a future generic execution/artifact lineage. |

## Open questions

- After the VS Code reload, will `0.146.0-alpha.10.1` route `collaboration.spawn_agent` through `PreToolUse` and complete the terminal ACI binding?
- Should generic execution/artifact lineage become a separate capability while AgentReferenceLineage remains reference-specific?
- What exact evidence should authorize promotion from `observed_read` to semantic `used_input`?

## Next steps

1. Run `Developer: Reload Window` in VS Code so the extension starts the configured `0.146.0-alpha.10.1` executable.
2. In the fresh session, confirm the active `codex.exe` path and version before launching any subagent.
3. Run exactly one read-only `collaboration.spawn_agent` smoke with the required workflow-binding envelope.
4. Verify new Codex hook state, matching YAML/ACI open and close evidence, and one terminal `host_workflow_turn_bindings` row.
5. Resume the lineage designer and two independent reviewers only after the smoke passes.
6. Design the minimum attempt-centered relations for observed reads and produced output revisions without inferring semantic use.

## Recommendation

Treat the live smoke as the keystone: prove the configured host enters the mandatory wrapper before accepting any further subagent evidence, then resume the already-scoped lineage design from the three scout matrices.

## Files touched

- `.agents/skills/backlog/SKILL.md`
- `.agents/skills/backlog/agents/openai.yaml`
- `.agents/skills/backlog/assets/backlog-template.md`
- `.claude/skills/backlog/SKILL.md`
- `.claude/skills/backlog/agents/openai.yaml`
- `.claude/skills/backlog/assets/backlog-template.md`
- `.codex/skills/backlog/SKILL.md`
- `.codex/skills/backlog/agents/openai.yaml`
- `.codex/skills/backlog/assets/backlog-template.md`
- `sessions/2026-07-27-1549-backlog-lineage-fanout-and-codex-hook-handoff.md`
