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
