---
name: engineer-view
description: "Use when: authoring the mechanics-and-verdicts view of a target — the decision inventory (RESOLVED/OPEN/CRITICAL with authority cites), the schemas and contracts, and the single owning verdict for every stance named in its system-view — as the lower half of a system-view / engineer-view pair."
argument-hint: "<target-or-path> [--ontology-view <path>] [--system-view <path>] [--output <md-path>] [--depth quick|standard|deep]"
surface_kind: native-runtime-package
canonical_source: null
mutation_policy: author-in-place
tier: arcana
domain: view-authoring
version: 0.1.0-seed
origin: generalized from the GoldenQuill engineer-view paired-doc pattern; owns every verdict and contract, decides nothing twice
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent
---

# Sigil: engineer-view

<objective>
Author one governed markdown view that refines a target's shape down to mechanics and verdicts: the decision inventory where every load-bearing stance gets its **single owning verdict** with status and authority, the schemas and contracts, and the runtime mechanics. It is the one place verdicts live — `system-view` names a stance, this view decides it, and nothing is decided twice.
</objective>

<logic-type>
Arcana: fixed-altitude refinement that owns verdicts, contracts, and mechanics under cross-view single-owner discipline.
</logic-type>

<status>
Seed. Defines the lane model, the decision-inventory contract, and the cross-reference surface. Not promoted.
</status>

<altitude>
This view operates at the **mechanics and verdicts** altitude.

| Owns (single canonical home) | Forbidden here (defer across) |
| --- | --- |
| The decision inventory — one verdict per stance, with status and authority | Re-narrating the shape → `system-view` |
| Schemas, record fields, enums, failure-code families | Redefining a term → `ontology-view` |
| Runtime/implementation mechanics | Naming new stakeholder-altitude stances (those originate in `system-view`) |
| The cross-reference map (which view owns which claim) | Re-deriving the layering story |

Status legend for the inventory: **RESOLVED** (decided and enforced) · **OPEN** (named, not decided) · **CRITICAL** (OPEN *and* blocks the core thesis until built). Every stance `system-view` named must resolve to exactly one row here.
</altitude>

<inputs>
- the target (text, repository subtree, artifact, or design) or a path to it,
- optional handles to sibling views (`--ontology-view`, `--system-view`) so deferrals and named stances resolve,
- optional output path, depth, and audience constraints.
</inputs>

<canonical-lanes>
Fixed lane set; record omitted-lane reasons.

| Lane | Vision | Output Handle |
| --- | --- | --- |
| `decision_inventory` | Every load-bearing decision: verdict, status, authority. | `decisions.table` |
| `contracts` | Schemas, record fields, enums, failure-code families. | `contracts.catalog` |
| `mechanics` | How the load-bearing behaviors actually wire together. | `mechanics.map` |
| `cross_reference_map` | Which view owns which claim; the single-owner map. | `xref.map` |
| `deferrals` | Term meanings (to ontology-view) and shape (to system-view). | `deferrals.handles` |
</canonical-lanes>

<cross-reference-contract>
- **Owns** handles of the form `decision:#<id>` (e.g. `decision:#D7`). Each row that answers a system-view stance must back-reference it (`decision:#D7 ← system-view#stance:learning-loop`).
- **Defers** term meaning with `defer:term → ontology-view#term:<slug>` and shape with `defer:shape → system-view#<anchor>`.
- Every decision row must cite an **authority** (file, ADR, architecture version, or "no running gate in repo" for OPEN). A verdict without authority is a contract violation.
- Every stance named in the bound `system-view` must have **exactly one** row here. Zero rows, or two rows answering one stance, is caught by the `paired-views` spell.
</cross-reference-contract>

<process>
1. Resolve the target boundary; load the bound `system-view` and `ontology-view` if provided.
2. Build the evidence boundary: cite the authority for each verdict and contract.
3. Author `decision_inventory` — one row per load-bearing decision: verdict · status (RESOLVED/OPEN/CRITICAL) · authority. Back-reference each system-view stance.
4. Author `contracts` — schemas, record fields, enums, failure-code families, each source-cited.
5. Author `mechanics` — how the load-bearing behaviors actually wire, referencing terms via ontology-view handles.
6. Author the `cross_reference_map` — the single-owner table across the three views.
7. Emit `deferrals` for term meaning and shape; never restate them.
8. Validate: every system-view stance has exactly one row; every row has an authority; no term redefined; no shape re-narrated.
9. Report unresolved stances, missing authorities, and contract gaps honestly.
</process>

<output-contract>
Return a governed markdown view plus a status block:

```markdown
## engineer-view Result

- Status: pass | flag | block
- Target boundary: <resolved scope or blocked reason>
- Lane handles:
  - decision_inventory / contracts / mechanics / cross_reference_map / deferrals: <handle or omitted reason>
- Decisions: <#id · status · has-authority? ...>
- Stance-coverage check: <every system-view stance has exactly one row: pass | gaps/dupes listed>
- Authority check: <every verdict cites authority: pass | rows missing authority>
- Nothing-decided-twice check: <no shape re-narrated, no term redefined: pass | violations>
- Open / Critical rows: <the rows a stakeholder must weigh>
```

The view body opens with a "what this view owns" note and a pointer up to system-view and sideways to ontology-view, then the decision-inventory table (# · decision/stance · verdict · status · authority), the contracts sections, the mechanics sections, and a closing cross-reference map.
</output-contract>

<quality-bar>
A successful run must:

- give every load-bearing decision exactly one verdict with status and a cited authority,
- resolve every system-view-named stance to exactly one row,
- present schemas, enums, and failure codes with sources,
- explain mechanics by reference to ontology-view terms, not by redefining them,
- re-narrate no shape and redefine no term,
- mark CRITICAL the rows that block the core thesis,
- distinguish source-backed verdicts from inference,
- preserve seed status until live examples and Experiment Harness evidence support promotion.
</quality-bar>

<anti-patterns>
Avoid:

- re-telling the shape story (that is system-view; point up),
- redefining a term owned by ontology-view,
- a verdict with no authority citation,
- leaving a system-view stance with no row, or answering one stance in two rows,
- inventing a new stakeholder-altitude stance here instead of in system-view,
- marking a thesis-blocking gap as merely OPEN when it is CRITICAL.
</anti-patterns>

<observability>
Record: target boundary, decision count by status, rows missing authority, system-view stances resolved vs orphaned, duplicate-verdict violations, term-redefinition violations, shape-renarration violations, and user correction signals.
</observability>

<promotion-gate>
Promotion requires Sigil Development review plus Experiment Harness evidence for:

- one target with a full RESOLVED/OPEN/CRITICAL spread,
- one example where every system-view stance resolves to exactly one row,
- one contracts section with sourced schemas and a failure-code family,
- one validation pass confirming authority coverage and nothing-decided-twice,
- one blocked/flagged example for a stance with no authority.
</promotion-gate>
</content>
