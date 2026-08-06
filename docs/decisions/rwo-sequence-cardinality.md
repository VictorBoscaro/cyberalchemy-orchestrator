---
status: accepted
date: 2026-08-06
scope: recursive-work-orchestrator-composition-forms
decision_id: DG-RWO-CFM-001
selected_option: SEQ-NARY-MIN2
---

# RWO Sequence cardinality

## Decision

An authored RWO `Sequence` is an ordered N-ary collection containing at least two `WorkDefinitionRef` steps.

```text
SequencePayload {
  steps: OrderedList<WorkDefinitionRef>  // minItems = 2
  adjacent_transitions: OrderedList<{
    event_selector_ref: EventSelectorRef
    input_mapping_ref: InputMappingRef
  }>
}

adjacent_transitions.length == steps.length - 1
transition[i] connects steps[i] to steps[i + 1]
```

Compilation emits one ordinary event-triggered edge for every adjacent pair. A Sequence containing `N` steps therefore emits `N - 1` edges. A singleton or empty Sequence is invalid; callers use the underlying Work directly instead of an identity/no-op Sequence.

## Rationale

This reconciles the variadic public API `sequence(work...)` with the binary predecessor-to-successor primitive described by `sequence(A, B)`. It keeps authored source compact, avoids artificial nested Sequence identities, and reduces parsing, validation, serialization, hashing, diagnostic-path, and compilation overhead while leaving the compiled runtime graph unchanged.

The rejected binary-only alternative would require nested source objects and an additional associativity or flattening rule for longer chains. Singleton and empty variants have no current owner-defined identity or unit-Work semantics.

## Authority boundary

This decision settles authored Sequence cardinality and adjacency only. It does not authorize schema, design, ontology, implementation, generated-projection, promotion, release, deployment, or production mutation. It does not decide event meaning, authority, retry, quorum, late-arrival, journal acceptance, or runtime conformance.

## Source and consequences

- Source design: `docs/features/recursive-work-orchestrator/DESIGN.md` §5 and §5.1.
- Refined candidate: `docs/features/recursive-work-orchestrator/development/refinement-runs/20260806T173343Z-rwo-composition-form-metamodel/delegated-research/findings.md` under “Seven closed payloads”.
- Admissibility receipt: `docs/features/recursive-work-orchestrator/development/decision-gates/20260806T203541Z-composition-form-owners/receipts/DG-RWO-CFM-001-option-admissibility.json`.
- Decision source: repository owner selected option `SEQ-NARY-MIN2` in the active 2026-08-06 Decision Gate.

Future candidate schemas and fixtures may cite this record for `minItems = 2` and the `N - 1` adjacency invariant. All remaining composition-form owner decisions and execution gates remain independent blockers.
