# Skill Control Center backlog

This backlog contains work intentionally excluded from Phase 1. None of these items may be
silently implemented or represented as complete by the read-only/draft-only control center.

## P0 — authoritative apply safety

### SCC-BL-001 — Terminal operation fencing

Define a linearizable terminal-non-applied result, cancellation/fencing barrier, or equivalent
operation protocol that prevents a late append from racing with reconciliation or a new command.

Done when:

- late accepted receipts deterministically supersede stale reconciliation results;
- exact retry cannot create a second interpretation of the same logical operation;
- revise/revalidate uses a linked new key only after the prior operation is terminally fenced;
- concurrency, lost-ack and delayed-append tests pass.

### SCC-BL-002 — Reconciliation and receipt lookup

Define receipt/idempotency lookup before retry, the `indeterminate → reconciling` lifecycle, and
the proof required for terminal `failed`.

Done when:

- `failed` proves no append, unchanged authoritative revision and no accepted receipt;
- unknown acknowledgement never appears as failed or accepted;
- CF-06, CF-07, state matrix, screenshots and flow diagram agree;
- recovery retains draft, base revision, approval and idempotency lineage.

### SCC-BL-003 — Conflict recovery diagram

Route conflict to an explicit conflict state and revise/revalidate path; reserve
route-unavailable for missing authority bindings.

Done when the prose, state machine, Mermaid diagram and executable tests express the same branch.

## P1 — benchmark as a decision gate

### SCC-BL-004 — Valid action-efficiency score

Ensure every unsuccessful eligible assignment receives
`max(valid_observed_actions, threshold + 1)` while raw actions remain separately observable.
Bind a numeric threshold or explicit non-applicability to every CF-01–CF-07 flow.

### SCC-BL-005 — Production-only absolute acceptance

Calculate absolute variant acceptance only from production-eligible reference rows. Keep the
benchmark-only topology condition exclusively in paired promotion estimands.

### SCC-BL-006 — Estimability and convergence

Freeze a justified minimum effective participant count for the adjusted model, or simplify it.
Define blocking behavior for rank deficiency, separation, non-convergence, singular covariance,
degenerate bootstrap samples and insufficient effective clusters.

### SCC-BL-007 — Assistance taxonomy

Define allowed neutral orientation, prohibited hints, technical help, facilitator intervention,
accessibility accommodations, event recording, borderline adjudication and the binary
`unassisted` derivation.

### SCC-BL-008 — Withdrawal and worst-case population

Define observed-case and worst-case populations, planned-but-never-initiated assignment
imputation, denominators, paired-cell preservation and action scores after withdrawal.

Done for SCC-BL-004 through SCC-BL-008 when:

- the protocol is frozen before recruitment and unblinding;
- identical input records produce identical acceptance decisions;
- simulated failure, missingness, withdrawal and non-convergence fixtures have expected results;
- an independent statistical reviewer returns no blocking objection.

## Phase 1 guardrails

- No authoritative Apply, Retry Apply, Reconcile or “Applied” success claim.
- Draft, diff and validation preview remain local/proposed states.
- Benchmark results are descriptive only and cannot select or promote a variant.
- Any UI control for deferred work is disabled or absent and links to the relevant backlog ID.
