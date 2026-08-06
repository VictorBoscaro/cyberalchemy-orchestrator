# Stage 09 — Invoke Plan

## Invoke Result

- Mode: `plan`
- Complexity: `high`
- Output: split Work Pack
- Planning gate: `pass` for L0 selection
- Distill validation: `pass`
- SWUs: 10
- Recommended first SWU: `SWU-RRD-001`
- Selected/executing SWU: none
- Later owner blockers: G1–G4
- Authority/mutation effect: none

## Planning Decision

The exact model is not one implementation task. It is four proof layers:

1. L0 makes canonical IDs, case admission, classification, and identity
   transitions executable without mutable or external dependencies.
2. L1 adds RecoveryFrontier and atomic journal acceptance.
3. L2 binds domain, exact-effect, and optional ARE evidence through separately
   admitted owner contracts.
4. L3 may update the ontology only after executable evidence and a separate
   promotion decision.

This order prevents current runtime convenience from defining the model and
prevents design vocabulary from being promoted before it has executable proof.

## Artifacts

- `plan/IMPLEMENTATION-LAYERING.md`
- `plan/WORK-PACK.md`
- `plan/EXECUTION-PACK.md`
- `plan/allowed-routes.json`
- `plan/swu-manifest.json`
- `plan/DISTILL-VALIDATION.md`
- `plan/PLAN-TRANSPORT.md`
- four task contracts, five waves, and four shared context/gap/trace files

## First Executable Unit

`SWU-RRD-001` wraps the existing frozen `aci.canonical-json@1` bytes with
object-kind domain separation and proves exact IDs through golden vectors. It
is first because every stable trigger, case, decision, frontier, transition,
compensation, and reconciliation identity depends on it, while it changes no
lifecycle, storage, authority, effect, or ontology semantics.

## Handoff Boundary

The plan is `selection-ready`, not executing. A later explicit execution route
must run W0, select one SWU, and admit it through Task Session. G1–G4 remain
owner prerequisites; the Work Pack cannot substitute for those decisions.

