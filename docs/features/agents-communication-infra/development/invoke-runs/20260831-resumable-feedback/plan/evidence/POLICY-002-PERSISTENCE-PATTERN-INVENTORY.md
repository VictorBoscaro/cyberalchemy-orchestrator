# POLICY-002 persistence pattern inventory

Date: 2026-09-01

Status: bounded architecture evidence; no code-entry or execution authority

## Outcome

POLICY-002 has no unresolved persistence-design blocker. The smallest repository-consistent design
is a second, explicitly test-only harness over the same temporary file-backed `RuntimeDatabase` used
by POLICY-001. It first reopens and revalidates the exact POLICY-001 lineage, then inserts or replays
one canonical fake-denial receipt in exactly one additional local table.

This inventory fixes reversible implementation choices only. It does not authorize code entry,
select product policy, admit an action, create an effect, or prove provider/host enforcement.

## Observed repository pattern

The recommendation is grounded in these existing mechanics:

- `SyntheticPolicyLineageHarness` creates test tables locally after applying production migrations;
  neither table enters `MIGRATION_NAMES`.
- `RuntimeDatabase.write()` owns the serialized `BEGIN IMMEDIATE` transaction and commits on normal
  exit or rolls back on exception.
- POLICY-001 resolves both uniqueness axes inside that writer transaction; no unlocked pre-read
  establishes replay.
- `ArtifactStore.prepare()` is transaction-free and `ArtifactStore.finalize(conn, ...)` can join an
  existing transaction. POLICY-002 needs no new artifact, so it should call neither
  `ArtifactStore.finalize()` nor `ArtifactStore.commit()`.
- `canonical_bytes()`, `digest_bytes()` and `parse_strict_json()` provide the existing
  `aci-cjson-1`, SHA-256 and strict-reopen boundaries.
- POLICY-001 proves file-backed reopen, lost-response convergence, corruption rejection, production
  parser rejection, exact row inventories and fail-on-call external-boundary spies.

POLICY-002 is simpler than POLICY-001: its durable unit has no ordered child collection and no new
payload artifact. A receipt row containing exact canonical bytes and their digest is therefore the
complete atomic unit.

## Recommended names

| Concern | Candidate name |
|---|---|
| Test-only module | `implementations/tests/runtime/policy_denial_harness.py` |
| Harness | `ExecutionPolicyFakeDenialHarness` |
| Persist/replay method | `deny_synthetic_attempt(...)` |
| Fresh-handle reader | `reopen_fake_denial(...)` |
| Table constant | `DENIAL_TABLE` |
| Table | `test_execution_policy_fake_denial_receipts` |
| Validation error | `SyntheticDenialValidationError` |
| Identity/digest conflict | `SyntheticDenialConflict` |
| Preimage schema | `aci.execution-policy-fake-denial@1` |
| Receipt schema | `aci.execution-policy-fake-denial-receipt@1` |
| Fixture | `implementations/tests/runtime/execution_policy_fake_denial_oracle_v1.json` |
| Focused tests | `implementations/tests/runtime/test_execution_policy_denial.py` |

Use Python snake_case at the implementation boundary while preserving the DomainSpec method names
as the mapped interface vocabulary. Keep `AUTHORITY = "test-only-non-executable"`, the twelve
labels and the two ordered reason codes as closed module constants.

## One-table persistence shape

Recommended local DDL:

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

Column rationale:

- `lineage_identity` is the domain identity, the second uniqueness axis and a direct FK to the
  exact POLICY-001 source receipt.
- `denial_key` is the independent transport-idempotency axis.
- the four evidence digests reproduce the exact source and denial preimage without treating the
  receipt BLOB as self-authenticating;
- `receipt_digest` binds the exact canonical receipt bytes required by T-ACI-POL2-1 and POL2-6;
- `receipt_bytes` preserves the first byte-identical receipt, including its first `denial_key`.

SQLite already creates indexes for the primary key and `UNIQUE(denial_key)`. Add no secondary
index: the only admitted lookup is `WHERE denial_key=? OR lineage_identity=?`, and both terms are
already indexed uniqueness axes.

Do not store an action label, timestamp, decision column, reason-code columns, provider identity,
event id, request/effect identity or L3 evidence. The label is excluded by contract; clock access
must remain zero; decision and reasons are closed constants reconstructed and checked against the
canonical bytes. Duplicating them as mutable columns would add drift without adding evidence.

## Denial construction and transaction

1. Require non-empty string `denial_key`, non-empty string `lineage_identity` and one scalar string
   `action_attempt_label` in the exact twelve-label set. A list, tuple or other collection rejects;
   repeated calls with the same scalar label are replay, not a batch or “duplicate-label” input.
2. Before entering the denial transaction, instantiate fresh POLICY-001 database/artifact handles
   and call its reopen path for `lineage_identity`.
3. Reproduce all seven member bytes/digests, rerun the POLICY-000 parsers and production-authority
   rejections, require every budget ceiling and `max_child_processes` to equal zero, and require all
   filesystem/network/process/credential grants to be empty.
4. Build the exact denial preimage from only the schema, authority, lineage identity/unit digest,
   resource-budget digest, sandbox-policy digest, `decision=denied` and the ordered two reason
   codes. Exclude `denial_key` and the action label. Canonicalize it and derive `denial_digest`.
5. Build the exact receipt by adding the first caller's `denial_key`, receipt schema and
   `denial_digest`; derive canonical `receipt_bytes` and `receipt_digest` before transaction entry.
6. Enter one `RuntimeDatabase.write()` transaction and fire `policy_denial.after_begin`.
7. Query by `denial_key OR lineage_identity` inside that transaction. Two different matched rows are
   a permanent `SyntheticDenialConflict`. One row must first pass stored-row/receipt integrity
   validation; then the same `denial_digest` returns its first receipt and a changed digest is a
   no-write conflict.
8. With no match, insert the one row, fire `policy_denial.after_receipt`, then
   `policy_denial.before_commit`.
9. Fire `policy_denial.after_commit` only after `RuntimeDatabase.write()` exits. It models a lost
   response; a fresh retry must return the first persisted receipt.

No POLICY-001 row is updated. The action label only selects test coverage and never dispatches to a
callable.

## Replay, conflict and corruption classification

| Condition | Required result |
|---|---|
| Same key and same denial digest | Return first canonical receipt bytes. |
| Same lineage identity, unused key and same denial digest | Return first receipt, including the first stored key. |
| Same key bound to another lineage/digest | Permanent `SyntheticDenialConflict`; zero mutation. |
| Key and lineage match two different rows | Permanent `SyntheticDenialConflict`; zero mutation. |
| Invalid/missing/tampered POLICY-001 source | Typed validation/integrity rejection before denial transaction. |
| Stored denial row or receipt bytes are internally inconsistent | `IntegrityError`; never rewrite or self-heal. |
| Unknown, missing or non-scalar label | `SyntheticDenialValidationError`; zero denial rows. |

The stored-row validator must strict-parse `receipt_bytes`, require exact canonical bytes and closed
receipt fields, recompute the denial preimage and all digests, compare every receipt value with the
row, and verify the row's lineage binding against a fresh POLICY-001 reopen. Persisted bytes are
evidence only after this reconstruction; they do not infer authority.

## Failpoints and atomicity

The complete admitted set is:

```text
policy_denial.after_begin
policy_denial.after_receipt
policy_denial.before_commit
policy_denial.after_commit
```

For the first three, close and reopen the database and assert zero denial rows. For
`after_commit`, assert exactly one row and require a fresh-handle retry to return the first receipt.
There is no artifact/member failpoint because POLICY-002 creates neither.

## Required test inventory

| Contract | Minimum executable proof |
|---|---|
| T-ACI-POL2-1 | Fixture independently pins exact denial-preimage bytes/digest, receipt bytes/digest, closed fields and ordered reasons; expected bytes are not generated only by the harness under test. |
| T-ACI-POL2-2 | Missing lineage/receipt/member/artifact; member order/body/digest/unit drift; six independent positive budget ceilings; five grant classes plus positive child-process limit; noncanonical bytes and production/harness digest-domain substitution all reject before transaction with zero denial rows. |
| T-ACI-POL2-3 | Exactly twelve scalar labels yield the same receipt; wrong type, empty and unknown labels reject; decision and reason spelling/count/order mutations reject. Repeated invocation is tested as replay, not as a batch input. |
| T-ACI-POL2-4 | All four failpoints prove rollback or lost-response convergence and `PRAGMA foreign_key_check` remains empty. |
| T-ACI-POL2-5 | Both uniqueness axes converge on the same digest; cross-bound key/identity and changed unit/policy/decision/reason evidence conflict without a second row. |
| T-ACI-POL2-6 | Fresh `RuntimeDatabase`, POLICY-001 harness and POLICY-002 harness handles reproduce receipt bytes/digest, denial digest and exact lineage/unit/policy bindings. |
| T-ACI-POL2-7 | Run all twelve labels independently while fail-on-call spies cover workload filesystem, network, subprocess/process, credential, tool, provider, audit, journal, runtime service, clock and environment. Only the supplied SQLite path may perform I/O. |
| T-ACI-POL2-8 | POLICY-001 remains exactly seven artifacts, one receipt and seven members; POLICY-002 adds one table/row only; the enumerated production tables and all L3 evidence stay empty; production confirmation/plan/request/effect seams reject the synthetic inputs before mutation. |

Add explicit corruption cases for noncanonical/extra/missing receipt fields, receipt-vs-row key or
lineage mismatch, each stored digest changed independently, receipt BLOB changed with and without
its stored digest, missing source FK target with FK checks deliberately bypassed, and a partial or
wrong source binding. Retry and reopen must both fail closed.

## Layer and dependency limits

Allowed implementation dependencies:

- `policy_lineage_harness.py` for exact source reopen and validation;
- pure execution-policy parsers;
- `canonical.py`, `database.py` and the closed runtime error vocabulary;
- `ArtifactStore` only transitively through POLICY-001 reopen;
- the caller-supplied temporary file-backed SQLite path.

Forbidden implementation dependencies and changes:

- no production migration or `MIGRATION_NAMES` entry;
- no `RuntimeService`, `RuntimeJournal`, API, CLI or production package export;
- no confirmation, Run, Group, plan, request, Attempt, event, effect, audit or provider writer;
- no process, network, workload-path, credential, tool, environment or clock access;
- no new artifact or mutation of the seven POLICY-001 artifacts, receipt or members;
- no `AgentExecutionRequest`, `EffectIntent`, production fence, cutover epoch, watcher-disable
  evidence, host path observation or POLICY-003 claim.

The likely later write scope is the new test-only harness, one exact oracle fixture and one focused
test module. Traceability, descriptor and readiness paths must be named separately by the eventual
work pack; this inventory does not authorize them.

## Alternatives rejected

- **Extend the POLICY-001 receipt table:** rejected because a denial is a distinct L2 result and
  would mutate an already-reviewed L1 unit.
- **Add a POLICY-002 member/artifact table:** rejected because the denial has no ordered collection
  or new artifact; it violates the exact one-table/one-row boundary.
- **Persist the denial as an ArtifactStore artifact:** rejected because it adds an unnecessary row
  and finalization step; exact canonical bytes already fit atomically in the one denial row.
- **Use `ArtifactStore.commit()`:** rejected because it creates a separate transaction and cannot
  strengthen a single-row unit.
- **Use RuntimeJournal or a runtime migration:** rejected because an event/aggregate would imply a
  production runtime surface expressly excluded by POLICY-002.
- **In-memory SQLite:** rejected because it cannot prove close/reopen durability.
- **Filesystem receipt plus SQLite index:** rejected because it introduces two persistence
  resources without an atomic cross-resource commit.
- **Persist labels or accept a batch of labels:** rejected because labels are routing selectors
  outside preimage, receipt, identity and authority; the contract exposes one scalar label.
- **Caller-supplied policies, reasons or decision:** rejected because POLICY-002 consumes only the
  exact reopened POLICY-001 unit and closed denial constants.

## Evidence pins

| Evidence | SHA-256 |
|---|---|
| `implementations/tests/runtime/policy_lineage_harness.py` | `sha256:8f8d74d4f02d89392e853e14d48acdc7317c9dd17b0fbd91e49c5f90683b812b` |
| `implementations/tests/runtime/test_execution_policy_lineage.py` | `sha256:fd82c46ffbc6ac36656c646bdb1dffe3b7cc34f36920e1c27725d47688dd8e75` |
| `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json` | `sha256:9cc5ffd931a911b2c6fb5dcaaf5d5f0e336514663dbd8866209218e67084952b` |
| `implementations/server/runtime/database.py` | `sha256:4f04c889d4b0f7b4cf6f6a58d93c445dd3201c801e78fd22a83777fac9fcae66` |
| `implementations/server/runtime/artifacts.py` | `sha256:e1a02b2580498c1b6eeb2741cb4303b45570396519228c0b138135ec7d8f1354` |
| `implementations/server/runtime/canonical.py` | `sha256:db4eb8b3e3f8508e7004fa2ce4ab83cc4e863266d680f4c73cd05394b8889bfb` |
| Execution-policy capability | `sha256:8b8fa86efbd49ed74dd49da9cd05e33ed183e5194d4c3c27f2d0a08d8f7f241a` |
| Domain contract | `sha256:978e5c018e8aaa97d277cbd403594c0dca511aa395cb603a0496cb567ba91f9c` |
| Interface contract | `sha256:c5e055ef443a3f3a1391b49e20b1f74b0bc7e5c523ca54295bf496037e70f028` |
| Rule contract | `sha256:233fa87c826aeeaae87d5f439a7a324f401f874304a778f3003ed57e327e7485` |
| Test contract | `sha256:07f9da9ff3a7f51f1b03ceed52c7a59b0857f45da9917a2e228db4d78c61aa0e` |

## Deferred gates

Before code entry, POLICY-002 still requires its own exact descriptor, fresh readiness receipt,
fixture review, bounded implementation and independent red-team review. Product policy values,
non-empty grants, a production fence, host enforcement and provider admission remain POLICY-003 or
later decisions and are not gaps in this persistence seam.

