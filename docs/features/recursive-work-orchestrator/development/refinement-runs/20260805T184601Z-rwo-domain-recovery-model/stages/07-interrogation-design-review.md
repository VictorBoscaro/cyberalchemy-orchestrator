# Stage 07 — Interrogation `refine-design-review`

## Interrogation Result

- Target: `stages/06-invoke-design.md`
- Mode: `refine-design-review`
- Independent challenger: `recovery-model-adversary`
- Adversary receipt: `stages/subagents/recovery-model-adversary.receipt.json`
- Independent findings: 11 block, 4 flag
- Parent traceability findings: 1 flag
- Accepted repairs: 12
- Rejected findings: 0
- Verdict: `block`
- Next route: Stage 08 Distill repair and concrete game validation

The architecture thesis survives: domains own meaning, the RWO recovery
contract owns structural treatment selection, accepted history owns durable
facts, and authority/effect owners remain independent. The Stage 6 contract
does not yet survive concurrency and identity falsification, so it cannot be
called exact or handed to implementation unchanged.

## Review Method

The parent checked each adversarial counterexample against the Stage 6 schemas,
ordered classifier, identity matrix, and acceptance boundary. A finding was
accepted only when the current text permits two treatments for the same facts,
cannot encode a promised treatment, conflates identities, or relies on an
unstated owner guarantee. No finding was repaired in Stage 6; Stage 08 owns the
replacement contract.

## Finding Disposition

| Finding | Decision | Why | Required repair |
| --- | --- | --- | --- |
| ADV-01 trigger reused after head change | accept/block | decision identity changes with the history cut, so compare-and-append alone does not consume the causal trigger | stable `recovery_trigger_key`; atomic trigger consumption |
| ADV-02 conflicting valid case kinds | accept/block | per-case totality does not arbitrate execution versus unresolved effect facts | subject-scoped `RecoveryFrontier` with blocking refs and atomic advancement |
| ADV-03 quarantine admission contradiction | accept/block | step A admits only `pass`, while trusted conflicts return `quarantine` | reduce admission to `pass \| reject`; normalize trusted contradiction to a passing `ConflictCase` |
| ADV-04 missing inputs unrepresentable | accept/block | mandatory policy/mapping fields prevent promised missing-input escalations | closed `OwnerGapCase` and typed absence sentinels |
| ADV-05 sameness preempts terminal truth | accept/block | Stage 6 can propose new work after known success/permanent outcome | terminal and unknown-effect posture before continuation eligibility; sameness only constrains an otherwise eligible continuation |
| ADV-06 effect retry equals Work retry | accept/block | `effect_attempt_id` and Work `attempt_id` are distinct but share one disposition | add `RETRY_NEW_EFFECT_ATTEMPT`; never use it to allocate a Work Attempt |
| ADV-07 unbounded reconciliation | accept/block | policy names a limit but decision acceptance neither debits it nor closes exhaustion | original-effect-scoped counter, deadline, atomic debit, closed exhaustion route/reason |
| ADV-08 unadmitted signal/policy | accept/block | a correct digest is not owner admission | admitted owner-bound handles for signal and policy |
| ADV-09 deadline nondeterminism | accept/block | deadline state is absent from case bytes and atomic compare | admitted logical deadline observation in validation vector |
| ADV-10 partial fence relation | accept/flag | `older` is handled but foreign/impossible values can continue | owner-defined `equal \| older \| impossible_or_foreign` relation |
| ADV-11 resume routing ambiguity | accept/flag | resume may be read as permission to redeliver pending effects | route-free cursor reconstruction only; pending items become new cases |
| ADV-12 no exhaustion-escalation reason | accept/block | a known exhausted counter cannot truthfully use `BUDGET_STATE_UNKNOWN` | closed exhaustion escalation reasons by counter kind |
| ADV-13 duplicate compensation intent | accept/flag | at-least-once observation of one decision can allocate multiple compensation entries | stable compensation intent, message, input digest, and idempotency key |
| ADV-14 incomplete atomic validation | accept/block | policy, authority, permit, route, and mapping can change without head/fence change | complete `DecisionValidationVector` checked atomically |
| ADV-15 underspecified hashes | accept/flag | executable implementations can disagree on tuple framing and field ordering | domain-separated canonical encoding with self-field exclusions |

## Parent Traceability Finding

### PAR-01 — Required cancellation variant disappeared

- Severity: `flag`
- Evidence: Stage 03 required a closed `CancellationCase`, and Stage 05
  retained seven case families. Stage 06 reduced the union to six without an
  explicit elimination argument and placed cancellation under `ExecutionCase`.
- Counterexample: a run-scoped cancellation is accepted before a Work Attempt
  exists. It cannot satisfy the mandatory current-attempt fields of an
  `ExecutionCase`, although the reason vocabulary promises
  `STOP_TERMINAL(CANCELLATION_TERMINAL)`.
- Decision: accept.
- Repair: add a closed `CancellationCase` with target scope, accepted
  cancellation-terminal fact, and current cancellation fence. Cancellation is
  evaluated as terminal before continuation logic.

## Repaired Contract Constraints

Stage 08 must satisfy all of the following together:

1. One admitted structural trigger has one stable trigger key and can release
   at most one accepted treatment.
2. One subject has one owner-reduced RecoveryFrontier; unresolved effect or
   reconciliation posture inhibits incompatible continuation cases.
3. Admission has one legal path to conflict and one representable path for
   owner/input gaps.
4. Known terminal, cancellation, and effect-unknown facts dominate continuation.
5. Work-attempt retry and exact-effect-attempt retry are different dispositions
   with different identity transitions.
6. Attempts, rounds, deliveries, reconciliation, and compensation all have
   explicit stable identities, budgets where applicable, and exhaustion routes.
7. Signals, policies, deadlines, authority bases, mappings, routes, and effect
   permits are admitted handles or validation-vector members, not trusted hashes.
8. Runtime resume only rebuilds projections/cursors and produces no route.
9. Every digest and identifier has a versioned canonical-encoding contract.
10. Cancellation and owner gaps are first-class closed case variants.

## Stable Controls To Preserve

- older accepted facts remain visible but release no route;
- outcome-unknown effects never select redelivery or retry;
- same-message redelivery preserves the logical envelope and Work Attempt;
- new-run selection remains a proposal to ordinary entry, not authorization;
- compensation remains correlated new Work and never rollback;
- raw ARE output, projections, UI state, and provider responses remain invalid
  structural evidence;
- every `RecoveryDecision` retains `authority_effect: none`.

## Verdict Basis

`block` applies to Stage 6 as an exact implementation contract. It is not an
architecture rejection. Every finding has a bounded repair that preserves the
selected owner-separated design, so the Refine route proceeds to Stage 08
rather than restarting Define or opening external research.

