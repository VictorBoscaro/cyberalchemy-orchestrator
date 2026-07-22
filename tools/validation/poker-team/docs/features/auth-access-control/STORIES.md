---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control User Stories
summary: Capability-scoped user stories and acceptance scenarios for authentication and authorization.
status: implemented
pillar: platform
domain: auth-access-control-stories
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
updatedAt: 2026-04-16
dependencies:
  - SPEC.md
includes: []
---

# User Stories: Authentication and Access Control

> Navigate by capability: [System Bootstrap](#system-bootstrap) · [Login](#login) · [Authenticate Request](#authenticate-request) · [Authorize Request](#authorize-request) · [Logout](#logout) · [Introspect Token](#introspect-token) · [Browse Permission Catalog](#browse-permission-catalog)

---

## System Bootstrap

### US-10: Admin principal is auto-created on first boot

As an **operations engineer**, I want **the application to auto-create an admin principal on first boot**, so that **I can immediately log in and configure the system without manual database setup**.

**Given** the application starts and no principal with identifier matching `ADMIN_USERNAME` (default: `admin`) exists
**When** the bootstrap seed runs during startup
**Then** an admin principal is created with a randomly generated password, bcrypt-hashed (cost 12), roleKeys `['admin']`, and the password is logged to stdout

**Acceptance checks**

- [ ] Admin principal created with `subjectType: 'user'`, `status: 'ACTIVE'` ([SeedSystemBootstrap C2](operations.md#seedsystembootstrap)).
- [ ] Password is at least 24 characters with >= 128 bits of entropy ([SeedSystemBootstrap R2](operations.md#seedsystembootstrap)).
- [ ] Credential hash uses bcrypt with cost factor 12 ([SeedSystemBootstrap R3](operations.md#seedsystembootstrap)).
- [ ] Password is printed to stdout and never persisted in plaintext.
- [ ] `ADMIN_USERNAME` env var overrides the default `admin` identifier.

**Capability links:** [System Bootstrap](capabilities/system-bootstrap.md)

### US-11: Role permission grants are seeded on every boot

As the **auth system**, I want **all predefined role → permission grants to be synced on every startup**, so that **new permissions added to role definitions are automatically available**.

**Given** the application starts (first or subsequent boot)
**When** the bootstrap seed runs
**Then** all 4 role definitions (admin, manager, coach, player) have their permission grants created in `auth_permission_grants` with effect `ALLOW`

**Acceptance checks**

- [ ] Admin role has grants for `player-management.*.*`, `auth-access-control.admin.*`, `player-makeup.*.*`, `financial-settlement.*.*`, `player-onboarding.*.*`, `player-stats.*.*` ([RoleDefinition](domain.md#roledefinition)).
- [ ] Manager role has scoped grants per [RoleDefinition](domain.md#roledefinition) table.
- [ ] Coach role has read-only grants for assigned player data per [RoleDefinition](domain.md#roledefinition) table.
- [ ] Player role has self-scoped grants per [RoleDefinition](domain.md#roledefinition) table.
- [ ] Grant sync is idempotent — existing grants are not duplicated ([SeedSystemBootstrap R4](operations.md#seedsystembootstrap)).
- [ ] No grants are removed during sync (additive only).

**Capability links:** [System Bootstrap](capabilities/system-bootstrap.md)

### US-12: Subsequent boots skip admin creation but sync grants

As the **auth system**, I want **to skip admin creation if the principal already exists**, so that **credentials are not regenerated and existing admin access is preserved**.

**Given** the admin principal already exists in the database
**When** the application restarts
**Then** principal creation is skipped (R1) and role grants are synced (R4)

**Acceptance checks**

- [ ] No new principal is created.
- [ ] No password is logged.
- [ ] Role grants that are missing are added.
- [ ] Pre-existing grants remain unchanged.

**Capability links:** [System Bootstrap](capabilities/system-bootstrap.md)

---

## Login

### US-01: User logs in with valid credentials

As an **end user**, I want **to authenticate with my credentials**, so that **I receive a session and access token for API calls**.

**Given** a principal exists with status ACTIVE and valid credentials
**When** I submit identifier and secret to POST /auth/login
**Then** a session is created with 8h TTL, an access token is issued with `sid` claim, and LoginSucceeded + TokenIssued events are emitted

**Acceptance checks**

- [ ] Session expiration equals login instant + 8h ([Login C1](operations.md#login)).
- [ ] Effective permissions are resolved from roleKeys + directPermissions + grants ([Login C2](operations.md#login)).
- [ ] JWT contains `sid`, `jti`, `iat`, `exp` claims ([IssueAccessToken](operations.md#issueaccesstoken)).
- [ ] Response matches `{ accessToken, expiresAt, sessionId }` ([POST /auth/login](interfaces.md#post-authlogin)).

**Capability links:** [Login](capabilities/login.md)

### US-02: Login rejected for invalid credentials or disabled principal

As the **auth system**, I want **to reject invalid login attempts deterministically**, so that **unauthorized access is prevented and errors are explicit**.

**Given** credentials are invalid, principal is disabled, or risk policy denies
**When** login is attempted
**Then** the API returns the specific error code matching the failed rule

**Acceptance checks**

- [ ] Missing/disabled principal returns `PRINCIPAL_DISABLED` ([Login R1](operations.md#login)).
- [ ] Wrong password returns `INVALID_CREDENTIALS` ([Login R2](operations.md#login)).
- [ ] Blocked IP, ≥5 failed attempts, or missing user-agent returns `FORBIDDEN` ([Login R3](operations.md#login)).
- [ ] No session or token is created on failure.

**Capability links:** [Login](capabilities/login.md)

---

## Authenticate Request

### US-03: Protected endpoint validates bearer token and builds auth context

As an **API gateway**, I want **to validate the bearer token on every protected request**, so that **only authenticated principals with active sessions can proceed**.

**Given** a request includes a valid, non-expired, non-revoked bearer token with a `sid` claim linked to an active session
**When** the request passes through AuthenticateRequest
**Then** an AuthContext is built with principalId, sessionId, permissions, and tokenId from the session

**Acceptance checks**

- [ ] Auth context permissions come from server-side session, not from JWT claims ([JWTClaimsToAuthContext](mappings.md#jwtclaimstoauthcontext)).
- [ ] The auth context is available for downstream AuthorizeRequest ([AuthorizeRequestFlow](workflows.md#authorizerequestflow)).

**Capability links:** [Authenticate Request](capabilities/authenticate-request.md)

### US-04: Authentication fails deterministically per rule

As the **auth system**, I want **each authentication failure to map to a specific error code**, so that **callers can distinguish between token issues and session issues**.

**Given** a request with a missing, invalid, expired, or revoked token, or with a dead session
**When** AuthenticateRequest processes it
**Then** the matching error code is returned

**Acceptance checks**

- [ ] No bearer prefix → `AUTH_REQUIRED` ([R1](operations.md#authenticaterequest)).
- [ ] Bad signature → `INVALID_TOKEN` ([R2](operations.md#authenticaterequest)).
- [ ] Expired token → `TOKEN_EXPIRED` ([R3](operations.md#authenticaterequest)).
- [ ] Revoked token → `TOKEN_REVOKED` ([R4](operations.md#authenticaterequest)).
- [ ] Missing `sid` → `INVALID_TOKEN` ([R5](operations.md#authenticaterequest)).
- [ ] Inactive session → `AUTH_REQUIRED` ([R6](operations.md#authenticaterequest)).

**Capability links:** [Authenticate Request](capabilities/authenticate-request.md)

---

## Authorize Request

### US-05: Route permission is enforced with deny-overrides policy

As an **API gateway**, I want **to check the required permission against the principal's effective permissions**, so that **only explicitly allowed access proceeds**.

**Given** a request is authenticated and the route requires a specific permission
**When** AuthorizeRequest evaluates the permission
**Then** access is allowed only if a matching allow exists with no overriding deny

**Acceptance checks**

- [ ] Exact allow match with no deny → allowed ([AuthorizeRequest R2](operations.md#authorizerequest)).
- [ ] Any deny match → `FORBIDDEN` regardless of allow entries ([AuthorizeRequest R3](operations.md#authorizerequest)).
- [ ] Scoped wildcard (`service.read.*`) matches when no deny exists ([PermissionResolutionPolicy](workflows.md#permissionresolutionpolicy)).
- [ ] No matches → default deny → `FORBIDDEN`.
- [ ] AccessDenied event emitted on rejection ([AccessDenied](events.md#accessdenied)).

**Capability links:** [Authorize Request](capabilities/authorize-request.md)

---

## Logout

### US-06: User terminates own session

As an **authenticated user**, I want **to logout and terminate my session**, so that **my tokens are revoked and the session cannot be used again**.

**Given** I am authenticated and own the target session
**When** I send POST /auth/logout with my sessionId
**Then** the session transitions to TERMINATED, active tokens are revoked, and LogoutCompleted + TokenRevoked events are emitted

**Acceptance checks**

- [ ] Session state transitions `ACTIVE → TERMINATED` ([SessionLifecycle](states.md#sessionlifecycle)).
- [ ] All linked active tokens transition `ACTIVE → REVOKED` ([TokenLifecycle](states.md#tokenlifecycle)).
- [ ] Revocation evidence is persisted ([Logout R3](operations.md#logout)).
- [ ] Subsequent requests with revoked tokens receive `TOKEN_REVOKED`.

**Capability links:** [Logout](capabilities/logout.md)

### US-07: Admin force-terminates another user's session

As an **admin**, I want **to terminate any user's session**, so that **I can respond to security incidents**.

**Given** I have `auth-access-control.admin.logoutAnySession` permission
**When** I send logout for a session I don't own
**Then** the target session is terminated as in US-06

**Acceptance checks**

- [ ] Non-admin caller without ownership returns `FORBIDDEN` ([Logout R2](operations.md#logout)).
- [ ] Admin with permission succeeds for any active session.

**Capability links:** [Logout](capabilities/logout.md)

---

## Introspect Token

### US-08: Inspect token state with explicit inactive reason

As a **security operator**, I want **to introspect a token and see why it's inactive**, so that **I can diagnose auth failures**.

**Given** I have `auth-access-control.read.introspectToken` permission
**When** I call GET /auth/introspect with a token value
**Then** I receive the active state, claims, and a deterministic inactive reason if not active

**Acceptance checks**

- [ ] Active token returns `{ active: true, principalId, exp, iat, scopes }` ([IntrospectToken](queries.md#introspecttoken)).
- [ ] Revoked token returns `{ active: false, inactiveReason: 'TOKEN_REVOKED' }`.
- [ ] Expired token returns `{ active: false, inactiveReason: 'TOKEN_EXPIRED' }`.
- [ ] Terminated session returns `{ active: false, inactiveReason: 'SESSION_TERMINATED' }`.
- [ ] Unknown token returns `{ active: false, inactiveReason: 'NOT_FOUND' }`.
- [ ] Reason precedence: NOT_FOUND > TOKEN_REVOKED > TOKEN_EXPIRED > SESSION_TERMINATED > SESSION_EXPIRED.

**Capability links:** [Introspect Token](capabilities/introspect-token.md)

---

## Browse Permission Catalog

### US-09: Admin lists available permissions

As an **admin**, I want **to browse the permission catalog**, so that **I can configure roles and grants from known keys**.

**Given** I have admin access
**When** I query the permission catalog with optional namespace filter
**Then** I receive all matching permission keys with descriptions and active/deprecated status

**Acceptance checks**

- [ ] Catalog includes canonical keys like `auth-access-control.read.introspectToken` ([GetPermissionCatalog](queries.md#getpermissioncatalog)).
- [ ] `includeDeprecated: false` (default) omits deprecated keys.
- [ ] Namespace filter scopes results to matching service prefix.

**Capability links:** [Browse Permission Catalog](capabilities/browse-permission-catalog.md)

---

## Story Coverage Matrix

| Capability | Story IDs | Covered Concepts | Notes |
| ---------- | --------- | ---------------- | ----- |
| Login | US-01, US-02 | Login, IssueAccessToken, SessionLifecycle, TokenLifecycle, LoginSucceeded, TokenIssued | Happy path + all 3 rejection rules |
| Authenticate Request | US-03, US-04 | AuthenticateRequest, JWTClaimsToAuthContext, AuthorizeRequestFlow | Happy path + all 6 failure rules |
| Authorize Request | US-05 | AuthorizeRequest, PermissionResolutionPolicy, AccessDenied | Deny-overrides, wildcards, default deny |
| Logout | US-06, US-07 | Logout, SessionLifecycle, TokenLifecycle, TokenRevoked, LogoutCompleted | Self-logout + admin force-logout |
| Introspect Token | US-08 | IntrospectToken, AccessToken, Session | All 5 inactive reasons with precedence |
| Browse Permission Catalog | US-09 | GetPermissionCatalog, PermissionGrant | Namespace filter + deprecated toggle |
