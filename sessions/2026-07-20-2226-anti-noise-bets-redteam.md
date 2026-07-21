---
tags: [anti-noise, orchestrator, hypothesis, registered-bets, red-team, kahneman, category-theory]
node_type: premise
is_session: true
layer: architecture
nature: explanatory, reference
status: active
created: 2026-07-20
timestamp: 2026-07-20T22:26:27-03:00
expires: 2026-09-18
conversation_id: unknown
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Seeds the anti-noise design axis (complementing the mature anti-bias machinery) via two full red-team lifecycles with real gate/ledger discipline, but stays candidate/exploratory with a critical finding (BET-CT unfalsifiable) explicitly parked, not fixed."
---

# Anti-noise thesis: registered bets and two red-teams

## Summary

The session set out to define the orchestrator's design principles, grounded in Kahneman's
noise-reduction and extending the repo's existing anti-bias machinery. It established a
three-axis frame — Kahneman (error model: bias⊕noise) ⊕ Thaler/Nudge (choice architecture:
process-not-content) ⊕ Category Theory (operationalization) — plus the core reframe bias⊥noise
and a two-level Estimate-Talk-Estimate pipeline (freeze the independent judgment before any
channel opens). It authored the hypothesis node HYP-ORCH-NOISE
(`vault/hypothesis/orquestracao-anti-ruido.md`) as an exploratory, non-legislating referential.
A first red-team (3 tensioned attackers: Feyerabend/Gigerenzer/Taleb) returned a FIX verdict —
sharpest being that √N rests on an independence LLM agents cannot supply (triple convergence)
and that the fork-guard needs an oracle the premise denies; two decisions were escalated to the
owner. Per the owner's direction, unproven claims were reframed as explicitly registered bets
(schema assume→falsifier→experiment): a "Registered bets" section (BET-CT/√N/PERSONA/TAG/THALER/
FORK) was added and the stale CT table row rewritten from "scenery" to CT-operationalization
(~1:1 analogy), reflecting the owner's clarification and the promoted `costura-feasibility`
information-geometry results. A scoped delta red-team (Fritz on CT-substance, Popper on
falsifiability) then found a CRITICAL — BET-CT as written is unfalsifiable (a universal claim
plus a "we don't surrender to CT" retreat clause immunize it, and it counts the collapsed nudge
optic as a survival) — plus four fidelity gaps in the promoted costura math. On the owner's
decision none was fixed; all delta findings were parked as OQ-9..12, with OQ-10 flagged "owner's
call" because it challenges promoted research. Both red-teams ran the full lifecycle —
check-tension gate (both PASS each time) → owner confirm → append-only ledger (dispatch + close
rows) — and a recon of the knowledge-taxonomy repo fed OQ-4's tagging design.

## Contradictions

- questions `vault/hypothesis/orquestracao-anti-ruido.md` — the delta red-team (Fritz on
  CT-substance, Popper on falsifiability) found `BET-CT` unfalsifiable as written (universal claim
  + "we don't surrender to CT" retreat clause immunizes it; the collapsed nudge optic is
  over-counted as a survival) plus four fidelity gaps in the promoted `costura-feasibility` math
  (F=MAP asserted not constructed, nudge well-definedness justified by an irrelevant property,
  Banerjee regime-pinning, CLT-vs-Sanov framed as exclusive when they coexist). Per the owner's
  decision none was fixed — all parked in the same node as OQ-9..12, OQ-10 flagged "owner's call".

## Next steps

- Reconcile the survived-mapping count in `vault/hypothesis/orquestracao-anti-ruido.md` between the
  CT table row (lists 4) and BET-CT's Status (lists 3, dropping aggregation↦m-projection), and record
  the nudge as "candidate 1 falsified, re-typed" rather than a survival — both are unambiguous edits,
  independent of how OQ-9's scoping question is resolved.
- Route OQ-10's four costura fidelity gaps back to the `costura-feasibility` research to defend or
  correct (owner's call) — do not edit the promoted findings from the hypothesis node.
- Tighten OQ-11 (BET-THALER — fixed N + pre-registered blind decisions) and OQ-12 (BET-TAG — an
  anchor-quality control independent of rater count), whose methods are already specified.

## Recommendation

Of the parked items, attack OQ-9 (BET-CT's falsifiability) before OQ-10 — a hunch, not a licensed
call: the finding is parked and unresolved, so this is a priority judgment. The reasoning: OQ-9 is
the one CRITICAL, and how BET-CT is re-scoped governs what "survived via costura" is even allowed to
claim — which is exactly the ground OQ-10's costura gaps stand on. Deciding OQ-9's scoping question
first therefore constrains OQ-10 rather than the reverse.

## Files touched

- vault/hypothesis/orquestracao-anti-ruido.md
- telemetry/agents/subagents-dispatch.yaml (2 dispatch + 2 close rows)
