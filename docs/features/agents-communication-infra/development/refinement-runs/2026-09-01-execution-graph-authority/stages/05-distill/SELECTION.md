# Distill — coherent authority unit

## Selection question

What is the smallest unit that preserves one user-confirmed JSON, prevents hidden executable
defaults and maintains a truthful confirmation/runtime boundary?

## Tournament

| Candidate | Authority integrity | User comprehension | Determinism | Runtime feasibility | CONF v1 migration | Verdict |
|---|---|---|---|---|---|---|
| A. Monolithic lifecycle JSON: graph + observation + run state + receipts | Low: mixes proposal with facts that do not exist yet | Low | Low: document mutates during execution | Low | Low | Reject |
| B. One canonical authority JSON with resolved values and inline or digest-pinned content members; evidence/state outside | High | High through fixed projections | High | High with `@2` adapter | Medium/high | **Select** |
| C. Thin logical graph plus separate capability/DispatchSpec authority resolved later | Low: hidden or competing authority | Medium | Medium | High reuse | High | Reject |

Candidate B Pareto-dominates A and C on authority integrity and comprehension without losing
runtime feasibility. Its price is a new closed contract and explicit acceptance adapter.

## Smallest coherent unit

The SCU is one immutable `aci.execution-graph@2` document containing:

- logical dispatch identity and revision;
- objective and exact executable instructions;
- ordered nodes and typed edges with input/output mappings;
- exact effective provider/model/tool grants;
- selected context/content members, inline or digest-pinned;
- budgets, sandbox/network/command/effect constraints;
- output/validation, failure and stop semantics; and
- a digest-pinned execution-semantics contract reference.

The calculated graph digest, rendered views, confirmation observation, accepted-authority envelope
and all run state are neighboring evidence/state, not members of the SCU.

## Recomposition proof

1. The compiler emits the SCU from user intent and resolved local capabilities.
2. The canonicalizer validates closed shape and calculates `execution_graph_digest`.
3. A versioned projector renders topology/basic/full from the same bytes and labels the view with
   the external digest.
4. A trusted adapter records what principal saw/approved, including graph identity/revision,
   digest, view kind/projector version and displayed-view digest.
5. `ConfirmRuntimeDispatch@2` accepts graph bytes + trusted observation + pinned contract evidence,
   then derives runtime IDs and persists state atomically.

No step supplies a second source for an executable value. Replacing the graph, a content member or
an effective grant changes authority and requires reconfirmation.

## Role trace

- Proposer: candidate B, because it directly implements the owner-selected single authority.
- Balancer: retained external evidence/state and digest-pinned dependencies to avoid false
  self-containment.
- Tournament: candidates A/B/C compared against five explicit criteria.
- Pareto gate: B survives; A and C each lose an essential invariant.

## Pre-mortem

- If this fails, likely cause 1 is a mutable context/tool reference. Prevention: verify every
  digest-pinned member before acceptance and every read; drift fails closed.
- Cause 2 is a reassuring but insufficient basic view. Prevention: make its disclosure table
  normative and test it against the full graph.
- Cause 3 is an adapter that still trusts v1 pending/spec inputs. Prevention: `@2` accepts logical
  values only from graph bytes and records explicit digest lineage.

## Evolution profile

- Stable: single logical authority, external confirmation evidence, external runtime state.
- Versionable: node/edge variants, projector contract, execution semantics and acceptance envelope.
- Forbidden compatibility move: aliasing v2 bytes/digest into v1 schema/digest domains.
- Promotion threshold: accepted spec + golden graph/view/observation fixtures + negative vectors +
  independent review.
