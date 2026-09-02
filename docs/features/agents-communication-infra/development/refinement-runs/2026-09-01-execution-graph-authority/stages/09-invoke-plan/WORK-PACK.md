# Work pack — SPEC-ACI-EXECUTION-GRAPH-V2-001

## Work unit

- ID: `SPEC-ACI-EXECUTION-GRAPH-V2-001`
- Kind: specification and conformance design
- Goal: close `GAP-ACI-CANONICAL-GRAPH-CONTRACT-001` at the contract level.
- Code authority: none.
- Owner: runtime architecture, with repository-owner confirmation of any product-policy change.

## Inputs

- `DEC-ACI-CANONICAL-EXECUTION-GRAPH-001` and
  `DEF-ACI-CANONICAL-EXECUTION-GRAPH-001`.
- `specs/confirmation-authority.md` and its complete CONF v1 fixture package.
- This refine run's definition, selected boundary, proposed schema, toy graph, projector contract
  and validation.

## Required outputs

1. Normative v2 specification with closed field tables and formal rules.
2. Closed graph/view/observation/command/accepted-envelope schema artifacts.
3. Semantic validator contract beyond JSON Schema.
4. Real golden graph plus topology/basic/full vectors and exact canonical digests.
5. Negative vector set and expected typed failures/postconditions.
6. CONF v1 coexistence/cutover map and `@2` ingestion contract.
7. Independent review receipt and ledger update reflecting specified—not implemented—status.

## Acceptance criteria

- Every value capable of changing work, information flow, grants, resources, effects or stopping is
  inside the graph or in an immutable digest-pinned content member.
- No field created by confirmation/execution is accepted as a graph member.
- Every executable string is either exact model instruction or interpreted under a digest-pinned,
  closed contract; runtime control never depends on ad hoc prose.
- Graph validation covers uniqueness, reference integrity, topology, reachability, lifecycle,
  budgets, content digests, validator/tool/command refs and credential scope.
- Topology/basic/full are reproduced without model inference and bind one full digest.
- Basic discloses objective, agent/model, limits, writable scope, network/commands/effects and
  completion/failure policy.
- Any canonical graph-byte mutation requires revision + confirmation; presentation choice alone
  does not.
- V2 does not reuse v1 digest fields for different bytes or weaken trusted observation, replay,
  conflict or atomicity.

## Negative cases

- Missing prompt/model/tool/policy/limit/stop rule.
- Unknown object key, duplicate key/ID or dangling node/output/member reference.
- Unreachable node, undeclared communication path, impossible join or resource total violation.
- Mutable/ref-drifted content, schema, provider, model, tool, validator or credential scope.
- Free-text command/predicate/validator resolution.
- Topology/basic view referring to a different full digest.
- Confirmation observation referring to a stale revision/view/projector.
- Same `(dispatch_id, revision)` with different graph digest.
- Attempt to embed principal/time/run/status/receipt/result in the graph.
- V2 bytes relabeled as any CONF v1 document.

## Execution sequence

1. Promote/refine the proposed contract into the target v2 spec.
2. Write golden/negative vectors and deterministic reproduction checks.
3. Run independent contract and fixture review; repair until PASS.
4. Update Craft to mark the contract gap specified/closed at its exact ceiling.
5. Create a separate code-entry work unit for L2; do not begin L2 implicitly.

## Stop conditions

- A product choice would change one authority, agent compilation or three-view semantics.
- A required field cannot be classified as authority, evidence or state.
- The projector cannot be specified without nondeterministic summarization.
- V1 coexistence requires digest aliasing or retroactive fixture mutation.
- Independent review reports a surviving blocker.

## Verification commands for the future work unit

- JSON/meta-schema and semantic-validator checks over every fixture.
- Canonical-byte/digest reproduction from clean checkout.
- Golden projector comparison for all views.
- Negative-vector runner with exact typed results and zero-mutation postconditions where applicable.
- Existing CONF/runtime regression suite selected by the accepted spec work pack.

## Non-goals

- Runtime parser/service/database changes.
- Provider or tool calls.
- OPEN, scheduling or external effects.
- Deleting or rewriting CONF v1.
