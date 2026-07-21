# TASK-AUDIT-ALIGNMENT — Architecture and authority audit

## Smallest Working Unit Exemption

- **Reason:** closure-only audit task.
- **Allowed because task ID contains:** `AUDIT`.

Audit implementation dependency direction, store authorities, sole-writer boundaries, replay
purity, projection non-authority, provider independence, spec immutability and absence of parallel
skill/UI execution paths. Every finding names severity, concrete path/symbol, violated contract,
repair owner and retest. Any authority violation blocks pilot closure.

