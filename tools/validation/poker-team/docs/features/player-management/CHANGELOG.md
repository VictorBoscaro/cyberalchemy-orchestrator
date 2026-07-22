# player-management — Changelog

All notable changes to the **player-management** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — converted CreatePlayer, CreateCoach, AssignCoach, and UnassignCoach postconditions into ID-based guarantee rows with formal assertions and traceability links.
- **integration relationship traceability** — integration guarantees now include explicit relationship semantics references where event production behavior applies.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed from latest instrumentation to FLAG with no open P0 telemetry gaps (canonical verifier CLI rerun remains pending).
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.

## 2026-04-24

### Changed

- **player identity model** — player records now support explicit auth principal linkage for deterministic self-visibility resolution.
- **visibility authority** — ResolvePlayerVisibility now uses player principal linkage instead of implicit id equivalence for coach/player self scope.
- **create-player contract** — create flow now accepts optional principal linkage with explicit duplicate-principal conflict semantics.
- **player and coach lifecycle events** — create/assign/unassign operations now emit deterministic lifecycle events aligned with events.md contracts.
- **coach-scope authorization guard** — `getCoachPlayers` no longer treats read permission as an admin bypass, preserving own-coach visibility boundaries.
- **pilot blockers register** — PM-BLK-01, PM-BLK-02, PM-BLK-03, PM-BLK-04, and PM-BLK-05 were closed from implementation and artifact evidence.
- **alignment artifacts** — ALIGNMENT-REPORT and LAYERING-ALIGNMENT-REPORT were refreshed to DomainSpec 1.8.2 with current identity and visibility evidence.

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.
- **states.md** — added player, coach, and assignment lifecycle state machines.
- **events.md** — added event contracts for player/coach creation and coach assignment transitions.
- **workflows.md** — documented player registration and coach assignment orchestration flows.
- **ALIGNMENT-REPORT.md** — established baseline spec-to-implementation drift findings for player-management.
- **LAYERING-ALIGNMENT-REPORT.md** — established baseline layering findings for player/coaching rule placement.

### Changed

- **SPEC.md** — expanded aspect coverage and concept registry links for states, events, and workflows.
- **SPEC.md** — expanded ownership to include web maintainers for coach/player management surfaces.
- **TEST-SPEC.md** — corrected stale suggested evidence paths and refreshed uncovered notes now that states/events/workflows aspects exist.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: docs: add observability specs for 5 remaining MVP features.
- **history** — 2026-04-15: style: formatting cleanup — UI components, hooks, E2E tests, feature docs.
