---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control Decisions
summary: Key decisions and scope boundaries for reusable auth contracts.
status: implemented
pillar: platform
domain: auth-access-control-decisions
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
includes: []
---

## Confirmed Decisions

- Permission naming format is `microservice.scope.action`.
- Authorization is deny-by-default when no permission match exists.
- Deny permission matches override allow matches.
- Wildcard support is allowed (`service.scope.*`, `service.*.*`, `*.*.*`) and evaluated by precedence.
- Standard auth error payload is `{ code, message, details }`.
- Token metadata is persisted for revocation and introspection.
- Protected route guard order is authenticate first, authorize second.
- JWT carries only token metadata and session identity (`sid`, `jti`, `iat`, `exp`); principal and permissions are resolved server-side from session.
- Login and logout are in scope as first-class operations backed by session lifecycle transitions.
- Session TTL is fixed at 8 hours.
- Session expiry rejects requests as `AUTH_REQUIRED`.
- Token revocation evidence is persisted in database-backed storage.
- Effective permissions are resolved from `Principal.roleKeys` plus `Principal.directPermissions` using permission grants.
- Permission catalog governance is registry-first.
- Login credential contract is `identifier + password`.
- Login risk policy deny conditions are fixed: blocked IP reputation, >=5 failed attempts in 15 minutes, or missing user-agent signal.
- `IssueAccessToken` session-activity violation maps to `AUTH_REQUIRED`.
- `TokenRevoked.reason` uses enum values: `LOGOUT_TARGETED`, `LOGOUT_ALL_SESSION_TOKENS`, `ADMIN_FORCED_LOGOUT`.
- Introspection inactive responses must include deterministic `inactiveReason` precedence.

## Open Decisions

- Session inactivity timeout behavior beyond fixed 8-hour TTL (no sliding window in v1).

## Deferred Scope

- Multi-factor authentication policy.
- Refresh-token rotation and token-family replay protections.
- Fine-grained attribute-based access control (ABAC) beyond permission keys.
- Cross-region key management and rotation operations.
