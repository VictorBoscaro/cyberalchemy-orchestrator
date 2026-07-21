# TASK-080 — Sequential composition, built-in recipes and client cutover

## Objective

Prove extensibility without turning the kernel into a switch over business workflow types, then
move current skills/UI to the canonical runtime boundary.

- **Layer/slice:** L4 / S-006 / W6.
- **Dependencies:** L3 pass; applicable recipe supply-chain/override/spec-split ADRs accepted.
- **Write scope:** built-in recipe/compiler modules, sequential handoff, command clients and
  compatibility tests.

## Smallest Working Units

- **SWU-ACI-028 — Sequential handoff:** deliver one committed group result once to a dependent
  group, deduped by source aggregate and connection ID; recover across restart.
- **SWU-ACI-029 — Two immutable built-ins:** define read-only `research` and `review` recipe packages
  with schemas, prompts/contracts, digests and finite graphs.
- **SWU-ACI-030 — Recipe compiler:** compile either built-in to the same canonical `DispatchSpec`;
  reject invalid capability/policy combinations before confirm.
- **SWU-ACI-031 — Skill/UI migration:** make existing authoring surfaces command clients; preserve
  legacy fallback only for explicitly legacy-managed dispatches; collect cutover/rollback receipt.
- **SWU-ACI-032 — Kernel specialization audit:** automated/review check finds no `if research`,
  `if review` or provider branch in domain/application kernel code.

| SWU | Dependencies | Write scope | Acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|
| 028 | L3 pass | connection/handoff modules | restart-safe one-handoff trace | duplication/fault tests | local-fallback |
| 029 | recipe ADRs | built-in recipe packages | immutable digests and schema fixtures | package validation | local-fallback |
| 030 | 029 | recipe compiler | equivalent canonical specs and rejection cases | compiler contract tests | local-fallback |
| 031 | 028-030 | skills/UI/API clients | cutover and rollback receipt; no dual owner | compatibility E2E | local-fallback |
| 032 | 031 | audit/check only | zero provider/business branches in kernel | static scan + review | manual |

## Done when

Both recipes and a sequential two-group run recover correctly, and a runtime-managed dispatch has
exactly one execution authority from confirmation through official close.
