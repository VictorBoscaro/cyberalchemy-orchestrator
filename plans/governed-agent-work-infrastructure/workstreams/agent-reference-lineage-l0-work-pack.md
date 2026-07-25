---
tags: [plans, agent-reference-lineage, work-pack, task-session, dry-run, aci]
node_type: work-pack
status: implementation-complete-review-pending
version: 0.2.0
last_updated: 2026-07-25
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
selected_layer: L0
execution_mode: local
runtime_handoff: none
---

# Agent Reference Lineage L0 Work Pack

This work-pack defines exactly one Smallest Working Unit. It is a planning and task-session dry-run
artifact; it does not authorize or report runtime implementation.

## Controlling Artifacts

| Artifact | Authority for this SWU |
|---|---|
| [Implementation layering](agent-reference-lineage-implementation-layering.md#l0-minimum-working-unit) | Selects L0 as the minimum ACI-owned proof and defers L1–L3. |
| [Decision gate](agent-reference-lineage-decision-gate.md#gate-result) | PASS for planning/dry-run with zero blockers; records assumptions and failure triggers. |
| [Accepted Option A](../../../docs/decisions/host-agent-dispatch-input-binding.md#decision) | Keeps the host boundary bounded and forbids silently expanding into the general invocation pipeline. |

## SWU Manifest

| Field | Value |
|---|---|
| SWU ID | `SWU-ARL-L0-001` |
| Title | ACI reference-bundle target settlement and evidence reader |
| Layer | L0 only |
| Status | `implementation-complete-review-pending` |
| Execution status | `implemented-validation-pass-review-blocked` |
| Owner | ACI implementation seat |
| Reviewer 1 | independent ACI contract reviewer |
| Reviewer 2 | independent contract-test reviewer |
| Runtime | local repository runtime, future execution only |
| External handoff | none |

## Objective

Implement the smallest ACI-owned slice that accepts one already committed and lifecycle-delivered
Scout bundle into one authenticated same-Dispatch Attempt, records its exact
`EffectiveInputEntry.reference_bundle` and `AgentReferenceDelivery` atomically, and returns complete
target/delivery evidence to an APT consumer without implying access, declared use or claim support.

## Dependencies

| ID | Dependency | Required state | Gate behavior |
|---|---|---|---|
| `DEP-L0-01` | Accepted Option-A host Dispatch/group/seat/attempt binding | Exact binding can be consumed by an ACI-owned adapter without claiming full provider input. The adapter preallocates a logical ACI `agent_instance_id` from the authenticated Dispatch/group/seat binding; this is not the nullable host/provider `agent_id` learned after launch. | If the logical identity cannot be derived before launch, `BLOCK`; do not substitute the provider ID or choose the general pipeline. |
| `DEP-L0-02` | Accepted Scout commit and immutable bundle artifact | Exact ScoutRun, artifact, digest and ordered recommendation membership. | Missing or divergent evidence fails closed. |
| `DEP-L0-03` | Distinct accepted Scout lifecycle-delivery event | Same ScoutRun/artifact/digest; no recommendation-membership claim. | Missing or mismatched event fails closed. |
| `DEP-L0-04` | Authenticated target delivery capability and target Attempt | Same Dispatch; target Attempt/seat/agent instance derived by ACI. | Caller-authored or cross-Dispatch identity blocks acceptance. |
| `DEP-L0-05` | Existing ACI journal, artifact and canonicalization boundaries | Support one atomic settlement and deterministic wrapper digests. | Missing atomic/canonical path blocks implementation. |

## Owner Responsibilities

### ACI implementation seat

- Inspect existing runtime conventions before choosing the internal module split.
- Implement only the L0 acceptance and evidence-reader paths.
- Preserve Option A's compatibility/non-correspondence boundary.
- Add contract tests with each behavior branch, not after implementation.
- Produce a change/evidence summary for both reviewers.

### Independent ACI contract reviewer

- Review ownership, authorization, same-Dispatch identity, preallocation, atomicity, idempotency,
  crash behavior and no-general-pipeline expansion.
- Compare implementation behavior to ACI domain, mapping, event/operation and `T-ACI-R22` contracts.
- Return `pass | fix`; never review own implementation.

### Independent contract-test reviewer

- Review positive, mutation, retry, fault and evidence-boundary coverage independently from the ACI
  implementation reviewer.
- Verify each `T-ACI-R22` and `T-ACI-ARD1..5` obligation maps to an executable case.
- Reject tautological mocks, omitted atomic members and any test that infers access/use/support.

## Declared Write Scope for Future Execution

Only these paths may be created or changed by `SWU-ARL-L0-001`:

```text
implementations/server/runtime/migrations/010_agent_reference_delivery.sql
implementations/server/runtime/reference_delivery.py
implementations/server/runtime/database.py
implementations/server/runtime/service.py
implementations/server/runtime/artifacts.py
implementations/server/runtime/journal.py
implementations/tests/runtime/test_agent_reference_delivery.py
implementations/tests/runtime/test_agent_reference_evidence_reader.py
implementations/tests/runtime/aci-test-traceability.json
implementations/tests/runtime/test_aci_traceability.py
docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
implementations/server/runtime/local_pilot.py
```

Any need to edit another runtime file is a scope-change request and returns `BLOCK` until reviewed.
Specs, plans, host hooks, APT projector/query code, telemetry, UI and provider adapters are
explicitly outside the execution write scope.

## Deliverables

1. Migration `010_agent_reference_delivery.sql` with immutable delivery/effective-input metadata,
   semantic uniqueness and same-source/target retry constraints; no raw bundle body duplication.
2. ACI settlement component that:
   - preallocates delivery and target-event IDs;
   - verifies commit, immutable bytes/order/digest and lifecycle delivery;
   - derives target identity from authenticated ACI authority;
   - finalizes one exact `reference_bundle` entry;
   - accepts the full L0 unit atomically or accepts none.
3. Complete, versioned target-resolution and delivery wrappers plus
   `verify_reference_bundle_entry`, with closed typed failures.
4. Executable tests for `T-ACI-R22`, `T-ACI-ARD1..5`, retry/drift, all member failpoints, wrapper
   completeness/as-of/scope/version/digest and the evidence boundary.
5. Updated ACI test traceability for these exact test IDs.
6. Independent ACI and contract-test review verdicts.

## Done Criteria

- Exactly one canonical delivery exists per `(scout_run_id,target_attempt_id)`.
- Exact retry returns the original IDs/receipt; any semantic drift conflicts with no new acceptance.
- Commit plus immutable bytes own recommendation membership; lifecycle delivery never does.
- One unique `reference_bundle` entry matches artifact, digest, delivery ID, policy and ordinal.
- Delivery, effective-input metadata, Attempt, target-delivery event, `attempt.requested` and
  existing sealed-request/effect members commit as one unit or none.
- Target-resolution and delivery-reader wrappers are complete, canonical, owner-versioned,
  query-scoped and fail closed on omission, extra, future, duplicate, wrong scope/version/digest or
  incomplete group.
- No output, event, projection or test claims access, reading, declared use or claim support.
- All listed validations pass and both independent reviewers return PASS.
- No file outside the declared write scope changes.

## Validation Surface

Future execution must run, at minimum:

```text
python -m unittest implementations.tests.runtime.test_agent_reference_delivery
python -m unittest implementations.tests.runtime.test_agent_reference_evidence_reader
python -m unittest implementations.tests.runtime.test_aci_traceability
python -m unittest discover -s implementations/tests/runtime -p "test_*.py"
python implementations/tests/audit_enums.py
git diff --check -- <declared-write-scope>
```

The implementer must also report the exact failpoint matrix and test-ID-to-case mapping. A command
that is unavailable or fails cannot be silently skipped; the task returns `FLAG` or `BLOCK` with
the nearest evidence and unblock action.

## Explicit Non-Goals

- No APT binder, reducer, Query, mapper or projection.
- No host SourceObservation available manifest or access inference.
- No L1 `producer_resolution` implementation or fresh cross-document review receipt; the current
  synchronized L1 contract remains outside this SWU.
- No general invocation pipeline, provider adapter, agent launch, production deployment or external
  runtime handoff.
- No new telemetry or observability implementation.

## Execution Report — 2026-07-25

### Result

`FLAG`: the L0 implementation and all available validation passed, but the two mandatory
independent reviews remain blocked because the current Codex task does not apply the repaired
`spawn_agent` hook and therefore produces no durable launch/close receipts.

### Implemented

- Migration `010_agent_reference_delivery.sql` persists the complete attempt acceptance unit:
  logical Attempt, finalized effective-input metadata, sealed request, pending sandbox effect and
  immutable `AgentReferenceDelivery`.
- `reference_delivery.py` derives pre-launch logical target identity, verifies immutable bundle
  bytes and membership, builds the unique typed input entry, verifies it and emits complete
  digest-bound owner wrappers.
- `RuntimeService.settle_agent_reference_delivery` binds the exact lifecycle-delivery event through
  the authenticated capability and atomically commits
  `reference_scout.bundle_delivered_to_agent@1` plus `attempt.requested`.
- Target and delivery evidence readers reject wrong schema/owner/digest, incomplete or extra wrapper
  fields, entry omission/duplication/drift and incomplete accepted journal groups.
- ACI traceability now maps `T-ACI-R22` and `T-ACI-ARD1..5` to executable cases.

The pre-launch ACI `agent_instance_id` is a logical runtime identity derived from the authenticated
Dispatch/group/seat binding. It is deliberately distinct from the nullable host/provider
`agent_id`, which remains post-launch correlation evidence.

### Validation evidence

| Check | Result |
|---|---|
| Targeted delivery/evidence/traceability suites | PASS, 10 tests |
| Complete runtime discovery | PASS, 88 tests |
| Transaction failpoints | PASS for rollback before commit and convergence after commit |
| Python compileall | PASS |
| Stage-E source-integrity preflight exercised by runtime suite | PASS |
| `git diff --check` over the amended L0 scope | PASS; line-ending warnings only |
| Enum audit | Command PASS; reports the same 9 pre-existing legacy `dispatch_type=others` rows |

### Remaining gate

Do not mark the SWU `complete` until:

1. a fresh Codex task loads the repaired `.codex/hooks.json`;
2. one smoke launch produces matching durable opening and closing receipts;
3. the independent ACI contract reviewer and contract-test reviewer both return PASS;
4. the parent reviews their complete evidence and closes this `FLAG`.

## Dry-Run Report

### Task Session Result

| Field | Result |
|---|---|
| Task | `SWU-ARL-L0-001` |
| Result | `FLAG` for planning/dry-run; execution remains blocked on lifecycle-receipt evidence |
| Execution state | `not-started` |
| Decisions | `0` new; inherited accepted Option A; one execution assumption |
| Context pack | [lean pack](agent-reference-lineage-l0-context-pack.md), 8 files, 8/8 obligations covered |
| Handoff pack | none |
| Strict coverage | `pass` for planning/dry-run |
| Fallback search | named gaps only; no broad search authorized |
| Runtime | local repository runtime for future execution |
| Adapter | none |
| Gate verdict | L0 path, scope, done criteria and validations are known; execution still requires explicit construction authority and DEP-L0-01 preflight |
| Subagent closeout | `flag`: 6/6 reviewers are completed in the live agent tree, but current durable hook-managed receipt IDs could not be located |
| Files updated by the task session | this planning work-pack only |
| Experiment harness | `not_applicable` |
| Synchronized records | this work-pack; no implementation/completion status changed |
| Follow-up | reconcile or expose the hook-managed lifecycle receipts before an execution-mode task session |

### Context and Constraint Extraction

The lean pack establishes these controlling constraints:

1. Option A is closed and remains a bounded host-observable bridge.
2. ACI alone owns target identity, delivery and effective-input acceptance.
3. Commit plus immutable bundle bytes, not lifecycle delivery, own recommendation membership.
4. ACI settlement and evidence wrappers fail closed and remain distinct from all access/use/support
   facts.
5. L0 contract tests are `T-ACI-R22` and `T-ACI-ARD1..5`; R9 is downstream non-regression context,
   not an APT implementation obligation in this SWU.
6. No runtime handoff, spec mutation, telemetry work or L1–L3 implementation is authorized.

### Decision Pack

No blocker-level multi-option decision remains.

| Item | Classification | Dry-run treatment |
|---|---|---|
| Bounded bridge versus general pipeline | inherited accepted | Option A controls; never reopen or silently choose the general pipeline. |
| Option-A binding can feed ACI-owned adapter | resolved constraint | Preallocate a logical ACI agent-instance identity from the authenticated Dispatch/group/seat binding. Keep it distinct from the nullable host/provider `agent_id`, which is only correlation evidence learned after launch. |
| Internal module split | deferrable | Recommend isolating new settlement/reader logic in `reference_delivery.py`; implementer may adjust only inside write scope and reviewer approval. |
| Persistence path | constrained recommendation | Extend existing journal/artifact transaction and migration path; no second store or projection authority. |
| Evidence-reader materialization | constrained recommendation | Derive complete wrappers from accepted owner state; no caller-authored member collection or raw bundle response. |

### Gate Evaluation

| Gate | Dry-run result | Evidence / execution condition |
|---|---|---|
| Exactly one task | pass | One SWU, `SWU-ARL-L0-001`. |
| Source authority | pass | Accepted Option A plus current ACI/APT contracts. |
| Blocker decisions | pass | Decision gate reports zero L0 blockers. |
| Context coverage | pass | Lean pack covers 8/8 obligations with no L0 contradiction. |
| Write scope | pass | Nine exact future paths; current status check found no changes on those paths and four planned new files do not yet exist. `database.py` is included because its explicit migration registry must admit migration 010. |
| Validation surface | pass | Exact commands and failpoint/traceability obligations are recorded. |
| Independent roles | pass for plan | Three distinct future seats are mandatory; absence blocks execution review. |
| Construction authority | not evaluated | Not requested by this dry-run; future execution must obtain it. |
| Runtime handoff | n/a | No `--via runtime`, adapter or handoff pack. |
| L1 cross-doc receipt | n/a for L0 | Required before L1, not consumed here. |

### Ordered Future Execution Path

1. Re-read the exact work-pack, decision and lean context pack; verify source digests/currentness.
2. Confirm DEP-L0-01 against the live Option-A binding without modifying code. Derive a stable
   logical ACI seat and agent-instance identity before launch from the authenticated binding; never
   substitute the nullable host/provider `agent_id`. If this cannot supply a same-Dispatch ACI
   Attempt binding within the bounded bridge, return `BLOCK`.
3. Inspect only the declared existing runtime files and confirm migration `010` is still available.
4. Add failing `T-ACI-R22`/ARD contract tests for the first settlement branch.
5. Add migration and isolated settlement/reader module; wire only the minimum existing
   service/artifact/journal seams.
6. Implement preallocation, bundle verification, exact input-entry canonicalization and atomic
   acceptance branch-by-branch, keeping each new behavior paired with its test.
7. Implement complete target/delivery wrappers and typed reader failures without raw bytes.
8. Add retry/drift, every-member failpoint, wrapper completeness/as-of/scope/version/digest and
   evidence-boundary cases; update traceability.
9. Run every validation command and capture exact results.
10. Send the bounded diff first to the independent ACI reviewer, apply confirmed fixes, then send
    tests/evidence independently to the contract-test reviewer. Both must PASS.
11. Synchronize execution evidence only after tests and both reviews pass; do not mark L1 ready.

### Completion Validation Plan

The future session must evaluate every Done Criterion against:

- the targeted `test_agent_reference_delivery` suite;
- the targeted `test_agent_reference_evidence_reader` suite;
- ACI traceability and enum audit;
- the complete current runtime regression suite;
- an explicit failpoint matrix;
- a path-scoped clean-diff check;
- independent ACI and contract-test review receipts.

This dry-run verified that the commands, paths and acceptance obligations are specified. It did not
run nonexistent L0 tests or treat current baseline tests as implementation evidence.

### Subagent Closeout

| Metric | Count |
|---|---:|
| Spawned for readiness artifact review | 6 |
| Joined in live agent tree | 6 |
| Completed with final verdict in live agent tree | 6 |
| Durable hook receipt IDs verified | 0 |
| Blocked | 0 |
| Timed out | 0 |
| Handed off | 0 |
| Open | 0 |

Result: `flag`. The live collaboration tree shows every reviewer completed and no open agent, but
the required durable receipt audit is not proven. The audit checked the configured hook contract
at `.codex/hooks.json`, the configured ledger
`telemetry/agents/subagents-dispatch.yaml`, and
`telemetry/runtime/local-pilot/orchestration-hooks/codex/`; no current receipt IDs for these six
reviewers were discoverable. No row was appended or repaired manually. This count covers the
layering, decision and context artifact reviews, including the three fresh continuations required
after concurrent source changes. The independent final review of this completed work-pack is a
subsequent document gate and is reported in the overall readiness handoff.

### Decision Gate Result

| Field | Result |
|---|---|
| Target scope | `Agent Reference Lineage implementation / L0` |
| Result | `PASS` |
| Decisions resolved in this session | `0` |
| Inherited accepted decision | Option A |
| Blockers remaining | `0` for planning/dry-run |
| Decision artifact | [Agent Reference Lineage L0 Decision Gate](agent-reference-lineage-decision-gate.md) |
| Deferred decisions | module/migration internal split and L2 host SourceObservation version |
| Assumptions recorded | Option-A binding can feed an ACI-owned adapter; execution preflight must prove it |
| Validation | decision artifact `fix → pass`, then fresh continuation `pass`; current L0 blocker audit remains zero |
| Recommendation | Proceed only to an explicitly authorized L0 execution session; keep L1–L3 deferred. |
| Next step | Independent review of this work-pack, then reconcile lifecycle receipts before execution. |

### Dry-Run Follow-up

- Required next action: obtain explicit construction authority and start one execution-mode task
  session for `SWU-ARL-L0-001`.
- Mandatory execution preflight: prove the Option-A binding can supply the required ACI-owned
  same-Dispatch Attempt binding without broadening into Option B.
- Governance evidence: expose or reconcile the hook-managed reviewer lifecycle receipts; do not
  manually append ledger rows.
- Later, before L1: obtain a fresh cross-document PASS for the synchronized
  `producer_resolution`/seven-digest contract.
