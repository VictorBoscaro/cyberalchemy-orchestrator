# Stage E execution receipt

- Executed: 2026-07-24
- Scope: local orchestration logging bridge, operator recovery, and milestone reconciliation
- Owner authorization: `go ahead then, you can fix this issues`
- Authorization evidence:
  `sha256:7bcdc0f29560ce0f3a3e2f13571c1c1759b0f02616986c8715f2eadc3becf17f`
- Result: accepted for the bounded loopback/operator-mediated pilot
- Production/provider/materializer cutover: not authorized

## Externally pinned integrity set

This receipt deliberately binds the verifier from outside its self-checked source manifest. The
manifest is a fail-closed drift detector, not an authentication root.

| Evidence | SHA-256 |
|---|---|
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:686197c241176276b0a4acfbb6dcdd75bc8f485f803dea05763e60cba6dd8427` |
| Stage-E source manifest | `sha256:e57d973d13dfc61fec4fbda08b1a9bfd358a54ef9b780a97a825533fc359a7a5` |
| Stage-C tests `implementations/tests/runtime/test_stage_c.py` | `sha256:ce86cd1eb3354928e988807f5d75948701c247d8c98436a34e43e7b5ca2c16ec` |
| Bridge tests `implementations/tests/runtime/test_orchestration_bridge.py` | `sha256:07576feffac340a13056e2adab7279ec987a52e3af5dc1d07715d09eebf30de9` |
| Validated YAML appender | `sha256:ec4ea40efce5a1026b1a1f7e0be95e74d1dc37199804457e23a815cf9403fca5` |
| Subagent strategy | `sha256:7299f165819748985fbe8e7827721659fbf93731a54d3fe7760e3d6cc009ed54` |
| DomainSpec code type skill | `sha256:e8cb57ffcb40e0107d209971a8459e45cc7eab909d06a84433fe501673a8f0a9` |

The companion `execution-receipt.sha256` pins this receipt, including the reviewer and dispatch
evidence below, without introducing a verifier self-hash cycle.

## 2026-08-03 protocol-compilation integrity addendum

`SWU-ACI-PROTOCOL-COMPILATION-001` added one pure, non-authoritative compiler module, one internal
ArtifactStore application seam, and its bounded tests. Because `service.py`, traceability files and
the new compiler/test are inside the fail-closed local-pilot source boundary, the Stage-E manifest
and its verifier pin were refreshed after the final bytes stabilized. This addendum records
integrity closure only; it grants no API, confirmation, `DispatchSpec`, Run, provider/tool,
production or cutover authority.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/protocol_compilation.py` | `sha256:cb52746c2619de1dcece68c431745c06297ab94b28ce35b3898782abe8005262` |
| `implementations/server/runtime/service.py` | `sha256:a80574d71191d871013387cfb35f883ae28229dad6f2f9c43309a0c1efcbf11f` |
| `implementations/tests/runtime/test_protocol_compilation.py` | `sha256:7211ff29dd48cbd3af778138a7c5927f9a16cd441cad00d2a847070008a76181` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:74cb27f8ba542ffefce931c5f9f3afa880d5b27458de75270a44d492016672aa` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:ec714aabd52e7aa6a88a7276e207eb388198d2542784b7901bc31d517469fab0` |
| Stage-E source manifest | `sha256:0641c92d35a0bbaa9ab6a31f1383127d375d462b82b1dbfb5f1bf8c591bfa5eb` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:6b34d99e9efbaf00eb0a447c80be1967909763042bfc4f25cf22a7d56a47a392` |

Verification results:

- focused protocol-compilation plus traceability: 13 tests, PASS;
- complete runtime discovery: 131 tests, PASS in 86.617 seconds (root re-run after final repin);
- independent authority-boundary re-review: PASS;
- independent spec/test re-review: PASS for bounded PC1–PC12 evidence; residual risks are structural
  PC12 coverage and generated rather than separately versioned negative vectors.

## 2026-09-01 CONF-001 integrity addendum

`SWU-ACI-CONFIRMED-DISPATCH-001` added the bounded durable writer that accepts the reviewed
CONF-000 authority package and atomically reaches `opening_pending`. The accepted unit contains the
immutable observation, derived confirmed authority, run/graph/mappings, exactly nine new artifact
metadata members, two events, a version-2 run head, a stable receipt, and one pending unclaimed
generic audit-opening effect intent. No API, UI, CLI, host hook, provider/tool start, effect claim,
agent launch, continuation, deployment, or other external action was added or performed.

The post-implementation red-team found and closed three bounded gaps before handoff: preliminary
same-key replay now preserves and validates prerequisite heads in the command digest; all 56 frozen
negative vectors are bijectively dispatched from their own action/error/postcondition fields with
complete authority-table snapshots; and capability-preview reads verify authorized finalized bytes,
content identity, schema, media type, classification, all four policy references, policy-bundle
digest, and finalization receipt through a metadata-preserving artifact-store seam. The Stage-E
baseline also now pins migration 011, which was already executed by `database.py` but absent from
the integrity manifest.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/012_runtime_confirmation.sql` | `sha256:de1fb043c7593219595a0f86c822a9a13cb7f01861fb2cf88db9f2b434d6a4e0` |
| `implementations/server/runtime/database.py` | `sha256:4780da075e0453fe81665ea15ae8a7fef259f4a398b18b7951646dad977543f5` |
| `implementations/server/runtime/errors.py` | `sha256:4de30cb67cf13053cdd633e7ea4c9c161b40bf9350c56974989b182ea5e8f0d3` |
| `implementations/server/runtime/artifacts.py` | `sha256:e1a02b2580498c1b6eeb2741cb4303b45570396519228c0b138135ec7d8f1354` |
| `implementations/server/runtime/confirmation.py` | `sha256:9340b1429f29e44512dd8a13688e2885e57ff82bc302f5bdff51a9538721850c` |
| `implementations/server/runtime/journal.py` | `sha256:cd6725b7d39fe8f92d041ee3b529bea0b6b7f47918e9ca3e8f5d83fa146ee86d` |
| `implementations/server/runtime/migrations/011_bus_reveal_delivery.sql` | `sha256:2d798ab2ab8c6962e0a6f67ad17665ad4d8b441a9b26fe72d9e2c08df44877e1` |
| `implementations/server/runtime/service.py` | `sha256:9a5957495f0ab330af95a7e94dee27147d82476143675d73daa99033b034bb0c` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `sha256:ba2678c819e0395d438780afff3d66e534cfbaaca4d9137f68680d35e70cda4f` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:3567375773651369ce034282516db9fd645ab97106622970a04b6b8a0b3a04d0` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:e10a146875c40d6effeed6030a081f4a991c01d71804e957563f68343a13ced3` |
| Stage-E source manifest | `sha256:d29d7959fde52f6f7a67b50382dd2e7c52bc8ae395713cbcca9d095d2f6bbb92` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:e0a774822b45748c54801ea5d13fab50014d4858ad110662f76a8a1f38ee32b2` |

Verification results:

- focused confirmation: 8 tests, PASS, including all 56 negative cases, all 21 failpoints and a
  complete post-reopen comparison of the AUTH1 durable unit;
- focused Stage-B: 6 tests, PASS;
- ACI traceability: 1 test, PASS;
- Stage-C verifier: 8 tests, PASS;
- orchestration bridge: 18 tests, PASS;
- complete runtime discovery: 160 tests, PASS in 61.799 seconds;
- Python compileall: PASS;
- `git diff --check`: PASS; line-ending conversion warnings only;
- strict DomainSpec code tagging: unavailable in the installed repository skill/command set and not
  invoked through the external DomainSpec checkout because the tagger may mutate paths outside this
  SWU's exact 14-path write scope.

### Concurrent-writer freeze incident

After the first implementation pins were prepared, several unattributed post-pin writes changed
`test_runtime_confirmation.py`, then `artifacts.py`, `service.py`, the Stage-E manifest, the local
pilot pin, and this receipt between 03:46:55Z and 03:51:43Z. A monitored focused run exposed the
`artifacts.py` regression as an `AttributeError`. Process observation showed an appserver and its
code-host child, but the available evidence does not attribute any individual write to either
process. The parent operator stopped those processes before restoration.

The final metadata-preserving read seam, service checks, and regressions were restored without
overwriting the useful concurrent test enhancements. Two reads three seconds apart were stable
before repinning. The final 14-path snapshot then remained byte-identical after every one of the
eight required validation commands. No commit, push, deploy, provider/tool invocation, agent
launch, or external effect was performed by CONF-001.

## Verification

- Integrated Python runtime: PASS, 54/54.
- Compatibility agent runtime: PASS, 31/31.
- Pure TypeScript APT contracts: PASS, 27/27.
- TypeScript typecheck: PASS.
- Python compileall: PASS.
- Stage-E source-manifest verification: PASS.
- `git diff --check`: PASS; line-ending conversion warnings only.

## 2026-09-01 CONT-001 persisted-replay repair addendum

Independent review exposed one MAJOR in the CONT-001 replay path: an accepted suspension was
reconstructed by joining the current source Attempt and current confirmed mapping rows before the
generic journal replay. Consequently, post-commit drift in a confirmed mapping could reject an
otherwise byte-identical retry before `RuntimeJournal.accept` returned its durable receipt.

The bounded repair changes only the persisted replay projection. It now reconstructs the command,
event and semantic intent from `agent_continuations` plus the ordered
`agent_continuation_mapping_members`; it does not re-read the current Attempt, confirmed mappings or
official facts. Caller discriminant drift remains fail-closed through the generic journal
idempotency conflict. A new negative mutates the current mapping after commit and proves that an
identical retry returns the original receipt while a changed provider-reference digest conflicts.

The existing Stage-E source manifest already fixed the repaired bytes and was not repinned:

| Repaired evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/service.py` | `sha256:7e4d9147e98eebdd3c92aa4bafb9200c0166334ce3b00b9a0f9c229b4eeecfe7` |
| `implementations/tests/runtime/test_agent_continuation.py` | `sha256:f60aaf02213624af068efb30bb11a381111535c5b3e7963783a6884b2c439c0a` |
| Stage-E source manifest | `sha256:56a4438b5c3f1e23ec1a2c98a405e791d52c418dbf02b204cba053d3c5527259` |

Repair verification:

- focused CONT-001: 10 tests, PASS;
- focused CONF-001 regression: 8 tests, PASS;
- Stage-C verifier plus orchestration bridge: 26 tests, PASS;
- curated runtime regression: 248 tests across 26 modules, PASS in 148.795 seconds;
- bounded Python compileall and `git diff --check`: PASS.

By explicit user direction, literal runtime discovery was replaced for this repair closure by a
curated module invocation that omitted an external out-of-scope artifact without reading or using
it as evidence. This substitution does not expand the CONT-001 component claim or repin unrelated
Stage-E sources.

### 2026-07-25 code-type hardening

- Orchestration bridge: PASS, 17/17, including pinned DomainSpec `code_contract` acceptance,
  missing-contract rejection, planner FAIL rejection, path-escape rejection, and exact-topology
  enforcement, plus brownfield/readiness equality and closed capability-profile enforcement.
- Stage-C verifier: PASS, 8/8.
- Ledger reader/classification suite: PASS.
- Skill package validators: PASS for strategy, DomainSpec implementation, and registration.
- Appender JavaScript syntax and Stage-E source-manifest integrity: PASS.
- Total executable tests: 112.

## Independent review

Two independent auditors reviewed the bridge before launch authorization and completed two bounded
loops:

- Security review attacked authority, crash consistency, idempotency, appender locking, and
  filesystem/secret exposure.
- Integration review attacked operator usability, end-to-end CLI coverage, status reconciliation,
  source-integrity evidence, and release claims.

Their final findings required operation-specific expiring capability binding and consumption,
trusted-internal method clarification, CLI token/scope/action/source-manifest tests, owner metadata
and safe recovery for stale appender locks, corrected close retry labels/ordering, a supported log
query, reproducible operator commands, corrected local-pilot documentation, this external
integrity receipt, and a native dispatch close. Those items were implemented and verified before
the close was accepted. The remaining limitation is explicit: Codex host integration does not yet
make this bridge an automatic mandatory wrapper around `spawn_agent`.

## Native infrastructure evidence

- Database:
  `telemetry/runtime/local-pilot/aci-apt-stage-c.sqlite3`
- Dispatch: `2026-07-24-orchestration-bridge-review`
- Session: `ses_1f5d704231d1b706fb96b91987cdaefb`
- Session start: offset `11`, event `evt_766c38e4ea79b62874a653f5ce47939e`,
  command `cmd_bd73047d0aa0566de6b386203082ee55`
- Session-to-Dispatch link: offset `12`, event `evt_6fe8fa75499d42534c2737d209079f0e`,
  command `cmd_cea5ed31ac82e01c1d534557e24c8a6c`
- Orchestration opened: offset `13`, event `evt_ae9c055f9ef5268667312d55ed71f2d9`,
  command `cmd_37e9b2a5202a8ebbbf380c425589a836`
- Orchestration closed: offset `14`, event `evt_bb19e27f24412996d59d2490b2e3a8ac`,
  command `cmd_e7df97b80cfef9300bfa27484d3f9fca`
- YAML opening row:
  `sha256:7d8a274afd469b2be7849d2e4804a6808f46cd9ed407ce005135974b8af5fe3f`
- YAML close row:
  `sha256:0e914656b5b32cb49d94b7453a30bef0f48a250e5974bbe213f807a21306362b`
- Ledger after close:
  `sha256:22f6e21492444825a657e5d2f4b19e852735aaf31a7b07d25646531a8c6bace7`
- Journal after close: 8 accepted groups, effective through offset 14, SQLite `quick_check=ok`,
  WAL mode, synchronous full, foreign keys enabled.

The historical opening predates capability consumption and the appender's `output_mode` emission
fix. It remains append-only and is disclosed rather than rewritten. The close used the final
capability-gated implementation.

## 2026-09-01 CONT-001 integrity addendum

`TASK-CONT-001` implements the bounded, effect-free `AgentContinuation` suspension writer on top
of the accepted CONF-001 authority. It adds isolated migration 013, a pure continuation reducer,
confirmation-relative UTC deadline derivation, immutable attempt/snapshot bindings, exact
zero-of-two official-fact admission, same-transaction TOCTOU rechecking, and stable replay through
the generic runtime journal writer. The runtime derives the fixed continuation scope and
`suspend@1` idempotency key; callers cannot supply either. No API, UI, CLI, provider/tool start,
agent launch, effect intent, effect claim, deployment, or external action was added or performed.

The implementation is bound to descriptor
`sha256:e440c54ee65aa4c90596aca12dbcbef9b86e3d919d869e7fd66babc4812ad620`
and readiness evidence
`sha256:cc017802059b3a4a29f5af232c0bc0b05c023861cae139e39cc4b3db9e6ee6a0`.

The post-implementation red-team found and closed one transactional authority gap and one proof
gap. The mutation closure now compares the complete frozen source-attempt row and reconstruction
snapshot row, revalidates requested and terminal journal linkage, and rejects target-attempt races
before inserting anything. Tests now inject drift into agent instance, seat, turn, operation,
version, requested event, terminal event/offset, and snapshot linkage; snapshot all journal,
continuation, receipt, artifact, effect, and attempt surfaces at every rollback failpoint; and prove
identical and divergent concurrent requests converge to one durable unit with the required receipt
or typed conflict. Replay still precedes current official-fact admission.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/013_agent_continuation.sql` | `sha256:80f32c1a389ee0e773d69342cb407542f87a2e6760c99f902b7c9d5cbbf828c9` |
| `implementations/server/runtime/database.py` | `sha256:ccebed82678d943145bfd67d81ef47ca4f1db56cf5296690fc4243c834a081f6` |
| `implementations/server/runtime/continuation.py` | `sha256:688a351ffcf1f19c9e948798de86ebc3f610fa69f8a25a0d0ba60ec28339ad89` |
| `implementations/server/runtime/errors.py` | `sha256:be342cf8470a4897e7378297567b6b763088491f75081d5671d657c44dd30843` |
| `implementations/server/runtime/service.py` | `sha256:acf93c2555f4bd5d2d50f35f5e7f5fca26dd718fb6aff168eaa3d1f443ecb0d3` |
| `implementations/tests/runtime/test_agent_continuation.py` | `sha256:4e60af0b51054a54e231604eddb5adeb3ebd6a81c7dafc6e98ba86cf5ef44ae6` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `sha256:49929b9db7a9deb2e4b3378b490ce4941f30da9d716c035dd2475deceb24c498` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:f02888ee2a48bc64320ebb9a22c4ceb675d998e8590f4c1f998152742036bf10` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:de7bcd4094f49dba2294dc174584622573148cc78022429ecbcfce071dbcc4eb` |
| Stage-E source manifest | `sha256:0f130e89cef8596883f4bb27ad38b31658e05c3e72a2480aedab2a35a387b0c7` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:68b1b21551e41c07744dfa89abdd6bf1364d32918f863defcc5cdf6ac0883981` |

Verification results:

- focused continuation: 9 tests, PASS;
- focused confirmation: 8 tests, PASS;
- focused reference delivery: 5 tests, PASS;
- ACI traceability: 1 test, PASS;
- Stage-C verifier: 8 tests, PASS;
- orchestration bridge: 18 tests, PASS;
- complete runtime discovery: 169 tests, PASS in 74.731 seconds;
- canonical Control Center discovery from `implementations/`: 36 tests, PASS in 55.802 seconds;
- Python compileall: PASS;
- `git diff --check`: PASS; line-ending conversion warnings only;
- strict DomainSpec code tagging was not invoked because the available tagger may mutate governance
  paths outside the exact CONT-001 write scope.

## 2026-09-01 HEADS-001 integrity addendum

`SWU-ACI-RUNTIME-RUN-GROUP-HEADS-001` adds the bounded component foundation for isolated Run and
Group heads. Migration 014 creates only `runtime_run_heads` and `runtime_group_heads`, directly
parented by the confirmed Run/graph, with no backfill or legacy mutation. The pure `run_group.py`
module implements the closed RunLifecycle and GroupLifecycle reducers, the fixed two-seat decision
rule, terminal exit mapping and a fail-closed opening execution fence.

The accepted claim is component evidence only. Positive opening evidence exists solely in the
explicitly labelled test harness; there is no audit-opening materializer/verifier, service/API
method, production Run/Group writer, effect release/claim, attempt start, provider/tool call,
adapter invocation, deployment or other external action. `opening_pending` and
`reconciliation_required` remain ineligible.

The implementation is bound to amended descriptor
`sha256:208cdea8da659d3e85da783d3264ea2a6a5b1ea5c035fed2ef3cf7d4fae5f5da`
and readiness receipt
`sha256:14a40fa75e9ad1333acb8200cf193a46c2223296285fda384f35e0a36496792e`.
The amendment added only the mechanical confirmation migration expectation required by version 14.

Independent red-team review found and closed three proof cycles before handoff. The journal-backed
harness now binds complete projections and confirmed Run/graph/group identities into semantic
intent, revalidates exact graph and prior event identity, admits only reducer-produced transitions,
requires both runtime-managed mode and unique frozen digest for Run creation, proves Group
`v0 -> v1 -> v2`, and rejects stale Group evidence and a stale Run prerequisite on a Group-only
mutation without changing either head. Exact replay still returns the original receipt; semantic
or evidence drift conflicts.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/014_runtime_run_group_heads.sql` | `sha256:0b5c7e3e363bfe1d4778145a0933207cfb9ec610ca067c64f907e95a80a63ef3` |
| `implementations/server/runtime/database.py` | `sha256:a184d5dff427936d32cb18cb210741837be54e064679ac5da0bca90667de2c2c` |
| `implementations/server/runtime/run_group.py` | `sha256:9d16960cfb48a720c887bd816edbe8d3b243af04c679c50f30ec7bd83484df29` |
| `implementations/server/runtime/errors.py` | `sha256:ad4aef95054838e82d34913d37bcd4688fa997e28d463d741202ecd7bc432168` |
| `implementations/tests/runtime/test_runtime_run_group_heads.py` | `sha256:c53830c504941f0f203aacdd94d4ea65ddd35a5f0715595985dcc957c8ed2445` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:b65887f16f7f37c08219d6cd45e021b8d57193737a1923f90a487ff035baa2df` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:644cc5717ff5b47db1156bf684f3e77fa19e6515c753f8d6e6384c14fb8bd06d` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `sha256:5831c280d36c4d446a1609be674a7a922dbe33633f7e84321604b4b848449918` |
| Stage-E source manifest | `sha256:7f2df9e474d9f9a589a1c4d5adc770fbaadff20aa4e161cfc1bebff79ca3619c` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:ac1eb2baa1cac603a6cd6c28c752a462dc79cf7337f1e97b5b4420df146a8c63` |

Verification results:

- focused HEADS-001: 7 tests, PASS;
- focused continuation: 9 tests, PASS;
- focused confirmation: 8 tests, PASS;
- ACI traceability: 1 test, PASS;
- Stage-C verifier: 8 tests, PASS;
- orchestration bridge: 18 tests, PASS;
- complete runtime discovery: 176 tests, PASS in 74.943 seconds;
- Python compileall: PASS;
- `git diff --check`: PASS; line-ending conversion warnings only;
- strict DomainSpec code tagging was not invoked because no scope-safe, non-mutating strict tagger
  is available in the accepted validation contract.

### HEADS-001 group-identity repair

A later BUS architecture audit found that migration 014's initial primary key omitted the confirmed
graph/run scope even though the normative Group identity is `(run_id, group_id, group_version)`.
Because each confirmed graph uniquely binds its Run, the repaired physical identity is
`(graph_id, group_id, group_version)`. The earlier HEADS hash set above is retained as historical
pre-repair evidence and is superseded by this final set.

The focused harness now creates two different confirmed graphs/runs that both own local
`group_authoring` version 1, advances both independently through CAS to aggregate version 2,
reopens SQLite at each boundary, rejects a duplicate tuple in the same graph and rejects a stale
prior-event CAS without changing either aggregate. Every Group read/update in the harness includes
the exact `graph_id`. Before reading or changing either head, the mutation closure also revalidates
in the same transaction that the confirmed graph is parented by the supplied Run. Both crossed
pairs (Run A with graph B and Run B with graph A) are rejected without changing any journal or head
surface.

| Repaired evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/014_runtime_run_group_heads.sql` | `sha256:44e17ec6cd9b9ed917a68142145ebb8f378aca02872758ed7d43a8f3b3d0ca93` |
| `implementations/tests/runtime/test_runtime_run_group_heads.py` | `sha256:4802bc36934825832a907b8006aa16126350f8e8d3e70a04d7b2245cdb977e7e` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:cada57580fba510e70d1bf579fea0f1542b7e826eb555296610579fb9ba0a30b` |
| Stage-E source manifest | `sha256:8f188b4d619f0bf16c7b47dff6756b6e2ef6051fa89c643de8faf3a057fb027f` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:2d06ee178362c12006a6cfe390899ea3b9bed9eac8b2b7963beb2593eb177bad` |

Post-repair verification:

- focused HEADS-001: 8 tests, PASS;
- focused continuation: 9 tests, PASS;
- focused confirmation: 8 tests, PASS;
- ACI traceability: 1 test, PASS;
- Stage-C verifier: 8 tests, PASS;
- orchestration bridge: 18 tests, PASS;
- complete runtime discovery: 177 tests, 618 subtests, PASS in 74.03 seconds;
- Python compileall and `git diff --check`: PASS.

## 2026-09-01 BUS-001 integrity addendum

`SWU-ACI-RUNTIME-ATTEMPT-RESULT-BUS-001` adds the bounded component proof from one exact confirmed
continuation mapping, one authenticated completed Attempt and one persisted publication candidate to
one official message and its ordered accepted-event pair. Migration 015 creates only
`runtime_attempt_result_acceptances`, with direct confirmed mapping, Run, graph, Attempt, candidate,
event and composite Group parents; it performs no backfill or legacy mutation.

The pure `confirmed_bus.py` kernel verifies the complete frozen mapping version and binding digest,
including target, slot and canonical visibility policy; derives the exact graph-scoped Group
aggregate; authenticates the immutable publication event, receipt bytes, command receipt and
contribution artifact against the completed Attempt scope; and derives stable acceptance, command
and event identities. `attempt.result_accepted` is a non-transition link fact. Both ordered events
live on the exact Group stream at the prior versions `+1` and `+2`; only the second event applies the
declared Group self-transition. The composite Group head and generic aggregate head end at the same
official event/version/offset, while BUS acceptance leaves the completed Attempt projection and its
post-publication aggregate head unchanged.

The accepted claim remains component evidence only. The positive writer is test-only and invokes
the existing journal as a harness. There is no production publisher, service/API route, opening,
continuation creation, effective-input materialization, resume, effect request/claim, provider/tool
call, adapter invocation, deployment or external action. `PRODUCT-PASS`, `CONT-002` and every such
production surface remain blocked outside this SWU.

The implementation is bound to descriptor
`sha256:cfc8f64d052f9adc5f85e5ce63985f6b90ed7ce6c55845c7d379ac117f21ca53`
and code-readiness receipt
`sha256:b5d09dd470fd3beeb9d5e5d7be0d28df6f2c5af22baa653c9545afe52bd497e3`.

Independent red-team review returned final `PASS/KEEP` after the proof closed: strict canonical
receipt equality and artifact integrity; exact four-event Attempt and pre-accept Group journal
chains; coherent candidate/event/command lineage; Group-stream version/head alignment; complete
authority-negative coverage including coherent two-row scope drift and frozen mapping digest
drift; atomic rollback/replay/race behavior; isolated migration proof; and unchanged actual
`_continuation_official_facts` visibility at zero, one and two exact official sources.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/migrations/015_runtime_attempt_result_bus.sql` | `sha256:242bdc82394d0e0c52a6dd629bfbcea6f258420843227aea6e49d054180991d9` |
| `implementations/server/runtime/database.py` | `sha256:4f04c889d4b0f7b4cf6f6a58d93c445dd3201c801e78fd22a83777fac9fcae66` |
| `implementations/server/runtime/confirmed_bus.py` | `sha256:1e4573cbcf7c3c50dbc062bf36d0b07f85630fb1c27c7eca3fc0a39c34c6659f` |
| `implementations/tests/runtime/test_runtime_confirmed_bus.py` | `sha256:80ae84ed0ba2f38c6281f6214eb0bd524be134346a30e50df31df50992b71a3e` |
| `implementations/tests/runtime/test_runtime_run_group_heads.py` | `sha256:0cbdb756728b5bd99f7e41a2530cc824b079fda9ed6bfe796097bcabe0237ac1` |
| `implementations/tests/runtime/test_runtime_confirmation.py` | `sha256:31cdbded7c452fc54418d5b97e38ba1cb0980d3aa7b8fcaee2c202bfe5545d9e` |
| `implementations/tests/runtime/aci-test-traceability.json` | `sha256:d7af43552f6b7c37ca3129812b9fa3116eecc9207eddacc8b5a4dbed8ef780c9` |
| `implementations/tests/runtime/test_aci_traceability.py` | `sha256:c9db1c8c88eb185f4952986eccf6babeea68be669ddd206d7ea3f413774d10c5` |
| Stage-E source manifest | `sha256:e3232eb2b74e201f0a717e1ca42c2814f37ef79c54503b76e6654cc8b31337bd` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:6d4359456d86169e344838807e550fbba238aef46fb59e4d07b19d3a4a29fb34` |

Verification results:

- focused BUS-001: 23 tests, PASS in 6.375 seconds;
- focused HEADS-001: 8 tests, PASS;
- focused continuation: 9 tests, PASS;
- focused confirmation: 8 tests, PASS;
- ACI traceability: 1 test, PASS;
- Stage-C verifier: 8 tests, PASS;
- orchestration bridge: 18 tests, PASS;
- complete runtime discovery: 200 tests, PASS in 79.787 seconds;
- Python compileall: PASS;
- `git diff --check`: PASS; line-ending conversion warnings only.

## 2026-09-01 upstream RWO rebase integrity refresh

Rebasing onto accepted upstream commit `2e373f7` changed the pinned dispatch-workflow source and
test bytes. This refresh binds those exact upstream bytes in the Stage-E manifest and updates the
local-pilot manifest pin. The two upstream paths have no branch-local diff from `origin/master`.

This is integrity closure only. It does not claim behavioral compatibility between the upstream
RWO workflow revision and the repository's existing ACI workflow fixtures or root-governance
layout.

| Evidence | SHA-256 |
|---|---|
| `implementations/server/runtime/dispatch_workflow.py` | `sha256:85f13889d01b56b7427ac2c883d71ef0577c9e4e7fcb2c45cda1db5f2d0654fd` |
| `implementations/tests/runtime/test_dispatch_workflow.py` | `sha256:4b880deac5c5ac74605f7e82cf5f4e94126199af38295f114d101a76c24a1fef` |
| Stage-E source manifest | `sha256:b2160ab37d0cf1648ba422123f6abe27323406313af25c8fc5524b70817b9d6f` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:f9ec5b9efd7ba0cd56af4edaf2dff488220adf539e2d5e9b5f3daa0d04841f16` |

Verification results:

- bounded confirmation, continuation, heads, bus and policy suites: 108 tests, PASS;
- Stage-C manifest and preflight suite: 8/8, PASS;
- hook and bridge suites: 28/29, with one upstream workflow-manifest shape error;
- complete runtime discovery: 267 tests, 7 failures and 15 errors, all retained as unresolved
  upstream integration evidence rather than reported as passing.
