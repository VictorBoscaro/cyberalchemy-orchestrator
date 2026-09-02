# Negative vectors

`fixtures/negative-vectors.json` is executable and pins both error code and path. The validator
applies 41 attacks to positive fixtures; semantic context mutations are re-signed only when the
vector explicitly says `resign: true`.

| IDs | Boundary | Exact expected codes |
|---|---|---|
| AIR-N01..N08 | identity spelling/value/uniqueness | `DG_POOL_NAME_MISSING`, `DG_POOL_NAME_AMBIGUOUS` (conflict and equal), `DG_POOL_NAME_EMPTY`, `DG_POOL_NAME_TYPE`, `DG_POOL_LEGACY_NAME_FORBIDDEN`, `DG_POOL_NAME_KEY_INVALID`, `DG_POOL_IDENTITY_DUPLICATE` |
| AIR-N09..N13 | YAML stream and authority | `DG_POOL_YAML_DUPLICATE_KEY`, `DG_POOL_UNKNOWN_KEY`, `DG_POOL_DOCUMENT_COUNT`, `DG_POOL_DOCUMENT_ORDER`, `DG_POOL_METADATA_DRIFT` |
| AIR-N14..N17 | role and override | `DG_ROLE_UNKNOWN` (arbitrary and `others`), `DG_ROLE_FIT_MISMATCH`, `DG_IDENTITY_CONTEXT_SCHEMA_INVALID` at empty reason |
| AIR-N18..N23 | assignments and signed refs | `DG_AGENT_REUSED`, `DG_AGENT_ASSIGNMENT_MISSING`, `DG_AGENT_ASSIGNMENT_EXTRA`, `DG_AGENT_ASSIGNMENT_UNKNOWN`, `DG_ROLE_REGISTRY_DRIFT`, `DG_AGENT_POOL_DRIFT` |
| AIR-N24..N28 | allocator evidence | `DG_IDENTITY_CONTEXT_TAMPERED`, `DG_ALLOCATOR_SIGNATURE_INVALID`, `DG_IDENTITY_CONTEXT_STALE`, `DG_AUTHORITY_CONFLICT`, `DG_ALLOCATOR_EVIDENCE_REPLAY` |
| AIR-N29..N34 | registry immutability | `DG_ROLE_REGISTRY_SUBSTITUTION`, `DG_ROLE_REGISTRY_DUPLICATE`, `DG_ROLE_REGISTRY_DISABLED`, `DG_ROLE_REGISTRY_MISSING_ROLE`, `DG_ROLE_REGISTRY_EXTRA_ROLE`, `DG_ROLE_REGISTRY_UNTRUSTED` |
| AIR-N35..N37 | closed authorship/fit/assignment key | `DG_DRAFT_SCHEMA_INVALID`, `DG_ROLE_UNKNOWN`, `DG_AGENT_ASSIGNMENT_DUPLICATE` |
| AIR-N38 | role admitted only by illustrative future registry, checked under v1 | `DG_ROLE_UNKNOWN` |
| AIR-N39 | raw-only trusted-source substitution | `DG_POOL_SOURCE_SUBSTITUTION` |
| AIR-N40 | registry-v1 row reorder | `DG_ROLE_REGISTRY_SCHEMA_INVALID` |
| AIR-N41 | registry-name substitution | `DG_ROLE_REGISTRY_UNTRUSTED` |

Positive coverage separately proves exact v1 roles, singular `other` with signed override, Ed25519
verification, the three-name projection, real two-document v0.6 source digest/metadata/414 rows,
and preservation of every non-identity roster field during the deterministic v0.7 projection. The
unaccepted illustrative v2 fixture proves only that a structurally valid future role traverses the
unchanged pool schema when supplied as the semantic allowed set; it grants no v2 authority.
