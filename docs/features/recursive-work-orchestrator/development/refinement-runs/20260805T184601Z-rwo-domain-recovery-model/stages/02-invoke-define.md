# Stage 02 — Invoke Define: RWO Domain Recovery

## Invoke Result

- Mode: `define`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library capability authoring a target-local Refine artifact
- Phase status: `pass`
- Mode contract: `.agents/skills/invoke/define.md`
- Outputs: this definition/spec and glossary artifact
- Template selection: DomainSpec `domainspec-spec/SPEC.md`, adapted into one stage artifact because Refine owns the run folder
- Dispatch techniques: `sequence`, `sentence_grammar`, `frame_handoff`, `mandatory_component`, `owner_boundary_check`, `residue_ledger`
- Distill validation: scheduled as canonical s05; definition-scope sanity check below passes with explicit split pressure
- Decisions: recovery is one classifier capability over typed facts, policy, domain signal, and accepted history; its output is non-authorizing
- Unresolved gaps: journal/domain truth ownership, exact-effect/reconciliation owner, executable ARE conformance, Design selection validator evidence
- Next route: s03 `interrogation:refine-review`

## Intent And Approval Record

The operator confirmed the persisted Refine strategy on 2026-08-05. No further
interview question was necessary because the seed fixes the target, output,
evidence boundary, write scope, validation surface, and non-goals. Questions
that require another owner are retained as gaps rather than answered by Invoke.

## Inventory Lookup Record

- Mode: `lookup`
- Inventory root: `.arcanum/inventory/`
- Machine index: `index.json`
- Validation: `pass`, `lookup_readiness=ready`; 146 uncontrolled historical tag warnings do not affect lookup readiness
- Selected entry: `cyberalchemy-orchestrator-rwo-are-current-state-research-result-synthesis`
  - Effect: use the accepted current-state findings and their claim ceiling; do not reopen broad implementation discovery.
- Selected adjacent entry: `agent-reasoning-engine-contract-strategy-result-synthesis`
  - Effect: retain the semantic evaluator as separately versioned and non-authorizing; do not let its actor-kernel analogy redefine RWO ownership.
- Excluded adjacent taxonomy and generic Invoke entries: they do not close a recovery-model obligation more directly than the selected owner sources.
- Authority notice: Inventory is a discovery read model, not proof, design authority, or promotion.

## Definition Thesis

RWO recovery is a deterministic structural decision over an immutable
`RecoveryCase`. A domain supplies a versioned interpretation of its event, but
does not choose the lifecycle transition. RWO selects exactly one declared
`RecoveryDisposition` using a versioned `RecoveryPolicy` and a verified
`AcceptedHistorySlice`. The decision may schedule or suppress work, but it does
not decide domain truth, semantic truth, lifecycle acceptance, artifact
admission, authority, or external-effect outcome.

```text
accepted DomainEvent
  -> domain-owned pure RecoveryMapping
  -> DomainRecoverySignal

trusted structural observations + DomainRecoverySignal
  + RecoveryPolicy + AcceptedHistorySlice
  -> RecoveryCase
  -> RecoveryClassifier
  -> RecoveryDecision(RecoveryDisposition, identity transition, owner route)
```

## What This Capability Owns

The candidate recovery capability owns:

- normalization of declared recovery inputs into one immutable case;
- deterministic precedence over structurally comparable conditions;
- selection of one closed disposition;
- an explicit identity-transition declaration;
- attempt/round budget and fence checks delegated to their existing owners;
- a decision receipt that the ordinary RWO route may consume.

It does not own:

- the meaning or truth of a domain event;
- domain state or a domain's recovery mapping;
- accepted journal history;
- ARE semantic evaluation or observation admission;
- ACI command/effect-intent acceptance;
- artifact admission, authority, exact-effect permission, or adapter outcome;
- implementation, ontology promotion, or canonical definitions.

## Identity Model

| Identity | Stable scope | May change when | Must not imply |
| --- | --- | --- | --- |
| `work_ref` | immutable WorkDefinition version | new definition only | run, attempt, or authority identity |
| `work_run_id` | one invocation of one definition/input/authority basis | revalidation or genuinely new invocation | attempt success or domain outcome |
| `node_path` | structural position in expanded root plan | new graph/version or different position | inherited tools, context, budget, evidence, or authority |
| `round_id` | one bounded-repeat generation within a WorkRun | declared repeat decision | new WorkRun or implicit topology expansion |
| `attempt_id` | one execution attempt of one addressed node in one round | eligible new-attempt retry | message redelivery or changed definition/input/authority |
| `message_id` | one exact command/event envelope | new message only | new attempt or new business effect |
| `idempotency_key` | equivalence identity for exact accepted bytes in its declared scope | new command/effect identity | external-effect idempotency without owner evidence |
| `effect_intent_id` | one exact requested effect envelope | different envelope or separately accepted new intent | effect attempt or effect outcome |
| `effect_attempt_id` | one adapter attempt for one accepted effect intent | separately authorized adapter retry | successful, failed, or exactly-once effect |
| `history_cut_id` | one verified ordered journal cut plus reducer version | later accepted history or reducer version | completeness of unobserved domain/effect state |
| `recovery_case_id` | digest identity of normalized case inputs | any material case input changes | durable domain state or owner authority |
| `recovery_decision_id` | one classifier result for one case/policy version | new case or policy version | command acceptance or effect permission |

## Candidate Concept Registry

All IDs below are local candidates. They are not Definitions or Ontology Vault
promotions.

| Concept | Candidate ID | Type | Definition |
| --- | --- | --- | --- |
| RecoveryObservation | `rwo-recovery.RecoveryObservation` | Value Object | Immutable source fact with source identity, event/message digest, observed lifecycle/effect state, and freshness/fence references. |
| DomainRecoverySignal | `rwo-recovery.DomainRecoverySignal` | Value Object | Domain-owned interpretation of one accepted event, including typed failure/rework meaning, semantic constraints, confidence posture, and evidence refs; never a disposition. |
| RecoveryMapping | `rwo-recovery.RecoveryMapping` | Mapping | Versioned pure mapping from accepted domain event plus explicit domain-state/semantic references to `DomainRecoverySignal`. |
| AcceptedHistorySlice | `rwo-recovery.AcceptedHistorySlice` | Value Object | Journal-owner-verified cut containing relevant accepted facts, prior recovery decisions, budgets, fences, and pending delivery/effect references. |
| RecoveryPolicy | `rwo-recovery.RecoveryPolicy` | Policy | Versioned owner-supplied limits and eligibility rules for redelivery, attempts, rounds, reconciliation, compensation, terminal stops, and escalation. |
| RecoveryCase | `rwo-recovery.RecoveryCase` | Entity | Immutable classifier input aggregating subject identity, observation, domain signal, sameness tests, delivery/execution/effect states, policy, and history cut. |
| RecoveryClassifier | `rwo-recovery.RecoveryClassifier` | Service | Pure deterministic function that evaluates precedence and returns one `RecoveryDecision`. |
| RecoveryDisposition | `rwo-recovery.RecoveryDisposition` | Closed Enum | Structural treatment selected by the classifier; never a domain outcome or authority verdict. |
| RecoveryDecision | `rwo-recovery.RecoveryDecision` | Entity | Immutable decision receipt containing case/policy digests, disposition, reason, identity transition, required owner, fence/budget effects, and evidence refs. |
| AttemptFence | `rwo-recovery.AttemptFence` | Value Object | Trusted current-attempt/round marker preventing late observations from releasing current routes. |
| ReconciliationWork | `rwo-recovery.ReconciliationWork` | WorkDefinition role | Separately owned work that determines the outcome of an uncertain external effect without repeating it. |
| ExhaustionRoute | `rwo-recovery.ExhaustionRoute` | Policy reference | Declared terminal, compensation, or owner-escalation route used when limits are exhausted. |

## Closed Disposition Vocabulary

| Disposition | Meaning | Identity effect | Routing effect |
| --- | --- | --- | --- |
| `DEDUPLICATE` | Identical already-accepted bytes were observed again. | none | acknowledge/retain; no new work |
| `REDELIVER_SAME_MESSAGE` | Exact command was not accepted and delivery policy permits another delivery. | preserve run, round, attempt, message, key, and effect intent | deliver the same bytes only |
| `RETRY_NEW_ATTEMPT` | Known execution failure is retryable and sameness/budget/fence conditions hold. | same run and round; new attempt and new attempt-addressed commands | schedule one new Attempt |
| `REPEAT_NEW_ROUND` | Domain requests bounded rework and repeat policy permits it. | same containing WorkRun; new round and new child attempts | enter the declared repeat edge |
| `REVALIDATE_NEW_RUN` | Definition, normalized input, authority basis, effect envelope, or current applicability changed. | new WorkRun; fresh authority/admission receipts | invoke ordinary entry path |
| `RESUME_FROM_JOURNAL` | Runtime restarted while accepted history remains valid. | preserve run/round/attempt identities already recorded | rebuild cursor, then reconcile pending deliveries |
| `IGNORE_STALE_FOR_ROUTING` | Observation belongs to an older attempt, round, or run fence. | none | retain as diagnostic/history; release no edge |
| `RECONCILE_UNKNOWN_EFFECT` | External effect attempt outcome is unknown. | preserve original intent/attempt as unknown; create separately addressed reconciliation work if authorized | block repeated effect; route to effect owner/reconciler |
| `COMPENSATE` | A declared domain/effect policy selects explicit compensating work. | new compensation WorkRun correlated to original work/effect | propose declared compensation graph; never implicit rollback |
| `QUARANTINE_CONFLICT` | Same identity carries divergent bytes, impossible transitions, invalid schema/version, or contradictory trusted facts. | none | isolate and require conflict owner |
| `STOP_TERMINAL` | Permanent failure, cancellation completion, policy denial, or exhaustion has a declared terminal posture. | none | append terminal recovery decision; schedule no retry |
| `ESCALATE_OWNER` | Evidence is insufficient, mapping is ambiguous, or a required owner/policy is absent. | none by default | ask named owner; optional owner-review Work requires its own declared route |

The Design stage may narrow reason codes, but it may not add an open-ended
“retry” disposition or merge the twelve treatments without proving equivalence.

## Minimum RecoveryCase Contract

```yaml
recovery_case_id: digest(...)
subject:
  work_ref: work:name@version
  work_run_id: run-...
  node_path: root/...
  round_id: round-...
  attempt_id: attempt-...
  message_id: msg-... | null
  effect_intent_id: effect-... | null
  effect_attempt_id: effect-attempt-... | null
observation:
  source_ref: event-or-receipt
  source_digest: sha256:...
  observed_at: ...
  attempt_fence: ...
domain_signal:
  mapping_ref: domain:recovery-mapping@version
  signal_type: ...
  failure_class: ...
  rework_intent: none | requested
  semantic_receipt_ref: ... | null
sameness:
  definition_same: true | false | unknown
  normalized_input_same: true | false | unknown
  authority_basis_same: true | false | unknown
  effect_envelope_same: true | false | unknown | not_applicable
states:
  delivery: ...
  execution: ...
  effect: ...
history:
  history_cut_id: ...
  prior_decision_refs: []
limits:
  attempt_used: 0
  attempt_max: 0
  round_used: 0
  round_max: 0
  deadline_state: open | elapsed
policy_ref: rwo:recovery-policy@version
```

Unknown values are explicit. They never default to retry eligibility.

## Domain Interaction Contract

`RecoveryMapping` is a domain-owned, versioned, total mapping over its admitted
event types. It may:

- classify domain meaning such as transient resource unavailability, invalid
  request, requested rework, already-satisfied intent, or business rejection;
- identify domain invariants and required evidence;
- reference an admitted ARE semantic receipt when the domain contract requires
  reasoning;
- request compensation or owner review as domain intent.

It may not:

- allocate a WorkRun, Attempt, round, message, or effect attempt;
- reset a budget, advance a fence, or discard accepted history;
- select redelivery versus new Attempt versus new WorkRun;
- authorize an effect or claim that a stable message key makes the effect safe;
- let an ARE result, confidence score, or recommendation release a route;
- map an unknown/unsupported event to a permissive default.

Unsupported, stale, contradictory, or non-total mapping results become
`ESCALATE_OWNER` or `QUARANTINE_CONFLICT`, never automatic retry.

## ARE And ACI Boundary

ARE is optional to this model. When a domain mapping requires semantic
evaluation, the path is:

```text
separately owned reasoning-entry pass
  -> ACI-accepted addressed reasoning command
  -> verified history cut and admitted observations
  -> ARE semantic receipt
  -> separate artifact admission when applicable
  -> RecoveryMapping references the admitted receipt
```

The semantic receipt may influence `DomainRecoverySignal`; it cannot itself be
a `RecoveryDisposition`. ACI owns acceptance of lifecycle/effect intents and
the integrated journal boundary. Exact-effect and adapter owners remain
separate. An unknown effect outcome bypasses ordinary semantic retry analysis
and routes first to `RECONCILE_UNKNOWN_EFFECT`.

## Definition-Level Invariants

1. One case plus one policy version yields one decision byte-for-byte.
2. A decision cites the exact case, policy, mapping, history cut, reducer, and fence versions it used.
3. Unknown or contradictory required facts cannot produce redelivery, retry, repeat, revalidation, compensation, or an effect intent.
4. Same-message redelivery preserves exact bytes and the same idempotency identity.
5. A new Attempt cannot change definition, normalized input, authority basis, graph, or effect envelope.
6. A new repeat round consumes a declared bound and cannot silently change topology.
7. Changed definition, input, authority basis, or effect envelope requires a new WorkRun.
8. Historical replay and restart/resume do not create a new execution attempt by themselves.
9. Stale observations remain evidence but have zero routing effect.
10. Unknown effect outcome blocks another effect attempt until reconciliation or explicit owner decision.
11. Compensation is explicit Work with its own authority and evidence; it is never rollback inference.
12. Domain mapping, RWO classification, journal acceptance, ARE evaluation, ACI acceptance, artifact admission, exact-effect judgment, and adapter execution remain separately receipted.

## Definition-Scope Sanity Check

- Broadest layer: complete RWO recovery lifecycle.
- Selected coherent definition unit: `RecoveryCase -> RecoveryClassifier -> RecoveryDecision`, with `RecoveryMapping`, `RecoveryPolicy`, and `AcceptedHistorySlice` as owned inputs.
- Split pressure accepted: delivery mechanisms, adapter reconciliation, ARE
  semantics, domain mapping implementations, and ontology materialization are
  separate owner components.
- Recomposition: the selected unit consumes existing RWO identities/history
  and returns a structural decision to the ordinary route evaluator.
- Verdict: `pass` for definition authoring; s05 owns the formal Distill result.

## Dispatch Technique Trace

| Technique | Activation | Artifact/gate effect |
| --- | --- | --- |
| `sequence` | Define consumes the strict context pack and feeds review. | This artifact is the only s02 output consumed by s03. |
| `sentence_grammar` | The short operator request required structured scope. | Intent, target, outcome, constraints, and next route are explicit. |
| `frame_handoff` | Context Builder owns source selection. | Source context is referenced by pack handle, not recopied wholesale. |
| `mandatory_component` | Exact model needs a minimum typed vocabulary. | Identity table, concept registry, disposition enum, case contract, invariants, and gaps are mandatory sections. |
| `owner_boundary_check` | Recovery crosses domain/RWO/ARE/ACI/effect owners. | Every concept and operation names what it does not own. |
| `residue_ledger` | Four owner/evidence gaps are material. | They remain explicit and prevent mutation-capable readiness. |

Skipped at Define: `toy_game`, `tournament`, and full design selection; those
belong to s06–s08. The existing `REFINE-DISPATCH.json` is the full validated
dispatch, so no second dispatch document is needed.

## Layering Or Gap

Define emits no implementation-layering artifact. The required full layering
artifact belongs to Invoke Plan at s09. Until s09 and Distill validation pass,
mutation-capable readiness is blocked.

## Transport Report

- Observed capability: `invoke`, mode `define`.
- Target artifact: candidate RWO recovery definition owned by this Refine run.
- Upstream sources changed: none.
- Inventory changed: none.
- Canonical glossary/definitions changed: none.
- Target lifecycle status: candidate definition authored; design not yet accepted.
- Next owner: `interrogation:refine-review`.

