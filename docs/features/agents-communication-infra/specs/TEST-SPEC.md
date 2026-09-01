---
tags: [agents-communication-infra, spec, test, protocol-compilation, execution-policy]
node_type: spec
is_session: false
layer: application
nature: [procedural, technical]
status: draft
version: 0.5.0
last_updated: 2026-09-01
---

# Test Spec: ACI Bounded Contract Slices

This aspect-level test specification defines executable obligations for separately gated, bounded
contract slices. T-ACI-PC1 through T-ACI-PC12 elaborate the protocol-compilation index in the
[feature-wide TEST-SPEC](../TEST-SPEC.md). T-ACI-POL0-1 through T-ACI-POL0-8 freeze only the pure
POLICY-000 execution-policy contract oracle; they authorize no persistence, runtime authority or
external effect. T-ACI-POL1-1 through T-ACI-POL1-8 specify only the isolated test-only synthetic
lineage seam; they authorize no production surface or runtime authority. T-ACI-POL2-1 through
T-ACI-POL2-8 specify only a durable fake-denial probe over that exact lineage; they authorize no
process, provider, workload filesystem, network, credential, production fence or L3 enforcement.

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

## POLICY-000 L0 Test Matrix

| ID | Test | Required assertion | Validates |
|---|---|---|---|
| [T-ACI-POL0-1](#t-aci-pol0-1--recursive-closed-schema-rejection) | Recursive closed-schema rejection | Every required field missing, every extra/duplicate/misspelled field and every wrong primitive rejects in `VersionedReference`, budget-policy target, `ResourceBudget`, sandbox-enforcement target, `SandboxPolicy`, production fence, harness fence and `ExecutionPolicyOracleFixture`, including all five fields of the combined envelope and every nested structure. | [VersionedReference](domain.md#versionedreference), [ResourceBudget](domain.md#resourcebudget), [SandboxPolicy](domain.md#sandboxpolicy), [fences](domain.md#executionauthorityfence), [ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture) |
| [T-ACI-POL0-2](#t-aci-pol0-2--strict-integers-and-explicit-zero) | Exact int64 bounds with no defaults or coercion | Boolean, numeric string, float, negative, null, non-finite and overflow/wraparound representations reject for every integer. Each `ResourceBudget` ceiling and `max_child_processes` accepts exactly `0..9223372036854775807`; `cutover_epoch` accepts exactly `1..9223372036854775807` in production and harness fences. Omission always rejects. | [ResourceBudget](domain.md#resourcebudget), [SandboxPolicy](domain.md#sandboxpolicy), [ExecutionAuthorityFence](domain.md#executionauthorityfence), [ExecutionAuthorityFenceHarness](domain.md#executionauthorityfenceharness) |
| [T-ACI-POL0-3](#t-aci-pol0-3--canonical-bytes-and-golden-digests) | Exact `aci-cjson-1` bytes and digest goldens | Every reviewed fixture and reference target reproduces its literal bytes and qualified lowercase SHA-256 digest; a one-byte drift changes the digest and cannot reuse lineage. | [ResourceBudget](domain.md#resourcebudget), [SandboxPolicy](domain.md#sandboxpolicy), [ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture), [TECH-POLICY-D0 goldens](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md#fake-deny-all-lane) |
| [T-ACI-POL0-4](#t-aci-pol0-4--versioned-reference-resolution) | Every reference is bound to exact caller-supplied target bytes | A missing map entry or digest mismatch rejects before acceptance. Budget-policy and sandbox-enforcement targets additionally reject the wrong closed schema; credential targets are digest-verified under the reference owner's contract without inventing a universal credential-target schema. The parser performs no I/O. | [VersionedReference](domain.md#versionedreference), [ResourceBudget](domain.md#resourcebudget), [SandboxPolicy](domain.md#sandboxpolicy) |
| [T-ACI-POL0-5](#t-aci-pol0-5--sandbox-grammar-and-grant-rejection) | Default-deny nested grammar and lexical roots are exact | Allow-by-default, `link_policy` other than `deny`, empty path components, `.`, `..`, drives, UNC, wildcards, duplicate credential refs, embedded secret bytes and endpoint/executable entries without closed definitions reject. Physical symlink, junction/reparse-point and resolved-containment checks are deferred to POLICY-003/L3. | [SandboxPolicy](domain.md#sandboxpolicy) |
| [T-ACI-POL0-6](#t-aci-pol0-6--attempt-budget-separation) | Attempt and dispatch budgets cannot be inferred from one another | `tool.none` with nonzero `max_tool_calls` rejects; parsing never divides/copies dispatch ceilings, resets the Run deadline, converts unknown usage to zero or synthesizes an Attempt budget. | [ResourceBudget](domain.md#resourcebudget) |
| [T-ACI-POL0-7](#t-aci-pol0-7--fence-digest-domain-separation) | Production and harness fences have disjoint schemas and preimages | Fence/preimage digest-domain substitution rejects; the harness parses only under its harness parser and the production parser rejects the harness schema before evidence resolution. | [ExecutionAuthorityFence](domain.md#executionauthorityfence), [ExecutionAuthorityFenceHarness](domain.md#executionauthorityfenceharness) |
| [T-ACI-POL0-8](#t-aci-pol0-8--oracle-authority-firewall-and-zero-effects) | Pure oracle cannot become executable authority | The combined oracle is valid only for its test parser and rejects structurally at a pure production policy-document parser; fail-on-call spies prove zero DB, artifact, journal, audit, clock, environment, filesystem, network, credential, process, provider and tool effects. | [ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture), [SPEC POLICY-000 amendment](SPEC.md#bounded-spec-amendment-policy-000-execution-policy-contracts) |

### T-ACI-POL0-1 — Recursive closed-schema rejection

Generate a single-fault matrix for every field at every nesting depth, including the five exact
`ExecutionPolicyOracleFixture` envelope fields and both nested policy documents, and feed
duplicate-key cases to the raw JSON decoder before ordinary object construction. A parser must
return a typed rejection, never drop an unknown field or fill a missing one.

### T-ACI-POL0-2 — Strict integers and explicit zero

Apply every invalid representation to each integer leaf, including `cutover_epoch` and
`max_child_processes`. For every `ResourceBudget` ceiling and `max_child_processes`, prove that `0`
and `9223372036854775807` accept while `-1` and `9223372036854775808` reject without wraparound. For
`cutover_epoch`, prove that `1` and `9223372036854775807` accept while `0` and
`9223372036854775808` reject under both the production and harness fence parsers. A present zero
budget ceiling is explicit denial; omission is never equivalent to zero.

### T-ACI-POL0-3 — Canonical bytes and golden digests

Compare byte-for-byte with the seven reviewed literals below; do not derive the expected value only
from mutable fixture input.

| Golden | Expected digest |
|---|---|
| fake budget-policy target | `sha256:08f3494d9e869053ee097e854840ade80afcda65cce75ef774038be5c6c242d2` |
| fake sandbox-enforcement target | `sha256:88f400d1661b69ac6536b548216bb7f5a370042050df2ea7bae49e03952725ea` |
| all-zero ResourceBudget | `sha256:e6e3a27b6fecf0ca8667ca722bb1e74a39e4d1f685da172f75a8077a67ba3836` |
| deny-all SandboxPolicy | `sha256:d865e9f97c6b73afc4748e5bd6d58095e471450d72cd45c3fb4a55a8185e3b1a` |
| combined execution-policy oracle | `sha256:9abfb7e61f995a90e8a08a72dfa96dda2df956f63e4e4360e78eca22493641f6` |
| harness-fence preimage | `sha256:124d06fa0b4c2e55eef48bc5b0c33ce19880d15ce82e0d3af9518a80536de70f` |
| complete harness-fence document | `sha256:4672e47ccc7fb906a14c0cd57de0bbd74271cfb7697d3a539dc97251bb864ba4` |

### T-ACI-POL0-4 — Versioned reference resolution

Supply the pure parser an exact target-byte map keyed to every `VersionedReference`, including every
non-empty `credential_refs` entry. Exercise a missing entry, a one-byte digest mismatch and, for the
budget-policy and sandbox-enforcement references only, a wrong closed schema. Every case rejects
before the enclosing value is accepted. Credential target bytes are verified under the reference
owner's contract; this suite does not impose a universal credential-target schema. Fail-on-call
spies prove that reference validation performs no filesystem, network, credential-store or other
I/O.

### T-ACI-POL0-5 — Sandbox grammar and grant rejection

Mutate each nested scope independently. Empty grant lists are valid explicit deny-all values;
non-empty endpoint/executable lists remain invalid in L0 because no closed entry grammar is
ratified. Exercise non-empty, duplicate-free `credential_refs` with an exact caller-supplied
target-byte map; credential values remain opaque `VersionedReference` objects, never secret
material. Root validation is lexical only: canonical relative `/` paths accept, while empty
components, `.`, `..`, drives, UNC paths and wildcards reject, and `link_policy` must equal `deny`.
Do not inspect the host filesystem in L0. Physical symlink, junction/reparse-point and
resolved-path containment tests belong exclusively to POLICY-003/L3.

### T-ACI-POL0-6 — Attempt budget separation

The pure parser may compare `max_tool_calls` with an explicitly supplied confirmed tool-profile
literal. It receives no scheduler or usage service and exposes no calculation that derives one
budget level from the other.

### T-ACI-POL0-7 — Fence digest-domain separation

Independently mutate schema literals, preimage fields and embedded `fence_digest`. Complete-document
content-digest drift remains a T-ACI-POL0-3 byte oracle, not a second fence-preimage domain. A
harness-schema failure at the production parser must occur before its evidence resolver is called.

### T-ACI-POL0-8 — Oracle authority firewall and zero effects

Exercise valid goldens and representative failures through pure document parsers with fail-on-call
spies. This L0 test performs no confirmation, plan/request or effect-boundary integration; those
operational rejections remain allocated to later layers. No test may fabricate cutover evidence,
verified opening or runtime identity to make the oracle executable.

## POLICY-001 L1 Test Matrix

| ID | Test | Required assertion | Validates |
|---|---|---|---|
| [T-ACI-POL1-1](#t-aci-pol1-1--exact-seven-member-lineage-unit) | Exact seven-member lineage unit and closed receipt | Only the reviewed members accept at ordinals `0..6` with exact names, artifact identities and content digests; receipt schema/authority/member fields and canonical `unit_digest` are exact. Addition, omission, rename, reorder, artifact substitution, reference-target drift, swapped target, member-body drift, combined-oracle drift or harness digest-domain substitution rejects or conflicts. | [ExecutionPolicySyntheticLineageReceipt](domain.md#executionpolicysyntheticlineagereceipt), [lineage invariants](capabilities/execution-policy-authority.md#policy-001l1-lineage-invariants) |
| [T-ACI-POL1-2](#t-aci-pol1-2--transaction-failpoints-are-all-or-none) | One shared transaction survives every failpoint as all-or-none | Failure after begin, after each of seven artifact finalizations, after the receipt, after each of seven bindings and before commit reopens to the complete unit or no POLICY-001 rows. | [Lineage invariants](capabilities/execution-policy-authority.md#policy-001l1-lineage-invariants), [persistence inventory](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md#transaction-and-reopen-pattern) |
| [T-ACI-POL1-3](#t-aci-pol1-3--synthetic-key-replay-and-conflict) | Synthetic-key replay converges and drift conflicts | Same `synthetic_key` plus the same `unit_digest` returns the byte-identical first receipt; the same key plus a changed digest is a permanent conflict with no second unit. | [Receipt identity](domain.md#executionpolicysyntheticlineagereceipt) |
| [T-ACI-POL1-4](#t-aci-pol1-4--lineage-identity-replay-and-conflict) | Lineage-identity replay converges and drift conflicts | Same `lineage_identity` plus the same `unit_digest` returns the byte-identical first receipt even through a different transport key; the same identity plus a changed digest is a permanent conflict with no second unit. | [Receipt identity](domain.md#executionpolicysyntheticlineagereceipt) |
| [T-ACI-POL1-5](#t-aci-pol1-5--lost-response-converges-on-first-receipt) | Post-commit lost response is idempotent | A failpoint after transaction commit but before returning the response, followed by identical retry, returns the first receipt and creates no duplicate artifact, receipt or binding row. | [Lineage path](capabilities/execution-policy-authority.md#lineage-path) |
| [T-ACI-POL1-6](#t-aci-pol1-6--file-backed-reopen-reproduces-exact-lineage) | File-backed reopen reproduces exact bytes and receipt | Closing and reopening the same temporary database reproduces every member body/digest, ordinal/name binding, canonical `unit_digest` and receipt field exactly. | [ExecutionPolicySyntheticLineageHarness](capabilities/execution-policy-authority.md#executionpolicysyntheticlineageharness-test-only) |
| [T-ACI-POL1-7](#t-aci-pol1-7--production-parser-rejection-survives-persistence) | Persistence cannot promote oracle or harness bytes | Before persistence and after reopen, production policy-document parsers reject the combined oracle structurally, and `parseExecutionAuthorityFence` rejects the harness schema before evidence resolution. | [ExecutionPolicyContractParser](interfaces.md#internal-executionpolicycontractparser), [ExecutionPolicyOracleFixture](domain.md#executionpolicyoraclefixture), [ExecutionAuthorityFenceHarness](domain.md#executionauthorityfenceharness) |
| [T-ACI-POL1-8](#t-aci-pol1-8--zero-authority-rows-and-zero-l2-effects) | Exact zero-row/effect firewall holds after success and every failure | Only finalized artifact metadata and the two test-only lineage tables may contain POLICY-001 rows; every named production authority, plan/request/attempt, event/effect, publication and message table remains empty, and fail-on-call spies observe no audit, provider, launcher, tool or other external effect. | [Capability exclusions](capabilities/execution-policy-authority.md#exclusions), [persistence inventory](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md#mandatory-zero-row-inventory) |

### T-ACI-POL1-1 — Exact seven-member lineage unit

Load the exact POLICY-000 vector corpus and independently revalidate all seven source bytes/digests
before persistence. The admitted ordered names are `budget_policy`, `sandbox_enforcement_policy`,
`resource_budget`, `sandbox_policy`, `combined_oracle`, `harness_fence_preimage` and
`harness_fence_document` at ordinals `0..6`. Assert the closed receipt literal
`aci.execution-policy-synthetic-lineage-receipt@1`, authority
`test-only-non-executable`, exact key/identity/member fields and
`unit_digest=sha256(aci-cjson-1(lineage_unit_preimage))`.

Independently mutate reference-target bytes/digests, swap the two targets, drift resource or sandbox
bytes against the combined oracle's member digests, omit/add/rename/reorder any of the seven lineage
members, substitute an artifact identity, and cross the harness preimage/fence/full-document digest
domains. Missing source artifact bytes reject before commit; missing persisted artifact bytes after
reopen fail closed without returning a receipt. Semantically equivalent `combined_oracle` bytes with
non-canonical key order reject before commit independently from its content-digest drift. Every
other case rejects before commit or permanently conflicts with an already persisted unit.

### T-ACI-POL1-2 — Transaction failpoints are all-or-none

Prepare all artifacts before entering the transaction. Inject a failure immediately after begin,
after each of the seven `ArtifactStore.finalize(conn, ...)` calls, after the receipt insert, after
each of seven ordered-member inserts and immediately before commit. Close and reopen after every
failure and assert either all seven finalized artifacts plus one receipt and seven bindings exist,
or none of those POLICY-001 rows exists. A test must fail if the seam calls per-artifact
`ArtifactStore.commit()`.

### T-ACI-POL1-3 — Synthetic-key replay and conflict

Persist once, then retry with the same `synthetic_key` and identical unit. Assert canonical receipt
bytes and persisted identity equal the first result and table cardinalities do not change. Mutate
one member while retaining the key and require a permanent conflict with no write.

### T-ACI-POL1-4 — Lineage-identity replay and conflict

Repeat the replay matrix for `lineage_identity`, including a different unused transport key with
the same unit. Equal identity/digest converges on the first receipt; one-member drift under the same
identity conflicts with zero mutation.

### T-ACI-POL1-5 — Lost response converges on first receipt

Fire `after_commit` only after the shared transaction exits, then simulate response loss. Retry the
identical command through a fresh harness instance and assert it returns the original receipt with
one receipt row, seven bindings and seven content-addressed artifact identities.

### T-ACI-POL1-6 — File-backed reopen reproduces exact lineage

Close every database/artifact handle, construct a fresh runtime database and artifact store over the
same temporary path, and reload through the artifact boundary. Compare every body byte, qualified
digest, ordered binding and receipt field, including `unit_digest`, against the first accepted
values. In-memory SQLite is not an acceptable fixture for this obligation.

### T-ACI-POL1-7 — Production-parser rejection survives persistence

Call the production policy-document parsers with the combined-oracle bytes and require structural
rejection. Separately call `parseExecutionAuthorityFence` with only the raw harness-fence bytes while
a fail-on-call evidence-resolver spy remains outside the parser dependency graph and uninvoked;
require schema rejection before any evidence resolution could occur. Repeat both assertions on
bytes loaded after reopen so persistence cannot change their authority domain.

### T-ACI-POL1-8 — Zero authority rows and zero L2 effects

Use a fresh temporary file-backed database for each scenario. After the happy path and every
failure/replay/conflict case, assert POLICY-001 rows occur only in
`artifacts` and the two test-only receipt/member tables. The following production tables remain
empty: `confirmed_dispatches`, `runs`, `confirmed_turn_graphs`, `agent_invocation_plans`,
`agent_execution_requests`, `agent_attempts`, `command_receipts`, `events`, `aggregate_heads`,
`effect_intents`, `sandbox_launch_effects`, `publication_candidates`, `publication_receipts` and
`messages`. Fail-on-call spies around the runtime service, journal, audit appender, confirmation,
provider, launcher, policy resolver, credential resolver, filesystem/network/process/tool boundary
and any effect worker must remain at zero. Artifact persistence itself is the admitted L1 mutation;
no denial receipt or attempted external action from POLICY-002/L2 belongs in this suite.

## POLICY-002 L2 Test Matrix

| ID | Test | Required assertion | Validates |
|---|---|---|---|
| [T-ACI-POL2-1](#t-aci-pol2-1--exact-fake-denial-receipt) | Exact closed denial receipt and digest domains | Reopening the reviewed POLICY-001 lineage produces the exact closed `aci.execution-policy-fake-denial-receipt@1` bytes, exact two reason codes, exact denial preimage digest and exact receipt content digest. | [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt), [TECH-POLICY-D0 L2](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md#implementation-layering) |
| [T-ACI-POL2-2](#t-aci-pol2-2--lineage-must-reopen-and-revalidate-before-denial) | Missing, partial or drifted lineage denies the probe itself before persistence | Missing receipt/member/artifact bytes, wrong member order, changed unit digest, non-canonical member bytes, any budget ceiling changed from zero, any non-empty sandbox grant or production-parser-domain substitution produces a typed rejection and zero POLICY-002 rows. | [ExecutionPolicySyntheticLineageReceipt](domain.md#executionpolicysyntheticlineagereceipt), [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-3](#t-aci-pol2-3--decision-reasons-and-attempt-labels-are-closed) | The only admitted outcome is exact denial for every closed action-attempt label | Each of the twelve non-executable labels below yields only `decision=denied` with ordered reasons `resource.max_wall_time_ms.zero` and `sandbox.process.no-executable-grant`; unknown labels and any decision/reason drift reject. Labels never enter the receipt or authority. | [ResourceBudget](domain.md#resourcebudget), [SandboxPolicy](domain.md#sandboxpolicy), [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-4](#t-aci-pol2-4--denial-persistence-is-atomic) | One denial row commits or none does | Failure after begin, after receipt insert or before commit reopens with zero POLICY-002 rows; `after_commit` models only a lost response and leaves exactly one durable receipt. | [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-5](#t-aci-pol2-5--dual-replay-and-conflict) | Denial-key and lineage-identity replay converge; drift conflicts | Either uniqueness axis plus the same denial digest returns the first byte-identical receipt; either axis plus changed evidence conflicts permanently with no second row. | [ExecutionPolicyFakeDenialReceipt identity](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-6](#t-aci-pol2-6--file-backed-reopen-reproduces-denial) | Reopen reproduces exact durable denial evidence | Fresh database and harness handles reproduce the first canonical receipt bytes, denial digest, receipt digest and exact source-lineage binding. | [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-7](#t-aci-pol2-7--every-attempt-label-denies-with-zero-external-action) | Every enumerated action attempt is denied without performing it | Route each of the twelve labels independently through the fake boundary; every call returns the same durable denial receipt while fail-on-call spies prove zero process/subprocess, provider, tool, network, credential, audit, journal, runtime service, clock, environment or workload-filesystem calls. Only the supplied temporary SQLite test path is touched. | [TECH-POLICY-D0 L2 vectors](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md#l2--policy-002--fake-deny-all-behavior), [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt) |
| [T-ACI-POL2-8](#t-aci-pol2-8--production-and-l3-firewall) | Durable denial cannot become an effect or host-enforcement claim | POLICY-001 artifact/receipt/member cardinalities remain unchanged; POLICY-002 adds only its one test table and one row; all production authority/runtime/effect tables stay empty; production confirmation/plan/request/effect boundaries reject oracle/harness inputs before mutation; no `AgentExecutionRequest`, `EffectIntent`, production fence, host path resolution or L3 evidence is created. | [ExecutionPolicyFakeDenialReceipt](domain.md#executionpolicyfakedenialreceipt), [ExecutionAuthorityFence](domain.md#executionauthorityfence), [EffectIntent](domain.md#effectintent) |

### T-ACI-POL2-1 — Exact fake-denial receipt

First persist and reopen the exact POLICY-001 fixture. Independently reproduce the literal denial
preimage, `denial_digest=sha256:bc8655ac88276258d8e320b8a9757a8b625c9e9249dc7255a5578d2eb7e65399`,
complete canonical receipt bytes and receipt content digest
`sha256:5ffde80fbfb897ceb4b90cb85bcdb019538777c91ae3525ac0f7e0ebc43a9b11`.
The expected fixture must carry these literals rather than deriving its expected value only from
the harness under test.

### T-ACI-POL2-2 — Lineage must reopen and revalidate before denial

Exercise a missing lineage, missing or reordered member, missing artifact bytes, corrupted receipt,
changed `unit_digest`, non-canonical member bytes and a harness/production digest-domain
substitution. Independently change each of the six ResourceBudget ceilings from `0` to `1`, add one
filesystem read grant, filesystem write grant, network endpoint, process executable or credential
reference, and change `max_child_processes` from `0` to `1`. Every case falls outside the exact
fake-deny-all lineage, rejects before the denial transaction begins and leaves the POLICY-002 table
empty. The harness may consume only the exact first POLICY-001 receipt and reopened members;
caller-supplied policy dictionaries or an oracle aggregate alone are insufficient.

### T-ACI-POL2-3 — Decision, reasons and attempt labels are closed

Parse the reopened all-zero ResourceBudget and deny-all SandboxPolicy through the reviewed pure
parsers. Require `max_wall_time_ms=0`, `process_scope.default=deny` and an empty
`allowed_executables`. The returned reason list is the exact ordered two-element list frozen by the
domain receipt. The fake port accepts exactly this closed, non-executable action-attempt label
corpus:

```text
filesystem.read
filesystem.write
network.connect
process.child.start
credential.resolve
tool.call
resource.wall_time.consume_positive
resource.input_tokens.consume_positive
resource.output_tokens.consume_positive
resource.tool_calls.consume_positive
resource.payload_bytes.consume_positive
resource.artifact_bytes.consume_positive
```

Every label is a test selector only. It is excluded from the denial preimage, receipt bytes,
identity, replay digest and every authority contract; it never denotes an `EffectIntent` or grants
permission to attempt the named external action. Unknown, missing or duplicate labels reject.
Mutation of the decision, reason spelling, count or order rejects instead of being normalized.

### T-ACI-POL2-4 — Denial persistence is atomic

Use one test-only receipt table in the same temporary file-backed database as POLICY-001. Inject
failures after transaction begin, after the denial receipt insert and before commit; close/reopen
must show zero POLICY-002 rows. Fire `policy_denial.after_commit` only after transaction exit; a
lost response then leaves exactly one durable row and an identical retry returns it.

### T-ACI-POL2-5 — Dual replay and conflict

Resolve both `denial_key` and `lineage_identity` under the same writer transaction. Same key or
identity plus the same `denial_digest` returns the first canonical receipt. A different unused key
may converge through the same lineage identity. Drift in the lineage unit, policy digests,
decision or reason list under either identity is a permanent no-write conflict.

### T-ACI-POL2-6 — File-backed reopen reproduces denial

Close every handle, reopen the same temporary SQLite file through fresh POLICY-001 and POLICY-002
harnesses, and compare the receipt bytes, its content digest, denial preimage digest, source
lineage identity/unit digest and both policy digests with the first result. In-memory SQLite does
not satisfy this durability obligation.

### T-ACI-POL2-7 — Every attempt label denies with zero external action

For each closed action-attempt label, invoke the test-only denial port independently with the exact
persisted lineage, identities and temporary database path. Require the same byte-identical durable
denial receipt for all twelve labels. The port accepts no process/provider/tool/network/credential
callable and no sealed request. Fail-on-call spies cover process creation, subprocess helpers,
sockets, HTTP/provider calls, credential resolution, tools, audit appender, runtime
service/journal, clock, environment and workload-path inspection; every spy count remains zero in
every subcase. Temporary SQLite reads/writes are the only filesystem activity admitted by this
test. The label proves routing coverage only and is not persisted.

### T-ACI-POL2-8 — Production and L3 firewall

Before and after every success, failure, replay, conflict and reopen, assert the seven POLICY-001
artifacts, one lineage receipt and seven member bindings are unchanged. POLICY-002 may add only its
single test-only table and first denial row. Keep `confirmed_dispatches`, `runs`,
`confirmed_turn_graphs`, `agent_invocation_plans`, `agent_execution_requests`, `agent_attempts`,
`command_receipts`, `events`, `aggregate_heads`, `effect_intents`, `sandbox_launch_effects`,
`publication_candidates`, `publication_receipts` and `messages` empty. Submit the combined oracle
and harness fence to the production confirmation, plan/request acceptance and effect-boundary
admission seams available to the test and require rejection before mutation. No production
migration, fence evidence, host path resolution, physical link check or launcher/provider
observation exists.

## Fixture Corpus and Readiness

| Corpus item | Present state | What it can prove | What it cannot prove |
|---|---|---|---|
| POLICY-000 reviewed local oracle | Exact bytes and seven independently reproduced digests are documented in the [design review](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/TECH-D0-REVIEW.md); the parser, reviewed local fixture and tests are frozen by the [implementation review](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md) (`sha256:76ed9cd9efd6794e7b1d4c40421635db16edc8a580e789f837b415d892b13c8c`) at exact output digests and PASS/KEEP | Bounded executable conformance for T-ACI-POL0-1 through T-ACI-POL0-8; focused suite `37 passed` and full runtime regression `237 passed` | POLICY-001 persistence, L2 denial effects, product-selected values, runtime authority or host enforcement |
| POLICY-001 persistence pattern inventory | Digest-pinned architecture evidence defines the temporary file-backed database, one-transaction artifact/receipt/member unit and exact zero-row inventory; no lineage implementation or test result is claimed here | Normative harness and mutation targets for T-ACI-POL1-1 through T-ACI-POL1-8 | Executable persistence/reopen conformance, L2 denial effects, external action or production authority |
| POLICY-002 fake-denial design | TECH-POLICY-D0 fixes the test-only fake deny-all lane and L2 zero-action outcome; the DomainSpec receipt now freezes one exact denial preimage and receipt | Normative harness, durability, replay/conflict and firewall targets for T-ACI-POL2-1 through T-ACI-POL2-8 | Executable conformance, product-selected policy, a production fence, host enforcement or provider admission |
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

### G4 - POLICY-000 evidence stops at pure L0

The digest-pinned [POLICY-000 implementation review](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md)
records PASS/KEEP for the exact parser, seven-vector fixture and 37-test focused suite, with the
237-test runtime regression passing. This closes the bounded executable L0 oracle only. It proves
no POLICY-001/L1 synthetic persistence or reopen, POLICY-002/L2 fake-denial behavior,
POLICY-003/L3 target-host enforcement, product-selected values or runtime authority.

### G5 - POLICY-001 executable lineage evidence is a separate prerequisite

This amendment does not create or review POLICY-001 executable evidence. POLICY-002 code entry
requires the POLICY-001 harness, persistence and file-backed reopen evidence to be separately
reviewed and digest-pinned. POLICY-002/L2 implementation and POLICY-003/L3 target-host enforcement
remain separate work.

## Out of Scope

- Persistent profile/binding/recipe registry lifecycle, activation, supersession, revocation, compare-and-swap, and trust anchors.
- Arbitrary or mutating recipes, transitive skill closure, compatibility/latest resolution, and schema migration.
- Candidate-to-`DispatchSpec` projection, capability resolution, human confirmation, runtime commands/events, scheduling, providers, execution, recovery, and replay.
- Existing non-protocol ACI runtime test obligations except the POLICY-000 L0 oracle, POLICY-001
  L1 synthetic-lineage seam and POLICY-002 L2 fake-denial seam.
- POLICY-003/L3 target-host enforcement, product-selected policy and every real provider action.

## Connections

| Document | Type | Description |
|---|---|---|
| [Feature-wide TEST-SPEC](../TEST-SPEC.md) | `elaborates` | Owns the feature-level matrix and already indexes T-ACI-PC1 through T-ACI-PC12; this aspect file adds fixture-readiness and no-artifact detail without claiming a second test namespace. |
| [SPEC.md](SPEC.md) | `tests` | Supplies the bounded implementation authorization and authority boundary. |
| [protocol-compilation.md](protocol-compilation.md) | `tests` | Owns the closed schemas, calculation, mapping, failures, fixture admission, persistence seam, and T-ACI-PC1 through T-ACI-PC12 obligations. |
| [Domain model](domain.md#resourcebudget) | `tests` | Owns the closed execution-policy value shapes checked by T-ACI-POL0-1 through T-ACI-POL0-8. |
| [TECH-POLICY-D0](../development/invoke-runs/20260831-resumable-feedback/plan/TECH-POLICY-D0.md) | `derives-from` | Reviewed golden bytes, digests, negative-vector allocation and L0-L3 layering boundary. |
| [TECH-D0 review evidence](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/TECH-D0-REVIEW.md) | `validated-by` | Independent second-pass reproduction of every POLICY-000 reference, policy and harness digest. |
| [POLICY-000 implementation review](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md) | `validated-by` | PASS/KEEP receipt for the exact pure L0 parser, seven-vector fixture and focused/full regression evidence; it promotes no L1-L3 claim. |
| [Execution-policy capability](capabilities/execution-policy-authority.md) | `tests` | Owns the bounded L0-L2 capability, parser, lineage-harness and fake-denial-harness boundaries, invariants and authority firewall checked by T-ACI-POL0-1 through T-ACI-POL2-8. |
| [POLICY-001 persistence pattern inventory](../development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-PERSISTENCE-PATTERN-INVENTORY.md) | `derives-from` | Digest-pinned temporary file-backed persistence, replay/conflict/failpoint/reopen and zero-row pattern. |
| [Protocol compilation fixture v1](fixtures/protocol-compilation-v1/manifest.json) | `uses-fixture` | Supplies the compiled and required-unsupported production-admitted cases; negative and canonicalization-edge variants remain absent. |

## Change History

| Version | Date | Change |
|---|---|---|
| 0.5.0 | 2026-09-01 | Adds POLICY-002/L2 exact fake-denial receipt, source-lineage revalidation, durable one-row replay/reopen and zero-external-action/production/L3 firewall obligations. |
| 0.4.0 | 2026-09-01 | Adds POLICY-001/L1 exact seven-member lineage, atomic persistence, replay/conflict, failpoint/reopen, production-parser and zero-authority/effect test obligations; L2-L3 remain excluded. |
| 0.3.1 | 2026-09-01 | Fixes POLICY-000 integer bounds, caller-supplied credential-reference bytes and the lexical-L0 versus physical-L3 link boundary without changing the seven reviewed goldens. |
| 0.3.0 | 2026-09-01 | Adds POLICY-000 L0 strict parsing, canonicalization, digest-domain and non-authority obligations while explicitly deferring L1-L3 operational vectors. |
| 0.2.0 | 2026-08-03 | Aligns tests with the two-case production admission gate, digest-only compiler identity, schema-first validation precedence, literal fixture hashes, non-recursive scalar substitution, and qualified ArtifactStore receipt behavior. |
| 0.1.0 | 2026-08-03 | Creates the bounded protocol-compilation test contract, separates pure compilation from optional idempotent artifact persistence, and records missing/inconsistent fixture evidence without claiming execution. |
