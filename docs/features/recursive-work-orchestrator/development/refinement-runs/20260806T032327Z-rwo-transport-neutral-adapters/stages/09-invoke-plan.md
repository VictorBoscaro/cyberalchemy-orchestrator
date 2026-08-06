# Stage 09 — Invoke Plan

Capability: `invoke`  
Mode: `plan`  
Plan kind: validation-first remediation  
Execution status: NOT STARTED

## Planning Decision

Candidate-2 is `authored-complete`, not `design-validator-pass`. A normal
runtime implementation plan would overstate the evidence. This stage therefore
plans only the shortest path to executable design evidence and owner decisions.
Transport adapters, runtime integration, ontology promotion, and production
admission remain later gated work.

## Selected Planning Unit

The smallest coherent future unit is:

```text
closed candidate schemas
  + positive/negative fixtures
  + deterministic candidate validator
  + exact validation receipt
```

That unit can falsify message identity, observations, manifests,
requirements, admission tuples, and retry/recovery distinctions without
sending messages or granting authority.

## Planned Sequence

1. materialize candidate-only schemas and closed vocabularies;
2. encode the Stage 08 scenario matrix as fixtures;
3. build a deterministic offline validator and zero-call replay spy;
4. run fixture, mutation, and schema-closure tests;
5. obtain G1–G3 owner decisions and update the design candidate;
6. rerun independent design validation;
7. only after `design-validator-pass`, propose ontology promotion and one
   reference in-memory adapter as separately authorized work.

## Gating

| Gate | Required evidence | Failure action |
| --- | --- | --- |
| V1 schema closure | unknown fields/atoms rejected | repair candidate schemas |
| V2 identity | canonical digest and duplicate fixtures pass | block |
| V3 observation safety | no observation implies journal/Work/effect truth | block |
| V4 admission binding | stale/mismatched tuples fail | block |
| V5 recovery separation | replay zero-call; unknown effect selects reconcile | block |
| G1–G3 owners | signed decisions/receipts from journal/domain, effect, ARE/ACI owners | stop and hand off |
| G4 ontology | ontology-owner review after design validation | no ontology mutation |
| G5 adapter | exact implementation/config receipt | no runtime admission |

## Non-Execution Statement

No SWU is selected or admitted. No schema, fixture, validator, adapter, runtime,
ontology, definition, ARE/ACI route, effect integration, or external transport
is changed or executed by this plan.

Detailed dependency layering is in `plan/IMPLEMENTATION-LAYERING.md`; bounded
future tasks and acceptance criteria are in `plan/WORK-PACK.md`.

