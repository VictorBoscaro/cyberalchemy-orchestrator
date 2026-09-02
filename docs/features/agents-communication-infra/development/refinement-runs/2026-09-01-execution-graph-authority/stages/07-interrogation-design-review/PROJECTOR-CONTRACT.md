# Proposed projector contract

The projector consumes validated canonical `aci.execution-graph@2` bytes and the externally
calculated full digest. It never calls a model, capability resolver or environment discovery.
Object keys use `aci-cjson-1`; source array order is preserved.

## Topology

Copy `dispatch_id`, `revision`, ordered `nodes[].{node_id,agent.display_name,agent.role}`, complete
ordered `edges[]`, and
`lifecycle.{entry_nodes,terminal_nodes,completion,failure,max_parallel_nodes}`. Rename only the two
agent fields into the node projection. Add the full graph digest and fixed projector reference in
the view envelope.

## Basic

Copy everything in topology plus `objective`, `global_limits`, each node's `objective`, complete
provider/model/profile refs, `limits`, and the exact isolation disclosure:
read/write paths, each policy mode, and commit/push booleans. Copy the complete lifecycle. No prose
summary is generated.

## Full

Identity projection: the view payload is the complete parsed graph value and its canonical payload
bytes equal the canonical graph bytes. The golden full payload is therefore
`review-correct-verify-toy-graph.json`; an envelope may add the full digest and projector metadata
outside the payload.

All three views bind
`sha256:4a38e63293f630930cb624830433dea147bdb018f3ceb7eef949dafe052cd275`.
The placeholder projector digest marks this as a proposal, not an accepted golden fixture.
