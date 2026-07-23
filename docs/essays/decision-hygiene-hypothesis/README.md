---
tags: [orchestration, decision-hygiene, kahneman, thaler, noise, bias, framing, anti-bias, nudge, judgment]
node_type: essay
is_session: false
session_ref: null
layer: domain, epistemology
nature: explanatory
status: draft
veracity: low
conviction: medium
version: 0.1.0
last_updated: 2026-07-23
---

# The Decision-Hygiene Hypothesis — Orchestrating Agents as a Judgment Problem, Not a Plumbing One

> **Draft.** Read every "cancels bias" / "reduces noise" below as a claim we are testing, not a
> result.

## The problem, for anyone who runs agents

You have a task too big or too delicate for one model call, so you fan it out. Three agents
research the question in parallel; a fourth stitches their returns into a synthesis; maybe a fifth
scores which answer is best. It feels like more coverage — five looks instead of one — and the
output reads clean. Then you ship it, and it is wrong in a way none of the five caught, or it is
subtly different from what the same pipeline produced yesterday on the same input, or the whole
thing was quietly doomed the moment you phrased the opening prompt the way you did.

The uncomfortable observation underneath all three of those failures is the same: **what comes back
from a fan-out is only ever as good as the judgment behind it.** Fanning out multiplies throughput.
It does not, by itself, multiply *judgment*. And judgment — human or model — does not fail
randomly. It fails in a small number of specific, nameable ways that decision science has spent
decades cataloguing. The bet of this essay is that those same failure modes show up when you
orchestrate LLM agents, that they are the real ceiling on quality, and that the useful way to think
about an orchestrator is therefore not as a message bus that moves work between agents but as a
**decision-hygiene machine** whose job is to counter those failures on purpose.

That reframe matters because it changes what "orchestrate well" means. Treated as plumbing, a better
orchestrator is a faster, more reliable, more observable pipe. Treated as a judgment problem, a
better orchestrator is one that produces *less error* — and error, it turns out, comes in kinds that
call for opposite tools. Kahneman's *Noise* gives us the error model: total judgment error splits
into **bias** (systematic, directional, correlated) and **noise** (unwanted scatter). Thaler's
*Nudge* gives us the process moves: arrange the choice architecture so the hygienic path is the
default one, and the friction falls on the mistakes rather than on getting it right. Neither of
those is about how bytes travel between agents. (A separate essay explores whether these moves can
be given a categorical *typing*; that is a different question and not developed here.)

## The three failures this lens targets

Three failure modes, each with a countermeasure decision science already names. This section stays
at the level of intuition and example; the machinery comes after.

### Correlated bias — N agents that are really one look repeated

The seductive thing about a fan-out is that it *looks* like independent replication. Ask five agents
and average, and surely the shared errors wash out? They do not — if the errors are shared. Five
agents built on the same base model carry the same training distribution, the same blind spots, the
same rhetorical reflexes. Ask them all "is this argument sound?" and they will tend to agree not
because it *is* sound but because they were shaped to find the same things persuasive. When errors
are correlated, adding more agents buys you almost nothing: **N of them is closer to one look
repeated N times than to N independent looks.** The confidence you read off their agreement is
counterfeit — it measures how alike they are, not how right they are.

The countermeasure is not more agents. It is **structural opposition**: if two agents are pointed at
deliberately conflicting angles — one arguing from the formal literature, one from practitioner
experience; one attacking on precedent, one on vacuity — then a bias internal to the first is likely
to be *surfaced* by the second rather than *seconded* by it. The test is sharp and worth stating in
its cleanest form: for a pair of agents, ask *what error inside agent A would fail to survive a
confrontation with agent B's output?* If the honest answer is "none — they would just produce two
compatible findings," the pair is diverse but not tensioned, and its agreement is worthless as
evidence. Diversity of surface presentation (different wording, different personas) is necessary but
nowhere near sufficient; only opposed *direction* breaks the correlation.

### Noise — scatter you cannot see unless you measure it

Bias is a bias *of the aggregate* — the whole panel leans the same wrong way. Noise is the opposite
kind of error: **dispersion of individual judgments around their own average**, for reasons that
have nothing to do with the task. Reorder the three findings before you ask an agent to rank them
and the ranking changes. Reword the rubric and the scores shift. Re-sample at the same temperature
and you get a different verdict. None of that variation tracks the actual quality of the work; it is
just scatter injected by phrasing, ordering, and sampling.

The insidious part is that noise is **invisible unless it is measured.** A single run gives you one
number and no way to know how much that number would have jumped had you nudged the setup. You only
ever see noise by taking the same judgment more than once and looking at the spread — and most
pipelines take it exactly once. The classic countermeasure is the one you would reach for
instinctively: collect *independent* judgments and **aggregate** them, because the scatter of the
average shrinks as you add independent votes (the standard-error-of-the-mean fact). The catch, which
we return to at the dense end, is the word *independent* — the same correlation that poisons bias
also caps how much aggregation can shrink noise.

### Framing — the prompt that steers everything downstream

Before any agent runs, someone poses the question. That framing — the choice of lens, the way the
problem is cut, what is treated as given — is itself a judgment, and it is the one with the longest
reach, because everything downstream inherits it. An ill-posed frame does not produce a visibly
broken pipeline; it produces a fluent, well-executed answer to the *wrong question*. If you frame
"which of these two designs is better?" you will get a comparison; you will not get the answer that
both are wrong. The frame poisons the source filter, the investigation, the synthesis, and the
scoring, all silently, because none of those stages is allowed to see outside it.

Framing is a judgment, so it inherits both of the failures above. It has a slant of its own that an
opposed framing can expose; and it also *scatters*, in a way worth seeing concretely: hand the same
one-line ticket to two capable engineers and ask each to write the problem statement, and you get two
legitimately different statements — not one right and one wrong, just genuinely apart. That gap is a
signal. A small gap means the problem was well-posed and everyone saw the same thing; a wide gap is a
hint that the ticket itself is ill-posed, that there is no single question there to answer yet. This
is the least-built of the three targets, and we flag it as such below; but conceptually it belongs
here, because a frame chosen badly caps the pipeline before it starts.

## The hypothesis and its moves

Put the three together and a consequence follows — one we bet on but have not demonstrated: **what
helps is not *more* agents but *structurally different* ones.** More looks from the same viewpoint
compound correlated bias and do nothing for noise you never measured. The moves that would actually
help are moves against the specific failures:

- **Pair on opposed angles** so bias is surfaced rather than seconded.
- **Keep the agents blind to each other** until each has committed a position, so no one anchors the
  next.
- **Aggregate judgments rather than fuse them** — combine independent scores into a reproducible
  distribution instead of dissolving them into a single prose "consensus" that quietly launders away
  the disagreement.
- **Add process nudges** that make the hygienic sequence the default: *freeze before you discuss*
  (seal your position before the channel to peers opens), *fork-guard* (before averaging, check
  whether the spread is noise to be averaged or a real disagreement to be escalated), and
  *default-to-the-hygienic-path* (a gate that blocks, not a guideline that asks).

One of these — the anti-bias gate — has real, enforced machinery in this repo today; the aggregation
move has only a recording substrate; the rest do not exist yet. Being exact about which is which is
the whole discipline.

**The anti-bias gate is built and runs.** The move against correlated bias is not a slogan here — it
is an executable gate, enforced at init time. When a dispatch fans a task out to any group of two or
more agents, the sheet must declare an `anti_bias` axis for the group (drawn from a closed
vocabulary — methodology, source-corpus, attack-vector, temporal-prior) and an explicit `angle` for
each agent's position on it (`.claude/skills/register-dispatch/SKILL.md`, schema v0.6.1). Before that
sheet reaches the human for confirmation, the `check-tension` gate fires: **two independent agents**
read the proposed sheet and run four tests — the axis is a real canonical axis, no two angles are
clones, the agents do not all share one methodology or one attack (this spread test is where the
investigate-vs-evaluate distinction lives, not in the firing condition), and every pair carries a
written sentence predicting *how* one agent's bias would be exposed by another. Only a "both PASS"
reaches the human; any reproval, or any disagreement between the two checkers, bounces the sheet back
to be redesigned (`.claude/skills/check-tension/SKILL.md`). The design principle behind it
(`anti-bias-vector-composition`) is explicit that this is composition, not coverage: the
micro-vectors must be *opposed* so bias cancels, not merely non-overlapping so concerns don't repeat.
This runs as an enforced init-time gate today — the anti-bias, generate-stage half of the hypothesis
made to run. (Two honesties about *how* it runs: the gate is agent-and-prompt logic with no test file
of its own, and its four semantic tests are the checkers' judgment, not something the strict appender
mechanically enforces — the appender's strict runtime validation covers the schema, not the tension.)

**Aggregation has a foothold; the anti-noise half is mostly on paper.** The substrate records what
it needs to (typed group connections `sequential | zig-zag | feedback`, a per-group `robot_talks`
flag for whether agents discuss after their parallel runs, per-agent `token_budget`), and the ledger
is append-only behind a strict validating appender. But the moves that would counter *noise* —
independent producer-blind scorers on a common scale, aggregate-the-estimate-not-the-individuals, the
freeze-before-the-channel rule as an enforced barrier rather than a convention, the fork detector
that separates dispersion from real dissent — are **argued, not built.** The escalation *channel* for
a genuine fork exists (a close-row can carry `exit_reason: dissent_irreconcilable`); the *detector*
that decides when to use it does not. The freeze primitive (recording an initial and a final
position) exists; the rule that you *cannot* open the discussion before freezing does not. This is
the honest state: one axis enforced, the other named and designed but awaiting construction
(`docs/PLAN.md` §3.1).

## Full density: the error model, the ceiling, and the open question

Why those specific moves, and where their ceiling sits, comes down to the error model underneath
them. The error model the repo runs on is written as a single line: **`residue = bias ⊕ noise`.** Total
judgment error decomposes into a directional part (bias, the error of the aggregate) and a
dispersion part (noise, the scatter of individuals about that aggregate), and — this is the point of
splitting them — the two call for *opposite* tools. Bias wants tension, opposition, red-team:
correlated error is broken by pointing agents against each other. Noise wants independence and
aggregation: uncorrelated scatter is shrunk by averaging independent votes. A design that reaches for
one tool against the other failure gets no purchase.

The `⊕` deserves one caveat, kept honest rather than buried: bias and noise separate *cleanly* —
add with no cross-term — only under a particular assumption about the loss geometry (a convex,
divergence-generating potential; the "anchored common scale"). Without it, the honest form keeps an
interaction term, `residue = bias + noise + interaction`, and the clean orthogonality is a
conditional refinement, not a free lunch (`HYP-ORCH-NOISE`, the `seam-feasibility` conditional). We
state the split because it organizes the design; we do not claim the clean version unconditionally.

There is a deeper subtlety worth stating, because it dissolves an apparent contradiction. Tension
(for bias) and independence (for noise) look like opposite disciplines — one deliberately correlates
agents against each other, the other deliberately de-correlates them. They are not opposites. Both
are settings of a single **decorrelation knob**: the variance of an aggregate is governed by the
mean pairwise *error*-correlation among its members, and tension is simply *negative* error-
correlation engineered on purpose, which does strictly better than the zero-correlation of mere
independence. So the design does not resolve a real mathematical tension (there was none); it places
two points on one axis — engineer negative correlation (opposed probes) at the generate stage where
you can, fall back to zero correlation (independent, producer-blind scorers) at the judge stage where
you cannot. This is the load-bearing idea, and it too is a claim to test on data, not a result.

**The ceiling, stated up front and without softening.** Every agent in a fan-out that shares a base
model shares a slice of that model's errors. Those errors are correlated, and correlation is exactly
the thing that caps how much independence — and therefore how much aggregation — can buy. Negative
correlation (tension) can be engineered where you control the angles; but the *residual* correlation
baked in by the shared base model cannot simply be prompted away, and **we do not yet know how large
it is.** That number is the ceiling on the whole anti-noise program. If effective-N collapses toward
1 — if five scorers on one base model behave like one scorer sampled five times — then aggregation
buys a rounding error and the noise half of the hypothesis fails on its own terms. We have not
measured it. Until we do, the honest posture is that the anti-noise lever *should* work and is
*designed* to work, not that it *does*.

**The sharp open question.** Grant that these three failures occur — that correlated bias, invisible
noise, and framing lock-in are real in multi-agent LLM work. The lens still faces one question that
decides whether it is science or vocabulary: **do the countermeasures actually *cancel* the
failures, or only *relabel* them?** It is entirely possible to build a tension gate that produces the
*appearance* of opposition — two agents with different-sounding angles whose errors are still
correlated underneath — so that the sheet passes `check-tension`, the human sees a clean double-
check, and the correlated bias sails through wearing the costume of diversity. It is equally possible
to average a panel of producer-blind scorers, watch the reported variance drop, and mistake shared-
bias-masquerading-as-reliability for genuine noise reduction. The failure mode of a decision-hygiene
frame is precisely that its moves are *checkable for form* (did we declare opposed angles? did the
variance drop?) while the thing that matters is *substance* (did the errors actually decorrelate? did
the residue actually shrink?). Distinguishing those requires an **external target** — downstream
decision quality, a labeled reference, a held-out outcome — because dispersion and agreement are
internal quantities that cannot, alone, tell "well-tensioned" from "theater." Building that external
check is the work the hypothesis has not yet done.

So the claim, held to its proof: the decision-hygiene lens is worth adopting because each failure it
names carries a known countermeasure, which turns "orchestrate agents well" from a vibe into moves
that can be *stated and falsified*. One of those moves — the anti-bias tension gate — is built and
runs today. The rest — independence, blind aggregation, the freeze barrier, the fork detector,
framing's noise arm — are argued and unbuilt. And whether any of them *cancels* rather than
*relabels* its failure is the open question the whole program is pointed at.

## Connections

*Provenance and discipline.* This is essay cohort-1 / draft-1, local (no push). It operates under
`claim ≤ proof`: every statement holds only as far as the linked artifact supports it, which is why
the built anti-bias gate and the still-thesis anti-noise moves are marked apart throughout. The one
thing the essay asks the reader to take on is the *lens* — that coordinating LLM agents is a
decision-making problem — and a lens earns its keep by naming failures precisely enough to be
falsified, not by being true a priori.

- **Derives from:** `vault/hypothesis/anti-noise-orchestration.md` (`HYP-ORCH-NOISE`) — the
  red-teamed thesis with registered bets and collapse-tests this essay renders in accessible form,
  keeping only the decision-hygiene (Kahneman ⊕ Thaler) lens.
- **Grounds in:** `docs/PLAN.md` (§1 the business problem, §2 the hypothesis, §3.1 the
  decision-making front); `.claude/skills/check-tension/SKILL.md` and
  `.claude/skills/anti-bias-vector-composition/SKILL.md` (the built anti-bias gate and its design
  principle); `.claude/skills/register-dispatch/SKILL.md` (dispatch angles, `anti_bias`,
  `robot_talks`, the append-only ledger).
- **Sibling essay (not developed here):** the categorical typing of these moves lives in a separate
  essay and in `FRAMINGS.md`; this one deliberately stays on the decision lens.
- **Would inform:** a future anti-noise constitution that promotes the still-thesis moves
  (independence-by-stage, blind aggregation, freeze-before-the-channel, fork-guard) into enforceable
  rules once each has earned its proof.
- **External references:** Kahneman, Sibony & Sunstein, *Noise* (2021) — the bias ⊕ noise error
  model; Thaler & Sunstein, *Nudge* (2008) — process choice architecture.
