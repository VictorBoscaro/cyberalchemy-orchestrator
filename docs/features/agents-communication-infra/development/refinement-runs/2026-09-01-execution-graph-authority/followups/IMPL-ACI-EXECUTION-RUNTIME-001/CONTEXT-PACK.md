# Context pack — IMPL-ACI-EXECUTION-RUNTIME-001

Status: session evidence for one bounded `task-session` fallback; not canonical specification.

## Task and evidence ceiling

- Task: implement and test one local deterministic path from reviewed DraftGraph fixtures through
  the existing compiler into a terminal execution state, using a fake/local adapter only.
- Mode: standard, strict. Twelve files/selectors were selected; every selection closes an
  obligation below. No runtime handoff pack is needed because execution is local in this worker.
- Evidence ceiling: the compiler is conformance-reviewed, but `aci.execution-graph@2` remains a
  proposed authority shape and `ConfirmRuntimeDispatch@2` is not implemented. This task may prove
  local digest-bound admission and execution under an exact acceptance-digest allowlist plus
  configured issuer evidence;
  it may not claim canonical-v2 promotion, human confirmation `@2`, production host authentication,
  provider/tool execution, or production readiness.

## Obligation matrix

| ID | Obligation | Controlling evidence | Status |
|---|---|---|---|
| O1 | Compile real DraftGraph JSON deterministically | Draft compiler work pack; `DraftGraphCompiler.compile`, `CompilationResult`; canonical fixture | covered |
| O2 | Keep compilation non-authoritative; admit only an exact digest-allowlisted local graph acceptance; detect replay/conflict/tamper | compiler canonical bytes/digest; persisted nine-input/evidence/trust/acceptance manifest; canonical JSON boundary; proposed runtime exclusion | covered by byte-exact local acceptance and durable revalidation, explicitly not a signature or confirmation `@2` |
| O3 | Persist run/node/attempt/result/receipt state | `RuntimeDatabase` serialized SQLite boundary and immutable migrations | covered |
| O4 | Deterministic dependency, lifecycle and predicate execution | compilation contract `Edges and dataflow`, `Semantic validation`; expected review-correct-verify graph | covered |
| O5 | Fake/local worker launch with identity evidence | accepted identity field-consumer matrix and expected graph node agents | covered |
| O6 | Prove success, retry/correction, failure, cancel, replay and conflict | required task acceptance surface plus compiler/bootstrap tests | covered |
| O7 | Close the five existing bootstrap handoff failures | exact failing tests and `compile_bound_launch_plan` empty-slot implementation | covered |
| O8 | No external effects and no orphan keys | graph isolation fields, field ownership, new field-consumer inventory | covered |

## Selected sources and selectors

1. `AGENTS.md` — repository policy, evidence discipline and host binding.
2. `.agents/skills/task-session/SKILL.md` — one-task gates, validation and report contract.
3. `.agents/skills/context-builder/SKILL.md` — strict bounded selection and evidence format.
4. `stages/09-invoke-plan/WORK-PACK.md` — original contract acceptance criteria and non-goals.
5. `stages/09-invoke-plan/implementation-layering.md` — L3/L4 boundary and why this patch remains local.
6. `followups/SPEC-ACI-DRAFT-GRAPH-001/COMPILATION-CONTRACT.md` — policy, mappings,
   dataflow, predicates, lifecycle and runtime exclusion selectors.
7. `followups/IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001/WORK-PACK.md` — accepted compiler API
   scope and evidence ceiling.
8. `followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001/FIELD-CONSUMERS.md` — `display_name` and
   `role` producer/consumer rules.
9. `implementations/server/runtime/draft_graph_compiler.py` — public gate/compiler/result,
   canonicalizer and semantic validator symbols only.
10. `implementations/server/runtime/database.py` — migration manifest and serialized write boundary.
11. `implementations/server/runtime/dispatch_workflow.py` — `compile_bound_launch_plan`, binding
    marker and workflow-manifest generation.
12. `implementations/tests/runtime/test_runtime_type_bootstrap*.py` — the exact 19-case bootstrap
    surface; baseline is 14 pass, four failures and one error.

Excluded: general repository docs, UI, live provider adapters, credentials, network/effect layers,
and unrelated runtime services because none closes an obligation in this local test-only path.

## Objective, assumptions and decisions

- Objective served: prove that the reviewed JSON/compiler output can drive deterministic local work
  rather than stopping at a static graph.
- Success evidence: exact E2E terminal snapshot, byte-identical replay, idempotent duplicate,
  divergent-digest conflict, retry/correction, failure and cancellation tests; bootstrap 19/19;
  adjacent compiler tests; `git diff --check`.
- Auto-selected decision: reuse `RuntimeDatabase` and add one immutable migration rather than create
  a second persistence mechanism.
- Auto-selected decision: execute nodes in stable graph order with `max_parallel_nodes=1`; reject
  any local graph requesting a different parallelism until concurrency semantics are implemented.
- Reviewer-driven decision: separate candidate compilation from admission and require exact issuer
  evidence plus an allowlisted canonical acceptance digest binding graph, allocator assignment and
  compilation authority. The local fixture does not claim signature authentication.
- Reviewer-driven decision: admit only `cancel_running_nodes` and complete audit requirements; each
  receipt is validated against its graph-pinned schema before persistence and after reopen.
- Auto-selected decision: support only inline UTF-8 content and JSON-pointer `$` input selection in
  this increment; fail closed on immutable URI, base64 or other selectors.
- Assumption: the fake adapter is an injected deterministic function whose scripted outputs are
  test evidence, not evidence of model/provider execution.
- Assumption: validator refs are checked against the graph and output contracts are enforced with
  Draft 2020-12 JSON Schema; no external validator is invoked.

## Write scope

- `implementations/server/runtime/dispatch_workflow.py` for the five existing handoff gaps only.
- `implementations/server/runtime/execution_graph_runtime.py` and one immutable SQLite migration.
- `implementations/server/runtime/database.py` migration manifest.
- focused tests under `implementations/tests/runtime/`.
- this follow-up package, its field-consumer evidence, and exact CRAFT/ledger/traceability rows when
  evidence supports them.

All pre-existing dirty files outside this inventory are shared state and must not be rewritten.

## Gate verdict

PASS for bounded local implementation. No product-policy blocker is hidden: unsupported semantics
fail closed, external effects are prohibited, and the non-production evidence ceiling is explicit.
