# Review — IMPL-ACI-EXECUTION-RUNTIME-001

- Frozen worker manifest: `a4ec50abe3425797fb24ca74afda7a9b5b0ee92f2afd8e81615d16af06525f4c`
- Review date: 2026-09-02
- Verdict: **FIX**
- `recheck_required`: `true`
- Output mode: persisted
- Reviewer: `/root/execution_runtime_reviewer`
- Paired worker: `/root/execution_runtime_worker`

## Coverage

| reviewer | lens | attacks and result |
|---|---|---|
| `/root/execution_runtime_reviewer` | mechanics / correctness | Reproduced 89/89 declared tests; attacked persisted-byte integrity, conditional readiness, cancellation modes, restart behavior, retry/failure/stop/cancel and the five bootstrap gaps. Four functional defects survived. |
| `/root/execution_runtime_reviewer` | fidelity / governance | Compared the public execution boundary with the accepted DraftGraph runtime exclusion and the package's own evidence ceiling. Missing independent acceptance/confirmation survived. |
| `/root/execution_runtime_reviewer` | ownership / reference integrity | Traced graph, authority, assignment, result, receipt and audit fields to their readers. `audit_requirements` and its receipt schema reference have no enforcing runtime consumer. |
| `/root/execution_runtime_reviewer` | abuse / gaming | Mutated durable graph bytes beneath an unchanged digest and exercised valid alternate lifecycle/topology values. The runtime executed the mutated instruction and silently changed authored semantics. |
| `/root/execution_runtime_reviewer` | operability | Re-ran the exact seven-module command, checked hashes and exercised independent temporary-database reproducers. The happy-path local fake adapter and bootstrap repair are real, but insufficient for KEEP. |

Every owned code/test/package target was attacked through the applicable lenses. This is not a
zero-findings review. The three pre-existing runtime-adjacent test files changed only for migration
version 16 and passed. No provider, tool, credential, network, VCS or external effect was invoked by
the reviewer.

## `implementations/server/runtime/execution_graph_runtime.py`

### F1 — execution self-authorizes without an accepted confirmation envelope

- Severity: **MAJOR**
- Evidence from the implementation:

  > `"""Compile, admit, and execute JSON bytes through the local-only adapter."""`

  > `admitted = self.compile_and_admit(`

  > `authority = self._local_authority(`

  The public call accepts only the nine compiler inputs. The same runtime compiles the candidate,
  manufactures `aci.local-execution-admission@1`, admits it and executes it. No independent caller,
  trust root, acceptance decision or confirmation envelope is an input.

- Contradicting package evidence:

  > `This task may prove local digest-bound admission and execution; it may not claim ... human confirmation @2`

  Correctly declining a `ConfirmRuntimeDispatch@2` claim does not turn allocator/compiler evidence
  into execution authority. The governing runtime boundary says the runtime receives an accepted
  ExecutionGraph and its confirmation envelope; a DraftGraph is non-authoritative and must not be
  sent to the runtime.

- Reproduction: `test_real_json_compiles_executes_and_replays_byte_identically` succeeds through
  `execute_draft_locally(**self.raw)` without supplying any acceptance/confirmation value.
- Required fix: split compilation from execution admission. The executable public boundary must
  consume frozen canonical ExecutionGraph bytes plus a separately supplied, trust-checked local
  acceptance envelope that binds the exact graph digest and assignment/allocator authority. Missing,
  malformed, tampered or mismatched acceptance must fail before migration/admission writes. Keep the
  local/test ceiling explicit and do not relabel it as `ConfirmRuntimeDispatch@2`.

### F2 — persisted graph bytes can change while the old authority digest is retained

- Severity: **CRITICAL**
- Evidence from the implementation:

  > `graph = parse_strict_json(bytes(row["graph_bytes"]))`

  > `return graph, row["graph_digest"]`

  `_graph` neither recomputes `digest_bytes(graph_bytes)` nor rechecks canonical bytes, schema,
  semantic validity, authority digest or the admitted identity before scheduling. Assignments then
  carry the stale stored digest alongside fields read from the changed graph.

- Independent reproduction (temporary SQLite database): admit the reviewed fixture; update only
  `local_execution_admissions.graph_bytes` so the first node instruction is
  `TAMPERED AFTER ADMISSION`; leave `graph_digest` unchanged; call `execute(run_id,max_steps=1)`.
  Observed result:

  > `ACCEPTED running TAMPERED AFTER ADMISSION True`

  The final `True` proves the adapter received the old admitted digest with the mutated instruction.
- Required fix: before every snapshot/reopen/pre-launch use, verify stored graph bytes against the
  stored digest, canonicalization and the closed ExecutionGraph validator, then verify the stored
  authority bytes/digest and graph binding. Cross-check durable node identity/role heads against the
  verified graph. Add corruption tests for graph, authority, assignment, result and receipt bytes;
  all must fail closed before adapter launch or an apparently valid snapshot.

### F3 — `any_predecessor_succeeded` is implemented as an all-predecessors barrier

- Severity: **MAJOR**
- Evidence from the implementation:

  > `all_terminal = all(states[edge["from_node_id"]] in NODE_TERMINAL for edge in incoming)`

  > `return all_terminal and any(active(edge) for edge in incoming)`

  The accepted compiler's conditional-readiness proof permits an `any` consumer to activate on the
  first active incoming route once its required producers are guaranteed. Waiting for every incoming
  predecessor to terminate invents a hidden barrier and changes authored scheduling.
- Independent reproduction: a compiler-accepted graph ordered
  `review, verify, correct` used `verify.start_when=any_predecessor_succeeded`, a required review
  input, and a second `correct -> verify` control/on-success route. After review succeeded, verify's
  required input was available. Observed adapter order was nevertheless:

  > `['node:review', 'node:correct', 'node:verify']`

- Required fix: implement route-event activation for `any_predecessor_succeeded` without the
  `all_terminal` barrier, retaining deterministic graph-order tie-breaking and the compiler's
  must-availability guarantee. Add accepted all/any/always/on-success/on-failure graphs whose node
  order makes premature waits and linear-runner behavior observable.

### F4 — one admitted cancellation policy has no runtime semantics

- Severity: **MAJOR**
- Evidence from the implementation:

  > `if graph["lifecycle"]["max_parallel_nodes"] != 1:`

  > `if any(edge["kind"] == "feedback" for edge in graph["edges"]):`

  `_validate_local_subset` restricts unsupported concurrency and feedback, but never restricts
  `lifecycle.cancellation`. No production code reads that field, while `_cancel_run` always cancels
  every non-terminal node and launched attempt.
- Independent reproduction: change only the fixture DraftGraph cancellation value to
  `allow_running_nodes_to_stop` and call `compile_and_admit`. Observed result:

  > `ADMITTED sha256:0f0cd84bede942c505ad3ce430db63d3deb56050d1921c04085f6dabdb56ef0f pending`

- Required fix: either implement both closed cancellation modes with race/restart tests or reject
  `allow_running_nodes_to_stop` in `_validate_local_subset` before admission. The runtime may not
  silently execute it as `cancel_running_nodes`.

### F5 — ExecutionGraph audit authority is ignored in favor of an invented receipt shape

- Severity: **MAJOR**
- Evidence from the implementation:

  > `RECEIPT_SCHEMA = "aci.local-execution-receipt@1"`

  > `receipt = { "schema": RECEIPT_SCHEMA, ... }`

  The runtime never reads `graph["audit_requirements"]`; in particular,
  `receipt_schema_member_id` is not resolved and emitted receipts are not validated against the
  graph-pinned schema member. `FIELD-CONSUMERS.md` therefore does not substantiate its claim that the
  execution fields have enforcing consumers.
- Reproduction: `rg -n "audit_requirements|receipt_schema_member_id" implementations/server/runtime/execution_graph_runtime.py`
  returns no match, while the accepted graph fixture contains both.
- Required fix: resolve and enforce every `audit_requirements` field, validate receipt bodies against
  the referenced pinned schema before persistence, and add negative tests for missing/tampered schema
  members and each unsupported audit choice. If the local receipt format is intentionally narrower,
  reject incompatible graphs at admission and document the exact supported subset.

**Artifact verdict:** **FIX**

## `implementations/server/runtime/dispatch_workflow.py`

The five historical bootstrap failures are genuinely closed. The exact combined suite passed, and
the current implementation rejects missing sequential receipts, feedback, zig-zag, fanout and
reverse order while materializing exact ordered producer sources. No independent finding survived
for this bounded repair.

**Artifact verdict:** **KEEP**

## Migration, focused tests and evidence package

Migration 016 applies idempotently and the happy path persists admission/run/node/attempt/receipt
rows. The focused suite proves review-correct-verify, equal replay, divergent-draft conflict,
expected-digest rejection, retry, worker failure, stop/fail branches, between-node cancellation and
migration reopening. It does not attack the five surviving defects above, so `VALIDATION.md` and
the CRAFT/ledger `review pending` state must remain non-accepted until repair and recheck.

**Artifact verdict:** **FIX**

## Verification record

- Worker key hashes reproduced:
  - `execution_graph_runtime.py`: `af4db98f3c3d0741d121accc6a94696e5aeb1dc96918629bdc7e47e2d021eedb`
  - migration 016: `2540b3249ce1da5fa3a6e5bef154efe9cea5ae7607be14b4221ad456ad76b2e8`
  - focused runtime test: `b207d784f4bda65a088c0308bb46530061442a6ac40b4c21a0371f2c68699fc5`
  - `FIELD-CONSUMERS.md`: `cfc9c116ce39028dea28e71fcdb1f75331aed747972c9fcc6e652d45d4f21838`
  - `VALIDATION.md`: `17e514e021ec9c6edff7c0d0e4e48c6983ef4d2a33680b602c613560f14517b8`
- Exact declared command: **89/89 passed** in 37.122 seconds.
- Bootstrap pair within that command: **19/19 passed**; none of the five old failures remains.
- Independent graph-byte tamper attack: **accepted incorrectly**.
- Independent valid `any` scheduling attack: **executed in the wrong order**.
- Independent alternate cancellation-policy attack: **admitted without a consumer**.
- `git diff --check`: worker reported pass; no finding depends on line-ending warnings in shared
  dirty files.

## Change requests

1. **CRITICAL** — Revalidate durable graph/authority bytes and all persisted evidence digests before
   scheduling or presenting a valid snapshot.
2. **MAJOR** — Require a separately supplied, trust-checked local acceptance envelope; allocator and
   compiler evidence cannot self-authorize execution.
3. **MAJOR** — Implement true `any_predecessor_succeeded` route-event activation.
4. **MAJOR** — Implement or fail closed on `allow_running_nodes_to_stop`.
5. **MAJOR** — Consume and enforce `audit_requirements`, including the pinned receipt schema.
6. Add the exact reproducers above as deterministic regression tests, rerun the 89-test baseline,
   update FIELD-CONSUMERS/VALIDATION/CRAFT/ledger without exceeding the local-fake proof, and return
   the repaired frozen corpus to this same reviewer.

Exit reason: `verified_authority_integrity_and_scheduler_defects_require_repair`

Agents spawned by this reviewer: `0`.

## Recheck 1 — 2026-09-02

- Repaired worker manifest: `26ef2bbd039c7275044732f3dd65c374d12ef7fe0d9d83e43a7280c79864e71c`
- Prior review SHA-256: `569559E51B0E06CFE4C81576D8E455F9534F26D702F1D880EB16B88F03F8AEBD`
- Recheck verdict: **FIX**
- `recheck_required`: `true`
- Original F2–F5: resolved by code and regression evidence
- Original F1 API self-authorization: structural split resolved, acceptance authenticity still unresolved
- New findings: `R1`, `R2`

### Recheck coverage

The reviewer reproduced the new key hashes and the exact seven-module suite: **94/94 passed** in
43.178 seconds. Independent attacks then covered missing/tampered acceptance, caller forgery under a
configured issuer, graph/authority/assignment/result/receipt corruption, route-event `any` ordering,
unsupported cancellation, audit flags and the pinned receipt-schema path. The 19/19 bootstrap repair
remains green.

The repaired implementation now recomputes durable graph/authority/evidence digests before use,
checks node heads and assignments, activates `any_predecessor_succeeded` on the first active route,
rejects `allow_running_nodes_to_stop`, and validates receipt bodies against the graph-selected schema.
Those repairs survived. Two evidence/authority defects remain.

### R1 — configured issuer metadata does not authenticate the acceptance envelope

- Severity: **MAJOR**
- Evidence from the implementation:

  > `if self.trusted_acceptance_issuers.get(issuer_key) != evidence_digest:`

  > `raise GateBlockedError("local execution acceptance issuer is not trusted")`

  The check proves only that the caller repeated a public issuer name and configured evidence digest.
  There is no signature/MAC, verification key, or configured exact acceptance digest. Any caller that
  can submit the envelope can change `accepted_by` or mint a new accepted envelope while copying the
  same issuer metadata.

- Independent reproduction: compile the positive candidate, take the ordinary acceptance, replace
  only `accepted_by` with `principal:forged-by-caller`, keep the configured issuer/evidence fields,
  and call `admit_execution_graph`. Observed result:

  > `FORGED_ACCEPTED principal:forged-by-caller`

- Claim mismatch:

  > `requires a separately issued local acceptance bound to configured issuer trust`

  The API is now separate, but issuance is not authenticated; caller-supplied metadata is not proof
  of a separately issued decision.
- Required fix: for the local/test boundary, configure and verify the exact canonical acceptance
  digest (or implement a real signature-verification key and signature) in addition to issuer
  provenance. Altering `accepted_by`, decision, graph binding or any other byte must reject before
  database creation. Keep the explicit non-production/non-`ConfirmRuntimeDispatch@2` ceiling.

### R2 — the E2E silently rewrites a claimed pinned JSON input inside the test

- Severity: **MAJOR**
- Evidence from the test artifact:

  > `"resources": (FIXTURES / "resources.json").read_bytes(),`

  > `receipt["content"] = canonical_text(LOCAL_RECEIPT_SCHEMA)`

  > `receipt["digest"] = digest_bytes(receipt["content"].encode("utf-8"))`

  > `self.raw["resources"] = canonical_bytes(resources)`

  The on-disk `resources.json` pins a different schema requiring only `status`. The positive harness
  replaces it with a test-defined local receipt schema before compilation. Therefore the E2E does
  not execute the “all nine pinned compiler input documents” claimed by `TEST-SPEC.md`, and no
  immutable fixture or manifest binds the actual successful input bytes.

- Related acceptance evidence: `TRUSTED_EVIDENCE_DIGEST = "sha256:" + "a" * 64` names no pinned
  issuer-evidence artifact, while the same test helper constructs the acceptance it calls
  independently issued.
- Required fix: persist an exact local-execution fixture bundle containing the nine input documents,
  compatible receipt schema/resource bytes, issuer evidence/trust configuration, and canonical
  accepted envelope. Add a digest manifest that the test actually verifies. The positive E2E must
  load those exact bytes without semantic mutation, compile to the pinned candidate digest, admit
  only the pinned/authenticated acceptance, execute to terminal, and replay byte-identically.

### Recheck 1 artifact verdicts

| Artifact | Verdict | Reason |
|---|---|---|
| `execution_graph_runtime.py` | **FIX** | F2–F5 are repaired, but R1 permits forged acceptance under copied issuer metadata. |
| `test_execution_graph_runtime.py` | **FIX** | R2 hides a material input rewrite and self-authors the alleged independent acceptance. |
| migration 016 | **KEEP** | No migration finding survived. |
| `dispatch_workflow.py` bootstrap repair | **KEEP** | Remains 19/19 and fail-closed. |
| FIELD-CONSUMERS / VALIDATION / CRAFT / ledger | **FIX** | Preserve review-pending state and replace “separately issued/trusted” plus pinned-input claims until R1/R2 are proven. |

### Recheck 1 change requests

1. **MAJOR** — Authenticate exact acceptance bytes, not caller-repeated issuer metadata.
2. **MAJOR** — Replace generated/mutated E2E authority inputs with an immutable digest-manifested
   fixture bundle and execute it byte-for-byte.
3. Rerun the 94-test baseline plus explicit forged-principal and fixture-manifest attacks; return the
   new frozen corpus to this same reviewer without commit or push.

Recheck exit reason: `acceptance_authenticity_and_pinned_e2e_evidence_still_missing`

## Recheck 2 — 2026-09-02

- Repaired worker manifest: `8409269b2b5d339d8ed36da991701be73056f24afa139efcd4904825728a9c55`
- Prior review SHA-256: `33D6870F1675E85AB93F6542A9206E013037C6680A5B7D2E56A572D0E3193C0C`
- Recheck verdict: **KEEP**
- `recheck_required`: `false`
- Original findings resolved: `F1`–`F5`
- Recheck 1 findings resolved: `R1`, `R2`
- New findings: none
- Exit reason: `local_acceptance_and_byte_exact_e2e_survived_independent_recheck`

### Final coverage and zero-findings defence

| lens | independent final attacks | why no finding survived |
|---|---|---|
| authority / abuse | changed `accepted_by` under the trusted issuer, removed trust, changed graph binding and replayed exact acceptance | Runtime now requires both issuer evidence and an allowlisted digest of the complete canonical acceptance bytes; the forged principal rejected with `GateBlockedError` before database creation. |
| persistence integrity | changed admitted graph bytes beneath the original digest and rechecked durable authority/assignment/result/receipt regressions | Independent graph attack rejected with `IntegrityError` and zero adapter calls; the focused corruption matrix remained green. |
| scheduler / lifecycle | route-event `any`, all/always/success/failure coverage, alternate cancellation and terminal branches | `any` no longer waits for all predecessors; graph-order tie breaking is stable; unsupported cancellation rejects before writes. |
| audit / ownership | complete audit flags, selected receipt member, schema conformance, receipt reopen and field-consumer map | Admission requires the supported audit projection, every receipt is checked before write and after reopen against the graph-selected schema, and incompatible schemas reject. |
| operability / evidence | loaded the fixture manifest, recomputed all referenced digests, ran the exact E2E and full suite | The bundle loaded exactly nine named input documents, the local resources bytes matched their manifest digest, issuer evidence/trust/acceptance formed the checked chain, and the positive test performs no semantic input rewrite. |
| claim discipline | CRAFT, ledger, TASK-SESSION, TEST-SPEC, FIELD-CONSUMERS and VALIDATION | They preserve local-fake/proposed-graph limits and explicitly exclude `ConfirmRuntimeDispatch@2`, production authentication, live provider/tool/credential execution and production readiness. |

The zero-new-findings result is not based only on worker assertions. The reviewer reproduced the
suite and reran the two attacks that previously broke authority: exact-acceptance forgery and
post-admission graph mutation. Both failed closed before adapter launch or durable creation as
applicable.

### Final verification record

- Key frozen hashes reproduced:
  - `execution_graph_runtime.py`: `27fc4f7226aa340559f2e94a37a68160995bedbed4229b150da41dc36a18c681`
  - `test_execution_graph_runtime.py`: `ec76b84345b78f409d7184bf3a17f346e8b0002f49a4352c9c19114cee6650e4`
  - fixture `manifest.json`: `bcd040b9ec798763c22c65cc4861981d83be6efbefcda902e04686caa014c130`
  - `VALIDATION.md`: `d1a827ab71526f1675f84392b177f6e17b49fd059103659184fb0840a58aeb48`
  - ledger: `4cd03cc9376ce607710c5e1f52d04b7a72aa627ba4445e0b765c408e8c51a492`
  - CRAFT: `e15f4fd0357a8eb10b966c45270d3a27b6c18e91316584565411d5e9ff928b1c`
- Exact seven-module suite: **95/95 passed** in 41.621 seconds.
- Fixture loader: **9/9 exact named inputs**, acceptance bytes matched the trust digest.
- Independent acceptance forgery: `FORGE_REJECTED GateBlockedError True`; `True` means no database
  was created.
- Independent post-admission graph tamper: `TAMPER_REJECTED IntegrityError 0`; `0` means zero adapter
  calls.
- Bootstrap remains **19/19** with the five old handoff gaps closed.
- No commit or push was performed by the worker or reviewer.

### Final artifact verdicts

| artifact | verdict | reason |
|---|---|---|
| local ExecutionGraph runtime | **KEEP** | Separately accepted canonical bytes, durable fail-closed verification and deterministic local scheduling are implemented within the stated subset. |
| focused runtime tests and fixture bundle | **KEEP** | The E2E starts from manifested JSON bytes, binds exact acceptance, reaches terminal review-correct-verify, replays deterministically and carries non-tautological authority attacks. |
| migration 016 | **KEEP** | Idempotent durable state remains compatible with adjacent runtime suites. |
| sequential handoff bootstrap repair | **KEEP** | 19/19 remains green and unsupported/missing handoffs fail closed. |
| evidence package, CRAFT and ledger | **KEEP** | Status and capability ceiling match the reproduced proof. |

### Capability ceiling accepted by this KEEP

This KEEP proves one bounded local path:

`9 manifested JSON inputs -> pure DraftGraph compilation -> proposed ExecutionGraph candidate -> exact local acceptance -> SQLite admission/state machine -> ScriptedLocalAdapter -> terminal receipts/snapshot`.

It does **not** prove canonical `aci.execution-graph@2` promotion, `ConfirmRuntimeDispatch@2`, human
confirmation, production host authentication, a live subagent/provider/tool/credential adapter,
external effects, concurrency, feedback cycles or production readiness.

Final change requests: none.

Agents spawned by this reviewer: `0`.
