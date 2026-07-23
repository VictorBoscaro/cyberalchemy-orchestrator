---
name: discovery-writing
description: How to write a discovery document covering problem space, design decisions, and implementation detail. Use when authoring or restructuring a feature discovery at a pipeline-visible discovery path or any discovery-stage design document. Not for implementation plans or task lists.
---
# Discovery Writing

> Ported from ZefraHub (`.claude/skills/custom/discovery-writing.md`) 2026-07-14 and adapted to this repository's corpus, vault paths, decision register, OQ IDs, connections, versioning, and pipeline-visible paths.

## Purpose

A discovery captures the problem space, design decisions, and enough detail for an agent to write an implementation plan. It is **not a task list**. A discovery answers "what are we changing and why" — an implementation plan answers "how, step by step."

If the output of this session is a list of tasks, you are writing an implementation plan, not a discovery.

---

## File Location (pipeline-visible)

Write application discoveries to `docs/features/<feature>/discovery/<slug>.md` and knowledge discoveries to `vault/discovery/<topic>-definitions/<slug>.md`. These are the only two target shapes this skill and the `domainspec-discovery-writer` accept. A different path requires changing the owning pipeline/agent contract first; a changelog note is not an override. If a SPEC.md already links an Authority path, keep that link resolvable when moving files.

---

## Frontmatter Template

Use this repository-local contract:

```yaml
---
tags: [<feature>, <domain keywords>]
node_type: discovery
is_session: false
layer: [ontology | architecture | domain | application | external — what applies]
nature: [explanatory, reference, technical — what applies]
status: active
veracity: <low|medium|high>     # evidence quality
conviction: <low|medium|high>   # decision confidence
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

The owner handle is a required briefing input. Do not infer it from Git authorship or a previous
document; refuse authoring when it is absent.

---

### 1. Business Context

Open the section with one sentence anchoring this work to the repo's overall goal. Resolve the
project overview that actually exists (this repository currently uses root `README.md`) and compute
the relative Markdown link from the target file; never copy a fixed relative path.

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

Diagrams are embedded in the section they explain, not collected at the end: data model as one `classDiagram` (field-level `%%` comments for nullability/ownership semantics), each non-trivial flow as a `sequenceDiagram` with `autonumber`, boundary/scope contrasts as a two-subgraph `flowchart` with a labeled dashed edge for the join key.

---

### Open Questions

Collect unresolved items after the detailed specifications. Use numbered `OQ-<prefix>N` entries,
each with a bold **Question:**, **Recommendation:** and named settlement stage. Questions are closed
by amendment, never silently deleted.

---

### Decisions Baked In (required when the session ratified decisions)

A decision register: a table `| <P>D-N | Decision | Where |` — one row per design decision the document commits to, `Where` pointing at the owning §section. Pick a per-doc ID prefix (OD, WD, …) and reference decisions by ID throughout the body, not by restating them. These IDs are load-bearing: the downstream SPEC's Authority line locks them and its OD-Trace table must resolve every one to an aspect block.

Once a SPEC cites this document's version, the register is **locked**: never edit or renumber a locked row. Decisions ratified after the lock go in a `### Post-vX.Y.Z amendments` table below it as `DD-N | Decision | Where | Amends / motivated by`; each DD must cite the section it amends, the gap that motivated it, and which locked decisions remain untouched.

---

### Connections

A table `| Document | Type | Description |` of typed edges to related docs (`derives-from`, `cites`, `created-by`, `modified-by`, `supersedes`, …): the predecessor discovery, sibling discoveries the seam touches, source findings, any derived child. Edges are bidirectional: when this doc declares an edge to another, add the inverse row to that document (a patch-level version bump + changelog entry there).

The writer is authorized to edit only the user-confirmed discovery target. Record required inverse
edge updates as pending follow-up paths in the completion report; do not mutate linked documents
without their own explicit authorization.

---

### Flow Diagram, Changelog, and Source Footer

After `Connections`, place `## Flow Diagram`, then `## Appendix — Changelog`. When the confirmed
provenance mode requires one, the final content is the **Source dispatch** or **Source basis**
footer. This is the canonical ending order. The diagram is created before review and synchronized
after remediation; the changelog and optional footer remain last.

---

## Quality Checks Before Finishing

- [ ] Objective written before any other section; Status/Owner(/Companion) block present
- [ ] Every item in "What's broken" has a specific file location and the snapshot is dated
- [ ] "What stays" is non-empty and names the owning doc for every shared concept
- [ ] Core concepts have stable PascalCase names (and meta-types where clear)
- [ ] Every ratified decision has an ID, a `Where` §, and is cited by ID in the body
- [ ] Open questions have IDs, recommendations, and settlement stages — or the section says exactly `No open questions.`
- [ ] Connections table present; pending inverse edges reported without out-of-scope writes
- [ ] Version bumped ⇒ changelog entry written (with the locked-decisions statement)
- [ ] No implementation steps disguised as design decisions — if it's "do X then Y", it belongs in an implementation plan
- [ ] File is at a pipeline-visible path (`docs/features/<feature>/discovery/<slug>.md` or `vault/discovery/<topic>-definitions/<slug>.md`)
- [ ] Every invoked probe passed the Probe Proposal Gate; accepted/rejected improvements and reasons are present in the completion report
- [ ] Independent Review Loop (below) reached `NO_OBJECTION` from every confirmed reviewer in one round, or stopped honestly at the confirmed round ceiling with residue reported
- [ ] Flow Diagram Gate (below) executed — flow diagram present and synchronized with the reviewed body

---

## Orchestration and Confirmation

Discovery authoring uses the two-level planning model in
`.claude/skills/domainspec-subagents-strategy/SKILL.md`. The discovery orchestrator owns both
proposals and the human gates; the discovery writer never changes the confirmed topology.

The `StructuralGraphProposal` resolves the number of probe slots and review seats, their
connections, whether any group uses `robot-talks`, the interaction mode, the maximum review rounds,
and the confirmation mode. The `ConcreteDispatchProposal` then resolves every agent name,
role/lens, initial prompt, source boundary, model/budget, output contract, tool/skill profile,
reviewer instantiation rule, and retry limit. All potential seats are declared before execution. An
unused optional probe slot is not spawned; changing a seat or lens later requires a new proposal
revision and the applicable gate.

For every review group with two or three seats, the concrete proposal includes a P5 tension matrix:
one row per reviewer pair, a named disagreement axis, the question likely to split them, and each
seat's predicted position. Complementary labels alone are not tension. The matrix must make overlap
visible and explain why one reviewer cannot subsume another.

Before fine confirmation, a read-only capability reviewer checks each task against its proposed
tool/skill profile. Its task digest and tool-profile digest are part of the concrete proposal. Tool
names in agent frontmatter are adapter-level grants; the proposal also states the logical
capabilities and any restricted command classes. `Bash` never means unrestricted shell by
implication.

Every resolved concrete field records `ResolutionProvenance`: `user_set`, `recipe_default`,
`skill_constraint`, `orchestrator_inferred`, or `capability_reviewer_amendment`, plus a source
reference or digest and a short reason. A structural change invalidates the concrete and final
confirmations. A concrete-only change invalidates final confirmation. Retry creates a new attempt
under the same confirmed revision; it does not silently change the plan.

Supported confirmation modes:

- `structure_and_final`: confirm structure, resolve the concrete plan, then confirm it.
- `final_only`: show the structure as context and require only confirmation of the complete concrete
  plan.
- `structure_only`: authorize continued planning only. It never authorizes probes, writing, review,
  promotion, or any other execution.

Until durable gate receipts exist, preserve proposal revision IDs, SHA-256 digests, explicit user
acknowledgements, and the capability-review reference in the completion report. Do not describe a
chat acknowledgement as a bus receipt.

---

## Evidence Acquisition — Probe Proposal Gate

Use a probe only for a bounded information gap that can change a claim, decision, boundary, or open
question. Ordinary repository reads, exact lookups, link checks, and validation commands are not
probes. Do not use a probe merely to make the discovery look researched.

One probe-budget slot includes at most one validator helper plus one acquisition. A budget of `0`
forbids both proposal helpers and acquisitions; turn unresolved evidence gaps into Open Questions.
Once all slots are consumed, do the same. Report supplied, consumed, and remaining slots.

For each confirmed probe slot that the orchestrator proposes to use, spawn one small read-only
helper to evaluate the proposal. Give it the current
discovery objective, the precise information gap, the proposed question, intended sources, and
budget. Do not give it the answer the writer hopes to obtain. Require this response:

```text
Verdict: RUN | IMPROVE | SKIP
Necessity: <what decision the probe can change, or why it is redundant>
Suggested question: <smallest falsifiable/retrievable question>
Suggested scope: <sources, exclusions, and stopping condition>
Risk: <duplication, authority, cost, or confirmation-bias risk>
```

The orchestrator decides `ACCEPT`, `PARTIAL`, or `REJECT` for the suggested improvement and records a
one-line reason. `SKIP` is advisory, not a veto, but running despite it requires naming the decision
that still needs evidence. Keep this decision in the completion report; put it in the discovery only
when it materially qualifies the evidence.

Then use the narrowest available acquisition surface:

1. Use a real, authorized probe tool when the runtime exposes one.
2. Otherwise, use one bounded read-only Task helper and label it `helper_probe`; this is not evidence
   that the bus-backed `reference-probe` runtime exists.
3. Never simulate receipts, bus persistence, reviewer consensus, or canonical authority.

Require the probe to return sources/locations, findings, limitations, and an explicit no-result
outcome. The orchestrator checks material references and decides what enters the writer briefing;
the writer remains responsible for Claim <= Proof in the artifact.

---

## Flow Diagram Gate

After the body passes the quality checks, create or update a `## Flow Diagram` section containing one
Mermaid overview and a paragraph of at most four sentences. The diagram must use only concepts from
the body. It must exist before the first independent review so reviewers inspect the complete
artifact; after every remediation before the terminal round, synchronize it before starting the
next review round. Keep `Appendix — Changelog` and the confirmed optional provenance footer after
it.

The writer produces and synchronizes this section. A separate diagram helper requires its own
predeclared seat and tool profile. The requirement is a synchronized diagram, not a particular
model or helper.

---

## Independent Review Loop

The orchestrator reads `.claude/skills/review/SKILL.md` before launching reviewers. After the
complete draft and Flow Diagram exist, launch the confirmed two or three fresh read-only reviewers
independently. Reviewers in a round receive the same frozen digest and never receive another
reviewer's return.

This bounded helper topology is authorized by the scoped discovery-authoring exception in
`.claude/skills/domainspec-subagents-strategy/SKILL.md` P11. Any wider fan-out, persisted review
artifact, or work beyond the discovery returns to the normal confirmation/register/close lifecycle.

Launch all reviewers in a round together when the tool supports parallel tasks.

- **Content/fidelity lens:** attack contradictions with sources or governing documents,
  unsupported decisions, missing promised scope, undefined concepts, unresolved IDs, and
  claim-greater-than-proof.
- **Form/operability/reference-integrity lens:** attack mandatory structure, clarity for a
  fresh reader, executable guidance, path/link validity, table/diagram legibility, ownership drift,
  and whether the discovery can feed a SPEC without invention.
- **Optional architecture/provenance lens:** when the structural proposal contains a third seat,
  attack ownership boundaries, graph semantics, invalidation, gate/provenance claims, capability
  minimization, and reuse versus duplication of adjacent systems.

Each reviewer reads the entire current discovery and material sources. Require:

```text
Revision digest: sha256:<digest supplied by the writer>
Verdict: NO_OBJECTION | OBJECTIONS
Objections:
1. <severity> — <file/section and quoted evidence> — <problem> — <concrete fix>
Survival evidence: <required for NO_OBJECTION: attempted attacks and why the artifact survived>
Checks performed: <reads/commands>
```

Compute the digest before launching the group and require every reviewer to echo it. A missing or
mismatched digest
or a `NO_OBJECTION` without concrete survival evidence is an insufficient review and counts as an
objection. When every return has zero objections, the orchestrator explicitly checks the review skill's
all-zero-findings red flag: each lens must name its attempted attacks and evidence of survival before
the group can yield `REVIEW_CLEAN`.

After the round barrier, the orchestrator sends all independent returns together to the writer. For
each objection before the terminal round, the writer records `ACCEPT`, `PARTIAL`, or `REJECT` with
a one-line, evidence-based reason, then rewrites every accepted/partial item. Rejection is allowed;
silent discard is not. Re-run deterministic checks and synchronize the Flow Diagram before the next
round.

Use fresh reviewer activations on every round, with the exact confirmed seats and lenses. The round
machine is: freeze artifact bytes and digest; launch the sealed group; close the all-reviewer
barrier; validate and batch the returns; let the writer disposition and remediate; run checks and
synchronize the diagram; freeze the next digest; then launch the next fresh activations. Reviewers
receive the artifact and confirmed sources, never peer returns. Stop early
only when every reviewer independently returns `NO_OBJECTION` against the same frozen revision. Run
at most the confirmed ceiling, which must be between one and five rounds. The ceiling round is
terminal: if any reviewer objects, do not edit the reviewed revision. Record accepted objections as
residue, return the reviewed file digest plus `REVIEW_LOOP_CEILING`, and never report a clean review.

---

## Provenance (repo addition)

When the discovery derives from a registered research dispatch, end the document with a **Source
dispatch** footer containing its exact dispatch id and exact findings path supplied in the briefing.
The concrete plan also carries the exact optional research source path when one is used; never
derive it by changing the findings basename. When there is no registered research dispatch, the
concrete plan explicitly selects either a final `**Source basis:**` footer with exact durable source
links or no provenance footer. Never fabricate a dispatch ID.

A verified probe may support a decision only when the owning section and decision-register row cite
the durable source/location, state the probe mode (`tool_probe` or `helper_probe`), and preserve
material limitations. Otherwise it may only qualify a claim or Open Question. Never fabricate a
decision from an uncited helper return.
