---
id: auth-access-control
feature: auth-access-control
title: Auth Access Control Alignment Report
summary: 2026-04-30 read-only alignment audit after latest auth bootstrap and test changes.
status: in-progress
pillar: platform
domain: auth-access-control
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - platform-core
  - backend-core
updatedAt: 2026-04-30
dependencies:
  - SPEC.md
  - TEST-SPEC.md
  - operations.md
  - interfaces.md
  - events.md
  - PILOT-DECISIONS.md
includes: []
---

# Alignment Report: auth-access-control

**Audit date:** 2026-04-30  
**Framework version:** DomainSpec 2.0.3 (baseline from [domainspec/CHANGELOG.md](../../../domainspec/CHANGELOG.md))  
**Audit mode:** Read-only (no code edits)  
**Sources:** [SPEC.md](SPEC.md), [operations.md](operations.md), [interfaces.md](interfaces.md), [events.md](events.md), [TEST-SPEC.md](TEST-SPEC.md), [PILOT-DECISIONS.md](PILOT-DECISIONS.md)

## Scope

- Latest auth changes touching bootstrap seeding, auth repository adapter, and auth E2E setup.
- Mandatory alignment checks from domainspec-audit-alignment:
  - Infrastructure binding audit (ports, adapters, migrations, startup wiring).
  - Stub and dead-code scan in auth domain and use-case paths.
  - Event producer/consumer contract alignment against [events.md](events.md) and [TEST-SPEC.md](TEST-SPEC.md).
  - Pilot strictness decision impact from [PILOT-DECISIONS.md](PILOT-DECISIONS.md).

## Verification Evidence

- Completed: targeted backend auth suites.
  - Command: npm test --workspace=backend -- src/use-cases/auth-access-control/seed-system-bootstrap.test.ts src/infrastructure/http/auth/auth-access-control.test.ts src/infrastructure/http/routes/auth.routes.contract.test.ts
  - Result: 3 files passed, 100 tests passed.
- Attempted but incomplete in this audit run:
  - npm run typecheck:web (interrupted, exit code 130).
- Not executed in this audit run:
  - Full Playwright suite from [PILOT-DECISIONS.md](PILOT-DECISIONS.md) verification profile.

## Severity-Ranked Findings (Open)

| ID | Severity | Gate Impact | Category | Requirement | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| AUTH-ALG-07 | BLOCK | Blocker | missing-runtime-consumers | Event consumers declared in [events.md](events.md) and required by [TEST-SPEC.md](TEST-SPEC.md) AUTH-EVT-006..010 must exist and be wired in runtime path. | Consumer declarations: [events.md](events.md) lines 40-45, 61-67, 88-94, 109-115, 130-135. Test obligations: [TEST-SPEC.md](TEST-SPEC.md) lines 116-120. Runtime uses optional onEvent only: [backend/src/use-cases/auth-access-control/login.ts](../../../backend/src/use-cases/auth-access-control/login.ts) lines 101-107 and 268-291; [backend/src/use-cases/auth-access-control/authorize-request.ts](../../../backend/src/use-cases/auth-access-control/authorize-request.ts) lines 46-48 and 120-144; [backend/src/use-cases/auth-access-control/logout.ts](../../../backend/src/use-cases/auth-access-control/logout.ts) lines 41-46, 114-120, 225-249. Production call sites do not pass onEvent: [backend/src/infrastructure/http/routes/auth.routes.ts](../../../backend/src/infrastructure/http/routes/auth.routes.ts) lines 42-47 and 160-167; [backend/src/infrastructure/http/auth/auth.guard.ts](../../../backend/src/infrastructure/http/auth/auth.guard.ts) lines 69-73 and 245-252. Consumer handlers currently exist only as local test doubles: [backend/src/infrastructure/http/auth/auth-access-control.test.ts](../../../backend/src/infrastructure/http/auth/auth-access-control.test.ts) lines 1918-2025. | MISSING |
| AUTH-ALG-08 | HIGH | FLAG | undocumented-runtime-behavior | SeedSystemBootstrap contract defines ADMIN_USERNAME input and subsequent boot role-sync only; implementation introduces ADMIN_PASSWORD override and credential rotation behavior not captured in docs. | Contract: [operations.md](operations.md) lines 39-41, 48, 56, 71, 77; [capabilities/system-bootstrap.md](capabilities/system-bootstrap.md) lines 35-39. Implementation: [backend/src/use-cases/auth-access-control/seed-system-bootstrap.ts](../../../backend/src/use-cases/auth-access-control/seed-system-bootstrap.ts) lines 43, 52-54, 83-93. Tests codify new behavior: [backend/src/use-cases/auth-access-control/seed-system-bootstrap.test.ts](../../../backend/src/use-cases/auth-access-control/seed-system-bootstrap.test.ts) lines 187-223. E2E defaults rely on this path: [apps/web/e2e/auth.setup.ts](../../../apps/web/e2e/auth.setup.ts) lines 6-8 and [apps/web/e2e/auth-access-control/auth.spec.ts](../../../apps/web/e2e/auth-access-control/auth.spec.ts) lines 4-5. | EXTRA/PARTIAL |
| AUTH-ALG-09 | MEDIUM | FLAG | verification-evidence-gap | Strict pilot profile requires full backend plus web plus e2e verification run before go decision. | Policy: [PILOT-DECISIONS.md](PILOT-DECISIONS.md) lines 30 and 39-43. This audit has completed targeted backend auth tests only; typecheck:web interrupted (exit 130); full Playwright run not executed in this audit. | PARTIAL |

## Compliance Snapshot

- Compliant:
  - Infrastructure binding for auth ports and DB adapters.
    - Ports: [backend/src/domain/auth-access-control/auth.repository.ts](../../../backend/src/domain/auth-access-control/auth.repository.ts) lines 6-37.
    - Adapters: [backend/src/infrastructure/repositories/drizzle-auth.repository.ts](../../../backend/src/infrastructure/repositories/drizzle-auth.repository.ts) lines 35-102 and 115 onward.
    - Production path binds drizzle adapters (no in-memory binding in non-test files): [backend/src/infrastructure/http/routes/auth.routes.ts](../../../backend/src/infrastructure/http/routes/auth.routes.ts) lines 17-20 and [backend/src/infrastructure/http/auth/auth.guard.ts](../../../backend/src/infrastructure/http/auth/auth.guard.ts) lines 61-69.
  - Migration gate and startup lifecycle wiring.
    - Auth schema tables present: [backend/src/infrastructure/database/schema.ts](../../../backend/src/infrastructure/database/schema.ts) lines 248-296.
    - Migration file includes auth tables: [backend/drizzle/0000_thick_yellowjacket.sql](../../../backend/drizzle/0000_thick_yellowjacket.sql) lines 12-51.
    - Migration runner exists: [backend/src/infrastructure/database/migrate.ts](../../../backend/src/infrastructure/database/migrate.ts) lines 5-10.
    - CI runs migration before backend tests: [/.github/workflows/ci.yml](../../../.github/workflows/ci.yml) lines 38-44.
    - Bootstrap runs before listen: [backend/src/index.ts](../../../backend/src/index.ts) lines 15-23.
  - Stub/dead-code scan in auth domain/use-cases found no open stub markers in production path.
  - Targeted backend auth suites pass (100/100).

- Partial:
  - Verification profile evidence is incomplete for strict pilot run profile (web typecheck and full e2e not completed in this audit).

- Missing:
  - Runtime-wired event consumer handlers required by events contract and TEST-SPEC event-consumer obligations.

- Extra:
  - Runtime ADMIN_PASSWORD override and existing-admin credential hash refresh behavior not reflected in docs.

## Open Blockers vs Non-Blockers

- Open blockers:
  1. AUTH-ALG-07 (BLOCK) - event consumer handlers are not wired in runtime path.

- Open non-blockers:
  1. AUTH-ALG-08 (HIGH FLAG) - bootstrap runtime behavior drift (ADMIN_PASSWORD override and credential rotation semantics undocumented).
  2. AUTH-ALG-09 (MEDIUM FLAG) - strict verification profile evidence incomplete in this audit run.

## Prioritized Remediation Actions

1. Implement and wire a production event dispatcher for auth events, then register concrete handlers for audit subsystem, session tracker, cache invalidator, security analytics, and alerting pipeline.
2. Decide and codify SeedSystemBootstrap behavior for ADMIN_PASSWORD and subsequent-boot credential handling:
   - Option A: Document this behavior in [operations.md](operations.md), [interfaces.md](interfaces.md), and [capabilities/system-bootstrap.md](capabilities/system-bootstrap.md), including complexity/rotation constraints.
   - Option B: Remove runtime credential-rotation side effect and keep docs-as-contract behavior (subsequent boot role-grant sync only).
3. Re-run strict pilot verification profile end-to-end and attach run artifacts:
   - npm run test:backend
   - npm run typecheck:web
   - cd apps/web && npx playwright test

## Pilot Decision Under Strict Block-on-FLAG

Policy evidence: [PILOT-DECISIONS.md](PILOT-DECISIONS.md) line 30 selects Strict block on any FLAG.

Result for this audit: BLOCKED.

Reasoning:

1. At least one open BLOCK finding exists (AUTH-ALG-07).
2. Even if BLOCK were resolved, open FLAG findings (AUTH-ALG-08 and AUTH-ALG-09) still block pilot under strict policy.
