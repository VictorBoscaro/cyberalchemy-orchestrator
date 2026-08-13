# Cycle-2 amendment review — Stage-A bootstrap contract

**Reviewed artifact:** `bootstrap-contract.json`  
**Reviewed SHA-256:** `A6229BC948CFCA80521643438A1C731E882BF59FF981D201488F0A2471D78DC1`  
**Verdict:** **AMEND**

## Coverage

| lens | result | evidence |
|---|---|---|
| Authorized scope and owner identity | PASS | The contract limits cycle 2 to A-001/A-002/A-004/A-005, retains the original runtime/compiler/service owners for their exact production files, gives the literal A-004 reproduction to a disjoint supplemental-test owner, and keeps test, receipt, integrity, review, and approval ownership separate. Superseded and interrupted roles have no current write authority. |
| Receipt truth and temporal authority | PASS | Reaffirmation begins responsibility at its actual timestamp, discloses that no past durable receipt exists, links rather than overwrites attempts, and forbids invented, inferred, or backdated lifecycle. Interrupted work remains non-PASS residue. No clause authorizes reconstruction of a past launch or authorship claim. |
| A-004 producer-output binding | PASS | Compiler and service scopes require equality to one immutable terminal producer-output receipt across dispatch, producer binding and agent identity, artifact ID, canonical repository-relative path, schema, SHA-256, byte count, route digest, and receipt digest. The positive and negative cases include missing receipt, nonterminal producer, caller-created/arbitrary path, every wrong binding field, symlink, cross-output substitution, and post-registration mutation. |
| A-005 historical grandfathering | PASS | A current 0.6.4 close requires the exact opening route digest. Digest omission is limited to one uniquely resolved opening whose own immutable row satisfies the explicit historical pre-route-schema predicate; orphan, absent, duplicate, malformed, fake-historical, swapped, and validate-only cases fail closed. This does not grant a general validate-only or caller-asserted legacy exception. |
| Supplemental test inclusion | PASS | `test_host_workflow_binding.py` is justified by the verified Stage-A review as the literal A-004 laundering reproduction. Its owner may change only canonical opening setup and A-004 assertions, and the required command set runs it in both preliminary and terminal passes. |
| Dirty-work preservation | PASS | Every repair begins from a frozen current hash and complete diff, preserves original-baseline/user and named-producer attribution, blocks on intervening or ambiguous overlap, and forbids reset, reconstruction, normalization, or receipt/integrity rewrites of production/test hunks. |
| Test, report, integrity, lifecycle, review, and approval ordering | **AMEND** | The cycle-2 order correctly states preliminary tests → preliminary lifecycle/integrity → post-integrity terminal tests → final repin/integrity → full review → approval → final lifecycle → completion. Other still-active graph/order clauses contradict that sequence, and terminal closure is circular. |
| Full cycle-2 review and Stage-B isolation | **AMEND** | Three whole-corpus lenses, writer–skeptic convergence, coverage, and a dedicated approver are preserved, and Stage B is explicitly blocked on cycle-2 completion. However, the review denominator contains two artifacts that can exist only after review and approval, so that review cannot freeze the corpus it claims to attack. |

## Surviving findings

### C2-01 — Approval, final lifecycle, completion, and the review corpus form an impossible cycle — CRITICAL

**Contract evidence:**

- `review_contract.frozen_target_corpus` includes both `lifecycle-manifest.final.json` and `cycle-2-completion.json`.
- The authoritative order says: “After the approver writes approval.json and its own terminal receipt, a_receipt_lifecycle_finalizer performs a new final-mode attempt ...; a_cycle_2_terminal_verifier then ... writes cycle-2-completion.json.”
- The finalizer must validate “every cycle-2 attempted seat” and the Stage-B gate requires the final lifecycle manifest to validate “every attempted seat terminal including approver.”
- Terminal approval itself requires `all_attempted_agents_terminal`, while the approver, finalizer, and terminal verifier cannot have terminal receipts before producing the artifacts assigned to them.

The full review must precede approval, but its frozen corpus requires artifacts produced only after approval. The finalizer is also required to enumerate its own final attempt in the manifest it writes; its terminal receipt cannot truthfully exist until after that write. The terminal verifier has the same self-closure problem for completion. Satisfying the current contract therefore requires a backdated close, an invented receipt, omission of an attempted seat, or review of a future artifact. Each violates A-002 and the contract's own no-invention rule.

**Required amendment:** establish one finite, non-self-referential closure boundary. At minimum:

1. remove `lifecycle-manifest.final.json` and `cycle-2-completion.json` from the pre-approval frozen review corpus;
2. make the substantive full review consume only artifacts that already exist, including the preliminary lifecycle manifest, terminal test report, and final integrity manifest;
3. make approval attest only that frozen substantive corpus and the attempted seats terminal before approval—not the approver's own future close or later mechanical closure roles;
4. define how the post-approval finalizer and terminal verifier are joined and checked without requiring either artifact to contain its own future terminal receipt (for example, an external Stage-B entry check over their host-joined receipts), and state the finite attempted-seat denominator at each phase;
5. keep Stage B blocked until that independent post-approval check verifies approval, final lifecycle evidence, completion, exact hashes, and zero surviving CRITICAL/MAJOR findings.

No cycle-2 execution or Stage-B handoff may rely on this hash until the cycle is removed and the repaired contract is independently reviewed.

### C2-02 — Three active scheduling descriptions disagree on terminal test and integrity order — MAJOR

**Contract evidence:**

- `cycle_2_execution.authoritative_order` requires a preliminary complete command pass, receipt finalization, preliminary integrity, a later post-integrity terminal command pass, and then a final report repin plus integrity rerun.
- `repair_contract.order` instead says the test owner “runs the full fixed test contract,” then “a_integrity_owner runs only after all repaired production and test bytes are final,” then freezes one final manifest and starts review.
- The top-level `execution_graph` likewise contains only `a_test_implementer → a_integrity_owner → attackers`; it contains neither the preliminary lifecycle/integrity pass nor the integrity → terminal-test → final-integrity loop required to close A-001.

Calling one prose list “authoritative” does not mark the other top-level graph and repair order historical or superseded. An operator can follow the latter two exactly and produce only a pre-integrity test report, recreating A-001 while appearing contract-compliant.

**Required amendment:** retain exactly one executable cycle-2 graph, or explicitly mark every earlier graph/order as historical and non-operative. The operative graph must encode, not merely narrate:

`production/adoption joins → supplemental and exclusive tests/preliminary report → preliminary receipt finalization → preliminary integrity → complete post-integrity terminal command set → terminal report → final report repin and integrity rerun → frozen full review → substantive approval → finite post-approval lifecycle/completion check`.

The complete command set must include `test_host_workflow_binding` in both applicable passes, and any terminal-report byte change must force another repin and integrity rerun.

## Preserved conclusions

The amendment does not need broader production scope. Exact A-004 output provenance, narrow A-005 historical handling, supplemental-test ownership, future-only receipt authority, dirty-work preservation, three-lens review, and the Stage-B block are contractually adequate. The two findings concern only executable ordering and closure semantics; they do not justify weakening strict `code`, canonical `other`, route-digest validation, historical compatibility, evidence requirements, or role separation.

Freeze a repaired contract hash and independently re-review C2-01/C2-02 before launching or resuming any cycle-2 seat. This AMEND verdict approves no implementation, receipt, test result, integrity result, Stage-A PASS, or Stage-B entry.

## Repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `896878711BCFC9DFA062963DBC88EA0F167CBCC3C160EEEBC0201CF94A6DCF58`  
**Verdict:** **BLOCK**

### C2-02 repair — PASS

There is now exactly one operative cycle-2 order. `cycle_2_execution.authority` declares itself
`SOLE_AUTHORITATIVE_CYCLE_2_ORDER`; `execution_graph_status` and
`repair_contract.order_status` explicitly make both older descriptions historical and
non-executable. The operative dependencies encode preliminary repair/test receipts, preliminary
integrity, the complete post-integrity terminal command pass, terminal-report repin and integrity,
full review, pre-approval freeze, approval, closeout, and terminal verification. The complete
command set still includes `test_host_workflow_binding`, and report changes still force repin and
integrity rerun.

### C2-01 repair — BLOCK

The approval/closeout split is directionally correct: approval, its receipt, closeout, completion,
and the terminal-verifier receipt are now outside the approved corpus, and the terminal verifier is
not required to approve its own receipt. However, the new pre-approval boundary still contains two
future/self-produced review targets:

- `review_contract.frozen_target_corpus` includes
  `lifecycle-manifest.pre-approval.json` and `review.md`;
- the same contract says three “full-corpus” attackers run at T3, while T3 itself creates and
  finalizes `review.md`;
- T4 occurs only after coverage and then creates `lifecycle-manifest.pre-approval.json`.

The attackers therefore cannot review the whole declared target corpus: one target is their own
later synthesis/coverage artifact and the other does not exist until the following phase. Freezing
those artifacts for the approver is valid; declaring them targets of the earlier full-corpus review
is not. It preserves the exact future-evidence defect C2-01 required the amendment to remove.

The pre-approval lifecycle finalizer also runs a second attempt at T4 but is neither cleanly outside
that boundary nor capable of placing its own terminal receipt in the manifest it is still writing.
`required_pre_approval_seats` includes `a_receipt_lifecycle_finalizer`, while
`external_boundary_seats` lists only the approver, closeout owner, and terminal verifier. The
contract excludes receipts later than coverage from the frozen corpus, yet approval requires every
attempted pre-approval seat to be terminal. It does not state whether or how the T4 finalizer
attempt's necessarily later receipt is verified without retroactive inclusion. This is the same
self-terminality ambiguity at a moved boundary.

**Required final repair:** distinguish the **review target corpus** from the broader
**pre-approval corpus**. Attackers review only already-existing implementation, test, receipt,
terminal-report, and final-integrity artifacts. After review and coverage finish, T4 may freeze a
broader approval corpus that additionally contains final `review.md` and the pre-approval lifecycle
manifest, but those two artifacts must not be represented as attacker-reviewed targets. Define the
T4 finalizer attempt as an explicit external boundary receipt, or assign its terminal join to a
later mechanical checker, so its authored manifest never needs its own future receipt and approval
does not claim unavailable terminality. State the exact receipt denominator separately for review,
approval, closeout, and Stage-B entry.

### Regression verification

No regression was found in the already accepted terms. Exact A-004 producer-output equality, narrow
A-005 historical omission, future-only/non-backdated receipts, supplemental A-004 test ownership
and command inclusion, dirty-hunk preservation, independent three-lens review roles, and the dual
PASS Stage-B block remain intact.

No cycle-2 seat may launch or resume from this hash. Freeze and independently re-review the final
C2-01 boundary repair; C2-02 does not need redesign.

## Terminal C2-01 repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `3C5929ABE9C8A1A503F052075CAE7BAE6237C4F24DB03153A5DF97F889B66DC3`  
**Verdict:** **BLOCK**

### Verified repair

The former future-target cycle is repaired. T3 now freezes only artifacts that already exist;
attackers consume that fixed target corpus; `review.md`, Coverage, and review-role receipts are
clearly downstream deliverables; and the approver separately hashes the unchanged targets plus
those deliverables and the external target-freeze author receipt as an ordered evidence package.
Approval and post-approval artifacts never become attacker targets retroactively.

The PRE_REVIEW_FREEZE attempt is also finite in its primary definition: it is the second and final
pre-approval finalizer attempt, atomically emits the manifest and a separate immutable author
receipt, and excludes that receipt from the manifest's own content/hash. The required receipt
denominators distinguish frozen-target seats, review-deliverable seats, and external boundary seats.

### Remaining C2-01 defect — receipt chronology still contains one impossible rule — MAJOR

`cycle_2_execution.receipt_before_integrity_rule` still says:

> “Later terminal-test/review receipts are new linked attempts and enter only
> lifecycle-manifest.pre-approval.”

But the sole authoritative order now creates `lifecycle-manifest.pre-approval.json` at T3 **before**
any attacker, writer, skeptic, or coverage seat runs at T4. The frozen-target denominator correctly
excludes those later receipts, and the approval package correctly includes them separately. The
quoted rule directly contradicts both mechanisms and can be satisfied only by backdating review
receipts or rewriting the already frozen manifest. Either path violates A-002 and the no-overwrite
rule.

The post-approval boundary has a related omission. `external_boundary_seats` includes
`a_post_approval_closeout_owner`, but the closeout contract refers generically to “post-approval
attempt receipts” without saying that the closeout artifacts exclude their own author's future
receipt, and `terminal_close_verifier` requirements do not explicitly verify that closeout-owner
receipt is terminal. The contract must not leave the same self-receipt question implicit at C1.

**Required terminal repair:**

1. replace the stale receipt rule with the actual finite chronology: terminal test/integrity
   receipts enter the PRE_REVIEW_FREEZE manifest; the finalizer's atomic author receipt and all
   attacker/writer/skeptic/coverage receipts remain external to that manifest and enter only the
   ordered approval evidence package;
2. state that closeout artifacts exclude the closeout owner's own receipt, which is written
   externally after/atomically with those artifacts and is verified by C2;
3. add the closeout-owner receipt hash and terminality check to the terminal verifier's required
   evidence, while keeping the verifier's own receipt outside its verdict.

### Regression verification

C2-02 remains repaired. No regression was found in exact A-004 producer-output binding, A-005
historical grandfathering, non-backdated responsibility, supplemental test scope and command
coverage, dirty-hunk preservation, full three-lens review, ordered approver package, or the dual-PASS
Stage-B block.

This is a narrow receipt-boundary repair. Freeze and independently re-review one final hash before
any cycle-2 launch or resume.

## Final receipt-boundary repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `BEF303F71CD8C6A69C12B0B00528EEF63C705657BAFB9751B9F31E2308FE3CCA`  
**Verdict:** **PASS**

The remaining receipt chronology is finite and internally consistent:

- `lifecycle-manifest.pre-approval.json` contains only receipts that already exist through terminal
  integrity. It excludes the PRE_REVIEW_FREEZE author's separately and atomically emitted receipt.
- Attacker, writer, skeptic, and coverage receipts are created later at their actual times and enter
  only the ordered approval evidence package; no clause inserts them into either earlier lifecycle
  manifest.
- Frozen attacker targets, review/Coverage deliverables, approval evidence, approval outputs, and
  post-approval closeout are distinct evidence classes with explicit one-way chronology.
- The closeout owner atomically writes `lifecycle-manifest.closeout.json`,
  `cycle-2-completion.json`, and a separate external owner receipt. The artifacts exclude the
  receipt from their content/hash; the receipt hashes both completed artifacts.
- The terminal verifier is required to verify that external closeout-owner receipt and both artifact
  hashes. Its own later receipt is neither input to nor approved by its verdict.

C2-01 and C2-02 are therefore closed at the contract level. No future artifact, self-receipt,
backdated lifecycle, overwrite, or retroactive corpus enlargement is required to execute the two
boundaries.

Regression checks also pass. The sole authoritative cycle-2 order remains explicit; old order/graph
descriptions remain non-operative; A-001 terminal-test and repin order is unchanged; A-002 retains
future-only attributable receipts; A-004 retains exact producer-output receipt equality; A-005
retains its uniquely resolved pre-route historical exception; the supplemental A-004 test, dirty
preservation, three-lens review, ordered approval package, and dual-PASS Stage-B block remain intact.

This PASS approves only the repaired bootstrap contract at the reviewed hash. It is not evidence
that implementation, receipts, tests, integrity, review, approval, closeout, or Stage-A completion
has occurred, and Stage B remains blocked until both required PASS boundaries exist and verify.
