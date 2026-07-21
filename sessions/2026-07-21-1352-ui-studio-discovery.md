---
tags: [ui, agents, anti-bias, dispatch]
node_type: discovery
is_session: true
layer: application
nature: explanatory, technical
status: active
created: 2026-07-21
timestamp: 2026-07-21T13:52:29-03:00
expires: 2026-09-19
decisions_made: true
contradictions_found: true
specs_updated: [docs/features/ui-studio/discovery.md, docs/features/ui-studio/README.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Produces the spec-ready foundation for the ui-studio harness and, along the way, corrects a previously-unverified CONST-FE cross-reference (FE-1/FE-5 are hybrid) that an earlier paired audit had missed."
---

# UI Studio discovery — first-cut fitness harness, paired-reviewed

## Summary

The session set out to start developing the ui-studio feature, examining the ZefraHub
"newspaper" prior art and the user's idea — a "Matrix" variant grid, per-element UI feedback,
and agents that generate new UIs from that feedback — to judge whether it made sense. The
assessment was that the idea is sound and already largely designed in the feature README,
which prescribes "substrate before engine": build the measurement harness and close the loop
once before any autonomous generator. With the user we decided no further research was needed
(the README evidence is first-hand paired-audit-verified) and scoped a discovery to the
measurement substrate only — The Matrix + per-element vote + aggregation, human runs the
Decision Gate, autonomous generation deferred. I authored `docs/features/ui-studio/discovery.md`
via the discovery-writing skill (mandatory structure + mermaid flow diagram). I then ran a
paired anti-bias review dispatch (falsifier ⊥ completeness), registered it in the ledger, and
both auditors converged on two weak zones: the FE-rule→gate-type mapping and the `#vote`/`#tt`
capture section. The falsifier returned FAIL and the completeness reviewer GAPS; the user chose
to apply all corrections, so I baked every fix into the discovery — a closed category enum
`{FE-1,2,4,5,6,7,9}`, required non-empty comment, dedup-to-latest aggregation, jsonc API shapes,
coverage via a per-variant testid manifest, overall = mean of per-category means, an FE-9-style
vote-mode toggle, and an FE-5 states section. A factual bug was then corrected in both the
discovery and README §6.1: FE-1 and FE-5 are `hybrid`, not `review`/`deterministic`, and the
earlier paired verification never checked this internal CONST-FE cross-reference. I closed the
review dispatch with a ledger close row and opened the linear UI in the browser; the discovery
is now spec-ready.

## Contradictions

- validates `vault/constitution/frontend-constitution.md` — confirmed first-hand that FE-1 and
  FE-5 carry `Validation: hybrid` (`:123`, `:169`) and corrected the `review`/`deterministic`
  mischaracterization that had propagated into `discovery.md` and `README.md` §6.1; the
  feature's earlier paired audit (`verification.md`) never covered this internal cross-reference.

## Open questions

- Does the interim `overall` formula (equal-weight mean of the per-category means) survive the
  first real scoring cycle, or does it need OQ-1's weighting — i.e. do some CONST-FE categories
  discriminate variants enough that equal-weighting hides the signal?

## Next steps

1. Write the executable spec `vault/spec/ui-fitness-harness.md` from the discovery (skill
   `domainspec-spec-feature` / agent `domainspec-spec-writer`): `POST /api/vote` + validated
   `votes.ndjson` appender + `GET /api/fitness` aggregation + the `#vote` widget.

## Recommendation

Write the spec next — it is the keystone, and it is licensed now that the discovery has been
corrected and hardened through the paired review (both auditors' findings landed). The widget
and the appender named in Next steps both wait on that one artifact.

## Files touched

- docs/features/ui-studio/discovery.md
- docs/features/ui-studio/README.md
- telemetry/agents/subagents-dispatch.yaml
