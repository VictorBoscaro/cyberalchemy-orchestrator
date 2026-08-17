---
module: bounded-terminal-output-handoff
version: current
status: draft
updatedAt: 2026-08-16
docType: work-pack
---

# WORK-PACK: Bounded Terminal-Output Handoff

## Control fields

| Field | Value |
| --- | --- |
| workPackGateStatus | block pending HTR-000 |
| complexity | high |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` |
| distillValidationStatus | block pending host-payload proof |
| swuAtomicityStatus | pass after second-pass splits |
| firstUnitNarrownessStatus | pass: HTR-000 |
| closeoutSyncStatus | pass |
| admissionTiming | selected-unit-at-task-session |
| executionEntryState | owner-prerequisite |
| allowedRoutesDigest | `50b1138103df318d8c34fff0645533f7cc0909df63f2a5e10dcfb00a3c07099d` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |

## Objective

Deliver an evidence-preserving lifecycle from exact host-observed subagent output to staged downstream launch, then prove it on the artifact-schema research dispatch. Success requires TOH-001–008, bounded fan-in, no duplicate launch, no premature close, a live three-wave dispatch and required review.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependency | Validation |
| --- | --- | --- | --- | --- | --- |
| S-000 | Prove the real Codex hook payload supplies canonical complete bytes and correlation. | L0 preflight | [W0](work-pack/waves/W0.md) | accepted design | HTR-000 probe receipt |
| S-001 | Host-owned terminal bytes become an attributable immutable receipt. | L0 | [W0](work-pack/waves/W0.md) | S-000 | TOH-001–005 across service/adapter/gate boundaries + live smoke |
| S-002 | One accepted producer unlocks one consumer once. | L1 | [W1](work-pack/waves/W1.md) | S-001 | TOH-006–008 + replay |
| S-003 | Complete ordered fan-in and close authorization are proven separately. | L2 roadmap | [W2](work-pack/waves/W2.md) | new normative version + S-002 | fan-in matrix, then close matrix |
| S-004 | Research and independent review finish as separate dispatches. | L3 roadmap | [W3](work-pack/waves/W3.md) | S-003 | research receipts/artifacts, then review receipt/artifact |

## Task board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-HTR-CAPTURE](work-pack/tasks/TASK-HTR-CAPTURE.md) | Host preflight, runtime byte commit and Codex capture adapter. | L0 | W0 | HTR-000 owner-prerequisite | not started |
| [TASK-HTR-SEQUENTIAL](work-pack/tasks/TASK-HTR-SEQUENTIAL.md) | One authenticated sequential edge. | L1 | W1 | blocked by W0 | not started |
| [TASK-HTR-FANIN](work-pack/tasks/TASK-HTR-FANIN.md) | Bounded fan-in, then an independent close gate. | L2 roadmap | W2 | blocked by normative revalidation | not admitted |
| [TASK-HTR-ROLLOUT](work-pack/tasks/TASK-HTR-ROLLOUT.md) | Live research, then independent review. | L3 roadmap | W3 | blocked by W2 | not admitted |

## SWU manifest

| SWU | Parent | Primary behavior | Dependencies | Write scope summary | Acceptance | Owner | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-ACI-HTR-000 | [CAPTURE](work-pack/tasks/TASK-HTR-CAPTURE.md) | Prove actual host payload canonicality/completeness. | none | one probe receipt | byte/correlation fixtures | task-session | owner-prerequisite |
| SWU-ACI-HTR-001 | [CAPTURE](work-pack/tasks/TASK-HTR-CAPTURE.md) | Atomic byte commit and receipt. | HTR-000 | service + focused tests + pins | TOH-001 + receipt retry | subagent/local fallback | blocked |
| SWU-ACI-HTR-002 | [CAPTURE](work-pack/tasks/TASK-HTR-CAPTURE.md) | Exact proven-field capture and delayed close. | HTR-000, HTR-001 | hook/config + focused tests + pins | synthetic + live exactness | subagent + parent smoke | blocked |
| SWU-ACI-HTR-003 | [SEQUENTIAL](work-pack/tasks/TASK-HTR-SEQUENTIAL.md) | One staged 1→1 handoff/launch. | HTR-002 | compiler/read port/tests + pins | TOH-006–008 | subagent/local fallback | blocked |
| SWU-ACI-HTR-004A | [FANIN](work-pack/tasks/TASK-HTR-FANIN.md) | Ordered complete fan-in and durable launch intent. | new spec + HTR-003 | compiler/service/tests + pins | 3→3→1 fan-in matrix | subagent/local fallback | roadmap |
| SWU-ACI-HTR-004B | [FANIN](work-pack/tasks/TASK-HTR-FANIN.md) | Declared-seat complete-close gate. | HTR-004A | service/hook/tests + pins | no-premature-close matrix | subagent/local fallback | roadmap |
| SWU-ACI-HTR-005 | [ROLLOUT](work-pack/tasks/TASK-HTR-ROLLOUT.md) | Live research pilot. | HTR-004B | `research.md`, `findings.md` | reconciled research run | parent/governed subagents | roadmap |
| SWU-ACI-HTR-006 | [ROLLOUT](work-pack/tasks/TASK-HTR-ROLLOUT.md) | Independent review dispatch. | HTR-005 | `review.md` | reconciled review result | parent/`$review` | roadmap |

## Atomicity review

| SWU | Candidate splits | Why retained | Verdict |
| --- | --- | --- | --- |
| HTR-000 | payload capture / byte fixtures | Both answer one admission predicate and produce no runtime capability. | pass |
| HTR-001 | bytes artifact / terminal transition | Either alone exposes an unauthorized partial fact; one atomic journal acceptance is the behavior. | pass |
| HTR-002 | matcher / extraction / correlation / close | Partial adapter can falsely attribute output; these form one accepting boundary. | pass |
| HTR-003 | read / materialize / stage | None independently proves or authorizes the consumer transition. | pass |
| HTR-004A | group readiness / slot order / durable stage | None independently authorizes the fan-in launch; close is split to HTR-004B. | pass, roadmap |
| HTR-004B | seat inventory / close decision | Together form one close authorization gate, independent of fan-in launch. | pass, roadmap |
| HTR-005 | live research phases / review | Research phases are one dispatch; review is split to HTR-006. | pass, roadmap |
| HTR-006 | review open / verdict / close | One review dispatch and artifact form one independently accepted result. | pass, roadmap |

The first unit, HTR-000, is a reversible evidence-only prerequisite. It can falsify the host seam before any runtime source mutation.

## Task Session closeout synchronization

The common rules are in [CLOSEOUT-CONTRACT.md](work-pack/shared/CLOSEOUT-CONTRACT.md). HTR-000 is an evidence-only owner prerequisite whose preflight receipt is its expected result; it does not enter Task Session closeout. Each mutation-capable admitted SWU uses `baseline.json`, `task-session-receipt.json` and `owner-receipt.json` under `plan/session-evidence/<SWU>/`.

| SWU | Lifecycle owner | Declared target inventory | Baseline | Allowed deltas | Owner validation | Successor |
| --- | --- | --- | --- | --- | --- | --- |
| HTR-001 | `invoke:refresh:apply-approved` | WORK-PACK, CAPTURE task, W0, HTR-001 evidence directory | exact pre-mutation target digests | evidence/status/blocker/route | focused tests + receipt schema | HTR-002 |
| HTR-002 | same | WORK-PACK, CAPTURE task, W0, HTR-002 evidence directory | exact digests | same | hook suite + live smoke | HTR-003 |
| HTR-003 | same | WORK-PACK, SEQUENTIAL task, W1, HTR-003 evidence directory | exact digests | same | 1→1/replay suites | HTR-004 |
| HTR-004A/B, HTR-005/006 | not admitted | requires a new plan projection after normative L2/L3 revalidation | n/a | n/a | n/a | none |

Expected owner receipt: `plan/session-evidence/<SWU>/owner-receipt.json` with owner, source receipt digest, validated targets, admitted deltas, validation result, blockers and eligible successor.

## Execution policy

The machine projection is [EXECUTION-ENTRY.json](EXECUTION-ENTRY.json). Internal task-session and closeout routes are repository-local/reversible. Automatic decisions are limited to tool/owner routing, reversible defaults/fallback, one same-route retry, and fresh Task Session resumption. Semantic choice, scope expansion, destructive/external/secret/cost/authority effects and failed acceptance-critical validation stop.

## Technique trace and Distill

- Full route: [planning-dispatch.json](planning-dispatch.json), validated by Dispatch Spec.
- Human trace: [DISPATCH-TECHNIQUE-TRACE.md](DISPATCH-TECHNIQUE-TRACE.md).
- Distill: [DISTILL-VALIDATION.md](DISTILL-VALIDATION.md), second pass pending.

## Blockers

HTR-000 is a real blocker before runtime mutation. Its failure stops W0 and preserves the fence. L2/L3 are separately blocked by the current design-version boundary; their roadmap rows grant no execution route.

## Gate checks

Runtime mutation remains blocked until: HTR-000 passes, Distill is refreshed to pass, the execution entry is reclassified to selection-ready, HTR-001 is explicitly selected by Implementation Readiness, and Task Session creates its execution-time context/baseline pack. Structural validators passing does not satisfy HTR-000.

## Change log

| Date | Change |
| --- | --- |
| 2026-08-16 | Re-routed HTR-000 from proposal-only `experiment` to executable `task-session`; retained its receipt-only scope and owner-prerequisite fence. |
| 2026-08-16 | Initial high-complexity plan created from the accepted design and current runtime evidence. |
