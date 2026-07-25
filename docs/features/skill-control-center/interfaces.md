# Interfaces: Skill & Dispatch Control Center

Phase 1 exposes one host-neutral HTTP/JSON read contract plus internal local-preference and draft
ports. Deployment host, authentication mechanism and route owner remain unresolved by OQ-SCC5;
an implementation must bind them explicitly or report the interface unavailable. No endpoint in
this document applies, approves, retries or reconciles authoritative configuration.

## External: Control Center Read API (HTTP/JSON)

**Version prefix:** `/v1/control-center`  
**Auth:** inherited from the explicitly bound host; never invented by this feature  
**Content type:** `application/json`

### ResponseEnvelope

Every endpoint returns:

| Field | Type | Maps To |
|---|---|---|
| `request_id` | string | [Common Query Contract](queries.md#common-query-contract) |
| `schema_version` | string | [Common Query Contract](queries.md#common-query-contract) |
| `scope_id` | string | [Common Query Contract](queries.md#common-query-contract) |
| `snapshot_id` | string/null | [Common Query Contract](queries.md#common-query-contract) |
| `result_state` | enum | `complete`, `partial`, `unavailable`, `error` |
| `error_scope` | enum/null | `domain`, `transport`, `protocol`; null unless result is error |
| `completeness` | enum | `complete`, `partial`, `unavailable` |
| `source_facts` | array | [Evidence contract](discovery/control-center.md#5-evidence-and-observation-contract) |
| `warnings` | array | Safe typed diagnostics |
| `data` | object/null | Query-specific response; conditional under [state mapping](queries.md#state-mapping) |

### HTTP status mapping

| HTTP | Condition | Body rule |
|---|---|---|
| `200` | Complete/partial/unavailable query result or typed domain outcome | Full `ResponseEnvelope`; unavailable has null data |
| `400` | Syntactically invalid request or typed `invalid-request` | Envelope with safe field errors |
| `404` | Route does not exist | Host response; never used for a query-level `not-found` |
| `409` | `invalid-cursor` or `stale-snapshot` | Envelope with query state and current safe snapshot hint |
| `422` | Valid JSON violates endpoint schema | Envelope with safe validation errors |
| `500` | Transport/protocol failure | `result_state=error`, `error_scope=transport|protocol`, null data |

Query-level `not-found`, `invalid-endpoint`, `no-path` and domain `error` use HTTP 200 because the
request was processed and their typed semantics are carried inside the envelope.

### GET /v1/control-center/attention

**Exposes:** [GetAttentionQueue](queries.md#getattentionqueue)

**Request query parameters:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id` | string | `GetAttentionQueue.scope_id` |
| `request_id` | string | `GetAttentionQueue.request_id` |
| `window_start_utc` | timestamp | `GetAttentionQueue.window_start_utc` |
| `window_end_utc` | timestamp | `GetAttentionQueue.window_end_utc` |
| `kinds` | repeated string | `GetAttentionQueue.kinds` |
| `severity` | repeated string | `GetAttentionQueue.severity` |
| `object_kind` | repeated string | `GetAttentionQueue.object_kind` |
| `limit` | integer | `GetAttentionQueue.limit` |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Complete/partial/unavailable | Envelope + attention data per query |
| 400/422 | Invalid window/filter/limit | Envelope + `query_state=invalid-request` |

### GET /v1/control-center/catalog

**Exposes:** [SearchCatalog](queries.md#searchcatalog)

**Request query parameters:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id`, `request_id` | string | Common query input |
| `query` | string | `SearchCatalog.query` |
| `object_kinds` | repeated enum | `SearchCatalog.object_kinds` |
| `status`, `evidence_class`, `freshness` | repeated enum | `SearchCatalog.filters` |
| `has_attention` | boolean | `SearchCatalog.filters.has_attention` |
| `limit` | integer | `SearchCatalog.limit` |
| `cursor` | string | `SearchCatalog.cursor` |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Success/no-match/partial/unavailable | Envelope + catalog data |
| 409 | Invalid cursor or stale snapshot | Envelope + exact typed query state |
| 400/422 | Invalid query/filter | Envelope + `invalid-request` |

### GET /v1/control-center/objects/{object_kind}/{object_id}

**Exposes:** [GetObjectDetail](queries.md#getobjectdetail)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `object_kind` | enum | `GetObjectDetail.object_kind` |
| `object_id` | string | `GetObjectDetail.object_id` |
| `scope_id`, `request_id` | string | Common query input |
| `window_start_utc`, `window_end_utc` | timestamp | Optional evidence window; both or neither |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Found, query-level not-found, partial or unavailable | Envelope + detail data when trustworthy |
| 400/422 | Unsupported kind/window | Envelope + `invalid-request` |

### GET /v1/control-center/topology/{model}

**Exposes:** [GetTopology](queries.md#gettopology)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `model` | enum | `GetTopology.model` |
| `focus_id` | string | `GetTopology.focus_id` |
| `dispatch_id` | string | Required for `intra-dispatch` |
| `direction` | enum | `GetTopology.direction` |
| `depth`, `node_limit` | integer | Bounded query limits |
| `edge_kinds` | repeated enum | Non-empty supported set |
| `scope_id`, `request_id` | string | Common query input |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Success/truncated/invalid-endpoint/unsupported-model | Envelope + typed topology data |
| 200 | Partial/unavailable identity authority | No `invalid-endpoint` claim |
| 400/422 | Invalid bounds/kinds/missing conditional dispatch ID | Envelope + `invalid-request` |

### POST /v1/control-center/path-query

**Exposes:** [FindPath](queries.md#findpath)  
**Mutation semantics:** none; POST is used only for a structured, potentially large read request.

**Request JSON:**

| Field | Type | Maps To |
|---|---|---|
| `scope_id`, `request_id`, `schema_version` | string | Common query input |
| `model` | enum | `FindPath.model` |
| `source_id`, `target_id` | string | Path endpoints |
| `dispatch_id` | string | Required for `intra-dispatch` |
| `direction` | enum | `FindPath.direction` |
| `allowed_edge_kinds` | non-empty array | `FindPath.allowed_edge_kinds` |
| `max_depth` | integer 0..10 | `FindPath.max_depth` |
| `max_paths` | integer 1..100 | `FindPath.max_paths` |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Typed complete/partial/domain-error path outcome | Envelope + `query_state` and path/error data |
| 200 | Unavailable | Envelope with null data |
| 400/422 | Invalid request | Envelope + `query_state=invalid-request` |
| 500 | Transport/protocol failure before typed result | Envelope with error scope and null data |

### GET /v1/control-center/evidence/{object_kind}/{object_id}

**Exposes:** [GetUsageEvidence](queries.md#getusageevidence)

**Path/request:**

| Field | Type | Maps To |
|---|---|---|
| `object_kind`, `object_id` | string | Observed object identity |
| `scope_id`, `request_id` | string | Common query input |
| `claim_id` | string | Evidence claim |
| `window_start_utc`, `window_end_utc` | timestamp | Half-open UTC window |

**Responses:**

| Status | Condition | Body |
|---|---|---|
| 200 | Complete/partial/unavailable evidence | Envelope + evidence data when trustworthy |
| 200 | Object not found under complete identity coverage | Envelope + `query_state=not-found` |
| 400/422 | Invalid window/object kind | Envelope + `invalid-request` |

## Internal: LocalPreferencePort

**Consumers:** Variant adapter only

| Method | Maps To | Description |
|---|---|---|
| `load(scopeId)` | Local preference read | Returns revisioned user-local preferences |
| `save(input)` | [SaveLocalPreference](operations.md#savelocalpreference) | Atomic local CAS; no external writer |

## Internal: DraftPort

**Consumers:** Variant adapter only

| Method | Maps To | Description |
|---|---|---|
| `get(proposalId)` | [ChangeProposal](discovery/control-center.md#changeproposal) read | Returns one local proposal |
| `list(scopeId)` | Local draft read | Returns local proposal summaries |
| `save(input)` | [SaveChangeProposal](operations.md#savechangeproposal) | Atomic local proposal CAS |
| `validate(input)` | [ValidateChangeProposal](operations.md#validatechangeproposal) | Stores non-authoritative validation preview |

## Forbidden Interface Inventory

The Phase 1 route/port inventory must contain none of:

- `apply`, `retry-apply`, `reconcile`, `approve-and-apply`;
- accepted receipt write/lookup semantics;
- authoritative configuration mutation;
- benchmark accept/promote/select endpoints.

If a future host already has similarly named routes, the Control Center must not bind or surface
them through this feature. Required future work is tracked by
[SCC-BL-001..008](BACKLOG.md).

## Interface Invariants

| ID | Invariant | Formal | Authority |
|---|---|---|---|
| IF-I1 | Every external route exposes exactly one query. | `count(route.exposed_query)=1` | [SPEC graph](SPEC.md#feature-concept-graph) |
| IF-I2 | External routes are side-effect free. | `write_set(external_route)=∅` | [Q-I1](queries.md#query-invariants) |
| IF-I3 | Local ports cannot reach authoritative stores. | `dependencies(local_port) ∩ authoritative_writers=∅` | [AR-005](architecture.md#dependency-and-interface-rules) |
| IF-I4 | Unknown schemas/codes fail closed. | `unknown_contract => result_state=error && error_scope=protocol` | [AD-007](architecture.md#ad-007) |
| IF-I5 | Host/auth binding is explicit or unavailable. | `host_binding=null => interface_state=unavailable` | [OQ-SCC5](discovery/control-center.md#oq-scc5) |
