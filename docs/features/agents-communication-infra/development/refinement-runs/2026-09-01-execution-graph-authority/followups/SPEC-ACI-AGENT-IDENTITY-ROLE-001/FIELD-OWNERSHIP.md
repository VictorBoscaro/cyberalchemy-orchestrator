# Field ownership and consumer status

Status: proposed correction to the consumer claims in `SPEC-ACI-DRAFT-GRAPH-001/FIELD-OWNERSHIP.md`.
The earlier 105/105 result means only that schema leaves were classified. It does not prove 105
implemented runtime consumers. Historical `KEEP` reviews remain intact and are superseded only for
the identity/role and consumer-status claims listed here.

Consumer status vocabulary:

- `implemented`: a current production component reads the value for the stated behavior;
- `compiler-only`: the current pure compiler reads or derives it, but no downstream runtime does;
- `projected`: a specific downstream consumer is designed or named but not implemented;
- `missing`: no justified consumer is currently identified; retain only with a new decision.

## Identity and role fields

| Field | Sole producer | Current consumer | Status | Required code change |
|---|---|---|---|---|
| source YAML `agent_name` | governed canonical v0.7 pool | proposed pool loader | projected | atomically migrate real v0.6 `name`; implement strict two-document loader |
| normalized pool `agents[].display_name` | loader | proposed allocator and compiler | projected | implement digest verification and lookup |
| normalized pool `agents[].role_fit[]` | loader | proposed allocator/compiler fit check | projected | implement explicit override semantics |
| registry `roles[].role_id` | governed immutable registry | proposed compiler/registrar/MCP/UI/audit | projected | implement shared pinned resolver; remove seven-role constants |
| pool `role_fit[]` role ID | governed canonical pool | loader against selected registry | projected | keep source schema structural; reject IDs absent from pinned registry |
| `DG.nodes[].agent_request.role` | LLM from intent | current compiler policy tuple check | compiler-only | switch fixtures to canonical registry roles |
| `X.agent_assignments[].node_key` | allocator | proposed compiler | projected | exact node coverage check |
| `X.agent_assignments[].display_name` | allocator from normalized pool | proposed compiler | projected | emit final display name from assignment |
| `X.agent_assignments[].role_fit_override` | allocator | proposed compiler | projected | reject silent mismatch |
| `X.agent_assignments[].role_fit_override_reason` | allocator | proposed compiler/report | projected | require iff override is true |
| `EG.nodes[].agent.display_name` | compiler from signed assignment | future projector/audit/launcher | projected | current compiler incorrectly copies draft text |
| `EG.nodes[].agent.role` | compiler from admitted draft role | future projector/audit/launcher | projected | current compiler emits it; no runtime ingestion exists |
| new opening `agent_role_registry_ref` | pinned role resolver | appender, workflow/host hook, strict snapshot resolver | projected | required on telemetry opening schema `0.7.0`; absent on immutable legacy rows |
| new close `agent_role_registry_ref` | appender from matched opening | appender, bridge and strict snapshot resolver | projected | require exact opening ref and schema `0.7.0`; reject mixed pair |
| installer/package selection | current hard-coded v1 path; future operator default or explicit legacy flag | runtime installer and route-strategy instructions | implemented | make v2 the only default new-write line; retain explicit v1 verification |
| confirmation `appender_contract_version` | current confirmation producer; future selected package authority | audit-opening effect/request consumer | implemented | remove 0.6.4 literal; emit selected 0.7.0 plus the same role-registry ref |

## Every author-facing `key` and its consumer

| Draft key | Consumer | Status | Why it exists |
|---|---|---|---|
| `resources[].alias` | current compiler references/member ID derivation | compiler-only | local resource reference namespace |
| `resources[].resource_key` | current compiler resource lookup | compiler-only | selects exact external resource record |
| `nodes[].key` | current compiler node refs/IDs/dataflow | compiler-only | stable local node reference |
| `capability_requests[].capability_key` | current compiler catalog/policy lookup | compiler-only | selects exact capability grant |
| `inputs[].key` | current compiler local refs/input IDs/predicates | compiler-only | stable node-local input reference |
| `outputs[].key` | current compiler local refs/output IDs/dataflow/predicates | compiler-only | stable node-local output reference |
| `validation[].key` | current compiler rule ID derivation | compiler-only | stable node-local validation identity; downstream audit use projected |
| `validation[].validator_key` | current compiler validator lookup | compiler-only | selects exact validator ref |
| `edges[].key` | current compiler authored edge ID derivation | compiler-only | stable authored control/feedback identity; scheduler use projected |
| `provider_key` / `model_key` / `profile_key` / `credential_key` | current compiler catalog/policy lookup | compiler-only | selects exact binding records |
| `lifecycle.*_node_keys[]` | current compiler node lookup | compiler-only | selects roots and terminals |
| predicate `input_key` / `output_key` | current compiler local lookup | compiler-only | binds closed predicates to local ports |
| source `node_key` / `output_key` | current compiler dataflow lookup | compiler-only | binds a consumer input to one producer output |

There is no accepted arbitrary key. Every accepted key above is read by the compiler. This does not
mean its derived EG ID has an implemented runtime consumer.

## ExecutionGraph consumer groups

| EG field group | Producer | Existing downstream consumer | Status |
|---|---|---|---|
| `schema`, `dispatch_id`, `revision` | compiler/system context | proposed v2 parser/confirmation/journal | projected |
| objective and `done_when` | compiler from draft | proposed views/agents/audit | projected |
| semantics/content/global limits | compiler | proposed parser/content loader/scheduler | projected |
| node IDs, prompts and agent binding | compiler | proposed scheduler/launcher/projector/audit | projected |
| tools and isolation | compiler | proposed guards/launcher/projector | projected |
| inputs/outputs | compiler | proposed dataflow/materializer/validators | projected |
| validation/success/stop conditions | compiler | proposed validator/predicate/scheduler | projected |
| edges and lifecycle | compiler | proposed scheduler/projector | projected |
| audit requirements | compiler from policy | proposed audit/receipt validators | projected |
| prohibited command-grant branch | compiler enforces absence | conformance checks only | compiler-only |

Current production runtime ingestion of `aci.execution-graph@2` is absent. Therefore this follow-up
makes no `implemented` downstream-runtime claim and no 105/105 consumer claim. The implementation
worker must preserve this ceiling until code and tests prove otherwise.
