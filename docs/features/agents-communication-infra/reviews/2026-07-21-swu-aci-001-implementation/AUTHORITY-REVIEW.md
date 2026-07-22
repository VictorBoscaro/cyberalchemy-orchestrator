---
feature: agents-communication-infra
review_date: 2026-07-21
scope: SWU-ACI-001
axis: domain-authority-and-transaction-semantics
verdict: FIX
review_set_sha256: 35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946
runtime_gate: block
---

# SWU-ACI-001 authority review

## Verdict

**FIX.** The baseline hashes and composed review-set digest reproduce exactly, the SQL fixture
applies to an empty SQLite database with `foreign_key_check` clean, and all four declared canonical
byte lengths and SHA-256 values reproduce. The writer, atomic command/outcome, idempotency, crash
and pure-replay decisions otherwise agree with ACI-R5, ACI-R6, ACI-R7 and ACI-R14. Acceptance is
blocked by the contract gaps below.

## Findings

### High — The SQL fixture accepts malformed values in authoritative digest columns

The ADR requires migration bytes to be sealed as lowercase `sha256:<64 hex>`
([ADR-001, lines 212-215](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#4-migration-busy-and-corruption-policy))
and defines the same lowercase-hex representation for canonical acceptance identity
([ADR-001, lines 258-274](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes)).
The fixture checks only length and the `sha256:` prefix for `migration_checksum`
([slice0-schema.sql, lines 15-20](../../adrs/fixtures/slice0-schema.sql)), and repeats that weaker
pattern for content, command, schema, payload, state, effect and receipt digests. An independent
execution successfully inserted `sha256:` followed by 64 uppercase `Z` characters into
`schema_migrations`.

This permits non-hex and noncanonical identifiers into the authority store, undermining migration
drift detection, idempotency comparisons and replay verification. Add one reusable-equivalent SQL
constraint pattern that requires exactly 64 lowercase hexadecimal characters after the prefix to
every authoritative digest/hash column, plus rejection tests for uppercase and non-hex values.

### Medium — The executable schema contract omits the required attempt-winner constraint

ADR-001 says the executable schema must include the constrained records and indexes from the
persistence contract, explicitly including attempt-winner uniqueness
([ADR-001, lines 163-167](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#2-logical-schema-and-constraints)).
The controlling persistence contract requires an `attempts` primary key, `(operation_id,
attempt_no)` index and partial `UNIQUE(operation_id) WHERE accepted_result = 1`
([persistence-and-replay.md, lines 160-173](../../persistence-and-replay.md#32-rebuildable-constrained-indexes-and-projections)).
The SQL fixture ends after publication/message constraints and contains no `attempts` table or
accepted-winner index ([slice0-schema.sql, lines 198-249](../../adrs/fixtures/slice0-schema.sql)).

That leaves one of the named synchronous acceptance invariants unfrozen while the fixture presents
itself as the TASK-010 executable SQL contract. Add the attempts constraint and a test proving zero
or one accepted result per operation while allowing multiple non-winning attempts, or explicitly
narrow the fixture and provide a separately reviewable fixture that freezes this required invariant.

### Medium — Golden evidence does not cover every canonicalization decision and does not freeze the core pin

ADR-001 requires golden coverage for a schema-version change
([ADR-001, lines 276-280](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes)),
but every positive vector uses `aci.contract@1` and neither the rejection vectors nor the test plan
exercise a version change
([canonical-contract-vectors.json, lines 23-108](../../adrs/fixtures/canonical-contract-vectors.json);
[test plan, lines 23-34](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md#dependency-and-canonical-contract)).
The ADR also freezes both `pydantic==2.13.4` and `pydantic-core==2.46.4` and requires exact dependency
evidence ([ADR-001, lines 246-252](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes)),
while the fixture and test plan state only the Pydantic range/lock and omit the exact core pin
([canonical-contract-vectors.json, lines 5-10](../../adrs/fixtures/canonical-contract-vectors.json);
[test plan, lines 16-21](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md#dependency-and-canonical-contract)).

Add a version-change vector proving that the explicit schema version affects canonical bytes/digest,
name its executable test, and make the fixture/test plan agree with the ADR's exact Pydantic and
pydantic-core dependency policy.

## Acceptance recommendation

Do not mark ADR-001 or SWU-ACI-001 accepted on this baseline. Correct the three contract gaps,
recompute an immutable baseline and repeat independent review. Keep `workPackGateStatus=block`; this
review does not authorize TASK-010 or any runtime, migration, adapter or provider implementation.

## Closure Review — 2026-07-21

### Verification

The four file hashes in `FINAL-BASELINE.md` reproduce exactly, as does composed review-set digest
`d6093473703ce1cf21353dff785ad69f7aa38f253980adfbcc0e21ded1ec014f`. The remediated SQL applies
to an empty SQLite database with a clean `foreign_key_check`. Independent probes confirmed that its
digest constraints reject uppercase and non-hex payloads, that a second accepted attempt for one
operation is rejected, and that an additional non-winning attempt is admitted. All six canonical
vectors reproduce their declared byte lengths and prefixed SHA-256 digests.

### Closure verdict

**FIX.** The schema-version and exact dependency-pin finding is closed. The physical halves of the
digest and attempt-winner findings are corrected, but their requested executable test contracts are
still absent. A separate high-severity gate deadlock also prevents accepting this ADR as written.

### High — ADR acceptance depends on the runtime task that the ADR is supposed to unblock

The ADR says it becomes `accepted` only when the independent receipt references **all** listed
evidence, then leaves transaction crash, idempotency/CAS, durability and replay execution pending
TASK-010 and the dependency lock/install receipt pending implementation
([ADR-001, lines 328-342](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#acceptance-evidence-required)).
The controlling gate forbids runtime work and releases TASK-010 only after B-001/B-002 are accepted
([WORK-PACK, lines 152-157](../../WORK-PACK.md#gate-checks)); TASK-000 in turn defines SWU-ACI-001 as
done only when this ADR is accepted. Consequently TASK-010 cannot produce the evidence required to
accept the ADR that must be accepted before TASK-010 starts.

Split W0 decision acceptance from later implementation conformance: ADR acceptance should require
the frozen contract fixtures, independently reproduced static evidence and review receipt. Keep
TASK-010 failpoint, startup, replay and resolved-lock results as TASK-010 exit/conformance evidence,
not as prerequisites to accepting the W0 decision. This must not promote the runtime gate by itself;
the remaining TASK-000/B-002/B-003 W0 obligations still apply.

### Medium — Two corrected invariants still have no named TASK-010 rejection tests

The SQL now enforces lowercase hexadecimal digest forms and the one-winner-per-operation partial
index, but the executable test plan names neither a malformed uppercase/non-hex digest rejection
test nor a test that admits multiple losing attempts while rejecting a second accepted winner
([test plan, lines 40-68](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md#sqlite-acceptance-cas-and-crash-matrix)).
This leaves the test-plan part of the first two original findings unresolved and conflicts with the
plan's statement that TASK-010 must attach results for every named obligation.

Add explicit names/assertions for both constraint families so production migration conformance is
tested rather than inferred from the W0 fixture.

### Residual acceptance recommendation

Do not mark ADR-001 or SWU-ACI-001 accepted on final baseline `d609347…`. Remove the W0/TASK-010
acceptance cycle, add the two missing named tests, produce a new immutable baseline and rerun closure
review. `workPackGateStatus` remains `block`; no runtime, migration, adapter or provider work is
authorized by this review.

## Final Closure Review — 2026-07-21

### Final verification

The current `FINAL-BASELINE.md` is internally valid. Each listed file hash reproduces and the
ordered composition reproduces SHA-256
`70c2312b9ecd75bfa814ba9548fa11c3508b75a662fec42db3d29b71429b310b`.

Independent execution against a temporary file-backed SQLite database confirmed that the contract
schema applies with `journal_mode=wal`, `synchronous=2` (`FULL`), `foreign_keys=1`,
`busy_timeout=5000`, `quick_check=ok` and no foreign-key violations. Adversarial probes continue to
reject uppercase/non-hex digests and a second accepted attempt while allowing additional losing
attempts. All six canonical vectors reproduce their declared UTF-8 byte lengths and prefixed
SHA-256 digests.

### Final verdict

**PASS.** No material residual authority, transaction, replay, idempotency, crash-semantics or gate
finding remains in this review scope.

The former gate deadlock is closed by explicitly separating W0 architectural-decision acceptance
from TASK-010 implementation conformance
([ADR-001, lines 328-363](../../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#decision-acceptance-and-downstream-implementation-evidence)).
Runtime failpoints, production dependency resolution, migration/startup behavior and replay results
remain downstream TASK-010 obligations; they are no longer circular prerequisites to accepting the
decision that eventually enables that task.

The two missing executable obligations are now named with falsifiable outcomes:

- malformed prefix, uppercase, non-hex and wrong-length values are parameterized across every
  digest/hash column
  ([test plan, line 64](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md#startup-migration-corruption-and-replay));
- multiple losing attempts are admitted while duplicate identity/number and a second accepted
  winner are rejected
  ([test plan, line 80](../../adrs/fixtures/SWU-ACI-001-TEST-PLAN.md#constrained-sql-records-and-immutability)).

### Acceptance recommendation

Accept ADR-001 for the **W0 decision scope** of SWU-ACI-001 on baseline `70c2312…`. This PASS is a
contract-review receipt only: it does not claim production SQLite, migration, recovery, runtime,
adapter or provider evidence and does not by itself complete TASK-000, close every W0 blocker or
authorize TASK-010. Preserve `workPackGateStatus=block` until the complete WORK-PACK gate checks are
satisfied independently.
