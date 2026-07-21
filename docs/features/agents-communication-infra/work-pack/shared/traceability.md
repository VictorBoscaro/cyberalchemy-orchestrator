# Traceability Matrix

| Requirement/invariant | Task | Primary evidence |
|---|---|---|
| Explicit human confirmation | TASK-000, TASK-030, TASK-080 | command fixtures and legacy-client cutover test |
| Opening verified before any external effect | TASK-020, TASK-030 | crash-boundary and negative execution tests |
| One validated physical writer per authority (EG-1) | TASK-000, TASK-020, TASK-AUDIT-ALIGNMENT | sole-writer guard and materializer receipt |
| Strict write, lenient historical read (EG-2/EG-6) | TASK-020 | golden legacy/appender fixtures |
| Command idempotency and CAS | TASK-010 | duplicate/conflicting-key/concurrency tests |
| Pure deterministic replay | TASK-010, TASK-030 | stable state hashes and no-effect replay spies |
| One logical result and terminal winner | TASK-030, TASK-040 | duplicate/race traces |
| Sealing until reveal | TASK-040 | cross-surface ACL matrix |
| Realtime is projection | TASK-040 | cursor/gap/rebuild tests |
| Adapter is provider-independent | TASK-050, TASK-070 | shared conformance suite |
| Product value justifies complexity | TASK-060 | preregistration and blinded evaluation decision |
| Recipes do not specialize kernel | TASK-080, TASK-AUDIT-ALIGNMENT | kernel branch audit and two-recipe fixture |
| Layer promotion follows evidence | TASK-AUDIT-LAYERING | promotion audit |

## Slice falsifiers

- **L0:** any execution before verified opening, replay-triggered effect, duplicate logical effect,
  non-convergent crash boundary or divergent ledger row treated as success.
- **L1:** sealed content visible before reveal, two terminal winners, unrecoverable SSE gap or hidden
  projection failure.
- **L2:** provider-specific state leaks into kernel, unknown effect presented as success, credential
  leak or unbounded resource consumption.
- **L3:** second provider requires kernel/schema fork, or product-value threshold fails.
- **L4:** adding `research`/`review` requires business-type branches in kernel, or skill/UI retain a
  parallel execution authority after cutover.

