# Validation — IMPL-ACI-EXECUTION-RUNTIME-001

Status: second repair-forward validation complete; same-reviewer recheck pending. First review was `FIX`
`569559E51B0E06CFE4C81576D8E455F9534F26D702F1D880EB16B88F03F8AEBD`; recheck 1 was `FIX`
`33D6870F1675E85AB93F6542A9206E013037C6680A5B7D2E56A572D0E3193C0C`.

## Results

| Command | Result |
|---|---|
| `python -m py_compile implementations/server/runtime/execution_graph_runtime.py implementations/server/runtime/dispatch_workflow.py implementations/tests/runtime/test_execution_graph_runtime.py` | exit 0 |
| `python -m unittest implementations.tests.runtime.test_execution_graph_runtime -v` | 15/15 pass |
| `python -m unittest implementations.tests.runtime.test_draft_graph_compiler implementations.tests.runtime.test_runtime_type_bootstrap implementations.tests.runtime.test_runtime_type_bootstrap_abuse -v` | 41/41 pass |
| `python -m unittest implementations.tests.runtime.test_runtime_run_group_heads implementations.tests.runtime.test_runtime_confirmed_bus implementations.tests.runtime.test_runtime_confirmation -q` | 39/39 pass |
| final second-repair combined invocation of the seven modules above | 95/95 pass in 42.829s |
| persisted fixture manifest verification | 9/9 input digests, issuer/trust artifacts, canonical acceptance and expected candidate digests pass |
| structural YAML/index check for `.craft/ledger.yml` | `craft-ledger-structural-pass 43 126` |
| `git diff --check` | exit 0; line-ending warnings only on pre-existing shared dirty files |

The final distinct integrated total is 95/95; focused is 15/15. The added focused regressions attack
independent reviewer findings; they are not duplicate happy-path counts.

## Recheck-1 repair matrix

| Finding | Repair | Regression evidence |
|---|---|---|
| R1 issuer metadata did not authenticate acceptance | runtime trust configuration now pins the exact canonical acceptance digest in addition to issuer/evidence; durable reopen repeats the same check | changing only `accepted_by`, graph digest or any other acceptance byte rejects before database creation; missing/untrusted acceptance remains rejected |
| R2 positive E2E rewrote resources and used a dummy evidence digest | persisted local-execution manifest binds paths/digests for all nine input files, a compatible persisted resources document, real issuer-evidence/trust fixtures, canonical acceptance bytes/digest and expected graph/authority digests | positive E2E loads manifest bytes without mutation and asserts candidate/acceptance digests; missing resource, resource digest drift and acceptance digest drift reject |

## Reviewer `FIX` repair matrix

| Finding | Repair | Regression evidence |
|---|---|---|
| F1 self-authorizing compile/execute API | split pure `compile_candidate` from `admit_execution_graph` / `execute_accepted_graph`; require a separate canonical acceptance whose issuer evidence exactly matches runtime-configured trust | missing, digest-tampered and untrusted acceptance all fail before database creation |
| F2 durable graph bytes executed beneath stale digest | revalidate graph, admission authority, node heads, assignment, result, output and receipt bytes/digests before snapshot, scheduling, adapter launch and result reduction | independent graph/authority/assignment/result/receipt SQL tampering all raises `IntegrityError`; graph/authority/assignment/receipt paths make zero adapter calls |
| F3 `any_predecessor_succeeded` hidden all-terminal barrier | activate on the first active route event; keep stable graph-array tie breaking | compiler-accepted `review, verify, correct` graph executes `review, verify`, then deterministically skips `correct` after terminal completion |
| F4 ignored `allow_running_nodes_to_stop` | local admission accepts only `cancel_running_nodes` | alternate valid cancellation mode fails closed before database creation |
| F5 ignored `audit_requirements` and pinned receipt schema | require the complete four-field local audit subset; project exact canonical objective/agent/route/result; validate each full receipt against the graph-pinned schema before insert and on reopen | false audit choice, missing member and incompatible schema fail before writes; normal receipts validate on every snapshot |

## Five formerly failing bootstrap cases

| Case | Baseline | Current proof |
|---|---|---|
| sequential consumer slot materialization | `IndexError` because `slots` was empty | exact ordered producer receipts appear in one consumer slot; pass |
| missing sequential handoff receipt | compile returned a launch plan | fail-closed `GateBlockedError`; pass |
| `feedback` connection | compile accepted unsupported semantics | fail-closed `GateBlockedError`; pass |
| `zig-zag` connection | compile accepted unsupported semantics | fail-closed `GateBlockedError`; pass |
| reverse sequential connection | compile ignored canonical group order | fail-closed order error; pass |

The same abuse test also covers `fanout` as an unsupported connection; it was already grouped with
the topology test but is not counted as a sixth baseline failure.

## Capabilities supported by evidence

- One pure call accepts the nine JSON/byte compiler inputs and freezes a candidate. A separate
  public execution boundary accepts canonical ExecutionGraph bytes, compilation authority and an
  exact digest-allowlisted local acceptance, then persists and runs to a terminal state.
- Equal replay is byte-identical and side-effect free; divergent identity and expected-digest drift
  fail before mutation.
- Stable sequential scheduling, exact node-output binding, schema checks, explicit validator
  outcomes, output predicates, retry/exhaustion, stop/fail branches and cancellation are durable.
- Each launch preserves `display_name`, `role`, graph/node/attempt identity, exact inputs and result
  digests.
- The previously red bootstrap handoff surface moved from 14/19 to 19/19 without weakening the
  tamper/cross-route tests.

## Residue

- `aci.execution-graph@2` remains proposed, not canonically promoted.
- This is `aci.local-execution-admission@2` plus `aci.local-execution-acceptance@1`, not
  `ConfirmRuntimeDispatch@2`. The local acceptance records a principal and an exact configured
  issuer/evidence binding and exact acceptance bytes, but proves neither a cryptographic signature,
  human confirmation nor production host authentication.
- `ScriptedLocalAdapter` performs no provider/tool/credential/filesystem/network/VCS/effect call.
  Its `validations` are deterministic fake outcomes, not executions of pinned validator refs.
- `max_parallel_nodes` must equal 1; cancellation must equal `cancel_running_nodes`; all four audit
  recording choices must be true; feedback cycles, immutable URI/base64 members and selectors other
  than `$` fail closed.
- No commit or push was performed by this worker.

## 2026-09-02 commit-time integration addendum

The commit integrator found one compatibility regression outside the accepted
95-test matrix. A valid single-group `0.7.0` opening may omit the optional
`connections` property, but `_sequential_handoffs` rejected the missing value
instead of treating it as an empty topology. The dispatch-ledger schema does
not require `connections`.

The bounded repair changes `record.get("connections")` to
`record.get("connections", [])`. The focused host-dispatch suite then passed
11/11, and the combined identity/runtime matrix passed 161/161 in 335.760s.
Stage-C passed 8/8 after the Stage-E member and verifier pins were refreshed;
the 41/41 specification vectors, provenance contracts, MCP smoke/RPC, and
current package self-check also passed.

The earlier same-reviewer `KEEP` remains evidence for its exact reviewed
bytes and the bounded local-fake runtime. It does not independently approve
this later one-line repair. No independent re-review was run during commit
integration, so that exact-byte recheck remains pending.
