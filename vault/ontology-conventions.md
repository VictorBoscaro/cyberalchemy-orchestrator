---
tags: [vault, ontology]
node_type: constitution
is_session: false
layer: ontology
nature: reference
status: active
version: 1.1.0
last_updated: 2026-07-21
---

# Vault Conventions

> Rules every node in the vault must follow. This is the vault's internal
> constitution — what determines quality, not just format.
>
> Ported and adapted from ZefraHub's `ontology-conventions.md` (v1.4.0). The
> classification system, the two confidence dimensions, and the orthogonality
> principle are kept intact; ZefraHub domain specifics (FIDC/CCB tags, `house_project`
> paths, companion docs not yet in this vault) were re-grounded to this repo.

---

## Objective

This document defines the **classification system** of the vault — an **adaptive**
system designed to **reduce the entropy of the knowledge base** by enforcing
orthogonal labeling.

The core objective is: every classification label should be **statistically
independent** from every other label. When labels are orthogonal, each contributes
maximum unique information and zero redundancy. Adding a label that correlates with
existing labels increases noise without increasing knowledge; removing a label that was
truly independent destroys information no other label can recover. (See
[Appendix A](#appendix-a-mathematical-foundation) for the formal framework.)

This is the same lever the rest of the repo runs on: `residue = shadow ⊕ structure`
([FRAMINGS.md F1](../FRAMINGS.md)) and entropy as log-cardinality. A redundant label is
a shadow that adds no structure.

The system is **not static**. As the vault grows, labels may be added, merged, split, or
retired. The only invariant is the orthogonality constraint: every label must earn its
place by contributing information no other label provides. This makes the ontology
self-correcting — redundant labels are detected and eliminated, and missing dimensions
are surfaced when existing labels fail to disambiguate nodes.

---

## Index

1. [Required Frontmatter](#required-frontmatter)
2. [`node_type` — Epistemic Role](#node_type--epistemic-role)
3. [`layer` — System Scope](#layer--system-scope)
4. [`nature` — Document Format](#nature--document-format)
5. [`status` — Maturity Level](#status--maturity-level)
6. [`veracity` and `conviction` — The Two Dimensions of Confidence](#veracity-and-conviction--the-two-dimensions-of-confidence)
7. [`tags` — Domain Keywords](#tags--domain-keywords)
8. [Edge Types (Connections Section)](#edge-types-connections-section)
9. [The Orthogonality Principle](#the-orthogonality-principle)
10. [Appendix A: Mathematical Foundation](#appendix-a-mathematical-foundation)
11. [Appendix B: Label Value Catalog](#appendix-b-label-value-catalog)
12. [Appendix C: Edge Type Catalog](#appendix-c-edge-type-catalog)
13. [Appendix D: Quick Reference — The 7 Labels](#appendix-d-quick-reference--the-7-labels)

---

## Required Frontmatter

```yaml
---
tags: [list of topical tags]           # Domain/topic labels only — see Tag System
node_type: axiom | premise | constitution | discovery | implementation-plan | spec | audit | conceptual | essay | test | backlog | readme
is_session: true | false               # Is this a conversation/session record?
session_ref: <session-id> | null       # Optional — the session that produced this document
layer: ontology | architecture | domain | application | external  # Multi-value allowed
nature: explanatory | procedural | reference | technical          # Multi-value allowed
status: draft | exploratory | active | consolidated | evergreen
veracity: high | medium | low        # Belief nodes only (see applicability)
conviction: high | medium | low         # Belief nodes only (see applicability)
version: 0.x.x
last_updated: YYYY-MM-DD
private: true                            # Optional — do-not-publish flag (see below); omitted = publishable
---
```

> **The optional `private` key.** A boolean do-not-publish flag. Omitted (the default) means
> publishable. It is **orthogonal to the 7 epistemic labels** — publishability is independent of
> role, layer, nature, maturity, evidence, commitment, and topic (a `veracity: high` node can be
> private; a `veracity: low` node can be public) — so it passes the Level-1 admission test and
> earns its place. Use it for **private proof targets**: nodes excluded from
> `publication-research-pipeline`, `reading-learning-package`, the README, and the essays, even if
> discharged. First consumer: [[framework-self-similarity]].

---

## `node_type` — Epistemic Role

### What it is

`node_type` classifies **what role this document plays** in the knowledge graph — what
kind of claim it makes and how it participates. The role is intrinsic and does not change
with maturity: an axiom stays an axiom whether it's `draft` or `evergreen`. Trust levels
are captured by `status`, `veracity`, and `conviction`.

The clearest way to assign `node_type` is to ask: *"If someone challenges this document,
what is the right response?"*

| node_type | Challenge response |
| --- | --- |
| `axiom` | "That's foundational — revisiting it breaks everything built on it" |
| `premise` | "Show me evidence and we'll update it" |
| `constitution` | "Change it through governance, not informally" |
| `discovery` | "It's exploration — enrich it or supersede it with a decision" |
| `implementation-plan` | "Follow it, update it if scope changed, or supersede it with a new plan" |
| `spec` | "Update it if the code changed" |
| `audit` | "Run the audit again and see if the findings still hold" |
| `conceptual` | "It's context — you can enrich or correct it" |
| `essay` | "It's a committed argument from experience — engage with the reasoning or counter it" |
| `test` | "Run the tests and see if they pass" |
| `backlog` | "Prioritize it, schedule it, or close it — it tracks pending work" |
| `readme` | "Update it to reflect what's actually in the directory" |

### Why it matters

This is the most important label. It determines **how the document participates in the
knowledge graph**. An axiom anchors the graph — everything derives from it. A premise is
a branch that might be pruned. A constitution is a law that governs behavior. Without
`node_type`, every document looks equally authoritative.

### How it differs from `status` and `conviction`

- **`node_type`** measures the **role** — what kind of claim it makes. It almost never
  changes. An axiom stays an axiom; a spec stays a spec.
- **`status`** measures the **maturity** — how much it's been reviewed and tested. It
  changes frequently, from `draft` toward `evergreen`.
- **`conviction`** measures the **bet** — how committed the team is. It shifts as strategy
  shifts. A premise can go from `high` to `low` conviction.

> **The hypothesis → premise → law arc (this repo's extension).** A `candidate` framing
> in `vault/hypothesis/` is a falsifiable thesis (`node_type: premise`, low veracity). A
> `constitution` ratifies the rules a thesis has earned. In this repo we go one step
> finer: **each rule inside a candidate constitution is itself a hypothesis** — it states a
> claim and what would falsify it, and carries its own confidence labels — until it
> survives its falsifier under real use and is promoted to a premise. See
> [[frontend-constitution]] for the worked pattern.

---

## `layer` — System Scope

### What it is

`layer` classifies **what part of the system** the document concerns. It is a topical
scope — not an epistemic level, not a format.

### Why it matters

Without `layer`, an agent searching for "all architecture rules" would have to read every
document's content. With `layer: architecture`, it's a single filter. This is the primary
filter for narrowing scope.

### How it differs from `node_type`

`node_type` and `layer` are independent axes. An axiom can be about the ontology or the
application. A constitution can be about architecture or the ontology. Knowing one tells
you nothing about the other.

### Multi-value layer

A document **may belong to more than one layer** (e.g., `layer: architecture, ontology`).
Use multi-value when a document genuinely spans scopes. **Do not** use a special value to
indicate multi-layer documents — just list the layers.

The five `layer` values for this repo — `ontology`, `architecture`, `domain`,
`application`, `external` — each scope a different part of the system. (`external`
replaces ZefraHub's `market`: outside context — references, prior art, upstream repos —
rarely load-bearing here.) For full definitions, see
[Appendix B](#appendix-b-label-value-catalog).

---

## `nature` — Document Format

### What it is

`nature` classifies the **structural format** — if you printed it, what would it look
like? A numbered checklist? A prose essay? A lookup table? A schema? This is about the
*shape* of the text, not what it says or how trustworthy it is.

### Why it matters

`nature` is primarily a **reading instruction for agents**. An agent looking for "how to
do X" needs a `procedural` document; one looking for "what a term means" needs a
`reference` document. Without `nature`, the agent must read the content to learn how to
consume it.

`nature` has **lower independent entropy** than the other labels — knowing a document is
`node_type: constitution` makes `procedural`/`technical` more likely. This correlation is
acceptable because `nature` still captures format variation no other label expresses: a
constitution can be prose (`explanatory`) or a rule table (`reference`), and that changes
how an agent should read it.

The four `nature` values — `explanatory`, `procedural`, `reference`, `technical` — each
describe a different structural format. Multi-value is allowed. See
[Appendix B](#appendix-b-label-value-catalog).

---

## `status` — Maturity Level

### What it is

`status` classifies **how mature and trusted** a document is: `draft` → `exploratory` →
`active` → `consolidated` → `evergreen`.

### How it differs from `node_type`

`node_type` is the **category** (what kind of knowledge). `status` is the **maturity**
(how much it's been tested). They are independent: a `premise` can be `draft` or
`consolidated`; an `axiom` can be `draft` or `evergreen`.

Each status level has precise **entry and exit criteria**. See
[Appendix B](#appendix-b-label-value-catalog).

> **The hard boundary:** A higher-level document can NOT reference a lower-level document
> as a source of truth. A `consolidated` constitution may cite a `draft` session as
> "context", but it cannot derive its authority from it.

---

## `veracity` and `conviction` — The Two Dimensions of Confidence

Every belief document (and, in this repo, every candidate **rule**) can be labeled with
two confidence metrics: **veracity** (evidence) and **conviction** (commitment).

### Why two dimensions?

A single "confidence" metric is ambiguous: does "low confidence" mean *we don't have
data* or *we aren't betting on it*? These are different situations that require different
responses. Orthogonality eliminates the ambiguity.

### The difference between them

**Veracity** measures how much the world confirms this — external evidence, determined
by reality (data, tests, production results). It changes through evidence. Low = "we
haven't tested this yet." High = "this has been tested and confirmed."

**Conviction** measures how hard the team is betting on this — internal posture,
determined by the team (strategy, priorities, resource allocation). It changes through
decisions. Low = "we aren't committing resources." High = "we are building around this."

### The 2×2 Matrix

- `veracity:low` + `conviction:high` → **A Strategic Bet.** Building around it before it's proven.
- `veracity:high` + `conviction:low` → **An Ignored Fact.** Established, but we don't act on it.
- `veracity:high` + `conviction:high` → **A Consolidated Law.** Proven and actively driving design.
- `veracity:low` + `conviction:low` → **A Loose Thread.** Untested, nobody acting on it. Record, don't build on.

### Applicability

These dimensions are meaningful for `axiom`, `premise`, `discovery`, and `audit` — node
types that make a claim, bet, or evaluative judgment. For `implementation-plan`, `spec`,
`conceptual`, and `test`, they are **omitted** (maturity is `status`; evidence is
observable, not estimated).

> **This repo's extension for `constitution`.** ZefraHub omits these fields for
> constitutions (a constitution is ratified or not — that's `status`). Here, while a
> constitution is `candidate`/unreviewed, **each of its rules is treated as a falsifiable
> hypothesis** and carries `veracity`/`conviction` **inline, per rule** — because a
> candidate rule is a claim before it is law. The document-level constitution still omits
> the fields; only the rules carry them, and they drop away when a rule is promoted to a
> premise and the constitution is ratified. See [[frontend-constitution]].

For per-value operational criteria and criteria by `node_type`, see
[Appendix B](#appendix-b-label-value-catalog).

---

## `tags` — Domain Keywords

Tags are **topical/domain labels only**. Epistemic role is `node_type`; maturity is
`status`. Do not duplicate either as a tag. Tags answer *"what domain does this touch?"*
and drive graph filtering with no epistemic weight.

### Domain (this repo)
`#orchestration` `#agents` `#dispatch` `#anti-bias` `#anti-noise` `#residue` `#category-theory`

### Technical
`#architecture` `#ui` `#ledger` `#skills` `#ontology`

### Vault
`#vault`

---

## Edge Types (Connections Section)

Declare relationships in the `## Connections` section of each document:

```markdown
| Document | Type | Description |
|----------|------|-------------|
| `other.md` | `resolves` | description of the relationship |
```

### Directionality Principle

Edges can be **bidirectional** to maximize explicit information (a child declaring
`derives-from` parent, and the parent declaring `grounds` child). A visualization or query
layer must **deduplicate** these — `derives-from → B` and `B grounds → A` are the same
edge.

For the full catalog of 14 edge types, see [Appendix C](#appendix-c-edge-type-catalog).

> `contradicts` is the most valuable edge type: it flags inconsistencies that must be
> resolved before a document moves up a level. Its **absence does not mean the vault is
> contradiction-free** — only that none have been formally identified.

> `validates` is the mechanism for a document to increase its `veracity` over time.

---

## The Orthogonality Principle

> **A new label or node should only be created if it adds orthogonal information to what
> already exists.**

This is the single governing constraint of the ontology. Two signals are orthogonal when
their **mutual information is zero** — knowing one tells you nothing about the other. A
redundant signal increases description length without increasing knowledge. It applies at
two levels:

### Level 1: Labels

The 7 labels (`node_type`, `layer`, `nature`, `status`, `veracity`, `conviction`,
`tags`) are designed so that **knowing one gives no information about another.**

> **Admission question for a new label:** *"Can I predict this label's value from the
> existing labels? If yes, it is redundant. If no, it carries unique information and
> should exist."*

### Level 2: Nodes

> **Admission question for a new node:** *"If I remove this document, is any information
> lost that cannot be recovered from the others?"*

**Corollaries:** two documents with high semantic overlap should be **merged** or one
becomes a **reference** of the other; an index (like a README) does not violate this — its
function (navigation) is orthogonal to the content it indexes; a *how-to* is orthogonal to
a *why* even on the same topic.

---

## Appendix A: Mathematical Foundation

Let the system have *n* labels **L₁ … Lₙ** (currently *n = 7*). Each is a discrete random
variable over a finite set. Shannon entropy of one label:

```
H(Lᵢ) = − Σ p(x) · log₂ p(x)
```

Two labels are orthogonal iff their **mutual information** is zero:

```
I(Lᵢ ; Lⱼ) = H(Lᵢ) + H(Lⱼ) − H(Lᵢ, Lⱼ) = 0
```

When orthogonality holds for **all pairs**, total capacity is maximized:

```
H(L₁, …, Lₙ) = H(L₁) + … + H(Lₙ)     (maximum, no waste)
```

Otherwise the joint entropy is strictly less — the system wastes capacity on redundancy.

**Admission test for a new label** `Lₙ₊₁`, net contribution
`ΔH = H(Lₙ₊₁) − I(Lₙ₊₁ ; L₁ … Lₙ)`:

- `ΔH ≈ H(Lₙ₊₁)` → fully orthogonal. **Add it.**
- `ΔH ≈ 0` → predictable from existing labels. **Redundant.**
- `0 < ΔH < H(Lₙ₊₁)` → partial overlap. Judge whether the unique portion justifies the cost.

This is the same "shadow vs structure" decategorification wall as [FRAMINGS.md F1/F2](../FRAMINGS.md):
a scalar that adds no separating power is a shadow the codomain already sees.

---

## Appendix B: Label Value Catalog

### `node_type` Values

The test: *"If someone challenges this, what is the right response?"*

| node_type | Definition | Example (this repo) |
| --- | --- | --- |
| `axiom` | Foundational commitment taken as given. Revising it forces rethinking everything built on it. | `PLAN.md` §1 (A6 "framework as its own instance") |
| `premise` | Working bet — an informed hypothesis that guides decisions but may be disproven. Carries confidence labels. | [[anti-noise-orchestration]] (HYP-ORCH-NOISE) |
| `constitution` | An enforceable rule set, formally ratified. Versioned, amended through governance. | [[frontend-constitution]] (CONST-FE) |
| `discovery` | Exploratory mapping of a possibility space; investigates options without prescribing. | UI prior-art recon (2026-07-20 research dispatch) |
| `implementation-plan` | Actionable roadmap with phases, dependencies, success criteria. | `PLAN.md` phase/E-item breakdown |
| `spec` | Behavioral description kept in sync with code. | `implementations/UI-CONTRACT.md` |
| `audit` | Evaluative assessment of current state against rules/quality standards. | ledger enum-drift finding (2026-07-18 close rows) |
| `conceptual` | Explanatory context that grounds understanding without prescribing behavior. | `README.md`, `FRAMINGS.md` |
| `essay` | A committed argument from lived experience; authorial voice is part of the meaning. | `docs/essays/anti-noise-orchestrator/README.md` |
| `test` | A record of executable validation; generates evidence that raises `veracity`. | `implementations/tests/` runs |
| `backlog` | Prioritized pending work / open questions awaiting scheduling. | Next-Step lists in session notes |
| `readme` | Reflects what's actually in a directory. | any `README.md` |

### `layer` Values

| layer | What it scopes |
| --- | --- |
| `ontology` | The vault itself — its schema, rules, navigation, classification (this document). |
| `architecture` | System-level structure and constitutions about how the repo is organized. |
| `domain` | Internal domain logic — the dispatch model, anti-bias/anti-noise disciplines, the residue calculus. |
| `application` | Application concerns — the control-plane UI, endpoints, workflows. |
| `external` | Outside context — prior art, upstream repos (e.g. ZefraHub), references. Rarely load-bearing. |

### `nature` Values

| nature | Shape | Reader behavior |
| --- | --- | --- |
| `explanatory` | Prose — reasoning and context. | Reads linearly, absorbs the *why*. |
| `procedural` | Numbered steps, checklists. | Follows instructions in order. |
| `reference` | Tables, catalogs, dictionaries. | Searches for a specific item. |
| `technical` | Schemas, code patterns, diagrams. | Inspects structure, not prose. |

### `status` Entry and Exit Criteria

| Status | Entry criteria | Exit criteria (to promote) |
| --- | --- | --- |
| **draft** | Document exists. Anyone can create. | Minimal structure, defined topic, ≥1 link to an existing concept. |
| **exploratory** | Complete frontmatter; ≥1 link; status + confidence labels set. | Discussed in a session; not contradicted by code or hard evidence. |
| **active** | Does not contradict any `evergreen`/`consolidated` doc; aligned with code (or deviation documented). | Reviewed against real system state; survived without contradiction. |
| **consolidated** | Version ≥ 1.0; no open `contradicts` edges; referenced by ≥2 lower-level docs. | Formal review confirms it; no open controversy. |
| **evergreen** | Approved by formal review; no known contradictions; tested against multiple real scenarios. | Only leaves by documented refutation + formal review — **never by abandonment.** |

### `veracity` (evidence) — Operational Criteria

| Value | Criteria |
| --- | --- |
| **high** | Tested against reality: data confirms it, experiments validate it, or it matches authoritative sources. Point to concrete evidence. |
| **medium** | Derived from established principles/industry patterns, but not yet tested in *this* system. Reasonable extrapolation. |
| **low** | Untested hypothesis, projection, or interpretation. Only a plausible argument. |

### `conviction` (commitment) — Operational Criteria

| Value | Criteria |
| --- | --- |
| **high** | Actively drives real decisions (architecture, priorities). If wrong, we'd undo significant work. |
| **medium** | Influences decisions but doesn't block them. We'd adjust course if disproven, without a rewrite. |
| **low** | Exploration, no firm position. Noted, not acted on. |

### `veracity` Criteria by `node_type` (selected)

| node_type | `veracity: high` means | `veracity: low` means |
| --- | --- | --- |
| **axiom** | Well-established principle in the field | Novel assumption, no external validation |
| **premise** | Hypothesis tested in production or backed by data | Untested working bet |
| **constitution** (per-rule, this repo) | Rule followed for weeks/months; violations caught and corrected | Brand new; not yet tested in practice |
| **discovery** | Options thoroughly researched with data/PoCs | Quick brainstorm without evidence |
| **spec** | Description matches current code exactly | Code has drifted from the spec |
| **audit** | Findings verified against current code; issues reproduced | Based on stale code or incomplete review |

---

## Appendix C: Edge Type Catalog

| Type | Direction (A → B means…) | When to use |
| --- | --- | --- |
| `resolves` | A offers a solution to the problem stated in B | A is a resolution or answer |
| `derives-from` | A was motivated by, built upon, or generated by B | The canonical parent→child chain |
| `grounds` | A is the foundation B is built upon | Theoretical inverse of `derives-from` |
| `implements` | A is the concrete implementation of B | B is a spec/constitution; A is code or a concrete doc |
| `validates` | A provides evidence or tests that prove B | Increases B's `veracity` |
| `promotes-from` | A is a ratification of the thesis stated in B | Constitution ← hypothesis (this repo's arc) |
| `exemplifies` | A is a concrete example of B | B is abstract; A is an instance |
| `refines` | A is a more detailed version of B | Incremental depth, same topic |
| `contextualizes` | A provides purely informational background for B | No functional dependency |
| `depends-on` | A does not function without B | Stronger than `derives-from`: runtime dependency |
| `alternative-to` | A is a competing/discarded alternative to B | Design decision not taken |
| `contradicts` | A is in tension with or refutes B ⚠️ | Flags inconsistency — resolve before promotion |
| `supersedes` | A is the direct successor of B, making B obsolete | Major version succession |
| `deprecates` | A replaces B informally/partially | Soft retirement |

---

## Appendix D: Quick Reference — The 7 Labels

| Label | Question | What it captures | Independent of |
| --- | --- | --- | --- |
| **`node_type`** | *What role does this document play?* | Kind of claim: axiom, premise, constitution, discovery, plan, spec, audit, conceptual, essay, test, backlog | All others |
| **`layer`** | *What part of the system does it concern?* | Scope: ontology, architecture, domain, application, external | `node_type`, `nature` |
| **`nature`** | *What structural format does it use?* | Reading instruction: prose, steps, table, schema | `node_type`, `layer` |
| **`status`** | *How mature/trusted is it?* | Lifecycle: draft → … → evergreen | `node_type`, `nature` |
| **`veracity`** | *How much evidence backs it?* | External evidence: how tested against reality | `conviction` |
| **`conviction`** | *How hard are we betting on it?* | Internal commitment: how much it drives decisions | `veracity` |
| **`tags`** | *What specific topics does it touch?* | Domain keywords | All others |

> **Why not fewer labels?** Merging `node_type` and `status` would lose "an axiom in
> draft" vs "a premise that's consolidated." Merging `veracity` and `conviction` would
> lose "a strategic bet" vs "an ignored fact." Each label captures information no other
> can express.

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [[frontend-constitution]] | `exemplifies` | First constitution whose rules carry per-rule `veracity`/`conviction` + inline falsifiability. |
| [[anti-noise-orchestration]] | `contextualizes` | Anti-noise thesis; its `residue = bias ⊕ noise` shares the entropy/orthogonality lever. |
| [FRAMINGS.md](../FRAMINGS.md) | `grounds` | F1/F2 (`shadow ⊕ structure`, entropy as log-cardinality) is the formal root of the orthogonality principle. |
| ZefraHub `ontology-conventions.md` v1.4.0 | `derives-from` | Source document this was ported and adapted from. |
