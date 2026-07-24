---
tags: [orchestration, agents, agent-telemetry, provenance, sessions, dispatch, research-records, event-bus, sqlite, replay]
node_type: test
is_session: true
layer: [architecture, domain, application]
nature: [explanatory, technical]
status: active
created: 2026-07-24
timestamp: 2026-07-24T10:37:44-03:00
expires: 2026-09-22
decisions_made: true
contradictions_found: false
specs_updated:
  - docs/features/agent-provenance-telemetry/WORK-PACK.md
  - docs/features/agent-provenance-telemetry/integration/stage-a/SWU-ACI-APT-VS-001.md
  - docs/features/agent-provenance-telemetry/integration/stage-b/execution-receipt.md
  - docs/features/agent-provenance-telemetry/integration/stage-c/local-pilot-enablement.md
  - docs/features/agent-provenance-telemetry/work-pack/shared/03-cross-task-decisions.md
  - docs/features/agents-communication-infra/WORK-PACK.md
  - docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-APT-VS-001.json
  - docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md
promoted_candidates: []
expected_importance: 9
importance_rationale: "Establishes and validates the first end-to-end, restart-safe local provenance slice across session, dispatch, and structured research, while production authority and automatic agent launch remain deliberately gated."
---

# Agent provenance local pilot

## Summary

The goal was to turn the incremental agent-provenance discovery into a minimum usable local infrastructure covering session identity, dispatch linkage, a durable event bus, structured research, and logging. The discovery and specification corpus was refined around the three levels of session, dispatch, and research, with exact profiles, storage rules, and authority boundaries. Independent review gates closed the initial work package and authorized only the scoped ACI-to-APT vertical slice. The implementation now provides a SQLite-backed journal, artifact handling, capabilities, accepted-prefix tracking, candidate-to-official publication, and APT session and research projections and APIs. Research captures question, final answer, references, problems, claims, and formalizations, while protected answer bodies are stored as artifacts. Reviews found and drove fixes for authority, retry behavior, compare-and-swap semantics, schema, lineage, projection lag and rebuild, and privacy boundaries. Validation completed with 35 of 35 runtime tests, 8 of 8 Stage C tests, 31 of 31 legacy tests, and 27 of 27 TypeScript tests, plus typecheck, contract, compilation, and diff checks. A localhost-only pilot is running at `127.0.0.1:8766` on a dedicated database, and a live session-to-dispatch-to-research flow survived restart. Production exposure, external providers, automatic agent launch, materializers, and cutover remain intentionally blocked. No commit was created, and unrelated dirty-worktree changes were preserved.

## Open questions

- How should scoped capabilities be issued to real agent launches without exposing raw tokens or broadening the localhost pilot's authority?

## Next steps

1. Add a supported launcher and bootstrap workflow for real agent dispatches while retaining the localhost and capability gates.
2. Document operator procedures for starting, stopping, backing up, and tombstoning the dedicated pilot database.
3. Require host, access-control, sole-writer, and recovery evidence before considering production promotion.

## Recommendation

Prioritize the launcher and capability-bootstrap workflow because persistence and restart behavior are validated, while safe automatic agent invocation is the remaining prerequisite named above.

## Files touched

- docs/features/agent-provenance-telemetry/WORK-PACK.md
- docs/features/agent-provenance-telemetry/integration/stage-a/SWU-ACI-APT-VS-001.md
- docs/features/agent-provenance-telemetry/integration/stage-b/execution-receipt.md
- docs/features/agent-provenance-telemetry/integration/stage-b/execution-receipt.sha256
- docs/features/agent-provenance-telemetry/integration/stage-c/local-pilot-enablement.md
- docs/features/agent-provenance-telemetry/work-pack/shared/03-cross-task-decisions.md
- docs/features/agents-communication-infra/WORK-PACK.md
- docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-APT-VS-001.json
- docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-APT-VS-001-stage-b-execution-receipt.json
- docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md
- implementations/server/main.py
- implementations/server/runtime/api.py
- implementations/server/runtime/cli.py
- implementations/server/runtime/journal.py
- implementations/server/runtime/local_pilot.py
- implementations/server/runtime/projections.py
- implementations/server/runtime/provenance.py
- implementations/server/runtime/service.py
- implementations/tests/runtime/test_apt_projector.py
- implementations/tests/runtime/test_apt_stage_b.py
- implementations/tests/runtime/test_stage_b.py
- implementations/tests/runtime/test_stage_c.py

## User emphasis

Keep this first slice incremental and modular: the probe bus, session identity, dispatch evidence, and enriched research records must be usable now and remain separable enough to evolve before a broader unification.
