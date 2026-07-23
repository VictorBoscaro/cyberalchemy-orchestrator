---
feature: agent-provenance-telemetry
artifact: work-pack
status: draft
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

This work-pack authorizes documentation only while the DomainSpec corpus is being written and
reviewed. Runtime mutation remains blocked until the architecture, specification, derived tests and
implementation-readiness gates pass.

## Planner Control Fields

| Field | Value | Notes |
|---|---|---|
| `plannerGateStatus` | `pass` | Pass applies only to W0/W1 documentation; it does not authorize mutation-capable stages. |
| `mutationGateStatus` | `block` | Only `@victor`, the project owner recorded by the focused discovery, may lift it after the formal evidence predicate below is satisfied. |
| `complexity` | `high` | Crosses session, dispatch, research, probe, persistence, replay, UI and ACI boundaries. |
| `architectureWave` | `W0` | Mandatory architecture and authority baseline. |
| `activePlanRef` | `WORK-PACK.md#W0` | This file is the current planning entrypoint. |
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

At L0, `ResearchCapture.raw_return` is always a content-addressed artifact reference. Inline raw
returns are forbidden. Artifact metadata must carry data classification, redaction policy, retention
policy and tombstone behavior before any capture is accepted.

Out of scope for this first increment:

- a parallel Work Bus, journal, artifact store, dispatch appender or knowledge registry;
- assertion-level promotion, ontology acceptance or treating extracted claims as global truth;
- historical backfill without a separately accepted provenance policy;
- unbounded probe orchestration, automatic extra debate rounds or production deployment.

## Task Status Board

| Task ID | Goal | Complexity | Assigned Waves | Gate Status | Status |
|---|---|---:|---|---|---|
| `TASK-000` | Establish work-pack, scope, authority map and complete stage matrix. | high | W0 | ready | completed |
| `TASK-010` | Ratify architecture, glossary and feature-level concept registry. | high | W0-W1 | documentation-only | not-started |
| `TASK-020` | Specify domain, states, rules, operations, events and workflows. | high | W1 | after TASK-010 | not-started |
| `TASK-030` | Specify interfaces, mappings, queries, persistence/replay and observability. | high | W1 | after TASK-010 | not-started |
| `TASK-040` | Derive stories, acceptance fixtures and test specifications from exact coverage IDs. | high | W1-W2 | after TASK-020/030 | not-started |
| `TASK-050` | Freeze the ACI protocol-profile mapping and reference-probe small-profile contract. | high | W1-W2 | after TASK-020/030 | not-started |
| `TASK-100` | Run implementation-readiness and resolve every mutation blocker. | high | W2 | after specs/tests pass review | not-started |
| `TASK-110` | Implement schemas, canonicalization, artifact-only raw capture, append port and ACI-subordinate local adapter. | high | W3 | blocked by TASK-100 | not-started |
| `TASK-120` | Implement session/research operations and deterministic replay projections. | high | W3 | blocked by TASK-100/110 | not-started |
| `TASK-130` | Wire the small reference-probe bus profile without creating a second runtime. | high | W3 | blocked by TASK-050/100/110 | not-started |
| `TASK-140` | Wire derived Sessions, Dispatches and Research Records projections into existing read surfaces without adding ledger keys or persisted joins. | high | W3 | blocked by TASK-100/120 | not-started |
| `TASK-150` | Instrument classified/redacted operational logs, traces and metrics without making them workflow authority. | medium | W3 | blocked by TASK-100/110 | not-started |
| `TASK-VERIFY` | Run `domainspec-verify-feature agent-provenance-telemetry` and publish `VERIFICATION.md`. | high | W4 | ready-after-implementation | not-started |
| `TASK-AUDIT-ALIGNMENT` | Run `domainspec-audit-alignment agent-provenance-telemetry` and publish `ALIGNMENT-REPORT.md`. | high | W4 | ready-after-mutation | not-started |
| `TASK-AUDIT-LAYERING` | Run `domainspec-audit-layering agent-provenance-telemetry` and publish `LAYERING-ALIGNMENT-REPORT.md`. | high | W4 | ready-after-mutation | not-started |

If a closure task returns `FLAG` or `BLOCK`, remediation is appended as a new task. The original
verification or audit obligation is retained.

## Mutation Gate Authority and Evidence

The implementation worker, its reviewer and any automation they run may produce evidence, but none
may change `mutationGateStatus`. Only `@victor`, the project owner identified by the
[focused discovery](discovery/session-dispatch-research-records.md#objective), may append the gate
decision after an independent reviewer has verified this predicate:

```text
MUTATION_READY =
  every_spec_file_review = PASS
  AND corpus_review = PASS
  AND exact_coverage_registry_frozen
  AND derived_test_spec_review = PASS
  AND implementation_readiness_verdict = PASS
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
that narrower gate.

## Architecture-Guided Task Directives

Until the reviewed DomainSpec corpus assigns final coverage IDs, directives cite existing
APT decisions, TODOs and discovery anchors. TASK-040 must replace these discovery citations with
exact final IDs before TASK-100 may pass.

| Task ID | DomainSpec Sources | Current Coverage Sources | Architecture References | Implementation Directive | Verification Evidence |
|---|---|---|---|---|---|
| `TASK-110` | `specs/operations.md`; `specs/events.md`; `specs/interfaces.md`; `specs/persistence-and-replay.md` | [APT-D13 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT1, TODO-APT4 and TODO-APT10](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [minimal ACI binding](discovery/session-dispatch-research-records.md#46-minimal-module-and-aci-binding) | Planned `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec dependency constraints](../../../domainspec/architecture/pattern-library/DEPENDENCY-RULES.md#layer-dependency-constraints); [ACI scope boundary](../agents-communication-infra/specs/architecture.md#scope-boundary) | Keep canonicalization and validation pure; put storage behind the APT port; require artifact-only raw capture with classification/retention metadata; map accepted facts one-to-one through ACI authority; acknowledge only after durable append. | Derived idempotency, conflict, atomic-batch, crash, artifact-policy and canonical-digest tests. |
| `TASK-120` | `specs/operations.md`; `specs/states.md`; `specs/queries.md`; `specs/rules.md` | [APT-D2, APT-D12, APT-D13 and APT-D15](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT2 and TODO-APT7](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [three-level read models](discovery/session-dispatch-research-records.md#5-three-level-read-models) | Planned `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec dependency constraints](../../../domainspec/architecture/pattern-library/DEPENDENCY-RULES.md#layer-dependency-constraints) | Preserve single edge authorities, immutable captures and append-only fact revisions; rebuild every view at an explicit event offset without external calls. | Replay-from-zero/checkpoint parity, CAS races, dedupe, supersession and as-of fixtures. |
| `TASK-130` | `specs/interfaces.md`; `specs/events.md`; `specs/workflows.md`; `specs/mappings.md` | [APT-D6, APT-D10 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT5 and TODO-APT10](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [reference lineage](discovery/session-dispatch-research-records.md#43-reference-uses-and-checks) | Planned `specs/architecture.md`; [ACI high-level structure](../agents-communication-infra/specs/architecture.md#view-2-high-level-structure-view); [ACI data and evidence artifacts](../agents-communication-infra/specs/architecture.md#data-and-evidence-artifacts) | Register and verify the exact protocol profile before enablement; use ACI publications and receipts; stamp source-observation lineage; reject profile mismatch before publication. | Profile mismatch, lost-response retry, partial seat, empty reviewed bundle and lineage tests. |
| `TASK-140` | `specs/interfaces.md`; `specs/queries.md`; `specs/mappings.md`; planned `UI-SPEC.md` | [APT-D5, APT-D12 and APT-D15](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT7 and TODO-APT8](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [three-level read models](discovery/session-dispatch-research-records.md#5-three-level-read-models) | Planned `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [DomainSpec testing alignment](../../../domainspec/architecture/pattern-library/TESTING-ALIGNMENT.md#layer-to-test-mapping) | Add only rebuildable read projections over authoritative session links, current dispatch data and research facts. Do not add dispatch ledger keys, persist reverse joins, copy raw answers or introduce another Session-to-Dispatch or Dispatch-to-Research authority. | Projection contract, list/detail parity, historical-unlinked and three-table UI state tests. |
| `TASK-150` | `specs/observability.md`; `specs/events.md`; `specs/rules.md` | [APT-D11, APT-D13 and APT-D14](discovery/session-dispatch-research-records.md#decisions-baked-in); [TODO-APT4](discovery/session-dispatch-research-records.md#7-deferred-decisions-and-validation-todo); [raw capture contract](discovery/session-dispatch-research-records.md#41-immutable-researchcapture) | Planned `specs/architecture.md`; [DomainSpec layer model](../../../domainspec/architecture/pattern-library/ARCHITECTURE-FOUNDATIONS.md#layer-model); [ACI trace and log correlation](../agents-communication-infra/specs/observability.md#trace-and-log-correlation) | Emit correlated logs/traces/metrics from committed facts and adapter outcomes; log only classified/redacted metadata and digests, never raw-return bodies; never use operational telemetry as command, replay or projection authority. | Signal schema tests, no-raw-body assertions, redaction checks, correlation assertions and zero-authority review. |

## Required Links and Split Strategy

This high-complexity work-pack starts as a single reviewed planning entrypoint. Before W2 begins it
must split implementation detail into:

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
| W0 | Lock scope, authority boundaries, architecture baseline and stage coverage. | Focused discovery reviewed. | WORK-PACK reviewed; architecture/glossary/SPEC ready for file gates. | in-progress | This file; focused discovery v0.2.0. |
| W1 | Author and review every DomainSpec aspect plus derived stories/tests. | W0 work-pack gate passes. | Every file passes its reviewer gate; corpus-wide review has no objection. | not-started | Planned `specs/` corpus and test artifacts. |
| W2 | Freeze ACI profile/mappings and prove implementation readiness. | W1 corpus-wide gate passes. | TASK-100 passes; mutation blockers closed; work-pack split complete. | not-started | Planned readiness report and reviewed task files. |
| W3 | Implement the modular local pilot, derived projection/UI wiring and telemetry. | Owner-recorded `mutationGateStatus=pass` backed by complete evidence receipts. | Derived tests pass; no parallel authority or layering violation remains. | not-started | Code, fixtures, command logs and observability evidence. |
| W4 | Run feature verification, alignment audit and layering audit; remediate findings. | W3 implementation evidence complete. | All three closure verdicts pass and registry/docs reflect actual state. | not-started | `VERIFICATION.md`, `ALIGNMENT-REPORT.md`, `LAYERING-ALIGNMENT-REPORT.md`. |

## Pipeline Stage Coverage

All canonical stages remain listed even when deliberately skipped.

| Stage | Required | Wave Mapping | Status | Evidence | Skip Reason |
|---|---:|---|---|---|---|
| plan | yes | W0 | in-progress | `WORK-PACK.md` | — |
| architecture-baseline | yes | W0 | in-progress | Planned `specs/architecture.md`, `specs/glossary.md`, `specs/SPEC.md` | — |
| spec | yes | W1 | not-started | Planned aspect corpus under `specs/` | — |
| stories | yes | W1 | not-started | Planned `STORIES.md` | — |
| tests | yes | W1-W3 | not-started | Planned `TEST-SPEC.md`, fixtures and implementation test outputs | — |
| backend-implement | yes | W3 | not-started | TASK-110/120/130 | Blocked until TASK-100. |
| ui-pipeline | yes | W1/W3 | not-started | Planned `UI-SPEC.md`, read-surface applicability decision and TASK-140 | Derived projections only; blocked until TASK-100. |
| observability-spec | yes | W1 | not-started | Planned `specs/observability.md` | — |
| instrument-otel | yes | W3 | not-started | TASK-150 | Blocked until TASK-100. |
| otel-verify | yes | W3-W4 | not-started | Planned observability verification output | Blocked until instrumentation exists. |
| infra-deploy | yes | W4 | skipped | Pilot boundary in this work-pack | First increment is local-only; deployment requires a later authorized work-pack. |
| registry-sync | yes | W4 | not-started | Planned DomainSpec/ACI profile registry evidence | Runs only after implementation and verification agree. |
| verify-readiness | yes | W2 | not-started | TASK-100 readiness report | — |
| verify-feature | yes | W4 | not-started | `VERIFICATION.md` | — |
| audit-alignment | yes | W4 | not-started | `ALIGNMENT-REPORT.md` | Seeded because mutation stages are planned. |
| audit-layering | yes | W4 | not-started | `LAYERING-ALIGNMENT-REPORT.md` | Seeded because mutation stages are planned. |

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
| `APT-WP-D1` | planning | selected | Documentation gate passes now; runtime mutation remains separately blocked. | This work-pack | 2026-07-23 |
| `APT-WP-D2` | delivery | selected | Local pilot first; infrastructure deployment is skipped in this work-pack. | User scope plus focused discovery | 2026-07-23 |
| `APT-WP-D3` | data safety | selected | L0 forbids inline raw returns and requires a classified, redacted, retained and tombstone-capable artifact reference; rationale: bounded-pilot risk control. | This work-pack | 2026-07-23 |
| `APT-WP-D4` | governance | selected | Only `@victor`, the workspace project owner, may lift the mutation gate after independent, digest-bound evidence receipts satisfy `MUTATION_READY`; the gate-changing documentation digest needs its own review receipt. Rationale: mutation governance. | This work-pack | 2026-07-23 |

Selected-for-specification decisions constrain authorship but are not runtime claims. A reviewer may
return them to blocked status if the aspect corpus exposes a contradiction.

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target |
|---|---|---|---|---|---|
| `APT-B1` | mutation | No reviewed DomainSpec corpus or exact coverage registry exists yet. | spec group | Complete W1 file gates and corpus-wide review. | W1 |
| `APT-B2` | mutation | Storage, transaction and adapter details are not yet ratified for the local APT module. | architecture/spec group | Settle in architecture and persistence/replay specs with crash fixtures. | W1 |
| `APT-B3` | probe enablement | The exact reference-probe protocol profile is not yet registered against ACI. | APT/ACI owners | Freeze mapping/profile and verify digest before TASK-130. | W2 |
| `APT-B4` | mutation | Implementation-readiness, derived test and architecture-coverage gates have not run. | implementation orchestrator | Complete TASK-040 and pass TASK-100. | W2 |
| `APT-B5` | UI mutation | The existing read-surface integration and UI applicability contract are not yet frozen. | architecture/spec group | Specify projection-only integration and its tests before TASK-140; do not depend on a nonexistent UI architecture document. | W1 |
| `APT-B6` | policy | L0 artifact classification, redaction, retention and tombstone contracts and tests are not yet accepted. Inline raw is already forbidden. | spec/security owners | Ratify the artifact-only contract and produce no-inline, redaction, retention and tombstone test receipts before mutation. | W1 |

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
