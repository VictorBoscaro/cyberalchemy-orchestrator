# HEADS-001 — final implementation evidence

## Result

`IMPLEMENTED-REVIEWED-PASS / KEEP` for the bounded HEADS component.

Migration 014 and the harness use exact Group identity `(graph_id, group_id, group_version)`. Before
either head mutation, the journal-supplied transaction verifies that
`confirmed_turn_graphs(graph_id).run_id == run_id`. Both crossed pairs—Run A with Graph B and Run B
with Graph A—reject without changing any journal, Run head or Group head surface.

Harness-only positive transitions remain component evidence, not opening-materialization evidence.
HEADS adds no service/API, production Run/Group writer, effect, provider/tool call or external
action. CONT-002 remains `not-promoted`; this result authorizes only the separately bounded BUS-001
readiness gate.

## Historical entry authorization

| Artifact | SHA-256 |
|---|---|
| Pre-implementation descriptor | `sha256:208cdea8da659d3e85da783d3264ea2a6a5b1ea5c035fed2ef3cf7d4fae5f5da` |
| `domainspec-code-readiness@1` receipt | `sha256:14a40fa75e9ad1333acb8200cf193a46c2223296285fda384f35e0a36496792e` |

These remain historical authorization for the old scope; they are not post-repair promotion
evidence and are not repinned.

## Repair-closure authorization

| Artifact | SHA-256 |
|---|---|
| Amended repair descriptor | `sha256:bb3c7ffc4aa7039551b42accc3c9694b993187fccd9e53980f1e745b0123eecd` |
| Fresh repair readiness | `sha256:9328de32077ae6938bb22fc1117a58135a8d7bae17736cdec969ace1692018f2` |

The readiness was `PASS` only to enter the bounded repair over the same ordered twelve paths. It is
preserved as historical entry authority and is not repinned to final implementation bytes.

## Coordination incident and repair-entry snapshot

| Artifact | SHA-256 | Evidence |
|---|---|---|
| Reopened descriptor before amendment | `sha256:8d68b0f381f44f492703a6eef8480f2d50c39d7a2b8b2b2db25d72a7f3c5841f` | represented the first MAJOR |
| Migration 014 | `sha256:44e17ec6cd9b9ed917a68142145ebb8f378aca02872758ed7d43a8f3b3d0ca93` | graph-scoped Group key present |
| Focused HEADS test | `sha256:3871363e15dd2462bb5c9dafdd0ea860aea76ca5e047ae02c5520919370c4ebc` | pre-second-repair snapshot; lacked cross-pair negatives |
| `source-manifest.json` | `sha256:0a73a9bab6a42cc90456e3cc6386426407ebd06b9ed586d45a04bc0a968e7a66` | refreshed before descriptor drift was observed |
| `local_pilot.py` | `sha256:b037c52ef17c26a150da89c94430e8d1a753d73ab7dc828259977d594a97b964` | refreshed before stop |
| `execution-receipt.md` | `sha256:9255877dde09b833561471aa9b7f70eacf0c72258221bb8f7c2832356057201f` | refreshed before stop |
| `execution-receipt.sha256` | `sha256:33fdbb121491175f9c055bff0b226cf5407cd922e962e91e82af9c1261eddcca` | deliberately stale; still names `ef5982e3...` |

The original descriptor/readiness authorized the same twelve paths. While the coder was already
repairing in-scope migration/tests under the root instruction, the descriptor was changed to the
reopened digest. The coder then completed the in-scope manifest/local/receipt refresh before seeing
the drift and stopped before the sidecar. The repair-closure descriptor/readiness then established a
new clean entry snapshot before the final repair resumed.

## Final repaired bytes

| Artifact | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/014_runtime_run_group_heads.sql` | `sha256:44e17ec6cd9b9ed917a68142145ebb8f378aca02872758ed7d43a8f3b3d0ca93` |
| `implementations/server/runtime/database.py` | `sha256:a184d5dff427936d32cb18cb210741837be54e064679ac5da0bca90667de2c2c` |
| `implementations/server/runtime/run_group.py` | `sha256:9d16960cfb48a720c887bd816edbe8d3b243af04c679c50f30ec7bd83484df29` |
| `implementations/server/runtime/errors.py` | `sha256:ad4aef95054838e82d34913d37bcd4688fa997e28d463d741202ecd7bc432168` |
| `implementations/tests/runtime/test_runtime_run_group_heads.py` | `sha256:4802bc36934825832a907b8006aa16126350f8e8d3e70a04d7b2245cdb977e7e` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:cada57580fba510e70d1bf579fea0f1542b7e826eb555296610579fb9ba0a30b` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:644cc5717ff5b47db1156bf684f3e77fa19e6515c753f8d6e6384c14fb8bd06d` |
| `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` | `sha256:8f188b4d619f0bf16c7b47dff6756b6e2ef6051fa89c643de8faf3a057fb027f` |
| `implementations/server/runtime/local_pilot.py` | `sha256:2d06ee178362c12006a6cfe390899ea3b9bed9eac8b2b7963beb2593eb177bad` |
| `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md` | `sha256:e86a9ea76be568facd13a17cafecc053021b1c14384d6c1e81d9f4626e67f2be` |
| `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256` | `sha256:ce9eacfd971673a37303e8f1bb853a7760e19a0b20b0d1120078ed3407693a67` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `sha256:5831c280d36c4d446a1609be674a7a922dbe33633f7e84321604b4b848449918` |

The sidecar names the final receipt digest exactly. The Stage-E manifest reproduces 72/72 entries.

## Final validation and review

- Focused HEADS: 8/8 PASS.
- CONT: 9/9 PASS.
- CONF: 8/8 PASS.
- Traceability: 1/1 PASS.
- Stage-C: 8/8 PASS.
- Orchestration bridge: 18/18 PASS.
- Complete runtime discovery: 177 tests, 618 subtests, PASS.
- A/B and B/A graph/run probes: rejected with zero journal/head mutation.
- Python compileall and `git diff --check`: PASS.
- Independent red-team: `PASS / KEEP`; no finding remains.

This promotes HEADS-001 to `implemented-reviewed-pass` only. BUS-001 remains a separate component
proof, and PRODUCT-PASS still blocks opening, Run `ready`, effective input, resume, effects and any
adapter/provider execution.
