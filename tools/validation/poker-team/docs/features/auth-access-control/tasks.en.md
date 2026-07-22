---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control Tasks
summary: Wave-ordered implementation plan for reusable auth contracts — 10 waves, 42 tasks, 84 TEST-SPEC obligations.
status: implemented
pillar: platform
domain: auth-access-control-delivery
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
  - mappings.md
  - queries.md
  - states.md
  - events.md
  - workflows.md
  - TEST-SPEC.md
includes: []
---

# Auth Access Control — Implementation Plan

## Planning Context

- **Complexity:** HIGH (17 concepts, 84 test obligations, 6 capabilities, cross-cutting drift remediation)
- **Orchestration:** GSD-phase with DomainSpec normalization
- **Existing code:** Partial infra in `backend/src/infrastructure/http/auth/` — auth.guard.ts, session-store.ts, permission-checker.service.ts
- **Scaffold tests:** 84 `it.todo()` stubs in auth-access-control.scaffold.test.ts
- **Status:** `planned` → `in-progress` at W0 start

## Audit Findings (Pre-Implementation)

| Finding                                                                                             | Severity | Remediation Wave |
| --------------------------------------------------------------------------------------------------- | -------- | ---------------- |
| Permission format: colon-style (`admin:*`, `makeup:write`) vs canonical `microservice.scope.action` | HIGH     | W0               |
| No deny-override in permission checker — only checks allow matches                                  | HIGH     | W4               |
| Token revocation not checked in auth guard (AuthenticateRequest R4)                                 | HIGH     | W4               |
| Session expiration not enforced — `resolveAuthSessionBySid` ignores `expiresAt`                     | MEDIUM   | W4               |
| Non-ACTIVE session returns `PRINCIPAL_DISABLED` instead of `AUTH_REQUIRED`                          | LOW      | W4               |
| 2-part permission keys in onboarding (`player-onboarding.review`) need 3-part format                | MEDIUM   | W0               |

## Assumptions

- A1: PostgreSQL + Drizzle ORM is the persistence target (consistent with player-stats).
- A2: JWT signing uses `process.env.JWT_SECRET` (existing pattern in auth.guard.ts).
- A3: Event emission uses in-process domain events (no external broker in v1).
- A4: Credential store for principals is seeded — Login verifies against existing records.
- A5: Permission catalog is config/seed-driven; no runtime admin CRUD in v1.

---

## W0 — Foundation & Permission Format Migration

**Gate:** All existing routes use canonical 3-part permission keys. Directory structure created.

| #   | Task                                                                                                                                                                                                 | Type    | Concepts                                 | Files                |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ---------------------------------------- | -------------------- |
| 1   | Create `backend/src/domain/auth-access-control/` directory                                                                                                                                           | backend | —                                        | new dir              |
| 2   | Create `backend/src/use-cases/auth-access-control/` directory                                                                                                                                        | backend | —                                        | new dir              |
| 3   | Migrate `requireAdminPermission` from `admin:*` to `auth-access-control.admin.*`                                                                                                                     | backend | [PermissionKey](domain.md#permissionkey) | auth.guard.ts        |
| 4   | Migrate `requireManagerPermission` from `makeup:write` to `player-makeup.write.manageMakeup`                                                                                                         | backend | [PermissionKey](domain.md#permissionkey) | auth.guard.ts        |
| 5   | Migrate `requirePlayerPermission` from `makeup:read` to `player-makeup.read.viewMakeup`                                                                                                              | backend | [PermissionKey](domain.md#permissionkey) | auth.guard.ts        |
| 6   | Migrate makeup.routes.ts permissions: `makeup:read` → `player-makeup.read.viewMakeup`, `makeup:write` → `player-makeup.write.manageMakeup`, `makeup:policy:read` → `player-makeup.policy.readPolicy` | backend | [PermissionKey](domain.md#permissionkey) | makeup.routes.ts     |
| 7   | Migrate settlement.routes.ts permission: `settlement:write` → `financial-settlement.write.recordSettlement`                                                                                          | backend | [PermissionKey](domain.md#permissionkey) | settlement.routes.ts |
| 8   | Migrate onboarding.routes.ts permissions: `player-onboarding.review` → `player-onboarding.review.evaluateApplication`                                                                                | backend | [PermissionKey](domain.md#permissionkey) | onboarding.routes.ts |
| 9   | Update session-store.ts test seeds and any test fixtures using old permission keys                                                                                                                   | backend | —                                        | test files           |

**Checkpoint:** `npx tsc --noEmit` clean + existing test suite passes with new keys.

---

## W1 — Domain Entities, VOs, Enums

**Gate:** All domain types compile and export from barrel. No logic yet.

| #   | Task                                                                                                                            | Type    | Concepts                                                                       | Files                                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------ | ------------------------------------------------------- |
| 10  | Define `AuthErrorCode` enum with 6 values                                                                                       | backend | [auth-access-control.AuthErrorCode](domain.md#autherrorcode)                   | `domain/auth-access-control/auth-error-code.enum.ts`    |
| 11  | Define `Principal` entity type (id, subjectType, status, roleKeys, directPermissions)                                           | backend | [auth-access-control.Principal](domain.md#principal)                           | `domain/auth-access-control/principal.entity.ts`        |
| 12  | Define `Session` entity type (id, principalId, status, effectivePermissions, createdAt, expiresAt)                              | backend | [auth-access-control.Session](domain.md#session)                               | `domain/auth-access-control/session.entity.ts`          |
| 13  | Define `AccessToken` entity type (tokenId, sessionId, issuedAt, expiresAt, revokedAt, scope)                                    | backend | [auth-access-control.AccessToken](domain.md#accesstoken)                       | `domain/auth-access-control/access-token.entity.ts`     |
| 14  | Define `PermissionGrant` entity type (grantId, granteeType, granteeKey, permissionKey, effect, createdAt)                       | backend | [auth-access-control.PermissionGrant](domain.md#permissiongrant)               | `domain/auth-access-control/permission-grant.entity.ts` |
| 15  | Define `AuthContext` VO and `PermissionKey` VO                                                                                  | backend | [AuthContext](domain.md#authcontext), [PermissionKey](domain.md#permissionkey) | `domain/auth-access-control/auth-context.vo.ts`         |
| 16  | Define repository contracts: `AuthSessionRepository`, `AuthTokenRepository`, `PrincipalRepository`, `PermissionGrantRepository` | backend | —                                                                              | `domain/auth-access-control/auth.repository.ts`         |
| 17  | Define domain event types: `LoginSucceeded`, `TokenIssued`, `TokenRevoked`, `LogoutCompleted`, `AccessDenied`                   | backend | [events.md](events.md)                                                         | `domain/auth-access-control/auth.events.ts`             |
| 18  | Domain barrel export `index.ts`                                                                                                 | backend | —                                                                              | `domain/auth-access-control/index.ts`                   |

**Checkpoint:** `npx tsc --noEmit` clean.

---

## W2 — State Machines & Validation

**Gate:** State transitions enforced; invariant validators exported.

| #   | Task                                                                                                                                                                             | Type    | Concepts                                                           | Files                                             |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| 19  | Implement `SessionLifecycle` state machine: ACTIVE → TERMINATED, ACTIVE → EXPIRED, invalid transitions rejection                                                                 | backend | [auth-access-control.SessionLifecycle](states.md#sessionlifecycle) | `domain/auth-access-control/session-lifecycle.ts` |
| 20  | Implement `TokenLifecycle` state machine: ACTIVE → EXPIRED, ACTIVE → REVOKED, invalid transitions rejection                                                                      | backend | [auth-access-control.TokenLifecycle](states.md#tokenlifecycle)     | `domain/auth-access-control/token-lifecycle.ts`   |
| 21  | Implement domain invariant validators: canonical permission key regex (I1), expiresAt > issuedAt (I2), revoked ⇒ not active (I3), unique permissions (I4), JWT sid required (I5) | backend | [domain.md invariants](domain.md#invariants)                       | `domain/auth-access-control/auth.validation.ts`   |

**Checkpoint:** `npx tsc --noEmit` clean.

---

## W3 — Login + IssueAccessToken Use Cases

**Gate:** Login creates session, issues JWT, emits events.

| #   | Task                                                                                                                                                                                                                              | Type    | Concepts                                                                         | Files                                                 |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 22  | Implement `loginUseCase` with R1 (principal active), R2 (credential verification), R3 (risk policy: blocked IP, ≥5 failed attempts, missing user-agent), C1 (session expiresAt = now + 8h), C2 (effective permissions resolution) | backend | [auth-access-control.Login](operations.md#login)                                 | `use-cases/auth-access-control/login.ts`              |
| 23  | Implement `issueAccessTokenUseCase` with R1 (session active), R2 (ttlSeconds bounds), C1 (token expiresAt), C2 (JWT claims {sid, jti, iat, exp})                                                                                  | backend | [auth-access-control.IssueAccessToken](operations.md#issueaccesstoken)           | `use-cases/auth-access-control/issue-access-token.ts` |
| 24  | Implement `LoginRequestToSession` mapping                                                                                                                                                                                         | backend | [LoginRequestToSession](mappings.md#loginrequesttosession)                       | `use-cases/auth-access-control/login.ts` (inline)     |
| 25  | Emit `LoginSucceeded` + `TokenIssued` events from login use case                                                                                                                                                                  | backend | [LoginSucceeded](events.md#loginsucceeded), [TokenIssued](events.md#tokenissued) | `use-cases/auth-access-control/login.ts`              |

**Tests (W3):** AUTH-RULE-001–003, AUTH-RULE-004–005, AUTH-CALC-001–004, AUTH-POST-001–002, AUTH-ERR-001–002, AUTH-EVT-001–002, AUTH-MAP-001–002, AUTH-STATE-001, AUTH-STATE-008 → **20 obligations**

**Checkpoint:** W3 tests pass. `npx tsc --noEmit` clean.

---

## W4 — AuthenticateRequest + AuthorizeRequest (Drift Remediation)

**Gate:** Auth guard refactored to use domain operations. Deny-override + revocation enforced.

| #   | Task                                                                                                                                                                                                         | Type    | Concepts                                                                         | Files                                                            |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 26  | Implement `authenticateRequestUseCase` with R1–R6, C1 (auth context). Replace ad-hoc logic in auth.guard.ts                                                                                                  | backend | [auth-access-control.AuthenticateRequest](operations.md#authenticaterequest)     | `use-cases/auth-access-control/authenticate-request.ts`          |
| 27  | Implement `JWTClaimsToAuthContext` mapping with validation (missing sid/jti → INVALID_TOKEN, expired exp → TOKEN_EXPIRED)                                                                                    | backend | [auth-access-control.JWTClaimsToAuthContext](mappings.md#jwtclaimstoauthcontext) | `use-cases/auth-access-control/authenticate-request.ts` (inline) |
| 28  | Implement `authorizeRequestUseCase` with R1 (canonical format), R2 (allow match), R3 (deny override). Replace simple `hasRequiredPermission`                                                                 | backend | [auth-access-control.AuthorizeRequest](operations.md#authorizerequest)           | `use-cases/auth-access-control/authorize-request.ts`             |
| 29  | Implement `PermissionResolutionPolicy`: deny > exact allow > scoped wildcard > global wildcard > default deny                                                                                                | backend | [PermissionResolutionPolicy](workflows.md#permissionresolutionpolicy)            | `domain/auth-access-control/permission-resolution.ts`            |
| 30  | Implement `RoutePermissionBinding` mapping                                                                                                                                                                   | backend | [RoutePermissionBinding](mappings.md#routepermissionbinding)                     | `use-cases/auth-access-control/authorize-request.ts` (inline)    |
| 31  | Refactor `auth.guard.ts` to delegate to `authenticateRequestUseCase` + `authorizeRequestUseCase`. Fix: session expiration check, token revocation check, error code for non-ACTIVE session → `AUTH_REQUIRED` | backend | [auth-access-control.AuthorizeRequestFlow](workflows.md#authorizerequestflow)    | auth.guard.ts                                                    |
| 32  | Emit `AccessDenied` event on FORBIDDEN                                                                                                                                                                       | backend | [AccessDenied](events.md#accessdenied)                                           | `use-cases/auth-access-control/authorize-request.ts`             |

**Tests (W4):** AUTH-RULE-006–014, AUTH-CALC-005–006, AUTH-POST-003–004, AUTH-ERR-003–004, AUTH-MAP-003–004, AUTH-MAP-007–008, AUTH-WF-001–005 → **25 obligations**

**Checkpoint:** W4 tests pass. All existing consumer routes still pass with refactored guard.

---

## W5 — Logout + Token Revocation

**Gate:** Session termination + token revocation with evidence persistence.

| #   | Task                                                                                                                                            | Type    | Concepts                                                                             | Files                                              |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------ | -------------------------------------------------- |
| 33  | Implement `logoutUseCase` with R1 (session active), R2 (ownership or admin permission), R3 (revocation evidence persisted), C1 (revocation set) | backend | [auth-access-control.Logout](operations.md#logout)                                   | `use-cases/auth-access-control/logout.ts`          |
| 34  | Implement `LogoutRequestToTermination` mapping with defaults (revokeAllSessionTokens = false) and validation                                    | backend | [LogoutRequestToTermination](mappings.md#logoutrequesttotermination)                 | `use-cases/auth-access-control/logout.ts` (inline) |
| 35  | Emit `TokenRevoked` + `LogoutCompleted` events from logout use case                                                                             | backend | [TokenRevoked](events.md#tokenrevoked), [LogoutCompleted](events.md#logoutcompleted) | `use-cases/auth-access-control/logout.ts`          |

**Tests (W5):** AUTH-RULE-015–017, AUTH-CALC-007, AUTH-POST-005, AUTH-ERR-005, AUTH-EVT-003–004, AUTH-MAP-005–006, AUTH-STATE-002, AUTH-STATE-010 → **12 obligations**

**Checkpoint:** W5 tests pass.

---

## W6 — Queries (IntrospectToken + GetPermissionCatalog)

**Gate:** Read-model queries with deterministic outputs.

| #   | Task                                                                                                                                                        | Type    | Concepts                                                                    | Files                                                     |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------- | --------------------------------------------------------- |
| 36  | Implement `introspectTokenUseCase` with R1–R3, inactive reason precedence: NOT_FOUND > TOKEN_REVOKED > TOKEN_EXPIRED > SESSION_TERMINATED > SESSION_EXPIRED | backend | [auth-access-control.IntrospectToken](queries.md#introspecttoken)           | `use-cases/auth-access-control/introspect-token.ts`       |
| 37  | Implement `getPermissionCatalogUseCase` with namespace filter and includeDeprecated flag                                                                    | backend | [auth-access-control.GetPermissionCatalog](queries.md#getpermissioncatalog) | `use-cases/auth-access-control/get-permission-catalog.ts` |

**Tests (W6):** AUTH-QUERY-001–004 → **4 obligations**

**Checkpoint:** W6 tests pass.

---

## W7 — REST Routes + Drizzle Schema

**Gate:** All 4 AuthAPI endpoints live. Persistent storage for sessions, tokens, grants.

| #   | Task                                                                                                                                                                                    | Type    | Concepts                                                            | Files                                                |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| 38  | Add Drizzle schema: `auth_sessions`, `auth_access_tokens`, `auth_permission_grants`, `auth_principals` tables with proper enums                                                         | backend | [domain.md](domain.md)                                              | `infrastructure/database/schema.ts`                  |
| 39  | Implement `DrizzleAuthSessionRepository`, `DrizzleAuthTokenRepository`, `DrizzlePermissionGrantRepository`                                                                              | backend | [auth.repository.ts](../../../backend/src/domain/auth-access-control/auth.repository.ts) | `infrastructure/database/drizzle-auth.repository.ts` |
| 40  | Implement auth routes: POST /auth/login (200/401/403), POST /auth/token (200/403/422/500), POST /auth/logout (200/401/403/500), GET /auth/introspect (200/401/403) with Zod schemas | backend | [auth-access-control.AuthAPI](interfaces.md#external-authapi-rest)  | `infrastructure/http/routes/auth.routes.ts`          |
| 41  | Implement `ErrorToHttpResponse` mapping for standard error payload `{ code, message, details? }`                                                                                        | backend | [ErrorToHttpResponse](mappings.md#errortohttpresponse)              | `infrastructure/http/routes/auth.routes.ts` (inline) |
| 42  | Register auth routes in app.ts                                                                                                                                                          | backend | —                                                                   | `infrastructure/http/app.ts`                         |

**Tests (W7):** AUTH-API-001–006, AUTH-MAP-009 → **7 obligations**

**Checkpoint:** W7 tests pass. Full route smoke test.

---

## W8 — State Machine + Event Tests

**Gate:** Remaining 16 state + 6 event consumer obligations green.

| #   | Task                                                                                            | Type    | Concepts                                                                                   | Files                      |
| --- | ----------------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------ | -------------------------- |
| —   | Implement remaining state machine tests: AUTH-STATE-003–007, AUTH-STATE-009, AUTH-STATE-011–016 | backend | [SessionLifecycle](states.md#sessionlifecycle), [TokenLifecycle](states.md#tokenlifecycle) | scaffold test → real tests |
| —   | Implement event consumer tests: AUTH-EVT-005–010                                                | backend | [events.md consumers](events.md)                                                           | scaffold test → real tests |

**Tests (W8):** AUTH-STATE-003–007, AUTH-STATE-009, AUTH-STATE-011–016, AUTH-EVT-005–010 → **16 obligations**

**Checkpoint:** All 84/84 TEST-SPEC obligations pass.

---

## W9 — Verification & Cross-Cutting

**Gate:** Typecheck clean, full suite green, alignment audit PASS, zero cross-domain leakage.

| #   | Task                                                                                                      | Type    | Concepts | Files                                                   |
| --- | --------------------------------------------------------------------------------------------------------- | ------- | -------- | ------------------------------------------------------- |
| —   | Run `npx tsc --noEmit` — zero errors                                                                      | backend | —        | —                                                       |
| —   | Run full test suite — all pass including pre-existing tests                                               | backend | —        | —                                                       |
| —   | Verify zero cross-domain imports (auth domain does not import from player-stats, player-management, etc.) | backend | —        | —                                                       |
| —   | Run alignment audit → produce ALIGNMENT-REPORT.md                                                         | docs    | —        | `docs/features/auth-access-control/ALIGNMENT-REPORT.md` |
| —   | Update SPEC.md frontmatter `status: planned` → `status: in-progress`                                      | docs    | —        | SPEC.md + all aspect docs                               |
| —   | Run `npm run docs:index` to sync indexes                                                                  | docs    | —        | `docs/index/*`                                          |

---

## Concept Traceability Matrix

| Concept ID                                 | Wave | Tasks         |
| ------------------------------------------ | ---- | ------------- |
| auth-access-control.Principal              | W1   | #11           |
| auth-access-control.Session                | W1   | #12           |
| auth-access-control.AccessToken            | W1   | #13           |
| auth-access-control.PermissionGrant        | W1   | #14           |
| auth-access-control.AuthErrorCode          | W1   | #10           |
| auth-access-control.Login                  | W3   | #22, #24, #25 |
| auth-access-control.IssueAccessToken       | W3   | #23           |
| auth-access-control.AuthenticateRequest    | W4   | #26, #27      |
| auth-access-control.AuthorizeRequest       | W4   | #28, #30, #32 |
| auth-access-control.Logout                 | W5   | #33, #34, #35 |
| auth-access-control.GetPermissionCatalog   | W6   | #37           |
| auth-access-control.IntrospectToken        | W6   | #36           |
| auth-access-control.AuthAPI                | W7   | #40, #41, #42 |
| auth-access-control.TokenLifecycle         | W2   | #20           |
| auth-access-control.SessionLifecycle       | W2   | #19           |
| auth-access-control.JWTClaimsToAuthContext | W4   | #27           |
| auth-access-control.AuthorizeRequestFlow   | W4   | #31           |

**Coverage:** 17/17 concepts traced.

## TEST-SPEC Traceability

| Wave      | Test IDs                                                                                                                                      | Count  |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| W3        | AUTH-RULE-001–005, AUTH-CALC-001–004, AUTH-POST-001–002, AUTH-ERR-001–002, AUTH-EVT-001–002, AUTH-MAP-001–002, AUTH-STATE-001, AUTH-STATE-008 | 20     |
| W4        | AUTH-RULE-006–014, AUTH-CALC-005–006, AUTH-POST-003–004, AUTH-ERR-003–004, AUTH-MAP-003–004, AUTH-MAP-007–008, AUTH-WF-001–005                | 25     |
| W5        | AUTH-RULE-015–017, AUTH-CALC-007, AUTH-POST-005, AUTH-ERR-005, AUTH-EVT-003–004, AUTH-MAP-005–006, AUTH-STATE-002, AUTH-STATE-010             | 12     |
| W6        | AUTH-QUERY-001–004                                                                                                                            | 4      |
| W7        | AUTH-API-001–006, AUTH-MAP-009                                                                                                                | 7      |
| W8        | AUTH-STATE-003–007, AUTH-STATE-009, AUTH-STATE-011–016, AUTH-EVT-005–010                                                                      | 16     |
| **Total** |                                                                                                                                               | **84** |

## Permission Migration Map

| File                 | Old Key                    | New Key (canonical)                            |
| -------------------- | -------------------------- | ---------------------------------------------- |
| auth.guard.ts        | `admin:*`                  | `auth-access-control.admin.*`                  |
| auth.guard.ts        | `makeup:write`             | `player-makeup.write.manageMakeup`             |
| auth.guard.ts        | `makeup:read`              | `player-makeup.read.viewMakeup`                |
| makeup.routes.ts     | `makeup:read`              | `player-makeup.read.viewMakeup`                |
| makeup.routes.ts     | `makeup:write`             | `player-makeup.write.manageMakeup`             |
| makeup.routes.ts     | `makeup:policy:read`       | `player-makeup.policy.readPolicy`              |
| settlement.routes.ts | `settlement:write`         | `financial-settlement.write.recordSettlement`  |
| onboarding.routes.ts | `player-onboarding.review` | `player-onboarding.review.evaluateApplication` |

## Ownership Labels

- **backend:** domain entities, use cases, state machines, auth guard refactor, repository implementations, routes, tests (W0–W9).
- **shared:** typed permission constants and AuthContext contract export (deferred until first consumer needs).
- **docs:** permission catalog, alignment report, status update, index sync (W0, W9).
- **web:** client 401/403 flow update (out of scope for this plan — separate task after backend stabilization).

## Done Criteria

- All 84 TEST-SPEC obligations pass with real assertions (zero `it.todo()`).
- `npx tsc --noEmit` clean.
- All pre-existing tests pass (player-stats, player-management, onboarding, makeup, settlement).
- Permission format is canonical 3-part across all routes.
- Auth guard delegates to domain use cases — no ad-hoc logic.
- No cross-domain imports from auth domain.
- ALIGNMENT-REPORT.md produced with ≥ 90% compliance.
