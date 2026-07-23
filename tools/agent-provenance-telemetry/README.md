# Agent Provenance Telemetry — pure L0

This package implements only APT-owned pure contract candidates: exact decoders, validation,
normalization, canonical-payload candidates, an injected candidate canonicalizer, fixture-only
reducer kernels and partial as-of projector candidates. TASK-120 owns the final query contracts.

It deliberately contains no durable adapter, bus, journal reader/writer, receipt authority,
profile registry, artifact backend or runtime enablement. Artifact/profile/acceptance references
are structural values, not locally verified authority. Fixture events are explicitly marked
`fixture-supplied-unverified`. A digest returned by an injected candidate canonicalizer is test
evidence only and never claims ACI canonical compatibility.

Run:

```powershell
npm.cmd test
npm.cmd run typecheck
```
