# Mint — Experiment Profile

PROFILE_ID: sigil-development
LIFECYCLE_OWNER: sigil-development
ARTIFACT_TYPE: sigil
CONTRACT_PATH: .claude/skills/mint/SKILL.md
PROMPT_SET: development/example-prompts/
REGIME_SET: development/regimes/ (loop-first; not yet populated — smoke regime below)
PROFILE_VALIDATION: pass

## What this harness validates
Mint is intended-not-shipped emit-logic. A "run" = a native subagent plays Mint: given a small
`<DOMAIN>` spec, it follows `cyberAlchemy-v2/development/mint/templates/EMIT-PROCEDURE.md` to emit the
domain authority spine (core 6 + the 13 committed additions) into a scratch target, then runs the §7
self-checks (1–9). The harness verifies the emitted output against the acceptance markers — turning the
static build checks into an executed pass on a domain OTHER than the resonantos fixture (generalization probe).

## Acceptance markers (from EMIT-PROCEDURE §7 + WORK-PACK SWUs)
1. parses — every emitted authority-model table parses (4 cols, no dangling `<...>`).
2. default-deny — every proposed kind has a non-empty Blocked-use cell.
3. no-leak — zero "as (an) (external) method authority" matches; cav2 only in citation/precedent/forbid frame.
4. domain-originated — ≥1 kind fails F3(c) vs every cav2 D49 row (lexical AND owner-route new).
6. methods present (#13) — every domain-originated kind has a METHODS-CATALOGUE block.
7. ratify-close (#11) — no AUTHORITY-MODEL row left `PROPOSED` without a matching `defer` in the ratify record.
8. seed-format zero-cav2-rows (#3/#17) — AUTHORITY-POSTURES has none of cav2's 8 posture names; CONSTITUTION-IMPORT-PACK has no `CAV2-C*` rule body.
9. drift-audit target resolves (#8) — DEFINITION-DRIFT-AUDIT + DEFINITIONS-INDEX exist and the constitution rule points at them.

## Golden fixtures
- resonantos-economy-research (external sibling) — the hand-done precedent for the core 6.
- examples/release-approval/ (in-repo worked example) — the core-6 emitted shape.
- This harness adds a FRESH domain (see example-prompts/mint-smoke-01.md) to exercise the additions + generalization.
