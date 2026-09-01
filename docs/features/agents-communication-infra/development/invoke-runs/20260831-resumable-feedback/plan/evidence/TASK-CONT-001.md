# TASK-CONT-001 — implementation evidence

## Result

`PASS` for `SWU-ACI-AGENT-CONTINUATION-001` as a bounded component/consumer capability.
`TASK-CONT-001` is `implemented-reviewed-pass`: migration 013 and the continuation kernel/service
persist one CONF-001-backed, effect-free suspension with deterministic replay, transaction-local
zero-of-two revalidation and no legacy authority or production attempt-writer claim.

This promotion permits planning the exact CONT-002 work pack. It does not authorize official-input
resolution, target attempt/effect creation, resume/reconstruction/cancellation, adapter/provider
work, production use, commit, push or deploy.

## Historical entry authorization

| Artifact | SHA-256 |
|---|---|
| Pre-implementation descriptor bytes | `sha256:e440c54ee65aa4c90596aca12dbcbef9b86e3d919d869e7fd66babc4812ad620` |
| `domainspec-code-readiness@1` entry receipt | `sha256:cc017802059b3a4a29f5af232c0bc0b05c023861cae139e39cc4b3db9e6ee6a0` |

The descriptor is promoted after implementation, so its current digest intentionally differs from
the entry digest. The readiness JSON remains the immutable entry authorization and is not repinned.

## Final integrity pins

| Artifact | SHA-256 |
|---|---|
| `implementations/server/runtime/service.py` | `sha256:acf93c2555f4bd5d2d50f35f5e7f5fca26dd718fb6aff168eaa3d1f443ecb0d3` |
| `implementations/tests/runtime/test_agent_continuation.py` | `sha256:4e60af0b51054a54e231604eddb5adeb3ebd6a81c7dafc6e98ba86cf5ef44ae6` |
| Stage-E `source-manifest.json` | `sha256:0f130e89cef8596883f4bb27ad38b31658e05c3e72a2480aedab2a35a387b0c7` |
| `implementations/server/runtime/local_pilot.py` | `sha256:68b1b21551e41c07744dfa89abdd6bf1364d32918f863defcc5cdf6ac0883981` |
| Stage-E `execution-receipt.md` | `sha256:f8564f24b0efe9bd3d2f3d101001001eec5a90b5c4b34c1f6f0cfe4a0d0d6dbe` |

## Verification evidence

- Focused continuation suite: 9/9 PASS.
- Required regression suites: 40/40 PASS.
- Complete runtime discovery: 169/169 PASS.
- Control Center canonical suite, executed from `implementations` as required by its README:
  36/36 PASS.
- T-ACI-CONT1 and the L2/base T-ACI-CONT9 matrix pass, including invalid transitions, authority
  substitutions, zero/one/two/ambiguous official-fact states, transactional TOCTOU, replay after a
  later fact, semantic drift, migration/reopen, failpoints and zero effects.
- Migration 013 uses isolated runtime tables with direct CONF-001 parents, zero backfill and no
  legacy schema/row/behavior change.
- The independent implementation reviewer returned `PASS` for the bounded claim.

## Promotion boundary

CONT‑001 proves only durable suspension and query/replay behavior for a writer-confirmed source.
The full attempt prerequisite remains a test-only journal-backed harness, and production
`ACI_SCHEMAS` is unchanged. CONT‑002 must receive its own exact work pack, audits and fresh readiness
before official inputs, target work or any effect is implemented.

