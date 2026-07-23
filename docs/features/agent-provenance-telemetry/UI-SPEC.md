---
id: agent-provenance-telemetry-ui
feature: agent-provenance-telemetry
title: "Agent Provenance Telemetry UI Applicability"
summary: L0 decision that no APT UI surface is currently applicable; preserves read-only future presentation constraints.
status: deferred
pillar: application
domain: agent-provenance-telemetry-ui
audience:
  - developers
  - reviewers
priority: p2
lang: en
owners: []
updatedAt: 2026-07-23
dependencies:
  - specs/SPEC.md
  - specs/interfaces.md
  - specs/queries.md
  - specs/states.md
  - specs/observability.md
includes: []
constitution: null
applicability: not-applicable-l0
runtimeGate: block
---

# UI Applicability: Agent Provenance Telemetry

> L0 decision: **not applicable; deferred**. This file registers no frontend implementation,
> route, page, component, action or transport endpoint.

## Applicability Decision

APT has three specified read-only projections, but no implemented APT runtime or UI wiring. The
feature root explicitly says the specification does not create a deployed runtime or UI
([module boundary](specs/SPEC.md#what-this-module-owns)), and its runtime gate remains blocked.
Consequently, specifying concrete pages or API bindings now would invent an integration boundary
that does not exist.

Repository evidence inspected for this gate:

- The implemented server is a **Dispatch control-plane reader**, with handlers for
  `/api/snapshot`, `/api/dispatch/{repo_name}/{dispatch_id}`, `/api/overview`,
  `/api/repo/{repo_name}` and `/api/stream`; its only HTTP write is the separate
  `/api/confirm` marker flow ([current server](../../../implementations/server/main.py)).
- Existing static UIs consume those Dispatch control-plane endpoints, for example the
  [linear reader](../../../implementations/static/ui/linear/index.html). They do not consume
  `SessionRecord`, `DispatchScopeProjection`, `ResearchRecord` or
  `ProvenanceQueryPort`.
- Repository search found the three APT query result names in the APT specification corpus, not in
  current frontend or server implementation code. The authoritative query contract itself states
  that it introduces no external API ([Queries](specs/queries.md)).

The existing Dispatch reader is therefore adjacent evidence, not an APT presentation surface.
This decision does not extend it, assign it APT ownership or reinterpret `/api/confirm` as an APT
action.

## L0 UI Inventory

| UI concern | L0 count | Decision |
|---|---:|---|
| Routes | 0 | None registered |
| Pages | 0 | None registered |
| Components | 0 | None registered |
| Forms | 0 | None registered |
| Hooks/bindings | 0 | None registered |
| User actions | 0 | None registered |
| Mutations | 0 | None registered |
| APT transport/API endpoints | 0 | No transport contract exists |
| UI concepts | 0 | Registry intentionally empty |

## Route Table

No APT routes exist or are reserved in L0.

| Route | Page title | Layout | Auth required | Permission |
|---|---|---|---|---|
| _none_ | _not applicable_ | _not applicable_ | _not specified_ | _not specified_ |

Route names, navigation placement and URL identity are re-entry decisions. This document does not
reserve placeholders for them.

## Future Read-Only Presentation Contract

If the applicability gate is reopened, future Session, Dispatch and Research tables may consume
only the following three closed query outputs. These are data-contract requirements, not current
pages, components, APIs or implementation claims.

| Future table concern | Sole APT query output | Minimum presentation boundary |
|---|---|---|
| Session | [`SessionRecord`](specs/queries.md#sessionrecord) | Exact Session identity, immutable origin/name/time, currentness, authoritative Dispatch links and derived research/fact counts |
| Dispatch | [`DispatchScopeProjection`](specs/queries.md#dispatchscopeprojection) | Exact pinned Dispatch snapshot, authoritative Session links, declared scope, current capture summaries and policy/check maps |
| Research | [`ResearchRecord`](specs/queries.md#researchrecord) | Exact named capture, capture currentness/status/evidence refs, questions, answers, references, checks, problems, claims and formalizations |

Any future presentation must render the returned `requested_o`, `effective_as_of`,
`pinned_input_manifest`, `pinned_input_digests`, `snapshot_digest` and `projection_hash` according
to the closed [`QueryResult`](specs/interfaces.md#query-request-and-result) contract. It must not:

- infer Session–Dispatch membership, research access, support or verification;
- fetch mutable Dispatch state to decorate a pinned historical projection;
- expose raw artifact bodies, answer bytes, selectors, prompts or operational logs;
- collapse policy/assessor maps or independent check disagreement into one unqualified verdict;
- treat a projection, cache, dashboard or rendered table as authority; or
- submit an append, repair, retry, projection rebuild or other mutation.

There is no L0 pagination or filtering contract
([Authorization, Errors and Pagination](specs/queries.md#authorization-errors-and-pagination)).
A UI cannot add page/offset/cursor/filter semantics without a registered query-contract revision.

## Future State Requirements

These states are requirements for a future applicability cycle only. They do not imply current
state components, labels, colors or interaction behavior.

| State | Required future behavior |
|---|---|
| Empty | Distinguish an authorized successful projection with an empty canonical collection from `NOT_FOUND`; do not imply missing provenance or failed capture without returned evidence. |
| Loading | Identify which exact identity and `requested_o` are pending; do not show stale data as if it answered the pending boundary. |
| Error | Map only the closed query error union; preserve safe detail and retryability, and never repair, append or silently fall back to mutable current data. |
| As-of | Show both `requested_o` and `effective_as_of` when they differ, including that the effective value is the preceding complete verified group boundary. |
| Profile-blocked | For `SCHEMA_UNSUPPORTED`, `PINNED_INPUT_INVALID` or profile/manifest verification failure, show that the projection is unavailable; do not synthesize partial data or offer an authority-changing recovery action. |

The exact copy, visual treatment and retry control—if any—remain unregistered until a concrete host
UI and transport exist.

## Data Flow and Mutation Authority

No APT API call, hook, cache key or mutation is defined in L0. A future binding may request only a
closed intent through [`ProvenanceQueryPort`](specs/interfaces.md#provenancequeryport) and render
its derived result:

```text
authenticated future UI
  -> closed Session | Dispatch | Research query intent
  -> ProvenanceQueryPort
  -> verified as-of derived projection
  -> read-only presentation
```

The reverse direction terminates at the query intent. There is no UI-to-Operation edge. Query
evaluation and presentation have zero append, artifact-write, Dispatch-write, retry, repair,
checkpoint-build or projection-rebuild authority.

## Form Contracts and Actions

There are no L0 forms or APT user actions. Identity selection, as-of selection, retry controls,
exports and navigation are not specified. In particular, this file does not expose any of the six
APT append Operations as a UI mutation.

## Accessibility Constraints for Re-entry

Before any future UI concept is registered:

- Session, Dispatch and Research collections must use semantic tables with programmatically
  associated headers and captions identifying the exact projection and as-of boundary.
- Empty, loading, error, as-of and profile-blocked meanings must be available to assistive
  technology and cannot rely on color alone.
- Loading updates must not steal focus; error summaries and refreshed projection boundaries must
  be announced through an appropriate live-region strategy.
- Keyboard users must be able to traverse nested canonical sets/maps and reach any disclosed
  evidence reference without pointer-only interaction.
- Truncated opaque IDs and digests must retain an accessible exact value and a clear distinction
  between identity, status, disposition, assessment and check result.
- Any future virtualization or progressive disclosure must preserve table semantics, reading order
  and the complete canonical-result meaning.

## Privacy and Non-Authority Constraints for Re-entry

- Render only fields present in the authorized query result; never resolve or preview
  `raw_return_ref` in the APT table surface.
- Do not place raw bodies, answer text, selectors, prompts, source locators, credentials or
  exception text in DOM attributes, client logs, analytics, traces, URLs or cache keys.
- Opaque IDs, digests, actor refs and evidence refs require the same access control as their source
  projection and must not become telemetry dimensions.
- Client caches, exports and browser persistence are derived copies with bounded retention, never
  accepted provenance or replay checkpoints.
- Dashboard/runbook signals remain non-authoritative and cannot enable commands, retries, rebuilds
  or policy decisions ([Non-Authority Contract](specs/observability.md#non-authority-contract)).

## UI Concept Registry

No concepts are registered for L0.

| Concept | ID | Type |
|---|---|---|
| _none_ | _none_ | _none_ |

The three rows in the future presentation table are query consumers under consideration, not UI
concept registrations.

## Applicability Re-entry Gate

Change `applicability` from `not-applicable-l0` only through a reviewed revision that supplies all
of the following evidence:

1. an implemented and conformance-tested `ProvenanceQueryPort` for all three closed query outputs;
2. an approved authenticated transport contract with exact request/result/error mapping, without
   inventing fields, filters, pagination or mutations;
3. an identified host UI, navigation owner and applicable UI architecture/constitution;
4. explicit authorization, retention and client-cache rules for each projection;
5. concrete route/page/component concepts registered without collision;
6. designs for all five future states above, including requested/effective as-of disclosure;
7. accessibility review and tests for semantic tables, focus, announcements and non-color meaning;
8. privacy tests proving prohibited content does not enter DOM, URL, cache or client telemetry; and
9. architecture tests proving the UI remains a derived query consumer with zero mutation or
   authority effects.

Until every item is available, this UI specification remains deferred and the L0 inventory remains
zero.

## Connections

- [Feature specification](specs/SPEC.md)
- [Query contracts](specs/queries.md)
- [Interface contracts](specs/interfaces.md)
- [State and reducer contracts](specs/states.md)
- [Observability non-authority contract](specs/observability.md#non-authority-contract)
- [Planned test contract](TEST-SPEC.md)
