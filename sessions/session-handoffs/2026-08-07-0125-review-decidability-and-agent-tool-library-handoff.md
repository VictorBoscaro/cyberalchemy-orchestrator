# Session Handoff: Review Decidability and the Agent-Accreted Tool Library

## Epistemic Status — read before anything else

**This is not novel, and no precedent search was run.**

Everything below is an observation from one session plus an architecture proposal drawn from it.
The composition may well be owned. Candidate owners, recalled from memory and explicitly
**UNVERIFIED**:

- **"Visual review becomes a pixel metric"** is productised in visual-regression tooling — Percy,
  Chromatic, BackstopJS. If the ratchet is already their operating loop, Observation 2 is a
  re-description of a shipped product category.
- **`bug -> regression test`** is standard engineering practice; characterization tests (Feathers,
  *Working Effectively with Legacy Code*) are the named form. If the ratchet reduces to this, it is
  decades old and free.
- **Agent-accreted tool libraries** have candidates in Voyager (Wang et al., 2023) and *Large
  Language Models as Tool Makers* (Cai et al., 2023). If either already indexes tools by the
  question they decide, Observation 3 is owned.

Status of this document's contribution: **unclaimed composition, not new math**. Never "novel".
Ownership kills a novelty *claim*, never a *use* — if an owner is found, cite it and build on it.

**The first obligation on the receiving end is to run that precedent search**, before any of this is
cited, planned against, or built on.

**Subset rule.** There is no formal artifact, no proof, and no measurement across a corpus. n = 1
worked instance. Nothing here may be read as validated.

## Identity

- Source session reference: working session of 2026-08-06/07 in `domainspec-lean-formalization`
  (produce a print-quality PDF by transplanting a reference document's visual system onto different
  text). No transcript is readable from this repository.
- Destination label: `review-decidability-and-tool-library`
- Handoff type: `research-direction`
- Target project or lifecycle: `cyberalchemy-orchestrator` — dispatch routing and cost, not
  documentation
- Created for: recording an observation about when a verification step should dispatch an agent at
  all, and a proposal for persisting the checks that replace agents

## The Observation in One Statement

> Across one document-production run, the review layer split cleanly into checks that were decidable
> by program and checks that required perception; the perceptual reviewer, having found a defect,
> named a metric for it, and that metric is a script from then on — so the correct number of agents
> for a verification step is not a constant, it decreases as findings accumulate.

**Collapse test (a), bound to that statement:** if the fraction of review findings a reviewer can
honestly convert into a metric turns out to be small, the ratchet turns too slowly to matter and the
whole claim reduces to "write a regression test when you find a bug" — owned, free, decades old,
contribution zero.

**Collapse test (b), bound to the library proposal:** if agents cannot reliably find an existing tool
and write duplicates anyway, the library is a cost rather than an asset. It is measurable as
duplicate rate — the fraction of newly written tools whose deciding question already had an entry.

## The Run

One writer agent, two adversarial reviewer agents (text fidelity, design fidelity), approximately
720k subagent tokens for a single document.

## Observation 1 — a reviewer that should not have been an agent

The text-fidelity reviewer burned 87k tokens and returned 0 defects. It returned 0 because every
check it ran is decidable by program:

- order-sensitive token diff: 3549 == 3549, zero non-equal opcodes;
- non-ASCII codepoint census;
- glyph-level bullet count: 141/141;
- font-span emphasis check: 7/7 italics, 9/9 bolds.

No judgment anywhere. That belongs in a fail-closed script inside the render step, at near-zero cost.
The agent was not wrong; it was the wrong instrument.

## Observation 2 — the ratchet

The design reviewer found, by eye, a defect no script could have found: the crop marks "read as a
drawn frame rather than a registration ghost." Pure perception — no pre-existing predicate would have
fired.

But it reported the finding numerically: reference 0.42pt stroke at RGB(220,209,196), Δ21 from
ground; produced 0.75pt at RGB(213,202,185), Δ28; net ink ≈ 2.4×.

Once that metric was named, the defect never needs an agent again. It is
`assert stroke_pt <= 0.5 and delta_from_ground <= 24`, permanently.

The loop:

> **agent judges → agent names the metric → metric becomes a tool → next run catches it by script,
> no agent invoked.**

The agent layer shrinks monotonically as defects accumulate.

### Decidability criterion

To keep this from degrading into vibes: **is there a computable predicate over the artifacts whose
truth does not depend on taste?** Operationally — can the check be written as "extract X from A,
extract X from B, compare under relation R"? If yes, script it. If the comparison is against a norm
that exists only in someone's eye, it is an agent.

### Goodhart guard — mandatory, not optional

The reviewer must have **explicit permission to answer "this is taste, I have no metric."** Demand a
metric for every finding and reviewers will fabricate bad ones, and the system will then optimise for
the fabrications. The guard is load-bearing: without it the ratchet manufactures its own false
positives and the decidability criterion becomes decorative.

## Observation 3 — the library, whose hard part is the index

Tools written on the fly must persist, or the next agent rewrites them. But tag-based indexing rots
into dozens of near-duplicates nobody finds — which is collapse test (b) arriving.

Proposal: **index by the question the tool decides, not by what the tool is**, because agents search
semantically. Each entry carries:

| Field | Content | Why it is required |
| --- | --- | --- |
| Assertion | the question the tool decides, one sentence | it is the search key; agents retrieve by question, not by filename |
| Originating defect | the defect that caused it, with date | a tool with no originating defect is speculative |
| Self-test | one case it catches, one case it lets pass | unaudited on-the-fly code becoming load-bearing is a real risk |
| Provenance | which agent, when, human-reviewed or not | the library's own trust level must be readable |

## Relevance to this repository

This is a routing and cost question, not a documentation question. It bears on three things this
repository already owns:

1. whether a verification step should dispatch an agent at all;
2. where a persistent tool index would be owned and consulted;
3. the fact that the correct number of agents for a step is not fixed — it decreases over time as
   findings are converted into checks.

**Implications drawn by the author of this handoff, not handed over as observed** (flagged so they
are not mistaken for session findings):

- If the number of agents for a step is time-varying, then any dispatch plan that fixes a seat count
  by role is fixing the wrong quantity. This was not tested in the session and is inference only.
- A tool index of the shape in Observation 3 has no owner here yet, and choosing one is a decision
  this handoff does not make.

No routing rule, integration point, or orchestrator design decision beyond the above was discussed in
the source session, and none should be read into this document.

## Context Builder Selection

Context Builder was **not run**. The source session is in another repository and its transcript is
not readable from here; the content above was relayed, not selected from evidence.

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| O-001 Preserve the token/defect figures exactly. | covered | relayed session report | The figures are the only quantitative content; paraphrase destroys them. |
| O-002 Preserve the Goodhart guard as mandatory. | covered | relayed session report | Without it the ratchet is actively harmful, not merely weak. |
| O-003 State non-novelty in the document's own voice. | covered | authoring constraint | A precedent-free claim of newness is the failure mode this repository already refuses. |
| O-004 Verify precedent. | **not covered** | — | No search was run. This is the first obligation on the receiving end. |
| O-005 Ground the claim in a formal artifact. | **not coverable** | — | None exists. n = 1. |

Strict coverage: `flag` — O-004 open, O-005 permanently open at this stage.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| The document being produced, its subject matter, and the reference document's identity | not obligation-relevant; the observation is about the review topology, not the artifact |
| Full per-agent token accounting beyond the 87k and ~720k figures | not needed for the routing question |
| Any generalization to review layers outside document production | unsupported at n = 1 |

## Target Boundary

- **In scope for the next thread:** run the precedent search; decide whether the ratchet survives
  collapse test (a) by sampling real review findings and counting how many convert to an honest
  metric; decide whether a tool index has an owner in this repository.
- **Out of scope:** implementing a tool registry, changing dispatch seat policy, or citing any part of
  this as validated. No permission is granted here for schema, ontology, or routing changes.
- **Prior decisions to preserve:** none — this handoff creates no decision and reverses none.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| Precedent search not run | receiving thread | `open` | Search visual-regression tooling, characterization testing, Voyager, Cai et al. before any use. |
| Convertible-fraction unmeasured (collapse test a) | receiving thread | `open` | Sample past review findings; count how many yield a metric the reviewer would sign. |
| Duplicate rate unmeasured (collapse test b) | receiving thread | `open` | Define duplicate rate over deciding-questions before building an index. |
| Tool index has no owner | unassigned | `open` | Decide ownership before authoring entries; do not create the index incidentally. |
| n = 1, no formal artifact | — | `open` | Nothing here may be promoted on current evidence. |

## Next-Session Start Prompt

```text
Continue from sessions/session-handoffs/2026-08-07-0125-review-decidability-and-agent-tool-library-handoff.md.

That handoff records one observation from a document-production session in
domainspec-lean-formalization: a text-fidelity reviewer spent 87k tokens returning 0 defects
because every check it ran was decidable by program, while a design reviewer found a
perception-only defect and then named a metric for it that turns the defect into a permanent
script. Claimed consequence: the number of agents needed for a verification step decreases
over time.

The observation is explicitly NOT novel and NO precedent search was run. Run that search
first: visual-regression tooling (Percy, Chromatic, BackstopJS), characterization tests
(Feathers), Voyager (Wang et al., 2023), Large Language Models as Tool Makers (Cai et al.,
2023). If an owner is found, cite it and treat the remainder as a use, not a discovery.

Then attack collapse test (a): what fraction of real review findings can a reviewer honestly
convert into a metric? If the fraction is small, the whole thing reduces to "write a
regression test when you find a bug" and contributes nothing.

Do not implement a tool registry. Do not change dispatch policy. n = 1; there is no proof.
```

## Provenance

- Source refs: relayed report of a 2026-08-06/07 session in `domainspec-lean-formalization`; no
  transcript, no artifact, and no repository evidence in this repository supports it.
- Context Builder mode: not run.
- Precedent search: **NOT RUN**.
- Evidence date: 2026-08-07
- Output path: `sessions/session-handoffs/2026-08-07-0125-review-decidability-and-agent-tool-library-handoff.md`
- Convention: the `invoke.session-handoff` template family
  (`.claude/skills/invoke/templates/session-handoff/session-handoff.md`). Free-form content sections
  follow the sibling precedent in `domainspec-core`.

## Gate Result

- Status: `flag`
- Reason: the handoff is readable and its content is preserved, but Context Builder did not run, the
  precedent search did not run, and there is no formal artifact behind any claim. It is a
  research-direction handoff and carries no execution authority.
