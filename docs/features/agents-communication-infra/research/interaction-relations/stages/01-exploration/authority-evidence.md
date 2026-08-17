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
