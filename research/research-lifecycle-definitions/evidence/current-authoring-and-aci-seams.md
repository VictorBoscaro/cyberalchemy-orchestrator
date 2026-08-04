---
tags: [artifact-contracts, frontmatter, connections, skills, protocol-compilation, validation]
artifact_kind: research-evidence
layer: project
version: 0.1.0
created_at: 2026-08-04T17:12:45-03:00
updated_at: 2026-08-04T17:42:02-03:00
---

# Current Authoring Contracts and ACI Integration Seams

## Evidence purpose and boundary

This record preserves the repository observations and owner direction raised while diagnosing why
recent research artifacts omitted frontmatter and typed Connections. Direct observations below are
limited to the cited repository artifacts as they existed on 2026-08-04. The proposed direction is
conversation-sourced input for the open research; it is not an accepted finding, specification, or
runtime contract.

## Direct observations

1. `.claude/skills/custom/frontmatter.md` requires governed Markdown to carry YAML frontmatter and
   a `## Connections` section, assigns semantic selection to the creating agent, and states that the
   hook must not invent values or targets.
2. `.claude/hooks/doc-frontmatter-nudge.cjs` recognizes governed paths and checks only whether a
   frontmatter fence and `## Connections` heading exist. It emits additional context and does not
   validate required fields, relation vocabulary, target resolution, reciprocal declarations, or
   accepted output bytes.
3. `.agents/skills/research/SKILL.md` requires `research.md` and `findings.md` outputs but does not
   bind either output to the artifact-specific references under `reference/`.
4. `.agents/skills/research/reference/research-writing.md` and `findings-writing.md` prescribe
   reciprocal relations between those two files. They use `derives` as the inverse of
   `derives-from`, while the current frontmatter guide names `grounds` as that inverse and does not
   list `derives`. Their referenced `implementation/domainspec` convention paths are not the
   repository-local canonical guide.
5. `docs/features/agents-communication-infra/specs/protocol-compilation.md` and
   `implementations/server/runtime/protocol_compilation.py` define each profile output through
   `output_id`, a closed scalar `content_schema`, and `required`. The current contract carries no
   Markdown artifact schema, output path template, field-producer binding, or connection rule.
6. `docs/features/agents-communication-infra/specs/domain.md` requires `DispatchSpec.schema_refs`
   to include every executable input/output schema and later materializes an exact effective input
   for an attempt. These are existing seams, not evidence that document artifact contracts have
   already been integrated.
7. `docs/features/agents-communication-infra/specs/canonical-vault-reads.md` specifies read-only
   frontmatter, raw-connection, and logical-edge projections. It never repairs source documents and
   folds only the documented `derives-from`/`grounds` inverse pair. Its current staged gate remains
   blocked and it does not own authoring or output acceptance.
8. The `runtime-v2-migration-inventory` research package demonstrates the enforcement gap:
   `research-initial-definitions.md` has frontmatter but no Connections, while `research.md`,
   `findings.md`, and `review/review.md` have neither frontmatter nor Connections. The package's
   research output contract establishes the `research.md`/`findings.md` relationship, and its
   corresponding session has typed links to the initial-definitions and review artifacts; the
   missing document surfaces therefore coexist with known workflow and session relationships.

## Owner-proposed direction

The owner proposed that artifact kinds have distinct contracts: for example, research should
retain its objective and questions, while findings should retain the objective, questions, and
their answers. The owner also proposed deriving predictable Connections from already-known workflow
inputs: a findings producer receives the path of its research source, and a discovery producer
receives the path of its findings source.

The discussion refined that direction into a candidate architecture for research rather than an
accepted design:

- version contracts per artifact output kind instead of relying only on a category attached to the
  producing skill;
- compose a common metadata envelope with kind-specific fields and sections;
- materialize known paths, fixed metadata, and workflow-derived relations before authoring;
- leave topical tags and genuinely semantic relations to the author;
- validate the exact output against its frozen contract before acceptance or dispatch closure;
- persist one canonical relation direction where possible and derive inverse navigation in a read
  projection rather than requiring out-of-scope reciprocal mutations; and
- use a hook as fallback feedback for uncompiled writes, not as the authority that invents an
  artifact contract after generation.

## Questions this evidence does not settle

- Whether objective and question text should be duplicated, referenced by stable local IDs, or
  carried through a versioned artifact reference.
- Whether the first contract registry belongs to repository authoring governance, ACI Protocol
  Governance, or a separately owned capability later bound into ACI.
- Which relations are safe to derive from workflow topology without falsely converting access,
  sequence, or file proximity into semantic provenance.
- Whether a single persisted direction plus a derived inverse satisfies every current authoring,
  offline-reading, migration, and audit requirement.
- Which completion boundary can reject malformed Markdown without claiming semantic truth for
  agent-authored tags and relations.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Research Lifecycle Definitions — Initial Definitions](../research-initial-definitions.md) | `derives-from` | Defines the bounded research question and evidence boundary this record supports. |
| [Frontmatter & Connections](../../../.claude/skills/custom/frontmatter.md) | `contextualizes` | Supplies the current authoring obligations and non-invention rule observed here. |
| [Protocol compilation](../../../docs/features/agents-communication-infra/specs/protocol-compilation.md) | `contextualizes` | Supplies the current output-profile and compilation seams without yet defining document contracts. |
| [Canonical Vault Reads](../../../docs/features/agents-communication-infra/specs/canonical-vault-reads.md) | `contextualizes` | Supplies the existing non-mutating projection and inverse-folding boundary. |
