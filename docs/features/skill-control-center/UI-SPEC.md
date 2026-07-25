---
id: skill-control-center-ui
feature: skill-control-center
title: "Skill & Dispatch Control Center UI Specification"
summary: Three structurally distinct, functionally equivalent operator workspaces
status: draft
pillar: control-plane
domain: skill-control-center-ui
audience:
  - developers
  - designers
  - operators
priority: p0
lang: en
owners:
  - "@VictorBoscaro"
updatedAt: 2026-07-25
dependencies:
  - SPEC.md
  - architecture.md
  - queries.md
  - interfaces.md
  - operations.md
  - states.md
includes: []
constitution: none
---

# UI Specification: Skill & Dispatch Control Center

This document governs exactly three original frontend structures over one Phase 1 contract.
Existing repository variants are excluded as creative, visual, CSS or layout references.

## Route Table

The owning host must bind the route before publication. The local validation harness uses the
stable route template below; production publication is unavailable until `host_id`,
`auth_contract_id` and `route_owner_id` are all bound.

Runtime configuration separates:

- `ui_route_base = {bound_host}/control-center`
- `api_base_uri = {bound_api_origin}/v1/control-center`

Same-origin is allowed only when the binding explicitly sets the two origins equal. If either base
or any IF-I5 host/auth/owner binding is absent, the harness renders `read-api-unavailable`, the
production host publishes no Control Center route, and no API request is made. This interface
condition is distinct from `authoritative-route-unavailable`: the latter is the intentional Phase
1 absence of apply/receipt authority inside an otherwise available read UI.

| Route template | Page Title | Layout | Auth Required | Permission |
|---|---|---|---|---|
| `{bound_host}/control-center?variant=A` | Control Center — Variant A | `ControlCenterLayout(A)` | Host-defined | Host-defined read access |
| `{bound_host}/control-center?variant=B` | Control Center — Variant B | `ControlCenterLayout(B)` | Host-defined | Host-defined read access |
| `{bound_host}/control-center?variant=C` | Control Center — Variant C | `ControlCenterLayout(C)` | Host-defined | Host-defined read access |

Unknown/missing variant is `invalid-request`; it never creates a fourth shell. The local harness
may bind `{bound_host}` to its own loopback origin and fixture API.

## Shared Variant Contract

Variants A, B and C must be equal over:

| Contract dimension | Frozen value |
|---|---|
| External API | Exactly the six routes in [IF-I6](interfaces.md#interface-invariants) |
| Local operations | `SaveLocalPreference`, `SaveChangeProposal`, `ValidateChangeProposal` |
| Query semantics | [queries.md](queries.md) including typed partial/error states |
| Navigation | [WorkspaceNavigation](states.md#workspacenavigation) |
| Draft lifecycle | [DraftLifecycle](states.md#draftlifecycle) |
| Fixture IDs/digests | [SPEC fixture contract](SPEC.md#fixture-contract) |
| Semantic actions | `select`, `open-detail`, `open-topology`, `back`, `expand`, `submit-path`, `save-preference`, `edit-draft`, `save-draft`, `validate-draft` |
| Critical flows | Exactly `CF-01` through `CF-06`; CF-06 ends at the Phase 1 authoritative boundary |
| Test IDs | Shared table below; variant prefix is forbidden |
| Copy semantics | Same state/evidence/authority terminology; decorative microcopy may differ only if expected answers do not |

Every shared semantic element uses the same `data-testid` in all variants:

| Test ID | Semantic target |
|---|---|
| `cc-scope` | Active scope/window/source summary |
| `cc-attention` | Attention queue region |
| `cc-source-health` | Source degradation/freshness region |
| `cc-search` | Catalog search commit control |
| `cc-filters` | Cumulative filter region |
| `cc-catalog` | Skill/Dispatch catalog |
| `cc-selection` | Selected stable identity |
| `cc-open-detail` | Explicit detail action |
| `cc-open-topology` | Explicit topology action |
| `cc-detail` | Object detail region |
| `cc-topology` | Focal visual topology |
| `cc-topology-table` | Complete semantic graph alternative |
| `cc-path-form` | Bounded path query controls |
| `cc-path-result` | Typed path result |
| `cc-evidence` | Evidence/coverage/freshness detail |
| `cc-draft` | Draft inspector/editor |
| `cc-draft-status` | Draft lifecycle indicator |
| `cc-authoritative-route-unavailable` | Intentional Phase 1 authoritative route boundary explanation |
| `cc-back` | In-product restoration action |
| `cc-status-live` | Polite live status region |

## Structural Variant A — Signal Deck

**Distinct dimensions:** top-down hierarchy, stable catalog navigation, spacious density/rhythm,
dedicated topology workspace.

```text
┌──────────────────────────────────────────────────────────────┐
│ Scope · source health · evidence legend · saved view         │
├──────────────────────────────────────────────────────────────┤
│ ATTENTION DECK: ranked cards + safe next action              │
├───────────────────────────────────────┬──────────────────────┤
│ Search + filters                      │ Detail drawer        │
│ Skill / Dispatch catalog              │ identity/evidence    │
│ stable selection, no auto-navigation  │ draft inspector      │
└───────────────────────────────────────┴──────────────────────┘

Explicit open-topology replaces the lower workspace:
┌──────────────────────────────────────────────────────────────┐
│ Back · model · focus · bounds · evidence                     │
├───────────────────────────────────────┬──────────────────────┤
│ Focal topology                        │ Semantic table       │
│                                       │ Path query/result    │
└───────────────────────────────────────┴──────────────────────┘
```

Visual direction: quiet daylight control surface; broad spacing, strong typographic hierarchy,
layered paper-like panels and restrained motion. It must not imitate any current repository UI.

## Structural Variant B — Ops Rail

**Distinct dimensions:** persistent three-region hierarchy, region-preserving navigation, compact
density/rhythm, topology in the center with persistent attention context.

```text
┌──────────────┬──────────────────────────────┬─────────────────┐
│ ATTENTION    │ Catalog / topology center    │ INSPECTOR       │
│ persistent   │ search · filters · selection │ detail/evidence │
│ source health│                              │ draft/status    │
│ scope        │                              │                 │
└──────────────┴──────────────────────────────┴─────────────────┘
```

Selection updates only stable identity and selection affordances without populating or opening
detail. Only explicit `open-detail` populates the inspector. `open-topology` explicitly replaces
only the center; attention stays visible. Visual direction: compact but humane operations rail,
crisp separators, high information density, clear grouping and near-zero decorative motion.

## Structural Variant C — Guided Ledger

**Distinct dimensions:** sequential full-width hierarchy, anchored stage navigation, editorial
density/rhythm, semantic table before visual topology.

```text
┌──────────────────────────────────────────────────────────────┐
│ Stage anchors: 1 Attention · 2 Catalog · 3 Detail · 4 Graph │
├──────────────────────────────────────────────────────────────┤
│ 1. Attention summary + source health                         │
├──────────────────────────────────────────────────────────────┤
│ 2. Searchable catalog ledger                                 │
├──────────────────────────────────────────────────────────────┤
│ 3. Full-width detail/draft sheet                             │
├──────────────────────────────────────────────────────────────┤
│ 4. Semantic topology table, then optional visual graph       │
└──────────────────────────────────────────────────────────────┘
```

The topology stage is inserted/activated only after `open-topology`. Visual direction: editorial
ledger with strong headings, measured rhythm, table-first legibility and purposeful anchored
scroll restoration.

## Responsive Layout Rules

| Variant | Desktop (`>=1024px`) | Mobile (`<1024px`) |
|---|---|---|
| A | Attention band + catalog/detail split | Single stack; detail/topology explicit full-screen views |
| B | Three persistent regions | Attention becomes collapsible summary; catalog/inspector/topology remain explicit views |
| C | Full-width stages with sticky stage index | Same reading order; stage index becomes horizontal scrollable landmark list |

At 320 CSS px no two-dimensional page scroll is required except inside the optional visual graph;
the semantic topology table remains reflowable/scrollable with labeled columns.

## Component Inventory

| Component | Type | Planned location | Typed props / consumed hooks | Purpose |
|---|---|---|---|---|
| `ControlCenterWorkspace` | Page | `pages/control-center.tsx` | `{variant:"A"|"B"|"C"}` / workspace-state hook | Owns route, shared state and restoration stack |
| `ControlCenterLayout` | Layout | `layouts/ControlCenterLayout.tsx` | `{variant,children}` / none | Applies A/B/C structural composition without semantic drift |
| `AttentionQueuePanel` | Component | `components/control-center/AttentionQueuePanel.tsx` | `{items:AttentionQueue}` / `useAttention` | Shows ranked attention, scope, proof and safe next action |
| `CatalogWorkspace` | Component | `components/control-center/CatalogWorkspace.tsx` | `{rows,selection,filters}` / `useCatalog` | Search, filters, result set and stable selection |
| `DetailInspector` | Component | `components/control-center/DetailInspector.tsx` | `{detail,onBack,onOpenTopology}` / `useObjectDetail` | Identity, provenance, available models and safe actions |
| `EvidenceInspector` | Component | `components/control-center/EvidenceInspector.tsx` | `{objectId,window}` / `useEvidence` | Evidence classes, coverage intervals, freshness and usage diagnostics |
| `TopologyWorkspace` | Component | `components/control-center/TopologyWorkspace.tsx` | `{model,focus,limits}` / `useTopology,usePathQuery` | Focal topology, semantic mirror and bounded path query |
| `DraftInspector` | Component | `components/control-center/DraftInspector.tsx` | `{proposal,validators}` / local draft hooks | Target/base/diff/origins plus editor and validation preview |
| `CatalogSearchForm` | Form | `components/control-center/CatalogSearchForm.tsx` | `{scope,initialQuery,allowedFilters}` / `useCatalog` | Commits bounded catalog query and filters |
| `PathQueryForm` | Form | `components/control-center/PathQueryForm.tsx` | `{model,endpoints,limits}` / `usePathQuery` | Commits one bounded path query |
| `DraftEditorForm` | Form | `components/control-center/DraftEditorForm.tsx` | `{proposal,validatorOptions}` / draft save/validate hooks | Edits local proposal and commits save/validate actions |
| `PreferenceForm` | Form | `components/control-center/PreferenceForm.tsx` | `{scope,kind,value,revision}` / local preference hook | Saves presentation-only workspace preferences |
| `DraftStatusIndicator` | State Indicator | `components/control-center/DraftStatusIndicator.tsx` | `{state,authoritative:false}` / none | Text/icon/color encoding of local lifecycle |

## View Models and Adapters

| View model | Typed target shape | Source | Adapter rule |
|---|---|---|---|
| `AttentionQueue` | `{items: Array<{object_kind,object_id,reason,priority,state,scope,evidence,safe_next_action}>, result_state, source_facts, snapshot_id}` | `GetAttentionQueue` response envelope | Preserve backend order and stable IDs; format labels only; never infer priority/evidence |
| `DispatchLineage` | `{focus_id,nodes:Array<{dispatch_id,parent_dispatch_id?,status}>,edges:Array<{parent_id,child_id,evidence_id}>,unresolved_parent_ids,completeness,snapshot_id}` | `GetTopology(model=dispatch-lineage)` | Preserve parent direction and unresolved parents; never infer missing ancestry |
| `IntraDispatchTopology` | `{dispatch_id,focus_group_id,nodes:Array<{group_id,label}>,edges:Array<{from_group_id,to_group_id,kind,evidence_id}>,limits,truncated,snapshot_id}` | `GetTopology(model=intra-dispatch)` | Keep composite dispatch/group identity; never merge groups across Dispatches |
| `CatalogResultSet` | `{matches,active_filters,matched_fields,next_cursor,query_state,snapshot_id}` | `SearchCatalog` | Normalize display labels only; preserve matched fields, state and cursor |
| `EvidenceSummary` | `{classes,freshness,window,coverage,count?,outcomes,source_facts}` | `GetUsageEvidence` | Format UTC/window values; count remains absent unless observed and covered |

Adapters are pure and presentation-only. They cannot recompute evidence class, freshness, coverage,
path order, source health, no-path, invalid-endpoint, lineage, or authority.

## Data Flow

| API Call | Hook / Binding | Cache Key | Triggers |
|---|---|---|---|
| `GET {api_base_uri}/attention` | `useAttention` / `AttentionReadBinding` | `cc.attention(scope,window,filters,snapshot)` | Route load, scope/window/filter commit |
| `GET {api_base_uri}/catalog` | `useCatalog` / `CatalogReadBinding` | `cc.catalog(scope,query,filters,cursor,snapshot)` | Route load, search/filter/page commit |
| `GET {api_base_uri}/objects/:kind/:id` | `useObjectDetail` / `ObjectDetailBinding` | `cc.object(scope,kind,id,window,snapshot)` | Explicit `open-detail` |
| `GET {api_base_uri}/topology/:model` | `useTopology` / `TopologyReadBinding` | `cc.topology(scope,model,dispatch?,focus,depth,kinds,snapshot)` | Explicit `open-topology`, expand |
| `POST {api_base_uri}/path-query` | `usePathQuery` / `PathReadBinding` | `cc.path(digest(normalizedRequest),snapshot)` | Explicit path submit |
| `GET {api_base_uri}/evidence/:kind/:id` | `useEvidence` / `EvidenceReadBinding` | `cc.evidence(scope,claim,kind,id,window,configRevision)` | Detail evidence open/window commit |

Cache keys contain no raw prompt, return, credential, log or artifact body. Partial/unavailable
responses remain cached only with their exact source facts and snapshot identity.

### Local operations

| Action | Port/Operation | On success | On failure |
|---|---|---|---|
| Save workspace preference | `LocalPreferencePort.save` | Reflect new local revision | Show closed code and safe action |
| Save draft | `DraftPort.save` / `SaveChangeProposal` | Enter `draft-saved`; retain target/base/diff | Follow exact operation matrix |
| Validate draft | `DraftPort.validate` / `ValidateChangeProposal` | Enter `valid` or `invalid` preview state | Return to state required by operation matrix |

No UI hook, binding or action named apply, retry-apply, reconcile or accepted-receipt exists.

## Form Contracts

### PreferenceForm

Contracts [`LocalPreferencePort.save`](interfaces.md#internal-localpreferenceport). It can alter
presentation only; it cannot change authority, evidence, ranking, topology, validation, or source
data.

```typescript
const PreferenceSchema = z.object({
  scope: z.literal("skill-control-center"),
  expected_revision: z.number().int().nonnegative(),
  kind: z.enum(["variant", "density", "theme", "last-safe-route"]),
  value: z.unknown(),
  schema_version: z.string().min(1),
});
```

| Closed code | Message | Retain input | Focus | Safe next action |
|---|---|---:|---|---|
| `saved-local` | Preference saved at the returned local revision. | no | Invoking control | Continue |
| `invalid-local-scope` | This preference belongs to another local scope. | no | Scope summary | Restore the current scope |
| `local-conflict` | The local preference changed after this form opened. | yes | Revision notice | Refresh revision and review retained value |
| `invalid-local-preference` | The preference kind, value, or schema is invalid. | no | First invalid field | Correct kind, value, or schema |
| `forbidden-local-target` | Only a local presentation target is allowed. | no | Target notice | Choose a local target |
| `save-failed` | The local store did not commit the preference. | yes | Error summary | Retry the exact retained input |
| `protocol-error` | The local store returned an undeclared result. | no | Error summary | Stop and report the contract mismatch |

### CatalogSearchForm

Contracts the read-only [`GET /v1/control-center/catalog`](interfaces.md#get-v1control-centercatalog)
request through `CatalogReadBinding`.

```typescript
const makeCatalogSearchSchema = (supported: {
  status: ReadonlySet<string>;
  evidenceClass: ReadonlySet<string>;
}) => z.object({
  query: z.string().trim().default(""),
  object_kinds: z.array(z.enum(["skill", "dispatch"])).min(1),
  limit: z.number().int().min(1).max(200).default(50),
  cursor: z.string().min(1).optional(),
  filters: z.object({
    status: z.array(z.string().refine(v => supported.status.has(v), "Unsupported status.")).default([]),
    evidence_class: z.array(z.string().refine(
      v => supported.evidenceClass.has(v), "Unsupported evidence class."
    )).default([]),
    freshness: z.array(z.enum(["fresh", "stale", "unknown"])).default([]),
    has_attention: z.boolean().nullable().default(null),
  }).default({}),
});
```

| Field | Type | HTML input | Validation | Error message |
|---|---|---|---|---|
| `query` | string | `<input type="search">` | Trimmed Unicode string | “Enter a valid search.” |
| `object_kinds` | enum array | checkbox group | Non-empty subset of skill/dispatch | “Choose skills or Dispatches.” |
| `limit` | integer | `<select>` | 1..200 | “Choose 1 to 200 results.” |
| `cursor` | opaque string | hidden | Non-empty when present | “Restart from the first page.” |
| `filters.status` | string array | multi-select | Supported values for active kind | “One or more statuses are unsupported.” |
| `filters.evidence_class` | string array | multi-select | Supported evidence classes | “One or more evidence classes are unsupported.” |
| `filters.freshness` | enum array | multi-select | fresh/stale/unknown | “Choose a supported freshness value.” |
| `filters.has_attention` | boolean/null | select | true/false/all | “Choose an attention filter.” |

| Result/code | HTTP status | UI message/action |
|---|---:|---|
| `invalid-request` | 400 parse / 422 semantics | Review search scope and filters; retain entered values. |
| `invalid-cursor` | 409 | Restart from the first page; clear cursor only. |
| `stale-snapshot` | 409 | Refresh the result set against the disclosed snapshot. |
| `no-match` | 200 | Show active query/filter/scope and reversible clear controls. |
| transport/protocol error | 4xx/5xx or no response | Preserve context and disclose the failed boundary; do not invent a query state. |

### PathQueryForm

Contracts read-only [`POST /v1/control-center/path-query`](interfaces.md#post-v1control-centerpath-query)
through `PathReadBinding`; POST does not imply mutation.

```typescript
const makePathQuerySchema = (
  supportedEdgeKinds: Readonly<Record<"skill-relations"|"dispatch-lineage"|"intra-dispatch", ReadonlySet<string>>>
) => z.object({
  model: z.enum(["skill-relations", "dispatch-lineage", "intra-dispatch"]),
  source_id: z.string().min(1),
  target_id: z.string().min(1),
  dispatch_id: z.string().min(1).optional(),
  direction: z.enum(["outbound", "inbound", "undirected-view"]),
  allowed_edge_kinds: z.array(z.string().min(1)).min(1),
  max_depth: z.number().int().min(0).max(10),
  max_paths: z.number().int().min(1).max(100),
}).superRefine((value, ctx) => {
  if (value.model === "intra-dispatch" && !value.dispatch_id) {
    ctx.addIssue({code: "custom", path: ["dispatch_id"], message: "Dispatch is required."});
  }
  for (const kind of value.allowed_edge_kinds) {
    if (!supportedEdgeKinds[value.model].has(kind)) {
      ctx.addIssue({code: "custom", path: ["allowed_edge_kinds"], message: "Unsupported edge type."});
    }
  }
});
```

| Field | Type | HTML input | Validation | Error message |
|---|---|---|---|---|
| `model` | enum | `<select>` | Exactly one supported model | “Choose one topology model.” |
| `source_id` | string | combobox | Non-empty stable ID | “Choose a source.” |
| `target_id` | string | combobox | Non-empty stable ID | “Choose a target.” |
| `dispatch_id` | string | combobox | Required for intra-dispatch | “Choose the owning Dispatch.” |
| `direction` | enum | `<select>` | outbound/inbound/undirected-view | “Choose a supported direction.” |
| `allowed_edge_kinds` | string array | checkbox group | Non-empty supported subset | “Choose at least one edge type.” |
| `max_depth` | integer | `<input type="number">` | 0..10 | “Choose depth from 0 to 10.” |
| `max_paths` | integer | `<input type="number">` | 1..100 | “Choose 1 to 100 paths.” |

| Result/code | HTTP status | UI message/action |
|---|---:|---|
| `invalid-request` | 400 parse / 422 semantics | Review model, direction, edge types and bounds. |
| `invalid-endpoint` | 200 | Name the invalid endpoint; keep selection/query unchanged. |
| `unsupported-model` | 200 | Explain that this topology model is unavailable. |
| `no-path` | 200 | State the exact bounded request; never claim global disconnection. |
| `truncated` | 200 | Show applied limits, returned paths and `more_paths_exist`. |
| transport/protocol error | 4xx/5xx or no response | Preserve request/context and disclose boundary failure; do not invent a path state. |

### DraftEditorForm

| Field | Type | Input | Validation | Error |
|---|---|---|---|---|
| Target kind/ID | read-only string | Text | Stable, non-empty | “Target identity is unavailable.” |
| Base revision/hash | read-only string | Text | Stable, non-empty | “Base revision is unavailable.” |
| Proposed patch | structured JSON array | Code/text editor with semantic label | Non-empty, known schema, well formed | Closed code from `SaveChangeProposal` |
| Effective values/origins | read-only table | Table | Every value has origin | “Every effective value needs an origin.” |
| Validator | select | Native/select-like | Known ID and version | `invalid-validator` |

The form submits only to local ports. Its authority section always displays:
“Authoritative apply is unavailable in Phase 1” plus links to SCC-BL-001..003.

```typescript
const DraftEditorSchema = z.object({
  proposal_id: z.string().min(1),
  expected_draft_revision: z.number().int().nonnegative(),
  target_kind: z.string().min(1),
  target_id: z.string().min(1),
  base_revision_or_hash: z.string().min(1),
  proposed_patch: z.array(z.object({
    op: z.enum(["add", "remove", "replace", "test"]),
    path: z.string().startsWith("/"),
    value: z.unknown().optional(),
  })).min(1),
  effective_values: z.record(z.object({value: z.unknown(), origin: z.string().min(1)})),
  schema_version: z.string().min(1),
  validator_id: z.string().min(1),
  validator_version: z.string().min(1),
});
```

`Save draft` submits to `DraftPort.save`; `Validate draft` is enabled only for the exact saved
revision and submits `{proposal_id,draft_revision,validator_id,validator_version}` to
`DraftPort.validate`.

| Closed operation code(s) | UI message | Retain input | Focus | Safe next action |
|---|---|---:|---|---|
| `draft-saved` | Draft saved at the returned local revision. | no | Draft status | Inspect or validate |
| `invalid-draft` | Required draft content or effective-value origins are invalid. | no | First invalid field | Correct required content/origins |
| `forbidden-draft-state` | This draft is outside the Phase 1 lifecycle. | no | Lifecycle notice | Return to the Phase 1 lifecycle |
| `draft-conflict` | The saved revision changed after this form opened. | yes | Revision notice | Refresh base/revision and review retained input |
| `invalid-draft-schema` | The draft schema is unsupported. | no | Schema field | Choose a supported schema |
| `invalid-draft-patch` | The proposed patch is malformed. | no | First invalid patch row | Correct the patch |
| `unsupported-target-kind` | This target kind cannot have a local proposal. | no | Target summary | Choose a supported target |
| `draft-state-ineligible` | Saving is unavailable while this draft state is active. | no | Lifecycle notice | Wait or return to an editable state |
| `save-failed` | The local store did not commit the draft. | yes | Error summary | Retry the exact retained input |
| `validation-valid` | Validation completed with a non-authoritative valid preview. | no | Preview heading | Review preview |
| `validation-invalid` | Validation completed with non-authoritative findings. | no | Findings heading | Edit proposal |
| `draft-not-found` | The exact saved proposal no longer exists. | no | Draft list link | Return to the catalog or draft list |
| `validation-ineligible` | Only the exact saved revision can be validated. | no | Save draft action | Save proposal first |
| `invalid-validator` | The validator ID or version is unknown. | no | Validator field | Select a known validator/version |
| `forbidden-validation-effect` | This validator would exceed preview-only authority. | no | Authority notice | Stop and use a preview-only validator |
| `validation-unavailable` | The validator is temporarily unavailable. | yes | Error summary | Retry the same validation |
| `validation-error` | The validator failed without producing a preview. | yes | Error summary | Retry after reviewing diagnostics |
| `validation-save-failed` | The complete preview could not be stored atomically. | yes | Error summary | Retry the exact validation request |
| `protocol-error` | A local port returned an undeclared result. | no | Error summary | Stop and report the contract mismatch |

## Shared Interaction Rules

1. First paint exposes scope, attention, health and evidence legend before topology.
2. `select` never changes view or steals focus.
3. Detail/topology/back follow [WorkspaceNavigation](states.md#workspacenavigation).
4. Every topology answer is available in `cc-topology-table`; graph/table selections are bidirectional.
5. Weak `named_reference` edges use “mentions”, a dashed/non-color marker and an opt-in inclusive mode.
6. Usage counts always show window, completeness, freshness and source coverage; unknown is never zero.
7. A local draft can say dirty/saved/valid/invalid/failed, never approved/applied/accepted.
8. Benchmark instrumentation is descriptive and cannot modify route, layout, promotion or winner state.

## Phase 1 Critical Flows

Each case selector is a committed row inside the named frozen fixture; it is not a new independent
fixture. The executable test ID is identical across A/B/C.

| ID | Fixture / case | Actions | API/port | Required states | Expected answer / end | Test ID |
|---|---|---|---|---|---|---|
| CF-01 TriageAttention | `FX-DISPATCH-CATALOG-v1 / cf01-attention` | inspect, optional `open-detail/back` | GET attention, optional GET object | loading, empty, stale-degraded, partial-error | Stable identity/reason/state/scope/safe action; no lost workspace | `cc-cf-01` |
| CF-02 LocateObject | `FX-DISPATCH-CATALOG-v1 / cf02-known-object` | search/filter commit, `select` | GET catalog | loading, no-match | Stable ID/kind/scope; selection with unchanged view | `cc-cf-02` |
| CF-03 InspectEvidence | `FX-EVIDENCE-MIXED-v1 / cf03-mixed` | `open-detail`, inspect evidence | GET object, GET evidence | observed-overlay, stale-degraded, partial-error | Exact class/freshness/source/window/limitation; no unknown-as-zero | `cc-cf-03` |
| CF-04 FindPath | `FX-SKILL-TOPOLOGY-v1 / cf04-bounded-path` | `open-topology`, submit path, select graph/table | GET topology, POST path-query | focal-lineage, invalid-endpoint, truncated-path, partial-error | Ordered typed answer; visual/semantic identity sets agree | `cc-cf-04` |
| CF-05 DiagnoseCoverage | `FX-EVIDENCE-MIXED-v1 / cf05-partial-window` | inspect source facts | GET evidence | observed-overlay, stale-degraded, partial-error | Exact gap/exclusion/ingest/SLA; no false zero/healthy claim | `cc-cf-05` |
| CF-06 ReviewChange | `FX-DRAFT-v1 / cf06-authoritative-boundary` | edit/save/validate/inspect boundary | DraftPort; no authoritative route | draft-dirty, draft-saved, validating, valid, invalid, save-failed, local-conflict; `authoritative-route-unavailable` boundary | Exact diff/validity; draft retained; no apply/receipt conclusion; SCC-BL-001/002/003 linked | `cc-cf-06` |

CF-06 deliberately stops at `authoritative-route-unavailable`. No receipt flow exists in Phase 1.
Every approval/apply/reconcile/accepted-receipt transition is
[blocked](BACKLOG.md#p0--authoritative-apply-safety).

## Mandatory UI States

This table is the single source of fixture identity, producer, representation/focus, flow,
executable test identity and digest reference across A/B/C.

| State | Fixture / case | Producer | Required representation / focus | Flows | Test ID | Digest ref |
|---|---|---|---|---|---|---|
| `loading` | `FX-DISPATCH-CATALOG-v1 / state-loading` | Pending read request | Busy status; stable scope/identity/focus; polite completion | CF-01,02 | `cc-state-loading` | `#state-loading.sha256` |
| `empty` | `FX-DISPATCH-CATALOG-v1 / state-empty` | Complete successful empty result | Scope-specific empty copy; not unavailable/unused | CF-01,02 | `cc-state-empty` | `#state-empty.sha256` |
| `no-match` | `FX-DISPATCH-CATALOG-v1 / state-no-match` | Complete search no-match | Active query/filters/scope; focus on reversible reset | CF-02 | `cc-state-no-match` | `#state-no-match.sha256` |
| `focal-lineage` | `FX-SKILL-TOPOLOGY-v1 / state-focal-lineage` | Explicit topology success | Model/focus plus graph/table identity parity | CF-04 | `cc-state-focal-lineage` | `#state-focal-lineage.sha256` |
| `observed-overlay` | `FX-EVIDENCE-MIXED-v1 / state-observed` | Observed evidence answer | Counts/window/proof/coverage/freshness/source | CF-03,05 | `cc-state-observed` | `#state-observed.sha256` |
| `stale-degraded` | `FX-EVIDENCE-MIXED-v1 / state-stale` | Stale/degraded source | Source/SLA/origin/last ingest/impact; no focus theft | CF-01,03,05 | `cc-state-stale` | `#state-stale.sha256` |
| `partial-error` | `FX-EVIDENCE-MIXED-v1 / state-partial` | Partial result + failed partition | Lower-bound copy, retained facts, failed source | CF-01,03,04,05 | `cc-state-partial` | `#state-partial.sha256` |
| `invalid-endpoint` | `FX-SKILL-TOPOLOGY-v1 / state-invalid-endpoint` | Complete identity coverage | Named endpoint/model; unchanged query/selection | CF-04 | `cc-state-invalid-endpoint` | `#state-invalid-endpoint.sha256` |
| `truncated-path` | `FX-SKILL-TOPOLOGY-v1 / state-truncated` | Bounded truncation | Limits, returned evidence IDs, more-paths state | CF-04 | `cc-state-truncated` | `#state-truncated.sha256` |
| `draft-dirty` | `FX-DRAFT-v1 / state-draft-dirty` | Local edit | Unsaved marker, target/base/diff; focus remains edited field | CF-06 | `cc-state-draft-dirty` | `#state-draft-dirty.sha256` |
| `draft-saved` | `FX-DRAFT-v1 / state-draft-saved` | `draft-saved` | Local revision/diff and validate action | CF-06 | `cc-state-draft-saved` | `#state-draft-saved.sha256` |
| `validating` | `FX-DRAFT-v1 / state-validating` | `validation-started` | Attempt status; save/edit protected; live announcement | CF-06 | `cc-state-validating` | `#state-validating.sha256` |
| `valid` | `FX-DRAFT-v1 / state-valid` | `validation-valid` | “Valid preview — non-authoritative”, validator/version | CF-06 | `cc-state-valid` | `#state-valid.sha256` |
| `invalid` | `FX-DRAFT-v1 / state-invalid` | `validation-invalid` | Findings linked to fields; non-authoritative label | CF-06 | `cc-state-invalid` | `#state-invalid.sha256` |
| `save-failed` | `FX-DRAFT-v1 / state-save-failed` | Retryable persistence error | Retained input, unchanged revision, focus on retry/error | CF-06 | `cc-state-save-failed` | `#state-save-failed.sha256` |
| `local-conflict` | `FX-DRAFT-v1 / state-local-conflict` | Local CAS mismatch | Stored/caller revision, retained input, refresh/review action | CF-06 | `cc-state-local-conflict` | `#state-local-conflict.sha256` |
| `read-api-unavailable` | `FX-INTERFACE-BOUNDARY-v1 / state-read-api-unavailable` | Missing IF-I5 read binding | No published/read call; missing binding and recovery; focus on explanation | CF-01,02,03,04,05 | `cc-state-read-api-unavailable` | `#state-read-api-unavailable.sha256` |

Authoritative `approval-pending`, `indeterminate-reconciling`, `failed-after-reconcile`, and
`accepted-receipt` states are not Phase 1 UI states.

### State fixture contract

This projection must reuse the Mandatory UI States row values exactly; it cannot define or rename a
fixture, producer, representation/focus, test ID, or digest. All entries resolve through
`fixtures/manifest.json`. Each referenced digest is a non-null lowercase SHA-256 of RFC 8785/JCS-
normalized fixture JSON; a missing or mismatched digest fails before render.

| State ID | Fixture / case | Producer | Required representation / focus | Test ID | Digest ref |
|---|---|---|---|---|---|
| loading | `FX-DISPATCH-CATALOG-v1 / state-loading` | Pending read request | Busy status; stable scope/identity/focus; polite completion | `cc-state-loading` | `#state-loading.sha256` |
| empty | `FX-DISPATCH-CATALOG-v1 / state-empty` | Complete successful empty result | Scope-specific empty copy; not unavailable/unused | `cc-state-empty` | `#state-empty.sha256` |
| no-match | `FX-DISPATCH-CATALOG-v1 / state-no-match` | Complete search no-match | Active query/filters/scope; focus on reversible reset | `cc-state-no-match` | `#state-no-match.sha256` |
| focal-lineage | `FX-SKILL-TOPOLOGY-v1 / state-focal-lineage` | Explicit topology success | Model/focus plus graph/table identity parity | `cc-state-focal-lineage` | `#state-focal-lineage.sha256` |
| observed-overlay | `FX-EVIDENCE-MIXED-v1 / state-observed` | Observed evidence answer | Counts/window/proof/coverage/freshness/source | `cc-state-observed` | `#state-observed.sha256` |
| stale-degraded | `FX-EVIDENCE-MIXED-v1 / state-stale` | Stale/degraded source | Source/SLA/origin/last ingest/impact; no focus theft | `cc-state-stale` | `#state-stale.sha256` |
| partial-error | `FX-EVIDENCE-MIXED-v1 / state-partial` | Partial result + failed partition | Lower-bound copy, retained facts, failed source | `cc-state-partial` | `#state-partial.sha256` |
| invalid-endpoint | `FX-SKILL-TOPOLOGY-v1 / state-invalid-endpoint` | Complete identity coverage | Named endpoint/model; unchanged query/selection | `cc-state-invalid-endpoint` | `#state-invalid-endpoint.sha256` |
| truncated-path | `FX-SKILL-TOPOLOGY-v1 / state-truncated` | Bounded truncation | Limits, returned evidence IDs, more-paths state | `cc-state-truncated` | `#state-truncated.sha256` |
| draft-dirty | `FX-DRAFT-v1 / state-draft-dirty` | Local edit | Unsaved marker, target/base/diff; focus remains edited field | `cc-state-draft-dirty` | `#state-draft-dirty.sha256` |
| draft-saved | `FX-DRAFT-v1 / state-draft-saved` | `draft-saved` | Local revision/diff and validate action | `cc-state-draft-saved` | `#state-draft-saved.sha256` |
| validating | `FX-DRAFT-v1 / state-validating` | `validation-started` | Attempt status; save/edit protected; live announcement | `cc-state-validating` | `#state-validating.sha256` |
| valid | `FX-DRAFT-v1 / state-valid` | `validation-valid` | “Valid preview — non-authoritative”, validator/version | `cc-state-valid` | `#state-valid.sha256` |
| invalid | `FX-DRAFT-v1 / state-invalid` | `validation-invalid` | Findings linked to fields; non-authoritative label | `cc-state-invalid` | `#state-invalid.sha256` |
| save-failed | `FX-DRAFT-v1 / state-save-failed` | Retryable persistence error | Retained input, unchanged revision, focus on retry/error | `cc-state-save-failed` | `#state-save-failed.sha256` |
| local-conflict | `FX-DRAFT-v1 / state-local-conflict` | Local CAS mismatch | Stored/caller revision, retained input, refresh/review action | `cc-state-local-conflict` | `#state-local-conflict.sha256` |
| read-api-unavailable | `FX-INTERFACE-BOUNDARY-v1 / state-read-api-unavailable` | Missing IF-I5 read binding | No published/read call; missing binding and recovery; focus on explanation | `cc-state-read-api-unavailable` | `#state-read-api-unavailable.sha256` |

## State-to-UI Mapping

| State/value | Required representation |
|---|---|
| complete/fresh | Text “Complete”/“Fresh”, icon and neutral/positive treatment |
| partial | Text “Partial — lower bound”, named missing source/interval, non-color icon |
| unavailable | Text “Unavailable”, reason/scope, no zero/empty copy |
| stale | Text “Stale”, last ingest, SLA and origin |
| `explicit_path` | “Explicit path reference”, solid line + text |
| `named_reference` | “Mention”, dashed line + text |
| valid/invalid draft | “Valid preview” / “Invalid preview”; always “Non-authoritative” |
| `read-api-unavailable` | No published/read call; missing binding named; recovery requires all IF-I5 bindings |
| `authoritative-route-unavailable` | No apply/receipt control or conclusion; Phase 1 backlog links remain visible |

## Accessibility Requirements

Applicable WCAG 2.2 Level A/AA criteria for these flows include:

`1.1.1`, `1.3.1`, `1.3.2`, `1.3.4`, `1.4.1`, `1.4.3`, `1.4.10`, `1.4.11`,
`1.4.12`, `1.4.13`, `2.1.1`, `2.1.2`, `2.1.4`, `2.4.1`, `2.4.2`, `2.4.3`,
`2.4.6`, `2.4.7`, `2.4.11`, `2.5.3`, `2.5.7`, `2.5.8`, `3.1.1`, `3.2.1`,
`3.2.2`, `3.2.3`, `3.3.1`, `3.3.2`, `3.3.3`, `3.3.7`, `4.1.2`, `4.1.3`.

| Surface | Requirement |
|---|---|
| Workspace regions | Named landmarks and one H1; skip link reaches main workspace |
| Catalog | Semantic table/list; headers, result count and selection state announced |
| Detail/drawer | Focus moves only after explicit open; close/back restores invoking control |
| Topology | Full keyboard operation plus complete semantic table alternative; canvas never sole source |
| Evidence/status | Text/icon meaning; polite live updates; color never sole carrier |
| Draft form | Programmatic labels, error identification/suggestion, retained values |
| Responsive | 200% zoom and 320 CSS-px reflow; no hidden required action |
| Motion | Respects `prefers-reduced-motion`; no essential animation |

Manual evidence crosses every applicable critical-flow/state cell with keyboard/focus,
screen-reader name/role/value/status announcements, 200% zoom/320px reflow, reduced motion,
light/dark theme and non-color meaning.

Each manual record has the exact shape
`{variant,flow_id,state_id,fixture_digest,criteria[],keyboard,focus,screen_reader,live_region,reflow_200,width_320,reduced_motion,non_color,non_canvas,tester,timestamp,status,evidence_digest}`.
Every field is required; result fields are `pass|fail|not-applicable`, with a reason required for
`not-applicable`. Missing records fail the variant.

| Flow | Applicable surfaces/states | Required checks | Evidence IDs |
|---|---|---|---|
| `CF-01` | Attention/catalog; loading, empty, partial-error, stale-degraded, read-api-unavailable | landmarks, H1, skip link, result count, non-color source state, focus continuity, 200%/320px | `a11y-cf01-{A|B|C}-{state}` |
| `CF-02` | LocateObject catalog/search; loading/empty/no-match/read-api-unavailable | search/filter keyboard completion, result count/selection announcement, stable focus and reversible recovery | `a11y-cf02-{A|B|C}-{state}` |
| `CF-03` | InspectEvidence detail/evidence; observed/stale/partial/read-api-unavailable | explicit-open focus, close/back restoration, names/roles/values, polite status, non-color provenance | `a11y-cf03-{A|B|C}-{state}` |
| `CF-04` | Topology semantic mirror; focal-lineage, partial-error, truncated-path, invalid-endpoint, read-api-unavailable | canvas-equivalent table, same nodes/edges/limits, keyboard parity, screen-reader reading order | `a11y-cf04-{A|B|C}-{state}` |
| `CF-05` | DiagnoseCoverage evidence/source facts; observed/stale/partial/read-api-unavailable | gaps/exclusions/SLA announced, non-color health meaning, no unknown-as-zero, stable inspection focus | `a11y-cf05-{A|B|C}-{state}` |
| `CF-06` | ReviewChange draft editor; dirty/saved/validating/valid/invalid/save-failed/conflict plus authoritative boundary | labels, field/error association, retained-value behavior, focus recovery, explicit non-authoritative and unavailable-route announcements | `a11y-cf06-{A|B|C}-{state}` |

For each listed cell, the evidence runner records keyboard-only completion, expected initial and
restored focus selectors, screen-reader announcement transcript, live-region behavior, 200% zoom,
320 CSS-px reflow, reduced-motion behavior, non-color equivalence, and `CF-04` non-canvas parity.
The same fixture digest used by the screenshot row is mandatory.

## Screenshot and Design Review Contract

Reference aliases are fixed for Phase 1:

- `desktop`: 1440 × 1024 CSS px
- `mobile`: 390 × 844 CSS px
- themes: `light`, `dark`

The manifest is exactly `3 variants × 2 viewports × 2 themes × 17 states = 204` rows. Every row
binds variant, viewport, theme, state, fixture/test ID, source/backend/frontend digests and
screenshot digest/path. Screenshots are static evidence only.

Blind randomized review scores each screenshot set from 1–5 on:

- clarity;
- usability;
- visual consistency;
- operational efficiency;
- structural distinctness.

No score selects/promotes a variant in Phase 1. A score below 3 on any of the first four criteria
creates a design defect to fix; structural distinctness requires every pair to differ in at least
three of layout hierarchy, navigation model, density/rhythm and topology treatment.

## UI Concept Registry

| Concept | ID | Type |
|---|---|---|
| ControlCenterWorkspace | `ui.skill-control-center.ControlCenterWorkspace` | Page |
| ControlCenterLayout | `ui.skill-control-center.ControlCenterLayout` | Layout |
| AttentionQueuePanel | `ui.skill-control-center.AttentionQueuePanel` | Component |
| CatalogWorkspace | `ui.skill-control-center.CatalogWorkspace` | Component |
| DetailInspector | `ui.skill-control-center.DetailInspector` | Component |
| EvidenceInspector | `ui.skill-control-center.EvidenceInspector` | Component |
| TopologyWorkspace | `ui.skill-control-center.TopologyWorkspace` | Component |
| DraftInspector | `ui.skill-control-center.DraftInspector` | Component |
| CatalogSearchForm | `ui.skill-control-center.CatalogSearchForm` | Form |
| PathQueryForm | `ui.skill-control-center.PathQueryForm` | Form |
| DraftEditorForm | `ui.skill-control-center.DraftEditorForm` | Form |
| PreferenceForm | `ui.skill-control-center.PreferenceForm` | Form |
| DraftStatusIndicator | `ui.skill-control-center.DraftStatusIndicator` | State Indicator |
| AttentionQueue | `ui.skill-control-center.AttentionQueue` | View Model |
| DispatchLineage | `ui.skill-control-center.DispatchLineage` | View Model |
| IntraDispatchTopology | `ui.skill-control-center.IntraDispatchTopology` | View Model |
| CatalogResultSet | `ui.skill-control-center.CatalogResultSet` | View Model |
| EvidenceSummary | `ui.skill-control-center.EvidenceSummary` | View Model |
| AttentionAdapter | `ui.skill-control-center.AttentionAdapter` | Adapter |
| DispatchLineageAdapter | `ui.skill-control-center.DispatchLineageAdapter` | Adapter |
| IntraDispatchAdapter | `ui.skill-control-center.IntraDispatchAdapter` | Adapter |
| CatalogAdapter | `ui.skill-control-center.CatalogAdapter` | Adapter |
| EvidenceAdapter | `ui.skill-control-center.EvidenceAdapter` | Adapter |
| useAttention | `ui.skill-control-center.useAttention` | Hook |
| useCatalog | `ui.skill-control-center.useCatalog` | Hook |
| useObjectDetail | `ui.skill-control-center.useObjectDetail` | Hook |
| usePathQuery | `ui.skill-control-center.usePathQuery` | Hook |
| useEvidence | `ui.skill-control-center.useEvidence` | Hook |
| CatalogReadBinding | `ui.skill-control-center.CatalogReadBinding` | Binding |
| AttentionReadBinding | `ui.skill-control-center.AttentionReadBinding` | Binding |
| ObjectDetailBinding | `ui.skill-control-center.ObjectDetailBinding` | Binding |
| useTopology | `ui.skill-control-center.useTopology` | Hook |
| TopologyReadBinding | `ui.skill-control-center.TopologyReadBinding` | Binding |
| PathReadBinding | `ui.skill-control-center.PathReadBinding` | Binding |
| EvidenceReadBinding | `ui.skill-control-center.EvidenceReadBinding` | Binding |
| DraftWriteBinding | `ui.skill-control-center.DraftWriteBinding` | Binding |
| DraftValidationBinding | `ui.skill-control-center.DraftValidationBinding` | Binding |
| PreferenceWriteBinding | `ui.skill-control-center.PreferenceWriteBinding` | Binding |
| SearchCatalogAction | `ui.skill-control-center.SearchCatalogAction` | Action |
| SubmitPathAction | `ui.skill-control-center.SubmitPathAction` | Action |
| SavePreferenceAction | `ui.skill-control-center.SavePreferenceAction` | Action |
| SaveDraftAction | `ui.skill-control-center.SaveDraftAction` | Action |
| ValidateDraftAction | `ui.skill-control-center.ValidateDraftAction` | Action |

## UI Concept Graph

| From | Edge | To | Evidence |
|---|---|---|---|
| `ui.skill-control-center.ControlCenterLayout` | wraps | `ui.skill-control-center.ControlCenterWorkspace` | [Structural variants](#structural-variant-a--signal-deck) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.AttentionQueuePanel` | [Task-led rule](#shared-interaction-rules) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.CatalogWorkspace` | [Component inventory](#component-inventory) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.DetailInspector` | [Component inventory](#component-inventory) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.EvidenceInspector` | [Component inventory](#component-inventory) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.TopologyWorkspace` | [Explicit topology rule](#shared-interaction-rules) |
| `ui.skill-control-center.ControlCenterWorkspace` | renders | `ui.skill-control-center.DraftInspector` | [Component inventory](#component-inventory) |
| `ui.skill-control-center.AttentionQueuePanel` | consumes | `ui.skill-control-center.useAttention` | [Data flow](#data-flow) |
| `ui.skill-control-center.AttentionQueuePanel` | displays | `ui.skill-control-center.AttentionQueue` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.AttentionReadBinding` | fetches | `skill-control-center.GetAttentionQueue` | [Data flow](#data-flow) |
| `ui.skill-control-center.AttentionAdapter` | shapes | `ui.skill-control-center.AttentionQueue` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.CatalogWorkspace` | consumes | `ui.skill-control-center.useCatalog` | [Data flow](#data-flow) |
| `ui.skill-control-center.CatalogWorkspace` | displays | `ui.skill-control-center.CatalogResultSet` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.CatalogSearchForm` | submits | `ui.skill-control-center.SearchCatalogAction` | [Catalog form](#catalogsearchform) |
| `ui.skill-control-center.CatalogSearchForm` | contracts | `skill-control-center.ControlCenterReadAPI` | [Catalog form](#catalogsearchform) |
| `ui.skill-control-center.CatalogReadBinding` | fetches | `skill-control-center.SearchCatalog` | [Data flow](#data-flow) |
| `ui.skill-control-center.CatalogAdapter` | shapes | `ui.skill-control-center.CatalogResultSet` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.DetailInspector` | consumes | `ui.skill-control-center.useObjectDetail` | [Data flow](#data-flow) |
| `ui.skill-control-center.ObjectDetailBinding` | fetches | `skill-control-center.GetObjectDetail` | [Data flow](#data-flow) |
| `ui.skill-control-center.EvidenceInspector` | consumes | `ui.skill-control-center.useEvidence` | [Data flow](#data-flow) |
| `ui.skill-control-center.EvidenceInspector` | displays | `ui.skill-control-center.EvidenceSummary` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.EvidenceReadBinding` | fetches | `skill-control-center.GetUsageEvidence` | [Data flow](#data-flow) |
| `ui.skill-control-center.EvidenceAdapter` | shapes | `ui.skill-control-center.EvidenceSummary` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.TopologyWorkspace` | consumes | `ui.skill-control-center.useTopology` | [Data flow](#data-flow) |
| `ui.skill-control-center.TopologyWorkspace` | consumes | `ui.skill-control-center.usePathQuery` | [Data flow](#data-flow) |
| `ui.skill-control-center.TopologyWorkspace` | displays | `ui.skill-control-center.DispatchLineage` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.TopologyWorkspace` | displays | `ui.skill-control-center.IntraDispatchTopology` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.TopologyReadBinding` | fetches | `skill-control-center.GetTopology` | [Data flow](#data-flow) |
| `ui.skill-control-center.DispatchLineageAdapter` | shapes | `ui.skill-control-center.DispatchLineage` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.IntraDispatchAdapter` | shapes | `ui.skill-control-center.IntraDispatchTopology` | [View models](#view-models-and-adapters) |
| `ui.skill-control-center.PathQueryForm` | contracts | `skill-control-center.ControlCenterReadAPI` | [Path form](#pathqueryform) |
| `ui.skill-control-center.PathQueryForm` | submits | `ui.skill-control-center.SubmitPathAction` | [Path form](#pathqueryform) |
| `ui.skill-control-center.PathReadBinding` | fetches | `skill-control-center.FindPath` | [Data flow](#data-flow) |
| `ui.skill-control-center.DraftEditorForm` | submits | `ui.skill-control-center.SaveDraftAction` | [Local operations](#local-operations) |
| `ui.skill-control-center.DraftEditorForm` | submits | `ui.skill-control-center.ValidateDraftAction` | [Local operations](#local-operations) |
| `ui.skill-control-center.DraftEditorForm` | contracts | `skill-control-center.DraftPort` | [Draft port](interfaces.md#internal-draftport) |
| `ui.skill-control-center.DraftWriteBinding` | mutates | `skill-control-center.SaveChangeProposal` | [Local operations](#local-operations) |
| `ui.skill-control-center.DraftValidationBinding` | mutates | `skill-control-center.ValidateChangeProposal` | [Local operations](#local-operations) |
| `ui.skill-control-center.PreferenceForm` | submits | `ui.skill-control-center.SavePreferenceAction` | [Preference form](#preferenceform) |
| `ui.skill-control-center.PreferenceForm` | contracts | `skill-control-center.LocalPreferencePort` | [Preference port](interfaces.md#internal-localpreferenceport) |
| `ui.skill-control-center.PreferenceWriteBinding` | mutates | `skill-control-center.SaveLocalPreference` | [Local operations](#local-operations) |
| `ui.skill-control-center.DraftStatusIndicator` | reflects | `skill-control-center.DraftLifecycle` | [State mapping](#state-to-ui-mapping) |

## Explicitly Deferred

- authoritative apply, retry, reconciliation and accepted receipt: SCC-BL-001..003;
- benchmark-based acceptance, promotion or winner selection: SCC-BL-004..008;
- any fourth product variant;
- copying or adapting existing repository variants.
