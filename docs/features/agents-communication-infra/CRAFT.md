# Agents Communication Infrastructure Craft Ledger

Human-readable view of [`.craft/ledger.yml`](.craft/ledger.yml). The YAML ledger is the source of
truth; this page is only a linked navigation and status view.

## Quick links

- Selected authority decision:
  [DEC-ACI-CANONICAL-EXECUTION-GRAPH-001](#decision-dec-aci-canonical-execution-graph-001)
- Selected identity/role decision:
  [DEC-ACI-AGENT-IDENTITY-ROLE-001](#decision-dec-aci-agent-identity-role-001)
- Selected generic handoff architecture:
  [DEC-ACI-GENERIC-STAGE-HANDOFF-ARCH-001](#decision-dec-aci-generic-stage-handoff-arch-001)
- Active technical gap:
  [GAP-ACI-CANONICAL-GRAPH-CONTRACT-001](#gap-gap-aci-canonical-graph-contract-001)
- Active generic handoff promotion gap:
  [GAP-ACI-GENERIC-STAGE-HANDOFF-PROMOTION-001](#gap-gap-aci-generic-stage-handoff-promotion-001)
- Open blocking decisions: none. Active human/product blockers: none.
- [HEADS final evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-HEADS-001.md)
- [BUS final evidence](development/invoke-runs/20260831-resumable-feedback/plan/evidence/TASK-BUS-001.md)
- [CONF-000 contract evidence](development/invoke-runs/20260831-resumable-feedback/evidence/CONF-000.md)
- [POLICY-002 final review](development/invoke-runs/20260831-resumable-feedback/plan/evidence/POLICY-002-IMPLEMENTATION-REVIEW.md)
- [Current decision gate](development/invoke-runs/20260831-resumable-feedback/plan/DECISION-GATE.md)
- [Current readiness](development/invoke-runs/20260831-resumable-feedback/plan/READINESS.md)
- Pending artifact: [ART-ACI-ROADMAP-CLOSURE-REVIEW](#artifact-art-aci-roadmap-closure-review),
  proposed only and not run.
- Next move: independently recheck the repaired agent-identity/role delta, then adapt the stale
  DraftGraph compiler before broader `ExecutionGraph v2` or runtime work.

## Current state

### <a id="context-ctx-aci-root"></a>CTX-ACI-ROOT — Agents Communication Infrastructure

- Stage / gate: `validate` / `block`.
- Scope: deterministic dispatch infrastructure; Schema Service excluded.
- Closed bounded increments: CONF-000, CONF-001, CONT-001, HEADS-001, BUS-001 and the
  non-executable POLICY-000 through POLICY-002 ladder.
- Owner decision: the agent compiles one complete canonical `ExecutionGraph` JSON from user intent;
  the user may inspect topology, basic or full views, but confirmation binds the full graph digest.
- Current boundary: the missing v2 contract blocks CONT-002, OPEN, positive Run transition, RESUME,
  WORKER, VERIFY and POLICY-003/L3 real attempted action.
- Identity/role refinement: the owner kept final `display_name`, required it to come from a YAML
  canonical `agent_name` pool through a signed allocator assignment, and closed initial roles as
  `explorer|synthesizer|skeptic|writer|auditor|planner|coder|other`. The proposed delta, schemas,
  fixture and 41 negative vectors have received an independent review and two rechecks, all `FIX`;
  the repaired candidate is ready for another independent recheck. Current compiler code is
  stale for this dimension and remains blocked from promotion until adaptation plus review.
- Review residue: `2026-09-01-aci-roadmap-closure-review` is only a proposed transversal review;
  it has not been opened, registered or executed and supplies no closure evidence.
- Next move: close the active
  [canonical graph contract gap](#gap-gap-aci-canonical-graph-contract-001) through specification,
  fixtures and independent review.

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
- It does not yet compile the owner-selected single complete `ExecutionGraph v2` authority.

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
- CONT-002 is not promoted. Product responsibility is decided; the next move is the v2 graph
  contract and its evidence, not runtime code.

### <a id="context-ctx-aci-execution-policy"></a>CTX-ACI-EXECUTION-POLICY â€” Bounded execution policy

- Stage / gate: `validate` / `pass` for the exact non-executable L0-L2 ladder.
- POLICY-000/L0 is a pure oracle; POLICY-001/L1 persists and reopens synthetic test-only inputs;
  POLICY-002/L2 records one deterministic durable fake denial over one exact L1 lineage.
- POLICY-002 is `implemented-reviewed-bounded / PASS-KEEP`: 12/12 focused, 59/59 combined policy
  and 260/260 curated runtime tests across 27 modules, with Lean excluded.
- Boundary: no `ConfirmedDispatch`, Run, Group, Attempt, execution request, provider call, host
  enforcement or real attempted action is created. POLICY-003/L3 remains product-gated.

### <a id="context-ctx-aci-generic-stage-handoff"></a>CTX-ACI-GENERIC-STAGE-HANDOFF — Generic stage handoff

- Stage / gate: `design` / `block`.
- The reviewed discovery, capability spec 0.2.0 and architecture selection ACI-GSH-001 are accepted.
- The selected design extends the bounded host-workflow pipeline and preserves commitment,
  authorization, publication, delivery and acceptance as separate durable facts.
- `SourceToSlotMapping` supplies preconfirmed topology and visibility intent; it is not the
  post-commitment publication authorization for exact producer bytes.
- Next move: promote the capability into aggregate domain, operation, mapping and workflow
  contracts, then independently red-team the result before implementation.

## Resolved product blocker

`BLK-ACI-PRODUCT-AUTHORITY-001` is resolved. The owner decided that the agent, not the user,
compiles every execution-relevant value into one canonical graph. The user confirms that proposed
authority. Remaining work is a technical contract gap, not a request for the user to populate
fields manually.

## Decisions

### <a id="decision-dec-aci-generic-stage-handoff-arch-001"></a>DEC-ACI-GENERIC-STAGE-HANDOFF-ARCH-001

- Status: `closed`; selected by the repository owner.
- Selected: extend the existing staged host-workflow pipeline rather than create a standalone
  aggregate in this version.
- Both candidates can satisfy the nine collapse tests; the staged extension was chosen to reuse
  verified producer, materialization and launch seams with less duplicate authority machinery.
- Failure to preserve any collapse-test separation reopens the standalone-aggregate alternative.
- Evidence: [ACI-GSH-001](../../../decisions/aci-generic-stage-handoff-architecture.md) and the
  [accepted capability](specs/capabilities/generic-stage-handoff.md).

### <a id="decision-dec-aci-canonical-execution-graph-001"></a>DEC-ACI-CANONICAL-EXECUTION-GRAPH-001

- Status: `closed`; selected by the repository owner.
- The agent compiles user intent into one canonical JSON containing the complete execution graph
  and every execution-relevant value.
- Chat may show topology, basic or full projections. These are presentations of the same complete
  authority, not separate authority levels.
- Confirmation always binds the digest of the complete canonical graph. Any material change
  requires a new digest and confirmation.
- `pending-sheet` and `capability-resolution` may remain internal compilation concepts or normalized
  evidence, but they are not separate user-confirmed authority documents in v2.
- CONF v1 remains immutable historical/component evidence; this decision does not rewrite it or
  prove v2 runtime support.

### <a id="decision-dec-aci-product-pass-001"></a>DEC-ACI-PRODUCT-PASS-001

- Status: `superseded`, non-blocking.
- Its premise that the owner would manually supply every prompt, reference and policy was replaced
  by the agent-compiled canonical graph decision above.
- No concrete CONF v2 graph has yet been specified, confirmed or executed.

### <a id="decision-dec-aci-agent-identity-role-001"></a>DEC-ACI-AGENT-IDENTITY-ROLE-001

- Status: `closed`; selected by the repository owner; implementation remains gated.
- Final `display_name` is retained, but the DraftGraph does not author it. Canonical pool v0.7 uses
  only YAML `agent_name`; the boundary loader normalizes it, and the trusted allocator freezes one
  distinct node-to-agent assignment in the signed compilation context. `agent-name` is rejected,
  not a permanent alias.
- `role` remains DraftGraph-authored against a versioned, digest-pinned allowlist. Initial roles are
  `explorer`, `synthesizer`, `skeptic`, `writer`, `auditor`, `planner`, `coder` and singular `other`.
- The real legacy pool still uses `name`; migration must be atomic with all known consumers/tests in
  the code SWU. `name` cannot become an unversioned permanent alias.
- Evidence: [identity/role follow-up](development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001/DECISION.md).

Previously closed authority decisions remain in the source ledger: explicit user confirmation is
authority; chat is sufficient now and a future UI must use the same digest-bound confirmation
boundary; CONF-000 precedes CONF-001;
CONF-001 ends at `opening_pending`; legacy FK decoupling is staged; fake adapter precedes live
provider admission.

## Active gaps

### <a id="gap-gap-aci-generic-stage-handoff-promotion-001"></a>GAP-ACI-GENERIC-STAGE-HANDOFF-PROMOTION-001

- Severity: `block`; treatment: `plan`; owner: domain architecture.
- Missing: concrete aggregate aspects, durable operations/events, mappings, workflow guards and
  conformance fixtures for all five accepted handoff facts.
- Consequence: the capability and architecture are accepted, but no aggregate or runtime
  implementation claim is authorized.

### <a id="gap-gap-aci-canonical-graph-contract-001"></a>GAP-ACI-CANONICAL-GRAPH-CONTRACT-001

- Severity: `block`; treatment: `plan`; owner: runtime architecture.
- Missing: the closed `ExecutionGraph v2` schema, canonical bytes/digest, agent compiler ownership,
  reviewed identity/role compiler adaptation, per-node execution fields, data-flow semantics,
  topology/basic/full projections, confirmation
  observation, runtime-derived facts, CONF v1 compatibility and runtime-ingestion boundary.
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

Closed gaps retained historically in the ledger: product-authority responsibility, confirmation
contract, durable writer, global runtime-baseline drift and POLICY-002 code entry/review.

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
- [Agent identity/role proposed delta](development/refinement-runs/2026-09-01-execution-graph-authority/followups/SPEC-ACI-AGENT-IDENTITY-ROLE-001/DECISION.md)
- [Generic stage handoff discovery](discovery/generic-stage-handoff.md)
- [Generic stage handoff capability](specs/capabilities/generic-stage-handoff.md)
- [Generic stage handoff architecture decision](../../../decisions/aci-generic-stage-handoff-architecture.md)
- [Generic stage handoff closing session](../../../sessions/2026-09-01-2235-generic-stage-handoff-spec.md)
- [Session record](../../../sessions/2026-08-31-2006-aci-dispatch-continuation-gate.md)

## Boundary check

- The repository root Craft ledger and other project ledgers were not mutated; this feature ledger
  owns the ACI continuation scope.
- Historical descriptor/readiness entry digests were not altered.
- Component PASS, including POLICY-002/L2, does not promote CONT-002, OPEN or POLICY-003/L3 and
  does not authorize product defaults, external actions, provider/tool use, commit, push or deploy.
- The single-graph decision resolves product responsibility but does not prove a v2 schema,
  compiler, confirmation adapter, persistence path or runtime execution.
- The identity/role follow-up supersedes earlier identity/consumer claims only; it does not erase
  historical `KEEP` reviews. Its schemas and fixture validator do not prove the required code
  migration, production YAML loader, allocator signature, projector or runtime consumer.
- The planned closure review remains unexecuted and cannot authorize any blocked execution slice.
- Generic-stage-handoff architecture selection and capability review do not prove aggregate
  promotion, durable runtime facts, conformance fixtures or implementation.
