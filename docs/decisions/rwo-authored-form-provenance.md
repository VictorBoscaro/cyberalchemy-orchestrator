---
status: accepted
date: 2026-08-06
scope: recursive-work-orchestrator-composition-forms
decision_id: DG-RWO-CFM-005
selected_option: PROVENANCE-EMBEDDED-SELECTORS
---

# RWO authored-form provenance

## Decision

Every authored composition form embeds a non-empty collection of immutable source selectors. The form remains self-contained and does not require a provenance registry or separately resolved provenance record.

```text
ImmutableSourceSelector {
  source_ref: StableSourceRef
  source_version: ExactVersion
  selector: ExactSelector
  byte_domain: ByteDomainDescriptor
  byte_size: NonNegativeInteger
  digest_algorithm: ExactDigestAlgorithm
  digest: Digest
}

authored_form.provenance: NonEmpty<ImmutableSourceSelector>
```

Selectors are unique by their complete canonical tuple. Collection order has no semantic meaning; canonical serialization sorts by source reference, source version, selector, byte-domain identity, digest algorithm, and digest. A source change creates new provenance bytes and a new authored-form digest; it never silently rewrites existing evidence.

## Rationale

Embedded selectors make every form independently inspectable and offline-validatable, avoid resolver availability and registry-ownership dependencies, and do not add an ornamental ontology concept. Repetition across forms is accepted as a smaller cost than introducing another authoritative identity and lifecycle.

A digest alone is insufficient: reproducibility also requires source identity, exact version, selector, byte domain, size, and named digest algorithm. Provenance establishes source binding only; it does not prove truth, correctness, admission, authority, or runtime conformance.

## Authority boundary

This decision settles the representation of authored-form provenance only. It does not authorize source collection, schema, design, ontology, implementation, generation, promotion, publication, release, deployment, or production mutation.

## Source and consequences

- Refined envelope: `docs/features/recursive-work-orchestrator/development/refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/delegated-research/findings.md` under “Exact authored source envelope”.
- Admissibility receipt: `docs/features/recursive-work-orchestrator/development/decision-gates/20260806T203541Z-composition-form-owners/receipts/DG-RWO-CFM-005-option-admissibility.json`.
- Decision source: repository owner selected option `PROVENANCE-EMBEDDED-SELECTORS` in the active 2026-08-06 Decision Gate.

Future candidate schemas, fixtures, compilation results, and ontology source-binding queries may cite this record. Exact selector grammars and source-owner acceptance remain separately owned.
