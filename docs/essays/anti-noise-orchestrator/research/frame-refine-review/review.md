---
canonical_kind: review
title: "Review — frame/refine/citation additions to HYP-ORCH-NOISE"
description: "Tensioned review (n=2, internal-fit vs external-soundness axis) of the 2026-07-20 edits to the anti-noise hypothesis: frame, refine, citation spine, OQ-6/7. One factual HIGH finding (question belongs to discovery, not research) and one structural HIGH finding (frame needs a noise arm). All fixes applied."
evidence_for: [HYP-ORCH-NOISE]
created: 2026-07-20
last_updated: 2026-07-20
tags: [review, frame, refine, citation, anti-noise, claim-proof]
---

# Review — frame/refine/citation additions to HYP-ORCH-NOISE

Dispatch `2026-07-20-anti-ruido-frame-refine-review` (review, n=2, `output_mode` persisted).
Tension axis: **internal-fit (consistency + claim≤proof)** vs **external-soundness (true or
decorative ideas)**. The two reviewers disagreed at the predicted load point — whether the
frame belongs only to the tension axis — which validated the tension design.

## Findings (severity · verdict · fix)

| # | Sev | Finding | Verdict | Fix applied |
|---|---|---|---|---|
| 1 | **HIGH** | `question` was cited as a field that "the `research` kind already requires"; in fact it belongs to the `discovery` kind and is **optional**. Worse: it anchored on the `discovery` model that OQ-6 rejects. | confirmed (both) | Rewritten as an honest anchor annotation; the false requirement removed; reconciled with `[[OQ-6]]`. |
| 2 | **HIGH** | Placing the frame only on the tension axis contradicts the thesis's own `bias ⊕ noise` orthogonality; independent frames disperse (noise), they don't oppose — the tension machinery (`check-tension`) doesn't even apply. The doc already has the right treatment in OQ-4 and didn't apply it to the frame. | confirmed (skeptic); consistency said "doesn't break the rule" — reconcilable | Frame now has **two arms**: tension (bias) + independent-dispersion (noise, à la OQ-4, PENDING). Collapse-test gained the dispersion failure mode. |
| 3 | MEDIUM | `refine` described as "universal operator with zig-zag convergence"; the actual skill is a fixed pipeline of ~10 stages + budget, and `loop_cap`/`max_loops` belong to the dispatch, not to a solo artifact. Zig-zag criterion fabricated. | confirmed (both) | Downgraded: refine ends via fixed pipeline + budget; solo-convergence marked **PENDING**. |
| 4 | MEDIUM | Raw fail-closed citation fabricates availability/Goodhart bias (discards unanchorable truth; pastes a key just to pass; GREEN coverage measures conformity). Missing `supports` vs `mentioned`; collides with adjustment 3. | confirmed (skeptic) | "Invariant" → "candidate discipline"; two safeguards: link-quality (`supports`/`mentioned`) + `reasoning` valve for truth-by-reasoning. |
| 5 | LOW | OQ-6 under-framed as a taxonomy; the root-input (problem-recognition) is unowned = live risk. | confirmed (skeptic) | OQ-6 gained a "live risk: unaudited root-input" paragraph. |
| 6 | LOW | Anchor "codomain C"/"common thread" pointed to PLAN/MAPPING (not literally there); they live in README/FRAMINGS. | confirmed (consistency) | Anchor corrected to README/FRAMINGS. |

## Passed (no fix)

- Frame on the tension axis does **not** break the generate→tension / evaluate→independence
  separation (fix #2 *adds* the noise arm, it doesn't remove the tension one).
- Citation spine does **not** conflict with the ETE's 5 adjustments (it reinforces adjustment 4).
- Hygiene: no OQ collisions, valid mermaid, coherent frontmatter/tags, `derives-from` is a real anchor.

## Method note

Dispatch logged and closed in the ledger (`telemetry/agents/subagents-dispatch.yaml`) — the
repo's anti-bias discipline applied to its own work (self-application A6). `exit_reason:
resolved` — no irreconcilable dissent; the reviewers' disagreement was **reconcilable**
(frame gains both arms).
