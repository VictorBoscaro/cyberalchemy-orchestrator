# TASK-POLICY-002 - durable test-only execution-policy fake denial

## Status

- **State:** `PLANNED_READINESS_PENDING`
- **SWU:** `SWU-ACI-EXECUTION-POLICY-DENIAL-002`
- **Planning gate:** `PASS`
- **Code-entry gate:** `BLOCK` until a separate exact code-readiness receipt is authored and passes.
- **Claim boundary:** one test-only L2 harness may reopen the reviewed POLICY-001 lineage and persist
  one package-level fake-denial receipt in one additional temporary SQLite table. It grants no
  execution authority and performs no attempted external action.

## Decision question

After this L2 unit, we know whether the exact reopened, non-executable POLICY-001 package can route
each of twelve closed scalar test labels to the same durable package-level denial without attempting
the named action, mutating L1 evidence, creating production authority or claiming POLICY-003 host
enforcement.

## Frozen entry evidence

- `TECH-POLICY-D0.md` at
  `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e`.
- `POLICY-001-IMPLEMENTATION-REVIEW.md` at
  `sha256:cbb9c03460ae755f39d194b58d0db2f8ca531bc8572f27ec4bf2949deeef885b`,
  final `PASS / KEEP` for the exact L1 harness/oracle/test outputs pinned by the descriptor.
- `POLICY-002-DOMAINSPEC-REVIEW.md` at
  `sha256:1a758c0d0223f6a26b2408a32c2f7ba087a456a26b80c6e0fd38b7f053497ff9`,
  accepted for bounded workpack planning only.
- `POLICY-002-PERSISTENCE-PATTERN-INVENTORY.md` at
  `sha256:2319202dc75eb09306523e54623a2c20f60b4be35fd1e62c4538743116d3d869`.
- `POLICY-002-ALIGNMENT-LAYERING-AUDIT.md` at
  `sha256:34ece0e88c7a67a4065285d476d8143a617a111a579daa0ba6713d5bf811e8a3`,
  verdict `PASS for workpack authoring; not code entry`.
- Current POLICY-002 normative contracts:
  - `specs/domain.md` at
    `sha256:978e5c018e8aaa97d277cbd403594c0dca511aa395cb603a0496cb567ba91f9c`;
  - `specs/SPEC.md` at
    `sha256:319130e802af1d85aec2373517b3f9d72f79f6a68a221154c6691c47e2620c60`;
  - `specs/capabilities/execution-policy-authority.md` at
    `sha256:8b8fa86efbd49ed74dd49da9cd05e33ed183e5194d4c3c27f2d0a08d8f7f241a`;
  - `specs/TEST-SPEC.md` at
    `sha256:bfd080bc0ec4860d7c5b9f3f028b8bbd0560786e9e61a83ce51168b0d21b985d`;
  - `specs/rules.md` at
    `sha256:eeac22fe4dc0edc3a31a2f9cbf94aea7d976cda1e61e1ce793fe66e0fc758225`;
  - `specs/interfaces.md` at
    `sha256:c5e055ef443a3f3a1391b49e20b1f74b0bc7e5c523ca54295bf496037e70f028`;
  - `specs/architecture.md` at
    `sha256:6991ebb1b470733b8044a9f081ba5284ce87f127671e12db0b9a2e205c381832`.
- Exact reviewed POLICY-001 implementation inputs:
  - `implementations/tests/runtime/policy_lineage_harness.py` at
    `sha256:8f8d74d4f02d89392e853e14d48acdc7317c9dd17b0fbd91e49c5f90683b812b`;
  - `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json` at
    `sha256:9cc5ffd931a911b2c6fb5dcaaf5d5f0e336514663dbd8866209218e67084952b`;
  - `implementations/tests/runtime/test_execution_policy_lineage.py` at
    `sha256:fd82c46ffbc6ac36656c646bdb1dffe3b7cc34f36920e1c27725d47688dd8e75`.

Embedded historical pins inside planning evidence do not replace the descriptor's current normative
pins. Any current-pin drift stops the task before code mutation.

## Exact write scope

Implementation may create or edit only:

1. `implementations/tests/runtime/policy_denial_harness.py`;
2. `implementations/tests/runtime/execution_policy_denial_oracle_v1.json`;
3. `implementations/tests/runtime/test_execution_policy_denial.py`.

All production code, migrations, POLICY-000 and POLICY-001 outputs, specs, work-pack artifacts,
ledgers and readiness artifacts are read-only during implementation.

## Closed implementation contract

- Use the normative implementation symbol `ExecutionPolicyFakeDenialHarness`, with public
  `deny_synthetic_attempt(...)` and `reopen_fake_denial(...)` methods. Consume L1 only through
  `SyntheticPolicyLineageHarness.reopen_synthetic_lineage(...)`; do not import L1 private SQL,
  tables or validators.
- Accept a non-empty `denial_key`, exact persisted `lineage_identity`, one scalar string
  `action_attempt_label` and an optional named failpoint. Lists, tuples, sets, mappings, empty or
  unknown labels reject. A fixture label collection must contain exactly twelve unique literals;
  duplicate collection input rejects. Repeating an identical scalar invocation is replay.
- Admit exactly the twelve labels frozen by T-ACI-POL2-3:

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

  A label is a test selector only and never enters the denial preimage, receipt, row, digest, replay
  identity or authority.
- Reopen and revalidate the complete POLICY-001 source before entering the denial transaction.
  Require all six resource ceilings and `max_child_processes` to be zero and every filesystem,
  network, process and credential grant list to be empty.
- Freeze the exact denial digest
  `sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399`
  and first receipt content digest
  `sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11`.
- Create exactly one test-only table, `test_execution_policy_fake_denial_receipts`, in the caller's
  temporary file-backed database. It has direct L1 lineage identity/key/digest/receipt bindings,
  no label, timestamp, event, effect, provider, artifact or L3 column, and no migration entry.
- Resolve `denial_key` and `lineage_identity` inside one `RuntimeDatabase.write()` transaction.
  Same digest through either axis returns the first byte-identical receipt; cross-bound axes or
  changed evidence conflict permanently without a second row.
- Support only `policy_denial.after_begin`, `policy_denial.after_receipt`,
  `policy_denial.before_commit` and post-transaction `policy_denial.after_commit`. The first three
  reopen to zero rows; the last models a lost response and fresh retry returns the first receipt.
- Strictly reconstruct stored receipt bytes and every row/digest/source binding on replay and reopen.
  Corruption fails closed and is never rewritten or self-healed.

## T-ACI-POL2-1 through T-ACI-POL2-8

| Obligation | Required proof |
|---|---|
| `T-ACI-POL2-1` | Independently compare the exact closed receipt, canonical preimage, ordered reasons, denial digest and receipt digest with the checked-in oracle. |
| `T-ACI-POL2-2` | Missing/partial/reordered/tampered L1 evidence, noncanonical bytes, each positive budget ceiling, each non-empty grant class, positive child-process limit and authority-domain substitution reject before the denial transaction with zero rows. |
| `T-ACI-POL2-3` | Exactly twelve unique scalar labels accept and collapse to one receipt; wrong type, collection, duplicate fixture labels, missing/empty/unknown labels and decision/reason drift reject. Repeated scalar invocation is replay. |
| `T-ACI-POL2-4` | Three pre-commit failpoints roll back completely; `after_commit` leaves one row and converges after fresh retry; `PRAGMA foreign_key_check` stays empty. |
| `T-ACI-POL2-5` | Both uniqueness axes replay unchanged evidence; cross-bound axes and controlled internal evidence drift conflict without mutation. Public caller-controlled decision, reasons or digest are forbidden. |
| `T-ACI-POL2-6` | Fresh database, L1 harness and L2 harness handles reproduce source binding, receipt bytes and both digests; in-memory SQLite is invalid. |
| `T-ACI-POL2-7` | Exercise all labels independently while workload filesystem, network, process/subprocess, credentials, tools, provider, runtime service, journal, audit, clock and environment spies remain zero. Supplied temporary SQLite I/O is the sole exception. |
| `T-ACI-POL2-8` | L1 remains seven artifacts, one receipt and seven members; L2 adds one table/row only; production authority/runtime/event/effect/publication/message tables and L3 evidence remain empty, and existing production seams reject synthetic inputs before mutation. |

Corruption coverage must include noncanonical, extra and missing receipt fields; row/receipt key or
lineage mismatch; every stored digest changed independently; receipt bytes changed with and without
the stored receipt digest; a missing source FK target with checks deliberately bypassed; and partial
or wrong source binding. Retry and reopen must both reject.

## Capability and forbidden scope

The implementation capability is repository write access to the three exact paths plus validation-
only temporary file-backed SQLite. Network, credentials, production access, destructive actions,
external tools and process/provider launch are denied.

Forbidden changes include migrations or `MIGRATION_NAMES`; runtime service, journal, API, CLI or
package exports; production confirmation, Run, Group, plan, request, Attempt, command, event, effect,
audit, publication or message writes; new artifacts or L1 mutation; caller-supplied policy/decision/
reasons/digest/external callables; product values, production fence, cutover evidence, host paths,
provider identity and every POLICY-003 claim.

## Validation contract

```powershell
python -B -m unittest implementations.tests.runtime.test_execution_policy_denial -v
python -B -m unittest implementations.tests.runtime.test_execution_policy implementations.tests.runtime.test_execution_policy_lineage implementations.tests.runtime.test_execution_policy_denial -v
$aciRuntimeModules = Get-ChildItem -LiteralPath implementations/tests/runtime -Filter 'test_*.py' | Where-Object { $_.Name -ne 'test_agent_continuation_lean_bridge.py' } | ForEach-Object { 'implementations.tests.runtime.' + $_.BaseName }; python -B -m unittest $aciRuntimeModules
python -B -m compileall implementations/tests/runtime/policy_denial_harness.py implementations/tests/runtime/test_execution_policy_denial.py
git diff --check -- implementations/tests/runtime/policy_denial_harness.py implementations/tests/runtime/execution_policy_denial_oracle_v1.json implementations/tests/runtime/test_execution_policy_denial.py
```

The curated runtime command excludes the Lean bridge entirely. Passing these future commands is
implementation evidence, not evidence created by this planning task.

## Entry predicates and stop conditions

Code entry remains blocked until a separately authored readiness receipt returns `PASS` while:

- every descriptor pin matches current bytes;
- all three output paths are absent at gate time;
- the capability profile denies network, credentials, production and destructive actions;
- write scope, tests, validation commands and forbidden scope exactly match this task; and
- no independent review blocker remains.

Stop before mutation on pin drift, pre-existing output, additional write need, missing L1 reopen
contract, need for a collection/batch API, production dependency, external callable, migration,
second table/artifact, real action, POLICY-003 evidence or any validation path that would execute or
depend on the Lean bridge.
