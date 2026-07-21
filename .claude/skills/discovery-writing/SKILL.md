---
name: discovery-writing
description: How to write a discovery document — problem space, design decisions, and implementation detail. Use when authoring or restructuring a feature discovery (docs/features/<feature>/discovery/<slug>.md) or any discovery-stage design document. Not for implementation plans or task lists.
---
# Discovery Writing

> Ported from ZefraHub (`.claude/skills/custom/discovery-writing.md`) 2026-07-14; adapted for zagr-plataforma (corpus frontmatter, this repo's vault paths, Grep/Read instead of GitNexus) and extended with the corpus + pipeline conventions the original omitted (decision register, OQ IDs, connections, versioning, pipeline-visible paths).

## Purpose

A discovery captures the problem space, design decisions, and enough detail for an agent to write an implementation plan. It is **not a task list**. A discovery answers "what are we changing and why" — an implementation plan answers "how, step by step."

If the output of this session is a list of tasks, you are writing an implementation plan, not a discovery.

---

## File Location (pipeline-visible)

Write application discoveries to `docs/features/<feature>/discovery/<slug>.md` and knowledge discoveries to `vault/discovery/<topic>-definitions/<slug>.md` — these are the ONLY two paths the DomainSpec Step 0 gate globs (`domainspec-pipeline` step 3d, `domainspec-spec-feature` step 0.3). A discovery anywhere else (feature root, `discoveries/` plural) halts the pipeline with "No discovery exists for <feature>". If a SPEC.md already links an Authority path, keep that link resolvable when moving files.

---

## Frontmatter Template

Match the existing corpus convention (exemplars: `docs/features/zagr-marketplace/discoveries/marketplace-without-payment-api/DISCOVERY.md`, `docs/dlocal-integration/DISCOVERY.md`):

```yaml
---
tags: [<feature>, <domain keywords>]
node_type: discovery
is_session: false
layer: [architecture, domain | market | application — what applies]
nature: [explanatory, reference, technical — what applies]
status: active
veracidade: <low|medium|high>   # evidence quality
convicção: <low|medium|high>    # decision confidence
version: 0.1.0
last_updated: <YYYY-MM-DD>
---
```

---

## Mandatory Document Structure

Sections must appear in this order. Do not skip or reorder them.

### Objective (≤3 sentences, required first)

What is being changed and what the end state looks like. No motivation here — that goes in Business Context.

**Quality gate:** If you cannot write this in 3 sentences, the scope is unresolved. Stop and clarify with the user before continuing.

Immediately below the Objective, add a bold-label block: `**Status:**` (version + one-line provenance), `**Owner:**` (@handle), and, when a sibling discovery exists, `**Companion:**` — a relative link plus one sentence declaring the ownership split: what the companion owns and that this doc treats it as defined. If the companion is version-locked, pin the version.

---

### 1. Business Context

Open the section with one sentence anchoring this work to the repo's overall goal — link [docs/PROJECT-OVERVIEW.md](../../docs/PROJECT-OVERVIEW.md) (or the project's equivalent) so a reader can trace why this feature serves the project at all.

Three subsections, all required:

**Why now** — The triggering condition: a business rule that cannot be expressed, a failure in production, an architectural constraint that blocks future work. One concrete paragraph. No speculation.

**What's broken (as of <date>)** — Enumerate each problem with a specific location (`file.ts:line` or `ClassName.method` or doc §section). A problem without a location is unverified. Date the snapshot.

**What stays the same** — Explicit scope boundary: list the assets, models, and behaviors that are out of scope. An unnamed boundary is an unbounded scope. When an in-scope concept is **owned by another document or sibling feature**, name the owning doc with a relative link and the seam by which this feature touches it (event, read model, mapping); every later mention cites `[link] §N.N` instead of restating the definition. One owner per concept — this doc may declare a seam contract against it, never a second definition. An unlisted shared concept invites duplicate registry entries downstream.

---

### 2. Core Concepts

Introduce the new abstractions and key design decisions. Short code sketches are appropriate here when they communicate the contract clearly. This section answers "what and why" — save step-by-step detail for later sections.

Each concept should have:
- A stable **PascalCase name** — it becomes the SPEC concept-table entry and the registry ID `<feature>.<ConceptName>` (synced to `docs/registry.md`), so it must survive discovery → spec unrenamed
- What it does (one sentence)
- Why this design was chosen over alternatives (if non-obvious)
- Where the shape is already clear, the meta-type per `domainspec/TAXONOMY.md` (Entity, Value Object, Enum, Operation, Query, Rule, Policy, Workflow, Interface, Event, Mapping, State Machine) so the spec-writer knows which aspect file receives it

---

### 3–N. Detailed Specifications

One section per area of change. Typical sections (use what applies):

- **Data model changes** — schema diffs, migration strategy, index changes
- **Interface / API contracts** — new base classes, method signatures, port definitions
- **Service / execution flow** — sequence of operations, what changes vs. today (a before/after table is often clearest)
- **Phases and gates** (when the discovery stages downstream work) — a roadmap diagram plus an exit-criteria table (`| From → To | Mandatory criteria |`) with an explicit `any → ESCAPE` row; escape hatches must name concrete alternatives, not "reassess". State the honest-gate rule: what it costs to discover the failure now vs. at the next phase.
- **Cleanup** — what gets deleted, with location and reason
- **Open questions** — numbered `OQ-<prefix>N`, each with a bold **Question:** and **Recommendation:** pair and a named settlement stage ("Settle in SPEC" / plan / implementation). The recommendation must be adoptable as-is: the spec-writer ratifies within its bounds without a user round and records `OQ-N ratified → <choice>`. Questions are closed by amendment (a DD-N citing the OQ), never silently deleted.

Diagrams are embedded in the section they explain, not collected at the end: data model as one `classDiagram` (field-level `%%` comments for nullability/ownership semantics), each non-trivial flow as a `sequenceDiagram` with `autonumber`, boundary/scope contrasts as a two-subgraph `flowchart` with a labeled dashed edge for the join key.

---

### Decisions Baked In (required when the session ratified decisions)

A decision register: a table `| <P>D-N | Decision | Where |` — one row per design decision the document commits to, `Where` pointing at the owning §section. Pick a per-doc ID prefix (OD, WD, …) and reference decisions by ID throughout the body, not by restating them. These IDs are load-bearing: the downstream SPEC's Authority line locks them and its OD-Trace table must resolve every one to an aspect block.

Once a SPEC cites this document's version, the register is **locked**: never edit or renumber a locked row. Decisions ratified after the lock go in a `### Post-vX.Y.Z amendments` table below it as `DD-N | Decision | Where | Amends / motivated by`; each DD must cite the section it amends, the gap that motivated it, and which locked decisions remain untouched.

---

### Connections

A table `| Document | Type | Description |` of typed edges to related docs (`derives-from`, `cites`, `created-by`, `modified-by`, `supersedes`, …): the predecessor discovery, sibling discoveries the seam touches, source findings, any derived child. Edges are bidirectional: when this doc declares an edge to another, add the inverse row to that document (a patch-level version bump + changelog entry there).

---

## Quality Checks Before Finishing

- [ ] Objective written before any other section; Status/Owner(/Companion) block present
- [ ] Every item in "What's broken" has a specific file location and the snapshot is dated
- [ ] "What stays" is non-empty and names the owning doc for every shared concept
- [ ] Core concepts have stable PascalCase names (and meta-types where clear)
- [ ] Every ratified decision has an ID, a `Where` §, and is cited by ID in the body
- [ ] Open questions have IDs, recommendations, and settlement stages — not just questions
- [ ] Connections table present; inverse edges added to the linked docs
- [ ] Version bumped ⇒ changelog entry written (with the locked-decisions statement)
- [ ] No implementation steps disguised as design decisions — if it's "do X then Y", it belongs in an implementation plan
- [ ] File is at a pipeline-visible path (`docs/features/<feature>/discovery/<slug>.md` or `vault/discovery/<topic>-definitions/<slug>.md`) — or the operator-designated path, with the deviation noted in the changelog
- [ ] Review Gate (below) run — the reviewer's accepted findings applied
- [ ] Final Step (below) executed — flow diagram appended

---

## Final Step — Mermaid Flow Diagram (mandatory, last action)

After the Review Gate fixes are applied and the Quality Checks pass, dispatch a **Sonnet subagent** to append a `## Flow Diagram` section to the discovery file containing a mermaid overview diagram of what the discovery describes (this is the whole-document overview; the per-section inline diagrams above remain mandatory and are not a substitute).

Do not invoke it before the body is complete, do not skip it. **Exception:** if you are running as a subagent without access to the Agent tool, produce the diagram yourself as the last action instead — the requirement is the diagram, not the dispatch.

Use the Agent tool with `subagent_type: "general-purpose"` and `model: "sonnet"`. The prompt must be self-contained — the subagent has not seen this conversation:

> Read the discovery at `<absolute path to the .md file>`. Append a new section titled `## Flow Diagram` at the end of the file. The section must contain:
> 1. One mermaid diagram (`flowchart`, `sequenceDiagram`, or `stateDiagram-v2` — pick whichever best fits the discovery's nature) that captures the system, flow, or state transitions the discovery describes. Nodes/edges should mirror the entities and relationships named in the discovery body — do not invent new concepts.
> 2. A short paragraph (≤4 sentences) below the diagram explaining what the diagram shows and how to read it, in the same vocabulary the discovery uses.
>
> Constraints: edit the file in place using Edit (do not rewrite it). Do not modify any existing section. Do not add the diagram if a `## Flow Diagram` section already exists — update it in place instead.

---

## Review Gate (mandatory, after the body is written)

Spawn ONE reviewer subagent — attack discipline per the `review` skill (`.claude/skills/review/SKILL.md`), but run as a plain helper: **no dispatch row, no ledger registration**. It reviews EVERYTHING and returns numbered apontamentos (exact section, what is wrong, concrete fix), covering both dimensions:

- **Content** — inconsistencies and gaps in the actual content: claims that contradict the source findings/evidence or each other, missing areas the scope promises but no section covers, decisions without rationale, open questions without recommendations, concepts used but never defined, numbers/IDs that don't resolve.
- **Form** — organization (section order per this skill), clarity for a reader who hasn't seen the sources, Business Context sufficiency including the repo-overall-goal link, table/diagram legibility, and whether the relative links resolve on disk.

Apply the accepted apontamentos before the Final Step; rejected ones need a one-line reason in your report. When running as a subagent without the Agent tool, return the draft and ask the invoking strategist to run this gate.

---

## Provenance (repo addition)

When the discovery derives from a registered research dispatch, end the document with a **Source dispatch** footer: dispatch id, link to the `research/findings.md` it builds on. Do not fabricate decisions the findings don't support — if the findings don't surface a decision, say so in an open question instead.
