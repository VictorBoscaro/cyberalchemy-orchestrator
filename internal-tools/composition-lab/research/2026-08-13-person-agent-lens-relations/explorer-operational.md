# Operational evidence: people, enacted lenses, schemas, instances, and transformations

## Evidence boundary

This return uses local Codex conversation evidence dated 2026-08-07 through
2026-08-13 and artifacts in `cyberalchemy-orchestrator` and
`domainspec-lean-formalization`. Conversation text is paraphrased by default.
Forked subagent sessions repeat parent history, so repeated copies were treated as
one occurrence, not independent support.

The dispatch was explicitly authorized without `research-initial-definitions.md`.
That is an exception to the current generic `research` skill precondition, not
evidence that the precondition normally does not apply.

The strongest corpus-level limitation is attribution: the corpus contains concrete
Victor-to-agent interactions and artifacts that name Vlad as collaborator,
co-leader, coauthor, target, or future consumer. It does **not** contain a bounded
turn in which a Vlad-authored distinction is independently recoverable and then
consumed by Victor or the agent. Therefore this report does not manufacture a
three-person witness.

## Working distinctions

The same person can enact different operations in different episodes. These labels
refer to an occurrence, not to the person's identity:

- **selection:** chooses the question, evidence boundary, or distinctions that matter;
- **schema-proposal:** offers reusable slots, constraints, relations, or admissibility rules;
- **instantiation:** supplies a concrete realization under an already declared schema;
- **interpretation:** assigns a task-relative meaning to a source or result;
- **revision:** changes a prior distinction or rule after tension or counterevidence;
- **synthesis:** produces a new organized artifact from multiple bounded inputs;
- **transport/transformation:** maps an input artifact into another representation under a stated contract.

These roles should not be collapsed. The local formal artifact explicitly separates
declaration, instantiation, execution, mark, operational influence, and causality
(`../domainspec-lean-formalization/lean-formalization/PerspectiveMark.lean:11-29`).
The current lens audit likewise says that observer/lens identity has not been
operationally established and that a lens enacted in one episode can collapse into
the already-defined local `frame` unless it has an independent identity condition
(`../domainspec-lean-formalization/research/discipline-lens-observer-question-2026-08-13/research/findings.md:5-24`).

## Reconstructed episodes

### 1. ResonantOS meeting classification: coarse proposal, differentiated attacks, demotion

On 2026-08-08 Victor proposed an initial coarse classification of meetings into
work and community groupings, while identifying himself and Vladimir as community
leaders. He asked the agent to inspect local ResonantOS context and compare its own
view before and after that context
(`C:/Users/victo/.codex/sessions/2026/08/07/rollout-2026-08-07T22-52-06-019fdf11-feac-7b32-b3f3-8e4aef608455.jsonl:9`).

Occurrence typing:

| participant/seat | evidenced operation | input consumed | output |
|---|---|---|---|
| Victor | selection + schema-proposal | practical meeting problem | proposed coarse `work/community` distinction and request for two contextual readings |
| agent system | interpretation + revision + synthesis | Victor's proposal plus bounded repository evidence and independently differentiated attempts | ontology/system/engineer views, then a stricter minimal-ontology synthesis |
| Vlad | contextual stakeholder only | not evidenced | co-leadership is stated, but no separate distinction or transformation is attributable to him in this occurrence |

The resulting ontology retained `work` and `community-life` only as low-confidence
candidate families and recorded that the opposition may be false
(`research/resonantos-meetings/ontology-view.md:34-36,96-103`). Six independent
attempts then converged only on a bounded meeting occurrence, with purpose, actor,
authority, record, and other additions remaining perspective-dependent
(`research/resonantos-meetings/minimal-ontology-exploration/findings.md:7-37,51-74`).

Operationally, Victor did not *become a schema*. He proposed a schema candidate.
The agent did not simply instantiate it: it instantiated the research procedure,
used several enacted lenses, and revised/demoted the proposed classification. Vlad
was neither schema nor functor here on available evidence.

### 2. Perspective mark: intuition, scope correction, formal separation

On 2026-08-12 Victor proposed that residue might include a mark left by a productive
perspective, using a text/author example; he then sharpened the idea by distinguishing
declaring a perspective, instantiating its object, and checking whether its influence
is present
(`C:/Users/victo/.codex/sessions/2026/08/12/rollout-2026-08-12T15-55-43-019ff754-9322-7c73-962b-72a18b9fc6f6.jsonl:64,425`).

Occurrence typing:

- Victor enacted **example construction**, **distinction selection**, and **revision**.
  His second intervention narrowed a binary present/absent reading into separately
  testable declaration, instantiation, and observed influence.
- The agent system enacted **interpretation** and **formal transformation** by turning
  that distinction into `PerspectiveProtocol`, with separately typed declaration,
  realized lens, context, artifact, mark readout, and outcome readout
  (`../domainspec-lean-formalization/lean-formalization/PerspectiveMark.lean:34-48`).
- The formal result then pushed back on the initiating intuition: mark and operational
  influence are independent without soundness/completeness conditions, and neither
  instantiation nor a counterfactual mark implies execution
  (`../domainspec-lean-formalization/lean-formalization/PerspectiveMark.lean:200-210,492-525`).
- Vlad has no independently attributable move in this episode.

This is genuine consumption in both directions: the agent consumes Victor's
informal instance/example and constraint revisions; Victor can subsequently consume
a formal artifact whose counterexamples constrain the original intuition. It is
better described as a feedback chain of typed operations than as either person
being intrinsically a schema or functor.

### 3. Adaptive handoff to Vlad: proposal transformed into a governed candidate packet

On 2026-08-13 Victor proposed a handoff to Vlad whose permission/evidence burden
varies with risk, whose object may begin with a minimal schema and mature toward
category-level treatment, and whose representation leaves extension room
(`C:/Users/victo/.codex/sessions/2026/08/13/rollout-2026-08-13T12-12-25-019ffbae-824c-7083-9d9d-a308eb725a1c.jsonl:9`).

The agent transformed this conversational proposal into an informational baseline:
the target, risk rule, minimal-schema requirement, maturation requirement,
extension mechanisms, paired-scout topology, read-only boundary, and remaining
unknowns became explicit fields and obligations
(`research/adaptive-schema-handoff-domainspec-core/research-initial-definitions.md:5-41`).
It also produced two bounded dispatch proposals, separating target-repository
precedent inspection from source-side packet/non-vacuity inspection
(`research/adaptive-schema-handoff-domainspec-core/target-repo/opening-proposal.json:18-47`;
`research/adaptive-schema-handoff-domainspec-core/source-handoff/opening-proposal.json:18-55`).

Occurrence typing:

- Victor: **schema-proposal** at the product-obligation level and **selection** of
  recipient, safety posture, and scout arrangement.
- Agent: **interpretation**, **schema instantiation** (the proposal is instantiated
  in the repository's research/dispatch contracts), and **synthesis** into two
  inspectable artifacts.
- Vlad: **declared destination and anticipated evaluator/consumer**, not yet an
  observed interpreter, transformer, or functor. No returned Vlad artifact appears
  in the bounded evidence.

Calling Vlad a functor in this episode erases the most important fact: the mapping
has not yet been performed by him. Calling him a schema erases the difference
between his repository/authority context and the explicit schema that the handoff
packet must declare.

### 4. Joint-authorship and named participation are not lens witnesses

Recent conversations also identify Victor and Vladimir as coauthors/collaborators
on the *Entre Sistemas e Categorias* work. That establishes provenance and social
relationship, not a decomposition of semantic contributions. The relevant research
supports only joint use of several repertoires and explicitly rejects promoting
that joint use into one formal architecture of composed lenses
(`../domainspec-lean-formalization/research/entre-sistemas-lens-reflexivity-extension/research/findings.md:9-26`).

The same audit gives the applicable positive gate: lens composition survives only
for common-domain readouts `O_i : X -> Y_i`, an independently fixed task/pair, and a
demonstrated factorability change; without these, composition is a tuple of labels
with no added discriminative content (same file, line 20). A person's name cannot
supply the missing common carrier, readout, or law.

## Smallest positive witness

The smallest witnessed alternation is the first transformation in the adaptive
handoff episode:

1. Victor supplies a bounded obligation set `C` in conversational form: target,
   risk proportionality, minimal admission, maturation, extensibility, paired scouts.
2. The repository already supplies a research-initial-definition schema `R` and a
   dispatch-proposal schema `D`.
3. The agent produces `r : R(C)` and two proposal instances `d_target, d_source : D(r)`.

The parts are independently identifiable: Victor's constraints precede the files;
the artifact schemas exist independently of that content; and the outputs can be
checked field by field against both. This witnesses **schema-proposal ->
interpretation -> schema-instantiation/synthesis**. It does **not** yet witness a
functor in the categorical sense, because no category of inputs/outputs, morphism
mapping, identity law, or composition law was supplied. The strongest justified
term is a contract-governed transformation.

## Negative case

The ResonantOS meeting episode is the clean negative. Treating Victor, Vlad, and the
agent as three schemas/functors would imply three independently recoverable
representations or transformations. The evidence contains only Victor's initial
binary proposal, the agent system's multi-perspective revision, and Vlad's stated
co-leadership. Worse, the revision demoted the binary proposal and found a one-concept
intersection. Person-level naming would therefore hide both (a) absence of a Vlad
operation and (b) the difference between proposing a schema and revising it through
counterposed readouts.

Collapse condition: if a claimed participant-lens cannot be assigned a distinct
input, output/readout, task, and repeatable distinction policy in an occurrence,
“participant as lens/schema/functor” collapses to ordinary attribution, role naming,
or communication.

## Operational conclusion

The useful unit is not `Person = Lens`. It is an **enacted, typed relation**:

`actor/seat × task × input × distinction-policy × operation -> output/readout`.

A person may recurrently enact similar distinction policies, which can motivate a
reusable lens hypothesis. In another episode the same person can propose a schema,
instantiate someone else's schema, interpret an instance, revise a distinction, or
synthesize several returns. “Consumes instances” is useful when the consumed
artifact and governing schema are named. “Acts as a functor” becomes justified only
after object/morphism mappings and preservation of identities/composition are
shown. Until then, **schema proposer**, **instance producer/consumer**, **interpreter**,
and **contract-governed transformer** preserve more of what actually happened.

The corpus supports this weaker account for Victor and the agent. It leaves Vlad's
distinct enacted lens open pending one attributable input/output episode rather
than inferring it from collaboration, coauthorship, authority, or destination.
