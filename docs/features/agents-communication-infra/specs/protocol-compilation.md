---
tags: [agents-communication-infra, spec, protocol-compilation]
node_type: spec
is_session: false
layer: [domain, application]
nature: [technical, reference]
status: specified-bounded-slice
version: 1.0.0
last_updated: 2026-08-03
---

# Protocol Compilation Candidate v1

## Contract status and objective

This capability specifies the first implementation slice owned by **ACI Protocol Governance**:
validate four exact immutable inputs and deterministically compile them into one canonical,
non-authoritative `DispatchCandidate`. The slice proves protocol fidelity and identity without
creating execution authority.

The source decision is [ACI-PG-001](../../../decisions/aci-protocol-governance-ownership.md). The
protocol and delegated-supervision discoveries provide the promoted rationale, not parallel
normative schemas: [Agents Communication Protocols](../discovery/agents-communication-protocols/README.md)
and [Agent Tools and Delegated Supervision](../discovery/agent-tools-and-delegated-supervision.md).

This contract is deliberately smaller than the complete lifecycle proposed by discovery. V1 has
one repository-built-in fixture package containing exactly two read-only cases: one compiled case
and one required-unsupported case. It does not implement a registry, activation,
supersession, revocation, compare-and-swap, arbitrary recipe admission, confirmation projection or
runtime execution.

## Ownership and authority boundary

| Concern | Owner | V1 boundary |
|---|---|---|
| Skill intent, obligations, outputs, sources and quality criteria | Skill author/domain owner | Supplied as an exact skill revision and represented by an exact profile; compilation cannot add or reinterpret them. |
| Profile, binding snapshot, recipe/DAG and deterministic candidate compilation | ACI Protocol Governance | Owned through the canonical `DispatchCandidate` bytes and digest only. |
| Effective capability resolution and final canonical `DispatchSpec` | Existing ACI confirmation owner | Not called, projected or simulated by this capability. |
| Human acceptance, `ConfirmedDispatch` and `Run` | Existing ACI confirmation/runtime contracts | No authority is created by a candidate or its artifact. |
| Scheduling, attempts, providers, tools, effects, recovery and replay | ACI runtime/kernel | Entirely outside this capability. |
| Candidate byte persistence | Existing [`Artifact`](domain.md#artifact) boundary | Optional idempotent storage of already compiled bytes; it creates no journal fact or command/publication/dispatch receipt. The ArtifactStore finalization receipt remains boundary-owned metadata. |

The authority chain remains:

```text
exact skill revision + profile + binding snapshot + recipe/DAG + invocation
  -> pure CompileDispatchCandidate
  -> non-authoritative DispatchCandidate
  -> [deferred confirmation projection and capability resolution]
  -> canonical DispatchSpec digest accepted by a human
  -> ConfirmedDispatch / Run
```

A `ProtocolRecipe` is reusable compilation input. It is not a second `DispatchSpec`, an executable
plan, a confirmation object or a runtime authority. A `DispatchCandidate` is proposal data. Its
digest MUST NOT be accepted where a `dispatch_spec_digest` is required.

## Concept registry

| Concept | ID | DomainSpec meta-type | V1 status |
|---|---|---|---|
| [SkillExecutionProfile](#skillexecutionprofile) | `agents-communication-infra.SkillExecutionProfile` | Value Object | Specified |
| [SkillProtocolBinding](#skillprotocolbinding) | `agents-communication-infra.SkillProtocolBinding` | Entity | Immutable entity snapshot specified; lifecycle operations deferred |
| [ProtocolRecipe](#protocolrecipe) | `agents-communication-infra.ProtocolRecipe` | Entity | One built-in immutable revision specified |
| [SkillProtocolInvocation](#skillprotocolinvocation) | `agents-communication-infra.SkillProtocolInvocation` | Value Object | Specified |
| [DispatchCandidate](#dispatchcandidate) | `agents-communication-infra.DispatchCandidate` | Value Object | Specified; non-authoritative |
| [CompiledDispatchCandidate](#compile-result) | `agents-communication-infra.CompiledDispatchCandidate` | Value Object | Specified tagged result |
| [ObligationDisposition](#obligationdisposition) | `agents-communication-infra.ObligationDisposition` | Enum / Type | Specified |
| [CompileDispatchCandidate](#compiledispatchcandidate) | `agents-communication-infra.CompileDispatchCandidate` | Calculation | Specified; pure |
| [ProtocolCompiler](#protocolcompiler) | `agents-communication-infra.ProtocolCompiler` | Interface | Specified; internal |
| [ProtocolInputsToDispatchCandidate](#protocolinputstodispatchcandidate) | `agents-communication-infra.ProtocolInputsToDispatchCandidate` | Mapping | Specified |

Binding entity identity is `(skill_id, skill_revision_digest, binding_revision)` and recipe entity
identity is `(recipe_id, recipe_revision)`. V1 consumes immutable snapshots of those entities and
defers their lifecycle operations and history persistence. All remaining structural concepts are
equal by canonical value; `Artifact` remains a separately owned existing entity.

## Canonical contract common to every schema

Every input and output schema in this document is closed. Every listed field is required unless
the table says otherwise. A decoder MUST reject unknown fields, duplicate object keys, missing
required fields, `null` except where explicitly admitted, and a value of the wrong primitive type.
Closed-schema validation MUST occur before digest acceptance or semantic compilation. The outer
request bytes must themselves equal their canonical projection; a whitespace, key-order, BOM or
trailing-newline variant is `invalid_request_schema`.

Canonical bytes use [`aci-cjson-1`](../adrs/ADR-001-persistence-replay-and-canonical-contracts.md#6-pydantic-and-canonical-acceptance-bytes):

- values are projected through the versioned closed schema;
- strings and object keys are Unicode NFC; a normalization collision is invalid;
- object keys are sorted by Unicode scalar value and arrays retain their contract order;
- bytes are compact UTF-8 JSON without BOM, insignificant whitespace or trailing newline;
- integers use shortest base-10 form; booleans are not integers;
- JSON floats, NaN, infinities and binary payloads are forbidden;
- omitted optional fields remain omitted and are not defaulted into accepted bytes; and
- `ContentDigest(bytes) = "sha256:" + lowercase_hex(SHA-256(bytes))`.

Every `*_digest` field in this document is an algorithm-qualified
[`ContentDigest`](domain.md#contentdigest). Raw 64-character hexadecimal strings are invalid.
Digest equality never substitutes for closed-schema validation.

All integer parameter values are signed 64-bit (`-9223372036854775808` through
`9223372036854775807`). Schema `min_length` and `max_length` are integers in `0..65536`.

Arrays called sorted below are semantic ordered sets. Callers MUST supply them in ascending order
by the named key with no duplicate key; the compiler rejects unsorted input instead of repairing
it. `target_refs` use ascending exact-string order. Object-valued invocation parameters retain the
canonical object-key order defined above; array-valued parameters retain user-significant order.

V1 safety bounds are normative: identifiers are 1–128 UTF-8 bytes; statements, requirements and
schema text are 1–8,192 UTF-8 bytes; prompt templates are 1–65,536 UTF-8 bytes; a profile has at
most 256 obligations, 128 parameters, 128 capability requirements and 128 outputs; a recipe has at
most 128 nodes, 512 edges and 256 obligation rules; an invocation has at most 128 values. Exceeding
a bound is `invalid_document_schema`, never truncation or implementation-defined behavior.

## Closed input schemas

### SkillExecutionProfile

Schema literal: `aci.skill-execution-profile@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `skill_id` | string | Non-empty stable logical identifier; NFC. |
| `skill_revision_digest` | `ContentDigest` | Exact admitted skill-revision bytes. V1 does not discover a transitive closure. |
| `profile_revision` | string | Non-empty immutable revision label. |
| `obligations` | object[] | Non-empty, sorted by `obligation_id`; each closed item is `{obligation_id, statement, required}` with unique non-empty ID/text and boolean `required`. |
| `parameters` | object[] | Sorted by `parameter_id`; each closed item is `{parameter_id, value_schema, required}` with unique ID, boolean `required`, and a closed schema from the v1 parameter subset below. |
| `capability_requirements` | object[] | Sorted by `capability_id`; each closed item is `{capability_id, requirement, required}` with unique non-empty ID/text and boolean `required`. These are logical needs only. |
| `outputs` | object[] | Non-empty, sorted by `output_id`; each closed item is `{output_id, content_schema, required}` with unique ID, boolean `required`, and a closed schema from the v1 parameter subset. |

The v1 `value_schema` and `content_schema` subset is itself closed:
`{type, enum_values?, min_length?, max_length?}`. `type` is exactly one of `string`, `integer`,
`boolean`. `enum_values` is optional, non-empty, unique, sorted and contains only values of `type`.
String enums sort by Unicode scalar-value sequence after NFC normalization; integer enums sort by
numeric value; boolean enums sort `false` before `true`.
`min_length` and `max_length` are optional non-negative integers admitted only for `string`, with
`min_length <= max_length`; they count Unicode scalar values after NFC normalization, not UTF-8
bytes or grapheme clusters. No default, coercion, pattern, object, array, float or implicit value
is available in v1.

### SkillProtocolBinding

Schema literal: `aci.skill-protocol-binding@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `status` | enum | One of `active`, `stale`, `superseded`, `revoked`; only `active` passes semantic compilation. |
| `skill_id` | string | Equals the profile `skill_id`. |
| `skill_revision_digest` | `ContentDigest` | Equals the profile `skill_revision_digest`. |
| `profile_digest` | `ContentDigest` | Equals the digest of the supplied canonical profile bytes. |
| `recipe_digest` | `ContentDigest` | Equals the digest of the supplied canonical recipe bytes. |
| `binding_revision` | string | Non-empty immutable revision label. |

`binding_digest` is the digest of the complete canonical binding bytes and is carried beside those
bytes in the compile request. The status records an exact caller-supplied snapshot; semantic
validation rejects every non-`active` value as `inactive_binding`. V1 does not query or mutate a
binding registry and therefore makes no claim that an accepted snapshot remains active after
compilation.

### ProtocolRecipe

Schema literal: `aci.protocol-recipe@1`.

The only admitted V1 recipe snapshots have `recipe_id="protocol_compilation_read_only"`. The
compiled case has `recipe_revision="v1"` and digest
`sha256:92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3`;
the required-unsupported case has `recipe_revision="v1-required-unsupported"` and digest
`sha256:16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1`.
The exact profile, binding, recipe and invocation digest tuple MUST equal one complete manifest
case. A different merely schema-valid tuple is `fixture_not_admitted`. Compiler identity is a
separate fixed check and is not part of case admission. Changing package bytes requires a new
normative fixture revision and contract promotion.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `recipe_id` | string | Non-empty immutable recipe identity. |
| `recipe_revision` | string | Non-empty immutable revision label. |
| `mode` | string | Exact literal `read_only`. |
| `profile_digest` | `ContentDigest` | Equals the supplied profile digest. |
| `nodes` | object[] | Non-empty, sorted by `node_id`; closed node schema below. |
| `edges` | object[] | Sorted by `(from_node_id, to_node_id, edge_id)`; closed edge schema below. |
| `terminal_node_ids` | string[] | Non-empty, unique and sorted; every ID resolves to a terminal node. |
| `obligation_rules` | object[] | Sorted by `obligation_id`; exactly one rule for every profile obligation and no other rule. |

A recipe node is exactly `{node_id, node_kind, prompt_template, parameter_ids, capability_ids,
output_ids}`. `node_kind` is one of `work`, `review`, `decision`, `integration`, `projection`,
`terminal`. Every ID is non-empty. Each nested ID array is unique and sorted and every referenced
parameter, capability and output resolves exactly once in the profile. `prompt_template` is a
non-empty string containing only literal text and explicit placeholders of the exact form
`{{parameter:<parameter_id>}}`; every placeholder resolves to a parameter declared by that node.
V1 substitution is UTF-8 text substitution of the canonical JSON scalar representation. It does
not evaluate code, expressions, includes, environment variables or templates recursively.

A recipe edge is exactly `{edge_id, from_node_id, to_node_id, edge_kind}`. IDs are non-empty and
unique. `edge_kind` is one of `depends_on`, `review_of`, `feeds`, `gates`.

An obligation rule is exactly `{obligation_id, disposition, target_refs, authority_ref?}`. Its
closed semantics are defined below. `target_refs` contain only `node:<node_id>` or
`output:<output_id>` references that resolve in this recipe/profile pair.

### SkillProtocolInvocation

Schema literal: `aci.skill-protocol-invocation@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `skill_id` | string | Equals the profile and binding `skill_id`. |
| `skill_revision_digest` | `ContentDigest` | Equals the profile and binding skill revision. |
| `profile_digest` | `ContentDigest` | Equals the supplied profile digest. |
| `binding_digest` | `ContentDigest` | Equals the supplied binding digest. |
| `recipe_digest` | `ContentDigest` | Equals the supplied recipe digest. |
| `values` | object[] | Sorted by `parameter_id`; each closed item is exactly `{parameter_id, value}`. |

Every required parameter occurs exactly once. An optional parameter occurs zero or one time. No
undeclared parameter is admitted. Each `value` is validated against the declared v1 schema with no
coercion: strings remain strings, integers exclude booleans, and booleans remain booleans. Missing
values are never inferred from skill text, profile prose, environment, prior runs or defaults.
For V1, a string invocation value containing either template delimiter `{{` or `}}` is
`invalid_parameter_value`; this makes recursive or second-pass template evaluation impossible.

`invocation_digest` is the digest of the complete canonical invocation bytes and is supplied beside
those bytes in the compile request.

## ObligationDisposition

The closed set is `preserved`, `compiled`, `superseded`, `unsupported`.

| Disposition | Meaning | Required shape |
|---|---|---|
| `preserved` | The obligation remains explicit in candidate structure or output. | `target_refs` is non-empty; `authority_ref` is absent. |
| `compiled` | The obligation is translated into concrete candidate structure or output. | `target_refs` is non-empty; `authority_ref` is absent. |
| `superseded` | A separately identified superior authority replaces the obligation. | `target_refs` is empty; `authority_ref` is required and exactly `{authority_kind, authority_digest}`. Both fields are non-empty and the digest is qualified. |
| `unsupported` | V1 cannot preserve or compile the obligation. | `target_refs` is empty; `authority_ref` is absent. |

Every profile obligation has exactly one disposition and every disposition identifies an existing
profile obligation. Any required obligation marked `unsupported` yields the closed blocked result;
it never yields a partial candidate. Neither admitted built-in case may use `superseded`.

## DAG validity

The embedded recipe graph is valid only when all of the following hold:

1. `nodes` and `edges` satisfy the normative V1 safety limits above.
2. Every edge endpoint resolves to exactly one node and no self-edge exists.
3. Node IDs and edge IDs are independently unique.
4. The directed graph is acyclic; a deterministic topological sort using ascending `node_id` as
   the tie-breaker must consume every node.
5. Every node with no incoming edge is a source. Every non-source has at least one incoming edge.
6. Every non-terminal node reaches at least one declared terminal node.
7. A declared terminal node has `node_kind=terminal` and has no outgoing edge.
8. Every node/edge, parameter, capability, output, obligation and target reference is closed over
   the supplied profile/recipe pair.
9. `node_kind=terminal` if and only if `node_id` is present in `terminal_node_ids`.

Compilation cannot add a missing node, edge, source, terminal, gate or reference to make an invalid
graph valid.

## Closed output schemas

### DispatchCandidate

Schema literal: `aci.dispatch-candidate@1`.

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact schema literal. |
| `source_binding` | object | Exactly `{skill_id, skill_revision_digest, profile_digest, binding_digest, recipe_digest, invocation_digest, compiler_contract_digest}`. |
| `invocation_values` | object[] | Exact ordered projection of invocation `values`. |
| `nodes` | object[] | Recipe nodes after explicit scalar substitution; no other transformation. |
| `edges` | object[] | Exact ordered recipe edge projection. |
| `terminal_node_ids` | string[] | Exact ordered recipe projection. |
| `obligation_dispositions` | object[] | Exact ordered total projection of recipe obligation rules. |
| `capability_requirements` | object[] | Exact logical profile requirements. No effective grant field exists. |
| `outputs` | object[] | Exact ordered profile output contracts. |

`compiler_contract_digest` identifies the canonical
[`compiler-contract.json`](fixtures/protocol-compilation-v1/compiler-contract.json) bytes. Its V1
value is `sha256:9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543`.
It identifies the accepted schema/canonicalization contract, not arbitrary implementation-file
closure or proof of code conformance.

Candidate bytes contain no timestamp, clock result, random value, generated dispatch/run/attempt/
command/event/receipt identity, user confirmation, provider or model selection, credential,
sandbox permission, resolved capability, effective grant, scheduling state, journal offset, audit
row or legacy-session identity.

The `candidate_digest` is the `ContentDigest` of the complete canonical candidate bytes. The
candidate binds every semantics-bearing input digest in `source_binding`; therefore changing any
profile, binding, recipe or invocation canonical byte invalidates the old
compile request and candidate lineage. V1 performs exact equality only: there is no compatibility,
migration or latest-version resolution.

### Compile result

`CompiledDispatchCandidate` is a closed tagged result with schema
`aci.compiled-dispatch-candidate-result@1`:

- compiled: exactly `{schema, outcome: "compiled", candidate_document, candidate_digest}`;
  `candidate_document` is the canonical JSON text whose UTF-8 bytes hash to `candidate_digest`;
- unsupported: exactly `{schema, outcome: "unsupported", unsupported_obligation_ids}` with a
  sorted, non-empty, unique array and no candidate field.

Only required obligations marked `unsupported` produce the `unsupported` result. All malformed,
stale, inconsistent or non-deterministically resolvable requests fail with a typed error and no
result object, candidate bytes or artifact descriptor.

## CompileDispatchCandidate

**Type:** Calculation (pure deterministic function)
**Actor:** Internal ACI Protocol Governance caller
**Interface:** [`ProtocolCompiler.compileCandidate`](#protocolcompiler)

The closed request schema is `aci.compile-dispatch-candidate-request@1` with exactly:

| Field | Type | Constraint |
|---|---|---|
| `schema` | string | Exact request schema literal. |
| `profile_document`, `profile_digest` | string, `ContentDigest` | Document string re-encoded as UTF-8 must already equal canonical profile bytes and verify the digest. |
| `binding_document`, `binding_digest` | string, `ContentDigest` | Document string re-encoded as UTF-8 must already equal canonical binding bytes and verify the digest. |
| `recipe_document`, `recipe_digest` | string, `ContentDigest` | Document string re-encoded as UTF-8 must already equal canonical recipe bytes and verify the digest. |
| `invocation_document`, `invocation_digest` | string, `ContentDigest` | Document string re-encoded as UTF-8 must already equal canonical invocation bytes and verify the digest. |
| `compiler_contract_digest` | `ContentDigest` | Must equal the fixed V1 compiler identity. No compiler-contract document is supplied in the request. |

The package's informational compiler contract document is closed with exactly `{compiler_contract_ref,
canonicalization_ref, input_schema_refs, output_schema_refs}`. Its first two fields equal
`aci.protocol-compiler@1` and `aci-cjson-1`. Both schema-reference arrays are non-empty, unique and
ascending by exact string; their values equal the frozen fixture exactly. Its canonical digest is
the request's fixed compiler identity, but its bytes are not a request field.

The calculation executes in this order:

1. parse strict UTF-8 outer request bytes, validate its closed shape, and require the bytes to equal
   their canonical projection before decoding embedded document strings;
2. UTF-8 encode each embedded profile, binding, recipe and invocation document string, parse it
   with duplicate-key rejection, and validate its closed schema before trusting canonical form or
   any supplied digest;
3. require each validated document's bytes to equal its `aci-cjson-1` canonical projection;
4. verify each of the four supplied document digests against its exact canonical bytes;
5. require `compiler_contract_digest` to equal the fixed V1 compiler identity;
6. verify all cross-document IDs and digests by exact equality;
7. validate invocation values without coercion or defaults;
8. validate ordering, total obligation disposition and DAG invariants;
9. establish that the exact `(profile_digest, binding_digest, recipe_digest, invocation_digest)`
   tuple equals one of the two manifest cases; no result may be constructed before this gate;
10. if a required obligation is unsupported, construct and return only the closed unsupported
    result;
11. otherwise perform only explicit scalar placeholder substitution, construct and validate the
    closed candidate, canonicalize it, compute its digest and return the compiled result.

Failure precedence is total. The first failing category wins in this order:

1. outer `invalid_request_schema`, including noncanonical outer bytes;
2. `invalid_document_schema` in profile, binding, recipe, invocation order;
3. `noncanonical_bytes` in profile, binding, recipe, invocation order;
4. `digest_mismatch` in profile, binding, recipe, invocation order;
5. `compiler_identity_mismatch`;
6. `inactive_binding`;
7. `binding_mismatch`;
8. `invocation_mismatch`;
9. `invalid_parameter_value`;
10. `invalid_obligation_mapping`;
11. `invalid_graph`;
12. `fixture_not_admitted`.

The admission gate is part of the pure calculation and precedes both result branches. It is not a
registry lookup: it compares the request's exact four-digest tuple with the two immutable manifest tuples.
Artifact persistence runs only after an admitted `compiled` result; its sole additional failure is
`artifact_content_conflict`. An admitted `unsupported` result contains no candidate bytes or
artifact descriptor and can never enter the persistence seam.

The function has no clock, randomness, environment, filesystem discovery, registry, network,
provider, model, tool, scheduler, bus, command, journal, confirmation, pending-sheet, audit-ledger
or legacy-dispatch dependency. Equal request bytes and equal compiler/schema identities MUST return
byte-identical results.

### Rules and invariants

| ID | Rule | Formal obligation |
|---|---|---|
| PC-R1 | Closed validation precedes trust | `accepted(x) => closed_schema_valid(x) && canonical(x) && digest_verified(x)` |
| PC-R2 | Exact binding | `binding.(skill_id, skill_revision_digest, profile_digest, recipe_digest) == referenced_inputs` |
| PC-R3 | Exact invocation | `invocation.(skill_id, skill_revision_digest, profile_digest, binding_digest, recipe_digest) == referenced_inputs` |
| PC-R4 | Total obligations | `set(recipe.obligation_rules.obligation_id) == set(profile.obligations.obligation_id)` |
| PC-R5 | Required unsupported blocks | `exists required unsupported => outcome=unsupported && candidate_absent` |
| PC-R6 | Closed acyclic graph | `all_refs_resolve_once && topo_count == node_count && every_nonterminal_reaches_terminal` |
| PC-R7 | No inference or coercion | `output_semantics = explicit(validated_inputs, scalar_substitution_only)` |
| PC-R8 | Logical capability ceiling | `candidate.capability_requirements == profile.capability_requirements && effective_grants(candidate)=empty` |
| PC-R9 | Determinism | `same_request -> byte_identical_result` |
| PC-R10 | Zero authority/effects | `commands + events + receipts + confirmations + runs + provider_calls + scheduler_actions + external_effects = 0` |
| PC-R11 | Complete invalidation lineage | `candidate.source_binding` contains every supplied semantics-bearing digest exactly once. |
| PC-R12 | Candidate is not executable authority | `candidate_digest != authority_token && candidate cannot satisfy dispatch_spec_digest` |

## ProtocolCompiler

Internal interface with one method:

```text
compileCandidate(request_bytes) -> compiled_result_bytes | CompileFailure
```

`request_bytes` and successful `compiled_result_bytes` are canonical bytes under their respective
closed schemas. The interface MUST expose no `confirm`, `run`, `launch`, `schedule`, `resolve`,
`activate`, `revoke` or provider-specific method.

## ProtocolInputsToDispatchCandidate

**From:** validated `SkillExecutionProfile`, `SkillProtocolBinding`, `ProtocolRecipe`,
`SkillProtocolInvocation` and explicit compiler identities
**To:** canonical non-authoritative `DispatchCandidate`
**Direction:** internal

| Source | Candidate field | Transform |
|---|---|---|
| Exact input/compiler digests | `source_binding` | Direct copy; no alias or version resolution. |
| Invocation `values` | `invocation_values` | Direct ordered copy after validation. |
| Recipe `nodes` | `nodes` | Direct projection plus explicit scalar placeholder substitution. |
| Recipe `edges`, `terminal_node_ids` | Same-named fields | Direct ordered copy. |
| Recipe `obligation_rules` | `obligation_dispositions` | Direct ordered copy after totality validation. |
| Profile `capability_requirements` | Same-named field | Direct ordered copy as logical requests only. |
| Profile `outputs` | `outputs` | Direct ordered copy. |

There is no mapping from this capability directly to `DispatchSpec`, `ConfirmedDispatch`, `Run`,
an agent invocation, a provider request, a journal command/event or an audit-ledger row.

## Artifact persistence seam

`CompileDispatchCandidate` itself performs no persistence. After a compiled result exists, the
bounded `RuntimeService.compile_and_store_dispatch_candidate` application method MAY idempotently
UTF-8 encode `candidate_document` and put those bytes through the existing finalized
[`Artifact`](domain.md#artifact) boundary using exactly:

```text
schema_ref = "aci.dispatch-candidate@1"
classification = "runtime-internal"
content_hash = candidate_digest
media_type = "application/json"
```

`artifact_id` and `finalization_receipt_ref` are ArtifactStore-owned operational metadata outside
candidate/result bytes; V1 uses the existing content-derived `art_<first-32-hex>` identity and does
not redefine it. The application method returns `{compiled_result, artifact_ref}` where
`artifact_ref` is the existing ArtifactStore reference shape. The put is the only permitted
persistence. Equal content and policy return the same artifact identity; the receipt reference may
be the already-finalized stored receipt. Equal content under divergent metadata/policy fails closed
as `artifact_content_conflict`. The put
MUST NOT append a runtime command/event, create a command or publication receipt, mutate a pending
sheet, write YAML, create `ConfirmedDispatch`/`DispatchSpec`/`Run`, resolve capabilities, schedule a
node, launch a provider or emit any external effect. The candidate artifact remains proposal
evidence and may be deleted under artifact retention policy without altering runtime authority.

## Closed failures

| Code | Meaning |
|---|---|
| `invalid_request_schema` | Request is not the exact closed request schema. |
| `noncanonical_bytes` | Embedded bytes do not equal canonical bytes for the decoded value. |
| `digest_mismatch` | A supplied profile, binding, recipe or invocation digest does not verify its exact bytes. |
| `invalid_document_schema` | An embedded document violates its closed schema. |
| `inactive_binding` | Binding status is not exactly `active`. |
| `binding_mismatch` | Binding identities/digests do not equal supplied inputs. |
| `invocation_mismatch` | Invocation identities/digests do not equal supplied inputs. |
| `invalid_parameter_value` | A value is absent, undeclared, duplicated, out of bounds, needs coercion/defaulting or is a string containing the forbidden V1 template delimiters `{{` or `}}`. |
| `invalid_obligation_mapping` | Obligation coverage, disposition shape or target reference is invalid. |
| `invalid_graph` | Closure, uniqueness, ordering, acyclicity, reachability or terminal rules fail. |
| `compiler_identity_mismatch` | Compiler-contract digest differs from the frozen V1 manifest. |
| `fixture_not_admitted` | The four input-document digests do not equal either complete case tuple in the frozen V1 package. |
| `artifact_content_conflict` | Optional artifact persistence found unequal bytes at the same identity. |

Errors are stable identifiers. A failure returns no partial candidate, artifact descriptor or
persistent mutation. Error-detail text is diagnostic and non-authoritative.

## Frozen V1 fixture and admission

V1 admits exactly one repository-built-in fixture package with exactly two cases:
[protocol-compilation-v1@1](fixtures/protocol-compilation-v1/manifest.json). The manifest's canonical
digest is `sha256:e5cc329254ab8f748888f198ee004cba45f186b5ca21702612932f2c66ef0420`.
The `compiled` case maps its exact four-input digest tuple to `result.json` and `candidate.json`.
The `required-unsupported` case maps its exact four-input digest tuple to
`unsupported-result.json`; it has no candidate artifact.

Repository files are newline-terminated JSON transport containers. Their `raw file SHA-256` binds
the checked-in bytes. `Canonical document digest` is computed by strict parsing followed by
`aci-cjson-1` projection; only that no-newline canonical text may populate a compile request's
`*_document` field.

| Artifact | Raw file SHA-256 | Canonical document digest |
|---|---|---|
| [skill-source.json](fixtures/protocol-compilation-v1/skill-source.json) | `sha256:1a1b13f817e88b9ab08f05c15ca33b709d75fa0cd153455cfe9cf35480e1a742` | `sha256:13ea3dea6640fd553a56662c7efd4bc63480f82b07c49f6e3614b72f4201bc36` |
| [profile.json](fixtures/protocol-compilation-v1/profile.json) | `sha256:da430d5f1cb0bc73c20f5722a5678c993983d70a6b3076f33021083dadd19ed5` | `sha256:43229944b101d12c6d14008d1db17f40c41277b7b441417c7ca5cd38006d7d17` |
| [recipe.json](fixtures/protocol-compilation-v1/recipe.json) | `sha256:05731f234c5a9aaada6b253c012219da33ae36301820b85bd7f5d55c2953d0bd` | `sha256:92fbf20eebbe5ba490bcd1969eed86e3ae91e4e643d7f448a1a089d3be2b50e3` |
| [binding.json](fixtures/protocol-compilation-v1/binding.json) | `sha256:e8e6a30e697b4bf0a646c1345a1c3a299b95fcd66dc8cc41f6fc7405936df681` | `sha256:26d7a8a3fb4955a9442d5807b7c27c1c1f204b394e3862437c49a4aae5b14c7b` |
| [invocation.json](fixtures/protocol-compilation-v1/invocation.json) | `sha256:d83595d04a3a4808dc8925aba6195561a37ffea75d7512e9d388749743be66ce` | `sha256:469dff24fc67a048a0f5f7040704c3601861beb386b9713dc3eb4e3b233de77b` |
| [compiler-contract.json](fixtures/protocol-compilation-v1/compiler-contract.json) | `sha256:6b15b4f6091058181cf7f32c9a8f155b5c0d8a6e6d4e9c35c6a36c716b2b947b` | `sha256:9fd10473647a5ea5a7f03df6370773fab2af911cca9d37ffc1e2b7912a009543` |
| [candidate.json](fixtures/protocol-compilation-v1/candidate.json) | `sha256:e05ae398a2f6111e3fff4620156b28320eeebbb835bee3a0c2f4a7d77a26f9b4` | `sha256:9b829ca70a4717a133a8e42b18e7d95210d1bbfcd5c1e785b56b38778f6df795` |
| [result.json](fixtures/protocol-compilation-v1/result.json) | `sha256:09714366cd3af0e3f965570b77c334bd3fc880ff38bb80b1ef379945039d0542` | `sha256:1a38bb57cddfc8940c1ff19011f543b18e8844a2e2d68b12a340ded527aecb84` |
| [unsupported-profile.json](fixtures/protocol-compilation-v1/unsupported-profile.json) | `sha256:0db09987f24184a2e05aa7179f3017283a81f646afeb69d0d60035e6f597322b` | `sha256:43ec4c29eca01a6786ec9fff2723c2623828af286e80c67f2b320672d002fa1e` |
| [unsupported-recipe.json](fixtures/protocol-compilation-v1/unsupported-recipe.json) | `sha256:e89e07b4ad082a7cf00e00fe2eb3125e22fdc054a6e31a635dce9fd67d068da3` | `sha256:16ce0d514a5b1b42d1c2170d0c4eb8b04a72d150adb4f7bb7b0ef91796c8aaa1` |
| [unsupported-binding.json](fixtures/protocol-compilation-v1/unsupported-binding.json) | `sha256:9e021be2fecd37b594d8d586086027d4a79413fe5f2b366dd2dd7a40a5ee114b` | `sha256:10bc707b787041d8b3327a1f3096b5635fae56d75975b0ffbf81f82fa2b00f8a` |
| [unsupported-invocation.json](fixtures/protocol-compilation-v1/unsupported-invocation.json) | `sha256:ef06ac2d4cd7deaf59b9c570af1b638574caeefceed33d6592e5d001c68e7e5c` | `sha256:0fdbd75e214f91a0ad53cec35849d43208af1d51dfa1f1c0300cfa0be3a11c17` |
| [unsupported-result.json](fixtures/protocol-compilation-v1/unsupported-result.json) | `sha256:61c7722659c8c152c35e6f8c0887b2b48e9862e202db70cdfd220ed1ece29ad4` | `sha256:9544a32ccf39309dc778d78623948675c9f80e73ecae52a0108458db35ae0578` |
| [manifest.json](fixtures/protocol-compilation-v1/manifest.json) | `sha256:8b902a972e7c605dc5df3ba51b35a0e1d0c0bfafb7d27d7e592f7bbcc49b7553` | `sha256:e5cc329254ab8f748888f198ee004cba45f186b5ca21702612932f2c66ef0420` |

The calculation rejects every four-digest tuple other than these two complete tuples as
`fixture_not_admitted` before constructing either result variant. Tests may use malformed or
internally inconsistent inputs to prove earlier closed failures, but a schema-valid third tuple is
never admitted and cannot produce or persist a candidate. General recipe/profile admission requires
the deferred governed registry lifecycle.

## Verification obligations

| Test ID | Required executable proof |
|---|---|
| `T-ACI-PC1` | Every input, nested item, request, output and result rejects unknown/missing/duplicate fields, forbidden nulls and wrong primitive types. |
| `T-ACI-PC2` | Golden vectors assert exact canonical bytes and qualified SHA-256 digests, including NFC, key order, array order, omission, integers and rejected floats. |
| `T-ACI-PC3` | Each mismatched profile/binding/recipe/invocation digest is `digest_mismatch`; any non-fixed `compiler_contract_digest` is solely `compiler_identity_mismatch`; changing any canonical input byte changes its digest and invalidates old lineage. |
| `T-ACI-PC4` | Missing/extra/duplicate/unsorted parameters, invalid scalar values, coercion, template delimiters inside invocation strings and undeclared recipe placeholders fail without defaults, inference or recursive evaluation. |
| `T-ACI-PC5` | Obligation mapping is total and unique; the admitted required-unsupported case returns only exact `unsupported-result.json` and never reaches ArtifactStore. A schema-valid mutation of a recipe obligation to `superseded`, with the required authority reference and every dependent digest recomputed, reaches admission and is rejected as a third tuple with `fixture_not_admitted`. |
| `T-ACI-PC6` | Unknown endpoints, duplicate IDs, self-edges, cycles, unreachable terminal paths, outgoing terminal edges and unresolved references fail deterministically. |
| `T-ACI-PC7` | Candidate capabilities equal logical profile requirements byte-for-byte and contain no provider, credential, permission, availability, resolution or effective-grant claim. |
| `T-ACI-PC8` | Repeated compilation across process restarts returns byte-identical candidate/result bytes, digest and artifact identity. |
| `T-ACI-PC9` | Spies prove zero clock/random/environment/registry/network/provider/tool/scheduler/bus/journal/confirmation/YAML/legacy effects during compilation. |
| `T-ACI-PC10` | Optional Artifact put is idempotent for equal bytes, conflicts for unequal bytes at one identity and produces no runtime command/event or command/publication/dispatch receipt; the existing artifact-finalization receipt remains outside candidate/result bytes. |
| `T-ACI-PC11` | The package's compiled case produces exact candidate/result bytes and its required-unsupported case produces exact unsupported-result bytes with no candidate; all output fields trace to explicit input or allowed scalar substitution. |
| `T-ACI-PC12` | Boundary tests prove candidate bytes/digest cannot satisfy `DispatchSpec` or confirmation inputs and no API path creates `ConfirmedDispatch`, `Run`, attempts or effects. |

## Implementation status and first slice

The contract is specified for one bounded implementation slice. Bounded conformance evidence for
`T-ACI-PC1` through `T-ACI-PC12` and separate independent reviews now pass. The implementation
status is **implemented and verified for the frozen two-case package only**. The claim is limited to
pure candidate compilation plus optional runtime-internal artifact storage for the package's one
compiled read-only case; the required-unsupported case is never persisted.

The implementation MUST NOT generalize the fixture registry, accept repository/user-provided
recipes, discover skill closures, or wire the compiler into confirmation or runtime execution as
part of this slice.

## Explicitly deferred contracts

The following require separate promotion and test obligations:

- persistent profile/binding/recipe registry ownership records;
- activation, supersession, revocation, history, compare-and-swap and revocation races;
- trust anchors and `ProtocolAuthoringCommand` admission;
- arbitrary or mutating recipes, path ownership, rework and dynamic graph variants;
- compatibility/latest-version resolution and schema migration;
- candidate-to-confirmation projection, capability resolution and the total mapping into canonical
  `DispatchSpec` bytes;
- human acceptance of the exact displayed `dispatch_spec_digest`;
- `ConfirmedDispatch`, `Run`, commands, events, receipts, journals, provider lifecycle, scheduling,
  effects, recovery and replay.

The future confirmation projection MUST consume candidate evidence as non-authoritative input,
resolve capabilities under its existing owner, produce and display complete canonical
`DispatchSpec` bytes and digest, and accept only that exact digest. It MUST NOT mutate the candidate
into authority, accept `candidate_digest` as `dispatch_spec_digest`, or redefine `ProtocolRecipe`
as a second executable recipe authority.

## Feature concept graph

The current DomainSpec relationship vocabulary has no canonical edge from a Mapping to a Value
Object. Its `calculates` edge is Calculation-to-Operation, but this pure slice defines no protocol
compilation Operation and no admissible edge from the Calculation directly to its Value Object
result. Therefore `ProtocolInputsToDispatchCandidate`, `DispatchCandidate` and
`CompileDispatchCandidate` remain in the Concept Registry without inventing a graph triple.

## Decisions

| ID | Decision |
|---|---|
| PC-D1 | ACI Protocol Governance owns exact profile/binding/recipe/invocation compilation only through a non-authoritative candidate. |
| PC-D2 | V1 consumes immutable caller-supplied snapshots and implements no lifecycle registry. |
| PC-D3 | V1 supports one repository-built-in package with exactly two read-only finite-DAG cases and performs no inference. |
| PC-D4 | Canonical closed schemas and qualified SHA-256 digests define identity and invalidation. |
| PC-D5 | Capabilities remain logical requirements until the separately owned confirmation boundary resolves them. |
| PC-D6 | Compilation is pure; the only persistence seam is an optional runtime-internal `Artifact` put. |
| PC-D7 | Candidate and recipe data cannot substitute for canonical confirmed `DispatchSpec` authority. |

## Connections

| Document | Type | Description |
|---|---|---|
| [ACI-PG-001](../../../decisions/aci-protocol-governance-ownership.md) | `derives-from` | Ratifies ownership through non-authoritative candidate compilation. |
| [Agents Communication Protocols](../discovery/agents-communication-protocols/README.md) | `derives-from` | Supplies the promoted protocol intent, identity and authority separation. |
| [Agent Tools and Delegated Supervision](../discovery/agent-tools-and-delegated-supervision.md) | `depends-on` | Preserves the external capability-resolution boundary and closes OQ-ATD3. |
| [ACI Domain](domain.md) | `depends-on` | Owns `Artifact`, `ContentDigest`, `DispatchSpec`, `ConfirmedDispatch` and `Run`; this capability references but does not redefine them. |
| [ACI canonical contract ADR](../adrs/ADR-001-persistence-replay-and-canonical-contracts.md) | `depends-on` | Owns `aci-cjson-1` canonical-byte and digest rules. |
| [Storage and artifact policy](../storage-and-artifact-policy.md) | `depends-on` | Owns ArtifactStore finalization, content addressing and authority separation. |
