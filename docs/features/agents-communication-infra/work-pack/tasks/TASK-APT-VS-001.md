# SWU-ACI-APT-VS-001 — Local provenance/bus vertical slice

## Status

- Descriptor: frozen candidate
- Documentation gate: Stage-A authoring complete pending independent review
- Mutation-test authorization: pending
- Local-pilot serve enablement: blocked
- Production, external network, provider execution, materializer and audit-ledger cutover: blocked

## Objective

Deliver one local single-host path:

```text
runtime activation Session
  -> strict existing-dispatch link
  -> opaque reference-probe capability
  -> durable publication candidate
  -> parent receipt verification
  -> exactly one official message
  -> APT capture/facts/probe lineage
  -> restart and deterministic readback
```

The exact machine-readable contract is
[`SWU-ACI-APT-VS-001.json`](../descriptors/SWU-ACI-APT-VS-001.json). This task does not authorize
full RunLifecycle, provider launch, reveal/vote/commit, automatic orchestration or ledger writes.

## Entry predicate

All terms must be true and digest-bound in the root authorization receipt:

1. APT `TASK-105=accepted`, with final code/test/contract evidence digest.
2. ACI `SWU-ACI-001=accepted`.
3. ACI `SWU-ACI-002=accepted`.
4. B-001/B-002 are closed.
5. B-003's W0 contract is frozen while physical target-host proof remains open.
6. All four exact protocol profile registrations pass independent review.
7. Storage/artifact ownership review passes.
8. Architecture, product/protocol, engine and root approve only this descriptor digest.

Failure or absence of any term leaves mutation blocked.

## Two-step enablement

`mutationTestAuthorization` permits only descriptor-bound code, immutable migrations, tests and
temporary/test databases. After its execution receipt and independent implementation review pass,
a separate `localPilotServeEnablement` may permit `127.0.0.1` serving with explicit configuration
and a dedicated local database.

Neither gate promotes production, external networking, agent execution, materializer or cutover.

## Acceptance

The complete descriptor test matrix passes; authoritative-table hashes survive projection rebuild;
the ledger byte hash never changes; no request body supplies authority; a candidate becomes official
only through atomic parent verification; reference-probe lineage resolves an official message and
the exact registered profile.

