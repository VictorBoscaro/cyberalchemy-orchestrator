---
feature: agent-provenance-telemetry
artifact: seed-registry-gate
status: superseded
version: 0.1.0
---

# Empirical seed-registry gate

> Superseded by discovery v0.3. This is retained as evidence of the discarded registry design; raw
> string capture does not wait for a seed registry.

The empirical registry used by P001–P003 cannot yet be honestly frozen.

The local agent pool supplies a coarse `field` and 721 usage-derived expertise labels, but the labels
do not carry one definition per tag. Importing them all as `accepted` would manufacture definitions
and give a profile vocabulary runtime authority it does not currently possess.

## Admission rule

A fixture-independent seed registry may be frozen only when every admitted tag has:

- stable `tag_id` and canonical label;
- non-empty operational definition;
- provenance reference and source snapshot digest;
- lifecycle status;
- aliases reviewed for NFC/collision safety;
- an explicit rule stating whether it is eligible for canonical resolution or lookup only.

Agent-pool labels may enter initially as `candidate`/`lookup_only`. P001's primary free-emission metric
does not need them. The resolved-ID agreement metric runs only over `accepted` and
`resolution_eligible` tags.

## Independence from probe fixtures

The registry manifest and digest must be frozen before selecting or revealing the 12 P001/P002 task
fixtures. Four additional held-out fixtures remain unavailable to registry curators. Any later registry
change creates a new probe run; it cannot retroactively improve coverage or agreement.

## Next evidence

Produce a bounded curation pilot for a small, explicitly sampled subset of pool tags. Measure definition
agreement, alias collisions and residue before deciding whether broader import is worth its governance
cost. Until then, the synthetic registry under `contracts/fixtures/` is conformance data only.
