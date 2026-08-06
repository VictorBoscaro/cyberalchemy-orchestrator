# Refine Result: RWO Domain Recovery Model

Status: `pass`  
Model: `RecoveryDecisionContract@candidate-2`  
Evidence level: exact candidate design plus non-executed implementation plan

## Outcome

The recovery model is now exact within its candidate boundary. It can describe
one admitted recovery situation, prove which facts and owners are required,
select one closed structural treatment, state exactly which identities change,
and fail closed when evidence or ownership is missing. It does not grant
authority or perform the treatment.

The Stage 6 design was not accepted on first pass. The independent adversary
blocked it with 11 critical and 4 flagged findings. Stage 7 accepted every
substantive repair. Stage 8 produced candidate-2 and passed 20/20 deterministic
scenario games. Final Interrogation found and repaired two additional internal
consistency defects before this pass.

## Exact Architecture

```text
DomainEvent
  -> domain-owned, pure RecoveryMapping
  -> owner-admitted DomainRecoverySignalHandle

accepted structural records
  -> journal-owned RecoveryFrontier

signal + frontier + policy/deadline/authority/effect handles
  -> CaseAssembler: pass(RecoveryCase) | reject
  -> RecoveryClassifier
  -> RecoveryDecision(authority_effect:none)
  -> atomic journal/ACI compare-and-accept + trigger consumption
  -> ordinary RWO route
  -> independent entry/authority/ACI/effect gates
```

The case union has eight variants: conflict, owner gap, runtime resume,
delivery, execution, repeat, cancellation, and effect. The treatment vocabulary
has thirteen dispositions. Crucially, `RETRY_NEW_ATTEMPT` and
`RETRY_NEW_EFFECT_ATTEMPT` are different operations.

## Treatment Semantics

| Situation | Treatment | Identity rule |
| --- | --- | --- |
| same accepted duplicate | deduplicate or return prior accepted decision | allocate nothing |
| command known unaccepted | redeliver same logical message | preserve Work Attempt/message bytes/key; delivery attempt may change |
| transient terminal execution | retry new Work Attempt | preserve run/round; allocate exactly one Work Attempt |
| failed-known exact effect with permit | retry new effect attempt | preserve Work Attempt/effect intent; allocate exactly one effect attempt |
| domain rework | repeat new round | preserve containing run; allocate bounded round and later child attempts |
| definition/input/authority/effect envelope changed during an otherwise valid continuation | propose revalidation as new run | old run preserved; new run still needs ordinary entry gates |
| runtime restart | resume from journal | reconstruct cursor only; no route, debit, or delivery |
| stale fence | ignore for routing | retain evidence; allocate nothing |
| effect outcome unknown | reconcile or escalate/stop at bounded exhaustion | never retry Work or effect |
| declared compensation | propose correlated compensation Work | stable compensation intent and entry key; original facts preserved |
| trusted contradiction | quarantine conflict | no continuation route |
| terminal/canceled/exhausted | stop or declared escalation/compensation | exact reason; no permissive retry |
| required owner/input absent | owner-gap escalation or protocol rejection | no default owner/policy |

## Concurrency Rule

`RecoveryFrontier` selects at most one actionable trigger for an overlapping
subject scope. The accepted-history owner atomically checks the complete
DecisionValidationVector, consumes the stable trigger, debits counters,
allocates identities, appends the decision, and advances the frontier. If any
policy, mapping, deadline, authority, route, permit, fence, counter, or history
member changed, the whole transaction performs no mutation and the case is
rebuilt. Rebuilding is classification, not Work retry.

## Domain And ARE

The domain owns meaning through a versioned, deterministic RecoveryMapping. It
may report failure class, rework intent, compensation intent, and semantic
constraints. It cannot choose the structural case, disposition, route, budget,
WorkRun identity, or effect permission.

ARE is optional evidence only. Raw ARE output is never accepted. An ARE result
must pass its entry, ACI, and semantic/artifact admission chain before the
domain mapping may reference it. ARE never returns a recovery disposition or
authority verdict, and the model has a valid zero-ARE-call path.

## Validation

- Independent adversary: `block` on Stage 6, 15 findings, 11 repairs.
- Repaired scenario matrix: 20/20 pass.
- Final audit: 12/12 questions pass; 2 final consistency repairs applied.
- Plan validation: 10 atomic SWUs, 9 bounded automatic routes, disjoint scopes,
  canonical route digest, and complete closeout contracts.
- External research: not run; no named evidence gap required it.

## Implementation Plan

The split plan has four layers:

1. L0: canonical IDs, closed case admission, pure classifier, identity transitions.
2. L1: RecoveryFrontier and atomic journal acceptance.
3. L2: domain, exact-effect/reconciliation, and optional ARE/ACI conformance.
4. L3: evidence-backed ontology proposal through a separate owner decision.

The recommended first unit is `SWU-RRD-001`: reuse the current frozen
`aci.canonical-json@1` payload bytes, add RWO object-kind domain separation,
and prove byte-identical golden IDs. No SWU was selected or executed.

## Remaining Owner Gates

- G1: journal/domain truth reconciliation.
- G2: exact-effect permit and reconciliation schemas.
- G3: executable ARE/ACI semantic receipt conformance.
- G4: ontology/definitions promotion authority.

These do not make the candidate model ambiguous; they make later integrations
fail closed until their owners decide.

## Claim Ceiling

This run proves a coherent, adversarially repaired, candidate-local model and a
selection-ready plan. It does not prove implementation, owner adoption,
canonical definitions, ontology promotion, runtime integration, deployment,
pilot readiness, release, or production behavior. Current DESIGN.md, ontology,
runtime, ARE/ACI sources, Git, Inventory, and external systems were not mutated.
