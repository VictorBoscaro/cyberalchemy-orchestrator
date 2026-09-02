# Proposed DraftGraph compilation contract

Status: `proposed`; specification evidence only; not implemented or accepted as canonical ACI v2.

## Boundary

`DraftGraph` is a closed, non-authoritative authoring value. It is not shown for confirmation, does
not authorize work and must never be sent to the runtime. The only proposed logical authority is the
closed `ExecutionGraph` emitted after successful compilation. Confirmation binds the canonical
`ExecutionGraph` digest.

The compilation function is:

```text
compile(verified_compilation_context, draft, policy, catalog, resources)
  -> ExecutionGraph | typed compilation error
```

Every output value must have exactly one source class:

1. copied or name-mapped from the draft or frozen system compilation context;
2. fixed by this contract or the selected policy; or
3. selected by exact key from the catalog/resource set.

There is no inference, best match, fallback provider, fallback model, implicit permission, mutable
lookup or runtime completion step.

## Inputs

- `draft`: validates against `draft-graph-v1.proposed.schema.json` and the semantic rules below.
- `verified_compilation_context`: a closed, frozen allocation produced by the trusted system
  allocator while its reservation is held. It
  contains exactly `schema`, `dispatch_id`, `revision`, `allocation_id`, `allocation_status` and
  `prior_accepted_graph_digest`; no value is copied from or selected by the LLM. `revision` matches
  `^r[1-9][0-9]*$`; `r1` requires a null prior digest, and every later revision requires the exact
  prior accepted graph digest.
- `policy`: one closed policy value. Unknown fields or unsupported policy versions are rejected.
- `catalog`: one closed set of immutable, digest-pinned semantics/provider/model/profile/tool/
  validator/credential records. Keys are unique within each table. DraftGraph v1 cannot request
  commands.
- `resources`: one closed set of exact inline bytes or immutable URI records with a SHA-256 digest.
  The fixture uses inline UTF-8 bytes only. Resource keys are unique.

For the fixture formats in this work unit, every object is closed even though separate JSON Schemas
for those compiler-input formats are deferred to the implementation/conformance SWU. The compiler
must reject an unknown field rather than ignore it.

## Alias and identifier rules

Draft keys are author-facing aliases. They are not canonical IDs. For this proposed contract, all
keys already match `^[a-z][a-z0-9_]{0,63}$`; the compiler must not sanitize or repair a key.

| Canonical value | Exact derivation |
|---|---|
| `dispatch_id` | exact `compilation_context.dispatch_id` allocated and reserved by the trusted system |
| `revision` | exact `compilation_context.revision` allocated and reserved by the trusted system |
| member ID | `"member:" + resource_binding.alias` |
| node ID | `"node:" + node.key` |
| input ID | `"input:" + input.key`, scoped to its node |
| output ID | `"output:" + output.key`, scoped to its node |
| validation rule ID | `"rule:" + validation.key`, scoped to its node |
| authored control/feedback edge ID | `"edge:" + edge.key` |
| derived data edge ID | `"edge:" + producer_key + ":" + consumer_key + ":data"` |

Any derived-ID collision is `DG_ID_COLLISION`; the compiler may not add a suffix. Within one node,
input, output and validation aliases are separately unique. Node, resource and authored-edge aliases
are globally unique in their respective arrays.

The DraftGraph contains neither a dispatch identity nor a revision. Author-facing node/resource/
edge keys are local aliases only and cannot select `(dispatch_id, revision)`.

The allocator is the sole identity/revision producer. For a new logical dispatch it atomically
reserves a new opaque `dispatch_id` and `r1`. For an existing dispatch it reserves exactly the next
revision after the latest accepted revision; it also carries that prior accepted digest in
`prior_accepted_graph_digest`. The system holds that exact reservation through compilation; only its
trusted verifier can construct the `verified_compilation_context` accepted by the pure compiler.
Missing, released, expired or no-longer-latest reservations fail at that entry gate as
`DG_IDENTITY_CONTEXT_STALE`. A pair already bound to any accepted graph fails as
`DG_AUTHORITY_CONFLICT`; the compiler cannot reuse it even when bytes happen to match. Allocation
and acceptance are system operations outside the DraftGraph and runtime. The compiler copies the
frozen pair but cannot allocate, increment, override or repair it.

## Ordered compilation

The implementation must perform these steps in order and return before emitting graph bytes on the
first error. A failure emits no partial `ExecutionGraph`.

1. Parse all five inputs with duplicate-key rejection and validate their closed structural shapes.
2. Require the trusted allocator gate's verified context type, validate its closed value and reject
   stale/conflicting authority identity before invoking the pure compiler. The compiler itself does
   not query mutable allocator or runtime state.
3. Verify uniqueness of every key/alias and verify all catalog `digest_source` and resource content
   digests against exact UTF-8 bytes.
4. Resolve every draft key by exact equality. Zero matches is `DG_UNKNOWN_REFERENCE`; more than one
   is `DG_AMBIGUOUS_REFERENCE`.
5. Check the requested agent tuple `(role, provider_key, model_key, profile_key, credential_key)`
   against one exact `policy.allowed_agent_bindings` row. Check catalog compatibility among provider,
   model and profile. A mismatch is `DG_AGENT_BINDING_DENIED`.
6. Check requested capabilities, validators, resources and access against policy. Permission excess
   is rejected; numeric limit excess is restricted by the exact rule below.
7. Validate dataflow, predicates, topology, lifecycle and total budgets. No missing producer,
   impossible output contract, unreachable node or unclosed control string is repairable.
8. Emit the logical graph using the mappings and array-order rules below.
9. Validate the emitted value against the proposed ExecutionGraph schema and the semantic rules.
10. Canonicalize only the complete successful graph. The proposed `aci-cjson-1` profile is UTF-8 JSON
   Canonicalization Scheme (RFC 8785), with no BOM; `execution_graph_digest` is
   `"sha256:" + lowercase_hex(SHA-256(canonical_bytes))`. The digest is external evidence and is
   not inserted into the graph.

Step 10 is a proposed contract choice for independent review. This work unit did not execute a
compiler or a conforming RFC 8785 implementation and therefore does not claim a canonical digest.

## Policy rules

### Limits

All three global and per-node requested limits are mandatory in the draft. There are no defaults.
For each dimension, first compute the effective global value and every effective node value:

```text
effective_global[d] = min(requested_global[d], policy_global_ceiling[d])
effective_node[n,d] = min(requested_node[n,d], policy_node_ceiling[d])
```

This restriction is allowed only when `numeric_limit_excess_action == "restrict"`; otherwise excess
is `DG_LIMIT_DENIED`. For every component restriction, a compiler report outside the authority graph
must contain exactly `{kind:"numeric_limit_restriction", path, requested, effective,
policy_ceiling}`. The compiler may never emit a value greater than requested.

The sum of effective node `max_tokens` and `wall_clock_seconds` must not exceed the corresponding
effective global value. The sum of node `max_attempts` must not exceed global `max_attempts` for this
proposed contract. This invariant is evaluated after every component restriction. Failure is
`DG_GLOBAL_BUDGET_EXCEEDED`; the compiler emits no graph and must not silently rebalance other nodes
or the global value. Thus effective node tokens `[12000,12000,6000]` against global `24000` fail
because their reserved total is `30000`.

### Permissions

- Every requested capability key must exist in the catalog and policy.
- Every requested operation must occur in both the catalog capability record and the policy grant.
- Every requested path must exactly equal an allowed policy path. Prefix matching is forbidden.
- `deny` requires an empty allow/grants array.
- DraftGraph v1 supports only `commands={mode:"deny",grants:[]}`. `allowlist`, any grant, and any
  `command_key`, `argv`, `cwd` or environment resource are structurally unrepresentable and fail as
  `DG_DRAFT_SCHEMA_INVALID` (or `DG_COMMAND_UNSUPPORTED` if encountered after a trusted migration).
- An allowlisted network target, effect, commit or push must be explicitly allowed by the
  corresponding policy ceiling.
- The emitted set and order equal the requested set and order after validation. The policy cannot
  inject a capability, operation, path, network target, command, effect or version-control grant.

Any excess is `DG_AUTHORITY_EXPANSION` if introduced by the compiler or `DG_PERMISSION_DENIED` if it
was requested by the draft but denied by policy. Both fail closed.

## Field transformation

### Graph envelope

| ExecutionGraph field | Transformation |
|---|---|
| `schema` | fixed literal `aci.execution-graph@2` |
| `dispatch_id`, `revision` | exact frozen system compilation context; never draft values |
| `objective` | exact copy of `draft.objective` |
| `semantics_ref` | select `catalog.semantics[policy.semantics_key].ref` |
| `global_limits` | limit rule over `draft.requested_global_limits` |
| `nodes` | one output node per draft node, preserving draft order |
| `edges` | derived data edges, then authored control/feedback edges |
| `lifecycle` | copy draft choices and map node aliases to node IDs |
| `audit_requirements` | copy fixed booleans from policy and map its receipt resource key to a member ID |

### Content members

For each `draft.resources` binding in draft order, select exactly one resource by `resource_key`, copy
its kind/media type/content-or-URI/digest and replace its key with the derived member ID. Then append
the policy receipt resource if it was not already bound, using the alias equal to its resource key.
Two bindings to one resource or one alias to multiple resources are rejected as
`DG_RESOURCE_BINDING_CONFLICT`.

All output contract resources and validator configuration resources must be bound by the draft and
have `kind == "schema"`. The policy receipt resource must have `kind == "schema"`. A mismatch or a
schema that is not a valid closed JSON Schema is `DG_OUTPUT_CONTRACT_INVALID`. The compilation
contract does not accept schema refs without exact bytes.

### Nodes

| ExecutionGraph path | Transformation |
|---|---|
| `nodes[].node_id` | node identifier rule |
| `.objective`, `.instructions` | exact draft strings |
| `.agent.display_name`, `.agent.role` | exact draft strings |
| `.agent.{provider,model,profile}_ref` | exact `.ref` from the keyed catalog records |
| `.agent.credential_ref` | `null` for a null key; otherwise exact catalog credential authority record after policy admission |
| `.tools[]` | exact tool ref for each requested capability plus requested operations; preserve request order and operation order |
| `.inputs[]` | preserve order; derive input ID; map resource alias to member ID or node/output aliases to canonical IDs |
| `.outputs[]` | preserve order; derive output ID; map contract resource alias to schema member ID |
| `.limits` | per-node limit rule |
| `.isolation` | exact validated access request; commands are fixed to deny/empty in DraftGraph v1 |
| `.start_when` | exact closed enum |
| `.validation[]` | derive rule ID; select validator ref; map optional configuration alias; copy `on_fail` |
| `.success_condition` | map one required output alias to ID; only `output_present` or `output_field_equals` is admitted |
| `.stop_conditions[].when` | map local input/output alias to ID; closed stop predicates may also use required-input unavailability or attempts exhaustion |
| `.stop_conditions[].{action,reason_code}` | exact closed draft values |

#### `output_field_equals` proof

For every success or stop `output_field_equals`, the compiler resolves the named output to its
bound exact schema content member before graph emission. It decodes JSON Pointer tokens using only
RFC 6901 `~0` and `~1`. Every traversed object ancestor must declare literal `"type":"object"` and
the selected property must be explicitly **required**; every traversed array ancestor must declare
literal `"type":"array"`, and an `items` schema may be selected only by a canonical decimal index
proven present by `minItems`. Absent `type`, type arrays/unions such as `object|null` or
`array|null`, and composition cannot prove traversal even when `properties`, `required`, `items` or
`minItems` are present; these cases are `DG_PREDICATE_POINTER_UNPROVABLE`. A missing
property/index rule or malformed escape is `DG_PREDICATE_POINTER_INVALID`.

The resolved subschema must directly expose at least one proof keyword among `type`, `const` or
`enum`. `$ref`, `$dynamicRef`, `allOf`, `anyOf`, `oneOf`, `not` and conditional composition are
fail-closed as `DG_PREDICATE_POINTER_UNPROVABLE` in DraftGraph v1; the compiler may not guess or use
a permissive fallback. The scalar predicate `value` must validate against the resolved Draft
2020-12 subschema. Type, const or enum failure is `DG_PREDICATE_VALUE_INVALID`. The same checks run
again over the emitted EG and its resolved `schema_member_id` before canonical bytes/digest.

### Edges and dataflow

Node inputs are the sole output-to-input mapping. For every distinct `(producer node, consumer
node)` pair used by a `node_output` source, emit exactly one `data/on_success` edge. Iterate consumer
nodes in draft order and their inputs in input order; emit a pair on first occurrence only.

Draft `edges` may contain only `control` or `feedback`; map aliases and append them in draft order.
There is no draft `data` edge because that would duplicate the authoritative input mapping.

A `node_output` source must name one earlier producer node and one of that node's outputs, unless an
explicit feedback edge authorizes the reverse dependency. Missing producers/outputs are
`DG_INPUT_WITHOUT_PRODUCER`; undeclared feedback, cycles outside feedback semantics, unreachable
nodes and impossible joins are `DG_TOPOLOGY_INVALID`.

## Semantic validation

In addition to JSON Schema validation, compilation fails unless:

- all aliases and derived IDs satisfy the uniqueness/scoping rules;
- every input, output, schema member, predicate, node, root and terminal reference resolves once;
- each predicate refers to an input/output of its owning node;
- every success predicate names an output declared `required:true`; output contract validation is a
  mandatory predecessor to predicate evaluation, so presence/equality cannot bypass schema checks;
- `input_unavailable` is valid only in a stop condition, must name an owning-node input declared
  `required:true`, and cannot signal success;
- `attempts_exhausted` is valid only in a stop condition and its action must be `stop_node` or
  `fail_graph`; it cannot signal success;
- an `output_field_equals` pointer exists in the owning output's JSON Schema and its value is
  admitted by that location's schema under the exact proof algorithm above;
- every output contract and receipt contract is a valid closed Draft 2020-12 JSON Schema;
- entry nodes have `roots_ready`; non-entry nodes are reachable and their start condition is
  satisfiable by their predecessors;
- every terminal is reachable and every reachable branch can reach a terminal or an explicit graph
  stop/fail action;
- requested/emitted authority is a subset of policy and never larger than the draft request; and
- no confirmation principal/time, run/attempt/status, receipt value or result value appears in any
  compiler input or output.

## Fixture expectation and evidence ceiling

Applying this contract to `fixtures/compilation-context.json`, `review-correct-verify.draft.json`,
`fixtures/policy.json`, `fixtures/catalog.json` and `fixtures/resources.json` is specified to produce the logical value in
`review-correct-verify.expected.execution.json`. The expected value validates against the current
proposed ExecutionGraph schema and deliberately replaces the old toy's placeholder artifact hashes
with explicit fixture catalog records.

That expected value is a conformance target, not evidence that compilation occurred. No compiler was
implemented or run in this SWU, no byte-for-byte equivalence with the old toy is claimed, and the
canonical v2 specification remains blocked pending independent review and the successor SWU.

## Runtime exclusion

The runtime receives only an accepted `ExecutionGraph` and its confirmation envelope. It may derive
run/node-attempt/message/effect identifiers and observations, but it may not choose a provider,
model, profile, credential scope, tool, validator, input, output, limit, path, effect, predicate,
edge or lifecycle behavior omitted by compilation.
