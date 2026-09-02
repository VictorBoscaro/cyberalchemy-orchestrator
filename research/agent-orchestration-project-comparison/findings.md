---
title: Agent-orchestration comparison findings
status: research-findings-reviewed
date: 2026-09-01
source: research.md
review_dispatch: 2026-09-01-deep-comparative-agent-orchestration-review
---

# Findings

## Decision surface

The research found bounded implementation witnesses, not a replacement architecture or evidence of
novelty. The immediate priority is to implement a producer-output → consumer-input binding for
staged work: the current turn-zero compiler emits `slots: []`. Declared `connections` express
topology; they are not currently data edges. This research itself required three dispatches to keep
exploration, synthesis and review inputs frozen
([research](research.md#answer-in-one-paragraph); `dispatch_workflow.py:312-324`).

The next strongest follow-ups are approval race/content protection, a human authority channel that
agents cannot exercise, typed recovery components, structural/evidence checks and identity keys
with distinct lifecycles. Each remains a separate mechanism; none may be collapsed into a generic
“governance” feature.

## What changes the roadmap

| Priority | Finding | Classification | Next authority required |
|---|---|---|---|
| P0 | No compiled producer-output → consumer-input binding exists for staged turn-zero work. | **Implemented gap relative to staged synthesis** | Discovery + runtime contract decision. |
| P0 | One observed Codex host build bypassed the intended hook path. | **Known integration gap, host/build bounded** | Fresh host smoke and existing gate closure. |
| P1 | OMA implements plan/checkpoint/replay; Orloj and Temporal supply adjacent resume-state precedents. None demonstrates the exact local manifest contract. | **GO discovery; exact witness gap retained** | Design the local immutable binding and replay contract. |
| P1 | OMA implements approval CAS/content binding; Temporal separates the human channel from parent agents. | **Two GO patterns, not one owned composition** | Governance decision on race protection and authority separation. |
| P1 | Orloj, BoundFlow and Chorus implement different retry, lease, dead-letter and interruption components. | **Conditional GO** | Decide whether durable/remote execution enters scope. |
| P2 | OMA structural receipts and Agent Fleet assertion checks perform different jobs. | **Two GO patterns** | Ensure they extend rather than duplicate ACI/APT. |
| P2 | Chorus strongly distinguishes actor/connection/session/resume identities; GitMesh is adjacent. | **GO pattern, source bounded** | Define local identities and lifecycles; do not copy AGPL code. |
| Later | Multi-tenancy, managed cloud, full SDLC, model gateways, Kubernetes and broad ops UI. | **Outside inspected surface / undecided**, not proven deficiencies | Product authority before architecture work. |
| Blocked | Any code-level compatibility conclusion. | **Receiving-license blocker** | Choose Cyberalchemy license + compatibility/legal review. |

## Comparative conclusions

- **Closest partial peers:** Agent Fleet for a local harness and evidence checks; OMA for runtime
  topology, structural receipts, context lineage and replay.
- **Adjacent operational products:** Mission Control and GitMesh.
- **Execution/runtime references:** BoundFlow, Orloj and Temporal Agent Harness.
- **Application-layer reference:** Chorus.
- **Cyberalchemy’s bounded difference:** a validated confirmation marker; sanctioned
  append/open/close actions; host-mediated digest-bound parent-seat launch; declared
  role/group/connection/final-approver topology; evidence standing; and the broader
  objective-to-authority/evidence relation. No inspected repo showed that whole combination in the
  pinned surfaces. The combination is heterogeneous, partly host-dependent and not a novelty claim.
- **External territory not evidenced in inspected Cyberalchemy planning surfaces:** broad multiuser
  operations, managed cloud, Kubernetes/model gateways, full SDLC/Kanban, recurring tasks,
  GitHub/GitLab integration and provider-specific panes. This is not an exhaustive repository-wide
  negative and does not establish a deliberate permanent boundary.

## Reuse verdicts after the three gates

Named repositories below are observed implementers of components, not owners or inventors of
generic patterns. Proposed combinations belong to this research synthesis. `GO` means “worth a
bounded follow-up,” never “adopt.”

| Candidate | Observed witness / qualification | Gate result | Boundary fit | Verdict / use mode |
|---|---|---|---|---|
| Immutable producer-output → consumer-input binding | Local `slots: []` gap; OMA/Orloj adjacent only | Exact external witness gap; definition sound as local design | High | **REVISE → GO discovery**; design locally |
| Executable plan/replay | OMA IW + focal EO | Witnessed; distinct from cross-seat binding | High | **GO**; reimplement pattern informed by OMA |
| Checkpoint/frozen resume context | OMA, Orloj, Temporal variants | Witnessed with different guarantees | Medium-high | **GO investigate**; compare semantics first |
| Structural role/order receipt | OMA | Witnessed; validates conformance, not content | High | **GO**; reimplement pattern |
| Assertion-support cross-check | Agent Fleet | Witnessed; support is not authority | High if non-duplicative | **GO**; reimplement operational check |
| Approval CAS/content hash | OMA | Witnessed; prevents stale/racing decision, not illegitimate authority | High | **GO hardening study**; local defect still unproven |
| Human-only approval channel | Temporal | Witnessed; authority separation is distinct from CAS | High | **GO**; adopt invariant, design locally |
| Typed failure/recovery components | Orloj, BoundFlow, Chorus, each for different components | Witnessed by component; no single owned package | Conditional | **GO if remote/durable runtime enters scope** |
| Desired-versus-observed reconciliation | Orloj declarations/partial IW | Controller-transition witness gap | Conditional | **INVESTIGATE**, not unqualified GO |
| Authoritative decision record separate from telemetry | BoundFlow partial + local ACI/APT | Separation witnessed; external stable-ID correlation under-witnessed | High | **GO with revision**; design local correlation |
| Distinct actor/connection/run/session/resume keys | Chorus primary; GitMesh adjacent | Chorus bounded witness passes | High | **GO**; reimplement contract, AGPL code blocked |
| Capability-surface restriction with declared enforcement boundary | OMA default-deny; Fleet harness reduction | Witnessed; neither proves OS sandbox or universal host enforcement | High but host-dependent | **GO** defense-in-depth |
| Work-ownership arbitration | Mission claim; GitMesh checkout | Witnessed; separate from backpressure and repair | Conditional | **GO when concurrent work enters scope** |
| Queue admission/backpressure | BoundFlow | Witnessed | Conditional | **GO when workload requires it** |
| Stranded-work reconciliation | Mission and BoundFlow | Witnessed; delivery/idempotency semantics required | Conditional | **GO for asynchronous work** |
| Derived per-run evidence archive | Agent Fleet | Witnessed; prunable and non-authoritative | Medium | **GO** derived view only |
| Drift/scope/task-budget guardrails | Agent Fleet | Witnessed; advisory and authority-parametrized | Medium | **GO investigate**, start advisory |
| Scoped cryptographic attestation | Mission narrow; GitMesh async adjacent; generic prior art | Witnessed narrowly; proves neither authority nor semantic provenance | Undecided | **GO investigate** after key/scope decision |

No candidate is labeled `novel-attempt` because no originality search was performed. No candidate is
`KILL` solely for lack of a concrete job, but immutable cross-seat binding, desired/observed
reconciliation and stable-ID correlation retain exact witness gaps and therefore remain
`REVISE/INVESTIGATE`.

## Guardrails retained

- External claims stop at the pinned revisions and evidence labels in
  [explorer-evidence.md](explorer-evidence.md).
- “Not evidenced” is not “absent”; CI/test evidence is not production deployment evidence.
- Confirmation, runtime approval, authority, receipt, provenance, attestation, evidence standing,
  telemetry and derived archives remain distinct types.
- Cyberalchemy’s built, local-pilot, proposed, open and contested states remain distinct.
- Findings inform discovery and adoption packets; they do not authorize requirements,
  architecture, licensing, code copying or implementation.

## Required next packet

Create a bounded discovery/contract packet for producer-output workflow binding with immutable
source digest, byte/cardinality limits, terminal producer status and replay semantics. Its collapse
test is simple: if a downstream consumer can start with an empty manifest despite a declared staged
dependency, the contract has not solved the observed requirement.

**Answer:** use the repositories as named witnesses for individual mechanisms, not owners of the
local design. Fix staged input binding and the observed host-hook gap first; then evaluate approval,
recovery, identity and evidence mechanisms separately. Keep product expansion and every code-level
reuse decision behind explicit product and licensing authority.
