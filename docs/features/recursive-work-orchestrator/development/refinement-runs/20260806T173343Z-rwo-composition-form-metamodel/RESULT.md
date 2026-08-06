# RWO composition-form metamodel refine result

Status: ten-stage Refine complete with a constrained candidate verdict.

## Result

The exact model is smaller than the seed proposal:

- Keep the existing seven `CompositionForm` subtypes; do not create a parallel `FormDefinition` taxonomy.
- Treat an authored form as immutable source syntax inside one `CompositeWorkDefinition`.
- Use closed, subtype-specific operand fields; do not add a universal operand union.
- Reuse `EventSelector`, `InputMapping`, `ReleasePolicy`, and `SidecarLifecyclePolicy`.
- Do not create a generic condition/evaluator language. Domain, recovery, admission, authority, ARE/ACI, budget, journal, and effect concerns enter only through exact typed references to their existing owners.
- Keep `ExplicitComposition` as source syntax.
- Compile to `WorkGraph` through disjoint `CompilationSuccess` or `CompilationRejection`; compiler defects are structural only.
- Keep redelivery, Work retry, bounded repeat, domain rework, replay/resume, recovery classification, and effect reconciliation as different mechanisms with different identities and owners.

The optional `FormOccurrence` survives only as a compile-time diagnostic identity when an embedded source path is insufficient. It is never a `WorkNode`, run, attempt, repeat round, or runtime form instance.

## Ontology integration

The minimal candidate delta is:

- optional compile-only `FormOccurrence`;
- immutable non-authorizing `CompilerProfile`;
- disjoint `CompilationSuccess` and `CompilationRejection`;
- compiler-owned `FormCompilationDefect`;
- repaired success-mediated `compiles-to` lineage and separate rejection lineage.

Existing form, selector, mapping, release, lifecycle, graph, work-reference, and authority relations are reused. Generic condition, evaluator, policy, and external-reference nodes are rejected as aliases or owner collapse.

This delta was not applied. Ontology identity/migration and exact owner schemas are open, and the current ontology validator has a pinned candidate-ontology source-digest mismatch.

## Validation posture

The nine-agent research pipeline completed. The three reviewers forced one synthesis repair, and the auditor forced one bounded writer repair. The final findings include the missing quorum schedules, separate domain-rework/recovery cases, forbidden-owner predicates, split stale-version and digest failures, and exact missing-reference fixtures.

The 28-row scenario matrix and expanded fixture contract are planned and unexecuted. They do not prove non-vacuity, compiler behavior, runtime behavior, ontology migration, or conformance.

## Final gate

Definition/design candidate: PASS.  
Findings and validation-first planning: READY.  
Execution-entry plan: FLAG / BLOCKED.  
Adoption, implementation, ontology mutation, conformance, promotion, deployment, release, and production: BLOCKED, UNSUPPORTED, or NOT AUTHORIZED.

The next safe move is an owner-decision pass followed by an Invoke Plan refresh that selects one narrow validation unit. No Task Session or mutation route is admitted by this result.
