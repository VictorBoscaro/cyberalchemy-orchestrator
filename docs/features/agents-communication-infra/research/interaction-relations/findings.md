---
tags: [agents-communication-infra, typed-graph, interaction-relations, findings]
node_type: research-findings
is_session: false
layer: [architecture, application]
nature: [research, decision-support]
status: draft
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Basis — Findings

## Finding

The smallest basis supported by the examined local and external traces has five directed relation
types:

1. `requires` — one accepted state is a prerequisite for another occurrence or transition;
2. `supplies` — exact evidence is made visible in a declared input slot;
3. `delegates` — a responsibility holder authorizes bounded work while retaining responsibility
   and the continuation;
4. `transfers_control` — the active responsibility for a control scope moves to a successor;
5. `gates` — authoritative decision evidence selects, permits, denies, or terminates a transition.

`assessed_by` is meaningful behavior but does not survive the minimality test as a primitive edge.
It can be represented without observable loss by a typed assessment occurrence with an exact
subject slot supplied to it, declared criteria and output schema, and separate independence and
authority policies. Review, zig-zag, feedback, robot-talks, and `sequential` remain recipes or
aliases over the basis plus graph combinators, roles, schemas, policies, and runtime effects.

This is a bounded candidate basis, not a universal algebra and not a statement of current runtime
capability.

## Evidence boundary and endpoint model

The basis explains the local traces in
[local-as-built.md](stages/01-exploration/local-as-built.md), the authority counterexamples in
[authority-evidence.md](stages/01-exploration/authority-evidence.md), and the external behavior map
in [current-solutions.md](stages/01-exploration/current-solutions.md). The full evidence record is
in [research.md](research.md).

Relations connect logical, versioned endpoints rather than informal agent names:

| Endpoint kind | Meaning |
|---|---|
| Occurrence | A versioned work, assessment, decision, or terminal occurrence. Its performer and role are bindings, not its identity. |
| Evidence | Immutable, addressable output, message, dissent, assessment, or decision evidence with provenance. |
| Slot or transition | A declared input position or a guarded change of workflow state. |
| Control scope | The bounded responsibility whose active holder may delegate work or change. It may later compile to a dispatch, group, work item, thread, or another owned runtime identity. |

Agent, seat, group, writer, reviewer, skeptic, synthesizer, and approver are bindings or roles.
They are not additional relation types. A later physical schema may represent some logical
endpoints with nodes and others with ports or state records; the semantic contract does not depend
on that choice.

## From observable traces to the basis

| Observable difference | What must remain observable | Consequence |
|---|---|---|
| A downstream occurrence may wait for completion without seeing the producer's bytes. | Eligibility is distinct from visibility. | Keep `requires` separate from `supplies`. |
| A target receives an exact accepted artifact with provenance, but no approval or ownership power. | Evidence delivery is distinct from authority. | Keep `supplies`; do not infer `gates` or control change. |
| A specialist performs bounded work and returns while the manager remains responsible. | Scoped execution authority, retained responsibility, and required return. | Admit `delegates`. |
| A handoff makes the receiver the active task owner. | The post-relation responsibility holder changes. | Admit `transfers_control`; do not compile it as delivery alone. |
| A reviewer finding exists without releasing rework; an accepted decision can release it. | Assessment evidence is distinct from authoritative disposition. | Represent assessment as an occurrence; keep `gates` for authority. |
| The same `A -> B` or `A <-> B` topology supports sequential delivery, review, zig-zag, or dialogue. | Payload, obligation, authority, visibility, and terminal behavior. | Topology and named patterns are insufficient as primitive semantics. |

## Admitted relation contracts

### `requires`

- **Endpoints and direction:** accepted evidence or a completed/accepted occurrence state -> a
  dependent occurrence or transition.
- **Payload/evidence:** the required identity and version, acceptance predicate, and any declared
  cardinality; no content grant is implied.
- **Precondition:** the source satisfies the declared accepted-state predicate.
- **Semantic effect:** the dependent becomes eligible with respect to this prerequisite. Other
  prerequisites may still block it.
- **Authority effect:** none. It neither authorizes the source nor grants the target a right to
  inspect, decide, revise, or execute.
- **Visibility:** none. Visibility requires `supplies` or another separately authorized channel.
- **Terminal and failure behavior:** an unmet prerequisite waits; an impossible, rejected, or
  terminally failed prerequisite makes the dependent blocked or impossible according to explicit
  recipe policy. It does not silently skip the dependent.
- **Legal composition:** chains and conjunction/disjunction over prerequisites are legal. A
  same-version dependency cycle is invalid because it has no initial witness; repetition must use
  distinct round/version occurrences.

The implemented sequential path and the declared `depends_on` edge are local precedents, although
the generic relation is not currently executed as specified here
([local-as-built: status inventory](stages/01-exploration/local-as-built.md#surfacestatus-crosswalk)).

### `supplies`

- **Endpoints and direction:** immutable evidence -> a declared input slot of an occurrence.
- **Payload/evidence:** content-addressed reference, schema/media type, producer provenance,
  subject/version where relevant, and preservation markers such as dissent or disposition.
- **Precondition:** the evidence has been accepted, the target is authorized to receive it, and it
  matches the slot contract.
- **Semantic effect:** the exact evidence becomes the materialized value of that slot. This is a
  delivery fact, not a truth or approval fact.
- **Authority effect:** none beyond the already authorized act of delivery. The receiver gains no
  right to revise, approve, delegate, or transfer control.
- **Visibility:** grants the target only the declared evidence view; it may be full, filtered, or
  redacted by the slot contract.
- **Terminal and failure behavior:** successful materialization yields a receipt. Identical
  redelivery is idempotent; conflicting evidence for a single-valued slot fails. Missing or invalid
  evidence leaves the slot unsatisfied.
- **Legal composition:** fan-out to several authorized slots and fan-in to a structured input are
  legal. Reverse delivery in a feedback protocol targets a new round/version; it does not mutate
  prior evidence.

The narrow deployed witness is the digest-bound producer receipt and target manifest in the
sequential compiler
([local-as-built: sequential](stages/01-exploration/local-as-built.md#1-sequential)).

### `delegates`

- **Endpoints and direction:** a responsibility-holding occurrence or control scope -> a bounded
  work occurrence performed by the delegate.
- **Payload/evidence:** task scope, permitted capabilities, context slice, expected result/return
  contract, delegator identity, and any deadline or resource boundary that is semantic to the
  assignment.
- **Precondition:** the delegator currently holds authority for the scope; the delegate is eligible
  and capable; the delegated task stays within that scope.
- **Semantic effect:** the delegate becomes obligated and authorized to perform the bounded work;
  the delegator remains responsible and retains the continuation. A result or failure must return
  to the delegator through declared evidence and dependency relations.
- **Authority effect:** grants scoped performance authority only. It does not grant final approval,
  permission to exceed the scope, or ownership of the parent continuation.
- **Visibility:** the delegate sees only the explicitly supplied context, not automatically the
  delegator's full history.
- **Terminal and failure behavior:** completion returns the contracted result; rejection, timeout,
  cancellation, or failure returns a typed outcome to the delegator. None silently transfers
  responsibility. Runtime retry remains a runtime policy.
- **Legal composition:** nested delegation is legal only when the delegated scope permits it and
  each link remains auditable. Delegation is not transitive by default. A recipe normally combines
  it with `supplies` for context/result and `requires` for the manager's continuation.

OpenAI Agents SDK and Microsoft Agent Framework independently witness manager-retained
agent-as-tool behavior, contrasted with handoff
([OpenAI orchestration](https://openai.github.io/openai-agents-python/multi_agent/),
[Microsoft handoff](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)).
This relation has no equivalent current local executable edge.

### `transfers_control`

- **Endpoints and direction:** the current holder of a control scope -> the successor holder of
  that same scoped responsibility.
- **Payload/evidence:** control-scope identity/version, successor identity, continuation state,
  context boundary, allowed-successor constraint, and transfer receipt.
- **Precondition:** the source is the current authorized holder, the target is eligible to take
  over, and any required gate has authorized the transfer.
- **Semantic effect:** the target becomes the active owner of the scoped continuation; the source
  ceases to be the active owner unless a separate oversight role or later transfer is declared.
- **Authority effect:** transfers only the control authority already held within the scope. It does
  not manufacture domain approval authority or widen permissions.
- **Visibility:** the successor receives only the declared transferred context. Full-history and
  filtered handoffs are different payload policies under the same control effect.
- **Terminal and failure behavior:** success requires an accepted transfer receipt and one new
  active holder. If delivery or acceptance fails, control remains with the source; partial or
  ownerless transfer is invalid. A return of control requires another explicit transfer.
- **Legal composition:** transfer chains are legal. Cycles require versioned occurrences and an
  explicit bound/termination policy. Parallel transfers of the same exclusive scope are invalid
  unless the scope itself declares multi-holder semantics.

OpenAI handoffs and Microsoft handoff orchestration independently witness the ownership change
([OpenAI handoffs](https://openai.github.io/openai-agents-python/handoffs/),
[Microsoft handoff](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)).
This is a target-model relation, not current local runtime behavior.

### `gates`

- **Endpoints and direction:** accepted decision evidence -> a guarded transition, branch, release,
  or terminal occurrence.
- **Payload/evidence:** decision type and value, deciding actor, authority scope, subject/version,
  rationale/evidence references, policy/profile identity, and quorum when applicable.
- **Precondition:** the actor has the declared authority, the decision concerns the exact eligible
  subject/version, and the required decision policy is satisfied.
- **Semantic effect:** permits, denies, selects, or terminates the guarded transition. An
  assessment or message without an accepted authoritative disposition cannot substitute for it.
- **Authority effect:** exercises pre-existing authority; the edge does not create that authority.
- **Visibility:** the transition evaluator sees the decision evidence required for audit. Wider
  disclosure remains a separate visibility policy.
- **Terminal and failure behavior:** an absent decision waits; deny/reject follows its declared
  branch; invalid authority or subject mismatch fails closed. Conflicting decisions require an
  explicit precedence/quorum policy rather than last-write-wins.
- **Legal composition:** gates may guard branches, joins, loop exits, rework, or terminal release.
  Several gates compose only through an explicit boolean/quorum rule. A gate may precede
  `transfers_control`, but authorizing a transfer and performing it remain distinct facts.

Local precedents include declared `gates`, review acceptance, skeptic confirmation, and the human
disposition in robot-talks. Their authority owners differ, which is why gate evidence must carry
scope and actor rather than rely on the word “approval”
([authority-evidence: action matrix](stages/01-exploration/authority-evidence.md#action-and-authority-matrix)).

## What is not a relation type

| Layer | Contents | Why separate |
|---|---|---|
| Graph combinators | `then`, parallel, branch, fan-out, fan-in/barrier, repeat | They determine shape and activation, not evidence, obligation, or authority. |
| Roles and bindings | writer, reviewer, skeptic, synthesizer, verifier, human approver; agent/seat/group assignment | The same role may participate in different relations, and the same relation survives reassignment. |
| Schemas and occurrence kinds | artifact schema, message schema, assessment occurrence, decision occurrence, subject slot | They type data and work contracts; they do not by themselves create a relation between owners. |
| Recipes | sequential handoff, review, zig-zag, feedback, robot-talks, delegation workflow, handoff workflow | They compose several relations, combinators, roles, and policies. |
| Policies | independence, reveal, quorum, convergence, loop cap, deadline, allowed successor, no-self-review | They constrain a relation or recipe and vary independently of its meaning. |
| Runtime effects | schedule, bind, materialize, checkpoint, interrupt, retry, cancel, replay, compensate | These are performed by runtime owners. A semantic edge may require an outcome but does not appropriate its mechanism. |

### Why `assessed_by` is demoted, not erased

An assessment remains a first-class occurrence with:

- an exact subject/version input slot populated by `supplies`;
- a declared assessment profile, criteria, lens, and disposition/output schema;
- a reviewer binding and separate no-self-review/independence policy;
- output evidence supplied to synthesis or a decision occurrence;
- a `gate` only when an authorized disposition may release or deny work.

Under that contract, `subject assessed_by reviewer-occurrence` adds no observable fact. Subject
identity is recoverable from the typed slot, the assessment obligation from the occurrence kind,
criteria from its profile, authorship from its binding, and authority from a separate gate. Keeping
the edge would duplicate those facts. This resolves the exploration disagreement by retaining the
behavior proposed in
[generative-basis.md](stages/01-exploration/generative-basis.md) while rejecting only its primitive
edge status. If a later trace shows an assessment relation whose subject, obligation, or authority
cannot be recovered this way, the demotion must be reopened.

## Recipe reconstructions

### Sequential handoff

`producer occurrence -> accepted evidence -> consumer slot`, using `requires` for readiness and
`supplies` for exact materialization, composed with `then` or fan-in. Runtime acceptance and target
binding stay runtime/control-plane effects. No authority transfers.

### Review

The frozen subject is `supplies`-linked to independent assessment occurrences. Those occurrences
run in parallel and supply their findings to synthesis; verifier assessment may follow in the same
way. Only accepted approver decision evidence `gates` rework or release. Reviewer, verifier, and
approver remain distinct bindings/policies rather than edge kinds.

### Zig-zag

A draft is supplied to a fan-out of assessment occurrences. Their evidence fans in to the writer's
next version, which requires the prior round and receives the objections. The revision is supplied
back to the same skeptic bindings for reconfirmation. `repeat` plus preserved identity,
convergence, dissent, and loop-cap policies controls further rounds; gate decisions release or
terminate. No `zig-zag` primitive is needed.

### Feedback

A finding or assessment is supplied to a decision occurrence. An accepted `changes_required`
decision gates a remediation branch; the responsible work occurrence requires that decision and
receives the exact finding/evidence. New output is a new version and may be reassessed. Advisory
feedback omits the gate and therefore cannot release work. This is one concrete recipe; the corpus
does not justify assigning it to every use of the legacy `feedback` label.

### Robot-talks

A human gate authorizes decomposition. Independent investigation occurrences run in parallel and
supply evidence to synthesis. Optional cross-challenge adds assessment occurrences and repeated
evidence exchange, not a new relation. The synthesized tensions are supplied to a human decision
occurrence; only its gate disposition authorizes a follow-up branch. Agent evidence never becomes
action authority by itself.

## Removal tests and verdict matrix

| Candidate | Owner or operational precedent | Witnessed? | Sound as primitive? | What removal loses | Verdict and use mode |
|---|---|---|---|---|---|
| `requires` | Local Protocol Governance `depends_on`; local sequential readiness | Yes, locally, with generic execution still absent | Yes, provisionally | A pure prerequisite with no content visibility becomes indistinguishable from delivery or must be hidden in scheduler code. | **GO — build from owned local precedent.** |
| `supplies` | Local legacy-managed sequential compiler | Yes, narrowly deployed | Yes | Exact bytes, provenance, slot visibility, and conflicting-delivery behavior disappear into generic ordering. | **GO — already deployed narrowly; generalize from owned precedent.** |
| `delegates` | OpenAI agent-as-tool; Microsoft agent-as-tool | Yes, in two official external contracts | Yes, for the examined corpus | A bounded specialist call with retained manager responsibility and mandatory return becomes indistinguishable from an independent dependency. | **GO — build from identified external precedents; no local implementation claim.** |
| `transfers_control` | OpenAI handoff; Microsoft handoff orchestration | Yes, in two official external contracts | Yes, for the examined corpus | The identity of the active responsibility holder before and after a handoff is lost. | **GO — build from identified external precedents; no local implementation claim.** |
| `gates` | Local Protocol Governance `gates`; review, skeptic, and human dispositions | Yes, locally, across several manually governed workflows | Yes, provisionally | Advice, assessment, and authoritative release become indistinguishable; authority must be inferred from topology or text. | **GO — build from owned local precedent.** |
| `assessed_by` | Local `review_of`, review skill, and exploration proposal | Assessment behavior yes; irreducible edge no | No, under the mandatory assessment-occurrence contract | Nothing: exact subject, obligation, criteria, authorship, and authority remain recoverable from `supplies`, occurrence/profile/binding, policy, and optional `gates`. | **KILL as primitive — tautological; retain the assessment occurrence contract.** |

“Owned external precedent” means an official, operationally described behavior from an identified
system that can be built from; it does not mean local implementation or market adoption.

Named protocols also fail removal as primitives: `sequential`, review, zig-zag, feedback, and
robot-talks decompose into the retained relations plus separated layers. Their protocol names
remain valuable recipe identities.

## Pairwise-collapse tests

Every pair among the five admitted relations preserves at least one observed difference:

| Pair | Why they do not collapse |
|---|---|
| `requires` / `supplies` | Eligibility can exist without visibility; delivery can occur before all prerequisites make the consumer eligible. |
| `requires` / `delegates` | A prerequisite grants no performance authority, retained-parent responsibility, or return obligation. |
| `requires` / `transfers_control` | Readiness does not change the active owner. |
| `requires` / `gates` | A fact may be a prerequisite without being an authoritative decision; a gate can select or deny a branch. |
| `supplies` / `delegates` | Context delivery grants visibility, not an obligation and scoped authority to perform work or return its outcome. |
| `supplies` / `transfers_control` | The same context can be delivered while control stays put; handoff changes the active holder even with filtered context. |
| `supplies` / `gates` | Evidence can be delivered without authority; a gate requires authenticated decision scope and has a release effect. |
| `delegates` / `transfers_control` | After delegation the source remains responsible and continuation returns; after transfer the target becomes active owner and no automatic return exists. This is independently witnessed by OpenAI and Microsoft. |
| `delegates` / `gates` | Delegation assigns bounded performance while retaining parent ownership; a gate decides a transition and need not assign any performer. |
| `transfers_control` / `gates` | A gate may authorize a handoff, but the decision fact alone does not mutate ownership; a transfer may also be permitted by standing policy without a new approval gate. |

The strongest rejected collapse is `delegates == transfers_control`: it would make two externally
documented traces with the same participants indistinguishable precisely where responsibility and
return-of-control differ. The strongest accepted collapse is `assessed_by == supplies(subject,
assessment.subject_slot) + assessment occurrence contract`; authority, if any, remains in `gates`.

## Compact mapping to current systems

| System | What it directly supplies | Mapping to the candidate basis | Semantic remainder |
|---|---|---|---|
| OpenAI Agents SDK | Runner, tools, agent-as-tool, handoff, HITL, `RunState`; ordinary Python control flow | Strong witness for `delegates` and `transfers_control`; tool approvals can supply gate evidence | Generic graph relations, joins, review authority, and convergence remain application code. |
| LangGraph | State, nodes, fixed/conditional edges, `Command`, `Send`, cycles, checkpointers, interrupts | Substrate for `requires`/`supplies`; application state and routing can implement transfer and gates | Relation meaning, authority, visibility, quorum, and protocol termination remain application contracts. |
| Google ADK 2.x | Graph nodes/routes, typed output, joins, back-edges, human input | Substrate for dependency, supply, composition, and human decision evidence | No separate semantic edge algebra for delegation, ownership, review, or authority. |
| Microsoft Agent Framework | Typed executors/messages, routing edges, checkpoints, agent-as-tool, handoff orchestration | Strong witness for both `delegates` and `transfers_control`; graph substrate covers composition | Evidence acceptance, review authority, privacy, quorum, and convergence remain application code. |
| CrewAI | Event-driven starts/listeners/routers, state, persistence, human feedback | Substrate for dependency, branching, loops, and possible gate evidence | No first-class ownership transfer or typed semantic relation contract. |
| AutoGen, adjacent | Experimental GraphFlow, teams, handoff messages | Expressive precedent only | Maintenance mode prevents treating it as an active-foundation candidate. |

Official-source details and maturity caveats remain in
[current-solutions.md](stages/01-exploration/current-solutions.md). The corpus establishes available
mechanisms and publisher contracts, not adoption.

## Current runtime versus target semantic model

### Current local capability

- `ProtocolRecipe` V1 names `depends_on`, `review_of`, `feeds`, and `gates`, but is a
  non-authoritative DAG candidate; those labels do not have the relation contracts above.
- The legacy-managed compiler executes only `sequential`, requires pre-materialized handoff
  receipts, and rejects feedback and zig-zag connections.
- The sequential path provides the narrow `supplies` witness: immutable accepted output to a
  digest-bound target manifest.
- Zig-zag is manually staged; review is partly witnessed by executed dispatches; feedback remains
  underdetermined; robot-talks is outside the governed dispatch runtime.
- No current local relation executes general delegation-with-return or transfer of control.
- Scheduling, binding, retry, cancel, checkpoint, recovery, and effective-input construction remain
  runtime/kernel responsibilities; routing/delivery remains the Work Bus concern; confirmation
  authority remains with ACI governance.

### Target model proposed by this research

- Recipes compile to versioned graphs whose edges use the five semantic relation types and whose
  topology uses separate combinators.
- Occurrence, evidence, slot, decision, and control-scope contracts make evidence and authority
  queryable without inferring them from prose or adjacency.
- A compiler validates endpoint compatibility, authority scope, visibility, legal composition,
  and terminal/failure obligations before runtime execution.
- Runtime owners implement scheduling and durable effects but report evidence sufficient to prove
  that each semantic obligation was or was not satisfied.

Nothing in this section authorizes implementation or claims the present compiler can execute the
target model.

## Completeness claim, counterexamples, and extension rule

The claim is only this: the five relations reconstruct the five examined local protocol families
and preserve the additional delegation/control distinction witnessed in the external sample. It
does not prove coverage of every possible agent communication.

Known counterexamples or unresolved areas that may force extension are:

- negotiation in which authority and commitments emerge mutually rather than from a current
  responsibility holder;
- revocation, lease, or shared-control semantics that cannot be represented as a gate plus a
  versioned control transfer;
- private multi-party channels, selective reveal, dynamic membership, broadcast receipt, or
  confidentiality obligations that are not reducible to per-slot supply policy;
- compensation and irreversible external effects;
- generic feedback whose owner and generation boundary differ from the concrete rework recipe;
- whether mandatory input slots could make some uses of `requires` redundant;
- whether delegation belongs on a control scope or on a work occurrence in the eventual physical
  graph schema.

A new primitive should be admitted only when a concrete trace has an owner and witness, and removal
or replacement by the current relations plus combinators, roles, schemas, recipes, policies, and
runtime effects loses an observable endpoint, payload/evidence obligation, authority change,
visibility boundary, or terminal/failure behavior. Otherwise it belongs to one of those separated
layers.

## Explicit hypotheses for the next gates

### Precedent gate

- **P1:** `requires`, `supplies`, and `gates` each build from owned local artifacts rather than
  invented vocabulary.
- **P2:** `delegates` and `transfers_control` each have at least two independent official operational
  precedents — OpenAI Agents SDK and Microsoft Agent Framework — with the claimed responsibility
  difference.
- **P3:** No current official source in the sample establishes real-world adoption or a complete
  semantic relation algebra; any stronger market claim must fail.

### Non-vacuity gate

- **N1:** A pure prerequisite trace exists that does not disclose source evidence; otherwise
  `requires` should collapse into mandatory `supplies`.
- **N2:** The digest-bound sequential handoff is a concrete `supplies` witness with observable
  provenance, visibility, and conflict behavior.
- **N3:** Agent-as-tool is a concrete `delegates` witness because the manager retains responsibility
  and receives a bounded return.
- **N4:** Handoff is a concrete `transfers_control` witness because the receiver becomes active owner.
- **N5:** Review/human disposition supplies a concrete `gates` witness only where actor authority,
  exact subject, decision evidence, and release effect are all present.

### Definitional-soundness gate

- **D1:** Each of the ten admitted relation pairs preserves at least one observable difference in
  the pairwise-collapse table.
- **D2:** `assessed_by` adds no fact beyond the mandatory assessment-occurrence contract; if a
  skeptic produces a non-recoverable subject, obligation, or authority fact, restore it as a
  candidate and rerun minimality.
- **D3:** All five local named patterns reconstruct without hidden authority or visibility encoded
  only in prose.
- **D4:** `gates` authorizes a transfer while `transfers_control` changes the holder; neither is
  allowed to impersonate the other.
- **D5:** The layer boundary remains intact: relation semantics do not absorb roles, topology,
  quorum/convergence, or retry/checkpoint mechanisms.

Failure of a hypothesis changes the candidate basis; it is not a documentation defect to be edited
away.
