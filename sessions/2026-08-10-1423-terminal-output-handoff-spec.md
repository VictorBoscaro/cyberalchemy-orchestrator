---
tags: [agent-handoff, terminal-output, workflow-inputs, runtime-authority, replay-safety]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-10T14:23:49-03:00
updated_at: 2026-08-10T14:23:49-03:00
expires: 2026-10-09
decisions_made: true
contradictions_found: true
specs_updated: [docs/features/agents-communication-infra/specs/SPEC.md, docs/features/agents-communication-infra/specs/domain.md, docs/features/agents-communication-infra/specs/operations.md, docs/features/agents-communication-infra/specs/states.md, docs/features/agents-communication-infra/specs/events.md, docs/features/agents-communication-infra/specs/interfaces.md, docs/features/agents-communication-infra/specs/persistence-and-replay.md, docs/features/agents-communication-infra/specs/rules.md, docs/features/agents-communication-infra/specs/glossary.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "This session converted a broken multi-stage handoff into a bounded normative contract and exposed the exact infrastructure gap blocking governed reviews."
---

# Terminal-output handoff specification

## Summary

The session investigated why a governed review launched downstream seats with empty input slots and confirmed that connections were parsed but not materialized as data handoffs. A fail-closed compiler fence was added and tested so connected legacy-managed topologies cannot produce misleading launch plans. The owner accepted D1, persisting exact host-observed terminal response bytes as content-addressed evidence, and D2, retaining the Python and SQLite runtime baseline. Invoke Define and Design artifacts were authored to translate those decisions into a bounded terminal-output handoff. An independent four-agent review found that the first amendment overstated readiness because producer attribution collided with content identity and downstream mapping, persistence, visibility, lifecycle and launch contracts were incomplete. The spec was repaired by separating shared content from producer-turn evidence and defining host binding authority, source-to-slot mapping, manifest, binding, materialization, launch authorization, crash recovery and non-byte-bearing terminal outcomes. The implementation boundary was narrowed to one completed producer feeding one required consumer slot, while fan-in and the full attackers-to-writer-to-skeptic topology remain L2. Design selection was refreshed against the amended sources and passed at fixed point with no diagnostics. The governed review itself remains impossible until terminal-output handoff is implemented, and its compiler failure provided direct evidence of the gap. No implementation of the new normative contracts was attempted.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Phase-A output evidence and implementation baseline](../docs/decisions/phase-a-output-evidence-and-implementation-baseline.md) | `derives-from` | The session implements the owner-selected D1 and D2 as specification and design authority. |
| [Agents Communication Infra SPEC](../docs/features/agents-communication-infra/specs/SPEC.md) | `contextualizes` | The session records why and how the ACI terminal-output contracts were amended. |
| [Terminal-output handoff Design transport](../docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/DESIGN-TRANSPORT.md) | `validates` | The refreshed fixed-point selection validates the bounded L0/L1 design handoff. |

## Open questions

- Does a second independent review refute any of the repaired content/evidence, mapping, visibility, persistence or launch contracts?
- Which later spec version should introduce bounded fan-in and non-success producer completion policies?

## Next steps

1. Repeat the independent adversarial review against the repaired spec and update only findings that survive literal verification.
2. If the review passes, run `invoke plan` only for L0/L1: one completed producer, one required slot and one launch intent.
3. Keep the connected-topology compiler fence until the L0/L1 witnesses pass under restart and conflict injection.

## Recommendation

Re-run the review before planning; the prior review uncovered two critical modeling defects, so a verified clean pass is the licensing fact for `invoke plan`.

## Files touched

- `.codex/workflow-inputs/2026-08-10-terminal-output-spec-review/opening.json`
- `docs/decisions/README.md`
- `docs/decisions/phase-a-output-evidence-and-implementation-baseline.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/ARCHITECTURE.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/CONTEXT.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/DESIGN-TRANSPORT.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/DISPATCH-TECHNIQUE-TRACE.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/DISTILL-VALIDATION.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/GLOSSARY-CONSISTENCY.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/IMPLEMENTATION-LAYERING-SEED.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/define/DEFINE-CONTEXT.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/define/DEFINE-TRANSPORT.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/define/DISPATCH-TECHNIQUE-TRACE.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/define/DISTILL-VALIDATION.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/define/TEMPLATE-SELECTION.md`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/design-selection/authored-concerns.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/design-selection/design-denominator-receipt.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/design-selection/design-scope-manifest.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/design-selection/design-selection-result.json`
- `docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/design-selection/planned-witnesses.json`
- `docs/features/agents-communication-infra/specs/SPEC.md`
- `docs/features/agents-communication-infra/specs/domain.md`
- `docs/features/agents-communication-infra/specs/events.md`
- `docs/features/agents-communication-infra/specs/glossary.md`
- `docs/features/agents-communication-infra/specs/interfaces.md`
- `docs/features/agents-communication-infra/specs/operations.md`
- `docs/features/agents-communication-infra/specs/persistence-and-replay.md`
- `docs/features/agents-communication-infra/specs/rules.md`
- `docs/features/agents-communication-infra/specs/states.md`
- `implementations/server/runtime/dispatch_workflow.py`
- `implementations/server/runtime/local_pilot.py`
- `implementations/tests/runtime/test_dispatch_workflow.py`
