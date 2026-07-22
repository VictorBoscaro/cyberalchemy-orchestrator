---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control Layering Alignment Report
summary: Focused layering audit of login abuse denial semantics and route status mapping ownership.
status: in-progress
pillar: platform
domain: auth-access-control-layering
audience:
  - developers
  - architecture
priority: p1
lang: en
owners:
  - platform-core
  - backend-core
updatedAt: 2026-04-24
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
  - TEST-SPEC.md
  - ALIGNMENT-REPORT.md
includes: []
auditor: domainspec-layering-auditor
auditedAt: 2026-04-24
domainspecVersion: 1.8.2
---

# Layering Alignment Report: auth-access-control

**Audited at:** 2026-04-24
**Framework version:** DomainSpec 1.8.2

## Scope

- Login abuse denial semantics (`POST /auth/login`).
- Route status mapping ownership across domain/use-case/http/docs/tests.

## Layer Ownership Snapshot

| Concern | Domain owner | Use-case owner | HTTP owner | Docs/tests owner | Drift |
| --- | --- | --- | --- | --- | --- |
| Login abuse denial decision | `backend/src/domain/auth-access-control/login-risk-policy.ts` (R3 emits `FORBIDDEN`) | `backend/src/use-cases/auth-access-control/login.ts` delegates to domain risk policy | `backend/src/infrastructure/http/routes/auth.routes.ts` maps `FORBIDDEN` to `403` | `docs/features/auth-access-control/operations.md`, `docs/features/auth-access-control/interfaces.md`, `docs/features/auth-access-control/UI-SPEC.md`, `docs/features/auth-access-control/TEST-SPEC.md` | NO |
| Auth error -> HTTP status mapping | Domain/use-cases emit semantic error codes only | Use-cases return `AuthValidationError` codes | Inline mappings duplicated in `backend/src/infrastructure/http/routes/auth.routes.ts` and `backend/src/infrastructure/http/auth/auth.guard.ts` | `docs/features/auth-access-control/mappings.md` defines `ErrorToHttpResponse`, but no canonical status matrix is enforced by tests | YES |

## Findings

| ID | Severity | Status | Layering issue | Evidence | Impact | Required remediation |
| --- | --- | --- | --- | --- | --- | --- |
| AUTH-LDR-04 | HIGH | RESOLVED | Login abuse semantics were split across layers without a single authoritative mapping model. | `docs/features/auth-access-control/interfaces.md`, `docs/features/auth-access-control/UI-SPEC.md`, `docs/features/auth-access-control/TEST-SPEC.md`, `backend/src/infrastructure/http/routes/auth.routes.ts` | API-boundary abuse outcomes are now deterministic and consistent. | None. |
| AUTH-LDR-05 | MEDIUM | OPEN | Route status mapping ownership remains duplicated in adapters instead of one canonical mapper. | `backend/src/infrastructure/http/routes/auth.routes.ts`, `backend/src/infrastructure/http/auth/auth.guard.ts`, `docs/features/auth-access-control/mappings.md` | Future drift risk: the same error code can be interpreted differently across adapters over time. | Introduce one shared auth error -> HTTP status mapper and consume it from both route and guard adapters. |
| AUTH-LDR-06 | HIGH | RESOLVED | Contract test ownership for status mapping was incomplete and permissive for login semantics. | `backend/src/infrastructure/http/routes/auth.routes.contract.test.ts`, `backend/src/infrastructure/http/auth/auth-access-control.test.ts`, `docs/features/auth-access-control/TEST-SPEC.md` | Route contract evidence is now deterministic for login/logout/introspect and no longer accepts unstable statuses. | None. |

## Minimal Remediation Backlog

1. Centralize auth error -> HTTP status mapping in one adapter-level mapper.
2. Wire `auth.routes.ts` and `auth.guard.ts` to the shared mapper.

## Layer Verdict

**FLAG** - blocker semantics are resolved; remaining work is mapper-centralization hardening.
