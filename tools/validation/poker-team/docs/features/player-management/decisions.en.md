---
id: player-management
feature: player-management
title: Player Management Decisions
summary: Decision log for player identity constraints, validation boundaries, and API error semantics.
status: implemented
pillar: operations
domain: player-management-decisions
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - backend-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
includes: []
---

## Confirmed Decisions

- `email` uniqueness uses canonical normalization key: lowercase plus special character stripping.
- `bankroll` and `makeup` are non-negative integer monetary fields.
- `currentLimit` comes from configured allowed limits module.
- Initial allowed limits are `NL20`, `NL40`, `NL60`, `NL80`, `NL100`.
- `initialBankroll` defaults to zero when omitted.
- Player default status at creation is `OBSERVATION`.
- Error payload contract is `{ code, message, details }`.
- Duplicate email conflict code is `DUPLICATE_EMAIL`.
- Route auth model reuses auth-access-control contracts: login/logout/session lifecycle plus `AuthenticateRequest` and `AuthorizeRequest` for protected routes.
- Overview query is period-based with `periodDays` parameter (default 30).

## Open Decisions

- None at this stage.

## Deferred Scope

- Player lifecycle write operations beyond create (activate/inactivate/observation transitions).
- Player profile mutation endpoint and audit trail semantics.
