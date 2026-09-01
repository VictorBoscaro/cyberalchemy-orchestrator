# Implementation scaffold — SWU-ACI-EXECUTION-POLICY-DENIAL-002

## Gate and source authority

- Task: [`TASK-POLICY-002`](../tasks/TASK-POLICY-002.md) at
  `sha256:9e7d32981c028df50bb89c2f113e85cfb9121bbcbed38a8af10443627b1d7f80`.
- Descriptor: [`SWU-ACI-EXECUTION-POLICY-DENIAL-002`](../descriptors/SWU-ACI-EXECUTION-POLICY-DENIAL-002.json)
  at `sha256:b6853f2026f4a3881fc08b253dd7c5a2f2ef81e4f018f151b0875df68725a73e`.
- Code entry: **BLOCK** until a separate readiness receipt revalidates every pin, confirms all three
  outputs are absent and returns `PASS`.

This scaffold is symbol-first implementation guidance, not mutation authority.

## Function-first targets

| Path | Owned symbols/data | Required shape |
|---|---|---|
| `implementations/tests/runtime/policy_denial_harness.py` | `ExecutionPolicyFakeDenialHarness`, `deny_synthetic_attempt(...)`, `reopen_fake_denial(...)`, `DENIAL_TABLE`, closed schemas/reasons/labels/failpoints and local typed errors | Reopen L1 only through its public method; validate the closed zero/deny-all fixture; project exact canonical denial; resolve both uniqueness axes in one `RuntimeDatabase.write()` transaction; reconstruct stored evidence strictly on replay/reopen. |
| `implementations/tests/runtime/execution_policy_denial_oracle_v1.json` | Independent input/expected vector | Freeze exact L1 identity/digests, 12 labels, ordered reasons, four failpoints, denial preimage bytes/digest and first receipt bytes/content digest. Expected values must not be derived only from the harness under test. |
| `implementations/tests/runtime/test_execution_policy_denial.py` | T-ACI-POL2-1 through T-ACI-POL2-8 | Own exact fixture, negative, atomicity, replay/conflict, corruption, reopen, zero-call and production/L3-firewall coverage. Enforce the harness AST/import allowlist and absence of `DENIAL_TABLE` from `MIGRATION_NAMES`. |

No fourth implementation path is authorized.

## Closed constants and vectors

```text
PREIMAGE_SCHEMA = aci.execution-policy-fake-denial@1
RECEIPT_SCHEMA  = aci.execution-policy-fake-denial-receipt@1
AUTHORITY       = test-only-non-executable
DECISION        = denied
DENIAL_TABLE    = test_execution_policy_fake_denial_receipts

REASONS =
  resource.max_wall_time_ms.zero
  sandbox.process.no-executable-grant

FAILPOINTS =
  policy_denial.after_begin
  policy_denial.after_receipt
  policy_denial.before_commit
  policy_denial.after_commit
```

Exact fixture vectors:

- `lineage_identity=policy-lineage-oracle-001`
- `lineage_unit_digest=sha256:f702b9d2954307a91039cd3ea92285cb464c2c997c2166c0d68c446513a2801d`
- `resource_budget_digest=sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836`
- `sandbox_policy_digest=sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a`
- `denial_key=policy-denial-command-001`
- `denial_digest=sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399`
- `receipt_content_digest=sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11`

The fixture contains exactly these scalar selectors:

```text
filesystem.read
filesystem.write
network.connect
process.child.start
credential.resolve
tool.call
resource.wall_time.consume_positive
resource.input_tokens.consume_positive
resource.output_tokens.consume_positive
resource.tool_calls.consume_positive
resource.payload_bytes.consume_positive
resource.artifact_bytes.consume_positive
```

Reject empty/unknown labels and every list, tuple, set or mapping. Reject duplicate labels when
validating the fixture collection. Repeating one identical scalar invocation is replay, not batch
input. The label must never enter the preimage, receipt, row, digest or identity.

## Layer and dependency boundaries

```text
POLICY-000 pure parser/oracle       read-only
              |
POLICY-001 public reopen result     read-only, exact seven-member unit
              |
POLICY-002 closed projection        pure before transaction
              |
RuntimeDatabase.write()             one BEGIN IMMEDIATE writer
              |
one test-only denial row            no artifact/event/effect/action
```

- Call only `SyntheticPolicyLineageHarness.reopen_synthetic_lineage(lineage_identity)` across the
  L1 boundary. Never import L1 private SQL, tables or validators.
- Reparse returned exact members through public POLICY-000 functions where the L2 all-zero and
  deny-all predicate needs proof.
- Use `canonical_bytes()`, `digest_bytes()`, strict JSON parsing and the existing database/error
  vocabulary read-only.
- Do not call `ArtifactStore.finalize()` or `ArtifactStore.commit()`; POLICY-002 creates no artifact.
- Production confirmation, invocation-plan, service and journal modules are negative-test/spy
  targets only. They are not implementation dependencies.

## One-table persistence shape

The harness creates this table locally after production migrations, never through `MIGRATION_NAMES`:

```sql
CREATE TABLE IF NOT EXISTS test_execution_policy_fake_denial_receipts(
  lineage_identity TEXT PRIMARY KEY
    REFERENCES test_execution_policy_lineage_receipts(lineage_identity),
  denial_key TEXT NOT NULL UNIQUE,
  lineage_unit_digest TEXT NOT NULL,
  resource_budget_digest TEXT NOT NULL,
  sandbox_policy_digest TEXT NOT NULL,
  denial_digest TEXT NOT NULL,
  receipt_digest TEXT NOT NULL,
  receipt_bytes BLOB NOT NULL
);
```

Do not add a label, timestamp, decision, reason, provider, request, event, effect, artifact or L3
column. Add no secondary index, table, migration or repository export.

## Required operation sequence

1. Validate non-empty string `denial_key`, exact non-empty `lineage_identity`, one scalar label and
   optional admitted failpoint.
2. With fresh L1 handles, reopen and revalidate all seven source members before beginning the L2
   writer transaction.
3. Require all six resource ceilings and `max_child_processes` to be zero and every filesystem,
   network, process and credential grant list to be empty.
4. Project the exact denial preimage without `denial_key` or label; canonicalize and hash it.
5. Add only first `denial_key`, receipt schema and `denial_digest`; canonicalize and hash the receipt.
6. Enter one `RuntimeDatabase.write()` transaction; fire `policy_denial.after_begin`.
7. Resolve `denial_key OR lineage_identity` inside that transaction. Validate any stored row and
   receipt by full reconstruction before replay/conflict judgment.
8. With no match, insert one row; fire `policy_denial.after_receipt`, then
   `policy_denial.before_commit`.
9. Fire `policy_denial.after_commit` only after transaction exit. A fresh retry returns the first
   receipt unchanged.

## Replay, conflict and integrity

| Condition | Result |
|---|---|
| Same key and same `denial_digest` | Return first canonical receipt. |
| Same lineage, unused key and same digest | Return first receipt including its first key. |
| Key and lineage resolve to different rows | Permanent conflict; zero mutation. |
| Either axis with changed source/projection | Permanent conflict; zero mutation. |
| Invalid/tampered L1 | Reject before L2 transaction. |
| Inconsistent L2 row or receipt | Integrity failure; never rewrite or self-heal. |

Corruption coverage must include noncanonical, extra and missing receipt fields; row/receipt key or
lineage mismatch; each stored digest changed independently; receipt-byte drift with and without
receipt-digest drift; missing source FK with checks deliberately bypassed; and partial or wrong
source binding. Retry and reopen must both fail closed.

## Test map

| Selector | Focus |
|---|---|
| `T-ACI-POL2-1` | Independent exact preimage/receipt bytes, ordered reasons and both digest goldens. |
| `T-ACI-POL2-2` | Complete L1/policy/authority negative matrix before transaction, always zero rows. |
| `T-ACI-POL2-3` | Exactly 12 scalar selectors collapse to one receipt; invalid types/values and drift reject. |
| `T-ACI-POL2-4` | Three rollback failpoints, post-commit lost response, fresh retry and empty FK check. |
| `T-ACI-POL2-5` | Key/lineage replay, cross-bound conflict and controlled internal drift without mutation. |
| `T-ACI-POL2-6` | Fresh file-backed database and harness handles reproduce exact durable evidence. |
| `T-ACI-POL2-7` | Every selector independently denies with all external/workload spies at zero. |
| `T-ACI-POL2-8` | L1 unchanged, exactly one L2 row, production tables and L3 evidence empty. |

## Authority and effect firewall

The only admitted I/O is SQLite access to the caller-supplied temporary test path. Fail-on-call
spies cover workload filesystem, network, subprocess/process, credentials, tools, provider,
runtime service, journal, audit, clock and environment. Keep production confirmation, Run, Group,
plan, request, Attempt, command, event, aggregate, effect, sandbox, publication and message tables
empty. Existing production policy/fence/confirmation/plan seams must reject synthetic values before
mutation.

POLICY-003 product grants, production fence, target-host path/link proof, provider admission,
launcher behavior, cutover and deployment remain deferred. A durable denial is neither consent nor
an attempted effect.

## Validation commands

Run only after readiness `PASS`:

```powershell
python -B -m unittest implementations.tests.runtime.test_execution_policy_denial -v
python -B -m unittest implementations.tests.runtime.test_execution_policy implementations.tests.runtime.test_execution_policy_lineage implementations.tests.runtime.test_execution_policy_denial -v
$aciRuntimeModules = Get-ChildItem -LiteralPath implementations/tests/runtime -Filter 'test_*.py' | Where-Object { $_.Name -ne 'test_agent_continuation_lean_bridge.py' } | ForEach-Object { 'implementations.tests.runtime.' + $_.BaseName }; python -B -m unittest $aciRuntimeModules
python -B -m compileall implementations/tests/runtime/policy_denial_harness.py implementations/tests/runtime/test_execution_policy_denial.py
git diff --check -- implementations/tests/runtime/policy_denial_harness.py implementations/tests/runtime/execution_policy_denial_oracle_v1.json implementations/tests/runtime/test_execution_policy_denial.py
```

The excluded Lean bridge is outside this workpack and supplies no evidence.

## Stop conditions and done boundary

Stop before or during mutation on pin drift, pre-existing output, failed/missing readiness,
additional write need, private L1 dependency, collection API, external callable, migration, second
table/artifact, real action, production dependency, POLICY-003 evidence or Lean-dependent
validation.

Done requires the exact three outputs, T-ACI-POL2-1 through T-ACI-POL2-8 passing, all pins and
read-only paths unchanged, zero external/production/L3 evidence, clean three-path diff and an
independent implementation review. It does not authorize commit, push, deploy or promotion beyond
bounded POLICY-002/L2 test-only evidence.
