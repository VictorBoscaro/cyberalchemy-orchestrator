# Task session — IMPL-ACI-EXECUTION-RUNTIME-001

Status: `READY_FOR_RECHECK`; second repair-forward after reviewer `FIX` values
`569559E51B0E06CFE4C81576D8E455F9534F26D702F1D880EB16B88F03F8AEBD` and
`33D6870F1675E85AB93F6542A9206E013037C6680A5B7D2E56A572D0E3193C0C`; `task-session` fallback because the routed `domainspec-implement` capability
is blocked by the absent `implementation-axioms` package. This record does not claim formal
DomainSpec conformance.

## Contract

- One task: implement a local deterministic ExecutionGraph runtime and repair the directly related
  legacy sequential-handoff compilation gaps.
- Context: `CONTEXT-PACK.md`, standard/strict, 100% obligation coverage.
- Runtime/adapter: local Python; injected fake worker adapter; no provider, tool, credential,
  network, command, VCS or external-effect calls.
- Review pairing: worker `/root/execution_runtime_worker`; exactly one independent reviewer
  `/root/execution_runtime_reviewer`. Only that reviewer may return `KEEP`.
- Gate: PASS with the evidence ceiling and assumptions recorded in the context pack.

## Done criteria

1. A real DraftGraph fixture compiles and reaches a deterministic terminal run through persisted
   node attempts and fake results.
2. Compilation only freezes a candidate. Runtime admission requires a separate trusted local
   acceptance whose exact canonical digest is configured, verifies graph/authority/acceptance bytes and is idempotent for equal
   identity/digest while rejecting conflict/replay drift.
3. Review-correct-verify ordering, required inputs, output schemas, retry and predicates are
   enforced fail-closed.
4. Failure and cancellation produce explicit terminal node/run states and receipts.
5. Graph-pinned receipts record canonical objective, agent (`display_name` and `role`), route and
   result evidence, plus attempt/result digests where applicable.
6. The five bootstrap failures are fixed without weakening route/handoff byte checks.
7. Every new persisted/document field has one named producer and consumer.
8. Focused, adjacent and whitespace validations pass; no commit or push occurs.

## Validation surface

- `python -m unittest implementations.tests.runtime.test_execution_graph_runtime -v`
- `python -m unittest implementations.tests.runtime.test_runtime_type_bootstrap implementations.tests.runtime.test_runtime_type_bootstrap_abuse -v`
- `python -m unittest implementations.tests.runtime.test_draft_graph_compiler -v`
- focused migration/database regression selected after implementation.
- `python -m py_compile` over changed Python modules/tests.
- `git diff --check` and owned-diff inventory.

## Current baseline

On 2026-09-01, the bootstrap pair ran 19 tests: 14 passed, four failed and one errored. All five
failures originate in `compile_bound_launch_plan`: it writes `slots: []`, ignores sequential
handoff receipts, and does not reject unsupported/reverse connections. No runtime capability claim
is based on this baseline.

## Worker closeout

- Result: first reviewer verdict `FIX`; recheck 1 closed F2-F5 but returned `FIX` for acceptance
  authenticity and mutated fixture evidence. Both R1/R2 are repaired for another same-reviewer
  recheck; no `KEEP` claimed here.
- Decisions: four conservative assumptions recorded in `CONTEXT-PACK.md`; no blocker decision.
- Runtime: local Python with the concrete in-memory `ScriptedLocalAdapter`.
- Files and consumers: `FIELD-CONSUMERS.md` maps every new persisted/JSON field to one producer and
  enforcing consumer.
- Validation: focused 15/15 and final integrated 95/95 pass; exact commands, reviewer regressions and five repaired bootstrap cases are in
  `VALIDATION.md`.
- Craft synchronization: feature ledger records identity/role `KEEP` and this artifact as `flag`
  while review is pending. The canonical graph gap remains active.
- Subagent closeout: one worker active-to-ready, one paired reviewer awaiting handoff, zero hidden
  agents spawned by this worker.
- Experiment harness: not applicable; this is a bounded product-code task.
- Prohibited actions: no provider/tool/effect call, commit, push or deploy occurred.
