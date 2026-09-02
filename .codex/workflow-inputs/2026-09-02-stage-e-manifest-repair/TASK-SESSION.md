# Task Session Result — Stage-E manifest repair

- Task: repair the Stage-E integrity drift blocking the confirmed Craft opening.
- Result: `PASS`, pending the assigned independent reviewer.
- Context pack: lean/strict, 8 selected files, 7/7 obligations covered; SHA-256
  `212f186df2b495ebdbe3e96c2958f3969e6c633bb0ef4a1b6bd242b7312a1360`.
- Decisions: one safe non-blocking repair-forward decision; refresh every accepted mismatch and add
  the newly loaded migration, without altering product sources.
- Runtime/adapter: local checks only; no task runtime delegation.
- Gate verdict: PASS; current bytes have same-reviewer acceptance and exact adjacent tests.
- Subagent closeout: n/a for this worker; no child agents spawned.
- Experiment harness: not applicable.

## Authority and drift

Pre-repair member scan of the 83-entry manifest found zero missing files and five mismatches:

| Path | Manifest before | Current accepted bytes |
|---|---|---|
| `implementations/server/runtime/database.py` | `4f04c889d4b0f7b4cf6f6a58d93c445dd3201c801e78fd22a83777fac9fcae66` | `623771651c603057b206ab1859f6cb8633dfeca7b4179585a9349838b2a3273a` |
| `implementations/server/runtime/dispatch_workflow.py` | `a1d50cd51316b57eeb1eb3eb313279ac72c477e93ff555cc7a89e53edcf12d7c` | `c3522e41506c950d2d4e8233858128c546ecfebb85b8ce8631b90e97ee51a996` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `953a0a01c1599d49e24ec14dd3f7260c206f5d693a27125ba8bb246c0ec4d709` | `c9c001ddd5fb926d75d5cea1b0d7530ff61528ceb8ea9c84078d9304820e65c2` |
| `implementations/tests/runtime/test_runtime_confirmed_bus.py` | `c18e1b78f32ac15ef2180067dd060c1dcd718c5cf9a5627aa13ee2e08f02e83d` | `7e1d4b4c462aa87bc839f3d090c895d44fb66bab263b80e22fd74025028b25f8` |
| `implementations/tests/runtime/test_runtime_run_group_heads.py` | `3871dd762f355ff4974b15a8238fa119bd0ef882828b5b016fbe3b017d591aed` | `ca96736094c4856734ae1cce265b34e15ce97626d817e0a3fef39c9eb3455f6e` |

Review `IMPL-ACI-EXECUTION-RUNTIME-001/review.md`, SHA-256
`8b5f152cd04ae9bbe44bc868802241432c779acae5fa3c01e0828937eb8f9dff`, explicitly accepts migration
016, the three migration-version-only adjacent test changes, and the sequential bootstrap repair.
It reproduces 95/95 and 19/19 respectively. Migration 016 itself has SHA-256
`2540b3249ce1da5fa3a6e5bef154efe9cea5ae7607be14b4221ad456ad76b2e8`.

The observed `841236ae...` value is an older RWO source-closure pin. It does not match the current
Stage-E manifest or current bytes and was not used.

## Owner and generation

The bounded repository search found no Stage-E generator. Ownership is the chain implemented by:

1. canonical sorted compact `source-manifest.json`;
2. exact manifest digest constant in `local_pilot.py`;
3. append-only Stage-E `execution-receipt.md`;
4. exact receipt digest in `execution-receipt.sha256`.

The manifest was deterministically regenerated with Node from its existing inventory, after an
exact precondition check of the prior manifest digest, refreshing all current member hashes and
adding only `implementations/server/runtime/migrations/016_local_execution_graph_runtime.sql`.

## Files changed by this task

| Path | Before SHA-256 | After SHA-256 |
|---|---|---|
| `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` | `919793a406fa4ca7b90b97ab65c6cd23e8c203c57392037ff5735fceffbcc4c2` | `88cb809196e7a42affd2f4f9533f7bbb263ac1122f3bdb0cd805f61c88bbfbc1` |
| `implementations/server/runtime/local_pilot.py` | `41e2d26d2e1bd9ea724012e52a9ec607735390edd0f855e53220fe769ddbe429` | `a85681373790ddbd89688ecdb172ef495c3d7cd5ae26b783dbb21aa21608f830` |
| `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md` | `1706211f85e571eaf92b7dacc1bcadf67fa1e0a0aed3ef047f6a0386d321adca` | `a832f79b09d8db2e0ec5e9c004e8b34cc94283c5987407bc47dba9acdfb3f372` |
| `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256` | `9be85d0dd1329a02367e1694edca6d5f6c39134fcd2554fff5faebb0cb093017` | `f3ab8a3cdce6d5c64c4ef126078809414e276d6bef65ed661831adea99aa0b13` |
| `.codex/workflow-inputs/2026-09-02-stage-e-manifest-repair/CONTEXT-PACK.md` | absent | `212f186df2b495ebdbe3e96c2958f3969e6c633bb0ef4a1b6bd242b7312a1360` |

`source-manifest.json` and `local_pilot.py` were already dirty on entry; this task preserved their
unrelated changes and modified only the integrity cascade. `database.py`, `dispatch_workflow.py`,
the three adjacent tests, and migration 016 were not edited by this task.

## Validation

| Command/check | Result |
|---|---|
| all manifest members recomputed; direct `_verify_source_manifest(repo)` | 84/84, zero missing/mismatch; PASS |
| `python -m unittest implementations.tests.runtime.test_stage_c -v` | 8/8 PASS |
| seven-module execution/compiler/bootstrap/adjacent matrix from predecessor review | 95/95 PASS in 86.193s |
| `python docs/features/agent-provenance-telemetry/contracts/verify_contracts.py` | PASS: 6 ACI vectors, 5 positive, 8 rejection, 16 candidates |
| installer and copy-drift unittest modules | 6/6 PASS |
| receipt sidecar recomputation | exact match |
| `git diff --check` | exit 0; only line-ending warnings on dirty files |

The no-effects probe loaded the exact confirmed opening SHA-256
`4265998b14e796081709510d5a916ab727496529e358f9cbf75b221277d57464`, passed opening validation and
the LIVE-type gate, then exercised the same `HostDispatchHook._runtime_bridge()` used by `open`
against a temporary database. It returned ready at migration 16. The probe stopped before authority
issuance and `bridge.open_dispatch`; the telemetry ledger hash and workflow-directory listing were
unchanged.

## Residue and claim ceiling

- This proves the exact opening can advance beyond Stage-E preflight in the current working tree.
- It does not prove or claim an actual dispatch open, append, session, seat launch, host binding,
  provider/tool execution, external effect, commit, or push.
- The repository remains broadly dirty with unrelated/inherited work; no cleanup was performed.
- The assigned independent reviewer must emit `KEEP` or `FIX` before the parent continues.

## Post-review commit-integration addendum

After the recorded reviewer returned `KEEP`, the commit integrator ran a broader 161-test matrix.
It exposed a valid single-group opening with an omitted optional `connections` property. The
bounded one-line default-to-empty repair changed `dispatch_workflow.py`, so the preceding review is
historical exact-byte evidence rather than approval of the new line.

The Stage-E member digest and verifier pin were refreshed to the repaired bytes. The host suite
passed 11/11, the combined matrix passed 161/161 in 335.760s, and Stage-C passed 8/8. Independent
exact-byte re-review of this post-review repair was not run during commit integration and remains
pending.

## Post-rebase checkout-portability addendum

Rebase replay exposed that the prior manifest/package digest for the appender came from the
ignored host `.agents` copy with mixed line endings, not the canonical tracked `.claude` LF blob.
The selected-registry JSON and frozen-v1 archive also needed explicit LF attributes to reproduce
their committed digests under Windows `core.autocrlf=true`.

A subsequent full manifest-to-`HEAD` blob proof found three older mixed-line-ending pins for the
`experiment`, `register-dispatch`, and `research` skill documents. Each already declared LF, so the
manifest was repinned to its existing committed blob without changing skill content.

The tracked appender and Stage-E pins now bind committed checkout bytes. Copy-drift normalizes only
line-ending representation before comparing content. Stage-C passed 8/8, copy-drift/installer
passed 6/6, the v2 package self-check passed, and all four frozen-v1 members matched their existing
manifest. This locally green portability repair is not covered by the earlier exact-byte review;
independent re-review remains pending.
