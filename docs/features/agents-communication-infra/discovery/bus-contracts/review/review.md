# Review — Bus Contracts after remediation

## Coverage

| attacker | lens | findings raised | zero-findings defence |
|---|---|---:|---|
| Fowler, Martin | remediation traceability | 0 | Checked all 18 prior findings and 15 consolidated change requests against current text; all have corresponding remediation. |
| Booch, Grady | clean-room operability | 8 | n/a |

- Collapse note: `robot_talks=false`; both reviewers remained independent.
- Lens coverage: the first reviewer audited completeness of the remediation; the second attacked the
  remediated document as a standalone operational contract.
- Parent verification: all eight clean-room citations were checked against the current target. None
  is refuted by the cited text. The clean-room findings are new gaps, not failures to apply the
  previous review: the traceability result remains 18/18 findings and 15/15 change requests remediated.

## `docs/features/agents-communication-infra/discovery/bus-contracts/README.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---:|---|---|---|---|
| 1 | `bus-contracts/README.md` | “Sobreposição ou atribuição ambígua bloqueia a aceitação.” Blocking acceptance happens after an agent may already have changed the shared worktree. | MAJOR | Require an isolated workspace or write gateway with lease enforcement before mutation; atomically promote an accepted change set and quarantine/reconcile orphan effects. |
| 2 | `bus-contracts/README.md` | `submission_accepted` says “consumers may be released”, while handoff waits for “um resultado oficialmente comprometido”. | MAJOR | Define an event-to-consumer table: accepted submission may release only declared local phases; cross-work-item/dispatch delivery requires the configured committed result. |
| 3 | `bus-contracts/README.md` | The runtime produces an “`RoutingPlan` imutável”, but the orchestrator also “cria/reabre a operação”. | MAJOR | Separate immutable routing topology/templates from mutable journaled assignment/generation state; topology changes require a new plan version. |
| 4 | `bus-contracts/README.md` | The objective says agents “recebem informação produzida por outros agentes”, but consumption is only described as roles resolved by `RoutingPlan`. | MAJOR | Define a `ConsumerInputManifest` with source submission IDs/digests, order, visibility decision, target assignment/generation, snapshot digest and delivery/replay semantics; state whether agents consume only through materialized invocations. |
| 5 | `bus-contracts/README.md` | The implementation example has only `summary`, while `submit_work` converts `output`; review provides unspecified “parecer e findings semânticos”, and `remediation_scope` is routing-critical without absence/default rules. | MAJOR | Add candidate schemas for research, implementation and review, including one-of inline/scratch, evidence modes, verdict/findings/evidence and required/default remediation scope; explicitly forbid server-derived fields. |
| 6 | `bus-contracts/README.md` | The lifecycle maps “missing/invalid/stale” to `candidate_rejected`, while retry returns an original receipt and stale attempts become retained observations. | MAJOR | Define distinct states and transitions for persisted-unverified, verification failure, stale observation, rejected and accepted, including terminality, expiration, retry eligibility and CAS. |
| 7 | `bus-contracts/README.md` | `submit_work` permits “outro output permitido pelo `OutputContract`”, while `work_kind` is immutable. | MAJOR | Require every `OutputContract` to declare a compatible `work_kind`; validate compatibility at compilation and publication, and constrain other outputs to subtypes of the active kind. |
| 8 | `bus-contracts/README.md` | `ExecutionObservationManifest` is an “artifact incremental/finalizado”, while official artifacts are immutable/content-addressed. | MINOR | Use append-only content-addressed observation segments plus an immutable final manifest, or distinguish mutable staging identity from the final artifact; official refs target only the final form. |

**Verdict:** FIX

## Change requests

1. MAJOR — Isolate or mediate workspace writes before acceptance and define promotion/quarantine.
2. MAJOR — Make release events explicit per consumer class and distinguish accepted submission from committed result.
3. MAJOR — Separate immutable `RoutingPlan` topology from mutable assignment/routing state.
4. MAJOR — Specify consumption/materialization, visibility, ordering, delivery and replay with a `ConsumerInputManifest` or equivalent.
5. MAJOR — Provide implementable, disjoint candidate schemas for research, implementation and review.
6. MAJOR — Complete the candidate verification state machine and recovery semantics.
7. MAJOR — Bind every `OutputContract` to the immutable `work_kind`.
8. MINOR — Give incremental observations an append-only staging model and immutable final identity.

## Dispatch closure

- `exit_reason`: `resolved`
- `agents_spawned`: 2 (`explorer`: 2, helpers: 0); loops used: 1
