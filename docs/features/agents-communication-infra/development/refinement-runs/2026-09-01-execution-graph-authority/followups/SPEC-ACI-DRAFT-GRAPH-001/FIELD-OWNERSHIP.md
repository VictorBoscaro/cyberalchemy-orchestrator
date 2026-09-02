# ExecutionGraph field ownership

Status: proposed ownership audit for `SPEC-ACI-DRAFT-GRAPH-001`. `Compiler` means the only writer of
the logical graph; `origin` identifies the sole allowed source of the value it writes.

All fields in the current `aci.execution-graph@2` proposal are covered below. Every included field
changes canonical bytes and therefore participates in authority under the proposal's conservative
material-change rule—even display text. Whether display-only names should remain in that digest is
still a canonical-v2 review question, not silently answered by this work unit.

Abbreviations: `X` = frozen system compilation context, `DG` = DraftGraph, `P` = policy, `C` =
catalog, `R` = resource set, `EG` = ExecutionGraph.

| ExecutionGraph path | Sole origin / graph producer | Consumer | Authority effect | Deterministic source or rule | Failure |
|---|---|---|---|---|---|
| `schema` | compiler / compiler | EG parser, projector, confirmation writer | selects contract | fixed `aci.execution-graph@2` | unsupported contract |
| `dispatch_id` | trusted system allocator / compiler | confirmation conflict key, journal, projector | logical dispatch identity | exact frozen `compilation_context.dispatch_id`; DG has no identity field | stale allocation or accepted-pair conflict |
| `revision` | trusted system allocator / compiler | confirmation conflict key, projector | authority revision | exact frozen `compilation_context.revision`; DG has no revision field | stale/non-next reservation or accepted-pair conflict |
| `objective.statement` | LLM from user intent / compiler | agents, projector, audit | work purpose | exact `DG.objective.statement` | missing/empty |
| `objective.done_when[]` | LLM from user intent / compiler | assigned agents, projector, user and audit reader | non-controlling purpose/evidence expectation | exact ordered draft values; never read by scheduler, predicate evaluator or executable validator | missing/empty; executable control must use closed predicates/validation/lifecycle |
| `semantics_ref.{name,version,digest}` | policy selects, catalog defines / compiler | semantic validator, runtime | evaluator/scheduler meaning | exact `C.semantics[P.semantics_key].ref` | unknown/ambiguous/drifted digest |
| `content_members[]` membership/order | LLM/user selects; policy selects receipt / compiler | node input resolver, validators, audit | exact authorized content | draft binding order, then missing policy receipt resource | duplicate/conflicting/unresolved binding |
| `content_members[].member_id` | compiler / compiler | inputs, outputs, validators, audit | content identity within graph | `member:` + binding alias | collision |
| `.kind` | resource provider / compiler | semantic validator, content loader | permitted use of bytes | exact `R.resource.kind` | wrong kind for use |
| `.media_type` | resource provider / compiler | loader/parser | parsing mode | exact resource value | unsupported media type |
| `.encoding` | resource provider / compiler | content verifier/loader | byte interpretation | exact `utf-8` or `base64` | unsupported/invalid encoding |
| `.content` | user/resource provider / compiler | agent input or schema/policy parser | exact inline bytes | exact resource string | digest mismatch |
| `.immutable_uri` | resource provider / compiler | immutable content resolver | external byte location | exact resource URI; mutually exclusive with content | mutable/unsupported URI or digest mismatch |
| `.digest` | resource provider, verified by compiler / compiler | acceptance/content loader | pins exact bytes | SHA-256 over decoded exact content or resolved immutable bytes | mismatch/unavailable bytes |
| `global_limits.{max_attempts,max_tokens,wall_clock_seconds}` | LLM requests; policy caps / compiler | scheduler, projector | total resource ceiling | componentwise `min(DG.requested_global_limits, P.global_limit_ceiling)` | missing or budget inconsistency |
| `nodes[]` membership/order | LLM / compiler | scheduler, projector, audit | authorized work decomposition | one per draft node, draft order | zero, duplicate key, unreachable node |
| `nodes[].node_id` | compiler / compiler | scheduler, edges, dataflow, lifecycle | node identity | `node:` + `DG.nodes[].key` | collision |
| `.objective` | LLM / compiler | assigned agent, projector, audit | node outcome | exact draft string | missing/empty |
| `.instructions` | LLM / compiler | assigned agent | exact model instruction | exact draft string | missing/empty |
| `.agent.display_name` | LLM / compiler | projector, audit | presentation bytes currently affect digest | exact draft string | missing/empty |
| `.agent.role` | LLM / compiler | policy admission, projector, audit | behavioral responsibility | exact draft role admitted by one P binding | tuple denied/ambiguous |
| `.agent.provider_ref.{name,version,digest}` | catalog / compiler | provider adapter, projector | provider selection | exact provider record keyed by draft and admitted tuple | unknown/mismatch/drift |
| `.agent.model_ref.{name,version,digest}` | catalog / compiler | provider adapter, projector | model selection | exact model record keyed by draft and compatible with provider/profile | unknown/mismatch/drift |
| `.agent.profile_ref.{name,version,digest}` | catalog / compiler | host adapter, projector | execution profile | exact profile record keyed by draft and compatible tuple | unknown/mismatch/drift |
| `.agent.credential_ref` nullability | LLM requests; policy admits / compiler | credential resolver | whether a credential authority exists | null iff draft key is null and admitted tuple says null | missing or policy mismatch |
| `.credential_ref.handle` | catalog credential record / compiler | credential resolver | stable secret handle authority | exact selected record | unknown/mutable handle |
| `.credential_ref.resolver_ref.{name,version,digest}` | catalog / compiler | credential resolver | resolver implementation | exact selected record | unknown/drift |
| `.credential_ref.contract_version` | catalog / compiler | credential resolver | handle interpretation | exact selected record | unsupported version |
| `.credential_ref.scope_digest` | catalog, policy admits / compiler | credential resolver/policy | maximum credential privilege | exact selected record and admitted tuple | scope drift/expansion |
| `.tools[]` membership/order | LLM requests; policy admits / compiler | tool adapter, projector | tool capability | one per request, same order; never injected | unknown/denied/duplicate capability |
| `.tools[].tool_ref.{name,version,digest}` | catalog / compiler | tool adapter | tool implementation | exact capability record | unknown/drift |
| `.tools[].allowed_operations[]` | LLM requests; policy and catalog constrain / compiler | tool adapter, policy | operation grant | exact request order after membership checks | empty/unknown/denied/expanded op |
| `.inputs[]` membership/order | LLM / compiler | prompt assembler, scheduler | information flow | exact draft input order | duplicate local alias |
| `.inputs[].input_id` | compiler / compiler | predicates, prompt assembler | local input identity | `input:` + local alias | local collision |
| `.inputs[].required` | LLM / compiler | scheduler, stop evaluator | availability requirement | exact draft boolean | missing |
| `.inputs[].source.kind` | LLM / compiler | dataflow/content resolver | source namespace | `resource` maps to `content_member`; `node_output` copies | unknown variant |
| `.source.member_id` | LLM alias / compiler | content resolver | authorized content selection | bound alias to derived member ID | missing/wrong-kind member |
| `.source.selector` | LLM / compiler | content resolver | selected portion of content | exact draft selector under fixed semantics | invalid/unsupported selector |
| `.source.node_id` | LLM alias / compiler | scheduler/dataflow | producer identity | producer alias to derived node ID | missing producer |
| `.source.output_id` | LLM alias / compiler | scheduler/dataflow | producer output | producer-local alias to derived output ID | missing output |
| `.outputs[]` membership/order | LLM / compiler | agent output adapter, validators | required result surface | exact draft order | empty/duplicate alias |
| `.outputs[].output_id` | compiler / compiler | predicates, consumers, validators | local output identity | `output:` + local alias | local collision |
| `.outputs[].schema_member_id` | LLM selects resource / compiler | output validator | output contract | contract alias to schema member ID | absent/invalid/non-schema contract |
| `.outputs[].required` | LLM / compiler | scheduler/validator | required result | exact draft boolean | missing |
| `.limits.{max_attempts,max_tokens,wall_clock_seconds}` | LLM requests; policy caps / compiler | node scheduler, projector | node resource ceiling | componentwise minimum | missing/exceeds global total |
| `.isolation.read_paths[]` | LLM requests; policy admits / compiler | filesystem guard, projector | read authority | exact requested order; exact policy membership | denied/injected path |
| `.isolation.write_paths[]` | LLM requests; policy admits / compiler | filesystem guard, projector | write authority | exact requested order; exact policy membership | denied/injected path |
| `.isolation.network.{mode,allow[]}` | LLM requests; policy admits / compiler | network guard, projector | network authority | exact request; deny requires empty list | denied/injected target/inconsistent deny |
| `.isolation.commands.mode` | contract fixed / compiler | command guard, projector | command authority mode | DraftGraph v1 literal `deny` only | any allowlist is `DG_DRAFT_SCHEMA_INVALID`/`DG_COMMAND_UNSUPPORTED` |
| `.isolation.commands.grants[]` | contract fixed / compiler | command guard | no process authority in DraftGraph v1 | exact empty array | any grant is rejected as unsupported/authority expansion |
| `.commands.grants[].command_ref.{name,version,digest}` | compiler owns enforced absence / compiler | conformance validator; command guard only in a future contract | executable identity is prohibited | branch is never emitted while command mode is deny | candidate presence is `DG_COMMAND_UNSUPPORTED` |
| `.commands.grants[].argv[]` | compiler owns enforced absence / compiler | conformance validator; command guard only in a future contract | invocation authority is prohibited | no argv grammar or allow case exists; fail closed | candidate presence is `DG_COMMAND_UNSUPPORTED` |
| `.commands.grants[].cwd` | compiler owns enforced absence / compiler | conformance validator; command guard only in a future contract | cwd authority is prohibited | no cwd admission rule exists; fail closed | candidate presence is `DG_COMMAND_UNSUPPORTED` |
| `.commands.grants[].environment_member_id` | compiler owns enforced absence / compiler | conformance validator; command guard only in a future contract | environment authority is prohibited | no environment admission rule exists; fail closed | candidate presence is `DG_COMMAND_UNSUPPORTED` |
| `.isolation.external_effects.{mode,allow[]}` | LLM requests; policy admits / compiler | effect guard, projector | external-effect authority | exact request/order | denied/injected effect/inconsistent deny |
| `.isolation.version_control.{commit,push}` | LLM requests; policy admits / compiler | VCS guard, projector | repository mutation authority | exact booleans | denied or compiler-enabled action |
| `.start_when` | LLM / compiler | scheduler | join/start behavior | exact closed draft enum | impossible join/root mismatch |
| `.validation[]` membership/order | LLM / compiler | output validator, scheduler | acceptance/response behavior | exact draft order | empty/duplicate rule alias |
| `.validation[].rule_id` | compiler / compiler | validator/audit | local validation identity | `rule:` + local alias | local collision |
| `.validator_ref.{name,version,digest}` | catalog / compiler | validator dispatcher | validator implementation | exact keyed validator admitted by P | unknown/denied/drift |
| `.configuration_member_id` | LLM alias / compiler | validator | exact validator config | null or bound schema member ID | missing/wrong-kind config |
| `.on_fail` | LLM / compiler | scheduler | validation failure control | exact closed enum | unsupported action |
| `.success_condition.kind` | LLM / compiler | predicate evaluator after output-contract validation | success behavior | only `output_present` or `output_field_equals` | failure predicate or ambiguous kind |
| `.success_condition.output_id` | LLM alias / compiler | predicate evaluator after output-contract validation | observed required output | owning-node alias to a `required:true` output | absent/nonlocal/optional output |
| `.success_condition.json_pointer` | LLM / compiler | predicate evaluator/schema checker | tested output field | RFC 6901 pointer resolved only through ancestors with literal exact `type:"object"` plus required properties, or literal exact `type:"array"` plus array indices guaranteed by `minItems`, in the named output's exact bound schema; absent/union/nullable types and unsupported composition fail closed | `DG_PREDICATE_POINTER_INVALID` or `DG_PREDICATE_POINTER_UNPROVABLE` |
| `.success_condition.value` | LLM / compiler | predicate evaluator/schema checker | required success value | exact scalar validated against the resolved Draft 2020-12 subschema `type`/`const`/`enum` | `DG_PREDICATE_VALUE_INVALID` |
| `.success_condition.input_id` | compiler owns enforced absence / compiler | conformance validator; stop evaluator owns input unavailability elsewhere | prohibited success trigger | `input_unavailable` exists only in stop predicates | candidate presence is `DG_DRAFT_SCHEMA_INVALID` |
| `.success_condition` attempts variant | compiler owns enforced absence / compiler | conformance validator; stop evaluator owns exhaustion elsewhere | prohibited success trigger | `attempts_exhausted` exists only in stop predicates | candidate presence is `DG_DRAFT_SCHEMA_INVALID` |
| `.stop_conditions[]` membership/order | LLM / compiler | scheduler | explicit stop/fail behavior | exact draft order | empty/missing terminal behavior |
| `.stop_conditions[].when.*` | LLM aliases/values / compiler | stop predicate evaluator | stop/failure trigger | output predicates map as above; `input_unavailable` must name a required local input; `attempts_exhausted` requires `stop_node` or `fail_graph` | unresolved, optional-input or incoherent action |
| `.stop_conditions[].action` | LLM / compiler | scheduler | node/graph stop effect | exact closed enum | unsupported action |
| `.stop_conditions[].reason_code` | LLM / compiler | audit/scheduler | stable reason classification | exact draft key | missing/invalid code |
| `edges[]` membership/order | compiler derives data; LLM authors control/feedback / compiler | scheduler, projector, audit | communication/control topology | derived data pairs first; authored edges second | duplicate/undeclared/cyclic/impossible route |
| `edges[].edge_id` | compiler / compiler | scheduler/audit | edge identity | exact ID rules | collision |
| `.from_node_id`, `.to_node_id` | LLM dataflow/edge aliases / compiler | scheduler/dataflow | authorized route | aliases to derived node IDs | dangling endpoint |
| `.kind` | compiler for data; LLM for control/feedback / compiler | scheduler/projector | route semantics | data iff derived from input; otherwise exact authored closed value | duplicate mapping/unknown kind |
| `.condition` | fixed for data; LLM for control/feedback / compiler | scheduler | route activation | data=`on_success`; authored exact enum | unsupported/inconsistent condition |
| `lifecycle.entry_nodes[]` | LLM / compiler | scheduler, projector | graph roots | map exact ordered aliases | empty/dangling/non-root |
| `.terminal_nodes[]` | LLM / compiler | scheduler, projector | success frontier | map exact ordered aliases | empty/dangling/unreachable |
| `.completion` | LLM / compiler | scheduler, projector | graph success aggregation | exact closed enum | unsupported/impossible policy |
| `.failure` | LLM / compiler | scheduler, projector | branch failure behavior | exact closed enum | unsupported policy |
| `.cancellation` | LLM / compiler | scheduler | cancellation behavior | exact closed enum | unsupported policy |
| `.max_parallel_nodes` | LLM requests; policy may cap only if a ceiling is added / compiler | scheduler, projector | concurrency ceiling | current fixture copies exact request; no hidden default | invalid or unsupported policy restriction |
| `audit_requirements.record_objective` | policy / compiler | runtime audit validator | required evidence class | exact fixed policy boolean | missing/false under fixture policy |
| `.record_agents` | policy / compiler | runtime audit validator | required evidence class | exact fixed policy boolean | missing/false under fixture policy |
| `.record_route` | policy / compiler | runtime audit validator | required evidence class | exact fixed policy boolean | missing/false under fixture policy |
| `.record_results` | policy / compiler | runtime audit validator | required evidence class | exact fixed policy boolean | missing/false under fixture policy |
| `.receipt_schema_member_id` | policy selects resource / compiler | runtime receipt validator | receipt evidence contract | policy resource key to member ID | missing/invalid schema resource |

## Values deliberately outside the graph

These values still have producers and consumers, but including them in the pre-execution graph would
misstate their lifecycle.

| External value | Producer | Consumer | Why outside / failure rule |
|---|---|---|---|
| canonical graph bytes | canonicalizer | projector, confirmation writer, runtime parser | derived from complete EG; canonicalization failure emits no digest |
| `execution_graph_digest` | canonicalizer | views, observation, confirmation conflict check | self-digest cannot be a graph member; mismatch rejects |
| view bytes/kind/digest/projector ref | deterministic projector/catalog | trusted host, confirmation writer | presentation evidence, not execution choice; mismatched full digest rejects |
| principal/channel/time/action | trusted host adapter | confirmation writer/audit | does not exist before observation; untrusted observation rejects |
| accepted command/envelope IDs and journal position | confirmation writer/runtime | replay/audit | acceptance state; replay/conflict rules apply |
| run/group/attempt/message/effect IDs | runtime | scheduler/journal/audit | operational identity created after acceptance |
| status, receipts and results | runtime/agents/providers | reducers/audit/user | post-execution facts; cannot retroactively authorize work |

No runtime-owned value is accepted as an EG field, and the runtime consumes every executable EG
field listed above. Consequently there is no included field without a producer or consumer in this
proposal.

## Machine-checkable schema-leaf coverage

The following inventory is extracted from the current proposed ExecutionGraph schema. Every one of
its 105 leaf paths is classified by a row above; brace notation in the table is only compression.

```text
audit_requirements.receipt_schema_member_id
audit_requirements.record_agents
audit_requirements.record_objective
audit_requirements.record_results
audit_requirements.record_route
content_members[].content
content_members[].digest
content_members[].encoding
content_members[].immutable_uri
content_members[].kind
content_members[].media_type
content_members[].member_id
dispatch_id
edges[].condition
edges[].edge_id
edges[].from_node_id
edges[].kind
edges[].to_node_id
global_limits.max_attempts
global_limits.max_tokens
global_limits.wall_clock_seconds
lifecycle.cancellation
lifecycle.completion
lifecycle.entry_nodes[]
lifecycle.failure
lifecycle.max_parallel_nodes
lifecycle.terminal_nodes[]
nodes[].agent.credential_ref.contract_version
nodes[].agent.credential_ref.handle
nodes[].agent.credential_ref.resolver_ref.digest
nodes[].agent.credential_ref.resolver_ref.name
nodes[].agent.credential_ref.resolver_ref.version
nodes[].agent.credential_ref.scope_digest
nodes[].agent.display_name
nodes[].agent.model_ref.digest
nodes[].agent.model_ref.name
nodes[].agent.model_ref.version
nodes[].agent.profile_ref.digest
nodes[].agent.profile_ref.name
nodes[].agent.profile_ref.version
nodes[].agent.provider_ref.digest
nodes[].agent.provider_ref.name
nodes[].agent.provider_ref.version
nodes[].agent.role
nodes[].inputs[].input_id
nodes[].inputs[].required
nodes[].inputs[].source.kind
nodes[].inputs[].source.member_id
nodes[].inputs[].source.node_id
nodes[].inputs[].source.output_id
nodes[].inputs[].source.selector
nodes[].instructions
nodes[].isolation.commands.grants[].argv[]
nodes[].isolation.commands.grants[].command_ref.digest
nodes[].isolation.commands.grants[].command_ref.name
nodes[].isolation.commands.grants[].command_ref.version
nodes[].isolation.commands.grants[].cwd
nodes[].isolation.commands.grants[].environment_member_id
nodes[].isolation.commands.mode
nodes[].isolation.external_effects.allow[]
nodes[].isolation.external_effects.mode
nodes[].isolation.network.allow[]
nodes[].isolation.network.mode
nodes[].isolation.read_paths[]
nodes[].isolation.version_control.commit
nodes[].isolation.version_control.push
nodes[].isolation.write_paths[]
nodes[].limits.max_attempts
nodes[].limits.max_tokens
nodes[].limits.wall_clock_seconds
nodes[].node_id
nodes[].objective
nodes[].outputs[].output_id
nodes[].outputs[].required
nodes[].outputs[].schema_member_id
nodes[].start_when
nodes[].stop_conditions[].action
nodes[].stop_conditions[].reason_code
nodes[].stop_conditions[].when.input_id
nodes[].stop_conditions[].when.json_pointer
nodes[].stop_conditions[].when.kind
nodes[].stop_conditions[].when.output_id
nodes[].stop_conditions[].when.value
nodes[].success_condition.input_id
nodes[].success_condition.json_pointer
nodes[].success_condition.kind
nodes[].success_condition.output_id
nodes[].success_condition.value
nodes[].tools[].allowed_operations[]
nodes[].tools[].tool_ref.digest
nodes[].tools[].tool_ref.name
nodes[].tools[].tool_ref.version
nodes[].validation[].configuration_member_id
nodes[].validation[].on_fail
nodes[].validation[].rule_id
nodes[].validation[].validator_ref.digest
nodes[].validation[].validator_ref.name
nodes[].validation[].validator_ref.version
objective.done_when[]
objective.statement
revision
schema
semantics_ref.digest
semantics_ref.name
semantics_ref.version
```
