---
tags: [schema-governance, artifact-modeling, knowledge-representation, open-world-typing]
artifact_kind: session
layer: project
version: 0.1.0
created_at: 2026-08-17T14:00:44-03:00
updated_at: 2026-08-17T14:02:26-03:00
expires: 2026-10-16
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: [projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/findings.md]
expected_importance: 9
importance_rationale: "The session established the bootstrap conceptual boundary that later Schema Service research, refinement, and implementation must preserve."
---

# Schema Service artifact model and open-world governance

## Summary

The repository seeks to preserve the objectives, decisions, assumptions, actions, and evidence that make agent-produced artifacts meaningful, and this session clarified the Schema Service contribution to that objective. The session set out to understand the existing Schema Service research and refine the role of schema beyond examples such as Plan, Research, and Discovery. A bounded scan of prior `research-domainspec` work showed that it already separates schema, instance, relation, composition, and authority, but does not settle domain/type/instance granularity or organizational knowledge promotion. The session decided that a reusable `Type` must be distinguished from each immutable `SchemaDefinitionRevision`, while a concrete `Artifact` is described by a `ManifestRevision` rather than receiving its own schema merely by existing. It also decided that every artifact admitted to a governed boundary may enter through a resolvable fallback and later be reclassified after a candidate type receives authorized publication. A three-agent Robot-Talks exposed nine cross-layer tensions and established that artifact identity, manifest assertions, representations, and representation snapshots must remain distinct logical roles. The accepted findings were used to update the Schema Service README with open-world admission, explicit path-constraint/composition boundaries, and 26 intentionally unresolved questions. The governed research dispatch required reconciling the Stage-E source manifest with the current `AGENTS.md`, after which the focused bridge/workflow tests passed and the dispatch closed as resolved. A project-local knowledge ledger was judged feasible and likely useful, but its entry schema, authority, canonical-source relationship, and non-overlap with telemetry and the schema registry were deliberately deferred to refinement. No Schema Service runtime or project-local ledger was implemented.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Schema Service README](../projects/schema-service/README.md) | `is-part-of` | This session shaped the bootstrap model and open questions of the Schema Service project represented by the README. |
| [Universal artifact schema role findings](../projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/findings.md) | `derives-from` | The accepted conceptual changes and deferred tensions were derived from the three-perspective Robot-Talks synthesis. |
| [Artifact schema governance landscape findings](../projects/schema-service/research/artifact-schema-governance-landscape/findings.md) | `derives-from` | The session's distinctions and research boundary build on the bounded synthesis of prior DomainSpec research. |

## Open questions

- What stable identity does a `Type` retain across immutable schema-definition revisions?
- How do overlapping domains, multiple typing, subtyping, refinement, and reusable capabilities differ operationally?
- What lifecycle and authority distinguish descriptive labels, candidates, drafts, published schemas, deprecation, and active enforcement?
- How are artifact, manifest revision, representation, snapshot, authored assertion, and inferred observation kept consistent without hiding disagreement?
- What exact fields belong to the minimum manifest, and which artifact families require specialized identity or snapshot contracts?
- What entry schema, append authority, and canonical-source rules would make a project-local ledger useful without duplicating research, sessions, telemetry, or the schema registry?

## Next steps

1. Run `refine` over the Schema Service project using the README, research findings, and Robot-Talks session as the evidence baseline.
2. Resolve the `Type`/`SchemaDefinitionRevision` identity boundary and the artifact/manifest/representation temporal model before implementation planning.
3. Define a project-local ledger contract during refinement and create the ledger only if its owner and non-overlap are demonstrated.
4. Open separate research on promotion of observations and evidence into institutional knowledge only if refinement confirms that gap is required for the current boundary.

## Recommendation

Run the refinement loop before creating the ledger or implementing runtime services; use the accepted Robot-Talks tensions and the README's explicit open questions as the seed, and require every proposed resolution to state which role it owns and which questions it intentionally leaves open.

## Files touched

- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `implementations/server/runtime/local_pilot.py`
- `projects/schema-service/README.md`
- `projects/schema-service/research/artifact-schema-governance-landscape/findings.md`
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/dialogue.md`
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/findings.md`
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/01-conceptual-model.md`
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/02-admission-governance.md`
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/reports/03-representation.md`
- `.codex/workflow-inputs/2026-08-17-schema-domain-prior-art-scan/opening.json`
- `.codex/workflow-inputs/2026-08-17-schema-domain-prior-art-scan/explorer-0-turn-0.json`
- `.codex/workflow-inputs/2026-08-17-schema-domain-prior-art-scan/launch-plan.json`
- `.codex/workflow-inputs/2026-08-17-schema-domain-prior-art-scan/close.json`
- `telemetry/agents/subagents-dispatch.yaml`
- `telemetry/runtime/aci-slice0.sqlite3`
- `sessions/2026-08-17-1400-schema-service-artifact-model.md`
