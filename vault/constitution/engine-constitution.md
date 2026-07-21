---
constitution_id: CONST-ENG
title: Engine Constitution — Orchestrator Core
status: candidate
owner: Victor
authority_level: candidate
updated_at: 2026-07-21
---

# Engine Constitution — Orchestrator Core

> Defines the enforceable patterns for the **code of the orchestrator engine** — today, the
> audit ledger, its appender, the parse/aggregation layer, and the read endpoints that serve
> the control plane; in the target runtime, also the write boundaries of the event journal and
> knowledge store. Answers: *"how should engine code preserve honest, non-overlapping authority?"*
>
> **Not** an import of ZefraHub's `development-practices-constitution`. The fundamental
> ideas were brought over; the finance-domain machinery (Pure Domain Slices, CNAB/XML
> pipelines, `use_cases → domain → infrastructure` layers, fund-administrator golden sets)
> was **left out on purpose** — none of it grounds here. Most rules below **ratify practice
> the code already earned** (see [ledger.py](../../implementations/server/ledger.py)), so
> several carry `veracity: high` — unlike [[frontend-constitution]], which bets on things
> not yet built. Statute: `candidate`, unreviewed. Claim ≤ proof.

---

## Objective

This constitution governs **the engine's own code** — everything under
`implementations/server/**` plus the appender that owns the current audit-ledger file. It answers
one question: *how must any function that accepts, reads, writes, caches or aggregates an
authoritative engine fact be built?*

What we want is a single property: **each fact has one declared authoritative home and one
validated physical write boundary; no code path corrupts it or lies about it.** Today that means
the append-only audit ledger. In the proposed communication runtime it also means keeping runtime
events and promoted knowledge out of that ledger's authority. A **corrupt write** poisons the
source. A **silent lie** — a count over a served window pretending to cover history, a swallowed
fault, a projection presented as canonical — injects noise the surface then presents as fact.

The mechanism is the repo's own lever, `residue = shadow ⊕ structure`
([FRAMINGS.md F1](../../FRAMINGS.md)) and the anti-noise discipline of
[[anti-noise-orchestration]] (`residue = bias ⊕ noise`), applied one layer below the UI: a
derived number is a **shadow** of the rows that produced it, and it must never claim more
than the **structure** underneath it supports. A reader should leave this section knowing
what "good engine code" means here: **strictness at each authoritative write boundary and honesty
where facts are projected or derived** — the write side protects the artifact, the read side never
invents.

---

## Index

1. [Scope](#scope)
2. [Selection Predicates](#selection-predicates)
3. [Rules](#rules) (EG-1 … EG-8)
4. [Examples](#examples) · [Non-Examples](#non-examples)
5. [Composition](#composition)
6. [Validation](#validation)
7. [Promotion Boundary](#promotion-boundary)
8. [Connections and Falsifiability](#connections-and-falsifiability)
9. [Maintenance](#maintenance)

---

## Scope

The implemented scope today is the high-level audit ledger at
`telemetry/agents/subagents-dispatch.yaml`. The event journal, bus and knowledge store below are
target architecture from [[orchestration-infra]], not claims of shipped code. The constitutional
boundary is nevertheless explicit now so their implementations cannot accidentally turn the audit
ledger into a catch-all store.

| Component | Authoritative for | Logical publisher | Exclusive physical write boundary |
|---|---|---|---|
| bus | no durable fact; publication, routing, visibility and delivery | authorized agents, kernel and human tools | none; the Bus API validates and forwards |
| event journal | accepted runtime events, messages, transitions, attempts, rounds, deliveries and commits | agents for their messages; kernel for lifecycle events | journal writer |
| audit ledger | confirmed dispatch/spec authorization and official terminal outcome | dispatcher/kernel requests | current audit-ledger appender |
| knowledge store | promoted definitions, premises, decisions, claims and typed relationships | agents/humans propose; policy or reviewer promotes | promotion writer/materializer |
| artifact store | immutable large bodies referenced by id/hash | authorized runtime components | artifact service |
| realtime projection | no authoritative fact; reconstructible user-facing view | projection workers | none |

An agent publishing a message is therefore not a second journal writer. It calls the bus contract;
the journal writer durably accepts the event before delivery. Likewise, **only the current appender
writes the audit ledger**, but that exclusivity does not prohibit agents from publishing in-session
messages or knowledge proposals through their authorized APIs.

`dispatch_type` deserves a separate boundary: the closed enum in schema `0.6.1` is a current
implementation fact, not a constitutional invariant. The target is a namespaced, versioned registry
of user-configurable types and recipes. “Strict on write” means resolving and validating against the
active contract; it does not mean that the universe of types must remain embedded in a closed enum.

Applies to:

- every module under `implementations/server/**` (`ledger.py`, `main.py`, `config.py`) — the
  current parse, cache, aggregation and read-endpoint layer,
- `register-dispatch/append-dispatch.cjs` **as the current audit-ledger write contract**,
- `telemetry/agents/subagents-dispatch.yaml` and the pending sheets under
  `telemetry/agents/pending/*.json` **as artifacts** — their integrity, not their UI form,
- future bus acceptance, event-journal, knowledge-promotion and artifact write boundaries when
  [[orchestration-infra]] is implemented.

Does not apply to:

- the *form* of any UI surface (governed by [[frontend-constitution]]),
- the vault's classification system (governed by [[ontology-conventions]]),
- the **semantics/schema** of the dispatch model — what a `dispatch_type`, `group`, or
  typed `connection` *means* (owned by `dispatch-spec` / `register-dispatch`); this
  constitution governs how the engine code *treats* those rows, not what they mean.

## Selection Predicates

Use this constitution when:

- writing or changing any code that parses, caches, aggregates, or serves the ledger,
- adding a new read endpoint or a new derived number to `/api/*`,
- touching the audit appender or a future authoritative store writer,
- the complaint is "a count is wrong / an endpoint 500s / the number doesn't add up."

Do not load this constitution when:

- the change is purely UI form with no effect on what the data *is* (load CONST-FE),
- it is a vault/document classification question (load ontology-conventions),
- it is a proposal to change the dispatch *schema* itself (route to `dispatch-spec`).

---

## Rules

> These rules are stated as **hypotheses, not ratified law.** Each is a `candidate` claim
> carrying two confidence labels from [[ontology-conventions]]: **veracity** (external
> evidence — how tested against reality) and **conviction** (how hard we bet on it). Unlike
> [[frontend-constitution]], most rules here **ratify behavior the code already practices**,
> so their veracity is often `high` — they are close to premises already. Every rule is
> **self-contained**: the claim, its two labels, **what would falsify it**, and its
> validation mode (`deterministic` | `review` | `hybrid` | `none-yet`). When a rule survives
> its falsifier under real use it graduates from hypothesis to **premise** and drops the
> confidence labels.

### EG-1: Scoped Writers — One Validated Physical Write Boundary per Authority

The current **audit ledger** is append-only and owned by
`register-dispatch/append-dispatch.cjs`. **No other code path writes**
`subagents-dispatch.yaml`. New dispatch and close records pass the appender's applicable strict
validator before touching the file; the Python reader NEVER writes
([ledger.py:21](../../implementations/server/ledger.py#L21)).

This exclusivity is scoped to the audit ledger. In the target runtime, agents publish their own
in-session messages and proposals through the bus, while the journal writer performs the physical
event-journal write. Knowledge promotion similarly crosses a promotion writer. A logical publisher
is not a physical store writer, and no writer may claim a fact owned by another store.

- **veracity:** medium — the reader/appender split is real and old, **but** the 2026-07-18
  enum-drift (two close rows that bypassed the validated appender — see [[ledger-enum-drift-finding]])
  is a live counterexample: the invariant is aspired, not yet enforced end-to-end.
- **conviction:** high — this is the integrity spine. A corrupt source poisons every endpoint,
  replay and aggregation downstream; overlapping authority makes conflicts undecidable.
- **Falsified if:** an authoritative store genuinely needs multiple independent physical write
  paths that cannot share one validation/commit boundary, or two stores must own the same canonical
  fact to provide a needed capability.
- **Validation:** `deterministic` — a guard/test asserts no module besides the appender opens
  the audit ledger for write, and the appender rejects records failing the applicable validator.
  Future stores require equivalent contract tests and an authority-overlap review. **Blocked** for
  the current ledger until the drift is traced (see [Promotion Boundary](#promotion-boundary)).

### EG-2: Strict on Write, Lenient on Read

The two sides have opposite jobs and opposite postures. The appender is **strict** — it
refuses to write into a corrupt ledger, *protecting* the file. The reader is **lenient** —
an unreadable row becomes a warning and is skipped; the rest of the ledger is served
([ledger.py:11-19](../../implementations/server/ledger.py#L11-L19)). Never lose a repo's
whole history over one malformed row.

The target generalization preserves the asymmetry per authority: command acceptance and physical
store writes are strict; UI projections and compatibility readers may degrade visibly. Kernel
replay and promotion decisions are not ordinary UI reads: they must fail closed or quarantine bad
records rather than silently skip state required for a decision. This extension is **PENDING** until
those stores exist.

- **veracity:** high — implemented and tested: `parse_ledger` has explicit `strict`/
  `lenient` modes; strict raises `LedgerError` on the first problem, lenient accumulates
  `warnings` and continues.
- **conviction:** high — the asymmetry *is* the design; collapsing either side (lenient write
  or strict read) breaks the artifact or the UI.
- **Falsified if:** leniency on read ever masks a corruption that then propagates downstream —
  a skipped row that should have *blocked* — i.e. the asymmetry hides a fault the strict side
  should have caught at write time.
- **Validation:** `deterministic` — parse a ledger with a broken row: strict raises, lenient
  returns the good rows plus a warning.

### EG-3: A Degraded Row Warns — It Never Crashes an Endpoint

No single malformed row, missing file, or mid-scan deletion may 500 an endpoint or kill the
SSE generator. Defensive reads degrade to a warning or empty-state, never an exception that
reaches the client: non-string `dispatch_id`/`close_of` skipped
([ledger.py:178](../../implementations/server/ledger.py#L178)), `stat` inside the read guard
so a sheet deleted mid-scan does not 500 three endpoints and the stream
([ledger.py:404-411](../../implementations/server/ledger.py#L404-L411)), the daily-series span
cap so one corrupt `1970` date cannot balloon the axis to tens of thousands of buckets.

- **veracity:** high — every one of these guards exists **with a comment naming the exact
  500 it prevents**, several pinned to tests. This rule ratifies observed practice.
- **conviction:** high — one repo's bad row must never darken the whole control plane; the SSE
  generator dying takes every connected UI with it.
- **Falsified if:** swallowing a fault ever hides a real regression that a hard failure would
  have surfaced sooner — resilience buying silence.
- **Validation:** `hybrid` — deterministic (mock a broken row / missing file → endpoint
  returns 200 with a warning, not 500) + review (the degradation is visible, not silent).

### EG-4: Derived Numbers Are Honest — Aggregate Over the Whole Ledger, Never the Window

Every surfaced count is computed over **all** joined rows, not the `limit`-truncated view:
*"a panel saying 181 dispatches but counting only the 40 served would be a silent lie"*
([ledger.py:531-533](../../implementations/server/ledger.py#L531)). Any number the UI shows is
traceable to the rows that produced it, and any set that is **not** a partition is declared,
not implied (live/reserved/legacy do **not** sum to total —
[ledger.py:586-593](../../implementations/server/ledger.py#L586)).

- **veracity:** high — `summarize_repo` reads the whole ledger (`copy=False` over all rows);
  the non-partition caveat is pinned to `test_legacy_live_double_count`.
- **conviction:** high — this is the anti-noise discipline ([[anti-noise-orchestration]]) at the
  data layer: a number that misleads is *bias* the surface injects, exactly the residue this
  repo exists to cancel.
- **Falsified if:** full-ledger aggregation becomes too costly to serve per request **and** a
  windowed count is provably indistinguishable to the user — honesty and performance forced
  apart, with performance winning.
- **Validation:** `deterministic` — `test_overview_totals`: aggregate counts match the full
  row set, not the served window.

### EG-5: Computed Fields Never Shadow Ledger Keys (the `_` Prefix)

On any object that shares a ledger row's namespace, **every field this reader computes carries
a `_` prefix** ([ledger.py:23-30](../../implementations/server/ledger.py#L23)). A real
`status` key exists in pre-v0.5.2 rows; a computed field named `status` would overwrite
historical data. The prefix guarantees a **shadow** (computed) never collides with **structure**
(a real key). Container/aggregate objects that are *not* rows (`summarize_repo`'s `total`,
`open`, `by_type`) are exempt — they have no ledger namespace to protect.

- **veracity:** high — the convention is stated and followed throughout the module.
- **conviction:** medium — load-bearing for row-shaped objects, but a naming discipline, not an
  axis of the system.
- **Falsified if:** a future real ledger key legitimately begins with `_` (the shadow collides
  with structure after all), or the row/aggregate boundary stops being clear enough to apply
  the rule — then it needs re-scoping.
- **Validation:** `review` — each new computed field on a row-shaped object is `_`-prefixed;
  aggregates are exempt. (Promotable to `deterministic` with a static check.)

### EG-6: Backward Compatibility Is Structural — Old Rows Are Artifacts, Never Re-Validated

Rows written under a prior schema are **historical artifacts**: parsed structurally, marked
`_legacy`, and **never re-validated** against the current semantic schema
([ledger.py:9-11](../../implementations/server/ledger.py#L9), `append-dispatch.cjs:61` — "old
keys keep passing"). A schema bump adds forward validation for *new* writes; it never
retroactively invalidates history.

- **veracity:** high — practiced: `_legacy` marking on rows without `groups`, `LIVE_TYPES`
  gating, and the appender explicitly never re-validating old keys.
- **conviction:** high — the ledger *is* the audit trail; rewriting or rejecting history
  destroys the thing it exists to preserve.
- **Falsified if:** a schema change renders old rows genuinely unreadable (not merely legacy)
  such that structural-only parsing yields a *wrong* aggregate — backward tolerance breaking a
  real number rather than preserving one.
- **Validation:** `deterministic` — a fixture of pre-v0.5.2 rows parses, marks `_legacy`, and
  still counts correctly in `summarize_repo`.

### EG-7: Reads Are Deterministic and Idempotent — Content-Keyed Cache, Copy-on-Write

The parse cache is keyed by the file's own **content fingerprint** (`mtime_ns` + size), so a
stale hit is impossible; shared cache values are **never mutated in place** — every writer in
the module reconstructs what it touches, and the list container is privatized per caller
([ledger.py:245-333](../../implementations/server/ledger.py#L245)). Re-reading unchanged input
returns identical output without re-parsing.

- **veracity:** high — the fingerprint + copy-on-write discipline is implemented, with a
  `parse_count` probe that lets a test *prove* the cache hit (not infer it from timing).
- **conviction:** high — determinism is what lets `/api/stream` poll every second without
  re-parsing the largest (~1.5 MB) ledger each tick.
- **Falsified if:** an out-of-band edit preserves the exact size **and** `mtime_ns`
  (fingerprint collision) and serves stale — the content-key assumption breaks.
- **Validation:** `deterministic` — `parse_count` proves a second read of an unchanged ledger
  does not re-parse; mutating a returned list does not corrupt the cache's chronological order.

### EG-8: The Comment Names the Risk and Pins the Caveat — Claim ≤ Proof in Code

Every non-obvious guard states the **exact failure it prevents**; every invariant that does
**not** hold is *declared*, not implied, and **pinned to a test** (the non-partition caveat →
`test_legacy_live_double_count`). "Claim ≤ proof" applies to code the same way it applies to a
hypothesis: a defended behavior names its collapse-test.

- **veracity:** high — the module is uniformly written this way; this rule ratifies observed
  practice rather than proposing it.
- **conviction:** high — it is the repo's whole epistemic ethos (FRAMINGS, OBLIGATIONS: *"named risk,
  not hidden"*) applied to the engine; without it EG-1..EG-7's "Falsified if" lines
  have nowhere to land in the code.
- **Falsified if:** comment density measurably slows change without preventing a proportionate
  share of regressions — documentation as ceremony rather than proof.
- **Validation:** `review` — each new guard names the failure it prevents; each declared
  non-invariant has a pinning test.

---

## Examples

- **EG-1 applied to closing a dispatch:** a close is appended by calling the audit-ledger appender
  with a `close_of` record that passes the applicable close validation — **not** by opening the
  YAML and writing a `close_of:` line by hand. The [[ledger-enum-drift-finding]] is precisely the
  second path happening, which is why EG-1 exists and why its promotion is blocked.
- **EG-1 applied inside a dispatch:** an agent publishes a sealed position through the authorized
  bus API. The journal writer validates and persists the accepted event. This respects EG-1; making
  the agent open the journal directly would violate it.
- **EG-3 applied to a deleted pending sheet:** `read_pending` does its `stat` *inside* the
  try-guard, so a sheet removed between the `glob` and the read degrades to one entry with
  `_error` set — `/api/snapshot`, `/api/overview`, `/api/repo` and the SSE stream all stay up.
- **EG-4 applied to the overview:** `summarize_repo` counts over the whole ledger via
  `load_repo_rows(repo, copy=False)`, while `read_repo` serves only the `limit` most recent —
  two functions, two jobs, and the *count* never comes from the *window*.
- **EG-5 concrete:** the reader adds `_state`, `_legacy`, `_live`, `_close`, `_agent_count` —
  all prefixed — because a bare `state` or `close` could collide with a real historical key;
  but `summarize_repo` returns `open`, `closed`, `by_type` unprefixed, because it is an
  aggregate with no ledger namespace to shadow.

## Non-Examples

- A second script (or an ad-hoc editor keystroke) appending a `close_of:` line straight into
  the audit YAML, skipping the appender and its close validation (violates EG-1 — this is the drift).
- Treating an accepted bus message as both an audit-ledger fact and a knowledge-store fact, with
  either copy independently editable (violates EG-1 by overlapping authority).
- A `/api/overview` count computed from the `limit`-sliced list served to the UI, so "total"
  silently means "last 40" (violates EG-4).
- A reader field named `status` or `close` with no `_` prefix, overwriting a pre-v0.5.2 row's
  real key (violates EG-5).
- A parse that raises on the first malformed row and returns a 500, losing the whole repo's
  history because one line was prettified JSON (violates EG-2/EG-3).
- A migration that rewrites old rows into the new schema "to keep the file clean" (violates
  EG-6 — it destroys the audit trail).

---

## Composition

Precedence (narrowest to broadest):

1. a module-specific constitution pack (if one exists),
2. **this constitution** (artifact-type: engine/backend code),
3. the dispatch schema + `UI-CONTRACT.md` (data/schema — they govern the *what*, not the *how*),
4. the repo's categorical mapping discipline (`PLAN.md` §4).

Conflicts:

- **EG-1 (strict on authoritative write) × EG-3 (lenient UI read):** an apparent tension,
  **reconciled by side** — this is exactly what EG-2 states. Strictness lives at each authoritative
  write boundary; visible degradation belongs to compatibility readers and projections. Kernel
  replay or promotion may instead quarantine/fail closed because it makes decisions from the data.
- **EG-4 (aggregate over the whole ledger) × EG-7 (fast, cached reads):** a real
  cost-vs-honesty tension, **preserved**. Resolution today: EG-7's content-keyed cache is what
  *makes* EG-4 affordable (the whole ledger is parsed once per change, not per request). If
  the ledger grows past what the cache can carry, this conflict routes to a Decision Gate —
  honesty does not yield silently to performance.
- vs. [[frontend-constitution]] at the `UI-CONTRACT.md` seam: CONST-ENG **produces** the data,
  CONST-FE **presents** it. Neither governs the other side of the contract. A dispute about
  what a field *means* is neither's — it routes to `dispatch-spec`.

---

## Validation

Deterministic route (the tests that pin EG-2..EG-7 already exist):

```bash
cd implementations && python -m pytest tests/ -k \
  "overview_totals or snapshot_shape or repo_errors or legacy_live_double_count or parse"
```

Missing validators (block promotion of the rules they cover):

- **EG-1:** no guard yet asserts the audit appender is the *sole* audit-ledger writer, and the drift
  that motivated the rule is not yet traced. Journal/knowledge writer guards remain PENDING because
  those stores are target architecture. This is the one rule with a live current counterexample.
- **EG-8:** `review`-only — no automated check that a guard names its failure or that a caveat
  is pinned.

---

## Promotion Boundary

Required before canonical status:

- **Trace the drift.** EG-1 cannot promote until the [[ledger-enum-drift-finding]] is
  investigated: *how* did two close rows reach the file without the audit appender's close
  validation? The answer either yields the scoped audit-writer guard (and EG-1's current-scope
  veracity rises to `high`) or reveals a legitimate competing path (and EG-1 is amended, not
  promoted). This is the pre-condition the memory already flags for Phase 2.
- **EG-8 gets at least a lint-level check** (or is accepted as permanently `review`),
- the `deterministic` rules (EG-2, EG-4, EG-6, EG-7) are green in CI, not just locally,
- **collapse-test:** if "honest number" and "affordable read" (EG-4 × EG-7) turn out to be
  genuinely incompatible at real ledger sizes, EG-4 is re-scoped through a Decision Gate rather
  than silently traded away.

---

## Connections and Falsifiability

This constitution **ratifies practice the engine already earned** and must stay falsifiable
with it. Per the repo's model (`vault/hypothesis/` holds falsifiable theses; a constitution
ratifies rules a thesis — or, here, working code — has earned), the rules and their code are
linked and share collapse-tests.

| Document | Relationship | Description |
|---|---|---|
| [agents-communication-infra discovery](../../docs/features/agents-communication-infra/discovery/agents-communication-infra.md) | `governs` | Applies EG-1/EG-6 to the proposed journal-to-audit materialization seam while preserving the live drift caveat. |
| [ledger.py](../../implementations/server/ledger.py) | `implements` | The module that already practices EG-2..EG-8; this constitution reads its earned discipline back out as law. |
| `register-dispatch/append-dispatch.cjs` | `implements` | The strict validated appender — the write contract EG-1/EG-6 defend. |
| [[ledger-enum-drift-finding]] | `grounds` | The audit (2026-07-18 close rows bypassing the appender) that motivates EG-1 and blocks its promotion. |
| [[orchestration-infra]] | `proposes-target` | Defines the bus, journal, audit-ledger and knowledge-store authority split that EG-1 generalizes without claiming it is implemented. |
| [[ontology-conventions]] | `governed-by` | Defines the `veracity`/`conviction` labels and the hypothesis → premise arc each rule carries; EG-5 is its orthogonality principle applied to *code fields* (a shadow that must not collide with structure). |
| [[frontend-constitution]] | `sibling` | Governs the *form* of the data this engine produces; they meet at `UI-CONTRACT.md` and neither crosses the seam. |
| [FRAMINGS.md F1](../../FRAMINGS.md) (`residue = shadow ⊕ structure`) | `grounded-in` | EG-4 (derived number ≤ its rows) and EG-5 (computed ≠ real key) are this lever applied to the data layer. |
| [[anti-noise-orchestration]] (HYP-ORCH-NOISE) | `sibling` | EG-4 is the anti-noise thesis (`residue = bias ⊕ noise`) enforced at the point numbers are derived. |
| `OBLIGATIONS.md` | `contextualizes` | Shares the "name the collapse-test, hide no risk" discipline EG-8 makes a rule. |

**Falsifiability (collapse-tests for the constitution itself):**

- If the drift trace shows the audit ledger cannot have one physical write boundary without losing
  a needed operation, EG-1 collapses to a weaker coordination rule and is amended, not retired.
- If journal, audit ledger and knowledge store require overlapping canonical ownership rather than
  references and projections, the scoped-authority generalization of EG-1 is false.
- If EG-4 and EG-7 prove incompatible at real scale (honest counts unaffordable), the "honest
  derived number" property this constitution is built on is only partially reachable, and the
  Objective is re-scoped.
- If the engine migrates off the append-only YAML ledger to a database, EG-2/EG-7 (written for
  file parsing + a file-fingerprint cache) are rewritten or retired; the invariants that
  survive the migration are EG-1 (one validated write boundary per authority), EG-4 (honest
  aggregates), and EG-6 (history is never re-validated).

---

## Maintenance

Split trigger:

- if the aggregation layer (`summarize_repo`, `daily_series`, and successors) accumulates
  enough rules of its own, extract a narrower `CONST-ENG-AGG`.

Retirement trigger:

- if the audit ledger moves from append-only YAML to a transactional store, the file-shaped rules
  (EG-2, EG-7) are rewritten; the integrity/honesty invariants (EG-1, EG-4, EG-6) carry over.
