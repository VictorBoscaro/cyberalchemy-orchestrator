# Review — Stage-A evidence-recovery successor dispatch

**Reviewed artifact:** `evidence-recovery-dispatch.json`  
**Reviewed SHA-256:** `B94D943078D9ACFD82AF8CFED13F8660D36FAC39DE2C4C3989BFC0EB61C51670`  
**Verdict:** **BLOCK**

## Coverage

The successor was reviewed against the immutable predecessor contract and hashes, the approved
P3 amendment review, the terminal correction-set BLOCK, and the immutable attempt-1 BLOCK. The
review covered forward-only authority, defect and receipt cardinality, namespaces and identities,
exact receipt fields and scope, independent review, finite-gate behavior, downstream role
separation, Stage-B promotion, and mutation order. The dispatch-spec validator was rerun and
returned `VALIDATION=pass`. The recovery namespace was absent at review time, so no execution or
code mutation preceded this review.

The following checks pass:

- all four declared predecessor hashes match the current bytes;
- the old BLOCK receipts remain immutable inputs and are not relabeled or waived;
- the recovery scope is limited to P3-RS-01 through P3-RS-04 and exactly four new receipts;
- assigned recovery identities and paths are fresh and unique;
- the four receipt contracts name the missing exact fields and preserve the read-only source
  bounds;
- receipt authors and the receipt-set reviewer are independent;
- `RECOVERY_PRE_INTEGRITY_01` is a new, single-attempt, fail-closed gate in a fresh namespace, not
  predecessor `PRE_INTEGRITY_RETRY`;
- Stage B still requires both successor approval PASS and independent terminal-close PASS.

## Blocking findings

### 1. The required continuation assignment map has no producer, path, or executable handoff

**Severity:** MAJOR

The artifact requires:

> “Before s4 starts, the root records a reviewed assignment map giving every predecessor
> continuation role a fresh unique successor agent_id and unique receipt path under
> recovery_namespace.”

It also requires:

> “the recovery receipt-set reviewer must verify the concrete continuation assignment map before
> s3.”

No step produces that map, no identity/path assignment names its artifact, and the receipt-set
review step does not receive it as an input. The chronology is therefore not executable as written:
the map must already exist and be reviewed before `s3`, but its only timing rule says merely
“before s4.” Allowing the root to invent or supply it out of band would contradict the declared
subagent-only work/validation model and make the reviewed dispatch hash insufficient to determine
the downstream identities and write paths.

**Required fix:** add a bounded pre-`s2` subagent-owned assignment-map step, an exact append-only
path and schema, and a distinct review result consumed by `s3`; alternatively freeze all downstream
role, agent, attempt, and receipt-path assignments directly in the successor dispatch and have the
successor-contract reviewer verify them at this hash.

### 2. The downstream graph collapses thirteen independent roles into one aggregate executor

**Severity:** MAJOR

Steps `s4` and `s5` both declare only:

> `"roles": ["successor_stage_a_continuation"]`

while `continuation_identity_contract.required_roles` requires thirteen separately identified
P4/T1/T2/review/approval/closeout roles and states that no person may occupy two roles. The
aggregate role also owns gate `g3`. Consequently, the dispatch DAG neither assigns the required
fresh identities to the downstream steps nor represents the predecessor's independence and
self-exclusion boundaries. The prose promise that the aggregate role executes through distinct
subagents is not an enforceable role/path contract.

**Required fix:** replace the aggregate continuation role with explicit downstream steps or groups
for every required role, each bound to the reviewed assignment map and exact receipt path. Encode
the predecessor P4→T1→T2→T3→review→approval→closeout→terminal-verifier dependencies and preserve
the different fresh agents required for the two integrity phases. Give `g3` to an independent
continuation verifier, not the aggregate executor.

## Change requests

1. **MAJOR** — Materialize and independently review the continuation assignment map before the
   recovery pre-integrity gate.
2. **MAJOR** — Replace the aggregate continuation executor with explicit fresh downstream roles,
   paths, dependencies, and an independent policy-gate owner.

The successor is a legitimate forward-recovery design in its evidence-repair portion, but it is
not yet a complete executable successor for Stage A. This BLOCK authorizes no recovery seat, code
mutation, predecessor retry, downstream continuation, or Stage-B handoff. Repair under a new hash
and obtain another independent review before execution.

## Repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `E3EEC8A39BA4314C6F293C7E41B03E64484EB95E52D91933378F64D602BA4A1C`  
**Verdict:** **BLOCK**

### Verified repairs

Both earlier findings are closed:

- `s1a_continuation_assignment_map` now gives the map a subagent producer, exact artifact and
  receipt paths, a schema, a digest contract, and frozen sources. The distinct
  `s2a_continuation_assignment_map_review` consumes and independently reviews it before `s3`.
- The aggregate `successor_stage_a_continuation` role is gone. Thirteen concrete downstream seats
  now have thirteen unique roles, agent IDs, attempt IDs, and receipt paths. The steps explicitly
  encode P4, T1, T2, T3, three-lens fanout, bounded writer/skeptic convergence, coverage, approval,
  closeout, and terminal verification. P4 and T2 use different identities, and independent C2 owns
  the downstream policy gate.
- The downstream repair policy permits zero repair rounds. Any non-PASS approval terminates this
  successor; another attempt requires a new independently reviewed successor.
- The recovery portion remains limited to the same four defects and four recovery receipts.
  `RECOVERY_PRE_INTEGRITY_01` still has attempt limit one, predecessor hashes still match, the old
  BLOCKs remain immutable, and Stage B still requires approval PASS plus independent C2 PASS.
- The dispatch-spec validator again returned `VALIDATION=pass`. The recovery namespace was absent
  during this review, so no recovery seat, code mutation, or downstream write preceded it.

### Remaining defect 1 — The `s3` denominator has contradictory definitions — MAJOR

The repaired route necessarily creates two new lifecycle receipts before `s3`: the assignment-map
author receipt and the independent assignment-map review receipt. The `s3` step correctly asks for:

> `"ref": "complete predecessor-plus-successor denominator"`

But gate `g2_one_finite_recovery_pre_integrity` narrows that same gate to:

> “the complete preserved predecessor graph plus successor review and four recovery receipts”

That list omits both attempted assignment-map seats and their receipts. A finalizer cannot satisfy
both definitions without either omitting attempted successor lifecycle evidence or silently
expanding the gate denominator. The reviewed map decision is an input to `s3`, but the map author
and reviewer lifecycle evidence is not explicitly part of the manifest condition.

**Required repair:** define one exact `s3` denominator that includes the immutable predecessor
graph, successor-dispatch review, assignment-map artifact and author receipt, assignment-map review
receipt, exactly four recovery receipts, and the independent recovery receipt-set review. Use that
same named denominator in the step, gate, manifest contract, and terminal C2 verification.

### Remaining defect 2 — Downstream outputs violate the declared read-only predecessor namespace — MAJOR

`boundary_evidence.state_namespaces` declares the entire predecessor namespace:

> `.arcanum/observability/runs/2026-08-13-runtime-type-expansion/stage-a/cycle-2`

with:

> `"write_policy": "read-only immutable historical evidence for this recovery"`

The immutable-predecessor boundary applies to every downstream step. Nevertheless, the fixed T3
and C1 assignments require creation of:

> `.arcanum/observability/runs/2026-08-13-runtime-type-expansion/stage-a/cycle-2/lifecycle-manifest.pre-approval.json`

and:

> `.arcanum/observability/runs/2026-08-13-runtime-type-expansion/stage-a/cycle-2/lifecycle-manifest.closeout.json`

Neither file existed at review time. Creating them is a write inside a namespace the successor
declares wholly read-only, so a compliant operator must either violate the write policy or fail T3
and C1.

**Required repair:** place successor T3/C1 lifecycle artifacts under the append-only recovery
namespace and carry explicit links to the immutable predecessor graph, or narrow the predecessor
read-only boundary to the exact historical artifacts that must remain immutable and explicitly
authorize these two previously absent paths. Keep all existing predecessor receipts and BLOCKs
read-only.

No execution is authorized at this hash. Freeze the two boundary repairs under a new hash and
obtain another independent review before `s1a` or any recovery seat launches.

## Terminal repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `5CA5680B5BE3F4546CDA71573655F2E8E405CD1E98F6BCCF960E345A5789F309`  
**Verdict:** **PASS**

Both remaining defects are closed.

The recovery gate now has one canonical ordered denominator. Ordinals 1–21 are the immutable
predecessor receipts, and every declared SHA-256 matches the current bytes. Ordinals 22–24 are the
successor-dispatch review, assignment-map author receipt, and independent assignment-map review;
ordinals 25–28 are exactly the four bounded recovery receipts; ordinal 29 is the independent
receipt-set review. The receipt-set reviewer consumes exactly ordinals 1–28 and explicitly excludes
its own ordinal-29 output. The distinct pre-integrity finalizer consumes and recomputes exactly
ordinals 1–29 while excluding its own later manifest and receipt. The step, projection, and `g1`/`g2`
conditions now use the same cardinalities and self-exclusion boundary.

The successor-created T3 pre-approval manifest, C1 closeout manifest, and recovery-completion
artifact now live under the append-only `evidence-recovery-01` namespace. No downstream
observability output or receipt writes into the predecessor `cycle-2` tree, which remains wholly
read-only. T3 and C1 retain the predecessor's behavior and self-exclusion semantics while using the
successor's explicit paths; C2 verifies those exact relocated artifacts and treats any predecessor-
namespace write as BLOCK.

Regression checks pass. The dispatch-spec validator returns `VALIDATION=pass`; all predecessor
anchors and all 21 denominator hashes match; the recovery namespace was absent during review; the
four-defect recovery still emits exactly four receipts; `RECOVERY_PRE_INTEGRITY_01` remains a single
attempt; the thirteen downstream roles, agent IDs, attempt IDs, and receipt paths remain unique;
the aggregate continuation role remains absent; P4 and T2 remain independently owned; downstream
repair rounds remain zero; and Stage B remains blocked until both approval PASS and independent C2
PASS.

This PASS approves only the successor dispatch contract at the reviewed hash. It does not claim
that a map, recovery receipt, gate, code change, test, review, approval, closeout, or Stage-B handoff
has executed or passed. Execution may begin only with the independently reviewed `s0` boundary and
must remain fail-closed under the contract.
