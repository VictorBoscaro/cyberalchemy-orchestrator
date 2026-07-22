# UI Review — player-makeup

**Date:** 2025-04-15
**Overall:** FLAG

## Pillar Scores

| Pillar              | Score | Notes                                                                    |
| ------------------- | ----- | ------------------------------------------------------------------------ |
| Route Coverage      | PASS  | Route `/players/[id]/makeup` present                                     |
| Component Coverage  | FLAG  | Sub-components not extracted; all UI in single dashboard                 |
| Data Flow           | FLAG  | Dashboard uses direct fetch instead of React Query                       |
| Form Contracts      | FLAG  | `EditPolicyDialog` Zod schema correct; `AdjustMakeupForm` schema missing |
| State-to-UI Mapping | FLAG  | `MakeupDebtBadge` not implemented                                        |
| Accessibility       | FLAG  | `EditPolicyDialog` has `aria-modal` ✓; `AdjustMakeupDialog` not verified |

## Issues

| #   | Severity | Description                                                                                                                |
| --- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | FLAG     | Component decomposition missing — MakeupSummaryCard, AdjustMakeupDialog, MakeupHistoryTable, MakeupDebtBadge not extracted |
| 2   | FLAG     | Direct fetch instead of React Query — inconsistent with codebase                                                           |
| 3   | FLAG     | Missing `AdjustMakeupForm` validation schema                                                                               |

## Recommendations

- Refactor dashboard into separate sub-components matching UI-SPEC.
- Migrate to React Query hooks for consistency and cache management.
- Implement `AdjustMakeupForm` with Zod schema and `MakeupDebtBadge`.
