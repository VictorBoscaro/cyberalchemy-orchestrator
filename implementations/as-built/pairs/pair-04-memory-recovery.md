# Pair 04 — Memory and recovery

## Executive answer

The runtime database has credible, tested local convergence and conservative recovery. Commands commit as one unit, exact retries recover the committed result, corrupt or incomplete journal groups fail closed, projections can be rebuilt, and verified backups can be retained and restored.

The harness as a whole does not yet have one recoverable history. Official YAML, SQLite, repository or external artifacts and source state, plus process-local Control Center drafts, are joined by retry conventions and operator procedure rather than one durable recovery boundary. If the bridge writes YAML and stops before recording the matching runtime facts, that mismatch can remain indefinitely unless an operator repeats the exact operation.

## Failure matrix

| Failure phase | Durable state | Recovery action | Convergence proof | Uncovered boundary |
|---|---|---|---|---|
| Before SQLite commit | Prior official runtime state only | Retry from the prior head | Transaction rollback and focused failpoint test | Actual host interruption receipt |
| After SQLite commit, before caller receipt | Accepted group and persisted result | Repeat the exact command | Exact retry returns persisted result; divergent retry conflicts | Generic result JSON has no independent integrity digest |
| Projection failure or restart | Journal remains authoritative; read model may lag | Startup preflight catch-up or explicit catch-up/rebuild | Projector failure and deterministic rebuild tests | Crash between rebuild reset and catch-up; an availability window, not known data loss |
| SQLite corruption | Candidate is rejected and preserved | Restore a separately verified backup at a new path | Tamper, profile substitution, backup and retirement tests | Automatic repair and production disaster recovery |
| Backup interruption | Source remains; incomplete destination is unpublished | Retry to a new destination | Online-backup cleanup test | Power loss and off-machine retention |
| Retirement | Stopped source and separately verified, structurally matching backup | Recover from the moved source or backup | Normal and denial paths tested | Crash around the final move; content-complete equality |
| YAML append, then process interruption | Official YAML may exist without matching runtime facts | External exact retry | YAML-only failpoint retry avoids duplicate row and finishes the call | Automatic discovery/reconciliation and later bridge failpoints |
| Whole-harness restore | No single synchronized recovery set | Operator assembles component versions | None | YAML, SQLite, repository/external artifacts, and source state are not bound to one checkpoint |
| Control Center restart | Official runtime survives; local previews do not | Recreate drafts/preferences manually | In-memory implementation is explicit | Persistence of unfinished human intent |

## What is built

- One transactional acceptance boundary inside SQLite, with exact-retry idempotency and divergent-retry rejection.
- A journal verifier that rejects incomplete, duplicate, orphaned, corrupt, schema-divergent, or endpoint-mismatched event groups.
- Derived APT views that fail on lag and can catch up or rebuild from verified journal groups.
- Conservative database verification, online backup to a new path, and recoverable retirement after stop and backup checks.
- A YAML-first bridge whose exact retry can finish the two-store operation without duplicating the YAML row.

## What remains open and what it buys

1. Add durable bridge reconciliation state and startup scanning. This buys automatic discovery and completion or escalation of orphaned YAML/runtime work.
2. Bind YAML, SQLite, repository or external artifacts, and source state into one signed recovery manifest. This buys a known whole-harness recovery point.
3. Digest canonical command results and recompute aggregate state from events. This buys semantic corruption detection, not only structural integrity.
4. Operate scheduled, retained, off-machine, encrypted backups and rehearse restore against explicit recovery objectives. This buys predictable survivability.
5. Persist Control Center preview state behind an explicit promotion boundary. This buys reconstruction of unfinished human reasoning without making drafts authoritative.
6. Seal the executable YAML appender in the source manifest. This buys reproducibility of the bridge continuity proof.

## Evidence and limits

Eighteen unique focused unittests passed from isolated temporary stores under `C:/tmp/cyberalchemy-as-built/pair-04-memory-recovery`. No real runtime store, product code, or product documentation was changed. The executable YAML appender used by bridge tests is absent from the current source manifest, so the bridge proof is not yet fully reproducible from the sealed corpus.

The worker and reviewer completed one robot-talk round and reached agreement. Missing result-receipt and reducer checks are established from code; no observed corruption is claimed. Uncovered bridge failpoints are missing proof, not known non-convergence.

## Document drift

- The recovery runbook refers generically to receipt-digest failure, but generic command result JSON has no independently checked digest.
- The root infrastructure plan still says the durable journal and store are not built. A bounded local journal/store is now built and tested; whole-harness recovery is still open.
