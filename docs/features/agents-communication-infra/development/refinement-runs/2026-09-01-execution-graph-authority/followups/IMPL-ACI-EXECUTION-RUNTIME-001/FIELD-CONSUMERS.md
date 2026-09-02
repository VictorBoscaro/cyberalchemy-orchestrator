# Local execution field consumers

Status: second repair-forward worker traceability evidence. Initial `FIX`
`569559E51B0E06CFE4C81576D8E455F9534F26D702F1D880EB16B88F03F8AEBD` and recheck-1 `FIX`
`33D6870F1675E85AB93F6542A9206E013037C6680A5B7D2E56A572D0E3193C0C`; same-reviewer recheck pending. All objects below are local-only
execution evidence, not `ConfirmRuntimeDispatch@2` authority.

| Field or field group | Producer | Enforcing consumer | Durable use |
|---|---|---|---|
| compilation candidate graph bytes/digest | reviewed compiler over the nine exact JSON inputs | `admit_execution_graph`, durable verifier and independently accepted graph digest | candidate identity only; never self-authorizes execution |
| compilation authority `schema`, ceiling, dispatch/revision/allocation/graph/report/input digests and prior digest | `compile_candidate` from verified allocator context and compiler result | closed authority validator, independent acceptance binding, durable verifier and lineage transaction | preserves compiler/allocator evidence without treating it as acceptance |
| acceptance exact canonical bytes plus `schema`, ceiling, `decision`, issuer ref/evidence, principal, dispatch/revision/allocation/graph and compilation-authority digest | pinned local fixture acceptance | configured issuer/evidence and exact acceptance-digest allowlist, acceptance validator and durable verifier | byte-authenticated local/test execution authorization; any field drift rejects; explicitly not a signature or `ConfirmRuntimeDispatch@2` |
| fixture manifest nine input paths/digests, issuer evidence/trust artifacts, canonical acceptance bytes/digest and expected candidate digests | persisted local-execution fixture bundle | focused manifest loader and E2E assertions before compilation/admission | proves the successful test uses exact persisted bytes without semantic rewrite |
| admission bundle graph, compilation-authority and acceptance digests | `admit_execution_graph` after all three exact canonical documents validate | durable verifier before snapshot, scheduling, adapter launch and result reduction | detects graph or authority byte drift on reopen/use |
| `admission_id`, `run_id` | closed digest preimages | table PK/FK joins and snapshot API | deterministic local operational identity |
| run `status`, `cancel_requested`, `terminal_reason`, `next_receipt_sequence` | state machine/cancel boundary | scheduler, idempotent cancel, durable verifier and receipt writer | deterministic resumption, cancellation and audit order |
| graph lifecycle `cancellation` | compiler/policy | local-subset admission gate and cancel reducer | only `cancel_running_nodes` is admitted; `allow_running_nodes_to_stop` fails closed |
| node `node_id`, `node_ordinal`, `max_attempts` | accepted graph and graph array order | scheduler/input resolver/retry fence | stable selection and bounded attempts |
| node `display_name`, `role` | compiler-emitted signed assignment projection | worker assignment and receipts/snapshot | preserves identity and responsibility through launch evidence |
| node `status`, `attempts`, `output_json`, `output_digest`, `terminal_reason` | state machine and accepted worker result | dependency resolver, completion/failure reducer and snapshot | durable node head and exact downstream input |
| worker assignment `graph_digest`, node/attempt identity, agent, tools, objective, instructions, inputs | graph plus persisted run state | `ScriptedLocalAdapter` and attempt evidence reader | exact fake-worker launch input; tools are described but never invoked by this adapter |
| worker result `outputs` | scripted local adapter | output-contract validator, predicate evaluator and downstream resolver | candidate output bytes and node-output handoff |
| worker result `validations` | scripted local adapter | exact rule-coverage and `on_fail` reducer | deterministic fake validation outcomes; does **not** prove execution of the pinned external validator |
| attempt `status`, assignment/result JSON and digests, `failure_code` | launch/result reducer | durable verifier, recovery, retry reducer and snapshot | reconstructible attempt history; byte/digest drift blocks adapter or presentation |
| graph `audit_requirements.record_*` | compiler/policy | local-subset gate and deterministic receipt audit projector | requires exact objective, agent, route and result evidence in this local subset |
| graph `audit_requirements.receipt_schema_member_id` | compiler/policy | pinned member resolver and JSON Schema validator before every receipt insert and on every reopen/snapshot | graph-authorized receipt contract; missing/incompatible/tampered members fail closed |
| receipt `sequence`, `kind`, graph/node/attempt refs, canonical `payload_json`, exact audit JSON strings and `receipt_digest` | transaction-local receipt writer | pinned schema validator, durable verifier, ordered snapshot consumer and uniqueness constraints | deterministic graph-pinned evidence without timestamps |
| workflow manifest slot `name`, schema, cardinality, max bytes, purpose, ordered sources | validated sequential handoff receipt | host workflow manifest consumer | closes the pre-existing empty-slot gap without changing source bytes |
| launch plan `handoffs` | exact validated `aci-workflow-sequential-handoff/v1` documents | host/diagnostic plan reader and bootstrap assertions | exposes which receipt authorized each materialized slot |

No principal, confirmation time, provider response, tool result, credential, network action, VCS
action or external-effect receipt is created. There is no orphan field in the local migration or
the candidate/acceptance/admission/assignment/result/receipt shapes. SQLite-only `authority_json`,
`graph_bytes`, assignment, result, output and receipt bytes are revalidated with their digests and
graph heads before scheduling, adapter launch, result reduction or snapshot presentation.
