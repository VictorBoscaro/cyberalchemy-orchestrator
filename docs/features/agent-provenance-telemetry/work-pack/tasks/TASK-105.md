# TASK-105 — Pure APT L0 Module

- Status: pass
- Scope: `tools/agent-provenance-telemetry/` plus evidence synchronization
- Dependency: TASK-100
- Deliverables: types, validators, normalization, payload candidates, injected canonicalizer,
  pure reducers/projectors, test-only doubles and exact-ID tests
- Prohibited: durability, bus/store/journal ownership, ACI compatibility claims and runtime enablement
- Validation: `npm test` and `npm run typecheck`

## Accepted Evidence

- Fresh 2026-07-23 run: `npm.cmd test` PASS, 27/27 bounded cases in one file.
- Fresh `npm.cmd run typecheck`: PASS.
- Fresh contract verifier: PASS,
  `aci_vectors=6 positive=5 rejection=8 candidates=16`.
- Final independent implementation review: `PASS / NO OBJECTION`, cycle 5/5.
- Digest-bound receipt:
  `../../session-evidence/TASK-105/acceptance-receipt.md`.
- Exact source manifest:
  `../../session-evidence/TASK-105/source-digests.sha256`.
- Test names reference APT-TEST-R1..R8 and APT-TEST-C01..C18 only as bounded smoke
  sub-obligations; they do not prove each complete family.
- L3/L4, operation, integration, replay/checkpoint and profile-conformance families remain
  planned/not-run.

The acceptance is restricted to pure L0 construction. It does not satisfy TASK-110 entry,
registration, durability, storage-policy, mutation or enablement gates.
