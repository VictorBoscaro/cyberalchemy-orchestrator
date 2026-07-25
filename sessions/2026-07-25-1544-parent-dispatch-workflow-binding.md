---
tags: [orchestration, agents, dispatch, ledger, architecture]
node_type: conceptual
is_session: true
layer: [architecture, domain, application]
nature: [explanatory, technical]
status: active
created: 2026-07-25
timestamp: 2026-07-25T15:44:55-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session repaired a load-bearing dispatch-governance binding, added exact provenance enforcement, and validated the result with 77 passing runtime tests, directly enabling the planned research topology."
---

# Parent Dispatch Workflow Binding

## Summary

The session began by checking the planned research sequence and identified a first wave on foundational kernel invariants, Lean's determinism guarantees, and Lean kernel/runtime applicability. The requested topology was refined to one parent research Dispatch containing three independent researchers, robot-talks, a synthesizer, and three independent zig-zag reviewers. An audit found that the mandatory host hook incorrectly wrapped every spawn as a separate compatibility Dispatch even though the ledger and bridge already supported a multi-group parent. The repository owner directed that this binding be repaired before the research ran. A bounded host-workflow bridge was selected because it enables the immediate topology without falsely claiming complete provider-side `EffectiveInputArtifact` capture. The runtime now persists each group, seat, and turn under an already-confirmed parent, validates frozen prompts and follow-up templates, stores strict workflow manifests and exact source bytes and hashes, and binds follow-ups to the prior agent. Bound turns no longer append separate YAML Dispatch rows, `followup_task` is governed, and the parent cannot close while a turn is running. The source-integrity manifest and documentation were refreshed, and the complete runtime suite passed 77 of 77 tests.

## Open questions

- Which Lean kernel mechanisms actually guarantee deterministic checking or execution, and which of those mechanisms can transfer to this repository's application-level determinism?
- Does the existing Lean kernel contain reusable architectural precedents beyond its trusted checking boundary?

## Next steps

- Construct and confirm the single parent research Dispatch with three independent first-wave researchers.
- Run robot-talks across their persisted findings, route the result to one synthesizer, then execute three independent reviewer zig-zags.
- Persist the research artifacts under `research/foundational-kernel-and-formalization/waves/phase-1/`.

## Recommendation

Launch the three-source first wave next, using the now-tested parent binding and exact artifact manifests so the open Lean applicability questions are answered before implementation claims are made.

## Files touched

- .codex/hooks.json
- docs/decisions/host-agent-dispatch-input-binding.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md
- docs/features/agent-provenance-telemetry/integration/stage-f/host-workflow-binding-receipt.md
- implementations/server/runtime/database.py
- implementations/server/runtime/host_dispatch_hook.py
- implementations/server/runtime/local_pilot.py
- implementations/server/runtime/migrations/009_host_workflow_binding.sql
- implementations/server/runtime/service.py
- implementations/tests/runtime/test_host_dispatch_hook.py
- implementations/tests/runtime/test_host_workflow_binding.py
- telemetry/agents/subagents-dispatch.yaml

## Research topology to carry forward

Lean is not limited to a supporting role: the research must examine both how Lean guarantees determinism and whether its kernel provides reusable reference architecture. The initial wave remains three independent angles followed by robot-talks, synthesis, and three independent reviewers with bounded zig-zag feedback.
