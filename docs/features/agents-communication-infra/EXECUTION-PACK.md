---
module: agents-communication-infra
version: current
status: draft
updatedAt: 2026-07-23
docType: execution-pack
---

# Execution Pack: Agents Communication Infra

## Planning control

| Field | Value |
|---|---|
| `planningGateStatus` | **W0 PASS — independent review cycle 5/5** |
| `mutationTestAuthorization` | **pass_for_exact_swu** — only `SWU-ACI-APT-VS-001` |
| `protocolCompilationPlanningGate` | **pass_for_exact_swu** — only `SWU-ACI-PROTOCOL-COMPILATION-001`; independent L0 adjunct, not W6/L3 promotion |
| `protocolCompilationReadiness` | **pass_for_exact_swu** — refreshed descriptor/context/test pins and bounded implementation verification |
| `localPilotServeEnablement` | **block** — separate post-implementation gate |
| `productionEnablement` | **block** |
| `specAuthoringGateStatus` | **pass** — W0 DomainSpec contracts only; runtime remains blocked |
| `complexity` | high |
| `baselineWave` | W0 |
| `activePlanRef` | [W0](work-pack/waves/W0.md) |
| `workPackManifest` | [WORK-PACK.md](WORK-PACK.md) |
| `layeringArtifact` | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| `activeLayerWindow` | L0 |
| `lastPlannedAt` | 2026-07-23 |
| `readinessProfile` | pilot |

## Wave status board

| Wave | Objective | Entry gate | Exit gate | Status | Evidence target |
|---|---|---|---|---|---|
| [W0](work-pack/waves/W0.md) | Freeze Slice-0 authority and protocol contracts. | Plan exists. | Digest-bound independent PASS over ADRs, fixtures, profiles, storage policy and exact descriptor. | completed; PASS | W0 closure packet and reviewer receipt |
| [W1](work-pack/waves/W1.md) | Prove one deterministic replayable run. | Exact mutation receipt, not a global W0 promotion. | Named-SWU test matrix passes. | ready for exact `SWU-ACI-APT-VS-001` only | state hashes, artifact/ledger receipts, fault matrix |
| [W2](work-pack/waves/W2.md) | Prove sealing, recovery and realtime. | W1 pass and Slice-1 ADRs. | S-002 tests pass. | blocked | ACL/race/reconnect/reconciliation evidence |
| [W3](work-pack/waves/W3.md) | Prove one real adapter safely. | W2 pass and adapter ADRs. | S-003 conformance passes. | blocked | adapter and security receipts |
| [W4](work-pack/waves/W4.md) | Decide product value. | W3 pass and preregistration. | continue, simplify or stop decision. | blocked | blinded evaluation report |
| [W5](work-pack/waves/W5.md) | Prove provider portability. | W4 continue. | mixed-provider conformance passes. | blocked | capability matrix and mixed trace |
| [W6](work-pack/waves/W6.md) | Prove composition and migrate clients. | W5 pass and recipe ADRs. | S-006 passes without kernel specialization. | blocked | recipe/handoff/cutover receipts |
| [W7](work-pack/waves/W7.md) | Close and audit pilot. | W6 pass. | verification and audits pass or remediation is created. | blocked | closure reports |
| PG adjunct | Implement the bounded non-authoritative candidate compiler. | ACI-PG-001 and normative review PASS; refreshed exact-SWU readiness receipt. | T-ACI-PC1–PC12 plus independent verification pass. | complete for bounded SWU; 131 runtime tests and two re-reviews PASS | nine-path diff, exact fixture bytes, Stage-E addendum and verifier verdict |

## Delivery-stage coverage

| Stage | Required | Wave | Status | Evidence / rule |
|---|---|---|---|---|
| discover | yes | W0 | complete for named slice | Current-state anchors and strict seam inventory. |
| design-baseline | yes | W0 | complete | ADR-001 and the ADR-002 Stage-A corpus passed digest-bound review. |
| specification | yes | W0-W6 | complete for named slice | Exact descriptor, profiles, commands/events and gates frozen. |
| scenarios | yes | W1-W6 | not-started | Golden traces and failure scenarios. |
| tests | yes | W1-W7 | not-started | Tests precede or accompany each implementation SWU. |
| implementation | yes | W1-W6 | ready for exact named SWU only | `SWU-ACI-APT-VS-001` may mutate only its descriptor-bound scope; all other implementation remains blocked. |
| protocol-governance adjunct | yes | independent L0 adjunct | complete for bounded SWU | `SWU-ACI-PROTOCOL-COMPILATION-001` remains independent of W6 and historical `ACI-030`; Stage-E repinning adds no runtime authority. |
| interface-experience | yes | W2/W6 | blocked | Runtime SSE first; command UI/client cutover last. |
| telemetry-spec | yes | W1-W3 | not-started | Correlation IDs, state hashes and resource observations. |
| telemetry-instrument | yes | W1-W3 | not-started | Journal/projection/adapter instrumentation. |
| telemetry-verify | yes | W1-W7 | not-started | Replay and receipt assertions. |
| deployment | no | later | skipped | MVP is local single-host; packaging is outside Slices 0-4. |
| concept-index-sync | yes | W7 | not-started | Update feature index/README claims only after evidence. |
| readiness-review | yes | W7 | not-started | TASK-VERIFY. |
| completion-verify | yes | W7 | not-started | TASK-VERIFY. |
| audit-alignment | yes | W7 | not-started | TASK-AUDIT-ALIGNMENT. |
| audit-layering | yes | W7 | not-started | TASK-AUDIT-LAYERING. |

## Dependency and synchronization rules

1. Waves are sequential because each unlocks a distinct architectural decision.
2. Within a wave, test/schema SWUs may run in parallel only when their write scopes are disjoint.
3. Persistence schema, event vocabulary and reducer transitions have a single merge owner in W1.
4. The audit-ledger appender is never edited concurrently with materializer integration work.
5. W4 is a decision wave: `simplify` or `stop` supersedes W5/W6 rather than marking them failed.
6. Task and SWU status is updated in `WORK-PACK.md` and the relevant task file in the same planning
   change that records an execution receipt.
7. The Protocol Governance adjunct runs `alignment-audits` (two independent auditors), then one
   coder, then one verifier. The coder cannot start while its readiness receipt is stale.
8. This adjunct cannot satisfy a W6 entry/exit gate, promote L3/L4, or authorize confirmation,
   runtime commands/events, providers, tools, scheduling, routes or production use.

## Decision lock summary

| Decision | Status | Selected option | Source |
|---|---|---|---|
| D-001 | locked | Keep this work under `agents-communication-infra`; do not create a duplicate runtime feature. | Feature README sections 2-4 and 12 |
| D-002 | locked | Use incremental migration with fake adapters before real providers. | Feature README section 12 |
| D-003 | locked | Event journal governs workflow; audit ledger remains high-level authorization/outcome authority. | Feature README section 9 |
| D-004 | locked | Current validated appender remains sole physical audit-ledger writer. | Engine constitution EG-1 |
| D-005 | locked | MVP is single-host/single-tenant; distributed infrastructure is deferred. | Feature README sections 1.1 and 12 |
| D-006 | proposed | Implement runtime package beside the existing FastAPI reader under `implementations/server/runtime/`. | This plan; confirm in W0 |
| D-007 | locked | Python/FastAPI remains the host; Pydantic validates but runtime-owned canonical bytes/digests define acceptance. | External Tool Adoptions ETD-1/ETD-2 |
| D-008 | locked | First real provider is a repository-local subprocess behind `SandboxLauncher`; Octopus/Eve remain outside the kernel. | External Tool Adoptions ETD-3/ETD-4 |
| D-009 | locked | PydanticAI is deferred, Zod is derived-boundary-only, and lint alone cannot prove EG-1. | External Tool Adoptions ETD-5–ETD-7 |
| D-010 | locked | W0 specifies the sole-writer evidence contract; TASK-020 supplies complete target-host proof before materializer cutover, without blocking TASK-010 journal work. | B-003 / D-012 |
| D-011 | locked | Candidate publication becomes official only through atomic parent verification and a unique `messages` fact. | ADR-002 |
| D-012 | locked | Mutation-test, local-pilot serving and production/cutover are three distinct gates. | W0 closure packet |
| D-PG-001 | locked | ACI Protocol Governance owns deterministic compilation only through a non-authoritative candidate/result; the exact SWU is an independent L0 adjunct. | ACI-PG-001 and protocol-compilation normative review |

## Closure obligations

- TASK-VERIFY must evaluate every acceptance and falsification criterion claimed by the pilot.
- TASK-AUDIT-ALIGNMENT must audit authorities, dependency direction and absence of kernel business branches.
- TASK-AUDIT-LAYERING must reject promotion unsupported by prior-layer evidence.
- Any closure `flag` or `block` creates a remediation task; closure findings are never deleted.
