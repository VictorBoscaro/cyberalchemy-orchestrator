# Stage 05 — Distill: Exact Recovery Decision Unit

## Distill Result

- Target context: RWO recovery semantics spanning domain interpretation,
  lifecycle routing, accepted history, ARE evidence, and effect uncertainty
- Objective and output artifact: select the smallest coherent design unit that
  can yield one exact recovery model in s06
- Mode and budget: `standard`; one proposal track, two recursive rounds, one reconciliation pass
- Proposal tracks: 1; labeled parent-native Proposer and Balancer passes
- Recursive rounds: 2 / 2
- Verdict: `pass`
- Current smallest coherent unit: `RecoveryDecisionContract`
- Next route: `invoke design`

The approved route permits one helper only after s06, so Distill did not spawn
additional Proposer/Balancer agents. The same role trace is preserved below.

## Discovery Baseline

### Evidence-backed facts

- WorkDefinition is immutable/versioned; a WorkRun may have several Attempts
  without changing definition, graph, or authority basis.
- At-least-once message delivery requires stable idempotency and does not imply
  exactly-once business effects.
- BoundedRepeat requires a bound, decision work, and exhaustion route.
- Accepted journal history, orchestration cursor, and domain state are distinct.
- Stale observations are retained but cannot release current routes.
- Replay is historical and side-effect-free; current revalidation is a new run.
- ARE semantic evaluation, ACI acceptance, artifact admission, exact-effect
  authority, and adapter evidence are separate boundaries.

### Required repairs from s03

- discriminated case variants;
- runtime resume separated from ordinary failure interpretation;
- logical delivery attempt separated from Work Attempt;
- three-tier classification instead of one untyped global list;
- new-run selection as proposal, not authority;
- closed quarantine and terminal reason codes;
- admitted ARE receipt only through domain mapping;
- current fence/sameness/budget evidence before a new Attempt.

### Blocker unknowns

None for candidate design. Missing exact-effect/reconciliation owners and ARE
conformance must be represented as typed blocks.

## Broadest Concept Layer

`RWO Recovery Architecture` is the broad layer. It contains message delivery,
work lifecycle, repeat policy, restart/resume, domain interpretation, semantic
evaluation, effect reconciliation, compensation, persistence, and operator
escalation. Designing all of those implementations as one unit would collapse
owners and overbuild the kernel.

## Round 1

### Proposer claim

Select a `RecoveryClassifier` with a discriminated `RecoveryCase` union. Give
each case kind a decision table and return one `RecoveryDisposition`.

Evidence/assumption:

- The s03 review shows a flat case permits impossible state combinations.
- The current RWO design requires single-valued routes and fail-closed unknowns.
- Assumption: a closed case union can evolve by versioning rather than an open
  fallback variant.

### Balancer objections

| Category | Objection |
| --- | --- |
| responsibility closure | A classifier alone does not own the input completeness contract or output receipt semantics. |
| hidden glue | Domain signal, policy, history cut, and fences would need undocumented assembly. |
| abstraction mismatch | Runtime resume must occur before ordinary case construction, while a case union suggests peer alternatives. |
| authority boundary | Returning a disposition without an explicit non-authorizing decision receipt invites direct execution. |

### Reconciliation

`revise`. The unit must include the case contract, assembly boundary, policy
reference, staged classifier, and decision receipt. Runtime resume is a
pre-classification guard with a separately typed `RuntimeResumeCase`.

## Round 2

### Proposer claim

Select `RecoveryDecisionContract`:

```text
domain-owned RecoveryMapping -> DomainRecoverySignal
verified history/fences + trusted observations + policy
  -> RecoveryCaseUnion
  -> staged deterministic RecoveryClassifier
  -> non-authorizing RecoveryDecision receipt
```

The contract has four internal parts:

1. shared case header and closed case variants;
2. canonical assembly/validation rules;
3. common guards plus one table per case kind plus emission guards;
4. decision receipt with exact identity transition and next owner.

Boundary inputs remain owner-held: RecoveryMapping, domain-state/semantic
references, AcceptedHistorySlice, fences, authority/effect receipts, and
RecoveryPolicy publication.

### Balancer objections

| Category | Objection | Resolution |
| --- | --- | --- |
| cognitive load | Twelve dispositions plus reason codes may be too much. | Reject reduction: each has a different identity/routing effect and collapsing them loses safety. Present them through a decision matrix. |
| requisite variety | Delivery, execution, repeat, runtime, effect, cancellation, and conflict cases need different mandatory fields. | Accept: closed discriminated variants with `additionalProperties: false` and total validation. |
| boundary object | Domain and effect owners need a stable cross-boundary object. | Accept: DomainRecoverySignal and RecoveryDecision are the two boundary objects; neither grants authority. |
| concept-vs-knowledge | Exact names are not canonical definitions. | Accept: label the complete design candidate-local and versioned. |
| premature scale | A generic rule DSL or plugin engine would be elegant. | Defer: one explicit ordered table is sufficient until variation pressure is observed. |

### Reconciliation

`accept` the revised unit. No smaller unit closes responsibility, because:

- case schema without classifier cannot select a treatment;
- classifier without case assembly admits impossible/unknown state;
- decision enum without receipt cannot bind evidence and identity transitions;
- embedding domain mapping or effect execution would exceed the unit's owner.

## Current Smallest Coherent Unit

### Name

`RecoveryDecisionContract@candidate-1`

### Responsibility

Given one valid, immutable recovery case assembled from separately owned
evidence and one versioned policy, deterministically produce one
non-authorizing recovery decision or fail closed.

### Inputs

- trusted structural observation and subject identities;
- domain-owned `DomainRecoverySignal` where the case kind requires it;
- verified `AcceptedHistorySlice` and current fences;
- versioned `RecoveryPolicy`;
- accepted authority/effect/semantic references only where required.

### Outputs

- exactly one `RecoveryDecision`, including disposition, closed reason code,
  identity transition, budget/fence consequences, required next owner, and
  complete evidence/version digests;
- or schema/admission rejection before classification.

### Abstraction Level

Design-level decision contract between owner-held meaning/evidence and ordinary
RWO route scheduling. It is not an executor, journal, reasoner, or authority gate.

## Rejected Alternatives

| Alternative | Verdict | Elimination condition |
| --- | --- | --- |
| flat RecoveryCase + one global precedence list | reject | permits impossible cross-family combinations and compares unrelated protocol layers |
| domain-owned recovery policy selects retry route | kill | collapses domain meaning into WorkRun/Attempt scheduling |
| ARE decides recovery disposition | kill | collapses semantic reasoning into lifecycle routing and possibly effect authority |
| adapter-specific recovery state machines only | reject | cannot guarantee common run/attempt/round identities, fences, budgets, and replay semantics |
| generic rule DSL/plugin engine | defer | no observed variation requires executable extensibility; adds interpretation and versioning risk |
| disposition-only enum without case/receipt contracts | reject | cannot prove determinism, evidence binding, or identity effects |
| model compensation as rollback | kill | contradicts explicit compensation Work and honest external-effect uncertainty |

## Concept Layer Map

```text
RWO Recovery Architecture
  -> Domain/RWO/Journal/ARE/ACI/Effect ownership seams
    -> Recovery decision boundary
      -> RecoveryDecisionContract
        -> Case union
        -> Assembly/admission rules
        -> Staged classifier tables
        -> Decision receipt
```

## Technique Pack Trace

| Technique | Trigger / inspected state | Output and decision | Readiness effect |
| --- | --- | --- | --- |
| abstraction-level guard | target crossed architecture, domain, runtime, and effect layers | selected a design contract, not an implementation subsystem | pass |
| recomposition proof | unit must fit current RWO | decision receipt feeds the existing route evaluator; owners remain outside | pass |
| evolution profile | domains/policies will vary | version case/policy/mapping; defer generic DSL | pass |
| frame-expiry note | owner/schema decisions may change | expiry conditions listed below | pass |
| navigable result check | s06 needs a concrete start point | start with case union, then tables, then owner matrix/fixtures | pass |
| cognitive load check | 12 dispositions | keep because identity effects differ; require matrix | pass |
| requisite variety check | seven case families | closed discriminated union selected | pass |
| boundary-object check | domain-to-RWO and RWO-to-route seams | DomainRecoverySignal and RecoveryDecision selected | pass |
| concept-vs-knowledge status | names are newly authored | candidate-local labels only | pass |
| premortem | unsafe retry can duplicate effects | guard unknown effect before ordinary retry and require negative fixture | pass |
| set-based tournament | one standard track only | skipped; s06 dispatch already supplies model alternative comparison | no downgrade |

## Closure And Recomposition Proof

The unit closes because it owns one behavior: structural recovery selection.
Its inputs and outputs are named, invalid input blocks before selection, and
the decision is evidence-bound. It recomposes upward as follows:

1. existing work adapters and domains emit accepted facts;
2. owner-held mapping/history/policy boundaries assemble a case;
3. the selected unit emits a non-authorizing decision;
4. existing RWO route/command machinery proposes the named next action;
5. ACI, authority, effect, and adapter owners independently accept or reject it.

No hidden component is required to reinterpret the decision. Actual case
assembly, persistence, adapters, and owner gates are future implementation
components with explicit interfaces.

## Evolution Profile

Expected evolution is new domain signal types, new policy versions, and more
reason codes—not arbitrary new lifecycle effects. The smallest extension
boundary is versioned tables and schema unions. Adding a disposition requires
a design/ontology migration because it changes identity/routing semantics.

## Deferred Complexity

- executable policy DSL;
- pluggable classifier engine;
- cross-host locking implementation;
- generic effect reconciliation adapters;
- runtime ARE integration;
- automatic ontology generation or promotion;
- dynamic graph/topology extension.

## Tension Ledger

- Resolved: flat versus discriminated case shape.
- Resolved: runtime resume precedes ordinary case evaluation.
- Resolved: domain signal versus RWO disposition ownership.
- Resolved: new-run decision is not entry authorization.
- Stable residue: journal/domain source-of-truth ownership.
- Stable residue: exact-effect/reconciliation owner and accepted schemas.
- Stable residue: executable ARE/ACI compatibility and conformance.

## Premortem

Most likely failure: a caller treats `RETRY_NEW_ATTEMPT` or
`RECONCILE_UNKNOWN_EFFECT` as permission to issue an effect, bypassing ordinary
authority/ACI gates. Guardrail: RecoveryDecision is explicitly
`authority_effect:none`; fixtures assert zero adapter/effect calls before the
required owner receipts.

## Frame-Expiry Note

This optimization point expires if an owner adopts a materially different
WorkRun/Attempt identity model, the journal becomes authoritative domain state,
effect attempts receive an accepted idempotency/reconciliation contract that
changes outcome handling, or a promoted ARE/ACI integration reallocates the
current owner boundaries. Those changes require revalidation, not replay of
this design.

## Navigation Guide

Start s06 with the shared header and seven case variants. Then define common
guards, per-case tables, emission guards, disposition/reason matrices, owner
interfaces, and negative fixtures. Keep all missing owners as explicit
`ESCALATE_OWNER`/blocked routes. Do not begin with ontology nodes or runtime code.

## Evidence Emission And Telemetry

- Evidence emission: `not-required`; no accepted Distill runtime-event ledger was supplied.
- Telemetry: prepared for Refine closeout inside the run folder; not appended outside the confirmed write scope.

