---
artifact_kind: research-initial-definitions
status: initial
date: 2026-08-17
topic: concrete-artifact-family-precedents
---

# Concrete artifact-family precedents

## Context

Schema Service is intended to keep governed artifacts connected to stable identity, reusable type
meaning, immutable schema revisions, manifests, representations, validation, and authority. Its
bootstrap model is currently conceptual and must remain grounded in repository practices that
already carry useful semantics.

The immediate problem is to determine whether the proposed distinctions explain concrete artifact
families already used by agents and DomainSpec, rather than merely forming a coherent abstract
vocabulary. This matters because implementation should build from existing ownership and contracts
where they exist.

## Purpose

This document establishes the context for research that will inform refinement of the Schema
Service artifact model and the later decision about its implementation boundary.

## Research Question (Can be refined)

How do existing ontology conventions and DomainSpec schema definitions instantiate, contradict, or
leave gaps in the proposed Schema Service model for documents, skills, agent tools, and folders,
with code-schema definitions used as supporting evidence?

## Confirmed Product Constraints

- The initial concrete families are documents, skills, agent tools, and folders.
- Code-schema definitions in `../domainspec-core` are supporting evidence, not an additional
  universal family requirement for this pass.
- A reusable `Type` is conceptually distinct from each immutable `SchemaDefinitionRevision`.
- A governed `Artifact` is distinct from its `ManifestRevision`, `Representation`, and
  `RepresentationSnapshot`.
- Admission may use a resolvable fallback; descriptive classification does not acquire normative
  authority automatically.
- This research does not authorize Schema Service runtime implementation or creation of its
  candidate project-local ledger.

## Current Evidence Baseline

- `projects/schema-service/README.md` records the current bootstrap model and intentionally open
  questions.
- `projects/schema-service/robot-talks/2026-08-17-universal-artifact-schema-role/findings.md`
  records the accepted cross-layer tensions behind that model.
- `sessions/2026-08-17-1400-schema-service-artifact-model.md` records that the model is documented
  but not implemented.
- The user identified `vault/ontology-conventions.md` in this repository and schema definitions in
  `../domainspec-core` as concrete precedent sources.

## Known Gaps

- It is not yet known which proposed Schema Service roles have direct existing counterparts in the
  two precedent sources.
- It is unclear whether the sources use stable semantic identity separately from revision or
  representation identity.
- It is unclear how document, skill, tool, folder, and code schemas divide ownership between a
  common kernel and family-specific contracts.
- It is unclear whether composition, containment, inheritance, validation, and publication have
  compatible meanings across the sources.
- It is unclear whether the evidence supports a standalone service, shared library, registry, or
  interoperability contract.
