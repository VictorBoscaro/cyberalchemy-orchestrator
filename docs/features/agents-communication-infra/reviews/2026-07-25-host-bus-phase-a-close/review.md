# Phase A closing review — Host Workflow Binding → BUS reveal delivery

- Review date: 2026-07-25
- Dispatch: `2026-07-25-host-bus-phase-a-close`
- Proposal: `proposal-v1.json`
- Frozen corpus: 18/18 SHA-256 bindings verified before dispatch, by both attackers, and again before this verdict
- Exit reason: `resolved`
- Overall verdict: **FIX**

## Scope and coverage

This verdict is limited to the frozen 18-file seam named by `proposal-v1.json`: host workflow
binding, BUS reveal/materialization, their focused tests, SWU descriptor/readiness material, and the
Stage-E source manifest. It does not claim full feature-spec closure because the frozen corpus omits
the normative `domain.md`, `rules.md`, `events.md`, `operations.md`, and
`persistence-and-replay.md`.

| Seat | Lens | Corpus result | Surviving findings |
|---|---|---:|---:|
| Lamport | mechanics/correctness | 18/18 hashes matched; focused suites executed | 3 MAJOR |
| Liskov | fidelity/governance | 18/18 hashes matched | 3 MAJOR |
| Parent | evidence verification and collapse | all six findings reproduced against frozen files; one transitive-dependency candidate rejected as unproven | 6 MAJOR |

No `robot_talks` collapse was needed. The independent returns were complementary: the mechanics
seat found identity and byte-integrity breaks, while the governance seat found authority,
attribution, and verification-claim breaks. Neither seat returned zero findings.

## Findings

### F1 — Invocation-plan authority remains partly caller-authored

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `docs/features/agents-communication-infra/specs/interfaces.md:224-235` assigns
    `operation_id`, `model_ref`, role/task refs, `response_schema_ref`, `tool_profile_ref`,
    policy/budget fields, `sandbox_policy`, and `authority_fence` to runtime, confirmed specs,
    resolvers, or policy owners.
  - `implementations/server/runtime/service.py:2950-2967` derives and compares only binding,
    group, attempt, seat, provider, and adapter authority.
  - `implementations/server/runtime/service.py:3119-3136` then seals the remaining
    caller-supplied authority fields into the request.
  - `implementations/tests/runtime/test_bus_reveal_delivery.py:278-295` mutates only attempt,
    seat, group, provider, and adapter.
- Why it matters: a valid capability can carry an invocation plan whose tool, sandbox, model,
  budget, response, or cutover authority was not derived from its declared owner.
- One-line fix: derive or exact-bind every authority-bearing plan field before persistence and add
  one zero-commit forgery test per field.

### F2 — `binding-output` attribution is not backed by producer output evidence

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `implementations/server/runtime/service.py:5329-5348` accepts any repository path as
    `binding-output` when the named producer merely exists in a terminal state, including
    `error` and `cancelled`.
  - `implementations/server/runtime/service.py:5670-5761` records terminal state and optional
    agent identity but no output artifact reference, byte digest, or output receipt.
  - `implementations/tests/runtime/test_host_workflow_binding.py:366-419` creates
    `workflow/kernel-output.md` outside the producer completion, marks the producer resolved, and
    accepts that file as the producer's output.
- Why it matters: arbitrary repository bytes can inherit false provenance from a prior binding;
  failed or cancelled turns can be claimed as producers.
- One-line fix: persist content-addressed terminal output evidence and accept `binding-output` only
  on an exact resolved-producer membership/hash match; otherwise classify it as repository input.

### F3 — BUS verification status has no completed execution receipt

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-BUS-DELIVERY-001.json:88-96`
    declares four validation commands and `implementation_status: implemented-verified`.
  - `docs/features/agents-communication-infra/WORK-PACK.md:108` claims focused, regression,
    alignment, layering, and verifier PASS.
  - `docs/features/agents-communication-infra/WORK-PACK.md:182` requires an execution receipt for
    every completed SWU.
  - The execution directory contains only
    `SWU-ACI-BUS-DELIVERY-001-code-readiness.json`, a pre-implementation readiness artifact; no
    completed execution receipt binds touched files, all four command results, and reviews.
- Why it matters: downstream planning treats an unproven completion claim as an accepted
  prerequisite.
- One-line fix: downgrade the status until a content-addressed completion receipt records the full
  declared validation matrix and independent review evidence.

### F4 — Follow-up identity can bypass the previously bound agent

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `implementations/server/runtime/service.py:5470-5492` rejects a mismatched follow-up target only
    when `prior_turn["agent_id"] is not None`.
  - `implementations/server/runtime/service.py:5675-5679` allows terminal completion with
    `agent_id=None` for every terminal state.
- Why it matters: once a terminal row has a null agent identity, the next turn may name an
  arbitrary target despite the follow-up continuity contract.
- One-line fix: require a non-empty persisted prior `agent_id` and exact target equality before any
  follow-up, with null/mismatch tests proving zero new binding rows.

### F5 — Peer payload bytes are not rehashed during materialization

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `implementations/server/runtime/service.py:3041-3049` loads message fields plus stored
    `artifact_content_hash`, but not artifact bytes.
  - `implementations/server/runtime/reveal_delivery.py:72-76` compares the contribution hash and
    stored artifact hash to the reveal hash without recomputing the digest from the body.
  - By contrast, base and role artifacts are loaded and rehashed at
    `implementations/server/runtime/service.py:3054-3058`.
- Why it matters: corrupted artifact bytes can materialize behind an unchanged stored hash and
  trusted reveal entry.
- One-line fix: load and hash each peer artifact body at materialization and compare the computed
  digest to both stored and reveal hashes; assert corruption causes `IntegrityError` and zero writes.

### F6 — Stage-E source integrity omits active BUS runtime sources

- Severity: **MAJOR**
- Artifact verdict: **FIX**
- Evidence:
  - `implementations/server/runtime/service.py:46-53` directly imports `reveal_delivery`.
  - `implementations/server/runtime/database.py:14-26` registers migration
    `011_bus_reveal_delivery.sql`.
  - `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` includes
    migrations through 010 but contains neither
    `implementations/server/runtime/reveal_delivery.py` nor
    `implementations/server/runtime/migrations/011_bus_reveal_delivery.sql`.
- Why it matters: Stage-E startup integrity can pass after tampering with code and schema that the
  active BUS path executes.
- One-line fix: add exact hashes for both active sources and extend source-integrity tests with a
  tamper case for each.

## Ordered change requests

1. Close authority and identity holes: F1 and F4.
2. Close byte/provenance holes: F2 and F5.
3. Restore integrity inventory coverage: F6.
4. Run the descriptor's complete four-command validation matrix and independent review.
5. Emit a completed, content-addressed SWU execution receipt and only then restore
   `implemented-verified`: F3.

These repairs should be dispatched as bounded implementation work. ACI-005 discovery remains
downstream until this FIX set closes; building on the current status would compound unbound
authority and unverifiable provenance.

## Validation performed

- `python -B -m unittest implementations.tests.runtime.test_host_workflow_binding -v`
  — **PASS**, 5/5.
- `python -B -m unittest implementations.tests.runtime.test_bus_reveal_delivery -v`
  — **PASS**, 7/7.

The green focused suites establish current behavior but do not refute the six findings because the
missing adversarial cases are outside their present assertions.

## Final disposition

The review dispatch is resolved with a **FIX** deliverable, not blocked. The implementation is
locally functional under its current focused tests, but Phase A is not safe to promote as a
verified foundation until the six MAJOR change requests and the completion receipt are closed.
