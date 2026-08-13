# Stage-A Review — runtime type expansion

Frozen inputs verified before adjudication:

- `bootstrap-contract.json` SHA-256 `0F5F0B55380D12367050982EE72D8E871099F5A6A29CFFA2DDC12FF624563EBF`.
- `final-hash-manifest.json` SHA-256 `4DB6986BDE286F6E84E2C92D9AA9CC256C297769E0DBA0AF0C62DF2B7B07E862`.
- Every path pinned by `final-hash-manifest.json`, including all three governing-evidence files, matched its frozen SHA-256 during this review.
- Six distinct candidates remained after cross-attacker deduplication. Four supported findings survive skeptic round 1 below.

## Coverage

Coverage gate: **PASS** for the frozen review denominator; this is not an overall Stage-A PASS. The denominator is 18 targets: the 15 paths in `final-hash-manifest.json.final_targets`, plus `test-report.json`, `final-hash-manifest.json`, and `bootstrap-contract.json`. I independently recomputed all 18 SHA-256 values; every value matched its frozen pin. The three host-delivered attacker summaries state full-corpus reads through fidelity/governance, mechanics/correctness, and abuse/gaming respectively. The matrix below normalizes those summaries to the contract denominator and records the concrete attack made in each of the 54 required cells. “Clean” means no additional candidate survived that attack, not that the target is generally correct.

| frozen target | fidelity / governance | mechanics / correctness | abuse / gaming |
|---|---|---|---|
| `implementations/contracts/dispatch-type-registry.v1.json` | Checked specialized-type and generic-fallback declarations against the contract; clean. | Checked schema, aliases, authority modes, and resolver inputs; clean. | Exercised registry tampering, unknown/qualified identities, and specialized-to-generic fallback; clean. |
| `implementations/server/runtime/dispatch_types.py` | Checked canonical registry ownership and strict-code/no-fallback rules; clean. | Checked registry validation, capability resolution, collision rejection, and path containment; clean. | Exercised malformed identities, authority-mode mismatch, collision, and fallback gaming; clean. |
| `implementations/server/runtime/capability_routes.py` | Checked capability-root authority against the registry; clean. | Checked ordered root resolution and repository containment; clean. | Exercised path traversal and alternate-root selection; clean. |
| `.claude/skills/register-dispatch/append-dispatch.cjs` | Checked route-digest continuity across open/close; **A-005 survives**. | Reproduced validation of an orphan/route-unverifiable close; **A-005 survives**. | Exercised missing, forged, and swapped route-digest paths, including the historical-alias boundary; **A-005 survives**. |
| `implementations/server/runtime/dispatch_workflow.py` | Checked compiled handoffs against the exact upstream-output contract; **A-004 survives**. | Checked sequential receipt parsing, digest/size checks, source containment, and binding fields; **A-004 survives**. | Exercised digest, path, symlink, cross-route, and caller-supplied binding tricks; **A-004 survives**. |
| `implementations/server/runtime/service.py` | Checked service consumption against route, authority, and producer-provenance requirements; **A-004 survives**. | Checked binding lookup and observed that terminal state is not tied to an output artifact; **A-004 survives**. | Exercised forged binding attribution, source-path substitution, symlink, and cross-dispatch/route cases; **A-004 survives**. |
| `implementations/server/runtime/legacy.py` | Checked compatibility boundary and approved legacy versions; clean. | Checked strict parsing, duplicate/orphan rejection, snapshot selection, and mutation detection; clean. | Exercised malformed versions, duplicate fields, ambiguous rows, BOM/encoding, and historical aliases; clean. |
| `implementations/server/runtime/host_dispatch_hook.py` | Checked synthesized route and open/close behavior against host-binding law; clean apart from corpus-wide receipt failure in **A-002**. | Checked strict policy parsing, open/close route flow, and runtime calls; clean. | Exercised forged/swapped routes, malformed hook payloads, and authority escape; clean. |
| `implementations/tests/runtime/test_dispatch_workflow.py` | Checked migrated fixtures preserve the governed workflow contract; clean. | Checked compiler and sequential-handoff assertions; coverage does not disprove **A-004**. | Checked whether fixtures could pass with substituted paths/digests or topology inflation; clean. |
| `implementations/tests/runtime/test_orchestration_bridge.py` | Checked bridge fixtures preserve route, readiness, and legacy authority rules; clean. | Checked open/close, readiness, permission, and source-manifest cases; clean. | Checked malformed permission, route, authority, and source inputs; clean. |
| `implementations/tests/runtime/test_host_dispatch_hook.py` | Checked host-hook fixtures preserve lifecycle continuity; clean. | Checked resolved close, synthesized route, and host runtime integration; clean. | Checked whether fixture construction could bypass route or authority validation; clean. |
| `implementations/tests/runtime/test_runtime_type_bootstrap.py` | Checked positive/migration coverage against the Stage-A behavior contract; clean. | Checked registry/resolver, appender, compiler, route, and multi-source cases; coverage does not disprove **A-004/A-005**. | Checked whether positive fixtures could conceal generic fallback or unbound sources; clean. |
| `implementations/tests/runtime/test_runtime_type_bootstrap_abuse.py` | Checked negative coverage against the fail-closed contract; clean. | Checked unknown identities, swapped routes, fallback, topology, registry tampering, and legacy-version rejection; clean. | Directly exercised the declared gaming surface; clean, while **A-004/A-005** remain outside or survive its assertions. |
| `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json` | Checked minimal-merge and pre-existing-hunk preservation claims; clean. | Checked Stage-A source pins against current bytes; clean. | Exercised stale-pin and manifest-tampering scenarios; clean. |
| `implementations/server/runtime/local_pilot.py` | Checked that only the authorized Stage-E manifest pin changed; clean. | Checked exact manifest-path/digest preflight and strict ledger checks; clean. | Exercised alternate ledger/path, stale pin, and manifest substitution; clean. |
| `internal-tools/need-driven-system-writing/runtime-type-expansion/stage-a/test-report.json` | Checked persisted evidence against the contract’s test-before-integrity order; **A-001 survives**. | Checked exact commands, exit codes, and terminal result; **A-001 survives**. | Checked whether later prose could launder blocked command evidence into PASS; **A-001 survives**. |
| `internal-tools/need-driven-system-writing/runtime-type-expansion/stage-a/final-hash-manifest.json` | Checked test, provenance, dirty-hunk, and terminal claims against governing evidence; **A-001/A-002 survive**. | Checked all target pins and compared manifest PASS claims with the pinned BLOCK report; **A-001/A-002 survive**. | Checked registry/manifest tampering, stale pins, receipt substitution, and PASS inflation; **A-001/A-002 survive**. |
| `internal-tools/need-driven-system-writing/runtime-type-expansion/stage-a/bootstrap-contract.json` | Checked objective, authority, separation of roles, receipts, preservation, and terminal conditions; **A-001/A-002/A-004/A-005 map to violated clauses**. | Checked graph, scopes, frozen denominator, fixed commands, receipt schema, and PASS rule; the contract is mechanically readable, but its required evidence is incomplete under **A-001/A-002**. | Checked whether readiness, topology, host identity, or manifest prose could substitute for required evidence; **A-001/A-002 survive**. |

Lens coverage is therefore `18 × 3 = 54/54` cells. All-zero-findings flag: **false**—each attacker raised candidates, six distinct candidates reached synthesis, and four CRITICAL/MAJOR findings survived skeptic convergence. The two refuted candidates are absent from this report, so no refuted finding survived.

Evidence limitations and downstream action:

- Raw attacker summaries used denominators of 19, “15 then-current targets plus governing artifacts,” and 18. The mismatch is explained by some summaries counting `baseline.json` as governing evidence; `baseline.json` is pinned by the manifest but is not named in `review_contract.frozen_target_corpus`. This section uses the contract’s 18-target denominator and does not claim a nineteenth target.
- Review intentionally persists no attacker/verifier transcript. Cell proof therefore rests on the frozen hashes, the host-delivered full-corpus summaries, the concrete attack map above, and the surviving quoted target evidence—not on reconstructing independent returns.
- The skeptic’s terminal handoff reports convergence with all four survivors accepted, but each finding body still says “pending convergence.” That stale wording is outside the coverage auditor’s write scope and must be corrected by the review writer before final approval.
- Overall Stage-A result remains **BLOCK** because four CRITICAL/MAJOR findings survive and the contract permits PASS only when none remain.

## A-001 — CRITICAL — Frozen test evidence is BLOCK while the manifest asserts PASS

**Exact evidence / reproduction**

`test-report.json` records the required bridge command with `"exit_code": 1` and `"result": "BLOCK"` (lines 61–70), the required host-hook command as BLOCK (73–82), the required repository integrity command as BLOCK (96–105), and the required Stage-C command as BLOCK (108–117). It ends with `"final_result": "BLOCK"` and blockers (164–167).

The frozen `final-hash-manifest.json` pins that exact blocked report at SHA-256 `30aa036867407590ac3ad456220b35390cc7245ac59ef28cf1f5cd94b2c67791`, but declares the same required bridge, host-hook, integrity, and Stage-C commands `"result": "PASS"` (lines 88–96), then declares overall `"result": "PASS"` with `"blockers": []` (98–99). No durable post-integrity test report is identified.

**Violated contract / impact**

The contract says `test-report.json` records each exact command, exit code, evidence digest, and final PASS/BLOCK; requires all test receipts PASS before pin regeneration; and permits terminal PASS only when tests and integrity PASS. The manifest therefore launders later unrecorded claims over the frozen BLOCK evidence. Final approval cannot establish the required execution order or test result from the persisted corpus.

**Original repair owner**

`a_test_implementer` owns `test-report.json` and the fixed-command evidence; `a_integrity_owner` owns `final-hash-manifest.json` and must regenerate it only after a terminal test receipt.

**Proposed fix**

After final pin regeneration, have `a_test_implementer` rerun the fixed commands and replace `test-report.json` with terminal evidence, then have `a_integrity_owner` regenerate only the report pin and manifest claims from that evidence.

**Disposition pending skeptic**

SURVIVES — skeptic CONVERGED.

## A-002 — CRITICAL — Required durable lifecycle and adoption receipts do not exist

**Exact evidence / reproduction**

The contract names `.arcanum/observability/runs/2026-08-13-runtime-type-expansion/stage-a` as the receipt namespace and requires per-seat spawn, join, close, before/after hash, validation, blocker, residue, and reroute fields. `Test-Path` for that exact namespace returns false, and a repository search for the contract ID and named recovery/adoption agents finds no durable receipt set. `final-hash-manifest.json` instead says its provenance is `"host-delivered terminal agent identity; not a durable filesystem receipt"` (line 68) and that post-adoption PASS has `"no separate durable filesystem receipt"` (line 79).

**Violated contract / impact**

The contract requires attributable terminal receipts for recovery, both adoption paths, post-adoption review, tests, and integrity before downstream launch, and requires terminal approval to prove all attempted agents joined and closed. Host-delivered identities cannot prove those gates, authorship, preserved hunks, or launch ordering. The Stage-A result is therefore unapprovable regardless of code behavior.

**Original repair owner**

Each original Stage-A seat owner owes its own contract-complete receipt. The dedicated final approver verifies terminality and receipt completeness. `a_integrity_owner` must not substitute manifest prose for those receipts.

**Proposed fix**

Have each original seat persist its contract-required receipt in the named namespace, then require the dedicated final approver to verify every attempted seat is terminal and every required field is present before approval.

**Disposition pending skeptic**

SURVIVES — skeptic CONVERGED.

## A-004 — MAJOR — A terminal binding ID can launder any repository file as its output

**Exact evidence / reproduction**

`dispatch_workflow.py:130–169` accepts a non-empty caller-supplied `producer_binding_id`, reads any repository-contained `path`, and validates only the caller-supplied file digest and size before emitting `source_kind: "binding-output"`. `service.py:5395–5427` again validates the current file bytes, then queries only `SELECT dispatch_id,state FROM host_workflow_turn_bindings`; acceptance requires merely a binding in the same dispatch with a terminal state. No producer output path, output artifact ID, or output digest is registered or compared. `complete_host_workflow_turn()` (`service.py:5768–5859`) records only terminal state and agent identity.

The existing fixture demonstrates the mechanic directly: `test_host_workflow_binding.py:383–426` binds a producer, independently writes `workflow/kernel-output.md`, marks the producer resolved, and then obtains `launch-authorized` by naming that binding ID and the independently created file. The acceptance path and missing linkage are literal in the frozen production code.

**Violated contract / impact**

The contract requires canonical sequential upstream output to be materialized as the exact digest-bound downstream input and missing or tampered upstream output to fail explicitly. Current checks prove that a file exists and that some same-dispatch binding terminated; they do not prove the file was that binding's output. A caller able to write a handoff receipt can misattribute arbitrary repository bytes as agent-produced evidence.

**Original repair owner**

`a_compiler_implementer` for handoff receipt materialization and `a_manifest_service_implementer` for binding-output provenance validation.

**Proposed fix**

Register each terminal binding's exact output path, digest, size, and artifact identity, then require compiler and service validation to match every `binding-output` source to that registered output.

**Disposition pending skeptic**

SURVIVES — skeptic CONVERGED.

## A-005 — CRITICAL — Close validation permits orphan or route-unverifiable closes without a route digest

**Exact evidence / reproduction**

`append-dispatch.cjs:268–288` returns `null` when the ledger is absent, the opening is absent, the opening route is malformed, or the route digest is missing. `validateClose()` only requires a matching `capability_route_digest` when that lookup returns a value (`636–639`). The append path then explicitly warns when no opening exists and appends the close anyway. Exact read-only reproduction against the frozen repository:

```text
node .claude/skills/register-dispatch/append-dispatch.cjs docs/features/agents-communication-infra/adrs/fixtures/golden-close-input-v0.6.1.json --validate-only
```

The fixture names nonexistent `2026-07-23-local-probe-fixture` and contains no route digest, yet exits 0 with `valid close record (schema v0.6.4)`.

**Violated contract / impact**

The contract requires appender/open/bridge/host-binding/close to verify the same route digest and requires missing, forged, mismatched, or swapped route digests to fail closed across close. Conflating historical route-less openings with absent or malformed openings lets an orphan close satisfy current validation and, without `--validate-only`, append an unbound lifecycle record.

**Original repair owner**

`a_runtime_implementer`, owner of `.claude/skills/register-dispatch/append-dispatch.cjs` and route-digest close validation.

**Proposed fix**

Resolve the referenced opening and reject absent or malformed openings, requiring the exact route digest for current-schema openings while allowing omission only for a verified historical route-less opening.

**Disposition pending skeptic**

SURVIVES — skeptic CONVERGED.
