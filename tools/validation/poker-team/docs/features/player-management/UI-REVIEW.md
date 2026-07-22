# UI Review — player-management

**Date:** 2025-04-15
**Overall:** PASS WITH FLAG

## Pillar Scores

| Pillar              | Score | Notes                                                                  |
| ------------------- | ----- | ---------------------------------------------------------------------- |
| Route Coverage      | PASS  | All 6 routes present                                                   |
| Component Coverage  | FLAG  | `CreateCoachForm` has undocumented `principalId` field not in UI-SPEC  |
| Data Flow           | FLAG  | Player hooks correct; coach assignment hooks need backend verification |
| Form Contracts      | PASS  | Both forms validate with Zod; 409 conflict mapped                      |
| State-to-UI Mapping | PASS  | `PlayerStatusBadge` and `LimitBadge` render correct colors             |
| Accessibility       | PASS  | Forms have `role="form"` and `aria-label`; dialog has `aria-modal`     |

## Issues

| #   | Severity | Description                                                                              |
| --- | -------- | ---------------------------------------------------------------------------------------- |
| 1   | FLAG     | `CreateCoachForm` requires `principalId` — add to UI-SPEC or clarify                     |
| 2   | FLAG     | Coach assignment hooks (`useCoachPlayers`, `useUnassignCoach`) need backend verification |

## Recommendations

- Update UI-SPEC to document `principalId` field or remove from form.
- Verify coach assignment hook contracts against backend endpoints.
