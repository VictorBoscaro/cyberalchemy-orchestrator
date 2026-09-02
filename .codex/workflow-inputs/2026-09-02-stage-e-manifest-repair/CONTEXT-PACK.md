# Context Pack — Stage-E manifest repair

Session evidence only; not a canonical planning artifact.

## Scope

- Task: repair only the Stage-E integrity drift that blocks the already-confirmed Craft opening.
- Mode: lean, strict.
- Non-goals: do not execute `open`, append telemetry, create a session, launch a seat, alter
  `database.py`, commit, or push.
- Write scope: Stage-E source manifest, its verifier pin, its execution receipt/sidecar, and this
  task-session evidence directory.

## Obligation matrix

| ID | Obligation | Evidence | Status |
|---|---|---|---|
| O1 | Prove the current `database.py` bytes are accepted | `database.py:14-30` adds only migration 016; predecessor `review.md:22-23,293-294,343,358-360` accepts migration 016, the three adjacent migration-version test edits, and sequential bootstrap | covered |
| O2 | Identify the complete Stage-E drift, not only the first mismatch | deterministic check of all 83 manifest members found five mismatches and zero missing files | covered |
| O3 | Preserve unrelated dirty work | pre-mutation `git status --short` captured; only the Stage-E chain will be edited | covered |
| O4 | Follow manifest ownership and provenance | `local_pilot.py:33-83` pins and verifies the manifest and every member; `execution-receipt.md:26,427-449` demonstrates append-only receipt plus sidecar pattern | covered |
| O5 | Include new loaded integrity dependency | `database.py:30,86` loads `016_local_execution_graph_runtime.sql`; existing manifest lists every prior migration but omits 016 | covered |
| O6 | Run complete preflight and adjacent tests | `test_stage_c.py:30-162`; predecessor validation names the exact adjacent runtime and bootstrap suites | covered |
| O7 | Prove `open` can advance past Stage-E without effects | call the read-only Stage-E verifier directly and, if available, exercise preflight/open with the mutating hook patched or stopped before the hook boundary | covered |

## Selected context

1. `AGENTS.md` — repository policy, claim ceiling, repair-forward and host-binding constraints.
2. `implementations/server/runtime/database.py:14-30,86-116` — migration registry and migration
   integrity consumer.
3. `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` — canonical
   Stage-E member inventory and digests.
4. `implementations/server/runtime/local_pilot.py:33-83,139-170` — manifest digest pin and fail-closed
   member verifier.
5. `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md:26,390-449` —
   provenance owner and prior integrity-refresh pattern.
6. `docs/features/agents-communication-infra/development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md:22-23,293-294,311-368`
   — same-reviewer acceptance and exact validation ceiling.
7. `implementations/tests/runtime/test_stage_c.py:30-162` — Stage-C/Stage-E preflight tests.
8. `implementations/server/runtime/dispatch_workflow.py:233-255,424-538,570-612` — opening validation,
   compilation and open boundary used for the no-effects proof.

## Drift evidence before repair

- Manifest SHA-256: `919793A406FA4CA7B90B97AB65C6CD23E8C203C57392037FF5735FCEFFBCC4C2`.
- Verifier pin: the same digest.
- Manifest members: 83; missing: 0; mismatched: 5.
- `database.py`: expected `4F04C889...CAFE66`, actual `62377165...3273A`.
- Other accepted drifts: `dispatch_workflow.py` and the three adjacent migration-version tests.
- Historical `841236AE...` belongs to an older RWO frozen closure; it is neither the current Stage-E
  manifest value nor the current bytes.
- No repository-local Stage-E manifest generator was located by bounded searches across the Stage-E
  integration folder, runtime tests, runtime source and `tools`; prior history records direct
  canonical repins.

## Decisions and gate

- Auto-selected, non-blocking: canonical deterministic manifest regeneration from its current
  inventory, refreshing all five accepted members and adding migration 016.
- Preserve the manifest inventory otherwise; do not add the independent local execution module or
  tests because they are not loaded by the Stage-E/open path and are outside this repair.
- Refresh the verifier pin after manifest bytes stabilize, append a bounded receipt section, and
  refresh the receipt sidecar.
- Gate: PASS. Every obligation is covered; no destructive or external effect is authorized.

## Validation surface

- exact member digest inventory, including zero missing/mismatched members;
- direct `_verify_source_manifest(repo_root)`;
- `test_stage_c`, adjacent migration/runtime tests, workflow bootstrap tests;
- execution-receipt sidecar equality;
- no-effects proof at/before open hook boundary;
- `git diff --check` and scoped diff review.

## Context Pack Summary

- Files selected: 8
- Snippets selected: 14
- Obligation coverage: 100%
- Noise ratio: low
- Handoff pack: none
- Strict coverage: pass
- Blockers: 0
