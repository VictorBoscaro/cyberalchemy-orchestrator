---
status: accepted
date: 2026-08-06
scope: recursive-work-orchestrator-composition-forms
decision_id: DG-RWO-CFM-006
selected_option: OCCURRENCE-OMIT-USE-SOURCE-PATH
---

# RWO form-occurrence representation

## Decision

The RWO composition-form source model does not add `FormOccurrence`. Compilation results and defects identify an authored form use directly with:

```text
source_form_ref: ExistingCompositionFormRef
canonical_source_path: CanonicalSourcePath
```

The root path is represented canonically as `/`; nested paths are always explicit. Within one compilation input, the exact occurrence key is:

```text
(raw_source_digest, source_form_ref, canonical_source_path)
```

This tuple supports diagnostic grouping, deduplication, navigation, source reuse, and reproducible compilation without introducing another identity object. A source restructure changes the canonical path and therefore creates a different occurrence key; the system must not claim continuity across changed source bytes without an explicit migration.

## Rationale

No current fixture, compiler, diagnostic workflow, cache, or ontology query demonstrates a need for an independently addressable occurrence node. Materializing one would package the same form reference and path while adding another schema, identity, resolver, relation set, and validation surface.

If future evidence requires persistent occurrence annotations, cross-pass incremental caching, or shared occurrence-level references, a later version may introduce a compile-only concept through a new owner decision and migration. It must never become a runtime `FormInstance` or alias `WorkNode`, `WorkRun`, `Attempt`, repeat-round, or journal identity.

## Authority boundary

This decision settles source-occurrence representation only. It does not authorize compiler-result schema, design, ontology, implementation, generation, promotion, release, deployment, or production mutation.

## Source and consequences

- Refined candidate: `docs/features/recursive-work-orchestrator/development/refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/delegated-research/findings.md`.
- Admissibility receipt: `docs/features/recursive-work-orchestrator/development/decision-gates/20260806T203541Z-composition-form-owners/receipts/DG-RWO-CFM-006-option-admissibility.json`.
- Decision source: repository owner selected option `OCCURRENCE-OMIT-USE-SOURCE-PATH` in the active 2026-08-06 Decision Gate.

Future candidate schemas and ontology proposals should omit `FormOccurrence` and require canonical source paths on compilation results and defects.
