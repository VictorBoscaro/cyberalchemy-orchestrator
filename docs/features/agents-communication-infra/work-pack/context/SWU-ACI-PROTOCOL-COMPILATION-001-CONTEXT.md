# Context — SWU-ACI-PROTOCOL-COMPILATION-001

## Objective

Implement the smallest accepted ACI Protocol Governance slice: exact canonical profile, binding,
recipe and invocation documents plus the fixed `compiler_contract_digest` compile deterministically into a
non-authoritative `DispatchCandidate`. Success is byte equality with the frozen candidate/result,
closed failures with no partial state, and zero path into confirmation or runtime execution.

## Authority

- `ACI-PG-001` owns compilation only through candidate/result.
- `protocol-compilation.md@1.0.0` is the detailed contract.
- The feature-wide and aspect TEST-SPECs jointly define T-ACI-PC1 through T-ACI-PC12.
- The 2026-08-03 two-lens normative review is PASS.

## Existing seams

- `runtime/canonical.py` owns strict JSON parsing, `aci-cjson-1`, and qualified SHA-256 helpers.
- `runtime/artifacts.py` owns content-derived Artifact identity and idempotent finalized storage.
- `RuntimeService` already constructs the shared ArtifactStore; the new application wrapper must
  call it only after admitted successful compilation.

## Non-negotiable boundary

The pure compiler has no clock, randomness, environment, filesystem discovery, registry, network,
provider, tool, scheduler, bus, journal, confirmation or persistence dependency. The calculation
admits exactly the two immutable tuples in the frozen package: one `compiled` and one
`required-unsupported`. Every third schema-valid tuple is `fixture_not_admitted`; malformed
mutations exist only to prove earlier closed failures.

No code in `dispatch_workflow.py`, API routes, migrations, providers, legacy surfaces, pending
sheets or YAML is in scope.
