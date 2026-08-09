---
tags: [resonantos, meeting-model, community-governance, participation, research-lifecycle]
artifact_kind: session
layer: domain
version: 0.1.0
created_at: 2026-08-08T00:53:04-03:00
updated_at: 2026-08-08T00:53:04-03:00
expires: 2026-10-07
decisions_made: true
contradictions_found: true
specs_updated:
  - ../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md
promoted_candidates: []
expected_importance: 8
rationale: Establishes the evidence plan and first coherent vocabulary, narrative, and decision triad for a community-facing meeting model while exposing unresolved admission and ratification gates.
---

# Session: ResonantOS meeting model

## Summary

This repository governs how agent work remains connected to objectives, decisions, assumptions, actions, and evidence. The session aimed to frame a small, understandable ontology for ResonantOS meetings without prematurely turning it into policy. Official public material supported treating meetings as social infrastructure spanning philosophy, operating practices, and governance. The coarse distinction between work and community life was retained as a hypothesis and primary orientation, not as an exclusive taxonomy. Openness was separated into access, participation, decision rights, recording, and records, avoiding the false equation of transparency with unrestricted attendance. A bounded research plan was created, and `research-plan` was registered as a candidate canonical kind with its operational contract deliberately unresolved. Ontology, system, and engineer views were authored together, with a consistency report showing structural alignment across eighteen terms and nine decision stances. Structural and link checks passed, but no real meeting inventory or participant interviews have yet tested the model. Ratification ownership remains critical before the proposal can be represented as an official community model.

## Connections

| Target | Relation | Rationale |
|---|---|---|
| [Research plan](../research/resonantos-meetings/research-plan.md) | `is-part-of` | This session established and began the bounded research and view-authoring work described by the plan. |

## Open questions

- Who has authority to ratify the meeting model, and through which community process?
- What producer, authority rollup, instance contract, and permitted edges would be required to admit `research-plan` as an operational canonical kind?
- Will the proposed `work / community life` orientation survive classification of real ResonantOS meetings and participant interviews?
- How should this repository's `artifact_kind` discriminator coexist with the sibling ontology's candidate `canonical_kind` field?

## Next steps

- Build the evidence set specified in the research plan: 10–15 meeting instances, 5–8 interviews, and the bounded source review.
- Revise the ontology, system narrative, and decision register together when evidence changes a term or stance.
- Route the `research-plan` producer and authority questions through an explicit decision gate before changing validators or allowed edges.
- Name the ratification owner and review path before presenting the meeting model as official.
- Align the new view artifacts with repository frontmatter and connection requirements once their artifact-kind assignments are confirmed.

## Recommendation

Run the evidence phase before promoting either the meeting taxonomy or `research-plan` into policy. Treat the current views as a coherent working hypothesis, and resolve ratification ownership before asking the wider community to adopt them.

## Files touched

- `research/resonantos-meetings/research-plan.md`
- `research/resonantos-meetings/ontology-view.md`
- `research/resonantos-meetings/system-view.md`
- `research/resonantos-meetings/engineer-view.md`
- `research/resonantos-meetings/paired-views-report.md`
- `../domainspec-core/cyberAlchemy-v2/ontology/canonical-kinds/CANONICAL-KINDS.md`
- `sessions/2026-08-08-0053-resonantos-meeting-model.md`
