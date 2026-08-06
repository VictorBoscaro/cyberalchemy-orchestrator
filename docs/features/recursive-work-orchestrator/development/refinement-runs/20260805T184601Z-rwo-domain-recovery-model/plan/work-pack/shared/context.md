# Shared Context

## Objective

Turn `RecoveryDecisionContract@candidate-2` into separately testable layers
without collapsing domain meaning, accepted history, ARE evidence, lifecycle
routing, authority, or exact-effect ownership.

## Source Anchors

- Repaired exact model: `../../../stages/08-distill-repair.md`
- Scenario matrix: `../../../stages/08-scenario-matrix.json`
- Adversarial evidence: `../../../stages/subagents/recovery-model-adversary.md`
- Current RWO design: `../../../../../../DESIGN.md`
- Existing canonical profile: `implementations/server/runtime/canonical.py`
- Existing atomic journal: `implementations/server/runtime/journal.py`
- Existing persistence owner: `implementations/server/runtime/database.py` and `schema.sql`
- Current ontology: `docs/features/recursive-work-orchestrator/ontology/`

## Invariants

1. One stable trigger releases at most one accepted treatment.
2. RecoveryFrontier arbitrates overlapping case kinds before classification.
3. Work, delivery, effect, reconciliation, compensation, and run identities do
   not substitute for one another.
4. Missing owners and unknown facts fail closed.
5. Every decision is non-authorizing and must be atomically accepted.
6. Runtime resume reconstructs only; replay has zero mutable/external calls.

## Claim Ceiling

Planning and later candidate implementation do not prove owner acceptance,
ontology promotion, deployment, pilot readiness, release, or production use.

