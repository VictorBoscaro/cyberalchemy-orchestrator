# C2-TECH-D0 — technical/product split for CONT-002

## Decision result

`PASS` for the technical split; `BLOCK` for the complete CONT-002 product path. The accepted sequence
is:

`HEADS-001 -> BUS-001 -> PRODUCT-PASS -> OPEN -> positive Run transition -> RESUME -> WORKER -> VERIFY`.

[Robot Talks evidence](../../../../robot-talks/2026-09-01-continuation-c2-split/findings.md) records
the cross-layer challenge and disposition.

## Technically closed decisions

1. Derive runtime publication `source_message_id` from its exact confirmed mapping.
2. Normalize group identity deterministically from the confirmed graph.
3. Use typed official author/reviewer acceptance events together with
   `attempt.result_accepted`.
4. Materialize exactly four ordered effective-input entries: reconstruction base, official prior
   author output, official reviewer output and revision instruction. Any wrapper belongs in separate
   metadata/reference.
5. Derive attempt, plan, request, effect and event IDs from confirmed authority and canonical input.
6. Treat `agent_resume` as non-retryable.
7. Advance dependent Run/Group heads through one atomic multi-head CAS.
8. Derive the author-turn-1 response schema and adapter/model/tool references from confirmed
   authority, never caller defaults.

## HEADS-001 boundary

HEADS-001 is a foundation/component proof only. Migration 014 adds isolated
`runtime_run_heads` and `runtime_group_heads` with direct confirmed Run/graph parents, no backfill and
no legacy mutation. A pure `run_group.py` owns total reducers. Generic journal/DB test harnesses
prove exact CAS, races, atomic multi-head behavior and reopen.

No production positive writer, opening materializer, service or API is added. Harness-only verified
opening evidence may exercise a positive transition but is explicitly not proof that opening can be
materialized. `opening_pending` and `reconciliation_required` never make work eligible and never
release or claim provider/tool/start effects.

## BUS-001 boundary

BUS-001 is a later, separately readied migration 015 component proof. It uses preallocated message
identity and journal-backed completed attempt prerequisites created only in tests to prove candidate
to receipt to official events/message. It does not create an initial attempt writer, effective input,
effect or adapter.

## Product gate

PRODUCT-PASS must provide exact bytes/refs/digests for prompts and revision instruction; role/task
and provider references; resource, sandbox and execution-fence policies; and every field of the
canonical opening row. Those values change confirmed authority. Real execution therefore needs a
new dispatch identity/CONF v2 and a new human confirmation, preserving CONF v1 unchanged.

## Hard stop

After BUS-001, stop before real opening materialization/verification, Run `ready`, effective-input
finalization, `agent_resume`, effect claim/release or adapter invocation. CONT-002 remains blocked
until PRODUCT-PASS and the later exact work packs/readiness receipts exist.

