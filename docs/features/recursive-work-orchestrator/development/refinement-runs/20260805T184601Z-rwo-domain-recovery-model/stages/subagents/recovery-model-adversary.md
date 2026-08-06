# Recovery Model Adversarial Review

## Review Identity

- Role: `recovery-model-adversary`
- Capability: `interrogation`
- Mode: `refine-design-review`
- Target: `stages/06-invoke-design.md`
- Claim ceiling: artifact-only adversarial review; no authority,
  implementation, or promotion effect
- Verdict: `block`
- Finding count: 11 block, 4 flag, 0 note

`block` means the Stage 6 model is not yet exact enough to hand to an
implementation owner. It does not mean the architectural direction is unsound.
The owner separation, effect-unknown prohibition, identity vocabulary, and
compare-and-append direction survive review, but the contract still permits or
cannot represent several safety-critical executions.

## Falsification Method

The review attempted to produce two different legal treatments from the same
accepted facts, make a stale or duplicate decision release work, cross the
delivery/Work/effect identity boundaries, bypass an owner through a forged or
revoked input, and find states named by the reason vocabulary that cannot be
encoded by the case union. Each finding below names the challenged Stage 6
rule, a concrete counterexample, whether the current text survives, and the
smallest repair.

## Findings

### ADV-01 — A consumed trigger can schedule a second recovery action after the head advances

- Severity: `block`
- Challenged rule: **3.5 Shared RecoveryCase Header**, **3.10
  RecoveryDecision**, **4.4 Decision Acceptance And Concurrency**, and
  classifier step B.
- Counterexample: classifiers A and B build the same `ExecutionCase` from
  history cut H0. A's `RETRY_NEW_ATTEMPT` is accepted, which appends a record
  and advances the head to H1. B loses compare-and-append and rebuilds. Because
  `history_cut_ref` is part of the canonical case, the rebuilt case has a new
  `case_digest`; therefore its `recovery_decision_id` also changes. Step B only
  deduplicates an identical decision for the same case/policy/version. Unless
  an unstated reducer drops or marks the original trigger, B can select a
  second new Attempt from the same terminal failure.
- Current design survives: **no**. Atomic append prevents two H0 decisions,
  but it does not prove semantic one-shot consumption across H0 and H1.
- Smallest repair: add a stable `recovery_trigger_key` independent of the
  history cut, derived from the admitted observation and its lifecycle
  generation. Atomically record `trigger consumed -> accepted decision` with
  decision acceptance. Rebuilt cases must consult that record and return
  `DEDUPLICATE` without another budget debit or identity allocation.

### ADV-02 — Per-case totality does not prevent conflicting cases for one subject

- Severity: `block`
- Challenged rule: **3.6 Closed RecoveryCase Variants**, **4.4 Decision
  Acceptance And Concurrency**, **5.1 Ordered Classifier**, and the
  **Persistence And Concurrency Extension**.
- Counterexample: one attempt has both an accepted transient executor terminal
  event and an accepted effect-attempt-start with outcome unknown. An
  `ExecutionCase` and `EffectCase` are independently valid at H0. The effect
  case wins acceptance and schedules reconciliation. The execution decision
  loses H0, rebuilds at H1, and may still select `RETRY_NEW_ATTEMPT`; no rule
  says an accepted unresolved reconciliation blocks every continuation case
  for the same attempt/effect scope.
- Current design survives: **no**. The unknown-effect guard dominates only
  inside an `EffectCase`; it does not dominate another simultaneously valid
  case kind.
- Smallest repair: define a journal-owned `RecoveryFrontier` (or equivalent
  subject-scoped reducer) that selects the currently actionable observations
  and carries `blocking_recovery_refs`. Admission must reject or suppress an
  execution/repeat/delivery continuation while the same scope has an unresolved
  effect, compensation, or terminal recovery decision. Compare-and-append must
  atomically advance this frontier.

### ADV-03 — `quarantine` cannot legally reach the classifier that emits quarantine

- Severity: `block`
- Challenged rule: **3.7 CaseAdmissionVerdict** and classifier step A/C.
- Counterexample: trusted journal records prove divergent bytes under one
  idempotency key. Admission returns `quarantine` and emits a `ConflictCase`.
  Classifier step A requires `CaseAdmissionVerdict=pass`, while the interface
  text says only pass or a trusted ConflictCase reaches the classifier. The
  contract does not state whether the ConflictCase is re-admitted as `pass`,
  whether step A accepts `quarantine`, or whether admission directly creates a
  `RecoveryDecision`.
- Current design survives: **no**. `QUARANTINE_CONFLICT` has no single legal
  transition from the stated admission state machine.
- Smallest repair: choose one model. Prefer `reject | pass`, with accepted
  contradictory facts normalized into a closed `ConflictCase` that receives
  `pass`; malformed or untrusted envelopes remain `reject`. Alternatively,
  explicitly allow only `(quarantine, ConflictCase)` at classifier step A.

### ADV-04 — Named missing-input escalations are not representable

- Severity: `block`
- Challenged rule: **3.3 AcceptedHistorySlice**, **3.4 RecoveryPolicy**,
  **3.5 Shared RecoveryCase Header**, **3.9 Closed Reason Families**, **4.2
  Domain Mapping Flow**, and **3.10 RecoveryDecision**.
- Counterexample: the structural observation and escalation owner are valid,
  but no applicable policy exists. The reason vocabulary promises
  `ESCALATE_OWNER(MISSING_POLICY)`, yet `RecoveryCase.policy_ref` and
  `RecoveryDecision.policy_ref/policy_digest` are mandatory. Similarly, a
  mapping block is said to form an escalation case, but the closed union has no
  mapping-block or owner-gap variant and an `ExecutionCase` requires an
  accepted failure class.
- Current design survives: **no**. The prose names decisions that cannot be
  constructed under the schemas.
- Smallest repair: add a closed `OwnerGapCase`/`InputResolutionCase` with an
  explicit missing component enum and an admitted escalation owner, or define
  admission resolutions outside `RecoveryDecision`. If missing policy remains
  a decision, its ID formula must use a typed `policy_absent` sentinel rather
  than a nonexistent digest.

### ADV-05 — Changed sameness can override an already-known terminal outcome

- Severity: `block`
- Challenged rule: classifier step G before H, **5.3 ExecutionCase Table**, and
  **5.5 EffectCase Table**.
- Counterexample: effect attempt E is accepted as `succeeded`, but the current
  normalized input or authority basis differs from the original run. Step G
  applies to every effect case before the effect table and therefore selects
  `REVALIDATE_NEW_RUN`. The `succeeded -> STOP_TERMINAL(ALREADY_SATISFIED)` row
  is never reached. A fresh gate may still stop launch, but the recovery model
  has proposed repetition of an intent whose original effect is known to have
  succeeded. The same issue lets changed input preempt a permanent execution
  failure.
- Current design survives: **no**. “Proposal only” limits authority inflation
  but does not make the treatment semantically correct.
- Smallest repair: recognize accepted terminal success/permanent/cancellation
  and effect-unknown states before continuation sameness. Apply sameness only
  when a table row first establishes a domain/policy-backed continuation
  intent. A changed value then converts that continuation to a new-run
  proposal; it does not invent continuation after a terminal outcome.

### ADV-06 — Known effect retry is conflated with retrying the whole Work Attempt

- Severity: `block`
- Challenged rule: **5.5 EffectCase Table** and the **Identity Transition
  Matrix** row for `RETRY_NEW_ATTEMPT`.
- Counterexample: an adapter proves an exact external request failed before
  application and the exact-effect owner permits a second effect attempt. The
  effect table returns `RETRY_NEW_ATTEMPT`, which allocates a new Work Attempt,
  new addressed commands, and potentially re-executes unrelated logic or
  earlier effects. An `effect_attempt_id` was defined precisely as independent
  from a Work `attempt_id`, but the disposition collapses them.
- Current design survives: **no**, unless every effectful Work node is proven
  to have a one-to-one atomic Work-Attempt/effect-attempt binding. No such
  proof is required by the current case or permit.
- Smallest repair: either add a distinct exact-effect-owner disposition/route
  for `RETRY_NEW_EFFECT_ATTEMPT`, or require a digest-bound 1:1 binding receipt
  that proves a new Work Attempt can do nothing except the permitted exact
  effect. Without either, a failed-known EffectCase must escalate.

### ADV-07 — Reconciliation can loop without a defined debit or exhaustion result

- Severity: `block`
- Challenged rule: `RecoveryPolicy.reconciliation.max_attempts`, classifier
  step F, **5.6 Exhaustion Resolution**, and the **Effect State** diagram.
- Counterexample: reconciliation returns `still_unknown` repeatedly. The
  policy contains `max_attempts`, but step F checks only owner/policy/work
  completeness; it does not require, debit, or name the reconciliation counter.
  The reconciliation policy also has no exhaustion route. Every rebuilt
  EffectCase can therefore propose another reconciliation WorkRun while the
  design simultaneously claims boundedness.
- Current design survives: **no**.
- Smallest repair: key one reconciliation budget to the original
  `effect_intent_id/effect_attempt_id`, include its expected value and debit in
  decision acceptance, and add a closed exhaustion route and reason such as
  `RECONCILIATION_EXHAUSTED`. `still_unknown` at exhaustion must stop or
  escalate; it must never unlock an effect retry.

### ADV-08 — Domain signal and policy provenance are digest-shaped but not admitted

- Severity: `block`
- Challenged rule: **3.2 DomainRecoverySignal**, **3.4 RecoveryPolicy**, **3.7
  CaseAdmissionVerdict**, and the **Security And Abuse Extension**.
- Counterexample: an untrusted caller supplies a self-consistent signal with
  `failure_class=transient`, a plausible `mapping_ref`, and freshly computed
  `mapping_input_digest/signal_digest`. The signal schema has no producer-owner
  identity, admitted result record, or binding from the mapping implementation
  digest to the accepted input bytes. The shared case header carries only
  `domain_signal_ref`, not an owner admission receipt. A parallel substitution
  can inject a permissive policy digest.
- Current design survives: **partially**. It correctly rejects unadmitted
  `RecoveryObservation` and limits ARE receipts, but equivalent admission is
  not specified for the domain signal or policy.
- Smallest repair: require admitted `DomainRecoverySignal` and
  `RecoveryPolicy` handles containing owner, contract/version digest, exact
  input/output digest, and acceptance record. Case admission must verify those
  handles against the WorkDefinition's declared domain/policy owners; hashes
  alone are not trust evidence.

### ADV-09 — Deadline evaluation is neither deterministic nor atomic

- Severity: `block`
- Challenged rule: `RecoveryPolicy.deadline_ref`, classifier step I, **5.6
  Exhaustion Resolution**, **3.10 RecoveryDecision**, and **4.4 Decision
  Acceptance And Concurrency**.
- Counterexample: the classifier computes a retry one millisecond before the
  deadline and the journal accepts it one second after. No admitted clock or
  deadline-state observation appears in `RecoveryCase`; no deadline expectation
  appears in the compare set. If the classifier reads wall time, identical case
  bytes can yield different results, violating determinism. If it does not,
  deadline behavior is unimplementable.
- Current design survives: **no**.
- Smallest repair: include an owner-admitted `DeadlineObservation` or logical
  time/expiry state in the case and decision validation vector. Acceptance must
  fail if the deadline has elapsed or the clock/lease epoch changed, causing a
  rebuild rather than allocating an Attempt or round.

### ADV-10 — Fence comparison defines “older” but not “equal/newer/incomparable”

- Severity: `flag`
- Challenged rule: classifier step D, **AttemptFence**, and **CaseAdmissionVerdict**.
- Counterexample: an accepted adapter record carries fence 9 while current
  owner state says fence 8, or carries an opaque fence from another allocation
  domain. It is not “older”, so step D does not stop it; mere shape/internal
  consistency does not establish equality or legitimate succession.
- Current design survives: **partially**. Older observations are safely
  ignored and compare-and-append checks the current value, but classification
  lacks a closed fence relation.
- Smallest repair: define an owner-supplied comparison returning
  `equal | older | impossible_or_foreign`. Only `equal` may continue;
  `older` is ignored and `impossible_or_foreign` becomes a trusted conflict or
  protocol rejection. Relevant cases may not carry a null fence.

### ADV-11 — Resume is described as both pure reconstruction and potential redelivery

- Severity: `flag`
- Challenged rule: **4.1 Normal Flow**, classifier step E, the **Identity
  Transition Matrix** row for `RESUME_FROM_JOURNAL`, and the **State/Event
  Extension**.
- Counterexample: after restart, the journal shows a pending effect command
  whose broker acceptance and provider outcome are unknown. The resume row says
  “reconciliation may redeliver same message.” If `RESUME_FROM_JOURNAL` exposes
  that as a route, it can bypass the EffectCase unknown-outcome guard.
- Current design survives: **partially**. The text says reconstruction occurs
  before ordinary classification, but the identity matrix leaves a route side
  effect ambiguous.
- Smallest repair: make `RESUME_FROM_JOURNAL` projection/cursor reconstruction
  only, with `proposed_route_ref=null`, `budget_debit=null`, and no delivery.
  After reconstruction, each pending item must form a fresh DeliveryCase or
  EffectCase; pending effects take the unknown-effect path.

### ADV-12 — Declared exhaustion escalation has no closed reason code

- Severity: `block`
- Challenged rule: **3.9 Closed Reason Families**, **5.3 ExecutionCase Table**,
  **5.4 RepeatCase Table**, and **5.6 Exhaustion Resolution**.
- Counterexample: the round counter is authoritatively exhausted and policy
  declares `exhaustion_route=escalate` with a valid owner. The repeat table says
  `BUDGET_STATE_UNKNOWN` is only for missing truth and otherwise calls for an
  “owner-specific exhaustion reason.” No such closed `ESCALATE_OWNER` reason
  exists. The same hole applies to known attempt exhaustion with an escalation
  route.
- Current design survives: **no**. Totality and closed-enum claims conflict.
- Smallest repair: add closed reasons such as
  `ATTEMPT_EXHAUSTION_ESCALATION`, `ROUND_EXHAUSTION_ESCALATION`, and
  `RECONCILIATION_EXHAUSTION_ESCALATION`, or define one typed
  `DECLARED_EXHAUSTION_ESCALATION` reason with a closed counter-kind field.

### ADV-13 — Compensation proposal lacks a stable intent identity

- Severity: `flag`
- Challenged rule: **3.10 RecoveryDecision**, the **Identity Transition
  Matrix**, and the **Failure And Compensation Extension**.
- Counterexample: the same accepted compensation decision is observed twice by
  an at-least-once route evaluator. The decision has a route reference but no
  stable `compensation_intent_id`, exact compensation input digest, or ordinary
  entry idempotency key. Fresh gates can therefore accept two compensation
  WorkRuns even though decision acceptance happened once.
- Current design survives: **partially**. Compensation is correctly explicit,
  correlated, non-rollback Work through fresh authority, but route-level
  convergence is unspecified.
- Smallest repair: derive and bind one compensation intent/message/idempotency
  key from the accepted recovery decision, original subject/effect, declared
  compensation Work version, and exact normalized input. Re-observation must
  redeliver that same entry message, not allocate a second compensation intent.

### ADV-14 — Acceptance does not fence mutable policy, mapping, authority, or permit state

- Severity: `block`
- Challenged rule: **4.4 Decision Acceptance And Concurrency**, **Authority And
  Trust Extension**, and **Compatibility Rules**.
- Counterexample: a retry is classified under policy P7 and an effect-owner
  retry permit. Before journal acceptance, the policy is revoked or authority
  basis advances without changing journal head, attempt counter, or RWO fence.
  The compare set still matches and accepts the stale decision. A later exact
  effect gate helps protected calls but does not undo the unauthorized
  lifecycle/budget allocation, and not every retry is effectful.
- Current design survives: **partially**. Digests preserve what was evaluated,
  while later gates preserve some effect safety, but acceptance does not prove
  those inputs remain applicable.
- Smallest repair: replace the three-field expected set with an explicit
  `DecisionValidationVector` containing journal head, every debited counter,
  fence, policy applicability epoch, mapping/domain-state epoch where relevant,
  authority basis/lease, deadline state, route version, and exact-effect permit
  nonce/expiry when used. Acceptance validates the whole vector atomically or
  rejects and rebuilds.

### ADV-15 — Decision hashing has no canonical tuple/field-exclusion contract

- Severity: `flag`
- Challenged rule: **3.5 Shared RecoveryCase Header** and **3.10
  RecoveryDecision**.
- Counterexample: `sha256(case_digest + policy_digest + classifier_version)`
  uses unframed concatenation, so different component boundaries can serialize
  to identical bytes. `decision_digest` also does not state which fields are
  excluded from its own digest or how maps/lists are ordered. Independent
  replay implementations can therefore compute different IDs despite equal
  semantic inputs.
- Current design survives: **no** at an executable conformance level; the
  conceptual intent is clear.
- Smallest repair: define a versioned, domain-separated canonical encoding with
  length-delimited fields, normalized enum/string encoding, ordered maps, and
  explicit self-field exclusions for every case, trigger, decision, and
  identity-transition digest.

## Controls That Survived Direct Challenge

- A genuinely older accepted fence has zero routing effect.
- An `EffectCase(outcome=unknown)` cannot directly select redelivery or retry.
- Same-message redelivery preserves logical message bytes/key and does not
  allocate a Work Attempt.
- A changed identity basis is only a new-run proposal; it does not itself
  grant authority or start the run.
- Compensation remains new, correlated Work through fresh gates and never
  rewrites the original facts.
- Raw ARE output, projections, UI state, and unadmitted provider responses are
  not valid structural observations.

These controls remain necessary; the required repairs refine their composition
rather than replace them.

## Required Repairs

1. Add a history-cut-independent recovery trigger key and atomically consume it
   with accepted decision, budget, and identity changes.
2. Define a subject-scoped RecoveryFrontier/cross-case inhibition model so
   unresolved effect, compensation, terminal, and reconciliation facts dominate
   conflicting cases across classifier runs.
3. Make the admission-to-conflict transition single-valued and add a
   representable owner-gap/input-resolution path for missing policy, mapping,
   evidence, and owner cases.
4. Reorder terminal/outcome and continuation rules so sameness can constrain a
   requested continuation but cannot invent one after success/permanent outcome.
5. Separate effect-attempt retry from Work-Attempt retry, or require an exact
   1:1 atomic binding receipt before using `RETRY_NEW_ATTEMPT` for an EffectCase.
6. Specify reconciliation counter identity, atomic debit, deadline, closed
   exhaustion route, and exhaustion reason.
7. Require owner-admitted, digest-bound DomainRecoverySignal and RecoveryPolicy
   handles rather than trusting self-consistent hashes.
8. Add deadline state and every mutable policy/mapping/authority/permit epoch to
   an atomic DecisionValidationVector.
9. Close fence comparison over equal, older, and impossible/foreign values;
   make resume reconstruction route-free and reclassify pending items afterward.
10. Give compensation one stable intent/message/idempotency identity so
    at-least-once route observation cannot create duplicate compensation runs.
11. Close known exhaustion escalation reasons and define canonical,
    domain-separated digest serialization and IdentityTransition encoding.

## Verdict

`block` for exact-model acceptance. The architecture is repairable without
changing its owner-separated thesis or twelve-disposition vocabulary, except
that effect-attempt retry needs either a thirteenth structural treatment or an
explicit proof that it is safely identical to a new Work Attempt. Stage 7/8
should repair the eleven items above and rerun the concrete concurrency,
unknown-effect, terminal-sameness, exhaustion, and forged-input games before
Plan treats the model as implementation-ready.
