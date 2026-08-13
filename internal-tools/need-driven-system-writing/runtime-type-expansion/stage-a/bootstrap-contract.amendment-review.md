# Amendment review — Stage-A bootstrap contract

**Reviewed artifact:** `bootstrap-contract.json`  
**Reviewed SHA-256:** `1A3C31AB68080534CD835430704DF955246A1B9E2E85C554E95B68AE1E7153B0`  
**Verdict:** **AMEND**

## Coverage

| lens | result | evidence |
|---|---|---|
| Amendment necessity and minimality | PASS | The current three legacy suites fail on the exact schema `0.6.3`, missing `capability_route`, and plural `others` assumptions named by the amendment. The compiler now emits `route_digest`, while its downstream consumer still accepts only `{schema, dispatch_id, target, slots}`. Adding one consumer owner and one disjoint fixture-migration owner is necessary and otherwise bounded. |
| Exact ownership and dirty-work preservation | **AMEND** | The fixture files have one disjoint owner and explicit before-hash/diff preservation. The intended service owner is also disjoint, but its sole path does not exist; the actual consumer is a different tracked file. |
| Fail-closed route validation | PASS subject to the path repair | The required behavior rejects absent, malformed, stale, cross-route, and mismatched digests before consumption and accepts only the digest of the immutable route. Receipt fields require the expected-digest source and positive/negative fixtures. |
| Test migration strength | PASS | New openings must use registry-derived `0.6.4`, singular `other`, complete `capability_route`, and preserved `route_digest`; explicit historical `0.6.3`/plural fixtures remain compatibility-only. The exclusive Stage-A positive and abuse tests remain owned by a separate tester and currently pass 14/14. |
| Execution order, receipts, integrity, and review | PASS subject to the path repair | Production and fixture owners join before the test owner; tests join before integrity; integrity freezes hashes before three independent attacks, writer–skeptic convergence, coverage, and approval. Amendment-specific receipts cover before/after hashes, diffs, fixtures, test PASS, pin regeneration, and preservation. |
| Unrelated scope | PASS | Non-goals exclude new type behavior and unrelated compiler, bridge, hook, UI, and service changes. No additional production or fixture path is justified beyond the four intended amendment targets. |

## Surviving finding

### AR-01 — The manifest-service owner targets a nonexistent file — MAJOR

**Contract evidence:** the amendment says `"implementations/server/orchestration/service.py is the downstream workflow-manifest consumer"` and assigns that exact path as `a_manifest_service_implementer.write_scope`.

That path does not exist. The actual consumer is `implementations/server/runtime/service.py`: its `_validate_workflow_manifest` currently requires exactly `{"schema", "dispatch_id", "target", "slots"}` and therefore does not accept or validate the compiler's new `route_digest`. The Stage-E source manifest also pins `implementations/server/runtime/service.py`, not the path named by the amendment.

The error makes the service repair, baseline receipt, integrity pin, frozen review corpus, and terminal approval impossible under the stated exact ownership. Creating the named path would be an unrelated parallel service implementation, not a valid repair.

**Required amendment:** replace `implementations/server/orchestration/service.py` with `implementations/server/runtime/service.py` everywhere it appears in the amendment evidence, role write scope, required behavior, amendment baseline requirement, and frozen review corpus. Preserve the existing method's unrelated bytes, require the expected digest to come from the opened row's immutable `capability_route`, then freeze a new contract hash and obtain a new amendment review before launching the added owners.

## Verification performed

- Contract SHA-256 matched the requested hash.
- Approved parent SHA-256 matched `2D9C9C3B3ACD66D0A0C11DF69F2BC9265B45A3384BB7C317D7F76F78CB342051`; its terminal review verdict is `PASS` and explicitly does not prove execution.
- `python -m unittest implementations.tests.runtime.test_runtime_type_bootstrap implementations.tests.runtime.test_runtime_type_bootstrap_abuse -v` passed 14/14.
- The three legacy suites produced 20 failures/errors, including the exact stale schema/route fixtures described by the amendment; integrity-pin failures are correctly deferred to the serialized integrity owner.
- `git status` and `git diff` showed no current modifications to the actual runtime service or the three legacy fixture files. Existing unrelated dirty paths remain outside amendment ownership.

No Stage-A amendment owner should launch from this hash. The finding is narrow and repairable; no broader redesign is required.

## Repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `E871C82D8552D4F26F90AE4C5A6BB999941ADB7DC5A64879F6F0E60B5225B140`  
**Verdict:** **PASS**

AR-01 is repaired without scope expansion:

- every service reference now names the existing consumer, `implementations/server/runtime/service.py`; the nonexistent `implementations/server/orchestration/service.py` is absent;
- the contract freezes the service's actual clean before hash, `A80574D71191D871013387CFB35F883AE28229DAD6F2F9C43309A0C1EFCBF11F`, which matches both the current file and its Stage-E source-manifest pin;
- the service owner's validation contract derives the expected digest exclusively from the opened dispatch row's verified `capability_route.route_digest` and rejects a value supplied only by the manifest, prompt, caller, or unrelated receipt;
- required behavior still fails closed before slot, artifact, or dependency consumption for absent, malformed, stale, cross-route, and mismatched digests;
- baseline preservation, exact write ownership, fixture migration, test ownership, producer → test → integrity → review ordering, receipt requirements, parent hash, non-goals, and terminal gates remain intact.

The repaired hash may proceed to the amended baseline and disjoint Stage-A owners. This PASS approves the repaired bootstrap contract only; it is not evidence that implementation, tests, integrity, review, or approval have completed.

## Second amendment review — legacy schema and baseline reconciliation

**Reviewed SHA-256:** `6530FDB5C47E21E4D5A36A60810952B596984105E6F6BD250F1F56409B43F32E`  
**Verdict:** **AMEND**

### Coverage

| lens | result | evidence |
|---|---|---|
| Necessity and minimality of `legacy.py` owner | PASS | `SUPPORTED_OPENING_CONTRACTS` currently contains only `0.6.1`–`0.6.3`, so a canonical `0.6.4` opening cannot enter the legacy lifecycle. The new owner is confined to that whitelist and its adjacent rejection branch; parsing, projection, close, aggregation, types, and historical bytes are excluded. |
| Accepted and rejected versions | PASS | Required behavior and tests name the complete accepted set (`0.6.1`, `0.6.2`, `0.6.3`, canonical `0.6.4`) and reject missing, malformed, `0.6.5`, `1.0.0`, and arbitrary unknown versions before lifecycle use. No range-based future acceptance is permitted. |
| Test ownership | PASS | Version behavior is added only by the disjoint `a_test_implementer` in the two exclusive Stage-A test files. The schema owner and fixture migrator cannot edit those tests; historical `0.6.3`/plural coverage remains explicit. |
| Baseline reconciliation truthfulness and ordering | **AMEND** | The reconciler's append-only shape is sound, but its stated temporal claim is already impossible for the three fixture files and for previously completed producers. Current fixture diffs demonstrate that production work preceded reconciliation. |
| Integrity, receipts, and terminal review | PASS subject to repair | `legacy.py` is in the integrity pin set and frozen review corpus. Producer/test joins precede integrity; receipts require before/after hashes, exact version outcomes, historical-byte preservation, and unchanged unrelated hunks. |
| Scope and regression | **AMEND** | The legacy change itself is bounded, but the fixed host-hook suite cannot pass while the production compatibility-opening path still emits a new `0.6.3` row without `capability_route`, and the amendment explicitly forbids host-hook production repair. |

### SA-01 — The reconciler claims a pre-owner baseline after owner work already exists — MAJOR

**Contract evidence:** `dirty_overlap_policy.amendment_baseline_requirement` says the reconciler runs “Before any amended production or fixture owner launches” and treats every pre-existing byte or hunk as user-owned. The execution graph also puts `a_baseline_reconciler` before the runtime, compiler, service, legacy-schema, and fixture owners.

That ordering is not historically true at this hash. The original baseline proves the three legacy fixture files were clean at its capture, while all three now contain Stage-A migration diffs; the runtime and compiler producers have also already changed their owned files. A reconciliation captured now can truthfully record the current amendment-era state, but it cannot call those fixture hashes pre-owner state or classify their existing Stage-A hunks as user-owned. The graph cannot retroactively make already-completed producer hashes downstream of the reconciler.

**Required amendment:** make the reconciliation explicitly temporal and two-layered:

1. preserve the original baseline as the evidence of original clean/user-owned state;
2. record current post-existing-producer/pre-new-owner hashes and diffs as amendment-era state, identifying already-produced Stage-A hunks from terminal owner receipts rather than promoting them to user-owned baseline;
3. require reconciliation before only owners not yet launched (at minimum the new `a_legacy_schema_implementer`, and the service owner if still unlaunched);
4. make resumed owners verify the reconciled current hash before further mutation, without claiming that reconciliation preceded their earlier work;
5. retain append-only preservation and block if the baseline, contract, current bytes, or cited producer receipts change during capture.

### SA-02 — The required host-hook suite still needs an out-of-scope production migration — MAJOR

**Contract evidence:** the non-goals prohibit “host-hook production behavior,” while the fixed test contract requires the full `test_host_dispatch_hook` suite to pass and says new host-hook openings use the registry schema and complete route.

`implementations/server/runtime/host_dispatch_hook.py` still constructs a new compatibility opening with hard-coded `"schema_version": "0.6.3"` and no `capability_route`. The canonical appender now requires the registry's exact `0.6.4` and an immutable route. Migrating only `test_host_dispatch_hook.py` cannot make the automatic compatibility-opening tests pass without concealing the production defect; changing `legacy.py` cannot repair appender validation.

**Required amendment:** give a distinct owner an exact, minimal scope over the host hook's compatibility-opening constructor so new rows derive the registry schema and a verified immutable capability route, with explicit preservation of its compatibility purpose and negative authorization behavior. Baseline it before mutation, add its exact positive/fail-closed cases to the disjoint test owner, include it in integrity/receipts/frozen review, and preserve the existing producer → tests → integrity → review order. Alternatively, explicitly remove that automatic path and its passing-suite requirement through a separately justified product decision; silently weakening or deleting its tests is not acceptable.

### Preserved conclusions

The second amendment does not regress specialized-first routing, strict `code`, singular `other`, historical plural readability, route-digest validation, disjoint schema/test/integrity/review ownership, or Stage-B blocking. The two findings are bounded execution-contract defects; they do not justify broader legacy parsing or orchestration changes.

No new or resumed Stage-A owner should rely on this hash as the final amended contract. Freeze and independently re-review the repaired hash first.

## Second amendment repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `82A4C6100438B42DA9AE2FFF546F3B87C8CEB0E4CB0DDA8113017EB1C051CD6B`  
**Verdict:** **BLOCK**

### Verified repairs

- **SA-02 production scope is repaired.** The exact existing target is `implementations/server/runtime/host_dispatch_hook.py`; its clean current SHA-256 is `390BA016210EF03D4077E5F9C76FDF2C42340397C643200470BE92DD608F9DD8`, matching both the contract and Stage-E source-manifest pin. `a_host_hook_implementer` owns only that file and only automatic opening synthesis. It must derive the registry schema and canonical resolver route for the exact compatibility capability, preserve dispatch-type/route-digest equality through binding/open/close, reject missing/forged/mismatched/swapped routes, and preserve role, model, prompt, anti-bias, output mode, lifecycle, and unrelated hunks.
- **The three evidence times are named.** The original baseline remains unchanged; `post_existing_producer_state` records current state after prior producers without calling it before-state; `pre_new_owner_state` separately freezes `legacy.py` and `host_dispatch_hook.py` before their new owners. Both new files currently match their clean Stage-E pins.
- **The legacy owner remains bounded.** It may change only `SUPPORTED_OPENING_CONTRACTS` and the adjacent rejection branch, accepting exactly `0.6.1`–`0.6.4` while rejecting missing, malformed, future, and unknown versions. Parsing, projection, close, aggregation, types, and historical bytes remain excluded.
- **Tests and integrity remain disjoint and ordered.** The dedicated test owner retains the two exclusive Stage-A tests; fixture tests remain separately owned; all production and fixture owners precede the test owner; tests precede integrity; the host hook and legacy reader are pinned and included in the frozen review corpus and amendment receipts.

### Remaining SA-01 defect — reconciliation semantics and graph still disagree — MAJOR

The prose now correctly says that registry, resolver, appender, compiler, service, and fixture observations are `post_existing_producer_state`. However, the execution graph still places `a_baseline_reconciler` before `a_runtime_implementer`, `a_compiler_implementer`, and `a_manifest_service_implementer`, even though the contract itself says those producers may already have changed bytes. This preserves the retroactive ordering rejected by SA-01 instead of representing reconciliation as a boundary before only newly authorized owners or resumed work.

The same policy ends its otherwise-correct three-time rule with: `Any pre-existing byte or hunk is user-owned.` At reconciliation time, existing runtime/compiler/service/fixture diffs may be Stage-A producer work, not user work. That sentence can therefore overwrite the new provenance distinction and misclassify producer residue as user-owned baseline.

**Required final repair:**

1. remove the retroactive reconciler → already-run-producer edges; connect reconciliation directly as a prerequisite to the two newly authorized owners, and state separately that any resumed existing owner consumes and verifies the reconciled current hash without claiming its earlier work followed reconciliation;
2. qualify the ownership rule: only bytes/hunks established by the original baseline or independently attributable user evidence are user-owned; post-existing-producer hunks retain their cited producer provenance and must also be preserved unless returned to that exact owner;
3. keep producer/fixture joins → test → integrity → frozen review unchanged, freeze a new contract hash, and re-review only this remaining chronology repair.

No new or resumed Stage-A owner should launch from this hash. SA-02 and the legacy boundary are approved, but the baseline record would still make a stronger historical claim than its evidence supports.

## Terminal SA-01 repair verification — 2026-08-13

**Reviewed repaired SHA-256:** `9CFEFA575DB22467BB3C3BC7F91CDDA94838EA0E7B6BEFBF836D1AB84EBAE7F7`  
**Verdict:** **PASS**

SA-01 is now fully repaired:

- `execution_state` truthfully identifies runtime, compiler, service, and fixture migration as historical completed producers whose existing receipts retain provenance; reconciliation neither relaunches them nor moves them retroactively downstream;
- the execution graph now places the reconciler directly before only the two pending new owners, `a_legacy_schema_implementer` and `a_host_hook_implementer`;
- a historical producer may resume only for a bounded verified finding, after verifying the reconciled current hash and linking a new receipt to its prior producer receipt;
- the baseline retains three non-interchangeable evidence times: the unchanged original baseline, timestamped `post_existing_producer_state` with named producer receipts, and timestamped `pre_new_owner_state` for `legacy.py` and `host_dispatch_hook.py`;
- user ownership is limited to hunks present in the original baseline or supported by independent user-attribution evidence. Stage-A diffs remain agent-produced under named receipts and cannot be reclassified during reconciliation, resume, or integrity work.

Prior approvals remain intact:

- the host-hook owner still targets only the actual clean file `implementations/server/runtime/host_dispatch_hook.py`, whose observed SHA-256 remains `390BA016210EF03D4077E5F9C76FDF2C42340397C643200470BE92DD608F9DD8`; its registry-derived schema, canonical route, digest equality, fail-closed cases, behavior preservation, tests, receipts, integrity pin, and review-corpus requirements remain unchanged;
- the legacy owner remains limited to `SUPPORTED_OPENING_CONTRACTS` and its adjacent rejection branch, accepts exactly `0.6.1`–`0.6.4`, rejects missing, malformed, future, and unknown versions, and cannot alter historical bytes or broader lifecycle semantics;
- pending new owners and any triggered historical-owner resume join before the disjoint test owner; tests join before integrity; integrity freezes the exact corpus before the full attacker → writer ↔ skeptic → coverage → approval review.

No scope, authority, strict-`code`, canonical-`other`, historical compatibility, route-digest, dirty-work, test-ownership, integrity, review, or Stage-B-entry regression was found. This PASS approves the terminal amended Stage-A contract at the reviewed hash only; implementation and terminal receipts remain separately required.
