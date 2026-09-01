---
node_type: agent-dialogue
status: completed-human-authorized
date: 2026-09-01
topic: continuation-l2-d0
---

# Robot Talks — continuation L2 D0

## Scope and gate

The investigation asked how `TASK-CONT-001` can consume CONF-001 authority without turning a
component-level suspension proof into a production attempt-creation claim. It challenged three
assumptions: that a production predecessor writer was required, that suspension needed a specialized
journal writer, and that partially available official inputs could safely narrow the awaited set.

The user had already authorized autonomous local roadmap execution and use of Robot Talks for these
reversible technical decisions. This was direct multi-agent collaboration, not an ACI governed
dispatch; no dispatch, binding or receipt was created for the discussion.

The chosen decomposition separated two concerns:

- the confirmation/foreign-key auditor tested whether a real predecessor and a specialized writer
  were required to preserve authority and persistence integrity;
- the implementation-layering auditor tested the minimum component claim, existing journal seam,
  deterministic command construction and fail-closed source-fact boundary.

An alternative decomposition by files (`migration`, `service`, `tests`) was rejected because it
would have hidden the disagreement about the strength of the claim across several files.

## Dialogue reconstruction

This reconstruction records positions and responses from the two auditors' direct messages. It does
not invent verbatim quotations.

### Initial positions

The confirmation/foreign-key position initially preferred a real production predecessor attempt,
a specialized suspension writer and a deadline derived from verified audit opening. Its concern was
that a fixture-only predecessor or generic acceptance could weaken the authority and replay proof.

The layering position challenged that premise: `TASK-CONT-001` needs to prove only that the
continuation component consumes confirmed authority and suspends atomically. It does not need to
claim a production attempt factory. A test-only prerequisite may therefore be valid if it traverses
the complete journal-backed attempt lifecycle and does not expose a production symbol.

### Challenge and response

The layering auditor required the harness to accept `requested -> starting -> running -> completed`
through `RuntimeJournal.accept`, finalize a reconstruction snapshot, and link that immutable
snapshot to the terminal attempt fact. A direct seeded terminal row was rejected. With those
conditions, the foreign-key auditor accepted a test-only predecessor and capped the resulting claim
at component/consumer behavior. The attempt event schemas/validators are wired directly to the
journal by `test_agent_continuation.py`; production service symbols and `ACI_SCHEMAS` are not widened.

The layering auditor then argued that generic journal acceptance is sufficient when the service,
not the caller, fixes `scope_key = aci.agent-continuation:<continuation_id>` and
`idempotency_key = suspend@1`. The foreign-key concern was retained as an explicit stop condition:
re-evaluate if a caller controls either value or if another create operation shares the identity.

The initial opening-relative deadline was rejected because verified opening is not part of the
CONF-001 authority consumed by this layer. The accepted rule freezes the deadline at confirmation:
`confirmed_at + wall_clock_seconds`, calculated in UTC. Making opening verification extend that
deadline would introduce new authority.

For official source facts, the auditors considered narrowing `awaited_mapping_ids` when one of the
two inputs was already available. The layering challenge showed that this would silently add mixed
source-state semantics not proved by `TASK-CONT-001`. The accepted rule queries the journal for the
exact two confirmed source-message identities: zero official facts means both mappings remain
awaited in confirmed order; any partial, complete or ambiguous result fails closed for CONT-002.

The auditors also closed a replay/TOCTOU consequence of that rule. A derived-key replay must be
recognized before re-evaluating current official facts. When the continuation already exists, the
service reconstructs the command, event and semantic intent from persisted bytes and invokes
generic acceptance for replay/drift without consulting newer facts. Only a create evaluates
zero-of-two, and the mutation closure revalidates the exact source-message facts inside the same
transaction before inserting. Thus an official fact accepted after suspension does not invalidate
retry of the first receipt, while caller drift, including a supplied handle digest, still conflicts.

The foreign-key discussion converged on migration 013 with isolated runtime-managed tables whose
parents are CONF-001 rows. The legacy `agent_attempts`/`host_workflow_turn_bindings` path remains
unchanged and receives no backfill.

### Consensus

The accepted sequence is:

`L2-D0 -> L2-M13 -> L2-DOM -> L2-CONS -> L2-HAR -> L2-VERIFY`.

The semantic intent is fully service-derived and binds the authority digest, continuation and
dispatch identities, source attempt/turn/seat/instance, both ordered mapping identities, both
awaited identities, snapshot identity/digest, optional provider-handle digest, policy reference and
deadline. Suspension creates one event/receipt unit and zero effects.

The production service may perform read-only SELECTs through `database.connect()` and define the
mutation closure whose SQL runs on the connection supplied by `RuntimeJournal.accept`. It may not
open `database.write()`, commit, or create a second transaction/writer; repository methods are not
moved into `database.py`.

Implementation stops on inconsistent authority/digests, an invalid source attempt or snapshot,
any pre-existing target attempt, any official-source state other than exact zero-of-two, any new
effect, any CONF-001 or legacy mutation, any need for caller-controlled idempotency, or any
CONF/AUTH/baseline regression.

## Follow-up

- [Findings and dispositions](findings.md)
- [TASK-CONT-001](../../development/invoke-runs/20260831-resumable-feedback/plan/work-pack/tasks/TASK-CONT-001.md)
- [L2 readiness](../../development/invoke-runs/20260831-resumable-feedback/plan/READINESS.md)
