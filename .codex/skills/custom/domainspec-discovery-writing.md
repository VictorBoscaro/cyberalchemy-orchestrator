---
description: How to write a discovery document — problem space, design decisions, and enough detail for an implementation plan. The producing process for the `discovery` canonical kind.
---
# Discovery Writing

## Purpose

A discovery captures the problem space, design decisions, and enough detail for an agent to write an implementation plan. It is **not a task list**. A discovery answers "what are we changing and why" — an implementation plan answers "how, step by step."

If the output of this session is a list of tasks, you are writing an implementation plan, not a discovery.

This skill is the **producing process** for the `discovery` canonical kind. Its type-level facts (`authority_kind: Evidence`, `durability: ephemeral`, `authority_reachable: no`) are looked up from [`CANONICAL-KINDS.md`](../../../cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md), never declared in the file.

---

## Frontmatter

The contract is owned by the **Instance Contract** in [`CANONICAL-KINDS.md`](../../../cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md#instance-contract-frontmatter). Do not invent fields here. In force:

| Field | Required | Notes |
| --- | --- | --- |
| `canonical_kind` | yes | `discovery` — mirrors the filename, which is authoritative on conflict. |
| `title` | yes | Which discovery this is. |
| `description` | yes | **The retrieval surface, ≤ ~60 words.** It is what gets embedded and indexed — it must discriminate (a sentence that would serve another discovery equally well has failed), be dense, carry no filler, and stand alone with no outward pronouns. |
| `evidence_for` | yes | List. Which **authority kind** this evidence intends to feed — authority-bearing kinds only: `Definition` · `Constitution` · `Discipline` · `Decision` · `Spec` · `Runtime contract`. **Declares an intended destination and grants nothing.** Not named `authority_kind` on purpose — that is the artifact's own type-level fact, never written. |
| `created` | yes | |
| `last_updated` | yes | Starts equal to `created`; bumped on content edits. Coarse signal only — the event log is git. |
| `tags` | yes | |
| `question` | opt | The question the discovery was sent to answer. A discovery may be pure reconnaissance, with none. |
| `outcome` | opt | Requires `question`. `question` without `outcome` is an open investigation — legal while open, residue once closed. |

Never declare `process`, `authority_kind`, `durability`, `contradictions`, or `authority_reachable` — they are functions of the kind, and an instance that could declare them could self-promote.

---

## Mandatory Document Structure

Sections must appear in this order. Do not skip or reorder them.

### Objective (≤3 sentences, required first)

What is being changed and what the end state looks like. No motivation here — that goes in Business Context.

**Quality gate:** If you cannot write this in 3 sentences, the scope is unresolved. Stop and clarify with the user before continuing.

---

### 1. Business Context

Three subsections, all required:

**Why now** — The triggering condition: a rule that cannot be expressed, a failure in production, an architectural constraint that blocks future work. One concrete paragraph. No speculation.

**What's broken** — Enumerate each problem with a specific location (`file.py:line` or `ClassName.method`). A problem without a location is unverified.

**What stays the same** — Explicit scope boundary: list the assets, models, and behaviors that are out of scope. An unnamed boundary is an unbounded scope.

---

### 2. Core Concepts

Introduce the new abstractions and key design decisions. Short code sketches are appropriate here when they communicate the contract clearly. This section answers "what and why" — save step-by-step detail for later sections.

Each concept should have:
- A name
- What it does (one sentence)
- Why this design was chosen over alternatives (if non-obvious)

---

### 3–N. Detailed Specifications

One section per area of change. Typical sections (use what applies):

- **Data model changes** — schema diffs, migration strategy, index changes
- **Interface / API contracts** — new base classes, method signatures, port definitions
- **Service / execution flow** — sequence of operations, what changes vs. today (a before/after table is often clearest)
- **Cleanup** — what gets deleted, with location and reason
- **Open questions** — unresolved items; each must include a recommendation, not just a question

---

## Edges the discovery must carry

Declared in a `## Connections` block. The permitted set is owned by [`ALLOWED-EDGES.yaml`](../../../cyberAlchemy-v2/ontology/canonical-kinds/ALLOWED-EDGES.yaml) — **anything absent from it is forbidden**:

- `derives-from` → the `research` this discovery rests on (`0..N`). None, if it is reconnaissance with no research behind it. No edge is mandatory.
- `contradicts` → another `discovery` this one asserts incompatible things with (`0..N`). **Symmetric.** This is a *claim*, so it lives here, between the two artifacts — a session may never assert it. A session that notices a conflict records it by **updating** one of the two discoveries to carry this edge.

**`derives-from` and `alternative-to` between two discoveries are *unruled*** — denied by absence. Do not draw either.

**Never declare an inverse.** `derives`, `created-by`, `updated-by` are *read directions*, not edges: the arrow is written once, at its source. The `session --creates--> discovery` and `session --updates--> discovery` edges are written by the session, never by the discovery.

---

## Residue

**Residue is carried, never authored.** There is no `residue.md`. An open question with nowhere to land stays in this file's `## Open questions` section — every one of them carrying a recommendation, not just a question.

---

## Quality Checks Before Finishing

- [ ] Objective written before any other section
- [ ] Every item in "What's broken" has a specific file location
- [ ] "What stays" is non-empty (unbounded scope = future rework)
- [ ] Open questions include recommendations, not just questions
- [ ] `description` discriminates — it would not serve another discovery equally well
- [ ] No type-level facts declared in frontmatter (`process`, `authority_kind`, `durability`, …)
- [ ] `## Connections` declares only edges permitted by `ALLOWED-EDGES.yaml`
- [ ] No implementation steps disguised as design decisions — if it's "do X then Y", it belongs in an implementation plan
- [ ] Final Step (below) executed — diagram appended

---

## Final Step — Mermaid Flow Diagram (mandatory, last action)

After every other section is written and the Quality Checks pass, dispatch a **Sonnet subagent** to append a `## Flow Diagram` section to the discovery file containing a mermaid diagram of what the discovery describes.

This step is non-negotiable and is always the last action of the discovery-writing flow — do not invoke it before the body is complete, do not skip it, do not produce the diagram inline yourself.

Use the Agent tool with `subagent_type: "general-purpose"` and `model: "sonnet"`. The prompt must be self-contained — the subagent has not seen this conversation:

> Read the discovery at `<absolute path to the .md file>`. Append a new section titled `## Flow Diagram` at the end of the file. The section must contain:
> 1. One mermaid diagram (`flowchart`, `sequenceDiagram`, or `stateDiagram-v2` — pick whichever best fits the discovery's nature) that captures the system, flow, or state transitions the discovery describes. Nodes/edges should mirror the entities and relationships named in the discovery body — do not invent new concepts.
> 2. A short paragraph (≤4 sentences) below the diagram explaining what the diagram shows and how to read it, in the same vocabulary the discovery uses.
>
> Constraints: edit the file in place using Edit (do not rewrite it). Do not modify any existing section. Do not add the diagram if a `## Flow Diagram` section already exists — update it in place instead.

---

## Navigation

Before writing, anchor the discovery to existing vocabulary:

- **New concepts** — check the definitions towers before inventing a term. Arcanum-wide terms are owned in `arcanum/definitions/DEFINITIONS.md` (public); v2 spine terms (`CAV2-D*`) in `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` (private). v2 **references** Arcanum IDs — it never redefines them. Routing: `cyberAlchemy-v2/SOURCE-MAP.md`.
- **Architecture rules** — check `cyberAlchemy-v2/authority/constitutions/`. A design that violates a constitution must be **called out explicitly in the discovery**, never silently ignored.
- **Public/private boundary** — only Arcanum is public. A discovery must never route private prose into `arcanum/`.
