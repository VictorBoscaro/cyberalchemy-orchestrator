---
tags: [experiment, criterion, pre-registration, primitives, provenance]
node_type: experiment-criterion
is_session: false
status: proposal
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
authority: proposal-only
freeze_state: not-frozen
initial_definitions: experiments/tracking-spine-primitives/experiment-initial-definitions.md
---

# Criterion — Tracking Spine Primitives

**Freeze state: NOT FROZEN.** This is the designer's proposal. It becomes pre-registered only when
the owner accepts it at the human gate, before any probe exists. Until then every line here is
editable; after freeze, an edit is a new criterion, never an in-place mutation.

## Hypothesis

> Every link relationship instantiated among the pre-registered sample of this repository's
> artifacts can be expressed using at most six of the eleven pre-registered candidate constituents.

One claim. The falsifying observation is namable: a sampled link that either cannot be expressed at
all, or whose expression requires a seventh constituent.

## Non-goals

This probe explicitly does not test:

- whether a working context is a classification or a composition — it counts only whether `context`
  is necessary at all;
- whether links should hold between files or between identity-bearing objects — the expression
  records which, but the choice is not adjudicated here;
- any invariant. No invariant is proposed, ratified, or falsified by this probe.
- whether the six overlapping inventories of unresolved items in `plans/` describe overlapping
  objects;
- any storage design, schema, identifier scheme, or migration;
- whether a tracking spine, once built, improves anything a person does.

## Pre-registered candidate constituents

Fixed before the probe sees any artifact. Each carries the one-sentence definition the probe must
use; post-hoc redefinition invalidates the run.

| # | Name | Definition used by this probe |
|---|---|---|
| C1 | `object` | A thing with an identity that survives changes to its name, description, classification, and location. |
| C2 | `context` | A bounded working scope that artifacts are situated in or participate in. |
| C3 | `edge` | A typed, directed relationship asserted between two endpoints. |
| C4 | `emission` | An addressed or barrier-released act of one agent sending a payload. |
| C5 | `event` | The durable record that something occurred, ordered in time. |
| C6 | `group` | A set of emissions sharing a completion rule and a common judgment scale. |
| C7 | `graph` | A set of nodes and edges considered as one confirmable whole. |
| C8 | `digest` | A content-derived value fixing exactly what was confirmed or transported. |
| C9 | `prompt` | A versioned, typed instruction issued to an agent. |
| C10 | `format` | A versioned shape a response must satisfy, including a judgment scale. |
| C11 | `principal` | An identifiable actor or mechanism to which an act is attributed. |

## Pre-registered sample

Selection is deterministic: within each stratum, take the first instances in lexicographic path
order that satisfy the stratum predicate. Seventeen links total.

| Stratum | n | Predicate |
|---|---|---|
| S1 intra-context | 5 | Both endpoints under the same top-level directory. |
| S2 cross-context | 5 | Endpoints under different top-level directories (`plans/`, `vault/`, `docs/`, `telemetry/`, `experiments/`, `research/`). |
| S3 survived a move | 3 | The link's target was moved or renamed at some point recoverable from version history. |
| S4 non-file endpoint | 2 | At least one endpoint is not a file — a ledger row, a dispatch record, or an agent activation. |
| S5 assertion to activity | 2 | One endpoint is a claim or assertion; the other is the dispatch, research, or session that produced it. |

S4 and S5 are the strata that can falsify. They are included deliberately, and their presence is
what distinguishes this sample from one selected to pass.

**S5 fallback, pre-registered.** The root Plan records that the assertion-to-activity spine does not
exist, so S5 may yield zero instantiated links. If it does, the probe constructs the two cases from
artifact pairs that the objective requires to be linked but which carry no link today, and expresses
those. Zero instances is not an invalid sample; it is the condition the experiment exists to examine.

## Mechanical verdict rule

For each sampled link, the probe records: the expression, the subset of C1–C11 it uses, and for
every omitted constituent a stated reason for the omission. A constituent is **NECESSARY** when at
least one sampled link cannot be expressed without it.

- **INVALID** if any stratum cannot be populated to its stated `n` (S5 excepted by its fallback), or
  if any link's expression omits a constituent without a stated reason, or if any constituent is
  used under a definition other than the one tabled above.
- Otherwise **SURVIVED** if every sampled link is expressible **and** the count of NECESSARY
  constituents is ≤ 6.
- Otherwise **FALSIFIED**.

The rule resolves only into `SURVIVED`, `FALSIFIED`, or `INVALID`. It does not map onto an
execution-status tier.

## Discrimination check

Both outcomes are informative, and they redirect the work differently.

**SURVIVED** teaches that the spine's vocabulary is small. It also names which five or more
constituents are views rather than primitives — which is the reduction the work needs, and which
makes the next step possible: a transition set over ≤ 6 objects, and after that invariants stated in
the form the repository's own definition requires (a predicate preserved by every valid transition).

**FALSIFIED** teaches more, and in one of two distinguishable ways. If it fails by inexpressibility,
the probe has located a link the current vocabulary cannot carry — the single most valuable fact
available here, because a missing primitive is exactly what an eleven-name list assembled by
inspection would fail to notice. If it fails by count, the vocabulary is genuinely large, and the
premise that a small spine is achievable is wrong — which redirects the architecture rather than
refining it.

A result of "some links were awkward" is not available: the rule forces one of three verdicts.

## Known confound and its mitigation

The probe's author chooses each expression, and a motivated author can collapse constituents to hit
the threshold. This is the criterion's principal internal-validity risk.

Mitigation, pre-registered: the probe must record a stated reason for every omitted constituent on
every link, and adjudication checks the reasons rather than the count. An omission whose reason does
not hold against the tabled definition makes that constituent NECESSARY regardless of what the probe
concluded. A criterion that counted only the subset sizes would be gameable; this one is not,
provided the adjudicator is not the author.

## Reproducibility

Reproducibility here means deterministic **re-adjudication**, not re-execution. A second adjudicator,
given this frozen criterion and the probe's recorded expression table, must reach the same NECESSARY
count and the same verdict. The three things that make that possible are pre-registered above: the
eleven definitions, the deterministic sample selection rule, and the requirement that every omission
carries a stated reason.

## Open Questions

- Is six the right threshold, or is any fixed threshold arbitrary enough that the identity of the
  necessary constituents matters more than their count?
- Does S3 test anything the other strata do not, given that placement is already declared a
  projection rather than an identity?
- Should a twelfth candidate be pre-registered for the missing-primitive case, or does leaving the
  list at eleven bias the probe toward SURVIVED?
- Would a countermodel — constructing one link the vocabulary demonstrably cannot express — settle
  this more cheaply than a seventeen-link sample? The repository's precedent for attacking candidate
  invariants is countermodel, not measurement.
