---
tags: [document-information-estimator, prolixity, compression, gzip, marginal-information, claim-graph, dispatch]
node_type: discovery
is_session: true
layer: domain
nature: explanatory
status: active
created: 2026-07-23
timestamp: 2026-07-23T02:26:00-03:00
expires: 2026-09-21
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Converts the pre-PoC brief into a scoped, falsifiable v0 build plan with a load-bearing genre-confound finding, but nothing is built and the LM layer stays gated behind a bake-off."
---

# Assay — prolixity-first as the first use case, and the forward probe

## Summary

The session began by reviewing the sole artifact under `internal-tools/` — a pre-PoC brief for a
"document information estimator" (working name Assay) — with two independent subagent reviewers plus the
coordinator, who then cross-examined each other. All three converged on the same load-bearing defects (a
length-extensive scalar with an undefined ranking key; a prior corpus `K` that cannot fit the context
window; a pinned model whose pretraining swamps `K`) and agreed the six-group research dispatch the brief
proposed should not run — build a thin M1 instead. The owner then reframed the tool's first use case:
measure the prolixity/redundancy of his own operating instructions (`CLAUDE.md` + ~66 skills), building
narrow but designing for expansion. The coordinator judged this a strong fit — arguably better than the
brief's own novelty framing — because prolixity is an information-density ratio (so the length-extensivity
defect inverts into signal), the corpus is bounded/in-repo (`K` fits, pretraining-swamp is milder), and a
behavioral falsifier is available. Phase 1 dispatched three subagents, one per README framing (general
engine / prolixity-first / novelty-vs-ledger); they converged and the coordinator rewrote the README around
the primitive `marginal_information(unit|corpus)` with use cases as bindings, foregrounding prolixity as the
v0 binding, deferring novelty-vs-ledger to a store-gated v1, and relocating the brief from `internal-tools/`
to `internal-tools/research/`. Phase 2 dispatched an advocate⊥skeptic pair plus a research-scout,
synthesized into `initial-considerations.md`. The committed verdict: prolixity is the right target but the
README's full build (LM surprisal + behavioral A/B) is the wrong first move — ship a gzip-only,
confound-guarded audit first, let a bake-off earn the LM layer, use mask-and-regenerate (not agent-replay)
as the v0 falsifier, and evaluate wrapping LLMLingua before building a logprob estimator. The sharpest
finding: on instruction text surprisal anti-correlates with cut-safety (a repeated critical rule ranks as
top-prolix), forcing a mandatory protect-repeated-units guard. Both dispatches were registered and closed
in the ledger, and a memory pointer was written.

## Open questions

- Does `L(unit|rest)` beat conditioned gzip on instruction text, or is gzip-only the honest MVP? Unresolved
  until the S4 bake-off runs.
- Does conditioning move `L` on our private content (is `Δ = L(u|∅) − L(u|rest) > 0`), or does pretraining
  swamp `K` fatally even for idiosyncratic instructions?
- Is behavioral-equivalence (not benchmark-score) evaluation of compressed prompts an open contribution
  gap, or already solved externally?

## Next steps

- Ship S0: the stdlib gzip-only, confound-guarded (protect-repeated-units) redundancy audit over the skills
  corpus, emitting a ranked redundancy map.
- Spike LLMLingua / LongLLMLingua to settle adopt-vs-build for the LM column before standing up any logprob
  server (S2).
- Verify `telemetry/agents/subagents-dispatch.yaml` rows are replayable as a behavioral-falsifier task set.

## Recommendation

Ship S0 first. It is stdlib-cheap, produces a usable redundancy map immediately, and is the licensing gate
that decides — via the S4 bake-off — whether the LM layer is worth building at all; every heavier rung
(logprob server, LLMLingua wrap, falsifier) should wait behind it. Licensing fact: the build ladder in
`initial-considerations.md` §3.

## Files touched

- internal-tools/research/document-information-estimator/README.md
- internal-tools/research/document-information-estimator/initial-considerations.md
- telemetry/agents/subagents-dispatch.yaml

## To register (owner-specified)

Add a `dispatch_type: probe` to the subagents-strategy skill — a robuster-than-usual probe that both maps
what to research *and* renders a committed assessment (as this session's `initial-considerations.md` did).
Noted as a forward follow-on; it touches the appender's type enum, so it relates to the agent-role/enum
work already in flight. Not built here.
