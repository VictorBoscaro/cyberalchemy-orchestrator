---
tags: [agents-communication-infra, spec, vault-reads]
node_type: spec
is_session: false
layer: [application, ontology]
nature: [technical, reference]
status: draft
version: 0.5.0
last_updated: 2026-07-23
---

# Canonical Vault Reads

## Contract Status

This W0 aspect specifies a read-only, non-authoritative projection over admitted
Markdown files. It does not authorize runtime implementation while
[`runtimeGate`](SPEC.md#gate-result) remains blocked.

[ADR-CVR-001](../adrs/ADR-CVR-001.md) is a proposed decision prepared for owner
review, not an accepted implementation authority. `runtimeGate=block` and
`workPackGateStatus=block` take precedence over its non-pass
`cvrImplementationGate=approval_packet_prepared`.

The contract settles only the vault-read portion of
[Agent tools and delegated supervision](../discovery/agent-tools-and-delegated-supervision.md#6-stateless-canonical-vault-reads).
It does not import that discovery's `ATD-6` execution-authority claim. The local
absence/context evidence behind `ATD-4` was acquired by a `helper_probe`, is durably
bounded in the discovery's [Source Snapshot and bounded inspection](../discovery/agent-tools-and-delegated-supervision.md#9-source-snapshot-and-bounded-repository-inspection),
and was independently rechecked for this W0 authoring run. It is not a
repository-global proof.

## Ownership and Authority

| Concern | Owner | Contract |
| --- | --- | --- |
| Canonical source bytes and current node/connection conventions | Files under an admitted vault root and [Vault Conventions](../../../../vault/ontology-conventions.md) | Read projections never replace or rewrite them. |
| Effective roots, caller identity, admission, privacy and limits | Host/operator configuration | Callers and agents cannot supply or widen roots or policy. |
| Query evaluation and ephemeral snapshot | [`VaultReadAPI`](#vaultreadapi) | One call captures and evaluates one coherent byte set. |
| Optional inventory | Inventory read model | It may accelerate later implementations but never decides truth or admission. |
| Runtime authorization and evidence | Existing ACI gateway/runtime contracts | This aspect cannot authorize effects or mint runtime facts. |
| CVR execution verification/finalization | External bootstrap finalizer for GUARD; common CVR guard thereafter | Exactly one applicable finalizer creates a terminal receipt; root and implementation workers never do. |
| Research provenance | APT and host-owned observation boundaries | This aspect emits no `SourceObservation`, extraction, reference-use or reference-check fact. |

## Concept Registry

| Concept | ID | Type |
| --- | --- | --- |
| [VaultReadScope](#vaultreadscope) | `agents-communication-infra.VaultReadScope` | Value Object |
| [VaultSourceSelector](#vaultsourceselector) | `agents-communication-infra.VaultSourceSelector` | Value Object |
| [VaultSourceSnapshot](#vaultsourcesnapshot) | `agents-communication-infra.VaultSourceSnapshot` | Value Object |
| [VaultNodeProjection](#vaultnodeprojection) | `agents-communication-infra.VaultNodeProjection` | Value Object |
| [VaultEdgeDeclarationProjection](#vaultedgedeclarationprojection) | `agents-communication-infra.VaultEdgeDeclarationProjection` | Value Object |
| [LogicalVaultEdgeProjection](#logicalvaultedgeprojection) | `agents-communication-infra.LogicalVaultEdgeProjection` | Value Object |
| [VaultReadAPI](#vaultreadapi) | `agents-communication-infra.VaultReadAPI` | Interface |
| [ListVaultArtifacts](#listvaultartifacts) | `agents-communication-infra.ListVaultArtifacts` | Query |
| [GetVaultArtifact](#getvaultartifact) | `agents-communication-infra.GetVaultArtifact` | Query |
| [ListLogicalVaultEdges](#listlogicalvaultedges) | `agents-communication-infra.ListLogicalVaultEdges` | Query |
| [GetLogicalVaultEdge](#getlogicalvaultedge) | `agents-communication-infra.GetLogicalVaultEdge` | Query |

## Value Objects

### VaultReadScope

An immutable projection of effective host/operator policy for one call.

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `scope_id` | string | yes | Opaque identifier for the effective policy; not a registry key. |
| `principal_id` | string | yes | Authenticated caller supplied by the host. |
| `admitted_roots` | normalized path[] | yes | Resolved, repository-contained roots; never caller input. |
| `allow_private` | boolean | yes | Explicit privilege; default is `false`. |
| `max_file_bytes` | integer | yes | Positive hard cap for the bytes of any one eligible source. |
| `max_files` | integer | yes | Positive hard cap for the number of eligible sources captured in one call. |
| `max_total_bytes` | integer | yes | Positive hard cap for the aggregate bytes of all captured sources. |
| `max_results` | integer | yes | Positive hard cap for the complete projected item set returned by one call. |
| `policy_version` | string | yes | Version included in snapshot and result digests. |

The default admitted-root set is empty and returns `policy_unavailable`. A candidate
versioned development profile admits only `vault/`, only after explicit host/operator
selection and validation of repository identity, and retains `allow_private=false`.
There is no `cwd`, environment, autodiscovery or request-derived fallback and no request
may widen any policy field.

Candidate development values are `max_file_bytes=524288`, `max_files=2048`,
`max_total_bytes=33554432`, and `max_results=10000`. All are subject to compiled safety
ceilings and profile versioning. The first three have headroom over the bounded local
source observation recorded in ADR-CVR-001; `max_results` remains provisional until
golden projection measurement. Every cap breach is call-closing
`result_set_too_large`, never a partial success.

`max_results` counts only top-level items returned by the selected method:
`list_artifacts` counts projected nodes, `get_artifact` counts its one node,
`list_edges` counts projected logical edges, and `get_edge` counts its one logical
edge. Nested sections, declarations and residue do not consume separate result slots.
The whole-source `invalid_utf8` projection is one node and consumes one artifact-result
slot.

Hidden paths and filesystem links/reparse points are denied in L0. A path is admitted
only when both its lexical path and resolved path remain under one admitted root.
`private: true` is not itself an ACL grant: without `allow_private`, list and get return
the same non-enumerating `not_found` outcome.

Admission order is normative: lexical/resolved confinement; hidden-component and
link/reparse denial; a bounded prefix/frontmatter quarantine parse sufficient to classify
privacy; privacy exclusion; then full capture and projection. Malformed or unknown privacy is
non-enumerably excluded for an unprivileged scope; a privileged scope may return its typed
residue. An excluded private source does not consume source, byte or result caps. A visible
private source under `allow_private=true` consumes all applicable caps. Capture rechecks the
admitted source after classification; mutation produces one coherent admitted snapshot or
`snapshot_conflict`.

A candidate L0 source is a regular file whose normalized name ends in `.md`, discovered
recursively below an admitted root, and which passes confinement, hidden-component, link/reparse
and privacy checks. Before capture, the entire call fails with `result_set_too_large` if any
candidate exceeds `max_file_bytes`, the candidate count exceeds `max_files`, or aggregate candidate
bytes exceed `max_total_bytes`; a candidate becomes eligible only after all three checks pass. L0
defines no caller-provided ignore pattern and does not infer eligibility from an inventory. Host
policy narrows the admitted-root set before capture; it cannot alter parsing or projection
semantics.

### VaultSourceSelector

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `relative_path` | normalized repository-relative path | yes | No absolute path, empty segment, `.` or `..`. |
| `content_digest` | SHA-256 | no | When supplied, mismatch returns `selector_stale`. |

Selectors are evidence locators, not durable artifact identities.

### VaultSourceSnapshot

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `snapshot_digest` | SHA-256 | yes | Digest of policy version plus ordered `(path, byte_digest)` entries. |
| `scope_id` | string | yes | Binds the effective scope without exposing roots. |
| `parser_version` | string | yes | Version of parsing and projection semantics. |
| `sources` | ordered source manifest | yes | Path, byte digest and bytes captured for this call. |

The snapshot is ephemeral and call-local. A query captures all admitted bytes before
projection and completes against exactly those bytes. It is never returned as a reusable
reference. Cross-request cursors and retained snapshot bytes are deferred.
List methods capture all admitted visible sources needed by that operation. Direct gets
validate and capture only the selected visible source, so their snapshot manifest contains
exactly that selected set. List/get parity compares visibility and node projection under the
same policy/parser/source state; it does not require a direct get to scan unrelated sources.

### VaultNodeProjection

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `selector` | [VaultSourceSelector](#vaultsourceselector) | yes | Source evidence. |
| `snapshot_digest` | SHA-256 | yes | Call-local snapshot identity. |
| `frontmatter` | ordered map or typed residue | yes | Parsed values without silent schema repair. |
| `title` | string or null | yes | First level-one heading when present. |
| `sections` | heading locator[] | yes | Heading text and source span. |
| `connections` | [VaultEdgeDeclarationProjection](#vaultedgedeclarationprojection)[] | yes | Ordered declarations and residue. |
| `source_parse_outcome` | parsed or whole-source typed residue | yes | Closed parse status with source digest and safe locator; never repaired content. |
| `projection_digest` | SHA-256 | yes | Digest of canonical node-projection bytes under the typed domain/version contract. |

UTF-8 with an optional BOM is accepted. Invalid UTF-8 is represented by one
`invalid_utf8` whole-source residue with the selector, snapshot digest, source byte
digest and a safe byte-span locator; its `frontmatter` is typed residue,
`title=null`, `sections=[]`, and `connections=[]`. It consumes one `max_results` item
and remains in normalized path order, but exposes no undecoded bytes or decoded content.

An unterminated frontmatter fence produces `unterminated_frontmatter`; invalid YAML
produces `invalid_frontmatter_yaml`; a restricted-loader rejection records its closed
reason. These outcomes preserve safe source/fence locators and exact source digests,
never repair frontmatter, and never invent a heading, connection or edge. A missing
`Connections` section is distinct from a malformed section.

Parser ceilings are frontmatter payload 65,536 bytes, nesting depth 32, total YAML
nodes 10,000, collection items 4,096 and individual scalar UTF-8 bytes 32,768. Aliases,
merge keys and custom/application tags are forbidden. A ceiling breach produces the
whole-source `parse_limit_exceeded` residue with safe locator/digest and the same
null/empty non-invention shape. Every ceiling and its `+1` case is a golden vector.
Parser limits are evaluated before YAML construction. When multiple parser limits are
simultaneously detectable, stable precedence is frontmatter bytes, scalar bytes, depth,
node count, then collection count.

### VaultEdgeDeclarationProjection

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `source_selector` | [VaultSourceSelector](#vaultsourceselector) | yes | Declaring file. |
| `declaration_ordinal` | integer | yes | Zero-based order among recognized or residual rows. |
| `target_text` | string | yes | Exact declared target text. |
| `relation_text` | string | yes | Exact declared relation text. |
| `description` | string | no | Exact description when present. |
| `source_span` | line range | yes | Stable locator within captured bytes. |
| `resolution` | unresolved, resolved, broken, ambiguous, external, malformed | yes | CVR-001 uses `unresolved` for recognized targets not yet resolved; CVR-002 may produce the other endpoint outcomes; residue is never dropped. |

L0 recognizes the normative `Document | Type | Description` table and the observed
legacy `Relationship` header. Free-form bullets and malformed rows remain residue.

### LogicalVaultEdgeProjection

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `logical_key` | snapshot-scoped tuple | yes | Snapshot digest, normalized source, relation and target. |
| `source` | normalized path | yes | Resolved internal endpoint. |
| `relation` | string | yes | Canonical relation for the supported rule. |
| `target` | normalized path | yes | Resolved internal endpoint. |
| `supporting_declarations` | declaration[] | yes | Ordered evidence; never empty. |
| `projection_digest` | SHA-256 | yes | Canonical digest of this projection. |

Exact same-direction duplicates collapse into one logical edge. Only the inverse pair
documented by current conventions, `derives-from` and `grounds`, is folded into one
orientation. Every other relation preserves its declared direction and spelling.
Broken, ambiguous, external and malformed declarations do not mint endpoint identity.

## VaultReadAPI

The internal interface exposes four read-only methods. The host injects
[VaultReadScope](#vaultreadscope); wire callers never submit roots, privacy flags or
principal identity.

| Wire method | Query | Input | Output |
| --- | --- | --- | --- |
| `list_artifacts` | [ListVaultArtifacts](#listvaultartifacts) | `ListArtifactsRequest` | `VaultNodeListResult` or closed error |
| `get_artifact` | [GetVaultArtifact](#getvaultartifact) | `GetArtifactRequest` | `VaultNodeResult` or closed error |
| `list_edges` | [ListLogicalVaultEdges](#listlogicalvaultedges) | `ListEdgesRequest` | `LogicalVaultEdgeListResult` or closed error |
| `get_edge` | [GetLogicalVaultEdge](#getlogicalvaultedge) | `GetEdgeRequest` | `LogicalVaultEdgeResult` or closed error |

No method writes a file, event, ledger, inventory, cache or provenance fact.

The proposed implementation boundary is a transport-neutral core under
`implementations/vault_read/`, independently tested under
`implementations/tests/vault_read/`. The first implementation slice may not import
from, add routes to, or be imported by `implementations/server/`. HTTP, MCP and
agent-tool adapters are deferred and must reuse the same core.
The exact CVR dependency pin belongs in
`implementations/vault_read/requirements.lock`; editing the existing
`implementations/requirements.txt` is rejected because it would couple the vault-read
core to the audit-ledger control plane.

## Queries

### Request Shapes

| Request | Fields |
| --- | --- |
| `ListArtifactsRequest` | optional normalized `path_prefix`; optional sorted-unique `tags_all`, `node_types`, and `statuses`; no unknown fields |
| `GetArtifactRequest` | required [VaultSourceSelector](#vaultsourceselector) `selector`; no unknown fields |
| `ListEdgesRequest` | optional normalized `source_prefix` and `target_prefix`; optional sorted-unique exact `relations`; no unknown fields |
| `GetEdgeRequest` | required `snapshot_digest`, `parser_version`, normalized `source`, exact `relation`, normalized `target`; optional `expected_projection_digest`; no unknown fields |

Paths use `/`, are repository-relative, Unicode-normalized to NFC, contain no empty,
`.` or `..` segment and are compared case-sensitively after normalization. A host whose
filesystem cannot preserve that comparison must reject the scope as `policy_unavailable`.
Filter arrays are ANDed across fields and ORed within one field. Empty arrays are invalid;
omitted fields mean no filter. Unknown request fields return `invalid_selector`.

### Result Shapes

| Result | Required fields |
| --- | --- |
| `VaultNodeListResult` | `snapshot_digest`, `parser_version`, complete ordered `items`, `result_count` |
| `VaultNodeResult` | `snapshot_digest`, `parser_version`, `item` |
| `LogicalVaultEdgeListResult` | `snapshot_digest`, `parser_version`, complete ordered `items`, `result_count` |
| `LogicalVaultEdgeResult` | `snapshot_digest`, `parser_version`, `item` |

Every success carries one snapshot digest. No L0 result contains a host root, continuation,
reusable snapshot reference or unadmitted selector. All arrays are complete; if the
complete result would exceed a cap, the query returns only `result_set_too_large`.
For direct gets, the selected existing result has cardinality one for `max_results`;
an effective policy with `max_results < 1` returns `policy_unavailable`.

### ListVaultArtifacts

Captures one ephemeral snapshot, projects every admitted document, applies filters, sorts
by normalized relative path and returns the entire bounded result.

### GetVaultArtifact

Uses the same admission and snapshot rules as the list query. Disallowed, private,
hidden, missing and out-of-root selectors are indistinguishable as `not_found`.
It validates and captures only the selected source; it does not perform a global scan.

### ListLogicalVaultEdges

Projects declaration evidence, resolves only unambiguous repository-contained targets,
deduplicates under the L0 rule and sorts by `(source, relation, target)`. Supporting
declarations sort by `(relative_path, declaration_ordinal, content_digest)`.

### GetLogicalVaultEdge

Builds the complete admitted visible edge-source candidate set exactly as
`list_edges`, applies source/file/aggregate caps to that complete set, coherently
captures/parses/projects it, then resolves the snapshot-scoped logical key. It cannot
capture only the selected endpoints. An optional expected projection digest returns
`projection_conflict` on drift.

### Per-method outcome precedence

Stages are total and stop at the first outcome. Parse residues are successful items, not
closed errors.

| Stage | `list_artifacts` | `get_artifact` | `list_edges` | `get_edge` |
| ---: | --- | --- | --- | --- |
| 1 request form | `invalid_selector` | `invalid_selector` | `invalid_selector` | `invalid_selector` |
| 2 effective policy/profile | `policy_unavailable` | `policy_unavailable` | `policy_unavailable` | `policy_unavailable` |
| 3 confinement/hidden/link | exclude denied sources | `not_found` | exclude denied sources | `not_found` |
| 4 quarantine privacy | exclude private/unknown sources | `not_found` | exclude private/unknown sources | `not_found` |
| 5 visible source/file/aggregate caps | `result_set_too_large` | `result_set_too_large` for selected source only | `result_set_too_large` over complete visible corpus | `result_set_too_large` over the same complete visible edge-source candidate set as `list_edges` |
| 6 coherent capture/recheck | `snapshot_conflict` | `snapshot_conflict` | `snapshot_conflict` | `snapshot_conflict` |
| 7 expected source/snapshot binding | not applicable | `selector_stale` | not applicable | `snapshot_conflict` |
| 8 parsing | ordered node/declaration residue or continue | selected node residue or continue | residue does not mint edge | residue makes key `not_found` |
| 9 top-level `max_results` | `result_set_too_large` | success cardinality one | `result_set_too_large` | success cardinality one |
| 10 expected projection digest | not applicable | not applicable | not applicable | `projection_conflict` |
| 11 selection/result | complete success | success or `not_found` | complete success | success or `not_found` |

For a direct get, absence discovered at stages 3, 4, 8 or 11 is the same
non-enumerating `not_found`. Pairwise collision fixtures freeze every adjacent stage and
security-sensitive nonadjacent pairs such as invalid-request+private,
private+oversized, hidden+oversized, capture-race+stale and
snapshot-conflict+projection-conflict.

## Closed Outcomes

| Code | Meaning |
| --- | --- |
| `not_found` | Missing or non-enumerable denied selector/key. |
| `invalid_selector` | Malformed selector before filesystem access. |
| `selector_stale` | Expected source digest differs. |
| `snapshot_conflict` | Files changed during capture; caller may retry the whole query. |
| `projection_conflict` | Expected logical projection digest differs. |
| `result_set_too_large` | An individual-file-byte, aggregate-byte, source-count or result-count cap would be exceeded. |
| `policy_unavailable` | Host cannot supply an effective scope. |

Errors expose no resolved host path, denied filename or private-node metadata.
Invalid encoding is intentionally absent from call-closing outcomes: it is the
whole-source `invalid_utf8` projection residue defined by
[VaultNodeProjection](#vaultnodeprojection).

## Formal Rules

| ID | Rule | Formal obligation |
| --- | --- | --- |
| CVR-R1 | Source authority and inventory independence | For identical admitted source bytes, effective scope and parser version, results are identical with inventory absent, correct or stale; source bytes—not a projection or inventory—remain authoritative. |
| CVR-R2 | Root confinement | `admitted(p) => lexical_under_root(p) && resolved_under_root(p)` |
| CVR-R3 | Authorization parity | `visible_in_get(p) == visible_in_list(p)` for the same effective scope |
| CVR-R4 | One-call coherence | `forall result: result.snapshot_digest == call.snapshot_digest` |
| CVR-R5 | No mixed bytes | a capture race yields one coherent snapshot or `snapshot_conflict` |
| CVR-R6 | Fail closed | unknown policy, hidden path, link/reparse point or cap breach cannot produce content |
| CVR-R7 | Residue preservation | every observed connection row maps to a declaration or typed residue |
| CVR-R8 | Bounded inverse normalization | only `derives-from <-> grounds` folds across direction in L0 |
| CVR-R9 | No effects | `writes + emitted_events + provenance_facts == 0` |
| CVR-R10 | Complete-call bound | no continuation token or reusable snapshot reference is emitted in L0 |

**Checked by:**
[T-CVR-1 through T-CVR-12](../TEST-SPEC.md#canonical-vault-read-contracts).
The test matrix maps each rule to at least one named fixture.

## Mapping Contract

```text
host policy
  -> VaultReadScope
  -> capture admitted paths and bytes
  -> VaultSourceSnapshot
  -> Markdown/frontmatter/Connections projections
  -> ordered nodes + raw declarations
  -> bounded logical-edge normalization
  -> complete read result
```

Canonical digests use versioned field order and SHA-256. The proposed parser pipeline is
strict byte/fence handling, a restricted YAML loader, then local Markdown and
Connections projection. `PyYAML==6.0.1` is the sole current dependency candidate
because it is the only host-observed version; host presence is not admission.

Before implementation it must be pinned in a reproducible dependency declaration/lock
and pass golden vectors. The loader rejects duplicate keys, unknown/application tags
and merge keys; aliases are rejected unless a later finite policy is independently
accepted; timestamps remain strings; only `true`/`false` receive implicit boolean
meaning. PyYAML owns neither canonicalization nor digests. Pin, loader or golden-vector
failure blocks and requires an ADR amendment; no silent upgrade is conforming.

Normative digest bytes use typed domain prefix `aci.cvr`, an explicit projection type
and schema version, followed by compact UTF-8 JSON. Each projection schema fixes field
order; strings and object keys are Unicode NFC; required nulls remain present; integers
are base-10 JSON integers; floats, NaN and infinities are forbidden; arrays retain
contract order; and JSON escapes are deterministic with no insignificant whitespace or
trailing newline. SHA-256 is computed over exactly those bytes and rendered as
`sha256:<64 lowercase hex>`. The snapshot digest uses the typed
`aci.cvr.snapshot/v1` envelope over policy/parser versions plus ordered admitted
`(path, byte_digest)` entries. The node `projection_digest` uses
`aci.cvr.node/v1` over every public node field except the digest itself. Golden vectors
in T-CVR-6 assert exact canonical bytes and both digests.

The snapshot top-level field order is `domain`, `projection_type`, `schema_version`,
`policy_version`, `parser_version`, `scope_id`, `sources`; each source entry is
`relative_path`, `byte_digest`. The node top-level field order is `domain`,
`projection_type`, `schema_version`, `selector`, `snapshot_digest`, `frontmatter`,
`title`, `sections`, `connections`, `source_parse_outcome`; nested value objects use
their contract-table field order recursively. `projection_digest` is carried beside,
not inside, the hashed node envelope.

Nested canonical schemas are closed:

- selector order: `relative_path`, `content_digest`;
- source-manifest entry: `relative_path`, `byte_digest`;
- heading locator: `text`, `level`, `source_span`;
- source span: `start_byte`, `end_byte`, `start_line`, `end_line`;
- declaration: `source_selector`, `declaration_ordinal`, `target_text`, `relation_text`,
  `description`, `source_span`, `resolution`;
- parse residue: `kind`, `source_digest`, `source_span`, `detail_code`;
- recursive frontmatter subset: null, boolean, integer, NFC string, array, or object with
  NFC string keys sorted by UTF-8 bytes. Floats and non-JSON YAML values are rejected;
  two original keys colliding after NFC normalization produce
  `invalid_frontmatter_yaml`.

All required nullable fields remain present as JSON null. Literal golden constants live
in `implementations/tests/vault_read/fixtures_canonical.py` as
`SNAPSHOT_V1_VALUE`, `SNAPSHOT_V1_BYTES`, `SNAPSHOT_V1_SHA256`,
`NODE_V1_VALUE`, `NODE_V1_BYTES` and `NODE_V1_SHA256`; tests compare the literal bytes
and digests rather than regenerating expectations with production serialization.

## Verification Obligations

Before implementation is authorized, executable fixtures must cover:

1. relative, absolute, case-normalized and `..` selectors plus root escape;
2. symlink/junction/reparse retarget denial;
3. hidden/private non-enumeration and list/get parity;
4. mutation during capture, proving coherent bytes or `snapshot_conflict`;
5. SHA-256, BOM, invalid UTF-8, malformed and legacy frontmatter;
6. deterministic artifact, logical-edge and supporting-declaration order;
7. duplicate same-direction rows and the `derives-from`/`grounds` inverse pair;
8. malformed rows and broken, ambiguous and external targets retained as residue;
9. stale selector and expected projection-digest conflict;
10. individual-file-byte, aggregate-byte, source-count and result-count caps;
11. optional inventory presence/absence with identical semantics; and
12. spies proving zero writes, events and APT/host provenance facts.

## Deferred

- reusable or persisted snapshot references and cross-request pagination;
- inventory acceleration;
- broader inverse-relation catalog or durable edge registry;
- binding to `AgentToolProfile`, runtime attempts or `EffectiveInputArtifact`;
- bus delivery, inbox/listening and delegated supervision;
- APT/host provenance emission;
- any runtime implementation while the feature gate remains blocked.

## Delivery Units

| SWU | Contract slice | Global gates | Nominal CVR gate | Current state |
| --- | --- | --- | --- | --- |
| `SWU-ACI-CVR-000` | Five-entry packet plus seven derived indexes: 12 governed artifacts including the descriptor. | `runtimeGate=block`; `workPackGateStatus=block` | `approval_packet_prepared` | Documentation prepared for owner review only. |
| `SWU-ACI-CVR-GUARD-001` | Pure verifier, fixed descriptors and common CVR-001/002 finalizer; bootstrap has one external finalizer. | `runtimeGate=block`; `workPackGateStatus=block` | Proposed one-time root bootstrap via external trusted executor. | Blocked pending five-entry packet acceptance. |
| `SWU-ACI-CVR-001` | Capture/snapshot core, artifact projection, raw Connections declarations, `list_artifacts`, `get_artifact`, and applicable tests. | `runtimeGate=block`; `workPackGateStatus=block` | No `pass_with_named_swu_authorization` exists. | Blocked. |
| `SWU-ACI-CVR-002` | Endpoint resolution, logical-edge projection, `list_edges`, `get_edge`, and applicable tests. | `runtimeGate=block`; `workPackGateStatus=block` | No `pass_with_named_swu_authorization` exists. | Blocked and deferred until CVR-001 acceptance. |

All four queries remain in this contract. The staged delivery cannot duplicate source
capture, policy admission, parser or projection authority. Exact proposed future write
scopes and ratifications are recorded in
[ADR-CVR-001](../adrs/ADR-CVR-001.md#exact-future-write-scopes).
The proposed per-SWU predicate is non-operative until ADR, this spec, TEST-SPEC, TASK-CVR and the
selected deterministic descriptor are accepted as one five-entry packet. The CVR gate can then
use, for initial bootstrap, exactly
`docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json` as the
fifth entry and
create a narrow carve-out only for the descriptor-bound isolated, effect-free unit after
all named owner acceptances and root final approval. Global gates continue to block
runtime/integration, HTTP, MCP, agent tools and server wiring. No authorization is
present now. Ordering is strictly `000 -> GUARD-001 -> 001 -> 002`; GUARD bootstrap is
non-recursive and uses an external trusted executor with only
`implementations/vault_read_guard/**/*.py` and its tests in scope.

Every later execution persists exactly three content-addressed authority artifacts:
`authorization.json`, `claim.json` and the guard-created `execution-receipt.json` under
`work-pack/authorizations/<authorization_id>/`. There is no mutable pointer, persisted
`ClaimReceipt`, revocation artifact or second terminal receipt. Descriptors are deterministic,
immutable governance packet entries, not per-execution artifacts. This protects the sanctioned
workflow from drift; unrestricted host access remains advisory and is not a sandbox.

## Decisions

| ID | Decision |
| --- | --- |
| CVR-D1 | Host/operator configuration owns effective roots, admission, privacy and limits. |
| CVR-D2 | L0 is a non-authoritative, effect-free read projection. |
| CVR-D3 | Each call uses one ephemeral in-memory snapshot and returns no continuation. |
| CVR-D4 | All four query names are retained with identical admission semantics. |
| CVR-D5 | Malformed and unresolved evidence is preserved as typed residue. |
| CVR-D6 | Only the documented `derives-from`/`grounds` inverse is normalized in L0. |
| CVR-D7 | Runtime integration, provenance and acceleration remain separately owned and deferred. |
| CVR-D8 | Invalid source encoding and frontmatter failures are ordered typed projection residue, not repaired content or a call-wide encoding error. |
| CVR-D9 | The proposed core is transport-neutral and isolated from the current audit-ledger server. |
| CVR-D10 | Root admission defaults empty; explicit versioned host/operator policy is the only admission authority. |
| CVR-D11 | CVR-001 delivers artifact reads plus raw declaration preservation; CVR-002 adds endpoint resolution and logical edges while preserving one four-query contract and one core. |
| CVR-D12 | Operation-specific capture gives list a visible-corpus snapshot and direct get a selected-source snapshot without weakening parity. |
| CVR-D13 | Typed/versioned compact JSON is the sole snapshot and projection digest authority. |
| CVR-D14 | GUARD bootstrap uses one external authority-owned finalizer; thereafter the common guard combines pure verification, closed descriptors, direct invocation and exclusive CVR-001/002 finalization. |
| CVR-D15 | CVR-002 binds the CVR-001 PASS receipt and byte baseline, allowed delta and pre-write hashes, and reruns the complete CVR-001 suite. |

## Gate Result

- Status: **block**
- CVR proposal status: `cvrImplementationGate=approval_packet_prepared` (**non-pass**).
- Predicate:
  The proposed descriptor-bound per-SWU branch is non-operative until the coordinated five-entry
  packet is accepted.
- Current predicate result: **false**.
- Reason: parser, module, policy, limits and staging are prepared for owner/root
  ratification, but no author or reviewer can promote the gates or authorize code.
- Required follow-up: obtain ratification and exact-digest review of all five entries, then
  bootstrap `SWU-ACI-CVR-GUARD-001` once through the external trusted executor. Only a GUARD PASS
  can precede a fresh descriptor-bound CVR-001 authorization. This document creates none of them.

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.5.0 | 2026-07-23 | Added non-recursive GUARD-001, five-entry packets, three-artifact authority lifecycle, sole finalization and CVR-002 baseline/delta non-regression; status remains non-pass. |
| 0.4.0 | 2026-07-23 | Unified the gate predicate, append-only authorization/claim semantics, complete `get_edge` cap set and exact isolated command contract; status remains non-pass. |
| 0.3.0 | 2026-07-23 | Prepared owner-review remediation: authority-neutral status, parser ceilings, staged privacy, operation-specific capture, canonical projection bytes/digests, and raw-declaration ownership in CVR-001. |
| 0.2.0 | 2026-07-23 | Prepared ADR-CVR-001 integration: explicit restricted parser candidate, whole-source residues, empty-root policy, candidate bounded development profile, isolated core path, SWU staging and non-pass gate precedence. |
| 0.1.1 | 2026-07-23 | Reconciled the initial four-query W0 contract and hard-limit taxonomy. |

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [Agent tools and delegated supervision](../discovery/agent-tools-and-delegated-supervision.md) | `derives-from` | Supplies the candidate four-query seam and bounded local inspection. |
| [Vault Conventions](../../../../vault/ontology-conventions.md) | `depends-on` | Owns current file labels and declared connection conventions. |
| [ACI SPEC](SPEC.md) | `refines` | Keeps the projection inside the existing ACI feature and runtime gate. |
| [APT session-dispatch research](../../agent-provenance-telemetry/discovery/session-dispatch-research-records.md) | `contextualizes` | Preserves external provenance ownership without emitting APT facts. |
| [ADR-CVR-001](../adrs/ADR-CVR-001.md) | `refines` | Proposes parser, module, policy, limit and delivery decisions without authorizing implementation. |
