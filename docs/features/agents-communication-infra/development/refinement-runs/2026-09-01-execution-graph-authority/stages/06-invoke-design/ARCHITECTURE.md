# ExecutionGraph v2 architecture proposal

## Decision

Keep one canonical JSON. Narrow its claim to the **sole proposed logical execution authority**.
`aci.execution-graph@2` replaces the logical value ownership currently split among pending sheet,
capability resolution and DispatchSpec. Trusted confirmation evidence and runtime state remain
separate records bound to its externally calculated digest.

The JSON is what the compiler sends as the plan to the runtime. The confirmation call also carries
host-issued evidence that the user approved that plan; this evidence cannot be precompiled into the
plan because it does not exist before approval.

## View 1 — System context

`User intent → compiler/resolver → ExecutionGraph bytes → projector → user confirmation → trusted
observation → ConfirmRuntimeDispatch@2 → runtime state/effects`.

Only the compiler writes logical authority values. Projector, confirmation adapter and runtime may
reject or derive evidence/state, but may not fill an omitted executable default.

## View 2 — Contract components

The proposed closed shape is in `execution-graph-v2.proposed.schema.json`.

| Component | Purpose |
|---|---|
| identity/objective | Stable logical dispatch revision and intended outcome |
| semantics | Digest-pinned evaluator contract; no implicit scheduling semantics |
| content members | Inline exact content or immutable digest-pinned external bytes |
| nodes | Instructions, agent identity/grants, inputs/outputs, limits, isolation, validation and stop rules |
| edges | Allowed control/data/feedback flow and exact output→input mappings |
| lifecycle/global limits | Roots, terminal success, failure/cancellation and total resource ceilings |
| audit requirements | What execution must evidence; actual evidence remains outside |

`dispatch_id` is the logical identity. There is deliberately no self-referential `graph_digest` and
no CONF v1 runtime `graph_id` inside the document.

## View 3 — Authority and evidence

| Namespace | Owner | Contents |
|---|---|---|
| `aci.execution-graph@2` | compiler, then immutable | Every proposed executable choice |
| calculated graph identity | canonicalizer | canonical bytes + `execution_graph_digest` |
| presentation evidence | projector/host | view kind, projector ref, exact view bytes/digest |
| confirmation observation | trusted host adapter | principal, channel, time, action and graph/view bindings |
| accepted authority envelope | confirmation writer | graph/observation/contract digests and schema map |
| operational state | runtime/journal | run/node/attempt/message/effect IDs, status, receipts and results |

An accepted confirmation activates but does not modify the graph. `(dispatch_id, revision)` must
map to exactly one graph digest. A different digest under the same pair is a permanent conflict.

## View 4 — Presentation projections

Projection rules are normative in `aci.execution-graph-projector@2`, not selected fields inside a
graph revision.

| View | Deterministic disclosure |
|---|---|
| topology | dispatch/revision/full digest; ordered node IDs, names and roles; ordered typed edges and join/control flow |
| basic | topology + graph objective; each node's objective, provider/model/profile; limits; filesystem/network/command/effect summary; completion/failure policy |
| full | lossless canonical graph value plus dispatch/revision/full digest envelope |

The user's depth choice changes presentation evidence only. Every view names the same full graph
digest. Chat prose may format a projection, but the exact projected JSON bytes are retained and
digested; a language model may not invent the projection.

## View 5 — Confirmation and execution sequence

1. Compiler emits closed graph bytes with all effective grants resolved.
2. Validator rejects unknown/missing fields, semantic inconsistencies and unresolved defaults.
3. Canonicalizer emits `aci-cjson-1` bytes and calculates `execution_graph_digest`.
4. Projector deterministically emits the selected view and its digest.
5. Trusted host adapter observes approval and binds principal/channel/time, dispatch/revision,
   graph digest, view kind/projector ref and presented-view digest.
6. `ConfirmRuntimeDispatch@2` verifies graph, content members, resolver evidence, observation and
   replay key; it persists an accepted authority envelope atomically.
7. Runtime derives operational IDs and schedules only values present in the accepted graph.

## View 6 — Compatibility and deployment

- CONF v1 remains immutable and continues to accept only its v1 documents.
- A new `@2` operation consumes graph bytes; it must not translate the v2 digest into v1
  `pending_sheet_digest` or `dispatch_spec_digest`.
- Reuse is allowed below the authority boundary: canonicalization utilities, trusted issuer
  validation, single-writer transaction, replay/conflict rules and runtime materializers.
- A compatibility projector may derive an internal v1-shaped execution structure only after v2
  acceptance. It is a runtime projection, never a second confirmed authority.
- Cutover requires golden v2 graph/view/observation/envelope fixtures, negative vectors and
  independent spec review before parser, service or database changes.

## Content and secret rules

- Exact prompts are inline strings in the owning node.
- File/context/schema/policy bytes use `content_members`: either inline content with digest or an
  immutable URI plus digest. Acceptance verifies them; read-time drift fails closed.
- Credentials are never content members. A node authorizes a versioned credential handle and exact
  scope digest. Secret-value rotation is operational only if identity and privilege scope are
  unchanged; privilege expansion requires graph revision and reconfirmation.

## Material change

The objective rule is conservative: any change to canonical `aci.execution-graph@2` bytes is a new
authority revision and requires confirmation. Availability changes, attempts, results and other
external facts do not mutate the graph; they may block or fail execution.

## Status

Proposed and internally designed only. Not accepted, implemented or executable.
