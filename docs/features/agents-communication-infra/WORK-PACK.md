---
module: agents-communication-infra
version: current
status: draft
updatedAt: 2026-07-23
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
| `workPackGateStatus` | **pass-for-exact-swu** | Existing `SWU-ACI-APT-VS-001` and `SWU-ACI-BUS-DELIVERY-001` remain accepted. The 2026-07-26 owner-approved continuation additionally selects only `SWU-ACI-HOST-BUS-INTEGRITY-001` to close Phase-A F4/F5/F6. Every other runtime SWU remains blocked. |
| `mutationTestAuthorization` | **pass_for_exact_swu** | Owner-delegated authorization covers only the descriptor-bound F4/F5/F6 source, tests, Stage-E manifest and repository-local temporary DB work for `SWU-ACI-HOST-BUS-INTEGRITY-001`; it grants no F1/F2 policy invention, effect claim/provider execution, ACI-005 materializer or cutover authority. |
| `protocolCompilationPlanningGate` | **pass_for_exact_swu** | Applies only to [`SWU-ACI-PROTOCOL-COMPILATION-001`](work-pack/tasks/TASK-PROTOCOL-COMPILATION.md), an independent L0 Protocol Governance adjunct. It does not select W6, promote L3/L4, or reuse historical `ACI-030`. |
| `protocolCompilationReadiness` | **pass_for_exact_swu** | Descriptor, context and test pins are refreshed; the bounded implementation and T-ACI-PC1–PC12 harness pass with the full runtime suite. |
| `localPilotServeEnablement` | **pass-local-pilot-only; operative** | Independent Stage-C review accepted only explicit `127.0.0.1` serving of `SWU-ACI-APT-VS-001` with its dedicated SQLite DB and verified Stage-B receipt. |
| `hostHookRuntimeStatus` | **local-pass; host-binary-reload-required** | The matcher repair and all 48 focused infrastructure tests pass, but a fresh trusted smoke proved that embedded Codex `0.146.0-alpha.3.1` bypasses `PreToolUse` for its multi-agent handler. Official `0.146.0-alpha.10.1` is installed and selected in VS Code; no code/review dispatch may resume until the extension reloads and a smoke materializes hook state plus ACI/YAML receipts. |
| `productionEnablement` | **block** | External network, provider execution, materializer and audit-ledger cutover are excluded. |
| `cvrImplementationGateStatus` | **approval_packet_prepared — NON-PASS** | Prepared for named owner review; no owner acceptance, active exception or implementation authorization exists. |
| `cvrAuthorizationPredicate` | Global gates, or proposed exact descriptor-bound authorization for one enumerated CVR SWU | Proposed branch is non-operative until the coordinated five-entry packet is accepted; currently false. |
| `specAuthoringGateStatus` | **pass — W0 contracts only** | DomainSpec artifacts are frozen for the exact selected SWU. This does not authorize any other runtime unit or physical cutover. |
| `complexity` | high | Persistence, authorization, external effects and migration cross several authority boundaries. |
| `outputMode` | split | Tasks and waves have independent contracts. |
| `executionPackRef` | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave scheduler and delivery-stage coverage. |
| `layeringArtifactRef` | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Decision-first promotion boundaries. |
| `dispatchTechniqueTrace` | [section below](#dispatch-technique-trace) | Selected techniques affect gates and receipts. |
| `distillValidationStatus` | **pass** | W0 artifacts and the exact named-SWU descriptor passed independent digest review cycle 5/5. |
| `activeLayerWindow` | L0 | W0 decisions, then Slice 0 only. |
| `lastUpdatedAt` | 2026-08-03 | Added the exact Protocol Governance adjunct while preserving all runtime-wave gates. |
| `readinessProfile` | pilot | Single-host, single-tenant runtime. |

## Objective summary

- **Objective:** make the existing confirm -> ledger opening -> agent execution -> ledger close
  discipline an explicit, recoverable runtime without a big-bang cutover.
- **Primary inputs:** feature architecture, engine constitution, current FastAPI reader/confirm
  endpoint, current ledger parser and current validated appender.
- **Success condition:** Slices 0-4 pass their own falsifiers and the existing skills/UI become
  clients of one command/runtime boundary rather than parallel executors.
- **Current authorization:** the exact `SWU-ACI-APT-VS-001` Stage-B implementation and Stage-C
  loopback pilot are operative. The local orchestration logging bridge composes the validated
  legacy appender with ACI Session/link/lifecycle receipts under explicit owner authorization;
  Stage F makes it the fail-closed project hook for trusted local Claude and Codex Agent calls.
  This is not TASK-020 materialization or production cutover.

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
| [TASK-000](work-pack/tasks/TASK-000.md) | Resolve Slice-0 decisions and freeze contracts. | L0 | high | W0 | independent digest review cycle 5/5 PASS | completed |
| [SWU-ACI-APT-VS-001](work-pack/tasks/TASK-APT-VS-001.md) | Local Session/link/bus/probe/research vertical slice. | L0 | high | W1 bounded | Stage-B and Stage-C receipts PASS | implemented; local pilot operative |
| [TASK-CVR](work-pack/tasks/TASK-CVR.md) | Prepare and, only after exact authorization, deliver canonical vault reads in artifact then edge slices. | L0 adjunct | high | W0 adjunct | global block + nominal gate | documentation-prepared; implementation-blocked |
| [TASK-PROTOCOL-COMPILATION](work-pack/tasks/TASK-PROTOCOL-COMPILATION.md) | Compile one frozen skill/profile/binding/recipe/invocation package to a non-authoritative candidate/result. | L0 adjunct | high | independent PG adjunct | bounded implementation and verification complete | complete for exact SWU; broader protocol/runtime deferred |
| [TASK-010](work-pack/tasks/TASK-010.md) | Implement journal, reducer, command dedupe and state hashing. | L0 | high | W1 | exact `SWU-ACI-APT-VS-001` selected | bounded vertical slice implemented; broader Slice-1 work remains |
| [TASK-020](work-pack/tasks/TASK-020.md) | Implement audit-ledger opening/close materializers and reconciliation. | L0/L1 | high | W1-W2 | blocked by TASK-000/010 | not-started |
| [TASK-030](work-pack/tasks/TASK-030.md) | Execute the fixed protocol with deterministic fake adapters. | L0 | high | W1 | exact no-provider-effect SWU implemented but Phase-A FIX remains; remaining task blocked by TASK-010/020 | `SWU-ACI-BUS-DELIVERY-001` repair-required (F1-F6 and completion receipt); broader task not-started |
| [TASK-040](work-pack/tasks/TASK-040.md) | Add durable outbox, recovery, sealing, races and runtime SSE. | L1 | high | W2 | blocked by S-001 | not-started |
| [TASK-050](work-pack/tasks/TASK-050.md) | Integrate one real provider through `AgentAdapter`. | L2 | high | W3 | blocked by S-002 ADRs | not-started |
| [TASK-060](work-pack/tasks/TASK-060.md) | Run the preregistered product-value gate. | L2/L3 | high | W4 | blocked by TASK-050 | not-started |
| [TASK-070](work-pack/tasks/TASK-070.md) | Add second adapter and mixed-provider conformance. | L3 | high | W5 | blocked by continue decision | not-started |
| [TASK-080](work-pack/tasks/TASK-080.md) | Add sequential composition, built-in recipes and client cutover. | L4 | high | W6 | blocked by S-005 | not-started |
| [TASK-VERIFY](work-pack/tasks/TASK-VERIFY.md) | Verify pilot completion against acceptance/falsification criteria. | L4 | high | W7 | after S-006 | not-started |
| [TASK-AUDIT-ALIGNMENT](work-pack/tasks/TASK-AUDIT-ALIGNMENT.md) | Audit implementation against architecture and authorities. | L4 | high | W7 | after S-006 | not-started |
| [TASK-AUDIT-LAYERING](work-pack/tasks/TASK-AUDIT-LAYERING.md) | Audit that promotion evidence justified every layer. | L4 | medium | W7 | after S-006 | not-started |

## Selection state

`SWU-ACI-001` and the bounded `SWU-ACI-APT-VS-001` implementation are complete for their accepted
scope. No other runtime SWU is selected:

| SWU | Parent | Goal | Dependencies | Write scope | Done criteria | Evidence | Verification | Owner |
|---|---|---|---|---|---|---|---|---|
| `SWU-ACI-APT-VS-001` | bounded TASK-010/APT integration | Implement the exact local vertical slice. | [cross-workpack predicate](work-pack/tasks/TASK-APT-VS-001.md#entry-predicate) | descriptor-bound runtime/test paths only | Complete test matrix and execution receipt; no broadened claims. | mutation receipt, state/artifact hashes, independent implementation PASS | independent review plus root approval | selected |
| `SWU-ACI-BUS-DELIVERY-001` | bounded TASK-030 reveal-delivery proof | Prove publish→verify→sealed close→reveal→authorized peer input without external execution. | accepted journal/artifact/capability/publication base plus canonical amendment and T-ACI-PEER1–7 | exact descriptor paths only | Atomic wrapper-complete input delivery, stable retry/restart, no peer-read, zero provider/tool starts. | focused tests passed, but Phase-A review found F1-F6 and no completed execution receipt | delegated bounded owner authority plus independent review | fix-required; completion claim downgraded |
| `SWU-ACI-HOST-BUS-INTEGRITY-001` | Phase-A prerequisite maintenance | Close reviewed F4/F5/F6 without changing the accepted Host Binding or BUS behavior. | Phase-A FIX review plus T-ACI-PHASEA-I1–I3 | exact descriptor paths only | Null/mismatched follow-up identity, corrupted peer bytes and active-source tamper all fail closed; provider/tool starts remain zero. | focused Host Binding/BUS/source-integrity tests plus brownfield alignment/layering and verifier | owner-approved bounded continuation | planner/readiness PASS; prior proposal invalidated by source drift; refresh after live-host smoke |
| `SWU-ACI-PROTOCOL-COMPILATION-001` | [TASK-PROTOCOL-COMPILATION](work-pack/tasks/TASK-PROTOCOL-COMPILATION.md) | Implement the exact ACI-PG-001 candidate compiler and optional artifact-only persistence seam. | accepted ACI-PG-001, reviewed protocol contract and refreshed digest pins | nine exact paths: five functional/test paths plus the four-file Stage-E integrity chain | T-ACI-PC1–PC12 pass; exact compiled/required-unsupported bytes; no confirmation, runtime or provider path | 13 focused tests, 131 runtime tests, Stage-E addendum and two independent PASS re-reviews | owner-authorized exact adjunct | complete for bounded SWU |

All runtime SWUs except the accepted `SWU-ACI-APT-VS-001`, exact
`SWU-ACI-BUS-DELIVERY-001` and exact Phase-A repair
`SWU-ACI-HOST-BUS-INTEGRITY-001` remain unselected. Local-pilot serving is operative only on
`127.0.0.1`; provider/tool execution, TASK-020 materialization, external networking and production
cutover remain blocked. `SWU-ACI-008` cannot be selected before Phase-A completion and
`ACI-005`/`opening.verified`.

## Blockers

| Blocker | Scope | Description | Owner | Next action |
|---|---|---|---|---|
| B-001 | closed | ADR-001 plus ADR-002, exact profiles, executable fixtures and the named descriptor passed independent Stage-A review cycle 5/5. | architecture owner | Runtime crash evidence remains an implementation-exit obligation. |
| B-002 | closed | Fixed decision, terminal, snapshot and compatibility contracts plus golden trace passed independent Stage-A review cycle 5/5. | product/protocol owner | Preserve the frozen trace and exact profile bindings during implementation. |
| B-003 | W0 contract frozen; physical proof blocked | Bundle schema, historical-drift disposition, guard algorithm and named tests passed W0 review. No host/process/ACL/cutover claim exists. | engine owner | TASK-020 later supplies process/ACL/inventory/bypass evidence before any materializer or cutover. |
| B-004 | Invoke process | `.claude/skills/invoke/plan.md` referenced by the local skill is absent. | Invoke package owner | Treat this plan as template-based fallback; repair/regenerate skill separately. |
| B-005 | Slice 1+ | Slice-specific open questions in README section 17 require ADRs before their wave. | wave owner | Resolve in each wave's entry gate; do not pull them into W0. |
| B-PG-001 | closed | The audited nine-path scope, readiness inputs, Stage-E pins, append-only receipt addendum and external receipt digest are current. | protocol work-pack owner | Preserve the bounded authority ceiling; open a new governed SWU for any registry or downstream runtime work. |
| B-CVR-001 | Canonical vault reads | Coordinated five-entry packet and owner/root acceptance do not exist; proposed per-SWU predicate is non-operative. | architecture + product/protocol + host/operator + root owners | Accept ADR/spec/tests/task plus selected deterministic descriptor; preserve global integration blocks. |
| B-CVR-002 | CVR guard bootstrap | GUARD-001 and external trusted bootstrap evidence do not exist. | root/authority owner | Issue one exact bootstrap auth/claim and write only `implementations/vault_read_guard/` plus tests. |
| B-CVR-003 | CVR execution authority | No content-addressed authorization/claim/ExecutionReceipt exists. | root + external bootstrap finalizer/common guard owner | Materialize exactly three artifacts; external finalizer alone completes GUARD, common guard alone completes CVR-001/002, and root never writes receipts. |
| B-CVR-004 | CVR external trust boundary | Workspace hashes do not authenticate principals, trusted time/nonces or executor/finalizer identity. | host authority provider + root/operator | Supply versioned trust policy, reproducible repository binding, one-shot external AuthorityLaunchContext and target-filesystem CAS evidence before authorization. |

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
| Hidden acceptance-critical gaps | pass for W0 | Independent Stage-A review closed W0 gaps; runtime evidence and physical cutover proof remain explicit downstream gates. |
| Deferred complexity | pass | Real providers, generic recipes, distributed workers and rich memory are assigned to later layers. |
| Navigation to first unit | pass | Review the W0 closure packet, then authorize only `SWU-ACI-APT-VS-001`. |

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
  are frozen for the exact selected SWU; local serving and physical cutover stay blocked.

## Gate checks

1. W0 may edit planning/ADR artifacts while `workPackGateStatus = block`; no runtime code may start.
2. Promote mutation entry only for the exact `SWU-ACI-APT-VS-001` descriptor when B-001/B-002 are
   independently closed, B-003's W0 contract is independently frozen, the four profiles and
   storage policy pass, APT TASK-105 is accepted and the root receipt binds every digest. Keep
   local serving separate and materializer/cutover blocked until TASK-020 physical evidence.
3. Select exactly one SWU before each mutation-capable handoff.
4. Parallel SWUs require disjoint write scopes or an explicit merge owner.
5. A failed slice falsifier stops promotion; later waves do not compensate for it.
6. Any change to audit-ledger writes must satisfy the engine constitution and retain the current
   appender as sole physical writer.
7. Every completed SWU returns an execution receipt: files touched, validation results, state/event
   hashes where applicable, unresolved blockers and next handoff.
8. `cvrImplementationGateStatus=approval_packet_prepared` is non-pass. The proposed per-SWU branch
   remains non-operative until the five-entry packet is accepted. Order is
   `000 -> GUARD-001 -> 001 -> 002`; no integration surface is included.
9. Future execution state consists only of content-addressed `authorization.json`, `claim.json`
   and authority-owned `execution-receipt.json`. Descriptors are fixed governance entries. There
   is no current pointer, revocation artifact, ClaimReceipt or second receipt; host enforcement is
   advisory rather than sandboxing.

## Required links

- [Application discovery](discovery/feature-discovery/agents-communication-infra.md)
- [External Tool Adoptions](discovery/external-tool-adoption/external-tool-adoptions.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)
- [Execution pack](EXECUTION-PACK.md)
- [Shared context](work-pack/shared/context.md)
- [Cross-task decisions](work-pack/shared/cross-task-decisions.md)
- [Cross-task gaps](work-pack/shared/cross-task-gaps.md)
- [Traceability](work-pack/shared/traceability.md)
- [Shared SWU manifest](work-pack/shared/swu-manifest.md)
- [Wave W0](work-pack/waves/W0.md)
- [Task TASK-000](work-pack/tasks/TASK-000.md)
- [Task TASK-CVR](work-pack/tasks/TASK-CVR.md)

## Change log

| Date | Change | Author |
|---|---|---|
| 2026-07-23 | Added the prepared, non-pass CVR ApprovalPacket lane and exact SWU contracts while preserving both global runtime blocks. | controlled documentation writer |
| 2026-07-21 | Ratified ETD-1–ETD-7, added canonical-contract/provider-admission/sole-writer evidence gates and retained runtime block. | DomainSpec spec writer |
| 2026-07-21 | Linked the pipeline-visible application discovery as the authority source for DomainSpec authoring. | Codex / discovery-writing |
| 2026-07-21 | Initial detailed migration work-pack. | Codex / Invoke fallback |
