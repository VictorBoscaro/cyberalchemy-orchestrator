# Agents Communication Infrastructure Craft Ledger

Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The YAML ledger is the source of
truth; this page is only a linked navigation and status view.

## Quick links

- Blocking decision: [DEC-ACI-PRODUCT-PASS-001](#decision-dec-aci-product-pass-001)
- Active blocker: [BLK-ACI-PRODUCT-AUTHORITY-001](#blocker-blk-aci-product-authority-001)
- Active product gap: [GAP-ACI-PRODUCT-AUTHORITY-001](#gap-gap-aci-product-authority-001)
- [HEADS final evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-HEADS-001.md)
- [BUS final evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-BUS-001.md)
- [CONF-000 contract evidence](development/invoke-runs/20260831-resumable-feedback/evidence/CONF-000.md)
- [POLICY-002 final review](development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-IMPLEMENTATION-REVIEW.md)
- [Current decision gate](development/invoke-runs/20260831-resumable-feedback/plan/DECISION-GATE.md)
- [Current readiness](development/invoke-runs/20260831-resumable-feedback/plan/READINESS.md)
- Pending artifact: [ART-ACI-ROADMAP-CLOSURE-REVIEW](#artifact-art-aci-roadmap-closure-review),
  proposed only and not run.
- Next move: supply the exact CONF v2 product authority package and obtain a new explicit user
  confirmation before OPEN onward.

## Current state

### <a id="context-ctx-aci-root"></a>CTX-ACI-ROOT — Agents Communication Infrastructure

- Stage / gate: `validate` / `block`.
- Scope: deterministic dispatch infrastructure; Schema Service excluded.
- Closed bounded increments: CONF-000, CONF-001, CONT-001, HEADS-001, BUS-001 and the
  non-executable POLICY-000 through POLICY-002 ladder.
- Current boundary: PRODUCT-PASS blocks CONT-002, OPEN, positive Run transition, RESUME, WORKER,
  VERIFY and POLICY-003/L3 real attempted action.
- Review residue: `2026-09-01-aci-roadmap-closure-review` is only a proposed transversal review;
  it has not been opened, registered or executed and supplies no closure evidence.
- Next move: resolve [DEC-ACI-PRODUCT-PASS-001](#decision-dec-aci-product-pass-001).

### <a id="context-ctx-aci-runtime-baseline"></a>CTX-ACI-RUNTIME-BASELINE — Existing bounded runtime

- Stage / gate: `validate` / `pass` for the bounded local baseline.
- Implemented seams: migrations through 015; durable confirmation; effect-free continuation
  suspension; Run/Group heads and fail-closed fence; official publication component.
- Historical BUS closure validation: BUS 23/23, HEADS 8/8, CONT 9/9, CONF 8/8, traceability 1/1,
  Stage-C 8/8, bridge 18/18, runtime 200/200, Control Center 36/36, Stage-E 75/75 and compile/diff
  PASS.
- Latest bounded policy validation: POLICY-002 12/12, combined POLICY-000/001/002 59/59 and a
  curated runtime regression of 260/260 across 27 modules, explicitly excluding Lean; compileall
  and task-scope diff-check PASS.
- Boundary: no production opening, publisher, resume, effect, worker, provider/tool or adapter claim.

### <a id="context-ctx-aci-protocol-compilation"></a>CTX-ACI-PROTOCOL-COMPILATION — Bounded protocol compilation

- Stage / gate: `validate` / `pass`.
- The exact compiler SWU remains non-authoritative; its `DispatchCandidate` cannot confirm or
  execute a dispatch.

### <a id="context-ctx-aci-resumable-feedback"></a>CTX-ACI-RESUMABLE-FEEDBACK — Bounded resumable feedback

- Stage / gate: `blocked` / `block`.
- CONT-001 parks the terminal source Attempt without an effect.
- HEADS-001 provides graph-scoped Run/Group heads, total reducers, exact CAS and a fence that
  remains closed for pending/reconciliation states. Its repair incident and final `PASS / KEEP`
  lineage are preserved in the evidence.
- BUS-001 is `implemented-reviewed-pass / PASS-KEEP`. The publication candidate remains on the
  Attempt stream; official `attempt.result_accepted` and typed position/critique acceptance live on
  the Group stream. The Attempt link is non-transitioning; Group advances exactly `+2`, and Attempt
  remains unchanged.
- CONT-002 is not promoted. The next move is PRODUCT-PASS, not another technical mutation.

### <a id="context-ctx-aci-execution-policy"></a>CTX-ACI-EXECUTION-POLICY â€” Bounded execution policy

- Stage / gate: `validate` / `pass` for the exact non-executable L0-L2 ladder.
- POLICY-000/L0 is a pure oracle; POLICY-001/L1 persists and reopens synthetic test-only inputs;
  POLICY-002/L2 records one deterministic durable fake denial over one exact L1 lineage.
- POLICY-002 is `implemented-reviewed-bounded / PASS-KEEP`: 12/12 focused, 59/59 combined policy
  and 260/260 curated runtime tests across 27 modules, with Lean excluded.
- Boundary: no `ConfirmedDispatch`, Run, Group, Attempt, execution request, provider call, host
  enforcement or real attempted action is created. POLICY-003/L3 remains product-gated.

## <a id="blocker-blk-aci-product-authority-001"></a>Active blocker — BLK-ACI-PRODUCT-AUTHORITY-001

- Type / lane: `authority_blocker` / `product`.
- Status: active, refined; human/product authority required.
- Missing: the exact product values that form confirmed execution authority.
- Closure: supply the CONF v2 authority package and explicitly confirm its new dispatch identity.

## Decisions

### <a id="decision-dec-aci-product-pass-001"></a>DEC-ACI-PRODUCT-PASS-001

- Question: which exact product authority package should define the real resumable-feedback
  dispatch?
- Status: `active`, blocking.
- Options: supply a new CONF v2 authority package, or defer real execution.
- Required package:

  - revision-instruction bytes, reference and digest;
  - actual prompt bytes, references and digests;
  - role and task references;
  - `provider_ref` if distinct;
  - concrete resource-budget, sandbox and execution/authority-fence policies; and
  - complete canonical audit-opening 0.6.4 mapping, including dispatch type/route, goal, context,
    approver, agents and every remaining required field.

- Impact: these values change `confirmed_authority_digest`. Real execution requires a new dispatch
  identity, CONF v2 and new explicit user confirmation. CONF v1 remains a component fixture.

Previously closed authority decisions remain in the source ledger: explicit user confirmation is
authority; chat is sufficient now and a future UI must use the same digest-bound confirmation
boundary; CONF-000 precedes CONF-001;
CONF-001 ends at `opening_pending`; legacy FK decoupling is staged; fake adapter precedes live
provider admission.

## Active gaps

### <a id="gap-gap-aci-product-authority-001"></a>GAP-ACI-PRODUCT-AUTHORITY-001

- Severity: `block`; treatment: `delegate` to the repository/product owner.
- Missing: the exact CONF v2 product authority listed above.
- Consequence: OPEN, positive Run transition, RESUME, WORKER and VERIFY cannot begin.

### <a id="gap-gap-aci-legacy-dispatch-fk-001"></a>GAP-ACI-LEGACY-DISPATCH-FK-001

- Severity: `flag`; treatment: `plan`.
- Legacy host workflow/attempt foreign-key compatibility remains residue before a complete
  runtime-managed execution claim; it is not authority for the implemented bounded components.

Other active deferred gaps:

- `GAP-ACI-LIVE-PROVIDER-001`: restart retention, durable cancellation and real adapter
  conformance remain unproven.
- `GAP-ACI-GENERALIZATION-001`: general skill-profile support and long-term `dispatch_type` remain
  beyond the bounded slice.

Closed gaps retained historically in the ledger: confirmation contract, durable writer, global
runtime-baseline drift and POLICY-002 code entry/review.

## Key artifacts

### <a id="artifact-art-aci-roadmap-closure-review"></a>ART-ACI-ROADMAP-CLOSURE-REVIEW

- Status: `planned`; artifact type: `review-proposal`.
- Candidate output: `reviews/2026-09-01-aci-roadmap-closure-review/review.md` (not created).
- Proposed topology: eight agents with persisted output. No dispatch, registration, invocation or
  review result exists, so this row is pending residue rather than evidence.

- [Feature architecture](specs/architecture.md)
- [Continuation plan](development/invoke-runs/20260831-resumable-feedback/plan/WORK-PACK.md)
- [C2 technical/product split](development/invoke-runs/20260831-resumable-feedback/plan/C2-TECH-D0.md)
- [CONT evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-CONT-001.md)
- [HEADS evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-HEADS-001.md)
- [BUS evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-BUS-001.md)
- [POLICY-000 implementation review](development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-000-IMPLEMENTATION-REVIEW.md)
- [POLICY-001 implementation review](development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-001-IMPLEMENTATION-REVIEW.md)
- [POLICY-002 implementation review](development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-IMPLEMENTATION-REVIEW.md)
- [C2 Robot Talks findings](robot-talks/2026-09-01-continuation-c2-split/findings.md)
- [Session record](../../../sessions/2026-08-31-2006-aci-dispatch-continuation-gate.md)

## Boundary check

- The repository root Craft ledger and other project ledgers were not mutated; this feature ledger
  owns the ACI continuation scope.
- Historical descriptor/readiness entry digests were not altered.
- Component PASS, including POLICY-002/L2, does not promote CONT-002, OPEN or POLICY-003/L3 and
  does not authorize product defaults, external actions, provider/tool use, commit, push or deploy.
- The planned closure review does not alter `DEC-ACI-PRODUCT-PASS-001` and cannot authorize any
  blocked execution slice.
