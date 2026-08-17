# Context Pack - Staged Sequential Dispatch Lifecycle

Status: **superseded session evidence — do not execute**.

This pack predates inspection of the accepted terminal-output architecture. Its declared-file
proposal conflicts with D1 (`phase-a-output-evidence-and-implementation-baseline.md`), which permits
only exact host-observed terminal response bytes as `binding-output`. The replacement planning
source is
`docs/features/agents-communication-infra/development/invoke-runs/20260810-terminal-output-handoff/plan/WORK-PACK.md`.

## Task

Make a frozen `legacy-managed` dispatch with sequential connections executable in stages: launch
root producer groups before their outputs exist, register authentic terminal outputs, materialize
digest-bound handoffs, and compile only downstream groups whose complete inputs are available.

## Obligations

| id | obligation | controlling evidence | status |
|---|---|---|---|
| O1 | The first compile must succeed without pre-existing producer outputs and emit only root-group launches. | `dispatch_workflow.py:246-426`; observed compile failure at `_handoff_receipt` | covered |
| O2 | A terminal bound seat must be able to register an authentic repository-local output against its binding and agent identity. | `service.py:5850-6015` already accepts `producer_output` and returns a signed receipt | covered |
| O3 | The host hook must preserve the producer receipt outside the research working folder for later compiler consumption. | `host_dispatch_hook.py:600-692`; current hook omits `producer_output` | covered |
| O4 | Downstream compilation must validate route, seat order, path, bytes, digest, and registered terminal producer binding. | `dispatch_workflow.py:86-210`; `service.py:5286-5500` | covered |
| O5 | Fan-in DAGs must wait for every incoming group and must not relaunch groups with complete output receipts. | confirmed research graph in `opening-proposal.json` | covered |
| O6 | Missing, partial, failed, cancelled, stale, or tampered producer evidence must block downstream readiness rather than synthesize evidence. | lifecycle fail-closed rule; existing receipt validation | covered |
| O7 | Connectionless compilation and existing exact-receipt compilation must remain compatible. | `test_dispatch_workflow.py`; `test_runtime_type_bootstrap.py` | covered |
| O8 | Changes to Stage-E-pinned sources and tests must update their exact digests and the manifest self-digest. | `source-manifest.json`; `local_pilot.py:37-39` | covered |
| O9 | The original research dispatch must require a revised human confirmation if producer-output paths change its prompts. | lifecycle confirmation contract | covered |

## Selected Context

1. `.codex/workflow-inputs/2026-08-16-artifact-schema-governance-landscape/opening-proposal.json`
   - Exact confirmed DAG, prompts, group sizes, destination, and route.
   - Covers O5 and O9.
2. `implementations/server/runtime/dispatch_workflow.py`
   - `_handoff_receipt`, `compile_bound_launch_plan`, and CLI surface.
   - Covers O1, O4, O5, O6, and O7.
3. `implementations/server/runtime/host_dispatch_hook.py`
   - Bound-seat state, completion correlation, `_close_state`, and `SubagentStop` behavior.
   - Covers O2, O3, and O6.
4. `implementations/server/runtime/service.py`
   - `_host_workflow_source`, workflow-manifest validation, and
     `complete_host_workflow_turn(..., producer_output=...)`.
   - Covers O2 and O4; no change is initially required.
5. `implementations/tests/runtime/test_dispatch_workflow.py`
   - Compiler validation and missing-handoff behavior.
   - Covers O1, O5, O6, and O7.
6. `implementations/tests/runtime/test_host_dispatch_hook.py`
   - Host event shapes and completion correlation.
   - Covers O2, O3, and O6.
7. `implementations/tests/runtime/test_runtime_type_bootstrap.py`
   - Existing exact sequential output receipt and manifest test.
   - Covers O4 and O7.
8. `docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md`
   - Canonical implemented host-wrapper contract and recovery boundary.
   - Covers O2, O3, and documentation synchronization.
9. `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
   - Exact pinned source/test digests.
   - Covers O8.
10. `implementations/server/runtime/local_pilot.py`
    - Stage-E manifest self-digest pin.
    - Covers O8.

## Execution Decision

Use a deterministic control-plane output convention rather than changing the dispatch-row schema:

```text
.codex/workflow-inputs/<dispatch-id>/outputs/<group-id>-<seat-index>.md
.codex/workflow-inputs/<dispatch-id>/producer-output-<group-id>-<seat-index>.json
```

The confirmed agent prompt must explicitly require the Markdown output path. On bound-seat
completion, the hook registers that file through the existing
`complete_host_workflow_turn(..., producer_output=...)` contract and atomically persists only the
returned receipt in the control-plane directory. The compiler derives each handoff only from a
complete set of validated per-seat receipts. It never fabricates binding or agent identity.

Repeated compile calls act as stages:

1. no receipts: emit uncompleted seats in root groups only;
2. complete root receipts: emit newly ready downstream seats;
3. complete fan-in receipts: emit the sink group;
4. all groups complete: emit zero launches.

This is an implementation choice, not a new canonical product schema. It keeps the working folder
free of bridge stdout and makes the existing runtime receipt the authority.

## Preliminary Write Scope

- `implementations/server/runtime/dispatch_workflow.py`
- `implementations/server/runtime/host_dispatch_hook.py`
- `implementations/tests/runtime/test_dispatch_workflow.py`
- `implementations/tests/runtime/test_host_dispatch_hook.py`
- `implementations/tests/runtime/test_runtime_type_bootstrap.py` only if the existing receipt fixture must change
- `docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `implementations/server/runtime/local_pilot.py` restricted to the manifest digest constant

Any need to change the registry, appender schema, database migrations, `service.py`, or host hook
configuration is a scope expansion and must be justified before editing.

## Done Criteria

- First-wave compile succeeds for the confirmed three-group research DAG without handoff files.
- A bound Codex seat that writes its declared control output closes with a non-null authentic
  producer-output receipt persisted under `.codex/workflow-inputs/<dispatch-id>/`.
- A second compile materializes handoffs and emits reviewers only after every explorer receipt is
  present and valid.
- Fan-in synthesis remains blocked until both explorer and reviewer handoffs are complete.
- Completed seats are not relaunched; a fully completed graph emits zero launches.
- Missing, partial, failed, cancelled, stale, route-drifted, or tampered outputs fail closed.
- Existing connectionless and exact-receipt tests continue to pass.
- Focused runtime tests, full runtime suite, compileall, source-manifest verification, and
  `git diff --check` pass.
- The research opening record is revised with explicit output paths and shown to the user for a new
  confirmation before resuming the dispatch.

## Gate Result

PASS for bounded implementation, subject to independent architecture and test-plan checks. No
database schema, registry, or dispatch-row schema change is currently justified.
