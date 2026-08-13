# Decision recommendations — Need-Driven Writing System Boundaries

## Authority and stage

This artifact is the non-binding analysis for dispatch step `d01-analyze-decisions`. It does not
record a human choice, settle architecture, or authorize planning, schemas, skills, research,
automation, promotion, or code.

The classifications below are relative to one named next consequential stage: **a separately
authorized system-definition stage that may decide the internal tool's responsibility boundaries
and the order of later evidence-gathering, but may not implement them**. A decision is a blocker
only when that stage could otherwise assign authority or scope in a way that is difficult to undo.

The frozen evidence is the six-tension synthesis in [findings.md](findings.md), independently
verified by the `Repair verification addendum — 2026-08-12` in
[reports/05-synthesis.review.md](reports/05-synthesis.review.md). Every recommendation is advice;
only the human may select an option.

## Classification summary

| ID | Decision | Classification | Why now |
|---|---|---|---|
| `D-01` / `T-01` | Authority for durable personalization | **Blocker** | A system-definition stage cannot responsibly assign a persistent preference boundary without deciding whether continuity or per-run isolation governs it. |
| `D-02` / `T-02` | Status of the shared core | **Blocker** | The stage cannot define what is common to all use without deciding whether current candidates constrain work or remain only advisory. |
| `D-03` / `T-03` | Minimum formalization | **Deferrable** | The stage can preserve traceability as a goal while postponing mandatory fields until an observed handoff or bounded comparison supplies evidence. |
| `D-04` / `T-04` | Authority of automated checks | **Blocker** | Any future automation boundary would be unsafe if a structural result could silently inherit semantic-review authority. |
| `D-05` / `T-05` | When to specialize | **Deferrable** | No current evidence identifies a form with an independent contract; the general procedure can remain the only operative scope meanwhile. |
| `D-06` / `T-06` | Authority to promote learning residue | **Blocker** | A system-definition stage must not create a learning path that can silently rewrite personal or shared rules. |

No tension is classified as an assumption. Two temporary operating assumptions are stated under
the deferrable items; they constrain what may proceed and do not resolve the deferred decisions.

## D-01 — What authority may make writing preferences durable across uses?

- **Source tension:** `T-01`; eligible evidence `01.1`, `01.2`, `01.3`, `03.1`, `03.5`, `04.2`.
- **Classification:** **blocker** for the named system-definition stage.
- **Why it blocks:** the evidence supports neither silent persistence nor the necessity of a durable
  profile. Leaving the authority ambiguous could either overwrite the author's preferences or make
  cross-use continuity impossible by accident.

### Option A — Keep personalization per-run

- **Benefit:** preserves the authority boundary supported by the current per-text evidence and
  prevents inferred or observed residue from becoming canonical.
- **Cost or risk:** repeats preference discovery and provides no durable continuity even when an
  author wants it.
- **Choose when:** avoiding unsupported persistence matters more than continuity, or the next stage
  does not require cross-use personalization.
- **Reversibility:** high; a later, separately authorized durable path can be added after its owner
  and evidence threshold are decided.
- **Downstream impact:** the system-definition stage may discuss per-run intake but must leave
  durable profiles, promotion, and revocation outside scope.
- **Related decisions:** `D-06` promotion authority; `D-03` formalization.

### Option B — Permit durability only after explicit author ratification

- **Benefit:** allows continuity while keeping inferred preferences provisional and the author in
  control of what becomes durable.
- **Cost or risk:** introduces ratification and revocation obligations whose concrete lifecycle and
  representation are not established by the frozen evidence.
- **Choose when:** cross-use continuity is part of the intended system definition and the stage can
  preserve the unresolved lifecycle details without inventing them.
- **Reversibility:** medium to high if revocation remains possible; lower if later work treats the
  durable state as irrevocable or silently inferred.
- **Downstream impact:** the stage may establish an authority rule—explicit author acceptance is a
  precondition for durability—but may not choose profile fields, evidence thresholds, storage, or
  interview mechanics.
- **Related decisions:** `D-06` governs later promotion from use; `D-02` distinguishes personal
  preference from shared constraint.

### Recommendation — Option B, narrowly

Recommend allowing durable preference only as an **author-ratified possibility**, not assuming that
a durable profile is always necessary. This preserves both sides of the verified tension: current
evidence cannot justify inferred persistence (`01.1`–`01.3`), while an explicit authority boundary
can prevent a later continuity feature from redefining the author (`03.5`, `04.2`). The lifecycle,
fields, and evidence needed for ratification remain unresolved and outside this recommendation.

### Explain / more context

This is a non-committal choice and resolves nothing. If requested, explain why the decision blocks,
restate Options A and B unchanged, trace each to `T-01`, compare author effort and silent-persistence
risk, and show how the choice depends on `D-06`. Then ask the same question again with Options A,
B, and **Explain / more context**.

## D-02 — What status should the candidate shared core have?

- **Source tension:** `T-02`; eligible evidence `01.4`, `02.1`, `02.2`, `02.3`, `02.4`, `03.1`,
  `04.4`.
- **Classification:** **blocker** for the named system-definition stage.
- **Why it blocks:** without a status decision, the stage could accidentally present bounded
  defaults as universal rules or, in the other direction, omit every common reliance constraint.

### Option A — Treat the current core as scoped, versioned candidates

- **Benefit:** preserves a common basis for purpose, part/whole contribution, and evidence-calibrated
  claims without calling those candidates universal across all writing.
- **Cost or risk:** later uses must carry scope and evidence status; the candidates may change, and
  users may mistake “shared” for “permanent” unless status stays visible.
- **Choose when:** the next stage needs a common basis for purpose-driven writing but can preserve
  provisional scope and keep surface prescriptions outside it.
- **Reversibility:** high because the set remains versioned and revisable rather than constitutional.
- **Downstream impact:** the stage may distinguish candidate shared constraints from personal
  preferences and form-specific methods; it may not promote a universal writing doctrine.
- **Related decisions:** `D-05` specialization; `D-06` promotion authority.

### Option B — Keep all candidates advisory pending targeted evidence

- **Benefit:** makes the least claim beyond the frozen evidence and avoids premature promotion.
- **Cost or risk:** leaves the system-definition stage without an operative common constraint even
  for the bounded purpose-driven writing class supported by the evidence.
- **Choose when:** the intended scope extends beyond purpose-driven prose or the stage cannot keep
  provisional status visible and enforceable.
- **Reversibility:** high; candidate constraints can be admitted later through an explicit decision.
- **Downstream impact:** the stage may catalog candidates but cannot use them as cross-profile gates.
- **Related decisions:** `D-03` determines how status might later be represented; `D-06` governs
  promotion.

### Recommendation — Option A

Recommend a **versioned, scoped candidate core for purpose-driven writing**, with surface style
rules explicitly excluded. The final review confirms that `02.1`–`02.3` support bounded candidates
and that `02.4`, `01.4`, and `04.4` forbid silently promoting context-specific expression or a draft
model into universal law. This recommendation does not decide an admission test or future contents.

### Explain / more context

This is a non-committal choice and resolves nothing. If requested, explain the difference among a
scoped constraint, an advisory candidate, a personal preference, and a universal principle; trace
both options to `T-02`; restate Options A and B unchanged; then ask again with Options A, B, and
**Explain / more context**.

## D-03 — When should editorial judgment receive mandatory structure?

- **Source tension:** `T-03`; eligible evidence `02.4`, `03.3`, `04.1`, `04.2`.
- **Classification:** **deferrable**.
- **Why it can wait:** no minimum field set, comparative result, or measured author cost exists.
  The named stage can preserve the distinction between trace and proof without choosing a schema.

### Option A — Defer mandatory formalization until an observed handoff

- **Benefit:** avoids manufacturing objectivity or author burden before a concrete consumer and
  traceability need exist.
- **Cost or risk:** early judgments may remain less comparable, and evidence needed to design a
  later record may accumulate unevenly.
- **Choose when:** the next stage is defining responsibilities rather than running a bounded
  evaluation experiment.
- **Reversibility:** high.
- **Downstream impact:** conceptual work may proceed, but no universal form, mandatory field set,
  aggregate score, or schema gate may be introduced.
- **Related decisions:** `D-04` result authority; `D-01` preference representation.

### Option B — Authorize a bounded comparison of trace records

- **Benefit:** could produce evidence about interpretability and author cost using the candidate
  trace elements already supported by `04.1`.
- **Cost or risk:** even a pilot can be mistaken for a quality model; it requires a separate research
  authorization and cannot assume the candidate fields are the minimum.
- **Choose when:** a concrete handoff and comparison question have been named and the user separately
  authorizes research.
- **Reversibility:** high if outputs remain experimental and noncanonical.
- **Downstream impact:** permits only a future evidence-gathering proposal, not a schema or score.
- **Related decisions:** `D-02` provisional-core status; `D-04` semantic authority.

### Recommendation — Option A for the named stage

Defer mandatory formalization. The evidence supports traceable context but explicitly does not
identify a minimum structure or show that field completion proves textual quality. Reconsider when
an observed handoff has a named owner and consumer, or when a separately authorized comparison can
measure interpretability against author cost.

### Temporary operating assumption

The named stage may discuss traceability as a requirement, but **no mandatory schema, universal
quality form, or aggregate quality score exists**. This assumption expires when the reconsideration
trigger above is met or the human explicitly chooses otherwise.

## D-04 — What authority may an automated check have?

- **Source tension:** `T-04`; eligible evidence `02.3`, `03.4`, `04.3`.
- **Classification:** **blocker** for any system-definition scope that admits automation.
- **Why it blocks:** without an authority boundary, a future structural pass/fail result could be
  treated as evidence of clarity, adequacy, support, or reader effect that it cannot supply.

### Option A — Establish a strict result-authority boundary now

- **Benefit:** permits deterministic checks of explicit predicates while preserving attributable,
  evidence-bearing judgment for semantic conclusions.
- **Cost or risk:** every future check must state exactly what its result establishes and must avoid
  broader quality language; this adds discipline to check design.
- **Choose when:** automation remains in the future system's possible scope.
- **Reversibility:** medium; the boundary can later be refined, but relaxing it requires new evidence
  that a machine result supports the broader conclusion.
- **Downstream impact:** a check may constrain delivery only for its explicit predicate under a
  separately decided policy; it cannot approve prose, evidence sufficiency, criterion adequacy, or
  reader effect.
- **Related decisions:** `D-03` representation of judgments; `D-02` claim-force discipline.

### Option B — Defer the authority decision and exclude automated delivery constraints

- **Benefit:** avoids premature result types and false authority until concrete checks and failure
  cases exist.
- **Cost or risk:** forgoes even defensible structural enforcement and may preserve repeated,
  preventable omissions.
- **Choose when:** the next stage can exclude automation entirely and the user prefers concrete
  cases before setting a general boundary.
- **Reversibility:** high; a later decision can admit checks after evidence and review.
- **Downstream impact:** automation may not block or approve delivery; no automated quality claim is
  in scope.
- **Related decisions:** `D-03` and any later check-specific policy.

### Recommendation — Option A

Recommend establishing the authority boundary now, without designing any check. `04.3` supports
deterministic conclusions only where an explicit machine-readable predicate exists; `02.3` and
`03.4` preserve claim calibration and independent semantic-review authority. The recommendation
does not decide which checks exist or whether any check should block delivery.

### Explain / more context

This is a non-committal choice and resolves nothing. If requested, explain with concrete categories
of result—not new proposed checks—why predicate satisfaction differs from semantic adequacy; spell
out reversibility and delivery effects; restate Options A and B unchanged; then ask again with
Options A, B, and **Explain / more context**.

## D-05 — When should a form receive its own specialization?

- **Source tension:** `T-05`; eligible evidence `01.1`, `02.2`, `02.4`, `03.2`.
- **Classification:** **deferrable**.
- **Why it can wait:** form dependence is supported, but no current evidence identifies a form with
  an independent required field set or gate. Deferral does not prevent use of the general procedure.

### Option A — Defer specialization until a distinct contract is demonstrated

- **Benefit:** avoids duplicated guidance, fragmented ownership, and premature skill proliferation.
- **Cost or risk:** a real form-specific requirement could remain implicit until someone identifies
  and demonstrates the contract difference.
- **Choose when:** no current form has evidence of a requirement or gate the general procedure does
  not own.
- **Reversibility:** high.
- **Downstream impact:** the named stage may preserve specialization criteria but may not create a
  specialization.
- **Related decisions:** `D-02` shared versus form-specific constraints.

### Option B — Permit provisional form experiments without contract authority

- **Benefit:** can reveal whether a form has genuinely distinct requirements without immediately
  giving it a permanent owner or gate.
- **Cost or risk:** provisional guidance can still duplicate the general method or be mistaken for a
  canonical specialization.
- **Choose when:** a specific form and failure have been observed and a separate experiment is
  authorized.
- **Reversibility:** high if the experiment is explicitly noncanonical and expires.
- **Downstream impact:** permits only a future experiment proposal; it does not authorize a new
  skill, schema, or specialization now.
- **Related decisions:** `D-03` formalization and `D-02` core status.

### Recommendation — Option A

Defer specialization until a form demonstrates a required field set or gate not owned by the
general procedure. This directly preserves the reviewed formulation `03.2` without denying the
form dependence supported by `02.2` and `02.4`.

### Temporary operating assumption

The general procedure remains the only operative method. Form differences may be recorded as
noncanonical observations, but they create no new contract owner. Reconsider when a named form and
failure demonstrate a distinct required field or gate.

## D-06 — What authority may promote learning residue into durable rules?

- **Source tension:** `T-06`; eligible evidence `01.3`, `03.5`, `04.4`.
- **Classification:** **blocker** for any stage that admits learning from use.
- **Why it blocks:** an undefined promotion path can silently transfer authority from the author or
  human gate to the system, while forbidding all promotion would prevent validated learning from
  affecting later behavior.

### Option A — Require explicit approval by the relevant human authority

- **Benefit:** permits learning while ensuring residue, inference, and model updates remain
  noncanonical until a human with the relevant authority accepts the change.
- **Cost or risk:** the frozen evidence does not yet designate the concrete owner or evidence
  threshold for personal preferences, shared candidates, or operational methods; approval adds
  ongoing governance work.
- **Choose when:** the future system should learn across uses but must preserve human authority.
- **Reversibility:** medium to high if promoted changes remain versioned and revocable.
- **Downstream impact:** the stage may establish explicit human promotion as an invariant, but must
  defer owner assignment, thresholds, workflows, and automatic behavior.
- **Related decisions:** `D-01` durable personal preference; `D-02` shared-core status.

### Option B — Keep all use residue noncanonical pending targeted evidence

- **Benefit:** fully avoids silent promotion while ownership and evidence thresholds remain unknown.
- **Cost or risk:** no lesson from use can change durable behavior, even after repeated corrections,
  until a later decision opens a promotion path.
- **Choose when:** the next stage does not need durable learning or cannot yet identify the relevant
  human authority.
- **Reversibility:** high.
- **Downstream impact:** observations may be retained only as residue; they may inform a later
  proposal but cannot modify preferences, principles, skills, or system behavior.
- **Related decisions:** `D-01` and `D-02`.

### Recommendation — Option A, with owner assignment deferred

Recommend explicit human approval as the invariant for every durable promotion, while leaving the
specific owner and evidence threshold unresolved by category. `01.3` withholds canonical authorial
status from inference; `03.5` requires an explicit promotion decision by a designated owner; `04.4`
requires version and evidence status. This recommendation does not decide who the owner is, what
evidence is enough, or whether promotion should occur.

### Explain / more context

This is a non-committal choice and resolves nothing. If requested, distinguish observation,
noncanonical residue, recommendation, and promotion; explain how Options A and B change continuity,
governance cost, reversibility, and silent-rewrite risk; restate both options unchanged; then ask
again with Options A, B, and **Explain / more context**.

## Analyst gate posture

- **Result before human selection:** `BLOCK`.
- **Blockers remaining:** `D-01`, `D-02`, `D-04`, `D-06`.
- **Deferrable decisions:** `D-03`, `D-05`, each with a temporary operating assumption and a
  reconsideration trigger.
- **Assumption-classified decisions:** none.
- **Human decisions recorded:** none.
- **Next authorized step:** independent review of this recommendation artifact. It must not be
  presented as a human decision packet unless that review returns `PASS` and the dispatch's later
  mechanical presentation and packet-review steps also pass.
