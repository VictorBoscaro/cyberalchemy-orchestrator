---
artifact_kind: research-initial-definitions
status: candidate
date: 2026-08-25
topic: domainspec-lean-schema-precedents
---

# DomainSpec Lean schema precedents — initial definitions

## Context

Schema Service is intended to govern reusable artifact types, immutable schema-definition
revisions, durable artifacts, manifest revisions, representations, observations, and validation
without granting authority through path or convention alone. Its next experiment will begin with
the `skill` family, for which the semantic boundary among definition, source package, installation,
tool, invocation, and receipt is not yet settled.

The sibling `domainspec-lean-formalization` repository contains earlier formalization, research,
schemas, and project records relevant to these terms, but their status and exact distinctions have
not been reconstructed. Existing discussion has also raised multilevel metamodeling as a possible
comparison. Recovering the claims actually supported in both corpora matters because Schema Service
should reuse owned distinctions and avoid silently strengthening analogies, partial models, or
abandoned proposals.

## Purpose

This document establishes the informational context for research that will inform the design of
the Schema Service metaschema, universal artifact envelope, and first skill-family schema. It also
keeps proposed relational and reflexive interpretations separate from accepted product constraints.

## Research Question (Can be refined)

What have `domainspec-lean-formalization` and relevant primary literature established, proposed,
contested, or left open about schemas, metaschemas, multilevel classification, artifact instances,
identity, representations, and closure, and which of those results can responsibly inform the
current Schema Service design?

## Confirmed Product Constraints

- The first Schema Service artifact-family experiment will use `skill`; the exact experimental
  slice and schema remain undecided.
- A reusable semantic `Type` is distinct from an immutable `SchemaDefinitionRevision`.
- A durable `Artifact` is distinct from its `ManifestRevision`, representations, and observed
  representation snapshots.
- Schema revisions carry an objective explaining why their type contract exists.
- A schema revision's objective and an artifact instance's objective are distinct; the latter may
  be inherited or referenced rather than duplicated.
- Experimental schema candidates remain non-normative until an authorized publication operation.
- Path, location, and digest do not independently provide durable semantic identity or normative
  authority.
- No universal registry, resolver, runtime, or final serialization is currently accepted.

## Current Evidence Baseline

- The Schema Service README defines a bootstrap model that distinguishes type, immutable schema
  revision, durable artifact, manifest revision, representation, snapshot, validation, and
  enforcement. It leaves the metaschema serialization and minimum artifact manifest open.
- Repository-local precedent research found partial schema, handle, digest, receipt, and validation
  mechanisms in earlier DomainSpec work, but no complete operational witness for the proposed
  Schema Service lifecycle.
- The accepted `skill`-first decision changes the experiment order without approving a skill
  schema, criterion, fixture set, resolver, registry, or runtime. The earlier `analysis` package
  remains evidence and deferred material.
- Robot-Talks found that relative schema/instance roles are compatible with the current model only
  when governed record kinds and authority remain explicit. It also found that one `conformsTo`
  relation would currently collapse schema reference, classification, validation, and enforcement.
- The README currently presents the metaschema as a bootstrap root. That is an operational proposal;
  the mechanism and guarantees of kernel cutoff, self-description, self-validation, or self-hosting
  have not been demonstrated.
- The universal envelope still has no accepted decision on whether instance objectives and tags
  are always materialized, optional, inherited, or derived, nor on whether `type` is repeated or
  resolved through the exact schema reference.

## Known Gaps

- Which schema and metaschema definitions in the sibling repository were normative, experimental,
  historical, or abandoned is unknown.
- It is unknown whether the sibling repository formally separates semantic type identity from
  revision-exact schema identity.
- The exact relationship there among artifact, instance, carrier, representation, snapshot, digest,
  and path is not yet reconstructed.
- It is unknown which conclusions are backed by Lean definitions or theorems versus prose,
  examples, or plans.
- The transferable implications for a skill schema and universal artifact envelope have not been
  synthesized.
- It is unknown whether the useful model is strict/two-level metamodeling, a typed open graph,
  orthogonal linguistic and ontological classification, clabject/deep-instantiation machinery,
  powertypes, Type Object, a reflective architecture, or a smaller combination.
- The exact meanings and domains of `references_schema`, `classifies`, `instance_of`,
  `linguistically_conforms_to`, `satisfies`, `validated_against`, `extends`, and `represents` have
  not been compared. No transitivity or equivalence among them is established.
- It is unknown which object a metaschema should validate: a logical schema-definition revision,
  its manifest, its representation snapshot, its effective closure, or an explicit tuple.
- It is unknown whether `clabject`, potency, or deep instantiation provide necessary operational
  power for the `skill` witness or merely redescribe role relativity.
- Proposed distinctions between schema-level residue and instance/data-integrity failure have not
  been grounded in source terminology, shown exhaustive, or connected to a required metaschema
  capability.
- The trusted base and closure obligations remain open. A kernel cutoff, a self-describing
  meta-metamodel, self-validation, and structural self-hosting are not assumed equivalent.
