# TASK-VERIFY — Pilot completion verification

## Smallest Working Unit Exemption

- **Reason:** closure-only verification task.
- **Allowed because task ID contains:** `VERIFY`.

Verify every claimed acceptance criterion and falsifier from the feature README, layering artifact
and traceability matrix. Produce a report with exact commands, fixtures, state hashes, environment,
failures and skipped checks. A skipped acceptance-critical check is `block`, not pass.

Completion requires existing ledger/API/UI tests plus all runtime contract, fault, security,
adapter, mixed-provider, recipe and product-gate evidence appropriate to the claimed pilot scope.

