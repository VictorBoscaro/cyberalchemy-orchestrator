---
tags: [orchestration, agents, dispatch, architecture, ledger]
node_type: test
is_session: true
layer: [architecture, application]
nature: [explanatory, technical]
status: active
created: 2026-07-21
timestamp: 2026-07-21T14:11:45-03:00
expires: 2026-09-19
decisions_made: true
contradictions_found: false
specs_updated:
  - docs/features/agents-communication-infra/README.md
  - docs/features/agents-communication-infra/discovery/agents-communication-infra.md
  - docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md
  - docs/features/agents-communication-infra/WORK-PACK.md
  - docs/features/agents-communication-infra/EXECUTION-PACK.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session turned the proposed bus boundary into an executable, receipt-gated proof and established a viable subscription-based telemetry path."
---

# Agent communication plan and bus publication probe

## Summary

The session identified agents communication infrastructure as the migration of the existing human-gated dispatch discipline into a recoverable runtime, not as a second orchestration product. It placed the feature under `docs/features/agents-communication-infra`, produced discovery and a layered implementation/work/execution plan, and attached the DomainSpec authoring workflow needed for later specifications. The architecture preserved disjoint authority between the runtime journal, audit ledger, artifacts and projections while retaining the current audit-ledger appender boundary. Before writing specs, the session built a dependency-free MCP probe whose only agent-facing capability is `bus_publish`, with append-before-ack receipts, idempotency, logical uniqueness, phase closure and parent-side verification. Ten contract tests passed, including concurrent retry, forged or absent receipts, late publication and denial of peer-read capability. A real Codex subagent generated a contribution, published it through the MCP via a thin command client, returned only its receipt, and the parent independently matched one persisted event. The session decided that effective model inputs, raw provider outputs and accepted bus messages should be separate immutable records referenced from the journal, with runtime-generated identities rather than agent-supplied authority fields. A subscription-authenticated `codex exec --json` probe exposed exact CLI-reported input, cached-input, output and reasoning-token counters, supporting per-attempt through per-dispatch usage rollups while leaving a future API adapter possible but out of current scope.

## Contradictions

- validates `vault/hypothesis/orchestration-infra.md` — a controlled agent publication crossed an ephemeral MCP transport and survived as a uniquely receipted journal event.

## Open questions

- Which exact system instructions, history, tool descriptions and context artifacts constitute the canonical effective-input snapshot for an attempt?
- What redaction, encryption, access and retention policy should govern raw prompts and provider outputs?
- Does CLI-reported turn usage remain complete across tool-heavy, multi-turn, resumed and retried Codex executions?

## Next steps

1. Implement a `codex_cli` execution adapter that uses the existing subscription session, injects the bus as a native MCP tool and refuses results without a verified publication receipt.
2. Persist immutable effective-input and raw-output artifacts and link them to attempts, provider exchanges and accepted messages.
3. Parse `turn.completed.usage` into immutable usage events and aggregate them by attempt, operation, seat, group, run and dispatch.
4. Repeat the probe with multiple seats, retries, tool calls and phase transitions before freezing the production contracts.
5. Incorporate the validated publication, snapshot and usage semantics into the DomainSpec feature specs.

## Recommendation

Build the subscription-backed `codex_cli` vertical slice next, because the landed receipt test and CLI usage event jointly license native MCP publication, input/output capture and dispatch-level telemetry without introducing API billing now.

## Files touched

- .gitignore
- .claude/agents/domainspec-discovery-writer.agent.md
- .claude/agents/domainspec-spec-writer.agent.md
- .claude/agents/mars-researcher.agent.md
- .claude/skills/custom/discovery-writing.md
- .claude/skills/discovery-writing/SKILL.md
- docs/features/agents-communication-infra/README.md
- docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md
- docs/features/agents-communication-infra/WORK-PACK.md
- docs/features/agents-communication-infra/EXECUTION-PACK.md
- docs/features/agents-communication-infra/phase-2-confirm-handoff.md
- docs/features/agents-communication-infra/discovery/agents-communication-infra.md
- docs/features/agents-communication-infra/experiments/bus-publication-probe/.gitignore
- docs/features/agents-communication-infra/experiments/bus-publication-probe/README.md
- docs/features/agents-communication-infra/experiments/bus-publication-probe/mcp.example.json
- docs/features/agents-communication-infra/experiments/bus-publication-probe/package.json
- docs/features/agents-communication-infra/experiments/bus-publication-probe/prompts/subagent.md
- docs/features/agents-communication-infra/experiments/bus-publication-probe/src/bus.mjs
- docs/features/agents-communication-infra/experiments/bus-publication-probe/src/mcp-server.mjs
- docs/features/agents-communication-infra/experiments/bus-publication-probe/src/publish-probe.mjs
- docs/features/agents-communication-infra/experiments/bus-publication-probe/src/verify-result.mjs
- docs/features/agents-communication-infra/experiments/bus-publication-probe/test/bus.test.mjs
- docs/features/agents-communication-infra/experiments/bus-publication-probe/test/mcp.test.mjs
- docs/features/agents-communication-infra/work-pack/shared/context.md
- docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md
- docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md
- docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md
- docs/features/agents-communication-infra/work-pack/shared/traceability.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-000.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-010.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-020.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-030.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-040.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-050.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-060.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-070.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-080.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-AUDIT-ALIGNMENT.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-AUDIT-LAYERING.md
- docs/features/agents-communication-infra/work-pack/tasks/TASK-VERIFY.md
- docs/features/agents-communication-infra/work-pack/waves/W0.md
- docs/features/agents-communication-infra/work-pack/waves/W1.md
- docs/features/agents-communication-infra/work-pack/waves/W2.md
- docs/features/agents-communication-infra/work-pack/waves/W3.md
- docs/features/agents-communication-infra/work-pack/waves/W4.md
- docs/features/agents-communication-infra/work-pack/waves/W5.md
- docs/features/agents-communication-infra/work-pack/waves/W6.md
- docs/features/agents-communication-infra/work-pack/waves/W7.md
- vault/constitution/engine-constitution.md
- vault/hypothesis/orchestration-infra.md
