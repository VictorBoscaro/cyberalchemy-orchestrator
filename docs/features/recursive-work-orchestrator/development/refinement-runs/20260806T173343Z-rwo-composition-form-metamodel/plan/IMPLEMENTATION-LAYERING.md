# Composition Form Source Contract — Implementation Layering

Status: non-executed validation-first remediation plan  
Complexity: high  
Evidence prerequisite: Candidate-2 `authored-complete`; `design-validator-pass` absent

## Dependency rule

Higher layers consume only exact passing receipts from earlier layers. Owner choices cannot be filled by defaults. Compiler/schema evidence cannot promote ontology or authorize runtime use.

```text
L0 disjoint compilation-result proof
  -> L1 owner decisions and exact form schemas
  -> L2 serialized fixtures and deterministic compiler/validator
  -> L3 runtime and external-owner boundary harness
  -> L4 ontology migration candidate and independent review
```

## L0 — Result-contract proof

Decision question: after L0, do we know that compilation success and rejection are structurally disjoint and bind distinct byte domains without implying runtime state or authority?

Minimum unit: schemas and golden vectors for `CompilerProfile`, `CompilationSuccess`, `CompilationRejection`, and `FormCompilationDefect`. No form payload, compiler, runtime, ontology, or owner decision is changed.

Exit evidence: unknown fields reject; success requires one graph and zero defects; rejection requires non-empty defects and forbids graph; raw/canonical/output byte domains are distinct; deterministic schema/golden validation receipt passes.

## L1 — Owner decisions and source schemas

Decision question: after L1, can every existing form subtype be serialized with one closed, owner-approved field set?

First obtain explicit decisions for Sequence cardinality, quorum, late arrival, journal truth/reducer compatibility, typed external reference shapes, provenance, and optional `FormOccurrence`. Then materialize closed common metadata and seven subtype payload schemas using existing selector/mapping/release/lifecycle/graph/authority owners.

Exit evidence: one owner receipt per blocked semantic; unknown/generic conditions, policies, references, and extension bags reject; one minimal valid/negative structural fixture per subtype passes.

## L2 — Compiler and finite evidence

Decision question: after L2, does the candidate compile exact serialized sources deterministically and reject every structural negative without side effects?

Materialize the 28-case plan as exact bytes plus additional golden cases, implement canonical desugaring to `WorkGraph`, run identical recompilation, and bind source/dependency/profile/output digests and byte sizes.

Exit evidence: nested all-seven golden passes; same inputs yield byte-identical graph/result; each negative has one defect and no forbidden mutation; receipt binds all bytes and commands.

## L3 — Runtime and external-owner boundaries

Decision question: after L3, can the reducer consume accepted structural history without collapsing journal, recovery, admission, authority, reasoning, or effect ownership?

Add runtime-only fixtures for no-match, stale attempts, frozen join, late arrival, Gate mismatch/corruption, Sidecar failure, repeat exhaustion, redelivery, retry, replay, ARE misuse, and uncertain effects. Integrate only owner-approved typed references.

Exit evidence: runtime fixture receipts prove permitted evidence retention and forbidden control mutation; replay is zero-external-call; owner substitution negatives fail closed.

## L4 — Ontology candidate and migration review

Decision question: after L4, is the smallest source-backed ontology migration acceptable to the ontology owner without changing authority or promotion semantics?

Resolve current `0.1.0`/`0.2.0` identity divergence first. Propose only non-aliased compilation-result/profile/defect concepts, relation repair, per-form closed properties, queries, shields, fixtures, and provenance. Regenerate projections only after semantic-source owner acceptance.

Exit evidence: ontology source and machine identity agree; generators/validators and negative controls pass; independent owner receipt explicitly decides migration/promotion. Passing validation alone remains non-authoritative.

## Non-regression

Every layer must preserve: one root orchestrator, typed explicit graph, existing owner boundaries, no generic evaluator/reference engine, no external calls during compilation/replay, distinct retry/repeat/replay/effect identities, and `authority_effect: none` for candidate artifacts.

## Recommended next layer

L0 is the narrowest reversible trust-building unit. It proves the result boundary without deciding form semantics or touching runtime/ontology sources.
