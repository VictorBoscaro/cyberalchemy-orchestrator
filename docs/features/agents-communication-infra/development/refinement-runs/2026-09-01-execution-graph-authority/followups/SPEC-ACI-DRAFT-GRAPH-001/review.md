# Review — SPEC-ACI-DRAFT-GRAPH-001

- Output mode: `persisted`
- Aggregate verdict: **FIX**
- Exit reason: `verified_major_findings`
- Agents spawned by this reviewer: `0`
- `recheck_required`: `true`

## Coverage

The explicit parent dispatch assigned one independent reviewer for one worker. That instruction
replaced the review skill's usual multi-seat topology; this reviewer read the whole target corpus
and applied all requested lenses together. No target was edited during review.

| reviewer | lenses | targets attacked | findings raised | zero-findings defence |
|---|---|---|---:|---|
| `draftgraph_reviewer` | fidelity/governance; ownership/reference integrity; mechanics/correctness; operability/determinism; abuse/gaming; claim discipline | all 13 files listed below | 6 | n/a |

Lens coverage was corpus-wide, not partitioned. The governing comparison set was the session record,
run `RESULT.md`, proposed EG schema and architecture, toy graph/design review, stage-09 work pack,
feature `CRAFT.md`, and `.craft/ledger.yml`.

## Artifact verdicts

| Artifact | Verdict | Surviving findings |
|---|---|---|
| `COMPILATION-CONTRACT.md` | **FIX** | F1, F2, F4, F5 |
| `draft-graph-v1.proposed.schema.json` | **FIX** | F1, F4 |
| `FIELD-OWNERSHIP.md` | **FIX** | F1, F5, F6 |
| `NEGATIVE-VECTORS.md` | **FIX** | F2, F4, F5 |
| `review-correct-verify.draft.json` | **FIX** | F1 |
| `review-correct-verify.expected.execution.json` | **KEEP** | none |
| `TASK-SESSION.md` | **FIX** | F5 |
| `validate_artifacts.py` | **FIX** | F2, F3 |
| `VALIDATION.md` | **FIX** | F2, F3 |
| `WORK-PACK.md` | **KEEP** | none; its entry gate remains blocked by this review |
| `fixtures/catalog.json` | **KEEP** | none within its stated fixture-only evidence ceiling |
| `fixtures/policy.json` | **KEEP** | the deny-only fixture is coherent; F5 requires an additional specified allow case, not mutation of this fixture |
| `fixtures/resources.json` | **KEEP** | none |

## Verified findings

### F1 — LLM-authored keys still determine logical dispatch identity and authority revision

- Severity: **MAJOR**
- Files: `FIELD-OWNERSHIP.md`, `COMPILATION-CONTRACT.md`,
  `draft-graph-v1.proposed.schema.json`, `review-correct-verify.draft.json`
- Evidence from the reviewed artifacts:

  `FIELD-OWNERSHIP.md`:

  > `| revision | LLM/user alias / compiler | confirmation conflict key, projector | authority revision |`

  `COMPILATION-CONTRACT.md`:

  > `revision | "r" + decimal(draft.draft_revision) with no leading zero`

  > ``draft_revision` is an authoring input, not accepted authority state.`

  The draft schema requires both `graph_key` and `draft_revision`; the fixture supplies
  `"graph_key": "review_correct_verify"` and `"draft_revision": 1`. Yet `dispatch_id` is derived
  directly from `graph_key`, while the governing session says that IDs need deterministic system
  owners. Prefixing an LLM-authored identity/revision value does not change its effective origin.
  The downstream accepted-pair conflict check detects a collision but does not supply a
  deterministic identity or next revision.
- Verified consequence: two otherwise identical authoring attempts can choose different authority
  revisions, and unrelated drafts can choose the same `(dispatch_id, revision)`, without a rule in
  this compilation boundary deciding which value is correct.
- Proposed fix: keep any author-facing graph name as a non-identity alias, and supply frozen,
  system-owned `dispatch_id`/revision context to compilation (or define an equivalent deterministic
  allocation protocol). Remove `draft_revision` as LLM authority input and specify stale/collision
  behavior before code entry.

### F2 — DG-N09's expected success violates the contract's global-budget rule

- Severity: **MAJOR**
- Files: `NEGATIVE-VECTORS.md`, `COMPILATION-CONTRACT.md`, `validate_artifacts.py`, `VALIDATION.md`
- Evidence from the reviewed artifacts:

  `NEGATIVE-VECTORS.md`:

  > `Set review.requested_limits.max_tokens to 13000`

  > `successful deterministic restriction to 12000 plus a compiler-report restriction record`

  `COMPILATION-CONTRACT.md`:

  > `The sum of effective node max_tokens and wall_clock_seconds must not exceed the corresponding effective global value.`

  > `Failure is DG_GLOBAL_BUDGET_EXCEEDED; the compiler must not silently rebalance.`

  The positive node token limits are `6000 + 12000 + 6000 = 24000`. DG-N09 changes the first term
  to `13000`; policy restricts it to `12000`, producing `12000 + 12000 + 6000 = 30000`, above the
  effective global `24000`.
- Verification: an independent in-memory calculation returned
  `effective=[12000,12000,6000], sum=30000, global=24000,
  contract_result=DG_GLOBAL_BUDGET_EXCEEDED`. The shipped validator only asserts
  `min(13000, ceiling) == 12000`, so its printed claim
  `PASS negative-vector preconditions: DG-N01 through DG-N10` misses the contradiction.
- Proposed fix: mutate `correct.requested_limits.max_tokens` from `12000` to `13000` (effective
  totals remain `24000`) or use a global-limit restriction case that preserves node totals. Make
  the validator apply every vector's complete post-policy invariants and verify the specified
  restriction-report shape.

### F3 — The conformance script accepts extra executable authority

- Severity: **MAJOR**
- Files: `validate_artifacts.py`, `VALIDATION.md`
- Evidence from the reviewed artifacts:

  `validate_artifacts.py`:

  > `for draft_node, execution_node in zip(draft["nodes"], execution["nodes"]):`

  > `for capability, grant in zip(draft_node["capability_requests"], execution_node["tools"]):`

  `VALIDATION.md`:

  > `PASS static draft+fixtures to expected-EG mapping assertions`

  The same truncating `zip` pattern is used for inputs, outputs, validation rules and stop
  conditions. There are no exact-length checks for those arrays, and the script never compares
  `execution["audit_requirements"]` or `execution["lifecycle"]` to their sources.
- Verification: the nominal command exited `0`. Two in-memory adversarial executions of the same
  script also exited through every `PASS`: (a) appending a tool grant to the review node, whose draft
  requests no tools; and (b) appending a duplicate extra execution node. Both mutated graphs remain
  structurally valid under the proposed EG JSON Schema, and the current static mapping assertions
  did not reject them.
- Proposed fix: assert exact collection cardinality and exact ordered equality for every emitted
  collection; compare lifecycle and audit requirements; run a semantic EG validator over unique IDs
  and all references; add self-tests proving extra/missing node, tool, input, output, rule, stop and
  grant elements fail. Do not retain the current field-by-field PASS wording until those adversarial
  mutations are rejected.

### F4 — Failure predicates are admitted as node success conditions

- Severity: **MAJOR**
- Files: `draft-graph-v1.proposed.schema.json`, `COMPILATION-CONTRACT.md`, `NEGATIVE-VECTORS.md`
- Evidence from the reviewed artifacts:

  `draft-graph-v1.proposed.schema.json`:

  > `"success_condition": {"$ref": "#/$defs/predicate"}`

  The shared predicate union includes literal variants
  `{"kind":{"const":"input_unavailable"}...}` and
  `{"kind":{"const":"attempts_exhausted"}}`. `COMPILATION-CONTRACT.md` then says:

  > `.success_condition, .stop_conditions[].when | map local input/output alias to ID; copy closed kind/pointer/value`

  No semantic rule requires a success condition to prove required output presence/validity or
  excludes those failure variants from success.
- Verification: replacing the positive review node's success condition with either
  `{"kind":"attempts_exhausted"}` or
  `{"kind":"input_unavailable","input_key":"target"}` produced zero DraftGraph schema errors,
  while the node still declared `review_report` as a required output.
- Proposed fix: split success and stop predicate schemas. Limit success to predicates that establish
  required, validated outputs (or specify a separately named, justified exceptional success mode),
  and add semantic invariants plus negative vectors for exhaustion/unavailable-input success.

### F5 — Command admission has no deterministic rule for argv, cwd or environment bytes

- Severity: **MAJOR**
- Files: `COMPILATION-CONTRACT.md`, `FIELD-OWNERSHIP.md`, `TASK-SESSION.md`,
  `draft-graph-v1.proposed.schema.json`, `NEGATIVE-VECTORS.md`
- Evidence from the reviewed artifacts:

  `draft-graph-v1.proposed.schema.json`:

  > `"required": ["command_key", "argv", "cwd", "environment_resource_alias"],`

  `COMPILATION-CONTRACT.md`:

  > `An allowlisted network target, command, effect, commit or push must be explicitly allowed by the corresponding policy ceiling.`

  `FIELD-OWNERSHIP.md`:

  > `.commands.grants[].argv[] | LLM / compiler | command guard | exact invocation | exact requested strings/order | invalid/denied argv`

  However, the only concrete policy command ceiling is
  `"commands":{"mode":"deny","command_keys":[]}`; it defines no allowed argv, argv grammar, cwd,
  or environment-resource constraint. The contract defers compiler-input schemas and the task
  record claims `Credential and command branches are specified` while the positive fixture uses
  neither command nor credential.
- Verified consequence: an implementation that admits a command key cannot determine from this
  contract whether arbitrary LLM-authored arguments, cwd and environment bytes are permitted. For
  general interpreters or shells, command-key-only admission is not a meaningful bound on execution
  authority.
- Proposed fix: either make `commands.mode=allowlist` unsupported in DraftGraph v1 and reject it, or
  define closed policy/catalog/resource schemas and exact admission rules for the complete command
  tuple, including argv matching, cwd, environment resource kind/content constraints and duplicates.
  Add one positive allowlisted command fixture and negative argv/cwd/environment vectors before
  claiming this branch is specified.

### F6 — `done_when` prose is ambiguously assigned to validators despite being non-control prose

- Severity: **MINOR**
- File: `FIELD-OWNERSHIP.md`
- Evidence from the reviewed artifact:

  `FIELD-OWNERSHIP.md`:

  > `objective.done_when[] | LLM from user intent / compiler | agents, validators, projector | graph completion intent | exact ordered draft values | missing/empty/ambiguous prose remains review risk`

  `TASK-SESSION.md` separately says `objective.done_when remains purpose prose, not executable
  control`, and the governing contract requires runtime control not to depend on ad hoc prose.
  Naming validators as a consumer without limiting them to non-controlling evidence checks reopens
  the ambiguity the prior design review removed.
- Proposed fix: remove executable validators from this consumer list, or explicitly state that any
  validator use is advisory/audit-only and cannot affect scheduling, success, stopping or authority;
  point executable completion exclusively to closed predicates, validation rules and lifecycle.

## Change requests

1. **MAJOR — CR1:** move dispatch identity and authority revision out of the LLM-authored DraftGraph
   boundary and specify deterministic, frozen compilation context and conflict behavior.
2. **MAJOR — CR2:** correct DG-N09 and validate its full post-policy budget/result, not only the
   componentwise `min`.
3. **MAJOR — CR3:** harden `validate_artifacts.py` against extra/missing executable elements and add
   semantic EG/reference/lifecycle/audit checks plus adversarial harness tests.
4. **MAJOR — CR4:** separate allowed success predicates from failure/stop predicates and require
   required validated outputs for normal success.
5. **MAJOR — CR5:** close or remove the command-allowlist branch until full tuple admission and
   positive/negative conformance vectors exist.
6. **MINOR — CR6:** make `done_when` explicitly non-controlling in ownership and consumer language.

## Commands and results

| Check | Result |
|---|---|
| `python .../validate_artifacts.py` | exit `0`; six declared PASS lines plus the stated no-compiler/no-RFC8785 evidence limit |
| Independent Draft 2020-12 checks | draft and expected EG validate structurally; every object schema in the DraftGraph schema is closed with `additionalProperties:false` |
| Independent DG-N09 calculation | expected `DG_GLOBAL_BUDGET_EXCEEDED`, contradicting the vector's success result |
| In-memory EG mutation: add undeclared tool to reviewer | proposed EG schema: 0 errors; shipped validator: PASS |
| In-memory EG mutation: append duplicate extra node | shipped validator: PASS |
| In-memory DraftGraph mutation: success=`attempts_exhausted` | draft schema: 0 errors |
| In-memory DraftGraph mutation: success=`input_unavailable(target)` | draft schema: 0 errors |
| Manual digest spot-check | all five resource content digests and ten fixture `digest_source` hashes match the recorded values |
| Manual scope/governance check | no canonical spec, CRAFT/ledger, runtime, confirmation or projection artifact was modified by the worker package |

## Evidence boundary

This review establishes internal defects and the limits of the current conformance evidence. It does
not claim that a compiler exists, that RFC 8785/`aci-cjson-1` canonical bytes or a digest have been
reproduced, that fixture refs identify production artifacts, or that the proposed EG/schema is
canonical or production-ready. The nominal validator's exit `0` proves only the assertions it
actually executes; F2 and F3 show that two printed PASS claims are currently stronger than those
assertions.

The result is a resolved review deliverable with a **FIX** verdict, not an implementation blocker
caused by missing reviewer work. Repair must be followed by a full-corpus recheck before the
successor code-entry gate can pass.

## Recheck — 2026-09-01

- Recheck verdict: **FIX**
- Original findings resolved: `F1`, `F2`, `F3`, `F4`, `F5`, `F6`
- New surviving findings: `R1`, `R2`
- `recheck_required`: `true`
- Exit reason: `original_findings_repaired_new_major_findings_verified`
- Agents spawned by this reviewer: `0`
- Frozen-review check: before this recheck write, `review.md` still had the reviewer's prior SHA-256
  `FB40BA50908055B878F27CA818850337A1B39E029D17032F4F333A54D2746F9D`; the worker did not alter it.

### Original finding status

| Finding | Status | Recheck evidence |
|---|---|---|
| F1 — LLM-owned identity/revision | **RESOLVED** | Draft schema rejects `graph_key` and `draft_revision`; frozen `compilation-context.json` supplies the pair; released context is rejected independently. |
| F2 — contradictory DG-N09 | **RESOLVED** | Effective `[12000,12000,6000]` now returns `DG_GLOBAL_BUDGET_EXCEEDED`; safe restriction moved to DG-N11 with the exact report object. |
| F3 — truncating conformance comparison | **RESOLVED** | Exact whole-value comparison replaced truncating zips; independent duplicate/missing node and extra/missing tool attacks were rejected. |
| F4 — failure predicates as success | **RESOLVED** | Success and stop predicate schemas are split; exhaustion/unavailable-input success is structurally rejected; optional-output success is rejected semantically. |
| F5 — under-specified commands | **RESOLVED** | DraftGraph v1 structurally permits only `commands={mode:"deny",grants:[]}`; command tuple attack is rejected. |
| F6 — controlling `done_when` ambiguity | **RESOLVED** | Ownership now calls it non-controlling and excludes scheduler, predicate evaluator and executable validator consumption. |

### Recheck artifact verdicts

This table supersedes the initial artifact-verdict table for the repaired corpus.

| Artifact | Verdict | Reason |
|---|---|---|
| `COMPILATION-CONTRACT.md` | **KEEP** | F1–F6 contract repairs survived recheck. |
| `draft-graph-v1.proposed.schema.json` | **KEEP** | identity injection, failure-as-success and command tuple attacks are rejected. |
| `FIELD-OWNERSHIP.md` | **KEEP** | repaired origins, prohibited branches and non-controlling prose are explicit. |
| `NEGATIVE-VECTORS.md` | **FIX** | R2: missing pointer/value conformance vectors. |
| `review-correct-verify.draft.json` | **KEEP** | validates under the repaired schema and contains no authority identity/revision. |
| `review-correct-verify.expected.execution.json` | **KEEP** | exact positive mapping and semantic reference checks pass. |
| `TASK-SESSION.md` | **KEEP** | it claims F1–F6 repair and keeps code entry blocked for this recheck. |
| `validate_artifacts.py` | **FIX** | R2: two required output-predicate semantic failures are accepted. |
| `VALIDATION.md` | **KEEP** | its stated executed checks and evidence ceiling match the current script; it does not claim pointer/value negative coverage. |
| `WORK-PACK.md` | **FIX** | R1: successor inputs, vector range/results and review vocabulary are stale. |
| `fixtures/catalog.json` | **KEEP** | coherent command-free fixture catalog. |
| `fixtures/compilation-context.json` | **KEEP** | closed fixture value matches the frozen context contract for `r1`. |
| `fixtures/policy.json` | **KEEP** | coherent deny-only command policy fixture. |
| `fixtures/resources.json` | **KEEP** | digest and schema checks pass. |

### R1 — Successor work pack still encodes the pre-repair input/vector contract

- Severity: **MAJOR**
- File: `WORK-PACK.md`
- Evidence from the reviewed artifact:

  > `review-correct-verify.expected.execution.json from the four input fixtures.`

  > `Negative runner for every DG-N01 through DG-N10`

  > `except DG-N09, which emits only the specified restriction.`

  > `Entry gate: an independent reviewer must return PASS`

  The repaired corpus has five compilation inputs, DG-N01 through DG-N18, DG-N09 as a failing
  30k/24k reservation, and DG-N11 as the successful restriction. This review's governed verdicts
  are `KEEP`/`FIX`, while the same work pack's stop condition still names `BLOCK`/`FLAG`.
- Verified consequence: following the work pack literally would omit eight reviewed vectors, test
  the wrong DG-N09 result, miscount compiler inputs and leave the code-entry gate vocabulary
  ambiguous.
- Proposed fix: change four to five inputs; require DG-N01–N18; state DG-N09 fails with no graph and
  DG-N11 alone emits the restriction report; use `KEEP`/`FIX` consistently or define an explicit
  mapping from review verdict to gate status.

### R2 — Output-field predicates bypass the contract's pointer and value-schema checks

- Severity: **MAJOR**
- Files: `validate_artifacts.py`, `NEGATIVE-VECTORS.md`
- Governing evidence from `COMPILATION-CONTRACT.md`:

  > `an output_field_equals pointer exists in the owning output's JSON Schema and its value is admitted by that location's schema;`

- Evidence from the reviewed validator:

  > `assert success["kind"] in {"output_present", "output_field_equals"}`

  > `assert success["output_key"] in outputs and outputs[success["output_key"]]["required"] is True`

  `validate_draft_semantics` checks the predicate kind and required output but never resolves
  `json_pointer` into the bound output schema or validates `value` at that location. The negative
  vector set has no pointer-not-found or schema-incompatible-value case.
- Verification: two independent DraftGraph mutations passed both JSON Schema and
  `validate_draft_semantics`: (a) verification success pointer `/does_not_exist` with value `pass`;
  and (b) pointer `/verdict` with value `bogus`, outside the bound schema's
  `pass|flag|block` enum.
- Proposed fix: implement deterministic JSON Pointer resolution over the bound closed output schema,
  validate the comparison scalar against the located subschema, and add exact negative vectors for
  missing pointer and enum/type mismatch on both draft and emitted EG validation paths.

### Recheck commands and results

| Check | Result |
|---|---|
| Prior `review.md` SHA-256 | exact prior hash `FB40...F9D`; frozen by worker |
| `python .../validate_artifacts.py` | exit `0`; all declared F1–F6 regression lines pass |
| Independent F1 attacks | obsolete author identity/revision and released context rejected |
| Independent F2 calculations | 30k/24k rejected; safe restriction report exact |
| Independent F3 attacks | duplicate/missing node and extra/missing tool rejected |
| Independent F4 attacks | exhaustion/unavailable-input success rejected |
| Independent F5 attack | command allowlist/argv/cwd/environment rejected structurally |
| Independent F6 check | ownership row is non-controlling and does not name validators |
| Independent invalid pointer attack | **accepted unexpectedly** by `validate_draft_semantics` |
| Independent invalid enum value attack | **accepted unexpectedly** by `validate_draft_semantics` |
| Work-pack cross-check | 5 inputs and 18 vectors observed; work pack still says 4 and 10 |

### Recheck evidence boundary

The recheck proves that the six original findings were repaired at the proposal/fixture level. It
does not prove live allocator behavior, compiler typed errors, RFC 8785 canonicalization or runtime
readiness. The aggregate verdict remains **FIX** solely because R1 and R2 are new surviving MAJOR
findings. Repair both and rerun the full recheck before code entry.

## Recheck 2 — 2026-09-01

- Recheck verdict: **FIX**
- R1 status: **RESOLVED**
- R2 status: **PARTIALLY RESOLVED; remains open through S1**
- New surviving finding: `S1`
- `recheck_required`: `true`
- Exit reason: `r1_resolved_r2_type_guard_false_positive_verified`
- Agents spawned by this reviewer: `0`
- Frozen-review check: before this recheck write, `review.md` retained the prior reviewer SHA-256
  `C19B1E5289364CCF4FF70AA2A754D214827C3BA083394B4CA84912EEBC689121`; the worker did not alter it.

### R1/R2 repair status

| Finding | Status | Recheck evidence |
|---|---|---|
| R1 — stale successor work pack | **RESOLVED** | `WORK-PACK.md` consistently requires five inputs, DG-N01–N20, DG-N09 failure, DG-N11 safe restriction and aggregate `KEEP`/artifact `FIX`; old active gate/range/result text is absent. |
| R2 — pointer/value proof | **PARTIAL** | Missing pointer, malformed escapes, unguaranteed required/minItems routes, bad type/const/enum values, `$ref` and combinators are rejected; RFC 6901 escapes, nested objects and guaranteed array indices pass symmetrically in draft and EG. S1 shows ancestor type is not actually proven. |

### Recheck 2 artifact verdicts

This table supersedes the first recheck table for the twice-repaired corpus.

| Artifact | Verdict | Reason |
|---|---|---|
| `COMPILATION-CONTRACT.md` | **KEEP** | R1/R2 intended fail-closed rules are explicit; S1 is an implementation/check mismatch. |
| `draft-graph-v1.proposed.schema.json` | **KEEP** | pointer/value descriptions correctly defer the load-bearing proof to semantic validation. |
| `FIELD-OWNERSHIP.md` | **KEEP** | it requires properties/indices to be guaranteed and composite proof to fail closed. |
| `NEGATIVE-VECTORS.md` | **FIX** | S1 lacks a vector for typeless/nullable object or array ancestors. |
| `review-correct-verify.draft.json` | **KEEP** | current `/verdict` predicate remains valid. |
| `review-correct-verify.expected.execution.json` | **KEEP** | exact draft→EG correspondence and current predicate checks pass. |
| `TASK-SESSION.md` | **FIX** | O11 claims pointer-existence proof covered, but S1 refutes complete coverage. |
| `validate_artifacts.py` | **FIX** | S1 is accepted in both draft and emitted-EG semantic paths. |
| `VALIDATION.md` | **KEEP** | its listed N19/N20 and positive checks are accurate and its evidence ceiling remains bounded. |
| `WORK-PACK.md` | **KEEP** | R1 synchronization and review vocabulary are repaired. |
| `fixtures/catalog.json` | **KEEP** | unchanged and coherent. |
| `fixtures/compilation-context.json` | **KEEP** | unchanged and coherent. |
| `fixtures/policy.json` | **KEEP** | unchanged and coherent. |
| `fixtures/resources.json` | **KEEP** | current bound schemas and digests remain coherent. |

### S1 — Pointer traversal treats applicator keywords as proof of object/array type

- Severity: **MAJOR**
- Files: `validate_artifacts.py`, `NEGATIVE-VECTORS.md`, `TASK-SESSION.md`
- Governing evidence from `COMPILATION-CONTRACT.md`:

  > `walks explicitly declared required object properties, and walks array items only for a canonical decimal index proven present by minItems.`

- Evidence from the reviewed validator:

  > `if current.get("type") == "object" or "properties" in current:`

  > `elif current.get("type") == "array" or "items" in current:`

- Overstated evidence in `TASK-SESSION.md`:

  > `Prove output-field pointer existence and scalar schema admission on draft and emitted EG | contract, N19/N20 and permanent attacks | covered`

  Under JSON Schema, `properties`, `required`, `items` and `minItems` do not constrain an instance of
  the wrong type. The `or` branches therefore treat a keyword's presence as a type guarantee.
- Verification: both `validate_draft_semantics` and `validate_execution_semantics` accepted:

  1. `/nested/leaf` where `nested` has `properties` and `required` but no `type:"object"`; the full
     output `{"verdict":"pass","nested":5}` validates while the pointer is absent;
  2. `/arr/0` where `arr` has `items` and `minItems` but no `type:"array"`; the full output
     `{"verdict":"pass","arr":5}` validates while the pointer is absent;
  3. the same two cases with `type:["object","null"]` and `type:["array","null"]`; a null value
     validates and has no target path.
- Proposed fix: require the traversed ancestor's exact type to be `object` or `array`; absent,
  nullable or union ancestor types must return `DG_PREDICATE_POINTER_UNPROVABLE`. Add permanent draft
  and EG attacks plus a new negative vector, then synchronize the work-pack vector range.

### Recheck 2 commands and results

| Check | Result |
|---|---|
| Prior `review.md` SHA-256 | exact prior hash `C19...9121`; frozen by worker |
| `python .../validate_artifacts.py` | exit `0`; all declared F1–F6, R1 and R2 lines pass |
| Work-pack stale-text scan | only the explicit statement that `PASS/BLOCK/FLAG` are unused remains; five inputs/N01–N20/N09/N11/KEEP-FIX are coherent |
| RFC 6901 direct tests | `/a~1b`, `/c~0d`, `/`, `/~01` and `/~10` decode correctly |
| Nested/array positive tests | required nested leaf and indices `0..minItems-1` pass in draft and EG |
| Required/minItems negative tests | optional property, out-of-guarantee index, leading-zero index and `-` reject with the expected pointer errors |
| Scalar proof tests | valid and invalid `type`, `const` and `enum` values distinguish correctly |
| `$ref`/combinator tests | `$ref`, `allOf`, `oneOf` and conditional composition fail closed as unprovable |
| Draft/EG symmetry matrix | 5 valid pairs accepted; 12 malformed, unguaranteed, invalid-value or composite pairs rejected identically |
| S1 typeless ancestor attacks | **accepted unexpectedly** in both draft and EG; full counterexample outputs validate |
| S1 nullable-union attacks | **accepted unexpectedly** for object/null and array/null ancestors |

### Recheck 2 evidence boundary

This recheck does not establish general JSON Schema satisfiability, compiler/runtime behavior,
canonicalization or production readiness. It establishes that R1 is closed and most of R2's narrow
resolver contract works, including RFC 6901 escapes and deliberate fail-closed composition. The
aggregate verdict remains **FIX** because S1 permits a predicate path that is not guaranteed to
exist in an otherwise schema-valid required output.

## Recheck 3 — 2026-09-01

- Recheck verdict: **KEEP**
- S1 status: **RESOLVED**
- New surviving findings: none
- `recheck_required`: `false`
- Exit reason: `all_verified_findings_resolved`
- Agents spawned by this reviewer: `0`
- Frozen-review check: before this recheck write, `review.md` retained SHA-256
  `9920D6CC3A32FBC19C0D4CD60FAFCDB4C815607B6B99023891C73D01AC325092`; the worker did not alter it.

This section supersedes the earlier aggregate `FIX` verdicts for the current repaired corpus. The
earlier sections remain as the durable history of findings and repairs.

### S1 repair status

| Finding | Status | Recheck evidence |
|---|---|---|
| S1 — applicator keywords treated as ancestor-type proof | **RESOLVED** | `resolve_pointer_subschema` now traverses only when `current.get("type") == "object"` or `current.get("type") == "array"`. Typeless and nullable object/array ancestors reject with `DG_PREDICATE_POINTER_UNPROVABLE` in DraftGraph and EG. N21–N24, the contract, ownership row, work pack, validation record and task session are synchronized. |

### Recheck 3 artifact verdicts

| Artifact | Verdict | Reason |
|---|---|---|
| `COMPILATION-CONTRACT.md` | **KEEP** | requires literal exact object/array ancestor types, required properties, canonical guaranteed indices and fail-closed composition. |
| `draft-graph-v1.proposed.schema.json` | **KEEP** | structural predicate contract remains closed and delegates the load-bearing pointer/value proof to semantic validation. |
| `FIELD-OWNERSHIP.md` | **KEEP** | the pointer row mirrors the repaired exact-type and fail-closed rules. |
| `NEGATIVE-VECTORS.md` | **KEEP** | N21–N24 cover typeless/nullable object and array ancestors with validated scalar/null counterexamples on both paths. |
| `review-correct-verify.draft.json` | **KEEP** | validates and maps exactly under the repaired contract. |
| `review-correct-verify.expected.execution.json` | **KEEP** | exact expected mapping and semantic checks pass. |
| `TASK-SESSION.md` | **KEEP** | O12 and D13 accurately state the repaired S1 boundary and keep successor entry gated on this recheck. |
| `validate_artifacts.py` | **KEEP** | the full suite passes; independent adversarial matrices found no S1 or prior-pointer bypass. |
| `VALIDATION.md` | **KEEP** | recorded results and evidence ceiling match the command rerun. |
| `WORK-PACK.md` | **KEEP** | five inputs, N01–N24, DG-N09/DG-N11 outcomes and `KEEP`/`FIX` gate vocabulary are synchronized. |
| `fixtures/catalog.json` | **KEEP** | catalog digests and references pass. |
| `fixtures/compilation-context.json` | **KEEP** | frozen allocation context validates. |
| `fixtures/policy.json` | **KEEP** | policy tuple, ceiling and deny-only command controls remain coherent. |
| `fixtures/resources.json` | **KEEP** | resource digests and embedded schemas validate. |

### Zero-finding defense

No new finding survived the recheck. Independent attacks exercised both `validate_draft_semantics`
and `validate_execution_semantics` rather than relying only on direct resolver calls:

- typeless object/array ancestors with schema-valid scalar witnesses rejected;
- `object|null` and `array|null` ancestors with schema-valid null witnesses rejected;
- typeless and nullable inner transitions in object→array→object paths rejected, while the exact
  typed, required and `minItems`-guaranteed path passed;
- boolean property/item schemas and singleton type-array syntax failed closed as unprovable;
- `type: []` failed JSON Schema metaschema validation on both paths;
- inconsistent `const`/`enum` leaves rejected both candidate values;
- optional properties, absent `minItems`, missing paths, malformed RFC 6901 escapes, leading-zero or
  out-of-guarantee array indices, invalid scalar values, `$ref` and composition rejected;
- valid RFC 6901 escapes, required nested properties and guaranteed array indices still passed.

### Recheck 3 commands and results

| Check | Result |
|---|---|
| Prior `review.md` SHA-256 | exact prior hash `9920...092`; frozen by worker |
| `python .../validate_artifacts.py` | exit `0`; all declared F1–F6, R1–R2, S1 and inventory checks pass |
| Independent S1/edge matrix | 18 cases × 2 paths: 1 valid transition passed; 14 unprovable cases, 2 invalid-value cases and 1 invalid-schema case rejected as expected |
| Previous sampling replay | 8 valid and 12 adversarial pointer cases × DraftGraph/EG behaved as expected |
| Work-pack/vector synchronization scan | five inputs, N01–N24, N09 failure, N11 restriction and N21–N24 scalar/null witnesses present; stale active ranges absent |

### Recheck 3 evidence boundary

This `KEEP` is an artifact-level verdict for the frozen proposal corpus. It establishes the repaired
reference validator behavior, fixture coherence, exact expected mapping and the sampled pointer
proof boundary. It does not establish a production compiler, live allocator behavior, RFC 8785
canonicalization, general JSON Schema satisfiability, runtime isolation or production readiness.
Those remain successor implementation and validation obligations, not surviving defects in this
specification corpus.
