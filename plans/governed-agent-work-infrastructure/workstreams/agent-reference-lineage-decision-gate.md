---
tags: [plans, agent-reference-lineage, decision-gate, implementation-readiness]
node_type: decision-record
status: pass
version: 0.1.0
last_updated: 2026-07-25
target_scope: agent-reference-lineage-l0
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Agent Reference Lineage L0 Decision Gate

## Scope

This gate governs readiness planning and a task-session dry-run for L0 only:

```text
ACI AgentReferenceDelivery
+ EffectiveInputEntry.reference_bundle / EffectiveInputArtifact metadata
+ reference_scout.bundle_delivered_to_agent@1
+ complete ACI target/delivery evidence reader
+ T-ACI-R22 / T-ACI-ARD1..5 contract tests
```

It authorizes no runtime mutation. L1–L3 remain outside the selected task.

## Consequential Boundary

The only architecture-level choice that could have blocked L0 was whether to build through a
bounded host-workflow bridge or reopen the complete general ACI invocation pipeline. That choice is
already resolved by the accepted
[Host Agent Dispatch Input Binding decision](../../../docs/decisions/host-agent-dispatch-input-binding.md#decision):
Option A, bounded host-workflow binding bridge.

This gate consumes that decision; it does not reinterpret or reopen it.

## Decision Inventory

| ID | Classification | Question or condition | Resolution | Source / rationale |
|---|---|---|---|---|
| `DG-ARL-01` | inherited accepted decision | Which host-to-agent input boundary governs the bounded local implementation? | Option A — bounded host-workflow binding bridge. | Repository-owner decision is already accepted and implemented as a bounded host-observable bridge. |
| `DG-ARL-02` | assumption | Can the existing confirmed Option-A Dispatch/group/seat/attempt binding be consumed by an ACI-owned adapter without claiming complete provider input? | Proceed for planning; L0 execution must verify the adapter boundary before mutation and return BLOCK if the binding is insufficient. | Option A explicitly permits exact host-observable input/output binding and forbids the broader claim. |
| `DG-ARL-03` | governance constraint | Must implementation and contract-test review remain independent? | Yes. The future L0 work-pack/dry-run must assign an ACI implementer, an independent ACI reviewer and an independent contract-test reviewer; missing separation blocks its review. | Required by the requested dispatch and by L0 exit evidence; it is not an assumption or optional design choice. |
| `DG-ARL-04` | deferrable | Which migration number, module names and internal class split should L0 use? | Defer to the ACI implementer inside the declared write scope, subject to reviewer approval and no unrelated refactor. | Reversible internal organization does not change the owner contracts or layer boundary. |
| `DG-ARL-05` | evidence gate | Is the current cross-document `producer_resolution`/seven-digest synchronization independently accepted? | Synchronization is present, but a fresh cross-document PASS is still required before L1 implementation. It is not required for L0. | Current APT Query/Rule/Interface/TEST-SPEC contain the contract; independent acceptance evidence has not been established by this dry-run. |
| `DG-ARL-06` | deferrable | Which host SourceObservation contract version enables access? | Resolve in L2. | L0 proves delivery only and must not imply access. |

## Blocker Audit

| Candidate blocker | Current result | Why it does not block this dry-run |
|---|---|---|
| Option A versus general pipeline | resolved | Option A is already accepted repository-owner authority. |
| Missing ACI target-delivery implementation | expected task scope | L0 exists to implement it; the contracts and test obligations are specified. |
| APT `producer_resolution` cross-document acceptance | pending L1 evidence gate | L0 stops at ACI delivery/effective-input/evidence-reader authority and does not consume this wrapper. |
| Host access observation contract unavailable | deferred L2 capability | Delivery evidence explicitly does not prove access. |
| Production/readiness approval | not requested | This dispatch is planning plus dry-run only and performs no runtime handoff. |

No blocker-level decision remains unresolved for producing the L0 work-pack and dry-run.

## Execution Constraints and Failure Triggers

1. The L0 implementer treats the Option-A envelope as host-observable binding evidence only.
2. The ACI owner derives the target identity and owns delivery/effective-input acceptance; the host
   does not mint `AgentReferenceDelivery`.
3. If the current runtime cannot expose a same-Dispatch Attempt binding without broadening into the
   general invocation pipeline, L0 execution returns `BLOCK`; it does not silently choose Option B.
4. Exact migration/module placement is selected only after inspecting current runtime conventions
   and must remain within the work-pack write scope.
5. No task record may be marked implemented from this dry-run.

## Gate Result

| Field | Result |
|---|---|
| Target scope | `Agent Reference Lineage implementation / L0` |
| Result | `PASS` |
| New decisions resolved | `0` |
| Inherited accepted decisions | `1` (`DG-ARL-01`, Option A) |
| Blockers remaining | `0` |
| Deferred decisions | `2` (`DG-ARL-04`, `DG-ARL-06`) |
| Pending evidence gates | `1` (`DG-ARL-05`, L1 only) |
| Assumptions | `1` (`DG-ARL-02`) |
| Governance constraints | `1` (`DG-ARL-03`) |
| Execution failure triggers | `5` explicit conditions in the section above |
| User override | none |
| Next step | Build a strict lean context pack, then dry-run exactly the L0 task. |

This PASS permits planning artifacts only. It is not construction, mutation, enablement or
deployment authority.
