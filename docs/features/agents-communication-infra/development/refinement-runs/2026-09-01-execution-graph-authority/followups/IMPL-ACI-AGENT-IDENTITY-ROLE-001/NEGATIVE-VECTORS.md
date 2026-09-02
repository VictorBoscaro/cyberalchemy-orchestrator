# Negative compilation vectors

Each vector starts from the five positive inputs (compilation context, draft, policy, catalog and
resources) in this directory and applies only the stated
mutation. `No graph` means compilation returns the typed error before canonical bytes, digest,
confirmation or state mutation. These are proposed conformance cases; this work unit checks their
preconditions but does not claim a compiler executed them.

| ID | Required mutation | Expected result | Postcondition |
|---|---|---|---|
| `DG-N01-UNKNOWN-CAPABILITY` | Append `{"capability_key":"shell_exec","operations":["run"]}` to `correct.capability_requests`; neither catalog nor policy contains the key. | `DG_UNKNOWN_REFERENCE` at `nodes[correct].capability_requests[shell_exec]` | no graph |
| `DG-N02-UNKNOWN-MODEL` | Set `verify.agent_request.model_key` to `unlisted_model`. | `DG_UNKNOWN_REFERENCE` at `nodes[verify].agent_request.model_key` | no graph |
| `DG-N03-PERMISSION-OUTSIDE-POLICY` | Append `workspace:/secrets` to `correct.access_request.write_paths`; it is absent from the exact policy allowlist. | `DG_PERMISSION_DENIED` at `nodes[correct].access_request.write_paths[1]` | no graph; policy does not trim or widen paths |
| `DG-N04-INPUT-WITHOUT-PRODUCER` | Set `verify.inputs[1].source.node_key` to `missing_reviewer`. | `DG_INPUT_WITHOUT_PRODUCER` | no graph; no inferred producer |
| `DG-N05-INVALID-OUTPUT-CONTRACT` | Replace `correction_schema.content` with `{"type":"object","required":["patch"],"properties":{},"additionalProperties":false}` and its digest with `sha256:9b7f66b69daca245218bd6af6d627fab7cebad36ff9766fe48987a84ccb0994a`. The schema requires `patch` while forbidding every property. | `DG_OUTPUT_CONTRACT_INVALID` | no graph |
| `DG-N06-AMBIGUOUS-CONDITION` | Replace `verify.success_condition` with `{"kind":"free_text","expression":"the correction looks good"}`. | `DG_DRAFT_SCHEMA_INVALID`; no free-text predicate variant exists | no graph; model prose is not executed |
| `DG-N07-AUTHORITY-EXPANSION` | Given the unchanged positive inputs, a candidate implementation emits `verify.isolation.network={"mode":"allowlist","allow":["internet"]}` instead of the requested deny/empty value. | conformance failure `DG_AUTHORITY_EXPANSION` | candidate output rejected; no digest/confirmation |
| `DG-N08-UNKNOWN-VALIDATOR` | Set `review.validation[0].validator_key` to `best_effort_review`. | `DG_UNKNOWN_REFERENCE` | no graph; no validator inferred from name or prose |
| `DG-N09-GLOBAL-BUDGET-EXCEEDED` | Set `review.requested_limits.max_tokens` to `13000`. Its effective value is `12000`, so effective node tokens become `[12000,12000,6000] = 30000` against global `24000`. | `DG_GLOBAL_BUDGET_EXCEEDED` after component restriction and total reservation check | no graph; no silent rebalance |
| `DG-N10-RESOURCE-DIGEST-DRIFT` | Change one byte in `result_x.content` without changing its digest. | `DG_RESOURCE_DIGEST_MISMATCH` | no graph |
| `DG-N11-SAFE-LIMIT-RESTRICTION` | Set `correct.requested_limits.max_tokens` from `12000` to `13000`. Effective nodes remain `[6000,12000,6000] = 24000`. | success with exactly `{"kind":"numeric_limit_restriction","path":"nodes[correct].limits.max_tokens","requested":13000,"effective":12000,"policy_ceiling":12000}` in the external compiler report | graph effective limits remain within global; report is not authority |
| `DG-N12-EXHAUSTION-AS-SUCCESS` | Replace `review.success_condition` with `{"kind":"attempts_exhausted"}`. | `DG_DRAFT_SCHEMA_INVALID` | no graph; failure cannot establish success |
| `DG-N13-UNAVAILABLE-INPUT-AS-SUCCESS` | Replace `review.success_condition` with `{"kind":"input_unavailable","input_key":"target"}`. | `DG_DRAFT_SCHEMA_INVALID` | no graph; unavailable required input cannot establish success |
| `DG-N14-COMMAND-UNSUPPORTED` | Replace `correct.access_request.commands` with an allowlist containing any `command_key`, `argv`, `cwd` and environment alias tuple. | `DG_DRAFT_SCHEMA_INVALID` (`DG_COMMAND_UNSUPPORTED` only after a trusted migration bypasses structural validation) | no command grant and no graph |
| `DG-N15-AUTHOR-IDENTITY-INJECTION` | Add `graph_key` or `draft_revision` to the DraftGraph root. | `DG_DRAFT_SCHEMA_INVALID` | author input cannot select dispatch identity/revision |
| `DG-N16-STALE-IDENTITY-CONTEXT` | Change `compilation_context.allocation_status` from `reserved` to `released`, or present a non-latest allocation. | `DG_IDENTITY_CONTEXT_STALE` | no graph; compiler cannot allocate or repair identity |
| `DG-N17-EXTRA-EXECUTABLE-ELEMENT` | Add an undeclared EG node, tool, input, output, validation rule, stop condition or command grant to a candidate output. Include duplicate-ID and unique-ID node variants. | conformance failure `DG_AUTHORITY_EXPANSION` or `DG_COMPILATION_MISMATCH` before digest | candidate output rejected |
| `DG-N18-MISSING-EXECUTABLE-ELEMENT` | Remove one declared EG node, tool, input, output, validation rule or stop condition from a candidate output. | conformance failure `DG_COMPILATION_MISMATCH` before digest | candidate output rejected |
| `DG-N19-PREDICATE-POINTER-MISSING` | In `verify.success_condition`, replace `/verdict` with `/does_not_exist` while retaining value `pass`; repeat against the emitted EG predicate. | `DG_PREDICATE_POINTER_INVALID` after resolving the bound `verification_schema` | no graph/digest; both draft and emitted-EG semantic paths reject |
| `DG-N20-PREDICATE-VALUE-INVALID` | In `verify.success_condition`, retain `/verdict` but replace `pass` with `bogus`; repeat against the emitted EG predicate. | `DG_PREDICATE_VALUE_INVALID` because `bogus` is outside `pass|flag|block` | no graph/digest; both draft and emitted-EG semantic paths reject |
| `DG-N21-PREDICATE-TYPELESS-OBJECT` | Bind a valid closed output schema whose required `nested` field is `{"properties":{"leaf":{"type":"string"}},"required":["leaf"]}` without `type`; use `/nested/leaf`, and prove `{"nested":5,...}` is schema-valid. Repeat on draft and emitted EG. | `DG_PREDICATE_POINTER_UNPROVABLE`; `properties`/`required` do not prove an object ancestor | no graph/digest; both semantic paths reject |
| `DG-N22-PREDICATE-NULLABLE-OBJECT` | Bind the N21 schema with `nested.type=["object","null"]`; use `/nested/leaf`, and prove `{"nested":null,...}` is schema-valid. Repeat on draft and emitted EG. | `DG_PREDICATE_POINTER_UNPROVABLE`; an `object|null` ancestor is not literal exact `type:"object"` | no graph/digest; both semantic paths reject |
| `DG-N23-PREDICATE-TYPELESS-ARRAY` | Bind a valid closed output schema whose required `arr` field is `{"items":{"type":"string"},"minItems":1}` without `type`; use `/arr/0`, and prove `{"arr":5,...}` is schema-valid. Repeat on draft and emitted EG. | `DG_PREDICATE_POINTER_UNPROVABLE`; `items`/`minItems` do not prove an array ancestor | no graph/digest; both semantic paths reject |
| `DG-N24-PREDICATE-NULLABLE-ARRAY` | Bind the N23 schema with `arr.type=["array","null"]`; use `/arr/0`, and prove `{"arr":null,...}` is schema-valid. Repeat on draft and emitted EG. | `DG_PREDICATE_POINTER_UNPROVABLE`; an `array|null` ancestor is not literal exact `type:"array"` | no graph/digest; both semantic paths reject |

## Harness obligations

A future negative-vector runner must:

1. apply mutations structurally, never by brittle text replacement;
2. verify the exact typed error and JSON path;
3. assert absence of graph bytes/digest and persistent mutation on every failure;
4. compare requested and emitted authority sets for `DG-N07`, `DG-N17` and `DG-N18`;
5. calculate all post-policy component and global invariants for `DG-N09` and `DG-N11`;
6. prove both failure-as-success mutations and the command tuple are structurally rejected; and
7. verify the exact restriction-report object for `DG-N11` without treating that report as a second
   authority; and
8. resolve the bound output schema for `DG-N19` and `DG-N20` on both draft and emitted-EG paths,
   proving missing pointers and enum/type/const mismatch fail closed; and
9. run `DG-N21` through `DG-N24` on both paths, validate each scalar/null counterexample against its
   mutated output schema, and prove typeless or nullable object/array ancestors remain unprovable.
