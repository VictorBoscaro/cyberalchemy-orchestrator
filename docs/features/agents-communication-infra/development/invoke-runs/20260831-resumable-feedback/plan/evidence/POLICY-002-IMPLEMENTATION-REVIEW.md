# POLICY-002 implementation review

Date: 2026-09-01

Unit: `SWU-ACI-EXECUTION-POLICY-DENIAL-002`

Verdict: **PASS / KEEP**

This receipt freezes the final independently reviewed POLICY-002/L2 implementation. The claim is
limited to one test-only fake denial over one exact reopened POLICY-001 lineage, persisted in one
additional table and one row in caller-supplied temporary file-backed SQLite. It proves the closed
denial projection, replay/conflict, fail-closed integrity and zero attempted runtime or external
action. It does not establish production execution authority, host enforcement, provider launch,
product policy, POLICY-003/L3 evidence, deployment or any real attempted action.

## Entry-authority snapshots

These are immutable snapshots of the bounded code-entry gate. Their pre-implementation status
language records the state that authorized mutation; it is not rewritten as post-implementation
authority.

| Entry artifact | SHA-256 | Role |
|---|---|---|
| [`TASK-POLICY-002.md`](../../../../../work-pack/tasks/TASK-POLICY-002.md) | `sha256:9e7d32981c028df50bb89c2f113e85cfb9121bbcbed38a8af10443627b1d7f80` | Exact L2 objective, proof obligations, write scope and validation surface. |
| [`SWU-ACI-EXECUTION-POLICY-DENIAL-002.json`](../../../../../work-pack/descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json) | `sha256:b6853f2026f4a3881fc08b253dd7c5a2f2ef81e4f018f151b0875df68725a73e` | Exact SWU scope, symbols, pins and authority/effect ceiling. |
| [`TASK-POLICY-002-CONTEXT.md`](../../../../../work-pack/context/TASK-POLICY-002-CONTEXT.md) | `sha256:90079f5cd0e4097ea96841ce45cd9719822f44172cf499635cbeeaaccdf4f930` | Bounded implementation context and dependency map. |
| [`TASK-POLICY-002-SCAFFOLD.md`](../../../../../work-pack/context/TASK-POLICY-002-SCAFFOLD.md) | `sha256:2ba68d1db86358371a423f8cac837995cd4585e7c64de0298ab010dd0b52607c` | Three-path implementation scaffold and test allocation. |
| [`SWU-ACI-EXECUTION-POLICY-DENIAL-002-code-readiness.json`](../../../../../work-pack/execution/SWU-ACI-EXECUTION-POLICY-DENIAL-002-code-readiness.json) | `sha256:c87adb7655364fac6332d76310494e35901c147e3b8c7def151edaa3b4d20afb` | Historical PASS capability and exact write-scope gate. |

## Review and dependency pins

| Evidence | SHA-256 | Result used here |
|---|---|---|
| [`TECH-POLICY-D0.md`](../TECH-POLICY-D0.md) | `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` | L2/L3 boundary and zero-action design. |
| [`POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md`](POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md) | `sha256:2319202dc75eb09306523e54623a2c20f60b4be35fd1e62c4538743116d3d869` | File-backed SQLite and transaction pattern inventory. |
| [`POLICY-002-ALIGNMENT-LAYERING-AUDIT.md`](POLICY-002-ALIGNMENT-LAYERING-AUDIT.md) | `sha256:34ece0e88c7a67a4065285d476d8143a617a111a579daa0ba6713d5bf811e8a3` | PASS for the bounded three-path workpack layering. |
| [`POLICY-002-DOMAINSPEC-REVIEW.md`](POLICY-002-DOMAINSPEC-REVIEW.md) | `sha256:1a758c0d0223f6a26b2408a32c2f7ba087a456a26b80c6e0fd38b7f053497ff9` | Integrated DomainSpec review and exact denial vectors. |
| [`POLICY-001-IMPLEMENTATION-REVIEW.md`](POLICY-001-IMPLEMENTATION-REVIEW.md) | `sha256:cbb9c03460ae755f39d194b58d0db2f8ca531bc8572f27ec4bf2949deeef885b` | Independently reviewed L1 public reopen prerequisite. |
| [`TEST-SPEC.md`](../../../../../specs/TEST-SPEC.md) | `sha256:bfd080bc0ec4860d7c5b9f3f028b8bbd0560786e9e61a83ce51168b0d21b985d` | T-ACI-POL2-1 through T-ACI-POL2-8 authority. |

## Reviewed outputs

| Output | SHA-256 | Verdict |
|---|---|---|
| [`policy_denial_harness.py`](../../../../../../../../implementations/tests/runtime/policy_denial_harness.py) | `sha256:ed13e5f9c246f88767a5461230aa66eb870986cf11c565acd7a7ca4a87aa03b6` | KEEP |
| [`execution_policy_denial_oracle_v1.json`](../../../../../../../../implementations/tests/runtime/execution_policy_denial_oracle_v1.json) | `sha256:391f620df96289261ffa57e9eaec356dcb8b0397c94f6b75c1cff1507c5faefb` | KEEP |
| [`test_execution_policy_denial.py`](../../../../../../../../implementations/tests/runtime/test_execution_policy_denial.py) | `sha256:b82bd6a246e3c9a0bdc2b0b6813c338c1da2e2996040f37307a2a19a615c316e` | KEEP |

The final output set remains exactly inside the descriptor's three-path write scope. The harness
creates no production migration and adds only
`test_execution_policy_fake_denial_receipts` to the supplied temporary database. Its one successful
canonical denial creates one row; the twelve action-attempt labels are non-durable selectors and do
not enter receipt bytes, digests, identity or authority.

## Initial findings and repair closure

The initial independent review did not accept the first implementation. It raised the following
load-bearing blockers; all were repaired before the final output hashes above were frozen.

| Initial blocker | Final closure evidence |
|---|---|
| Caller-supplied callable failpoint exceeded the closed public input contract. | `deny_synthetic_attempt` now accepts only `str | None`; `_require_failpoint` admits exactly four nominal labels and `_trip` implements their deterministic behavior. |
| The exported label corpus could be mutated into a new accepted authority set. | Validation and per-call admission compare against a separately reconstructed closed twelve-label tuple; duplicate, expanded, collection, empty and unknown inputs reject. |
| Stored-corruption precedence and the required corruption matrix were incomplete. | Replay prevalidates stored rows and their source bindings before conflict classification. The final tests cover noncanonical, extra and missing receipt fields; key/lineage mismatch; every stored digest; independent and coupled byte/digest drift; wrong/partial source binding; missing FK source; and require retry plus reopen to fail without rewrite. |
| T-ACI-POL2-7 and T-ACI-POL2-8 did not yet prove the complete effect and cardinality ceilings. | The final tests exercise all twelve labels under fail-on-call workload/runtime boundaries, preserve exact L1 bytes and counts, require one L2 table/row, keep production tables empty and reject the receipt at production seams. |
| Two source-integrity TOCTOU windows remained between L1 reopen, L2 lookup and the writer transaction. | The final harness holds a guard connection, compares `PRAGMA data_version` around source reads, prevalidates matching rows, and requires the writer view to equal the preflight view before insert/replay. Both race windows have focused fail-closed tests with zero L2 rows. |

Independent re-review of the repaired bytes returned final **PASS / KEEP**. No CRITICAL, MAJOR or
MINOR change request survives this receipt.

## Coverage

| Reviewer function | Lens | Verified result | Zero-findings defence |
|---|---|---|---|
| Independent implementation review | Contract fidelity and authority | Exact oracle, ordered reasons, twelve selectors, four failpoints and forbidden public inputs match the accepted task/descriptor. | The first pass raised callable-failpoint and mutable-corpus blockers; the final pass rechecked the repairs. |
| Independent mechanics review | Transaction, replay and corruption correctness | Both identity axes, pre/post-commit behavior, lost-response recovery, fresh reopen, full corruption corpus and two TOCTOU windows are exercised. | The first pass raised corruption and TOCTOU blockers; the final pass reproduced the repaired focused suite. |
| Independent boundary review | Effects, layering and operability | L1 bytes/cardinalities remain stable; one L2 table/row is added; production/runtime/external/L3 state remains absent. | The first pass required fuller T7/T8 proof; the final pass rechecked the added spies, seams and cardinalities. |

Lens coverage included all three final outputs. The oracle was checked for exact canonical preimage,
receipt and both frozen digests; the harness for authority, transaction and integrity mechanics; and
the tests for every T-ACI-POL2-1..8 obligation and negative boundary.

## Verification bundle

The final reviewed bundle reports:

- focused POLICY-002: **12/12 PASS**;
- combined POLICY-000 + POLICY-001 + POLICY-002: **59/59 PASS**;
- curated runtime regression: **260/260 PASS** across 27 modules, explicitly excluding the Lean
  bridge module;
- Python `compileall`: **PASS**;
- task-scope `git diff --check`: **PASS**.

These results were supplied with the final independent review. This evidence-only consolidation
did not rerun the long runtime suite and makes no claim about the excluded external Lean bridge.

## Change requests

None survive verification. Each reviewed output has verdict **KEEP**.

## Claim boundary and promotion

POLICY-002 is **implemented-reviewed-bounded / PASS-KEEP** only for the L2 question: the exact
reviewed deny-all POLICY-001 package produces one deterministic, durable, non-executable fake-denial
receipt with fail-closed replay and reopen.

The implementation creates no `ConfirmedDispatch`, Run, Group, Attempt, invocation plan, execution
request, command receipt, event, aggregate head, effect intent, sandbox-launch effect, audit,
publication, message, provider identity, clock/environment evidence, workload file, network/process/
credential/tool call or other external action. The L2 row confers neither consent nor executable
authority. POLICY-003/L3, target-host enforcement, real provider admission, production fencing,
product policy, commit, push and deploy remain outside this review.

Review close: `exit_reason=resolved`; this consolidation spawned no subagents. Independent reviewer
execution counts are not asserted here because they were not part of the supplied final evidence
bundle.
