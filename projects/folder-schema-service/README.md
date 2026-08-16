# Folder Schema Service

Status: bootstrap.

This README describes the intended boundary of Folder Schema Service; it does not claim that the
service is implemented. The project will define and validate minimal schemas for governed folders.
It depends on Schema Service for schema identity, resolution, versioning, and definition validation.

## Why it matters

A filesystem records paths and containment, but not what a folder means. This service is intended
to make the minimum necessary folder semantics explicit and checkable. It can then compare declared
identity and relations before and after movement, composition, or extraction; it does not perform
those operations or guarantee portability during bootstrap.

## Operational model

A governed folder references an existing folder schema; creating a folder does not create a new
schema definition. Creation, movement, composition, and extraction are validation events. A new
folder schema or field is introduced only when a concrete case cannot be classified or validated by
the existing contracts.

## Responsibilities

- Define folder kinds and their minimum contracts.
- Define valid placement and recursive composition.
- Check declared folder identity and relations across repository boundaries.
- Validate folder manifests.
- Maintain conformance cases as evidence for each rule.

## Boundary

This service does not own `SchemaId`, the metaschema, or the generic schema registry; those belong to Schema Service. It also does not define the internal schemas of artifacts or code.

The first candidate folder-schema identifier is `folder/project@0`. Its contract grows only when a
concrete conformance case demonstrates that another rule or field is necessary.
