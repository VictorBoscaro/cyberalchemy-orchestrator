# Refine seed proposal — RWO composition-form conditions and metamodel

Status: confirmed research seed; candidate-only; not an accepted design or ontology mutation.

## Problem

RWO already names seven composition forms—`Sequence`, `FanOut`, `FanIn`, `Gate`, `Sidecar`, `BoundedRepeat`, and `ExplicitComposition`—and states that convenience forms compile to event-triggered edges. The design does not yet define one exact form envelope, operand roles, closed condition families, evaluator ownership, deterministic compilation receipt, or a complete validation and negative-control contract.

Without that layer, similar-looking words such as `all`, `approved`, `terminal`, `maxRounds`, `await`, or `retry` can silently cross owner boundaries. A boolean expression language would be compact, but it could let the kernel evaluate domain meaning, choose recovery, or manufacture authority. Seven unrelated schemas would preserve local meaning but lose a common compiler and inspection model.

## Candidate under test

`CompositionFormMetaModel@candidate-1` is initially hypothesized as a common closed envelope plus a discriminated family-specific payload:

```text
FormDefinition = {
  form_ref, form_kind, form_version,
  boundary_contract,
  operands: [OperandBinding...],
  conditions: [ConditionBinding...],
  policies: [PolicyRef...],
  limits,
  provenance
}

compile(FormDefinition)
  -> pass(ExplicitComposition, CompilationReceipt)
   | reject(FormValidationDefect[])
```

The candidate must prove that every convenience form desugars to the primitive graph without gaining domain, recovery, reasoning, or authority semantics.

## Condition families to refine

The starting families are deliberately separate and closed:

| Family | Question it may answer | Expected owner |
| --- | --- | --- |
| structural readiness | Are declared structural prerequisites present? | RWO compiler/runtime over accepted history |
| event selection | Does an accepted event match declared type/classification/payload structure? | event-contract owner plus RWO matcher |
| domain decision | What does the result mean in the domain? | gate or domain Work |
| route selection | Which declared edge corresponds to an accepted route label? | gate emits; RWO matches exactly one |
| lifecycle coupling | When is a companion started, awaited, detached, or cancellation-requested? | explicit sidecar policy; target Work owns response |
| boundedness | Is a finite round/budget/deadline ceiling still available? | definition/policy owner; journal owns atomic debit |
| recovery treatment | Redeliver, retry new Work Attempt, repeat round, reconcile effect, compensate, or stop? | accepted `RecoveryDecision`; never inferred by a form |
| authority/admission | May a command or external effect cross its boundary now? | authority/ACI/effect owners; form only carries references |

The run must decide whether these are all `Condition` subtypes, whether some are references to decisions rather than evaluable predicates, and which may legally affect compilation versus runtime routing.

## Forms that must receive exact schemas

1. `Sequence`: predecessor/source, selected release event, successor/target, input mapping, authority requirement.
2. `FanOut`: source release, non-empty keyed branches, per-branch mapping and admission requirements; no independence or equal-authority inference.
3. `FanIn`: keyed sources, canonical input ordering, closed structural release policy (`all`, `any`, `quorum(n)`), join Work, late-arrival policy; semantic reconciliation remains in join Work.
4. `Gate`: decision Work, closed route-label set, exactly one edge per label, explicit unmatched/ambiguous rejection; RWO never evaluates approval.
5. `Sidecar`: primary, companions, start trigger, observation selectors, finish behavior, output contribution; no implicit control over the primary.
6. `BoundedRepeat`: body, decision Work, continue/stop labels, strict positive bound or budget reference, round identity, exhaustion route; distinct from delivery redelivery and Work retry.
7. `ExplicitComposition`: typed nodes, event-triggered edges, boundary input/output mappings, graph constraints, and no convenience-form residue after compilation.

## Candidate comparisons

| Candidate | Strength | Failure risk |
| --- | --- | --- |
| universal boolean expression tree | one evaluator and compact serialization | collapses structural fact, domain meaning, recovery, and authority |
| seven unrelated form schemas | strong local typing | duplicates identity, provenance, compilation, and validation mechanics |
| common envelope plus closed typed families | common tooling with owner-preserving semantics | needs explicit admissible-family matrix and strict extension/version rules |

The third candidate is preferred only if finite witnesses prove it does not become a disguised universal policy engine.

## Required output

- exact common and per-form data model;
- operand-role and condition-family taxonomy;
- admissible-condition matrix by form and phase;
- evaluator and state-owner map;
- deterministic desugaring rules and compilation receipt;
- validation defects, invariants, positive fixtures, and discriminating negative controls;
- candidate ontology nodes, relations, constraints, and prohibited relations;
- compatibility/versioning and extension posture;
- non-executed, dependency-ordered Work Pack;
- explicit residue and owner gates.

## Claim ceiling and forbidden mutations

This run may produce candidate-local research, design, ontology delta, fixtures, and a plan. It may not edit `DESIGN.md`, `ontology/`, implementations, `cyberAlchemy-v2/`, definitions, authority state, Inventory, deployment, release, or production state. Passing internal validation is not implementation, promotion, or runtime proof.
