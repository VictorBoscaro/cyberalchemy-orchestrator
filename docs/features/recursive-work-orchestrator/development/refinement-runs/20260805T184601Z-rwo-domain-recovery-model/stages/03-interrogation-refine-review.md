# Stage 03 — Interrogation `refine-review`

## Structured Interview Result

- Target scope: `stages/02-invoke-define.md`
- Mode: `refine-review`
- Human questions asked: 0
- Evidence-backed review questions evaluated: 10
- Decisions recorded: 8 repairs accepted, 2 boundaries retained as owner gaps
- Artifacts updated: none; repairs are handed to s05/s06
- Remaining ambiguities: journal/domain reconciliation ownership and exact-effect/reconciliation owner
- Verdict: `flag`
- Next step: s04 research decision, then s05 Distill repair selection

No human question was necessary. The highest-discrimination issues have safe,
evidence-backed fail-closed defaults. The two unresolved questions belong to
other owner routes and can be represented as explicit missing-owner states.

## Dialectic Roles

| Role | Governing concern |
| --- | --- |
| kernel-semantics | deterministic structural routing without domain meaning |
| domain-semantics | domain ownership of event meaning and recovery intent |
| effect-authority | effect uncertainty, authorization, attempt evidence, and reconciliation |

## Review Ledger

### Q1 — Can one flat RecoveryCase safely carry every state family?

- Kernel claim: a single record gives the classifier one deterministic input.
- Domain objection — category `requisite variety`: runtime restart, duplicate
  delivery, domain rework, execution failure, and effect uncertainty require
  different mandatory facts; a flat record permits impossible combinations.
- Effect objection: `effect=outcome_unknown` with no effect intent/attempt must
  be structurally impossible, not merely rejected by prose.
- Decision: **revise** to a closed discriminated union with a shared header and
  case-specific bodies: `DeliveryCase`, `ExecutionCase`, `RepeatCase`,
  `RuntimeResumeCase`, `EffectCase`, `CancellationCase`, and `ConflictCase`.
- Readiness effect: flag until s06 defines the union and total schema rules.

### Q2 — Is restart/resume comparable to retry precedence?

- Kernel claim: `RESUME_FROM_JOURNAL` can be the third disposition in one precedence list.
- Domain objection — category `abstraction mismatch`: restart is recovery of
  orchestrator projection state, not interpretation of a work failure.
- Decision: **revise**. Keep one disposition vocabulary for operator clarity,
  but apply staged classification: admission/conflict guard → runtime-resume
  guard → case-kind classifier. A runtime-resume decision completes before a
  new domain/effect case is built from the reconstructed cursor.
- Readiness effect: removes the collision between restart and unknown effect.

### Q3 — Does same-message redelivery preserve `message_id` as well as bytes/key?

- Kernel claim: yes; lost delivery resends the exact addressed envelope.
- Effect objection — category `boundary ambiguity`: an adapter may generate a
  transport-specific delivery-attempt identity without changing the logical message.
- Decision: **accept with precision**. Preserve logical `message_id`, payload
  bytes, causal envelope, run/attempt identities, and idempotency key. A
  transport receipt may carry a new `delivery_attempt_id`, which is not a Work Attempt.

### Q4 — When is a new Attempt allowed?

- Kernel claim: known transient failure plus remaining budget.
- Domain objection — category `missing precondition`: retryability must come
  from a versioned policy applied to a domain signal; an event name alone is insufficient.
- Decision: **revise**. Require: current fence, accepted terminal failure fact,
  same definition/input/authority/effect envelope, policy eligibility, open
  deadline, and remaining attempt budget. Any unknown becomes `ESCALATE_OWNER`.

### Q5 — Can changed authority select `REVALIDATE_NEW_RUN` automatically?

- Kernel claim: a changed authority basis forces a new run.
- Effect objection — category `authority inflation`: forcing a new identity is
  not permission to start it.
- Decision: **revise**. The disposition means “the old run cannot be reused;
  propose ordinary entry for a new run.” Fresh confirmation/authority/admission
  must independently pass before creation or delivery.

### Q6 — Can a domain request `COMPENSATE` directly?

- Domain claim: domain meaning should be able to request compensation.
- Effect objection — category `effect safety`: request is not an authorized compensation effect.
- Decision: **accept with boundary**. `DomainRecoverySignal` may set
  `compensation_intent=requested`. The classifier may select `COMPENSATE` only
  when a declared policy and compensation Work reference exist. The decision
  proposes a new compensation WorkRun through ordinary authority gates.

### Q7 — Is `QUARANTINE_CONFLICT` too broad?

- Kernel claim: one fail-closed conflict disposition simplifies routing.
- Domain objection — category `diagnostic loss`: divergent duplicate,
  contradictory trusted facts, invalid schema, and impossible transition have different owners.
- Decision: **retain disposition, split reason codes**. Closed reason codes are
  required: `DIVERGENT_IDEMPOTENCY_BYTES`, `CONTRADICTORY_TRUSTED_FACTS`,
  `INVALID_OR_UNKNOWN_CONTRACT`, and `IMPOSSIBLE_STATE_COMBINATION`.

### Q8 — Does `STOP_TERMINAL` hide exhaustion versus permanent outcome?

- Kernel claim: both schedule no further recovery work.
- Domain objection — category `semantic collapse`: operationally identical
  scheduling does not make the reasons equivalent.
- Decision: **retain disposition, split reason codes**:
  `PERMANENT_FAILURE`, `POLICY_DENIED`, `ATTEMPT_EXHAUSTED`, `ROUND_EXHAUSTED`,
  `DEADLINE_ELAPSED`, `CANCELLATION_TERMINAL`, and `ALREADY_SATISFIED`.
  The domain outcome remains in its owner event, not the RWO reason code.

### Q9 — May an ARE semantic receipt be embedded in RecoveryCase?

- Domain claim: some recovery meanings require semantic evaluation.
- Kernel objection — category `routing-as-reasoning`: an evaluator result must
  not become a route or authority verdict.
- Decision: **accept only as an admitted reference** inside
  `DomainRecoverySignal`. The signal records mapping logic and evidence; the
  classifier sees typed domain intent, not an unrestricted model conclusion.
  Missing entry/admission receipts produces `ESCALATE_OWNER`, not a fallback.

### Q10 — Is one global precedence list sufficient?

- Kernel claim: a single list is simple and deterministic.
- Domain objection — category `invalid comparison`: a delivery duplicate and a
  domain rework intent may coexist but are resolved at different protocol layers.
- Decision: **revise** to three ordered tiers:
  1. admission guards common to all cases;
  2. case-kind-specific decision table;
  3. cross-cutting limits/owner checks before emitting the selected decision.
  The final result is still single-valued and byte-deterministic.

## Required Repairs For Distill And Design

1. Define the discriminated `RecoveryCase` variants and illegal combinations.
2. Add logical `delivery_attempt_id` separately from Work `attempt_id`.
3. Split classification into common admission guards, runtime-resume guard,
   case decision table, and emission guards.
4. Make a new-run disposition a proposal to ordinary entry, not authorization.
5. Close quarantine and terminal reason-code vocabularies.
6. Require current fence, terminal attempt evidence, sameness, policy, deadline,
   and budget for `RETRY_NEW_ATTEMPT`.
7. Require declared policy and Work reference for compensation.
8. Permit only admitted semantic receipt references through domain mapping.

## Stable Owner Gaps

- `G1-JOURNAL-OWNERSHIP`: the candidate model must carry both accepted-history
  evidence and a domain source reference; it cannot choose which owns truth.
- `G2-EFFECT-OWNER`: missing reconciliation/exact-effect owner makes
  `EffectCase(outcome_unknown)` select `ESCALATE_OWNER` or a blocked
  `RECONCILE_UNKNOWN_EFFECT`, never retry.

## Verdict Basis

`flag`, not `block`: the definition is coherent enough to refine, every
critical ambiguity has a safe repair, and the two unselected owners can remain
typed blockers. It is not yet an exact design.

