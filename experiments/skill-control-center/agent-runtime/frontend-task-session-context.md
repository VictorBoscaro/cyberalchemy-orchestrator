# Frontend Task Session Context Pack

Session evidence, not canonical product authority.

- Task: implement the bounded Phase 1 frontend and browser evidence.
- Mode: standard/strict; local runtime; no runtime handoff.
- Coverage: 11/11 obligations covered; no blockers.

## Obligation matrix

| ID | Obligation | Controlling evidence |
|---|---|---|
| F-01 | Exactly three structurally distinct but semantically equal variants | `UI-SPEC.md` — Shared Variant Contract; Structural Variants A–C |
| F-02 | Six critical flows and 17 mandatory states | `UI-SPEC.md` — Critical Flows; State Fixture Contract |
| F-03 | Search/filter/select/detail and explicit navigation | `UI-SPEC.md` — Interaction Rules; `states.md` — WorkspaceNavigation |
| F-04 | Skill path plus graph/table topology parity | `queries.md` — FindPath/GetTopology; `interfaces.md` — topology/path routes |
| F-05 | Honest usage, coverage, freshness and unknown ≠ zero | `queries.md` — GetUsageEvidence and evidence algebra |
| F-06 | Owner `@VictorBoscaro`, local preferences and local draft preview | `SPEC.md`; `UI-SPEC.md` — Local Operations |
| F-07 | No authoritative apply/retry/reconcile/receipt/promotion surface | `BACKLOG.md` — Phase 1 Guardrails; `interfaces.md` — Forbidden Inventory |
| F-08 | Responsive, light/dark, keyboard, semantic topology alternative | `UI-SPEC.md` — Accessibility and Responsive Rules |
| F-09 | Exact 204-row screenshot matrix | `TEST-SPEC.md` — SCC-T-VIS-001 |
| F-10 | Browser/console/network/a11y/ARIA/measurement/trace evidence | `ux-evidence-validator` evidence contract |
| F-11 | Preserve six-route backend contract and live fixtures | backend result; `implementations/server/control_center/`; fixture manifest |

## Write scope and validation

- Write: `implementations/static/control-center/`,
  `implementations/tests/control_center/test_frontend.py`,
  `output/playwright/ux-validator/skill-control-center-phase1/`, and this session report.
- Read-only inputs: canonical feature package, backend implementation and fixture corpus.
- Validate: frontend structural test, all backend/regression tests, 204 browser captures, manifest
  integrity, no console/request failure, no horizontal overflow, shared test-ID parity, and
  independent review.
- Assumptions auto-selected: native ES modules/CSS remain the smallest dependency surface; fixture
  states are selected only by explicit local harness query parameters; normal runs use the six live
  read routes.

## Exclusions

- Existing `implementations/static/ui/`, prior UI experimentation variants, and the graph experiment
  are excluded as visual or creative references.
- Authoritative mutations and benchmark-based variant promotion remain deferred as SCC-BL-001..008.
