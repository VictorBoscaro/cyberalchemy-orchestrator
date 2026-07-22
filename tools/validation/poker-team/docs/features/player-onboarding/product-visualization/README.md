# Player Onboarding Product Visualization Pack

This pack translates the player onboarding feature specification into a product-facing view that is easy to consume by operations, product, engineering, and leadership.

## Plain-language module objective

The module turns an interested candidate into a trustworthy intake record.

It does this by forcing three guarantees before and after submission:
1. The candidate reads and accepts the active rules version.
2. The candidate provides the minimum required data for initial screening.
3. Leadership can approve or reject with controlled permissions and auditable outcomes.

## What this module does

- Shows onboarding rules in grouped screens.
- Locks the form until rules acceptance is explicitly captured.
- Validates candidate data and blocks duplicates.
- Creates a `SUBMITTED` application for manual review.
- Supports controlled approve/reject decisions.
- Publishes review outcomes for downstream player management.

## What this module does not do

- It does not auto-approve candidates.
- It does not create player accounts directly.
- It does not bypass LGPD or rules acceptance gates.

## Pack structure

| File | Purpose |
| --- | --- |
| `player-onboarding-product-visualization.html` | Single-file shareable dossier for PM and stakeholder review |
| `00-PM-BRIEF.md` | One-page executive handoff for product manager review |
| `01-EPIC-POINT-OF-VIEW.md` | Holistic module view: system objective, boundaries, capability mesh, and external ecosystem |
| `02-CAPABILITY-MAP.md` | Capability atlas index and relationship map |
| `capabilities/` | Self-contained capability dossiers (one file per capability) |
| `03-RULES-PLAYBOOK.md` | Rule ownership index and routing map |
| `04-CONCEPT-RELATIONS.md` | Internal and external concept relationship map |
| `05-MARKET-METHODOLOGY.md` | Market-method lens, KPIs, and operating model |
| `06-IMPORT-GUIDE.md` | How to import this pack into GitHub, Confluence, Jira, and spreadsheets |
| `import/` | Machine-friendly CSV assets for backlog and reporting workflows |

## Capability dossiers (self-contained)

Each capability file is standalone and can be consumed without opening other capability files.
Operation-level rules are owned in capability files, while shared rules are owned in `01-EPIC-POINT-OF-VIEW.md`.

| Capability | File |
| --- | --- |
| CAP-01 Compose Guided Onboarding Flow | `capabilities/CAP-01-COMPOSE-GUIDED-ONBOARDING-FLOW.md` |
| CAP-02 Enforce Compliance Gate | `capabilities/CAP-02-ENFORCE-COMPLIANCE-GATE.md` |
| CAP-03 Capture Qualified Application | `capabilities/CAP-03-CAPTURE-QUALIFIED-APPLICATION.md` |
| CAP-04 Execute Controlled Review | `capabilities/CAP-04-EXECUTE-CONTROLLED-REVIEW.md` |
| CAP-05 Handoff Approved Intake | `capabilities/CAP-05-HANDOFF-APPROVED-INTAKE.md` |
| CAP-06 Observe Funnel Health | `capabilities/CAP-06-OBSERVE-FUNNEL-HEALTH.md` |

## Source of truth

This pack is a product visualization layer.
Normative behavior contracts remain in the feature specification set:
- `../SPEC.md`
- `../domain.md`
- `../operations.md`
- `../states.md`
- `../interfaces.md`
- `../workflows.md`
- `../events.md`
- `../queries.md`

## Recommended reading order

1. `player-onboarding-product-visualization.html`
2. `00-PM-BRIEF.md`
3. `01-EPIC-POINT-OF-VIEW.md`
4. `02-CAPABILITY-MAP.md`
5. `capabilities/` (all CAP files)
6. `03-RULES-PLAYBOOK.md`
7. `04-CONCEPT-RELATIONS.md`
8. `05-MARKET-METHODOLOGY.md`
9. `06-IMPORT-GUIDE.md`
