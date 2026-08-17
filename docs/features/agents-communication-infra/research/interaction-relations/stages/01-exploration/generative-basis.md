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
