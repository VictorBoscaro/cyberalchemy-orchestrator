---
tags: [ontology, document-metadata, graph-schema, schema-governance, provenance]
artifact_kind: session
layer: capability
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
timestamp: 2026-07-27T12:53:37-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session established the provisional boundary between authoring guidance, deterministic validation, and future graph-schema governance."
---

# Artifact Schema and Context Edges

## Summary

This session investigated how dispatches, tasks, research artifacts, and documents can retain links
to context at multiple altitudes. Research lifecycle artifacts were selected as the first bounded
case before extending the model from micro tasks to macro project context. The document-kind
discriminator was consolidated under `artifact_kind`, while topical tags, contextual `layer`, and
typed Connections remained separate dimensions. `others` and `other` were retained as deliberate
fallbacks rather than values a hook may invent automatically. The frontmatter guide and
close-session workflow were aligned around creator-authored metadata, real connection targets, and
the `is-part-of` edge. The preferred interim validation flow is deterministic: remain silent when
required structure and registered values are present, and inform the creating agent when fields
are missing or values are unknown. A repository-local YAML file under `schemas/` was proposed as
the single machine-readable source of truth for fields, artifact kinds, layers, and edge types,
while skills explain semantic selection and hooks only validate. Composition, inverses,
cardinality, source-target compatibility, user extensions, and promotion of recurring fallback
types remain later governance concerns rather than first-version enforcement.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Research Lifecycle Definitions — Initial Definitions](../research/research-lifecycle-definitions/research-initial-definitions.md) | `is-part-of` | This session belongs to the bounded research inquiry into a minimal node-and-relation contract. |
| [Document Metadata, Tags, and Artifact-Schema Governance — Findings](../research/research-lifecycle-definitions/findings.md) | `refines` | The session narrows the findings into a provisional single-source schema and deterministic validation boundary. |
| [Frontmatter & Connections](../.agents/skills/custom/frontmatter.md) | `contextualizes` | The session records the reasoning behind the guide's artifact-kind, layer, fallback, and connection conventions. |

## Open questions

- Should the first schema treat registered values as closed enums, or distinguish warnings from
  hard conformance failures so user-defined vocabularies can incubate?
- How should a recurring `others` or `other` usage be proposed, reviewed, named, versioned, and
  promoted into the registered vocabulary?
- Which composition, inverse, cardinality, and source-kind-to-target-kind rules should eventually
  be represented, and which should remain authoring guidance?

## Next steps

1. Define the minimal structure and authority boundary of `schemas/artifact-metadata.yaml`.
2. Make the frontmatter hook read that schema without writing metadata or duplicating its values.
3. Add deterministic fixtures for missing, valid, fallback, and unknown field and edge values.
4. Reconcile existing research lifecycle documents with the accepted schema after its first
   version is approved.

## Recommendation

Start with the first two next steps: establish one small schema containing only field requirements
and vocabularies, then prove that the hook can validate it silently and non-mutatively before
adding graph composition rules.

## Files touched

- .agents/skills/close-session/SKILL.md
- .agents/skills/custom/frontmatter.md
- .claude/hooks/doc-frontmatter-nudge.cjs
- .claude/skills/close-session/SKILL.md
- .claude/skills/custom/frontmatter.md
- .codex/hooks.json
- research/research-lifecycle-definitions/
- sessions/2026-07-27-1253-artifact-schema-and-context-edges.md
