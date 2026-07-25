# Queries: Skill & Dispatch Control Center

All queries are read-only, side-effect free and versioned. Their exact response ordering and
failure states below are normative Phase 1 refinements of
[SCD-01..08](discovery/control-center.md#decisions-baked-in). A query never converts an unavailable
source into an empty result, zero usage or `no-path`.

## Common Query Contract

### Common input

| Field | Type | Required | Description |
|---|---|---|---|
| `scope_id` | string | yes | Visible repository/operator scope |
| `request_id` | string | yes | Correlation identity, not evidence identity |
| `schema_version` | string | yes | Requested API schema |

### Common output

| Field | Type | Source | Description |
|---|---|---|---|
| `request_id` | string | Request | Echoed correlation identity |
| `schema_version` | string | Read API | Actual response schema |
| `scope_id` | string | Request | Evaluated scope |
| `snapshot_id` | string | Source adapters | Stable normalized source snapshot |
| `source_facts` | array | Source adapters | Expected/accepted/failed sources and revisions |
| `result_state` | enum | Query boundary | Envelope trust/completion: `complete`, `partial`, `unavailable`, `error`; errors are classified by `error_scope` |
| `error_scope` | enum/null | Query boundary | `domain`, `transport`, `protocol` when `result_state=error`; otherwise null |
| `completeness` | enum | [Evidence rules](SPEC.md#formal-rules-and-invariants) | `complete`, `partial`, `unavailable` |
| `warnings` | array | Source adapters | Safe typed limitations; never raw logs |
| `data` | query-specific | Query projector | Contains query-specific state; absent when unavailable or when error scope is transport/protocol |

`result_state` describes envelope trust/completion. `error_scope` classifies `domain`,
`transport`, or `protocol`; typed data is allowed only for a domain error and is absent for
transport/protocol errors. Each query declares a separate `query_state` for domain/query outcomes.
`partial` requires at least one trustworthy returned fact; `unavailable` carries no false empty
`data`.

### State mapping

| Situation | `result_state` | `query_state` rule |
|---|---|---|
| Healthy complete sources | `complete` | Query-specific closed state |
| Trustworthy subset plus named missing source/interval | `partial` | Cannot be an exhaustive absence state (`no-match`, `not-found`, `no-path`) |
| No trustworthy value | `unavailable` | No query state/data |
| Typed domain/traversal error after request binding | `error`, `error_scope=domain` | Minimal typed data is allowed; for FindPath it contains `query_state=error` and safe error metadata |
| Transport failure before a typed result | `error`, `error_scope=transport` | Data/query state absent |
| Protocol/schema contract failure | `error`, `error_scope=protocol` | Data/query state absent |
| Invalid input/cursor with healthy validation source | `complete` | Typed query-specific invalid state |

`invalid-endpoint` is legal only when every identity authority required by the selected topology
model has complete endpoint-resolution coverage for the bound snapshot. Otherwise the envelope is
`partial` or `unavailable`, with no `invalid-endpoint` claim.

## GetAttentionQueue

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `window_start_utc` | timestamp | yes | Inclusive UTC start |
| `window_end_utc` | timestamp | yes | Exclusive UTC end |
| `kinds` | set | no | Pending approval, blocker, degraded/stale source, conflict or failure |
| `limit` | integer 1..200 | no | Default 50 |

### Filters

| Field | Type | Default | Description |
|---|---|---|---|
| `severity` | set | all | Source-declared `critical`, `warning`, `info`; no inferred escalation |
| `object_kind` | set | skill, Dispatch, source, draft | Restricts returned targets |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `items` | `AttentionProjection[]` | Dispatch/source/draft adapters | Priority facts with stable object ID, reason, state, scope, evidence and safe next action |
| `query_state` | enum | Query projector | `success`, `invalid-request` |
| `empty_reason` | enum/null | Query projector | `no-actionable-item` only on complete success; otherwise null |
| `next_cursor` | string/null | Query projector | Opaque stable pagination cursor |

### Ordering

Items sort by source-provided severity rank (`critical < warning < info`), then
`occurred_or_detected_at_utc` descending, `object_kind` ascending and stable `object_id` ascending.
Missing time sorts last. Pagination uses the full sort tuple and snapshot ID.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Dispatch records | queries | Pending/open/closed state, blockers, stable ID, source revision |
| Source health projection | source-contract | Ingestion/freshness/degradation facts |
| `ChangeProposal` records | queries | Local conflict/save/validation state only |

**Authority:** [Task-led landing](discovery/control-center.md#task-led-landing).

## SearchCatalog

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `query` | string | no | Trimmed Unicode search string; empty means no text constraint |
| `object_kinds` | set | yes | Non-empty subset of `skill`, `dispatch` |
| `filters` | object | no | Cumulative filter values |
| `limit` | integer 1..200 | no | Default 50 |
| `cursor` | string | no | Opaque cursor bound to filters and snapshot |

### Filters

| Field | Type | Default | Description |
|---|---|---|---|
| `status` | set | all | Object-kind-specific source status |
| `evidence_class` | set | all | Exact evidence class match |
| `freshness` | set | all | `fresh`, `stale`, `unknown` |
| `has_attention` | boolean/null | null | Restricts by returned attention projection |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `matches` | array | Skill/Dispatch projections | Stable ID, kind, display label, status, matched fields, evidence summary |
| `query_state` | enum | Query projector | `success`, `no-match`, `invalid-request`, `invalid-cursor`, `stale-snapshot` |
| `active_filters` | object | Request normalization | Exact filters applied |
| `no_match` | boolean | Query projector | True only on complete successful search with zero matches |
| `next_cursor` | string/null | Query projector | Snapshot-bound cursor |

The canonical text key is: Unicode NFKC, locale-independent Unicode default case-fold, trim leading
and trailing whitespace, collapse each internal Unicode whitespace run to U+0020, then compare
Unicode scalar-value sequences lexicographically. Matches sort by that key, object kind and stable
ID. Search discloses which fields matched; it never searches raw prompts, returns or logs.

A cursor contains snapshot ID, normalized query/filter digest and full last sort tuple. Invalid
encoding/signature yields `invalid-cursor`; a valid cursor whose snapshot is no longer available
yields `stale-snapshot`; query/filter mismatch yields `invalid-cursor`. Neither silently restarts
pagination.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Skill source records | queries | ID, label, path metadata, status/evidence summary |
| Dispatch records | queries | Dispatch ID, task label, state, lineage/source summary |

**Authority:** [Task-led landing](discovery/control-center.md#task-led-landing),
[required operator answers](discovery/control-center.md#required-operator-answers).

## GetObjectDetail

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `object_kind` | enum | yes | `skill` or `dispatch` |
| `object_id` | string | yes | Stable object identity |
| `window_start_utc` | timestamp | no | Required only when evidence overlay requested |
| `window_end_utc` | timestamp | no | Required only when evidence overlay requested |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `identity` | object | Owned source | Stable ID, kind and display metadata |
| `query_state` | enum | Query projector | `found`, `not-found`, `invalid-request` |
| `source_revision` | string | Source adapter | Revision/hash used |
| `relations_available` | `TopologyModel[]` | Topology projectors | Models supported for this object |
| `evidence` | `EvidenceAnswer`/null | Evidence projector | Proof, coverage and freshness when requested |
| `safe_actions` | set | Query projector | Subset of `open-detail`, `open-topology`, `edit-local-preference`, `edit-draft` |
| `authority_route` | literal | Scope decision | Always `unavailable` for non-local configuration in Phase 1 |

Absent object returns `not-found`; source failure returns `unavailable` or `partial`, never
`not-found`.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Skill or Dispatch record | queries | Identity, metadata, source revision |
| Evidence projection | source-contract | Optional claim/scope/window answer |

**Authority:** [Explicit transitions](discovery/control-center.md#explicit-transitions),
[Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision).

## GetTopology

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `model` | [`TopologyModel`](discovery/control-center.md#topologymodel) | yes | Exactly one model |
| `focus_id` | string | yes | Node to center |
| `dispatch_id` | string | conditional | Required exactly when `model=intra-dispatch`; scopes `focus_id` as `(dispatch_id, group_id)` |
| `direction` | enum | no | `outbound`, `inbound`, `both`; default `both` |
| `depth` | integer 0..10 | no | Default 1 |
| `edge_kinds` | non-empty set | yes | Supported by selected model |
| `node_limit` | integer 1..1000 | no | Default 200 |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `model` | `TopologyModel` | Request | Selected isolated model |
| `query_state` | enum | Query projector | `success`, `invalid-request`, `invalid-endpoint`, `unsupported-model`, `truncated` |
| `focus_id` | string | Request | Centered stable node |
| `nodes` | array | Model projector | Stable IDs and safe display metadata |
| `edges` | array | Model projector | Directed typed edges with evidence IDs and provenance |
| `semantic_rows` | array | Model projector | Same nodes/edges in deterministic list/table order |
| `truncated` | boolean | Projector | True when depth/node/source limit hides data |
| `more_available` | boolean/unknown | Projector | Unknown when source completeness cannot prove it |

Model rules:

- `skill-relations`: `explicit_path`; optional inclusive mode adds `named_reference`.
- `dispatch-lineage`: parent/child edges only from `parent_dispatch_id`.
- `intra-dispatch`: group connections scoped by `(dispatch_id, group_id)`.

Nodes sort by stable ID. Edges sort by `(source_id, edge_kind, evidence_id, target_id)`.
Graph and semantic rows contain the same ordered identity sets.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Skill relation projection | source-contract | Skill IDs, typed evidence edges |
| Dispatch lineage projection | source-contract | Dispatch IDs and parent IDs |
| Intra-Dispatch projection | source-contract | Scoped groups and declared connections |

**Authority:** [Separate topology models](discovery/control-center.md#4-separate-topology-read-models).

## FindPath

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `model` | [`TopologyModel`](discovery/control-center.md#topologymodel) | yes | Exactly one model |
| `source_id` | string | yes | Existing endpoint in selected snapshot |
| `target_id` | string | yes | Existing endpoint in selected snapshot |
| `dispatch_id` | string | conditional | Required exactly for `intra-dispatch`; endpoints are `(dispatch_id, source_group_id)` and `(dispatch_id, target_group_id)` |
| `direction` | enum | yes | `outbound`, `inbound`, `undirected-view` |
| `allowed_edge_kinds` | non-empty set | yes | Supported for selected model |
| `max_depth` | integer 0..10 | yes | Zero permits only source=target path |
| `max_paths` | integer 1..100 | yes | Positive result limit |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `query_state` | enum | Path engine | `success`, `no-path`, `invalid-request`, `invalid-endpoint`, `unsupported-model`, `truncated`, `error` |
| `paths` | array | Path engine | Ordered complete bounded paths when allowed by state |
| `applied_limits` | object | Request | Normalized depth/path limits |
| `returned_depth` | integer/null | Path engine | Maximum returned complete path length |
| `more_paths_exist` | boolean/unknown | Path engine | Unknown under incomplete sources |

### Formal traversal rules

1. Validate request/model/edge kinds and both endpoints before traversal.
2. For `intra-dispatch`, validate `dispatch_id` and resolve endpoints only as composite
   `(dispatch_id, group_id)` identities; a group ID alone is never globally resolvable.
3. Return `invalid-endpoint` only when all identity authorities required by the selected model
   report complete endpoint-resolution coverage; a partial or unavailable identity source yields
   top-level `result_state=partial|unavailable` and no path query state.
4. Edge identity is `(source_id, edge_kind, evidence_id, target_id)`.
5. Visit a node at most once in one candidate path; cycles are allowed across different paths.
6. Sort complete paths by edge count, then lexical full edge-identity sequence.
7. Normalize exact duplicate edge IDs once; retain non-identical parallel edges.
8. Partial sources may return `truncated`, never `no-path` or `invalid-endpoint`. A traversal/domain
   failure after the request and snapshot are bound returns top-level `result_state=error`,
   `error_scope=domain`, and minimal data `{query_state:"error", error_code, safe_message,
   snapshot_id}`. A transport/protocol failure before a typed domain result returns
   `result_state=error`, the matching `error_scope`, and absent data/query state.
9. Every returned edge carries kind, evidence ID/class, provenance and snapshot.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Exactly one topology projection | source-contract | Nodes, directed typed evidence edges, completeness |

**Authority:** [Deterministic Path Query Contract](discovery/control-center.md#6-deterministic-path-query-contract).

## GetUsageEvidence

**Type:** Query (read-only)  
**Actor:** Operator

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| Common input | object | yes | [Common Query Contract](#common-query-contract) |
| `object_kind` | string | yes | Supported observed object kind |
| `object_id` | string | yes | Stable observed object identity |
| `claim_id` | string | yes | Requested usage/evidence claim |
| `window_start_utc` | timestamp | yes | Inclusive start |
| `window_end_utc` | timestamp | yes | Exclusive end; must exceed start |

### Output

| Field | Type | Source | Description |
|---|---|---|---|
| `query_state` | enum | Query projector | `success`, `not-found`, `invalid-request` |
| `normalized_window` | object | Query normalization | `{start_utc,end_utc,basis:"UTC"}` |
| `updated_at_utc` | timestamp/null | Evidence projector | Time this aggregate was computed |
| `configuration_revision` | string/null | Source registry | Expected-source/SLA configuration used |
| `accepted_sources` | string[]/null | Coverage calculation | Sources with trustworthy accepted facts |
| `expected_sources` | string[]/null | Source registry | Null when denominator is unknown |
| `evidence_classes` | [`EvidenceClassSet`](discovery/control-center.md#evidenceclassset) | Evidence projector | Positive subset or singleton unknown |
| `completeness` | [`EvidenceCompleteness`](discovery/control-center.md#evidencecompleteness) | Coverage calculation | Complete, partial or unavailable |
| `freshness` | [`FreshnessState`](discovery/control-center.md#freshnessstate) | Freshness reduction | Independent aggregate qualifier |
| `logical_invocation_count` | integer/null | Accepted attempts | “Times used”; null when no trustworthy value |
| `attempt_count` | integer/null | Accepted attempts | Distinct accepted attempts |
| `retry_count` | integer/null | Accepted retries | Accepted retry attempts |
| `redelivery_count` | integer/null | Delivery diagnostics | Null unless diagnostic source coverage is trustworthy |
| `conflict_count` | integer/null | Delivery diagnostics | Null unless diagnostic source coverage is trustworthy |
| `diagnostic_completeness` | enum | Delivery coverage | `complete`, `partial`, `unavailable` for diagnostic counts |
| `attempt_outcomes` | array/null | Accepted attempts | Attempt ID/number, optional provider-native raw outcome and normalized source outcome; raw value is non-authoritative |
| `logical_invocation_outcome` | enum | Versioned resolution rule | Exactly `succeeded`, `failed`, `cancelled`, `unknown` |
| `outcome_rule_id` | string/null | Source registry | Required for `succeeded|failed|cancelled`; null only for `unknown` |
| `outcome_rule_version` | string/null | Source registry | Required with rule ID; null only for `unknown` |
| `source_facts` | array | Observation adapters | Per source: raw/normalized intervals, interval ratio, gaps, exclusions, overlap diagnostic, ingestion state, last successful ingest, SLA/origin and freshness |
| `exhaustive` | boolean | Coverage calculation | True only for complete coverage |

### Evidence and coverage rules

- Window is `[start_utc,end_utc)` after UTC normalization.
- Delivery key is `(producer,event_id)`; attempt key is
  `(producer,logical_invocation_id,attempt_id)`.
- Duplicate semantic attempts do not increment use, attempts, retries or outcomes.
- `logical_invocation_count=0` requires `observed + complete` and
  `complete_window_coverage=true`.
- `observed + partial` is a lower bound with `exhaustive=false`.
- Unknown/unavailable is singleton evidence with null usage counts.
- Per-source accepted intervals are clipped, sorted, merged, exclusions subtracted and gaps
  calculated before completeness.
- Aggregate freshness reduces expected sources with `unknown > stale > fresh`; an empty/unknown
  expected set is `unknown`.

### Reads From

| Projection | Relationship | Fields Used |
|---|---|---|
| Accepted observation projection | source-contract | Canonical attempts and delivery diagnostics |
| Coverage projection | source-contract | Expected sources, intervals, gaps, exclusions |
| Freshness projection | source-contract | SLA origin, last successful ingest, evaluated time |

**Authority:** [Evidence and Observation Contract](discovery/control-center.md#5-evidence-and-observation-contract).

## Query Invariants

| ID | Invariant | Formal | Authority |
|---|---|---|---|
| Q-I1 | Queries have no side effect. | `write_set(query)=∅` | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |
| Q-I2 | One topology model per request. | `count(request.model)=1` | [SCC-R-002](SPEC.md#formal-rules-and-invariants) |
| Q-I3 | Unknown is not empty/zero/no-path. | `unavailable => !(empty || zero || no-path)` | [SCC-R-004/005/009](SPEC.md#formal-rules-and-invariants) |
| Q-I4 | Cursor is bound to snapshot and normalized query. | `decode(cursor).snapshot=query.snapshot && digest(filters)=cursor.filter_digest` | This aspect's deterministic pagination refinement under SCD-01/03 |
| Q-I5 | Raw prompts, returns, logs and credentials never enter outputs. | `output_fields ∩ forbidden_raw_fields=∅` | [Privacy boundary](discovery/control-center.md#privacy-and-non-authority) |

## Reads-From Typing Convention

The `queries` edge is emitted only for an identity-bearing Entity. `Dispatch` records, skill source
records and local `ChangeProposal` records are consulted as Entities under their owning source
contracts. Adapter projections, health facts, accepted observation sets, coverage unions and
freshness reductions are Value Objects/source contracts, not Entities; rows for them use
`source-contract` and deliberately do not create a DomainSpec `queries` edge. This avoids inventing
canonical external concept IDs before their owners publish them.

| Read source | Meta-type | Owner | Relationship use | Authority |
|---|---|---|---|---|
| Dispatch record | Entity (external) | Dispatch ledger/reader | `queries` | [Dispatch lineage authority](discovery/control-center.md#dispatch-lineage-semantics) |
| Skill source record | Entity (external, source-path identity) | Skill source tree | `queries` | [Skill relation authority](discovery/control-center.md#skill-relation-semantics) |
| [ChangeProposal](discovery/control-center.md#changeproposal) | Entity | Skill Control Center local draft boundary | `queries` | [Phase 1 decision](../../decisions/skill-control-center-phase-1-scope.md#decision) |
| Source health/observation/coverage/freshness projection | Value Object/source contract | Configured adapters; unresolved owners remain unavailable | `source-contract` (not graph edge) | [Evidence contract](discovery/control-center.md#5-evidence-and-observation-contract) |
