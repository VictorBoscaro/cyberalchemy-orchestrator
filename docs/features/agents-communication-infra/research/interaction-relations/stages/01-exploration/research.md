---
tags: [agents-communication-infra, typed-graph, research, phase-1]
node_type: research
is_session: false
layer: [architecture, domain, application]
nature: [informational, evidence]
status: draft
veracity: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Basis — Exploration Returns

## Provenance

These four returns are preserved verbatim from the bound seats of dispatch
`2026-08-17-typed-interaction-graph-basis-exploration`. Ordering follows seat index. The parent has
added only this provenance wrapper and the return headings; no return text was synthesized or
rewritten here.

## Return 1: Wirth, Niklaus — local as-built corpus

# Local as-built corpus: interaction patterns

## Scope and proof rule

This is an inventory of repository-observable behavior, not a proposed type basis. “Declared” means
accepted or recorded as data; “documented” means instructed by a skill/specification; “compiled”
means transformed by executable code; “executed” requires a run record or durable run artifacts.
Schema acceptance is not execution.

The current ledger admits only connection objects `{from,to,type,loop_cap?}`, with types
`sequential | zig-zag | feedback`; `loop_cap` is the only relation-specific parameter
(`.agents/skills/register-dispatch/SKILL.md:84-92`; executable validator:
`.claude/skills/register-dispatch/append-dispatch.cjs:583-598`). Groups add a separate boolean
`robot_talks`, glossed only as discussion after parallel runs
(`.agents/skills/register-dispatch/SKILL.md:64-72`). Thus the declaration surface names topology and
one bound, but not payload, state transition, authority, convergence, or failure semantics.

## Surface/status crosswalk

| Surface | What it demonstrably carries | What it does not prove |
|---|---|---|
| Ledger `connections` | group endpoints, one of three labels, optional loop ceiling | delivery, scheduling, execution, protocol, or authority |
| Type skills | role-specific protocols, evidence discipline, convergence and human gates | that the current runtime interprets those protocols |
| `ProtocolRecipe` V1 | exact closed DAG with `depends_on | review_of | feeds | gates`, compiled deterministically to non-authoritative candidate data (`docs/features/agents-communication-infra/specs/protocol-compilation.md:163-203,246-260`) | confirmation or runtime execution; those are explicitly out of scope (`docs/features/agents-communication-infra/specs/protocol-compilation.md:26-40,531-556`) |
| `legacy-managed` compiler | turn-0 manifests and exact upstream output slots for `sequential` | progressive scheduling or any `zig-zag`/`feedback` interpretation |
| Work Bus discovery | proposed ordered, digest-bound delivery into a new invocation, with review/rework separated from routing authority (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:385-429,441-449`) | deployed behavior: the owning artifact is still `status: draft` (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:1-10`) |

## 1. `sequential`

### Minimal observable trace

| Dimension | As-built reconstruction |
|---|---|
| Entities/states | Upstream group seats have terminal `resolved` turns and registered producer-output receipts; a downstream group seat has a turn-0 input manifest. There is no compiled group-level state machine. |
| Transition | `resolved producer output(s) -> sequential handoff receipt -> downstream manifest slot -> separately bound downstream turn`. |
| Payload/evidence | Exactly one digest-bound output receipt per upstream seat, all using one data schema; the downstream slot preserves producer order, paths, hashes and binding identities (`implementations/server/runtime/dispatch_workflow.py:86-127,181-201`). |
| Direction/cardinality | Directed `from` group to `to` group. Cardinality is exactly the upstream seat count for each target seat; multiple incoming slots are sorted by declared source-group order (`implementations/server/runtime/dispatch_workflow.py:341-361`). |
| Ordering/concurrency | Group declaration order must be forward; seats inside a group are prepared as peers. The label does not say whether several predecessor groups are conjunctive, quorum-based, or merely historical order. |
| Authority | Transported output is evidence, not launch authority. Binding still requires an open parent dispatch and exact confirmed seat/prompt (`implementations/server/runtime/service.py:5564-5628`). No authority transfers from producer to consumer. |
| Guards | Existing handoff receipt; matching dispatch/capability/route/connection; resolved, byte-identical producer output; canonical order and schema consistency. Missing or stale evidence fails closed (`implementations/server/runtime/dispatch_workflow.py:97-127,181-187`). |
| Repetition/termination/failure | No edge repetition. Producer termination is `resolved`; missing handoff blocks compilation, reverse/duplicate edges fail, and source tampering fails (`implementations/tests/runtime/test_runtime_type_bootstrap_abuse.py:117-148,214-218`). |
| Actual status | Unit-tested compilation/materialization exists: the test supplies two producer receipts and verifies ordered bindings in the consumer manifest (`implementations/tests/runtime/test_runtime_type_bootstrap.py:295-356`). Progressive execution does not: the current research graph failed before opening because the compiler required the downstream handoff before upstream ran (`docs/decisions/typed-interaction-graph-research-execution.md:19-25`). |

**First underdetermination.** At the ledger object itself: `sequential` says neither which terminal
result releases the target nor what evidence is transferred. The compiler supplies one particular
answer, but only after an external actor pre-materializes the handoff. A preserved counterexample
shows that older retrospective rows use sequential edges to encode observed launch order only and
explicitly disclaim governed dependency/binding (`telemetry/agents/subagents-dispatch.yaml:5978-5984`).

## 2. Review

Review is a dispatch/workflow kind, not a ledger edge type.

### Minimal documented trace

| Dimension | As-built reconstruction |
|---|---|
| Entities/states | Frozen target corpus -> independent attacker returns -> synthesized candidate findings -> verifier dispositions -> accepted `review.md`. |
| Payload/evidence | Attackers send claims anchored in quotations; surviving findings carry file, quote, severity and proposed fix. Review persists one synthesis, not attacker transcripts (`.agents/skills/review/SKILL.md:22-40,128-176`). |
| Direction/cardinality | Canonical documentation uses 2–4 parallel attackers, one writer, skeptic verifier(s), optionally one downstream coverage auditor (`.agents/skills/review/SKILL.md:81-97`). |
| Ordering/concurrency | Attackers inspect the whole corpus independently; synthesis follows; writer and verifiers alternate; coverage follows verification. |
| Authority | Attackers and verifiers are read-only. Writer owns the report, verifier can refute a finding, and final approver accepts the change-request list. Parent authorship can force human/separate approval (`.agents/skills/review/SKILL.md:105-125`). Review findings do not themselves apply fixes. |
| Guards | Frozen target, declared lenses, evidence quotation, no self-verification, target/lens coverage. Zero findings by all attackers is a red flag, not automatic cleanliness (`.agents/skills/review/SKILL.md:128-157`). |
| Repetition/termination/failure | The writer–verifier exchange converges when a verifier raises no objection; loop cap is a ceiling. A verified MAJOR/CRITICAL yields `FIX`, which is still a resolved review deliverable (`.agents/skills/review/SKILL.md:118-137,186-193`). |
| Actual status | A governed 2026-08-15 review launched two independent read-only attackers with no connections and inline output (`.codex/workflow-inputs/2026-08-15-interaction-morphisms-initial-definitions-review/opening.json:4-34`) and closed `resolved` with two spawned explorers (`.codex/workflow-inputs/2026-08-15-interaction-morphisms-initial-definitions-review/close.json:2-13`). This witnesses attack execution, not the documented writer/verifier topology. |

**First underdetermination.** At `dispatch_type: review`: even a valid executed review can have
`connections: []`. The type does not determine lenses, independence, verifier presence, output
authority, or whether fixes are applied. Those are supplied by prompts, the review skill, and the
parent.

## 3. `zig-zag`

### Minimal observable trace (knowledge formation)

| Dimension | As-built reconstruction |
|---|---|
| Entities/states | Writer draft with pending gate cells -> three independent skeptic gate reports -> writer response matrix/revision -> the same skeptics confirm or reopen each disposition -> converged or exhausted candidate state. |
| Payload/evidence | Candidate IDs, objections, response status, evidence and resulting change. Dissent remains verbatim. |
| Direction/cardinality | One writer fans out to three skeptics, their reports fan in to the writer, then revised dispositions return to the original three. |
| Ordering/concurrency | Skeptic reports are independent within a round; writer revision follows all; original-skeptic confirmation follows revision. |
| Authority | Writer may revise findings; skeptics confirm/refuse dispositions; parent alone owns the shared loop counter; final auditor/parent owns terminal acceptance (`research/knowledge-formation/dispatch.yaml:291-311,473-490`). |
| Guards | One loop is the complete draft/gates/response/revision/reconfirmation sequence. Convergence requires all three original skeptics; silence is not confirmation (`research/knowledge-formation/dispatch.yaml:291-305`). |
| Repetition/termination/failure | Repeat up to global cap 2. Unresolved objections survive and may cause `MORE RESEARCH REQUIRED`/dissent exit; cap exhaustion stops remediation (`research/knowledge-formation/dispatch.yaml:301-311`). |
| Actual status | Durable ledger evidence records two completed rounds: loop 1 reopened candidates and loop 2 left one provisional survivor with the budget exhausted (`research/knowledge-formation/LEDGER.md:63-71,100-107`). This was parent-scheduled behavior, not compiled edge execution. The same ledger still contains a stale “awaiting L4” statement beside later success metadata (`research/knowledge-formation/LEDGER.md:3-5,113-123`), so terminal-state reconstruction is not cleanly single-sourced. |
| Compiled status | Explicitly rejected: the compiler accepts only `sequential` (`implementations/server/runtime/dispatch_workflow.py:314-324`), and tests preserve rejection of `zig-zag` and `feedback` (`implementations/tests/runtime/test_runtime_type_bootstrap_abuse.py:207-213`). |

A second executed/manual shape is materially different: backlog-skill work declares one author,
two reviewers, cap 3, and PASS by both on the same revision
(`.codex/workflow-inputs/2026-07-27-backlog-skill-work/structural-proposal-v1.json:43-63`). Its first
backward payload contains two `FIX` verdicts and concrete findings
(`.codex/workflow-inputs/2026-07-27-backlog-skill-work/skill-author-feedback-round-1.json:4-49`), and
round-2 manifests bind reviewers to changed artifact hashes
(`.codex/workflow-inputs/2026-07-27-backlog-skill-work/reviewer-usability-round-2-manifest.json:4-49`).
Yet its close record is `error` after two loops
(`.codex/workflow-inputs/2026-07-27-backlog-skill-work/dispatch-close.json:2-13`).

**First underdetermination.** At the connection object: `zig-zag + loop_cap` does not identify what
constitutes a round, whether fan-in is all/quorum, whether the same reviewers must return, what
convergence means, or who owns revisions and the counter. Knowledge formation adds a separate named
scheduler because the edge label is insufficient (`research/knowledge-formation/dispatch.yaml:273-305`).

## 4. `feedback`

### Smallest evidenced trace

| Dimension | As-built reconstruction |
|---|---|
| Entities/states | Reviewer finds missing/defective material -> parent sends a bounded remediation prompt -> responsible worker revises or rechecks -> reviewer may run again. |
| Payload/evidence | Verbatim feedback ask and, in richer manual manifests, findings plus the exact artifact revision/digest under review. |
| Direction/cardinality | Semantically backward from a checking stage to one or more responsible producers; neither target-seat selection nor fan-out/fan-in is fixed by the label. |
| Ordering/concurrency | Conditional after review; rework precedes re-review. |
| Authority | Reviewer requests correction but does not schedule a worker; proposed Work Bus ownership leaves reopening/routing to the orchestrator (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:421-429`). Text alone does not change official state (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:431-449`). |
| Guards/repetition | Material omission/failure triggers it; `loop_cap` bounds it at declaration level. Whether it creates a round, group version, or new stage execution is explicitly unresolved (`docs/features/agents-communication-infra/README.md:1277-1285`). |
| Termination/failure | Re-review acceptance, loop ceiling, dissent, or error are plausible documented exits; the label does not select one. |
| Actual status | No compiled feedback edge. Manual feedback is recorded: a review with only one reviewer group closed after two loops with two re-review prompts (`telemetry/agents/subagents-dispatch.yaml:1157-1172`). The close schema allows `feedback_prompts` as verbatim asks (`.agents/skills/register-dispatch/SKILL.md:140-145`) but does not require a matching declared edge. |

**First underdetermination.** At `feedback`: it does not say who is asked, what prior state is
superseded, whether this is correction, missing-evidence acquisition, retry, or a new generation.
The repository has feedback behavior without feedback edges, and a file named “feedback” inside a
declared zig-zag. The current name therefore does not delimit one behavior.

## 5. Robot-Talks

### Minimal observable trace

| Dimension | As-built reconstruction |
|---|---|
| Entities/states | Human-approved question/assumptions -> 3–5 concern-specific investigators -> independent reports -> parent tension synthesis -> human disposition. Optional peer challenge adds report exposure and responses before synthesis. |
| Payload/evidence | Reports with findings, gaps, local tensions and synthesis questions; optional ring responses; `findings.md` with evidence-backed tensions and human dispositions (`.agents/skills/robot-talks/SKILL.md:44-67,79-100`). |
| Direction/cardinality | Initial fan-out from question to investigators, fan-in to parent synthesis, then parent-to-human gate. Optional challenge may be pairwise/many-to-many; the boolean does not say which. |
| Ordering/concurrency | Exploration is parallel and independent; synthesis is later. In the concrete session, peer exposure followed independent reports, then parent synthesis, fresh review, editor/reviewer alternation and human gate (`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:30-39,69-85`). |
| Authority | Agents investigate; parent synthesizes; only the human classifies tensions as actionable/deferred/misinterpretation/uncertain. The workflow explicitly does not implement fixes by itself (`.agents/skills/robot-talks/SKILL.md:6-9,64-68`). |
| Guards | User supplies central question and challenged assumptions and approves decomposition before launch (`.agents/skills/robot-talks/SKILL.md:26-42`). Findings without evidence are speculation. |
| Repetition/termination/failure | No generic convergence algorithm. It terminates at human disposition; optional direct confrontation is bounded only by the session design. Timeout guidance is 30 minutes per agent (`.agents/skills/robot-talks/SKILL.md:93-102`). |
| Actual status | The concrete session records completed independent reports and cross-challenge, but remains `awaiting-human-gate` with two explicit pending choices (`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:1-5,87-100,129-135`). The standalone skill explicitly says it is not a governed dispatch and requires no runtime receipts (`.agents/skills/robot-talks/SKILL.md:93-100`). |

**First underdetermination.** At `robot_talks: true`: a boolean cannot determine pairing, exposure
order, number of exchanges, disagreement preservation, synthesis owner, or human gate. The current
compiler reads only group ID and agents when creating turn-0 launches
(`implementations/server/runtime/dispatch_workflow.py:278-303,357-418`); it contains no robot-talk
scheduler.

## Cross-pattern negatives and missing evidence

- A connection label is not a communication grant. The feature architecture explicitly says
  connections are scheduling instructions, not channels, and that retries, durable delivery,
  restart recovery and group state machines are absent (`docs/features/agents-communication-infra/README.md:96-119`).
- `sequential` has one tested evidence-materialization path but no demonstrated progressive
  same-dispatch scheduler; staging into separate dispatches is the current operational adapter.
- No repository evidence found of the current compiler executing `zig-zag` or `feedback`; executable
  tests require them to fail.
- No declared `feedback` edge was found in the inspected executed examples. `feedback_prompts` proves
  manual remediation requests, not edge execution.
- Canonical review documentation is richer than the demonstrated 2026-08-15 run. That run witnesses
  independent attack only; it does not prove synthesized/verifier/coverage scheduling.
- Robot-Talks demonstrates a lived protocol and durable artifacts, but explicitly outside the
  governed dispatch runtime; its concrete run has not crossed the human gate.
- The same name can cover different semantics (`zig-zag`), and the same apparent order can carry no
  dependency semantics (retrospective `sequential`). Any later typing decision must therefore be
  supported by state/evidence/authority witnesses, not current labels alone.


## Return 2: Milner, Robin — generative basis

# Generative basis for typed interaction graphs — local exploration

## Bounded answer

The smallest basis supported by the inspected local corpus is **four provisional semantic
relations**—`requires`, `supplies`, `assessed_by`, and `gates`—plus graph combinators and policies.
`sequential`, review, `zig-zag`, feedback, and robot-talks are reconstructible as protocols over
that basis; none is justified as a primitive edge type by the local traces. This is sufficiency for
the declared corpus, not universal completeness. `assessed_by` remains the weakest candidate: it
collapses if subject/version/criteria can be owned completely by assessment-node schemas without
loss of graph queries or validation.

## Observed traces before vocabulary

### 1. `sequential` as built

The current compiler accepts only `sequential`, requires the source group to precede the target in
declared group order, and rejects every other connection semantic
(`implementations/server/runtime/dispatch_workflow.py:314-340`). A sequential edge does more than
order work: its handoff must contain one terminal-output receipt per upstream seat, in seat order,
with one data schema; the bytes, digest, size, route and receipt are verified before the target gets
an input slot (`implementations/server/runtime/dispatch_workflow.py:86-210`). The positive test
demonstrates two producer outputs becoming an ordered, digest-bound consumer manifest
(`implementations/tests/runtime/test_runtime_type_bootstrap.py:295-356`). Missing or malformed
handoff evidence blocks compilation rather than waiting for the upstream work
(`implementations/server/runtime/dispatch_workflow.py:97-106`).

Therefore the observed `sequential` label currently bundles at least (a) causal readiness, (b)
exact evidence delivery, (c) all-source cardinality and ordering, and (d) a compiler limitation.
These are not one semantic relation.

### 2. Review

The review contract runs independent full-corpus attacks under distinct lenses, combines them,
subjects the synthesis to verification, optionally repeats revision, audits coverage, and keeps
final approval separate from coverage work (`.agents/skills/review/SKILL.md:52-79,81-123`). An
executed review records three independent attackers, literal verification, dropped out-of-scope
findings, a FIX result and final acceptance
(`docs/features/agents-communication-infra/reviews/2026-07-26-phase-a-authoring-review/review.md:10-25,76-95`).
Completion of an attack is thus not approval; a verifier's assessment is not final authority; and a
FIX verdict is still a resolved review.

### 3. `zig-zag`

The strongest trace is not the edge label but the separate knowledge-formation scheduler. One loop
is writer draft, three independent assessments, a writer response/revision, then confirmation by
the **original** assessors. Convergence requires all three to confirm every disposition; silence is
not confirmation. A parent-owned counter caps the shared loop budget and exhaustion preserves
unresolved material (`research/knowledge-formation/dispatch.yaml:291-311`). The ledger records two
different objection/remediation rounds and the resulting candidate withdrawals
(`research/knowledge-formation/LEDGER.md:61-81,100-107`). The declared connection merely points to
that scheduler (`research/knowledge-formation/dispatch.yaml:273-284`).

So `zig-zag` is an iterative review/revision/reconfirmation protocol. Bidirectionality alone would
lose participant continuity, per-objection response, convergence and bounded exit.

### 4. Feedback

The current research and review contracts use feedback only conditionally when a verifier finds
that upstream material may be missing (`.agents/skills/research/SKILL.md:80-96` and
`.agents/skills/review/SKILL.md:81-97`). Historical execution records also use `feedback` for
reviewer-requested editor fixes: a `reviewers -> editors` feedback edge has a loop cap and its close
row preserves the concrete correction ask (`telemetry/agents/subagents-dispatch.yaml:675-687,707-712`).
Those are related but not identical: one requests missing upstream evidence; the other requests a
new artifact version. The current compiler explicitly rejects `feedback` and `zig-zag`
(`implementations/tests/runtime/test_runtime_type_bootstrap_abuse.py:207-218`). There is therefore
no single deployed feedback-edge semantics to promote; the label denotes a conditional remediation
subprotocol.

### 5. Robot-talks

Robot-talks requires human approval of the decomposition, independent parallel reports, synthesis
of cross-layer contradictions and a human disposition gate; an optional ring adds direct challenges
and responses (`.agents/skills/robot-talks/SKILL.md:26-70,87-100`). In one preserved run, two
independent reports preceded mutual cross-challenge, parent synthesis, fresh review, alternating
editor/reviewer turns and a human gate
(`.codex/skills/write-need-driven-documents/robot-talks/2026-08-13-need-driven-skill-evolution/dialogue.md:30-45,69-85,111-119`).
Robot-talks is therefore a configurable protocol family. Its container is not essential to the
relation semantics: the skill explicitly allows it to run outside governed dispatch records.

## Endpoint model

The candidate graph should connect stable logical entities, not equate an agent process with a
workflow node. The local discovery already warns that an agent is not universally a workflow node
(`docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md:283-291`).
The minimal endpoint kinds needed here are:

- **occurrence** — a versioned work, assessment, decision or terminal occurrence, optionally bound
  to a seat/role and round;
- **evidence** — an immutable accepted artifact, message, result, dissent, assessment or decision;
- **slot/transition** — a declared input slot or state transition of an occurrence.

Agents, seats and groups remain authors/executors or coordination scopes. Retry may change the
physical agent instance without changing the logical relation.

## Candidate relation basis

### R1 — `requires`

- **Endpoints and direction:** accepted occurrence/evidence state → dependent occurrence or
  transition.
- **Payload/evidence:** exact source identity/version and the state predicate that must hold; no
  content delivery is implied.
- **Precondition:** the prerequisite exists and reaches the declared accepted state.
- **Semantic effect:** makes the target eligible with respect to this prerequisite; it neither
  launches the target nor grants visibility.
- **Authority effect:** none.
- **Terminal/failure:** unsatisfied remains waiting; impossible, cancelled or invalid prerequisite
  is classified by completion policy rather than silently skipped.
- **Legal composition:** transitive chains and joins are legal; same-round cycles are not. Repeated
  protocols use round-indexed occurrences, so a next-round requirement does not create an
  unversioned causal cycle.

This separates dependency from communication, a distinction the candidate architecture states
explicitly: dependency never implies permission to communicate
(`docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md:287-296`).

### R2 — `supplies`

- **Endpoints and direction:** accepted evidence → declared input slot of an occurrence.
- **Payload/evidence:** content-addressed artifact/message/result references, schema, provenance and
  dissent references where present.
- **Precondition:** accepted source receipt, authorized visibility, active source-to-slot mapping,
  matching schema and declared cardinality.
- **Semantic effect:** materializes exact evidence as consumer input. It does not imply that the
  consumer is otherwise ready or that the evidence is true, accepted as a verdict, or authoritative.
- **Authority effect:** none; publication or delivery does not confer decision authority.
- **Terminal/failure:** missing, stale, mismatched or unauthorized evidence yields no materialized
  input; identical redelivery is idempotent and conflicting redelivery fails.
- **Legal composition:** fan-out to several slots and fan-in from several sources are legal through
  explicit mappings; a consumer normally also has `requires` edges for its readiness conditions.

The future handoff contract likewise says a connection is topology only, requires an explicit slot
mapping, and carries result, dissent and provenance
(`docs/features/agents-communication-infra/specs/operations.md:853-878`).

### R3 — `assessed_by`

- **Endpoints and direction:** exact subject evidence/version/claim → assessment occurrence.
- **Payload/evidence:** subject identity, version, criteria or lens, disposition vocabulary and any
  objection/reply identities.
- **Precondition:** the subject is immutable and visible to an eligible assessor; independence or
  no-self-review constraints, when required, are coordination policies.
- **Semantic effect:** creates an obligation to produce a judgment *about that exact subject*, not
  merely to consume it. The resulting assessment is separate evidence and may itself become the
  subject of a response or confirmation assessment.
- **Authority effect:** none by default. An assessment can criticize, confirm, refute or remain
  unresolved without authorizing a transition.
- **Terminal/failure:** a valid disposition completes the assessment occurrence; absence, malformed
  evidence or an ineligible assessor yields no valid assessment, not tacit approval.
- **Legal composition:** one subject may fan out to independent assessments; their outputs may
  supply synthesis/revision; an objection may be assessed by a response and that response by a
  confirmation.

Collapse test: if exact subject/version/criteria and assessment validity can be owned entirely by
node/output schemas while retaining queries such as “who assessed which version?” and validation
such as no-self-review, this relation should be demoted to a node contract. The local corpus supports
its semantic distinction, but not yet its irreducibility as an edge.

### R4 — `gates`

- **Endpoints and direction:** accepted decision evidence → guarded transition, branch or terminal.
- **Payload/evidence:** authority identity, policy/version, decision/disposition, cause references
  and any quorum result.
- **Precondition:** the decision was produced under already-confirmed authority and satisfies its
  declared policy.
- **Semantic effect:** authorizes, denies or selects a transition. It does not transport the work
  product and does not make the decision maker authoritative by assertion.
- **Authority effect:** consumes pre-existing authority; the edge cannot create or transfer it.
- **Terminal/failure:** may release a branch, hold for a human, reject, or select a typed terminal
  outcome. Missing decision means waiting, never implicit approval.
- **Legal composition:** may follow assessments and control branch/repeat/terminal combinators;
  multiple gates require an explicit AND/OR policy rather than edge-order inference.

The distinction is witnessed by review's separate verifier, coverage-auditor and final-approver
roles (`.agents/skills/review/SKILL.md:99-111`) and robot-talks' human-only action disposition
(`.agents/skills/robot-talks/SKILL.md:64-70`).

## Composition operators, policies and runtime effects

| Construct | Classification | Local reason |
|---|---|---|
| causal ordering | relation + combinator | `requires` states a real prerequisite; `then(A,B)` is graph sugar that wires declared exits to entries. Linear declaration order alone is not semantics. |
| parallelism | graph combinator | Group agents run in parallel (`.codex/skills/register-dispatch/SKILL.md:64-72`); no new relation exists between siblings. Runtime realizes eligible occurrences concurrently. |
| branching | graph combinator controlled by policy/gate | Robot-talks' human gate selects actionable, deferred, misinterpretation or follow-up branches. |
| fan-out / fan-in | graph combinators | They duplicate mappings or join declared inputs; completeness/cardinality belongs to slot or coordination policy, as the sequential receipt's all-seat rule demonstrates. |
| repetition | graph combinator | `repeat(body, next-round bindings)` creates versioned occurrences. It is not an edge type. |
| `loop_cap` | policy | It bounds semantic rounds; knowledge-formation preserves unresolved evidence on exhaustion. |
| quorum | coordination policy | It decides how many eligible assessments/contributions satisfy a join; it is not pairwise communication. |
| convergence | completion policy/predicate | “All original assessors confirm every row” and “no objection” are different predicates over the same topology. |
| independent/sealed reveal | coordination and visibility policy | Independence is lost if peers see each other too early; delivery/reveal is separate from dependency. |
| retry | runtime effect | It re-attempts the same logical occurrence after technical failure; it must not consume a semantic review round. Review assigns retries to runtime (`.agents/skills/review/SKILL.md:116-123`). |
| cancellation | runtime command/effect plus terminal policy | Request, acknowledgement and terminal cancellation are distinct, and journal order resolves races (`docs/features/agents-communication-infra/specs/operations.md:880-922`). |

## Reconstructions

### `sequential(A, B)`

`then(A,B)` adds `A.accepted requires B`; each declared output of A `supplies` a mapped slot of B;
fan-in policy requires exactly the declared upstream sources. The current implementation's single
label is therefore an alias for this composition. Ordering without delivery and delivery without
ordering remain expressible separately.

### Review

The frozen target `assessed_by` each attacker under `parallel` plus an independence policy. Attack
outputs `supplies` a fan-in synthesis. The synthesized version `assessed_by` verifier(s); surviving
assessments supply the report or revision. Optional repeat handles revision. Coverage and final
decision evidence separately `gates` acceptance. This preserves that attacks, verification,
coverage and approval have different authority.

### `zig-zag`

Draft evidence `assessed_by` a fan-out of original reviewers; all assessments supply a join into a
response/revision occurrence. Each objection is an exact subject `assessed_by` the writer response;
the new version and response matrix then become subjects `assessed_by` the original reviewers.
`repeat` creates the next round until the convergence policy passes or `loop_cap` selects a typed
terminal. The downstream stage is released by a convergence/exit `gates` relation. No primitive
bidirectional edge is needed.

### Feedback

An assessment that requests correction or missing evidence `gates` a remediation branch. The
request `supplies` a new versioned upstream occurrence, which `requires` that accepted request; the
new output supplies the suspended downstream occurrence. `repeat` and `loop_cap` bound recurrence.
Because local uses request different work, `feedback` should remain a protocol alias parameterized
by remediation target and completion predicate, not a relation type.

### Robot-talks

Human approval `gates` a parallel independent exploration. Reports fan in to synthesis. When direct
confrontation is enabled, each report becomes a subject `assessed_by` selected peers and the
challenge/response outputs supply synthesis; the ring is an optional all-to-all subgraph, not an
edge kind. Fresh review repeats `assessed_by`/revision as needed. A final human decision `gates` one
of the four disposition branches. Persistence and whether the run is a governed dispatch are
container choices, not interaction relations.

## Removal tests

| Candidate removed | Observable behavior lost | Result |
|---|---|---|
| `requires` | Cannot represent a prerequisite that grants neither input nor communication; dependency collapses into delivery, contradicting the local separation of workflow and communication. | retain |
| `supplies` | Sequential becomes mere order: exact bytes, schema, provenance, dissent, visibility and slot cardinality disappear. | retain |
| `assessed_by` | Review, challenge and confirmation become indistinguishable from generic evidence consumption; exact subject/version and no-self-review cannot be validated from the graph. | provisionally retain; demote if node contracts preserve all of this |
| `gates` | A completed assessment or task becomes indistinguishable from an authorized decision, erasing human approval and typed denial/wait branches. | retain |
| `sequential` | Nothing is lost when expanded to `requires` + `supplies` + fan-in/`then`. | demote to alias |
| `zig-zag` | Nothing is lost when expanded to assessment, supply, repeat, continuity and convergence policies; the expansion reveals semantics hidden by the label. | demote to protocol recipe |
| feedback | Nothing stable is lost when expanded to a gate-selected remediation branch and repeat; its local instances request different remediation. | demote to parameterized protocol recipe |
| review | Its distinctive behavior survives as a recipe with roles, independence, assessment, synthesis and approval policy. | demote to protocol recipe |
| robot-talks | Its distinctive behavior survives as an approved parallel exploration plus optional confrontation, synthesis and human branch. | demote to protocol family |

## Counterexamples and limits

- The same drawn arrow `A → B` may mean only “B waits for A”, “A's bytes enter B”, “B evaluates
  A”, or “A's authorized decision releases B”. Treating all four as `sequential` erases observable
  failure and authority differences.
- A delivered critique does not authorize revision, and a verifier's completion does not equal
  acceptance. Conversely, a gate may authorize a branch without sending the guarded work product.
- A two-way arrow does not reconstruct knowledge-formation: it omits response rows, original-reviewer
  continuity, unanimity, silence handling, shared loop accounting and typed exhaustion.
- `robot_talks: true` cannot say whether there is a ring, which peers confront each other, whether
  synthesis follows or which human disposition ends the run.
- The V1 `ProtocolRecipe` already names `depends_on`, `review_of`, `feeds` and `gates`, but defines
  only their closed literals inside an acyclic graph, not executable semantics
  (`docs/features/agents-communication-infra/specs/protocol-compilation.md:198-203,244-258`). The
  four-way resemblance is precedent, not proof that this candidate basis is final.
- No local trace demonstrates arbitrary dynamic membership, negotiation, delegation of authority,
  private multi-party channels, unbounded sessions or every possible agent communication. Extension
  should add a new relation only when a new trace cannot preserve its observable semantics through
  these relations, combinators and policies; otherwise it should add a recipe or policy.

## Research handoff

The synthesis stage should test three unresolved points: whether `assessed_by` belongs on edges or
node contracts; whether `requires` may be derived safely for mandatory `supplies` slots while still
remaining explicit for pure prerequisites; and whether external systems provide a stronger witness
for another irreducible relation (for example delegation or negotiation). Until then, the defensible
claim is a four-relation candidate basis sufficient for these five local patterns, not a universal
interaction algebra.


## Return 3: Follett, Mary Parker — authority and evidence

# Authority, evidence, visibility, and coordination in local interaction relations

## Scope and evidence strength

This return examines only `sequential`, review, `zig-zag`, feedback, and robot-talks. It does not
select a final type basis. Claims below are tagged implicitly by their source:

- **implemented**: enforced by current runtime code;
- **executed**: witnessed in a preserved run, even when coordinated manually;
- **specified**: required by a skill or normative workflow document, but not necessarily executed by
  the current runtime;
- **candidate**: proposed architecture or discovery text;
- **missing**: the repository explicitly leaves the authority or transition undecided.

The strongest result is negative: topology alone cannot encode these interactions. The V1 recipe
schema enumerates `depends_on`, `review_of`, `feeds`, and `gates`, but gives an edge only
`{edge_id, from_node_id, to_node_id, edge_kind}` and projects it unchanged into a non-authoritative
candidate; it neither defines per-kind authority nor executes the graph
(`docs/features/agents-communication-infra/specs/protocol-compilation.md:189-203`,
`docs/features/agents-communication-infra/specs/protocol-compilation.md:265-290`,
`docs/features/agents-communication-infra/specs/protocol-compilation.md:381-408`). Current
`legacy-managed` code is narrower still: it accepts only `sequential` and
rejects every other connection type (`implementations/server/runtime/dispatch_workflow.py:314-340`).

## What must remain separate

| Dimension | Meaning in this corpus | Examples |
|---|---|---|
| Relation semantics | What one endpoint's accepted fact permits or requires at the other endpoint, including payload/evidence, inspection rights, and any authority change. | “consume exact terminal output”; “adjudicate this exact submission”; “request remediation”. |
| Role assignment | Which seat performs a capability; changing the assignee need not change the relation. | writer, skeptic, reviewer, synthesizer, auditor, human approver. Roles are read separately from workflow position (`.agents/skills/research/SKILL.md:46-62`; `.agents/skills/review/SKILL.md:52-64`). |
| Graph combinator | Shape/order only. | sequence, fan-out/fan-in, barrier, alternation, cycle. |
| Policy | A configurable condition over a graph or relation. | loop ceiling, convergence rule, quorum, deadline, output mode, approval rule. |
| Runtime effect | Operational mutation performed by an owner other than the edge label. | bind a turn, materialize input, accept an artifact, reopen an assignment, schedule, retry, cancel. Runtime owns scheduling/retry/effective inputs (`.agents/skills/research/SKILL.md:121-125`). |

An edge type that merely repeats a role name, graph direction, or runtime command would collapse
these layers rather than preserve meaning.

## Action and authority matrix

“May” below means the cited contract grants the action. “Missing” means no such grant was found; it
does not mean permission is implicitly denied everywhere.

| Action | `sequential` | review | `zig-zag` | feedback | robot-talks |
|---|---|---|---|---|---|
| Propose | Producer authors a semantic output; the connection itself is already part of the confirmed record. | Attackers propose findings; a reviewer may submit `approved` or `changes_required` against an exact subject/version. | Writer proposes a draft/candidate; skeptics propose typed objections or dispositions. | A reviewer/verifier may identify missing or defective material. Whether the legacy edge itself carries a proposal is missing. | User proposes the central question and assumptions; orchestrator proposes the investigation strategy; agents propose findings (`.agents/skills/robot-talks/SKILL.md:26-42`). |
| Send/publish | Producer completes a resolved turn with an artifact receipt; it does **not** thereby publish an arbitrary handoff. The compiler consumes a separately materialized handoff receipt (`implementations/server/runtime/dispatch_workflow.py:86-127`, `implementations/server/runtime/service.py:5850-5942`). | In the review skill, returns flow to the synthesizer and verifier; in the candidate Work Bus, an authorized reviewer calls `submit_review`. | Coordination sends draft to the original skeptics and their objections back to the same writer; the current generic runtime does not implement this edge. | Candidate Work Bus semantics allow directed findings by subject plus allowlisted remediation scope; reviewer cannot pick an agent ID (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:345-371`). Equivalence to the legacy `feedback` label is unproved. | Explorers submit independent reports; direct challenge/response exists only in an optional `ring/`, not as a required edge (`.agents/skills/robot-talks/SKILL.md:44-62`, `.agents/skills/robot-talks/SKILL.md:72-100`). |
| Receive/inspect | Every downstream seat receives a manifest slot containing one exact immutable output per upstream seat, in seat order (`implementations/server/runtime/dispatch_workflow.py:125-202`, `implementations/server/runtime/dispatch_workflow.py:357-410`). No peer-stream inspection is granted. | Reviewer/verifier inspects the exact artifact/submission; final approver receives the complete evidence bundle (`.agents/skills/review/SKILL.md:89-107`). | Writer sees all gate rows; each original skeptic sees the writer's response/disposition. The frozen descriptive synthesis remains read-only (`research/knowledge-formation/dispatch.yaml:221-258`, `research/knowledge-formation/dispatch.yaml:291-304`). | Intended recipient is the responsible work item/role resolved by routing, not an arbitrary named agent. Visibility of prior evidence must be policy-authorized. Exact visibility for the legacy connection is missing. | Each agent initially works independently. Synthesis consumes reports; human sees synthesized tensions. Peer visibility is absent unless the optional confrontation ring is used. |
| Revise | Accepted source bytes are not edited; a different result needs a new receipt/version. The downstream consumer may create its own output, not mutate the source. | Review dispatch does not apply fixes. The subject owner performs later rework; findings refuted by verifiers are dropped, not softened (`.agents/skills/review/SKILL.md:125-145`). | Writer alone revises its owned artifact/response matrix; skeptics confirm or reopen dispositions and do not edit it. In knowledge-formation, parent-only frozen synthesis and terminal metadata are separately protected (`research/knowledge-formation/dispatch.yaml:291-311`, `research/knowledge-formation/dispatch.yaml:459-490`). | Candidate semantics create a new rework generation that supersedes the prior one; prior events are never altered (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:517-532`; `docs/features/agents-communication-infra/README.md:688-702`). Which generation boundary `feedback` should use remains explicitly open (`docs/features/agents-communication-infra/README.md:1274-1285`). | No implementation is revised. Human may choose a separate plan, backlog item, explanation, or targeted follow-up (`.agents/skills/robot-talks/SKILL.md:64-70`). |
| Confirm | Runtime verifies exact receipt, route, producer identity, bytes, schema, size, and digest before the target manifest can use the source (`implementations/server/runtime/dispatch_workflow.py:137-187`). This confirms provenance/integrity, not truth. | Verifier confirms that a finding survives the literal artifact; final approver accepts the change-request list. Human confirms output mode and review shape (`.agents/skills/review/SKILL.md:105-114`, `.agents/skills/review/SKILL.md:128-153`, `.agents/skills/review/SKILL.md:184-189`). | Every original skeptic must confirm every disposition; silence is not confirmation (`research/knowledge-formation/dispatch.yaml:291-304`). Final approval remains a separate authority. | Candidate review confirms either `approved` or `changes_required`; the relation's own confirmation vocabulary and convergence rule are missing. | Agents do not confirm actionable truth. Human validates each tension at the human gate. |
| Decide | No semantic decision is granted to producer or consumer by `sequential`; it only establishes a readiness/evidence dependency. | Reviewer/verifier decides an epistemic review verdict within its profile; final approver decides dispatch acceptance. A coverage auditor cannot double as dedicated approver in review (`.agents/skills/review/SKILL.md:99-111`). | Skeptics decide gate dispositions; parent owns loop accounting; auditor/final approver decides closure, depending on the workflow. | Reviewer may request correction, but routing/reopen is decided by orchestrator/kernel policy, not by reviewer (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:421-436`). The legacy edge's decision owner is missing. | Human alone decides actionable/deferred/misinterpreted/uncertain; agents only furnish evidence and tensions. |
| Release downstream work | A valid handoff is inserted into the target input; in the target architecture, committed group result—not mere submission—releases declared consumers (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:96-109`). | Accepted worker output may release a reviewer; `changes_required` may release only rework; approved review sets permit kernel completion/commit. | Only the protocol's terminal condition releases the next stage; knowledge-formation forbids advance before convergence or typed exit (`research/knowledge-formation/dispatch.yaml:273-304`). | Candidate `changes_required` releases a rework assignment of the same topology, not arbitrary downstream work (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:96-105`). Generic `feedback` release remains missing. | No implementation is released before human validation; any implementation plan is a separate session. |
| Retry | Binding and terminal retries must match the already accepted launch/result exactly or conflict (`implementations/server/runtime/service.py:5719-5746`, `implementations/server/runtime/service.py:5943-5954`). | Skill delegates retry mechanics to runtime. Candidate Work Bus distinguishes identical retry from rework generation. | Repetition is not retry: a loop contains new objections/responses. Parent counts it against the loop policy (`research/knowledge-formation/LEDGER.md:100-107`). Transport retry semantics for zig-zag are missing. | Rework is a new generation; identical retry returns the old receipt; replacement is a new attempt (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:517-532`). | No retry identity or idempotency contract is specified; an uncertain outcome may cause a separately chosen targeted follow-up. |
| Cancel | A host turn may terminate `cancelled`, but the sequential edge does not itself grant cancellation (`implementations/server/runtime/service.py:5850-5860`). | No review-role cancellation authority is defined; runtime/control plane owns it. | Loop exhaustion produces a typed exit in the executed protocol; it is not cancellation (`research/knowledge-formation/dispatch.yaml:306-311`). Cancellation owner is missing at relation level. | Candidate command/control plane owns cancel/reopen with authority, policy, idempotency and CAS; reviewer text cannot cancel (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:431-439`). | No cancellation contract exists beyond the user choosing not to proceed. |
| Accept evidence | Runtime accepts content-addressed producer evidence into a manifest; downstream interpretation remains separate. | Surviving findings must quote the attacked artifact; an attacker's assertion is not evidence (`.agents/skills/review/SKILL.md:139-145`). Final approver checks the bundle. | Skeptics accept/refute cited evidence per their gate; writer cannot convert silence into acceptance. | Candidate review requires visible evidence references, except a profile-authorized missing-artifact class (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:246-267`). Legacy `feedback` evidence acceptance is missing. | Each finding requires a path/line/doc reference; synthesis constructs tensions; human supplies the final disposition (`.agents/skills/robot-talks/SKILL.md:44-70`). |

## Observed transition semantics by pattern

### 1. `sequential`: integrity-bearing dependency, not delegated judgment

The implemented path is: resolved producer turn -> immutable producer-output receipt -> one receipt
per upstream seat -> target `slots` manifest -> authorized target binding. The target gets exact bytes,
schema, producer identity, order, digest, and cardinality
(`implementations/server/runtime/dispatch_workflow.py:125-210`,
`implementations/server/runtime/dispatch_workflow.py:357-410`).
The authority-changing events are runtime acceptance/binding and, before any run, human-confirmed
dispatch authority—not the movement of bytes. A `DispatchCandidate` or artifact cannot create this
authority (`docs/features/agents-communication-infra/specs/protocol-compilation.md:32-56`,
`docs/features/agents-communication-infra/specs/protocol-compilation.md:430-454`).

Immutable: confirmed prompt, route digest, source bytes/receipt, target manifest digest, prior
accepted retries. Visible: only sources placed in the target's manifest. Missing: a generic
progressive scheduler; the compiler currently requires the handoff receipt to pre-exist and does not
materialize it (`implementations/server/runtime/dispatch_workflow.py:97-106`).

### 2. Review: evidence-bound adjudication plus separately owned approval

The review workflow is composite: independent attacks -> synthesis -> verifier challenge -> optional
coverage audit -> final approval. Verifiers may refute findings; the final approver accepts the
change-request list; neither act edits the reviewed artifact (`.agents/skills/review/SKILL.md:81-126`,
`.agents/skills/review/SKILL.md:128-153`, `.agents/skills/review/SKILL.md:184-189`). The candidate
Work Bus sharpens this into an exact-subject review whose
verdict can be `approved` or `changes_required`; findings bind visible evidence and normalized
remediation scope (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:246-267`,
`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:421-429`).

Authority changes at verdict acceptance/release evaluation, not when the reviewer merely receives
the artifact. Review evidence is the quoted/version-bound subject. The role labels alone do not
carry this power: the same `skeptic` enum in research attacks one epistemic gate, while the review
verifier checks change requests.

### 3. `zig-zag`: bounded challenge/revision/confirmation protocol

The executed knowledge-formation witness shows more than a bidirectional edge: writer draft, three
independent gate reports, writer response matrix and revision, then confirmation by the **original**
skeptics. Convergence requires all confirmations; silence is not confirmation; unresolved objections
survive; parent alone owns the shared loop counter (`research/knowledge-formation/dispatch.yaml:273-311`).
The ledger witnesses two distinct rounds, new evidence/dispositions, and exhaustion of the shared
budget (`research/knowledge-formation/LEDGER.md:59-72`,
`research/knowledge-formation/LEDGER.md:100-107`).

Thus `zig-zag` in this corpus is at least alternation + preserved identity + revision ownership +
confirmation + convergence policy + loop policy. Which subset, if any, belongs in one edge type is
not established. Current runtime explicitly rejects the label.

### 4. Feedback: a required distinction with unresolved operational identity

Skills use feedback as a conditional back-edge when material is missing, never by default
(`.agents/skills/research/SKILL.md:80-96`; `.agents/skills/review/SKILL.md:81-97`). Candidate Work Bus
text supplies one plausible semantic witness: `changes_required` requests rework from the
responsible work item, creates a new generation, and cannot route or schedule directly from reviewer
text (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:345-371`,
`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:421-436`,
`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:517-532`). But the architecture explicitly
leaves open whether generic `feedback` creates a new round, group version, or stage execution
(`docs/features/agents-communication-infra/README.md:688-702`,
`docs/features/agents-communication-infra/README.md:1274-1285`).

Therefore it is unsupported to equate the legacy `feedback` label with review rework. Established:
prior evidence must remain immutable and a reverse request must not silently rewrite history.
Missing: endpoint identity, authority owner, release fact, confirmation rule, retry boundary, and
termination semantics of the generic relation.

### 5. Robot-talks: independent inquiry with human-only action authority

Robot-talks requires user-defined question/assumptions, user approval before spawning, independent
evidence-bearing reports, synthesis of tensions, and a human disposition before any action
(`.agents/skills/robot-talks/SKILL.md:26-70`). Reports and final findings are preserved; direct
cross-agent challenge is optional. The session is explicitly not a governed dispatch and needs no
runtime receipts (`.agents/skills/robot-talks/SKILL.md:72-100`).

The authority-changing event is the human gate. Agent messages can change the evidential record but
cannot authorize implementation, backlog commitment, or closure disposition. Retry, cancellation,
peer acceptance, and ring convergence are not specified.

## Same topology, different semantics

### Pair A: `producer -> consumer`

```text
A ----> B
```

- As `sequential`, B may consume A's exact accepted output after the release condition. B gains no
  authority to approve, reject, or reopen A.
- As review, B inspects a version-bound subject and may emit an adjudicative verdict whose accepted
  `changes_required` result can release rework. B still cannot select or schedule the reworker.

The arrow is identical; payload type, inspection obligation, verdict authority, evidence binding,
and release consequence differ.

### Pair B: `author <-> challenger`

```text
A <----> B
```

- As knowledge-formation `zig-zag`, A owns revision, B owns a named gate, B's explicit confirmation
  is necessary for convergence, and the parent owns the loop counter.
- As an optional robot-talks confrontation ring, A and B may challenge and respond, but neither
  acquires approval authority; only the later human gate can authorize action, and no convergence
  rule is specified.

The bidirectional topology is identical; one exchange is a release-gated adjudication protocol and
the other is evidential dialogue.

### Pair C: `reviewer -> subject owner`

```text
reviewer ----> owner
```

- A non-verdict critique/deliberation message adds evidence but has no rework effect
  (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:421-425`).
- An accepted `changes_required` review requests remediation and may cause the orchestrator to
  create/reopen the responsible operation
  (`docs/features/agents-communication-infra/discovery/bus-contracts/README.md:427-436`).

Again the endpoints and direction match. The authority-changing distinction is the accepted,
profile-bound verdict—not data movement.

## Findings and explicit gaps

1. A useful typed relation must distinguish **delivery of evidence** from **grant or exercise of
   authority**. Receipt acceptance, reviewer verdict, skeptic confirmation, runtime release, and
   human approval are different events.
2. Visibility is semantic, not cosmetic. Sequential consumers receive an exact manifest; review
   sees an exact subject/evidence bundle; robot-talks begins independently; proposed deliberation
   uses sealed collect/reveal. The architecture makes reveal an explicit event rather than a prompt
   convention (`docs/features/agents-communication-infra/README.md:539-570`,
   `docs/features/agents-communication-infra/README.md:738-762`).
3. Accepted evidence is append-only/versioned. Revision produces a new artifact, event, generation,
   or response; it does not rewrite the antecedent
   (`docs/features/agents-communication-infra/README.md:1004-1023`).
4. Named patterns are not yet proven primitives. `zig-zag` and robot-talks are demonstrably
   composite protocols; feedback has insufficient semantics to classify; review combines evidence
   relation, adjudication, rework policy, and approval; `sequential` is the only implemented
   connection semantics.
5. Endpoint type remains open. Runtime evidence favors dispatch/group/seat/turn/artifact or
   work-item/result endpoints over human persona names: authority fields are derived from bound
   execution identity, not agent payload (`docs/features/agents-communication-infra/README.md:614-626`;
   `docs/features/agents-communication-infra/discovery/bus-contracts/README.md:264-267`). This is
   evidence for the later synthesis, not a selected model.
6. Missing authority must not be filled by analogy: generic feedback's owner and generation
   boundary; robot-talks ring convergence/retry/cancel; zig-zag transport recovery; and executable
   semantics for V1 `review_of`/`feeds`/`gates` all remain unspecified or unimplemented.

The candidate collapse-test for “topology is enough” is already met: Pairs A-C preserve node and
edge shape while changing who can decide, what evidence is admissible, what becomes visible, and
which event can release work. Any model that identifies those fragments therefore loses observed
product semantics.


## Return 4: Simon, Herbert — current external solutions

---
tags: [agents-communication-infra, typed-graph, external-research, agent-orchestration]
node_type: research-explorer-return
is_session: false
layer: [architecture, application]
nature: [research, informational]
status: draft
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Current External Solutions Sweep

## Scope and evidence discipline

This sweep compares executable behavior, not product vocabulary. It covers five systems for which
current official evidence shows active maintenance: OpenAI Agents SDK, LangGraph, Google ADK,
Microsoft Agent Framework, and CrewAI. AutoGen is retained as an adjacent precedent but is not
counted: Microsoft now declares it in maintenance mode and directs new users to Agent Framework.

All sources are official product documentation or official source repositories, accessed on
2026-08-17. “Documented” below means an official contract or example exists. “GA”, “stable”,
“experimental”, and “production-ready” preserve the publisher's own maturity language. Repository
activity demonstrates maintenance, not real-world adoption. **Actual adoption is not established
for any system by this corpus**; vendor case studies, star counts, certification counts, or product
claims were not treated as adoption evidence.

## One-line result

Current systems converge on generic execution graphs, state, routing, joins, loops, interruption,
and durability, but none of the five active systems demonstrates a minimal algebra of
semantically typed interaction relations: semantic differences such as control transfer,
delegation-with-return, review authority, and approval are usually encoded by distinct higher-level
patterns, node logic, messages, state, or policy rather than by a rich edge type alone.

## Status and maturity

| System | Version/date evidence | Publisher-declared maturity | Maintenance evidence | Adoption evidence |
|---|---|---|---|---|
| OpenAI Agents SDK | Docs accessed 2026-08-17; release contract remains `0.Y.Z` and says the leading zero means the SDK is evolving rapidly | No GA/stable claim found for the Python SDK; non-beta public interfaces may still break on minor releases | Current official docs and releases; [release policy](https://github.com/openai/openai-agents-python/blob/main/docs/release.md) | Not established |
| LangGraph | Official repository showed the 1.x line and a `1.2.9` release dated 2026-07-10 | v1 public line; official release notes describe LangGraph v1 | Current releases and v1 docs; [repository](https://github.com/langchain-ai/langgraph), [v1 notes](https://docs.langchain.com/oss/python/releases/langgraph-v1) | Not established |
| Google ADK | Python `2.1.0` released 2026-05-23; graph workflows supported from Python/Go `2.0.0` | ADK Python 2.0 GA since 2026-05-19 and Go 2.0 GA since 2026-06-30 | Current 2.x releases; [ADK 2.0](https://github.com/google/adk-docs/blob/main/docs/2.0/index.md), [releases](https://github.com/google/adk-python/releases) | Not established |
| Microsoft Agent Framework | Docs accessed 2026-08-17; official Python metadata observed on the 1.x line (`1.12.1` in the inspected snapshot), while checkpoint docs already describe behavior “starting in 1.13.0” | Python package classifier says `Production/Stable`; Agent Framework 1.0 is presented as the production successor to AutoGen | Active 1.x releases and docs; [package metadata](https://github.com/microsoft/agent-framework/blob/main/python/pyproject.toml), [repository](https://github.com/microsoft/agent-framework) | Not established |
| CrewAI | Versioned official docs resolved to `1.15.16` on access | “Production ready” is a vendor claim, not independently verified maturity | Current versioned docs and releases; [Flows docs](https://docs.crewai.com/v1.15.16/en/concepts/flows), [repository](https://github.com/crewAIInc/crewAI) | Not established |
| AutoGen (adjacent, not counted) | Latest official release page identifies the 0.7.x line | `GraphFlow` is experimental; repository declares the overall project in maintenance mode | Maintenance only; no new features promised | Not established |

The Microsoft version discrepancy is itself a warning: consumers should pin and verify the
installed package rather than assume the continuously updated documentation matches a deployed
minor version.

## Behavioral comparison

| System | Core executable primitives | Graph/orchestration model | Handoff / control transfer | Sequence, parallel, condition, loop |
|---|---|---|---|---|
| OpenAI Agents SDK | `Agent`, `Runner`, tools, agents-as-tools, handoffs, guardrails, sessions, `RunState` | No general graph DSL in the core orchestration guide; runner loop plus ordinary Python orchestration | Handoff is an LLM-visible tool whose target becomes the active agent and normally receives conversation history; agent-as-tool returns a bounded result while the manager retains control | Handoffs route dynamically; sequence, fan-out, evaluator loops, and joins are explicitly shown as application Python (`asyncio`, `while`, output transforms) |
| LangGraph | Shared `State`, nodes, edges, reducers/channels, `Command`, `Send`, subgraphs, checkpointers | Pregel-like state graph executing active nodes in supersteps | A handoff is normally a state update plus `Command(goto=...)`; `Command.PARENT` crosses a subgraph boundary | Native fixed and conditional edges, multi-destination parallel activation, fan-in through state/reducers, cycles, recursion limits |
| Google ADK | Workflow nodes (agents, tools, functions, human input), edges/routes, `Event.Output`, `JoinNode`, nested and dynamic workflows | Declarative graph runtime in ADK 2.0; dynamic workflows use code for recursion or control too complex for a static graph | Collaborative agent routing exists, but graph control is primarily route/event-driven; control transfer is not a separate rich edge contract | Native chains, conditional routes, fan-out/fan-in, and conditional back-edges; prebuilt sequential/parallel/loop agents remain higher-level templates |
| Microsoft Agent Framework | Executors, typed messages, direct/conditional/switch/fan-out/fan-in edges, workflow events, shared state, sub-workflows | Functional and graph APIs share a workflow run model; graph execution uses supersteps | Built-in handoff orchestration is a mesh with allowed transfers; receiver takes task ownership and full conversation context, unlike agent-as-tool where manager retains control | Native graph sequence, conditions, switch, and fan-out/fan-in; repeated turns and termination are documented in handoff/group-chat orchestrations, but a generic cyclic-graph contract was not established in this sweep |
| CrewAI | Flow methods, `@start`, `@listen`, `@router`, `and_`, `or_`, Flow state, Crews/Agents | Event-driven Flow projected as a directed execution graph; methods emit outputs/labels that activate listeners | Delegation is primarily inside Crews or ordinary method calls; Flow does not expose a first-class ownership-transfer relation analogous to handoff | Chaining, multiple starts/broadcast, `and_`/`or_` joins, conditional labels, and code/routing-based loops; no minimal typed edge vocabulary |
| AutoGen (adjacent) | Agents, teams, messages, termination conditions, `DiGraphBuilder`, `GraphFlow` | Conversational teams plus experimental directed graph execution | `Swarm` uses `HandoffMessage`; group chats use a manager/speaker selector | Experimental `GraphFlow` supports sequence, parallel, conditional edges, activation groups, and cycles |

## System findings

### OpenAI Agents SDK

The core distinction is semantic and useful: **agents-as-tools** preserves a manager's control and
final-answer ownership, whereas a **handoff** changes the active agent and gives the receiver the
conversation. Input filters may narrow what crosses the handoff, and typed `input_type` can validate
handoff metadata. This is a genuine difference in authority/control, but it is represented by two
different primitives and runner behavior, not by two types on a general graph edge. The SDK's
[orchestration guide](https://openai.github.io/openai-agents-python/multi_agent/) explicitly leaves
deterministic sequencing, parallel calls, evaluator loops, and output composition to normal Python;
the [handoff contract](https://openai.github.io/openai-agents-python/handoffs/) says handoffs remain
inside one run.

State has several layers: session history across runs, the current runner history, application
context, and serializable `RunState`. A default handoff exposes prior conversation; an input filter
can make the recipient's view private or reduced. `RunState` is the durable pause/resume boundary
for pending approvals and captures model responses, generated items, approval state, and optional
server conversation identifiers ([RunState](https://openai.github.io/openai-agents-python/ref/run_state/)).

Termination is a final output with no outstanding tool call, or a `max_turns` failure. Human
approval is tool-scoped: approval-required tools interrupt the outer run even when called after a
handoff or inside an agent-as-tool, and the original run resumes after approve/reject
([HITL](https://openai.github.io/openai-agents-python/human_in_the_loop/)). Model-call retries have
explicit replay-safety boundaries and policies; process-level durable recovery is delegated to
documented Dapr, Temporal, Restate, or DBOS integrations rather than supplied as a generic workflow
graph checkpoint engine ([running and recovery](https://openai.github.io/openai-agents-python/running_agents/),
[model retry](https://openai.github.io/openai-agents-python/models/)).

Types cover structured agent outputs and handoff inputs through Pydantic-compatible schemas, not
semantic compatibility of arbitrary agent-to-agent relations. Built-in tracing records model
generations, tools, handoffs, guardrails, and custom spans
([tracing](https://openai.github.io/openai-agents-python/tracing/)). Extension is ordinary code,
custom tools, hooks, guardrails, handoff filters, and custom session/durable orchestration adapters.

**Left to application code:** graph topology, join/quorum, convergence, reviewer authority,
cross-run workflow scheduling, and the meaning of repeated feedback.

### LangGraph

LangGraph provides the clearest general execution substrate in the sample. Its three base concepts
are shared state, nodes, and routing edges. Nodes and edges are ordinary functions; fixed edges,
conditional edges, `Command`, and `Send` determine activation. Multiple outgoing destinations run
in the next superstep, and cycles are valid. The graph ends at `END` or when no work remains; a
recursion limit/`RemainingSteps` bounds cycles
([Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api)).

Graph state may be declared with `TypedDict`, dataclasses, or Pydantic and merged with per-field
reducers. This types the data plane, not the semantic intent of an edge. Handoffs are a documented
pattern implemented as state mutation plus routing—often a tool returns `Command`—and therefore
do not add an irreducible runtime relation type
([handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs)). Subgraphs can
retain per-invocation or per-thread state, enabling private or persistent agent context, but the
designer chooses the visibility boundary.

Checkpointers save graph state at every step and enable resume, time travel, HITL, and recovery from
the last successful superstep. Successful parallel writes can be retained when a sibling fails
([persistence](https://docs.langchain.com/oss/python/langgraph/persistence)). `interrupt()` pauses
with a serializable payload and resumes with `Command(resume=...)`, making approval only one of many
possible external-input protocols
([interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)). Per-node retry policies
are stable across Python and TypeScript; newer timeout/error-handler additions in `langgraph>=1.2`
are explicitly marked alpha in the docs
([fault tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance)). LangSmith is
the documented tracing/inspection path.

**Left to application code:** the distinction between advice, review, approval, delegation, and
evidence transfer; authority; quorum/convergence; payload privacy; compensating effects; and most
domain-level termination predicates.

### Google ADK 2.x

ADK 2.0 moves its workflow runtime to graphs whose nodes can be agents, tools, functions, human
input, or nested workflows. Edges establish execution routes, node output travels through
`Event.Output`, route values select branches, and `JoinNode` provides an all-upstream barrier.
Back-edges implement loops and re-activate a node with a fresh lifecycle
([graph workflows](https://adk.dev/graphs/), [routes](https://adk.dev/graphs/routes/)). Dynamic
workflows deliberately use code when loops, recursion, or branching are too dynamic for a static
graph. The older `SequentialAgent`, `ParallelAgent`, and `LoopAgent` are retained as templates but
are superseded by graph/dynamic workflows for Python and Go 2.x.

ADK supports typed agent input/output schemas; Go additionally exposes generic typed agent nodes,
and successors receive typed `Event.Output`
([data handling](https://adk.dev/graphs/data-handling/)). Session state is serializable key/value
data with explicit session, user, app, and invocation-temporary scopes; persistence depends on the
selected `SessionService` ([state](https://adk.dev/sessions/state/)). This is richer state scoping,
but it still does not make an edge mean “review” or “transfer authority.”

HITL is a first-class node: `RequestInput` pauses execution and can require a response schema; Go's
node reruns on resume and passes the reply as typed output
([human input](https://adk.dev/graphs/human-input/)). Resumability is opt-in at the application
configuration boundary, and the 2.0 migration contract references `RetryConfig`; this sweep did not
establish a universal checkpoint-per-node or exactly-once effect guarantee
([resume](https://adk.dev/runtime/resume/), [ADK 2.0](https://github.com/google/adk-docs/blob/main/docs/2.0/index.md)).
Tracing follows OpenTelemetry GenAI conventions and exports OTLP
([traces](https://adk.dev/observability/traces/)). Extension is through function/tool/agent nodes,
nested workflows, custom agents, route functions, and fully dynamic code.

**Left to application code:** semantic relation labels, authority and evidence rules, convergence,
failure compensation, non-all join policies, and the distinction between a protocol loop and a
mere control-flow cycle. A documented `JoinNode` can stall if any upstream emits no output, showing
that failure semantics cannot be inferred from fan-in topology alone.

### Microsoft Agent Framework

Agent Framework exposes the strongest code-level message typing in the sample. Executors receive
and emit typed messages; edges may be direct, conditional, switch-case, fan-out, or fan-in, and the
runtime can report delivery failures such as type mismatch, false condition, or buffered fan-in.
These are type and control guarantees, not domain-semantic edge types
([workflow concepts](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/),
[edges](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/edges),
[observability](https://learn.microsoft.com/en-us/agent-framework/workflows/observability)).

Its built-in handoff orchestration provides a particularly valuable semantic witness. Handoff is a
mesh without a central orchestrator: the receiver takes full task ownership and full conversation
context. Agent-as-tool instead returns to a primary agent that retains responsibility. Allowed
handoffs constrain who may take over next, even though all participants remain context-connected
([handoff](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)).
Sequential, concurrent, group-chat, handoff, and Magentic are higher-level orchestration builders
over workflow mechanisms, not evidence that each is a primitive edge kind.

Maturity must be read per surface: the core Python package declares production/stable, while
official release notes still mark particular orchestration surfaces such as Magentic experimental.
The stable core label therefore does not promote every included pattern to the same contract level.

Workflow checkpoints capture executor state, pending messages, pending requests/responses, and
shared state at superstep boundaries; durable file and Cosmos stores allow cross-process recovery.
Rehydration requires the same topology and stable executor/agent identities
([checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints)). HITL uses
request/response events and tool-approval requests, both checkpointable
([HITL](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop)). The
framework supports shared workflow state and per-agent threads, but its docs warn that reused
executor or workflow instances can leak mutable state across runs unless instances are isolated or
reset ([state](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/state)).

The official checkpoint and core workflow pages establish resume, not a single generic retry
policy for every executor/effect. Application executors remain responsible for effect idempotency
and domain recovery unless a more specific provider contract says otherwise. Extension is through
custom executors, edge predicates and transforms, sub-workflows, orchestration builders, checkpoint
stores, middleware, and agent/provider adapters.

**Left to application code:** the semantics of evidence, review/acceptance authority,
convergence/quorum, compensation, privacy beyond context/state configuration, and whether two
topologically identical edges express different obligations.

### CrewAI

CrewAI separates autonomous `Crews` from event-driven `Flows`. A Flow marks entry points with
`@start`, activates downstream methods with `@listen`, combines triggers with `and_`/`or_`, and
routes on labels with `@router`. Multiple satisfied starts may execute in parallel. The resulting
structure can be plotted as a directed execution graph, but the public API is a decorator/event
model rather than a graph with semantically typed relations
([Flows](https://docs.crewai.com/v1.15.16/en/concepts/flows)).

Flow state may be an unstructured dictionary or a Pydantic model. `@persist` saves state, uses
SQLite by default, supports resume/fork by state ID, and allows a custom `FlowPersistence`
implementation. The documentation claims failed/restarted flows can reload state, but does not in
the inspected core contract establish checkpointing of every external effect or a graph-wide
exactly-once guarantee. Generic flow-step retry behavior was not established in this sweep.

`@human_feedback` pauses a Flow and can emit routing labels after interpreting free-form feedback;
without routing it simply collects feedback. The docs explicitly distinguish the local synchronous
decorator from managed webhook-based asynchronous HITL
([HITL](https://docs.crewai.com/v1.15.16/en/learn/human-in-the-loop)). This is a useful warning:
an LLM-collapsed feedback label is a routing decision, not proof of human authority unless the
application preserves the actual actor and decision evidence.

Observability in the inspected OSS Flow contract includes streamed execution, usage metrics, state
inspection, and graph plotting; detailed managed traces/logs are an AMP product claim and should
not be attributed automatically to the OSS runtime. Extension is ordinary Python Flow methods,
custom agents/Crews, custom decorators/providers, and custom persistence.

**Left to application code:** explicit control-transfer semantics, relation-level payload and
authority constraints, bounded/convergent loops, retry policy, effect recovery, and typed
compatibility between arbitrary listener outputs and downstream methods beyond normal Python and
Pydantic validation.

### AutoGen: adjacent transition evidence

AutoGen remains technically instructive but no longer satisfies the dispatch's “actively
maintained” requirement. The official repository says it is in maintenance mode and will receive
no new features, while recommending Agent Framework
([repository notice](https://github.com/microsoft/autogen)). Its `GraphFlow` executes directed
graphs with sequential, parallel, conditional, and cyclic paths, plus `all`/`any` activation
groups, but is explicitly experimental
([GraphFlow](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html)).
AgentChat also supplies round-robin/selector group chats, `Swarm` handoff messages, state save/load,
composable termination conditions, and OpenTelemetry tracing. Blocking `UserProxyAgent` input is
documented as unstable and non-resumable; persisted HITL is instead modeled by terminating, saving
team state, and starting another run
([HITL](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)).

AutoGen therefore demonstrates both a useful graph vocabulary and a maturity failure mode: a
feature can be expressively relevant while remaining an unsafe foundation for a new local contract.

## Cross-system behavior map

| Behavior needed locally | External witness | What the witness actually guarantees | What it does not settle |
|---|---|---|---|
| Dependency / sequence | Fixed edge or chain in LangGraph, ADK, Agent Framework; listener chain in CrewAI; Python chaining in OpenAI | B starts after A's activation/completion under that runtime | Whether A's output is accepted evidence, merely available input, or authoritative |
| Fan-out / fan-in | Supersteps and reducers (LangGraph), `JoinNode` (ADK), fan-in barrier edges (Agent Framework), multiple starts and `and_` (CrewAI), `asyncio.gather` (OpenAI) | Parallel activation and some barrier/merge rule | Quorum, partial failure, cancellation, ordering, dissent preservation |
| Conditional routing | Conditional edge/`Command`, routes, switch predicates, router labels, handoff tool choice | Selects one or more next activations from runtime data | Who is authorized to decide, whether the decision is evidence, and how it is audited |
| Control transfer | OpenAI and Agent Framework handoff; AutoGen `HandoffMessage` | Active specialist/task ownership changes, with defined context behavior | Whether all future protocols should encode this as an edge type, node, message, or subgraph |
| Delegation with return | Agent-as-tool in OpenAI and Agent Framework | Manager retains responsibility while a specialist returns a bounded result | Review/acceptance semantics and whether the result becomes canonical evidence |
| Review / approval | LangGraph interrupt, ADK human node, Agent Framework request/tool approval, OpenAI tool approval, CrewAI human feedback | Execution can pause and receive an external decision/input | Reviewer identity, authority scope, independence, quorum, and convergence are application contracts |
| Feedback loop / zig-zag | Back-edges in LangGraph/ADK, workflow loops in Agent Framework, routers/code in CrewAI, Python `while` in OpenAI | Repeated activation until a supplied predicate or limit ends it | Whether feedback is advisory or binding, who must respond, what changed, and what counts as convergence |
| Shared conversation | OpenAI default handoff, Agent Framework handoff mesh, AutoGen group chat | Participants receive a common or transferred history under the documented pattern | Selective disclosure, provenance, canonical artifact ownership, and least-privilege evidence flow |
| Durable pause/recovery | LangGraph checkpointer, Agent Framework checkpoints, OpenAI `RunState` plus durable integrations, ADK resumability, CrewAI persistence | Some state can be restored after interruption/restart | Exactly-once external effects, compensation, schema migration, and semantic validity after code/prompt changes |

## Implications for a local typed-relation basis

1. **Use graph mechanics as the substrate, not as the semantic answer.** Fixed, conditional,
   fan-out, fan-in, loop, and interrupt are well-supported execution behaviors. They say when work
   may run; they do not by themselves say what obligation or authority crosses the edge.

2. **Control transfer is the strongest externally witnessed semantic distinction.** OpenAI and
   Agent Framework independently distinguish handoff from agent-as-tool using task ownership,
   context, and return-of-control. Collapse test: if receiver ownership and return-of-control do not
   affect execution or evidence, the distinction disappears into ordinary routing.

3. **Type the data plane and the relation contract separately.** Frameworks commonly validate
   state/message/output schemas. That prevents malformed payloads but does not distinguish
   `advises`, `reviews`, `approves`, `delegates`, or `transfers-control`. A local relation candidate
   needs both endpoint/payload compatibility and a semantic effect.

4. **Treat named collaboration patterns as compiled subgraphs until necessity is shown.** No
   external system requires `zig-zag`, debate, group chat, or evaluator loop to be one primitive
   edge. They are normally compositions of activation, message/state transfer, choice, repetition,
   and termination plus an authority policy.

5. **Keep policy outside the edge unless it changes the relation's meaning.** Quorum, maximum
   rounds, convergence predicates, retry, timeout, and checkpoint frequency vary independently in
   current systems. Encoding all of them as edge types would multiply nominal types without
   demonstrating new interaction semantics.

6. **Model interruption and authority as distinct concerns.** An interrupt proves only that the
   runtime paused for input. Human approval additionally needs actor identity, decision scope,
   evidence, and authority. CrewAI's optional LLM classification of human feedback makes this
   distinction especially visible.

7. **Durability belongs to runtime ownership.** The external systems locate retry, checkpoints,
   replay safety, and idempotency in runners/checkpointers/storage/integrations. A typed relation may
   declare required delivery or evidence semantics, but should not silently appropriate recovery
   ownership from the runtime.

8. **Minimum external witness set for the next synthesis:** a candidate basis should at least
   distinguish (a) activation dependency, (b) payload/evidence delivery, (c) delegation with return,
   (d) transfer of control/ownership, and (e) authoritative gate/decision—unless the local corpus
   shows one can be compiled from the others without erasing observable behavior. Fan-out/fan-in,
   choice, repetition, quorum, convergence, retry, and interruption remain composition/runtime/policy
   candidates until their own necessity witnesses are produced.

This is a cautious implication, not a verdict on the final basis. The external corpus supplies
precedents and counterexamples; it does not prove minimality or sufficiency for the local patterns.


