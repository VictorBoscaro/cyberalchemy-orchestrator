---
module: agents-communication-infra
version: current
status: draft
updatedAt: 2026-07-21
docType: execution-pack
---

# Execution Pack: Agents Communication Infra

## Planning control

| Field | Value |
|---|---|
| `planningGateStatus` | **block** — W0 decisions only |
| `specAuthoringGateStatus` | **pass** — W0 DomainSpec contracts only; runtime remains blocked |
| `complexity` | high |
| `baselineWave` | W0 |
| `activePlanRef` | [W0](work-pack/waves/W0.md) |
| `workPackManifest` | [WORK-PACK.md](WORK-PACK.md) |
| `layeringArtifact` | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) |
| `activeLayerWindow` | L0 |
| `lastPlannedAt` | 2026-07-21 |
| `readinessProfile` | pilot |

## Wave status board

| Wave | Objective | Entry gate | Exit gate | Status | Evidence target |
|---|---|---|---|---|---|
| [W0](work-pack/waves/W0.md) | Freeze Slice-0 authority and protocol contracts. | Plan exists. | Slice-0 OQs plus Pydantic/canonical vectors accepted; EG-1 bundle schema, drift disposition, guard spec and named tests frozen; plan gate promoted for TASK-010 only. | not-started | ADRs, schema, canonical vectors, transition, crash and sole-writer guard test specifications |
| [W1](work-pack/waves/W1.md) | Prove one deterministic replayable run. | W0 pass. | S-001 tests and falsifiers pass. | blocked | state hashes, ledger receipts, fault matrix |
| [W2](work-pack/waves/W2.md) | Prove sealing, recovery and realtime. | W1 pass and Slice-1 ADRs. | S-002 tests pass. | blocked | ACL/race/reconnect/reconciliation evidence |
| [W3](work-pack/waves/W3.md) | Prove one real adapter safely. | W2 pass and adapter ADRs. | S-003 conformance passes. | blocked | adapter and security receipts |
| [W4](work-pack/waves/W4.md) | Decide product value. | W3 pass and preregistration. | continue, simplify or stop decision. | blocked | blinded evaluation report |
| [W5](work-pack/waves/W5.md) | Prove provider portability. | W4 continue. | mixed-provider conformance passes. | blocked | capability matrix and mixed trace |
| [W6](work-pack/waves/W6.md) | Prove composition and migrate clients. | W5 pass and recipe ADRs. | S-006 passes without kernel specialization. | blocked | recipe/handoff/cutover receipts |
| [W7](work-pack/waves/W7.md) | Close and audit pilot. | W6 pass. | verification and audits pass or remediation is created. | blocked | closure reports |

## Delivery-stage coverage

| Stage | Required | Wave | Status | Evidence / rule |
|---|---|---|---|---|
| discover | yes | W0 | in-progress | Current-state anchors in shared context. |
| design-baseline | yes | W0 | not-started | Accepted ADRs and frozen contracts. |
| specification | yes | W0-W6 | not-started | Versioned event, command, adapter and recipe schemas per slice. |
| scenarios | yes | W1-W6 | not-started | Golden traces and failure scenarios. |
| tests | yes | W1-W7 | not-started | Tests precede or accompany each implementation SWU. |
| implementation | yes | W1-W6 | blocked | Starts only after W0 pass. |
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

## Closure obligations

- TASK-VERIFY must evaluate every acceptance and falsification criterion claimed by the pilot.
- TASK-AUDIT-ALIGNMENT must audit authorities, dependency direction and absence of kernel business branches.
- TASK-AUDIT-LAYERING must reject promotion unsupported by prior-layer evidence.
- Any closure `flag` or `block` creates a remediation task; closure findings are never deleted.
