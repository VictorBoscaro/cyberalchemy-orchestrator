# P3 evidence-repair amendment review

**Reviewed artifact:** `bootstrap-contract.json`  
**Reviewed SHA-256:** `28FCA0E3766A252F213B1F14EBE28256D34172927F73E118D5BDFB5BCC0A0215`  
**Verdict:** **AMEND**

## Verified

- All nine original seat receipts still match the frozen SHA-256 values in
  `cycle_2_p3_evidence_repair.observed_receipt_set`; the PRE_INTEGRITY attempt-1 BLOCK receipt still
  matches `9536BD8637B0D3736688CC56D33BBE7E9C6ABCB6BB260A3669CC497684B2EC63`.
  The amendment forbids editing, replacing, omitting, relabeling, or converting any of them.
- Corrections are forward-only: each uses a new path, identity, and attempt, links the preserved old
  receipt by path and digest, binds the approved parent
  `2D9C9C3B3ACD66D0A0C11DF69F2BC9265B45A3384BB7C317D7F76F78CB342051` separately from
  the amended contract hash, and records responsibility only from the new timestamp.
- The host predecessor repair is exact. The old host receipt records stale digest
  `8CFDC80CC0346999A235ADB2C18797258D339B041B4E9C4D3D9751B2F131D628`; the preserved
  legacy receipt actually hashes to
  `3FEE82BF192F764D663B57A7231170D03DB35DB323BE2F0A94A49902695DB02B`. The new host
  receipt must use the actual digest of the new legacy-owner receipt after it exists.
- Fixture, preliminary-test, baseline, binding-test, compiler, and service corrections require the
  missing generic fields, correct parent/contract links, current artifact hashes, validation reruns,
  and honest preservation of preliminary BLOCK state. No old result is laundered into PASS.
- The two adoption audits are durable, fresh, mutually independent, read-only re-audits. Their
  owners are distinct and may reaffirm only after their respective auditor PASS; neither audit may
  be synthesized from the old ephemeral summaries.
- No clause authorizes backdating. Recorded, responsibility, spawn, join, close, audit, and
  predecessor evidence must reflect the later corrective attempts.
- Finalizer attempts are finite and non-self-referential: immutable PRE_INTEGRITY attempt 1 BLOCK;
  one fresh PRE_INTEGRITY_RETRY attempt 2; then one PRE_REVIEW_FREEZE attempt 3 after terminal pins.
  Attempt 2 writes its manifest only on PASS, and its separate receipt is not an input to that
  manifest. A BLOCK at attempt 2 or 3 ends Stage A; no fourth attempt exists.
- P4 is explicitly BLOCKED until amendment review, both audits, all correction receipts,
  correction-set review, and PRE_INTEGRITY_RETRY attempt 2 plus its manifest all PASS. The older
  execution graph and repair order remain explicitly superseded for cycle 2.

## Required amendment

### P3-01 — The P4 unlock contradicts the active integrity-owner receipt requirement — MAJOR

The P3 repair intentionally preserves the preliminary test state as BLOCK. Both
`cycle_2_p3_evidence_repair.authorized_corrections.test_reaffirmation` and
`receipts.p3_correction_receipt_contract.fixture_test_required_fields` require the new preliminary
test reaffirmation to remain BLOCK because integrity pins are stale. `cycle_2_execution.p3_retry_gate`
then permits P4 after the corrected receipt graph and PRE_INTEGRITY_RETRY attempt 2 PASS.

However, the still-active
`receipts.amendment_receipt_requirements.a_integrity_owner` requires
`all_test_receipts_PASS_before_pin_regeneration`. That condition can never be true while the
immutable preliminary BLOCK and its honest BLOCK reaffirmation remain in the denominator. P4
therefore cannot both obey its receipt contract and perform the repin needed to make the later
terminal tests pass.

Amend only that requirement so P4 accepts the independently reviewed preliminary receipt set when
all functional commands not blocked by expected stale pins pass, the remaining BLOCKs are exactly
and exclusively attributable to those stale pins, and PRE_INTEGRITY_RETRY attempt 2 is PASS. Keep
terminal PASS requirements unchanged for T1/T2 and final approval. Freeze the repaired contract
under a new hash and independently re-review this finding before launching any P3 correction or
P4 work.

This verdict approves no correction receipt, lifecycle retry, P4 launch, implementation, test,
integrity result, Stage-A PASS, or Stage-B entry.

## Repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `AA7B402E8A445199570A7E99EAF1B05F31978A0906DF15257090ACC1B1764855`  
**Verdict:** **PASS**

P3-01 is closed. The impossible `all_test_receipts_PASS_before_pin_regeneration` requirement is
gone. P4 may now consume an honestly retained preliminary BLOCK only when command-level evidence
proves that every ungated functional assertion passed and every remaining failure stopped at a
named frozen integrity-pin preflight. That proof must include the pin artifact and path, expected
and actual SHA-256 values, command, and failure boundary; mixed causes, unexplained failures,
post-preflight failures, changed artifacts, or any additional blocker fail closed before mutation.

Authority remains bounded. The test and affected fixture owners record the evidence,
PRE_INTEGRITY_RETRY attempt 2 checks it independently, and the integrity owner recomputes every
hash before changing only the proven stale pins and their mechanically consequent parent pin. The
preliminary BLOCK is neither edited nor converted to PASS.

The terminal boundary is unchanged and stronger than preliminary eligibility: T1 must rerun the
complete mandatory command set from the beginning and persist every command as PASS; T2 must pin
that exact report and rerun final integrity to PASS before target freeze or review. Preliminary
eligibility is explicitly not terminal-test or Stage-A PASS evidence.

The P3 correction graph, immutable attempt-1 BLOCK, single attempt-2 retry, later attempt-3 freeze,
P4 gate, fresh identities, forward-only links, auditor independence, no-backdating rules,
self-receipt exclusion, and supersession of older execution descriptions remain intact. This PASS
approves only the repaired P3 evidence-repair contract at the reviewed hash; it is not evidence
that corrections, P4, tests, integrity, Stage A, or Stage B executed or passed.
