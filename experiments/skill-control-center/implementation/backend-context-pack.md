# Backend Phase 1 context pack

Session evidence only; this is not a canonical feature specification.

## Context Pack Summary

- Task: bounded Skill Control Center backend Phase 1
- Mode: lean, strict
- Files selected: 8
- Snippets selected: 15
- Obligation coverage: 100%
- Noise ratio: low
- Handoff pack: none; execution is local
- Strict coverage: pass
- Blockers: 0

## Obligations

| ID | Obligation | Evidence | Resolution |
|---|---|---|---|
| BE-01 | Publish exactly six read routes | `interfaces.md` External API + IF-I6 | covered |
| BE-02 | Keep apply/retry/reconcile/receipt and promotion absent | `SPEC.md` SCC-R-010/013; `BACKLOG.md` guardrails | covered |
| BE-03 | Preserve three separate topology owners | `architecture.md` AR-003; `queries.md` GetTopology | covered |
| BE-04 | Deterministic bounded paths and typed absence | `queries.md` FindPath formal rules | covered |
| BE-05 | Never convert missing usage into zero | `SPEC.md` SCC-R-004..009; `queries.md` GetUsageEvidence | covered |
| BE-06 | Local preference/draft/preview only | `operations.md` three total result matrices | covered |
| BE-07 | Mount additively without changing legacy endpoints | `implementations/server/main.py` router/static structure | covered |
| BE-08 | Reuse existing ledger read semantics | `implementations/server/ledger.py` load/read/find selectors | covered |
| BE-09 | Commit scale/negative fixtures and tests | `SPEC.md` Fixture Contract; `BACKLOG.md` Phase 1 guardrails | covered |

## Included Context

- `docs/features/skill-control-center/SPEC.md` — scope, formal rules, fixtures — BE-02/03/05/09.
- `docs/features/skill-control-center/interfaces.md` — six HTTP routes, envelopes, publication gate — BE-01/02.
- `docs/features/skill-control-center/queries.md` — inputs, outputs, ordering, path/evidence algebra — BE-03/04/05.
- `docs/features/skill-control-center/operations.md` — local CAS and validation preview matrices — BE-06.
- `docs/features/skill-control-center/architecture.md` — adapters, dependency rules, authoritative boundary — BE-02/03/07.
- `docs/features/skill-control-center/BACKLOG.md` — explicit post-Phase-1 work — BE-02/09.
- `implementations/server/main.py` — additive FastAPI host — BE-07.
- `implementations/server/ledger.py` — lenient read-only ledger adapter — BE-08.

## Decisions (`--auto`)

- Use a ports/read-model package under `server/control_center`; safest match for AD-001.
- Bind the local reader explicitly and fail-close publication when any binding is missing.
- Return unavailable/null usage because no accepted observation source exists.
- Keep local operations as internal Python ports; do not add a seventh external route.
- Use deterministic committed fixtures; do not treat synthetic evidence as runtime authority.

## Excluded Candidates

- Existing static UI variants — frontend is outside this task and explicitly rejected as design input.
- Runtime authoritative services — forbidden dependency for Phase 1.
- Raw telemetry prompts/returns — excluded by the evidence contract.
