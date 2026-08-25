# Cyberalchemy Orchestrator Craft Ledger

Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The ledger is the source of truth; this page is a linked navigation surface.

## Quick links

- Root next move: [resolve the production cutover gate](#decision-dec-cutover-gate-001).
- Blocking decisions: [DEC-CUTOVER-GATE-001](#decision-dec-cutover-gate-001), [DEC-PHASE-A-BASELINE-001](#decision-dec-phase-a-baseline-001).
- Active blockers: [BLK-BROKERED-AUTHORITY-001](#blocker-blk-brokered-authority-001), [BLK-PHASE-A-OWNER-DECISION-001](#blocker-blk-phase-a-owner-decision-001).
- Active gaps: [write-side cutover](#gap-gap-write-side-cutover-001), [OBL-E3](#gap-gap-orch-category-proof-001), [EG-1](#gap-gap-eg1-sole-writer-001), [D9 authority](#gap-gap-d9-authority-001), [T0 automation](#gap-gap-t0-automation-001), and the four [Schema Service artifact-type gaps](#context-ctx-schema-service-artifact-types-v0).

## Contexts and pending work

### <a id="context-ctx-cyberalchemy-orchestrator-root"></a>CTX-CYBERALCHEMY-ORCHESTRATOR-ROOT — Cyberalchemy Orchestrator

- Stage / gate: `define` / `flag`
- Pending: production cutover interpretation and repository-level residue.
- Next move: resolve [DEC-CUTOVER-GATE-001](#decision-dec-cutover-gate-001) and synchronize root status with the active infrastructure Plan.

### <a id="context-ctx-gawi-program"></a>CTX-GAWI-PROGRAM — Governed Agent Work Infrastructure

- Stage / gate: `plan` / `flag`
- Authority: active, proposal-only root Plan.
- Pending: [OBL-E3](#gap-gap-orch-category-proof-001), [D9](#gap-gap-d9-authority-001), and [T0 automation](#gap-gap-t0-automation-001), plus child work below.
- Next move: advance only children with explicit authority and readiness.

### <a id="context-ctx-arl-l0-review"></a>CTX-ARL-L0-REVIEW — Agent Reference Lineage L0 Review

- Stage / gate: `review-audit` / `flag`
- Pending artifact: `agent-reference-lineage-l0-work-pack.md` is implementation-complete, review-pending.
- Next move: run the independent review and record its receipt.

### <a id="context-ctx-brokered-launcher"></a>CTX-BROKERED-LAUNCHER — Brokered Agent Launcher

- Stage / gate: `blocked` / `block`
- Pending: active proposal remains inert because governing authority is unknown.
- Next move: resolve [BLK-BROKERED-AUTHORITY-001](#blocker-blk-brokered-authority-001) through a repository-owner decision.

### <a id="context-ctx-host-bus-phase-a"></a>CTX-HOST-BUS-PHASE-A — Host Binding to BUS Phase A

- Stage / gate: `review-audit` / `block`
- Pending: output-evidence and implementation-baseline owner selection.
- Next move: resolve [DEC-PHASE-A-BASELINE-001](#decision-dec-phase-a-baseline-001).

### <a id="context-ctx-aci-protocol-governance"></a>CTX-ACI-PROTOCOL-GOVERNANCE — ACI Protocol Governance

- Stage / gate: `design` / `flag`
- Accepted ownership does not claim completed schemas, operations, implementation, or tests.
- Next move: retain separate readiness gates for those claims.

### <a id="context-ctx-schema-service-artifact-types-v0"></a>CTX-SCHEMA-SERVICE-ARTIFACT-TYPES-V0 — Schema Service Artifact Types v0

- Stage / gate: `review-audit` / `block`
- Scope: test the artifact model first with `analysis`, then conditionally with `skill` and `folder`, before implementing a universal registry or runtime.
- Evidence: [experimentation plan](projects/schema-service/experimentation-plans/artifact-types-v0/experimentation-plan.md), [analysis package](projects/schema-service/experimentation-plans/artifact-types-v0/experiments/01-analysis/README.md), [accepted review report](projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md), and [session close](sessions/2026-08-25-0843-schema-service-artifact-experiments.md).
- Pending: [candidate lifecycle](#gap-gap-schema-analysis-lifecycle-001), [base resolution](#gap-gap-schema-analysis-base-resolution-001), [revision immutability](#gap-gap-schema-analysis-immutability-001), and [successor-gate alignment](#gap-gap-schema-experiment-gate-alignment-001).
- Next move: correct the four confirmed findings, then verify references and hashes before freezing `criterion.md`.

## Blockers

### <a id="blocker-blk-brokered-authority-001"></a>BLK-BROKERED-AUTHORITY-001

- Status: active, refined; human governance decision required.
- Closure: durable authority decision or receipt names the owner and permitted binding scope.
- Evidence: `plans/governed-agent-work-infrastructure/workstreams/brokered-agent-launcher-capability-bootstrap.md`.

### <a id="blocker-blk-phase-a-owner-decision-001"></a>BLK-PHASE-A-OWNER-DECISION-001

- Status: active, refined; repository-owner decision required.
- Closure: select Phase-A output-evidence and implementation-baseline options with rationale.
- Evidence: `docs/decisions/phase-a-output-evidence-and-implementation-baseline.md`.

## Decisions

### <a id="decision-dec-cutover-gate-001"></a>DEC-CUTOVER-GATE-001 — What gates production cutover?

- Status: `active`, blocking production cutover only.
- Options: EG-1 closure gates cutover; EG-1 gates only veracity; compose a separate cutover gate.
- Rationale: README explicitly says the audit and Phase-2 session interpretations conflict.
- Evidence: [README.md](README.md), [enum-drift audit](vault/audit/ledger-enum-drift-finding.md), and [Phase-2 session](sessions/2026-07-22-1315-phase2-confirm-handoff.md).

### <a id="decision-dec-phase-a-baseline-001"></a>DEC-PHASE-A-BASELINE-001 — Phase-A evidence and baseline

- Status: `active`, blocking consequential Phase-A repair.
- Pending choice: binding-output evidence model and implementation baseline.
- Evidence: [decision record](docs/decisions/phase-a-output-evidence-and-implementation-baseline.md).

### Closed authority decisions

- `DEC-ACI-PROTOCOL-OWNERSHIP-001`: ACI Protocol Governance owns reusable protocol compilation boundaries.
- `DEC-HOST-INPUT-BINDING-001`: bounded host-workflow binding bridge selected.
- `DEC-REPOSITORY-LEVERAGE-001`: Host Binding→BUS first, then ACI-005.
- `DEC-SKILL-CONTROL-PHASE1-001`: Skill Control Center Phase 1 is read-only/draft-only.
- `DEC-WORKER-B-SEQUENCE-001`: close Phase A, implement ACI-005, then run the fake-worker slice.

## Gaps

### <a id="gap-gap-write-side-cutover-001"></a>GAP-WRITE-SIDE-CUTOVER-001

Production write-side cutover and associated sole-writer/provider/materializer proof remain incomplete. Governed by [DEC-CUTOVER-GATE-001](#decision-dec-cutover-gate-001).

### <a id="gap-gap-orch-category-proof-001"></a>GAP-ORCH-CATEGORY-PROOF-001

OBL-E3 remains open; the categorical claim may narrow to the sequential fragment. Evidence: [OBLIGATIONS.md](OBLIGATIONS.md).

### <a id="gap-gap-eg1-sole-writer-001"></a>GAP-EG1-SOLE-WRITER-001

Two post-vocabulary close rows demonstrate an unaccounted writer path; EG-1 remains promotion-blocked. Evidence: [enum-drift audit](vault/audit/ledger-enum-drift-finding.md).

### <a id="gap-gap-d9-authority-001"></a>GAP-D9-AUTHORITY-001

Macro-to-micro work-context authority ownership remains CRITICAL with no repository gate. Evidence: [README.md](README.md).

### <a id="gap-gap-t0-automation-001"></a>GAP-T0-AUTOMATION-001

The claim/probe/survival discipline runs manually, but its automated knowledge-machine loop is unbuilt. Evidence: [active Plan](plans/governed-agent-work-infrastructure/PLAN.md).

### <a id="gap-gap-schema-analysis-lifecycle-001"></a>GAP-SCHEMA-ANALYSIS-LIFECYCLE-001

Candidate lifecycle is promised per candidate but represented only by one global catalog state. Evidence: [review](projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md#f1--candidate-lifecycle-is-promised-but-cannot-be-represented-per-candidate).

### <a id="gap-gap-schema-analysis-base-resolution-001"></a>GAP-SCHEMA-ANALYSIS-BASE-RESOLUTION-001

The unresolved `analysis@0` base leaves candidate resolution fail-closed even after criterion freeze. Evidence: [review](projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md#f2--the-stated-execution-gate-still-leaves-every-candidate-resolution-fail-closed).

### <a id="gap-gap-schema-analysis-immutability-001"></a>GAP-SCHEMA-ANALYSIS-IMMUTABILITY-001

Candidate revision immutability begins too late to preserve revision identity from catalog admission. Evidence: [review](projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md#f3--candidate-revision-immutability-begins-too-late).

### <a id="gap-gap-schema-experiment-gate-alignment-001"></a>GAP-SCHEMA-EXPERIMENT-GATE-ALIGNMENT-001

The `skill` and `folder` placeholders weaken the substantive successor gates in the main plan. Evidence: [review](projects/schema-service/reviews/2026-08-20-artifacts-full-review/review.md#f4--local-placeholders-weaken-the-programs-substantive-successor-gates).

## Boundary check

- Nested ledgers under `Arcanum/`, `Arcanum/spells/goal/`, and `tools/test-derivation-engine/` were not imported or modified.
- Draft/discovery feature packages were not promoted to active execution contexts solely from their directory status.
- Schema Service candidates remain experiment-local and non-normative; no runtime, registry, resolver, criterion, fixture, or run was claimed complete.
- `BACKLOG.md` remains an available artifact whose contents are parked candidates, not committed work.
