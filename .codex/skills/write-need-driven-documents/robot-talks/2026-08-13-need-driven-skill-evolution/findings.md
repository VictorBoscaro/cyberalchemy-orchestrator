# Reviewed findings

Status: reviewed

## F1 - The movement contract lacks discriminating tests at its three main boundaries

- **Layer A holds:** The skill aims to conduct a reader through a necessary sequence and requires
  every passage to have a function (`SKILL.md:17-28`).
- **Layer B actually does:** Its opening rule can admit an interchangeable universal claim; its
  passage-function rule does not test whether one passage changes the reader state needed by the
  next; and its ending rule permits recap as an answer (`SKILL.md:22-28,94-100`;
  `reports/01-reader-movement.md` findings 1, 2, and 4;
  `ring/02-skill-engineering-response.md` sections 1-2).
- **Impact:** MAJOR for the intended essay behavior. The evidence establishes permissive gates, not
  that the skill alone caused any particular failed draft.
- **Action:** Add three compact, invisible revision tests: reject an opening that could introduce
  unrelated essays through noun substitution; after a passage, identify the new understanding or
  question that earns the next; require the ending to make the opening situation newly intelligible
  or judgeable rather than merely restating the route. Prescribe no rhetorical form or visible
  signposting.

## F2 - Sequential autonomy is absent and should remain a conditional case

- **Layer A holds:** A document must establish a reader-relative starting point (`SKILL.md:19-22`).
- **Layer B actually does:** The skill does not distinguish sufficient local grounding from recap or
  dependence on a predecessor (`reports/01-reader-movement.md` finding 3;
  `ring/02-skill-engineering-response.md` section 3).
- **Impact:** MAJOR when composing an essay series; none for a genuinely standalone task.
- **Action:** Add one conditional instruction: when a document belongs to a sequence, reconstruct
  the minimum causal premise needed to understand it alone, avoid redundant recap, and advance a
  new question. Test it alone and after its predecessor. Do not impose an absolute ban on naming a
  predecessor when that reference itself is necessary.

## F3 - Material restructuring is routed but lacks structural diagnosis

- **Layer A holds:** The description explicitly routes material restructuring (`SKILL.md:2-3`).
- **Layer B actually does:** The body supports forward composition and local revision but does not
  tell an editor to recover a draft's attempted reader movement before changing it
  (`SKILL.md:17-28,94-100`; `reports/01-reader-movement.md` finding 5;
  `ring/02-skill-engineering-response.md` section 4).
- **Impact:** MODERATE. The omission permits premature local or wholesale rewriting, but the review
  did not behaviorally demonstrate that failure.
- **Action:** Add one conditional diagnostic instruction: recover the draft's starting
  understanding, successive changes, and destination; locate the first unearned concept, inert
  transition, or restart; then revise from that break. Do not add a separate revision framework.

## F4 - No independent voice expansion is justified

- **Proposed concern:** The current permission for rhythm, warmth, and emphasis might allow
  expressive prose to disguise a missing relation (`reports/01-reader-movement.md:80-109`).
- **Counterevidence:** The same sentence already retains those choices only when they help
  comprehension and removes attention without return (`SKILL.md:54-57,94-100`). The reports provide
  no failed artifact attributable to this wording.
- **Disposition:** REJECTED as a standalone behavioral finding. The editor may sharpen the existing
  sentence only if it can do so without adding techniques, examples, a house voice, or a new section.
  F1's movement tests provide the stronger guard against decorative continuity.

## F5 - Example rebalancing is an implementation constraint, not a new capability

- **Evidence:** The catalogue and co-presence examples overlap, but terminology and presentation
  structure protect distinct failures (`SKILL.md:59-93`; `reports/02-skill-engineering.md` finding 3;
  `ring/01-reader-response.md` section 3).
- **Impact:** LOW by itself; relevant because simply appending F1-F3 would grow the skill toward a
  manual.
- **Action:** Fund the compact tests partly by compressing overlap only where both relational
  distinctions remain recoverable. Preserve the terminology and structure failures. Add a new
  example only if a later blind test shows that a compact instruction is repeatedly misunderstood;
  do not enforce a line-count target at the expense of behavior.

## F6 - Repository and package routing are compatible; intent is not proven

- **Evidence:** The package requests sparse explicit use and disables implicit invocation, while the
  repository mandates the same narrowly scoped skill by artifact type (`SKILL.md:2-3`;
  `agents/openai.yaml:4-7`; `AGENTS.md:13-18`; `ring/01-reader-response.md` section 1).
- **Impact:** LOW. Environment-dependent routing is expected and no actual conflict was found.
- **Disposition:** NO CHANGE. Retain metadata during this behavioral edit. Do not label the policy
  intentional as a fact; changing global invocation remains a separate product decision.

## F7 - Evidence location exposes a real policy tension but does not authorize relocation

- **Layer A holds:** Platform skill guidance excludes creation and testing documentation from a
  distributable runtime package (`C:/Users/victo/.codex/skills/.system/skill-creator/SKILL.md:123-133`).
- **Layer B actually does:** Robot-Talks requires preservation beside the context that owns the
  question and says existing sessions move only by explicit, separate request
  (`.agents/skills/robot-talks/SKILL.md`, Session Preservation). This investigation is currently
  beside the skill it evaluates.
- **Impact:** LOW for runtime context because the evidence is not referenced by `SKILL.md`;
  MODERATE only if the entire directory is distributed as the package.
- **Disposition:** DEFER TO HUMAN GATE. Do not move or delete the active or closed record as part of
  the skill edit. If package distribution makes purity material, choose an external owning context
  and authorize a separate atomic migration with stable references.

## F8 - Contract review cannot establish behavioral transfer

- **Layer A holds:** Mechanical validation can verify package shape, and the zig-zag reviews can
  verify whether the revised wording addresses the identified failure modes.
- **Layer B actually does:** Investigators and reviewers receive the diagnoses in advance; this is
  review, not blind forward-testing (`skill-creator/SKILL.md:362-370,386-416`;
  `reports/02-skill-engineering.md` finding 5; both ring responses on validation).
- **Impact:** MAJOR only if completion claims that the skill reliably improves essay output.
- **Action:** Before making that claim, run blind task executions that cover both the actual Part II
  problem and transfer to an unrelated conceptual essay in a sequence. Give fresh agents the skill,
  task, and raw source artifacts, not these findings. Evaluate the four behaviors in F1-F2. The two
  cases are a justified coverage design, not a universal minimum for every future skill edit.

## Review boundary

The behavioral edit is bounded to F1-F3, with F5 constraining its size. F4 and F6 require no
independent change. F7 requires an explicit human decision outside the edit. F8 limits the claim
that can be made after review. None of these findings authorizes turning the skill into a general
style manual.

## Findings review record

- Combined the opening, transition, and closure evidence under one movement-contract finding while
  separating what the evidence demonstrates from the unproven claim that the skill caused a draft.
- Narrowed sequential autonomy to a conditional capability and removed the absolute prohibition on
  naming a predecessor.
- Regraded restructuring from MAJOR to MODERATE because the failure is plausible but not
  behaviorally demonstrated.
- Rejected voice as a standalone expansion: the current skill already applies a comprehension and
  attention-return criterion, and additional technique guidance would risk a style manual.
- Reclassified example rebalancing as an implementation constraint and preserved the distinct
  terminology and structure examples.
- Corrected routing from "intentional" to "compatible but undecided"; no metadata change is
  supported.
- Corrected the evidence-location recommendation: Robot-Talks explicitly requires an independent
  migration request, so package purity remains a human-gated policy tension rather than an editor
  action.
- Limited the forward-test finding to claims of behavioral reliability and treated the proposed two
  cases as coverage for this revision, not a universal numerical rule.
- **Limits:** No blind writing execution was performed in this review; package distribution behavior
  and global invocation intent remain unknown. The review verifies the findings against the supplied
  contracts and records only.
