# Definition dialectic review

## Joined verdict

`FLAG`, with promotion to specification blocked until repair. Both independent roles agree that one
canonical JSON is coherent **as the complete proposed logical authority**. It is not the sole input
to confirmation or execution: trusted confirmation evidence and runtime-created state must remain
outside and cite its digest.

The runtime-boundary `BLOCK` is treated as a required design repair, not an owner-decision blocker.
The fixed decision already determines the answer: v2 replaces the split logical authority
(`pending + resolution + DispatchSpec`) with one graph; it does not erase the separately versioned
trust, replay and atomic-acceptance boundary.

## Agreements

- The graph contains resolved effective choices, not requirements that the runtime may satisfy
  differently later.
- `graph_digest` is calculated over the canonical document and cannot be a field inside those same
  bytes.
- A logical `dispatch_id` and `revision` may be fields; CONF v1's derived `graph_id`, run IDs,
  continuation IDs and message IDs are runtime state.
- Validation rules belong to authority; validation executions/results belong to evidence.
- Prompts, context and policy content are inline or immutable/retrievable/digest-pinned.
- Any canonical authority-byte change is material and requires a new revision and confirmation.
- Projection is deterministic and versioned; rendered bytes and display evidence are not graph
  fields.
- V2 needs its own acceptance envelope/operation. It must preserve CONF v1 trust, replay and atomic
  persistence semantics without aliasing v1 digests.

## Repairs required before design can pass

1. Replace “the runtime input contract” with “the sole proposed logical authority input.”
2. Define closed types/cardinalities, normative topology semantics and exact capability/policy
   structures.
3. Separate logical IDs, calculated digest, confirmation evidence and operational IDs.
4. Define topology/basic/full disclosure tables and projector versioning outside each graph
   revision but bound by `schema`/contract.
5. Define a v2 confirmation adapter and digest lineage; never map the v2 digest into both v1 digest
   fields.
6. Specify secret-reference versioning and deny privilege-expanding drift.

## Dispositions of disagreements

- **Raw user request:** included only when it is an exact instruction consumed by a node; otherwise
  compilation provenance is evidence outside the graph.
- **Names/roles:** labels are permitted but only instructions, routing and policies are
  authority-bearing. Changing a display-only label still changes canonical bytes in v2 and thus
  conservatively requires reconfirmation.
- **Self-contained versus referenced content:** the authority is one JSON, but a content member may
  be inline or an immutable digest-pinned reference. References are dependencies, not competing
  authority documents.
- **Presentation policy placement:** normative projector/disclosure rules live in the versioned
  v2 contract. The graph contains no view mode; the user's selected mode belongs to presentation
  evidence.

## Risks retained

1. A shallow view may be formally linked but insufficiently informative; basic disclosure must
   include grants, limits, effects and stop behavior.
2. Mutable references/defaults can create hidden authority; resolution drift must fail closed.
3. A compatibility adapter can accidentally preserve multiple authorities; only the v2 graph may
   supply logical execution values to an `@2` acceptance operation.

## Role receipts

### Single-authority advocate

- Agent: `/root/single_authority_advocate`
- Status: `flag`
- Join: `completed`
- Validation: read-only completeness/consistency review over the context, definition, ledger and
  CONF v1 contract.
- Main residue: closed field/semantic contract, immutable content-member rule, secret drift.
- Reroute: revise definition, then design and review.

### Runtime-boundary skeptic

- Agent: `/root/runtime_boundary_skeptic`
- Status: `block` for promotion of the current definition, not for continuing the refinement.
- Join: `completed`
- Validation: read-only boundary check against `project_dispatch_spec`,
  `build_confirmation_batch`, `confirm_runtime_dispatch` and CONF-R2.
- Main residue: explicit `@2` acceptance adapter and logical/runtime identity separation.
- Reroute: repair in the design stage.
