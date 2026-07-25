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

### After selecting a skill or dispatch

The primary detail surface becomes a **focal graph**:

- selected object centered;
- one hop upstream/downstream initially;
- path highlighting and depth controls;
- grid/list mirror with identical selection;
- tree only for proven single-parent acyclic relations;
- global graph only by explicit action;
- URL, filters and selection survive view changes.

This preserves the relational witness established by the repository graph and operational
lineage products without defaulting to a dense topology
([topology claims C1–C7](research.md#registro-de-claims)).

## Required evidence language

`declared`, `observed`, `inferred`, `unknown-or-unavailable` and `stale` are visible and
non-collapsing. A relation may be both declared and observed; freshness is a qualifier.

- Current graph data is `declared`.
- Skill usage is currently `unknown-or-unavailable`.
- `0 observed` is legal only with proven complete coverage for the selected window.
- Absence of telemetry must never become “unused”.
- Every aggregate shows window, UTC basis, coverage, exclusions and update time.

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

## Acceptance rubric to freeze before implementation

| Criterion | Required evidence | Minimum acceptance |
|---|---|---|
| **Clarity** | Tasks identify attention, state, scope, provenance, freshness and evidence class. | ≥90% correct; no inference/unavailable state rendered as fact; essential context on first paint. |
| **Usability** | Search, filters, detail, back, path, view switch and configuration review by keyboard. | ≥90% completion; zero keyboard traps; zero critical accessibility failure in critical flows. |
| **Visual consistency** | Same semantics, content, fixtures, states, actions and test IDs across three variants. | 100% functional equivalence; color never sole carrier; applicable contrast passes. |
| **Operational efficiency** | Locate known object/attention, find path, inspect provenance, diagnose stale/degraded. | ≤3 actions for attention/object; ≤5 for path/provenance; benchmark both task-first and topology-first. |

Performance targets remain provisional until the implementation environment is characterized:
first meaningful paint ≤1.5 s P95, filter/selection ≤100 ms P95, path ≤250 ms P95 and no long task
over 200 ms on the 70-node/262-typed-edge fixture.

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
