# Execution Pack: RWO Recovery Decision Contract

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | pass for W0/L0 selection; later owner gates remain blocked |
| complexity | high |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `../stages/08-distill-repair.md` |
| activeLayerWindow | L0 |
| lastPlannedAt | 2026-08-05T20:01:13Z |
| readinessProfile | pilot target only |

## Wave Choreography

| Wave | Layer | Included work | Entry | Exit |
| --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 baseline | read-only hashes/import/test state | direct selected execution request | immutable baseline receipt |
| [W1](work-pack/waves/W1.md) | L0 | SWU 001 -> 002 -> 003 -> 004 | W0 pass; one selected SWU at a time | pure model executable and all L0 receipts pass |
| [W2](work-pack/waves/W2.md) | L1 | SWU 005 -> 006 | W1 pass; G1 before 006 | concurrency/restart acceptance evidence |
| [W3](work-pack/waves/W3.md) | L2 | SWU 007, 008, 009 after individual owner gates | W2 plus G1/G2/G3 as applicable | all admitted seams pass or remain typed blocked |
| [W4](work-pack/waves/W4.md) | L3 | SWU 010 + closure audits | W2/L2 receipts and G4 | owner-validated candidate delta and final evidence package |

## Parallelization Boundary

- W0–W2 are sequential.
- W3 SWUs may run in parallel only after their own owner prerequisite and when
  the parent confirms the exact three-way route. Their file scopes are disjoint.
- W4 is manual and never an automatic successor.

## Closure Obligations

- Run the targeted suite for every SWU and the accumulated runtime regression.
- Compare actual writes against `allowed-routes.json`.
- Record source, fixture, test, and receipt digests.
- Preserve failing fixtures and blockers; do not turn a repairable result into
  completion or silently consume a second retry.
- Audit spec/model-to-code alignment, owner boundaries, replay zero-call
  behavior, and ontology claim ceilings before any L3 decision.

