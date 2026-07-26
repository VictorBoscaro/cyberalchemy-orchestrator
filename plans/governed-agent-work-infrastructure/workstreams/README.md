---
tags: [plans, workstreams, execution, delegation-envelope, work-pack, index]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.1
last_updated: 2026-07-26
owning_plan: plans/governed-agent-work-infrastructure/PLAN.md
---

# Governed Agent Work Infrastructure — workstreams

## 1. What is this?

Bounded execution artifacts under this Plan. Unlike the essays (which argue) and the subplan
(which researches), everything here exists to authorize, scope, or record a concrete piece of
work: decision gates, layering choices, context and work packs, dispatch routes, and the signed
envelopes that license delegated execution.

## 2. Business Context

This Plan's work is carried out by agents, and this repository does not let an agent act on
intent alone — it has to act inside a recorded scope. That is what most of these files are.
The three `delegated-execution-envelope@1` documents each pin an objective together with the
verbatim user confirmation that issued it, and one of them,
`scout-aci-apt-delegated-execution-envelope.json`, is the envelope referenced by the durable
authorization receipt at
[`../../../.codex/delegation-receipts/scout-aci-apt-20260725-v1.json`](../../../.codex/delegation-receipts/scout-aci-apt-20260725-v1.json).
The `agent-reference-lineage-*` set is one workstream carried through the full chain — decision
gate, implementation layering, context pack, work pack — with its layering choice bound to
`selected_option: A` of
[`../../../docs/decisions/host-agent-dispatch-input-binding.md`](../../../docs/decisions/host-agent-dispatch-input-binding.md).

## 3. Why it matters

The parent [`../PLAN.md`](../PLAN.md) indexes only **one** of the ten files below
(`brokered-agent-launcher-capability-bootstrap.md`). A reader following the canonical Plan
contract from [`../../README.md`](../../README.md) will therefore never learn that the other
nine exist — including the three execution envelopes and the entire agent-reference-lineage chain.
This index closes that gap. Two statuses also need reading carefully: the L0 work pack is
`implementation-complete-review-pending` (built, not yet reviewed), and the brokered-launcher
workstream records `authority_resolution.status: unknown` with a note that no durable governing
authority receipt was found when it was migrated — it is `active` but inert as a binding route.

## 📁 Navigation

- **[agent-reference-lineage-decision-gate.md](agent-reference-lineage-decision-gate.md)**:
  `node_type: decision-record`, `status: pass`, v0.1.0. The gate result for
  `target_scope: agent-reference-lineage-l0`.
- **[agent-reference-lineage-implementation-layering.md](agent-reference-lineage-implementation-layering.md)**:
  `node_type: plan-workstream`, `status: draft`, v0.1.0, `scope: capability`. Binds
  `authority.decision: docs/decisions/host-agent-dispatch-input-binding.md` with
  `selected_option: A`.
- **[agent-reference-lineage-l0-context-pack.md](agent-reference-lineage-l0-context-pack.md)**:
  `node_type: context-pack`, `status: draft`, v0.1.0. `task_ref: SWU-ARL-L0-001`, `mode: lean`,
  `strict: true`, `handoff_pack: none`, `runtime_handoff: false`.
- **[agent-reference-lineage-l0-work-pack.md](agent-reference-lineage-l0-work-pack.md)**:
  `node_type: work-pack`, `status: implementation-complete-review-pending`, v0.2.0.
  `selected_layer: L0`, `execution_mode: local`, `runtime_handoff: none`.
- **[brokered-agent-launcher-capability-bootstrap.md](brokered-agent-launcher-capability-bootstrap.md)**:
  `node_type: plan-workstream`, `status: active`, v0.2.1, `authority: proposal-only`.
  `authority_resolution.status: unknown` — migrated from feature-local storage with no durable
  governing-authority receipt found. The only file here indexed by `PLAN.md`.
- **[host-bus-aci005-dispatch-route.md](host-bus-aci005-dispatch-route.md)**: `status: active`,
  2026-07-25. The operating rule requiring the primary orchestrator plus one independent
  read-only readiness helper to classify a target before every mutation-capable dispatch, with
  the evidence-state → route table.
- **[host-bus-phase-a-review-envelope.json](host-bus-phase-a-review-envelope.json)**:
  `schema: delegated-execution-envelope@1`, `envelope_id: host-bus-phase-a-review-20260725`,
  version 1, confirmed 2026-07-26. Objective: run a persisted read-only closing review of the
  current Host Workflow Binding and ACI BUS reveal/materialized-input Phase-A seam, producing
  verified change requests or a KEEP verdict.
- **[reference-scout-bibliography-research-proposal.json](reference-scout-bibliography-research-proposal.json)**:
  `schema: concrete-dispatch-proposal@1`, `dispatch_type: research`,
  `dispatch_id: 2026-07-25-reference-scout-bibliography-research`. Carries a
  `post_dispatch_relocation` clause moving the accepted research under the Agent Provenance
  Telemetry feature, with a launch-time proposal digest.
- **[repository-leverage-priority-delegated-execution-envelope.json](repository-leverage-priority-delegated-execution-envelope.json)**:
  `schema: delegated-execution-envelope@1`, `envelope_id: repository-leverage-priority-20260725`,
  version 1. Objective: recommend the single next bounded capability with the greatest reusable
  construction leverage. Records the issuing user's verbatim confirmation.
- **[scout-aci-apt-delegated-execution-envelope.json](scout-aci-apt-delegated-execution-envelope.json)**:
  `schema: delegated-execution-envelope@1`, `envelope_id: scout-aci-apt-20260725`, version 1.
  Objective: reconcile Reference Scout ownership across ACI and APT, establish bibliography and
  reference-logging semantics, update accepted specs and plans, and implement the resulting
  bounded local-pilot tasks. Bound to the receipt in `.codex/delegation-receipts/`.

## Connections

| Edge | Target |
|---|---|
| owned-by | [`../PLAN.md`](../PLAN.md) — indexes only `brokered-agent-launcher-capability-bootstrap.md` |
| governed-by | [`../../../docs/decisions/host-agent-dispatch-input-binding.md`](../../../docs/decisions/host-agent-dispatch-input-binding.md) — `selected_option: A` |
| authorized-by | [`../../../.codex/delegation-receipts/scout-aci-apt-20260725-v1.json`](../../../.codex/delegation-receipts/scout-aci-apt-20260725-v1.json) — receipt for the scout envelope |
| sibling-of | [`../subplans/`](../subplans/), [`../essays/`](../essays/) — research and system views under the same Plan |
