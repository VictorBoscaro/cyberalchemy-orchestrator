---
name: system-view
description: "Use when: authoring the shape-and-stakes view of a target — the narrative explained one conceptual layer at a time, the given-vs-optimized layering, and the load-bearing stances named but not decided — as the upper half of a system-view / engineer-view pair."
argument-hint: "<target-or-path> [--ontology-view <path>] [--engineer-view <path>] [--output <md-path>] [--depth quick|standard|deep]"
surface_kind: native-runtime-package
canonical_source: null
mutation_policy: author-in-place
tier: arcana
domain: view-authoring
version: 0.1.0-seed
origin: generalized from the GoldenQuill system-view paired-doc pattern; owns shape, names stances, decides nothing
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent
---

# Sigil: system-view

<objective>
Author one governed markdown view that explains a target's *shape* at the altitude a stakeholder needs to judge whether the idea is sound — one conceptual layer at a time, no schemas and no code. It owns the narrative and the layering, it **names** every load-bearing stance, and it **decides none of them**: each stance is named here and its verdict is owned by `engineer-view`, pointed to but never restated.
</objective>

<logic-type>
Arcana: fixed-altitude shape synthesis with named-but-undecided stances and cross-view single-owner discipline.
</logic-type>

<status>
Seed. Defines the lane model, the named-stance discipline, and the cross-reference contract. Not promoted.
</status>

<altitude>
This view operates at the **shape and stakes** altitude.

| Owns (single canonical home) | Forbidden here (defer across) |
| --- | --- |
| The narrative shape, one conceptual layer at a time | Term definitions → `ontology-view` |
| The given-vs-optimized (or equivalent) layering | Verdicts on any stance → `engineer-view` decision inventory |
| The *naming* of each load-bearing stance | Schemas, record fields, enums, failure codes → `engineer-view` |
| "Alternative framings we considered / why set aside" | Runtime mechanics → `engineer-view` |
| Optional shape diagrams (Mermaid, L1) | Redefining a term already owned by `ontology-view` |

The rule that makes this a view and not a summary: where a stance is relevant to both altitudes, it is **named here and its verdict lives only in engineer-view**. Nothing is decided twice.
</altitude>

<inputs>
- the target (text, repository subtree, artifact, or design) or a path to it,
- optional handles to sibling views (`--ontology-view`, `--engineer-view`) so deferrals resolve,
- optional output path, depth, and audience constraints.
</inputs>

<canonical-lanes>
Fixed lane set; record omitted-lane reasons.

| Lane | Vision | Output Handle |
| --- | --- | --- |
| `surface` | What the target is and why a stakeholder is inspecting it. | `surface.summary` |
| `shape` | The protagonist idea and the conceptual layers, one at a time. | `shape.narrative` |
| `layering` | The given-vs-optimized (or domain-equivalent) stratification. | `layering.model` |
| `stances` | Each load-bearing stance, named with its tension, not decided. | `stances.named` |
| `alternative_framings` | Per section: framings considered and why set aside. | `framings.tables` |
| `shape_diagrams` | Optional Mermaid shape diagrams (no schemas). | `shape.diagrams` |
| `deferrals` | Stances and terms whose verdict/definition is owned elsewhere. | `deferrals.handles` |
</canonical-lanes>

<cross-reference-contract>
- **Owns** handles of the form `stance:<slug>` and `shape:<anchor>`. Each named stance must declare the engineer-view row that will own its verdict (`stance:<slug> → engineer-view#<id>`).
- **Defers** term meaning with `defer:term → ontology-view#term:<slug>` — never restates a definition.
- A stance named here must have **exactly one** verdict downstream. A stance with zero downstream verdicts, or a verdict stated here, is a contract violation the `paired-views` spell will catch.
</cross-reference-contract>

<process>
1. Resolve the target boundary and the stakeholder altitude.
2. Build the evidence boundary: source-backed shape vs inferred shape.
3. Author `surface` and `shape` — the protagonist idea first, then layers one at a time.
4. Author `layering` — what is given/fixed vs what is optimized vs what merely accumulates.
5. For each load-bearing decision point, author a `stances` entry: name the stance and its tension, then emit `stance:<slug> → engineer-view#<id>`. Do not state the verdict.
6. Add `alternative_framings` tables per section — the framings considered and why set aside.
7. Add `shape_diagrams` only where a diagram clarifies the shape; never embed schemas.
8. Emit `deferrals` for every term reference (to ontology-view) and every stance verdict (to engineer-view).
9. Validate: no verdict stated, no term redefined, every named stance points to exactly one engineer-view row.
10. Report missing context and any stance with no downstream owner honestly.
</process>

<output-contract>
Return a governed markdown view plus a status block:

```markdown
## system-view Result

- Status: pass | flag | block
- Target boundary: <resolved scope or blocked reason>
- Stakeholder altitude: <resolved or open question>
- Lane handles:
  - surface / shape / layering / stances / alternative_framings / shape_diagrams / deferrals: <handle or omitted reason>
- Stances named: <stance:slug → engineer-view#id ...>
- Decided-nothing check: <no verdict stated here: pass | violations listed>
- Term-deferral check: <no term redefined here: pass | violations listed>
- Evidence boundary: <source-backed vs inference>
```

The view body is a markdown document opening with a cross-reference note (points up to ontology-view, down to engineer-view), then `surface`, the layered `shape` sections each with an "alternative framings we considered" table, the `layering` model, and a closing "what this view does not cover" section that lists every named stance and its engineer-view owner.
</output-contract>

<quality-bar>
A successful run must:

- explain the shape one conceptual layer at a time at stakeholder altitude,
- name every load-bearing stance with its tension and point each to exactly one engineer-view verdict,
- state no verdict and define no term,
- include an "alternative framings we considered" table per major section,
- keep diagrams free of schemas and code,
- distinguish source-backed shape from inference,
- close with a "what this view does not cover" map,
- preserve seed status until live examples and Experiment Harness evidence support promotion.
</quality-bar>

<anti-patterns>
Avoid:

- stating a verdict (that is engineer-view's job — name the stance, point across),
- redefining a term owned by ontology-view,
- smuggling schemas, enums, or record fields into the shape or diagrams,
- naming a stance with no downstream verdict owner,
- producing a flat summary instead of layered shape,
- decorative diagrams that do not clarify the shape,
- deciding the same thing in two views.
</anti-patterns>

<observability>
Record: target boundary, stakeholder altitude, layer count, stances named, stances with/without downstream owner, verdict-leak violations, term-redefinition violations, inferred-vs-sourced ratio, and user correction signals.
</observability>

<promotion-gate>
Promotion requires Sigil Development review plus Experiment Harness evidence for:

- one product/idea target and one architecture/system target,
- one example with a full set of named stances each resolving to an engineer-view row,
- one "alternative framings" table grounded in real considered-and-rejected options,
- one validation pass confirming no verdict and no term definition leaked,
- one blocked/flagged example for insufficient context.
</promotion-gate>
</content>
