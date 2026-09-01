# TASK-POLICY-001 - synthetic execution-policy lineage persistence

## Status

- **State:** `READY_FOR_CODE_ENTRY`
- **SWU:** `SWU-ACI-EXECUTION-POLICY-LINEAGE-001`
- **Reason:** the L1 technical seam, complete normative DomainSpec package and POLICY-000 source
  implementation are independently reviewed and digest-pinned. The exact code-readiness receipt is
  `PASS` for only the three bounded test paths below; implementation has not started.

## Decision question

After this L1 unit, we know whether the exact seven-member POLICY-000 oracle can retain one
non-executable integrity lineage through an isolated, file-backed SQLite artifact transaction and
reopen without acquiring runtime authority or causing an external effect.

## Frozen planning and normative authority

- [TECH-POLICY-D0](../../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md)
  at `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e`.
- [POLICY-001 persistence pattern inventory](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md)
  at `sha256:d8eae9829069631caaef769635b3748b5440d5bfab4aacaf682f736eb546d84e`.
- [POLICY-001 DomainSpec integrated review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-DOMAINSPEC-REVIEW.md)
  at `sha256:4d05db37d0c1351ac2859b92dde001bc5932575c3b0d9549776b842109cf27ca`,
  verdict `PASS / KEEP` for the exact eight-document normative package it lists.
- [POLICY-000 implementation review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md)
  at `sha256:76ed9cd9efd6794e7b1d4c40421635db16edc8a580e789f837b415d892b13c8c`,
  verdict `PASS / KEEP` for the exact parser, fixture and test hashes pinned by the descriptor.

## Bounded deliverable

One implementation task may add only:

- `implementations/tests/runtime/policy_lineage_harness.py` - an internal test-only seam over a
  temporary file-backed `RuntimeDatabase` and `ArtifactStore`;
- `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json` - the exact closed L1
  input/expected receipt corpus derived from the reviewed seven POLICY-000 members;
- `implementations/tests/runtime/test_execution_policy_lineage.py` - the complete T-ACI-POL1-1
  through T-ACI-POL1-8 conformance suite.

The implementation may read the pinned POLICY-000 parser/fixture/test and existing database,
artifact and canonical helpers. It must not add a migration, change runtime/service/journal/API/CLI
or exports, populate production authority/runtime rows, produce an L2 denial receipt, or perform an
external action.

## L1 proof obligations

- Independently revalidate the exact seven source member bodies and content identities before
  persistence, in the fixed order `budget_policy`, `sandbox_enforcement_policy`,
  `resource_budget`, `sandbox_policy`, `combined_oracle`, `harness_fence_preimage`,
  `harness_fence_document` at ordinals `0..6`.
- Emit only the closed `aci.execution-policy-synthetic-lineage-receipt@1` receipt with authority
  `test-only-non-executable`, `synthetic_key`, immutable `lineage_identity`, exact ordered member
  identities and canonical `unit_digest`.
- Prepare seven artifacts outside the transaction, then finalize them, insert one receipt and
  insert seven ordered bindings inside one `RuntimeDatabase.write()` transaction. Never call
  per-artifact `ArtifactStore.commit()`.
- Exercise failure after begin, after every artifact, after the receipt, after every binding and
  before commit; close and reopen to either the complete unit or no POLICY-001 rows.
- Prove same-key and same-lineage-identity replay converge on the first receipt when the unit digest
  is unchanged and permanently conflict without mutation when it differs.
- Fire the lost-response `after_commit` seam only after transaction exit; a fresh-harness retry must
  return the first persisted receipt with unchanged cardinalities.
- Close and reopen the same temporary file-backed database and reproduce all seven exact member
  bodies/digests, ordinals/names, the unit digest and the first receipt.
- Reassert before persistence and after reopen that production policy parsers reject the combined
  oracle and that the production fence parser rejects the harness schema before evidence
  resolution.
- After success and every failure, allow POLICY-001 rows only in `artifacts` and the two test-only
  lineage tables. Keep `confirmed_dispatches`, `runs`, `confirmed_turn_graphs`,
  `agent_invocation_plans`, `agent_execution_requests`, `agent_attempts`, `command_receipts`,
  `events`, `aggregate_heads`, `effect_intents`, `sandbox_launch_effects`,
  `publication_candidates`, `publication_receipts` and `messages` empty, with fail-on-call spies
  proving zero audit/provider/launcher/tool or other external effect.

## Explicit deferrals and non-regression

POLICY-002/L2 fake-denial behavior, POLICY-003/L3 target-host enforcement, product-selected values,
CONF v2, a production fence, real plan/request binding and any `OPEN` or physical execution remain
deferred. POLICY-001 must preserve every POLICY-000 parser, canonicalization and authority-firewall
guarantee.

## Exact code-entry condition

Code entry is valid only while every descriptor pin still matches, all three deliverable paths are
absent, the descriptor has no blocker and the companion readiness receipt returns `PASS` for the
same three paths and five validation commands. Any pin, scope or output-presence drift closes the
gate before implementation.
