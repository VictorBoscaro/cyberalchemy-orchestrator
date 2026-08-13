# R2 final recheck — telemetry post-audit fixture

## Verdict

**PASS.** Both prior MAJOR findings are closed. The six bounded gates from `04` §Observability and
`08` R2 are satisfied by the fixture and its 27-case suite. This is fixture readiness evidence only;
it does not authorize bootstrap execution.

## Evidence

```text
powershell -NoProfile -ExecutionPolicy Bypass -File .\test.ps1
PASS: schemas and emitted positive/error results validate
PASS: 27 telemetry post-audit fixture cases
```

A separate invalid-UTF-8 reproduction returned exit `2`, schema version `1.0.0`, result
`BLOCK/OBSERVABILITY_GAP`, and failure `SIGNAL_JSONL_INVALID_UTF8`. The contention fixture creates a
competitor at the exact output path immediately before the verifier's create; the verifier blocks
and preserves the competitor bytes.

## Coverage

| gate | verified evidence | result |
|---|---|---|
| exact `RunRoot` / path / escape | canonical expected-path equality, reparse-component rejection, missing-run-dir rejection, and disallowed-path case | PASS |
| same-byte snapshot / concurrent append | parse, SHA-256, and size share the captured byte buffer; deterministic mutation before recheck blocks | PASS |
| divergent coexisting attempts | mixed correct/divergent same-run events produce `DIVERGENT_D1_ATTEMPT` and block | PASS |
| schema-valid errors / real validation | strict UTF-8 failures become stable codes; Draft 2020-12 plus format checking validates schemas and emitted positive, missing-input, and invalid-UTF-8 results | PASS |
| exact output / no overwrite / zero extras | exact attempt-specific output succeeds; pre-existing and deterministically contended outputs block; `FileMode.CreateNew` makes creation atomic; positive run contains exactly one file | PASS |
| RFC3339 UTC `Z` | runtime predicate and event schema require UTC `Z`; offset negative blocks | PASS |

## Prior findings disposition

### F1 — Invalid UTF-8 escaped the result contract

**CLOSED.** `verify-post-audit-telemetry.ps1:97-98` catches strict ledger decode failure and records
`SIGNAL_JSONL_INVALID_UTF8`. `test.ps1:76-82` covers invalid UTF-8 for both inputs, and
`validate-schemas.py:45-57` validates the emitted failure document with the real result schema.

### F2 — No-overwrite used check-then-overwrite

**CLOSED.** `verify-post-audit-telemetry.ps1:185` opens the exact path with
`FileMode.CreateNew`, `FileAccess.Write`, and `FileShare.None`. The deterministic contention case in
`test.ps1:96-117` proves that a competitor created immediately before open is preserved and the
verifier does not succeed.

## Findings

No CRITICAL or MAJOR finding survives this bounded recheck.

## Residue

- Reparse escape rejection remains established statically rather than by an explicit junction or
  symlink fixture.
- The second snapshot read detects mutation through the verification window exercised by the hook;
  it does not freeze the append-only ledger after that read.
- Caller-contract/path exceptions remain outside the telemetry result-schema channel; the governing
  text does not require those invocation errors to be encoded as telemetry-check results.

## Artifact verdict

**KEEP.** Exit reason: prior F1/F2 closed; 27 cases pass; no surviving material finding. No Inventory
or real observability content was modified. Agents spawned by this reviewer: `0`.
