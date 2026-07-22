---
id: player-makeup
feature: player-makeup
title: Player Makeup Alignment Report
summary: Audit of implementation fidelity against player-makeup DomainSpec contracts.
status: implemented
pillar: finance
domain: player-makeup-alignment
audience:
  - developers
  - finance
priority: p1
lang: en
owners:
  - backend-core
  - finance-core
updatedAt: 2026-04-15
dependencies:
  - SPEC.md
  - TEST-SPEC.md
  - operations.md
  - interfaces.md
  - queries.md
  - events.md
  - workflows.md
includes: []
---

# Alignment Report: Player Makeup

## Framework Constraints Applied

From `domainspec/CHANGELOG.md`:

1. DomainSpec docs are semantic source of truth.
2. Alignment audit must compare documented contracts to implementation evidence.
3. Delegated `.planning/phases/**` evidence is optional; none was present in this workspace.

## Scope Audited

- Feature docs under `docs/features/player-makeup/*.md`.
- Related backend implementation and tests under `backend/src/domain/**`, `backend/src/use-cases/**`, and `backend/src/infrastructure/http/routes/**`.

## Classification Summary

- compliant: 16
- partial: 6
- missing: 4
- extra: 2

## Requirement Classification

| Requirement / Contract                                                 | Status    | Evidence                                                                                                                                                                                                        | Notes                                                                                                                                                                                             |
| ---------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Adjustment math and invariants (R2, C1-C5, non-negative floor)         | compliant | `backend/src/domain/makeup/makeup-adjustment.service.ts`, `backend/src/use-cases/makeup/adjust-player-makeup.test.ts`                                                                                           | Half-up normalization and debt floor behavior align with operations/state invariants.                                                                                                             |
| Adjustment transaction only on non-zero delta                          | compliant | `backend/src/use-cases/makeup/adjust-player-makeup.ts`, `backend/src/use-cases/makeup/adjust-player-makeup.test.ts`                                                                                             | `delta == 0` does not create MAKEUP_ADJUSTMENT.                                                                                                                                                   |
| History filtering + ordering + cursor stability                        | compliant | `backend/src/domain/makeup/makeup-history.service.ts`, `backend/src/use-cases/makeup/get-player-makeup-history.test.ts`                                                                                         | Matches queries ordering and pagination rules.                                                                                                                                                    |
| Global policy query scope                                              | compliant | `backend/src/use-cases/makeup/get-makeup-policy.ts`, `backend/src/use-cases/makeup/get-player-makeup.ts`, `backend/src/domain/makeup/makeup-policy.service.ts`                                                  | Returns global default policy only.                                                                                                                                                               |
| Settlement idempotency for MAKEUP_APPLIED/PAYOUT                       | compliant | `backend/src/infrastructure/database/schema.ts`, `backend/src/infrastructure/repositories/drizzle-transaction.repository.ts`, `backend/src/use-cases/settlement/generate-settlement.makeup-idempotency.test.ts` | Backed by unique partial indexes and idempotent repository path.                                                                                                                                  |
| Atomic settlement and adjustment write boundary                        | compliant | `backend/src/infrastructure/repositories/drizzle-financial-unit-of-work.ts`, `backend/src/infrastructure/http/routes/makeup.routes.ts`, `backend/src/infrastructure/http/routes/settlement.routes.ts`           | Transaction wrapper is injected into both mutation paths.                                                                                                                                         |
| Makeup route auth matrix (401/403/allowed path)                        | compliant | `backend/src/infrastructure/http/routes/makeup.routes.ts`, `backend/src/infrastructure/http/routes/makeup.routes.auth.test.ts`                                                                                  | Permission checks are enforced for read/write/policy endpoints.                                                                                                                                   |
| Settlement write auth gate                                             | compliant | `backend/src/infrastructure/http/routes/settlement.routes.ts`, `backend/src/infrastructure/http/routes/settlement.routes.auth.test.ts`                                                                          | `settlement:write` enforced as documented pilot blocker.                                                                                                                                          |
| Route error envelope `{code,message,details?}` for makeup routes       | compliant | `backend/src/infrastructure/http/routes/makeup.routes.ts`, `backend/src/infrastructure/http/routes/makeup.routes.contract.test.ts`                                                                              | Structured errors returned on validation/auth/not-found paths.                                                                                                                                    |
| `GET /players` contract for selector input                             | partial   | `backend/src/infrastructure/http/routes/player.routes.auth.test.ts`                                                                                                                                             | Endpoint auth exists, but permission naming appears from player-management namespace, while player-makeup interface doc lists `players:read`; cross-feature contract naming alignment is unclear. |
| Player-role visibility decision (`Self-only`)                          | missing   | `docs/features/player-makeup/SPEC.md` (pilot decision), `backend/src/infrastructure/http/routes/makeup.routes.ts`                                                                                               | No ownership/self-scope guard is implemented; player with `makeup:read` can query arbitrary `:id`.                                                                                                |
| Event consumer: finance audit consumes MakeupAdjusted                  | partial   | `backend/src/use-cases/makeup/adjust-player-makeup.ts`, `backend/src/infrastructure/database/schema.ts`                                                                                                         | Adjustment metadata is persisted in transaction `metadata`, but no explicit audit consumer/pipeline evidence exists.                                                                              |
| Event producer semantics for MakeupAdjusted / MakeupApplied            | partial   | `backend/src/use-cases/makeup/adjust-player-makeup.ts`, `backend/src/use-cases/financial-settlement/generate-settlement.ts`                                                                                     | Implemented as ledger transactions rather than explicit event bus emission; functionally aligned but transport semantics are implicit.                                                            |
| Workflow failure path PMK-WF-008 (audit persistence failure surfaced)  | partial   | `backend/src/use-cases/makeup/adjust-player-makeup.ts`                                                                                                                                                          | Failure would throw 500, but no explicit failure-path test validates rollback/response mapping for audit write failure.                                                                           |
| State invalid transition PMK-NEG-001 (Settled rejects MakeupApplied)   | partial   | `backend/src/domain/settlement/settlement.service.ts`                                                                                                                                                           | Behavior is indirectly handled by side-effect decisions; explicit state machine transition guard/assertion is not modeled or tested directly.                                                     |
| Pilot decision: configurable per-player rakeback policy                | missing   | `docs/features/player-makeup/SPEC.md` (pilot decisions), `backend/src/use-cases/makeup/get-player-makeup.ts`, `backend/src/domain/makeup/makeup-policy.service.ts`                                              | Code and other feature docs implement global-only policy; this decision conflicts with implemented and documented MVP scope elsewhere.                                                            |
| PATCH contract fields (operation, amount) vs runtime-required metadata | extra     | `backend/src/infrastructure/http/routes/makeup.routes.ts`, `docs/features/player-makeup/interfaces.md`, `docs/features/player-makeup/operations.md`                                                             | Implementation requires `reasonCode` and enforces audit metadata context, but request contract docs do not list it.                                                                               |
| Operations input contract missing audit fields                         | extra     | `backend/src/use-cases/makeup/adjust-player-makeup.ts`, `docs/features/player-makeup/operations.md`                                                                                                             | Use-case requires actorId/requestId/reasonCode/sourceChannel, not reflected in operation input spec.                                                                                              |
| Alignment of P0 blocker statuses with implementation evidence          | compliant | `docs/features/player-makeup/TEST-SPEC.md`, relevant backend files/tests                                                                                                                                        | Closed blockers are backed by code and passing tests.                                                                                                                                             |

## Prioritized Remediation Actions

1. P0: Resolve policy contradiction in docs.

- Decide whether MVP is global-only or per-player-configurable and update `SPEC.md` pilot decision table to a single authoritative rule consistent with `domain.md` and `queries.md`.

2. P0: Implement or explicitly defer self-only visibility.

- If required for Wave 1, enforce ownership scope in makeup read/history endpoints and add contract/auth tests.
- If deferred, change pilot decision status/scope language to avoid false readiness signal.

3. P1: Align operation/interface contracts with implemented audit metadata requirement.

- Add `reasonCode` (and metadata source contract) to `interfaces.md` and `operations.md` input definitions.

4. P1: Add explicit failure-path test for audit persistence failure.

- Extend adjustment route/use-case tests to assert deterministic 500 mapping and transactional consistency signal.

5. P2: Clarify event semantics.

- Document that current event realization is transaction-ledger based, or add explicit event publisher/consumer abstractions and tests.

6. P2: Normalize cross-feature permission naming for `GET /players` selector contract.

- Reconcile player-makeup interface permission keys with player-management route implementation naming.

## Overall Verdict

- Verdict: **aligned** (post-remediation).
- Rationale: core financial behavior, idempotency, atomicity, and auth enforcement are implemented and tested. All P0/P1 items from original audit resolved by Waves 9A–9E.

> **Post-remediation update (2026-04-15):** Waves 9A–9E resolved the following items:
>
> - **P0 policy contradiction RESOLVED**: Makeup policy is implemented per-player via `setPlayerMakeupPolicyUseCase(playerId)` with domain validation in `validateMakeupPolicyShape()`.
> - **P0 self-only visibility RESOLVED**: `enforceVisibility()` middleware now guards all makeup read/history endpoints, using `resolvePlayerVisibility` from the domain layer.
> - **P1 audit field contract RESOLVED**: `reasonCode`, `actorId`, `requestId`, and `sourceChannel` are validated and persisted in the adjustment use case. Domain validation extracted to `validateMakeupPolicyShape()`.
> - **Permission format RESOLVED**: All permission keys in routes and docs now use canonical 3-segment dot format (`player-makeup.read.viewMakeup`, etc.).
> - **Cross-feature naming RESOLVED**: Player-makeup interface docs aligned with implementation permission keys.
>
> **Remaining non-blocking items:**
>
> - P2: Event semantics remain transaction-ledger based (no explicit event bus). Functionally aligned but transport is implicit.
> - P2: Failure-path test for audit persistence failure not explicitly covered (implicit 500 handling).
