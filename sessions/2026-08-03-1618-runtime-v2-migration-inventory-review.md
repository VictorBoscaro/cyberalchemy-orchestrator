---
tags: [agent-runtime, agent-communication, workflow-graphs, skill-compilation, migration-architecture, subagent-governance]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-03T16:18:32-03:00
updated_at: 2026-08-03T16:18:32-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "This session establishes the evidence-backed migration baseline and review corrections required before designing or implementing the new autonomous agent runtime."
---

# Runtime v2 Migration Inventory and Review

## Summary

This session connected the repository objective of preserving purpose, authority, action, and evidence across agent work to the concrete question of how a new agent runtime should be designed from the current repository. Its objective was to determine what already exists, what is missing, what can be adapted, and whether skills can become persisted executable DAGs whose agents communicate without the parent agent acting as scheduler or relay. The discovery was clarified to cover runtime realization and received an open question about the missing path from confirmed topology to provider launch, peer communication, recovery, and replay. A governed as-built investigation found a reusable transaction substrate for canonicalization, storage, journals, artifacts, capabilities, receipts, and some publication and input materialization, but no persisted executable DAG, skill-to-DAG compiler, scheduler/reducer, connection traversal, or integrated runtime-managed provider lifecycle. It also found that the legacy host and YAML path remains the live execution authority, while the separate agent runtime is an experimental shadow and the parent agent still schedules and relays work. The resulting migration inventory proposed preserving the reusable substrate while isolating legacy authority behind an explicit transition boundary and building the missing graph execution capabilities in phases. A governed review then identified six material corrections: separate authority from precedent, keep protocol ownership unsettled until ratified, narrow the provider gap to integrated runtime-managed execution, correct capability lifetime semantics, make drift evidence reproducible, and use the canonical review gate for existing artifacts. Two independent skeptical verifiers rejected two false-positive criticisms, required tighter evidence on two others, and gave terminal PASS after the synthesizer revised the review. The dispatch could not obtain its final independent approval because completed and interrupted seats continued consuming the collaboration thread limit, so it was closed honestly with `exit_reason: error` despite the reviewed artifact passing both skeptical verifiers. The next architectural work should start from the corrected inventory, settle ownership and target boundaries, and produce a phased high-level plan before moving implementation into a clean branch or worktree.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agents Communication Protocols](../docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md) | `is-part-of` | This session investigated the runtime realization, migration constraints, and unresolved ownership questions of the agents-communication capability described by the discovery. |
| [Runtime v2 research initial definitions](../docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/research-initial-definitions.md) | `derives-from` | The investigation and its evidence boundaries were governed by these initial definitions. |
| [Runtime v2 migration review](../docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/review/review.md) | `contextualizes` | This session records the objective, skeptical loop, accepted corrections, and approval-runtime failure surrounding the review artifact. |

## Open questions

- Which governed owner can authorize the skill-to-DAG contract, and what promotion evidence is required before that contract becomes SPEC?
- What target service boundaries are sufficient for graph persistence, scheduling, provider lifecycle, peer messaging, recovery, and replay without recreating the parent agent as an implicit coordinator?
- Which reusable transaction components should remain authoritative and which should be wrapped or replaced during the runtime-v2 cutover?

## Next steps

1. Run a bounded approval-only review dispatch for the existing final `review.md` digest after collaboration capacity is available.
2. Apply the six accepted review corrections to the migration research and findings before treating them as architectural input.
3. Write a high-level phased runtime-v2 implementation plan, giving each phase its own bounded discovery and evidence gate.
4. Snapshot the current repository state and create a clean branch or worktree only after the target nucleus and migration boundaries are accepted.

## Recommendation

Use the corrected inventory to derive an explicit `objective → authority → persisted graph → runtime execution → event evidence` chain, then move one thin vertical slice into a clean worktree before migrating additional legacy behavior.

## Files touched

- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/research-initial-definitions.md`
- `docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/research.md`
- `docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/findings.md`
- `docs/features/agents-communication-infra/research/runtime-v2-migration-inventory/review/review.md`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/opening-proposal.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/launch-plan.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/as-built-explorers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/as-built-explorers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/as-built-explorers-2-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration/close-error.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/opening-proposal.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/launch-plan.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/as_built_explorers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/as_built_explorers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/as_built_explorers-2-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-as-built-exploration-retry/close.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/opening-proposal.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/launch-plan.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/inventory_attackers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/inventory_attackers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/inventory_attackers-2-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/review_synthesizer-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/review_verifiers-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/review_verifiers-1-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/dedicated_approval-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-03-runtime-v2-inventory-review/close-error.json`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-03-1618-runtime-v2-migration-inventory-review.md`
