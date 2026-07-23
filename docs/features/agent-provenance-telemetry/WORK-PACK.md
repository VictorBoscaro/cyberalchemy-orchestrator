---
feature: agent-provenance-telemetry
artifact: work-pack
status: active
version: 0.1.0
created: 2026-07-23
last_updated: 2026-07-23
derived_from: discovery/session-dispatch-research-records.md@0.2.0
---

# WORK-PACK: Agent Provenance Telemetry

## Purpose

Plan-first execution manifest for the first modular Agent Provenance Telemetry (APT) increment:
coarse session identity, the existing dispatch seam, immutable research capture, append-only
research facts, deterministic read projections, and the bounded reference-probe profile. The
increment is subordinate to Agents Communication Infra (ACI); it does not create a second bus,
journal, appender, artifact service, receipt authority or dispatch lifecycle.

This work-pack authorizes planning plus isolated construction of a pure module and executable tests.
The DomainSpec files, stories, TEST-SPEC and UI applicability decision passed their individual and
corpus-wide review gates. Authority-bearing ACI integration and runtime enablement remain blocked
until their distinct profile, executable-test and readiness evidence gates pass.

## Planner Control Fields

| Field | Value | Notes |
|---|---|---|
| `plannerGateStatus` | `pass` | File gates and corpus-wide review passed; this authorizes task planning, not runtime enablement. |
| `constructionGateStatus` | `pass` | Pure TypeScript module construction and test-only in-memory doubles are authorized; no durable adapter, bus, journal, profile registration or runtime export is allowed. |
| `mutationGateStatus` | `block` | Authority-bearing ACI integration remains blocked until the integration predicate below passes. |
| `enablementGateStatus` | `block` | Probe/runtime enablement remains blocked until registered profiles and crash/race/replay/redaction evidence pass. |
| `complexity` | `high` | Crosses session, dispatch, research, probe, persistence, replay, UI and ACI boundaries. |
| `architectureWave` | `Stage A` | Pure construction passed; APT integration governance is frozen for independent review while authority-bearing integration remains blocked. |
| `activePlanRef` | `WORK-PACK.md#wave-status-board` | This file is the current planning entrypoint. |
| `lastPlannedAt` | `2026-07-23T05:55:59Z` | UTC. |
| `readinessProfile` | `pilot` | Local, modular first increment; no production deployment claim. |

## Scope and Authority Boundary

In scope:

- `ensure_session`, authorized `start_new_session` rollover and the sole
  `session.dispatch_linked` Session-to-Dispatch edge;
- the existing dispatch ledger as an external authority, with no new ledger keys in the first cut;
- immutable `ResearchCapture`, append-only extracted research facts and `ResearchRecord` as-of
  projections;
- typed source observation, reference use, claim relation and reference-check lineage;
- candidate mathematical/logical formalizations with interpretation and review provenance;
- an ACI-subordinate validated append port, local adapter, canonical digests, idempotent receipts and
  deterministic replay;
- the small reference-probe profile and its session/probe/recommendation/source-observation lineage;
- Sessions, Dispatches and Research Records projections, followed by granular derived projections.

At L0, `ResearchCapture.raw_return`, when present for `captured` or `partial`, is exactly one
content-addressed artifact reference; for `missing` it is canonical null. Inline raw returns are
forbidden. Artifact metadata must carry data classification, redaction policy, retention policy
and tombstone behavior before any capture is accepted.

Out of scope for this first increment:

- a parallel Work Bus, journal, artifact store, dispatch appender or knowledge registry;
- assertion-level promotion, ontology acceptance or treating extracted claims as global truth;
- historical backfill without a separately accepted provenance policy;
- unbounded probe orchestration, automatic extra debate rounds or production deployment.

## Task Status Board

| Task ID | Goal | Complexity | Assigned Waves | Gate Status | Status |
|---|---|---:|---|---|---|
| `TASK-000` | Establish work-pack, scope, authority map and complete stage matrix. | high | W0 | ready | completed |
| `TASK-010` | Ratify architecture, glossary and feature-level concept registry. | high | W0-W1 | corpus PASS | completed |
| `TASK-020` | Specify domain, states, rules, operations, events and workflows. | high | W1 | corpus PASS | completed |
| `TASK-030` | Specify interfaces, mappings, queries, persistence/replay and observability. | high | W1 | corpus PASS | completed |
| `TASK-040` | Derive stories, acceptance fixtures and test specifications from exact coverage IDs. | high | W1 | TEST-SPEC reviewed; execution not run | completed |
| `TASK-050` | Freeze the ACI protocol-profile mapping and reference-probe small-profile contract. | high | W1-W2 | APT-side requests/digests frozen; ACI registration receipts pending | in-review |
| `TASK-100` | Run implementation-readiness for isolated construction and split one task-session per TASK/SWU. | high | W2 | construction readiness PASS; integration unaffected | completed |
| `TASK-105` | Construct pure schemas, APT normalization/canonical-payload candidates, an injected canonicalizer interface, a pure reducer kernel over supplied verified fixtures, and executable tests under `tools/agent-provenance-telemetry/`; doubles stay test-only, in-memory and non-exported. | high | W2 | final reviewer PASS 5/5; 27/27 bounded cases, typecheck and contract vectors PASS; digest-bound receipt recorded | completed |
| `TASK-110` | Integrate artifact-only raw capture, append port and ACI-subordinate adapter with the complete closed set of registered ACI profiles. | high | W3 | blocked by four ACI registration receipts, independent storage-policy PASS and owner mutation gate | blocked |
| `TASK-120` | Implement session/research operations and deterministic replay projections. | high | W3 | blocked by TASK-100/110 | blocked |
| `TASK-130` | Wire the small reference-probe bus profile without creating a second runtime. | high | W3 | blocked by TASK-050/100/110 | blocked |
| `TASK-140` | Wire derived Sessions, Dispatches and Research Records projections into existing read surfaces without adding ledger keys or persisted joins. | high | W3 | blocked by TASK-100/120 and UI re-entry if applicable | blocked |
| `TASK-150` | Instrument classified/redacted operational logs, traces and metrics without making them workflow authority. | medium | W3 | blocked by TASK-100/110 | blocked |
| `TASK-VERIFY` | Run `domainspec-verify-feature agent-provenance-telemetry` and publish `VERIFICATION.md`. | high | W4 | blocked until implementation evidence | blocked |
| `TASK-AUDIT-ALIGNMENT` | Run `domainspec-audit-alignment agent-provenance-telemetry` and publish `ALIGNMENT-REPORT.md`. | high | W4 | blocked until mutation evidence | blocked |
| `TASK-AUDIT-LAYERING` | Run `domainspec-audit-layering agent-provenance-telemetry` and publish `LAYERING-ALIGNMENT-REPORT.md`. | high | W4 | blocked until mutation evidence | blocked |

If a closure task returns `FLAG` or `BLOCK`, remediation is appended as a new task. The original
verification or audit obligation is retained.

## Construction, Integration and Enablement Gates

The gates form a strict ladder:

1. documentation/planner review;
2. isolated construction of pure modules and executable tests;
3. authority-bearing ACI integration using exact registered profiles;
4. probe/runtime enablement after crash, race, replay, redaction and no-parallel-authority evidence.

Construction may not import or export a durable store, bus, journal or receipt authority. Test
doubles live only under test paths, are in-memory and non-durable, and simulate responses of the
specified ports. They are not runtime adapters. `TEST-SPEC.md` is the current test source; automated
`derive --out` and `emit-tests` remain disabled until the test-derivation engine supports the
`specs/` layout and exact APT syntax without identity or parser drift.

The implementation worker, its reviewer and any automation they run may produce evidence, but none
may change `mutationGateStatus`. Only `@victor`, the project owner identified by the
[focused discovery](discovery/session-dispatch-research-records.md#objective), may append the gate
decision after an independent reviewer has verified this predicate:

```text
INTEGRATION_READY =
  every_spec_file_review = PASS
  AND corpus_review = PASS
  AND exact_coverage_registry_frozen
  AND derived_test_spec_review = PASS
  AND isolated_construction_tests = PASS
  AND construction_readiness_verdict = PASS
  AND all_required_aci_profile_receipts = PASS
  AND open_mutation_blockers = 0
  AND storage_and_artifact_policy_review = PASS
```

Each conjunct requires an evidence receipt containing `receipt_id`, `gate_kind`, reviewed artifact
path and digest, reviewer identity, verdict, review timestamp and any superseded receipt. The owner
records the final decision in `work-pack/shared/03-cross-task-decisions.md` and changes this file to
`mutationGateStatus=pass` in the same documentation change. That change itself requires an
independent documentation-review receipt naming its exact digest; owner identity alone is not a
review bypass. Missing, stale, mismatched or self-reviewed evidence evaluates to false. Probe
enablement additionally requires the ACI
protocol-profile registration receipt described by APT-B3; a general mutation pass does not waive
that narrower gate. Fact append and probe-lineage enablement additionally require the distinct ACI
transactional semantic-uniqueness/result-mapping profile described by APT-B7.

`all_required_aci_profile_receipts` is a closed conjunction of independently verified registrations
and exact digests for:

1. atomic command receipt plus accepted-prefix/read-grouping;
2. transactional semantic-uniqueness/result-mapping;
3. event schema plus canonicalizer registry;
4. the reference-probe profile when the task includes probe publication or lineage.

An unrelated receipt cannot satisfy a missing member, and a placeholder digest is always false.
The APT-side frozen requests and their byte digests are recorded in
`integration/stage-a/profile-digests.sha256`. These are registration inputs, not ACI registration
receipts, and therefore do not make the conjunction true.

`enablementGateStatus` can pass only after integration passes and the exact crash/race/retry,
replay/checkpoint, redaction/no-raw and telemetry-non-authority suites pass against the integrated
boundary. Construction evidence never substitutes for integration or enablement evidence.

### Required ACI Transactional Semantic-Uniqueness/Result-Mapping Profile

L0 requires the exact ACI-owned binding
`{profile_id=aci.transactional-semantic-uniqueness-result-mapping,
profile_version=1, profile_digest=<ACI-registered digest>}`. The digest placeholder is not an
implementation default: until ACI publishes and a reviewer verifies the exact digest and
registration receipt, `TASK-110`, `TASK-120` and `TASK-130` remain blocked.

The profile guarantees in one ACI journal transaction: global uniqueness by `fact_id`; collision
comparison of canonical payload digest, `subject_id` and `supersedes_fact_id`; result identity
`existing_exact ∪ accepted(submitted_new)`; and atomic append/head/receipt coverage only for
`submitted_new`. Its total request mapping labels preexisting refs `existing_exact` without
reaccepting them or including them in the new receipt.

## Architecture-Guided Task Directives

The approved DomainSpec corpus and TEST-SPEC assign exact coverage IDs. The task directives retain
discovery citations as derivation provenance, not as substitutes for the exact registries.
TASK-100 construction-readiness evidence is required before TASK-105; a separate integration
preflight and owner gate are required before TASK-110 or later authority-bearing work.

| Task ID | DomainSpec Sources | Current Coverage Sources | Architecture References | Implementation Directive | Verification Evidence |
|---|---|---|---|---|---|
| `TASK-105` | `specs/domain.md`; `specs/rules.md`; `specs/states.md`; `TEST-SPEC.md` | APT-R1–APT-R8 and APT-C01–APT-C18 | `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model) | Implement only pure APT schemas/normalization, canonical-payload candidates, an injected canonicalizer interface and reducer kernels over supplied verified events. Do not claim authoritative ACI bytes/digests/receipts, read journal prefixes/checkpoints or export a durable adapter. | Exact-ID unit/property fixtures, deterministic pure-reducer tests and test-only double boundary checks. |
| `TASK-110` | `specs/operations.md`; `specs/events.md`; `specs/interfaces.md`; `specs/persistence-and-replay.md` | [APT-D13 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT1, TODO-APT4 and TODO-APT10](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [minimal ACI binding](discovery/session-dispatch-research-records.md#46-minimal-module-and-aci-binding) | `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec dependency constraints](../../../domainspec/architecture/pattern-library/DEPENDENCY-RULES.md#layer-dependency-constraints); [ACI scope boundary](../agents-communication-infra/specs/architecture.md#scope-boundary) | Keep canonicalization and validation pure; put storage behind the APT port; require artifact-only raw capture; enforce global `fact_id` uniqueness through the exact ACI semantic-uniqueness/result-mapping profile; acknowledge only after durable append. | Global-ID collision, idempotency, conflict, atomic-batch, result-partition, crash, artifact-policy and canonical-digest tests. |
| `TASK-120` | `specs/operations.md`; `specs/states.md`; `specs/queries.md`; `specs/rules.md` | [APT-D2, APT-D12, APT-D13 and APT-D15](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT2 and TODO-APT7](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [three-level read models](discovery/session-dispatch-research-records.md#5-three-level-read-models) | `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec dependency constraints](../../../domainspec/architecture/pattern-library/DEPENDENCY-RULES.md#layer-dependency-constraints) | Bind verified accepted ACI prefixes/checkpoints to the pure reducer kernel, implement session/research operations and expose deterministic as-of projections. Preserve single edge authorities and immutable capture/fact revisions. | Replay-from-zero/checkpoint parity, CAS races, dedupe, supersession and as-of fixtures against the integrated boundary. |
| `TASK-130` | `specs/interfaces.md`; `specs/events.md`; `specs/workflows.md`; `specs/mappings.md` | [APT-D6, APT-D10 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT5 and TODO-APT10](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [reference lineage](discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) | `specs/architecture.md`; [ACI high-level structure](../agents-communication-infra/specs/architecture.md#view-2-high-level-structure-view); [ACI data and evidence artifacts](../agents-communication-infra/specs/architecture.md#data-and-evidence-artifacts) | Verify both the probe profile and semantic-uniqueness/result-mapping profile; submit only `submitted_new`; return `existing_exact ∪ accepted(submitted_new)` without putting existing refs in the new receipt. | Profile mismatch, global fact-ID collision, mixed/zero-new result partition, lost-response retry and lineage tests. |
| `TASK-140` | `specs/interfaces.md`; `specs/queries.md`; `specs/mappings.md`; `UI-SPEC.md` | [APT-D5, APT-D12 and APT-D15](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT7 and TODO-APT8](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [three-level read models](discovery/session-dispatch-research-records.md#5-three-level-read-models) | `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec testing alignment](../../../domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md#layer-to-test-mapping) | Add only rebuildable read projections over authoritative Session links, the pinned immutable variant-specific Dispatch snapshot and accepted research facts. Never fetch or leak current mutable Dispatch state; do not add Dispatch ledger keys, persist reverse joins, copy raw answers or introduce another Session-to-Dispatch or Dispatch-to-Research authority. | Projection contract, list/detail parity, historical-unlinked and, only after UI applicability re-entry, three-table state tests. |
| `TASK-150` | `specs/observability.md`; `specs/events.md`; `specs/rules.md` | [APT-D11, APT-D13 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT4](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [raw capture contract](discovery/session-dispatch-research-records.md#41-immutable-researchcapture) | `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [ACI trace and log correlation](../agents-communication-infra/specs/observability.md#trace-and-log-correlation) | Emit correlated logs/traces/metrics from committed facts and adapter outcomes; log only classified/redacted metadata and digests, never raw-return bodies; never use operational telemetry as command, replay or projection authority. | Signal schema tests, no-raw-body assertions, redaction checks, correlation assertions and zero-authority review. |

## Required Links and Split Strategy

This high-complexity work-pack starts as a single reviewed planning entrypoint. As the first output
of TASK-100, before TASK-105 starts, it must split implementation detail into:

- `work-pack/shared/01-context.md`
- `work-pack/shared/02-cross-task-gaps-and-questions.md`
- `work-pack/shared/03-cross-task-decisions.md`
- `work-pack/shared/04-traceability.md`
- one file per mutation or closure task under `work-pack/tasks/`
- one file per active execution wave under `work-pack/waves/`

The root `WORK-PACK.md` remains the stable status entrypoint after the split.

### DomainSpec Corpus Layout Variant

This feature explicitly uses the ACI-local layout variant:
`docs/features/agent-provenance-telemetry/specs/`. `SPEC.md`, `architecture.md`, `glossary.md` and
all aspect documents live under that directory, following the neighboring ACI precedent. Every
DomainSpec template is rewritten with links relative to `specs/`; no template-root path is copied
unchanged. Root-level `STORIES.md`, `TEST-SPEC.md`, reports and this work-pack may link into that
corpus but do not become competing concept registries.

## Wave Status Board

<a id="W0"></a>

| Wave | Objective | Entry Gate | Exit Gate | Status | Evidence |
|---|---|---|---|---|---|
| W0 | Lock scope, authority boundaries, architecture baseline and stage coverage. | Focused discovery reviewed. | WORK-PACK and architecture baseline incorporated into W1 corpus review. | completed | Scope/baseline documentation completed; this is not a corpus, readiness, mutation or runtime PASS. |
| W1 | Author and review every DomainSpec aspect plus derived stories/tests. | W0 documentation available. | Corpus-wide review has no objection and issues its receipt. | completed | Corpus review PASS 4/5; `STORIES.md`, planned/not-run `TEST-SPEC.md` and deferred L0 `UI-SPEC.md` approved. |
| W2 | Construct the isolated pure module and executable contract tests; freeze ACI profile mappings separately. | W1 corpus-wide receipt and construction gate PASS. | TASK-100/105 pass; pure tests execute; no durable/runtime authority is introduced. | completed | TASK-105 final review PASS 5/5; fresh 27/27 bounded tests, typecheck and contract vectors PASS; source manifest and restricted acceptance receipt recorded. |
| Stage A | Freeze the exact APT integration requests, storage policy and vertical-slice contract without runtime mutation. | W2 accepted. | Independent reviewers can verify exact digests and owner gate proposal without ambiguity. | in-review | `integration/stage-a/`; four request digests frozen; ACI registrations, storage-policy verdict and owner gate remain pending. |
| W3 | Integrate the modular local pilot with exact ACI profiles, then wire projections and classified telemetry. | Owner-recorded `mutationGateStatus=pass` backed by integration-readiness receipts. | Integrated suites pass; no parallel authority or layering violation remains; enablement evidence is ready for owner review. | blocked | APT request digests exist, but ACI registration receipts, storage-policy PASS and owner mutation approval are absent. |
| W4 | Run feature verification, alignment audit and layering audit; remediate findings. | W3 implementation evidence complete. | All three closure verdicts pass and registry/docs reflect actual state. | blocked | Requires W3 implementation evidence. |

## Pipeline Stage Coverage

All canonical stages remain listed even when deliberately skipped.

| Stage | Required | Wave Mapping | Status | Evidence | Skip Reason |
|---|---:|---|---|---|---|
| plan | yes | W0-W1 | completed | `WORK-PACK.md`; corpus-wide review PASS 4/5 | none |
| architecture-baseline | yes | W0-W1 | completed | `specs/architecture.md`, `specs/glossary.md`, `specs/SPEC.md`; corpus PASS | none |
| spec | yes | W1 | completed | Approved aspect corpus under `specs/` | none |
| stories | yes | W1 | completed | `STORIES.md` PASS 2/5 | none |
| tests | yes | W1-W3 | in-progress | TASK-105 27/27 bounded cases accepted; no full R/C family is claimed | L3/L4, operation, integration, replay and profile families remain planned/not-run. |
| backend-implement | yes | W2-W3 | in-progress | TASK-105 pure construction accepted; TASK-110/120/130 remain integration-blocked | Authority-bearing implementation blocked. |
| ui-pipeline | yes | W1/W3 | skipped | `UI-SPEC.md` PASS 1/5 records L0 not applicable/deferred | Re-entry requires a later applicability decision. |
| observability-spec | yes | W1 | completed | `specs/observability.md` approved after authorized remediation | Instrumentation remains an implementation task. |
| instrument-otel | yes | W3 | blocked | TASK-150 | Blocked until TASK-100 and mutation authorization. |
| otel-verify | yes | W3-W4 | blocked | Planned observability verification output | Blocked until instrumentation exists. |
| infra-deploy | yes | W4 | skipped | Pilot boundary in this work-pack | First increment is local-only; deployment requires a later authorized work-pack. |
| registry-sync | yes | W4 | blocked | Planned DomainSpec/ACI profile registry evidence | Runs only after implementation and verification agree. |
| verify-readiness | yes | W2 | completed | `construction-readiness.md` PASS for isolated construction | Integration readiness remains blocked and separate. |
| verify-feature | yes | W4 | blocked | `VERIFICATION.md` not yet issued | Requires implementation. |
| audit-alignment | yes | W4 | blocked | `ALIGNMENT-REPORT.md` not yet issued | Requires implementation. |
| audit-layering | yes | W4 | blocked | `LAYERING-ALIGNMENT-REPORT.md` not yet issued | Requires implementation. |

## Decision Lock Summary

| Decision ID | Scope | Status | Selected Option | Source | Date |
|---|---|---|---|---|---|
| `APT-D1`, `APT-D2`, `APT-D3` | cross-task | selected-for-specification | Three levels; start-time session; existing dispatch remains authoritative. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D4`, `APT-D5`, `APT-D6`, `APT-D7` | cross-task | selected-for-specification | Research owns raw capture and attributed structure; reference axes stay typed; notation remains interpreted candidate. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D8`, `APT-D9`, `APT-D10`, `APT-D11` | cross-task | selected-for-specification | Incremental boundary; raw-first append-only facts; typed checks; capture status never mutates dispatch lifecycle. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D12` | cross-task | selected-for-specification | `session.dispatch_linked` and `ResearchCapture.dispatch_id` are the sole join authorities. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D13` | cross-task | selected-for-specification | Immutable capture, append-only extracted facts and as-of record projection are distinct. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D14` | architecture | selected-for-specification | Validated ACI-subordinate append port/local adapter; no second bus or new dispatch ledger keys. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-D15` | cross-task | selected-for-specification | Deterministic projections require as-of, dedupe, supersession and replay proofs. | Focused discovery v0.2.0 | 2026-07-23 |
| `APT-WP-D1` | planning | selected | Individual documentation gates and corpus-wide review passed. This authorizes isolated construction planning, not ACI integration or runtime enablement. | This work-pack | 2026-07-23 |
| `APT-WP-D2` | delivery | selected | Local pilot first; infrastructure deployment is skipped in this work-pack. | User scope plus focused discovery | 2026-07-23 |
| `APT-WP-D3` | data safety | selected | L0 forbids inline raw returns and requires a classified, redacted, retained and tombstone-capable artifact reference; rationale: bounded-pilot risk control. | This work-pack | 2026-07-23 |
| `APT-WP-D4` | governance | selected | Only `@victor`, the workspace project owner, may lift the integration mutation gate after independent, digest-bound evidence receipts satisfy `INTEGRATION_READY`; the gate-changing documentation digest needs its own review receipt. Rationale: mutation governance. | This work-pack | 2026-07-23 |
| `APT-WP-D5` | implementation stack | selected | Build L0 as Node 22 / TypeScript under `tools/agent-provenance-telemetry/`, matching the executable ACI bus and Vitest-oriented test ecosystem while remaining outside the read-only Python control plane. | User-delegated tool-selection gate, selector/reviewer PASS 3/5 | 2026-07-23 |
| `APT-WP-D6` | implementation gates | selected | Separate documentation, isolated construction, ACI integration and enablement. Pure construction is allowed before registered ACI digests; durable adapters/runtime remain blocked. | User-authorized incremental implementation scope plus selector/reviewer PASS 3/5 | 2026-07-23 |

Selected-for-specification decisions constrain authorship but are not runtime claims. A reviewer may
return them to blocked status if the aspect corpus exposes a contradiction.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target |
|---|---|---|---|---|---|
| `APT-B1` | closed | DomainSpec corpus and exact coverage registry passed individual and corpus-wide gates. | spec group | No action; retain receipt history. | W1 |
| `APT-B2` | integration | Storage, transaction and adapter contracts are specified; integrated crash/race receipts remain outstanding. | implementation group | Exercise crash/race fixtures only after exact ACI integration is authorized. | W3 |
| `APT-B3` | probe enablement | The reference-probe APT request is frozen at an exact digest, but ACI has not registered it or issued a receipt. | APT/ACI owners | Independently verify the request digest and obtain the matching ACI registration receipt before TASK-130. | Stage A |
| `APT-B4` | closed | TASK-105 pure L0 passed final reviewer cycle 5 with bounded evidence and no whole-family claim. | implementation orchestrator | Retain source manifest and acceptance receipt. | W2 |
| `APT-B5` | UI mutation | `UI-SPEC.md` records the reviewed L0 decision as not applicable/deferred with zero UI concepts; no read-surface runtime integration or UI re-entry evidence exists. | architecture/spec group | Keep TASK-140 blocked until query runtime readiness; if UI becomes applicable, satisfy the explicit UI re-entry gate before wiring. | W2-W3 |
| `APT-B6` | enablement | L0 artifact classification, redaction, retention and tombstone contracts are approved; executable integrated policy/privacy receipts remain outstanding. Inline raw is forbidden. | spec/security owners | Build pure policy tests in W2 and rerun against integrated boundaries before enablement. | W2-W3 |
| `APT-B7` | mutation/probe enablement | The semantic-uniqueness/result-mapping APT request is frozen at an exact digest, but its ACI registration receipt and integrated fixtures are absent. | APT/ACI owners | Register the exact digest and pass global-collision, mixed-result, crash and race fixtures before TASK-110/120/130. | Stage A-W3 |
| `APT-B8` | integration | The atomic receipt/accepted-prefix request is frozen at an exact digest, but its ACI registration receipt and grouping fixtures are absent. | ACI owners | Register the exact digest and verify atomic grouping/read-prefix fixtures before TASK-110. | Stage A-W3 |
| `APT-B9` | integration | The event-schema/canonicalizer request is frozen at an exact digest, but its ACI registration receipt and compatibility fixtures are absent. | ACI owners | Register the exact digest and verify schema/canonicalizer compatibility vectors before TASK-110. | Stage A-W3 |
| `APT-B10` | mutation | Storage/artifact policy packet is complete but has no independent digest-bound PASS receipt. | security/storage reviewer | Review `integration/stage-a/storage-artifact-policy-review.md` and issue PASS or FIX. | Stage A |

The following are deferred, not blockers for the bounded pilot: historical backfill, bibliographic
equivalence, global assertion promotion, ontology acceptance of notation, tensioned probe shape and
non-local deployment.

## Notes

- The superseded D0 topic/tag fixture is prior evidence only; it does not prove persistence,
  idempotency, replay, CAS, sole-writer enforcement or this research model.
- ACI remains authoritative for journal, bus, artifact, receipt and canonicalization contracts.
- Existing dispatch YAML is never edited directly. Any later additive ledger scope must pass the
  full pending-to-appender-to-reader-to-detail-to-list round trip.
- Task files created during the W2 split must include `Gaps and Questions`, `Decision Lock`,
  `DomainSpec Coverage`, `Architecture References` and `Implementation Directives`.
- W0 and W1 are documentation waves. No code, runtime store, registry profile or external
  deployment is authorized by their completion alone.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-07-23 | Initial plan-first work-pack created with documentation-only gate, canonical stage coverage and mutation-aware verification/alignment/layering obligations. | Codex spec group |
