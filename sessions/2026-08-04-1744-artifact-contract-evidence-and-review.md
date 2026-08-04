---
tags: [artifact-contracts, research-lifecycle, frontmatter, connections, protocol-compilation, review]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-04T17:44:30-03:00
updated_at: 2026-08-04T17:44:30-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session reconnects an unfinished research lifecycle inquiry to current authoring and ACI evidence without promoting the candidate architecture prematurely."
---

# Artifact Contract Evidence and Review

## Summary

The repository objective served was to keep generated agent artifacts connected to their purpose,
sources, decisions, and evidence rather than relying on locally plausible prose. The session
diagnosed that frontmatter and Connections vary by artifact kind and that predictable relations can
often be derived from workflow-bound output paths, while semantic tags and relations still require
author judgment. Instead of opening a competing research line, the existing research-lifecycle
initial definitions were refreshed and a new evidence record separated direct repository
observations, owner direction, candidate architecture, and unresolved questions. Two independently
bound read-only reviewers attacked the frozen three-document corpus through fidelity/governance and
mechanics/reference-integrity lenses. Their review found scope leakage into initial definitions,
stale unscoped corpus counts, missing source attribution, one missing reciprocal edge, and two
precision issues; the sustained corrections were applied while pre-existing inverse-edge migration
outside the target scope was left explicit rather than changed incidentally. The governed review
dispatch closed as resolved with both seats terminal and no reviewer output persisted into the
research folder.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Research Lifecycle Definitions — Initial Definitions](../research/research-lifecycle-definitions/research-initial-definitions.md) | `is-part-of` | This session belongs to the existing bounded inquiry into artifact fields, generation responsibility, relations, and validation. |
| [Current authoring contracts and ACI integration seams](../research/research-lifecycle-definitions/evidence/current-authoring-and-aci-seams.md) | `contextualizes` | The session records the owner direction, independent review, and correction boundary surrounding this evidence. |

## Open questions

- Should each artifact retain objective and question text, stable references to an upstream owner,
  or a digest-pinned combination of both?
- Which relation types are safe to materialize from workflow bindings, and should inverse
  navigation be projected rather than persisted twice?
- Does the first artifact-contract registry belong to repository authoring governance, Protocol
  Governance, or a separately owned capability bound into ACI?

## Next steps

1. Complete `research.md` and `findings.md` under `research/research-lifecycle-definitions/` using
   the accepted evidence and current repository witnesses.
2. Use the resulting findings to frame a repository-wide discovery before changing schemas,
   producer skills, hooks, Protocol Compilation, or dispatch completion gates.
3. Record or resolve the pre-existing inverse-edge migration residue without broad incidental edits.

## Recommendation

Finish the existing research before designing the registry: it already owns the unresolved
boundary among kind-specific payloads, output bindings, deterministic relations, author judgment,
validation receipts, and read projections.

## Files touched

- `research/research-lifecycle-definitions/research-initial-definitions.md`
- `research/research-lifecycle-definitions/evidence/README.md`
- `research/research-lifecycle-definitions/evidence/current-authoring-and-aci-seams.md`
- `.codex/workflow-inputs/2026-08-04-research-lifecycle-artifact-contract-review/`
- `telemetry/agents/subagents-dispatch.yaml`
- `sessions/2026-08-04-1744-artifact-contract-evidence-and-review.md`
