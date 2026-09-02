---
title: Deep comparison of agent-orchestration projects
status: research-synthesis-reviewed
date: 2026-09-01
source_dispatch: 2026-09-01-deep-comparative-agent-orchestration-synthesis
review_dispatch: 2026-09-01-deep-comparative-agent-orchestration-review
evidence_cutoff: 2026-09-01
---

# Deep comparison of agent-orchestration projects

## Answer in one paragraph

The eight projects are useful precedents, but they are not one peer class and none was evidenced as
an implementation of the whole governed system described by Cyberalchemy's objective. The strongest
mechanism families concern replayable plans and resume state, approval race protection, work
ownership and repair, typed recovery, separation of authoritative decisions from telemetry, and
identity keys with distinct lifecycles. Cyberalchemy's best-evidenced difference is a bounded,
heterogeneous combination: a validated confirmation marker; sanctioned append/open/close actions;
host-mediated, digest-bound parent-seat launch; declared role/group/connection/final-approver
topology; evidence standing; and a broader objective/authority model. This is neither a single
atomic mechanism nor a novelty claim, and some enforcement remains host-dependent. The immediate
workflow deficiency is precise: the current turn-zero compiler emits `slots: []` and implements no
producer-output-to-consumer-input binding for staged synthesis; `connections` express topology and
must not be misdescribed as data edges. This research therefore split stages
(`implementations/server/runtime/dispatch_workflow.py:312-324`) [C6]. Managed cloud, multi-tenant
boards, model gateways, full SDLC and Kubernetes operation are outside the inspected local surface
or remain undecided; comparison alone does not make them requirements.

## Evidence contract and temporal boundary

External claims below are limited to the eight pinned revisions recorded in the frozen explorer
return [E0]. **DA** means a documentation assertion, **IW** an implementation witness, **TW** a
repository test witness, and **EO** an observation executed by an explorer. A test file is not an
executed observation; an EO of a focal suite is not a live deployment; activity counts are not
maturity or adoption evidence. “Not evidenced” means only that the inspected public surfaces at the
pinned revision did not show the property. It is never a universal absence claim.

Local claims are bounded by the cited repository surfaces as they existed on 2026-09-01. The root
README itself labels the repository draft/private, distinguishes built from thesis, and reports no
`LICENSE` [C1]. The synthesis does not independently rerun the external repositories and does not
upgrade explorer labels.

### Source map

- **[E0]** [Frozen explorer evidence](explorer-evidence.md), including revision, activity,
  implementation/test/observation labels, contrary evidence and license caveats.
- **[E1]–[E8]** Sections 1–8 respectively in [E0](explorer-evidence.md): Mission Control,
  BoundFlow, Open Multi Agent (OMA), Orloj, Temporal Agent Harness, GitMesh, Chorus and Agent Fleet.
- **[C1]** `README.md:14-18,23-38,53-64,70-119`—objective and evidence states
  ([repository source](../../README.md)).
- **[C2]** `implementations/README.md:13-22,53-84`—reader, marker-only confirmation, governed
  runtime and pilot boundary ([repository source](../../implementations/README.md)).
- **[C3]** `implementations/server/main.py:311-353`—confirmation writes only a marker
  ([repository source](../../implementations/server/main.py)).
- **[C4]** `.agents/skills/register-dispatch/SKILL.md:37-62,94-160`—validated append/close contract
  and its non-enforced semantics ([repository source](../../.agents/skills/register-dispatch/SKILL.md)).
- **[C5]** `mandatory-host-wrapper.md:1-38,69-115`—bound launch, digests, fail-closed boundary and
  host caveats ([repository source](../../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md)).
- **[C6]** `implementations/server/runtime/dispatch_workflow.py:300-365`—turn-zero manifest and
  digest-bound launch plan ([repository source](../../implementations/server/runtime/dispatch_workflow.py)).
- **[C7]** `WORK-PACK.md:21-29`—local pass, live Codex hook bypass residue and blocked production
  enablement ([repository source](../../docs/features/agents-communication-infra/WORK-PACK.md)).
- **[C8]** `plans/governed-agent-work-infrastructure/PLAN.md:293-364`—built slice, portability caveat
  and unbuilt research/architecture fronts ([repository source](../../plans/governed-agent-work-infrastructure/PLAN.md)).
- **[C9]** `plans/autonomous-agent-graph-system/README.md:30-46`—intended system and the rule that
  precedents do not define its target model ([repository source](../../plans/autonomous-agent-graph-system/README.md)).

## RQ coverage and status

| RQ | Status | Answer and evidence | Remaining uncertainty / collapse condition |
|---|---|---|---|
| RQ0 | Answered, bounded | Ten reusable mechanism families survive below; full-product differences are classified as gap, boundary or undecided [E0][C1]. | Collapses if later inspection disproves the witnesses or product authority reclassifies boundaries. |
| RQ1 | Answered | Cyberalchemy states are separated in the next section [C1][C2][C7][C8]. | “Built” still does not mean deployed, correct or host-independent. |
| RQ2 | Answered at pinned revisions | Eight fact sheets and the capability matrix distinguish IW/TW/EO/DA [E1–E8]. | No independent production-use study was performed. |
| RQ3 | Answered | Material documentation/implementation divergences are recorded for all nine comparison objects [E1–E8][C1–C8]. | An omitted surface may resolve a bounded “not evidenced.” |
| RQ4 | Answered | Every external fact sheet pins a SHA/tag and 2026-09-01 cutoff [E0]. | Claims cease beyond those revisions; HEAD/release skew is noted. |
| RQ5 | Answered | OMA and Agent Fleet are closest partial peers; the others are adjacent product/runtime layers, not direct whole-system peers [E1–E8]. | “Peer” depends on comparing the implemented stratum, not the broader objective. |
| RQ6 | Answered, proposal-bounded | Per-project territory not evidenced in inspected Cyberalchemy proposals is listed below [E1–E8][C8][C9]. | This is not a declaration that Cyberalchemy must never enter that territory. |
| RQ7 | Answered, negative-bounded | No inspected external surface showed Cyberalchemy's whole confirmed-dispatch/bound-seat/evidence-standing combination [E0][C4–C6]. | Not a novelty or universal-absence claim; close precedents are named. |
| RQ8 | Answered provisionally | One immediate staged-input gap, conditional hardening candidates and undecided expansion territories are separated below [C6–C9]. | Only cited product authority can turn an observed surface boundary into a deliberate boundary. |
| RQ9 | Answered | Every negative is revision-, surface- and evidence-bounded; no “repo lacks X” claim is unqualified [E0]. | Broader source inspection is required before stronger negatives. |
| RQ10 | Answered provisionally | Repository-local operation is built/portability intent but not a settled permanent constraint; evidence-first governance is objective-level, while exact mechanisms remain revisable [C1][C8][C9]. | The durable product constitution has not settled the boundary. |
| RQ11 | Answered | Ten pattern-level candidates fit the objective without making precedent authoritative [E0][C9]. | Fit is informational until discovery/target authority accepts it. |
| RQ12 | Partially answered | TypeScript/Python/Go mechanisms can inform designs, but no integration spike or dependency analysis establishes implementation compatibility. | Technical compatibility needs one adoption packet per candidate. |
| RQ13 | Answered as blocker | MIT, Apache-2.0 and AGPL-3.0 were observed; Cyberalchemy has no receiving license, so code compatibility is unresolved [E0][C1]. | Pattern learning is not code copying; legal review remains required. |
| RQ14 | Answered | Findings can prioritize discovery, target-model decisions and adoption spikes; they cannot change requirements, license, architecture or implementation authority [C9]. | No single downstream owner has yet been designated. |

## Cyberalchemy evidence-state baseline (RQ1, RQ10)

| State | Bounded content | Evidence / caveat |
|---|---|---|
| **Built** | FastAPI/SSE reader and ten UIs; marker-only confirmation endpoint; append-only YAML ledger with sanctioned appender; deterministic agent pool; operational skills; host-wrapper implementation [C1][C2][C3]. | Confirmation alone neither appends nor launches. “Mandatory” host enforcement applies only when supported trusted clients load and execute the hook [C5]. |
| **Local pilot** | SQLite ACI/APT journal, immutable artifacts, hash-chained journal/projections, exact profiles, scoped capabilities, reference delivery and loopback serving [C1][C2]. | Opt-in, off by default, loopback/single-host; production serving remains closed [C2][C7]. |
| **Proposed** | Generic write-side/materializer cutover, agent-work language, broader work-context/target architecture and much of decision-science machinery [C1][C8][C9]. | Proposal is not implementation authority. |
| **Open** | Formal typing, permanent repository-local boundary, remote/durable execution shape, authority ownership and several architecture decisions [C1][C8]. | No Lean typing exists here; portability is not demonstrated on a second machine [C1][C8]. |
| **Contested** | Exact implications of the historical ledger writer hole and some cutover gates [C1][C8]. | The broader objective must not inherit stronger certainty from the dispatch stratum. |

The objective-level commitment is to preserve warranted relations from work to objective,
authorization/decision and evidence [C1]. Repository-local operation and the current YAML/SQLite,
skill and hook mechanisms are implementation properties or design choices unless separately made
product constraints [C1][C8][C9].

## Eight pinned fact sheets (RQ2–RQ7)

### 1. builderz-labs/mission-control

- **Revision / standing:** `5483a0e…`, package `2.3.0`, alpha, MIT; exact-SHA CI passed lint,
  types, unit, build and E2E, but no explorer local smoke ran [E1].
- **Layer and evidence:** self-hosted operational control plane. Atomic claim, routing,
  reconciliation and review/retry have direct IW, and the exact-SHA quality gate has EO-CI. Cost
  views, RBAC, command approvals and the broader integration surface remain DA/inspected surface
  claims here unless their claim-specific witnesses in [E1] are followed [E1].
- **Divergence:** “automated” pipeline progress still requires explicit advance; spawn failure can
  leave a step running; the project documents no declarative approval-policy engine. Ed25519 receipt
  scope is MCP call-log rows, not every dispatch [E1].
- **Territory not evidenced in current Cyberalchemy proposals:** multi-workspace operations,
  recurring tasks, runtime installers, GitHub synchronization, cost dashboard and broad RBAC.
  These are operational-product choices, not automatically gaps [E1][C8][C9].
- **Cyberalchemy-relative negative:** the inspected Mission Control surfaces did not evidence the
  whole exact-confirmation, sanctioned append/close, capability-route digest, bound-seat and
  evidence-standing combination. Its call-log signing is a close but narrower precedent [E1][C4–C6].

### 2. boundflow/boundflow

- **Revision / standing:** `ebe165b…`, public preview/pre-1.0, backend Apache-2.0 and SDK MIT;
  Go build/vet/test passed, Python integration had not completed, and no external production users
  were declared [E2].
- **Layer and evidence:** distributed Go/Postgres control plane plus Python workers. Persisted jobs,
  leases, approval/input gates, recovery and backpressure have direct IW/TW. Adaptive policies,
  rollback, multi-tenancy and OTel correlation are broader DA/partially witnessed surface claims and
  must not inherit the strength of the core execution witnesses [E2].
- **Divergence:** recovery is at-least-once between checkpoints; cost caps lag actual cost; approval
  may commit before best-effort audit; OTel is not mandatory evidence [E2].
- **Territory not evidenced in current proposals:** managed multi-tenant service, customer API keys,
  adaptive numerical policies/rollback and partitioned remote worker scheduling [E2][C8][C9].
- **Cyberalchemy-relative negative:** no inspected surface showed bound workflow seats tied to an
  exact human-confirmed dispatch and repository authority/evidence states; its governance audit is
  nevertheless strong prior art for correlated but separate evidence [E2][C4–C6].

### 3. open-multi-agent/open-multi-agent (OMA)

- **Revision / standing:** `6eece1d…`, after `v1.17.0`, MIT. Five focal suites passed in EO; one
  Windows timeout did not establish a product defect [E3].
- **Layer and implemented witnesses:** embeddable TypeScript runtime with task dependencies,
  concurrency, structural governance receipts, CAS/content-bound approvals, checkpoints, verifiable
  context journal, default-deny tools and plan/replay [E3].
- **Divergence:** durability, journal and durable approvals are opt-in rather than universal;
  HEAD is newer than release, and “three dependencies” omits optional peers [E3].
- **Territory not evidenced/proposed as a Cyberalchemy default:** automatic objective-to-DAG
  coordinator authority and built-in consensus/evaluation primitives. Automatic planning may be a
  proposal aid, not an authority source [E3][C9].
- **Cyberalchemy-relative negative:** OMA is the closest context-lineage/receipt precedent, but its
  inspected surfaces did not show the repository confirmation/appender/host-binding/evidence-state
  combination. This demotes any novelty claim, not the usefulness of OMA's mechanisms [E3][C4–C6].

### 4. OrlojHQ/orloj

- **Revision / standing:** `e6b723b…`, tag `v0.19.0`, pre-1.0, Apache-2.0 with NOTICE/trademark
  conditions; test files were inspected but no Go EO ran [E4].
- **Layer and evidence:** declarative platform and distributed runtime. Graphs/joins,
  leases/heartbeat/retry/dead-letter and approval blocks have direct type/consumer IW. Deterministic
  desired-to-observed reconciliation, gateways, schedules and Kubernetes operation remain broader
  DA/under-witnessed territory in this report [E4].
- **Divergence:** “production-grade” remains DA; deployment/reliability was not proven; audit can be
  no-op; in-memory mode loses state; APIs may change [E4].
- **Territory not evidenced in current proposals:** Kubernetes operator, model/secrets/memory
  gateways, schedules/webhooks and eval UI [E4][C8][C9].
- **Cyberalchemy-relative negative:** desired/observed and runtime recovery are richer than the
  local execution substrate, while exact repository authorization lineage was not evidenced in the
  inspected Orloj surfaces [E4][C4–C6].

### 5. temporal-community/temporal-agent-harness

- **Revision / standing:** `ab11f49…`, `0.1.0`, experimental, MIT, no observed release; no suite EO
  because `uv` was unavailable [E5].
- **Layer and implemented witnesses:** Temporal-based durable agent workflows, typed turn protocol,
  child workflows, durable human tool approval, separate human/agent channels, callbacks and
  structured events [E5].
- **Divergence:** the generic activity wrapper does not prove no duplicate arbitrary side effects;
  one declared progress event has no emitter; child termination may interrupt cleanup [E5].
- **Territory not evidenced in current proposals:** Temporal dependency, conversational session UI,
  callback-tool product surface and generated-code mode/sandbox [E5][C8][C9].
- **Cyberalchemy-relative negative:** Temporal supplies stronger durable execution and channel
  separation, but the inspected harness did not show Cyberalchemy's exact repository confirmation,
  sanctioned ledger and evidence-standing semantics [E5][C4–C6].

### 6. LF-Decentralized-Trust-labs/gitmesh

- **Revision / standing:** `a84df32…`, server `0.3.0`, later than prerelease `v0.4.0-alpha`,
  Apache-2.0; CI configuration but no verified run or local suite EO [E6].
- **Layer and evidence:** multiuser agent-operations server/UI/CLI. Conditional issue checkout and
  policy effects have direct IW. Persistent sessions, approval revisions, cost control, adapter
  identity codecs and attestation are broader or partially witnessed claims; the negative witnesses
  show bypass/asynchrony but do not prove every positive capability in that bundle [E6].
- **Divergence:** YAML is normalized, not automatically compiled to Rego; OPA failure can fall back
  to a permissive matcher; Codex can bypass approvals/sandbox via arguments; one cost path bypasses
  budget pause; attestation is non-blocking [E6].
- **Territory not evidenced in current proposals:** network multiuser issue-board product,
  GitHub/GitLab integration, persistent monetary budgets and broad CLI adapter marketplace [E6][C9].
- **Cyberalchemy-relative negative:** GitMesh has stronger operations/adapters, but no inspected
  evidence of the whole digest-bound confirmed seat and explicit evidence-state model. Its async
  attestation cannot substitute for authoritative lifecycle provenance [E6][C4–C6].

### 7. Chorus-AIDLC/Chorus

- **Revision / standing:** `e147e86…`, tag `v0.17.1`, AGPL-3.0; exact-SHA CI passed tests and
  release-contract checks, but no live-provider EO was performed [E7].
- **Layer and evidence:** full SDLC product with direct witnesses for acceptance verification,
  permission mapping, durable actor addressing and FIFO wakes. The complete
  actor/execution/product-session/provider-resume/interruption split is only partially witnessed;
  provider-resume transitions need a more exact follow-up [E7].
- **Divergence:** idea lineage is one untyped parent edge; wake queue is in-memory; host/cwd identity
  is self-reported; backend wiring does not prove live-provider operation [E7].
- **Territory not evidenced in current proposals:** full Kanban/SDLC application, OIDC/PKCE,
  revocable product keys, remote daemon and conversation product [E7][C9].
- **Cyberalchemy-relative negative:** Chorus has richer application lifecycle and identity
  separation, while typed objective/decision/evidence composition and bound repository launch were
  not shown. Direct code reuse is blocked pending receiving-license/legal decisions [E7][C1].

### 8. chankov/agent-fleet

- **Revision / standing:** `64a39a1…`, tag `v2.0.0`, MIT; exact release workflow passed and local EO
  ran 129 core tests, but not a live Pi/Herdr/Hermes system [E8].
- **Layer and implemented witnesses:** local Pi-centric harness with specialist dispatch, structured
  returns, deterministic budgets, assertion ledger, scope/drift controls, archives and provider
  semaphore [E8].
- **Divergence:** tool reduction is not OS sandboxing; scope gate is advisory; archives are
  retention-prunable conventions; provider caps are local; Hermes live support is unproven [E8].
- **Territory not evidenced in current proposals:** Pi roster/comms panes, installer/doctor/recovery
  workflow and deterministic context-pressure recycling [E8][C8].
- **Cyberalchemy-relative negative:** Agent Fleet is a close local-harness peer and strong evidence
  contract precedent, but the inspected surfaces did not show the exact append/open/close,
  capability-route and parent-seat binding semantics [E8][C4–C6].

## System-layer classification (RQ5)

| Project | Primary inspected layer | Relationship to Cyberalchemy's implemented stratum |
|---|---|---|
| Cyberalchemy | Repository-local governance/provenance substrate plus a local control reader/pilot | Baseline; broader objective exceeds the implemented stratum [C1][C2]. |
| Agent Fleet | Local model-specific orchestration harness | **Closest partial peer** for dispatch discipline, evidence and local constraints; weaker authoritative lifecycle [E8]. |
| OMA | Embeddable multi-agent runtime library | **Close partial peer** for topology, receipts, context lineage and replay; not a standalone governed repository control plane [E3]. |
| Mission Control | Self-hosted operational control plane/application | Adjacent operational peer; much broader UI/operations boundary [E1]. |
| GitMesh | Multiuser issue/agent operations platform | Adjacent operational peer; server/network/integration boundary [E6]. |
| BoundFlow | Distributed workflow governance/execution substrate | Runtime reference below/alongside the local control plane [E2]. |
| Orloj | Declarative platform plus distributed runtime/control plane | Broader platform/runtime reference [E4]. |
| Temporal harness | Durable agent runtime on Temporal | Execution/durability reference, not product/governance whole-system peer [E5]. |
| Chorus | Full SDLC application and remote daemon | Application-layer reference above orchestration [E7]. |

There is therefore no defensible one-dimensional ranking. Comparing feature counts would reward
projects for entering different product layers and obscure the objective/authority distinction.

## Cross-repository capability matrix (RQ2, RQ5–RQ7)

Legend: **IW** implementation witness; **TW** test witness; **EO** explorer execution/CI observation;
**B/LP** Cyberalchemy built/local-pilot evidence; **NF** not evidenced in the inspected surfaces at
the pinned revision; **—** outside the project's evident layer or not assessed. Combined labels do
not imply production maturity.

| Mechanism / territory | Cyberalchemy | External witnesses and exact semantic limit |
|---|---|---|
| Declared role/group/dependency topology | B [C1,C4] | Mission, BoundFlow, OMA, Orloj, Temporal, GitMesh, Chorus and Fleet expose task, graph, child or roster structure [E1–E8]. Topology does not imply data transport. |
| Confirmation of an exact dispatch proposal | Marker plus separately sanctioned lifecycle B [C2–C4] | **NF for the same mechanism** in inspected external surfaces. Runtime approvals, task review and acceptance verification are different mechanisms [E1–E8]. |
| Runtime approval of action or content | Not the same as dispatch confirmation | Mission, BoundFlow, OMA, Orloj, Temporal, GitMesh and Chorus have bounded approval/review witnesses [E1–E7]. Scope, durability and approving authority differ. |
| Authoritative authorization/decision lifecycle record | YAML B; SQLite LP [C1,C2] | BoundFlow audit is separate but non-atomic; Orloj audit may be no-op; GitMesh activity attestation is asynchronous [E2][E4][E6]. These are not context journals or telemetry. |
| Context lineage / reconstruction | ACI/APT LP [C1,C2] | OMA journal/verifier IW is the strongest external witness [E3]. Temporal events and Chorus transcripts do not by themselves prove reconstructible model context. |
| Operational telemetry / event stream | LP and host-dependent surfaces [C2,C5] | BoundFlow OTel, Temporal events, GitMesh activity and Chorus transcripts are observability witnesses with different reliability guarantees [E2][E5–E7]. |
| Derived per-run artifact archive | Not the authoritative ledger | Agent Fleet archive/assertion IW+EO; prunable by retention [E8]. Archive is not authorization, provenance completeness or WORM storage. |
| Parent-seat launch binding | Digest-bound, host-mediated B with bypass caveat [C5–C7] | **NF for the same binding** externally. Tool allowlists, policy, permission maps and human approval enforce different boundaries [E1–E8]. |
| Approval race/content protection | No local CAS race witness; hardening candidate | OMA CAS plus approved-content binding IW/EO [E3]. CAS prevents stale/racing decisions; it does not establish legitimacy or authority. |
| Capability-surface restriction | Host-bound and heterogeneous [C5,C7] | OMA default-deny IW; Fleet harness tool reduction IW/EO; Orloj/GitMesh policy witnesses have different bypass and isolation limits [E3][E4][E6][E8]. |
| Producer-output → consumer-input binding | **Absent in current turn-zero compiler: `slots: []`** [C6] | No inspected external witness demonstrates the exact proposed immutable manifest contract. OMA plan/checkpoint and Orloj resume context are adjacent precedents, not this binding [E3][E4]. |
| Checkpoint / plan replay / resume context | Not evidenced as a general current mechanism | OMA plan/checkpoint IW+EO; Orloj task/approval resume context IW; Temporal workflow persistence IW [E3–E5]. Their guarantees differ. |
| Failure/recovery state machine | Conditional future-runtime need | Orloj lease/retry/DLQ, BoundFlow lease/at-least-once recovery and Chorus typed interruption are separate witnesses [E2][E4][E7]. Desired/observed reconciliation remains under-witnessed. |
| Work ownership arbitration | NF in inspected local surface | Mission atomic claim and GitMesh conditional checkout IW [E1][E6]. This is distinct from concurrency limits and queue pressure. |
| Queue admission/backpressure | NF in inspected local surface | BoundFlow queue/coalesce/backpressure IW; Fleet provider semaphore is process-local concurrency control, not distributed admission [E2][E8]. |
| Stranded-work reconciliation | NF in inspected local surface | Mission deferred-run reconciliation and BoundFlow lease recovery IW [E1][E2]. This is distinct from initial claim and backpressure. |
| Identity and correlation keys | Parent, seat and session LP [C5,C6] | Chorus strongly distinguishes actor, connection, product session and provider resume identity; GitMesh adapters/sessions are adjacent [E6][E7]. Each key needs its own lifecycle. |
| Budget record, measurement and enforcement | Token budget recorded; effect unproven [C4] | Mission cost attribution, BoundFlow lagged policy, GitMesh bypassed pause path, Chorus rollups and Fleet deterministic task/turn budgets are different jobs [E1][E2][E6–E8]. None should be relabeled as a universal hard monetary cap. |
| Full operational UI/application and network tenancy | Reader UI B; not an ops product | Mission, GitMesh, Orloj and Chorus implement broader application/platform surfaces [E1][E4][E6][E7]. This is product territory, not a mechanical equivalence claim. |

The matrix supports two conclusions only: Cyberalchemy has a bounded, partly executed combination
not found as a whole in the inspected corpus, and several comparables are much stronger
execution/operations substrates. It does not support a novelty claim, universal absence, or the
collapse of approval, authority, provenance, attestation, observability and evidence standing into
one category.

## Documentation versus implementation (RQ3)

| Object | Documentary or surface impression | Bounded implementation/test/observation correction |
|---|---|---|
| Cyberalchemy | “Mandatory” hooks and a confirmation UI could read as universal governed launch. | Confirmation writes only a marker; host enforcement ends where hooks are not loaded, and one Codex build bypassed `PreToolUse`; production/cutover remain blocked [C2][C3][C5][C7]. |
| Mission Control | Automated pipelines and signed receipts. | Explicit advance is required, failure can strand a running step, and signing covers MCP call-log rows rather than all dispatches [E1]. |
| BoundFlow | Recovery, cost caps and governance audit. | Recovery is at-least-once, the cap observes lagged cost, and approval can precede best-effort audit [E2]. |
| OMA | Durable/auditable runtime. | Checkpoints, durable approvals and journal are opt-in; focal EO is not application-wide production evidence [E3]. |
| Orloj | “Production-grade.” | Production mechanisms exist, but deployment/reliability were not proven; audit may be no-op and memory mode is non-durable [E4]. |
| Temporal harness | No duplicate tool calls. | Generic activities lack a universal idempotency contract; one progress event is declared without an emitter [E5]. |
| GitMesh | YAML automatically compiles to Rego and policy governs runs. | YAML normalizes internally; OPA failure may permit via fallback; adapters can bypass approval/sandbox and one cost path bypasses pause [E6]. |
| Chorus | Durable SDLC/agent operation. | Actor/session models are strong, but wake queue crash recovery and live-provider execution were not demonstrated; lineage is a single untyped edge [E7]. |
| Agent Fleet | Sandbox/immutable archive/live monitoring language. | Tool removal is not an OS sandbox, archive is prunable convention, provider caps are local and Hermes live operation is unsupported [E8]. |

## Gap, boundary or undecided? (RQ6, RQ8, RQ10)

| Difference | Classification | Reason and evidence |
|---|---|---|
| No compiled producer-output → consumer-input binding exists for staged turn-zero work | **Immediate implemented gap relative to staged synthesis** | Every turn-zero manifest is generated with `slots: []`; `connections` express topology, not data semantics. This research had to split stages [C6]. |
| Codex multi-agent hook can bypass `PreToolUse` in an observed host build | **Known integration gap** | Explicitly recorded; host reload/live smoke required [C5][C7]. |
| Approval CAS plus approved-content hash | **Hardening candidate; local defect not proven** | OMA provides IW for the stale/race job, but this research did not produce a local race witness or exhaustive proof of absence [E3]. |
| Typed retry/lease/dead-letter/interruption semantics | **Conditional requirement for a future durable/remote runtime** | Orloj/BoundFlow/Chorus show concrete but different witnesses; the local remote-runtime boundary is unsettled [E2][E4][E7][C8]. |
| Full SDLC/Kanban/conversation product | **Outside inspected surface; expansion undecided** | Chorus is application-layer. No cited product decision makes its exclusion a permanent deliberate boundary [E7][C9]. |
| Automatic objective-to-DAG coordinator authority | **Not authorized as a default** | A coordinator may propose a plan under explicit delegation; external precedent cannot own objective or authorization [E3][C9]. |
| Multi-workspace RBAC, issue boards, GitHub/GitLab sync, recurring tasks | **Outside inspected planning surfaces; expansion undecided** | Mission Control/GitMesh territory; C8/C9 are not an exhaustive repository-wide negative [E1][E6][C8][C9]. |
| Managed cloud, multi-tenancy, remote worker scheduler, Kubernetes operator | **Undecided expansion boundary** | Strong external implementations exist, but repository-local permanence and runtime architecture are unsettled [E2][E4][C8]. |
| Monetary cost enforcement | **Undecided** | External examples have lag/bypass caveats; Cyberalchemy has no product decision or effect proof [E1][E2][E6]. |
| Cryptographic event attestation | **Undecided mechanism** | Witnessed narrowly in Mission Control/GitMesh; value collapses without scoped claims, keys and authoritative atomic write [E1][E6]. |
| Receiving license | **Decision blocker, not feature gap** | Without it, code-level compatibility cannot be concluded; Chorus is additionally AGPL-3.0 [E0][C1]. |

## Reuse verdict matrix (RQ11–RQ13)

“Observed implementer” below means only that the pinned repository contains the named witness. It
does not mean inventor, owner of a generic pattern, or owner of the local composition. No exhaustive
originality search was performed. **GO** means a bounded follow-up is warranted; it is not adoption
authority. `Reimplement pattern informed by witnesses` never authorizes code copying.

| Candidate | Owner / prior-art qualification | Concrete witness | Evidence mode | Witnessed? | Definitionally sound? | Boundary fit | Dependencies / license | Uncertainty / collapse test | Verdict | Use mode |
|---|---|---|---|---|---|---|---|---|---|---|
| Immutable producer-output → consumer-input binding | **Local design response**; OMA/Orloj are adjacent only | Current compiler `slots: []` [C6]; OMA plan/checkpoint and Orloj resume context [E3][E4] | Local IW; adjacent external IW | **Exact external witness gap** | Yes as a proposed contract, not an observed external mechanism | **High** | Local compiler; external licenses do not authorize copying | Must bind producer, digest, terminal status and bounds without mutable prompt regeneration | **REVISE → GO discovery** | Design locally, informed by adjacent witnesses |
| Executable plan artifact and replay | OMA observed implementer | OMA plan/checkpoint/journal [E3] | IW + focal EO | Yes | Yes; distinct from cross-seat input binding | High | MIT example; receiving license unresolved | Replay must preserve authority and exact source version | **GO** | Reimplement pattern informed by witness |
| Checkpoint / frozen resume context | OMA; Orloj and Temporal adjacent variants | Checkpoint, task/approval context and workflow persistence [E3–E5] | IW; OMA EO | Yes, guarantees differ | Yes when guarantee is stated per source | Medium-high | MIT/Apache examples; Temporal is a large dependency | Reject any claim of exactly-once arbitrary side effects | **GO investigate** | Compare guarantees before design |
| Structural role/order conformance receipt | OMA observed implementer | OMA governance receipt [E3] | IW + focal EO | Yes | Yes; validates structure, not content | High | MIT | Collapses if it merely repeats agent prose | **GO** | Reimplement pattern informed by witness |
| Assertion-support cross-check | Agent Fleet observed implementer | Fleet assertion ledger/evidence rules [E8] | IW + local EO | Yes | Yes; support is not authority | High if non-duplicative | MIT | Do not collapse `source` into authorization or provenance completeness | **GO** | Reimplement pattern informed by witness |
| Approval CAS and approved-content hash | OMA observed implementer | OMA durable approval [E3] | IW + focal EO | Yes | Yes; prevents race/stale content only | High | MIT | Local defect remains unproven until a race/coverage check exists | **GO hardening study** | Reimplement pattern informed by witness |
| Human authority channel unavailable to parent agents | Temporal observed implementer | Temporal human-only approval update [E5] | IW/TW | Yes | Yes; authority separation is distinct from CAS | High | MIT; Temporal dependency not required for the invariant | Must prevent agent autoapproval across all host paths | **GO** | Adopt invariant, design locally |
| Typed failure/retry/lease/dead-letter/interruption states | Orloj, BoundFlow and Chorus implement different components | Runtime consumer, lease/recovery and interruption witnesses [E2][E4][E7] | IW/TW | Yes by component | Yes when split by delivery, persistence and idempotency semantics | Conditional on remote runtime | Apache/AGPL examples; no code adoption | Only required if durable/remote execution enters scope | **GO conditionally** | Reimplement selected state contracts |
| Desired-versus-observed reconciliation | Orloj DA/partial IW | Resource declarations and consumer code [E4] | DA + partial IW | **Witness gap** | Sound concept, under-witnessed here | Conditional | Apache-2.0 | Needs controller transition code/tests before stronger attribution | **INVESTIGATE** | Do not claim implemented precedent yet |
| Authoritative decision record separated from best-effort telemetry | BoundFlow partial witness; local objective/LP | BoundFlow audit path plus caveat [E2]; ACI/APT [C2] | IW; local LP | Separation yes; stable-ID correlation under-witnessed externally | Yes; audit and telemetry have different jobs | High | Pattern-level; Apache example | Stable-ID correlation is a local design requirement, not a BoundFlow-owned witness | **GO with revision** | Strengthen local atomic record/correlation |
| Actor, connection, execution, product-session and provider-resume keys with distinct lifecycles | Chorus primary witness; GitMesh adjacent | Chorus schema/addressing tests; GitMesh adapter surface [E6][E7] | IW/TW; Chorus CI EO | Chorus yes; GitMesh adjacent | Yes when each key/lifecycle is enumerated | High | Chorus AGPL code blocked; reimplement contract | Collapses if keys are aliases with no lifecycle rules | **GO** | Reimplement contract informed mainly by Chorus |
| Capability-surface restriction with declared enforcement boundary | OMA default-deny; Fleet harness reduction | OMA config; Fleet work mode [E3][E8] | IW + focal EO | Yes | Yes; neither automatically proves OS sandbox or host interception | High, host-dependent | MIT examples; actual host APIs required | Every bypass and unsupported host must remain explicit | **GO** | Defense-in-depth pattern |
| Work-ownership arbitration | Mission atomic claim; GitMesh conditional checkout | Claim and checkout witnesses [E1][E6] | IW; Mission CI EO | Yes | Yes; distinct from queue pressure | Conditional on concurrent work | MIT/Apache | Avoid distributed machinery before boundary acceptance | **GO conditionally** | Reimplement selected primitive |
| Queue admission and backpressure | BoundFlow observed implementer | Lifecycle/scheduler witness [E2] | IW/TW | Yes | Yes; distinct from claim and repair | Conditional on remote/runtime load | Apache-2.0 | Needs local workload and priority semantics | **GO conditionally** | Investigate when concurrency enters scope |
| Stranded-work reconciliation | Mission and BoundFlow observed implementers | Deferred reconciliation and lease recovery [E1][E2] | IW/TW; Mission CI EO | Yes | Yes | Conditional on asynchronous/remote work | MIT/Apache | Delivery and idempotency semantics must be explicit | **GO conditionally** | Reimplement selected repair loop |
| Derived per-run evidence archive | Agent Fleet observed implementer | Run namespace/archive [E8] | IW + local EO | Yes | Yes if explicitly derived and prunable | Medium | MIT | Never replace authoritative ACI/APT facts or call it WORM | **GO** | Reimplement derived view |
| Drift, scope and task/turn budget guardrails | Agent Fleet observed implementer | Scope gate, watchdog and run budget [E8] | IW + local EO | Yes | Yes as operational guardrails, not evidence archive | Medium | MIT | Scope is advisory; thresholds need product authority | **GO investigate** | Start advisory |
| Scoped cryptographic event attestation | Mission narrow witness; GitMesh asynchronous adjacent witness; generic cryptographic prior art predates both | MCP call-log signing [E1]; async activity attestation [E6] | IW/TW; Mission CI EO | Yes, narrowly | Yes; integrity/authenticity relative to key is not authorization or semantic provenance | Medium/undecided | MIT/Apache; key management required | Never infer signed dispatch, completeness or authority | **GO investigate** | Reimplement only after key/scope decision |

No candidate is a `novel-attempt`: the research did not perform an originality search. No candidate
is `KILL` solely for lack of a job, but the immutable cross-seat binding, desired/observed
reconciliation and stable-ID correlation retain exact witness gaps and therefore remain
`REVISE/INVESTIGATE`, not unqualified `GO`. Boundary and licensing blocks defer adoption.

## Recommended use sequence (RQ14)

1. **Discovery/contract first:** define a governed producer-output manifest and replay semantics that
   close the `slots: []` handoff gap. Require exact source digest, byte/cardinality bounds, producer
   binding, terminal status and immutable downstream input [C5][C6].
2. **Approval hardening:** decide whether confirmation/approval must use compare-and-set and bind the
   approved content hash; preserve a human-only channel where an agent cannot approve its child
   [E3][E5].
3. **State model:** separate evidence standing (`built`, `proposed`, etc.) from operational
   desired/observed/retry/interruption states [E2][E4][E7][C1].
4. **Evidence contract:** add structural receipt and assertion-support checks only where they extend,
   rather than duplicate, the authoritative ACI/APT journal [E3][E8][C2].
5. **Expansion decisions later:** remote workers, multi-tenancy, budgets, full UI/SDLC and
   cryptographic attestation each require an owner decision before technical adoption work.
6. **License before code:** select a receiving license and obtain compatibility/legal review before
   copying any code. Treat Chorus code as blocked in the meantime [E0][E7][C1].

## Unresolved questions and retained dissent

- The corpus does not establish production reliability, adoption or complete security for any
  external project; stars and CI are bounded indicators only [E0].
- The upstream-handoff defect is concrete, but whether it is repaired inside the existing compiler
  or by a new staged-dispatch primitive is an architecture decision, not a research result [C6].
- Durable remote execution may be necessary for the broader “recovered” target, or it may remain an
  adapter boundary. BoundFlow, Orloj and Temporal prove available mechanisms, not the correct local
  product boundary [E2][E4][E5][C9].
- Repository-local operation is evidenced today and desired for portability, but not confirmed as
  immutable. The current implementation remains Windows-operator-specific in part [C1][C8].
- Fail-closed policy is only as strong as the active host interception boundary. A repository cannot
  force unsupported or untrusted clients to load hooks [C5][C7].
- OMA's context journal is close prior art for lineage, but adopting it wholesale could duplicate
  ACI/APT rather than strengthen it [E3][C2].
- Cryptographic attestation may improve tamper evidence or merely decorate best-effort logs; key
  ownership, transparency and authoritative atomicity decide which [E1][E6].
- Negative claims remain bounded to the inspected revisions/surfaces. A later repo version or
  uninspected module can overturn them without invalidating the historical report [E0].
- No downstream discovery document, target-model owner or adoption authority has been named as the
  sole consumer. This report therefore prioritizes questions but cannot promote them to requirements.

## One-line answer to RQ0

Use the repositories as named implementation witnesses for individual mechanisms, not as owners of
generic patterns or proof of novelty. Design the missing producer-output binding locally; evaluate
OMA plan/replay, OMA approval CAS, Temporal's human-only channel, typed recovery components,
Chorus's identity separation and the other bounded witnesses without collapsing their semantics.
Preserve Cyberalchemy's objective/authority/evidence distinctions, fix the current empty-manifest
and observed host-hook gaps first, and keep broader product expansion and code reuse gated by
explicit product and licensing decisions.

[E0]: explorer-evidence.md
[E1]: explorer-evidence.md#1-builderz-labsmission-control
[E2]: explorer-evidence.md#2-boundflowboundflow
[E3]: explorer-evidence.md#3-open-multi-agentopen-multi-agent
[E4]: explorer-evidence.md#4-orlojhqorloj
[E5]: explorer-evidence.md#5-temporal-communitytemporal-agent-harness
[E6]: explorer-evidence.md#6-lf-decentralized-trust-labsgitmesh
[E7]: explorer-evidence.md#7-chorus-aidlcchorus
[E8]: explorer-evidence.md#8-chankovagent-fleet
[C1]: ../../README.md
[C2]: ../../implementations/README.md
[C3]: ../../implementations/server/main.py
[C4]: ../../.agents/skills/register-dispatch/SKILL.md
[C5]: ../../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md
[C6]: ../../implementations/server/runtime/dispatch_workflow.py
[C7]: ../../docs/features/agents-communication-infra/WORK-PACK.md
[C8]: ../../plans/governed-agent-work-infrastructure/PLAN.md
[C9]: ../../plans/autonomous-agent-graph-system/README.md
