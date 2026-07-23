## Agent 1 — formal semantic contract and rejectable inference witness

## Initial position (verbatim)

At the current checkout, `projects/cyberalchemy-orchestrator` is not a pre-action reasoning engine. It owns orchestration governance, operational projections, confirmation handoff, and narrow agent-selection semantics, but it does not own a relation that transforms a problem-level semantic frame into a justified action judgment.

The smallest credible upgrade is not a general theorem prover or full claim graph. It is a versioned, executable judgment calculus with four linked objects:

`ProblemFrame → TechniquePlan → ReasoningReceipt → ActionPredicate`

The decisive non-vacuity condition is that a repository-defined evaluator can reject a syntactically valid but semantically unsupported model conclusion.

## Final position after confrontation

Hewitt’s replayable runtime and this semantic contract are complementary but have different owners. The kernel owns commands, events, attempts, joins, effects, idempotency, and closeout; replay proves what occurred, not that a conclusion followed. A semantic evaluator must separately own admissibility and reduction. A model may remain a declared synthesis actor, but recording its prompt and receipt does not transfer inference ownership to the repository.

Hewitt also exposes an ambiguity in my original `MayAct`: semantic recommendation and external-effect authorization must be separate. When reasoning materializes an action not knowable at entry, authorization may validly occur after the recommendation.

Tarski’s boundaries hold: a receipt is neither proof nor approval; effort, agent count, and token count imply neither confidence nor authority. `ProblemFrame`, `TechniquePlan`, `ReasoningReceipt`, and gate records may begin as non-authoritative local schemas composing existing intent, evidence, provenance, challenge, and residue concepts. No new canonical definitions are required for the minimum fixture.

`AntiBiasVector` is not required for the generic reasoning-engine witness. It likely is required before claiming that this repository’s distinctive anti-bias mission is semantically enforced. Model-mediated technique selection qualifies only if repository-owned applicability and composition predicates can reject an inapplicable but schema-valid plan.

## Evidence-backed findings

1. The scientific claim/probe/enrichment loop is explicitly unbuilt; today’s implementation is dispatch discipline plus a control plane (`projects/cyberalchemy-orchestrator/README.md:49-60`). The server says the surrounding Claude session still runs `check-tension → register-dispatch → agents`; its own confirmation endpoint only writes a marker (`projects/cyberalchemy-orchestrator/implementations/server/main.py:1-11`, `:229-271`).

2. Dispatch Spec validates route shape and explicitly does not choose capabilities (`.agents/skills/dispatch-spec/SKILL.md:22-31`, `:73-102`). The technique catalog says it is not an execution engine (`.claude/skills/dispatch-spec/TECHNIQUE-CATALOG.md:3-5`). Neither defines when premises support or defeat a conclusion.

3. The existing selector owns only meta-level inference: deterministic tag/role ranking (`projects/cyberalchemy-orchestrator/tools/agent-pool-mcp/src/select.mjs:36-61`) plus optional model judgment constrained to persona names and vocabulary (`tools/agent-pool-mcp/src/adjudicate.mjs:12-87`). It determines who should reason, not what follows about the problem.

4. The claim graph is the closest semantic seed—assertion types, premise/contradiction edges, decompositor, and proposed veracity propagation—but calls the working part expensive and unverified and leaves well-formedness and ownership open (`projects/cyberalchemy-orchestrator/vault/hypothesis/claim-graph.md:28-76`, `:96-121`). The planned kernel deliberately never decides which answer is better (`projects/cyberalchemy-orchestrator/docs/PLAN.md:179-188`).

## Minimal formal contract

Candidate local types:

\[
F=\langle question,premises,evidence,constraints,candidateActions,protectedActions\rangle
\]

\[
S=\langle F,\Pi,cursor,K,T,status\rangle
\]

where `Π` is a technique-plan DAG, `K` typed judgments, and `T` an append-only structured trace.

Each versioned technique has repository-owned semantics:

\[
\llbracket\tau\rrbracket_R(F,K)\rightarrow(J,r)
\]

Receipt `r` records the frame hash, cited premises/evidence, technique and evaluator versions, deterministic/model boundary, proposed judgment, challenges, residue, and validation results.

A transition occurs only when:

\[
Admissible_R(F,K,J,r)
\]

Otherwise the engine blocks or abstains. A repository reducer derives:

\[
Reduce_R(F,\Pi,K,T)=O
\]

Semantic recommendation:

\[
Recommend_R(a)\iff Supports_R(O,a)\land EvidenceSufficient_R(T,a)
\land NoUndefeatedContradiction_R(T,a)\land GovernanceValid_R(T,a)
\]

External effect authorization:

\[
PermitEffect_R(a,auth,state)\iff Recommend_R(a)
\land AuthorizationValid(auth,a,state)\land RuntimePreconditions(state,a)
\]

The runtime kernel owns execution receipts after `PermitEffect`; it does not own the semantic conclusion. A model-selected plan or judgment counts as repository-owned only if substantive predicates—not JSON conformance alone—can reject it.

## Fixtures

**Positive:** Frame the question “How may this project be described now?” with alternatives `reasoning_engine` and `read_orchestration_control_plane`, using the witnesses above. An `x_ray → concrete_path_evidence → reasoning_engine_witness → validation_loop` plan derives `Recommend(read_orchestration_control_plane)=true` and rejects the stronger label. Publishing or editing remains unauthorized until a separate effect authorization exists.

**Negative/control:** On the same frame, inject a schema-valid model receipt: “Multiple agents agreed; therefore this is a hybrid reasoning engine.” It supplies no rule connecting consensus to the witness and conflicts with the missing semantic path. Structural validation may pass, but `Admissible=false`; no later authorization may repair the unsupported conclusion. Acceptance would prove that the model or panel still owns inference.

## Residue and claim/proof limits

Open synthesis decisions are the minimum substantive `Admissible` relation, whether the first release stops at recommendation or integrates post-result effect authorization, and whether `AntiBiasVector` is mandatory only for the stronger decision-hygiene claim. Belief revision, knowledge promotion, and a full claim graph remain stronger capabilities, not minimum prerequisites.

This was read-only source inspection; no dependencies or runtime tests were run. The prior research froze `ca560b…`; the current parent checkout reported `d0b7368…`, while the target directory was untracked, so current line evidence is not a commit-addressable tracked subtree. Absence claims exclude reasoning performed by external sessions. This calculus is a candidate contract, not an implementation, proof of soundness, promoted definition set, or mutation authority.

## Agent 2 — replayable actor protocol and effect boundary

## Initial position (verbatim)

The repository can support a replayable **orchestration engine** from its owned primitives, but not a repository-owned semantic reasoning engine. The executable core should be a deterministic actor protocol: immutable confirmed spec, authenticated commands, append-only runtime events, per-lane agent attempts, bounded joins, explicit timeout/partial-failure events, receipt-gated handoffs, action authorization, and idempotent closeout.

The model remains an external reasoning actor. The kernel may schedule it, freeze its inputs, persist its outputs, validate their shape, and block effects; it must not pretend that transport, voting, or replay derives the model’s semantic conclusion.

At the frozen target commit `ca560b866b16440b3186f960ecc41d91e42dd03a`, most of this protocol exists as a coherent target design plus Dispatch Spec validation contracts. It is not yet an integrated runtime.

## Final position

The defensible target is a two-layer engine:

1. A deterministic **actor-protocol engine** owns identity, immutable inputs, lane isolation, authorization, lifecycle events, bounded joins, retries, timeouts, receipts, effect blocking, and closeout.
2. A separately versioned **judgment-calculus layer** owns executable technique semantics: typed observations and evidence enter; unsupported output is rejected; a traceable reasoning receipt and semantic action predicate emerge.

The protocol reducer derives run/group/attempt state. A semantic evaluator derives judgments under repository-owned rules. The kernel records and gates the evaluator’s result but does not silently become an authority on truth.

A semantic `MayAct`-like predicate is only a recommendation. External action additionally requires authorization bound to the exact spec/result/action/tool/target/scope digests. If those details were not frozen at entry, a separate action authorization is required.

`ProblemFrame`, `TechniquePlan`, `ReasoningReceipt`, and `ActionPredicate` are provisional runtime-schema roles here, not canonical definitions. Effort, agent count, agreement, and receipts do not imply confidence, proof, approval, or authority.

## Evidence-backed findings

1. The current server does not execute dispatches. `projects/cyberalchemy-orchestrator/implementations/server/main.py:1-11` delegates execution to a watching Claude session; `:229-271` only writes an idempotent confirmation marker. `implementations/server/ledger.py:95-221` parses and joins opening/close rows.

2. The constitution supplies useful topology but not replay evidence. `implementation/domainspec/internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md:61-78` defines dependency-ready groups, parallel independent lanes, and bounded connections; `:132-150` defines frozen confirmation, partial-result propagation, and approval. But `:44-47` explicitly provides no event log, while `:430-461` retains only terminal reason and spawn aggregates.

3. Dispatch Spec validates executable shape but does not run it. `arcanum/formulae/dispatch-spec/CAPABILITY-BOUND-DELEGATION.md:63-109` assigns spawn/join/gate/close ownership to a parent runtime and says native integration proof remains pending. `arcanum/formulae/dispatch-spec/dispatch.schema.json:302-400` and `:455-565` define waves, authorization, timeout labels, receipts, residue, and reroute.

4. The target infra proposal contains the missing protocol design. `projects/cyberalchemy-orchestrator/docs/features/agents-communication-infra/README.md:318-436` separates commands, events, outbox effects, CAS transitions, and group states; `:438-477` defines idempotent attempts and reconciliation; `:533-626` defines isolated lane phases and event/message envelopes; `:987-1040` defines replay without model regeneration.

5. The publication probe proves durable, idempotent message acceptance—not orchestration or inference. `.../bus-publication-probe/src/bus.mjs:141-237` persists before issuing verifiable receipts, but exposes no scheduler, reveal/read protocol, join, timeout, or semantic reducer.

## Minimal runtime protocol

1. A strategist proposes a typed problem frame and versioned technique plan. Each technique declares input/output schemas, lane roles, required receipts, join and missing-lane policy, evaluator version, and falsifier.
2. Dispatch validation checks topology, capabilities, scopes, gates, and receipts. Human approval binds the immutable plan and authorized action envelope.
3. `run.created` and an opening outbox entry are journaled. No agent or effect begins until the official opening row is acknowledged.
4. Each seat receives a frozen content-addressed snapshot and scoped capability. Retries retain `operation_id` and create new `attempt_id`s. Peer content remains sealed until a persisted reveal event.
5. Model/tool outputs become immutable observations. Deadline, cancellation, retry, replacement, and human decisions become events before affecting state.
6. The protocol reducer applies the predeclared all/quorum/deadline rule. Missing required receipts block; optional absence remains explicit residue.
7. The semantic evaluator consumes the exact frozen observation set and emits a reasoning receipt containing evaluator digest, inputs, support, challenge, missing-lane residue, conclusion, and falsifier result. Fluent unsupported prose must yield rejection or `insufficient_support`.
8. The effect broker requires both a positive semantic predicate and exact authorization. Effects use idempotency/outbox handling; ambiguity for non-retryable effects becomes `effect_unknown`.
9. One terminal event wins; close materialization reconciles idempotently and preserves per-lane attempts, receipts, semantic result, authorization/effect outcome, and residue.

Protocol replay reduces persisted facts into the same lifecycle state without reissuing commands or effects. Semantic replay reduces the recorded evaluator event. Independent semantic revalidation is possible only when the evaluator is deterministic over retained immutable inputs; neither replay regenerates model output.

## Partial-failure and authorization fixture

Freeze two evidence lanes, one required challenge lane, a deterministic evidence-support evaluator, and an action envelope. Lane A returns cited support; lane B returns fluent unsupported prose; the challenge lane times out.

Persist `deadline.fired`. Reject B semantically despite its valid publication receipt. Because the required challenge receipt is absent, emit a partial reasoning receipt with `insufficient_support`, derive `ActionPredicate=deny`, and block the effect even if an earlier human approval exists. Repeated deliveries remain logically unique.

Crash after each journal/outbox boundary and restart. Replay must produce the same state hash without calling a model or tool. A late challenge result remains an audited late observation and cannot rewrite the committed result; reevaluation requires a new version. Close once with named timeout and unsupported-output residue.

The positive control supplies all required support, derives `allow`, still blocks without exact effect authorization, and executes one logical effect after authorization despite repeated delivery.

## Residue and claim/proof limits

- Join labels such as `quorum`, `ranked`, `pareto`, and `parent_synthesis` still lack versioned executable semantics.
- The one-entry-human-gate rule conflicts with actions whose scope emerges only after reasoning.
- `AntiBiasVector` is a promising first executable technique, but would prove designed opposition—not statistical independence or conclusion quality.
- A model-only “semantic evaluator” remains delegated judgment unless repository code can reject unsupported output under inspectable rules.
- This is read-only analysis of clean commit `ca560b866b16440b3186f960ecc41d91e42dd03a`. No runtime integration, semantic calculus, replay, sealing, or effect enforcement is claimed as implemented.
- Research may propose runtime types and tests; it does not promote definitions, ontology, specifications, or authority.

## Agent 3 — canonical semantic admissibility and non-promotion

## Initial position (verbatim)

The proposed pre-action reasoning engine is semantically admissible only as a **non-authoritative, build-from-owned composition**. None of the eight labels appears as an active definition or alias in `DEFINITIONS.md` / `DEFINITIONS-INDEX.md`.

Most labels can serve as local record fields or spec-candidate object names assembled from existing governed semantics. They should not be promoted as new primitives merely because the engine benefits from naming them. `AntiBiasVector` is the clearest genuine semantic gap; `ApplicableObligations` and `ReasoningLane` contain conditional gaps if they are expected to make binding applicability or routing decisions.

No label should presently receive a new CAV2 ID or be represented as already canonical.

## Final position

The first credible witness should be a **versioned, two-layer spec candidate**: a replayable orchestration envelope plus a repository-checkable semantic-judgment envelope. Model synthesis remains a candidate input; versioned techniques and reducers produce typed judgments; a `ReasoningReceipt` records premises, applicable rule references, derivation, evidence strength, challenge routes, and residue; `CAV2-D37` gates—not the receipt, reducer, or consensus—decide movement.

The witness needs two separate instances of the same gate primitive:

```text
GateDecision(scope = orchestration_entry, ...)
GateDecision(scope = effect_execution, effect_target = ..., ...)
```

The entry gate authorizes only a bounded run under a named spec, actors, budget, and evidence boundary. The effect gate separately evaluates the exact mutation, target, authority basis, evidence, risk/residue, and rollback or compensation boundary. These are gate scopes, not new authority kinds. Entry confirmation must never silently authorize effects.

`MayAct` is admissible only as an internal criterion consumed by a gate, or as a narrow gate specialization that retains the complete `pass | flag | block | defer` record. A standalone Boolean would duplicate and weaken `CAV2-D37`.

A runtime receipt may carry a checked semantic derivation without becoming authority. The derivation may support the narrow claim “conclusion C follows from captured premises P under reducer version R.” It does not thereby prove the premises, real-world truth, implementation safety, or authorization. The gate still decides movement.

`AntiBiasVector` is excluded from the first witness. Neither bias classes, vector dimensions, aggregation, intervention efficacy, nor validation semantics are governed. Contestability should instead use a `CAV2-D40` challenge contract and named, evidence-bounded challenge techniques.

## Governing selectors

1. `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d21-four-facet-action-method` — every consequential action binds classification, schema, human-continuation, and machine-checkable views, or records typed residue. Machine-checkability is not proof or authority.
2. `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d23-authority-lifecycle-axis` — effort, status, evidence, commitment, provenance, owner, and authority must not silently stand in for one another.
3. `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d37-gate` — owner, scope, inputs, criteria, evidence, verdict, residue/risk, record location, and downstream effect govern both entry and effect authorization.
4. `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md#cav2-d38-claim-proof-bound` and `#cav2-d40-challenge-contract` — derivation claims cannot exceed support, and challenge machinery is a review path rather than a verdict or confidence axis.
5. `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md#cav2-c3-research-before-specification`, `#cav2-c9-validation-before-implementation`, and `#cav2-c18-artifact-admission-before-mutation` — research cannot self-promote into runtime; implementation needs an approved route; durable artifacts trigger admission review. The constitution and C18 retain their recorded candidate posture.

## Term admissibility

| Label | Admissible first-witness use | Boundary |
|---|---|---|
| `ProblemFrame` | Local schema over `CAV2-D39 Intent`, premises, evidence boundary, and residue | Not a requirement, accepted premise, spec, or scope approval |
| `ApplicableObligations` | Derived projection with selector, source, authority posture, scope-match reason, conflicts, and residue | Search/model selection does not make an obligation applicable |
| `TechniquePlan` | Action-specific instance of `CAV2-D32 Method` with versioned techniques, validation, stopping, and fallback | Not a new method primitive or authority |
| `EffortProfile` | Optional budget, depth, tool, timeout, and escalation configuration | Cannot imply evidence confidence, correctness, readiness, or authority |
| `ReasoningLane` | Optional `CAV2-D21` classification only if it adds a unique operational distinction under `CAV2-D22` | Not an authority kind or synonym for method, owner, effort, or queue |
| `ReasoningReceipt` | Premises, rule refs, technique/reducer versions, typed judgments, derivation, provenance, challenge, support strength, and residue | Not global proof, promotion, authority, or gate verdict |
| `ActionGateDecision` | Full `CAV2-D37` record; may reference separate entry and effect gate decisions | Not Boolean-only permission; `MayAct` remains subordinate |
| `AntiBiasVector` | Excluded | No governed construct or warranted anti-bias efficacy claim |

## Conservative governed composition

```text
OrchestrationEntryGate
  -> versioned EngineSpec and bounded run
  -> model/adapters propose ProblemFrame
  -> ApplicableObligations projection
  -> TechniquePlan + EffortProfile + optional ReasoningLane
  -> versioned typed judgments and deterministic reducer
  -> ReasoningReceipt with derivation, support, challenge, and residue
  -> ActionGateDecision under CAV2-D37
  -> EffectGate for the exact target and rollback boundary
  -> effect attempt
  -> event/effect receipt, validation, retry, closeout, or residue
```

Replay can reproduce deterministic reduction over captured inputs. Re-invoking a mutable model is a new attempt, not semantic replay. Idempotency and successful execution are operational properties, not authority.

Owner routes remain distinct:

- research establishes technique/reducer semantics, limits, and evidence classes;
- constitution-governance and the authority-model owner govern obligation applicability, precedence, and authorization scope;
- definitions-governance acts only if local labels become load-bearing cross-surface vocabulary;
- spec owner plus decision-gate promote a runtime contract;
- task-session or equivalent executes implementation under `CAV2-C9`;
- the effect owner authorizes the exact mutation;
- artifact/canonical-kind owners admit durable receipts or new artifact trees;
- challenge owners resolve contested judgments without allowing receipts to self-amend authority.

## Remaining residue

- Applicability still lacks owned selector precedence, exception, contradiction, and stale-rule semantics.
- `MayAct` still needs a decision on whether it is merely a gate criterion or the name of a fully conformant narrow gate.
- Each technique must state whether it validates shape, derivation, evidence sufficiency, contradiction freedom, or domain truth.
- Semantic replay must distinguish reducer replay from a fresh model attempt.
- `ReasoningReceipt` durability and artifact posture remain unresolved.
- `ReasoningLane` should be omitted unless it proves a unique routing or validation distinction.
- The narrower effect gate must define whether `flag` permits execution with named risk or only continued review.

## Forbidden authority claims

Do not claim that checked-in reducer code is authoritative; deterministic reduction proves real-world truth; replay, consensus, joins, or agent count constitute inference or proof; an immutable spec is canonical or promoted; a receipt becomes authority by containing a derivation; `MayAct` replaces the full gate or owner route; entry authorization covers effects; idempotent or successful effects retroactively supply authorization; gate scopes create new authority kinds; model/search output makes obligations applicable; more effort implies stronger evidence; `AntiBiasVector` measures or removes bias; schema conformance automatically passes a gate; or this research promotes any definition, constitution, spec, runtime contract, canonical kind, authority kind, implementation task, or public/private movement.

## Agent 4 — adaptive effort routing and stopping policy

### Position

Use a risk-sensitive controller that selects the cheapest route capable of exposing consequential uncertainty. Effort is not confidence, proof, readiness, or authority.

The candidate engine should separate:

1. a deterministic protocol kernel for immutable inputs, routes, receipts, and residue;
2. a versioned semantic evaluator returning `Recommend | Eligible | Ineligible | Deferred`;
3. an authorization layer applying a separate CAV2-D37 Gate to the exact action/spec/tool/target/scope.

`Eligible` never means effect permission. The first witness excludes `AntiBiasVector`; objections use CAV2-D40 Challenge Contract semantics where needed. `ProblemFrame`, `TechniquePlan`, `EffortProfile`, `ReasoningLane`, `ReasoningReceipt`, and `ActionGateDecision` remain local candidate schema labels.

### Evidence findings

1. The Technique Catalog is route vocabulary, not an execution engine or promotion grant. `authority_split_gate` blocks unresolved ownership; `protected_action_mapping` requires protected class, policy owner, and failure behavior.<br>
   Evidence: `.claude/skills/dispatch-spec/TECHNIQUE-CATALOG.md`, selectors `Boundary And Evidence Techniques > Boundary` and `Use Rule`, lines 75-85 and 119-122.

2. Existing techniques already cover bounded reduction, critique, validation, evidence handles, and residue. `zig_zag` requires stopping conditions; `dialectic` requires convergence; `tournament` requires elimination criteria and rejected alternatives.<br>
   Evidence: same catalog, selector `Arcanum Dispatch Techniques`, lines 18-37.

3. CAV2-D37 Gate requires owner route, scope, inputs, criteria, evidence, residue, record location, downstream effect, and verdict `pass | flag | block | defer`; it is not proof or unrecorded permission.<br>
   Evidence: `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md`, selector `CAV2-D37: Gate`, lines 2364-2419.

4. CAV2-D40 supplies contestability without adding confidence or authority: challenge modes, contradiction/validation links, owner, resolution Gate, blocking questions, and residue route.<br>
   Evidence: same definitions file, selector `CAV2-D40: Challenge Contract`, lines 2553-2618.

5. `reasoning_effort` is not a current register-dispatch field; unknown keys are rejected. Runtime controls do include native roles, declared `agent_count`, target/mode/input refs, write and forbidden scopes, waves, join policy, `gate_after`, and receipts.<br>
   Evidence: `implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/register-dispatch/SKILL.md`, selectors `The dispatch row` and field tables, lines 27-96; `.agents/skills/orchestrate/SKILL.md`, selector `<process>`, lines 23-33.

### Controller

Candidate inputs, each `low | medium | high | unknown`, with evidence/reason:

- risk;
- uncertainty;
- novelty;
- reversibility;
- authority impact;
- evidence gaps;
- action scope/blast radius;
- conflict state.

Universal preflight also binds raw intent, exact action/spec/tool/target/scope, evidence handles, owner route, effect class, and protected status.

Hard overrides precede scoring:

- unresolved owner, missing required evidence, unbound effect, or unanswerable material conflict → `block/defer`;
- protected action, high authority impact, irreversible effect, or broad external mutation → T4;
- high risk, uncertainty, novelty, low reversibility, or active conflict → at least T3;
- `unknown` escalates or becomes blocking residue; it never defaults to low.

Otherwise select the lowest tier covering every non-low input.

### Tiers

| Tier | Exact catalog techniques | Supported shape | Result/action |
|---|---|---|---|
| T0 preflight | `sentence_grammar`, `minimum_component_catalog`, `concrete_path_evidence`, `owner_boundary_check`, `residue_ledger` | Direct native execution; no subagent | Frame, cited handles, residue; read-only or draft only |
| T1 bounded analysis | `scu_swu_reduction`, `sequence`, `frame_handoff`, `artifact_contract_bridge`, `recomposition_proof` | Direct execution or one bounded native role with input refs and forbidden write scope | Narrow recommendation/draft; ordinary owner Gate still applies |
| T2 inspect/test | `x_ray`, `toy_game`, `validation_loop`, `execution_receipt_handoff`, `evidence_receipt_link`, `assessment_failure_reference` | Sequential explorer then auditor; explicit receipts and `gate_after` | `Eligible` only if required evidence lanes pass |
| T3 contested | `dialectic` or `tournament`, bounded `zig_zag`, `authority_split_gate`, `approval_semantics_map`, `handle_handoff`, `evidence_summary_handoff`, `residue_ledger` | Distinct explorer/skeptic roles then synthesizer; declared counts, waves, joins, receipts, convergence cap | Recommendation plus challenge/residue record; no effect permission |
| T4 protected effect | `protected_action_mapping`, `authority_split_gate`, `approval_semantics_map`, `validation_loop`, `execution_receipt_handoff`, `state_namespace_boundary`, `concrete_path_evidence` | Pre-action route followed by separate effect Gate; exact scopes and forbidden scopes; post-Gate dependency | Effect only on exact-bound Gate `pass`; `flag` cannot silently execute |

Use `tournament` only for real alternatives and `dialectic` only for an actual conflict.

### Adaptation and stopping

Escalate when scope expands, evidence becomes non-concrete, validation fails, contradiction appears, reversibility falls, or a new authority boundary is crossed. Add the missing discriminating lane, not automatic agents or tokens.

De-escalate only after recorded change: narrower/read-only scope, verified effect binding, resolved evidence gap, or conflict closed by its owner Gate. Agreement or model confidence is insufficient.

Stop on unresolved owner; missing required evidence; action/spec/tool/target/scope mismatch; absent protected-action control; unresolved material challenge; failed validation without safe repair; broken receipt dependency; or critique-loop cap. Return `block/defer`.

Orchestration-entry and effect-execution are separate Gates. The first may authorize investigation; only the second may authorize the bound effect.

### Routing examples

1. Locate a confirmation record read-only: T0, concrete paths, no fan-out.
2. Correct one private draft document: T1, smallest coherent edit and recomposition check.
3. Test whether an unsupported conclusion is rejected: T2, `toy_game` fixture plus `validation_loop`, explorer→auditor receipts.
4. Choose between competing semantic reducers: T3, `tournament` with criteria and rejected-candidate residue.
5. Publish public Arcanum material, deploy, or mutate tenant state: T4; map protected class and owner, validate exact effect, then require effect-Gate `pass`.

### Failure residue and limits

Local residue types: `risk-classification-undershoot`, `required-evidence-gap`, `authority-owner-unresolved`, `action-binding-mismatch`, `challenge-unresolved`, `semantic-witness-failed`, `receipt-chain-broken`, `convergence-cap-reached`, `non-informative-escalation`, and `protected-control-missing`. Each carries source, affected action, owner, repair route, and blocking status.

Underthinking means routing past blocking residue. Overload means adding orchestration without a new criterion, evidence source, or falsifier.

This is a candidate controller, not an implemented engine, promoted ontology, or proof that more deliberation improves correctness. The catalog proves available route vocabulary, not efficacy. CAV2-D37 proves Gate structure, not a candidate implementation. CAV2-D40 supplies challenge routing, not truth or an `AntiBiasVector`. The first witness should prove only deterministic reduction over recorded inputs, rejection of unsupported conclusions, typed insufficiency/conflict residue, and refusal to authorize an unbound effect.

## Connections

- `derives` → [findings.md](./findings.md)
