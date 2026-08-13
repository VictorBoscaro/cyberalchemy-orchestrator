---
tags: [agent-work, system-overview, editorial-composition, reader-progression, review]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-12T18:23:45-03:00
updated_at: 2026-08-12T18:23:45-03:00
expires: 2026-10-11
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session established the intended compositional progression for the product overview but demonstrated that the applied rewrite still violated its central editorial constraint."
---

# Work overview composition and editorial failure

## Summary

The repository needs an external overview that presents the product as infrastructure for expanding one person's capacity to work through AI agents while preserving comprehension and control. The session decided that an intelligent first-time reader should encounter concepts locally, when their practical need appears, and only afterward see the larger explanatory compositions those concepts form. A Robot-Talks investigation supported a progression from user objective and concrete experience to local concepts, then to bounded work, verifiable execution, and knowledge continuity as explicitly synthesized groupings rather than natural architectural divisions. The user approved those dispositions, and the overview was rewritten around them. Two independent reviews found material problems in the first rewrite, including an abstract example, late introduction of knowledge concepts, ambiguous containment, missing load-bearing relations, and a promotion to knowledge that appeared automatic. Those findings were checked and follow-up edits were applied. Despite that process, the resulting text still violated the user's explicit rule against chaining loosely related actions into catalogue-like sentences, exemplified by the opening sequence “explicar o objetivo, dividir o problema, distribuir contexto, acompanhar dependências, perceber quando uma premissa mudou, resolver decisões e depois reconstruir”. The failure shows that reviewing structural progression did not adequately enforce sentence-level relational composition, even though the governing writing skill stated that requirement directly. The rewritten overview therefore remains unaccepted, and no claim should be made that the requested editorial objective was achieved.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed Agent Work Infrastructure](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The overview being revised is the external explanation of this project-level infrastructure proposal. |
| [Work and Knowledge System Overview](../plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md) | `contextualizes` | This session records the rationale for its rewrite, the reviews applied, and why the resulting draft remains unaccepted. |
| [Work Overview Editorial Drift](2026-08-12-1757-work-overview-editorial-drift.md) | `derives-from` | This session continued the reader framing and progression established there. |

## Open questions

- What sentence-level test will reliably distinguish an explained composition from a catalogue of adjacent actions before another rewrite is attempted?

## Next steps

1. Do not treat the current overview as the accepted external presentation.
2. Before another rewrite, reduce each action sequence to the causal relation it is meant to explain and reject sentences whose items can be reordered without changing their apparent meaning.
3. Re-review the opening independently from the architecture, with explicit attention to sentence-level catalogues.

## Recommendation

Repair the editorial method before repairing the document: use the user's cited sentence as the negative control and require every multi-part sentence to state why its parts belong together.

## Files touched

- `plans/governed-agent-work-infrastructure/essays/work-and-knowledge-system-overview.md`
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/dialogue.md`
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/findings.md`
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/01-reader-journey.md`
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/02-system-composition.md`
- `plans/governed-agent-work-infrastructure/essays/robot-talks/2026-08-12-work-overview-composition/reports/03-product-fidelity.md`
- `plans/governed-agent-work-infrastructure/essays/reviews/work-overview-reader-fit/review.md`
- `plans/governed-agent-work-infrastructure/essays/reviews/work-overview-fidelity/review.md`
- `sessions/2026-08-12-1823-work-overview-composition-failure.md`
