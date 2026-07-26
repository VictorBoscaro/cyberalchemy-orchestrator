---
status: active
date: 2026-07-25
owner: governed-agent-work-infrastructure
---

# Host Binding → BUS → ACI-005 Dispatch Route

## Current execution state

The earlier `0.6.1 → 0.6.2` failure was transient concurrent-work evidence. The current appender
again declares schema `0.6.1` with `others` admitted through an in-place owner amendment.

Fresh validation on the current bytes passed:

- `implementations.tests.runtime.test_host_workflow_binding`: 5/5;
- `implementations.tests.runtime.test_bus_reveal_delivery`: 7/7.

The persisted Phase-A closing review is now complete with verdict `FIX`:

- review artifact:
  `docs/features/agents-communication-infra/reviews/2026-07-25-host-bus-phase-a-close/review.md`;
- frozen corpus: 18/18 hashes matched;
- focused validation: Host Binding 5/5 and BUS Reveal Delivery 7/7;
- surviving findings: six `MAJOR`;
- dispatch close: `resolved`, two independent attackers.

The findings split into two readiness classes:

| Repair cone | Findings | Readiness | Route |
|---|---|---|---|
| authority/provenance contract | F1 invocation-plan authority; F2 producer output evidence | authority sources and terminal output-evidence contract are not concrete enough for safe code | `others` authoring, independent readiness review, then `code` |
| bounded runtime integrity | F4 follow-up null identity; F5 peer-byte rehash; F6 Stage-E source manifest | accepted behavior and exact failure checks are already explicit | `code`, then independent review |
| completion evidence | F3 unsupported `implemented-verified` claim | executable only after both repair cones close | full validation matrix, execution receipt, status restoration |

ACI-005 discovery remains gated behind the repaired and re-reviewed Phase-A seam. The two repair
cones may advance in parallel because their initial write scopes are disjoint: contract authoring
does not mutate runtime, while bounded integrity code must not invent the unresolved authority or
output-evidence model.

## Operating rule

Before every mutation-capable dispatch, the primary orchestrator and one independent read-only
readiness helper classify the target:

| Evidence state | Route |
|---|---|
| Unknown external or repository facts | `research` |
| Product behavior, boundary, or architecture not settled | discovery authoring workflow |
| Falsifiable uncertainty with a bounded criterion | `experiment` |
| Existing artifact or implementation needs attack | `review` |
| Contracts are known but specs/tests/work-pack/descriptor are incomplete | `others` authoring |
| SPEC, test obligations, work-pack, exact SWU and readiness receipt pass | `code` |

`dispatch_type: plan` remains reserved and is not used. Plan and authoring artifacts use the LIVE
`others` route when delegation is needed.

## Phase A — repair and ratify the existing dogfood seam

1. **Review, read-only — complete (`FIX`):** verify mechanics/correctness and fidelity/governance across
   the current appender, Host Binding, BUS descriptor/readiness, runtime, tests, mappings and
   source-integrity evidence.
2. **Others, authority/provenance authoring:** settle F1 and F2 in the normative specs, mappings,
   test obligations, exact SWU descriptor and code-readiness receipt. Do not mutate runtime.
3. **Code, bounded runtime integrity:** repair F4, F5 and F6 with adversarial zero-write/tamper
   tests. This may run in parallel with step 2 but may not touch F1/F2 behavior.
4. **Review, readiness cone:** verify the F1/F2 authoring package before its code dispatch.
5. **Code, authority/provenance:** implement only the reviewed F1/F2 SWU.
6. **Review and completion evidence:** verify all six findings, run the descriptor's full
   four-command matrix, emit the completed content-addressed execution receipt, and only then
   restore `implemented-verified`.

Phase A exit evidence:

- confirmed dispatch → host binding → reveal → materialized input passes;
- current records use the accepted schema and historical rows remain readable without mutation;
- drift and one-byte mismatches fail closed;
- source manifests and receipts bind the final bytes;
- provider/tool starts remain zero.

## Phase B — prepare and implement ACI-005

7. **Short discovery:** settle current opening-row schema, isolated implementation versus cutover,
   exact evidence consumed from ACI-003/004, and which sole-writer proof blocks implementation
   versus activation.
8. **Others, authoring:** update discovery/SPEC/mappings/interfaces, add dedicated test IDs,
   reconcile TASK-020 and manifests, produce `SWU-ACI-005`, and produce code-readiness evidence.
9. **Review:** independently validate the complete readiness cone. Insert prerequisite SWUs if
   ACI-003/004 evidence is insufficient.
10. **Code:** implement only ACI-005.
11. **Review:** validate absent/identical/divergent rows, crash recovery, restart, verified-opening
    eligibility, zero provider starts, and no cutover.

## Autonomous delegation boundary

The orchestrator may prepare, review, register, execute, verify, and close contained repository
dispatches without repeated consultation. It returns to the owner when:

- a blocker-level product, ontology, persistence, or authority choice has multiple viable answers;
- the objective or repository scope expands materially;
- external writes, credentials, paid services, deployment, destructive actions, or publication
  become necessary;
- an existing owner artifact conflicts with the proposed route;
- a delegated envelope budget or expiry must change.

## Invoke fallback note

The installed `invoke` package references a relative `plan.md` contract that is absent. Therefore
this route uses the repository's current `domainspec-subagents-strategy` and records the missing
Invoke mode contract as a tooling gap rather than pretending the Invoke plan gate passed.
