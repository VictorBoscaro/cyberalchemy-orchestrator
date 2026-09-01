# Investigator 03 — Slicing and verification

## 1. Key Findings

- **The smallest code SWU that can precede `TASK-CONT-001` is a durable confirmation-authority
  writer, not any continuation behavior.** It should accept one already-resolved, authenticated
  `runtime-managed` confirmation; atomically finalize the approved source/spec authority; create
  exactly one `ConfirmedDispatch` and one `Run`; persist the expanded three-turn graph, one
  preallocated continuation identity, and exactly two ordered `ContinuationInputMapping` rows;
  append `run.created` and `audit_opening.requested`; persist the opening effect intent; and return
  one stable receipt. It must stop in `opening_pending`: no audit-ledger append, agent start,
  provider call, bus read, suspension, or continuation is in this SWU. **Specified:**
  `specs/operations.md:55-103` defines confirmation, idempotency, the two events, and the opening
  intent; `specs/domain.md:20-37,178-203` defines the immutable authority and confirmation-frozen
  mappings; `specs/workflows.md:164-171` fixes the three nodes, two execution edges, two official
  inputs, and their order. **Implemented:** no such writer exists: the migration manifest ends at
  `011_bus_reveal_delivery.sql` (`implementations/server/runtime/database.py:14-26`), and the
  runtime event registry contains neither confirmation event
  (`implementations/server/runtime/service.py:61-92`).

- **A small contract/golden-vector closure must be reviewed before the writer code SWU; the current
  documents state the semantic outcome but do not yet provide an executable expansion contract.**
  `DispatchSpec.group_graph` is only constrained as a finite object
  (`specs/domain.md:622-631`), while continuation and message identities are required to be
  deterministic (`specs/domain.md:196-203`). No reviewed projection specifies the exact admitted
  JSON fields, canonical identity inputs, ID namespace/version, or binding-digest projection.
  Moreover, the confirmation interface says the server compiles verified pending bytes into a
  `DispatchSpec` (`specs/interfaces.md:46-60`), while architecture explicitly says no v1
  candidate-to-confirmation mapping exists (`specs/architecture.md:259-264,270-278`). The minimum
  pre-code evidence is therefore one canonical admitted confirmation fixture plus golden expected
  bytes/digests/IDs for `ConfirmedDispatch`, `Run`, the three turns, the continuation, and both
  mappings, with malformed and drift mutations. Without it, two implementations can both satisfy
  the prose yet derive incompatible authority.

- **The existing continuation work pack must change before implementation begins.** The durable
  choice is closed in the ledger (`.craft/ledger.yml:340-369`), but `DECISION-GATE.md:40-42` still
  says the A/B choice is open; `TASK-CONT-001-DRY-RUN.md:54-59` says the gate passed and has zero
  blockers, while `READINESS.md:5-11,28-36` correctly blocks code until the writer is planned and
  reviewed. `TASK-CONT-001.md:27-45` also reserves migration `012` and tells suspension to consume
  “confirmed fixture data.” The prerequisite should become a named task/wave before W1, take the
  next migration number (`012`), and force `TASK-CONT-001` to `013`; the fixture language should be
  replaced with a query against writer-created authority. These are planning corrections, not
  runtime implementation.

- **The writer evidence package needs a confirmation-specific atomicity matrix, not merely
  `T-ACI-AUTH1`.** `T-ACI-AUTH1` currently proves legacy rejection, one dispatch/run pair, and
  identical replay (`TEST-SPEC.md:679-686`), but it does not assert graph expansion, exactly two
  mappings, source-message preallocation, opening-intent atomicity, restart durability, or
  lost-response recovery. The existing journal exposes the right transaction failpoint spine:
  validation/artifacts/events (`implementations/server/runtime/journal.py:145-188`), head/mutation
  (`journal.py:255-322`), receipt/commit/after-commit (`journal.py:323-353`); the established test
  pattern checks every table returns to its exact baseline and separately checks after-commit retry
  convergence (`implementations/tests/runtime/test_agent_reference_delivery.py:314-379`). The new
  matrix should cover valid runtime confirmation, legacy/no-write, missing or mismatched digest and
  principal, required schema/capability-resolution failure, same-key/same-digest replay,
  same-key/different-digest conflict, same-dispatch/different-authority conflict, every internal
  failpoint, after-commit retry, database reopen, and a consumer query proving the IDs come from the
  persisted graph rather than caller fields.

- **Acceptance can be focused, but it cannot support an unqualified feature-wide PASS.** The
  recorded pre-mutation baseline is 152 tests with one failure and 26 errors caused by unrelated
  Stage-E/old-fixture drift (`plan/BASELINE.md:9-24`). Its explicit policy is: every new focused
  test passes, the full suite adds no new failure/error signature, and continuation work does not
  repair unrelated baseline files (`plan/BASELINE.md:26-34`). The writer should therefore be
  accepted only with: migration apply/reopen evidence; the complete focused confirmation suite;
  focused `test_stage_b` remaining 19/19; a machine-readable or enumerated before/after full-suite
  signature comparison; `git diff --check`; traceability from O-CONF-1..5, O-CONT-S5,
  WF-CONT-01/07/08, and expanded `T-ACI-AUTH1`; and an independent reviewer verdict. Reopening
  `TASK-CONT-001` requires those focused checks and the writer/graph evidence to pass, while the
  feature-wide result remains FLAG/BLOCK until the external baseline drift is repaired.

## 2. Gaps or Inconsistencies

- There is no canonical schema or golden vector for the accepted bounded turn graph, nor a specified
  identity derivation for its turns, continuation, mappings, source messages, and
  `confirmed_binding_digest` (`specs/domain.md:178-203,622-631`). This is a specification gap, not
  merely missing code.
- `ConfirmRuntimeDispatch` promises `run.created`, `audit_opening.requested`, and an opening effect
  in one transaction (`specs/operations.md:87-93`), but the runtime has no generic opening-effect
  table or confirmation schemas; its only visible launch outbox is the later
  `sandbox_launch_effects` table (`migrations/010_agent_reference_delivery.sql:39-46`). The
  prerequisite needs a bounded audit-opening intent record, but not the external materializer.
- The TEST-SPEC does not yet make confirmed graph/mapping creation a confirmation acceptance
  criterion. `T-ACI-CONT1` assumes a preallocated graph and only tests that suspension rejects a
  substituted identity (`TEST-SPEC.md:247-259`); `T-ACI-AUTH1` stops at the dispatch/run pair
  (`TEST-SPEC.md:679-686`).
- The plan has mutually incompatible status claims: current readiness is BLOCK
  (`READINESS.md:5-11`), the dry-run says PASS/zero blockers
  (`TASK-CONT-001-DRY-RUN.md:54-59`), and the decision gate still requests a choice already closed
  in the ledger (`DECISION-GATE.md:40-42`; `.craft/ledger.yml:340-352`).
- `TASK-CONT-001` currently reserves migration `012` and accepts “confirmed fixture data”
  (`TASK-CONT-001.md:27-41`), which would either collide with the prerequisite or preserve the
  rejected synthetic-authority path.

## 3. Local Tensions

- **Confirmation semantics versus executable source:** the API contract claims server-side
  pending-sheet-to-`DispatchSpec` resolution (`specs/interfaces.md:46-60`), but architecture says
  that mapping is not specified (`specs/architecture.md:259-264,270-278`). A writer cannot prove a
  real JSON-to-authority path until one bounded input/projection is selected and frozen.
- **Confirmation operation versus continuation authority:** O-CONF creates the dispatch/run and
  opening intent (`specs/operations.md:77-93`), while O-CONT-S5 assumes the same confirmation also
  preallocated the continuation graph (`specs/operations.md:316-326`). The graph is not an explicit
  O-CONF postcondition, so the prerequisite's atomic unit is currently inferred across documents.
- **Reviewable slice versus eventual end-to-end flow:** the smallest writer should end at a durable
  unclaimed audit-opening intent and `opening_pending`; requiring the external materializer in the
  same SWU would mix authority creation with cross-store reconciliation. Conversely, omitting the
  intent would violate O-CONF and create an authority that cannot progress.
- **Focused acceptance versus repository health:** the baseline policy allows a bounded SWU to pass
  with no new signatures (`BASELINE.md:26-34`), but the same document correctly forbids an
  unqualified feature-wide PASS. The readiness record must name which result is being asserted.
- **Prior topology versus current immediate work:** the work pack requires two read-only auditors,
  one coder, and a different verifier per mutation SWU (`WORK-PACK.md:69-75` and
  `TASK-CONT-001.md:65-69`). This Robot-Talks report can inform the new task, but cannot substitute
  for its pre-code contract review or post-code independent verification.

## 4. Questions for Synthesis

1. Should synthesis require a separate non-code `CONF-000` contract/golden-vector review before
   authorizing the `CONF-001` writer, or can both be one governed work item with a hard internal
   review gate before code?
2. What exact canonical input is admitted for the first chat-driven confirmation: a newly specified
   bounded pending-sheet/`DispatchSpec` projection, or already finalized `DispatchSpec` bytes plus
   independently verified source bytes? The current architecture does not support claiming both.
3. Is the exit boundary agreed as “durable opening intent in `opening_pending`,” with the actual
   `AuditLedgerMaterializer` explicitly deferred, or is materializer execution required before
   `TASK-CONT-001` can consume the graph?
4. Which versioned deterministic derivation should govern `run_id`, turn IDs, `continuation_id`, both
   `mapping_id`s, both `source_message_id`s, and `confirmed_binding_digest`, and where will its
   golden vector be normative?
5. Will the work pack be amended so the prerequisite owns migration `012`, `TASK-CONT-001` moves to
   `013`, its fixture shortcut is removed, and its readiness exit explicitly requires a query that
   rejects caller/legacy authority?
