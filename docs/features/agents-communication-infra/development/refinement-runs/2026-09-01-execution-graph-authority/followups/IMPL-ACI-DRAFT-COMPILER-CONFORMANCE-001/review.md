# Review — IMPL-ACI-DRAFT-COMPILER-CONFORMANCE-001

Date: 2026-09-01

- Output mode: `persisted`
- Dedicated pairing: worker `/root/draftgraph_successor_worker`; reviewer
  `/root/draftgraph_impl_reviewer`
- Aggregate verdict: **FIX**
- `recheck_required`: `true`
- Exit reason: `verified_major_authority_and_conformance_findings`
- Agents spawned by this reviewer: `0`

## Coverage

The user's one-worker-to-one-reviewer requirement replaces the review skill's normal multi-attacker
topology. One independent reviewer attacked every target under each declared lens, verified every
surviving finding against literal artifacts and executable counterexamples, and wrote this sole
review artifact. No finding relies on worker testimony.

| reviewer | lens | targets attacked | findings raised | zero-findings defence |
|---|---|---|---:|---|
| dedicated reviewer | fidelity / authority | compiler, context gate, schemas, contract and worker claims | 2 | n/a |
| dedicated reviewer | mechanics / correctness | complete compiler and tests, five-input parsing, predicates, schemas, topology, budgets | 3 | n/a |
| dedicated reviewer | determinism / canonicalization | duplicate keys, Unicode, numbers, clean processes, digest/result coherence | 2 | n/a |
| dedicated reviewer | ownership / reference integrity | IDs, refs, selectors, content members, URIs, credentials and resource bindings | 3 | n/a |
| dedicated reviewer | abuse / test quality / scope | replay/conflict bypass, policy widening, malformed JSON, mutation attacks, broad regression and Git scope | 4 | n/a |

All listed targets were read in full. The governing predecessor was sampled only where needed to
establish the required behavior. Directed and adjacent suites survive, but adversarial variants
below refute the aggregate readiness claim.

## Commands and observed results

| Command / attack | Result |
|---|---|
| `python -m unittest implementations.tests.runtime.test_draft_graph_compiler -v` | 10/10 pass |
| predecessor `validate_artifacts.py` | exit `0`; all declared proposal checks pass |
| compiler + adjacent protocol compilation tests | 22/22 pass |
| `python -m py_compile` over both new Python files | pass |
| runtime discovery suite | 277 tests; 7 failures and 6 errors |
| same discovery suite with only `test_draft_graph_compiler` filtered out | 267 tests; the same 13 failure/error classes remain, plus one race-sensitive APT failure on this run |
| forged raw context + forged public `AllocatorReservation` | accepted as `dispatch:attacker/r1` |
| direct public `VerifiedCompilationContext` construction | compiler emitted graph under attacker-selected identity |
| returned-result mutation | one provider-ref mutation changed multiple nodes while stored bytes/digest remained unchanged |
| selector mutation | arbitrary `runtime://guess/free-form?x=../secret` accepted and emitted |
| URI mutation | `https://example.invalid/latest` accepted as `immutable_uri` with an unchecked digest |
| topology mutation | an `on_failure`-only route into `all_predecessors_succeeded` compiled successfully |
| explicit optional feedback input | rejected as `DG_TOPOLOGY_INVALID lifecycle.entry_node_keys` despite its declared feedback edge |
| output schema with `NaN` | accepted as a JSON Schema and emitted |
| satisfiability attack (`required` property with subschema `false`) | impossible output contract accepted and emitted |
| malformed policy `network.allow=[[]]` | raw `TypeError: unhashable type: 'list'`, not a typed compiler error |
| doubly invalid catalog under `PYTHONHASHSEED=1..12` | first error path alternated between `catalog.providers[0]` and `catalog.models[0]` |
| `python -m pip check` | existing `python-bcb/httpx` conflict and invalid local Django distribution; no `jsonschema` conflict |

## `implementations/server/runtime/draft_graph_compiler.py`

### F1 — The trusted allocator gate is forgeable through public data constructors

- Severity: **MAJOR**
- Evidence from the artifact:

  > `@dataclass(frozen=True)`
  > `class AllocatorReservation:`

  > `@dataclass(frozen=True)`
  > `class VerifiedCompilationContext:`

  > `if not isinstance(context, VerifiedCompilationContext): _fail("DG_IDENTITY_CONTEXT_STALE", "compilation_context")`

- Verification: constructing either a matching public `AllocatorReservation` and raw context, or a
  `VerifiedCompilationContext` directly, allowed compilation under
  `dispatch_id="dispatch:attacker"`, `revision="r1"` without allocator state, latest-reservation
  evidence or accepted-pair conflict evidence.
- Consequence: the core claim that only a trusted allocator verifier can introduce identity is a
  convention, not an enforced boundary. Stale/replay/conflict protection is bypassable before any
  graph validation begins.
- Proposed fix: make compiler entry consume an unforgeable allocator capability/receipt verified by
  the trusted host (or move the gate behind that host boundary); do not export constructible
  “verified” authority types as sufficient proof. Add direct-construction and forged-reservation
  attacks.

### F2 — The result does not keep logical graph, canonical bytes and digest coherent

- Severity: **MAJOR**
- Evidence from the artifact:

  > `class CompilationResult:`
  > `    graph: dict[str, Any]`
  > `    canonical_bytes: bytes`
  > `    digest: str`

  > `"provider_ref": provider["ref"]`

- Verification: all three fixture nodes share the same catalog `provider["ref"]` dictionary.
  Mutating the first returned node's provider name also changed another node, while
  `result.canonical_bytes` and `result.digest` stayed unchanged; re-canonicalizing `result.graph`
  produced a different digest.
- Consequence: a downstream projector/confirmation adapter can observe a graph that no longer
  matches the evidence carried beside it. `frozen=True` does not freeze nested values, and catalog
  references create additional cross-node aliasing.
- Proposed fix: establish one immutable authority representation. Return immutable canonical bytes
  plus a digest and decode fresh copies for views, or deeply freeze/copy the graph and verify its
  digest at every boundary. Never share mutable catalog dictionaries across emitted positions. Add
  post-return mutation and alias-identity tests.

### F3 — Output-contract validation accepts invalid JSON and trivially impossible schemas

- Severity: **MAJOR**
- Evidence from the artifact:

  > `schema = json.loads(resource["content"], object_pairs_hook=_duplicate_rejector(path))`

  > `Draft202012Validator.check_schema(schema)`

  > `if not isinstance(required, list) or not isinstance(properties, dict) or not set(required) <= set(properties):`

- Verification: Python's permissive JSON parser accepted a schema containing `const:NaN`; the
  metaschema check and compiler accepted it. A valid Draft 2020-12 schema with required `patch` and
  `properties.patch=false` also compiled although no output can satisfy it.
- Consequence: “valid closed JSON Schema” and “no impossible output contract” are not established;
  a node can be authorized with an output it can never produce.
- Proposed fix: parse embedded schemas with the same strict duplicate/non-finite rejection as all
  other JSON. Define an admitted, mechanically satisfiable output-schema subset (or a sound
  satisfiability check for the promised subset) and reject contradictions such as required
  `false` properties. Add both attacks on draft and emitted-EG validation paths.

### F4 — Selector authority is unchecked and the governing selector language is unspecified

- Severity: **MAJOR**
- Evidence from the artifact:

  > `_text(source["selector"], f"{path}.source.selector", code)`

  > `mapped = {"kind": "content_member", "member_id": "member:" + source["resource_alias"], "selector": source["selector"]}`

- Governing ownership requires an “exact draft selector under fixed semantics” and lists
  invalid/unsupported selectors as a failure, but the compiler accepts every non-empty string and
  no selected semantics artifact defines an admitted grammar.
- Verification: `runtime://guess/free-form?x=../secret` compiled and entered authority unchanged.
- Consequence: interpretation is deferred to the runtime, contradicting the no-runtime-choice
  boundary; the same authoritative bytes can rely on an undefined selector operation.
- Proposed fix: return this field to specification, define a closed selector language/version
  selected by the pinned semantics record, validate it before emission, and add positive/negative
  selector vectors. Until that exists, admit only an explicitly specified literal such as `$` or
  reject selectors entirely.

### F5 — URI resources are labeled immutable without proving content-addressed location or bytes

- Severity: **MAJOR**
- Evidence from the artifact:

  > `_text(row["immutable_uri"], f"{path}.immutable_uri", code)`

  > `if "content" not in resource:`
  > `    return`

- Verification: an input resource at `https://example.invalid/latest` with an arbitrary syntactic
  SHA-256 value compiled and was emitted as `immutable_uri`; no relation between URI and digest was
  checked.
- Consequence: the artifact claims a digest-pinned immutable resource while admitting mutable or
  unsupported locations. Later retrieval can fail or change, and the compiler has not verified the
  exact bytes claimed by field ownership.
- Proposed fix: admit only defined content-addressed URI schemes whose address binds the same digest,
  or require resolver-supplied frozen bytes/proof as an explicit compiler input. Reject ordinary
  mutable URLs and add unavailable/mismatched URI vectors. If resolution remains out of scope,
  remove URI admission from this conformance claim.

### F6 — Topology validation ignores activation conditions and defeats declared feedback

- Severity: **MAJOR**
- Evidence from the artifact:

  > `if edge["kind"] != "feedback":`
  > `    source = edge["from_node_id"][5:]; target = edge["to_node_id"][5:]; incoming[target].add(source); outgoing[source].add(target)`

  > `if (key in roots) != (node["start_when"] == "roots_ready"): _fail(...)`

- Verification: after replacing `correct`'s review input with a resource, an authored
  `review -> correct` control edge conditioned only on `on_failure` was accepted while `correct`
  retained `all_predecessors_succeeded`. Conversely, adding a valid-looking optional correction
  feedback input plus its explicit feedback edge caused the derived normal data edge to remove the
  root and fail lifecycle validation.
- Consequence: “start condition satisfiable by predecessors”, “impossible joins fail”, and explicit
  feedback support are not implemented. The compiler both admits a dead route and rejects the
  iterative route the contract says feedback can authorize.
- Proposed fix: specify the exact state machine relating edge `condition`, input availability,
  `start_when`, roots and feedback; then validate activation satisfiability. Do not count a
  feedback-authorized dependency as an ordinary DAG predecessor for root/cycle analysis. Add both
  counterexamples and multi-predecessor `any`/`all` cases.

### F7 — Five-input structural validation is neither schema-equivalent nor deterministic

- Severity: **MAJOR**
- Evidence from the artifact:

  > `members = _array(row["allow"], f"policy.access_ceiling.{field}.allow", code); _unique(members, lambda item: item, ...)`

  > `tables = {"semantics", "providers", "models", "profiles", "capabilities", "validators", "credentials"}`
  > `for table in tables:`

- Verification: the delivered policy schema rejects a nested array target, but the compiler's
  parallel manual validator reaches `_unique` and raises raw `TypeError`. With two malformed catalog
  tables, set iteration produced different first error paths across clean hash seeds.
- Consequence: closed schemas are not the compiler's actual structural gate, failures are not always
  typed, and identical invalid logical input does not have deterministic source-linked diagnostics.
- Proposed fix: make the delivered schemas the single structural validator (wrapping errors into
  stable typed paths), retain only semantic checks in code, use fixed ordered table traversal, and
  fuzz every nested field with wrong scalar/container types under multiple hash seeds.

**Verdict:** **FIX**

## `implementations/tests/runtime/test_draft_graph_compiler.py`

### F8 — The harness proves the toy vectors but misses the implementation's load-bearing boundaries

- Severity: **MAJOR**
- Evidence from the artifact:

  > `self.assertEqual(result.graph, self.expected)`

  > `self.assertFalse(any(hasattr(DraftGraphCompiler, name) for name in ("confirm", "store", "schedule", "run", "launch", "execute")))`

  > `source.clear(); source.update({..., "immutable_uri": "urn:sha256:...", ...})`

- Verification: the positive fixture and N01–N24 all pass, but the harness never attempts public
  context/reservation forgery, result mutation, unsupported selectors, mutable URIs, conditional
  join satisfiability, feedback cycles, non-finite embedded JSON, a different impossible schema,
  schema/manual-validator parity or deterministic invalid-input paths. Each omitted mutation found
  a real failure above.
- Consequence: the suite is overfit to the reviewed toy and its enumerated negatives; its passing
  result cannot support O3/O6/O8 as currently worded.
- Proposed fix: add permanent regression tests for F1–F7, including at least one non-toy valid graph
  and mutation-style missing/extra/duplicate tests that pass through the complete public entry
  boundary.

**Verdict:** **FIX**

## `implementations/requirements.txt`

The added line is:

> `jsonschema==4.21.1`

The compiler imports Draft 2020-12 validation directly, the installed version is 4.21.1, directed
tests pass, and `pip check` reports no conflict involving this package. Existing unrelated
environment conflicts remain.

**Verdict:** **KEEP**

## Implementation follow-up documentation and schemas

### F9 — Validation overstates historical attribution and conformance coverage

- Severity: **MINOR**
- Files: `VALIDATION.md`, `TASK-SESSION.md`
- Evidence from the artifacts:

  > `None referenced the new compiler or test module. The failures were in pre-existing dispatch/runtime-type bootstrap surfaces`

  > `O3 | Close all five compiler inputs ... | covered`

  > `O6 | Validate predicates/topology/lifecycle/budgets ... | covered`

- Verification: filtering only the new test module reproduces every one of the 13 recorded
  failure/error classes, so they are independent of that test module in the current tree. However,
  the repository is dirty/shared and there is no clean pre-worker snapshot, so historical
  “pre-existing” attribution is stronger than the evidence. F1–F7 also refute the two “covered”
  conformance rows.
- Proposed fix: say “reproduced outside the new module in the current shared tree; historical
  preexistence not established”, record the 276/277 count drift, and mark affected obligations open
  until regression tests pass.

Artifact verdicts:

| Artifact | Verdict | Reason |
|---|---|---|
| `TASK-SESSION.md` | **FIX** | F9 and readiness claim depend on refuted coverage. |
| `VALIDATION.md` | **FIX** | F9 plus missing adversarial coverage. |
| `schemas/compilation-context.schema.json` | **KEEP** | closed frozen value shape is coherent; F1 is the public trust boundary around it. |
| `schemas/catalog.schema.json` | **KEEP** | closed shape is coherent; F7 is compiler/schema divergence. |
| `schemas/policy.schema.json` | **KEEP** | it correctly rejects the malformed attack; the compiler does not enforce it equivalently. |
| `schemas/resources.schema.json` | **FIX** | `immutable_uri` is only a non-empty string, so F5 is structurally admitted. |

## Change requests

1. **MAJOR** — Establish a non-forgeable allocator/context boundary; direct construction must not
   satisfy compiler trust.
2. **MAJOR** — Bind returned authority immutably to canonical bytes/digest and remove shared mutable
   aliases.
3. **MAJOR** — Strictly parse embedded JSON and reject the admitted class of impossible output
   contracts.
4. **MAJOR** — Return selector semantics to specification, close the grammar and validate it.
5. **MAJOR** — Restrict URI resources to verified content-addressed forms or remove them from this
   bounded compiler claim.
6. **MAJOR** — Define and implement condition-aware join/feedback topology semantics.
7. **MAJOR** — Use one deterministic closed structural validation path with typed errors.
8. **MAJOR** — Extend the harness with the verified F1–F7 mutations and a non-toy positive graph.
9. **MINOR** — Narrow broad-suite attribution and obligation language to what the evidence proves.

## Evidence boundary

This review proves the listed counterexamples against the current shared files and records exact
directed/broad test observations. It does not claim that the 13 broad failures existed before this
SWU; it proves only that they reproduce when the new compiler tests are excluded and that no other
runtime test imports the new compiler. It does not assess live allocator internals because none are
integrated, general JSON Schema satisfiability beyond the demonstrated contradictions, production
URI retrieval, confirmation/persistence/projectors/scheduler integration, or canonical v2
acceptance.

The bounded RFC 8785 behavior that was actually attacked—UTF-16 property ordering, Unicode
preservation/no normalization, safe integers, float rejection, shuffled-key equivalence and clean
positive processes—survived. Duplicate JSON keys were rejected. `requirements.txt` is justified.
Those surviving checks do not offset the authority, topology and validation findings above.

## Recheck 1 — 2026-09-01

- Prior frozen `review.md` SHA-256: exactly
  `8EECD3DE6CAF2B892C69D949E74338CE8AC0EB3F028CC1607F3EF33E3C650E1C`
- Recheck verdict: **FIX**
- Original findings resolved: `F1`, `F2`, `F3`, `F4`, `F5`, `F9`
- Original findings partially resolved: `F6`, `F7`, `F8`
- New surviving findings: `R1`, `R2`, `R3`
- `recheck_required`: `true`
- Exit reason: `original_repairs_verified_three_new_major_gaps_survive`
- Agents spawned by this reviewer: `0`

The worker did not alter the frozen review. This section appends the independent recheck and
supersedes only the aggregate verdict for the repaired corpus; the initial findings remain durable
history.

### Original finding status

| Finding | Status | Independent recheck evidence |
|---|---|---|
| F1 — forgeable allocator context | **RESOLVED within the declared fixture-only boundary** | invalid/tampered/swapped evidence, direct and subclass instances, unregistered `object.__new__`, copy/deep-copy/pickle and stale/bound receipts reject; WeakSet entries disappear after collection; 40 concurrent verify/compile calls passed. Static signed evidence can be replayed to issue another process-local object, but the docs explicitly make no live-freshness/key-lifecycle claim. |
| F2 — mutable result/digest confusion | **RESOLVED** | canonical bytes are the sole stored authority; digest is recomputed; graph and report accesses return independent decodes; nested mutations do not affect later reads or bytes. |
| F3 — invalid/impossible output schemas | **RESOLVED for the documented witness subset** | duplicate/non-finite JSON, metaschema-invalid content, required `false`, refs and composition reject on draft and emitted-EG validation. The heuristic can reject satisfiable schemas outside its small witness subset; the evidence boundary no longer claims general completeness. |
| F4 — unchecked selectors | **RESOLVED at compiler semantics** | `$` alone compiles; `$.x`, `/x`, URI-like and free-form values reject. The reviewed structural schema remains broader, but `IMPLEMENTATION-BOUNDARIES.md` explicitly records the semantic narrowing and no runtime interpretation remains. |
| F5 — unchecked URI resources | **RESOLVED** | the resource schema admits inline forms only; both content-addressed URNs and mutable HTTPS records reject before emission; UTF-8/base64 bytes are digest-checked. |
| F6 — topology conditions/feedback | **PARTIAL; R1 remains** | failure-only initial joins reject; optional reverse feedback no longer changes roots/DAG; required feedback rejects. R1 shows required-input readiness is still absent from `any_predecessor_succeeded`. |
| F7 — nondeterministic/untyped gates | **PARTIAL; R2 and R3 remain** | delivered schemas gate normal malformed values, nested policy containers return typed paths, fixed catalog order is hash-seed stable. R2 finds two raw Unicode exceptions; R3 finds filesystem I/O hidden before the purity sentinel. |
| F8 — overfit harness | **PARTIAL** | a non-toy graph, base64, F1–F7 regressions and hash-seed positives were added. The harness encodes the unsafe R1 expectation and misses R2/R3. |
| F9 — overstated broad baseline | **RESOLVED** | the docs now claim only current-tree independence. Independent exclusion ran 267 tests with exactly 7 failures and 6 errors and makes no historical claim. |

### R1 — `any_predecessor_succeeded` can start before all required producer inputs exist

- Severity: **MAJOR**
- Files: `implementations/server/runtime/draft_graph_compiler.py`,
  `implementations/tests/runtime/test_draft_graph_compiler.py`, `IMPLEMENTATION-BOUNDARIES.md`
- Evidence from the implementation:

  > `if not conditions or any(condition == "on_failure" for condition in conditions):`
  > `    _fail("DG_TOPOLOGY_INVALID", f"nodes[{key}].start_when", ...)`

  This checks route conditions but never relates `start_when` to the owning node's required inputs.
- Evidence from the test artifact:

  > `for start_when in ("all_predecessors_succeeded", "any_predecessor_succeeded"):`
  > `    ... self.assertEqual(self.compile(draft=variant).graph["nodes"][2]["start_when"], start_when)`

- Verification: the accepted `verify` variant has required node-output inputs from both
  `node:review` and `node:correct`. Under the literal `any_predecessor_succeeded` transition, review
  can satisfy the start condition before correct has produced the required correction. Neither the
  implementation boundary nor a pinned evaluator artifact says required-input availability adds a
  second start gate.
- Consequence: runtime behavior must either start with missing required authority input or invent a
  hidden wait rule, contradicting the “no runtime completion choice” boundary.
- Proposed fix: return required-input readiness to the governing topology specification. Until a
  pinned evaluator rule exists, reject `any_predecessor_succeeded` whenever required node-output
  inputs come from more than one predecessor; add early-producer, all/any and optional-input cases.

### R2 — Lone-surrogate strings still escape the typed structural boundary

- Severity: **MAJOR**
- File: `implementations/server/runtime/draft_graph_compiler.py`
- Evidence from the artifact:

  > `context_bytes = json.dumps(context_value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")`

  > `actual = "sha256:" + hashlib.sha256(record["digest_source"].encode("utf-8")).hexdigest()`

- Verification: a structurally accepted catalog with
  `providers[0].digest_source="\ud800"` raised raw `UnicodeEncodeError`; a context whose
  `dispatch_id` was the same escaped lone surrogate raised raw `UnicodeEncodeError` before typed
  stale/signature handling. JSON Schema considers these Python strings structurally valid, so the
  “actual gate” does not close the encoding domain.
- Consequence: malformed untrusted input can bypass `DraftGraphCompileError`, stable paths and
  deterministic no-output reporting at two authority boundaries.
- Proposed fix: reject lone surrogates recursively immediately after every JSON parse (or catch
  every encoding site and map it to the source structural error), and add all five input roots plus
  allocator evidence under clean-process/hash-seed tests.

### R3 — The compiler's purity and deployability depend on repository filesystem reads at import

- Severity: **MAJOR**
- Files: `implementations/server/runtime/draft_graph_compiler.py`,
  `implementations/tests/runtime/test_draft_graph_compiler.py`
- Evidence from the compiler:

  > `schema = json.loads(_SCHEMA_PATHS[name].read_text(encoding="utf-8"), ...)`

  > `_CONTRACT_VALIDATORS = _load_contract_validators()`

- Evidence from the purported purity test:

  > `with patch("builtins.open", sentinel), ...:`
  > `    self.compile()`

  The patch runs after module import, so it cannot observe schema-file reads.
- Verification: in a clean subprocess, replacing `Path.read_text` with an I/O blocker before import
  made importing the runtime compiler fail. The module requires seven mutable repository-doc paths,
  including the proposed EG schema, before any compiler object exists.
- Consequence: the “pure compiler/no I/O” claim is false at the public import boundary, and an
  installed server package without the repository documentation tree cannot import the compiler.
  Schema-file mutation before process start also changes compilation behavior without a code or
  pinned-contract change.
- Proposed fix: generate/package the reviewed schemas as immutable code/package data bound to an
  explicit contract digest, or inject a previously verified validator bundle outside the pure
  compiler. Add a clean import/compile test with filesystem access denied from process start.

### Recheck artifact verdicts

| Artifact | Verdict | Reason |
|---|---|---|
| `implementations/server/runtime/draft_graph_compiler.py` | **FIX** | R1–R3 survive. |
| `implementations/tests/runtime/test_draft_graph_compiler.py` | **FIX** | asserts R1's unsafe case and cannot observe R2/R3. |
| `implementations/requirements.txt` | **KEEP** | both direct dependencies are used, installed at the pinned versions and absent from `pip check` conflicts. |
| `IMPLEMENTATION-BOUNDARIES.md` | **FIX** | topology omits required-input readiness and purity/import contract. |
| `TASK-SESSION.md` | **FIX** | F6–F8 cannot be marked fully repaired. |
| `VALIDATION.md` | **FIX** | accurately reports its commands but overstates F6–F8 coverage. |
| allocator/context/policy/catalog/resource schemas and signed fixtures | **KEEP** | reviewed shapes and signatures are coherent; R2 requires an I-JSON semantic guard around schema-valid strings. |

### Recheck commands and results

| Check | Result |
|---|---|
| frozen prior review hash | exact `8EECD3...C650E1C` before this append |
| directed compiler suite | 17/17 pass |
| predecessor validator | exit `0`; all declared checks pass |
| compiler + adjacent protocol suite | 29/29 pass |
| `py_compile` | pass |
| exclusion broad suite | 267 tests; 7 failures and 6 errors, matching the documented current-tree outcome |
| allocator attack matrix | tamper/swap/direct/subclass/copy/pickle/stale/bound reject; lifetime and 40-thread sample behave as documented |
| result mutation matrix | graph/report reads defensive; bytes/digest remain coherent |
| schema/resource/selector matrix | strict JSON, required-false, refs/composition, URI, invalid base64 and non-root selectors reject |
| condition-aware topology | failure-only and required feedback reject; optional feedback works; **multi-producer required `any` accepted** |
| hostile Unicode | **raw `UnicodeEncodeError`** at context and catalog boundaries |
| import with filesystem reads blocked | **module import fails before purity sentinel can run** |
| `pip check` | only documented `python-bcb/httpx` and invalid-Django environment issues |
| scope check | worker artifacts remain within code/test/requirements and the implementation follow-up directory; predecessor review hash remains `E70B...3D94` |

### Recheck change requests

1. **MAJOR** — Define required-input readiness for `any_predecessor_succeeded` and fail closed until
   the governing evaluator contract resolves it.
2. **MAJOR** — Add a typed I-JSON/lone-surrogate guard across every input and evidence boundary.
3. **MAJOR** — Remove repository filesystem reads from the pure compiler import boundary and test
   purity from a clean process.
4. Re-run every original and recheck attack, then append a new frozen-hash recheck section.

### Recheck evidence boundary

This recheck proves the repaired behaviors and three counterexamples against the current shared
tree. The signed receipt establishes only possession of fixture allocator evidence; replay after a
real allocator-state change is intentionally unproved because no live allocator/key lifecycle is
in scope. The schema witness algorithm is sound for witnesses it constructs but incomplete for
general satisfiable JSON Schema; safe false rejection outside the documented subset was not treated
as authority expansion. Non-canonical but decodable base64 pad bits were observed; because the
current field ownership makes the exact encoded content string authoritative and verifies decoded
bytes, this review does not elevate that representation choice into a finding without a governing
canonical-base64 rule.

No confirmation, projector, persistence, scheduler, provider/tool/credential invocation or
canonical-v2 promotion was exercised. The aggregate remains **FIX** solely because R1–R3 are
verified load-bearing omissions; the other original repairs survived independent attack.

## Recheck 2 — 2026-09-01

- Prior frozen `review.md` SHA-256: exactly
  `03B351EB4796B3149C64F7CB715B60EB9F58BACE899D4495208A8529FDBFC88A`
- Recheck verdict: **FIX**
- Original findings resolved: `F1`, `F2`, `F3`, `F4`, `F5`, `F7`, `F9`
- Original findings partially resolved: `F6`, `F8`
- Recheck findings resolved: `R2`, `R3`
- Recheck finding partially resolved: `R1`
- `recheck_required`: `true`
- Exit reason: `always_route_breaks_any_join_success_dominance`
- Agents spawned by this reviewer: `0`

The worker did not alter the frozen review. This section appends the second independent recheck and
supersedes only the aggregate verdict for the repaired corpus. The initial review and Recheck 1
remain durable history.

### Finding status after the second repair

| Finding | Status | Independent recheck evidence |
|---|---|---|
| F1–F5 | **RESOLVED within the previously documented boundaries** | The second repair did not reopen these surfaces; the directed suite preserving their attacks passes. |
| F6 — topology conditions/feedback | **PARTIAL; R1 remains** | Required inputs from optional outputs now reject, multi-producer `any` rejects, optional inputs do not add readiness obligations, and an `on_success` ancestor can satisfy the documented dominance rule. An `always` ancestor is still incorrectly treated as already succeeded. |
| F7 — deterministic typed gates | **RESOLVED for the declared input domain** | Recursive scalar guards now cover member names and values at every parsed boundary, inner schemas and both public comparison/canonicalization helpers. Clean-process seed tests pass, and additional key/value attacks returned typed stable paths. |
| F8 — non-overfit harness | **PARTIAL** | The suite now includes R1–R3 regressions and non-toy positives, but it does not distinguish success-preserving ancestry from ancestry reached through `always`; therefore the unsafe graph below remains untested. |
| F9 — claim discipline | **RESOLVED** | `VALIDATION.md` and `TASK-SESSION.md` explicitly say the broad/exclusion suites were not rerun and retain only the prior current-tree-independence claim. |
| R1 — required-input readiness | **PARTIAL; MAJOR residual below** | Producer-output requiredness and unqualified graph dominance were added. The dominance relation erases route conditions, so it is not a proof that an ancestor succeeded and emitted its required output. |
| R2 — lone-surrogate escape | **RESOLVED** | Context, evidence, draft, policy, catalog, resources, embedded schema member names/values, canonicalization and match attacks fail as `DraftGraphCompileError`; a valid escaped surrogate pair decodes to one Unicode scalar and canonicalizes. |
| R3 — filesystem-dependent import | **RESOLVED** | All seven compressed blobs decode byte-for-byte to their review artifacts and match their explicit SHA-256 values. Digest/blob corruption makes validator loading fail closed. A clean import succeeds with file/path, environment, network, subprocess, time and random access blocked after dependencies are loaded. |

### R1 residual — `always` ancestry is not success dominance

- Severity: **MAJOR**
- Files: `implementations/server/runtime/draft_graph_compiler.py`,
  `implementations/tests/runtime/test_draft_graph_compiler.py`, `IMPLEMENTATION-BOUNDARIES.md`
- Evidence from the implementation:

  > `for predecessor in incoming[key]:`
  > `    ancestors[key].add(predecessor)`
  > `    ancestors[key].update(ancestors[predecessor])`

  > `available_producers = ancestors[possible_trigger] | {possible_trigger}`

  `incoming` contains both `on_success` and `always` initial routes. The transitive closure records
  only node reachability and discards which condition established that ancestry.
- Evidence from the implementation boundary:

  > `all required input producers are that predecessor or its already-succeeded ancestors`

  An ancestor connected to a successful trigger through `always` is known only to have completed;
  it is not known to have succeeded or emitted its required output.
- Verification: an adversarial three-node graph was accepted with these changes to the positive
  fixture: `correct` no longer consumes the review output; `review -> correct` is an authored
  `control/always` route; `verify` uses `any_predecessor_succeeded`, requires `review_report`, and
  treats `correction` as optional. The compiler emitted both data triggers into `verify` and returned
  digest `sha256:1c1c80c0f436bdd229f06863a14aa1e5df8d34fd566a1dffb425677ecb008131`.
  If `review` fails, `always` can activate `correct`; when `correct` succeeds it can activate
  `verify`, although the required `review_report` cannot exist. The current ancestry test accepts
  this because `review` is an unqualified ancestor of `correct`.
- Consequence: the compiled graph can reach a declared runnable state without a required input.
  A runtime must either violate the required-input contract or invent an additional hidden wait,
  so the compiler has not eliminated runtime completion choice.
- Proposed fix: compute success-guaranteed dominance, not plain graph ancestry. For every possible
  successful trigger of an `any` join, each required producer must be the trigger itself or reach it
  only through a path whose activation proves that producer succeeded. In particular, an `always`
  route cannot establish producer-output readiness. Add the exact failing graph as a permanent
  regression alongside `on_success`, optional input/output, non-ancestor, feedback and mixed-join
  cases.

### Recheck 2 artifact verdicts

| Artifact | Verdict | Reason |
|---|---|---|
| `implementations/server/runtime/draft_graph_compiler.py` | **FIX** | The route-insensitive ancestor closure leaves R1 semantically open. |
| `implementations/tests/runtime/test_draft_graph_compiler.py` | **FIX** | It lacks the accepted `always`-ancestor counterexample. |
| `implementations/requirements.txt` | **KEEP** | No new dependency issue was introduced by the second repair. |
| `IMPLEMENTATION-BOUNDARIES.md` | **FIX** | Its "already-succeeded ancestors" claim is stronger than the implemented route-insensitive proof. |
| `TASK-SESSION.md` | **FIX** | It marks R1 and F6/F8 ready despite the accepted counterexample. |
| `VALIDATION.md` | **FIX** | Its R1 coverage claim omits the route-condition distinction. Broad/exclusion reporting itself is appropriately bounded. |
| embedded schemas and allocator fixtures | **KEEP** | Exact embedded bytes and digests match all seven reviewed artifacts; no R2/R3 defect survived. |

### Recheck 2 commands and results

| Check | Result |
|---|---|
| frozen prior review hash | exact `03B351...FC88A` before this append |
| directed compiler suite | 21/21 pass |
| predecessor validator | exit `0`; all declared checks pass |
| compiler + adjacent protocol suite | 33/33 pass |
| `py_compile` | pass |
| broad/exclusion suites | not rerun; documentation says so explicitly and does not upgrade the retained evidence |
| required-output/optional-input and ordinary dominance matrix | declared regressions pass |
| `always`-ancestor readiness attack | **unsafe graph accepted** with digest `sha256:1c1c80c0f436bdd229f06863a14aa1e5df8d34fd566a1dffb425677ecb008131` |
| Unicode scalar attacks | typed stable failures for keys/values and public helpers; valid pair accepted |
| embedded contract correspondence | 7/7 decompressed byte strings equal artifacts and match explicit SHA-256 |
| corrupt embedded digest/blob | validator loader raises `RuntimeError` |
| clean pure import | succeeds with filesystem, environment, network, subprocess, time and random hooks blocked after dependency preload |
| scope/review freeze | prior review hash exact; shared worktree remains dirty, so no stronger historical attribution is made |

### Recheck 2 change request

1. **MAJOR** — Replace route-insensitive ancestry with success-guaranteed dominance for required
   producers at `any_predecessor_succeeded`, add the `control/always` counterexample as a regression,
   and rerun the directed, adjacent, predecessor and compile checks before another frozen-hash
   recheck.

### Recheck 2 evidence boundary

This recheck verifies the R2 and R3 repairs and the ordinary R1 matrix against the current shared
tree. It does not execute a scheduler; the R1 counterexample follows directly from the documented
`always` and `any_predecessor_succeeded` activation semantics and the emitted graph. It does not
claim tamper resistance against arbitrary mutation of private Python module globals. It verifies
that fresh returned digest maps are defensive and that the embedded loader fails closed when its
digest or blob input is corrupted.

No broad suite was rerun, and no historical claim is inferred from the dirty worktree. No
confirmation, persistence, projector, runtime scheduler or canonical-v2 promotion was exercised.
The aggregate remains **FIX** solely because R1 still admits a graph whose required input need not
exist when its `any` join activates.

## Recheck 3 — 2026-09-01

- Prior frozen `review.md` SHA-256: exactly
  `826E73E87090D5A757092BCE8C3AB22984232D70D7F24AECD1EEED31B26B0760`
- Recheck verdict: **KEEP**
- Original findings resolved: `F1`–`F9`
- Recheck findings resolved: `R1`, `R2`, `R3`
- New findings: none
- `recheck_required`: `false`
- Exit reason: `conditional_readiness_counterexample_closed_no_new_finding_survived`
- Agents spawned by this reviewer: `0`

The worker did not alter the frozen review. This section appends the final independent recheck and
supersedes only the aggregate verdict for the repaired bounded corpus. Earlier findings remain
durable history.

### Coverage and zero-findings defence

| Lens | Targets attacked | Why no finding survived |
|---|---|---|
| mechanics / correctness | conditional dataflow, route conditions, joins, required inputs, feedback and state cap | The original accepted graph now rejects; hand-built and generated graphs agreed with an independent exhaustive activation model, and every directed/adjacent check passes. |
| fidelity / governance | `IMPLEMENTATION-BOUNDARIES.md`, code semantics and readiness claims | The route-event interpretation, conservative feedback rule and 4,096-state false-negative ceiling are stated explicitly and match the implementation. No runtime or canonical-v2 authority is claimed. |
| abuse / gaming | mixed duplicate routes, incompatible success/failure histories, multiple roots, optional outputs and hash iteration | Contradictory histories are discarded, missing must-producers reject, required inputs cannot bind optional outputs, and diagnostics remained stable across seeds. |
| operability | clean bounded compilation and regression corpus | Directed 22/22, adjacent 34/34, predecessor validation and `py_compile` pass; R2/R3 and F1–F9 attacks remain in the directed suite. |

The zero-findings result is not based only on the worker tests. The reviewer independently exercised
the exact prior counterexample, chains, diamonds, multiple roots, `any`/`all`, `always`,
`on_success`, `on_failure`, compatible and incompatible histories, required/optional producer
outputs, resource-only inputs, feedback targets, unreachable topology and the state ceiling.

### R1 final status — resolved within the documented conditional initial-DAG model

The repair replaces route-insensitive ancestry with outcome-state propagation. Evidence from the
compiler:

> `return None if succeeded & failed else (succeeded, failed)`

> `must_available = set.intersection(*(set(state[0]) for state in start_states))`

> `missing = required_input_producers[key] - must_available`

`on_success` contributes only source-success states, `on_failure` only source-failure states, and
`always` both. Incompatible all-route histories cannot merge. A consumer is admitted only when
every state that can activate it contains every required producer in the succeeded set.

The exact Recheck 2 counterexample now returns
`DG_TOPOLOGY_INVALID|nodes[verify].start_when|some activating outcome lacks required producer inputs: review`.
The corresponding success-only route compiles. An `all` join over the same source's `on_success`
plus `on_failure` routes rejects as mutually unsatisfiable, while `on_success` plus `always` narrows
to the compatible successful history and compiles.

Two independent generated corpora were compared with an exhaustive event/outcome simulator:

- 300 four-node DAGs: 80 accepted, 220 rejected, 0 mismatches;
- 300 five-node DAGs with shared histories: 76 accepted, 224 rejected, 0 mismatches.

The simulator explored scheduler order and both outcomes for every activated node, marking a graph
unsafe whenever a consumer could activate before all required producers had succeeded. This checks
the implementation against the documented closed route-event semantics; it is not evidence about
an unimplemented runtime scheduler.

### State ceiling and conservative cases

An `always` chain that produces exactly 4,096 distinct outcome states compiled. Extending it by one
node to 8,192 possible states rejected at `nodes[n13].start_when` with
`conditional readiness proof exceeds the closed state limit`. This is the false-negative behavior
explicitly permitted by `IMPLEMENTATION-BOUNDARIES.md`; the compiler did not assume readiness after
the proof ceiling.

Feedback targets with required node-output inputs reject conservatively, while a feedback target
whose required inputs are material resources compiles. Required reverse feedback inputs and
required inputs bound to optional producer outputs reject. These restrictions are explicit and
bounded, so they are not undocumented false negatives.

### Recheck 3 artifact verdicts

| Artifact | Verdict | Reason |
|---|---|---|
| `implementations/server/runtime/draft_graph_compiler.py` | **KEEP** | Conditional must-availability closes the verified R1 counterexample and survived independent generated attacks. |
| `implementations/tests/runtime/test_draft_graph_compiler.py` | **KEEP** | It preserves F1–F9/R2/R3 and now includes the exact R1 counterexample plus compatible/incompatible route cases. |
| `implementations/requirements.txt` | **KEEP** | Both pinned direct dependencies remain exercised; no dependency change belongs to the residual R1 repair. |
| `IMPLEMENTATION-BOUNDARIES.md` | **KEEP** | It accurately defines route events, must-availability, feedback conservatism and the finite state ceiling. |
| `TASK-SESSION.md` | **KEEP** | It limits readiness to reviewer recheck, fixture-only compilation and the stated residue. |
| `VALIDATION.md` | **KEEP** | Counts and evidence ceilings match the rerun checks; retained broad evidence is explicitly not presented as current rerun evidence. |
| embedded schemas and allocator fixtures | **KEEP** | The R1-only repair did not alter their reviewed boundary; their directed R2/R3/F1–F9 checks pass. |

### Recheck 3 commands and results

| Check | Result |
|---|---|
| frozen prior review hash | exact `826E73...B0760` before this append |
| directed compiler suite | 22/22 pass |
| predecessor validator | exit `0`; every declared check passes |
| compiler + adjacent protocol suite | 34/34 pass |
| `py_compile` | pass |
| original `always` counterexample | typed rejection at `nodes[verify].start_when` |
| hand-built conditional matrix | expected acceptance/rejection for chains, diamonds, mixed routes, roots, resources, outputs and feedback |
| generated exhaustive comparison | 600 graphs; 156 accepted, 444 rejected, 0 model mismatches |
| state ceiling | 4,096 accepted; 8,192 rejected fail-closed with typed path |
| hash-seed diagnostic | 12/12 identical code, path and detail for the prior R1 counterexample |
| broad/exclusion suites | not rerun; documentation preserves only the earlier current-tree result and says so explicitly |
| scope/review freeze | prior review hash exact; shared worktree remains dirty, so no historical scope attribution is inferred |

### Change requests

None. No CRITICAL, MAJOR or MINOR finding survived verification in the bounded implementation
corpus.

### Recheck 3 evidence boundary

This KEEP applies only to the pure fixture-backed DraftGraph-to-proposed-ExecutionGraph compiler and
the conditional initial-DAG semantics documented in `IMPLEMENTATION-BOUNDARIES.md`. It establishes
that the previously verified counterexamples are closed and that no new defect survived the stated
attacks. The 4,096-state ceiling intentionally permits documented safe false rejection.

No live allocator, feedback scheduler, provider/tool/credential invocation, confirmation,
persistence, projector or canonical-v2 acceptance ran. General JSON Schema satisfiability remains
outside the admitted witness subset. The broad runtime suite was not rerun. Accordingly, **KEEP**
recommends this bounded corpus as input to the next canonical-v2 specification work unit; it does
not make it runtime or production authority.
