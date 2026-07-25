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

### SCC-BL-013 — Codex collaboration hierarchy capture

Bind the current Codex `collaboration.spawn_agent` / `followup_task` lifecycle to the mandatory
YAML + ACI hook path. The Control Center already projects explicit `parent_dispatch_id` edges, but
this Phase 1 run proved that launches through the collaboration surface can complete without a
new local ledger row or hook-state file. Manual repair of hook-managed rows is forbidden.

Done when:

- launch fails closed unless both YAML and ACI return `launch-authorized`;
- every orchestrator and nested reviewer produces one correlated open/close lifecycle;
- each child carries the exact parent dispatch identity, without inferred name or timestamp joins;
- a dispatch-of-dispatches round-trip renders the same hierarchy in API, table and graph views;
- duplicate, orphan, late-close, retry and interrupted-launch fixtures pass;
- an end-to-end Codex collaboration probe proves the ledger and hook-state timestamps advance.

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

## P2 — Phase 1 validation and productization residues

These items were exposed by the implemented browser evidence. They do not invalidate the Phase 1
experiment, but they block selecting a winner or treating any variant as production-ready.

### SCC-BL-009 — Mobile topology legibility

Make the visual graph readable without depending on zoom or tiny labels while preserving the
semantic table as the complete, primary non-canvas answer.

Done when:

- every node and edge label meets the frozen mobile readability threshold;
- graph, table and path result still expose identical node and edge identity sets;
- 320 CSS-px reflow, keyboard traversal and screen-reader reading-order checks pass;
- the 204-row screenshot matrix is regenerated without overflow or digest drift.

### SCC-BL-010 — Consistent product language and localization

Choose and freeze the operator-facing locale strategy. Remove the current mixed-language
experience across navigation, states, source data explanations and recovery copy without
rewriting stable object identities or evidence.

Done when:

- one default locale and fallback policy are documented;
- every shared label, state explanation, error and safe next action is covered by the locale
  catalog;
- A, B and C render byte-equivalent semantic messages for the same fixture;
- missing translations fail visibly to the declared fallback and never erase evidence detail.

### SCC-BL-011 — Human usability and assistive-technology validation

Run the pre-registered operator study and manual assistive-technology matrix. Browser automation
does not prove comprehension, workload, trust, preference, real-user task success, complete
screen-reader behavior or full WCAG conformance.

Done when:

- eligible operators complete CF-01 through CF-06 under the frozen sampling and assistance rules;
- task success, valid action efficiency, comprehension and subjective workload are reported with
  uncertainty and withdrawals;
- keyboard-only, screen-reader, zoom/reflow and reduced-motion sessions have durable evidence;
- findings are separated into deterministic defects, UX risks and subjective preference.

### SCC-BL-012 — Production integration and promotion decision

Keep all three variants experimental until host, authentication, route ownership, observability,
operational support and rollout/rollback are explicitly owned. Promotion remains blocked until
SCC-BL-004 through SCC-BL-011 are satisfied or formally waived by their owners.

Done when:

- the production host and access-control boundary are ratified;
- logs, metrics, error budgets and support ownership are documented and exercised;
- a rollout and rollback rehearsal succeeds without changing authoritative data;
- the promotion decision cites the frozen benchmark and human-study evidence instead of the
  descriptive Phase 1 scores alone.
