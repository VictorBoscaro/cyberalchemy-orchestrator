---
feature: agent-provenance-telemetry
artifact: reference-probe-tool-compatibility-alias
status: compatibility-alias
version: 0.5.0
created: 2026-07-23
last_updated: 2026-07-23
---

# Reference Probe compatibility alias

The product concept formerly called `reference-probe` is now
[Reference Scout](reference-scout-tool.md).

This path remains available for inbound documentation links. Frozen schema, profile, event and
operation identifiers containing `reference-probe` remain valid v1 compatibility identifiers; new
product language, runtime operation names and projection names use `reference-scout`.

This alias does not describe the separate ACI publication-receipt spike.

It also does not identify Reference Scout with the general `ProbeTool -> ProbeRun(lens_ref) ->
observations[]` family. A Scout invocation is a `ScoutRun` owning `recommendations[]`; frozen v1
`probe` spellings on that run are compatibility identifiers, not evidence of subtype or containment.
