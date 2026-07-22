# UI Review — player-stats

**Date:** 2026-04-24
**Overall:** PASS WITH FLAG

## Pillar Scores

| Pillar              | Score | Notes |
| ------------------- | ----- | ----- |
| Route Coverage      | PASS  | Both routes are present and wired: `/players/[id]/stats`, `/stats/record`. |
| Component Coverage  | PASS  | `PlayerStatsPage`, `StatsWindowCard`, `StatsHistoryTable`, `RecordStatsForm`, and `StatsStatusBadge` are implemented. |
| Data Flow           | PASS  | History cursor pagination is wired with load-more; stats window now sends required `fromDate` and `toDate`; UI renders canonical `winrateBbPer100`. |
| Form Contracts      | PASS  | Record form validation remains aligned with UI-SPEC and backend field constraints. |
| State-to-UI Mapping | PASS  | `RECORDED` and `CORRECTED` statuses remain deterministic in table badge rendering. |
| Accessibility       | FLAG  | Load-more button has `aria-label`, but table headers are static and do not expose sortable semantics from UI-SPEC guidance. |

## Issues

| # | Severity | Description |
|---|----------|-------------|
| 1 | FLAG | Stats history table does not expose `aria-sort` semantics for sortable header interactions (if sorting is added). |

## Recommendations

- Keep current static table behavior explicit in UI-SPEC, or implement sortable headers with `aria-sort` when sort interactions are introduced.
