# POLICY-001 persistence pattern inventory

Date: 2026-09-01

Status: bounded architecture evidence; no code-entry authority

## Recommendation

Use a temporary file-backed `RuntimeDatabase` plus the existing `ArtifactStore`, behind an explicitly
test-only lineage harness. Do not add a runtime migration, service/API surface, journal command or
production package export.

The alternatives are weaker:

- in-memory SQLite cannot prove close/reopen durability;
- filesystem artifacts plus a SQLite receipt introduce two persistence resources without an atomic
  cross-resource commit or orphan recovery;
- SQLite BLOBs through `ArtifactStore.prepare()` and `ArtifactStore.finalize(conn, ...)` allow exact
  bytes, receipt and ordered membership to commit inside one `RuntimeDatabase.write()` transaction.

The harness may create exactly two test-only tables in the temporary database: one lineage-receipt
table and one ordered-member table. They must not be added to `MIGRATION_NAMES` or any production
migration.

## Transaction and reopen pattern

1. Create and migrate a temporary file-backed runtime database.
2. Create the two test-only tables locally.
3. Load and validate the seven POLICY-000 vectors before persistence.
4. Prepare every artifact outside the transaction.
5. In one `RuntimeDatabase.write()` transaction, resolve replay/conflict, finalize all prepared
   artifacts, insert one closed non-executable receipt and insert its seven ordered bindings.
6. Expose failpoints after begin, after each artifact, after the receipt, after each binding and
   before commit. Any failure must reopen to the complete unit or none.
7. Fire `after_commit` only after the transaction exits; a lost response must converge on the first
   persisted receipt.
8. Reopen the same SQLite path, reload all members through `ArtifactStore` and reproduce every exact
   body, digest and receipt.
9. Reassert production-parser rejection of the combined oracle and harness fence.

Do not call `ArtifactStore.commit()` for individual members: its per-artifact transaction would
destroy unit-level all-or-nothing behavior.

## Receipt and identity

The closed `aci.execution-policy-synthetic-lineage-receipt@1` receipt should carry only:

- `authority: test-only-non-executable`;
- `synthetic_key`;
- immutable `lineage_identity`;
- seven ordered member content identities;
- canonical `unit_digest`.

It contains no confirmation, Run, plan, request, event, effect, provider, opening or current-fence
claim. Replay rules are:

- same key and same unit digest returns the first receipt;
- same key and changed unit digest conflicts;
- same lineage identity and changed unit digest conflicts;
- same lineage identity and same unit digest converges on the first receipt.

## Proposed write scope

- `implementations/tests/runtime/policy_lineage_harness.py`;
- `implementations/tests/runtime/execution_policy_lineage_oracle_v1.json`;
- `implementations/tests/runtime/test_execution_policy_lineage.py`.

Read-only dependencies are the POLICY-000 fixture/parser and existing runtime database, artifact and
canonical helpers. Migrations, `RuntimeService`, `RuntimeJournal`, API, CLI and exports are forbidden.

## Mandatory zero-row inventory

After success and every failure, only `artifacts` and the two test-only lineage tables may contain
POLICY-001 rows. Authority, plan/request/attempt, event/effect, publication and message tables must
remain empty, including `confirmed_dispatches`, `runs`, `confirmed_turn_graphs`,
`agent_invocation_plans`, `agent_execution_requests`, `agent_attempts`, `command_receipts`, `events`,
`aggregate_heads`, `effect_intents`, `sandbox_launch_effects`, `publication_candidates`,
`publication_receipts` and `messages`.

## Repository evidence

- design obligations: `TECH-POLICY-D0.md`, implementation layering and POLICY-001 vectors;
- SQLite transaction/reopen: `implementations/server/runtime/database.py`;
- content-addressed BLOB integrity: `implementations/server/runtime/artifacts.py` and migration 002;
- atomic finalize/replay pattern: `implementations/server/runtime/journal.py`;
- reopen/conflict/lost-response precedents:
  `implementations/tests/runtime/test_runtime_confirmation.py`;
- seven exact source vectors:
  `implementations/tests/runtime/execution_policy_oracle_v1.json`.

This inventory removes the technical seam ambiguity. POLICY-001 still requires its own normative
DomainSpec amendment, work-pack descriptor, exact readiness receipt and independent review before
code entry.
