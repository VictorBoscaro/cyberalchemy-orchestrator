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
- Active host-launch gap:
  [GAP-ACI-JSON-DISPATCH-HOST-LAUNCH-001](#gap-gap-aci-json-dispatch-host-launch-001)
- Selected implementation route:
  [DEC-ACI-JSON-DISPATCH-IMPLEMENTATION-ROUTE-001](#decision-dec-aci-json-dispatch-implementation-route-001)
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
- Next move: repair and independently review one terminal parent-bound single seat first; only
  after `KEEP`, implement incremental handoff/feedback with a separate worker/reviewer pair and
  prove the JSON-to-host-bound-seat path end to end.

## Current state

### <a id="context-ctx-aci-root"></a>CTX-ACI-ROOT — Agents Communication Infrastructure

- Stage / gate: `validate` / `block`.
- Scope: deterministic dispatch infrastructure; Schema Service excluded.
- Closed bounded increments: CONF-000, CONF-001, CONT-001, HEADS-001, BUS-001 and the
  non-executable POLICY-000 through POLICY-002 ladder.
- Owner decision: the agent compiles one complete canonical `ExecutionGraph` JSON from user intent;
  the user may inspect topology, basic or full views, but confirmation binds the full graph digest.
- Current boundary: the bounded local fake path and Stage-E preflight integrity are accepted, but
  the first single-seat Craft attempt produced zero durable host-binding rows. Its orphaned seat was
  interrupted without a terminal manifest and the dispatch closed `error`. Sequential receipt and
  feedback support remain later gaps. Canonical v2 confirmation and production execution remain
  separate exclusions.
- Identity/role refinement: the owner kept final `display_name`, required it to come from a YAML
  canonical `agent_name` pool through a signed allocator assignment, and closed initial roles as
  `explorer|synthesizer|skeptic|writer|auditor|planner|coder|other`. The proposed delta, schemas,
  fixture and 41 negative vectors received final SPEC Recheck 3 `KEEP`. Implementation commit
  `f981397` reached `master`/`origin/master` before the required implementation review returned
  `FIX`; that chronology remains a process defect. The forward-only repair then received independent
  `KEEP` (review SHA-256 `E67819A7896AF0B58599233600853D0A70E8586F4594E5FDCDABC8F5CA4AE7DB`).
- Local execution increment: `IMPL-ACI-EXECUTION-RUNTIME-001` now separates pure candidate
  compilation from admission/execution. The latter requires a local acceptance whose exact
  canonical digest is allowlisted alongside issuer evidence, graph bytes and compilation/allocator
  authority. A persisted fixture manifest binds all nine unmodified compiler inputs, issuer
  evidence/trust and exact acceptance/candidate digests. It
  persists migration 016 state, revalidates all durable evidence before use, executes deterministic
  review-correct-verify/conditional routes through an in-memory scripted adapter and validates
  receipts against the graph-pinned audit schema. The first independent review returned `FIX`
  (`569559E51B0E06CFE4C81576D8E455F9534F26D702F1D880EB16B88F03F8AEBD`); all five findings were
  repaired. Recheck 1 closed F2-F5 but returned `FIX` for forgeable issuer metadata and mutated E2E
  inputs (`33D6870F1675E85AB93F6542A9206E013037C6680A5B7D2E56A572D0E3193C0C`); R1/R2 are repaired,
  focused 15/15 and integrated 95/95 pass. Recheck 2 returned final `KEEP` with no new findings
  (review SHA-256 `8B5F152CD04AE9BBE44BC868802241432C779ACAE5FA3C01E0828937EB8F9DFF`).
  This is not a cryptographic signature, canonical graph promotion, human confirmation `@2`,
  production host authentication or provider/tool/credential execution.
- Review residue: `2026-09-01-aci-roadmap-closure-review` is only a proposed transversal review;
  it has not been opened, registered or executed and supplies no closure evidence.
- Next move: repair the first missing single-seat binding seam through one paired `task-session`;
  only after its independent `KEEP`, address incremental handoff/feedback through another pair.

### <a id="context-ctx-aci-runtime-baseline"></a>CTX-ACI-RUNTIME-BASELINE — Existing bounded runtime

- Stage / gate: `validate` / `pass` for the bounded local baseline.
- Implemented seams: migrations through 016; durable CONF v1 confirmation; effect-free continuation
  suspension; Run/Group heads and fail-closed fence; official publication component; and one
  final-`KEEP` local fake ExecutionGraph state machine.
- Historical BUS closure validation: BUS 23/23, HEADS 8/8, CONT 9/9, CONF 8/8, traceability 1/1,
  Stage-C 8/8, bridge 18/18, runtime 200/200, Control Center 36/36, Stage-E 75/75 and compile/diff
  PASS.
- Latest bounded policy validation: POLICY-002 12/12, combined POLICY-000/001/002 59/59 and a
  curated runtime regression of 260/260 across 27 modules, explicitly excluding Lean; compileall
  and task-scope diff-check PASS.
- Final local runtime evidence: exact seven-module suite 95/95, fixture loader 9/9, bootstrap 19/19,
  acceptance forgery rejected before database creation and graph tamper rejected with zero adapter
  calls.
- Commit-time compatibility addendum: the current source defaults an omitted optional
  `connections` property to an empty topology; host 11/11, combined identity/runtime 161/161 and
  Stage-C 8/8 pass locally. The prior final `KEEP` does not cover this later line, so exact-byte
  re-review remains pending.
- Stage-E repair review: historical `KEEP`, 84/84 manifest members, SHA-256
  `4076878260B43E714AD9C79E525DF6705AC9D5A8D8DC1278BF32E4E4FB9BB71C`. The current manifest was
  locally refreshed to the compatibility repair and passes Stage-C, but that new pin is not covered
  by the preceding review. Neither state proves a host binding or terminal seat.
- Boundary: no canonical `aci.execution-graph@2`, `ConfirmRuntimeDispatch@2`, production host
  authentication, live provider/tool/credential adapter, external effects or production-readiness
  claim.
- Next move: preserve the accepted local runtime while a paired task-session repairs the missing
  single-seat binding; do not add live effects.

### <a id="context-ctx-aci-protocol-compilation"></a>CTX-ACI-PROTOCOL-COMPILATION — Bounded protocol compilation

- Stage / gate: `validate` / `pass`.
- The reviewed DraftGraph compiler deterministically emits the proposed complete ExecutionGraph
  candidate with allocator-owned display names. It remains non-canonical and cannot human-confirm
  a dispatch.
- The new local executor consumes that candidate only under an explicit local-fake admission; this
  is execution evidence, not `ConfirmRuntimeDispatch@2` authority.

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
- The confirmed research lifecycle remains blocked before launch: compile requires the producer's
  output receipt before that producer can launch, and the feedback edge with `loop_cap` is rejected.
- A later single-seat Craft lifecycle opened session `ses_87e29f91b9d29b273730af26b0c9b37e`,
  but produced zero `host_workflow_turn_bindings`; its orphaned seat was deliberately interrupted
  without a terminal mailbox/manifest and closed `error` at `evt_03d42c9a639768c5ddab0085d7b78983`.
- Next move: repair and review that single-seat binding seam first; then implement incremental
  handoff/feedback with a separate worker/reviewer pair.

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

### <a id="decision-dec-aci-json-dispatch-implementation-route-001"></a>DEC-ACI-JSON-DISPATCH-IMPLEMENTATION-ROUTE-001

- Status: `closed`, non-blocking; selected by the repository owner.
- Selected: bounded `task-session` with a worker and an independent reviewer because the
  `domainspec-implement` prerequisite is unavailable.
- Scope: two ordered paired task-sessions: first a terminal parent-bound single seat, then
  incremental initial-ready-group handoff plus governed feedback, followed by independently
  reviewed end-to-end JSON-to-host-bound-seat evidence.
- Exclusions: no canonical `aci.execution-graph@2` promotion, `ConfirmRuntimeDispatch@2`,
  production host authentication, live provider/tool/credential adapter, external effects or
  production-readiness claim.
- Evidence: the [host-gap lifecycle review](research/deterministic-json-dispatch/review-research-lifecycle.md)
  and [local-runtime final review](development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md).

### <a id="decision-dec-aci-generic-stage-handoff-arch-001"></a>DEC-ACI-GENERIC-STAGE-HANDOFF-ARCH-001

- Status: `closed`; selected by the repository owner.
- Selected: extend the existing staged host-workflow pipeline rather than create a standalone
  aggregate in this version.
- Both candidates can satisfy the nine collapse tests; the staged extension was chosen to reuse
  verified producer, materialization and launch seams with less duplicate authority machinery.
- Failure to preserve any collapse-test separation reopens the standalone-aggregate alternative.
- Evidence: [ACI-GSH-001](../../decisions/aci-generic-stage-handoff-architecture.md) and the
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

- Status: `closed`; selected by the repository owner; implementation recheck returned `KEEP`.
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

### <a id="gap-gap-aci-json-dispatch-host-launch-001"></a>GAP-ACI-JSON-DISPATCH-HOST-LAUNCH-001

- Severity: `block`; treatment: `plan`; owner: runtime architecture.
- Proven boundary: the manifested JSON bundle reaches a deterministic terminal result through the
  accepted local `ScriptedLocalAdapter` path, but cannot yet launch a host-bound seat.
- Cause: the observed single-seat launch created zero durable binding rows; beyond that first seam,
  lifecycle compilation requires downstream producer-output receipts before launching the initial
  producer and rejects the governed feedback connection with `loop_cap`.
- Treatment: first repair the single-seat host hook/binding seam and obtain independent `KEEP`;
  then use a separate paired task-session for incremental handoff/feedback and end-to-end evidence.

### <a id="gap-gap-aci-generic-stage-handoff-promotion-001"></a>GAP-ACI-GENERIC-STAGE-HANDOFF-PROMOTION-001

- Severity: `block`; treatment: `plan`; owner: domain architecture.
- Missing: concrete aggregate aspects, durable operations/events, mappings, workflow guards and
  conformance fixtures for all five accepted handoff facts.
- Consequence: the capability and architecture are accepted, but no aggregate or runtime
  implementation claim is authorized.

### <a id="gap-gap-aci-canonical-graph-contract-001"></a>GAP-ACI-CANONICAL-GRAPH-CONTRACT-001

- Severity: `block`; treatment: `plan`; owner: runtime architecture.
- Missing: accepted canonical-v2 promotion, topology/basic/full projections,
  `ConfirmRuntimeDispatch@2` observation/envelope, explicit CONF v1 cutover and a live
  provider/tool/credential/effect boundary. The reviewed compiler/identity path and final-`KEEP`
  local fake executor narrow this gap but cannot supply those missing authorities.
- Consequence: the local fake path is accepted, but canonical v2 and production execution claims
  remain blocked.

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
- [Agent identity/role implementation evidence](development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001/VALIDATION.md)
- [Agent identity/role implementation review (`KEEP`)](development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-AGENT-IDENTITY-ROLE-001/review.md)
- [Local ExecutionGraph runtime worker evidence and post-review addendum](development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/VALIDATION.md)
- [Local ExecutionGraph runtime final review](development/refinement-runs/2026-09-01-execution-graph-authority/followups/IMPL-ACI-EXECUTION-RUNTIME-001/review.md)
- [Deterministic JSON host-gap lifecycle review](research/deterministic-json-dispatch/review-research-lifecycle.md)
- [Stage-E manifest repair review (`KEEP`)](../../../.codex/workflow-inputs/2026-09-02-stage-e-manifest-repair/review.md)
- [Failed Craft lifecycle residue](../../../.codex/workflow-inputs/2026-09-02-craft-ledger-json-dispatch-update/lifecycle-residue.md)
- [Generic stage handoff discovery](discovery/generic-stage-handoff.md)
- [Generic stage handoff capability](specs/capabilities/generic-stage-handoff.md)
- [Generic stage handoff architecture decision](../../decisions/aci-generic-stage-handoff-architecture.md)
- [Generic stage handoff closing session](../../../sessions/2026-09-01-2235-generic-stage-handoff-spec.md)
- [Session record](../../../sessions/2026-08-31-2006-aci-dispatch-continuation-gate.md)

## Boundary check

- The repository root Craft ledger and other project ledgers were not mutated; this feature ledger
  owns the ACI continuation scope.
- Historical descriptor/readiness entry digests were not altered.
- Component PASS, including POLICY-002/L2, does not promote CONT-002, OPEN or POLICY-003/L3 and
  does not authorize product defaults, external actions, provider/tool use, commit, push or deploy.
- The single-graph decision plus reviewed compiler and reviewed local-executor baseline prove a
  bounded JSON-to-fake-terminal path. The later optional-topology compatibility line passes the
  local 161-test matrix but awaits exact-byte re-review. Neither state proves canonical promotion,
  confirmation `@2`, production host authentication, a live provider/tool/credential adapter,
  external effects or production readiness.
- The host-gap review proves that the current lifecycle cannot bootstrap the sequential producer
  or execute its feedback edge; it does not prove a host launch, append, seat, close or live result.
- The later Craft lifecycle proves that Stage-E preflight and open can pass, but its zero-binding
  orphan attempt closed `error`; partial ledger files and updater checkpoints are not execution
  success.
- The identity/role follow-up supersedes earlier identity/consumer claims only and its code repair
  now has `KEEP`; it does not erase historical reviews or prove projector/confirmation/live-adapter
  authority.
- The planned closure review remains unexecuted and cannot authorize any blocked execution slice.
- Generic-stage-handoff architecture selection and capability review do not prove aggregate
  promotion, durable runtime facts, conformance fixtures or implementation.
