---
id: player-onboarding
feature: player-onboarding
title: Player Onboarding Decisions
summary: Decision log for regulation-driven onboarding and candidate intake contracts.
status: implemented
pillar: operations
domain: onboarding-candidatos-decisions
audience:
  - developers
  - operations
priority: p1
lang: en
owners:
  - operations-core
  - backend-core
updatedAt: 2026-04-08
dependencies:
  - SPEC.md
  - operations.md
  - interfaces.md
includes: []
---

## Confirmed Decisions

- Feature id is `player-onboarding`.
- Documentation language is EN by default for this repository.
- Regulation sections can be grouped only when content still fits cleanly in one readable screen.
- Regulation acceptance is mandatory before the form is unlocked.
- Candidate submissions will be handled by backend API in this repository.
- Duplicate candidates are blocked by same WhatsApp OR same normalized email.
- LGPD explicit consent is required.
- No auto-screening in v1; all candidate decisions are manual review.
- All three room nicknames (`PokerStars`, `GGPoker`, `Suprema`) are optional in v1.
- `cityState` uses strict `City/State` format validation.
- Candidate age under 18 is blocked at submission.
- Rejected application retention period is 365 days.
- Successful submit returns confirmation page only (no WhatsApp/email acknowledgement in v1).
- Reviewer actions are available in a web admin page in the same release.

## Open Decisions

- Exact LGPD consent text copy and legal owner sign-off string.

## Deferred Scope

- Automated candidate scoring and ranking.
- Automatic creation of player record after approval.
- Reminder campaigns for incomplete onboarding sessions.
