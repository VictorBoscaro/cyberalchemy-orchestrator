---
artifact_kind: robot-talks-findings
status: accepted-for-research-framing
date: 2026-08-25
topic: relational-metaschema-research-design
---

# Findings — relational metaschema research design

## Tensions and dispositions

| tension | layer A | layer B | severity | disposition |
| --- | --- | --- | --- | --- |
| `conformsTo` collapses distinct acts | The proposed tower uses one repeated relation. | The current model separates schema reference, resolution, observation, validation, report interpretation, publication, and enforcement. | high | **Real + actionable:** research each relation separately; deny transitivity by default. |
| Relative roles versus governed kinds | A schema can be an instance of a metaschema. | `SchemaDefinitionRevision`, `ManifestRevision`, `RepresentationSnapshot`, and `ValidationReport` retain distinct identity and lifecycle contracts. | high | **Real + actionable:** model role relations and record kinds together; do not replace one with the other. |
| Linear levels versus open-world graph | `L0/L1/L2` suggests global disjoint ranks and one schema per population. | The project admits overlapping domains, independent schemas, fallback classification, and unresolved multiple typing. | high | **Real + actionable:** treat level as a possible derived path depth, not stored ontology. |
| Bootstrap root versus unproven closure | The README says the metaschema is the bootstrap foundation and no infinite tower is required. | Kernel cutoff, self-description, self-validation, and self-hosting have not been distinguished or demonstrated. | high | **Real + actionable:** demote closure to a proposed trusted cutoff in research context; defer README mutation until evidence and review. |
| Schema definition as artifact versus meta-validation target | Schema definitions are artifacts governed by the same substrate. | It is undefined whether meta-validation targets the logical definition, manifest, representation snapshot, effective closure, or a tuple. | high | **Uncertain:** targeted repository and literature research. |
| `clabject` as explanation versus confirmation bias | The class/object duality resembles the proposed role relativity. | Its exact definition, variants, critiques, and operational necessity for Schema Service are unverified. | medium | **Real + actionable:** compare strict/two-level, OCA, clabject/deep instantiation, powertype, Type Object, and reflective approaches using primary sources. |
| Craft witness versus accepted experiment order | Craft epistemic types could be a small domain corpus. | The accepted decision selects `skill` first and leaves its exact slice open. | medium | **Misinterpretation:** keep `skill` first; Craft may be a secondary comparison, not an implicit reorder. |

## Supported conclusions

- The strongest safe hypothesis is a typed graph in which schema-for and instance-of are relative
  roles while the participating records retain explicit kinds and authority boundaries.
- A chain of exact schema references or meta-references does not by itself establish conformance;
  conformance must remain scoped to evidence such as a validation report.
- The first skill witness can exercise a skill schema revision under a metaschema and a skill
  instance under that schema without claiming deep instantiation or self-hosting.
- The literature search must be comparative. `Clabject`, potency, and deep instantiation are
  candidates to test, not baseline vocabulary.

## Claims deliberately not accepted

- `conformsTo` is transitive or means the same thing at each meta-depth.
- The architecture has global levels or exactly one schema per level.
- The metaschema's well-formedness guarantees semantic adequacy, satisfiability, publication, or
  enforcement authority.
- The regress is solved by either a kernel or self-hosting.
- Multilevel modeling is necessary for the Schema Service.

## One-line answer

Improve the research by replacing the assumed tower with discriminating questions over typed
relations, concrete validation targets, competing metamodeling architectures, and explicit closure
obligations; keep `skill-first` as the operational witness.

