# TASK-105 Accepted Bounded Smoke Evidence

- Date: 2026-07-23
- `npm.cmd test`: PASS — 1 file, 27 bounded smoke tests
- `npm.cmd run typecheck`: PASS
- `python docs/features/agent-provenance-telemetry/contracts/verify_contracts.py`: PASS
  (`aci_vectors=6 positive=5 rejection=8 candidates=16`)
- Cycle-3 adversarial additions cover nested raw/objects, derivation locality/snapshot binding,
  typed evidence refs, probe/bundle origin evidence and completion-log enum/null consistency.
- Cycle-4 additions cover exact check enums/relation-use equality, exact and current fact evidence,
  injected snapshot-pointer verification, bytewise candidate ordering with Unicode/case,
  strict RFC3339 calendar/offset vectors and target-kind disposition enums.
- Cycle-5 additions cover current/local/non-missing aggregate targets, problem block subjects,
  shared domain timestamp decoding, frozen-input purity and assessment cross-kind vectors.
- Final reviewer verdict: `PASS / NO OBJECTION`, cycle 5/5.
- Acceptance receipt: `acceptance-receipt.md`.
- Source manifest: `source-digests.sha256`.

The test names map to bounded sub-obligations beneath APT-TEST-R1..R8 and APT-TEST-C01..C18.
No complete R/C family PASS is claimed until its full TEST-SPEC variant matrix is executable.

Operation, event-envelope, interface, durable replay/checkpoint, ACI integration and full
observability IDs remain planned/not-run. This evidence makes no whole-family, canonical-byte,
receipt or profile claim. See `coverage-manifest.md`.
