# Import Guide

This pack is intentionally split into Markdown and CSV assets.

- Markdown files are optimized for GitHub and Confluence page ingestion.
- CSV files are optimized for Jira issue import and spreadsheet/BI tooling.

## File inventory for import

| Asset | Recommended destination | Notes |
| --- | --- | --- |
| `player-onboarding-product-visualization.html` | Direct sharing via email/chat/file attach | Single-file view for PM and stakeholder iteration |
| `README.md` + `00..06` Markdown files | GitHub wiki/docs, Confluence pages | Import one file per page for clean navigation |
| `capabilities/*.md` | GitHub wiki/docs, Confluence child pages | Each capability is standalone and can be imported independently |
| `import/jira-epics.csv` | Jira CSV importer | Import first |
| `import/jira-stories.csv` | Jira CSV importer | Import second, linking to epics |
| `import/capabilities.csv` | Confluence table import, sheets, BI | Capability governance baseline |
| `import/rules.csv` | Confluence table import, sheets, BI | Rule and compliance catalog |
| `import/concept-relations.csv` | Graph tooling, sheets, BI | Relationship graph source table |

## Jira import sequence

1. Import `import/jira-epics.csv` and map fields:
   - `Issue Type`
   - `Summary`
   - `Epic Name`
   - `Description`
   - `Labels`
2. Import `import/jira-stories.csv` and map fields:
   - `Issue Type`
   - `Summary`
   - `Description`
   - `Epic Link`
   - `Labels`
3. Validate that each story row is linked to one epic via `Epic Link`.

## Confluence import sequence

1. Create a parent page named `Player Onboarding Product Visualization`.
2. Import `00-PM-BRIEF.md` first as the executive landing page.
3. Import `01-EPIC-POINT-OF-VIEW.md` and `02-CAPABILITY-MAP.md` next.
4. Import all files under `capabilities/` as child pages under the capability map page.
5. Import `03`, `04`, `05`, and `06` pages as governance and operations layer.
6. Attach CSV files from `import/` and use Confluence table/chart macros as needed.

## GitHub usage sequence

1. Keep folder structure intact under feature docs.
2. Use `README.md` as entrypoint.
3. For fast review cycles, open `player-onboarding-product-visualization.html` directly.
4. Review capabilities independently in `capabilities/` without cross-opening other capability files.
5. Render Mermaid diagrams directly in GitHub markdown preview.

## Spreadsheet and BI usage

1. Load CSV files from `import/` into the same workbook.
2. Join keys:
   - `capabilities.capability_id = rules.capability_id`
   - `rules.canonical_rule_ref` for operation-scoped rule identity
   - `capabilities.capability_doc` for direct linkouts to self-contained capability pages
   - `concept-relations.from_concept` and `to_concept` for graph pivots
3. Build dashboard tabs:
   - Capability health
   - Rule risk heatmap
   - Relation density and dependency hotspots

## Compatibility notes

- Delimiter: comma.
- Encoding: UTF-8.
- Header row: present in all CSV files.
- Rule identity uses canonical refs like `SubmitCandidateApplication.R1` and `CandidateApplicationLifecycle.I1`.
- `capabilities.csv` includes `capability_doc` and `self_contained` columns for page automation.
