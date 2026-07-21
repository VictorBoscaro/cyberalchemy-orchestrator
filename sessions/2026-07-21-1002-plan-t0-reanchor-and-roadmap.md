---
tags: [orchestration, dispatch, architecture, category-theory, anti-bias, ledger]
node_type: implementation-plan
is_session: true
layer: architecture, domain
nature: procedural, explanatory
status: active
created: 2026-07-21
timestamp: 2026-07-21T10:02:35-03:00
expires: 2026-09-19
decisions_made: true
contradictions_found: true
specs_updated: [PLAN.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Re-anchors the repo's single root planning document and, via a dogfooded draft→review→approve dispatch, surfaces a factual mis-anchor already propagated into two vault nodes plus a false dependency and an under-gated premise."
---

# PLAN re-anchor (T0 loop) + approved ordered build roadmap

## Summary

The session set out to understand the repo near-from-scratch across four axes (hypotheses,
scientific process, infrastructure, category theory) and to update the root PLAN.md. A three-agent
coverage read established the repo as a T0-loop epistemology engine with three faces (decision /
categorical / engineering) bound only by a still-absent provenance spine (BL-3), whose absence
simultaneously explains the missing `enrich` step, the falsified framework-self-similarity, and the
meta-ontology's non-convergence. PLAN.md was re-anchored (v0.3) from its old E0–E4 step list to this
engine/faces/spine structure. A correction landed: the `TO-ME/` OBL-E3 brief is not a "ghost" — it
exists in the sibling repo `domainspec-lean-formalization`; only the in-repo citations lack the
sibling-path prefix. On the user's direction that ROADMAP ≠ BACKLOG, a dogfooded dispatch
(`2026-07-21-roadmap-build-order`) produced an ordered build roadmap via two opposed drafters →
synthesizer → two opposed reviewers (both FAIL) → one revision → final approver Lakatos (REJECT v2 →
ACCEPT v3). The review loop caught real defects: `exit_reason` is gated by `validateClose` (not
`validateDispatch` — a mis-anchor propagated into the engine constitution and the enum-drift finding);
"zero out-of-enum rows" is unreachable on an append-only ledger; the `Monitor`-wakes-Claude bridge does
not exist; `D-1→B-1` was a false dependency; and P-1 under-gated fractality. The approved roadmap
(critical path `FT-1→B-1→B-3→B-4`, D-1 parallel, Track B `TR-2→FT-2→P-1` parallel) was written into
PLAN.md §7 with a ROADMAP≠BACKLOG scope note and graduation rule. Both roadmap dispatches were
registered and closed in the ledger; no domain code changed — the work was documentation, planning,
and orchestration.

## Contradictions

- contradicts [[engine-constitution]] — EG-1 anchors the `exit_reason` write-gate to `validateDispatch` (`:120`, `:132`), but `exit_reason` is gated by `validateClose` (`append-dispatch.cjs:242`); the rule mis-describes its own mechanism and the sole-writer guard must cover both row kinds. Correction folded into roadmap step B-1.
- contradicts [[ledger-enum-drift-finding]] — inherits the same `validateDispatch`/`validateClose` mis-anchor (`:54`) and frames "zero out-of-enum rows" as achievable, which is unreachable on an append-only ledger (the two 2026-07-18 rows can only be quarantined now, then superseded under BL-3).

## Next steps

1. Execute **FT-1** — inspect `append-dispatch.cjs` git history + the append-only hook's state at 2026-07-18 to establish the enum-drift cause among its three exhaustive outcomes.
2. In parallel, **TR-1** (verify the `TO-ME/` brief on disk, re-point in-repo citations to the sibling path, reconcile OBLIGATIONS.md's "absent" wording) and **TR-2** (verify the sibling Lean build-gate: `lake build` + `#print axioms` @ `6edb664`).

## Recommendation

**FT-1 is the keystone.** The entire B-1 scope — and whether EG-1 needs re-adjudication at all — is
conditional on its three-outcome result, and the ACCEPTED roadmap makes FT-1 the critical-path root.
Licensing fact: the roadmap survived two opposed reviewers plus a final approver with veto. Attack it
by reading the appender's git history and hook state at 2026-07-18 before touching any repair.

## Files touched

- PLAN.md
- telemetry/agents/subagents-dispatch.yaml
