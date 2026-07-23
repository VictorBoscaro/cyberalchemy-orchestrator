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
version: 0.1.0                  # new targets only; semver-bump existing targets
last_updated: <YYYY-MM-DD>
---
```

---

## Mandatory Document Structure

Sections must appear in this order. Do not skip or reorder them.

### `## Objective` (exact H2, ≤3 sentences, required first)

What is being changed and what the end state looks like. No motivation here — that goes in Business Context.

**Quality gate:** If you cannot write this in 3 sentences, the scope is unresolved. Stop and clarify with the user before continuing.

Immediately below the Objective, add the exact non-empty line
`**Status:** v<frontmatter-version> — <provenance text>`, then `**Owner:**` (@handle), and, when a
sibling discovery exists, `**Companion:**` — a relative link plus one sentence declaring the
ownership split. Use `0.1.0` only for a new target. For an existing target, preserve locked
decisions and apply the appropriate semver bump; the Status and newest changelog versions must
equal frontmatter.

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

When a checked source/evidence packet is present, derive all three Business Context subsections
from it and preserve material limitations. Do not substitute unsupported briefing intuition.

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

### Decisions Baked In

A decision register table is always present with exact header `| ID | Decision | Where |`. Add one row per design
decision the document commits to, with `Where` pointing at the owning §section. When no decision
was ratified, keep the table and use the exact `| — | No decisions ratified. | — |` row. Pick a
per-doc ID prefix (OD, WD, …) and reference actual decisions by ID throughout the body, not by
restating them. These IDs are load-bearing: the downstream SPEC's Authority line locks them and
its OD-Trace table must resolve every one to an aspect block.

Once a SPEC cites this document's version, the register is **locked**: never edit or renumber a locked row. Decisions ratified after the lock go in a `### Post-vX.Y.Z amendments` table below it as `DD-N | Decision | Where | Amends / motivated by`; each DD must cite the section it amends, the gap that motivated it, and which locked decisions remain untouched.

---

### Connections

A table `| Document | Type | Description |` of typed edges to related docs (`derives-from`, `cites`, `created-by`, `modified-by`, `supersedes`, …): the predecessor discovery, sibling discoveries the seam touches, source findings, any derived child. Edges are bidirectional: when this doc declares an edge to another, add the inverse row to that document (a patch-level version bump + changelog entry there).

The writer is authorized to edit only the user-confirmed discovery target. Record required inverse
edge updates as pending follow-up paths in the completion report; do not mutate linked documents
without their own explicit authorization.

---

### Flow Diagram, Changelog, and Source Footer

After `Connections`, place `## Flow Diagram`, then `## Appendix — Changelog`. The Flow section
contains one Mermaid fence and a non-empty explanatory paragraph of at most four sentences. The
changelog uses exact header `| Version | Date | Changes |` and contains at least one row with
semantic version, real `YYYY-MM-DD` date, and non-empty change text. Put the newest row first; its
version equals frontmatter and the Status line. The confirmed provenance mode is exactly
one of:

- `dispatch`: the final non-empty line, outside code fences, is
  `**Source dispatch:** \`<dispatch-id>\` — [findings](<relative-path>)`.
- `basis`: the final non-empty line, outside code fences, is
  `**Source basis:** [<label>](<relative-path>); ...`, containing every and only the confirmed
  durable source-basis paths.
- `none`: neither provenance footer appears.

This is the canonical ending order. The diagram is created before review and synchronized after
remediation; the changelog and optional footer remain last.

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
- [ ] `validate-discovery.py` passed with the explicit confirmed provenance mode; its trailing-
  whitespace check covers tracked and untracked targets

The validator owns deterministic syntax and structural minima only. Reviewers still own semantic
questions: whether locations prove the stated breakage, PascalCase concepts are well chosen,
decision rows link to their true owning sections, source links appear in the true provenance-owning
claim/decision locations, connections are complete, and the Flow paragraph/diagram faithfully
represent the body.

---

## Orchestration and Confirmation

Discovery authoring uses the two-level planning model in
`.claude/skills/domainspec-subagents-strategy/SKILL.md`. The discovery orchestrator owns both
proposals and the human gates; the discovery writer never changes the confirmed topology.

This is an owner-directed bootstrap workflow because no LIVE `discovery` dispatch type exists.
Exactly one controlled writer may persist only the confirmed parent-owned discovery target and
return `WriterHandoff`; do not register it or misclassify it as research/review/experiment. If a
discovery dispatch type is ratified, formal register open/close becomes mandatory.

The bootstrap structural schema contains objective, confirmed target/owner, source and mutation
boundaries, exactly one writer, probe-slot budget, two or three isolated reviewer seats,
`robot_talks: false`, connections, review-round ceiling, budgets, and confirmation mode. The
bootstrap concrete schema contains every helper/writer/reviewer name, role/lens, immutable prompt
template and typed data slots, exact source path/hash bindings, requested provider/model/adapter,
budgets, output contracts, proposed capability profiles, reviewer instantiation/retry rules,
provenance mode, capability-review evidence, tension matrix, and resolution provenance.

The `DiscoveryBootstrapStructuralProposal` resolves the number of probe slots and review seats, their
connections, whether any group uses `robot-talks`, the interaction mode, the maximum review rounds,
and the confirmation mode. The `DiscoveryBootstrapConcreteProposal` then resolves every agent name,
role/lens, immutable `prompt_template`, source boundary and exact path-to-SHA-256 bindings,
`requested_provider`, `requested_model`, `requested_adapter`, budget, output contract,
`proposed_capability_profile`, reviewer instantiation rule, and retry limit. It includes the group
anti-bias axis, each seat's angle/position, and for each pair the predicted disagreement question,
positions, and evidence. All potential seats are declared before execution. An unused optional probe slot is
not spawned; changing a seat, lens, or prompt template later requires a new proposal revision and
the applicable gate.

Both bootstrap proposals are session-local workflow evidence, not dispatch projections and not
derived from a pending dispatch sheet. Declare
`projection_schema_version`, reject duplicate object keys, and use RFC 8785 JCS before SHA-256. If
a conforming JCS implementation is absent, the local digest is workflow evidence only, never
portable or durable. ACI `ConfirmedDispatch` / `DispatchSpec` own durable approval bytes and
receipts when available.

For every review group with two or three seats, the concrete proposal includes a P5 tension matrix:
one row per reviewer pair, a named disagreement axis, the question likely to split them, and each
seat's predicted position. Complementary labels alone are not tension. The matrix must make overlap
visible and explain why one reviewer cannot subsume another.

Before fine confirmation, a read-only capability reviewer checks each task against its
`proposed_capability_profile`. Embed its result, amendments, task digest, and profile digest in the
`DiscoveryBootstrapConcreteProposal`. Tool names in agent frontmatter are proposal-level adapter requests;
the proposal also states logical capabilities and restricted command classes. Effective grants,
model, and sandbox remain ACI/runtime-owned. Record `effective_enforcement` as `observable` or
`non_observable`. An observable semantic mismatch fails closed; when non-observable, report the
gap and never call requested values effective. `Bash` never means unrestricted shell by implication.

After capability review, run two independent check-tension helpers against the same canonical
concrete digest. Concrete confirmation requires PASS from both. If either fails, revise the
bootstrap proposal, regenerate and re-digest the affected projections, and run two fresh
independent checks.

Every resolved concrete field records `ResolutionProvenance`: `user_set`, `recipe_default`,
`skill_constraint`, `orchestrator_inferred`, or `capability_reviewer_amendment`, plus a source
reference or digest and a short reason. A structural change invalidates the concrete and final
confirmations. A concrete-only change invalidates final confirmation. Retry creates a new attempt
under the same confirmed revision; it does not silently change the plan.

Final confirmation freezes prompt templates, not future returns. Each downstream template declares
data-only slots with name, authorized producer, data type/schema, cardinality, byte/token ceiling,
purpose, and source/response schema. Instructions, authority, lenses, source boundaries, and output
contracts cannot be dynamic. For an unregistered workflow, the host may materialize current data
into a workflow-only `WorkflowInputManifest`, bind files as `{path, sha256}`, and digest it. ACI
alone owns a true `EffectiveInputArtifact`. Every registered topology needing post-confirmation
downstream input is `UNAVAILABLE` unless ACI/runtime persists and binds its manifest. The
unregistered bootstrap may use a manifest as workflow evidence only and cannot claim durable
binding. Changing an instruction, authority, lens, source boundary, or output contract invalidates
concrete confirmation.

Supported confirmation modes:

- `structure_and_final`: confirm structure, resolve the concrete plan, then confirm it.
- `final_only`: show the structure as context and require only confirmation of the complete concrete
  plan.
- `structure_only`: authorize continued planning only. It never authorizes probes, writing, review,
  promotion, or any other execution.

Until durable gate receipts exist, the orchestrator preserves proposal revision IDs, SHA-256
digests, explicit user acknowledgements, the embedded capability-review result, and the two
check-tension results in its final completion report. Do not describe a chat acknowledgement as a
bus receipt.

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
The scoped independent reviewer group must declare `robot_talks: false`. Robot-talks requires a
formal registered review topology, not this isolated helper loop.

Each isolated reviewer return is a non-deliverable internal contribution: do not persist,
independently publish, or independently consume it. Only the complete barrier batch may feed the
writer's next `WriterHandoff` and the orchestrator's final report. If any return must be persisted
or separately consumed, use a formal review dispatch.

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
mismatched digest, malformed verdict, missing required field, or `NO_OBJECTION` without concrete
survival evidence is `INSUFFICIENT_REVIEW`: it is neither an objection nor clean evidence. Retry
that seat against the same frozen digest and unchanged template/effective-input contract. A
protocol-failure retry increments only the seat's technical-attempt counter and does not consume a
substantive review round. The concrete proposal sets a maximum of one to three confirmed technical
attempts per seat. If any seat remains insufficient when its attempt limit is exhausted, the
barrier is incomplete; stop with `INSUFFICIENT_REVIEW` and do not disposition objections or claim a
clean/ceiling round. When every valid return has zero objections, the orchestrator explicitly
checks the review skill's all-zero-findings red flag: each lens must name its attempted attacks and
evidence of survival before the group can yield `REVIEW_CLEAN`.

After the round barrier, the orchestrator sends all independent returns together to the writer. For
each objection before the terminal round, the writer records `ACCEPT`, `PARTIAL`, or `REJECT` with
a one-line, evidence-based reason, then rewrites every accepted/partial item. Rejection is allowed;
silent discard is not. Re-run deterministic checks and synchronize the Flow Diagram before the next
round. The writer returns only a `WriterHandoff`: current digest, deterministic checks,
dispositions, mutations made, pending inverse-edge paths, and unresolved gaps. The orchestrator
alone owns the final completion report, probe ledger, review ledger, and terminal status.

Before every review launch, require a `WriterHandoff` that names the target digest and reports PASS
for every deterministic check. A missing PASS or failed check stops `VALIDATION_FAILED` with the
digest and gap; launch no reviewer.

Use fresh reviewer activations on every round, with the exact confirmed seats and lenses. The round
machine is: freeze artifact bytes and digest; launch the sealed group; close the all-reviewer
barrier; validate and batch the returns; let the writer disposition and remediate; run checks and
synchronize the diagram; freeze the next digest; then launch the next fresh activations. Reviewers
receive the artifact and confirmed sources, never peer returns. Stop early
only when every reviewer independently returns `NO_OBJECTION` against the same frozen revision. Run
at most the confirmed ceiling, which must be between one and five rounds. The ceiling round is
terminal: if any reviewer objects, do not edit the reviewed revision. Record accepted objections as
residue, return the reviewed file digest plus `REVIEW_LOOP_CEILING`, and never report a clean review.
Disposition every terminal objection without mutating the artifact: `ACCEPT`/`PARTIAL` becomes
residue, while `REJECT` retains its evidence-based reason.

Bootstrap completion emits workflow terminal status only and never simulates a ledger close:
`REVIEW_CLEAN` maps to future legal `resolved`; `REVIEW_LOOP_CEILING` to
`loop_ceiling_reached`; and `VALIDATION_FAILED`, `INSUFFICIENT_REVIEW`, or `UNAVAILABLE` to `error`.
Precedence is `error` over `loop_ceiling_reached` over `resolved`. Never write this workflow-close
metadata into the reviewed discovery bytes. If formal registration is later ratified, keep close
evidence in the ledger/separate completion record and verify the close append before final report.

---

## Provenance (repo addition)

The concrete proposal explicitly selects `provenance_mode: dispatch | basis | none`.

- `dispatch` requires an existing registered source packet, exact dispatch ID, and exact findings
  path; use the exact terminal Source dispatch syntax above.
- `basis` requires a checked durable source packet and one or more exact source-basis paths; use the
  exact terminal Source basis syntax above.
- `none` requires no registered findings source and forbids both source footers.

Every source is bound by explicit path→SHA-256 pair, never by position in an ordered tuple. An
optional research source is also an exact path→hash pair; never derive it by changing a findings
basename. Its link must occur in the substantive owning section before `## Connections`.
Deterministic validation can prove that exact path is linked there, but reviewers own whether that
section and the corresponding decision row are semantically the true provenance owners. Never
fabricate a dispatch ID.

A verified probe may support a decision only when the owning section and decision-register row cite
the durable source/location, state the probe mode (`tool_probe` or `helper_probe`), and preserve
material limitations. Otherwise it may only qualify a claim or Open Question. Never fabricate a
decision from an uncited helper return.

Pass validator source bindings as `path=sha256:<64-lowercase-hex>` for `--expected-source` and each
repeated `--source-basis` / `--research-source`. The validator recomputes every binding before
review. Provenance links themselves remain relative repository-contained Markdown links.
