# TASK-AUDIT-LAYERING — Promotion evidence audit

## Smallest Working Unit Exemption

- **Reason:** closure-only audit task.
- **Allowed because task ID contains:** `AUDIT`.

For L0-L4, verify that the named exit evidence existed before promotion and that later layers did not
silently absorb deferred scope. Check non-regression fixtures across layers and the product-value
decision. Unsupported promotion becomes a remediation task or layer rollback; it is never repaired
by rewriting the earlier plan after the fact.

