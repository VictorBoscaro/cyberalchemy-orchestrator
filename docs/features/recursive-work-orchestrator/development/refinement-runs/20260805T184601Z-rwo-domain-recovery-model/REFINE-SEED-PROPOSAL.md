# Refine Seed Proposal: RWO Domain Recovery Model

Status: strategy proposed; execution not authorized  
Run ID: `20260805T184601Z-rwo-domain-recovery-model`  
Preset: `full`  
Research mode: `research-if-gap-appears`  
Target: `docs/features/recursive-work-orchestrator/`

## Operator Intent

Refine the current retry and recovery ideas into an exact model for how a
domain describes failure situations, how RWO identifies the appropriate
treatment, and how that treatment remains separate from ARE semantic reasoning
and exact-effect authority.

## Current Evidence Boundary

The run starts from these local sources:

- `DESIGN.md`: proposed WorkDefinition, WorkRun, Attempt, BoundedRepeat,
  journal, delivery, replay, stale-attempt, and compensation semantics.
- `ontology/ONTOLOGY.md` and the materialized graph: the accepted current-state
  explanatory model. The graph presently has no recovery-specific node family.
- `../../../../../../../../ops/development/2026-08-04-cyberalchemy-orchestrator-rwo-are-current-state-research/findings.md`:
  accepted research separating RWO coordination, ARE reasoning, ACI acceptance,
  and exact-effect boundaries.
- `../../../../../../../../cyberAlchemy-v2/development/agent-reasoning-engine/design/rwo-integration/ONTOLOGY-BRIDGE.md`:
  private, non-authoritative RWO-to-ARE bridge evidence. Its prose must not be
  copied into a public owner surface or treated as a runtime contract.
- `ontology/receipts/CURRENT-STATE-2026-08-05-VALIDATION.json`: graph validation
  receipt for the pre-refinement current-state projection.

These sources establish proposal and observation evidence, not implementation,
runtime compatibility, effect safety, authority selection, or promotion.

## Problem To Refine

The current design contains useful pieces but no single typed classifier that
can distinguish all of the following without collapsing their identities:

1. same-message redelivery;
2. a new Attempt under the same WorkRun;
3. a new bounded-repeat round;
4. current-state revalidation as a new WorkRun;
5. historical replay or restart/resume;
6. reconciliation of an external effect with an unknown outcome;
7. explicit compensation;
8. duplicate suppression, stale-observation handling, conflict quarantine,
   terminal exhaustion, and owner escalation.

The refinement must test, not assume, the candidate flow:

```text
DomainEvent
  -> domain-owned RecoveryMapping
  -> RecoveryCase
  + RecoveryPolicy
  + AcceptedHistory
  -> deterministic RecoveryClassifier
  -> RecoveryDisposition
```

Candidate names are hypotheses until the Refine loop accepts, repairs, or
rejects them.

## Exact-Model Questions

- Which identifiers distinguish delivery, command, WorkRun, Attempt, round,
  effect intent, and effect attempt?
- Which observations are facts, which are domain interpretations, and which
  are policy inputs?
- What is the closed disposition vocabulary, and what precedence makes one
  disposition deterministic?
- Which fields must be frozen for a retry to remain in the same WorkRun?
- Which changes force revalidation as a new WorkRun?
- How do attempt fences, idempotency keys, accepted history, budgets, and
  exhaustion routes interact?
- What does a domain own in `RecoveryMapping`, and what is it forbidden to
  decide about scheduling, authority, and effect safety?
- When may ARE classify semantic meaning, and why can ARE not decide lifecycle
  routing or exact-effect authorization?
- Which owner must reconcile an unknown external effect before any new attempt?
- How are late, duplicate, divergent, contradictory, or insufficient
  observations retained without becoming routing authority?

## Required Model Deliverables

The final synthesis is useful only if it includes all of these non-executed
design artifacts:

1. a glossary with exact identities and state scopes;
2. a closed recovery disposition algebra;
3. a typed `RecoveryCase`, `RecoveryPolicy`, `RecoveryMapping`, and classifier
   input/output contract;
4. deterministic precedence and fail-closed rules;
5. a state-transition model across message, run, attempt, repeat round, replay,
   and effect lifecycle;
6. an ownership and authority matrix covering domain, RWO, journal, ARE, ACI,
   exact-effect owner, adapter, and human/owner escalation;
7. invariants and forbidden topologies;
8. counterexample fixtures, including `payment.outcome-unknown`, lost delivery,
   divergent duplicate, stale attempt, transient provider timeout, domain
   rework, exhausted budget, restart/resume, and changed authority;
9. the delta against the current RWO design and ontology;
10. an implementation-ready but non-executed work plan and validation matrix.

## Candidate Classification Priority To Challenge

The stages must try to falsify this initial ordering:

1. divergent bytes under one idempotency identity -> quarantine conflict;
2. stale attempt/round observation -> retain, but ignore for routing;
3. process restart with accepted history -> resume from journal;
4. unknown external effect -> reconcile before another effect attempt;
5. changed definition, input, authority, or effect envelope -> new WorkRun;
6. domain-requested rework -> bounded-repeat round when policy permits;
7. command not accepted -> same-message redelivery when delivery policy permits;
8. known transient execution failure -> new Attempt when policy permits;
9. permanent failure or exhausted limits -> terminal stop;
10. insufficient or contradictory evidence -> owner escalation.

## Write Scope

During Refine, writes are limited to this run folder. Stage owners may write
their own artifacts beneath `stages/`. The one proposed adversarial helper may
write only `stages/subagents/recovery-model-adversary.md` and its receipt.

## Forbidden Scope

- `DESIGN.md` and all current ontology source, graph, schema, view, fixture, and
  receipt files;
- runtime code, tests, adapters, schemas, and journals;
- ARE, ACI, or exact-effect owner artifacts;
- canonical definitions, Inventory, publication, promotion, Git commits,
  pushes, deployments, and external effects.

## Done Criteria

- Every required deliverable above is present or has an explicit blocked owner
  and reason.
- Every disposition is distinguishable by input facts and has one allowed
  identity transition.
- The model never infers exactly-once business effects from at-least-once
  delivery.
- `payment.outcome-unknown` cannot route directly to automatic retry.
- Historical replay performs no mutable or external calls; current
  revalidation creates a new WorkRun.
- Domain semantics, RWO scheduling, journal truth, ARE reasoning, ACI
  acceptance, effect authorization, and adapter evidence remain separately
  owned.
- All counterexamples either select exactly one disposition or fail closed to
  an identified owner.
- The final plan names concrete future files and validation commands without
  executing the plan.

## Validation Surface

- Dispatch Spec schema and semantic validator for `REFINE-DISPATCH.json`.
- Ten native stage receipts or exact blocked reasons.
- Cross-artifact term and identifier consistency checks.
- Scenario decision-table coverage for every disposition and precedence rule.
- Negative controls for unsafe retry, stale routing, replay side effects,
  authority collapse, and changed-input reuse.
- Final Interrogation verdict before Refine synthesis.

## Planned Stage Configuration

The run uses the canonical ten-stage Refine loop with the `full` preset. It is
local-first. External research remains unavailable unless a stage names a
specific gap and the operator separately confirms one bounded pass.
