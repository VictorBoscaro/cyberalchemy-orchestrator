---
tags: [experiment, primitives, provenance, tracking, linking, architecture]
node_type: experiment-initial-definitions
is_session: false
status: active
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
authority: informational
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Tracking Spine Primitives — initial definitions

Informational context only. This document does not choose a hypothesis, a criterion, a method, or
a dispatch topology.

## Context

This repository is building infrastructure for governed agent work: a system where a request is
decomposed, fanned out to several agents, executed under confirmation, and recorded. Across that
whole surface the repository's stated purpose is not the fan-out itself but what the fan-out leaves
behind — a durable record of everything that was done, and the ability to connect an artifact to
other artifacts, both inside the same working context and across different ones.

The local problem is that this connecting capability has no vocabulary. The repository's root Plan
records that a provenance spine — assertion, the dispatch or research that generated it, and its
trail — does not exist today, and that identifiers currently live in four disjoint spaces. It
further records the suspicion that this single gap sits behind several other unfinished things:
the missing enrichment step in the learning loop, the unenforced freeze in the execution substrate,
and untyped self-reference. Meanwhile the surrounding artifacts describe the pieces of a system —
objects, contexts, relations, emissions, events, groups, graphs, digests, prompts, formats,
principals — without anyone having established which of those are irreducible and which are views
over the others.

This matters to someone governing the system because the size of that irreducible set determines
what can be built and what can be checked. A governed invariant is a predicate preserved across
transitions of a state; if the state's constituents are not settled, no invariant over them can be
stated sharply enough to be falsified, and every rule written about the system remains an opinion.
It matters to someone using the system for a plainer reason: if the connecting vocabulary is
larger than it needs to be, every artifact captured costs more to record and every link is one more
thing that can be wrong.

## Purpose

This document establishes the informational context for a future experiment about the vocabulary of
the tracking and linking spine. It records what is already decided, what is already known, and what
is not yet understood, so that a later criterion can be designed against a stable baseline rather
than against a moving one.

It will inform the design of that criterion, and downstream of it the candidate invariant set for
this architecture — which is a separate object from the repository's existing candidate kernel
invariants and must be reconciled with them rather than duplicating them.

## Experiment Question (can be refined)

Which of the currently named constituents of the tracking spine are irreducible, and which are
views over the others?

Two subsidiary framings are part of the same question and may be separated or absorbed as the
question is refined: whether a working context is a classification an artifact belongs to or a
composition an artifact participates in; and whether links hold between files or between
identity-bearing objects that files merely locate.

## Confirmed Product Constraints

Established by owner direction in session 2026-07-27:

- The shared objective of the composed services is tracking everything that was done and linking
  artifacts within one context and across different contexts.
- The transport fabric between two agents transports and never authors: it may address, deliver,
  seal, validate shape, and record, and it may not rewrite, summarise, reinterpret, or choose a
  recipient.
- Execution is a service separate from compilation; it owns prompt resolution.
- Prompts are versioned and classified by type.

Established by existing repository artifacts:

- A Plan supplies no execution authority by existing or being accepted
  ([`plans/README.md`](../../plans/README.md)).
- Physical placement is one projection of an object's properties, not its identity
  ([agent-language essay §4, §16.4](../../plans/governed-agent-work-infrastructure/essays/agent-language-system-view/essay.md)).
- Candidate kernel invariants K1–K7 exist with `authority: research-input-only` and are explicitly
  offered for removal, splitting, derivation, or falsification before any first set is ratified
  ([`CANDIDATE-INVARIANTS.md`](../../plans/governed-agent-work-infrastructure/plans/agent-work-language-research/CANDIDATE-INVARIANTS.md)).
- An invariant is defined here as a predicate preserved by every valid transition, which requires a
  state space and a transition set to be stated first (same source).

## Current Evidence Baseline

**The gap is already named by the repository.** The root Plan's §5 records the absent provenance
spine, the four disjoint identifier spaces, and the suspicion that this one gap is behind three
other unfinished things. Nothing in this experiment discovered that; it is inherited.

**A candidate constituent list already exists, dispersed.** Eleven names appear across the current
artifacts: object, context, edge, emission, event, group, graph, digest, prompt, format, principal.
They were never assembled into one list, and no test has been applied to any of them.

**One reduction has already been demonstrated, incidentally.** During the adversarial review of
[the system-and-engineer view essay](../../plans/governed-agent-work-infrastructure/essays/agents-infrastructure-system-and-engineer-view/essay.md),
the reviewer established that a group must carry no membership list, because its members are
derivable as exactly those emissions carrying a recipient with a barrier-release condition. That
argument was made to close a drift surface, not to test irreducibility, but it is an instance of
the reduction this experiment is about, and it arrived without an experiment.

**A failure of file-linking is already recorded in this repository.** The essays index documents
that the work-context essay's companion reference stopped resolving when the agent-language essay
moved directories, and that it was repaired on 2026-07-26. The repository also completed a
`subplans/` to `plans/` migration whose effects on existing references are visible in version
history.

**Two overlapping inventories of unresolved items already exist and are not reconciled.** The
agent-language essay carries thirteen named stances and fifteen open questions; the work-context
essay carries six open decisions; the system-and-engineer view carries nine decision rows; its
review carries twenty-one surviving or new findings. At least one duplication across these has been
identified — a decision row in the new essay substantially answers a stance named in the companion
essay under a different handle.

**No measurement has been taken.** No count of links, no inventory of link kinds, no sample of
artifacts, and no attempt to express any existing relationship under any candidate vocabulary.

## Known Gaps

- Which of the eleven named constituents are irreducible is unknown; no test has been applied to any
  of them, and the one reduction that exists was a side effect of a different argument.
- Whether a working context is a classification or a composition is unresolved, and the two existing
  essays lean in different directions without either deciding.
- Whether links hold between files or between identity-bearing objects is unresolved in practice,
  even though the artifacts state that placement is a projection.
- Whether cross-context links are the same kind of thing as intra-context links, or a distinct kind,
  is not addressed anywhere.
- The relationship between this architecture's future invariants and the existing candidate kernel
  invariants K1–K7 is undefined: whether they derive, extend, or conflict.
- The transition set over these constituents does not exist in any artifact, which is why no
  invariant over them can currently be stated in the form the repository's own definition requires.
- Whether the four disjoint identifier spaces named in the root Plan correspond to four of the
  eleven constituents, or cut across them, has not been examined.
- Whether the six overlapping inventories of unresolved items describe overlapping objects is
  unknown; only one duplication has been identified, and it was found by inspection rather than by
  a systematic pass.

## Open Questions

- Is the size of the irreducible set the decision-relevant quantity, or is the identity of its
  members what matters, independent of count?
- Can irreducibility be established over artifacts alone, or does it require a transition set that
  does not yet exist?
- Does an inherited gap need an experiment at all, or would a construction and its counterexamples
  settle it more cheaply? The repository's own precedent is mixed: the candidate kernel invariants
  were attacked by countermodel rather than by measurement.
