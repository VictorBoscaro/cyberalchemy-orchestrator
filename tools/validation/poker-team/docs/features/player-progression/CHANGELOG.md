# player-progression — Changelog

All notable changes to the **player-progression** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — converted CheckProgression postconditions into ID-based guarantee rows with formal assertions and traceability links.
- **integration relationship traceability** — event-emission guarantees now reference `produces` semantics for deterministic cross-aspect linkage.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed from latest instrumentation to FLAG with no open P0 telemetry gaps (canonical verifier CLI rerun remains pending).
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.

## 2026-04-24

### Added

- **progression event contract** — added typed `ProgressionChecked` event authority in `backend/src/domain/progression/progression.events.ts` and deterministic emission from `check-progression` use-case.

### Changed

- **operations.md / queries.md** — removed duplicated contract blocks and normalized canonical progression operation/query authority.
- **period boundary behavior** — progression route now rejects unsupported `period` query values with deterministic `400 VALIDATION_ERROR`.
- **formula semantics** — reconciled BB/100 winrate and threshold rules across STORIES, TEST-SPEC, and policy implementation evidence.
- **alignment artifacts** — ALIGNMENT-REPORT and LAYERING-ALIGNMENT-REPORT refreshed to DomainSpec 1.8.2 with resolved findings.
- **pilot blockers register** — PRG-BLK-01, PRG-BLK-02, PRG-BLK-03, and PRG-BLK-04 are now closed with evidence.

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.
- **mappings.md** — added request/response progression mapping contracts.
- **states.md** — added evaluation lifecycle and eligibility state models.
- **events.md** — added progression checked event contract.
- **workflows.md** — documented delegated progression check workflow.
- **ALIGNMENT-REPORT.md** — established baseline spec-to-implementation drift findings for progression capability.
- **LAYERING-ALIGNMENT-REPORT.md** — established baseline layering findings for progression policy boundaries.

### Changed

- **SPEC.md** — expanded concept registry and aspect index to include mappings, states, events, and workflows.
- **SPEC.md** — expanded ownership to include web maintainers for progression UI/report consumers.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: docs: add observability specs for 5 remaining MVP features.
- **history** — 2026-04-15: style: formatting cleanup — UI components, hooks, E2E tests, feature docs.
