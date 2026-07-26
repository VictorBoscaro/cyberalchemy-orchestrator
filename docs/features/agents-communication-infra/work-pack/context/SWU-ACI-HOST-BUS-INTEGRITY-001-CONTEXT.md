# Context pack — SWU-ACI-HOST-BUS-INTEGRITY-001

- Mode: standard
- Strict coverage: pass
- Target: Phase-A bounded runtime integrity repair F4/F5/F6
- Source budget: 13 files
- Runtime handoff: no; this is canonical task context, not session evidence

## Obligations

| ID | Obligation | Evidence | Status |
|---|---|---|---|
| O1 | Reject a follow-up when the prior terminal binding has no persisted agent identity. | Phase-A F4; T-ACI-PHASEA-I1; `RuntimeService.bind_host_workflow_turn` | covered |
| O2 | Reject a follow-up target that differs from the persisted prior identity with zero writes. | T-ACI-PHASEA-I1; Host Binding tests | covered |
| O3 | Recompute every official peer artifact digest from stored body bytes before materialization. | Phase-A F5; T-ACI-PHASEA-I2; `RuntimeService.materialize_authorized_peer_input` | covered |
| O4 | Corrupted peer bytes fail atomically before effective-input/request/Attempt/effect acceptance. | T-ACI-PHASEA-I2; operations atomicity contract | covered |
| O5 | Bind `reveal_delivery.py` and migration 011 in the Stage-E source manifest. | Phase-A F6; T-ACI-PHASEA-I3 | covered |
| O6 | Independently tamper-test both active sources and block startup/invocation. | T-ACI-PHASEA-I3; orchestration bridge source-integrity tests | covered |
| O7 | Preserve provider/tool start count zero and do not implement F1/F2/F3, ACI-005 or cutover. | descriptor non-goals; WORK-PACK authorization | covered |
| O8 | Keep all edits inside the exact seven-path write scope and run all four validations. | descriptor/readiness contract | covered |

## Selected evidence

| Path | Selectors | Obligations |
|---|---|---|
| `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-HOST-BUS-INTEGRITY-001.json` | complete descriptor | O1–O8 |
| `docs/features/agents-communication-infra/WORK-PACK.md` | control fields; selection state | O7–O8 |
| `docs/features/agents-communication-infra/TEST-SPEC.md` | T-ACI-PHASEA-I1–I3 | O1–O6 |
| `docs/features/agents-communication-infra/reviews/2026-07-25-host-bus-phase-a-close/review.md` | F4–F6; ordered change requests | O1–O6 |
| `docs/features/agents-communication-infra/specs/operations.md` | MaterializeAuthorizedPeerInput; StartAgentAttempt atomicity | O3–O4, O7 |
| `docs/features/agents-communication-infra/specs/interfaces.md` | ArtifactBoundary and materialization ownership | O3–O4 |
| `docs/PROJECT-DECISIONS.md` | Implementation Baseline Interview | O8 |
| `implementations/server/runtime/service.py` | `materialize_authorized_peer_input`; `bind_host_workflow_turn` | O1–O4 |
| `implementations/tests/runtime/test_host_workflow_binding.py` | binding/follow-up fixtures | O1–O2 |
| `implementations/tests/runtime/test_bus_reveal_delivery.py` | peer delivery fixtures and zero-start assertion | O3–O4, O7 |
| `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` | `files` map | O5 |
| `implementations/tests/runtime/test_orchestration_bridge.py` | source-manifest setup; failed-manifest test | O5–O6 |
| `implementations/tests/runtime/aci-test-traceability.json` | test-ID mappings | O8 |

## Constraints

- The runtime service remains the application owner; no new abstraction or provider path is added.
- Failure paths for O1–O6 must commit no new authoritative row, event, artifact or receipt.
- Active-source manifest hashes are computed from the final task-owned bytes.
- Source-integrity tests operate on isolated copies/fixtures and never mutate the repository source
  during validation.
- Existing unrelated working-tree changes are outside the task and must remain untouched.
- Requested capability enforcement is non-observable; completion may claim only inspected diff and
  executed test evidence, never OS sandbox enforcement.

## Done criteria

1. T-ACI-PHASEA-I1 proves null and mismatched follow-up identity fail before new bindings.
2. T-ACI-PHASEA-I2 proves peer-body corruption fails before materialization acceptance.
3. T-ACI-PHASEA-I3 proves both active BUS sources are manifest-bound and tamper-blocked.
4. All four descriptor validation commands pass.
5. Diff contains only the seven declared paths.
6. Traceability maps all three test IDs to concrete tests.
7. Independent verifier accepts the changed-symbol/test/traceability bundle.

## Deferred scope

- F1 invocation-plan authority derivation.
- F2 producer-owned terminal output evidence.
- F3 completed BUS execution receipt and final completion restoration.
- ACI-005 opening materializer.
- Effect claim, fake worker, real provider, tools, network, production and cutover.

