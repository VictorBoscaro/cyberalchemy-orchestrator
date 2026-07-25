---
tags: [skill-control-center, spec, test]
node_type: spec
is_session: false
layer: application
nature: procedural, technical
status: draft
version: 0.1.0
last_updated: 2026-07-25
owners:
  - "@VictorBoscaro"
---

# Test Spec: Skill & Dispatch Control Center

This specification defines implementation acceptance for the Phase 1 read-only/draft-only backend,
shared contracts, exactly three frontend variants, and revision-bound validation evidence. Tests
consume the five frozen fixture families and `fixtures/manifest.json`. No test may require or imply
authoritative apply, retry/reconcile, accepted receipt, or benchmark-based variant promotion.

## Suite Partition

| Suite | Runner boundary | Purpose |
|---|---|---|
| `fixture-contract` | Runtime-neutral unit | Schema/digest/case identity and source counts |
| `domain-read-model` | Backend unit/property | Projection, evidence, path and degradation algebra |
| `interface-contract` | HTTP/local-port integration | Six routes, envelopes, status mapping and closed local codes |
| `ui-shared` | Browser component/E2E, parameterized by A/B/C | Shared flows, states, navigation and authority safety |
| `ui-accessibility` | Browser automation + manual evidence | WCAG 2.2 A/AA and semantic topology parity |
| `performance` | Browser/backend harness | Separate topology/catalog cold/warm measurements |
| `visual-evidence` | Screenshot + blind review harness | Complete 204-row matrix and four design criteria |

## Fixture Corpus

| Fixture | Required invariant | Primary consumers |
|---|---|---|
| `FX-SKILL-TOPOLOGY-v1` | 70 nodes, 262 typed edges, 15 `explicit_path`, 247 `named_reference` | skill relations, path, topology performance |
| `FX-DISPATCH-CATALOG-v1` | 700 rows and valid/unresolved/legacy/orphan/pending/open/closed/intra-Dispatch cases | attention, catalog, lineage, catalog performance |
| `FX-EVIDENCE-MIXED-v1` | complete/partial/unavailable, fresh/stale/unknown, dedupe/retry/conflict | evidence algebra and degradation |
| `FX-DRAFT-v1` | target/base/diff/origins, valid/invalid previews, conflicts/failures, authoritative route unavailable | local operations and draft UI |
| `FX-INTERFACE-BOUNDARY-v1` | complete and missing host/auth/route-owner bindings with recovery explanation | IF-I5 publication and `read-api-unavailable` UI |

Every fixture and nested case used below has a non-null manifest digest. Tests recompute
`lowercase sha256(RFC8785_JCS(fixture JSON excluding sha256))` before consuming it.

## Test Matrix

### Fixture and architecture gates

| ID | Test | Validates |
|---|---|---|
| [SCC-T-FX-001](#scc-t-fx-001--fixture-manifest-integrity) | Manifest entries, schemas and JCS digests fail closed on mismatch | [SPEC Fixture Contract](SPEC.md#fixture-contract) |
| `SCC-T-FX-002` | Skill fixture counts and 15/247 relation split are exact | [SPEC Fixture Contract](SPEC.md#fixture-contract) |
| `SCC-T-FX-003` | Dispatch fixture has exactly 700 rows and every required lineage/degradation case | [SPEC Fixture Contract](SPEC.md#fixture-contract) |
| `SCC-T-ARCH-001` | UI/read-model modules cannot import raw stores directly | [AR-002](architecture.md#dependency-and-interface-rules) |
| `SCC-T-ARCH-002` | Local draft ports have no dependency path to ledger/config writers | [AR-005](architecture.md#dependency-and-interface-rules) |
| `SCC-T-ARCH-003` | Backend/API acceptance completes before frontend visual acceptance | [Architecture Gate Result](architecture.md#gate-result) |

### Read models, queries, and evidence

| ID | Test | Validates |
|---|---|---|
| `SCC-T-Q-001` | Common envelope preserves `complete|partial|unavailable|error`, source facts and snapshot identity | [Common Query Contract](queries.md#common-query-contract) |
| `SCC-T-Q-002` | Parameterized Attention cases exhaust `success|invalid-request`; success ordering and safe-next-action projection are deterministic | [GetAttentionQueue](queries.md#getattentionqueue) |
| `SCC-T-Q-003` | Parameterized Catalog cases exhaust `success|no-match|invalid-request|invalid-cursor|stale-snapshot`; normalization, filters, pagination and matches are deterministic | [SearchCatalog](queries.md#searchcatalog) |
| `SCC-T-Q-004` | Parameterized ObjectDetail cases exhaust `found|not-found|invalid-request`; `not-found` requires complete identity authority and found objects expose non-local authority as unavailable | [GetObjectDetail](queries.md#getobjectdetail) |
| `SCC-T-Q-005` | Parameterized Topology cases exhaust `success|invalid-request|invalid-endpoint|unsupported-model|truncated`; absence states require complete identity authority and model identity remains isolated | [GetTopology](queries.md#gettopology) |
| [SCC-T-Q-006](#scc-t-q-006--deterministic-path-contract) | Path validation/order/cycles/parallel edges/limits/non-success states are deterministic | [FindPath](queries.md#findpath) |
| [SCC-T-Q-007](#scc-t-q-007--evidence-algebra) | Parameterized UsageEvidence cases exhaust `success|not-found|invalid-request`; `not-found` requires complete identity authority and evidence algebra is exhaustive | [GetUsageEvidence](queries.md#getusageevidence) |
| `SCC-T-Q-008` | Redelivery, duplicate, retry and semantic conflict cases count logical invocations exactly once | [Evidence rules](queries.md#evidence-and-coverage-rules) |
| `SCC-T-Q-009` | Partial identity/path authority cannot return `not-found`, `invalid-endpoint`, or `no-path` | [Query invariants](queries.md#query-invariants) |
| `SCC-T-Q-010` | No query mutates source, draft, preference, ledger, or configuration state | [Q-I1](queries.md#query-invariants) |
| `SCC-T-Q-011` | Cursor succeeds only for its exact snapshot and normalized-filter digest; either mismatch returns invalid/stale cursor | [Q-I4](queries.md#query-invariants) |
| `SCC-T-Q-012` | Injected raw prompts, agent returns, logs and credentials never appear in any query/envelope output | [Q-I5](queries.md#query-invariants) |
| `SCC-T-Q-013` | Every `named_reference` edge renders `label=mention` and `strength=weak`; no call claim is produced | [SCC-R-003](SPEC.md#formal-rules-and-invariants) |

### Interface and local operations

| ID | Test | Validates |
|---|---|---|
| `SCC-T-IF-001` | External inventory equals six IF-I6 routes and each route binds exactly one declared query | [IF-I1/IF-I6](interfaces.md#interface-invariants) |
| `SCC-T-IF-002` | Route remains unpublished when host/auth/route-owner binding is incomplete | [IF-I5](interfaces.md#interface-invariants) |
| `SCC-T-IF-003` | HTTP 400/409/422/500 and typed HTTP-200 outcomes match the envelope contract | [HTTP status mapping](interfaces.md#http-status-mapping) |
| `SCC-T-IF-004` | Read-only POST path-query has no mutation effect | [Path endpoint](interfaces.md#post-v1control-centerpath-query) |
| `SCC-T-IF-005` | Missing IF-I5 binding produces `read-api-unavailable`, never the intentional `authoritative-route-unavailable` boundary | [Route table](UI-SPEC.md#route-table) |
| [SCC-T-OP-001](#scc-t-op-001--local-preference-total-matrix) | Every `SaveLocalPreference` row/code/precedence/revision/retention rule is tested | [SaveLocalPreference transition](operations.md#state-transition) |
| [SCC-T-OP-002](#scc-t-op-002--draft-save-total-matrix) | Every `SaveChangeProposal` row/code/precedence/revision/retention rule is tested | [SaveChangeProposal transition](operations.md#state-transition-1) |
| [SCC-T-OP-003](#scc-t-op-003--draft-validation-total-matrix) | Every `ValidateChangeProposal` row/code/precedence/atomic-preview rule is tested | [ValidateChangeProposal transition](operations.md#state-transition-2) |
| `SCC-T-OP-004` | Unknown producer code becomes consumer `protocol-error` without partial write | [AD-007](architecture.md#ad-007) |
| [SCC-T-SAFE-001](#scc-t-safe-001--forbidden-authoritative-surface) | No route, port, hook, action, state or copy claims authoritative mutation/receipt/promotion | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |

### Navigation and shared variant contract

| ID | Test | Validates |
|---|---|---|
| `SCC-T-NAV-001` | `select` preserves view, filters, scroll and comparison state in A/B/C | [WN-I1](states.md#invariants) |
| `SCC-T-NAV-002` | Detail and topology open only through explicit named actions | [WorkspaceNavigation](states.md#workspacenavigation) |
| `SCC-T-NAV-003` | Topology has exactly one model; explicit model change preserves restorable token | [WN-I2/3](states.md#invariants) |
| `SCC-T-NAV-004` | Back restores one LIFO token or the default workspace on an empty stack | [WN-I4](states.md#invariants) |
| `SCC-T-NAV-005` | Deep link restores supported members and reports unsupported/missing members | [WN-I5](states.md#invariants) |
| [SCC-T-UI-001](#scc-t-ui-001--cross-variant-semantic-parity) | A/B/C have identical actions, states, fixtures, expected answers and test IDs | [Shared Variant Contract](UI-SPEC.md#shared-variant-contract) |
| `SCC-T-UI-002` | Blind structure assertion distinguishes every variant pair in at least three declared dimensions | [Structural variants](UI-SPEC.md#structural-variant-a--signal-deck) |
| `SCC-T-UI-003` | Existing repository variants/assets are absent from implementation provenance/reference manifest | [UI Specification scope](UI-SPEC.md#ui-specification-skill--dispatch-control-center) |

### Critical flows and mandatory states

| ID | Test | Validates |
|---|---|---|
| `SCC-T-CF-01` | A/B/C complete TriageAttention with exact answer and state preservation | [CF-01](UI-SPEC.md#phase-1-critical-flows) |
| `SCC-T-CF-02` | A/B/C locate target without selection-driven navigation | [CF-02](UI-SPEC.md#phase-1-critical-flows) |
| `SCC-T-CF-03` | A/B/C report mixed evidence without unknown-as-zero | [CF-03](UI-SPEC.md#phase-1-critical-flows) |
| `SCC-T-CF-04` | A/B/C return identical path answer in visual and semantic views | [CF-04](UI-SPEC.md#phase-1-critical-flows) |
| `SCC-T-CF-05` | A/B/C diagnose partial source/window coverage without false healthy state | [CF-05](UI-SPEC.md#phase-1-critical-flows) |
| `SCC-T-CF-06` | A/B/C review/save/validate draft and stop at `authoritative-route-unavailable` without a receipt flow | [CF-06](UI-SPEC.md#phase-1-critical-flows) |
| [SCC-T-STATE-001](#scc-t-state-001--mandatory-state-matrix) | All 17 state rows render/assert identically in A/B/C | [State fixture contract](UI-SPEC.md#state-fixture-contract) |

### Accessibility, performance, and evidence

| ID | Test | Validates |
|---|---|---|
| [SCC-T-A11Y-001](#scc-t-a11y-001--accessibility-matrix) | Automated plus manual WCAG 2.2 A/AA matrix passes per variant/flow/state | [Accessibility Requirements](UI-SPEC.md#accessibility-requirements) |
| `SCC-T-A11Y-002` | Visual topology and semantic table have identical identities, relations, selection and path answer | [Topology requirement](UI-SPEC.md#accessibility-requirements) |
| `SCC-T-A11Y-003` | Keyboard/focus/back/live status/reflow/reduced-motion behavior passes | [Accessibility Requirements](UI-SPEC.md#accessibility-requirements) |
| [SCC-T-PERF-001](#scc-t-perf-001--separate-performance-runs) | Skill topology and Dispatch catalog run separately under frozen environment/cold-warm conditions | [SCD-13](discovery/control-center.md#separate-scale-fixtures-and-performance) |
| [SCC-T-VIS-001](#scc-t-vis-001--screenshot-manifest) | Screenshot manifest contains exactly 204 valid revision-bound rows | [Screenshot contract](UI-SPEC.md#screenshot-and-design-review-contract) |
| `SCC-T-VIS-002` | Blind review records all five criteria and creates a blocking design defect when any first-four score is below 3 | [Screenshot contract](UI-SPEC.md#screenshot-and-design-review-contract) |
| `SCC-T-VIS-003` | Design scores remain descriptive and no winner/promotion state or action is produced | [Phase 1 guardrails](BACKLOG.md#phase-1-guardrails) |

## Test Details

### SCC-T-FX-001 — Fixture manifest integrity

For each manifest entry:

1. load the fixture as JSON and reject duplicate object keys;
2. assert recognized `fixture_id` and `schema_version`;
3. remove only the top-level `sha256` member;
4. RFC 8785/JCS-normalize and SHA-256 hash;
5. assert lowercase digest equals both fixture and manifest expectations;
6. fail before any downstream render/query when an entry, digest or required case is missing.

### SCC-T-Q-006 — Deterministic path contract

Parameterize model, direction, allowed edge kinds, depth 0..10 and path limit 1..100. Assert:

- invalid request/endpoint/model precedence;
- source=target is the only zero-depth path;
- one node appears at most once per candidate path;
- exact duplicate edge IDs normalize once and non-identical parallel edges remain;
- complete paths sort by edge count then full edge-identity sequence;
- partial sources produce truncated/error, never no-path/invalid-endpoint;
- visual and semantic UI consume the returned order without recomputation.

### SCC-T-Q-007 — Evidence algebra

Generate every permitted `EvidenceClassSet × EvidenceCompleteness × FreshnessState` combination and
reject forbidden combinations. In particular:

- `{unknown-or-unavailable}` is singleton and pairs with unavailable when no trustworthy value exists;
- positive classes may coexist only with separate source facts;
- partial observed results are labeled lower bounds;
- zero/unused/none requires observed plus complete;
- freshness is independent and reduces `unknown > stale > fresh`;
- dedupe, redelivery and conflict diagnostics never increment accepted usage.

### SCC-T-OP-001 — Local preference total matrix

Run every row and first-match overlap from the SaveLocalPreference matrix. Verify success increments
revision exactly once; retryable rows retain input; every row has empty authoritative effects.

### SCC-T-OP-002 — Draft save total matrix

Run every allowed source state against every closed result code plus undeclared source/code. Verify
first-match precedence, CAS, atomic create/replace, no partial write, retention classes and the
absence of approval/capability/idempotency/receipt production.

### SCC-T-OP-003 — Draft validation total matrix

Run every preflight/result/persistence branch. `validation-valid` and `validation-invalid` require a
complete atomic preview bound to proposal/revision/validator. Retryable failures return to the saved
draft with retained request and unchanged revision. No branch grants authority.

### SCC-T-SAFE-001 — Forbidden authoritative surface

Search the compiled route/action/hook/state inventories for:

`approve`, `apply`, `retry-apply`, `reconcile`, `accepted-receipt`, `promote`, and equivalent
authoritative commands. Fail only on executable routes, controls, actions, hooks, effects, or copy
that falsely claims authoritative success. Source-projected read-only lifecycle facts, including
`Pending approval`, are allowed when they expose no command or granted authority. Also assert no
network request leaves the six-route read inventory and no local port reaches authoritative stores.

### SCC-T-UI-001 — Cross-variant semantic parity

Build one manifest per variant containing route, semantic regions, test IDs, actions, state IDs,
fixture selectors, expected-answer oracles and API/port bindings. Remove only declared visual fields
(tokens, layout coordinates, typography, motion). Deep-equality of the remaining manifests is
required. Then run `SCC-T-CF-01..06` and `SCC-T-STATE-001` against A, B and C using the same test body.

### SCC-T-STATE-001 — Mandatory state matrix

Load all 17 rows from `UI-SPEC.md#state-fixture-contract`. For every `variant × state`:

- verify fixture case/digest/test ID;
- assert required representation and focus behavior;
- assert the linked executable test reached the state;
- compare the semantic expected-answer snapshot across A/B/C;
- reject authoritative states not present in the Phase 1 matrix.

### SCC-T-A11Y-001 — Accessibility matrix

For each applicable `variant × critical flow × mandatory state` cell:

- validate every field in the exact record schema:
  `variant`, `flow_id`, `state_id`, `fixture_digest`, `criteria`, `keyboard`, `focus`,
  `screen_reader`, `live_region`, `reflow_200`, `width_320`, `reduced_motion`, `non_color`,
  `non_canvas`, `tester`, `timestamp`, `status`, and `evidence_digest`;
- recompute and match the fixture/evidence digests and require a non-empty reason for every
  `not-applicable`;
- run automated semantic/name/role/value/contrast checks;
- execute keyboard-only actions and verify focus order, visibility, restoration and no trap;
- record screen-reader labels, reading order and live-status announcements;
- verify 200% zoom and 320-CSS-px reflow, text spacing, non-color state, and reduced motion;
- complete the same topology answer using only the semantic table.

Any applicable WCAG 2.2 Level A/AA or required manual cell failure fails the variant. Automation
never substitutes for manual evidence. A missing field, missing/invalid digest, unjustified
`not-applicable`, or absent applicable cell also fails the variant.

### SCC-T-PERF-001 — Separate performance runs

Run `FX-SKILL-TOPOLOGY-v1` and `FX-DISPATCH-CATALOG-v1` independently. Record source/fixture digest,
browser/version, OS, CPU/memory class, exact viewport, network profile, cache state, and cold/warm
condition. Report first meaningful paint, filter/selection, path response and browser long tasks
against the provisional targets. Because the reference environment remains unsettled, report
misses as implementation evidence and defects where locally reproducible, but do not claim a final
cross-machine gate.

### SCC-T-VIS-001 — Screenshot manifest

Assert the Cartesian product `3 variants × 2 viewports × 2 themes × 17 states = 204`. Every row must
bind the canonical state fixture case/digest, source/backend/frontend revisions, screenshot
path/digest and executable state test. Missing/duplicate rows, stale revisions, digest mismatch or
orphan screenshots fail. Screenshots cannot satisfy functional/accessibility assertions.

### SCC-T-VIS-002 — Blind design review

Require one complete score record for clarity, usability, visual consistency, operational
efficiency and structural distinctness for every blind review set. Any score below 3 in the first
four criteria creates a blocking design defect that must be corrected and re-reviewed before
acceptance. Scores never promote or select a variant in Phase 1.

## Rule–Test Traceability Index

| Authority | Tests |
|---|---|
| SCC-R-001/002 navigation/topology | SCC-T-NAV-001..005, SCC-T-CF-02/04 |
| SCC-R-003 weak mention semantics | SCC-T-Q-013 |
| SCC-R-004..009 evidence/absence/path | SCC-T-Q-006..010, SCC-T-CF-03..05 |
| SCC-R-010/011 Phase 1 authority | SCC-T-OP-001..004, SCC-T-SAFE-001, SCC-T-CF-06 |
| SCC-R-012 exactly three variants | SCC-T-UI-001..003, SCC-T-CF-01..06 |
| AR-002/004/005/006 | SCC-T-ARCH-001/002, SCC-T-Q-006/007, SCC-T-UI-001 |
| IF-I1..006 | SCC-T-IF-001..005, SCC-T-SAFE-001, SCC-T-Q-010/012 |
| UI accessibility/evidence | SCC-T-A11Y-001..003, SCC-T-VIS-001/002 |

## Source Completeness Gate

Implementation readiness requires:

- every link in this TEST-SPEC and sibling DomainSpec documents resolves;
- every fixture/case/test ID referenced by UI-SPEC resolves to one manifest entry;
- every backend rule/state/code has at least one positive or negative assertion;
- every Phase 1 critical flow `CF-01..06` and mandatory state runs in A/B/C;
- no acceptance result depends on deferred benchmark statistics or authoritative mutation.

## Known Gaps and Backlog Obligations

| Gap | Why not tested in Phase 1 | Required follow-up |
|---|---|---|
| SCC-BL-001 terminal operation fencing | No authoritative apply route exists | Concurrency/lost-ack/late-append suite after protocol is ratified |
| SCC-BL-002 reconciliation/receipt lookup | No lookup authority/interface exists | Indeterminate/reconciliation/terminal-failure proof suite |
| SCC-BL-003 conflict recovery | Authoritative lifecycle is excluded | Executable conflict/revise/revalidate state/diagram parity |
| SCC-BL-004 scoring and SCC-BL-005 absolute acceptance | Benchmark cannot gate Phase 1 | Freeze valid action score and production-only acceptance |
| SCC-BL-006 estimability/convergence | Statistical model/sample authority unsettled | Independent statistical review and failure fixtures |
| SCC-BL-007 assistance taxonomy | Operator-study adjudication unsettled | Assistance/accommodation event and derivation tests |
| SCC-BL-008 withdrawal/worst-case population | Missingness protocol unsettled | Observed/worst-case denominator and imputation tests |

## Out of Scope

- authoritative approval, apply, exact retry, reconciliation, receipt acceptance and recovery;
- benchmark recruitment, inferential acceptance or variant promotion;
- a fourth product variant;
- deployment/host authentication choices not bound by an owning host.
