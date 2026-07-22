# player-stats — Changelog

All notable changes to the **player-stats** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — converted RecordPlayerStats postconditions into ID-based guarantee rows with formal assertions.
- **integration relationship traceability** — event-emission guarantees now reference `produces` semantics for deterministic cross-aspect linkage.
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.

## 2026-04-24

### Added

- **player-stats-window-policy.service** — introduced domain authority for derived window metrics (`avgHandsPerDay`, `winrateBbPer100`) with deterministic unit coverage.

### Changed

- **get-player-stats-window use-case** — refactored to orchestration-only behavior that delegates derivation policy to the new domain service.
- **stats UI data flow** — stats window hook now sends required `fromDate`/`toDate` parameters and uses canonical `winrateBbPer100` projection mapping.
- **UI/alignment artifacts** — refreshed UI-REVIEW, ALIGNMENT-REPORT, and LAYERING-ALIGNMENT-REPORT to DomainSpec 1.8.2 evidence baseline.
- **stats runtime observability** — `record-player-stats` now emits lifecycle/invariant/rule/workflow/event telemetry for transition, correction, and rejection paths.
- **pilot blockers register** — PST-BLK-01, PST-BLK-02, and PST-BLK-03 are closed with runtime instrumentation and verification evidence.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed to FLAG with no open P0 gaps (remaining O8/O13 hardening is non-blocking backlog).

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.
- **ALIGNMENT-REPORT.md** — established baseline spec-to-implementation drift findings for player-stats contracts.
- **LAYERING-ALIGNMENT-REPORT.md** — established baseline layering findings for stats derivation ownership.

### Changed

- **SPEC.md** — expanded ownership to include web maintainers for stats dashboard governance.
- **use-stats.ts + PlayerStatsPage.tsx** — implemented cursor-driven history pagination and wired load-more behavior in stats UI.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: docs: add observability specs for 5 remaining MVP features.
- **history** — 2026-04-15: style: formatting cleanup — UI components, hooks, E2E tests, feature docs.
