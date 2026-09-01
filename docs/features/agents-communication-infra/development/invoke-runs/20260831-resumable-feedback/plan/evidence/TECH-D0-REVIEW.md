# TECH-D0 independent review evidence

## Verdict

`PASS` for both corrected technical designs. This receipt preserves the second-pass result returned
by the independent `product_prompt_refs_audit` reviewer after its first pass returned `FIX` for both
documents.

| Design | Reviewed SHA-256 | Result | Authorized next planning ceiling |
|---|---|---|---|
| [TECH-OPEN-D0](../TECH-OPEN-D0.md) | `sha256:f538e31e2dd4743eebca5ded62bb1b40cafb37a79c1aabf7998f86576dcc324d` | `PASS` | One non-authoritative L0 experiment work pack only. |
| [TECH-POLICY-D0](../TECH-POLICY-D0.md) | `sha256:522a8cac79335e6190fb4799cbea95c0f58621f4f9ea5f72add2437690b8130e` | `PASS` | One `POLICY-000` pure contract/oracle work pack only. |

## Findings closed by the second pass

### TECH-OPEN-D0

- The earlier dual-authority AND gate is no longer ratified. Options A/B/C remain an explicit
  unresolved architecture/authority gate.
- Operation-scoped opening groups are audit projections only. The design records that the legacy
  compiler does not preserve the same runtime Seat, session or continuation identity.
- Any later authorized appender wrapper owns full comparison of every authority-bound unstamped
  field, durable original-receipt replay and lost-response reconciliation. Appender exit success or
  `already registered` output does not prove content equality.
- `created` remains appender-owned observation metadata; explicit `invoked_by` remains inside the
  compared projected input.

### TECH-POLICY-D0

- L0/L1/L2/L3 negative vectors are separated by the seams they can actually exercise.
- Synthetic budget-policy, sandbox-policy, ResourceBudget, SandboxPolicy, combined oracle and
  harness-fence bytes have explicit reproducible digests.
- `aci.execution-authority-fence-harness@1` is distinct from and rejected by the production fence
  parser; it cannot satisfy cutover, confirmation, plan/request acceptance or an effect claim.
- `POLICY-001` is synthetic lineage only. Real plan/request binding remains behind PRODUCT-PASS,
  complete CONF v2 bytes and explicit user confirmation.

## Independent reproduction

The reviewer independently recomputed the declared hashes for both referenced policy targets,
ResourceBudget, SandboxPolicy, harness preimage and harness fence and reported exact matches. The
root agent separately recomputed every JSON/text fixture digest in TECH-POLICY-D0; all seven values
matched, including the full harness-fence content digest declared outside its code block.

## Hard ceilings

This receipt does not resolve the A/B/C opening-authority decision, select product limits or grants,
freeze `confirmed-authority@2`, authorize an audit-ledger append, create or verify OPEN, advance a
Run/Group, persist a real plan/request, claim an effect, start a worker/provider, or promote any
synthetic fixture as executable authority.

Only the two bounded L0 work packs named above may now be authored. Each still requires its own
descriptor, context, test obligations, readiness evidence and independent implementation review
before code entry.
