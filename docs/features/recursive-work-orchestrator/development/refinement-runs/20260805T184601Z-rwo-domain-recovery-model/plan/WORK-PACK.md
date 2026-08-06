---
module: rwo-recovery-decision-contract
version: candidate-2
status: draft
updatedAt: 2026-08-05
docType: work-pack
---

# WORK-PACK: RWO Recovery Decision Contract

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | The L0 frontier is structurally ready; owner-blocked later SWUs remain non-routable. |
| complexity | high | Persistence, concurrency, three owner seams, and later promotion are distinct. |
| outputMode | split | Tasks and waves are separate executable contracts. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required split choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0–L3 decision boundaries. |
| dispatchTechniqueTrace | below | Only techniques affecting boundaries/gates are cited. |
| distillValidationStatus | pass | All SWUs are one behavior; first unit is narrowest. |
| swuAtomicityStatus | pass | Split analysis is recorded below and in task files. |
| firstUnitNarrownessStatus | pass | SWU-RRD-001 changes no lifecycle semantics or storage. |
| closeoutSyncStatus | pass | Every mutation-capable SWU has an exact closeout row. |
| admissionTiming | selected-unit-at-task-session | One SWU is admitted at a time. |
| executionEntryState | selection-ready | No SWU is selected or executing in this Refine run. |
| allowedRoutesDigest | `sha256:7370bedb4e73630fbfcfb576297a303073c01e67fef5eaae5ac921a73f74ede6` | Canonical digest of `allowed-routes.json.routes`. |
| activeLayerWindow | L0 | Pure candidate contract only. |
| lastUpdatedAt | 2026-08-05T20:01:13Z | Planning snapshot. |
| readinessProfile | pilot | Target profile only; no pilot readiness claim. |

## Work-Pack Execution Policy

```yaml
executionPolicy:
  routePolicy: automatic-in-scope
  allowedRoutesRef: allowed-routes.json
  allowedRoutesDigest: sha256:7370bedb4e73630fbfcfb576297a303073c01e67fef5eaae5ac921a73f74ede6
  automaticDecisions:
    - internal-tool-selection
    - capability-owner-routing
    - reversible-local-default
    - declared-fallback
    - declared-retry
    - fresh-task-session-resumption
  stopDecisions:
    - product-or-semantic-choice
    - scope-expansion
    - destructive-or-irreversible-effect
    - credentials-or-secret-access
    - external-message-or-network-effect
    - cost-policy-or-risk-acceptance
    - authority-promotion-publication-deployment
    - failed-acceptance-critical-validation
  scopeSource: exact-work-pack-and-selected-swu
  validationPolicy: owner-gates-remain-mandatory

executionEntry:
  state: selection-ready
  selectedUnit: null
  routeId: null
  nextOwner: implementation-readiness:execute

preExecutionOwnerPrerequisite: null
```

`declared-retry` has only the Work-Pack infrastructure meaning: one unchanged
owner-route retry after `REPAIRABLE_OWNER_CONDITION`. It is not an RWO recovery
disposition, does not consume a recovery counter, and cannot authorize any
external effect.

## Objective Summary

- Objective: implement and falsify the candidate-2 recovery decision contract
  in ordered layers, stopping at every unresolved owner boundary.
- Primary inputs: Stage 08 exact model and scenario matrix; existing canonical
  and journal implementation anchors.
- Active L0 success: deterministic canonical IDs, closed case admission,
  single-valued classification, and exact identity transitions pass executable
  fixtures without persistence, ARE, or adapter calls.
- Full-plan success: L1/L2 owner contracts and evidence exist, and L3 receives a
  separate promotion decision. Full success is not required to begin L0.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | baseline and source bindings captured | L0 | [W0](work-pack/waves/W0.md) | none | live hashes/import/test baseline |
| S-001 | pure exact model executable | L0 | [W1](work-pack/waves/W1.md) | S-000 | canonical, schema, classifier, identity tests |
| S-002 | accepted-history behavior proven | L1 | [W2](work-pack/waves/W2.md) | S-001, G1 owner admission for 006 | concurrency/restart/crash tests |
| S-003 | owner seams conform or fail closed | L2 | [W3](work-pack/waves/W3.md) | S-002, G1/G2/G3 | owner-substitution and zero-effect tests |
| S-004 | ontology candidate reviewed and closure evidence assembled | L3 | [W4](work-pack/waves/W4.md) | S-003, G4 | ontology validators plus complete regression |

## Task Status Board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) | executable pure contract | L0 | W0, W1 | ready | not-started |
| [TASK-FRONTIER](work-pack/tasks/TASK-FRONTIER.md) | cross-case reduction and atomic acceptance | L1 | W2 | 005 ready after L0; 006 owner-prerequisite | not-started |
| [TASK-INTEGRATIONS](work-pack/tasks/TASK-INTEGRATIONS.md) | domain, effect, and optional ARE seams | L2 | W3 | blocked by G1/G2/G3 individually | not-started |
| [TASK-GOVERNANCE](work-pack/tasks/TASK-GOVERNANCE.md) | evidence-backed ontology proposal | L3 | W4 | blocked by G4 and prior layers | not-started |
| TASK-VERIFY | regression, alignment, and claim-ceiling closeout | L3 | W4 | ready-after-mutation | not-started |

## SWU Manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope summary | Validation | Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-RRD-001 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) | domain-separated canonical recovery IDs | W0 | canonical wrapper, one test, golden vectors | targeted unittest + vector digest check | local-fallback | ready; recommended first |
| SWU-RRD-002 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) | closed case admission | 001 | case schema/validator/fixtures | valid union + invalid combination tests | local-fallback | ready-after-001 |
| SWU-RRD-003 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) | single-valued pure classification | 002 | classifier/test/fixtures | all 20 games + overlap/totality negatives | local-fallback | ready-after-002 |
| SWU-RRD-004 | [TASK-CONTRACT](work-pack/tasks/TASK-CONTRACT.md) | exact identity transitions and stable intents | 003 | identity/test/fixtures | transition matrix and idempotency tests | local-fallback | ready-after-003 |
| SWU-RRD-005 | [TASK-FRONTIER](work-pack/tasks/TASK-FRONTIER.md) | subject-scoped frontier inhibition | 004 | frontier/test/fixtures | competing-case and consumed-trigger reducer tests | local-fallback | ready-after-004 |
| SWU-RRD-006 | [TASK-FRONTIER](work-pack/tasks/TASK-FRONTIER.md) | atomic validation-vector acceptance | 005 + G1 | acceptance/journal/database/schema/test | two-writer, revocation, crash-window, restart | local-fallback | owner-prerequisite |
| SWU-RRD-007 | [TASK-INTEGRATIONS](work-pack/tasks/TASK-INTEGRATIONS.md) | admitted domain signal and policy handles | 005 + G1 | two contracts/domain/test | forged owner/mapping/policy negatives | manual | blocked-owner |
| SWU-RRD-008 | [TASK-INTEGRATIONS](work-pack/tasks/TASK-INTEGRATIONS.md) | exact-effect retry and bounded reconciliation handles | 006 + G2 | effect contracts/module/test | unknown zero-retry + permit/budget tests | manual | blocked-owner |
| SWU-RRD-009 | [TASK-INTEGRATIONS](work-pack/tasks/TASK-INTEGRATIONS.md) | optional admitted ARE receipt binding | 007 + G3 | semantic binding/module/test | raw-output rejection and zero-call path | manual | blocked-owner |
| SWU-RRD-010 | [TASK-GOVERNANCE](work-pack/tasks/TASK-GOVERNANCE.md) | candidate ontology delta from executable evidence | 006–009 + G4 | current ontology targets only after owner admission | graph build/validation and evidence refs | manual | blocked-promotion |

## SWU Atomicity Review

| SWU | Candidate split considered | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| 001 | wrapper vs vectors | neither proves canonical identity without the other | pass |
| 002 | schema vs validator | one admission behavior requires structural and executable rejection evidence | pass |
| 003 | tables by case kind | totality/non-overlap is the independent acceptance boundary | pass |
| 004 | each disposition transition | cross-disposition preservation/allocation collision is the behavior under test | pass |
| 005 | reducer vs inhibition rules | actionable trigger selection is incomplete without blocker computation | pass |
| 006 | validation compare vs atomic append | splitting would leave the unsafe crash window the SWU exists to close | pass |
| 007 | signal vs policy | both are required to prove the domain-to-case admitted boundary | pass |
| 008 | effect retry vs reconciliation | their mutual exclusion is the safety behavior | pass |
| 009 | ARE entry vs mapping reference | admission boundary is only proven end-to-end across both | pass |
| 010 | nodes vs relations | graph validity and evidence binding require a recomposable delta | pass |

## First-Unit Narrowness

`SWU-RRD-001` is the narrowest reversible trust-building unit. It reuses the
current canonical payload profile and adds only a domain-separated ID wrapper,
golden vectors, and tests. It makes no schema, lifecycle, storage, ontology,
authority, or external-effect decision. Splitting the wrapper from its vectors
would produce code with no independent identity proof or fixtures with no owner.

## Task Session Closeout Sync Contract

Common baseline rule: record pre-SWU SHA-256 and size for every existing target;
record `absent` for new targets. Allowed deltas are only `source_added`,
`source_changed`, `fixture_added`, `test_added`, `evidence_added`, and
`blocker_opened`. Every receipt must bind exact target inventory, commands,
results, and post-state digests. Any other delta blocks closeout.

| SWU | Lifecycle owner route | Targets | Owner validation | Receipt | Successor |
| --- | --- | --- | --- | --- | --- |
| 001 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l0-canonical.write_scope` | targeted unittest; golden vector digest equality; `git diff --check` | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-001.json` | 002 only |
| 002 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l0-case-contract.write_scope` | targeted unittest; all eight variants; unknown/additional fields reject | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-002.json` | 003 only |
| 003 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l0-classifier.write_scope` | targeted unittest; 20/20 matrix; reason/disposition totality | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-003.json` | 004 only |
| 004 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l0-identity.write_scope` | targeted unittest; allocation/preservation and stable-intent assertions | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-004.json` | 005 only |
| 005 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l1-frontier.write_scope` | targeted unittest; overlapping scope inhibition; consumed trigger absent | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-005.json` | 006 only after G1 |
| 006 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l1-acceptance.write_scope` | targeted plus full runtime tests; two-writer, failpoint, restart; SQLite integrity | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-006.json` | 007 and 008 when owners pass |
| 007 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l2-domain.write_scope` | targeted unittest; admitted owner binding; forged inputs reject | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-007.json` | 009 after G3 |
| 008 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l2-effect.write_scope` | targeted unittest; outcome-unknown has zero retry/effect calls; counter exhaustion | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-008.json` | 010 after other seams |
| 009 | `invoke:refresh:apply-approved` | `allowed-routes.json#rrd-l2-are-aci.write_scope` | targeted unittest; raw ARE rejects; missing optional ARE makes zero calls | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-009.json` | 010 after G4 |
| 010 | ontology owner route, not automatic | `ontology/nodes/nodes.json`; `ontology/relations/relations.json`; `ontology/views/typed-coordinated-work-atlas.json`; `ontology/ontology.json`; `ontology/ONTOLOGY.md`; `ontology/evidence/RECOVERY-DECISION-CONTRACT-CANDIDATE-2.json` | graph builders/validators; source evidence and claim ceilings | `docs/features/recursive-work-orchestrator/development/execution-receipts/SWU-RRD-010.json` | none |

## Blockers

| Blocker | Scope | Description | Owner | Next action |
| --- | --- | --- | --- | --- |
| B-RRD-001 | SWU-006/007 | journal/domain truth reconciliation contract unselected | journal + domain owners | accept exact handles, epochs, and mismatch behavior |
| B-RRD-002 | SWU-008 | exact-effect permit/reconciliation schemas unselected | exact-effect owner | accept attempt identity, nonce, budget, and outcome contract |
| B-RRD-003 | SWU-009 | ARE/ACI executable receipt binding unselected | ARE + ACI owners | provide exact versioned admitted receipt schema |
| B-RRD-004 | SWU-010 | ontology change requires evidence and promotion authority | ontology owner | review executable evidence and candidate delta after L2 |

## Dispatch Technique Trace

| Technique | Applied to | Evidence | Status |
| --- | --- | --- | --- |
| sequence | L0 -> L1 -> L2 -> L3 | waves and dependencies preserve proof order | pass |
| scu_swu_reduction | ten SWUs | each has one independently reviewable behavior | pass |
| recomposition_proof | SWUs -> candidate-2 | traceability table covers every model responsibility | pass |
| validation_loop | every SWU | exact targeted test or owner validator and receipt | pass |
| owner_boundary_check | 006–010 | named blockers prevent owner/promotion substitution | pass |

## Distill Validation

| Check | Result | Evidence |
| --- | --- | --- |
| smallest coherent SWU | pass | 001 is wrapper + inseparable golden proof only |
| atomicity and split analysis | pass | every plausible split and retained boundary is named |
| first-unit narrowness | pass | no lifecycle/storage/owner semantics in 001 |
| recomposition proof | pass | shared traceability maps full model to 001–010 |
| hidden acceptance-critical gaps | pass | G1–G4 are typed blockers with owner routes |
| deferred complexity | pass | persistence, owner seams, ontology remain later layers |
| navigation | pass | first unit is TASK-CONTRACT / SWU-RRD-001 / W1 |

## Gate Checks

- Only one selected SWU may enter Task Session.
- W0 live baseline is mandatory before selection.
- SWU-RRD-006 through 010 cannot run while their named owner gate is unresolved.
- Parallel L2 work requires disjoint write scopes and already accepted owner contracts.
- Current ontology, publication, deployment, or external effects always stop.
- A failed acceptance-critical test stops the current SWU before any successor.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-08-05 | Initial candidate-2 split work-pack | Refine Stage 09 |
