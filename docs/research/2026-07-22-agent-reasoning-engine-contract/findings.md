# Goal

Determine whether constitutions, Technique Catalog methods, risk-sensitive effort, tensioned subagents, semantic receipts, and gates can form a genuine pre-action reasoning engine; if so, state the smallest defensible candidate and its promotion conditions.

# TL;DR

The current repository is a governed dispatch/workflow coordination and read-oriented control plane, not a pre-action reasoning engine. Its catalog, dispatch validation, confirmation endpoint, selector, and protocol proposals organize work, but none owns an executable relation that decides whether a problem-level conclusion follows from admissible facts. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary)

The defensible first slice is **`semantic-judgment evaluator@1`**: a deterministic, replayable, finite, owner-authorized catalog evaluator that returns typed judgments and can abstain. It is an explicitly unwitnessed build/test candidate, not an implementation, promoted contract, or general reasoning-engine claim. The general/pre-action reasoning-engine label is **KILL** for this first slice; it becomes a candidate only if the promotion conditions below are met. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

# Context

The repository already has useful governed ingredients: route vocabulary and structural validation, proposed replayable runtime primitives, CAV2 gate and challenge semantics, and bounded effort-routing techniques. Yet the ingredients answer different questions—how work is shaped, what occurred, and who may move an action—and an inline review could not establish whether they jointly derive a justified conclusion before an effect. This dispatch therefore tested the missing semantic ownership, the actor/effect boundary, admissible local vocabulary, and a non-confidence-based effort policy. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion) [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)

## Converged model: three non-substitutable layers

```text
frozen AuthoritySnapshot + ProblemFrame + RuleCatalogManifest
                         |
                         v
      CAV2-D37 orchestration-entry GateDecision
                         |
                         v
       bounded actor-protocol kernel / RuntimeJournal
                         |
                         v
      semantic-judgment evaluator@1 (finite catalog reduction)
                         |
                         v
  ReasoningReceipt + semantic outcome (recommendation only)
                         |
                         v
       CAV2-D37 exact effect-execution GateDecision
                         |
                         v
                idempotent effect attempt
```

1. Full **CAV2-D37 gates** remain distinct entry and exact-effect decisions. The entry gate permits only a bounded run; the effect gate evaluates the exact action, target, scope, authority basis, evidence, risk/residue, and rollback or compensation boundary. A receipt or semantic recommendation is neither proof nor permission. [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion) [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)
2. The replayable **actor-protocol kernel** owns frozen inputs, commands, events, attempts, joins, timeouts, retries, effect idempotency, and closeout. It can replay what occurred without regenerating models or reissuing effects; it does not decide what conclusion follows. [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary)
3. The separately versioned **semantic evaluator** owns deterministic catalog applicability, admissibility, reduction, defeat, abstention, and the reasoning receipt. A model may propose observations or a plan, but cannot own the conclusion merely by emitting schema-valid prose. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness)

**Witness invariant:** entry `block` or `defer` produces zero actor and evaluator calls; entry `pass` permits only its bounded run. No effect occurs unless both the semantic outcome is positive and the downstream exact-effect Gate is `pass`.

## Candidate machine objects and invariants

The first witness may use the following **local candidate objects**. They do not receive CAV2 IDs and do not redefine canonical vocabulary. `TechniquePlan` and `EffortProfile` are local method/configuration records; `ReasoningLane` is omitted unless it demonstrates a unique operational distinction. `AntiBiasVector` is excluded. [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

| Object | Minimum job | Invariant |
| --- | --- | --- |
| `AuthoritySnapshot` | Freeze owner, authority posture, scope, applicable governed sources, expiry/revocation state | Model or search output cannot make an obligation applicable. |
| `ProblemFrame` | State question, candidate conclusions/actions, facts, evidence boundary, constraints, protected effects | It is not scope approval or an accepted premise. |
| `RuleCatalogManifest` | Name rule/evaluator digests, issuers, validators, precedence, challenge and temporal policy | No authority or self-judgment cycle. |
| `ApplicabilityDecision` | Record selector, scope match, conflicts, applicable rules/obligations, and residue | Applicability is owner-governed and reproducible. |
| `ObservationSet` | Hold typed, provenance-bearing facts | Every fact has admissible issuer and validator. |
| `TechniquePlan` / `EffortProfile` | Select catalog method, lanes, stopping and escalation shape | Effort never implies confidence, truth, readiness, or authority. |
| `ReasoningReceipt` | Bind inputs, digests, derivation, support, challenges, residue, and outcome | A receipt is not proof, approval, or promotion. |
| `RuntimeJournal` | Persist protocol events, attempts, joins, effects, and closeout | Replay emits no model/tool call or duplicate effect. |
| `GateDecision` × 2 | Preserve complete D37 records for entry and effect execution | Entry approval never silently authorizes an effect. |

The catalog must define: typed fact provenance; admissible issuer and validator; conclusion domain; applicability and precedence; required facts; grounded, well-founded defeaters; rule/effect-owned required lanes; challenge closure; unknown and temporal policy; digests, revocation, and expiry; and a prohibition on authority/self-judgment cycles. These are the substantive predicates that make a finite evaluator more than receipt-shaped model output. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

## Stable judgment algebra

For one registered conclusion under one manifest and snapshot, the evaluator returns exactly one typed outcome:

```text
InvalidInput
UnauthorizedCatalog
OutOfDomain
Ineligible.Defeated
Deferred.Insufficient
EscalateOwner
RecommendedUnderSnapshot     # non-authorizing
Invalidated
```

`RecommendedUnderSnapshot` means only that the registered conclusion follows from the captured, admissible observation set under the named evaluator and catalog. It cannot replace the D37 verdict vocabulary or grant authority. Unknown is not silently favorable: insufficient facts, an unclosed required challenge, unresolved ownership, invalid catalog status, or temporal drift produce typed deferral/escalation/invalidity rather than recommendation. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion) [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)

## Effort is a controller, not evidence

Hard overrides are derived from an owned policy/effect binding—not model self-report. Missing owner, required evidence, exact effect binding, or a resolvable material conflict blocks or defers. Protected action, high authority impact, irreversibility, or broad external mutation requires T4; unknown never defaults to low. Removing evidence or downgrading a required lane must never improve the outcome. [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)

| Tier | Purpose and method shape | Permitted result |
| --- | --- | --- |
| T0 | Preflight: frame, concrete evidence handles, owner boundary, residue | Read-only/draft only |
| T1 | Bounded analysis: one small route with stopping and recomposition | Narrow recommendation/draft; ordinary owner gate still applies |
| T2 | Inspect/test first witness: sequential explorer/auditor, fixture and validation | Eligibility only if required evidence lanes pass |
| T3 | Contested dialectic/tournament: distinct explorer/skeptic roles, declared joins and convergence cap | Recommendation plus challenge/residue; never effect permission |
| T4 | Protected effect: protected-action mapping, exact scopes, validation, separate effect gate | Effect only on exact-bound Gate `pass` |

Tensioned subagents are useful at T3 only when they add a discriminating challenge or alternative; consensus, agent count, and token use do not increase authority. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)

## Counterfactual witness family

The initial build/test candidate must register one conclusion and rule, then vary only the evidence or catalog condition:

| Fixture | Required result |
| --- | --- |
| Supported facts | `RecommendedUnderSnapshot` |
| Required fact removed | `Deferred.Insufficient` |
| Grounded defeater added | `Ineligible.Defeated` |
| Required challenge times out | `Deferred.Insufficient` |
| Irrelevant consensus added | Outcome unchanged |
| Rule removed | `OutOfDomain` |
| Catalog mutation, expiry, revocation, cyclicity, or self-judgment | Reject, invalidate, or typed escalation as specified |

The suite must also run a second independently authored rule family/frame through unchanged evaluator code. This proves a catalog evaluator rather than a fixture-specific conditional and makes unsupported, schema-valid model agreement rejectable. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary)

## Replay and effect boundary

Historical protocol/semantic replay reduces retained immutable facts into the same state and outcome; it does not re-run a mutable model. Current revalidation is different: it recomputes against current authority/catalog/evidence state. Scope expansion, late material defeat, revocation, or expiry invalidate the prior result and require recomputation. Post-effect invalidation opens an incident/compensation route, not retroactive authorization. [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

The observable effect invariant is deliberately small: with an identical fixed effect envelope, `RecommendedUnderSnapshot` plus an exact CAV2-D37 effect-gate pass causes exactly one test-double attempt; every other evaluator outcome causes zero; repeated positive delivery remains one logical effect. This is a boundary witness, not evidence that the repository has implemented an effect runtime. [Agent 2](research.md#agent-2--replayable-actor-protocol-and-effect-boundary) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

## Typed residue and non-promotion boundary

`AntiBiasVector` has a precise role as typed residue: its absence does not block the generic evaluator witness, but it blocks claims of an anti-bias engine, bias cancellation, or independent evidence. Contestability instead uses named challenge techniques and a CAV2-D40 challenge contract, which supplies review routing rather than truth, confidence, or authority. [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion) [Agent 4](research.md#agent-4--adaptive-effort-routing-and-stopping-policy)

Likewise, a deterministic reducer can establish only the narrow derivation claim over captured premises under a named version. It cannot establish real-world truth, premise truth, implementation safety, promotion, or gate authority. Research does not promote definitions, an ontology, a runtime contract, or public material; DomainSpec/CAV2 private authority remains private and Arcanum publication boundaries remain intact. [Agent 1](research.md#agent-1--formal-semantic-contract-and-rejectable-inference-witness) [Agent 3](research.md#agent-3--canonical-semantic-admissibility-and-non-promotion)

## Final verdict matrix and reviewer convergence

| Claim | Current status | Why |
| --- | --- | --- |
| Current checkout is a reasoning engine | KILL | Dispatch/control-plane and proposed protocol layers lack repository-owned semantic reduction. |
| General pre-action reasoning engine, first slice | KILL | Needs broader witnesses and owner admission; do not use the label. |
| `semantic-judgment evaluator@1` build/test candidate | UNWITNESSED CANDIDATE | Narrow finite evaluator can be deterministic, replayable, owner-authorized, and typed-abstaining, but this remains a research contract without executable witness evidence. |
| Replayable actor protocol | Candidate design | Useful independent layer; not evidence of semantic inference. |
| `AntiBiasVector` efficacy | KILL for first slice | No governed dimensions, interventions, or validation semantics. |

Lakatos, Gödel, and Quine initially returned REVISE/KILL against the current fixture and general label. After the separation of kernel/evaluator/gates, typed abstention and defeat, counterfactuals, exact effect behavior, and non-promotion limits, all returned PASS **as a research contract**. This does not claim implementation. The registration residue is also non-semantic: the canonical implementation appender accepts `synthesizer`, while the installed `.claude` projection is stale and rejected it. That is tooling projection drift, not engine evidence.

## Promotion conditions: evaluator to reasoning-engine candidate

Do not promote the claim until all conditions hold:

1. Positive, negative, abstention, defeat, timeout, consensus-invariance, no-rule, catalog-mutation, expiry, revocation, cyclicity, and self-judgment fixtures pass.
2. Two independently authored rule families/frames run through unchanged evaluator code.
3. An exact effect fixture proves one positive effect, zero effects for every non-positive outcome, and one logical result under repeat delivery.
4. Deterministic historical replay and drift-sensitive current revalidation both work.
5. Scope, late-defeat, lane, evidence, and authority changes cannot improve or silently preserve the result.
6. Entry and effect gates retain full D37 records in persisted order: the entry `GateDecision` precedes the first actor/evaluator event, and the effect `GateDecision` follows the semantic receipt.
7. Applicability and challenge closure are executable or explicitly pinned as remaining residue.
8. The spec owner and decision gate admit the candidate claim.

## Connections

- `derives-from` → [research.md](./research.md)

## Open Questions

- **OQ-1 (BLOCKER)** — Which owner supplies executable applicability, precedence, exception, contradiction, and stale-rule semantics for `AuthoritySnapshot`/`ApplicabilityDecision`? Recommendation: define the owner route and pinned source selector before evaluator implementation. Owner: authority-model owner.
- **OQ-2 (BLOCKER)** — Is challenge closure executable for the initial catalog, including timeout and late-material-defeat handling? Recommendation: select one bounded CAV2-D40-compatible closure policy and expose it in fixtures. Owner: challenge-contract owner.
- **OQ-3** — Should `MayAct` remain only an internal gate criterion or name a fully conformant narrow gate? Recommendation: retain the full D37 records while the decision is unresolved. Owner: decision-gate owner.
- **OQ-4** — What durability/admission posture applies to reasoning receipts and runtime journals? Recommendation: keep them local candidate artifacts until the artifact/canonical-kind route decides otherwise. Owner: artifact-admission owner.
- **OQ-5** — Does `ReasoningLane` add a distinct operational or validation role in the first witness? Recommendation: omit it unless a concrete fixture proves unique value. Owner: spec owner.
