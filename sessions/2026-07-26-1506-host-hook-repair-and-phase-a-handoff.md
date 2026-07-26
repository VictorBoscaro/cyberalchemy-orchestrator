---
tags: [orchestration, agents, dispatch, ledger]
node_type: test
is_session: true
layer: [architecture, application]
nature: [technical, explanatory]
status: active
created: 2026-07-26
timestamp: 2026-07-26T15:06:17-03:00
expires: 2026-09-24
decisions_made: true
contradictions_found: true
specs_updated:
  - docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md
  - docs/features/agents-communication-infra/WORK-PACK.md
  - docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session isolated a live host-enforcement gap, repaired its repository matcher and integrity pins, and left executable evidence for a safe Phase-A restart."
---

# Host hook repair and Phase-A handoff

## Summary

The session began by determining whether the accepted BUS proof was sufficient to proceed to Worker B and found that it proved request materialization but not provider execution. Existing DomainSpec contracts required the Phase-A F4/F5/F6 integrity repair before ACI-005 and the later worker loop. A bounded repair SWU, readiness receipt, context pack, scaffold, structural/concrete proposals, and dispatch inputs were authored, then three independent reviewers found seven authoring and governance defects that were corrected. Two code-dispatch attempts were stopped because real subagent launches produced no hook state, ACI dispatch link, workflow binding, or `launch-authorized` receipt. Investigation isolated a mismatch between the host's namespaced `collaboration.spawn_agent` spelling and the closed Codex hook matcher. The matcher was expanded to the supported bare, namespaced, and flattened spellings, a regression test was added, and the Stage-E source manifest plus `local_pilot` pin were synchronized. A 48-test focused suite passed, all 47 manifest entries matched their source bytes, and the manifest digest matched the runtime pin. A live smoke still produced no receipt because the current Codex client did not hot-reload its project hooks, so no reviewer or coder result was accepted and F4/F5/F6 implementation remains pending. Control documents now record `LOCAL_PASS / LIVE_HOST_RELOAD_REQUIRED` and require a fresh-session smoke before dispatch resumes.

## Contradictions

- questions `docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md` — repository-local tests validate the repaired contract, but live Codex enforcement remains unproven until a fresh client session materializes hook state and ACI/YAML receipts.

## Next steps

1. Start a fresh trusted Codex session and run one read-only `collaboration.spawn_agent` smoke.
2. Verify the smoke produced Codex hook state, append-only dispatch open/close, an ACI `dispatch_links` row, and a terminal binding when workflow-bound.
3. Rebuild the invalidated Phase-A concrete proposal against current source hashes and rerun capability plus two tension gates.
4. Run the three-reviewer post-gate review, then the alignment/layering → coder → verifier implementation topology for F4/F5/F6.
5. Run the four SWU validation commands and the focused 48-test infrastructure suite before updating completion status.

## Recommendation

Treat the fresh-session live smoke as the keystone: the repository implementation is locally green, but no further subagent evidence should be trusted until the host proves it loaded the repaired matcher.

## Files touched

- .codex/hooks.json
- .codex/workflow-inputs/2026-07-26-phase-a-host-bus-integrity/alignment-manifest.json
- .codex/workflow-inputs/2026-07-26-phase-a-host-bus-integrity/close-error.json
- .codex/workflow-inputs/2026-07-26-phase-a-host-bus-integrity/generate-auditor-manifests.mjs
- .codex/workflow-inputs/2026-07-26-phase-a-host-bus-integrity/layering-manifest.json
- .codex/workflow-inputs/2026-07-26-phase-a-post-gate-review/close-error.json
- .codex/workflow-inputs/2026-07-26-phase-a-post-gate-review/generate-reviewer-manifests.mjs
- .codex/workflow-inputs/2026-07-26-phase-a-post-gate-review/hoare-manifest.json
- .codex/workflow-inputs/2026-07-26-phase-a-post-gate-review/liskov-manifest.json
- .codex/workflow-inputs/2026-07-26-phase-a-post-gate-review/parnas-manifest.json
- docs/PROJECT-DECISIONS.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- docs/features/agent-provenance-telemetry/integration/stage-f/codex-namespaced-hook-matcher-repair-receipt.md
- docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md
- docs/features/agents-communication-infra/WORK-PACK.md
- docs/features/agents-communication-infra/reviews/2026-07-26-phase-a-authoring-review/review.md
- docs/features/agents-communication-infra/work-pack/context/SWU-ACI-HOST-BUS-INTEGRITY-001-CONTEXT.index.json
- docs/features/agents-communication-infra/work-pack/context/SWU-ACI-HOST-BUS-INTEGRITY-001-CONTEXT.md
- docs/features/agents-communication-infra/work-pack/context/SWU-ACI-HOST-BUS-INTEGRITY-001-SCAFFOLD.md
- docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-BUS-DELIVERY-001.json
- docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-HOST-BUS-INTEGRITY-001.json
- docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-HOST-BUS-INTEGRITY-001-code-readiness.json
- docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md
- implementations/server/runtime/local_pilot.py
- implementations/tests/runtime/test_host_dispatch_hook.py
- plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-capability-profile-v2.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-concrete-core-v2.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-concrete-v2.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-dispatch-row-v2.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-host-bus-integrity-structural-v2.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-post-gate-review-approval-v1.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-post-gate-review-concrete-core-v1.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-post-gate-review-row-v1.json
- plans/governed-agent-work-infrastructure/workstreams/phase-a-post-gate-review-structural-v1.json
- telemetry/agents/subagents-dispatch.yaml

## Closure constraint requested by the user

The next session must use the governed subagent infrastructure and prove that it is actually active; passing local tests alone is not sufficient evidence of live enforcement.
