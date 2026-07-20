---
name: ontology-view
description: "Use when: authoring the vocabulary-and-concept-graph view of a target — the single canonical home for each term, its typed relations, roles, confidence, and naming conflicts — as the floor beneath a system-view / engineer-view pair."
argument-hint: "<target-or-path> [--vault <ontology-vault-path>] [--system-view <path>] [--engineer-view <path>] [--output <md-path>] [--depth quick|standard|deep]"
surface_kind: native-runtime-package
canonical_source: null
mutation_policy: author-in-place
tier: arcana
domain: view-authoring
version: 0.1.0-seed
origin: generalized from the GoldenQuill system-view/engineer-view paired-doc pattern; the missing floor that owns term meaning
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent
---

# Sigil: ontology-view

<objective>
Project a target's vocabulary into one governed markdown view that owns — as the single canonical home — every load-bearing term's definition, its typed relations to other terms, its role and confidence, and any naming conflict or drift. This is the floor beneath a `system-view` (shape) and `engineer-view` (verdicts) pair: both of those views reference terms defined here and never redefine them.
</objective>

<logic-type>
Arcana: read-side projection of a governed concept store into a fixed-altitude view, with cross-view single-owner discipline and an evidence boundary.
</logic-type>

<status>
Seed. Defines the lane model, the cross-reference contract, and the validation surface. Not promoted; does not yet prove live reusable behavior across multiple targets.
</status>

<altitude>
This view operates at the **vocabulary and concept-graph** altitude.

| Owns (single canonical home) | Forbidden here (defer across) |
| --- | --- |
| The canonical definition of each load-bearing term | The verdict on a contested definition → `engineer-view` decision inventory |
| Typed relations / edges between concepts | The *narrative of why* a concept matters → `system-view` shape |
| The load-bearing axes/distinctions and their relation (e.g. orthogonality) | Schemas, record fields, enums → `engineer-view` contracts |
| Term role, confidence, and provenance | Implementation mechanics → `engineer-view` |
| Naming conflicts, overloads, drift between sources | Stance naming → `system-view` |

If a term needs a *decision* (which of two competing definitions wins), this view records the conflict and **points to** the engineer-view row that owns the verdict. It never decides.
</altitude>

<consumes>
This sigil is the read-side projection of `ontology-vault`. It does not reinvent a concept store:

- If an `ontology-vault` exists, read its roles, confidence, premises, and edge rules and project them at view altitude.
- If none exists, build a lightweight inline concept set (term → definition → relations → provenance) and recommend promoting it into a real `ontology-vault` via that sigil.
- Defer canonical-definition authority disputes to `definitions-governance` when one is installed.
</consumes>

<inputs>
- the target (text, repository subtree, artifact, or design) or a path to it,
- optional `--vault` path to an existing `ontology-vault`,
- optional handles to sibling views (`--system-view`, `--engineer-view`) so deferrals resolve,
- optional output path, depth, and audience constraints.
</inputs>

<canonical-lanes>
Every run selects from this fixed lane set and records omitted-lane reasons.

| Lane | Vision | Output Handle |
| --- | --- | --- |
| `terms` | Each load-bearing term, its single canonical definition, role, and confidence. | `terms.catalog` |
| `relations` | Typed edges between terms (is-a, part-of, depends-on, orthogonal-to, overrides, supersedes, alias-of). | `relations.graph` |
| `axes` | The load-bearing distinctions and how they relate (independence, precedence, coupling claims). | `axes.model` |
| `conflicts` | Naming collisions, overloaded terms, stale aliases, cross-source drift. | `conflicts.register` |
| `provenance` | Source-backed fact vs inference, one citation per term. | `provenance.boundary` |
| `deferrals` | Term meanings that need a verdict or a shape-narrative elsewhere, as resolvable handles. | `deferrals.handles` |
</canonical-lanes>

<cross-reference-contract>
This view emits and consumes single-owner handles.

- **Owns** handles of the form `term:<slug>` and `relation:<a>--<b>` — any sibling view referencing a term must cite `term:<slug>`, never restate the definition.
- **Defers** with handles of the form `defer:verdict → engineer-view#<id>` and `defer:shape → system-view#<anchor>`.
- A term defined here must appear in **exactly one** lane row. A second definition anywhere is a contract violation the `paired-views` spell will catch.
</cross-reference-contract>

<process>
1. Resolve the target boundary and the inspection depth.
2. Load the `ontology-vault` if provided; otherwise extract a lightweight concept set from the target.
3. Build the evidence boundary: separate source-backed definitions from inferred ones.
4. Author the `terms` lane — one canonical definition per term, with role and confidence.
5. Author the `relations` and `axes` lanes — typed edges; state independence/precedence/coupling explicitly, never as decoration.
6. Author the `conflicts` lane — every overload, stale alias, or cross-source drift, with both sources cited.
7. Emit `deferrals` — terms whose verdict belongs to engineer-view or whose narrative belongs to system-view, as resolvable handles.
8. Validate: each term has exactly one home, each relation names both endpoints, each claim cites evidence or is marked inference.
9. Report missing context, unresolved conflicts, and recommended `ontology-vault` promotion honestly.
</process>

<output-contract>
Return a governed markdown view plus a status block:

```markdown
## ontology-view Result

- Status: pass | flag | block
- Target boundary: <resolved scope or blocked reason>
- Vault source: <ontology-vault path | built-inline | none>
- Lane handles:
  - terms: <handle or omitted reason>
  - relations: <handle or omitted reason>
  - axes: <handle or omitted reason>
  - conflicts: <handle or omitted reason>
  - provenance: <handle or omitted reason>
  - deferrals: <handle or omitted reason>
- Single-owner check: <every term in exactly one row: pass | violations listed>
- Deferrals emitted: <term:slug → engineer-view#id | system-view#anchor ...>
- Evidence boundary: <source-backed vs inference>
- Conflicts open: <count and the contested terms>
```

The view body itself is a markdown document with a `terms` table (term · definition · role · confidence · source), a typed `relations` list, an `axes` section, and a `conflicts` register.
</output-contract>

<quality-bar>
A successful run must:

- give each load-bearing term exactly one canonical definition,
- type every relation and name both endpoints,
- state axis independence/precedence/coupling as an explicit claim, not decoration,
- cite a source for each definition or mark it inference,
- surface every naming conflict rather than silently picking a winner,
- emit resolvable deferral handles instead of importing verdicts or shape-narrative,
- recommend `ontology-vault` promotion when the inline set is load-bearing,
- preserve seed status until live examples and Experiment Harness evidence support promotion.
</quality-bar>

<anti-patterns>
Avoid:

- defining the same term in two places (the drift this sigil exists to kill),
- deciding a contested definition here instead of deferring the verdict to engineer-view,
- narrating why a concept matters (that is system-view's shape lane),
- emitting schemas, record fields, or enums (that is engineer-view's contracts lane),
- inventing relations not grounded in the target,
- collapsing a real naming conflict into a silent rename,
- treating correlation between axes as a coupling relation.
</anti-patterns>

<observability>
Record: target boundary, vault source, term count, relation count, conflicts open vs resolved, deferrals emitted, inferred-vs-sourced ratio, single-owner violations, and user correction signals.
</observability>

<promotion-gate>
Promotion requires Sigil Development review plus Experiment Harness evidence for:

- one target with an existing `ontology-vault` source,
- one target with an inline-built concept set,
- one example surfacing a real naming conflict with both sources cited,
- one example emitting deferral handles that a sibling view resolves,
- one validation pass confirming the single-owner invariant.
</promotion-gate>
</content>
</invoke>
