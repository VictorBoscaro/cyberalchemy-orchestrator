---
tags: [readme, work-context, warrant, objective-composition, dispatch-ledger, system-view-essays]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-29T03:00:10-03:00
updated_at: 2026-07-29T03:00:10-03:00
expires: 2026-09-27
decisions_made: true
contradictions_found: true
specs_updated: [README.md, docs/essays/what-this-is-for/essay.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Changed what the repository states it is for at its entry point, and recorded in the open that the root Plan does not yet carry that objective."
---

# README reframed around the composed objective

## Summary

The session opened as a request to update the root README and became a search for the project's
actual objective, because the README described the dispatch substrate as if it were the whole
purpose. A first candidate — the repository as a knowledge machine — was rejected by the owner, who
named instead the linking of the smallest unit of work to the larger context that gives it purpose;
that objective was found written in three proposal-only essays and absent from every governing
artifact. To test whether it was the principal objective, three subagents ran the same prompt with
no shared context and were asked only to rank the project's top five objectives. All three ranked
the built dispatch substrate first and `OBL-E3` last, all three volunteered the same counter-argument
that the repository declares decision hygiene as its telos, and none of the three found the
macro-to-micro work-context objective at all. The diagnosis was that the objective exists as
argument and not as authority: the root Plan's §1 states the business problem as correlated bias,
noise and framing only, and the work-context essay self-describes as a proposal-only companion. The
owner then framed the goal as a composition rather than a single objective, and the session proposed
that the programs are one relation at different strata — warrant made explicit, typed and composable
— anchored in `AX-2`'s four kinds of warrant. A governed dispatch wrote that framing as an essay and
attacked it with two opposed reviewers: the author refuted the tidy four-faces-to-four-programs
mapping, and both reviewers independently found that the essay's self-declared strongest evidence
was false and that it resolved by omission a question the README marks unresolved. The essay also
cited a `private: true` do-not-publish artifact whose exclusion list names essays — a breach
introduced by the parent's own brief, repaired in the same session by re-deriving the point from
`AX-3`. The README was then rewritten to open with the composed objective, to carry a six-row table
attaching each objective by a different typed edge with its honest standing, to qualify how much of
the warrant condition is actually machine-refused, and to record explicitly that `PLAN.md` §1 does
not yet carry that objective, so the two artifacts now disagree in the open rather than in silence.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [plans/governed-agent-work-infrastructure/PLAN.md](../plans/governed-agent-work-infrastructure/PLAN.md) | `contradicts` | The README now states a composed objective that this Plan's §1 does not carry; §1 states the business problem as correlated bias, noise and framing only. The disagreement is recorded in the README's navigation table rather than resolved. |
| [vault/axioms/axioms.md](../vault/axioms/axioms.md) | `derives-from` | The composed objective is built on `AX-2`'s type-appropriate warrant and its four warrant faces, including the `proof ∘ falsification` composition rule for applied formalisms. |
| [plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md](../plans/governed-agent-work-infrastructure/essays/work-context-system-view/essay.md) | `contextualizes` | Supplies background on this essay's visibility: three independent readers ranking the project's objectives did not surface its objective at all, which locates the gap in the governing artifacts rather than in the essay's argument. |

## Open questions

- Whether the composed objective should be promoted into `PLAN.md` §1, or whether the root Plan
  should stay scoped to governed agent work and the composed objective acquire a separate owner.
  The README currently states the disagreement without settling it.
- Whether the framing's collapse test can bind at all. It routes to `OQ-3` and `OQ-5`, which are
  parked with no owner or date, and whose source has already leaned toward the answer the framing
  needs — the pattern the repository elsewhere calls a deferral rather than tenure.
- Whether the private-artifact citation was a one-off or a systemic defect in how subagent briefs
  name the vault. The brief said to read `vault/` without excluding do-not-publish targets, and no
  gate caught it before the reviewer did.

## Next steps

1. Apply the five material repairs the reviewers named to `docs/essays/what-this-is-for/essay.md`:
   amend the §2 table in place instead of correcting it from §2b; restrict the independence claim
   to `AX-4` and `BET-VERACITY-PROP`; give "where warrant lives" concrete fields; bind `P4` to the
   golden case; replace "already scheduled" with the parked status.
2. Decide whether the proposed work-context operating rules go into `CLAUDE.md`; they were drafted
   in-session and never applied.
3. Reconcile the timestamp fields. The README still carries `last_updated`, which
   `.claude/skills/custom/frontmatter.md` says to replace with `updated_at` on substantive update,
   and the new essay carries both.

## Recommendation

`PLAN.md` §1 is the keystone. The README change makes the composed objective visible, but the
ranking exercise showed that independent readers anchor on the root Plan and inherit its statement
of the problem — so a fourth reader would repeat the same omission. Attack it by rewriting §1's
business problem as loss of context between levels, with the judgment-quality failure modes
retained as one defence among several rather than as the problem itself. This is a direction, not a
verdict: whether the root Plan is the right owner is the first open question above, and settling
that precedes the edit.

## Files touched

- README.md
- docs/essays/what-this-is-for/essay.md
- telemetry/agents/subagents-dispatch.yaml
