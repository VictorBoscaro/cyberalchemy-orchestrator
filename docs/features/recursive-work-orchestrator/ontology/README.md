---
tags: [orchestrator, recursive-work, ontology, architecture-properties]
node_type: readme
is_session: false
session_ref: null
layer: [ontology, architecture, application]
nature: [reference, technical]
status: draft
version: 0.1.0
last_updated: 2026-08-05
private: true
authority: proposal-only
---

# Recursive Work Orchestrator ontology package

This directory contains two deliberately different representations of the same candidate
architecture:

- [`ONTOLOGY.md`](ONTOLOGY.md) is the frozen, human-readable mapping of the design;
- [`ontology.json`](ontology.json) is its machine-addressable architecture-property projection.

Neither file is a canonical repository definition, an implementation specification, a runtime
observation, a conformance verdict, or an authorization decision. The semantic precedence is:

1. [`../DESIGN.md`](../DESIGN.md) — primary proposal meaning;
2. [`ONTOLOGY.md`](ONTOLOGY.md) — candidate structured narrative;
3. [`ontology.json`](ontology.json) — validated machine projection;
4. [`views/typed-coordinated-work-atlas.json`](views/typed-coordinated-work-atlas.json) — removable
   learner projection.

If these layers disagree, the package records a conflict or residue. A lower layer never repairs
or overrides a higher layer silently.

## Package anatomy

| Path | Responsibility | Cannot establish |
|---|---|---|
| [`ontology.json`](ontology.json) | Stable IDs, element types, typed properties, relations, shields, portable constraints, profiles, observation projections, premises, sources, and residue. | Runtime behavior, authority, promotion, or implementation conformance. |
| [`schemas/ontology.schema.json`](schemas/ontology.schema.json) | Structural interchange contract for the core ontology. | Semantic validity by itself. |
| [`views/typed-coordinated-work-atlas.json`](views/typed-coordinated-work-atlas.json) | Structure, Flow, Ownership/Proof, Inspector, legend, and negative-control projection contract. | A built interface, accessibility, or learner comprehension. |
| [`typed-coordinated-work-atlas.html`](typed-coordinated-work-atlas.html) | Standalone full-viewport SVG canvas with three lenses and one in-canvas Inspector. | Projection compilation, accessibility conformance, learner comprehension, or runtime behavior. |
| [`schemas/view.schema.json`](schemas/view.schema.json) | Structural contract for removable view projections. | That a projection preserves meaning in a concrete UI. |
| [`examples/all-operators.pipeline.json`](examples/all-operators.pipeline.json) | Illustrative recursively composed graph covering sequence, fan-out, fan-in, gate, sidecar, bounded repeat, and explicit composition. | Execution, delivery, replay, or universal expressiveness. |
| [`schemas/pipeline-instance.schema.json`](schemas/pipeline-instance.schema.json) | Structural contract for illustrative graph instances. | Runtime validity or effect safety. |
| [`scripts/validate.mjs`](scripts/validate.mjs) | Dependency-free integrity, source-digest, reference, endpoint, profile, view, and bounded-cycle checks. | Runtime conformance or ontology promotion. |

The machine projection makes three necessary local clarifications that the narrative tables only
imply: `LeafBinding`, `PropertyConstraint`/`RelationConstraint`, and `EvidenceReference` are explicit
endpoint types; `WorkDefinition` has an explicit `has-contract` relation. These additions close
machine-reference gaps. They remain proposal-only and do not alter repository-wide definitions.

## Read it in this order

1. Start with the `WorkDefinition`, `WorkRun`, and `Attempt` types in `ontology.json`.
2. Follow `CompositeWorkDefinition -> has-body -> WorkGraph -> contains-node/contains-edge`.
3. Read the composition-form subtypes, remembering that all compile to event-triggered edges.
4. Separate `Command`, `Event`, `WorkProtocol`, and `Journal` before reading runtime flow.
5. Compare `DomainState`, `ConfirmationState`, and `OrchestrationCursor` owners.
6. Read the shields before evaluating any profile or example.
7. Use the Atlas projection only after the semantic IDs are clear.

## Validate

From this directory:

```bash
node scripts/validate.mjs
```

The command exits non-zero on a structural or traceability violation. A passing run means only that
the candidate package is internally coherent against its pinned proposal sources.

## Current proof ceiling

- Package integrity: testable by the local validator.
- Design correspondence: source-bound but still proposal-only.
- Illustrative graph conformance: testable only for the included finite example.
- Browser behavior: locally passed in Chromium at desktop and mobile viewport sizes for this exact HTML digest.
- Runtime conformance: unsupported; there is no implementation witness in this package.
- Ontology promotion: not granted; the promotion owner remains open as `rwo:residue.010`.
- Source drift: open in `rwo:residue.015`–`.017`; frozen source bytes were not rewritten.

## Connections

| Document | Type | Description |
|---|---|---|
| [`../DESIGN.md`](../DESIGN.md) | `derives-from` | Primary proposal meaning. |
| [`ONTOLOGY.md`](ONTOLOGY.md) | `refines` | Human-readable architecture-property mapping preserved byte-for-byte. |
| [`../research/2026-08-04-best-understanding-view/findings.md`](../research/2026-08-04-best-understanding-view/findings.md) | `contextualizes` | Accepted research recommendation for the removable Atlas projection. |
| [`../../../../vault/ontology-conventions.md`](../../../../vault/ontology-conventions.md) | `grounds` | Local knowledge-node and confidence conventions. |
