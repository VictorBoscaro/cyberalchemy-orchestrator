---
feature: agents-communication-infra
review_date: 2026-07-21
scope: SWU-ACI-001
algorithm: SHA-256
composition: "SHA256(UTF8(join(path=lowercase_sha256, LF)))"
review_set_sha256: 35e54db2591fc2aa88f19345f91209e7ed99a379bf06dd3dc534daf78dfbf946
status: independent-review-pending
runtime_gate: block
---

# SWU-ACI-001 implementation review baseline

This immutable review set contains only W0 contract artifacts. It is not runtime or production
evidence and does not promote `workPackGateStatus`.

| Path | SHA-256 |
|---|---|
| `docs/features/agents-communication-infra/adrs/ADR-001-persistence-replay-and-canonical-contracts.md` | `98c4a0713b554317dcd79862415fcb12a9b3d69949f7a3b8033c377c470c97f0` |
| `docs/features/agents-communication-infra/adrs/fixtures/canonical-contract-vectors.json` | `a7d414c4fb684d73de43d46afdb77ff1b9fd138c8e02daffeaa5278e5ca9d204` |
| `docs/features/agents-communication-infra/adrs/fixtures/SWU-ACI-001-TEST-PLAN.md` | `e8aa44eca8b666c367183b845426e675c1837a7974d7d9c043fe5d1ac032734a` |
| `docs/features/agents-communication-infra/adrs/fixtures/slice0-schema.sql` | `fc6dfd222f82b22c542719626bd2bef08a8a1bef96a079e0abd3c01f3c5eca47` |
