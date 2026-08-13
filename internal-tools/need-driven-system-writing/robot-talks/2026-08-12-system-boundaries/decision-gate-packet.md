# Decision Gate — Writing-system boundaries

**Presentation:** pending. **Selections recorded:** none.

Choose one real option for each blocker: `D-01`, `D-02`, `D-04`, and `D-06`. The named
recommendations are non-binding. You may choose **Explain / more context** for any question; that
choice resolves nothing, and the same real options will be presented again after explanation.

## D-01 — What authority may make writing preferences durable across uses?

### D-01-A — Keep personalization per-run

- **Benefit:** prevents inferred or observed preferences from becoming canonical.
- **Cost or risk:** repeats preference discovery and provides no durable continuity.
- **Choose when:** avoiding unsupported persistence matters more than continuity.
- **Reversibility and downstream effect:** high reversibility; the system-definition stage may
  discuss per-run intake but leaves durable profiles, promotion, and revocation outside scope.
- **Related decisions:** `D-06` and `D-03`.

### D-01-B — Permit durability only after explicit author ratification

- **Benefit:** allows continuity while the author controls what becomes durable.
- **Cost or risk:** introduces ratification and revocation obligations whose lifecycle and
  representation remain unresolved.
- **Choose when:** cross-use continuity is intended and unresolved lifecycle details can remain
  explicitly undecided.
- **Reversibility and downstream effect:** medium to high if revocation remains possible; the stage
  may establish explicit author acceptance as a precondition, but may not choose profile fields,
  evidence thresholds, storage, or interview mechanics.
- **Related decisions:** `D-06` and `D-02`.

**Non-binding recommendation:** `D-01-B`, narrowly — allow durability only as an author-ratified
possibility, without assuming that a durable profile is always necessary.

**D-01-X — Explain / more context:** compare author effort, continuity, silent-persistence risk,
and the dependency on `D-06`, then present `D-01-A` and `D-01-B` again.

## D-02 — What status should the candidate shared core have?

### D-02-A — Treat the current core as scoped, versioned candidates

- **Benefit:** preserves a common basis for purpose, part/whole contribution, and
  evidence-calibrated claims without claiming universality.
- **Cost or risk:** scope and evidence status must remain visible; users may mistake “shared” for
  “permanent.”
- **Choose when:** the next stage needs a common basis for purpose-driven writing while keeping
  surface prescriptions outside it.
- **Reversibility and downstream effect:** high reversibility; the stage may distinguish candidate
  shared constraints from personal preferences and form-specific methods, but may not promote a
  universal writing doctrine.
- **Related decisions:** `D-05` and `D-06`.

### D-02-B — Keep all candidates advisory pending targeted evidence

- **Benefit:** avoids premature promotion and makes the least claim beyond current evidence.
- **Cost or risk:** leaves no operative common constraint even for the bounded purpose-driven
  writing class supported by the evidence.
- **Choose when:** scope extends beyond purpose-driven prose or provisional status cannot remain
  visible and enforceable.
- **Reversibility and downstream effect:** high reversibility; candidates may be catalogued but
  cannot be used as cross-profile gates.
- **Related decisions:** `D-03` and `D-06`.

**Non-binding recommendation:** `D-02-A` — use a versioned, scoped candidate core for
purpose-driven writing, explicitly excluding surface style rules.

**D-02-X — Explain / more context:** distinguish scoped constraint, advisory candidate, personal
preference, and universal principle, then present `D-02-A` and `D-02-B` again.

## D-04 — What authority may an automated check have?

### D-04-A — Establish a strict result-authority boundary now

- **Benefit:** permits deterministic checks of explicit predicates while reserving semantic
  conclusions for attributable, evidence-bearing judgment.
- **Cost or risk:** every future check must state exactly what its result establishes and avoid
  broader quality language.
- **Choose when:** automation remains within the future system's possible scope.
- **Reversibility and downstream effect:** medium reversibility; a check may constrain delivery only
  for its explicit predicate under a separately decided policy and cannot approve prose, evidence
  sufficiency, criterion adequacy, or reader effect.
- **Related decisions:** `D-03` and `D-02`.

### D-04-B — Defer the authority decision and exclude automated delivery constraints

- **Benefit:** avoids premature result types and false authority until concrete checks and failure
  cases exist.
- **Cost or risk:** forgoes defensible structural enforcement and may preserve preventable
  omissions.
- **Choose when:** the next stage can exclude automation entirely and concrete cases should precede
  a general boundary.
- **Reversibility and downstream effect:** high reversibility; automation may not block or approve
  delivery, and no automated quality claim is in scope.
- **Related decisions:** `D-03` and any later check-specific policy.

**Non-binding recommendation:** `D-04-A` — establish the result-authority boundary without
designing any check or deciding whether a check should block delivery.

**D-04-X — Explain / more context:** explain why explicit predicate satisfaction differs from
semantic adequacy, including reversibility and delivery effects, then present `D-04-A` and
`D-04-B` again.

## D-06 — What authority may promote learning residue into durable rules?

### D-06-A — Require explicit approval by the relevant human authority

- **Benefit:** permits learning while keeping residue, inference, and model updates noncanonical
  until accepted by a human with relevant authority.
- **Cost or risk:** concrete owners and evidence thresholds remain unknown, and approval adds
  governance work.
- **Choose when:** the future system should learn across uses while preserving human authority.
- **Reversibility and downstream effect:** medium to high if changes remain versioned and
  revocable; the stage may establish explicit human promotion as an invariant but must defer owner
  assignment, thresholds, workflows, and automatic behavior.
- **Related decisions:** `D-01` and `D-02`.

### D-06-B — Keep all use residue noncanonical pending targeted evidence

- **Benefit:** fully avoids silent promotion while ownership and evidence thresholds remain
  unknown.
- **Cost or risk:** no lesson from use can change durable behavior until a later decision opens a
  promotion path.
- **Choose when:** the next stage does not need durable learning or cannot identify the relevant
  human authority.
- **Reversibility and downstream effect:** high reversibility; observations may inform a later
  proposal but cannot modify preferences, principles, skills, or system behavior.
- **Related decisions:** `D-01` and `D-02`.

**Non-binding recommendation:** `D-06-A`, with owner assignment deferred — require explicit human
approval for every durable promotion while leaving the owner, evidence threshold, and whether any
promotion occurs unresolved by category.

**D-06-X — Explain / more context:** distinguish observation, noncanonical residue,
recommendation, and promotion; compare continuity, governance cost, reversibility, and
silent-rewrite risk; then present `D-06-A` and `D-06-B` again.

## Deferrable decisions recorded for the next stage

### D-03 — Minimum formalization

- **Recorded default:** defer mandatory formalization until an observed handoff (`D-03-A`). The
  stage may discuss traceability, but no mandatory schema, universal quality form, aggregate score,
  or schema gate exists.
- **Reconsideration trigger:** an observed handoff with a named owner and consumer, or a separately
  authorized comparison that can measure interpretability against author cost.

### D-05 — When to specialize

- **Recorded default:** defer specialization until a distinct contract is demonstrated (`D-05-A`).
  The general procedure remains the only operative method; noncanonical form observations create
  no new contract owner.
- **Reconsideration trigger:** a named form and failure demonstrate a required field or gate not
  owned by the general procedure.

These defaults are reversible deferrals, not human selections. Choosing the alternative for either
item would require separate research or experiment authorization.

Reply with one real option ID for each blocker, for example: `D-01-B, D-02-A, D-04-A, D-06-A`.
You may instead request any corresponding `-X` Explain option. No architecture, planning,
implementation, schema, skill, research, experiment, automation, promotion, or code is authorized
by this packet or by a recommendation.
