# Stage 06 — Invoke Design

- Capability: `invoke`
- Mode: `design`
- Verdict: `pass`
- Artifact type: candidate research architecture, not executed research

## 1. Research thesis and falsification

Candidate thesis:

> V1 can provide useful bounded composition and confined local work under one authority root if
> every protected operation and authority-changing transition is explicitly derived, conserved,
> enforced, and evidenced;
> composition and data flow alone never create authority.

The thesis fails if a necessary V1 workflow requires an unbounded or self-derived grant, or if a
child/tool/adapter/retry path can produce effective authority or effects beyond the approved
pre-state without a new authority-root decision.

## 2. Evidence architecture

The research uses four evidence tiers without collapsing them:

| Tier | Supports | Does not support |
|---|---|---|
| Accepted decisions | Product/governance boundary already chosen | Runtime enforcement |
| Code + executed tests | Implemented behavior under tested conditions | Deployment or trust-root legitimacy |
| As-built operational evidence | Observed local behavior at a recorded time | Universal or production guarantees |
| Proposal/design/research | Candidate obligations, vocabulary, counterexamples | Present capability or accepted authority |

External literature, if later approved, supplies precedents and counterexamples only. Local owners
retain the decision.

## 3. Research method

### Pass A — Current-state reconstruction

For each ATS, reconstruct grants, actors, transitions, enforcement, receipts, bypass paths, and
epistemic status from decisions, code/tests, and as-built evidence.

### Pass B — V1 envelope design

Classify each resulting matrix cell on independent axes:

- availability: `allowed | approval-gated | unavailable | out-of-model`;
- delegability: `delegable-attenuated | root-only | forbidden-to-delegate | n/a`;
- claim basis: `decision | code | test | as-built | proposal | none` references;
- current behavior: any defined combination of `implemented | enforced | observed | conventional |
  forbidden | unknown`;
- later target: `candidate-supported | candidate-gated | intentionally-out | undecided`, with
  prerequisites and non-goals.

Approval binds a canonical command/spec digest, target, version, and bounds; exact payload bytes are
required only when the effect payload already exists.

### Pass C — Transition attacks

Cross six transition classes with direct, child, tool/adapter, replay/aggregate/cross-run, and
concurrent/interleaved paths. Emit ordered or partially ordered ATS traces; test authority before
and after each checkpoint, global conservation, effective effects, revoke/use races, stale approval,
concurrent quota spend, cancellation, and separately granted compensation.

### Pass D — Utility and evolution

Run five utility workflows. For every restriction, populate a specific ladder:
`restriction -> fence -> negative tests -> receipt -> recovery/revocation -> owner decision`.
Filesystem, network/secrets, effects, dynamic graphs, delegation/nested authority, and long-lived
work require distinct evidence bundles.

## 4. Data model

Minimum ATS record:

```text
ats_id
parent_ats_ids_and_causal_predecessors
grant_id_and_root_decision_id
freedom_slice
transition_class
path_kind
initiator_and_authentication
effective_actor
authorization_owner_and_decision
issuer
enforcer
pre_state_and_grant_ancestry
operation_resource_phase
policy_and_version
derivation_rule
effective_principal_tool_adapter
bounds_before_and_after
attenuation_comparison_result
conservation_account
current_observed_enforcement
current_observed_receipts
current_evidence_refs_and_claim_status
v1_required_enforcement
v1_required_receipts
post_state_and_external_effects
typed_receipts
recommended_v1_availability
recommended_v1_delegability
later_target_and_prerequisites
failure_posture
utility_witness
amplification_counterexample
relaxation_evidence
residue_owner
```

Every typed receipt contains `type`, producer/principal, verifier/trust root, ATS/operation id,
subject and scope digest, policy/grant/version, timestamp/phase, outcome, evidence location, causal
link, and claim ceiling. Capability consumption is a distinct receipt. Authorization or delivery
never substitutes for enforcement or effect evidence; missing required evidence yields
`unknown/unavailable`.

## 4.1 Closed axes and coverage ledger

- Actors: user/operator, approver/authority root, root orchestrator, composite/Work definition,
  delegated seat/agent, tool/subprocess, adapter/external system.
- Phases: define/configure, confirm/issue, materialize/dispatch, execute, effect, collect/reveal,
  retry/resume/cancel/compensate, revoke/close.
- Action families and resources derive from the six transition classes and five Freedom Slices.

The coverage ledger maps each seed freedom to Slice, transition class/path, ATS ids, and matrix
cells. Every generated cell is decided or marked `not-applicable` with reason. This is the
completeness test, not the raw Cartesian product by itself.

## 5. Candidate V1 hypothesis to test, not adopt

- One authority root and one root scheduler per confirmed run.
- Recursive `Work` composition and separately confirmed child dispatch lineage are allowed; a child
  does not acquire scheduler or issuer authority.
- Authority-root-approved bounded subactions do not require one human confirmation per leaf.
  Reconfirmation is required for any qualitative scope widening, new admin/delegation bit, new
  external target/effect class, topology digest change, cumulative quota increase, or stale
  command/spec/policy digest. Pure attenuation does not require a new prompt.
- Local filesystem mutation and subprocesses may be allowed only inside demonstrably confined
  workspaces and command profiles; current inherited-host routes are not such proof.
- Network, tools, secrets, and external effects are adapter/gateway-specific and unavailable when
  the required fence and receipts do not exist.
- Capability issuance/revocation, policy/tool-profile/adapter mutation, authority-root creation, and
  dynamic graph promotion are non-delegable or separately approval-gated.
- Unknown capability, scope, schema, enforcement, or effect outcome fails closed to a named owner.

## 6. Scenario matrix design

Positive scenarios:

- bounded research fan-out/fan-in;
- confined code edit/test/review;
- draft/validation preview plus human gate; apply is admitted only when an independently enforced
  apply capability exists, otherwise it stops at an approved draft;
- bounded repair loop;
- mediated external effect.

Negative scenarios:

- self-issue and token lending;
- child invokes launcher through shell/tool;
- privileged credential arrives as ordinary context;
- child output becomes an automatically executed graph;
- fan-out/retry exceeds root budget or effect quota;
- policy/tool profile changes before a previously denied action;
- adapter receipt proves delivery but is reported as effect success;
- two seats combine partial grants into a forbidden effect.
- a child causes a separately confirmed run that attempts to inherit context, token, or budget;
- capability revocation races with in-flight use or effect delivery;
- model/provider selection creates undeclared data egress;
- cancellation occurs after dispatch and compensation is attempted without a separate grant.

Each scenario card freezes actor, pre-state, grant, resource/target, bounds, fences, and expected
outcomes. It returns separately: recommended V1 availability/delegability; current executable
status; missing fence/evidence; and later target. `undecided-owner-decision` may remain during
research, but the final packet must give exactly one recommended V1 disposition.

## 7. Required research deliverables

1. glossary and semantic split of “orchestrable”;
2. current-state transition inventory;
3. ATS dataset and five Freedom Slices;
4. closed-axis coverage ledger plus current/V1/later matrix with independent availability,
   delegability, claim-basis, and behavior status;
5. authority chain and typed-receipt model;
6. utility workflow results;
7. attack and non-amplification results;
8. closed V1 envelope recommendation;
9. relaxation evidence ladder;
10. decision packet with accepted candidates, rejected alternatives, residue, and owner routes.

## 8. Owner and write boundaries

The future research may write only its research folder. It may recommend but not modify RWO, ACI,
runtime, capability, UI, policy, or decision artifacts. Product/RWO/ACI/security owners separately
accept or reject its recommendations.

## 9. Open design residue

- Whether the research belongs under RWO or a repository-wide authority/capability feature.
- Whether nested authority is categorically forbidden or merely unavailable in V1.
- The canonical owner of the authority-root and capability-issuance decision.
- Which current route, if any, provides sufficient confinement for local mutation claims.
- The exact bounded external corpus for precedents and security counterexamples.
