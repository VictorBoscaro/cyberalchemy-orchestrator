---
module: agents-communication-infra
version: current
status: draft
updatedAt: 2026-07-21
docType: work-pack
---

# WORK-PACK: Agents Communication Infra

## Purpose

Executable migration plan from the current skill-led dispatch flow to the runtime specified by
[README.md](README.md). This is the coordinator control panel; task contracts, waves and shared
decision state live under [`work-pack/`](work-pack/).

## Control fields

| Field | Value | Notes |
|---|---|---|
| `workPackGateStatus` | **block** | Documentation-only W0 may proceed. Runtime code is blocked until Slice-0 ADRs are accepted. |
| `specAuthoringGateStatus` | **pass — W0 contracts only** | DomainSpec artifacts may ratify or defer discovery decisions; this does not promote runtime implementation or close B-001 through B-003. |
| `complexity` | high | Persistence, authorization, external effects and migration cross several authority boundaries. |
| `outputMode` | split | Tasks and waves have independent contracts. |
| `executionPackRef` | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave scheduler and delivery-stage coverage. |
| `layeringArtifactRef` | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Decision-first promotion boundaries. |
| `dispatchTechniqueTrace` | [section below](#dispatch-technique-trace) | Selected techniques affect gates and receipts. |
| `distillValidationStatus` | **flag** | Smallest unit closes; blocker ADRs and the missing local Invoke plan contract are recorded. |
| `activeLayerWindow` | L0 | W0 decisions, then Slice 0 only. |
| `lastUpdatedAt` | 2026-07-21 | Initial plan. |
| `readinessProfile` | pilot | Single-host, single-tenant runtime. |

## Objective summary

- **Objective:** make the existing confirm -> ledger opening -> agent execution -> ledger close
  discipline an explicit, recoverable runtime without a big-bang cutover.
- **Primary inputs:** feature architecture, engine constitution, current FastAPI reader/confirm
  endpoint, current ledger parser and current validated appender.
- **Success condition:** Slices 0-4 pass their own falsifiers and the existing skills/UI become
  clients of one command/runtime boundary rather than parallel executors.
- **Current authorization:** planning, ADR and DomainSpec contract artifacts only. No runtime
  implementation is authorized by this work-pack while the gate is `block`.

## Delivery boundary

Included:

- kernel, journal, outbox, materializers, runtime projection and adapter contracts;
- compatibility migration for current confirmation, skills and audit ledger;
- fake adapters first, then one real provider, portability and two built-in read-only recipes;
- deterministic, fault-injection and product-value gates.

Excluded until later phases:

- multi-host workers, Kafka/NATS, HA and multi-tenancy;
- arbitrary executable recipes, user namespaces and autonomous knowledge promotion;
- `feedback`, `zig-zag`, sealed voting, mutating `code` recipes and large-artifact service;
- rewriting or importing historical audit-ledger rows into the runtime authority.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-000 | Blocker decisions become accepted ADRs and executable contracts. | L0 | [W0](work-pack/waves/W0.md) | none | ADR gate checklist and schema review |
| S-001 | One deterministic run opens, executes, commits, closes and replays exactly once. | L0 | [W1](work-pack/waves/W1.md) | S-000 | protocol fixtures, state hashes, crash matrix |
| S-002 | The runtime survives failures while enforcing sealing and cursor-based observation. | L1 | [W2](work-pack/waves/W2.md) | S-001 | fault injection, ACL matrix, race traces, SSE recovery |
| S-003 | One real provider conforms safely to the canonical adapter contract. | L2 | [W3](work-pack/waves/W3.md) | S-002 | adapter, sandbox, credential and resource suites |
| S-004 | A preregistered product gate decides whether the architecture earns its cost. | L2/L3 boundary | [W4](work-pack/waves/W4.md) | S-003 | blinded evaluation report and threshold decision |
| S-005 | A second provider and a mixed group use the same protocol unchanged. | L3 | [W5](work-pack/waves/W5.md) | S-004 continue decision | common conformance and mixed-run fixture |
| S-006 | Sequential groups and two built-in recipes execute without kernel specialization. | L4 | [W6](work-pack/waves/W6.md) | S-005 | compiler, handoff, cutover and branch audit |
| S-007 | Completion and architecture audits close the pilot. | L4 | [W7](work-pack/waves/W7.md) | S-006 | verification, alignment and layering reports |

## Task status board

| Task | Goal | Layer | Complexity | Waves | Gate | Status |
|---|---|---|---|---|---|---|
| [TASK-000](work-pack/tasks/TASK-000.md) | Resolve Slice-0 decisions and freeze contracts. | L0 | high | W0 | ready for docs | not-started |
| [TASK-010](work-pack/tasks/TASK-010.md) | Implement journal, reducer, command dedupe and state hashing. | L0 | high | W1 | blocked by TASK-000 | not-started |
| [TASK-020](work-pack/tasks/TASK-020.md) | Implement audit-ledger opening/close materializers and reconciliation. | L0/L1 | high | W1-W2 | blocked by TASK-000/010 | not-started |
| [TASK-030](work-pack/tasks/TASK-030.md) | Execute the fixed protocol with deterministic fake adapters. | L0 | high | W1 | blocked by TASK-010/020 | not-started |
| [TASK-040](work-pack/tasks/TASK-040.md) | Add durable outbox, recovery, sealing, races and runtime SSE. | L1 | high | W2 | blocked by S-001 | not-started |
| [TASK-050](work-pack/tasks/TASK-050.md) | Integrate one real provider through `AgentAdapter`. | L2 | high | W3 | blocked by S-002 ADRs | not-started |
| [TASK-060](work-pack/tasks/TASK-060.md) | Run the preregistered product-value gate. | L2/L3 | high | W4 | blocked by TASK-050 | not-started |
| [TASK-070](work-pack/tasks/TASK-070.md) | Add second adapter and mixed-provider conformance. | L3 | high | W5 | blocked by continue decision | not-started |
| [TASK-080](work-pack/tasks/TASK-080.md) | Add sequential composition, built-in recipes and client cutover. | L4 | high | W6 | blocked by S-005 | not-started |
| [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Verify pilot completion against acceptance/falsification criteria. | L4 | high | W7 | after S-006 | not-started |
| [TASK-AUDIT-ALIGNMENT](work-pack/tasks/TASK-AUDIT-ALIGNMENT.md) | Audit implementation against architecture and authorities. | L4 | high | W7 | after S-006 | not-started |
| [TASK-AUDIT-LAYERING](work-pack/tasks/TASK-AUDIT-LAYERING.md) | Audit that promotion evidence justified every layer. | L4 | medium | W7 | after S-006 | not-started |

## First selected Smallest Working Unit

Only the following unit is selected while the gate is blocked:

| SWU | Parent | Goal | Dependencies | Write scope | Done criteria | Evidence | Verification | Owner |
|---|---|---|---|---|---|---|---|---|
| `SWU-ACI-001` | TASK-000 | Draft and decide the persistence/transaction ADR for Slice 0. | none | `docs/features/agents-communication-infra/adrs/` and decision ledger | ADR answers OQ-PERSISTENCE, OQ-STREAM and journal/outbox transaction boundary with alternatives and tests. | Accepted ADR plus schema sketch and crash-boundary table. | Human review against README sections 4.2, 9.1, 12 and 14. | manual |

All other SWUs remain unselected. Their task files contain the execution contracts required for
selection after dependencies pass.

## Blockers

| Blocker | Scope | Description | Owner | Next action |
|---|---|---|---|---|
| B-001 | Slice 0 | ADR-001 now accepts the SQLite transaction/offset and canonical-byte contracts for `SWU-ACI-001`; dependency-lock and runtime crash evidence remain downstream. The blocker remains open because `SWU-ACI-002` and the rest of TASK-000 are incomplete. | architecture owner | Complete SWU-ACI-002 and the remaining TASK-000 obligations; TASK-010 later applies the accepted pins and supplies executable crash/conformance evidence. |
| B-002 | Slice 0 | Decision, terminal and snapshot contracts are specified/proposed in DomainSpec, but are not W0-accepted or evidenced. | product/protocol owner | Complete TASK-000 ADR set and attach acceptance/fixture evidence. |
| B-003 | Audit materializer/cutover | EG-1 remains medium-veracity until W0 freezes the bundle schema, drift disposition, guard spec and named tests and TASK-020 proves the complete bundle on the target host. This does not block TASK-010 journal work. | engine owner | Freeze the contract in TASK-000; produce process identity, ACL, writer inventory and negative bypass evidence in TASK-020 before cutover; lint is auxiliary only. |
| B-004 | Invoke process | `.claude/skills/invoke/plan.md` referenced by the local skill is absent. | Invoke package owner | Treat this plan as template-based fallback; repair/regenerate skill separately. |
| B-005 | Slice 1+ | Slice-specific open questions in README section 17 require ADRs before their wave. | wave owner | Resolve in each wave's entry gate; do not pull them into W0. |

## Dispatch technique trace

| Technique | Applied to | Validation expectation | Status |
|---|---|---|---|
| `sequence` | W0 -> W7 | Every wave consumes explicit evidence from its predecessor. | pass |
| `scu_swu_reduction` | Tasks and selected SWU | The first unit is executable without starting runtime code. | pass |
| `recomposition_proof` | L0 vertical slice -> target runtime | L0 uses the same command/event/materializer boundaries later layers extend. | pass |
| `validation_loop` | Every slice | Each slice names fixtures, commands/review checks and a falsifier. | pass |
| `owner_boundary_check` | Journal, ledger, adapters, UI and skills | No task claims another store's physical-write authority. | pass |
| `authority_split_gate` | W0 ADRs and materializers | Unresolved authority ownership blocks code execution. | pass |
| `execution_receipt_handoff` | Every SWU | Completion returns files, tests, state hashes/receipts and blockers. | pass |
| `concrete_path_evidence` | Source anchors and acceptance evidence | Existing paths are linked; future paths are named plainly until created. | pass |

A full Dispatch Spec is not required for this authoring run: no subagent performs mutation and no
protected/private context crosses an execution boundary. Future implementation handoffs use one
SWU at a time and must generate their own bounded execution receipt.

## Distill validation

| Check | Result | Evidence or gap |
|---|---|---|
| Smallest coherent unit | pass | One accepted persistence ADR is the first useful unit; runtime code before it would encode accidental authority. |
| Recomposition proof | pass | The L0 command -> journal -> materializer -> fake adapter -> terminal chain is a strict subset of the target runtime. |
| Hidden acceptance-critical gaps | flag | Five Slice-0 OQs and EG-1 drift remain explicit blockers. |
| Deferred complexity | pass | Real providers, generic recipes, distributed workers and rich memory are assigned to later layers. |
| Navigation to first unit | pass | Start at TASK-000 / SWU-ACI-001, then W0 exit gate. |

### Proposer/Balancer trace

- **Proposer:** select a single deterministic vertical run, including the audit opening barrier,
  because persistence alone cannot prove the authorization invariant.
- **Balancer objection — hidden glue:** confirmation markers, appender invocation and journal
  acknowledgement could become three competing authorities.
- **Reconciliation:** the command/journal owns workflow intent; the marker is compatibility only;
  the current appender alone owns audit-ledger writes; verified acknowledgement unlocks execution.
- **Balancer objection — smuggled scale:** generic recipes, provider plurality and rich bus policy
  would obscure replay proof.
- **Reconciliation:** defer them to L3/L4; L0 has fixed seats, fixed rule and fake adapters.
- **Stable tension:** the exact SQLite durability/offset contract and legacy cutover semantics
  remain ADR decisions, so the implementation gate stays blocked.

## Gate checks

1. W0 may edit planning/ADR artifacts while `workPackGateStatus = block`; no runtime code may start.
2. Promote runtime entry for TASK-010 only when B-001/B-002 are accepted and B-003's W0 contract
   obligations are frozen. Keep audit materializer/cutover blocked until TASK-020 supplies B-003's
   complete target-host physical evidence.
3. Select exactly one SWU before each mutation-capable handoff.
4. Parallel SWUs require disjoint write scopes or an explicit merge owner.
5. A failed slice falsifier stops promotion; later waves do not compensate for it.
6. Any change to audit-ledger writes must satisfy the engine constitution and retain the current
   appender as sole physical writer.
7. Every completed SWU returns an execution receipt: files touched, validation results, state/event
   hashes where applicable, unresolved blockers and next handoff.

## Required links

- [Application discovery](discovery/feature-discovery/agents-communication-infra.md)
- [External Tool Adoptions](discovery/external-tool-adoptions.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)
- [Execution pack](EXECUTION-PACK.md)
- [Shared context](work-pack/shared/context.md)
- [Cross-task decisions](work-pack/shared/cross-task-decisions.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)
- [Traceability](work-pack/shared/traceability.md)
- [Shared SWU manifest](work-pack/shared/swu-manifest.md)
- [Wave W0](work-pack/waves/W0.md)
- [Task TASK-000](work-pack/tasks/TASK-000.md)

## Change log

| Date | Change | Author |
|---|---|---|
| 2026-07-21 | Ratified ETD-1–ETD-7, added canonical-contract/provider-admission/sole-writer evidence gates and retained runtime block. | DomainSpec spec writer |
| 2026-07-21 | Linked the pipeline-visible application discovery as the authority source for DomainSpec authoring. | Codex / discovery-writing |
| 2026-07-21 | Initial detailed migration work-pack. | Codex / Invoke fallback |
