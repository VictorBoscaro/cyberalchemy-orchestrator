# Skill Control Center — Phase 1 scope decision

- Date: 2026-07-25
- Decision owner: `@VictorBoscaro`
- Source: user authorization in the active Codex session
- Gate result: `PASS`

## Decision

Proceed with a read-only/draft-only Phase 1.

Phase 1 includes the attention queue, skill and dispatch catalogs, search, filters, stable
selection, detail views, the three separate topology models, path queries, evidence/coverage/
freshness presentation, local preferences, draft/diff/validation previews, exactly three
functionally equivalent UI variants, backend read models, tests, accessibility checks and
screenshot review.

Phase 1 must not expose or imply an authoritative apply operation. Its benchmark may collect
experimental evidence but may not approve, reject, promote or select a variant.

## Options considered

| Option | Benefit | Cost/risk | Result |
|---|---|---|---|
| Phase 1 read-only/draft-only | Delivers the control-center experiment while preserving authority safety | Apply and benchmark promotion remain deferred | Selected |
| Block until all residue is resolved | Produces a broader end-to-end contract | Delays the UI experiment for unrelated transactional/statistical detail | Rejected |

## Rationale

The terminal discovery review isolated all surviving objections to authoritative apply/reconciliation
or benchmark-gating mechanics. Reviewers confirmed that the task-led information architecture,
read-only topology/evidence contracts, exactly three variants and backend-first delivery survived.
The user authorized subagents to implement this bounded part and requested a clear backlog for the
remainder.

## Remaining blockers

No blocker remains for the bounded Phase 1. The items in
[`BACKLOG.md`](../features/skill-control-center/BACKLOG.md) remain blockers for authoritative apply
or using benchmark results as a product decision gate.

## Assumptions

- Drafts are proposals only and never change authoritative state.
- An unavailable authoritative route is shown as unavailable, not simulated.
- Tests and screenshots can verify Phase 1 behavior but cannot close deferred authority or
  statistical contracts.

