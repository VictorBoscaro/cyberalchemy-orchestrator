# Findings — skill and dispatch control center UX

## One-line answer

Open in a **task-led control workspace**, then make a **focal topology the primary detail surface
after selection**. Lists answer attention, location, comparison, and configuration questions;
the focal graph answers paths, lineage, and impact without exposing a 70-node hairball.

## Evidence verdict matrix

| candidate | owner | witnessed? | sound? | verdict | use-mode |
|---|---|---:|---:|---|---|
| Global graph as landing page | graph-product precedents | partly | no causal support; density risk | KILL | typed negative: precedent does not prove intuitiveness |
| List-only control center | catalog precedents | partly | loses relational path context | KILL | typed negative: no lineage witness |
| Task-led list + focal graph after selection | mixed HCI/product corpus | yes | yes, pending benchmark | GO | build-from-owned |
| Usage count from current skill graph | none | no | false: graph is declarative | KILL | typed negative: no observed telemetry |
| Separate declared and observed layers | APT/OpenLineage/Backstage patterns | yes | yes | GO | build-from-owned |
| Safe direct editing of derived edges | none | no | violates authority boundary | KILL | typed negative: wrong owner |
| Three visually original, functionally identical variants | user requirement | conditional | yes after contract/rubric freeze | GO | novel-attempt |

## Information architecture decision

### First paint

The default altitude is operational attention:

1. pending approvals or blockers;
2. current state and partial/degraded conditions;
3. visible scope, repository, period and filters;
4. provenance, freshness and coverage;
5. evidence-state legend;
6. searchable skill/dispatch catalog;
7. safe next action.

The landing surface is not a graph. It is a scannable workspace with an attention queue, compact
health summary, filters and catalog. This is supported by the repository's pending-first contract
and progressive-disclosure constraint, while external product documentation is treated only as
precedent, not causal UX proof
([task-first C1–C6](research.md#cartões-de-alegação)).

### Selection and detail transition

Selection alone does not change view. The interaction state machine is:

1. `select(object)` updates the stable selection and URL while preserving the current view;
2. `open-detail(object)` opens the detail workspace;
3. `open-topology(object, model)` explicitly opens a focal graph;
4. `back` restores the prior view, filters, scroll and selection;
5. a deep link restores `view`, `object`, `model`, filters and path query or reports which part
   could not be restored.

Inside an explicitly opened topology view, the primary detail surface is a **focal graph**:

- selected object centered;
- one hop upstream/downstream initially;
- path highlighting and depth controls;
- grid/list mirror with identical selection;
- tree only for proven single-parent acyclic relations;
- global graph only by explicit action;
- URL, filters and selection survive view changes.

The UI keeps three read models separate:

- **skill relations:** `explicit_path` is a strong declared path reference; `named_reference` is a
  weak extracted textual mention and must not be labeled “calls” or “depends on”;
- **dispatch lineage:** parent/child hierarchy derived only from `parent_dispatch_id`;
- **intra-dispatch topology:** groups and connections declared inside one dispatch.

No unified cross-model edge is shown until a governed read model defines its identity and
provenance. This preserves the actual skill-graph witness without extrapolating it to dispatches
([topology claims C1–C7](research.md#registro-de-claims)).

## Required evidence language

`declared`, `observed`, `inferred`, `unknown-or-unavailable` and `stale` are visible and
non-collapsing. A relation may be both declared and observed; freshness is a qualifier.

- Current skill graph contains strong `explicit-path` relations and weak `extracted-mention`
  relations. Both are source-derived, but only the former may be described as a declared path
  reference.
- Skill usage is currently `unknown-or-unavailable`.
- `0 observed` is legal only with proven complete coverage for the selected window.
- Absence of telemetry must never become “unused”.
- Every aggregate shows window, UTC basis, coverage, exclusions and update time.

### Observation contract

An observed usage event must include `event_id`, `object_id`, `object_kind`, `occurred_at_utc`,
`received_at_utc`, `producer`, `run_or_correlation_id`, `outcome`, `source`, `schema_version` and
optional `retry_of`. Deduplicate by `(producer, event_id)`; a retry is not another use unless it
has a new run identity. Counts use an inclusive-start/exclusive-end UTC window.

Coverage is `accepted_sources / expected_sources` for the selected scope, with both numerator and
denominator visible. `observed` requires at least one accepted event. `unknown-or-unavailable`
applies when the denominator is unknown, access is denied, or ingestion is absent. `stale`
qualifies any state when `now - last_successful_ingest > freshness_sla`; the initial SLA is a
configuration value, never silently assumed by the UI. Zero is shown only when coverage is
complete for the entire window.

## Operator questions

The product must answer:

1. What needs attention now?
2. What skills and dispatches exist in this scope?
3. What does the selected object depend on, and what depends on it?
4. Which path connects A to B?
5. What is declared versus actually observed?
6. How often and how recently was it observed, with what outcome?
7. What is stale, partial, unavailable or excluded?
8. What may I change safely, and what authority/receipt would that require?

## Path-query contract

A path query names its model, source, target, direction, allowed edge kinds, maximum depth and
maximum returned paths. Default skill queries use directed `explicit_path` edges only; an
“inclusive” option adds `named_reference` edges with a weak-evidence label. Dispatch lineage uses
only parent/child edges; intra-dispatch paths use only declared connections.

Return shortest paths first, then stable lexical node-ID order. Cycles are visited once per path.
Results disclose depth and path limits, whether more paths exist, and the evidence class of every
edge. Required states are `success`, `no-path`, `invalid-endpoint`, `unsupported-model`, `error`
and `truncated`; partial source failure may not be rendered as `no-path`.

## Configuration boundary

Read-model preferences may be manipulated locally: filters, layout, pins, comparison sets and saved
views. Derived relations are never edited directly.

An authoritative change needs:

- stable target identity and base revision/hash;
- explicit diff;
- resolved effective configuration and value origins;
- validation results;
- capability and approval;
- idempotency key;
- accepted journal/event reference;
- resulting receipt and correlation/run IDs.

Until that route exists, the UI shows drafts and differences but does not imply they were applied.

| action | owner/authority | state transition |
|---|---|---|
| Change local filter/layout/pin | current user; local preference store | `clean → saved-local` or `save-failed → retry` |
| Create/edit proposed configuration | draft owner | `clean → draft-dirty → draft-saved` |
| Validate proposal | configured validator | `draft-saved → validating → valid/invalid` |
| Request authoritative change | capability holder plus required approval | `valid → approval-pending → approved/rejected` |
| Apply accepted change | authoritative command handler | `approved → applying → accepted/conflict/failed` |
| Retry after conflict/failure | same authority, new base revision when required | `conflict/failed → revised → validating` |

Only `accepted` with an append-before-ack receipt changes authoritative status. Every failure keeps
the draft and exposes a retry-safe idempotency key and current base revision.

## Acceptance rubric to freeze before implementation

| Criterion | Required evidence | Minimum acceptance |
|---|---|---|
| **Clarity** | Tasks identify attention, state, scope, provenance, freshness and evidence class. | ≥90% correct; no inference/unavailable state rendered as fact; essential context on first paint. |
| **Usability** | Search, filters, detail, back, path, view switch and configuration review by keyboard. | ≥90% completion; zero keyboard traps; all enumerated WCAG 2.2 AA and manual-flow checks pass. |
| **Visual consistency** | Same semantics, content, fixtures, states, actions and test IDs across three variants. | 100% functional equivalence; color never sole carrier; applicable contrast passes. |
| **Operational efficiency** | Locate known object/attention, find path, inspect provenance, diagnose stale/degraded. | ≤3 actions for attention/object; ≤5 for path/provenance; benchmark both task-first and topology-first. |

The usability benchmark uses at least 10 representative operators who did not build the variants,
the same randomized task wording and fixed fixtures, and records correctness, completion without
assistance, actions and wall-clock time from task reveal to correct answer. A flow completes only
when the participant states the expected answer or obtains the expected accepted receipt. Report
median and P75 by task and variant; approve a direction only when it meets every absolute threshold
and its 95% bootstrap interval does not cross the allowed 10-percentage-point location penalty.

Performance uses two independent fixtures: (a) skill topology with 70 nodes/262 typed edges and
(b) dispatch catalog with approximately 700 rows plus representative lineage. Report browser
version, OS/hardware, viewport, cache state, network profile and cold/warm run. Provisional targets
are first meaningful paint ≤1.5 s P95, filter/selection ≤100 ms P95, path ≤250 ms P95 and no long
task over 200 ms; discovery must bind them to a reproducible reference environment.

Accessibility acceptance enumerates applicable WCAG 2.2 AA success criteria per critical flow and
also requires manual matrices for full keyboard operation and visible focus, focus restoration,
screen-reader names/states/live regions, 200% zoom and 320 CSS-pixel reflow, reduced motion, and a
non-canvas list/table alternative for every topology answer.

The design may promote topology closer to the landing page only if a representative benchmark
shows a material lineage/path advantage without more than a 10 percentage-point location-task
penalty.

## Three-variant boundary

The current ten-variant contract must be revised before implementation. The new contract will
require exactly three variants with:

- identical API, fixtures, mandatory content, states, commands and test IDs;
- distinct art direction verified by screenshot review;
- no reuse of existing repository variants as visual references;
- the same loading, empty, no-match, focal-lineage, observed-overlay, stale/degraded and partial-error
  screenshot scenarios;
- visual difference never changing meaning or authority.

Originality is structural, not a palette swap. Blind screenshot review must distinguish all three
variants through at least three of four dimensions: layout hierarchy, navigation model,
information density/rhythm and topology treatment. Review the same data at fixed desktop and
mobile viewports, light/dark themes, and every mandatory state. Reviewers see anonymized variants
in randomized order and score clarity, usability, visual consistency, operational efficiency and
structural distinctness before learning which implementation produced each image.

The visual directions returned by the topology researcher are candidates only; discovery owns
whether to keep, replace or reject them.

## Source-quality adjudication

- WCAG is normative for accessibility, not information architecture.
- W3C COGA/APG inform clarity and interaction obligations but do not prove layout superiority.
- Peer-reviewed visualization taxonomies structure tasks/interactions; they do not prove list-first
  or topology-first for this product.
- Official product docs prove implemented precedent and observable limits, not causal usability.
- `maestro-trama` remains non-authoritative adjacent evidence.

## Close

- `exit_reason`: `resolved`
- execution seats: 2 explorers
- capability/check-tension helpers: 3
- `agents_spawned.total`: 5
- `loops_used`: 1
- parent approval: accepted
- next stage: persisted red-team review over `research.md` and `findings.md`
