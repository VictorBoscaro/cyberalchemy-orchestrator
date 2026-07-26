# Implementation scaffold — SWU-ACI-HOST-BUS-INTEGRITY-001

## Function-first targets

| Obligation | Symbol/file | Required change |
|---|---|---|
| O1–O2 | `RuntimeService.bind_host_workflow_turn` in `service.py` | For follow-up turns, require `prior_turn.agent_id` to be a non-empty string and require exact `tool_input.target` equality before manifest preparation or journal acceptance. |
| O3–O4 | `RuntimeService.materialize_authorized_peer_input` in `service.py` | Select peer artifact `body` with stored hash; recompute `digest_bytes(body)` for every official message before `build_peer_entries`; reject missing/corrupt bytes with `IntegrityError`. |
| O5 | Stage-E `source-manifest.json` | Add final SHA-256 entries for `reveal_delivery.py` and migration 011. |
| O6 | `test_orchestration_bridge.py` | Add isolated tamper fixtures proving each new source fails the manifest gate. |
| O1–O2 | `test_host_workflow_binding.py` | Add null and mismatch follow-up tests with before/after authoritative row counts. |
| O3–O4 | `test_bus_reveal_delivery.py` | Add peer-body-only corruption test and assert the complete acceptance unit remains absent. |
| O8 | traceability JSON/test | Map T-ACI-PHASEA-I1–I3 and validate the mappings. |

## Layer boundaries

- Domain rules and operation names remain unchanged.
- `service.py` owns orchestration and fail-closed checks at the authoritative application boundary.
- Existing artifact/database components remain infrastructure owners; tests may inspect them but
  cannot introduce a second writer.
- Stage-E manifest remains the startup-integrity authority for its enumerated sources.

## Ordered implementation path

1. Add the three failing adversarial tests and traceability mappings.
2. Repair F4 and run the Host Binding suite.
3. Repair F5 and run the BUS suite.
4. Update F6 manifest hashes from final source bytes; add and run both tamper tests.
5. Run all four validation commands.
6. Inspect the task-owned diff and confirm the seven-path scope.

## Stop conditions

- Any required change to invocation-plan authority, producer-output evidence, effect claim or
  provider execution.
- Any test that can pass only by weakening existing validation.
- Any need to write outside the descriptor scope.
- Any conflict between the scaffold and accepted DomainSpec sources.

