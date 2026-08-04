---
tags: [agents-communication-infra, spec, test, protocol-compilation]
node_type: spec
is_session: false
layer: application
nature: [procedural, technical]
status: draft
version: 0.2.0
last_updated: 2026-08-03
---

# Test Spec: ACI Protocol Compilation Candidate v1

This aspect-level test specification elaborates the T-ACI-PC1 through T-ACI-PC12 index already present in the [feature-wide TEST-SPEC](../TEST-SPEC.md) and defines the executable proof required for the bounded protocol-compilation slice in [SPEC.md](SPEC.md) and [protocol-compilation.md](protocol-compilation.md). The current fixture source is [`fixtures/protocol-compilation-v1/`](fixtures/protocol-compilation-v1/); it supplies one admitted compiled case and one admitted required-unsupported case, not an implementation, executable harness, negative corpus, or conformance receipt.

## Test Matrix

| ID | Test | Required assertion | Validates |
|---|---|---|---|
| [T-ACI-PC1](#t-aci-pc1--closed-schema-rejection) | Closed-schema rejection for request, every document, every nested item, candidate, and result | Unknown, missing, duplicate, forbidden-null, and wrong-primitive mutations fail with the specified first error and produce no result, candidate, artifact descriptor, or mutation. | [Canonical contract](protocol-compilation.md#canonical-contract-common-to-every-schema), [closed failures](protocol-compilation.md#closed-failures), [PC-R1](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC2](#t-aci-pc2--canonical-bytes-and-golden-digests) | Canonical-byte and digest golden vectors | NFC, key order, contract array order, optional omission, shortest signed-64-bit integers, UTF-8/no-BOM/no-newline encoding, and rejected floats yield exact bytes and qualified lowercase SHA-256 digests. | [Canonical contract](protocol-compilation.md#canonical-contract-common-to-every-schema), [frozen fixture](protocol-compilation.md#frozen-v1-fixture-and-admission), [PC-R9](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC3](#t-aci-pc3--digest-verification-and-lineage-invalidation) | Digest and compiler-identity verification with complete lineage invalidation | Each input-document digest mismatch is `digest_mismatch`; every non-fixed compiler digest is solely `compiler_identity_mismatch`; every semantics-bearing canonical-byte change prevents reuse of the old `source_binding` lineage. | [CompileDispatchCandidate](protocol-compilation.md#compiledispatchcandidate), [DispatchCandidate](protocol-compilation.md#dispatchcandidate), [PC-R11](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC4](#t-aci-pc4--parameter-and-placeholder-closure) | Parameter, value, and placeholder closure without inference | Missing, extra, duplicate, unsorted, undeclared, out-of-bounds, wrong-type, coercion-dependent, default-dependent, and undeclared-placeholder cases fail with no candidate. | [SkillProtocolInvocation](protocol-compilation.md#skillprotocolinvocation), [CompileDispatchCandidate](protocol-compilation.md#compiledispatchcandidate), [PC-R7](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC5](#t-aci-pc5--total-obligation-disposition) | Total obligation mapping and closed `unsupported` result | Coverage is total and unique; every disposition shape is enforced; the admitted required-unsupported case returns only the closed blocked result; a schema-valid superseded-obligation third tuple is rejected by admission. | [ObligationDisposition](protocol-compilation.md#obligationdisposition), [compile result](protocol-compilation.md#compile-result), [PC-R4/PC-R5](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC6](#t-aci-pc6--dag-closure-and-deterministic-rejection) | DAG closure, acyclicity, reachability, and deterministic rejection | Unknown endpoints/references, duplicate IDs, unsorted sets, self-edges, cycles, unreachable terminal paths, outgoing terminal edges, terminal-kind mismatch, and safety-bound excess fail as specified. | [DAG validity](protocol-compilation.md#dag-validity), [closed failures](protocol-compilation.md#closed-failures), [PC-R6](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC7](#t-aci-pc7--logical-capability-ceiling) | Logical capability projection has no effective authority | Candidate requirements equal the profile requirements byte-for-byte and contain no provider, model, credential, permission, availability, resolution, enforcement, sandbox, or effective-grant claim. | [DispatchCandidate](protocol-compilation.md#dispatchcandidate), [mapping](protocol-compilation.md#protocolinputstodispatchcandidate), [PC-R8](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC8](#t-aci-pc8--determinism-across-restarts) | Repeated compilation and storage across fresh processes | Equal canonical request/compiler identities produce byte-identical result and candidate bytes/digests before and after restart; equal stored bytes resolve to the same content-derived artifact identity. | [CompileDispatchCandidate](protocol-compilation.md#compiledispatchcandidate), [artifact persistence](protocol-compilation.md#artifact-persistence-seam), [PC-R9](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC9](#t-aci-pc9--pure-compilation-has-zero-effects) | Spied pure-compiler boundary | Compilation performs zero clock, random, environment, filesystem-discovery, registry, network, provider, model, tool, scheduler, bus, journal, confirmation, pending-sheet, YAML, legacy-dispatch, or persistence calls. | [CompileDispatchCandidate](protocol-compilation.md#compiledispatchcandidate), [ProtocolCompiler](protocol-compilation.md#protocolcompiler), [PC-R10](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC10](#t-aci-pc10--separate-idempotent-artifact-persistence) | Separate application persistence seam | Store is invoked only after `compiled`; equal content/policy is idempotent, unequal content at one identity is `artifact_content_conflict`, no runtime authority receipt is produced, and any existing ArtifactStore finalization metadata remains outside candidate/result bytes. | [Artifact persistence seam](protocol-compilation.md#artifact-persistence-seam), [ownership boundary](protocol-compilation.md#ownership-and-authority-boundary), [PC-R10](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC11](#t-aci-pc11--admitted-fixture-cases-and-field-provenance) | Exact admission of both frozen cases and compiled-field trace | Both exact four-digest tuples pass production admission before result construction; the compiled case equals `candidate.json`/`result.json`, the required-unsupported case equals `unsupported-result.json`, and every declared fixture digest verifies. | [Frozen fixture](protocol-compilation.md#frozen-v1-fixture-and-admission), [mapping](protocol-compilation.md#protocolinputstodispatchcandidate), [PC-R2/PC-R3](protocol-compilation.md#rules-and-invariants) |
| [T-ACI-PC12](#t-aci-pc12--candidate-authority-firewall) | Candidate cannot cross the confirmation/runtime authority boundary | Candidate bytes/digest cannot validate as `DispatchSpec` or `dispatch_spec_digest`; no exposed path creates `ConfirmedDispatch`, `Run`, attempt, command/event/receipt, provider call, schedule, pending-sheet/YAML/legacy mutation, or other effect. | [Ownership boundary](protocol-compilation.md#ownership-and-authority-boundary), [DispatchCandidate](protocol-compilation.md#dispatchcandidate), [PC-R12](protocol-compilation.md#rules-and-invariants) |

## Test Details

### T-ACI-PC1 — Closed-schema rejection

Generate one-field mutations from each closed schema and nested closed item. Exercise duplicate keys against raw JSON before ordinary object decoding. Whitespace, alternate key order, BOM or a terminal newline on the outer request is `invalid_request_schema`. For embedded documents, closed-schema validation, including duplicate-key rejection, precedes canonical-form and digest checks; only a schema-valid noncanonical embedded document is `noncanonical_bytes`. Assert the total failure precedence in `CompileDispatchCandidate`; every failing case must leave result bytes, candidate bytes, artifact references, and mutation spies empty.

### T-ACI-PC2 — Canonical bytes and golden digests

Use byte-level golden vectors, not semantic JSON equality. At minimum include precomposed/decomposed Unicode pairs and normalization collisions, reverse key order, every contract-defined array ordering rule, omitted optional `authority_ref`, signed-64-bit endpoints, boolean-versus-integer, insignificant whitespace/BOM/trailing-newline inputs, raw 64-hex digests, uppercase hex, floats, NaN and infinities. Assert both exact accepted bytes and exact `sha256:<lowercase hex>` values.

The immutable oracle is the literal raw-file/canonical-document digest table under [Fixture Corpus and Readiness](#fixture-corpus-and-readiness), including the manifest. A test MUST compare against those literals as well as the manifest contents; trusting only the mutable manifest would not detect coordinated fixture drift.

### T-ACI-PC3 — Digest verification and lineage invalidation

Mutate the profile, binding, recipe, and invocation documents independently, first retaining the old digest and then recomputing the local digest while retaining every dependent old reference. The former cases must produce `digest_mismatch`; the other recomputed cases fail at their first dependent identity check and must never reuse prior candidate lineage. The request carries only `compiler_contract_digest`, never a compiler-contract document: every value other than the frozen digest must produce solely `compiler_identity_mismatch`. Assert all seven `DispatchCandidate.source_binding` fields exactly once.

### T-ACI-PC4 — Parameter and placeholder closure

Cover required and optional values, duplicate/unsorted/undeclared values, string bounds, integer bounds, enum membership, boolean/integer separation, forbidden defaults and coercion, malformed recipe placeholders, and placeholders undeclared by the node. Invocation string values containing either `{{` or `}}` MUST return `invalid_parameter_value` before admission. This closed V1 rule makes recursive or second-pass template evaluation unreachable; the compiler also performs no code execution, include expansion or environment lookup and may not consult skill prose, previous runs or defaults.

### T-ACI-PC5 — Total obligation disposition

Prove set equality between profile obligation IDs and recipe rule IDs, unique coverage, target resolution, and the exact shape of `preserved`, `compiled`, `superseded`, and `unsupported`. Use the frozen `required-unsupported` tuple and prove that production admission succeeds before the pure calculation returns exact `unsupported-result.json`; assert the absence of candidate and artifact fields. Separately mutate the compiled recipe obligation to `superseded`, supply its required authority reference, recompute the recipe plus dependent binding/invocation digests, and assert that the otherwise schema-valid third tuple reaches admission and returns `fixture_not_admitted`. Single-fault malformed or inconsistent mutations may prove earlier obligation errors through the same production entry point; no test path may admit that third tuple.

### T-ACI-PC6 — DAG closure and deterministic rejection

Use single-fault graph mutations for every DAG invariant and assert `invalid_graph` only when all earlier categories are valid. Include deterministic topological tie cases, but do not permit the implementation to reorder caller-supplied semantic ordered sets or repair any graph.

### T-ACI-PC7 — Logical capability ceiling

Deep-compare the canonical profile requirement bytes with the candidate projection. Scan the complete candidate/result schema for forbidden authority-bearing names and inject attempts to add such fields; closed validation must reject them rather than preserve or silently discard them.

### T-ACI-PC8 — Determinism across restarts

Run the same canonical request repeatedly in one process and in at least two fresh processes with isolated transient state. Compare full result bytes, embedded candidate text, candidate digest, and—when the separate storage path is invoked—content-derived artifact identity. Receipt metadata is boundary-owned and is not part of result/candidate equality.

### T-ACI-PC9 — Pure compilation has zero effects

Construct the pure compiler with fail-on-call spies for every forbidden dependency class. The admitted compiled case, admitted required-unsupported case, and representative failures must all complete without a spy invocation. Artifact storage is not present in this test's dependency graph.

### T-ACI-PC10 — Separate idempotent artifact persistence

Exercise `compile_and_store_dispatch_candidate` separately from the pure compiler. Assert no store call for any failure or `unsupported`; one idempotent put after `compiled`; exact metadata `schema_ref="aci.dispatch-candidate@1"`, `classification="runtime-internal"`, `content_hash=candidate_digest`, and `media_type="application/json"`; stable identity for equal content/policy; and `artifact_content_conflict` with no artifact descriptor or mutation when unequal bytes are presented at the same identity. Spies must prove that this application seam creates no runtime authority or effect. If the existing ArtifactStore implementation emits finalization metadata, its receipt reference is allowed only as boundary-owned operational metadata outside candidate/result bytes; this slice neither requires such a receipt nor treats one as compilation evidence.

### T-ACI-PC11 — Admitted fixture cases and field provenance

Load every transport file, verify raw-file and canonical-document hashes against the literal table below and the manifest, then assemble both exact closed requests from canonical no-newline document text. For each case, prove the exact four-digest tuple passes the production admission gate before any result is constructed. Assert the compiled case's exact equality with `candidate.json` and `result.json`, the required-unsupported case's exact equality with `unsupported-result.json`, and no candidate for the latter. Maintain a field-provenance assertion covering every compiled candidate leaf and the two allowed scalar substitutions for `topic`.

### T-ACI-PC12 — Candidate authority firewall

Test schema/API separation at every exposed boundary: candidate schema must not parse as `DispatchSpec`, `candidate_digest` must not satisfy a `dispatch_spec_digest`, and compiler/storage interfaces must expose no confirm, resolve, run, launch, schedule, activate, or revoke method. Use fail-on-call spies around confirmation, journal, bus, provider, scheduler, pending-sheet, YAML and legacy adapters.

## Fixture Corpus and Readiness

| Corpus item | Present state | What it can prove | What it cannot prove |
|---|---|---|---|
| `protocol-compilation-v1@1` transport files | Present: one shared skill source and compiler contract; compiled profile/binding/recipe/invocation/candidate/result; required-unsupported profile/binding/recipe/invocation/result; and one two-case manifest | Two exact production-admitted read-only cases and the declared raw/canonical hashes. A bounded 2026-08-03 fixture inspection found those hashes mutually consistent. | Compiler behavior, parser strictness, restart determinism, negative failures, effect isolation, or storage behavior. |
| Canonicalization edge-case goldens | Absent | Nothing yet. | NFC/collision behavior, ordering variants, integer boundaries, omission, encoding rules, and float rejection required by T-ACI-PC2. |
| Closed-schema and semantic negative vectors | Absent | Nothing yet. | T-ACI-PC1 and T-ACI-PC3 through T-ACI-PC7 rejection/error precedence. |
| Required-unsupported golden vector | Present in the same frozen package and manifest as the compiled case | Exact production admission followed by exact `unsupported-result.json`, with no candidate or persistence. | General recipe admission or implementation conformance without an executable harness. |
| Restart/effect-spy/storage/boundary harness | No harness or execution receipt is identified by the inspected sources | Nothing yet. | T-ACI-PC8 through T-ACI-PC10 and T-ACI-PC12. |

The checked-in JSON files are newline-terminated transport containers. Their current consistency is fixture inspection evidence only; it is not proof that a compiler implementation exists or conforms.

The following literals bind every checked-in JSON transport file and its strict-parse `aci-cjson-1` document. Raw hashes include the repository terminal newline; canonical hashes bind compact UTF-8 JSON without that transport newline.

| Transport file | Raw file SHA-256 | Canonical document digest |
|---|---|---|
| `skill-source.json` | `sha256:1a1b13f817e88b9ab08f05c15ca33b709d75fa0cd153455cfe9cf35480e1a742` | `sha256:13ea3dea6640fd553a56662c7efd4bc63480f82b07c49f6e3614b72f4201bc36` |
| `profile.json` | `sha256:da430d5f1cb0bc73c20f5722a5678c993983d70a6b3076f33021083dadd19ed5` | `sha256:43229944b101d12c6d14008d1db17f40c41277b7b441417c7ca5cd38006d7d17` |
| `recipe.json` | `sha256:05731f234c5a9aaada6b253c012219da33ae36301820b85bd7f5d55c2953d0bd` | `sha256:92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3` |
| `binding.json` | `sha256:e8e6a30e697b4bf0a646c1345a1c3a299b95fcd66dc8cc41f6fc7405936df681` | `sha256:26d7a8a3fb4955a9442d5807b7c27c1c1f204b394e3862437c49a4aae5b14c7b` |
| `invocation.json` | `sha256:d83595d04a3a4808dc8925aba6195561a37ffea75d7512e9d388749743be66ce` | `sha256:469dff24fc67a048a0f5f7040704c3601861beb386b9713dc3eb4e3b233de77b` |
| `compiler-contract.json` | `sha256:6b15b4f6091058181cf7f32c9a8f155b5c0d8a6e6d4e9c35c6a36c716b2b947b` | `sha256:9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543` |
| `candidate.json` | `sha256:e05ae398a2f6111e3fff4620156b28320eeebbb835bee3a0c2f4a7d77a26f9b4` | `sha256:9b829ca70a4717a133a8e42b18e7d95210d1bbfcd5c1e785b56b38778f6df795` |
| `result.json` | `sha256:09714366cd3af0e3f965570b77c334bd3fc880ff38bb80b1ef379945039d0542` | `sha256:1a38bb57cddfc8940c1ff19011f543b18e8844a2e2d68b12a340ded527aecb84` |
| `unsupported-profile.json` | `sha256:0db09987f24184a2e05aa7179f3017283a81f646afeb69d0d60035e6f597322b` | `sha256:43ec4c29eca01a6786ec9fff2723c2623828af286e80c67f2b320672d002fa1e` |
| `unsupported-recipe.json` | `sha256:e89e07b4ad082a7cf00e00fe2eb3125e22fdc054a6e31a635dce9fd67d068da3` | `sha256:16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1` |
| `unsupported-binding.json` | `sha256:9e021be2fecd37b594d8d586086027d4a79413fe5f2b366dd2dd7a40a5ee114b` | `sha256:10bc707b787041d8b3327a1f3096b5635fae56d75975b0ffbf81f82fa2b00f8a` |
| `unsupported-invocation.json` | `sha256:ef06ac2d4cd7deaf59b9c570af1b638574caeefceed33d6592e5d001c68e7e5c` | `sha256:0fdbd75e214f91a0ad53cec35849d43208af1d51dfa1f1c0300cfa0be3a11c17` |
| `unsupported-result.json` | `sha256:61c7722659c8c152c35e6f8c0887b2b48e9862e202db70cdfd220ed1ece29ad4` | `sha256:9544a32ccf39309dc778d78623948675c9f80e73ecae52a0108458db35ae0578` |
| `manifest.json` | `sha256:8b902a972e7c605dc5df3ba51b35a0e1d0c0bfafb7d27d7e592f7bbcc49b7553` | `sha256:e5cc329254ab8f748888f198ee004cba45f186b5ca21702612932f2c66ef0420` |

## Failure and No-Artifact Oracle

The suite must encode the total failure precedence exactly as specified: `invalid_request_schema`; ordered `invalid_document_schema`; ordered `noncanonical_bytes`; ordered `digest_mismatch`; `compiler_identity_mismatch`; `inactive_binding`; `binding_mismatch`; `invocation_mismatch`; `invalid_parameter_value`; `invalid_obligation_mapping`; `invalid_graph`; then `fixture_not_admitted`. Closed-schema validation therefore wins over canonical-form and digest faults in the same embedded document. A typed compile failure returns no result object, candidate bytes, partial candidate, artifact descriptor, or persistent mutation.

Admission is one step of the pure production calculation, not a wrapper exception or alternate test entry point. The exact four-digest tuple must match one of the two immutable manifest cases before either result branch is constructed. The admitted compiled case may proceed to candidate construction; the admitted required-unsupported case returns only the closed non-success result and produces no candidate or artifact. A schema-valid third tuple returns `fixture_not_admitted`.

Include combined-fault vectors that prove each adjacent precedence boundary: invalid outer request over every embedded fault; profile schema failure over profile noncanonical bytes; profile noncanonical bytes over profile digest mismatch; an earlier document's digest mismatch over a later document's schema-valid semantic fault; compiler identity mismatch over inactive binding; inactive binding over binding mismatch; binding mismatch over invocation mismatch; invocation mismatch over invalid parameters; invalid parameters over invalid obligation mapping; invalid obligation mapping over invalid graph; and invalid graph over a non-admitted tuple. Every vector asserts the exact first error and the common no-result/no-artifact/no-mutation oracle.

Persistence is tested only after a successful pure compilation. `artifact_content_conflict` belongs to that separate seam and must not be observable from `ProtocolCompiler.compileCandidate`.

## Known Gaps

### G1 — Canonicalization and negative goldens are absent

The frozen corpus has no durable byte-level variants for the canonicalization and rejection matrix. T-ACI-PC1 through T-ACI-PC7 cannot claim executable conformance until versioned golden and negative vectors exist and are reviewed.

### G3 — Bounded executable evidence now exists

`implementations/tests/runtime/test_protocol_compilation.py` supplies generated negative matrices,
golden vectors, effect spies, restart/storage checks and authority-firewall checks for T-ACI-PC1
through T-ACI-PC12. The focused 13-test run and complete 131-test runtime suite pass, and two
independent re-reviews report PASS. Coverage remains `bounded`: PC12 is primarily structural because
downstream confirmation/runtime surfaces are deferred, and negative vectors are generated rather
than stored as a separately versioned corpus.

## Out of Scope

- Persistent profile/binding/recipe registry lifecycle, activation, supersession, revocation, compare-and-swap, and trust anchors.
- Arbitrary or mutating recipes, transitive skill closure, compatibility/latest resolution, and schema migration.
- Candidate-to-`DispatchSpec` projection, capability resolution, human confirmation, runtime commands/events, scheduling, providers, execution, recovery, and replay.
- Existing non-protocol ACI runtime test obligations; this file covers only T-ACI-PC1 through T-ACI-PC12.

## Connections

| Document | Type | Description |
|---|---|---|
| [Feature-wide TEST-SPEC](../TEST-SPEC.md) | `elaborates` | Owns the feature-level matrix and already indexes T-ACI-PC1 through T-ACI-PC12; this aspect file adds fixture-readiness and no-artifact detail without claiming a second test namespace. |
| [SPEC.md](SPEC.md) | `tests` | Supplies the bounded implementation authorization and authority boundary. |
| [protocol-compilation.md](protocol-compilation.md) | `tests` | Owns the closed schemas, calculation, mapping, failures, fixture admission, persistence seam, and T-ACI-PC1 through T-ACI-PC12 obligations. |
| [Protocol compilation fixture v1](fixtures/protocol-compilation-v1/manifest.json) | `uses-fixture` | Supplies the compiled and required-unsupported production-admitted cases; negative and canonicalization-edge variants remain absent. |

## Change History

| Version | Date | Change |
|---|---|---|
| 0.2.0 | 2026-08-03 | Aligns tests with the two-case production admission gate, digest-only compiler identity, schema-first validation precedence, literal fixture hashes, non-recursive scalar substitution, and qualified ArtifactStore receipt behavior. |
| 0.1.0 | 2026-08-03 | Creates the bounded protocol-compilation test contract, separates pure compilation from optional idempotent artifact persistence, and records missing/inconsistent fixture evidence without claiming execution. |
