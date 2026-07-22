---
feature: agents-communication-infra
review_date: 2026-07-21
scope: SWU-ACI-001
algorithm: SHA-256
composition: "SHA256(UTF8(join(path=lowercase_sha256, LF)))"
review_set_sha256: 70c2312b9ecd75bfa814ba9548fa11c3508b75a662fec42db3d29b71429b310b
status: reviewed-pass
runtime_gate: block
---

# SWU-ACI-001 final implementation baseline

This review set follows remediation of all findings in the first independent implementation
review. It remains W0 contract evidence only and does not promote any runtime gate.

| Path | SHA-256 |
|---|---|
| `docs/features/agents-communication-infra/adrs/ADR-001-persistence-replay-and-canonical-contracts.md` | `5c932f4a41d9269a5750278f18f4908b24462d8b67068f36fa0c848e63391885` |
| `docs/features/agents-communication-infra/adrs/fixtures/canonical-contract-vectors.json` | `b29eba75b6bf157526e2c2fd60cc535d843b4c32298ccd81b1032dcb9130f8f1` |
| `docs/features/agents-communication-infra/adrs/fixtures/SWU-ACI-001-TEST-PLAN.md` | `ce3c78c1e79e69c911ce0c5d00d3e6feca41bc0f418eee2825652cd11a906267` |
| `docs/features/agents-communication-infra/adrs/fixtures/slice0-schema.sql` | `72e644e9cfea36e7e6ca94240d0138d8508023e2d2f25acb3ed64b0a061c9be0` |
