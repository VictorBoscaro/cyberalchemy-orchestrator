# Local-pilot operator and recovery runbook

Status: bounded Stage-C procedure. This does not authorize production serving,
external binding, automatic agent launch, or dispatch-ledger replacement.

## Invariants

- Bind only to `127.0.0.1` and retain the existing Stage-C opt-in and receipt gates.
- Treat `telemetry/agents/subagents-dispatch.yaml` as the strict legacy dispatch
  snapshot while that boundary remains configured. Backup and retirement helpers
  never write it.
- Keep the runtime database, its backups, and retired copies owner-readable only.
- Never copy a live WAL database with a filesystem copy. Use SQLite's backup API.
- Never overwrite a backup or retirement destination.
- Retirement is a recoverable move, not deletion. Artifact tombstoning is a
  separate, currently unauthorized operation.

## Start and stop

Start from the repository root with an explicit dedicated database:

```powershell
$env:ACI_LOCAL_PILOT_ENABLED='1'
python -m implementations.server.runtime serve --local-pilot `
  --host 127.0.0.1 --port 8766 `
  --database C:\absolute\path\pilot.sqlite3 `
  --ledger C:\absolute\path\repo\telemetry\agents\subagents-dispatch.yaml
```

A successful
preflight verifies receipts, the strict ledger bytes, migrations, profiles,
journal integrity, and the APT projection before the socket opens.

Stop the process normally. Retirement requires an explicit `confirmed_stopped`
assertion, checkpoints the WAL, and fails closed if the database is busy or WAL/SHM
sidecars remain afterward.

## Verify

From the repository root:

```powershell
python -m implementations.server.runtime verify-local-pilot-database `
  --database C:\absolute\path\pilot.sqlite3 `
  --repo-root C:\absolute\path\repo
```

Verification checks the immutable migration manifest, SQLite policy and foreign
keys, complete accepted-command groups, aggregate heads, the exact four local
profiles, and the APT projection watermark. Any failure removes the database
from the recovery candidate set; preserve it for investigation.

## Back up and restore

Create a new, non-existing destination:

```powershell
python -m implementations.server.runtime backup-local-pilot-database `
  --source C:\absolute\path\pilot.sqlite3 `
  --destination C:\absolute\path\backups\pilot-YYYYMMDD-HHMMSS.sqlite3 `
  --repo-root C:\absolute\path\repo
```

The helper uses SQLite's online backup API, verifies the resulting database, and
only then atomically publishes it at the destination. Record the returned SHA-256
and journal identity in the operator log.

To restore, keep the failed database untouched, copy the verified backup to a new
dedicated path using the same helper, verify that new path, and start the pilot
with that explicit database. Do not overwrite an existing database in place.

## Retire

Retirement requires a stopped pilot and a separately verified matching backup:

```powershell
python -m implementations.server.runtime retire-local-pilot-database `
  --source C:\absolute\path\pilot.sqlite3 `
  --destination C:\absolute\path\retired\pilot-YYYYMMDD-HHMMSS.sqlite3 `
  --verified-backup C:\absolute\path\backups\pilot-YYYYMMDD-HHMMSS.sqlite3 `
  --repo-root C:\absolute\path\repo `
  --confirmed-stopped
```

The source and backup must have the same migration version, event count, final
event identity, and command-receipt count. The source is moved to the explicit
retirement path; both it and the backup remain recoverable.

## Incident handling

On integrity, receipt-digest, profile, projection, or strict-ledger failure:

1. Do not reopen serving and do not edit the database or ledger.
2. Preserve the database plus any WAL/SHM sidecars as a single incident set.
3. Record paths, timestamps, the failing check, and any returned receipt.
4. Restore only from a separately verified backup to a new dedicated path.
5. Re-run the full local-pilot preflight before opening the loopback socket.

## Stale dispatch-appender lock

The appender uses the exclusive lock
`telemetry/agents/subagents-dispatch.yaml.append.lock`. The JSON lock record identifies its schema,
PID, creation time, and ledger. A lock can remain after forced termination or timeout, and its
presence intentionally blocks every append.

1. Preserve the lock bytes and record its SHA-256, timestamps, and resolved path.
2. Parse the lock only as evidence; if its schema or ledger differs from the expected exact values,
   stop and investigate.
3. Check the recorded PID. Confirm that no process with that PID exists and that no active Node
   process is running the exact `append-dispatch.cjs` against this repository. PID absence alone is
   insufficient if process identity is uncertain or the PID may have been reused.
4. If a writer is active or identity is uncertain, do not move or remove the lock.
5. Once absence is established, move the lock (do not delete it) to an owner-readable incident
   directory outside `telemetry/agents/`, preserving its filename plus a UTC timestamp.
6. Re-run the supported bridge operation. The appender creates a fresh exclusive lock, validates
   the complete ledger, appends at most one exact row, fsyncs, and releases the lock on normal
   completion.

Never edit the ledger to compensate for a stale lock. If the prior writer might have reached the
append, retrying the exact bridge record is the supported idempotent recovery.

These procedures intentionally do not implement artifact tombstoning, physical
erasure, production cutover, or external authority recovery.
