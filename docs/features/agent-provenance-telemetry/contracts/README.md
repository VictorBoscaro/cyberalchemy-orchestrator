---
feature: agent-provenance-telemetry
artifact: d0-contract-fixture
status: superseded
version: 0.1.0
canonical_policy: aci-cjson-1
---

# D0 executable contract fixture

> Superseded by discovery v0.3. This pack is retained as evidence of the discarded registry and
> resolution design; it is not the current topic-emission contract.

This pack turns the discovery's first telemetry boundary into executable conformance evidence without
creating another runtime, journal or canonicalization authority.

## Boundary

The pack covers four record projections:

1. `topic.emission_observed@1` — immutable agent testimony plus writer-stamped lineage;
2. `tag.resolution_projected@1` — system resolution relative to one registry/resolver pair;
3. `tag.registry_snapshot@1` — versioned system-managed tag definitions;
4. `lens.projected@1` — derived lexical organization referencing resolutions.

It verifies:

- free and assisted emissions cannot collapse into one payload;
- resolution cannot rewrite or embed raw emission terms;
- residue belongs to resolution, not testimony;
- every lens element cites a resolution included by the lens;
- accepted registry tags have definitions;
- unknown keys fail closed in these candidate projections;
- canonical projected JSON bytes and SHA-256 remain stable.
- the 16-candidate curation batch still matches the pinned pool bytes, exact counts and 8+8
  present/residue composition without premature promotion.

## Canonicalization dependency

Canonical bytes reuse `aci-cjson-1` from
[`ADR-001`](../../agents-communication-infra/adrs/ADR-001-persistence-replay-and-canonical-contracts.md).
The verifier implements only the already-projected JSON subset needed by these fixtures and first
checks itself against the ACI golden canonical strings. It is not a normative replacement for the
future ACI runtime canonicalizer and does not validate raw decimal/timestamp inputs.

Each vector's digest is over `record_without_digest` only. A runtime envelope would append the named
`digest_field` after computing it. IDs in this fixture are opaque and are not claimed to be
content-addressed.

## Run

```powershell
python docs/features/agent-provenance-telemetry/contracts/verify_contracts.py
```

Use `--print-digests` only while freezing a new vector; committed vectors must pass without it.

## Explicit non-claims

Passing this fixture does not prove append-only persistence, authenticated context, sole-writer
enforcement, CAS, idempotent retries, registry lifecycle transitions, lens utility or any empirical
probe. Those remain later gates.

The registry in these vectors is a small synthetic conformance registry. It is not the
fixture-independent empirical seed registry required by P001/P003; that gate is documented in
[`../research/seed-registry-gate.md`](../research/seed-registry-gate.md).
