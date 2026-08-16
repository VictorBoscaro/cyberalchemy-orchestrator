---
tags: [schema-governance, folder-topology, project-boundaries, metadata]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-14T22:14:29-03:00
updated_at: 2026-08-14T22:14:29-03:00
expires: 2026-10-13
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session established bootstrap ownership boundaries for schema infrastructure that may govern future repository topology and artifact metadata."
---

# Schema Services And Governed Folder Boundaries

## Summary

This session advanced the repository objective of preserving the reason and authority behind local work by making directory meaning a candidate for explicit, verifiable governance. The session set out to determine how autonomous and recursively composable folders should be represented and where the supporting schema infrastructure should live. It decided that governed instances reference reusable schema definitions rather than creating a new schema whenever an artifact or folder is created. It also established that governance applies only inside an explicit governed boundary, not automatically to every filesystem object. Schema growth was constrained by evidence: a new field or rule must answer a concrete conformance case that the existing contract cannot classify or validate. The current cross-domain candidate retains only a resolvable schema reference, while `id` and `objective` remain hypotheses, tags remain optional, and summaries remain derived until freshness or consumer evidence justifies persistence. An earlier `workspace-schema-service` design was found to collapse generic schema mechanics and folder-specific semantics, so it was replaced by separate [Schema Service](../projects/schema-service/README.md) and [Folder Schema Service](../projects/folder-schema-service/README.md) project boundaries. A toy tournament showed that the governed subject must be resolvable but did not determine whether that subject belongs in the schema identifier or its resolved definition. The session created orientation documents only; no schemas, manifests, runtime services, migrations, or adapters were implemented.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Repository README](../README.md) | `is-part-of` | The session refines repository-level infrastructure for keeping local artifacts connected to explicit objectives, boundaries, and evidence. |
| [Schema Service](../projects/schema-service/README.md) | `contextualizes` | The session records why generic schema mechanics were separated from governed-subject semantics and kept at bootstrap scope. |
| [Folder Schema Service](../projects/folder-schema-service/README.md) | `contextualizes` | The session records why folder meaning, placement, composition, and conformance require a specialized consumer of Schema Service. |

## Open questions

- Must `id` and `objective` belong to a shared instance envelope, or should domains derive or own them?
- Should a schema identifier encode its governed subject, as in `folder/project@0`, or should the resolved schema definition declare that subject?
- Which creation boundaries enroll a filesystem object as a governed subject, and how are those events observed without governing every file?
- What concrete freshness failure or consumer would justify persisting summaries and introducing a reconciliation service?

## Next steps

1. Create the smallest valid and invalid conformance cases for a generic governed instance and `folder/project@0`.
2. Test each candidate shared field against derivability, domain ownership, and an actual consumer.
3. Define the bootstrap `SchemaId` grammar and immutable revision behavior only as far as those cases require.
4. Introduce manifests or implementation directories only after the conformance evidence identifies their necessary shape.

## Recommendation

Start with paired valid and invalid cases that force `schema`, `id`, `objective`, tags, and summary to compete for admission; preserve only fields whose absence makes a required distinction impossible.

## Files touched

- `projects/README.md`
- `projects/schema-service/README.md`
- `projects/folder-schema-service/README.md`
- `projects/workspace-schema-service/README.md` (removed)
- `projects/workspace-schema-service/schemas/README.md` (removed)
- `projects/workspace-schema-service/service/README.md` (removed)
- `projects/workspace-schema-service/conformance/README.md` (removed)
- `tmp/schema-tournament/experiment.md`
- `tmp/schema-tournament/tournament.mjs`
- `tmp/schema-tournament/challenge.md`
- `tmp/schema-tournament/challenge.mjs`
- `tmp/schema-tournament/report.md`
- `sessions/2026-08-14-2214-schema-services-boundaries.md`
