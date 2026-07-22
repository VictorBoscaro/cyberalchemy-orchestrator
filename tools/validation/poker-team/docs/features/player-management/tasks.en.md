---
id: player-management
feature: player-management
title: Player Management Tasks
summary: Dependency-ordered execution tasks for implementing and validating player management contracts.
status: implemented
pillar: operations
domain: player-management-delivery
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
  - web-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
  - mappings.md
includes: []
---

## Ordered Tasks

1. docs: finalize canonical validation rules for `name`, `email`, `currentLimit`, and `initialBankroll`.
2. backend: create player limits config module with allowed values `NL20`, `NL40`, `NL60`, `NL80`, `NL100`.
3. backend: add typed request schema validation for `POST /players` and reject malformed payloads with deterministic 400 errors.
4. backend: implement canonical email key normalization (`lowercase + remove special chars`) before uniqueness checks.
5. backend: enforce duplicate email conflict mapping to 409 with code `DUPLICATE_EMAIL`.
6. backend: enforce route guards using [AuthenticateRequest](../auth-access-control/operations.md#authenticaterequest) and [AuthorizeRequest](../auth-access-control/operations.md#authorizerequest) from auth-access-control.
7. backend: align repository and route error translation to standardized payload shape `{ code, message, details }`.
8. backend: add route-level tests for create success, validation failures, duplicate email conflict, and authenticated permission checks.
9. web: align player creation and player list adapters to strict response/error contracts and authorization flow.
10. shared: publish request/response and permission contract types consumed by backend and web.
11. docs: update feature status to implemented after verification checklist passes.
12. docs: keep player route permissions synchronized with auth-access-control permission catalog and login/logout/session lifecycle assumptions.

## Ownership Labels

- docs: contract precision, constraints, and lifecycle updates.
- backend: validation, persistence constraints, error handling, and tests.
- web: API adapter alignment and error rendering behavior.
- shared: contract typing and cross-layer DTO stability.

## Verification Checklist

1. `POST /players` rejects invalid body fields with 400.
2. `POST /players` returns 409 when email already exists.
3. Player routes require JWT and route-specific permission strings.
4. `GET /players` returns persisted entities including bankroll and makeup.
5. `GET /players/overview` supports `periodDays` and returns period-based derived metrics.
6. Route test suite includes positive and negative path coverage.

## Done Criteria

- All player-management endpoints conform to documented interface contracts.
- Validation and uniqueness rules are enforced at runtime.
- Feature docs and implementation behavior are aligned with no unresolved critical gaps.
