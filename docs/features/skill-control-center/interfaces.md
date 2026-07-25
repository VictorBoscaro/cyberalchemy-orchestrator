# Interfaces: Skill & Dispatch Control Center

Phase 1 exposes one host-neutral HTTP/JSON read contract plus internal local-preference and draft
ports. Deployment host, authentication mechanism and route owner remain unresolved by OQ-SCC5;
an implementation must bind them explicitly or report the interface unavailable. No endpoint in
this document applies, approves, retries or reconciles authoritative configuration.

## External: Control Center Read API (HTTP/JSON)

**Version prefix:** `/v1/control-center`  
**Binding:** `host_id`, `auth_contract_id` and `route_owner_id` must all be explicitly configured  
**Content type:** `application/json`

If any binding member is absent, the entire Control Center Read API is unavailable and publishes
none of its routes. The feature never selects an authentication mechanism or route owner itself.

### ResponseEnvelope

Every endpoint returns:

| Field | Type | Maps To |
|---|---|---|
| `request_id` | string | [Common output](queries.md#common-output) |
| `schema_version` | string | [Common output](queries.md#common-output) |
| `scope_id` | string | [Common output](queries.md#common-output) |
| `snapshot_id` | string/null | [Common output](queries.md#common-output) |
| `result_state` | enum | [State mapping](queries.md#state-mapping) |
| `error_scope` | enum/null | [State mapping](queries.md#state-mapping) |
| `completeness` | enum | [Common output](queries.md#common-output) |
| `source_facts` | array | [Evidence contract](discovery/control-center.md#5-evidence-and-observation-contract) |
| `warnings` | array | [Common output](queries.md#common-output) |
| `data` | object/null | Query-specific response; conditional under [state mapping](queries.md#state-mapping) |

### HTTP status mapping

| HTTP | Condition | Body rule |
|---|---|---|
| `200` | Complete/partial/unavailable query result or typed domain outcome | Full `ResponseEnvelope`; unavailable has null data |
| `400` | Request value cannot be parsed into the declared primitive/JSON shape | `result_state=complete`, `data.query_state=invalid-request`, safe parse errors |
| `404` | Route does not exist | Host response; never used for a query-level `not-found` |
| `409` | Parsed cursor is invalid or its bound snapshot is stale | `result_state=complete`, `data.query_state=invalid-cursor|stale-snapshot` |
| `422` | Parsed values violate required/enum/range/cross-field semantics | `result_state=complete`, `data.query_state=invalid-request`, safe field errors |
| `500` | Transport/protocol failure before typed domain result | `result_state=error`, `error_scope=transport|protocol`, null data |

Query-level `not-found`, `invalid-endpoint`, `no-path` and domain `error` use HTTP 200 because the
request was processed and their typed semantics are carried inside the envelope.

### GET /v1/control-center/attention

**Exposes:** [GetAttentionQueue](queries.md#getattentionqueue)

**Request query parameters:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id` | string | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `request_id` | string | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `schema_version` | string | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `window_start_utc` | timestamp | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `window_end_utc` | timestamp | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `kinds` | repeated string | [GetAttentionQueue input](queries.md#getattentionqueue) |
| `severity` | repeated string | [GetAttentionQueue filters](queries.md#getattentionqueue) |
| `object_kind` | repeated string | [GetAttentionQueue filters](queries.md#getattentionqueue) |
| `limit` | integer | [GetAttentionQueue input](queries.md#getattentionqueue) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Complete/partial/unavailable | Envelope + attention data per query |
| 400 | Unparseable window/filter/limit | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed window/filter/limit violates semantics | `result_state=complete`, `data.query_state=invalid-request` |

### GET /v1/control-center/catalog

**Exposes:** [SearchCatalog](queries.md#searchcatalog)

**Request query parameters:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id`, `request_id`, `schema_version` | string | [SearchCatalog input](queries.md#searchcatalog) |
| `query` | string | [SearchCatalog input](queries.md#searchcatalog) |
| `object_kinds` | repeated enum | [SearchCatalog input](queries.md#searchcatalog) |
| `status`, `evidence_class`, `freshness` | repeated enum | [SearchCatalog filters](queries.md#searchcatalog) |
| `has_attention` | boolean | [SearchCatalog filters](queries.md#searchcatalog) |
| `limit` | integer | [SearchCatalog input](queries.md#searchcatalog) |
| `cursor` | string | [SearchCatalog input](queries.md#searchcatalog) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Success/no-match/partial/unavailable | Envelope + catalog data |
| 409 | Invalid cursor or stale snapshot | Envelope + exact typed query state |
| 400 | Unparseable query/filter | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed query/filter violates semantics | `result_state=complete`, `data.query_state=invalid-request` |

### GET /v1/control-center/objects/{object_kind}/{object_id}

**Exposes:** [GetObjectDetail](queries.md#getobjectdetail)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `object_kind` | enum | [GetObjectDetail input](queries.md#getobjectdetail) |
| `object_id` | string | [GetObjectDetail input](queries.md#getobjectdetail) |
| `scope_id`, `request_id`, `schema_version` | string | [GetObjectDetail input](queries.md#getobjectdetail) |
| `window_start_utc`, `window_end_utc` | timestamp | [GetObjectDetail input](queries.md#getobjectdetail) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Found, query-level not-found, partial or unavailable | Envelope + detail data when trustworthy |
| 400 | Unparseable kind/window | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed kind/window violates semantics | `result_state=complete`, `data.query_state=invalid-request` |

### GET /v1/control-center/topology/{model}

**Exposes:** [GetTopology](queries.md#gettopology)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `model` | enum | [GetTopology input](queries.md#gettopology) |
| `focus_id` | string | [GetTopology input](queries.md#gettopology) |
| `dispatch_id` | string | [GetTopology conditional input](queries.md#gettopology) |
| `direction` | enum | [GetTopology input](queries.md#gettopology) |
| `depth`, `node_limit` | integer | [GetTopology bounds](queries.md#gettopology) |
| `edge_kinds` | repeated enum | [GetTopology input](queries.md#gettopology) |
| `scope_id`, `request_id`, `schema_version` | string | [GetTopology input](queries.md#gettopology) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Success/truncated/invalid-endpoint/unsupported-model | Envelope + typed topology data |
| 200 | Partial/unavailable identity authority | No `invalid-endpoint` claim |
| 400 | Unparseable bounds/kinds | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed values violate bounds/kinds/conditional Dispatch ID | `result_state=complete`, `data.query_state=invalid-request` |

### POST /v1/control-center/path-query

**Exposes:** [FindPath](queries.md#findpath)  
**Mutation semantics:** none; POST is used only for a structured, potentially large read request.

**Request JSON:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id`, `request_id`, `schema_version` | string | [FindPath input](queries.md#findpath) |
| `model` | enum | [FindPath input](queries.md#findpath) |
| `source_id`, `target_id` | string | [FindPath endpoints](queries.md#findpath) |
| `dispatch_id` | string | [FindPath conditional input](queries.md#findpath) |
| `direction` | enum | [FindPath input](queries.md#findpath) |
| `allowed_edge_kinds` | non-empty array | [FindPath input](queries.md#findpath) |
| `max_depth` | integer 0..10 | [FindPath input](queries.md#findpath) |
| `max_paths` | integer 1..100 | [FindPath input](queries.md#findpath) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Typed complete/partial/domain-error path outcome | Envelope + `query_state` and path/error data |
| 200 | Unavailable | Envelope with null data |
| 400 | Unparseable request body | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed request violates semantic constraints | `result_state=complete`, `data.query_state=invalid-request` |
| 500 | Transport/protocol failure before typed result | Envelope with error scope and null data |

### GET /v1/control-center/evidence/{object_kind}/{object_id}

**Exposes:** [GetUsageEvidence](queries.md#getusageevidence)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `object_kind`, `object_id` | string | [GetUsageEvidence identity input](queries.md#getusageevidence) |
| `scope_id`, `request_id`, `schema_version` | string | [GetUsageEvidence input](queries.md#getusageevidence) |
| `claim_id` | string | [GetUsageEvidence input](queries.md#getusageevidence) |
| `window_start_utc`, `window_end_utc` | timestamp | [GetUsageEvidence window](queries.md#getusageevidence) |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Complete/partial/unavailable evidence | Envelope + evidence data when trustworthy |
| 200 | Object not found under complete identity coverage | Envelope + `query_state=not-found` |
| 400 | Unparseable window/object kind | `result_state=complete`, `data.query_state=invalid-request` |
| 422 | Parsed window/object kind violates semantics | `result_state=complete`, `data.query_state=invalid-request` |

When data is present its type is [EvidenceResponse](SPEC.md#evidence-inspection), whose field
contract is exactly the [GetUsageEvidence output](queries.md#getusageevidence).

## Internal: LocalPreferencePort

**Consumers:** Variant adapter only

`LocalPreferenceSnapshot = {scope_id, revision, schema_version, values}` is a local Value Object.

| Method | Input | Output / closed results | Maps To |
|---|---|---|---|
| `load(scopeId, schemaVersion)` | Non-empty local scope and schema | `LocalPreferenceSnapshot` or `local-preference-unavailable`; no write | [SaveLocalPreference input basis](operations.md#savelocalpreference) |
| `save(input)` | Exact [SaveLocalPreference input](operations.md#input) | Exact closed code set in [SaveLocalPreference transition](operations.md#state-transition) | [SaveLocalPreference](operations.md#savelocalpreference) |

## Internal: DraftPort

**Consumers:** Variant adapter only

`ChangeProposalSummary = {proposal_id, target_kind, target_id, draft_revision, lifecycle_state,
updated_at_utc}` is a local Value Object derived without authoritative status.

| Method | Input | Output / closed results | Maps To |
|---|---|---|---|
| `get(proposalId)` | Stable local proposal ID | [ChangeProposal](discovery/control-center.md#changeproposal) or `draft-not-found`; no write | [ChangeProposal](discovery/control-center.md#changeproposal) |
| `list(scopeId)` | Non-empty local scope | Ordered `ChangeProposalSummary[]` or `draft-list-unavailable`; no write | [Safe preparation](SPEC.md#safe-preparation) |
| `save(input)` | Exact [SaveChangeProposal input](operations.md#input-1) | Exact closed code set in [SaveChangeProposal transition](operations.md#state-transition-1) | [SaveChangeProposal](operations.md#savechangeproposal) |
| `validate(input)` | Exact [ValidateChangeProposal input](operations.md#input-2) | Exact closed code set in [ValidateChangeProposal transition](operations.md#state-transition-2) | [ValidateChangeProposal](operations.md#validatechangeproposal) |

## Forbidden Interface Inventory

The Phase 1 route/port inventory must contain none of:

- `apply`, `retry-apply`, `reconcile`, `approve-and-apply`;
- accepted receipt write/lookup semantics;
- authoritative configuration mutation;
- benchmark accept/promote/select endpoints.

If a future host already has similarly named routes, the Control Center must not bind or surface
them through this feature. Required future work is tracked by
[SCC-BL-001](BACKLOG.md#scc-bl-001--terminal-operation-fencing),
[SCC-BL-002](BACKLOG.md#scc-bl-002--reconciliation-and-receipt-lookup),
[SCC-BL-003](BACKLOG.md#scc-bl-003--conflict-recovery-diagram),
[SCC-BL-004](BACKLOG.md#scc-bl-004--valid-action-efficiency-score),
[SCC-BL-005](BACKLOG.md#scc-bl-005--production-only-absolute-acceptance),
[SCC-BL-006](BACKLOG.md#scc-bl-006--estimability-and-convergence),
[SCC-BL-007](BACKLOG.md#scc-bl-007--assistance-taxonomy), and
[SCC-BL-008](BACKLOG.md#scc-bl-008--withdrawal-and-worst-case-population).

## Interface Invariants

| ID | Invariant | Formal | Authority |
|---|---|---|---|
| IF-I1 | Every external route exposes exactly one query. | `count(route.exposed_query)=1` | [SPEC graph](SPEC.md#feature-concept-graph) |
| IF-I2 | External routes are side-effect free. | `write_set(external_route)=∅` | [Q-I1](queries.md#query-invariants) |
| IF-I3 | Local ports cannot reach authoritative stores. | `dependencies(local_port) ∩ authoritative_writers=∅` | [AR-005](architecture.md#dependency-and-interface-rules) |
| IF-I4 | Unknown schemas/codes fail closed. | `unknown_contract => result_state=error && error_scope=protocol` | [AD-007](architecture.md#ad-007) |
| IF-I5 | Host, auth and route owner are all explicit or the whole API is unavailable. | `any_null(host_id,auth_contract_id,route_owner_id) => interface_state=unavailable && published_routes=∅` | [OQ-SCC5](discovery/control-center.md#oq-scc5) |
| IF-I6 | The external route inventory is closed. | `external_routes = {GET attention, GET catalog, GET object detail, GET topology, POST path-query, GET evidence}` | [SPEC graph](SPEC.md#feature-concept-graph) |
