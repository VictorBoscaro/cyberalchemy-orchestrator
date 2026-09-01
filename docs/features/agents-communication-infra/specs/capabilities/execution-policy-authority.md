# Execution-Policy Contract, Synthetic Lineage and Fake Denial

This capability routes the bounded POLICY-000/L0, POLICY-001/L1 and POLICY-002/L2 contracts from the feature
[SPEC](../SPEC.md) into one non-executable contract surface. It refines the discovery's requirement
for fail-closed sandbox, credential and tool isolation without claiming that those controls are
implemented or that any policy value authorizes execution.

## Outcome and boundary

POLICY-000 defines pure, recursively closed parsing and canonicalization for exact execution-policy
documents and test-only oracle values. POLICY-001 adds an isolated test seam that may persist and
reopen the exact seven ordered POLICY-000 members plus one closed, non-executable lineage receipt as
one all-or-none synthetic unit. POLICY-002 adds a second isolated test seam that reopens that exact
lineage, routes twelve non-executable action-attempt labels through the package-level deny-all
decision and persists one closed denial receipt while every external-action spy remains zero. All
three layers preserve byte and digest lineage; none selects product values, creates a runtime
authority row, confirms a dispatch, opens a run or performs an effect.

## Contracts

| Aspect | Contract | Responsibility | Layer and status |
|---|---|---|---|
| Domain | [ResourceBudget](../domain.md#resourcebudget) | Closed one-Attempt ceilings with explicit zero, strict int64 bounds and no derivation from dispatch ceilings. | POLICY-000/L0 specified; implementation separately gated. |
| Domain | [SandboxPolicy](../domain.md#sandboxpolicy) | Recursively default-deny policy with explicit grants, lexical root checks and caller-supplied reference bytes. | POLICY-000/L0 specified; physical host resolution excluded. |
| Domain | [ExecutionAuthorityFence](../domain.md#executionauthorityfence) and [ExecutionAuthorityFenceHarness](../domain.md#executionauthorityfenceharness) | Keep production and test fence schemas, preimages and digest domains disjoint; the L0 parser validates shape only. | POLICY-000/L0 specified; no cutover authority. |
| Domain | [ExecutionPolicyOracleFixture](../domain.md#executionpolicyoraclefixture) | Bind the reviewed all-zero budget and deny-all sandbox goldens as test data that production policy paths reject. | POLICY-000/L0 specified; never executable authority. |
| Domain | [ExecutionPolicySyntheticLineageReceipt](../domain.md#executionpolicysyntheticlineagereceipt) and [member](../domain.md#executionpolicysyntheticlineagemember) | Bind exactly seven ordered artifact/content identities under a closed test-only receipt and canonical unit digest. | POLICY-001/L1 specified; implementation separately gated. |
| Domain | [ExecutionPolicyFakeDenialReceipt](../domain.md#executionpolicyfakedenialreceipt) | Bind the exact reopened lineage and policy digests to one canonical `denied` result and two exact reason codes. | POLICY-002/L2 specified; implementation separately gated. |
| Rule | [ACI-R16](../rules.md#aci-r16--canonical-contract-policy) | Enforce strict primitives, closed schemas, `aci-cjson-1`, declared digest domains, reference verification, zero parser I/O/effects and authority separation. | POLICY-000/L0 normative rule; L1-L3 remain separate. |
| Rule | [POLICY-001/L1 lineage invariants](#policy-001l1-lineage-invariants) | Require exact membership, one-transaction persistence, deterministic replay/conflict, exact reopen and zero production-authority rows or effects. | POLICY-001/L1 specified; implementation separately gated. |
| Rule | [ACI-R23](../rules.md#aci-r23--synthetic-fake-denial-is-durable-without-attempted-effect) | Require exact source-lineage revalidation, twelve label denials, one-row durability and zero external calls. | POLICY-002/L2 normative rule; product and L3 remain separate. |
| Interface | [ExecutionPolicyContractParser](../interfaces.md#internal-executionpolicycontractparser) | Parse exact caller-supplied bytes purely and return typed non-authoritative values or rejection. It exposes no persistence, launch or effect method. | POLICY-000/L0 specified; implementation separately gated. |
| Interface | [ExecutionPolicySyntheticLineageHarness](#executionpolicysyntheticlineageharness-test-only) | Expose only test-scoped persist and reopen operations over a temporary file-backed database; never export a production runtime method. | POLICY-001/L1 specified; implementation separately gated. |
| Interface | [ExecutionPolicyFakeDenialHarness](../interfaces.md#internal-executionpolicyfakedenialharness-test-only) | Route closed test labels to one durable deny-all receipt without accepting or invoking an external callable. | POLICY-002/L2 specified; implementation separately gated. |
| Tests | [T-ACI-POL0-1 through T-ACI-POL0-8](../TEST-SPEC.md#policy-000-l0-test-matrix) | Cover recursive closure, strict integers, goldens, references, sandbox grammar, budget separation, fence domains and the oracle authority firewall. | Test obligations specified; no executable result claimed here. |
| Tests | [T-ACI-POL1-1 through T-ACI-POL1-8](#policy-001l1-test-obligations) | Cover exact membership, atomic failpoints, replay/conflict, lost response, reopen, production-parser rejection and the zero-row/effect firewall. | Test obligations specified; no executable result claimed here. |
| Tests | [T-ACI-POL2-1 through T-ACI-POL2-8](#policy-002l2-test-obligations) | Cover exact denial bytes, source/mutation rejection, twelve attempted-action labels, atomic receipt persistence, replay/reopen and zero-action/production/L3 firewalls. | Test obligations specified; no executable result claimed here. |
| Evidence | [TECH-POLICY-D0](../../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md) and its [independent review](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/TECH-D0-REVIEW.md) | Pin the closed schemas, seven golden byte/digest domains and L0-L3 promotion boundaries. | Reviewed design evidence; not implementation evidence. |
| Evidence | [POLICY-001 persistence pattern inventory](../../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md) | Specify the temporary file-backed database seam, one-transaction artifact/receipt/member unit, replay/conflict/failpoint/reopen obligations and mandatory zero-row inventory. | Bounded architecture evidence; no code-entry authority by itself. |

## Non-authoritative path

The admitted path is exact supplied bytes -> pure POLICY-000 parser -> typed non-authoritative
values -> optional POLICY-001 test-only artifact unit -> non-executable lineage receipt. The L1
transaction commits seven finalized artifacts, the receipt and its seven ordered bindings together
or commits none. After reopen, every artifact body and digest must reproduce exactly. Same-key or
same-identity replay with the same unit digest converges on the first receipt; divergent content is
a permanent conflict. Only that exact reopened unit may enter POLICY-002, where any one of twelve
closed test labels returns the same durable package-level denial receipt. The label itself is never
persisted and no path reaches a production launcher, provider or effect.

## POLICY-001/L1 lineage invariants

The L1 seam accepts only the seven POLICY-000 golden members in the receipt's fixed ordinal/name
order. It prepares their artifacts before entering the transaction, then finalizes all seven
artifacts and writes the receipt plus seven ordered bindings inside one
`RuntimeDatabase.write()` transaction. It never calls per-artifact `ArtifactStore.commit()`.

```text
accepted_l1_unit(u) => authority(u.receipt) = test-only-non-executable
  AND members(u.receipt) = exact_ordered_policy000_members[0..6]
  AND unit_digest(u.receipt) = sha256(aci_cjson_1(lineage_unit_preimage(u)))
  AND every_member_body_reproduces_content_digest(u)

commit(u) => atomic(seven_finalized_artifacts(u), receipt(u), seven_bindings(u))
failure_before_commit(u) => policy001_rows(u) = empty
same_key_or_identity_and_same_unit_digest => return_first_receipt
same_key_or_identity_and_different_unit_digest => permanent_conflict
reopen(u) => exact_member_bodies_and_digests(u) AND same_receipt(u)
production_policy_parser(combined_oracle_or_harness) => reject
policy001_runtime_authority_rows = 0
policy001_external_effects = 0
```

### ExecutionPolicySyntheticLineageHarness (test-only)

This is an internal, test-only module boundary, not a service/API or production package export.

| Method | Input | Output | Contract |
|---|---|---|---|
| `persistSyntheticLineage` | temporary file-backed database, `synthetic_key`, `lineage_identity`, exact seven validated POLICY-000 member bodies, optional named test failpoint | first closed lineage receipt or typed rejection/conflict | Prepare outside the transaction; resolve replay/conflict and atomically finalize seven artifacts, one receipt and seven bindings inside one transaction. Failpoints exist only for atomicity tests. |
| `reopenSyntheticLineage` | same database path and persisted receipt identity | exact seven reopened member bodies/digests plus the first receipt, or typed rejection | Reopen through the existing artifact boundary; reproduce every byte/digest, membership ordinal/name and receipt field without invoking a provider, launcher, journal, appender or resolver with external effects. |

The harness may create exactly two test-only tables in the temporary database. They are absent from
production migrations, and the boundary exposes no confirm, run, plan, request, attempt, event,
effect, launch, audit or provider operation.

## POLICY-001/L1 test obligations

| ID | Required assertion |
|---|---|
| `T-ACI-POL1-1` | Only the seven reviewed POLICY-000 member bodies accept, at ordinals `0..6` with the receipt's exact names; addition, omission, renaming, reordering, artifact substitution or byte/digest drift rejects or conflicts. |
| `T-ACI-POL1-2` | Failpoints after transaction begin, after each artifact, after the receipt, after each binding and before commit reopen to the complete unit or no POLICY-001 rows. |
| `T-ACI-POL1-3` | The same `synthetic_key` and unit digest return the first receipt; a changed digest is a permanent conflict. |
| `T-ACI-POL1-4` | The same `lineage_identity` and unit digest return the first receipt; a changed digest is a permanent conflict. |
| `T-ACI-POL1-5` | A lost response after commit followed by retry converges on the first persisted receipt and creates no duplicate unit. |
| `T-ACI-POL1-6` | Closing and reopening the same file-backed database reproduces every exact member body/digest, binding and receipt field. |
| `T-ACI-POL1-7` | Production policy-document parsers reject the combined oracle structurally, and the production fence parser rejects the harness schema before evidence resolution. |
| `T-ACI-POL1-8` | After success and every failure, only finalized artifacts and the two test-only lineage tables may contain POLICY-001 rows; fail-on-call spies prove zero runtime, audit, provider, launcher, tool or other external effects. |

## POLICY-002/L2 fake-denial invariants

POLICY-002 accepts no policy document directly. It first reopens the exact first POLICY-001 receipt
and all seven members, reproduces their canonical bytes/digests and reruns the POLICY-000 parsers.
Any positive budget, non-empty sandbox grant, missing member or authority-domain substitution
rejects before a denial transaction begins.

```text
accepted_l2_source(u) => reopen_exact_policy001(u) AND policy000_valid(every_member(u))
label in closed_twelve_test_labels =>
  first_fake_denial_receipt(u)
  AND label notIn receipt_or_authority
  AND external_calls = empty
commit_denial(u) => atomic(one_test_only_denial_row(u))
replay_same_denial_digest => first_receipt
replay_changed_denial_digest => permanent_conflict_without_write
reopen_denial(u) => exact_receipt_bytes_and_digests(u) AND exact_source_binding(u)
policy002_runtime_authority_rows = 0
policy002_l3_evidence = 0
```

### ExecutionPolicyFakeDenialHarness (test-only)

This is the test-only interface defined in
[interfaces.md](../interfaces.md#internal-executionpolicyfakedenialharness-test-only). It accepts
only a temporary file-backed database path, denial key, persisted lineage identity, one closed test
label and optional named failpoint. It exposes no process/provider/tool/network/credential callable,
sealed request, production fence, runtime service, journal or audit dependency. The same database
may gain exactly one additional denial-receipt table; existing POLICY-001 rows never change.

The twelve labels are test-routing selectors frozen by
[T-ACI-POL2-3](../TEST-SPEC.md#t-aci-pol2-3--decision-reasons-and-attempt-labels-are-closed).
Every selector yields the same package-level receipt because labels are outside the preimage,
receipt, identity and authority. Temporary SQLite persistence is the only admitted I/O.

## POLICY-002/L2 test obligations

| ID | Required assertion |
|---|---|
| `T-ACI-POL2-1` | Exact denial preimage/receipt bytes and both declared digests reproduce independently. |
| `T-ACI-POL2-2` | Missing/drifted lineage, each positive ceiling and each non-empty grant rejects before denial persistence. |
| `T-ACI-POL2-3` | Exactly twelve non-executable labels accept; the only decision/reason list is the frozen denial, and labels never enter authority. |
| `T-ACI-POL2-4` | Begin/receipt/before-commit failures leave zero denial rows; after-commit loss leaves exactly the first durable receipt. |
| `T-ACI-POL2-5` | Denial-key and lineage-identity replay converge only on an unchanged denial digest; drift conflicts without mutation. |
| `T-ACI-POL2-6` | Fresh file-backed reopen reproduces receipt bytes/digests and exact source-lineage binding. |
| `T-ACI-POL2-7` | Each label independently returns the same durable denial while every external-action spy remains zero. |
| `T-ACI-POL2-8` | Only one test denial table/row is added; production confirmation/plan/request/effect inputs reject and no L3 evidence exists. |

## Exclusions

POLICY-003/L3 target-host enforcement is outside this capability version. It does not select
`ResourceBudget`, `SandboxPolicy`, tool-profile or credential
grant values for a product; mint `cutover_epoch` or watcher-disable evidence; create a production
migration, service, API, journal command or package export; populate `ConfirmedDispatch`, `Run`,
`AgentInvocationPlan`, `AgentExecutionRequest`, `Attempt`, event or effect tables; authorize an
audit opening, provider/tool call, subprocess or external action; or prove host isolation, current
fence enforcement or runtime cutover. OpenAI/Codex CLI or any other real provider remains outside
POLICY-002 and requires a later product/provider authority record, POLICY-003 host enforcement and
provider-admission evidence.
