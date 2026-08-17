---
tags: [agents-communication-infra, typed-graph, interaction-relations, research]
node_type: research-record
is_session: false
layer: [architecture, application]
nature: [research, informational]
status: draft
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Basis — Research Record

## Research question and boundary

What is the smallest extensible basis of semantically typed directed relations from which the
project can construct its observed agent-interaction protocols — including sequential handoff,
review, zig-zag, feedback, and robot-talks — without confusing relation meaning with graph shape,
roles, payload schemas, policy, or runtime mechanics?

This record synthesizes the four independent returns commissioned by
`2026-08-17-typed-interaction-graph-basis-exploration`. It does not repeat their full text. The
phase-one aggregate preserves all four returns verbatim in
[stages/01-exploration/research.md](stages/01-exploration/research.md); the decision-facing result is
in [findings.md](findings.md).

The result is bounded to the local artifacts and the contemporary official-source sample named
below. It is a candidate semantic model, not an implementation contract, schema, compiler design,
or claim of universal completeness.

## Provenance of the four independent returns

| Seat | Bound artifact | Assigned lens | Material contribution |
|---|---|---|---|
| Wirth, Niklaus | [local-as-built.md](stages/01-exploration/local-as-built.md) | Local executable and documented behavior | Distinguished declared, compiled, and executed semantics; reconstructed concrete traces for the five named patterns. |
| Milner, Robin | [generative-basis.md](stages/01-exploration/generative-basis.md) | Smallest local generative basis | Proposed `requires`, `supplies`, `assessed_by`, and `gates`; separated relations from combinators and policies; ran initial removal tests. |
| Follett, Mary Parker | [authority-evidence.md](stages/01-exploration/authority-evidence.md) | Authority, evidence, visibility, and topology counterexamples | Showed that identical graph shapes can carry different obligations and authority; identified the owner of propose, inspect, revise, confirm, decide, release, retry, and cancel actions. |
| Simon, Herbert | [current-solutions.md](stages/01-exploration/current-solutions.md) | Current external solutions | Compared five active systems plus AutoGen as an adjacent precedent; supplied the independent distinction between delegation-with-return and transfer of control. |

The initial definitions fixed the product-level graph decision and the evidence questions
([research-initial-definitions.md](research-initial-definitions.md)). The dispatch proposal required
independent exploration and later collapse testing
([dispatch-proposal.md](dispatch-proposal.md)). The staged execution decision explains why these
returns were produced as separate governed stages rather than through the current sequential
compiler, which cannot progressively materialize downstream handoffs
([typed-interaction-graph-research-execution.md](../../../../decisions/typed-interaction-graph-research-execution.md)).

## Method

The synthesis used five passes:

1. Separate names from observed traces. A ledger label, skill name, or market term was not treated
   as a primitive merely because it already existed.
2. Normalize each trace by endpoints, direction, payload/evidence, precondition, semantic effect,
   authority, visibility, completion/failure, and legal composition.
3. Place sequence, parallelism, branching, fan-out/fan-in, and repetition in a graph-combinator
   layer; place roles, schemas, recipes, policies, and retry/checkpoint effects in their own layers.
4. Admit a primitive only when removing it, or replacing it with another candidate plus the
   separated layers, loses an observed behavior.
5. Test every admitted pair for collapse and preserve counterexamples or uncertainty instead of
   resolving them by vocabulary preference.

The market sweep used only current official documentation and official repositories already
collected in the independent return. Publisher maturity claims were preserved as claims; repository
activity was treated as maintenance evidence, not adoption evidence. No new adoption claim is made.

## Material local evidence

### Implemented sequential trace

The narrow implemented trace is a resolved producer result, an immutable output receipt, a target
manifest slot, and a separately authorized target binding. Exact bytes, producer identity, schema,
ordering, cardinality, and digest are checked. The edge neither grants approval authority nor
creates the target binding. The compiler also requires the handoff receipt to exist before it
compiles, so it is not a progressive workflow scheduler. The detailed code citations and status
classification are preserved in
[local-as-built: sequential](stages/01-exploration/local-as-built.md#1-sequential)
and
[authority-evidence: sequential](stages/01-exploration/authority-evidence.md#1-sequential-integrity-bearing-dependency-not-delegated-judgment).

This trace independently witnesses two meanings that cannot be merged without loss: readiness
dependency and exact evidence delivery.

### Review trace

The canonical review shape is frozen subject material, independent attacks, synthesis, verifier
challenge, and final acceptance. Reviewing, verifying, and approving are different actions; a
reviewer does not thereby own revision, scheduling, or final acceptance. The executed example only
witnesses part of that canonical topology, a limitation retained in
[local-as-built: review](stages/01-exploration/local-as-built.md#2-review)
and the authority distinctions are in
[authority-evidence: review](stages/01-exploration/authority-evidence.md#2-review-evidence-bound-adjudication-plus-separately-owned-approval).

### Zig-zag trace

The local witness is a bounded protocol: writer draft, independent reports from three original
skeptics, writer response/revision, reconfirmation by those same skeptics, and convergence or a
typed exhausted exit. Identity preservation, revision ownership, dissent preservation, and the
parent-owned loop counter matter. It is manually staged and is explicitly rejected by the current
generic compiler. See
[local-as-built: zig-zag](stages/01-exploration/local-as-built.md#3-zig-zag)
and
[authority-evidence: zig-zag](stages/01-exploration/authority-evidence.md#3-zig-zag-bounded-challengerevisionconfirmation-protocol).

### Feedback trace

The corpus supports a conditional return to responsible work after a defect or missing-material
finding. It does not establish one generic `feedback` relation: endpoint identity, decision owner,
generation boundary, release fact, and convergence semantics remain open. A review
`changes_required` path is a concrete possible recipe, not proof that every feedback exchange means
review rework. See
[local-as-built: feedback](stages/01-exploration/local-as-built.md#4-feedback)
and
[authority-evidence: feedback](stages/01-exploration/authority-evidence.md#4-feedback-a-required-distinction-with-unresolved-operational-identity).

### Robot-talks trace

Robot-talks is independent inquiry followed by synthesis and a human disposition. Direct
cross-challenge is optional, and agent findings do not authorize implementation. It is presently a
skill workflow outside the governed dispatch runtime. See
[local-as-built: robot-talks](stages/01-exploration/local-as-built.md#5-robot-talks)
and
[authority-evidence: robot-talks](stages/01-exploration/authority-evidence.md#5-robot-talks-independent-inquiry-with-human-only-action-authority).

### Same topology, different meaning

The authority return supplies three decisive counterexamples: `A -> B` as sequential delivery
versus review; `A <-> B` as release-gated zig-zag versus optional evidential dialogue; and
reviewer-to-owner critique versus an accepted `changes_required` decision. Endpoint shape and
direction stay fixed while payload, authority, visibility, and release behavior change. The full
counterexamples are preserved in
[authority-evidence: same topology](stages/01-exploration/authority-evidence.md#same-topology-different-semantics).

## Material external evidence

The active sample was OpenAI Agents SDK, LangGraph, Google ADK 2.x, Microsoft Agent Framework, and
CrewAI. AutoGen was retained only as adjacent transition evidence because its official repository
declares maintenance mode. Full maturity qualifications and source-by-source observations are in
[current-solutions.md](stages/01-exploration/current-solutions.md).

The systems converge on graph or runner mechanics — state, typed messages, fixed or conditional
routing, joins, loops, interruption, and persistence — but do not establish a shared minimal
semantic edge algebra:

- OpenAI documents ordinary code orchestration and distinguishes
  [agents as tools from handoffs](https://openai.github.io/openai-agents-python/multi_agent/): the
  manager retains control in the first case, while the target becomes active in a
  [handoff](https://openai.github.io/openai-agents-python/handoffs/).
- LangGraph provides state, nodes, edges, conditional routing, `Command`, `Send`, cycles, and
  persistence in its [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api); its
  [handoff pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) remains
  application-defined state plus routing.
- Google ADK supplies graph nodes, routes, joins, and back-edges
  ([graph workflows](https://adk.dev/graphs/), [routes](https://adk.dev/graphs/routes/)), while
  typed outputs and human nodes do not themselves define review or authority semantics.
- Microsoft Agent Framework has typed workflow messages and routing
  [edges](https://learn.microsoft.com/en-us/agent-framework/concepts/workflows/edges). Its
  [handoff orchestration](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/handoff)
  independently distinguishes receiver task ownership from agent-as-tool manager responsibility.
- CrewAI Flows expose event-driven `start`, `listen`, joins, and routers
  ([Flows](https://docs.crewai.com/v1.15.16/en/concepts/flows)); human feedback can pause or route,
  but the application still owns the authority interpretation
  ([HITL](https://docs.crewai.com/v1.15.16/en/learn/human-in-the-loop)).
- AutoGen's [repository notice](https://github.com/microsoft/autogen) and experimental
  [GraphFlow](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/graph-flow.html)
  show why expressive precedent and suitable current foundation are different claims.

The strongest positive external witness is not a graph shape. It is an observable authority
difference repeated by OpenAI and Microsoft: delegation keeps responsibility with the manager and
expects a bounded return; handoff changes the active task owner. The synthesis therefore had to
test `delegates` and `transfers_control` in addition to the four locally proposed candidates.

## Preserved disagreements and uncertainties

- The generative-basis return provisionally retained `assessed_by` because it makes exact-subject
  review obligations easy to validate and query. The final synthesis demotes the edge only under an
  explicit assessment-occurrence contract; it does not demote assessment behavior.
- `requires` may be derivable from mandatory `supplies` slots in a more restrictive future model.
  The present corpus contains prerequisites that do not themselves grant visibility, so that
  collapse is not accepted here.
- Delegation and transfer of control have strong external witnesses but no equivalent current local
  executable relation. They are target-model candidates, not claims about current runtime support.
- The endpoint for control is not settled by the current storage schema. The synthesis uses a
  logical control scope or responsibility-holding occurrence and leaves physical schema choice to
  later design.
- Generic feedback, negotiation, private-channel dialogue, dynamic membership, compensation, and
  cross-run migration remain outside the proved sufficiency boundary.

## Research status

The four exploration returns are owned and usable. Their synthesis yields a five-relation candidate
basis and one explicit demotion, with no claim that implementation exists. The next gates should
attack precedent, non-vacuity, and definitional soundness using the hypotheses at the end of
[findings.md](findings.md).
