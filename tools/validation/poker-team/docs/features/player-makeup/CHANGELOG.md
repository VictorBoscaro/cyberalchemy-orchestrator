# player-makeup — Changelog

All notable changes to the **player-makeup** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — converted AdjustPlayerMakeup and SetPlayerMakeupPolicy postconditions into ID-based guarantee rows with formal assertions and traceability links.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed from latest instrumentation to FLAG with P0 O3/O9/O15/O16 obligations marked implemented (canonical verifier CLI rerun remains pending).
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.

### Changed

- **SPEC.md** — expanded ownership to include web maintainers for makeup dashboard governance.
- **TEST-SPEC.md** — corrected stale contract test file reference for makeup route coverage.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: docs: add observability specs for 5 remaining MVP features.
- **history** — 2026-04-15: style: formatting cleanup — UI components, hooks, E2E tests, feature docs.
