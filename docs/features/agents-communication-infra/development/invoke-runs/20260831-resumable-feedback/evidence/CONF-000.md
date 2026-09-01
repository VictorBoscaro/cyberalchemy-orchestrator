# CONF-000 — Contract and golden-vector closure

## Result

`PASS` for the bounded contract/golden oracle. This result authorizes CONF-001 planning and code
readiness; it is not runtime evidence for migration, persistence, replay, concurrency, rollback or
effect fencing.

## Pinned snapshot

| Artifact | SHA-256 |
|---|---|
| `confirmed-dispatch-v1/manifest.json` | `sha256:919385d226240fa66621d7b660ef49b70ad7e3d3a379bee3d7c29729243acd0a` |
| `expected-acceptance.json` | `sha256:fddfeebc18522e2e84d9dfa1a35fdfa845a798be20f160a994522e876c3e5bd2` |
| `confirmation-payload-schemas.json` | `sha256:44fbe7dd415bdcafd91c8f766f44b936e3e640234576f51aab399e5b2c565f33` |
| payload-schema dialect | `sha256:1fde625dc38238b2de389f1472ad993c580a076dcddf471e0066b54cc4a7ad26` |
| `negative-vectors.json` | `sha256:f7dd8dc62b2c23f67afc1cdc057af7d6bd7db9061c651c0f9ff3ac3c6e351807` |
| final 18-file snapshot set | `sha256:e941ba205c815f1d7a4e218d7563c413e0ff7a9ae1dd56ef1e4fb938b9ca8eb0` |

## Evidence

- All 18 JSON files strict-parse and equal their `aci-cjson-1` bytes; the manifest document set and
  every declared document digest reproduce.
- Independent red-team reproduced the authority chain, pending-to-spec projection, all derived
  IDs, both mapping bindings, command digest, ordered-payload digest, state hash and receipt links.
- The closed payload-schema dialect and bundle validate all four payloads without undefined named
  structures or constructors.
- The manifest orders 56 negative cases. Their RFC6902 targets are applicable and cover trusted
  observation, schema versions, graph/mapping closure, every derived-ID kind, replay, concurrency
  and effect-boundary scenarios.
- Twenty-one failpoints cover nine individual artifact finalizations and every remaining
  acceptance mutation through `before_commit`; runtime execution remains CONF-001 evidence.
- Two final directory-hash reads were identical. `git diff --check` reported no formatting error in
  the bounded ACI spec/plan scope.
- The repaired global runtime baseline was independently reproduced separately as 152/152 green.

## Authority boundary

CONF-000 proves only deterministic, closed and independently reproducible contract bytes. CONF-001
must still prove one authenticated single-writer SQLite acceptance ending at durable
`opening_pending`, with one pending/unclaimed audit-opening intent and zero external action.
