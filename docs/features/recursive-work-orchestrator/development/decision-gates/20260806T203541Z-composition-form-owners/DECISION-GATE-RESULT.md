# RWO composition-form Decision Gate result

Status: `BLOCK` for consequential mutation  
Decision selections: 6 of 6 complete  
Protected owner blockers: 1

## Resolved choices

| Decision | Selected option | Durable artifact | Effect |
|---|---|---|---|
| Sequence cardinality | `SEQ-NARY-MIN2` | `docs/decisions/rwo-sequence-cardinality.md` | N-ary authored list, minimum two, `N - 1` adjacency invariant |
| Structural quorum | `QUORUM-RWO-STRUCTURAL` | `docs/decisions/rwo-structural-quorum-ownership.md` | Distinct accepted-source count with `1 <= n <= source_count` |
| FanIn late arrival | `LATE-RETAIN-NONCONTRIBUTING` | `docs/decisions/rwo-fanin-late-arrival.md` | Retain accepted evidence; never reopen or rewrite release |
| Ontology identity | `ONTOLOGY-ROLLFORWARD-0.2` | `ONTOLOGY-OWNER-ROUTE-REQUEST.md` | Direction selected; protected owner route unsatisfied |
| Authored provenance | `PROVENANCE-EMBEDDED-SELECTORS` | `docs/decisions/rwo-authored-form-provenance.md` | Self-contained immutable source bindings |
| Form occurrence | `OCCURRENCE-OMIT-USE-SOURCE-PATH` | `docs/decisions/rwo-form-occurrence-omission.md` | No occurrence node; exact canonical path on results/defects |

## Remaining blocker

`ONTOLOGY-ROLLFORWARD-0.2` is a protected ontology identity/promotion route. The selection does not authorize generation or mutation. Consequential work remains blocked until the RWO ontology identity and promotion owner supplies a current, typed receipt admitting the exact staged migration scope.

## Direct owner prerequisites

These are not unresolved preference questions, but they continue to block their applicable downstream schemas or runtime work:

- exact journal truth, reducer compatibility, and replay-migration contract;
- exact authority, recovery, budget, journal-acceptance, ARE, ACI, artifact-admission, and exact-effect reference schemas;
- serialized fixture bytes and digest-bound expected results;
- admitted compiler/validator and runtime-conformance task contracts.

## Non-effects

No source design, ontology, machine projection, schema, implementation, Inventory, authority, promotion, publication, release, deployment, production system, Git commit, or remote was mutated by this Decision Gate. Accepted decision records authorize only the choices they state.
