# UI Review — player-onboarding

**Date:** 2026-04-24
**Overall:** FLAG

## Pillar Scores

| Pillar              | Score | Notes                                                                                              |
| ------------------- | ----- | -------------------------------------------------------------------------------------------------- |
| Route Coverage      | PASS  | Both routes are present (`/onboarding`, `/admin/onboarding`) with expected feature entrypoints.   |
| Component Coverage  | PASS  | `CandidateStatusBadge` behavior is implemented in admin review flow and rendered in list + detail. |
| Data Flow           | FLAG  | Admin flow still uses direct fetch instead of shared React Query hooks/cache invalidation pattern. |
| Form Contracts      | PASS  | Public submission and admin review fields match UI-SPEC contracts.                                 |
| State-to-UI Mapping | PASS  | Candidate status is visible and mapped in backlog and detail views.                                |
| Accessibility       | FLAG  | Step indicator now uses `aria-current="step"`; status badges still need explicit `aria-label`.     |

## Issues

| #   | Severity | Description                                                                            |
| --- | -------- | -------------------------------------------------------------------------------------- |
| 1   | FLAG     | Admin onboarding review data flow still uses direct fetch and local state orchestration. |
| 2   | FLAG     | `CandidateStatusBadge` has no explicit `aria-label` text for assistive technologies.    |

## Recommendations

- Migrate admin onboarding review reads/writes to shared React Query hooks and invalidate candidate queue/detail keys after review actions.
- Add `aria-label` on status badges (for example, `Candidate status: Approved`).
