# Frontend Phase 1 context pack

## Bounded task

Implement one browser frontend for the Skill & Dispatch Control Center with exactly three
structural variants over one semantic core.

## Controlling sources

- `docs/features/skill-control-center/SPEC.md`
- `docs/features/skill-control-center/UI-SPEC.md`
- `docs/features/skill-control-center/TEST-SPEC.md`
- `docs/features/skill-control-center/interfaces.md`
- `docs/features/skill-control-center/states.md`
- `docs/features/skill-control-center/queries.md`
- `docs/features/skill-control-center/operations.md`
- `docs/features/skill-control-center/BACKLOG.md`
- `docs/features/skill-control-center/implementation/backend-task-session.md`

## Hard constraints

- Consume exactly the six `/v1/control-center/*` read routes.
- One semantic core, common actions and common `data-testid` inventory.
- Exactly A Signal Deck, B Ops Rail and C Guided Ledger; no fourth shell.
- Unknown invocation evidence is unavailable/unknown, never zero.
- Selection is inert until explicit detail/topology action.
- Topology identity stays separated by model and has a semantic table alternative.
- Preferences/drafts/validation are local preview only.
- No Apply, Retry, Reconcile, accepted receipt or variant promotion.
- Do not use existing repository UI variants as visual references.

## Auto-selected implementation decisions

1. Native ES modules and CSS, matching the installed host and avoiding a new build dependency.
2. Shared HTML rendering core with variant-specific CSS structure, preventing semantic drift.
3. SVG graph as a complementary overview and HTML table as the exact accessible representation.
4. `localStorage` for the browser-local demonstration draft, with explicit non-authoritative copy.
5. Representative evidence before the full 204-row matrix; the unmaterialized matrix is preserved
   as explicit residue and never claimed complete.

## Gate verdict

PASS. The source contracts, write scope, backend route surface and validation paths were all
available. No blocker-level choice remained after the existing Phase 1 decision.
