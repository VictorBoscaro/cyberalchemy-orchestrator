---
tags: [frontmatter, document-metadata, lifecycle-timestamps, subagent-review, workflow-governance]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-07-27T16:22:18-03:00
updated_at: 2026-07-27T16:22:18-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session establishes timezone-aware document lifecycle metadata, separates document tags from activation telemetry, and verifies the direct authoring integrations through a governed review."
---

# Frontmatter timestamps and governed review

## Summary

The session resumed from the research-decomposition handoff and separated the generic dispatch
integration boundary from research-specific judgment. It decided that the generic strategy should
define integration handoffs while `research` proves bounded executable slices before universal
promotion. The invocation-and-collaboration research baseline was refined to record the unresolved
ownership boundary between skill-local canonical topologies, generic graph composition, confirmed
Dispatch authority, and runtime compilation. Inspection of document tagging established that the
governed-Markdown hook only reminds the authoring agent, the agent selects document tags, and
activation telemetry tags remain a separate observational record. The frontmatter guide was updated
to require immutable `created_at` and revision-sensitive `updated_at` as RFC 3339 timestamps produced
in the `America/Sao_Paulo` civil timezone, while forbidding fabricated legacy creation times. A
confirmed inline review dispatch used two independently tensioned attackers and found three
integration defects: a legacy session timestamp template, consumers pointing at the ignored mirror,
and an unsupported generic topical-tag fallback. The parent verified all three findings directly,
updated the affected integrations to use the canonical guide and new timestamp fields, and removed
the unsupported fallback. Source hashes, mirror synchronization, JavaScript syntax, diff hygiene,
dispatch registration, and dispatch closure were verified successfully.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Governed agent work infrastructure plan](../plans/governed-agent-work-infrastructure/PLAN.md) | `is-part-of` | The metadata, graph-ownership, and dispatch-review decisions support the project-wide governed agent-work infrastructure. |
| [Frontmatter and Connections guide](../.claude/skills/custom/frontmatter.md) | `validates` | The session records the independent review and direct integration checks applied to the revised authoring guide. |

## Open questions

- Which durable evidence sources may authorize `created_at` for pre-existing artifacts that have no
  trustworthy creation receipt?

## Next steps

1. Audit remaining authoring skills and templates for legacy lifecycle fields and `.agents`
   frontmatter-guide pointers.
2. Define a provenance-aware migration rule before bulk-backfilling `created_at` and `updated_at`
   across existing documents.

## Recommendation

Audit direct authoring consumers before attempting corpus-wide migration, because the governed
review demonstrated that consumer drift is the immediate failure mode.

## Files touched

- `.agents/skills/close-session/SKILL.md`
- `.agents/skills/custom/frontmatter.md`
- `.claude/hooks/doc-frontmatter-nudge.cjs`
- `.claude/skills/close-session/SKILL.md`
- `.claude/skills/custom/frontmatter.md`
- `research/agent-invocation-and-collaboration-topology/research-initial-definitions.md`
- `telemetry/agents/subagents-dispatch.yaml`
- `tmp/frontmatter-timestamp-review-proposal-v1.json`
- `sessions/2026-07-27-1622-frontmatter-timestamps-and-review.md`
