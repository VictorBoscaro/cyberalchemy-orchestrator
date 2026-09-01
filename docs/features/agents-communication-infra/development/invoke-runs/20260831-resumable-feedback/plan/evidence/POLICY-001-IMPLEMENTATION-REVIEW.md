# POLICY-001 implementation review

Date: 2026-09-01

Unit: `SWU-ACI-EXECUTION-POLICY-LINEAGE-001`

Verdict: **PASS / KEEP**

This receipt freezes the independently reviewed POLICY-001/L1 implementation. The claim is limited
to one test-only, file-backed SQLite seam that atomically persists and reopens the exact seven
POLICY-000 members plus one closed non-executable lineage receipt. It proves deterministic
replay/conflict, crash atomicity, exact byte/digest reproduction and zero runtime authority or
external effect. It does not promote POLICY-002/L2, POLICY-003/L3, product-selected policy,
production migration/service/journal/API integration, confirmation, opening, provider launch or
host enforcement.

## Entry-authority snapshots

The descriptor and readiness receipt below are immutable snapshots of the pre-implementation code
entry gate. Their `not-started-ready`/absent-output language records the state that authorized the
mutation; it is not the current implementation status and must not be repinned after the outputs
exist.

| Entry artifact | SHA-256 | Role |
|---|---|---|
| `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-EXECUTION-POLICY-LINEAGE-001.json` | `sha256:21a45e5cb7bc79afd1daaabfeb45dbae269be85015f09824327cbfdf49bee682` | Historical exact task, scope, dependency and validation authority. |
| `docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-EXECUTION-POLICY-LINEAGE-001-code-readiness.json` | `sha256:43b49b780d3d7a2658bd6c30536a54599cd5c290b46973e87b02dc941257eb47` | Historical `PASS` capability and write-scope gate. |
| `docs/features/agents-communication-infra/work-pack/tasks/TASK-POLICY-001.md` | `sha256:60a8351d70b5c38011fb08a45ecbe52757e4596156ee1dcd9fbece197fe4a543` | Bounded L1 decision question and proof obligations. |

The readiness receipt's `work_pack_digest` is the exact descriptor digest above, and the readiness
receipt points to that same entry snapshot. This final review supplies output evidence; it does not
rewrite either entry artifact or convert it into post-implementation authority.

## Governing and read-only input pins

| Input | SHA-256 |
|---|---|
| `TECH-POLICY-D0.md` | `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` |
| `POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md` | `sha256:d8eae9829069631caaef769635b3748b5440d5bfab4aacaf682f736eb546d84e` |
| `POLICY-001-DOMAINSPEC-REVIEW.md` | `sha256:4d05db37d0c1351ac2859b92dde001bc5932575c3b0d9549776b842109cf27ca` |
| `POLICY-000-IMPLEMENTATION-REVIEW.md` | `sha256:76ed9cd9efd6794e7b1d4c40421635db16edc8a580e789f837b415d892b13c8c` |
| `implementations/server/runtime/execution_policy.py` | `sha256:405b990c49edb330227e14af4ecc65a6d39566a8a6a298433fd7aa40eaf0e357` |
| `implementations/tests/runtime/execution_policy_oracle_v1.json` | `sha256:f6155aa8a615b00ec88b26cab480647eaeab871c02727781f7fd93db367caeac` |
| `implementations/tests/runtime/test_execution_policy.py` | `sha256:2c01b5dfd6a752e1e1f397e715feadbad351997a3365b27c3591851db046d8f0` |
| `implementations/server/runtime/database.py` | `sha256:4f04c889d4b0f7b4cf6f6a58d93c445dd3201c801e78fd22a83777fac9fcae66` |
| `implementations/server/runtime/artifacts.py` | `sha256:e1a02b2580498c1b6eeb2741cb4303b45570396519228c0b138135ec7d8f1354` |
| `implementations/server/runtime/canonical.py` | `sha256:db4eb8b3e3f8508e7004fa2ce4ab83cc4e863266d680f4c73cd05394b8889bfb` |

The implementation consumed these dependencies read-only. No production parser, database helper,
artifact helper, canonicalization helper, migration, service, journal, API, CLI or package export
was changed by POLICY-001.

## Reviewed outputs

| Output | SHA-256 |
|---|---|
| `implementations/tests/runtime/policy_lineage_harness.py` | `sha256:8f8d74d4f02d89392e853e14d48acdc7317c9dd17b0fbd91e49c5f90683b812b` |
| `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json` | `sha256:9cc5ffd931a911b2c6fb5dcaaf5d5f0e336514663dbd8866209218e67084952b` |
| `implementations/tests/runtime/test_execution_policy_lineage.py` | `sha256:fd82c46ffbc6ac36656c646bdb1dffe3b7cc34f36920e1c27725d47688dd8e75` |

The exact implementation stays inside the descriptor's three-path write scope:

- `SyntheticPolicyLineageHarness` creates only two test tables in a caller-supplied temporary
  file-backed runtime database;
- seven `ArtifactStore.prepare()` calls happen before the transaction, followed by seven
  `ArtifactStore.finalize(conn, ...)` calls, one receipt and seven ordered bindings inside one
  `RuntimeDatabase.write()` transaction;
- `ArtifactStore.commit()` is never used for an individual member;
- key and immutable-lineage replay/conflict are resolved under the writer transaction;
- `after_commit` fires only after transaction exit and models a lost response;
- fresh handles reopen every artifact through the existing authorization boundary, reproduce exact
  bytes/digests/order and rerun the pure POLICY-000 and production-firewall checks.

## Independent review and repair closure

The initial independent implementation review found one MAJOR in persisted receipt integrity:
replay/reopen needed to prove that the stored receipt bytes, row-level transport key and reconstructed
unit were one exact value rather than trusting a partially matching row.

The repair is present in the final reviewed hash set:

- `_validate_stored_receipt` reconstructs the canonical receipt from the stored identity, key,
  ordered bindings and unit preimage, parses the persisted bytes strictly, and requires exact field,
  digest and value equality;
- replay routes through the same stored-receipt validation before returning the first receipt;
- `test_pol1_6a_receipt_byte_tamper_blocks_retry_and_reopen` rejects tampered receipt bytes;
- `test_pol1_6b_row_and_receipt_key_mismatch_blocks_retry_and_reopen` rejects row/receipt key drift.

The independent reviewer rechecked the repaired outputs and returned final **PASS / KEEP**. No
CRITICAL, MAJOR or MINOR finding survives this receipt.

## Coverage

| Lens | Verified result |
|---|---|
| Contract fidelity | Exact seven-member names/order/content identities, closed receipt fields, authority literal and canonical unit digest match the accepted L1 contract. |
| Mechanics and integrity | Prepare/finalize transaction, every failpoint, dual replay axes, lost-response recovery, receipt/member/artifact tamper rejection and fresh-handle reopen are exercised. |
| Ownership and layering | All writes remain in the three test paths and temporary database; production code and migrations are read-only dependencies. |
| Authority firewall | Combined oracle and harness fence remain rejected by production parsers before and after persistence. |
| Effects and operability | Exact production table inventory remains empty and fail-on-call boundaries remain uninvoked; temporary SQLite/artifact persistence is the only admitted I/O. |

## Verification bundle

The final reviewed bundle reports:

- focused POLICY-001: **10/10 PASS**;
- combined POLICY-000 + POLICY-001: **47/47 PASS**;
- Stage-C verifier + orchestration bridge: **26/26 PASS**;
- curated runtime regression: **248/248 PASS**;
- Python compileall: **PASS**;
- task-scope `git diff --check`: **PASS**.

These are the final verification results supplied to the independent reviewer; this evidence
consolidation did not rerun the long suite.

## Integration evidence state

| Integration artifact | SHA-256 |
|---|---|
| Stage-E source manifest | `sha256:56a4438b5c3f1e23ec1a2c98a405e791d52c418dbf02b204cba053d3c5527259` |
| Stage-C verifier `implementations/server/runtime/local_pilot.py` | `sha256:4d74ffd4f1ed8226e34cdb03699d139e57075f13312d38adf8b147c85cb60e9d` |
| Stage-E execution receipt | `sha256:ea9620e7b5fc7acae0b6fbbc2c621f17946f7d8d97c675f1c6a2259723c69db1` |

These hashes identify the integration baseline against which the final review ran. The individual
POLICY-001 output authority remains the explicit three-output hash table above; this receipt does
not infer an output pin that the source manifest does not explicitly contain.

## Claim boundary and promotion

POLICY-001 is now **implemented-reviewed-bounded / PASS-KEEP** for the L1 question only: exact
reviewed POLICY-000 bytes retain one non-executable integrity lineage across atomic local
persistence, replay/conflict, crash and reopen.

The implementation creates no `ConfirmedDispatch`, Run, Group, Attempt, invocation plan,
execution request, command receipt, event, aggregate head, effect intent, sandbox-launch effect,
publication, message, provider identity, opening or external action. The two test-only lineage
tables and seven finalized test artifacts confer no consent or executable authority.

POLICY-002 may use this receipt and the exact output hashes as a read-only entry prerequisite for
its separately reviewed three-path workpack. This review itself authorizes no L2 fake-denial code,
no POLICY-003 target-host work and no production or deployment action.
