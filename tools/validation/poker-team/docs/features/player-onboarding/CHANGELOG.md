# player-onboarding — Changelog

All notable changes to the **player-onboarding** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — rewrote SubmitCandidateApplication and ReviewCandidateApplication postconditions into ID-based guarantee tables with formal assertions.
- **integration guarantee traceability** — integration guarantees now link to relationship semantics for `produces` and `produces-for` in the DomainSpec relationship catalog.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed from latest instrumentation to FLAG with no open P0 telemetry gaps (canonical verifier CLI rerun remains pending).
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.

## 2026-04-24

### Added

- **approved candidate intake handoff** — approved review outcomes now persist deterministic payloads for downstream player-management intake consumption.
- **rule grouping policy resolver** — onboarding flow composition now resolves regulation version and grouping through a configurable policy contract.

### Changed

- **admin onboarding permissions** — list/detail/review endpoints now enforce split permission keys aligned with interfaces and UI contracts.
- **candidate dedupe guarantee** — duplicate prevention now includes database uniqueness constraints plus race-condition handling in submission flow.
- **flow contract propagation** — GET onboarding flow now accepts and forwards `regulationVersion` to policy resolution.
- **pilot blockers register** — ONB-BLK-01 through ONB-BLK-05 were closed from backend and UI evidence.
- **UI review evidence refresh** — UI-REVIEW was updated to current implementation behavior and now records residual flags without stale BLOCK findings.
- **alignment artifacts** — ALIGNMENT-REPORT and LAYERING-ALIGNMENT-REPORT were refreshed to DomainSpec 1.8.2 with current layering and integration evidence.

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.
- **events.md** — added submission and review event contracts aligned with onboarding lifecycle transitions.
- **ALIGNMENT-REPORT.md** — established baseline spec-to-implementation drift findings for onboarding contracts.
- **LAYERING-ALIGNMENT-REPORT.md** — established baseline layering findings for onboarding policy placement.

### Changed

- **SPEC.md** — added events aspect coverage and event concept links in onboarding concept registry.
- **SPEC.md** — expanded ownership to include backend maintainers for onboarding review APIs.
- **AdminOnboardingReview.tsx** — added explicit candidate status badges in backlog and detail views.
- **OnboardingFlow.tsx** — added step indicators with `aria-current="step"` semantics for active regulation group.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: refactor(observability): migrate feature metrics to OpenTelemetry conventions.
- **history** — 2026-04-15: feat: observability specs for financial-settlement (~57 metrics) and player-onboarding (~61 metrics).
