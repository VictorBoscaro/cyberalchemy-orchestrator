# Stage 08 — Distill Repair: Exact Recovery Decision Contract

## Distill Result

- Repair target: Stage 07's 12 accepted repairs
- Smallest coherent unit: `RecoveryDecisionContract@candidate-2`
- Model status: `pass` as a candidate design contract
- Scenario games: 20 / 20 pass
- Remaining owner gaps: 3, represented fail-closed
- Authority effect: none
- Supersedes: Stage 06 wherever this artifact states a repaired contract
- Next route: Invoke Plan

This is the repaired exact model for this refinement run. “Exact” means the
case space, precedence, identity transitions, atomic acceptance preconditions,
and fail-closed outcomes are explicit and single-valued. It does not mean the
model is implemented, owner-approved, promoted into the ontology, or proven by
runtime execution.

## Responsibility Boundary

```text
admitted structural records
  -> journal-owned RecoveryFrontier
domain event -> owner-admitted DomainRecoverySignalHandle
owner-admitted policy/deadline/authority/effect handles
  -> CaseAssembler -> pass | reject
  -> closed RecoveryCase union
  -> deterministic RecoveryClassifier
  -> ProposedRecoveryDecision | PreviouslyAcceptedDecisionRef
  -> journal/ACI atomic compare-and-accept
  -> accepted decision becomes input to ordinary RWO routing
  -> independent entry, authority, ACI, and effect-owner gates
```

The contract owns one behavior: select a structural treatment for one active
recovery trigger. It does not decide domain meaning, write source truth, grant
authority, execute Work, call ARE, reconcile an effect, or perform compensation.

## 1. Trusted Inputs

### 1.1 RecoveryTriggerHandle

```yaml
schema_version: rwo-recovery-trigger.candidate-2
recovery_trigger_key: digest
accepted_record_ref: journal-record-id
accepted_record_digest: digest
observation_kind: conflict | runtime_restart | delivery | execution_terminal | repeat_decision | cancellation_terminal | effect_outcome
lifecycle_generation: owner-allocated-generation
subject_scope_key: digest
subject:
  work_ref: work:name@version
  root_work_run_id: run-id
  work_run_id: run-id
  node_path: root/path
  round_id: round-id | null
  work_attempt_id: attempt-id | null
  logical_message_id: message-id | null
  effect_intent_id: effect-intent-id | null
  effect_attempt_id: effect-attempt-id | null
source_owner_ref: owner-id
source_admission_ref: accepted-record-id
trigger_digest: digest
```

`recovery_trigger_key` is independent of the history cut. It is the canonical
digest of the admitted record identity, lifecycle generation, observation kind,
and exact subject identifiers. Rebuilding against a later head cannot create a
new trigger key for the same causal fact.

### 1.2 RecoveryFrontier

```yaml
schema_version: rwo-recovery-frontier.candidate-2
frontier_ref: frontier-id
frontier_epoch: integer
history_head_ref: record-id
history_head_digest: digest
reducer_ref: reducer@version
subject_scope_key: digest
actionable_trigger_key: digest | null
consumed_triggers:
  trigger-key: accepted-decision-ref
blocking_recovery_refs: []
terminal_posture: open | succeeded | permanent_failure | canceled | operationally_stopped
pending_effect_posture: none | known | outcome_unknown | reconciling
current_identities: {}
current_fences: {}
current_counters: {}
frontier_digest: digest
```

The journal owner reduces accepted records into this immutable snapshot. One
frontier exposes at most one actionable trigger for an overlapping subject
scope. Disjoint subject scopes may progress independently.

Cross-case inhibition is closed:

1. trusted conflict blocks every overlapping route;
2. runtime reconstruction completes before any pending item is classified;
3. unresolved effect or reconciliation blocks Work retry, repeat, delivery of
   another effect command, compensation, and run revalidation for the same or
   ancestor scope;
4. cancellation or known terminal posture blocks every continuation descendant;
5. an accepted compensation intent blocks a second compensation intent for the
   same original subject;
6. a consumed trigger cannot become actionable again.

### 1.3 Owner-Admitted Semantic And Policy Handles

```yaml
DomainRecoverySignalHandle:
  signal_ref: admitted-record-id
  signal_owner_ref: domain-owner
  mapping_ref: domain:recovery-mapping@version
  mapping_contract_digest: digest
  admitted_input_digest: digest
  admitted_output_digest: digest
  mapping_epoch: owner-epoch
  failure_class: transient | permanent | rework | rejected | canceled | already_satisfied | none
  rework_intent: none | requested
  compensation_intent: none | requested
  semantic_receipt_ref: admitted-receipt-id | null
  acceptance_record_ref: journal-record-id

RecoveryPolicyHandle:
  policy_ref: policy-id
  policy_owner_ref: policy-owner
  policy_version: version
  policy_digest: digest
  applicability_epoch: owner-epoch
  applies_to_work_ref: work:name@version
  case_kinds: []
  limits: {}
  routes: {}
  acceptance_record_ref: admitted-record-id
```

A self-consistent hash is not admission. The assembler verifies the owner and
contract declared by the WorkDefinition. Missing or mismatched handles form an
`OwnerGapCase` only when an admitted escalation owner is available; otherwise
admission rejects.

### 1.4 Deadline And Fence Inputs

```yaml
DeadlineObservation:
  deadline_ref: deadline-policy-id
  owner_ref: clock-or-lease-owner
  logical_epoch: owner-epoch
  state: open | elapsed
  observed_at_logical: integer
  expiry_at_logical: integer
  admission_ref: accepted-record-id
  digest: digest

FenceRelation:
  fence_owner_ref: owner-id
  fence_domain_ref: fence-domain@version
  observed: value
  current: value
  relation: equal | older | impossible_or_foreign
  admission_ref: accepted-record-id
```

Only `equal` can continue. `older` selects zero-route stale handling.
`impossible_or_foreign` is either protocol rejection or a passing
`ConflictCase`, depending on whether the contradiction itself is trusted.

## 2. Closed Case Model

### 2.1 Admission

`CaseAdmissionResult = pass(RecoveryCase) | reject(ProtocolRejection)`.

- Malformed, unknown-version, unaccepted, owner-mismatched, or cross-run input
  is rejected before classification.
- Accepted contradictory facts are normalized into a valid `ConflictCase` and
  receive `pass`; there is no third admission state.
- A known absent/missing owner input becomes a valid `OwnerGapCase` only with a
  typed missing-component code and an admitted escalation owner.

### 2.2 Shared Header

```yaml
schema_version: rwo-recovery-case.candidate-2
recovery_case_id: digest
case_kind: conflict | owner_gap | runtime_resume | delivery | execution | repeat | cancellation | effect
trigger_ref: recovery-trigger-key
frontier_ref: frontier-id
frontier_epoch: integer
subject_scope_key: digest
subject: exact-identities
policy_handle_ref: policy-id | policy_absent
domain_signal_handle_ref: signal-id | signal_not_required | signal_absent
deadline_observation_ref: deadline-id | deadline_not_required
fence_relation_ref: fence-relation-id | fence_not_required
case_body: discriminated-body
case_digest: digest
```

### 2.3 Eight Variants

| Case | Mandatory facts | Primary structural purpose |
| --- | --- | --- |
| `ConflictCase` | trusted contradictory refs; conflict kind; stable subject | quarantine divergent bytes, impossible transitions, or contradictory trusted facts |
| `OwnerGapCase` | otherwise admitted trigger; missing component enum; intended case kind; admitted escalation owner | represent missing policy, mapping, evidence, reconciliation owner, or authority safely |
| `RuntimeResumeCase` | restart record; verified cut; reducer; pending refs | reconstruct cursor/projections only |
| `DeliveryCase` | logical message bytes/digest/key; delivery attempt; acceptance posture; delivery budget/idempotency contract | distinguish redelivery from Work execution |
| `ExecutionCase` | current Work Attempt; accepted terminal execution fact; domain signal; attempt counter; whole-Work retry-safety posture | choose terminal handling or a new Work Attempt |
| `RepeatCase` | repeat edge; accepted decision event; scope digest; current round/counter | choose a new bounded round or exhaustion treatment |
| `CancellationCase` | cancellation target scope; accepted terminal cancellation fact; cancellation fence | stop the target without requiring a Work Attempt |
| `EffectCase` | exact effect intent/attempt; accepted outcome posture; exact-effect permit/reconciliation refs | separate exact-effect treatment from Work retry |

Each variant is closed (`additionalProperties: false` in the future schema).
For the six ordinary structural variants, case kind comes from the
RecoveryFrontier's admitted trigger. A trusted contradiction is normalized to
`ConflictCase`; a missing required handle on an otherwise admitted trigger is
normalized to `OwnerGapCase` and retains `intended_case_kind`. Neither
normalization may be requested by a domain signal or ARE output.

## 3. Closed Treatment Vocabulary

### 3.1 Thirteen Dispositions

```text
DEDUPLICATE
REDELIVER_SAME_MESSAGE
RETRY_NEW_ATTEMPT
RETRY_NEW_EFFECT_ATTEMPT
REPEAT_NEW_ROUND
REVALIDATE_NEW_RUN
RESUME_FROM_JOURNAL
IGNORE_STALE_FOR_ROUTING
RECONCILE_UNKNOWN_EFFECT
COMPENSATE
QUARANTINE_CONFLICT
STOP_TERMINAL
ESCALATE_OWNER
```

`RETRY_NEW_EFFECT_ATTEMPT` is intentionally distinct. It preserves the Work
Attempt and exact effect intent while proposing one new effect attempt through
the exact-effect owner. `RETRY_NEW_ATTEMPT` allocates a new Work Attempt and may
be selected only by an `ExecutionCase` with whole-Work retry-safety evidence.

### 3.2 Closed Reason Families

| Disposition | Reasons |
| --- | --- |
| `DEDUPLICATE` | `IDENTICAL_ACCEPTED_DUPLICATE` |
| `REDELIVER_SAME_MESSAGE` | `COMMAND_NOT_ACCEPTED`, `COMMAND_ACCEPTANCE_UNKNOWN_IDEMPOTENT` |
| `RETRY_NEW_ATTEMPT` | `TRANSIENT_EXECUTION_FAILURE` |
| `RETRY_NEW_EFFECT_ATTEMPT` | `KNOWN_EFFECT_FAILURE_WITH_EFFECT_RETRY_PERMIT` |
| `REPEAT_NEW_ROUND` | `DOMAIN_REWORK_REQUESTED` |
| `REVALIDATE_NEW_RUN` | `DEFINITION_CHANGED`, `NORMALIZED_INPUT_CHANGED`, `AUTHORITY_BASIS_CHANGED`, `EFFECT_ENVELOPE_CHANGED`, `REPEAT_SCOPE_CHANGED` |
| `RESUME_FROM_JOURNAL` | `RUNTIME_RESTART_WITH_VALID_HISTORY` |
| `IGNORE_STALE_FOR_ROUTING` | `OLDER_ATTEMPT_FENCE`, `OLDER_ROUND_FENCE`, `OLDER_CANCELLATION_FENCE`, `SUPERSEDED_RUN` |
| `RECONCILE_UNKNOWN_EFFECT` | `EFFECT_OUTCOME_UNKNOWN` |
| `COMPENSATE` | `DECLARED_IMMEDIATE_COMPENSATION`, `DECLARED_EXHAUSTION_COMPENSATION` |
| `QUARANTINE_CONFLICT` | `DIVERGENT_IDEMPOTENCY_BYTES`, `CONTRADICTORY_TRUSTED_FACTS`, `IMPOSSIBLE_STATE_TRANSITION`, `IMPOSSIBLE_OR_FOREIGN_FENCE` |
| `STOP_TERMINAL` | `PERMANENT_FAILURE`, `POLICY_DENIED`, `ATTEMPT_EXHAUSTED`, `ROUND_EXHAUSTED`, `RECONCILIATION_EXHAUSTED_UNKNOWN`, `DEADLINE_ELAPSED`, `CANCELLATION_TERMINAL`, `ALREADY_SATISFIED` |
| `ESCALATE_OWNER` | `MISSING_POLICY`, `MISSING_MAPPING`, `MISSING_REQUIRED_OWNER`, `MISSING_REQUIRED_EVIDENCE`, `AMBIGUOUS_DOMAIN_MAPPING`, `UNKNOWN_SAMENESS`, `BUDGET_STATE_UNKNOWN`, `RECONCILIATION_UNAVAILABLE`, `RESUME_EVIDENCE_MISSING`, `ATTEMPT_EXHAUSTION_ESCALATION`, `ROUND_EXHAUSTION_ESCALATION`, `RECONCILIATION_EXHAUSTION_ESCALATION` |

Unknown dispositions, reasons, or reason/disposition pairs reject.

## 4. Classifier Result And Decision

```yaml
ClassificationResult:
  result_kind: proposed | previously_accepted
  proposed_decision: RecoveryDecision | null
  accepted_decision_ref: accepted-decision-id | null

RecoveryDecision:
  schema_version: rwo-recovery-decision.candidate-2
  recovery_decision_id: digest
  trigger_ref: recovery-trigger-key
  case_ref: case-id
  case_digest: digest
  frontier_ref: frontier-id
  frontier_epoch: integer
  policy_handle_ref: policy-id | policy_absent
  mapping_handle_ref: mapping-id | mapping_not_required | mapping_absent
  classifier_ref: recovery-classifier@candidate-2
  disposition: closed-enum
  reason_code: valid-member-for-disposition
  identity_transition: IdentityTransition
  validation_vector: DecisionValidationVector
  budget_debits: []
  required_next_owner: owner-id | null
  proposed_route_ref: route-or-work-ref | null
  compensation_intent: stable-intent | null
  reconciliation_intent: stable-intent | null
  authority_effect: none
  evidence_refs: []
  decision_digest: digest
```

If the trigger is already consumed, the classifier returns the original
accepted decision reference. It does not append a new dedup decision, debit a
budget, or allocate an identity.

## 5. Ordered Deterministic Algorithm

```text
classify(case, frontier):
  A. Require CaseAdmissionResult=pass and exact frontier/case binding.
  B. If trigger is consumed, return PreviouslyAcceptedDecisionRef.
  C. If trigger is not the frontier's sole actionable trigger or has blockers,
     reject as stale input and rebuild; do not emit a decision.
  D. ConflictCase -> QUARANTINE_CONFLICT.
  E. OwnerGapCase -> ESCALATE_OWNER with exact missing-component reason.
  F. Fence older -> IGNORE_STALE_FOR_ROUTING.
     Fence impossible/foreign -> ConflictCase or protocol reject.
  G. RuntimeResumeCase -> RESUME_FROM_JOURNAL with null route/debits.
  H. Evaluate accepted terminal posture:
       cancellation -> STOP_TERMINAL(CANCELLATION_TERMINAL)
       known success/already satisfied -> STOP_TERMINAL(ALREADY_SATISFIED)
       known permanent outcome -> compensation if fully declared, else STOP_TERMINAL
       effect outcome unknown -> bounded reconciliation or exact escalation/stop
     These outcomes cannot be overridden by sameness.
  I. Evaluate the case-specific table to establish a continuation candidate.
  J. Only for a continuation candidate, evaluate definition, normalized input,
     authority basis, effect envelope, or repeat-scope sameness.
       changed -> REVALIDATE_NEW_RUN with exact changed reason
       unknown -> ESCALATE_OWNER(UNKNOWN_SAMENESS)
       same/not-applicable -> retain candidate
  K. Apply admitted deadline, exact counter, owner, route, idempotency, and
     retry-safety guards. Resolve exhaustion through the closed policy table.
  L. Emit exactly one ProposedRecoveryDecision and full validation vector.
```

### Case-Specific Continuation Table

| Case/fact | Required evidence | Candidate treatment |
| --- | --- | --- |
| Delivery accepted, identical duplicate | accepted same key/bytes | `DEDUPLICATE` |
| Delivery not accepted | exact envelope, current fence, recipient idempotency contract, budget | `REDELIVER_SAME_MESSAGE` |
| Delivery acceptance unknown | above plus convergence contract | `REDELIVER_SAME_MESSAGE` |
| Execution transient terminal | policy eligibility, open deadline, attempt budget, whole-Work retry-safety receipt if any effectful binding exists | `RETRY_NEW_ATTEMPT` |
| Repeat rework requested | allowed signal, repeat edge, current round fence, round budget | `REPEAT_NEW_ROUND` |
| Effect failed-known and exact retry safe | exact-effect permit, permit nonce/expiry, effect-attempt budget, stable intent | `RETRY_NEW_EFFECT_ATTEMPT` |
| Effect outcome unknown | reconciliation owner/work, original-effect-scoped counter, deadline | `RECONCILE_UNKNOWN_EFFECT` |
| Owner input missing | typed gap and admitted escalation owner | `ESCALATE_OWNER` |

No EffectCase selects `RETRY_NEW_ATTEMPT`. No ExecutionCase selects
`RETRY_NEW_EFFECT_ATTEMPT`.

## 6. Reconciliation And Exhaustion

One reconciliation budget is keyed by
`(effect_intent_id, effect_attempt_id, reconciliation_policy_version)`.
Each accepted `still_unknown` reconciliation result is a new admitted trigger;
it can propose the next stable reconciliation intent only while the counter and
deadline remain open.

```text
if deadline elapsed:
  STOP_TERMINAL(DEADLINE_ELAPSED)
else if counter truth missing:
  ESCALATE_OWNER(BUDGET_STATE_UNKNOWN)
else if counter remains:
  select the case table candidate and debit exactly one at acceptance
else switch declared exhaustion route:
  stop:
    ATTEMPT -> STOP_TERMINAL(ATTEMPT_EXHAUSTED)
    ROUND -> STOP_TERMINAL(ROUND_EXHAUSTED)
    RECONCILIATION -> STOP_TERMINAL(RECONCILIATION_EXHAUSTED_UNKNOWN)
  compensate:
    complete compensation refs -> COMPENSATE(DECLARED_EXHAUSTION_COMPENSATION)
    otherwise -> ESCALATE_OWNER(MISSING_REQUIRED_OWNER)
  escalate:
    ATTEMPT -> ESCALATE_OWNER(ATTEMPT_EXHAUSTION_ESCALATION)
    ROUND -> ESCALATE_OWNER(ROUND_EXHAUSTION_ESCALATION)
    RECONCILIATION -> ESCALATE_OWNER(RECONCILIATION_EXHAUSTION_ESCALATION)
```

Reconciliation exhaustion never changes the original effect outcome from
`unknown` and never unlocks an effect retry.

## 7. Identity Transition Contract

| Disposition | WorkRun | Round | Work Attempt | Message/delivery | Effect intent/attempt | Other stable identity |
| --- | --- | --- | --- | --- | --- | --- |
| `DEDUPLICATE` | preserve | preserve | preserve | preserve | preserve | no allocation |
| `REDELIVER_SAME_MESSAGE` | preserve | preserve | preserve | same logical message/bytes/key; new delivery attempt allowed | preserve; no effect attempt | same trigger generation |
| `RETRY_NEW_ATTEMPT` | preserve | preserve | allocate one new Work Attempt | new addressed messages | no exact-effect allocation by this decision | attempt budget debit |
| `RETRY_NEW_EFFECT_ATTEMPT` | preserve | preserve | preserve | exact-effect command through owner | same effect intent; allocate one effect attempt | effect-attempt budget debit + permit nonce |
| `REPEAT_NEW_ROUND` | preserve containing run | allocate one round | new child attempts only after route gates | new | independently governed | round budget debit |
| `REVALIDATE_NEW_RUN` | old run preserved; new run only proposed | none yet | none yet | stable entry proposal | fresh envelope only after entry | `new_run_proposal_id` |
| `RESUME_FROM_JOURNAL` | preserve | preserve | preserve | none | none | reconstruct cursor only |
| `IGNORE_STALE_FOR_ROUTING` | preserve | preserve | preserve | none | none | no allocation |
| `RECONCILE_UNKNOWN_EFFECT` | preserve original | preserve | preserve | stable reconciliation entry message | preserve unknown original | `reconciliation_intent_id` and counter debit |
| `COMPENSATE` | preserve original; compensation run proposed | preserve original | preserve original | stable compensation entry message | original facts preserved | `compensation_intent_id` |
| `QUARANTINE_CONFLICT` | preserve | preserve | preserve | none | none | quarantine record only |
| `STOP_TERMINAL` | preserve | preserve | preserve | none | none | terminal scheduling posture only |
| `ESCALATE_OWNER` | preserve | preserve | preserve | none | none | optional review intent must be separately declared |

Compensation identity is derived before the decision from the recovery trigger
key, case digest, policy digest/version, classifier version, original subject
and effect refs, declared compensation Work version, and normalized input
digest. It never depends on `recovery_decision_id`, so the decision can embed
the intent without a digest cycle. Re-observation of the accepted decision
redelivers the same entry message/idempotency key; it cannot allocate another
compensation intent.

Reconciliation intent is likewise derived before the decision from the
original effect intent/attempt, recovery trigger key, reconciliation policy
version, and expected pre-debit counter value. It does not depend on the
decision ID.

## 8. Atomic Decision Acceptance

### DecisionValidationVector

```yaml
history_head_digest: digest
frontier_ref: frontier-id
frontier_epoch: integer
frontier_digest: digest
trigger_ref: recovery-trigger-key
trigger_expected_state: unconsumed
counter_expectations: [{counter_ref, expected_value}]
fence_expectations: [{fence_domain_ref, expected_value}]
policy: {ref, digest, applicability_epoch, expected_state: active}
mapping: {ref, digest, epoch} | not_required
domain_state: {ref, digest, epoch} | not_required
authority_basis: {ref, digest, epoch_or_lease} | not_required
deadline: {ref, digest, logical_epoch, expected_state: open} | not_required
route: {ref, digest, version} | null
effect_permit: {ref, nonce, expiry_epoch, expected_state: active} | null
recipient_idempotency_contract: {ref, digest, version} | null
```

The journal/ACI owner performs one atomic transaction:

1. compare every validation-vector member to current owner state;
2. require the trigger unconsumed and still sole actionable trigger;
3. require no blocking recovery ref over the subject scope;
4. reserve exactly the declared new identities;
5. debit exactly the declared counters;
6. append the decision once by decision ID;
7. record `trigger -> accepted decision` consumption;
8. advance the RecoveryFrontier and expose the accepted decision.

Any mismatch performs none of steps 4–8. The caller rebuilds from a new
frontier. That rebuild is classification, not Work retry.

## 9. Canonical Encoding And IDs

`RWO Canonical Encoding candidate-2` is mandatory for case, trigger, frontier,
decision, transition, compensation, and reconciliation digests. Its payload
encoding delegates to the current runtime's frozen `aci.canonical-json@1`
profile rather than creating a competing JSON canonicalizer:

```yaml
canonicalizer_profile_id: aci.canonical-json
canonicalizer_profile_version: "1"
canonicalizer_profile_digest: sha256:6ed22971449c8ea911f9b885d26b01e6eb2e77f208cd8bc6419dff31d97b7ade
current_source_anchor: implementations/server/runtime/canonical.py
```

The profile supplies:

- UTF-8 JSON objects with keys sorted by Unicode code point;
- strings normalized to NFC; enums encoded as their exact lowercase or
  uppercase contract token; integers restricted to signed int64 and encoded
  in minimal base-10; binary floats forbidden; null explicit; list order
  preserved by schema;
- object-specific `*_id` and `*_digest` self-fields excluded from that object's
  payload; every other optional field must be explicit as null or a typed
  sentinel;
- after profile canonicalization, the RWO object ID input is
  `utf8("rwo:<object-kind>:candidate-2\\0") || u64be(payload_length) || payload`;
- digest is SHA-256 over those bytes.

Independent implementations must reproduce byte-identical fixtures before any
runtime adoption. Concatenating unframed digests or reimplementing a divergent
canonical JSON profile is forbidden. This candidate binding still requires an
owner conformance decision before implementation adoption.

## 10. Domain, ARE, And Authority Interaction

The domain interacts only through a versioned pure `RecoveryMapping` that maps
an admitted DomainEvent to an admitted `DomainRecoverySignalHandle`. The signal
may state failure class, rework intent, compensation intent, and semantic
constraints. It cannot choose case kind, disposition, route, WorkRun identity,
budget debit, or effect permission.

ARE is optional. If used, its output must first pass its own entry, ACI, and
artifact/semantic admission boundaries. The mapping may reference that admitted
receipt. Raw model output is never a signal or structural observation, and ARE
never returns a RecoveryDisposition.

Every accepted RecoveryDecision has `authority_effect: none`. The ordinary RWO
route evaluator may propose the declared next route only after decision
acceptance. New runs, reconciliation, compensation, effect attempts, and any
external effect independently pass their current entry/authority/ACI/effect
owner gates.

## 11. Scenario Game Result

The machine-readable cases are in `stages/08-scenario-matrix.json`.

| Game group | Cases | Result | Decisive invariant |
| --- | ---: | --- | --- |
| trigger/concurrency | 4 | pass | one trigger consumption and full-vector atomicity |
| terminal/cross-case | 4 | pass | frontier inhibition and terminal-before-continuation |
| delivery/identity | 2 | pass | logical delivery, Work Attempt, and effect attempt remain distinct |
| effect/reconciliation | 4 | pass | unknown never retries; known effect retry is exact-effect-only and bounded |
| exhaustion/cancellation | 2 | pass | closed truthful reasons and first-class cancellation |
| provenance/replay | 4 | pass | owner admission, canonical bytes, route-free resume, zero-call replay |

No scenario requires a new owner decision to select a safe treatment. Missing
owners resolve through `OwnerGapCase` and fail closed.

## 12. Repair Trace

| Repair source | Candidate-2 resolution |
| --- | --- |
| ADV-01 | stable trigger key + atomic consumed map |
| ADV-02 | journal-owned RecoveryFrontier + inhibition |
| ADV-03 | `pass \| reject`; conflicts normalize to passing case |
| ADV-04 | OwnerGapCase + typed absence sentinels |
| ADV-05 | terminal posture before continuation/sameness |
| ADV-06 | thirteenth `RETRY_NEW_EFFECT_ATTEMPT` disposition |
| ADV-07 | original-effect reconciliation counter/debit/exhaustion |
| ADV-08 | admitted owner-bound signal and policy handles |
| ADV-09/14 | full atomic DecisionValidationVector |
| ADV-10 | closed fence relation |
| ADV-11 | route-free runtime reconstruction |
| ADV-12 | truthful exhaustion escalation reasons |
| ADV-13 | stable compensation intent/message/key |
| ADV-15 | domain-separated canonical encoding |
| PAR-01 | first-class CancellationCase |
| FINAL-01 | OwnerGapCase is an assembler normalization with retained intended kind, not a forgeable observation kind |
| FINAL-02 | compensation/reconciliation intent formulas are acyclic and decision-ID-independent |

## 13. Remaining Owner Gaps

- `G1-JOURNAL-DOMAIN-TRUTH`: the exact owner contract reconciling journal
  structural facts with current domain truth remains unselected. Candidate-2
  carries both handles and blocks on mismatch.
- `G2-EXACT-EFFECT-OWNER`: exact permit, reconciliation, and effect-attempt
  schemas remain unselected. Candidate-2 escalates when their admitted handles
  are absent.
- `G3-ARE-ACI-CONFORMANCE`: executable cross-repository ARE/ACI schema versions
  and conformance receipts remain unselected. ARE remains optional and cannot
  be substituted by prose.

These gaps block owner integration and runtime claims, not the L0 pure schema,
classifier, and fixture plan.

## Verdict And Claim Ceiling

`pass` for a candidate exact model and for progression to planning. The model
has a closed input/case/treatment space, one-shot trigger consumption, explicit
cross-case arbitration, exact identity effects, deterministic bytes, and an
atomic acceptance boundary. It remains documentation-only, candidate-local,
non-authoritative, unimplemented, unpromoted, and unproven in production.
