---
node_type: agent-dialogue
status: completed-human-authorized
date: 2026-09-01
topic: continuation-c2-split
---

# Robot Talks — continuation C2 split

## Scope and strategy

The investigation asked which CONT-002 work is technically decidable from the current confirmed
authority and which work requires new product authority. It challenged the assumptions that opening
materialization could be simulated safely with a temporary ledger and that HEADS, BUS, opening,
resume and worker behavior belonged in one implementation unit.

The user had already authorized autonomous local roadmap decisions and Robot Talks. The discussion
was direct multi-agent collaboration, not an ACI governed dispatch; it created no dispatch, binding
or receipt.

The selected decomposition separated alignment/authority from implementation layering. The
alignment concern traced which bytes and identities are present in CONF v1. The layering concern
tested whether each proposed foundation produces useful independent evidence without widening the
claim. A file-based decomposition was rejected because it would distribute product defaults across
migrations, service and tests without exposing the authority gap.

## Dialogue reconstruction

This reconstruction preserves the auditors' positions, criticism, response and consensus without
presenting invented verbatim quotations.

### Initial position

The initial sequencing allowed OPEN and BUS before the product gate by replacing the external ledger
with a temporary local ledger. It also treated Run/Group heads as preparatory schema within the same
CONT-002 implementation arc.

### Criticism

The alignment auditor showed that a temporary ledger removes an external side effect but does not
supply the missing canonical opening bytes. CONF v1 lacks the total 0.6.4 opening-row projection,
including concrete prompts, revision instruction, role/task/provider references and resource,
sandbox and execution-fence policies. Materializing or verifying opening before those decisions
would invent authority.

The layering auditor challenged HEADS as potential dead schema. It is useful before the product
gate only if its own work pack proves total reducers, exact CAS/races/reopen and a fail-closed fence.
No API or service may turn caller evidence into `ready`. A verified positive used by the test harness
must be labeled component evidence, not opening-materialization evidence.

### Reply and convergence

The initial OPEN-first proposal was withdrawn. The auditors accepted a technical/product split:
technical D0 freezes deterministic bus identities, group normalization, official event types,
four-entry ordering, derived runtime IDs, non-retryable `agent_resume`, atomic multi-head behavior
and CONF-derived response/adapter references; product supplies the missing concrete bytes and policy
values.

HEADS-001 was retained before BUS because reducers, head CAS and the closed execution fence provide a
useful component proof even without a positive production writer. Its migration is isolated and its
tests use generic journal/database seams directly. BUS-001 then proves official publication from
preallocated identities with completed attempts created only as journal-backed test prerequisites.

### Consensus sequence

`C2-TECH-D0 -> C2-HEADS-001 -> C2-BUS-001 -> HARD PRODUCT GATE -> C2-OPEN -> positive Run transition -> C2-RESUME -> C2-WORKER -> C2-VERIFY`

The hard stop after BUS forbids real opening materialization/verification, Run `ready`, effective
input finalization, `agent_resume` creation and adapter calls until PRODUCT-PASS. Because filling the
missing values changes confirmed authority, executable product work requires a new dispatch
identity/CONF v2 and a new human confirmation; CONF v1 remains an immutable fixture and component
proof.

## Follow-up

- [Findings](findings.md)
- [C2 technical decision](../../development/invoke-runs/20260831-resumable-feedback/plan/C2-TECH-D0.md)
- [CONT-002 umbrella task](../../development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-002.md)

