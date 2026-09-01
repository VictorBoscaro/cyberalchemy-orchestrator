# Continuation L2 D0 — findings

## Disposition

All blocker-level tensions were accepted as real and resolved for the bounded L2 component claim.
The user had already authorized autonomous resolution of reversible technical decisions. None of
these decisions authorizes a production attempt writer, continuation resume, effect claiming,
provider work, legacy migration or deployment.

## Tensions and resolutions

| ID | Tension | Evidence | Impact | Disposition |
|---|---|---|---|---|
| D0-T1 | Production predecessor versus component-only proof | Existing `agent_attempts` are rooted through legacy host bindings in `010_agent_reference_delivery.sql`; CONF-001 supplies independent runtime authority in `012_runtime_confirmation.sql`. `T-ACI-CONT1` requires a completed source and finalized snapshot, not a public attempt-creation API. | A production predecessor would widen L2; a seeded terminal row would under-prove it. | Use a test-only fixture that accepts every `AttemptLifecycle` step through `RuntimeJournal.accept`, then finalizes and immutably binds the snapshot. Add no production attempt-writer symbol. |
| D0-T2 | Specialized suspension writer versus generic acceptance | `RuntimeJournal.accept` already owns atomic event/head/mutation/receipt acceptance. `O-CONT-S4` requires stable replay and drift conflict. | Caller-chosen scope/key or shared create identity could invalidate generic replay assumptions. | Service derives `aci.agent-continuation:<continuation_id>` and `suspend@1`; no caller key. Use generic acceptance. Stop and redesign if either discriminator becomes caller-controlled or another create shares the identity. |
| D0-T3 | Opening-relative versus confirmation-relative deadline | CONF-001 evidence ends at `opening_pending`; verified opening is explicitly deferred. `AgentContinuation.deadline` and policy are frozen confirmed inputs. | Opening-relative calculation would add authority not available in L2. | Compute UTC `confirmed_at + wall_clock_seconds`; opening verification does not extend it. |
| D0-T4 | Narrow awaited set versus zero-of-two boundary | The confirmed graph contains exactly two ordered mappings. `T-ACI-CONT2..3` own official contribution resolution and are deferred to CONT-002. | Accepting one-of-two or two-of-two would implement unreviewed mixed-source semantics. | Query exact source-message identities. Zero official facts => both mappings awaited in confirmed order. Any partial, complete or ambiguous state rejects as `continuation_mixed_source_state` and moves to CONT-002. |
| D0-T5 | Reuse legacy FK path versus isolated runtime parents | `009_host_workflow_binding.sql` roots legacy bindings in `dispatch_links`; `010_agent_reference_delivery.sql` roots legacy attempts there. `012_runtime_confirmation.sql` provides `confirmed_dispatches`, `confirmed_turn_graphs` and `continuation_input_mappings`. | Reuse would let compatibility structure masquerade as runtime authority. | Migration 013 creates isolated `runtime_agent_attempts`, `runtime_attempt_snapshot_bindings`, `agent_continuations` and `agent_continuation_mapping_members` with direct CONF-001 parents. No backfill; legacy schema and behavior remain unchanged. |
| D0-T6 | No-SQL service wording versus the existing atomic mutation seam | `RuntimeJournal.accept` supplies one transaction connection to its mutation closure; service already owns application-level reads/orchestration. | A blanket SQL ban would force a new writer or misplaced repository surface; unconstrained SQL could create a second transaction. | Permit read-only SELECTs through `database.connect()` and SQL only inside the journal-supplied mutation closure. Forbid `database.write()`, commit and a second transaction/writer; do not move repository methods to `database.py`. |
| D0-T7 | Current zero-of-two facts versus stable replay | O-CONT-S4 requires byte-identical retry to return the first receipt, while official facts may legitimately arrive after suspension. Generic acceptance replays by the derived scope/key. | Rechecking current facts before replay would turn a valid retry into a mixed-state rejection; checking only before the transaction leaves a create TOCTOU window. | For an existing continuation, rebuild command/event/intent from persisted bytes and attempt derived-key replay before fact evaluation. For create, precheck and revalidate exact source-message facts inside the journal mutation closure before inserts. Later official facts do not invalidate replay; caller drift conflicts. |

## Frozen implementation decisions

- Claim: component/consumer behavior only.
- Attempt prerequisite: test-only, journal-backed full lifecycle, immutable terminal snapshot link.
- Attempt event schemas/validators: wired directly to the journal by the test harness; no production
  service symbol or `ACI_SCHEMAS` widening.
- Command: generic `RuntimeJournal.accept`; derived scope/key; no caller idempotency key.
- Deadline: UTC confirmation time plus confirmed wall-clock budget.
- Awaited inputs: exact zero-of-two only; otherwise fail closed to CONT-002.
- Replay ordering: persisted derived-key replay precedes current-fact evaluation; only create
  prechecks and transactionally revalidates exact zero-of-two before inserts.
- Persistence: migration 013 isolated runtime tables, direct CONF-001 parentage, zero legacy mutation
  and zero backfill.
- Service persistence seam: read-only SELECTs plus journal-supplied mutation-closure SQL only; no
  `database.write()`, commit, second transaction or database-layer repository relocation.
- Suspension: one continuation/event/receipt atomic unit, no effect.

## Stop conditions

Stop rather than widen L2 if authority or digest bindings disagree; the source attempt is not the
completed confirmed author turn; the terminal snapshot is absent or not linked; a target attempt
already exists; official facts are partial, complete or ambiguous; a new effect is needed; CONF-001
or legacy rows would be mutated; scope/key must be caller-controlled; or focused/prior-layer/full
runtime evidence regresses.
