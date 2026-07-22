# auth-access-control — Changelog

All notable changes to the **auth-access-control** feature are documented in this file.

## 2026-04-30

### Added

- **typed postcondition guarantees** — introduced operation-level postcondition classification using State, Persistence, Temporal, Integration, and Audit guarantees.
- **PILOT-DECISIONS.md** — recorded pilot decision-gate outcomes (scope, visibility, strictness, auth, dedupe, audit, failure, decision model, and verification profile).

### Changed

- **operations postconditions formalization** — converted SeedSystemBootstrap, Login, IssueAccessToken, AuthenticateRequest, AuthorizeRequest, and Logout postconditions into ID-based guarantee rows with formal assertions and traceability links.
- **integration relationship traceability** — integration guarantees now include explicit `produces` semantics references for event-backed outcomes.
- **observability verification evidence** — OBSERVABILITY-REPORT was refreshed from latest instrumentation to FLAG with no open P0 telemetry gaps (canonical verifier CLI rerun remains pending).
- **SPEC and TEST-SPEC pilot provenance** — added explicit `## User Stories`, `## Story Coverage Matrix`, and pilot decision provenance references so launch policy and test gate authority are linked.
- **ALIGNMENT-REPORT.md** — refreshed read-only alignment audit against DomainSpec 2.0.3 with severity-ranked findings, explicit blocker/flag split, and strict block-on-FLAG pilot verdict = BLOCKED.

## 2026-04-24

### Changed

- **auth guard authorization contract** — route permission checks now run through AuthorizeRequest semantics (including deny-override) instead of direct permission matching.
- **test-runtime auth fallback** — authentication and authorization fallbacks were narrowed to test runtime so production authorization remains DB-backed and policy-authoritative.
- **pilot blockers register** — AUTH-BLK-01, AUTH-BLK-02, AUTH-BLK-03, and AUTH-BLK-04 were closed with implementation and contract evidence.
- **alignment artifacts** — ALIGNMENT-REPORT and LAYERING-ALIGNMENT-REPORT were refreshed to DomainSpec 1.8.2 with current wave evidence.
- **layering remediation plan** — LAYERING-ALIGNMENT-PLAN was replaced with a dependency-ordered minimal backlog focused on login abuse semantics normalization and centralized status-mapping ownership.
- **AUTH-BLK-03 closure** — login abuse semantics were normalized to canonical `403` behavior across route contracts, UI mapping, and test obligations with deterministic route contract assertions for login/logout/introspect.

## 2026-04-17

### Added

- **CHANGELOG.md** — initialized domain-level changelog for pilot-readiness governance and traceability.
- **POST /auth/token contract test** — added route contract coverage for unauthorized and validation error paths.

### Changed

- **auth.routes.ts** — implemented `POST /auth/token` endpoint to align runtime API with interfaces contract.
- **auth.guard.ts** — switched guarded authentication resolution to DB-backed auth repositories with explicit test-runtime fallback.
- **SPEC.md** — expanded ownership to platform, backend, and web maintainers for cross-layer auth governance.
- **history** — 2026-04-16: feat(auth): add admin bootstrap, role definitions, and Drizzle auth repositories.
- **history** — 2026-04-16: docs: add human-readable descriptions to all observability metrics.
- **history** — 2026-04-16: fix: move @source links outside yaml fences for markdown preview.
- **history** — 2026-04-16: docs: convert @source to markdown links across all observability specs.
- **history** — 2026-04-16: feat: OTel migration, infra governance skills, domainspec submodule update.
- **history** — 2026-04-15: docs: add observability specs for 5 remaining MVP features.
