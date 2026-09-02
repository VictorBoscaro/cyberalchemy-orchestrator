# Strict context pack

## Objective

Determine whether the selected single canonical `ExecutionGraph` JSON is a coherent
pre-execution authority, then define the smallest contract that preserves that choice without
absorbing confirmation evidence or post-confirmation runtime state.

## Fixed owner decisions

1. The agent compiles the technical dispatch from the user's intent.
2. One canonical JSON contains every value that may change what is executed.
3. Topology, basic and full are deterministic presentations of that same JSON.
4. Confirmation binds the digest of the complete JSON; a material change creates a new revision
   and requires confirmation again.

These are product decisions. This run may report an internal contradiction, but may not replace
them silently.

## Local evidence and what it proves

| Evidence | Selected surface | Supported claim |
|---|---|---|
| `.craft/ledger.yml` | `DEC-ACI-CANONICAL-EXECUTION-GRAPH-001`, `DEF-...`, `GAP-...` | The owner selected agent compilation, one complete authority and full-digest confirmation; the v2 contract remains unspecified. |
| `specs/confirmation-authority.md` | ownership, canonical bytes, digest taxonomy, bounded projection, success ceiling | CONF v1 already distinguishes editable input, compiled executable contract, trusted confirmation observation and runtime-created records. |
| `pending-sheet.json` | complete document | V1's editable source contains topology, requirements, refs and budgets, but not resolved capabilities or exact prompt bytes. |
| `capability-resolution.json` | complete document | V1 resolution freezes adapter/model/tool-profile refs separately from the pending sheet. |
| `dispatch-spec.json` | complete document | V1's closest executable logical authority combines the graph, resolved capabilities, policy refs, prompt refs and budgets. |
| `confirmed-turn-graph.json` | complete document | V1 derives runtime IDs, source-message identities and continuation bindings after compiling the logical spec. |
| `confirmation-observation.json` and `confirmed-authority.json` | top-level contract and digest bindings | Human identity/channel/time and accepted authority evidence are not user-authored plan values. |
| `confirmation.py` | `project_dispatch_spec`, `build_confirmation_batch` | Current runtime deterministically compiles the spec and derives confirmed graph/evidence; it does not ingest a v2 graph. |
| `service.py` | `confirm_runtime_dispatch` | Acceptance authenticates host context, retrieves finalized capability evidence, builds the batch and persists it atomically. |

## Authority test

A field belongs in `ExecutionGraph v2` if changing it before execution can change allowed work,
agent behavior, information flow, resource consumption, effects, or stopping behavior. A field
does not belong merely because it is needed to prove, persist or observe what happened after the
user confirmed.

This yields the initial boundary:

- In graph authority: objective, exact instructions, selected context, topology, dependencies,
  provider/model/tool grants, budgets, filesystem/network/command/effect policy, output contract,
  validation and stop rules.
- Outside graph authority: authenticated principal, confirmation channel/time, observation ID,
  accepted command ID, journal offsets, derived run/attempt/message IDs, claims, receipts, results,
  effect outcomes and current status.
- Digest-bound references are permitted only when their bytes are immutable and retrievable. If
  exact content is necessary to interpret execution and cannot be guaranteed by the reference,
  the content must be embedded in the graph.

## Compatibility constraint

CONF v1 is immutable historical evidence. V2 may replace the pending-sheet + resolution +
DispatchSpec chain as the user-confirmed authority, but must define an explicit adapter/projection
for any reused v1 acceptance machinery. It cannot relabel existing v1 fixture bytes as v2.

## Excluded from this run

- Runtime implementation, migrations or production provider calls.
- Changes to the feature spec, fixtures or ledger.
- External research; no local evidence gap currently requires it.
- A generalized orchestration language beyond the review/correct/verify proving example.

## Handoff

Define the contract around a single immutable `aci.execution-graph@2` document. Treat human-facing
views as projections and confirmation/operation as separate records that cite its digest. Preserve
one explicit residue: whether prompts and context are embedded bytes or digest-pinned content
members must be decided by the contract, not hidden behind implementation convenience.
