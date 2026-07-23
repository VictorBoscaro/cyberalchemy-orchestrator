---
tags: [vault, ontology, skills]
node_type: constitution
is_session: false
layer: [ontology, architecture]
nature: [reference, technical]
status: draft
version: 0.1.0
last_updated: 2026-07-23
---

# Skill Tag Conventions

> Rules every invocable skill (`.claude/skills/<name>/SKILL.md`) must follow when it
> declares its **classification tags**. This is to skills what
> [[ontology-conventions]] is to vault nodes: an **orthogonal labeling system** whose only
> invariant is that every axis carries information no other axis can predict.
>
> **Status:** `draft` — Track-A slice of the [[skill-protocol-compiler-direction]] program.
> Authored to be red-teamed by an independent `review` dispatch before ratification.

---

## Objective

Give every skill a small set of **orthogonal machine-readable tags** so that a catalogue, a
governance sweep, and — the load-bearing consumer — the future **skill-protocol-compiler** can
reason about a skill *without reading its whole body*. The compiler reads these tags to decide how
to decompose the skill into an execution graph (whether there are subagent contact points, whether
mutation gates are needed, what kind of work it is).

The governing constraint is the same as the vault's: **every tag axis must be statistically
independent** — knowing one axis's value must tell you nothing about another's. An axis that is
predictable from the others adds description length without adding knowledge (a *shadow*, not
*structure* — [FRAMINGS.md F1](../FRAMINGS.md)). This is the admission test for every axis below and
for any future axis.

---

## Why tags, and not the frontmatter

`create-skill` fixes the SKILL.md frontmatter at **exactly five fields** (`name`, `description`,
and the earned `argument-hint` / `allowed-tools` / `agent`); adding a project doc-convention to that
frontmatter is called out there as "the most common mistake." Therefore **tags never go in the
frontmatter.** They live in a **trailing block at the end of the SKILL.md body** (see Format).

Consequence — and it is deliberate: **tags do not affect routing.** Skill selection is
`description`-only, and the body (including this block) is unseen at selection time. Tags serve a
*different* consumer — the catalogue, governance, and the compiler — which read the body when the
skill is loaded. A weak `description` is still a dead skill; tags do not rescue it.

---

## The axes

Four axes. Three are required single-value; one is an optional boolean flag (the `meta` axis,
modeled on the vault's optional `private` key). Each passes the orthogonality admission test —
*"can I predict this value from the others?"* — as argued per axis.

### 1. `topology` — how it executes *(required, single-value)*

| value | meaning |
| --- | --- |
| `inline` | Does its own work in the calling context; spawns no subagents (a lone helper is still `inline`). |
| `router` | Chooses among and delegates to **other skills**; a dispatcher. |
| `dispatches` | Fans out to **subagents / groups** (a real dispatch under `domainspec-subagents-strategy`). |

*Orthogonality:* topology is independent of *what* the skill does (`domain`) and of *whether it
writes* (`effect`) — a `research` skill can be `inline` or `dispatches`; a `dispatches` skill can be
`read-only` or `mutating`.

### 2. `effect` — what it changes *(required, single-value)*

| value | meaning |
| --- | --- |
| `read-only` | Reads/analyzes/reports; writes nothing durable (no files, no ledger, no external calls). |
| `mutating` | Persists something: writes files, appends the ledger, or calls an external service. |

*Orthogonality:* effect is independent of topology (an `inline` skill can mutate; a `dispatches`
skill can be purely `read-only`) and of domain. It is the axis that tells the compiler whether a
mutation gate / `final_approver` over writes is needed (**P8 trust-but-verify**).

### 3. `domain` — what kind of work *(required, single-value)*

The topical axis (kin to the vault's `layer`/`tags`). Starter catalog — extend under governance,
never silently:

`authoring` · `review-tension` · `orchestration` · `governance` · `telemetry` · `research` ·
`sigil` · `ontology`

> **Naming guard:** the `orchestration` value (work *about* planning/dispatching) is deliberately
> **not** named `dispatch`, to avoid a read-collision with the `topology: dispatches` value. A skill
> can be `domain: orchestration, topology: inline` (plans but doesn't fan out) or
> `domain: research, topology: dispatches` (research that fans out) — the two axes stay independent.

*Orthogonality:* domain is the *subject* of the work; topology and effect are its *shape*. Knowing a
skill is `research` tells you nothing about whether it fans out or writes.

### 4. `meta` — is it about skills/dispatching itself *(optional boolean; omitted = false)*

`meta: true` marks a skill whose subject is skills or dispatching itself (mirrors **P13 meta +
lineage**). Omitted means ordinary object-level work.

*Orthogonality:* a `meta` skill can be `inline` or `dispatches`, `read-only` or `mutating`,
`authoring` or `orchestration` — the flag adds a bit no other axis carries, exactly as the vault's
`private` flag earns its place.

---

## Format

A single trailing block, last thing in the SKILL.md body, machine-parseable and human-readable:

```markdown
<!-- skill-tags
topology: dispatches
effect: read-only
domain: orchestration
meta: true
-->
```

Rules:
- Exactly one block per SKILL.md, and it is the **last** content.
- `topology`, `effect`, `domain` are **required**; `meta` is optional (omitted = `false`).
- Values come from the catalogs above; an unlisted value is invalid until added under governance.
- The block is a comment, so it renders invisibly and never interferes with the body's prose.

*(Alternative under review: a per-skill sidecar `tags.yaml`. Trade-off: a sidecar is easier for a
catalogue to bulk-read but splits the skill's truth across two files; the footer block keeps one
file but must be parsed out of Markdown. The review should settle this.)*

---

## Worked example — the skill-protocol-compiler

```markdown
<!-- skill-tags
topology: dispatches
effect: mutating
domain: orchestration
meta: true
-->
```

Read-only *over the target skill* but `mutating` overall because it **persists the Skill Execution
Profile**; `dispatches` because it fans out to a read-only decomposition worker; `orchestration`
because its subject is dispatch planning; `meta: true` (**P13**). No axis is forced or ambiguous —
which is the whole point of de-fusing them.

---

## Governance

- This is a `draft` `constitution`. Each axis and its catalog is a **falsifiable rule** until it
  survives review under real skills and is promoted (the [[ontology-conventions]] hypothesis →
  premise → law arc).
- Adding, merging, or retiring an axis or a catalog value is a **governance act** (it must pass the
  orthogonality admission test), never a silent edit.
- Backfilling existing skills with tags is **out of scope for this draft**; it is a follow-on once
  the axes are ratified.

## Connections

| Document | Type | Description |
| --- | --- | --- |
| [[ontology-conventions]] | `derives-from` | Same orthogonality principle; this is its analogue for skills instead of vault nodes. |
| [[skill-protocol-compiler-direction]] | `depends-on` | The compiler is the load-bearing consumer of these tags; this convention is its Track-A prerequisite. |
| [FRAMINGS.md](../FRAMINGS.md) | `grounds` | F1 `shadow ⊕ structure` — a redundant axis is a shadow that adds no separating power. |
