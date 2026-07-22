---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control Layering Alignment Plan
summary: Dependency-ordered minimal plan to normalize login abuse semantics and centralize route status mapping ownership.
status: in-progress
pillar: platform
domain: auth-access-control-layering
audience:
  - developers
  - operations
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
  - LAYERING-ALIGNMENT-REPORT.md
includes: []
auditor: domainspec-layering-auditor
auditedAt: 2026-04-24
domainspecVersion: 1.8.2
sourceReport: LAYERING-ALIGNMENT-REPORT.md
---

# Layering Alignment Plan: auth-access-control

## Objective

Track completed remediation and remaining hardening for:

1. Login abuse denial semantics (`FORBIDDEN` vs `429` split).
2. Route status mapping ownership spread across adapters and weak contract evidence.

## Dependency-Ordered Backlog

| Task ID | Layer | Task | Files | Depends On | Status |
| --- | --- | --- | --- | --- | --- |
| AUTH-LYP-01 | docs + product semantics | Choose and record canonical login abuse status model (`FORBIDDEN` -> `403`). | `docs/features/auth-access-control/interfaces.md`, `docs/features/auth-access-control/TEST-SPEC.md`, `docs/features/auth-access-control/UI-SPEC.md`, `docs/features/auth-access-control/STORIES.md` | report findings | completed |
| AUTH-LYP-02 | backend (domain/use-case) | Keep domain login risk policy on `FORBIDDEN` for all R3 abuse denials. | `backend/src/domain/auth-access-control/login-risk-policy.ts`, `backend/src/use-cases/auth-access-control/login.ts` | AUTH-LYP-01 | completed |
| AUTH-LYP-03 | backend (http adapter) | Centralize auth error -> HTTP status mapping in one adapter mapper and consume it from both route and guard adapters. | `backend/src/infrastructure/http/auth/` (new mapper), `backend/src/infrastructure/http/routes/auth.routes.ts`, `backend/src/infrastructure/http/auth/auth.guard.ts` | AUTH-LYP-01, AUTH-LYP-02 | pending |
| AUTH-LYP-04 | tests (contract) | Make route contract coverage authoritative for login/logout/introspect with deterministic status assertions and standard payload checks. | `backend/src/infrastructure/http/routes/auth.routes.contract.test.ts`, `backend/src/infrastructure/http/auth/auth-access-control.test.ts` | AUTH-LYP-03 | completed |
| AUTH-LYP-05 | web adapter | Sync login error messaging table to canonical backend statuses (remove unreachable branches). | `apps/web/src/components/auth/LoginForm.tsx`, `docs/features/auth-access-control/UI-SPEC.md` | AUTH-LYP-01, AUTH-LYP-04 | completed |

## Validation Steps

1. Run route contract suite:
   - `cd backend && npm run -s test -- src/infrastructure/http/routes/auth.routes.contract.test.ts`
2. Run focused scaffold contract checks:
   - `cd backend && npm run -s test -- src/infrastructure/http/auth/auth-access-control.test.ts -t "AUTH-API-001|AUTH-API-003|AUTH-API-004"`
3. Confirm no duplicated inline status mapping branches remain:
   - `cd backend && rg "error\.code ===|status =" src/infrastructure/http/routes/auth.routes.ts src/infrastructure/http/auth/auth.guard.ts`
4. Confirm docs/test parity on login abuse semantics:
   - `cd /home/vrondelli/projects/poker-team && rg "429|FORBIDDEN|too many attempts|Login R3" docs/features/auth-access-control/{interfaces.md,operations.md,UI-SPEC.md,TEST-SPEC.md,STORIES.md,capabilities/login.md}`

## Exit Criteria

- One canonical login abuse status model is present across domain/use-case/http/docs/tests.
- `auth.routes.contract.test.ts` contains deterministic assertions for `/auth/login`, `/auth/logout`, and `/auth/introspect`.
- Status mapping ownership is centralized in one HTTP mapper consumed by both guard and routes.
