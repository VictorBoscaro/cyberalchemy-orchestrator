# Ontology owner route request

Status: selected direction; protected owner gate required  
Decision: `DG-RWO-CFM-004`  
Selected option: `ONTOLOGY-ROLLFORWARD-0.2`

## Requested disposition

The repository owner selected roll-forward toward `rwo-architecture@0.2.0`. The ontology identity and promotion owner must separately decide whether to admit a staged migration that:

1. treats `ONTOLOGY.md` version `0.2.0` as the candidate semantic source;
2. generates, rather than hand-patches, a staged `0.2.0` machine ontology;
3. preserves `0.1.0` source identities and receipts as immutable historical evidence;
4. binds semantic source, generator, schema, byte domains, sizes, and digests;
5. regenerates candidate nodes, relations, views, examples, evidence bindings, and negative fixtures;
6. proves roll-forward and rollback without silently reinterpreting earlier receipts; and
7. replaces canonical machine/projection bytes only after exact validation and owner acceptance.

## Current evidence

- `ontology/ONTOLOGY.md` declares `rwo-architecture@0.2.0`, draft and proposal-only.
- `ontology/ontology.json` declares `rwo-architecture@0.1.0`.
- `ontology/nodes/nodes.json` is package `rwo.current-state-graph@0.1.0` but references ontology `0.2.0`.
- The graph validator passes.
- The main ontology validator fails the pinned `source:candidate-ontology` digest.
- The ontology folder was Git-clean when the Decision Gate inspected it, so this is tracked package drift rather than an uncommitted local edit.

## Non-effects

This request is not an owner-gate receipt. It does not authorize generation, ontology mutation, projection replacement, promotion, publication, implementation, release, deployment, or production use.
