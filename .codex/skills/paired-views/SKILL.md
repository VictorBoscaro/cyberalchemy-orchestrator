---
name: paired-views
description: "Composed Arcanum spell: paired-views. Authors a target's ontology-view, system-view, and engineer-view as one triad and validates the single-owner invariant across all three — no term defined twice, every stance named once and decided once."
surface_kind: native-runtime-package
canonical_source: null
mutation_policy: author-in-place
tier: arcana
domain: view-authoring
version: 0.1.0-seed
origin: composition of ontology-view + system-view + engineer-view; enforces the cross-view discipline no single sigil can own
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Agent
---

# Paired Views

## Identity

- Canonical ID: `paired-views`
- Aliases: none
- Scope: library

Paired Views composes `ontology-view`, `system-view`, and `engineer-view` into one triad for a single target, then runs a triad-validation pass that enforces the discipline none of the three sigils can own alone: **each load-bearing claim has exactly one authored home, and nothing is defined or decided twice.**

The altitude ladder: `ontology-view` (vocabulary & concept graph — the floor) → `system-view` (shape & stakes — names stances) → `engineer-view` (mechanics & verdicts — decides stances).

## Trigger Conditions

- A target (product idea, architecture, subsystem, or design) needs explanation at more than one altitude for more than one audience.
- The same terms and decisions are getting re-explained across documents and drifting.
- A stakeholder must judge soundness (shape) while an engineer must see verdicts and contracts — without the two narratives contradicting.
- An existing system-view / engineer-view pair needs a vocabulary floor and a drift check.

## Required Sigils

| Sigil           | Role In Spell                                                        | Required Mode / Input                          |
| --------------- | ------------------------------------------------------------------- | ---------------------------------------------- |
| `ontology-view` | Author the vocabulary & concept-graph floor; own term definitions.  | consumes `ontology-vault` if present           |
| `system-view`   | Author the shape; name every load-bearing stance, decide none.      | bound to the ontology-view output              |
| `engineer-view` | Author verdicts, contracts, mechanics; one verdict per named stance.| bound to ontology-view + system-view outputs   |

## Execution Phases

| Phase | Sigil / Step      | Input                                       | Output                          | Gate                                                                 | Failure Policy                                  |
| ----- | ----------------- | ------------------------------------------- | ------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------- |
| 1     | `ontology-view`   | target (+ optional ontology-vault)          | ontology-view.md + term handles | every term in exactly one home; conflicts surfaced                  | block if load-bearing terms are undefined       |
| 2     | `system-view`     | target + ontology-view handles              | system-view.md + stance handles | no verdict stated; no term redefined; every stance points downstream | flag stances with no downstream owner           |
| 3     | `engineer-view`   | target + ontology-view + system-view handles| engineer-view.md + decision rows| every stance → exactly one row; every verdict cites authority        | block on orphaned stance or missing authority   |
| 4     | triad validation  | all three view artifacts                    | single-owner report             | the four invariants below all pass                                   | report violations; do not certify on any breach |
| 5     | spell report      | phase outputs                               | paired-views report             | blockers named; open/critical stances surfaced                      | report partial when a view remains blocked      |

## Triad Invariants (Phase 4)

The validation pass certifies all four, by reconciling the emitted handles across the three artifacts:

1. **One home per term.** Every `term:<slug>` is defined in `ontology-view` and in no other view. A definition restated in system-view or engineer-view is a violation.
2. **Name once, decide once.** Every `stance:<slug>` named in `system-view` resolves to exactly one `decision:#<id>` in `engineer-view` — never zero, never two.
3. **No verdict upstream.** `system-view` and `ontology-view` state no verdicts; verdicts live only in `engineer-view`.
4. **Authority on every verdict.** Every `engineer-view` decision row cites a source authority (or an explicit "no running gate" for OPEN/CRITICAL).

Any breach blocks certification and is listed in the report with the offending handle and both locations.

## Observability

Record: target boundary, terms defined, conflicts open, stances named, stances resolved vs orphaned, duplicate-definition violations, duplicate-verdict violations, verdict-upstream leaks, decision rows by status (RESOLVED/OPEN/CRITICAL), authority-coverage gaps, and which phase blocked if any.

## Output Contract

Return a report with: the three artifact paths; the triad-invariant verdict (pass | violations listed per invariant); the decision inventory's OPEN and CRITICAL rows a stakeholder must weigh; open naming conflicts from ontology-view; and the recommended next step (promote inline ontology into an `ontology-vault`, resolve an OPEN stance via `decision-gate`, or render a visual layer via `x-ray`).
</content>
