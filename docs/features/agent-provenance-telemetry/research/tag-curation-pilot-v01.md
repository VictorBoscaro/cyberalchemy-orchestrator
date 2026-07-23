---
feature: agent-provenance-telemetry
artifact: tag-curation-pilot
status: superseded
version: 0.1.0
pool_snapshot: sha256:5c7b9745a336670ecb55df1276912166954a0d7960443f0df787405564099eba
---

# Tag curation pilot v0.1

> Superseded by discovery v0.3. This is retained as evidence of the discarded registry design; its
> candidates are not accepted tags and do not constrain agent emissions.

This pilot freezes a bounded 16-label curation batch before empirical task fixtures are selected. It
does not accept tags into the registry.

## Batch composition

Eight labels are already present in the agent-pool usage vocabulary and cover several relevant
profile perspectives:

- `software-engineering`, `information-theory`, `programming-language-design`, `epistemology`;
- `decision-theory`, `distributed-systems`, `software-architecture`, `formal-verification`.

Eight labels are required by the telemetry/ACI problem language but have zero exact occurrences in the
pool snapshot:

- `telemetry`, `provenance`, `event-sourcing`, `idempotency`;
- `replay`, `canonicalization`, `agent-orchestration`, `multi-agent-systems`.

The second group is vocabulary residue, not evidence that the concepts are absent under every synonym.
Semantic equivalence remains a curation question; the verifier asserts only exact-label facts.

## Why this sample

The batch intentionally contains both profile vocabulary and feature-native residue. Using only the
most frequent pool tags would mostly select mathematics/physics labels and would not test the boundary
between persona expertise and runtime operational language. Using only feature-native terms would not
test reuse at all.

This is a purposive contract pilot, not a statistically representative vocabulary sample. Its purpose
is to test the curation lifecycle before considering hundreds of tags.

## Required curation output

For every candidate, curation must produce:

1. one operational definition and explicit exclusions;
2. source/provenance references;
3. proposed aliases, including collision search against the full pool snapshot;
4. `lookup_only` versus `resolution_eligible` recommendation;
5. independent definition agreement and adjudicated disagreements;
6. one accept/reject/hold command proposal without applying it.

No candidate becomes `accepted` merely because it exists in `agent-pool.yaml`, appears frequently or
is used by this discovery.

## Machine-readable batch

[`../contracts/fixtures/seed-registry-candidates-v01.json`](../contracts/fixtures/seed-registry-candidates-v01.json)
pins the pool digest, exact counts, field distributions and candidate status. The D0 verifier recomputes
those facts directly from the current pool and fails on drift.
