# R2 post-audit telemetry fixture

This fixture freezes the mechanical linkage required by `08-execution-sheet-reaudit.md` R2. It is
preparation evidence only: it does not authorize the Inventory bootstrap or emit telemetry.

## Contract

`verify-post-audit-telemetry.ps1` reads exactly two inputs supplied by the caller:

1. one terminal audit barrier JSON document; and
2. one snapshot of the exact invocation JSONL ledger. Parsing, SHA-256, and size use the same byte
buffer, followed by a second read that fails if either input changed concurrently.
Both snapshots are decoded as strict UTF-8; invalid bytes produce a schema-valid
`BLOCK/OBSERVABILITY_GAP` result.

It requires exactly one matching pre-audit event and exactly one matching terminal event. The
events correlate by `run_id`, `sheet_producer_attempt`, typed `writer_attempt`, and typed
`audit_attempt`. The terminal event must follow the pre-audit event by JSONL line number and must
repeat the barrier's verdict, correction count, exit reason, and audit-artifact identity exactly.
Timestamps must be RFC3339 UTC (`Z`). They are not used to establish order. Any D1 event for the
same run with a divergent sheet, writer, or audit attempt makes the ledger ambiguous and blocks.

The schemas in `schemas/` define the fixture-local event, barrier, and result shapes. These are a
bounded R2 contract, not a replacement for the generic Arcanum invocation envelope.

The command emits the check JSON to stdout by default. A write requires both `-RunRoot` and
`-OutputPath`; the latter must resolve exactly to
`<RunRoot>/<run_id>/post-audit-telemetry-check-<audit_attempt>.json`. Missing directories,
siblings, traversal, reparse-point escapes, and existing files are rejected. The
final file creation uses atomic `CreateNew` semantics, so a concurrent creator is never
overwritten. The
command never writes the ledger, Inventory, observability indexes, or any other path. A successful
result exits `0` with `TELEMETRY_VERIFIED`; a failed check exits `2` with
`BLOCK/OBSERVABILITY_GAP` and stable failure codes.

```powershell
powershell -NoProfile -File .\verify-post-audit-telemetry.ps1 `
  -AuditBarrier .\cases\positive-attempt-1\audit-barrier.json `
  -SignalJsonl .\cases\positive-attempt-1\sigil-invocations.jsonl
```

For the authorized attempt-specific write, add `-RunRoot <exact-runs-root> -OutputPath
<exact-runs-root>/<run_id>/post-audit-telemetry-check-<audit_attempt>.json`.

Run the self-contained cases with:

```powershell
powershell -NoProfile -File .\test.ps1
```

The tests cover 27 cases, validate all three schemas with Draft 2020-12 plus format checking, and
validate emitted success and error documents. They also exercise no-overwrite, exact-path writing,
mixed attempts, and deterministic concurrent mutation detection. `jsonschema` is required only by
the schema test harness.
