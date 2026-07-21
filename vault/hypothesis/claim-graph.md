---
tags: [vault, ontology, claim-graph, assertion-typing, residue, category-theory, anti-noise]
node_type: premise
is_session: false
session_ref: null
layer: ontology, domain
nature: explanatory, technical
status: exploratory
veracity: low
conviction: medium
version: 0.2.0
last_updated: 2026-07-20
---

# HYP-CLAIM-GRAPH — typing at the granularity of the assertion

> **Status:** `exploratory`, unreviewed — a *candidate* thesis (informal sense) in the
> [[ontology-conventions]] arc (`premise` → law); the enum status is `exploratory`. This is a
> **falsifiable thesis**, not a result. `Claim ≤ proof`: everything below is a bet with a
> collapse-test, including the claim that this layer is worth its annotation cost. Grounded by
> [[axioms]] AX-2 (the scientific method it mechanizes).
>
> **Revised 2026-07-20** after tensioned review (`2026-07-20-review-claim-graph-axioms`): the
> body was downgraded from asserted identities to candidate mappings; the "dual of H-PORT-6" and
> "three faces meet" claims are now explicitly conditional on OBL-E3 + BET-DECOMP-CHEAP +
> BET-THALER; BET-VERACITY-PROP was reconciled with BET-√N.

## The thesis, in one line

> **The edge catalog the vault already runs at the document level — `contradicts`,
> `derives-from`/`grounds`, `refines` ([[ontology-conventions]] Appendix C) — is pushed one
> granularity *down*, to the atomic assertion: `this-is-a-premise-of`, `this-contradicts-that`,
> `this-is-a-corollary-of`, `these-are-the-premises-of-this-conclusion` — each edge and each
> assertion falsifiable.**

It would complete a **tower of typing**, coarse → fine:

`domain-object` (the system language in the sibling `domainspec-*` repos — external) ⊃
`document-node` ([[ontology-conventions]], here) ⊃ **`assertion`** (this thesis). The two upper
strata are already in place as materialized artifacts (the conventions here; the domainspec
system-language in the sibling repos); this thesis types the floor.

## The two halves — one machine

**Schema (this node).** The type system of the atomic claim: what an assertion *is* (premise,
corollary, conclusion, contradiction-bearer) and the typed edges between assertions.

**Ingestion — the decompositor.** How the graph gets *populated*: take an arbitrary user
process/skill and **decompose it into its main decision points**, then type them into the
grammar. Two faces of one machine — ingestion ↔ schema.

- **Type-theoretic (conditional).** The decompositor is a functor in the **opposite direction**
  to [`README.md` H-PORT-6](../../README.md): *into* `ORCH`, where H-PORT-6 is a functor
  *leaving* it. This is **not** a categorical dual — opposite-direction functors sharing `ORCH`
  as codomain vs domain are not duals, and calling it one would be exactly the loose CT the repo
  polices. The "`ORCH` as a hub with functors in and out" picture holds **only if** ingestion is
  generic (BET-DECOMP-CHEAP) **and** `ORCH` is a category (OBL-E3, **OPEN**). Note:
  categoricity ≠ domain-independence, so the functor framing does not by itself buy genericity.
- **It is a verb** ([DEF-ORCH-005](../../definitions/DEFINITIONS.md)) — morphism + the condition
  under which it preserves symmetry. Outside that condition it **generates residue**: decomposing
  loses structure, and the loss is **measurable per-verb**. This is the **expensive, unverified**
  part — the analogue of the canonicalization surface in the permguard brief
  (`../../research/permguard-kernel/`): the part that *does* the work is the part not yet proven.

## Why it matters — where the three faces *would* meet

The claim-graph is the candidate **atomic layer where the repo's three faces would stop being
juxtaposed** — **if** the categorical face discharges OBL-E3-one-floor-down and the engineering
face survives BET-THALER. Today one is an open obligation and one is a relabel under test, so the
meeting is **proposed, not achieved**:

| Face | What the claim-graph would make of it |
|---|---|
| **Epistemology (AX-2 / T0)** | `claim ≤ proof` becomes *mechanical*: a **veracity-propagation rule along `premise-of` edges** (BET-VERACITY-PROP). And `contradicts` **maps to** the F6 anomaly ([FRAMINGS.md F6](../../FRAMINGS.md)) — a candidate instance, not an identity: F6's anomaly is a fully-faithful-failure, `contradicts` is logical incompatibility of two assertions; structurally analogous. |
| **Formal type (categorical)** | assertions = objects, entailment = morphism, `premise → conclusion` = composition. It **poses OBL-E3 one floor down** ([OBLIGATIONS.md](../../OBLIGATIONS.md), OPEN): do these edges **compose associatively**? Is `contradicts` a morphism, or a 2-cell / obstruction outside the 1-skeleton? Open questions, not a meeting-point yet. |
| **Engineering (Thaler)** | the mechanism that **captures** assertions along a session, propagates veracity, and **surfaces contradictions / pending decisions to the human gate** = choice architecture. The "definitions taken along the session that wait for the user's approval" are a **candidate realization** of the claim-graph built live — exactly the relabel [[anti-noise-orchestration]]'s `BET-THALER` holds under test (mostly-a-relabel until a decision moves). |

## Collapse-tests (what falsifies this thesis)

- **CT1 — the typing is noise, not structure.** If two independent runs (or annotators) cannot
  agree on the **type of an assertion** or the **type of an edge** (`contradicts` vs `refines` vs
  `special-case-of`) **above chance**, the granular layer measures noise, not structure. This is
  the repo's *own* noise metric turned on itself (self-application, AX-3) — the same
  inter-tagger-agreement problem as [[orchestration-infra]] Open-question 4.
- **CT2 — annotation cost kills ingestion.** If populating the graph needs **manual
  per-assertion annotation** (see BET-DECOMP-CHEAP threshold), the decompositor is a hand-built
  adapter *per process*, not generic ingestion. The coupling is via the decompositor's own
  genericity — **not** via H-PORT-6 (README: H-PORT-1..5 don't depend on H-PORT-6). What falls is
  the *ingestion* leg: onboarding an arbitrary process cheaply.
- **CT3 — reliable but inert edges (distinct from CT1).** Even if edge-types agree *above chance*
  (CT1 passes), if the edges **never flag a contradiction/anomaly that changes a decision**, the
  edge layer is decoration — reproducible yet inert. This is the F6 worry that a discriminating
  signal is re-expressible noise, not a new separator. (CT1 tests *agreement*; CT3 tests
  *downstream bite* — orthogonal targets.)

## Registered bets

- **BET-CLAIM-TYPES** (`veracity: low`, `conviction: medium`): assertion-type and edge-type are
  assignable **above chance** by independent runs. **Falsifier:** CT1.
- **BET-DECOMP-CHEAP** (`veracity: low`, `conviction: medium`): the decompositor populates the
  graph from an **arbitrary skill/process in the existing skills library** without per-process
  wiring. **Falsifier (binary):** ≥1 such skill requires hand-built per-process wiring, or manual
  annotation on more than a pre-committed fraction of its assertions. (Note: "arbitrary" is scoped
  to the skills library, not literally any process, to avoid a straw target.)
- **BET-VERACITY-PROP** (`veracity: low`, `conviction: medium`): `claim ≤ proof` is a
  **computable propagation** — a claim's veracity ≤ the **aggregate evidence** of its `premise-of`
  parents, where **independent** parents *aggregate upward*: a conclusion drawn from N independent
  low-veracity premises may legitimately outrank any single one (this is the sanctioned `BET-√N`
  route in [[anti-noise-orchestration]], **not** a violation of `claim ≤ proof` — the aggregate
  evidence is genuinely larger). **Falsifier:** a well-formed graph admits a conclusion whose
  veracity exceeds the **aggregate** of its premises (not merely an individual premise).
  **Reconciliation:** an earlier wording "≤ its premises" (read per-individual) contradicted
  BET-√N; corrected here to the aggregate, with independence aggregating upward.

## Open questions

1. Is the decompositor's output a **dispatch** (typed by `dispatch_type`) or a **verb** (a
   morphism)? The *input process* is verb-shaped; the *output* may be a dispatch. Do not conflate.
2. Does `contradicts` compose? (The OBL-E3-one-floor-down question — probably a 2-cell.)
3. Who runs the decompositor — a skill, an LLM pass, a human-in-the-loop? Ties BET-DECOMP-CHEAP.
4. What is the pre-committed operational definition of a "well-formed" claim graph (BET-VERACITY-PROP)?

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[ontology-conventions]] | `derives-from` | Pushes its document-level edge catalog (Appendix C) down to the assertion. The schema is the same, one granularity finer. |
| [[axioms]] | `grounds` | AX-2 (scientific method) is what the claim-graph mechanizes; AX-1's "best way" is what a cheap decompositor would serve. |
| [`OBLIGATIONS.md`](../../OBLIGATIONS.md) | `refines` | OBL-E3 (is `ORCH` a category?) posed one floor down, on assertions/entailment. |
| [`README.md` H-PORT-6](../../README.md) | `contextualizes` | The decompositor is the *opposite functor direction* (into `ORCH`) — conditional on OBL-E3 + BET-DECOMP-CHEAP; not a categorical dual and not a discarded alternative. |
| [[anti-noise-orchestration]] | `depends-on` | Supplies the noise metric CT1 uses, the Thaler/choice-architecture face (BET-THALER), and the BET-√N aggregation BET-VERACITY-PROP reconciles with. |
| [`definitions/DEFINITIONS.md`](../../definitions/DEFINITIONS.md) | `depends-on` | DEF-ORCH-005 (verb + residue) types the decompositor; DEF-ORCH-004 (probe) types the edges. |
