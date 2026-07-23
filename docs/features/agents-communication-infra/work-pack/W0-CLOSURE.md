---
feature: agents-communication-infra
title: W0 closure packet
status: PASS-independent-review-cycle-5-of-5
date: 2026-07-23
---

# W0 closure packet

## Authored disposition

| Obligation | Authored result | Effective result |
|---|---|---|
| SWU-ACI-001 persistence/replay ADR | accepted by prior independent receipt | accepted |
| SWU-ACI-002 compatibility/terminal/snapshot ADR and fixtures | complete | accepted by Stage-A reviewer receipt |
| B-001 | closure conditions authored | closed |
| B-002 | closure conditions authored | closed |
| B-003 W0 contract | schema, drift disposition, guard and named tests frozen | frozen; physical proof/cutover open |
| TASK-010 selection | exact `SWU-ACI-APT-VS-001` descriptor prepared | selected only inside the exact named SWU |
| Profile registrations | four canonical definitions and digest manifest prepared | four exact registration receipts PASS |
| Storage/artifact ownership | policy prepared | independent storage receipt PASS |

## B-003 drift disposition

The historical direct-write/enum drift is a known counterexample to end-to-end EG-1. W0 does not
erase or declare it repaired. The disposition is:

- preserve the audit record;
- prohibit runtime writes to the ledger;
- require the current validated appender for all future opening/close rows;
- require strict exact-row verification before runtime acknowledgement;
- require TASK-020 target-host process, ACL, deployed writer inventory and negative bypass evidence
  before any materializer/cutover.

## Independent acceptance

Rawls recomputed the artifact manifest and profile canonical digests, reviewed ADR-002, fixtures,
storage policy, task/descriptor and cross-task status changes, and returned PASS at cycle 5/5.
The exact receipt is
[`ACI-STAGE-A-PASS-RAWLS-2026-07-23`](../reviews/2026-07-23-stage-a-freeze/reviewer-receipt.json).

## Gate result

`mutationTestAuthorization=pass_for_exact_swu` permits temporary/test DB
mutation for the descriptor-bound implementation. `localPilotServeEnablement` remains blocked
until implementation evidence and a separate reviewer/root decision. Production, cutover,
materializer, provider execution and external network remain blocked.
