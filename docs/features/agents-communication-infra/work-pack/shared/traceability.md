# Traceability Matrix

| Requirement/invariant | Task | Primary evidence |
|---|---|---|
| Explicit human confirmation | TASK-000, TASK-030, TASK-080 | command fixtures and legacy-client cutover test |
| Opening verified before any external effect | TASK-020, TASK-030 | crash-boundary and negative execution tests |
| One validated physical writer per authority (EG-1) | TASK-000, TASK-020, TASK-AUDIT-ALIGNMENT | sole-writer guard and materializer receipt |
| Strict write, lenient historical read (EG-2/EG-6) | TASK-020 | golden legacy/appender fixtures |
| Command idempotency and CAS | TASK-010 | duplicate/conflicting-key/concurrency tests |
| Pure deterministic replay | TASK-010, TASK-030 | stable state hashes and no-effect replay spies |
| One logical result and terminal winner | TASK-030, TASK-040 | duplicate/race traces |
| Sealing until reveal | TASK-040 | cross-surface ACL matrix |
| Realtime is projection | TASK-040 | cursor/gap/rebuild tests |
| Adapter is provider-independent | TASK-050, TASK-070 | shared conformance suite |
| Product value justifies complexity | TASK-060 | preregistration and blinded evaluation decision |
| Recipes do not specialize kernel | TASK-080, TASK-AUDIT-ALIGNMENT | kernel branch audit and two-recipe fixture |
| Layer promotion follows evidence | TASK-AUDIT-LAYERING | promotion audit |

## DomainSpec registry coverage

Coverage was checked by a manual exact-set comparison between the `SPEC.md` Concept Registry and
the primary `## DomainSpec Coverage` assignments in task files. The procedure is reproducible, but
is not claimed as automated while `tools/validate-work-pack-coverage.ts` is absent.

| Primary task | Source aspects | Registry IDs |
|---|---|---:|
| TASK-000 | Domain, Rules | 10 |
| TASK-010 | Domain, Operations, States, Interfaces | 9 |
| TASK-020 | Domain, Workflows, Mappings, Interfaces | 7 |
| TASK-030 | Domain, Operations, Queries, States, Interfaces, Workflows | 19 |
| TASK-040 | Domain, Operations, Queries, Interfaces, Workflows, Mappings | 24 |
| TASK-050 | Domain, Operations, Interfaces, Mappings, Events, Persistence, Rules | 15 |
| **Total** | **All registered source aspects** | **84** |

Result: **84/84 assigned; 0 duplicate primary assignments; 0 gaps**. TASK-060 through TASK-080,
TASK-VERIFY and the audit tasks consume or validate existing contracts and therefore own no
additional Concept Registry ID.

## Concept-to-test / fixture reverse matrix

Every current Concept Registry ID appears exactly once below. Test IDs refer to
[`TEST-SPEC.md`](../../TEST-SPEC.md); named fixtures are defined there or are explicit deferred
evidence obligations. A mapping specifies the contract evidence expected for the concept, not an
implementation pass claim. Runtime execution remains blocked by its independent gates.

| Concept ID | Test / fixture or deferred rationale |
|---|---|
| `agents-communication-infra.ConfirmedDispatch` | T-ACI-R13, T-ACI-R19; frozen-authority fixture |
| `agents-communication-infra.Run` | T-ACI-S1, T-ACI-C2 |
| `agents-communication-infra.Group` | T-ACI-S2, T-ACI-R20 |
| `agents-communication-infra.Seat` | T-ACI-R8, T-ACI-S2 |
| `agents-communication-infra.Attempt` | T-ACI-S3, T-ACI-C4 |
| `agents-communication-infra.Contribution` | T-ACI-R8, T-ACI-R15 |
| `agents-communication-infra.PublicationCandidate` | T-ACI-R15, T-ACI-C4 |
| `agents-communication-infra.EffectIntent` | T-ACI-R6, T-ACI-C1 |
| `agents-communication-infra.Artifact` | T-ACI-R9, T-ACI-R11 |
| `agents-communication-infra.EffectiveInputArtifact` | T-ACI-R9, T-ACI-R17, T-ACI-R18 |
| `agents-communication-infra.RawProviderOutput` | T-ACI-R9, T-ACI-R16 |
| `agents-communication-infra.RevealManifest` | T-ACI-R4, T-ACI-R18, T-ACI-C3 |
| `agents-communication-infra.GroupResult` | T-ACI-S2 |
| `agents-communication-infra.DispatchSpec` | T-ACI-R13, T-ACI-R17; frozen-digest fixture |
| `agents-communication-infra.AgentInvocationPlan` | T-ACI-R17, T-ACI-R20 |
| `agents-communication-infra.MaterializedAgentInvocation` | T-ACI-R17 |
| `agents-communication-infra.AgentExecutionRequest` | T-ACI-R17, T-ACI-R19 |
| `agents-communication-infra.BusPublication` | T-ACI-R2, T-ACI-R3, T-ACI-P1 |
| `agents-communication-infra.PublicationReceipt` | T-ACI-R3, T-ACI-R16, T-ACI-P1 |
| `agents-communication-infra.AgentTerminalResult` | T-ACI-R16, T-ACI-C4 |
| `agents-communication-infra.EffectiveInputEntry` | T-ACI-R18 |
| `agents-communication-infra.ResourceBudget` | T-ACI-R19 |
| `agents-communication-infra.SandboxPolicy` | T-ACI-R19; target-host negative fixtures remain runtime-gated |
| `agents-communication-infra.ExecutionAuthorityFence` | T-ACI-R19, T-ACI-R20 |
| `agents-communication-infra.RuntimeCommand` | T-ACI-R5, T-ACI-R6, T-ACI-R20 |
| `agents-communication-infra.RuntimeEventEnvelope` | T-ACI-R6, T-ACI-R7 |
| `agents-communication-infra.AggregateVersion` | T-ACI-R5, T-ACI-R7 |
| `agents-communication-infra.JournalOffset` | T-ACI-R3, T-ACI-R7 |
| `agents-communication-infra.ContentDigest` | T-ACI-R5, T-ACI-R9, T-ACI-R17 |
| `agents-communication-infra.ArtifactId` | T-ACI-R9, T-ACI-R18 |
| `agents-communication-infra.SeatId` | T-ACI-R8, T-ACI-S2 |
| `agents-communication-infra.VersionedReference` | T-ACI-R9, T-ACI-R16, T-ACI-R17 |
| `agents-communication-infra.ManifestEntry` | T-ACI-R4, T-ACI-R18 |
| `agents-communication-infra.ExecutionAuthorityMode` | T-ACI-R19; legacy/runtime cutover fixture |
| `agents-communication-infra.ReconciliationState` | T-ACI-C2 |
| `agents-communication-infra.RetryClass` | T-ACI-S3, T-ACI-C4 |
| `agents-communication-infra.EffectStatus` | T-ACI-C1, T-ACI-C4 |
| `agents-communication-infra.ArtifactClassification` | T-ACI-R11, T-ACI-R18 |
| `agents-communication-infra.AcceptRuntimeCommand` | T-ACI-R5, T-ACI-R6 |
| `agents-communication-infra.ConfirmRuntimeDispatch` | T-ACI-R13, T-ACI-R19; server-resolution fixture |
| `agents-communication-infra.StartAgentAttempt` | T-ACI-R17, T-ACI-R19, T-ACI-R20 |
| `agents-communication-infra.PublishBusContribution` | T-ACI-R2, T-ACI-R3, T-ACI-R15, T-ACI-P1 |
| `agents-communication-infra.VerifyPublicationReceipt` | T-ACI-R3, T-ACI-R16 |
| `agents-communication-infra.CloseCollection` | T-ACI-R4, T-ACI-C3 |
| `agents-communication-infra.PublishRevealManifest` | T-ACI-R4, T-ACI-R18, T-ACI-C3 |
| `agents-communication-infra.CommitGroupResult` | T-ACI-S2 |
| `agents-communication-infra.CancelRun` | T-ACI-S1, T-ACI-S3, T-ACI-R20 |
| `agents-communication-infra.RecordUsageObservation` | T-ACI-R12 |
| `agents-communication-infra.GetRuntimeProjection` | T-ACI-R7; cursor/gap/rebuild fixture |
| `agents-communication-infra.GetRunStatus` | T-ACI-S1; projection-lag fixture |
| `agents-communication-infra.GetVisibleGroupMessages` | T-ACI-R4, T-ACI-R18 |
| `agents-communication-infra.RunLifecycle` | T-ACI-S1 |
| `agents-communication-infra.GroupLifecycle` | T-ACI-S2 |
| `agents-communication-infra.AttemptLifecycle` | T-ACI-S3 |
| `agents-communication-infra.EventJournal` | T-ACI-R1, T-ACI-R5, T-ACI-R6, T-ACI-R7 |
| `agents-communication-infra.AgentAdapter` | T-ACI-R10, T-ACI-R16, T-ACI-R17 |
| `agents-communication-infra.DeliberationBus` | T-ACI-R2, T-ACI-R3, T-ACI-R4, T-ACI-R15 |
| `agents-communication-infra.RuntimeCommandAPI` | T-ACI-R5, T-ACI-R13; HTTP command fixture |
| `agents-communication-infra.AgentToolGateway` | T-ACI-R2, T-ACI-R4, T-ACI-P1 |
| `agents-communication-infra.ArtifactBoundary` | T-ACI-R9, T-ACI-R11, T-ACI-R18 |
| `agents-communication-infra.SandboxLauncher` | T-ACI-R19; target-host negative fixtures remain runtime-gated |
| `agents-communication-infra.AuditLedgerAppenderPort` | T-ACI-R1, T-ACI-C2 |
| `agents-communication-infra.RunExecutionWorkflow` | T-ACI-S1, T-ACI-C1, T-ACI-C2 |
| `agents-communication-infra.GroupDeliberationWorkflow` | T-ACI-R4, T-ACI-S2, T-ACI-C3 |
| `agents-communication-infra.ReceiptGatedPublicationWorkflow` | T-ACI-R3, T-ACI-R15, T-ACI-R16, T-ACI-C4 |
| `agents-communication-infra.AuditLedgerMaterializer` | T-ACI-R1, T-ACI-R13, T-ACI-C2 |
| `agents-communication-infra.ExternalEffectReconciliationWorkflow` | T-ACI-S3, T-ACI-C1, T-ACI-C4 |
| `agents-communication-infra.ExecutionAuthorityCutoverWorkflow` | T-ACI-R19; legacy/runtime cutover fixture |
| `agents-communication-infra.AgentInvocationPlanToMaterializedInvocation` | T-ACI-R17 |
| `agents-communication-infra.RawProviderOutputToCanonicalObservations` | T-ACI-R10, T-ACI-R12, T-ACI-R16 |
| `agents-communication-infra.BusPublicationToContribution` | T-ACI-R2, T-ACI-R15 |
| `agents-communication-infra.RevealManifestToEffectiveInput` | T-ACI-R4, T-ACI-R18 |
| `agents-communication-infra.FrozenAuthorityToAuditLedgerRow` | T-ACI-R13, T-ACI-C2 |
| `agents-communication-infra.RuntimeTerminalToExitReason` | T-ACI-S1 |
| `agents-communication-infra.UsageObservationToRollups` | T-ACI-R12 |
| `agents-communication-infra.UsageObservation` | T-ACI-R12 |
| `agents-communication-infra.PricingSource` | T-ACI-R12; incompatible-price and version-source fixture |
| `agents-communication-infra.UsageRollup` | T-ACI-R12; nullable-counter and source-offset fixture |
| `agents-communication-infra.CostCalculation` | T-ACI-R12; missing/incompatible pricing keeps cost unknown |
| `agents-communication-infra.SoleWriterEvidenceBundle` | T-ACI-ETA5; W0 schema/component fixtures and TASK-020 complete target-host proof |
| `agents-communication-infra.ExternalToolAdoptionPolicy` | T-ACI-ETA1 |
| `agents-communication-infra.CanonicalContractPolicy` | T-ACI-ETA2 |
| `agents-communication-infra.BoundaryValidationPolicy` | T-ACI-ETA3 |
| `agents-communication-infra.ProviderAdapterAdmissionGate` | T-ACI-ETA4 |

## Slice falsifiers

- **L0:** any execution before verified opening, replay-triggered effect, duplicate logical effect,
  non-convergent crash boundary or divergent ledger row treated as success.
- **L1:** sealed content visible before reveal, two terminal winners, unrecoverable SSE gap or hidden
  projection failure.
- **L2:** provider-specific state leaks into kernel, unknown effect presented as success, credential
  leak or unbounded resource consumption.
- **L3:** second provider requires kernel/schema fork, or product-value threshold fails.
- **L4:** adding `research`/`review` requires business-type branches in kernel, or skill/UI retain a
  parallel execution authority after cutover.
