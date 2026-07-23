---
tags: [information-theory, document-information-estimator, entropy, claim-graph, internal-tools]
node_type: discovery
is_session: true
layer: domain
nature: explanatory
status: active
created: 2026-07-22
timestamp: 2026-07-22T19:35:00-03:00
expires: 2026-09-20
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 5
importance_rationale: "Useful three-way split of 'amount of information' grounding a new internal tool, but pre-PoC: the research dispatch is still gated and two inline dispatches sit as unregistered debt."
---

# Document Information Estimator — pre-PoC brief

## Summary

The session explored whether we can mechanically estimate the amount of information in a document,
and concluded "amount of information" is not one quantity but at least three (intrinsic/compression,
semantic/propositional, relative/novelty), recommending the relative-surprisal reading as the working
definition. A 3-attacker review (mechanics / reference-integrity / conceptual-over-claim lenses) of
the initial pitch surfaced verified defects — chiefly mislabeling cross-entropy as "the bit count,"
claiming surprisal composes "for free," and importing the sibling Lean repo's count-capped /
beats-count theorems as if they proved a document's information is a graph (they are typed candidates,
not proof). The corrected design keeps **both** a scalar (magnitude) and a claim graph (structure with
contradiction edges) rather than replacing one with the other. Two independent revisers of the brief
then caught two repo-grounded blockers: the dispatch ledger is a process log (not a claims corpus),
so it cannot serve as the prior `K`; and Anthropic's API returns no token logprobs, so the estimator
must use local llama.cpp/vLLM or OpenAI. The brief was first written as `internal-tools/assay.md`, then
relocated to an explicitly-named folder `internal-tools/document-information-estimator/README.md`, with
"Assay" demoted to one name candidate among several. A research dispatch (subagents-strategy) is
proposed but **not** launched — it sits at the confirm gate pending owner assignment and the
CT-thread in/out decision. Two multi-subagent dispatches (the review and the revise) ran inline and
ungated and were deliberately **not** registered in the ledger, flagged as debt. No domain code
changed; this is a pre-PoC design/brief session.

## Open questions

- Is a relative-surprisal **scalar** actually adequate to rank documents by "how much you'd learn," or
  does the claim graph beat it on a real eval? (the falsifiable question the PoC exists to answer)
- Does a real functorial-entropy bridge (Baez–Fritz–Leinster / Vigneaux / Ellerman) connect the repo's
  Lean to a document-information metric, or is the category-theory grounding a dead end for this tool?

## Next steps

1. Assign an owner and decide the CT-thread in/out, then run `check-tension`, register, and launch the
   proposed research dispatch (`research/assay-poc/`).
2. Decide whether to register the two ungated inline dispatches (review, revise) as persisted
   artifacts, resolving the inline-vs-`working_folder` schema conflict.
3. Pick the final product name from the §0 candidates in the brief.

## Recommendation

Attack Open question 1 first by the cheapest path — the relative-surprisal **scalar** with a ranking
eval — before investing in the claim graph, and keep the category-theory bridge (Open question 2) out
until the scalar has earned it. This ranks Next-steps item 1 (launch the research dispatch) ahead of
items 2–3, licensed by the falsifiable question Open question 1 already names.

## Files touched

- internal-tools/document-information-estimator/README.md
- internal-tools/assay.md

## Extra section

- **Provenance flag (user-requested).** The directories under
  `docs/features/agents-communication-infra/discovery/` — `document-merge-debate/`,
  `document-unification-debate/`, `bus-contracts/`, `spec-integration-assessment/` — were **not**
  created by this session. They appeared ~18:07 and were still being modified ~19:30 by a separate /
  parallel process. This session touched **only** `internal-tools/`.
- **Home convention.** `internal-tools/` holds internal product briefs, each in an
  **explicitly-named folder** (says what the tool does) with a short codename kept as a candidate,
  not as the folder name.
