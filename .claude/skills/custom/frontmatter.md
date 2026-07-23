---
description: Minimal, self-contained cheatsheet for the frontmatter + Connections of any governed .md doc in this repo. Consume this instead of the full ontology-conventions.md when you just need to fill metadata correctly.
---

# Frontmatter & Connections Cheatsheet

> **This is the cheatsheet (schema + pickers).** The authority — with rationale, the
> orthogonality math, status entry/exit criteria, and per-node_type nuance — is
> [`vault/ontology-conventions.md`](../../../vault/ontology-conventions.md). Read that only
> when the pickers below don't settle a case. This file is derived and non-authoritative:
> if the two ever disagree, the conventions doc wins.

## Two hard gates (the PostToolUse nudge checks these)

Every governed `.md` (under `vault/`, `sessions/`, `research/`, `docs/`, or root) must carry:

1. a **YAML frontmatter** block (`---` … `---`), and
2. a **`## Connections`** section (a typed-edge table — may be empty with a one-line reason).

Excluded from the gate: `.claude/`, `node_modules/`, any `templates/` dir.

## The lists here are open, not closed enums

Every `|`-separated list below — in the frontmatter schema **and** the 14 edge types — is a
**starting vocabulary, not a closed enum**. On any field an agent may supply a new ("other")
value, and it may coin a new edge type, when nothing listed fits. The gate is the
**orthogonality admission test** ([ontology-conventions.md](../../../vault/ontology-conventions.md),
Orthogonality Principle): a new value or edge earns its place only if it adds information you
**cannot predict from the values that already exist** — otherwise it is redundant and just
grows the vocabulary without growing knowledge. So: prefer an existing value when one fits;
extend deliberately when none does.

## Frontmatter schema

```yaml
---
tags: [topical labels only]              # domain/topic — never role, never maturity
node_type: axiom | premise | constitution | discovery | implementation-plan | spec | audit | conceptual | essay | test | backlog | readme
is_session: true | false                 # is this a conversation/session record?
session_ref: <session-id> | null         # optional — the session that produced this doc
layer: ontology | architecture | domain | application | external   # multi-value OK
nature: explanatory | procedural | reference | technical            # multi-value OK
status: draft | exploratory | active | consolidated | evergreen
veracity: high | medium | low            # belief nodes only (see applicability)
conviction: high | medium | low          # belief nodes only (see applicability)
version: 0.x.x
last_updated: YYYY-MM-DD
private: true                            # optional — do-not-publish flag; omit = publishable
---
```

## `node_type` picker — "if challenged, the right answer is…"

| node_type | Challenge response |
|---|---|
| `axiom` | "Foundational — revisiting it breaks everything built on it" |
| `premise` | "Show me evidence and we'll update it" |
| `constitution` | "Change it through governance, not informally" |
| `discovery` | "Exploration — enrich it or supersede it with a decision" |
| `implementation-plan` | "Follow it, update it if scope changed, or supersede it" |
| `spec` | "Update it if the code changed" |
| `audit` | "Run the audit again and see if the findings still hold" |
| `conceptual` | "Context — enrich or correct it" |
| `essay` | "Committed argument from experience — engage the reasoning or counter it" |
| `test` | "Run the tests and see if they pass" |
| `backlog` | "Prioritize it, schedule it, or close it" |
| `readme` | "Update it to reflect what's actually in the directory" |

## The other labels, in one line each

- **`layer`** (system scope): `ontology` = the vault's own rules · `architecture` = cross-cutting technical structure · `domain` = business logic in a bounded context · `application` = end-user/product surface · `external` = outside context (prior art, upstream repos).
- **`nature`** (reading instruction): `explanatory` = prose, read linearly · `procedural` = steps, follow in order · `reference` = table/catalog, look up an item · `technical` = schema/code/diagram, inspect structure.
- **`status`** (maturity): `draft` → `exploratory` → `active` → `consolidated` → `evergreen`. Start at `draft`. **Hard boundary:** a higher-level doc never derives authority from a lower-level one.
- **`tags`** (topic only): domain `#orchestration #agents #dispatch #anti-bias #anti-noise #residue #category-theory` · technical `#architecture #ui #ledger #skills #ontology` · `#vault`.

## `veracity` (evidence) × `conviction` (bet)

Two orthogonal confidence axes, both `high | medium | low`:

- **veracity** = how much reality confirms it (changes through data/tests).
- **conviction** = how hard we're betting on it (changes through decisions).

|  | conviction: high | conviction: low |
|---|---|---|
| **veracity: high** | Consolidated Law (proven, driving design) | Ignored Fact (true, not acted on) |
| **veracity: low** | Strategic Bet (betting before proof) | Loose Thread (untested, parked) |

**Applicability:** carry both for `axiom`, `premise`, `discovery`, `audit` (and `essay`).
**Omit** for `implementation-plan`, `spec`, `conceptual`, `test`, `backlog`, `readme`, and the
document-level `constitution`. *This repo's extension:* while a `constitution` is
`candidate`, **each rule inside it carries `veracity`/`conviction` inline** (a candidate rule
is a hypothesis before it is law); the fields drop away when the rule is promoted to a premise.

## `## Connections` — the typed-edge table

```markdown
## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[other-doc]] | `derives-from` | one-line reason for the edge |
```

Edges are **bidirectional**: when you declare an edge here, add the inverse row to the other
doc (`derives-from` ↔ `grounds`), with a patch-level version bump there. A view/query layer
dedups the pair. Link by `[[slug]]` (vault node) or a markdown path.

### The 14 edge types

These are the starting set, not a closed list — coin a new edge type (same orthogonality
test) when none of the 14 captures the relationship.

| Type (A → B) | Meaning |
|---|---|
| `resolves` | A solves the problem B states |
| `derives-from` | A was built upon / generated by B — the canonical parent→child chain |
| `grounds` | A is the foundation B rests on — inverse of `derives-from` |
| `implements` | A is the concrete implementation of spec/constitution B |
| `validates` | A provides evidence/tests that raise B's `veracity` |
| `promotes-from` | A ratifies the thesis stated in B (constitution ← hypothesis) |
| `exemplifies` | A is a concrete instance of abstract B |
| `refines` | A is a more detailed version of B, same topic |
| `contextualizes` | A is informational background for B, no functional dependency |
| `depends-on` | A does not function without B (runtime dependency, stronger than `derives-from`) |
| `alternative-to` | A is a competing/discarded alternative to B |
| `contradicts` ⚠️ | A is in tension with / refutes B — **resolve before promotion** (most valuable edge) |
| `supersedes` | A is the direct successor of B, making B obsolete |
| `deprecates` | A informally/partially replaces B (soft retirement) |
| `other` | When none of the above fits