---
id: player-onboarding
feature: player-onboarding
title: Player Onboarding Tasks
summary: Dependency-ordered tasks for onboarding flow implementation across docs, web, and backend.
status: implemented
pillar: operations
domain: onboarding-candidatos-delivery
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - web-core
  - backend-core
  - operations-core
updatedAt: 2026-04-08
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
  - mappings.md
  - workflows.md
includes: []
---

## Ordered Tasks

1. docs: confirm final grouping map between regulation sections and onboarding screens under the screen size policy.
2. docs: finalize pending data contract decisions documented in [decisions.en.md](decisions.en.md).
3. backend: implement `GET /onboarding/flow` to deliver grouped rule screens and active regulation version metadata.
4. backend: implement `POST /onboarding/candidates` with deterministic validation and duplicate blocking by WhatsApp OR email.
5. backend: persist rule acceptance (`version`, `acceptedAt`, `source`) and LGPD consent flags in candidate records.
6. backend: implement `PATCH /onboarding/candidates/{id}/review` with auth-access-control permission guard `player-onboarding.review`.
7. backend: implement `GET /admin/onboarding/candidates` and `GET /admin/onboarding/candidates/{id}` for review backlog and detail.
8. backend: add tests for success paths, validation failures (city/state, under-18), duplicate conflicts, and unauthorized review attempts.
9. web: build onboarding screen flow with grouped rule pages, progress indicator, and acceptance gate.
10. web: build candidate form using documented enum options and conditional field behavior (tracker detail requirement).
11. web: add final submission confirmation and deterministic error rendering for validation/conflict responses.
12. web: implement authenticated admin review page with backlog, detail view, and approve/reject actions.
13. shared: publish typed DTO contracts shared between backend and web adapters for onboarding endpoints.
14. docs: set feature status to `implemented` after verification checklist is fully green.

## Ownership Labels

- docs: scope, policy, and contract finalization.
- backend: API behavior, validation, persistence, and tests.
- web: UX flow, form behavior, and API adapter integration.
- shared: DTO contract stability across slices.

## Verification Checklist

1. Candidate cannot submit the form before mandatory regulation acceptance.
2. Candidate submission rejects missing required fields with deterministic 400 responses.
3. Duplicate candidate detection blocks same WhatsApp or same normalized email with 409 conflict.
4. Candidate submission persists regulation acceptance and LGPD consent data.
5. Candidate submission rejects invalid `cityState` format and age under 18.
6. Review endpoint requires authenticated permission `player-onboarding.review`.
7. Approved and rejected review outcomes transition candidate status correctly.
8. Rejected review outcomes persist deterministic `retentionUntil = reviewedAt + 365 days`.
9. Web flow renders grouped rule screens and allows mobile-safe navigation.
10. Web admin review page allows listing, opening, and reviewing candidate applications.

## Done Criteria

- Onboarding documentation and API contracts are aligned with implementation behavior.
- Public onboarding journey is complete: rules, acceptance gate, candidate form, and confirmation.
- Operations team can manually review candidate outcomes via documented flow.
