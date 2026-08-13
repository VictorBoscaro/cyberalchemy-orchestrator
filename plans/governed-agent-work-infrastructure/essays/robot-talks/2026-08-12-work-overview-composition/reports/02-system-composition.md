# 1. Key Findings

- The smallest explanatory set supported by the overview is not its full noun inventory. It is: an
  **objective**; bounded **parts of work** intended to realize it; a **participant** acting through a
  **role** with limited **authority**; an authorized work description (**dispatch**); a particular
  execution (**attempt**); and the resulting records, result, and evidence. These distinctions are
  introduced across the document rather than as one initial catalogue: objective and parts at
  [work-and-knowledge-system-overview.md:62](../../../work-and-knowledge-system-overview.md#L62),
  participant and role at
  [work-and-knowledge-system-overview.md:97](../../../work-and-knowledge-system-overview.md#L97),
  dispatch and attempt at
  [work-and-knowledge-system-overview.md:92](../../../work-and-knowledge-system-overview.md#L92) and
  [work-and-knowledge-system-overview.md:139](../../../work-and-knowledge-system-overview.md#L139),
  and result versus evidence at
  [work-and-knowledge-system-overview.md:106](../../../work-and-knowledge-system-overview.md#L106).
  Knowledge requires a second, later local set: information, provenance, evidence, review,
  acceptance, and applicability scope
  ([work-and-knowledge-system-overview.md:184](../../../work-and-knowledge-system-overview.md#L184)).

- The consequential structure lies in the relations among those concepts, not in the concepts
  alone. At minimum, the overview must keep separate: a part **contributes to** an objective; a
  participant is **assigned** work; a decision **authorizes** action; an attempt **executes** a
  dispatch; an attempt **produces** a result; evidence **supports** acceptance; and accepted
  knowledge **applies within** a scope. The overview already warns that conformance does not imply
  success ([work-and-knowledge-system-overview.md:101](../../../work-and-knowledge-system-overview.md#L101))
  and that provenance does not imply truth or suitability
  ([work-and-knowledge-system-overview.md:189](../../../work-and-knowledge-system-overview.md#L189)).
  The companion view makes the structural reason explicit: `produced-by`, `accepted-as`,
  `part-of`, `authorized-by`, `uses`, and `supports` are not interchangeable
  ([work-context-system-view/essay.md:252](../../../work-context-system-view/essay.md#L252)).

- A first useful larger composition is a **bounded work arrangement**: objective + proposed parts +
  dispatch + participants + roles + authority + constraints. It is useful because it gathers the
  answers to “what are we trying to do, how are we dividing it, who may do what, and within which
  bounds?” What emerges is the capability to turn an incomplete intention into inspectable,
  authorized work rather than silent execution
  ([work-and-knowledge-system-overview.md:82](../../../work-and-knowledge-system-overview.md#L82)).
  Its boundary is synthesized: these responsibilities may be distributed differently, and the
  illustrated composition is explicitly not the system's definition
  ([work-and-knowledge-system-overview.md:130](../../../work-and-knowledge-system-overview.md#L130)).

- A second useful larger composition is **accountable execution**: dispatch version + attempt +
  contributions/decisions/events + result + evidence + observation. It is useful because these
  local elements together answer three questions that none answers alone: what was prescribed,
  what occurred, and what the occurrence establishes. The composition enables a current view,
  retrospective reconstruction, and independent assessment of authorization and success
  ([work-and-knowledge-system-overview.md:133](../../../work-and-knowledge-system-overview.md#L133),
  [work-and-knowledge-system-overview.md:169](../../../work-and-knowledge-system-overview.md#L169)).
  Its boundary is synthesized because observation is a projection over stored events, not another
  source record, and no projection is automatically complete
  ([work-and-knowledge-system-overview.md:176](../../../work-and-knowledge-system-overview.md#L176);
  [work-context-system-view/essay.md:666](../../../work-context-system-view/essay.md#L666)).

- A third useful larger composition is a **knowledge-continuity loop**: information produced by
  work + provenance + evidence + authorized review + acceptance within scope + use as context in
  later work. It is useful because it explains how learning can cross executions without turning
  every stored result into truth. What emerges is responsible reuse: later work can inherit
  supported understanding without reconstructing it, while retaining its source and limits
  ([work-and-knowledge-system-overview.md:195](../../../work-and-knowledge-system-overview.md#L195),
  [work-and-knowledge-system-overview.md:203](../../../work-and-knowledge-system-overview.md#L203)).
  The boundary is explicitly synthesized: “work system” and “knowledge system” are distinct
  responsibilities joined in both directions, not naturally isolated stores, and the knowledge
  infrastructure is not yet defined by its own system view
  ([work-and-knowledge-system-overview.md:215](../../../work-and-knowledge-system-overview.md#L215),
  [work-and-knowledge-system-overview.md:232](../../../work-and-knowledge-system-overview.md#L232)).

# 2. Gaps or Inconsistencies

- The overview presents a broad aggregate inventory before its local concepts and relations have
  been established (“objective, parts, responsibilities, decisions, limits, progress, results,
  and supporting evidence”), then repeats a similar inventory as if togetherness itself explained
  the system ([work-and-knowledge-system-overview.md:28](../../../work-and-knowledge-system-overview.md#L28),
  [work-and-knowledge-system-overview.md:76](../../../work-and-knowledge-system-overview.md#L76)).
  It does not yet return to show what capability emerges from specific subsets of those elements.

- The closest existing composition statement is a flat list—dispatch, attempts, participants,
  roles, authority, and records—immediately named “ephemeral work infrastructure.” It explains the
  persistence property but not why these elements form one explanatory unit or which relations
  hold it together ([work-and-knowledge-system-overview.md:160](../../../work-and-knowledge-system-overview.md#L160)).

- The overview's two trace directions compress several independent paths. It connects objective to
  work and result back to attempt/dispatch/decision/evidence
  ([work-and-knowledge-system-overview.md:144](../../../work-and-knowledge-system-overview.md#L144)),
  while the companion requires purpose, authority, assignment, causation, and realization to be
  independently inspectable and not inferred from one another
  ([work-context-system-view/essay.md:109](../../../work-context-system-view/essay.md#L109)).
  A simplified overview can omit vocabulary, but not imply that one generic trace establishes all
  five meanings.

- There is a direct architectural inconsistency about orchestration depth. The overview permits an
  orchestrator to invoke another orchestrator when the dispatch and depth limit permit it
  ([work-and-knowledge-system-overview.md:154](../../../work-and-knowledge-system-overview.md#L154));
  the agent-language view says an invoked orchestrator must not invoke another and assigns all
  decomposition to the root orchestrator
  ([agent-language-system-view/essay.md:211](../../../agent-language-system-view/essay.md#L211)).
  No larger composition should rely on either rule until this is resolved or explicitly presented
  as an open alternative.

# 3. Local Tensions

- **A small explanatory composition versus plural context.** Grouping work into a bounded
  arrangement helps explain the product, but the same work can simultaneously belong to a feature,
  Plan, sprint, research result, agent assignment, and authority decision. The group must be
  presented as one useful projection, not a universal container
  ([work-context-system-view/essay.md:186](../../../work-context-system-view/essay.md#L186)).

- **A three-composition explanation versus eight candidate architectural responsibilities.** The
  three proposed groups optimize explanatory altitude; the companion architecture separately lists
  authoring, knowledge/relations, governance, orchestration, execution, event history,
  verification, and observability. That list explicitly says its boundaries may be semantic,
  authority-related, or implementation choices
  ([agent-language-system-view/essay.md:323](../../../agent-language-system-view/essay.md#L323)).
  The overview should not make its explanatory groups look like selected deployment layers.

- **Knowledge acceptance versus authority to reuse.** Calling knowledge “accepted for reuse” is a
  useful compression, but the overview also says acceptance does not authorize every later use;
  authority and constraints are reevaluated in the receiving work
  ([work-and-knowledge-system-overview.md:189](../../../work-and-knowledge-system-overview.md#L189)).
  The knowledge-continuity composition must preserve this two-stage boundary.

- **Composition creates understanding but can manufacture conclusions.** Showing how parts compose
  is necessary, yet even an intuitive chain such as task → specification → feature → objective
  supports a derived claim only under accepted composition rules, applicable versions, and direct
  witnesses ([work-context-system-view/essay.md:701](../../../work-context-system-view/essay.md#L701)).
  Narrative grouping must not silently upgrade adjacency into evidence.

# 4. Questions for Synthesis

- Should the document name the three explanatory compositions, or present them first as natural
  answers to practical questions and disclose their synthesized boundaries afterward?

- Is “bounded work arrangement” the right boundary, or should dispatch remain the culminating
  local concept and the larger composition be called the work system only after execution and
  observation have also been introduced?

- How much of the five-path distinction—purpose, authority, assignment, causation, realization—must
  remain explicit in the concise overview so that simplification does not create false inference?

- Which orchestration rule is current: bounded nested orchestrators or root-only orchestration with
  leaf agents? Until adjudicated, should orchestration depth disappear from this overview?

- Should experience, control, and transparency be presented as a second projection over these
  compositions (user-facing outcomes), while the three groups above remain an explanatory model of
  system responsibilities?
