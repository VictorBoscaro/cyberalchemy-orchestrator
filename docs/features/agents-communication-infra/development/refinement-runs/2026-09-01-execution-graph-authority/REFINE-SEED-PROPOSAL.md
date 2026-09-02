# Refine seed — canonical ExecutionGraph authority

## Target

Refine the owner-selected decision that one agent-compiled canonical JSON carries the complete
pre-execution graph authority for ACI, while topology, basic and full chat presentations remain
views of the same authority.

## Source context

- `.craft/ledger.yml`: `DEC-ACI-CANONICAL-EXECUTION-GRAPH-001`,
  `DEF-ACI-CANONICAL-EXECUTION-GRAPH-001` and
  `GAP-ACI-CANONICAL-GRAPH-CONTRACT-001`.
- `specs/confirmation-authority.md`: frozen CONF v1 authority and digest boundaries.
- `specs/fixtures/confirmed-dispatch-v1/`: pending sheet, capability resolution, DispatchSpec,
  confirmed turn graph, mappings and authority fixture.
- `implementations/server/runtime/confirmation.py` and `service.py`: current v1 projection and
  acceptance surfaces.

## Refinement question

Is one complete canonical pre-execution JSON the best authority boundary, and what exact schema,
projection, confirmation and runtime-derived boundaries make that decision coherent without
collapsing post-confirmation evidence or operational state into the user-authored plan?

## Fixed owner decisions

1. The agent compiles the graph from user intent; the user does not fill technical fields.
2. There is one canonical pre-execution authority JSON.
3. Topology, basic and full are presentations of that same authority, not different authorities.
4. Confirmation binds the complete canonical digest; material change requires reconfirmation.

The refine run may challenge whether the boundary is internally coherent, but it may not silently
replace these decisions. A surviving blocker must be returned to the owner explicitly.

## Desired outcome

A reviewed, non-executed definition/design/plan package that:

- states whether the single-JSON decision should be kept, narrowed or returned to the owner;
- defines the minimum complete `ExecutionGraph v2` contract;
- separates pre-confirmation authority from confirmation evidence and post-confirmation facts;
- defines deterministic topology/basic/full projections;
- identifies CONF v1 compatibility and migration obligations;
- ends with bounded specification work, fixtures, validation and implementation sequencing.

## Write scope

Only this refinement-run folder during the refine loop. Existing feature specs, fixtures, ledger
and runtime code remain read-only. Any proposed mutation is emitted as a non-executed plan.

## Done criteria

- All ten canonical Refine stages have an artifact or explicit blocked reason.
- Competing boundary interpretations are preserved through critique and then resolved or recorded
  as owner residue.
- A toy `review -> correct -> verify` graph tests completeness, projection stability and
  reconfirmation behavior.
- Final output distinguishes specified, proposed, validated and implemented claims.
- No runtime code, migration, CONF v1 fixture or canonical feature spec is mutated.

## Validation surface

- Dispatch Spec schema and deterministic validator.
- Literal comparison against CONF v1 documents and current runtime inputs.
- Internal consistency of schema ownership, canonical bytes, digest and presentation projections.
- Negative cases for hidden-field drift, post-confirmation facts, graph mutation and replay.

## Configuration

- Preset: `standard`.
- Research: `research-if-gap-appears`, local-first; any external research requires a new explicit
  confirmation.
- Subagents: recommended, two read-only dialectic roles, only after operator permission.
- Next route after synthesis: specification authoring or deferred owner decision; never code
  execution inside this refine run.

