---
tags: [portability, translation, agents, dispatch, ledger]
node_type: conceptual
is_session: true
layer: architecture, domain, application
nature: explanatory, procedural
status: active
created: 2026-07-20
timestamp: 2026-07-20T22:18:33-03:00
expires: 2026-09-18
conversation_id: unknown
decisions_made: true
contradictions_found: false
specs_updated: [README.md]
promoted_candidates: []
expected_importance: 7
importance_rationale: "Establishes portability/genericity as a new falsifiable design axis (H-PORT-1..6) at the repo's front door and normalizes the whole core-docs surface to English, but is purely declarative — no collapse-test ran and no code/behavior changed."
---

# README overhaul, genericity goal, and full core-docs PT→EN translation

## Summary

The session rewrote the repo's thin README into a comprehensive one by dispatching three
independent, tensioned drafters (orientation / thesis / operation angles) plus a
synthesizer, ranking the drafts, and composing the best of each. It added a new
first-class design goal — the orchestration substrate should be generic, droppable into
any repo with near-zero integration — expressed as falsifiable hypotheses H-PORT-1..6
(each with a collapse-test) plus an open question OQ-PORT on the minimal portability kit.
It then translated all 15 in-scope docs from Portuguese to English, one translator plus
one paired reviewer per doc (zig-zag up to 3x), preserving every identifier, data-testid,
API route, Lean anchor, path/filename, frontmatter key, and mermaid structure; a read-only
recon probe first inventoried what to translate vs never touch (append-only ledger,
vendored skills, session logs, fixtures). Human-confirmed scope decisions: core docs only
(no session logs), delete the throwaway readme-candidates, translate doc prose only —
Python comments and the ten UI labels stay Portuguese so the Playwright tests are
untouched. Reviews returned 11 PASS + 4 small fixes, all applied; a final pass reslugged 5
cross-file anchor links in the README to the new English headings, and a sweep confirmed
zero residual Portuguese across the 15 in-scope docs. A byproduct finding: git HEAD already
held PLAN/FRAMINGS/MAPPING/OBLIGATIONS in English while the working tree held Portuguese
copies, so translating them restored a match with HEAD (they show as unmodified). Both
multi-agent efforts were registered in the append-only ledger — two dispatch rows plus two
close rows — per the register-dispatch discipline.

## Open questions

Is English now the repo's language of record? The 15 core docs are English, but
`sessions/*`, one Portuguese quote in `vault/constitution/engine-constitution.md`, and the
vendored `.claude/skills/` remain Portuguese — no policy yet decides whether the
out-of-scope surface follows, or whether the Portuguese working-tree/English-HEAD split on
the four root docs signals a prior, partially-reverted translation pass that should be
reconciled before more docs move.

## Recommendation

If the goal is a fully English repo, the keystone is deciding the language-of-record
question above before touching anything else — the licensing fact is that the 15 in-scope
docs are verified Portuguese-free and the ledger is consistent, so the substrate is a clean
base to extend from. Once decided, two mechanical tracks follow under the same
translator+reviewer discipline: (1) the low-risk cleanup of `sessions/*`, the
engine-constitution quote, and any own (non-vendored) skills; (2) the higher-risk UI phase —
translating the ten UI labels while synchronizing `test_ui.py` atomically. Treat track (2)
as a hunch about risk, not a settled plan: the ten UIs share one testid contract and PT
labels are asserted by the Playwright suite, so label and test must move in the same step or
the suite breaks.

## Files touched

- README.md
- PLAN.md
- FRAMINGS.md
- MAPPING.md
- OBLIGATIONS.md
- definitions/DEFINITIONS.md
- implementations/README.md
- implementations/UI-CONTRACT.md
- vault/hypothesis/orquestracao-anti-ruido.md
- docs/essays/orquestrador-anti-ruido/README.md
- docs/essays/orquestrador-anti-ruido/research/costura-feasibility/findings.md
- docs/essays/orquestrador-anti-ruido/research/frame-refine-review/review.md
- docs/essays/orquestrador-anti-ruido/research/prior-art-ct-kahneman-thaler/findings.md
- docs/features/ui-studio/README.md
- docs/features/ui-studio/verification.md
- telemetry/agents/subagents-dispatch.yaml (2 dispatch + 2 close rows)
- docs/readme-candidates/ (created then deleted — does not persist)
