---
node_type: craft-view
title: CRAFT — Deterministic Test-Derivation Engine
status: active
updatedAt: 2026-08-08
---

# CRAFT — Deterministic Test-Derivation Engine

> Human view of [`.craft/ledger.yml`](.craft/ledger.yml), the source of truth.

## Quick links

- Context: [`CTX-TDE-ROOT`](#context-ctx-tde-root)
- Next move: [bounded corpus validation](#next-move)
- Active blockers: none
- Blocking or open decisions: none
- Active gaps: [`GAP-TDE-POSTCONDITION-IDS-001`](#gap-gap-tde-postcondition-ids-001), [`GAP-TDE-PROGRESSION-PROSE-001`](#gap-gap-tde-progression-prose-001)
- Pending child recomposition: [`CTX-TDE-SMTFOL`](#context-ctx-tde-smtfol)
- Current package: [`ART-TDE-PACKAGE`](#artifact-art-tde-package)

<a id="context-ctx-tde-root"></a>
## `CTX-TDE-ROOT` — current state

Stage: `validate` · gate: `flag`

The committed TypeScript engine supports deterministic parsing and derivation,
content-addressed obligation keys, stable human-id allocation, residue receipts,
TypeScript/Python test emission, negative-control validation, and nested
feature-directory target resolution. Five identity maps are committed:
`financial-settlement`, `test-derivation-engine`,
`agent-execution-orchestrator`, `agents-communication-infra`, and
`agent-provenance-telemetry`.

Local validation on 2026-08-08 passed:

- `npm.cmd run typecheck`
- Vitest: 13 files, 132/132 tests

This is package-integrity evidence at the tested scope. It does not recreate the
historical corpus, E2/E3, SMT/FOL, or self-derivation evidence referenced by the
imported ledger; those external paths are absent in this checkout and their
artifact rows are marked `stale`.

## Current enablers and resolved blockers

- `ENA-TDE-VALIDATION-20260808`: typecheck and all 132 tests pass, including
  negative control, nested target resolution, stable identity, both emitters,
  and path containment.
- `BLK-TDE-GATE-HONESTY-001`: resolved in ledger history.
- `BLK-TDE-AUTH-CONVENTION-001`: resolved in ledger history.
- `BLK-TDE-COMMIT-DISCIPLINE-001`: resolved in ledger history.
- `GATE-TDE-CORPUS-GENERALIZATION-001`: historically marked resolved, but the
  supporting report is stale/missing here; no renewed corpus claim is made.

## Gaps

<a id="gap-gap-tde-postcondition-ids-001"></a>
- `GAP-TDE-POSTCONDITION-IDS-001`: per-row PC/WF/QT/MT source identity remains
  deferred; historical concept bucketing is weaker than per-row evidence.

<a id="gap-gap-tde-progression-prose-001"></a>
- `GAP-TDE-PROGRESSION-PROSE-001`: five player-progression calculation scenarios
  remained outside the deterministic fragment in the historical corpus result.

- `GAP-TDE-EMITTESTS-BODIES-001`: resolved/accepted for the deterministically
  evaluable subset; remaining cases are explicit coverage gaps rather than fake
  assertions.

<a id="context-ctx-tde-smtfol"></a>
## `CTX-TDE-SMTFOL` — pending recomposition

Gate: `flag`. The historical SMT/FOL research path is absent from this checkout,
so its claimed decidability map cannot be verified or recomposed from local
evidence. This remains residue, not a closure claim.

## Artifacts

<a id="artifact-art-tde-package"></a>
- `ART-TDE-PACKAGE` — [engine package](.) — `active`, locally validated.
- `ART-TDE-CRAFT-LEDGER` — [ledger source](.craft/ledger.yml) — `active`.
- `ART-TDE-CRAFT-VIEW` — this file — `active`.
- `ART-TDE-SPEC`, `ART-TDE-ARCH`, `ART-TDE-GLOSSARY`, `ART-TDE-WORKPACK`,
  `ART-TDE-L0-REPORT`, `ART-TDE-REFINE-RESULT`, `ART-TDE-DSFEATURE`, and
  `ART-TDE-SMTFOL-TOWER` — `stale`; their recorded paths are absent here.

## Next move

Run bounded corpus validation for the five committed id maps, record which
feature targets have executable source documents in this checkout, and replace
or retire the stale external evidence references before making a
corpus-generalization or self-derivation claim.
