---
feature: agents-communication-infra
title: W0 closure packet
status: pending-independent-review
date: 2026-07-23
---

# W0 closure packet

## Authored disposition

| Obligation | Authored result | Effective result before reviewer PASS |
|---|---|---|
| SWU-ACI-001 persistence/replay ADR | accepted by prior independent receipt | accepted |
| SWU-ACI-002 compatibility/terminal/snapshot ADR and fixtures | complete | pending |
| B-001 | closure conditions authored | open pending corpus receipt |
| B-002 | closure conditions authored | open pending corpus receipt |
| B-003 W0 contract | schema, drift disposition, guard and named tests frozen | pending corpus receipt; physical proof/cutover open |
| TASK-010 selection | exact `SWU-ACI-APT-VS-001` descriptor prepared | not selected until cross-workpack/root receipt |
| Profile registrations | four canonical definitions and digest manifest prepared | pending |
| Storage/artifact ownership | policy prepared | pending |

## B-003 drift disposition

The historical direct-write/enum drift is a known counterexample to end-to-end EG-1. W0 does not
erase or declare it repaired. The disposition is:

- preserve the audit record;
- prohibit runtime writes to the ledger;
- require the current validated appender for all future opening/close rows;
- require strict exact-row verification before runtime acknowledgement;
- require TASK-020 target-host process, ACL, deployed writer inventory and negative bypass evidence
  before any materializer/cutover.

## Required independent acceptance

The reviewer must recompute the artifact manifest and profile canonical digests, review ADR-002,
fixtures, storage policy, task/descriptor and cross-task status changes, and return `PASS` or
specific findings. The root then records the cross-feature predicate, APT TASK-105 evidence and
owner decisions. This packet cannot self-promote.

## Gate result after a future PASS

Only `mutationTestAuthorization=pass_for_exact_swu` may become true. It permits temporary/test DB
mutation for the descriptor-bound implementation. `localPilotServeEnablement` remains blocked
until implementation evidence and a separate reviewer/root decision. Production, cutover,
materializer, provider execution and external network remain blocked.

