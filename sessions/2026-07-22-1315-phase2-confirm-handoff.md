---
tags: [orchestration, dispatch, ledger, ui, anti-bias, architecture]
node_type: audit
is_session: true
layer: domain, application
nature: explanatory, technical
status: active
created: 2026-07-22
timestamp: 2026-07-22T13:15:00-03:00
expires: 2026-09-20
decisions_made: true
contradictions_found: true
specs_updated: [docs/features/agents-communication-infra/phase-2-confirm-handoff.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Re-scopes a mis-framed blocking finding and ships a fully-tested Phase-2 confirm slice that respects EG-1, though nothing is committed and only one endpoint landed."
---

# Repo investigation → enum-drift re-scoping → Phase 2 confirm handoff (linear UI)

## Summary

The session set out to investigate the repo from several opposed points of view and
decide what to do next. Using the repo's own subagents-strategy machinery, I proposed a
methodology-tensioned triad — Falsifier (claim≤proof), Builder (value from a running
loop), Theorist (the formal ground is the product) — passed the check-tension gate (both
verifiers PASS), and ran dispatch `2026-07-21-repo-standing-investigation`: three blind
investigators plus a synthesizer. The synthesis converged on two cheap, decidable moves
(trace the enum-drift; verify the sibling Lean build) and left a genuine three-way residue
on ordering: build-first vs ground-first vs prove-first. Probing the enum-drift, we
established it is mis-scoped — EG-1 as written is a code-path invariant, EG-6 already
handles the two historical rows, and the honest reading is "one validated writer per
authority," which Phase 2's own bus will need — so the drift blocks a veracity label, not
any operation. On that basis the owner chose to build. I shipped Phase 2's confirm handoff
for the `linear` UI in three layers: `POST /api/confirm` (writes a marker in the pending
dir, never the ledger, EG-1 untouched), a `_confirmed` reader flag, and the wired Dispatch
button, plus a protocol doc for the orchestrator handoff and marker lifecycle. All checks
pass: `test_main` (+12 new confirm checks, including "confirm never touched the ledger"),
`test_ledger`, the linear Playwright suite (24/24), and an end-to-end confirm-then-cleanup
against a live server. A stale server on port 8765 (predating `/api/overview`) was killed
and replaced with a fresh one running current code. Nothing was committed; the changes sit
in the working tree awaiting the owner's go.

## Contradictions

- questions `vault/audit/ledger-enum-drift-finding.md` — Phase 2's confirm slice shipped
  *without* tracing the 2026-07-18 drift, on the finding that it blocks only EG-1's
  veracity label (not any operation), which questions the finding's "keystone next step
  for Phase 2" framing.
- validates `vault/constitution/engine-constitution.md` (EG-1) — the `/api/confirm`
  marker-write (pending dir only, ledger untouched, pinned by the "confirm never touched
  the ledger" test) is the first concrete code instance of EG-1's logical-publisher ≠
  physical-writer scoping, not a claim against it.
- validates `vault/hypothesis/orchestration-infra.md` — the pending-dir confirm marker is
  the first concrete instance of its pre-confirm draft / `pending/` compatibility design
  row.

## Open questions

- Which ordering governs the backlog after this slice — build-first, ground-first
  (provenance spine / BL-3), or prove-first (Lean verify / OBL-E3)? The owner chose build
  for Phase 2; the strategic ordering across the whole backlog is unsettled, and
  ground-first would reprioritize the remaining UI/infra surface.

## Next steps

1. Commit the Phase-2 `linear` slice (green, awaiting the owner's go).
2. In a live orchestrator session with a real pending sheet, arm the Monitor watch and run
   the confirm → check-tension → register-dispatch → agents → close chain end-to-end (the
   first true full-loop exercise; only the endpoint is exercised so far).
3. Wire the confirm button in the other nine UI variants (same `pendingCard` change).

## Recommendation

Commit the slice first — it has landed green and pins EG-1, so it is safe to bank — then
settle the ordering question before expanding. Hold off on wiring the other nine UIs
(step 3) until the ordering is chosen: ground-first would reprioritize that surface, so
doing it now risks throwaway work.

## Files touched

- implementations/server/main.py
- implementations/server/ledger.py
- implementations/tests/test_main.py
- implementations/tests/test_ui.py
- implementations/static/ui/linear/index.html
- docs/features/agents-communication-infra/phase-2-confirm-handoff.md
- research/repo-standing-investigation/findings.md
- research/repo-standing-investigation/investigator-falsifier.md
- research/repo-standing-investigation/investigator-builder.md
- research/repo-standing-investigation/investigator-theorist.md
- telemetry/agents/subagents-dispatch.yaml

## Extra section

Owner directives worth carrying forward: (1) Phase 2 was explicitly scoped to the `linear`
UI **only** — the other nine variants were deliberately left disabled, not forgotten;
(2) at the decision point the owner cut off further option-surveying ("foda-se, o que
devemos fazer?") and asked for a committed recommendation — favor deciding and acting over
enumerating alternatives.
