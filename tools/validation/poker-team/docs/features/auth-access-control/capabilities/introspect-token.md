# Introspect Token

> ← Back to [Module Index](../SPEC.md#capabilities) · Stories: [US-08](../STORIES.md#us-08-inspect-token-state-with-explicit-inactive-reason)

Inspect token active/inactive state with explicit inactive reason.

## Aspect Map

| Aspect | Concept | Summary |
| ------ | ------- | ------- |
| Query | [IntrospectToken](../queries.md#introspecttoken) | Returns active state, claims, and deterministic inactive reason |
| Interface | [GET /auth/introspect](../interfaces.md#get-authintrospect) | `auth-access-control.read.introspectToken` permission |

## Rules

| ID | Rule | Formal |
| -- | ---- | ------ |
| R1 | Token lookup must be deterministic | `tokenRecord = findToken(token)` |
| R2 | Active depends on token and session | `active = (revokedAt = null) and (now < expiresAt) and (session.status = ACTIVE)` |
| R3 | Inactive reason must be explicit | `active = false => inactiveReason is one of documented values` |

## Inactive Reason Precedence

When `active = false`, the reason follows this strict precedence:

1. `NOT_FOUND` — token record does not exist
2. `TOKEN_REVOKED` — `revokedAt != null`
3. `TOKEN_EXPIRED` — `now >= expiresAt`
4. `SESSION_TERMINATED` — session status is TERMINATED
5. `SESSION_EXPIRED` — session status is EXPIRED

## Output Shape

| Field | Type | When |
| ----- | ---- | ---- |
| active | boolean | Always |
| principalId | string | When active |
| exp | integer | Always (unix timestamp) |
| iat | integer | Always (unix timestamp) |
| scopes | string[] | When active and `includeScopes = true` |
| inactiveReason | string | Only when `active = false` |

## Domain Concepts Used

- [AccessToken](../domain.md#accesstoken) — introspected token
- [Session](../domain.md#session) — session state affects active decision
