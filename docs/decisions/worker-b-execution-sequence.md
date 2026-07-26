---
status: accepted
date: 2026-07-26
scope: worker-b-execution-sequence
---

# Worker B execution sequence

## Decision question

Which bounded unit may follow the BUS reveal/materialized-input proof without bypassing the
accepted execution authority and opening barrier?

## Evidence

- `SWU-ACI-BUS-DELIVERY-001` intentionally stops with an unclaimed pending effect and zero
  provider/tool starts.
- `SWU-ACI-008` is the accepted work-pack unit for a fake adapter and durable worker loop.
- `StartAgentAttempt` requires `opening.verified` before the sandbox-launch/start effect may be
  released.
- The shared SWU manifest declares `ACI-003` through `ACI-005` as dependencies of `ACI-008`.
- The Phase-A Host Binding -> BUS closing review remains `FIX` until F1-F6 and a completion receipt
  close.

## Options considered

### A - Durable fake-worker route through the accepted barriers

Close Phase A, implement and verify ACI-005, then prepare and execute `SWU-ACI-008`.

- Benefit: proves a real durable consumer while preserving the canonical request, effect and
  opening-authority contracts.
- Cost: the worker proof waits for the Phase-A repair and opening materializer.
- Downstream impact: provider CLI, credentials and production sandboxing remain deferred.

### B - Immediate local worker exception

Allow a local host worker to consume the pending request before `opening.verified`.

- Benefit: faster visible execution.
- Cost/risk: creates a second execution rule that contradicts `StartAgentAttempt`, weakens the
  audit-opening barrier and cannot recompose into the accepted runtime.
- Downstream impact: requires a new exception contract and invalidates existing safety claims.

### C - Jump directly to the first real CLI provider

Advance to TASK-050/SWU-ACI-017 through 020.

- Benefit: proves external provider execution.
- Cost/risk: skips L0/L1 evidence and unresolved sandbox, credential, unknown-effect and resource
  gates.
- Downstream impact: broadens the task into a multi-SWU security and provider-admission program.

## Decision

Option A is accepted. The repository owner approved proceeding after the recommended
`SWU-ACI-008` fake-adapter route was presented. Later inspection exposed the accepted ACI-005
dependency; preserving that dependency is an authority constraint, not a new discretionary choice.

The execution sequence is:

1. close the surviving Phase-A findings and completion evidence;
2. prepare, implement and verify ACI-005;
3. prepare and execute `SWU-ACI-008`;
4. treat a real CLI provider as later TASK-050 work.

## Deferred decisions

- Target-host sandbox implementation for a real provider.
- Credential and resource-limit policy for TASK-050.
- Provider unknown-effect reconciliation beyond the deterministic fake-adapter proof.

