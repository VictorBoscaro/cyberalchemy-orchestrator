---
tags: [agents-communication-infra, canonical-vault-reads, authority, trust-boundaries, execution-guards, receipts]
node_type: discovery
is_session: true
layer: [architecture, domain]
nature: [explanatory, technical]
status: active
created: 2026-07-23
timestamp: 2026-07-23T19:10:15-03:00
expires: 2026-09-21
decisions_made: true
contradictions_found: false
specs_updated:
  - docs/features/agents-communication-infra/adrs/ADR-CVR-001.md
  - docs/features/agents-communication-infra/specs/canonical-vault-reads.md
  - docs/features/agents-communication-infra/TEST-SPEC.md
  - docs/features/agents-communication-infra/work-pack/tasks/TASK-CVR.md
  - docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json
promoted_candidates: []
expected_importance: 9
importance_rationale: "Establishes an independently reviewed trust contract and execution sequence for canonical vault reads while preserving the non-authorizing gate."
---

# Canonical Vault Reads Authority Contract and Guard

## Summary

This session examined whether canonical vault-read tools could be implemented safely under the repository's existing blocked gates. The work established the staged order `SWU-ACI-CVR-000 -> GUARD-001 -> CVR-001 -> CVR-002` and separated the external bootstrap finalizer from the common guard/finalizer. It defined exactly three content-addressed authority artifacts per execution and rejected mutable pointers, revocation files, `ClaimReceipt`, duplicate receipts and self-bootstrap. Independent adversarial deliberation exposed that workspace hashes prove integrity but not authenticated identity or durable single-use authority. The contract was therefore extended with closed owner, root, authorization, immutable claim-lease, `AuthorityLaunchContext` and receipt schemas, plus policy, repository, audience, executor, finalizer, nonce, time, locator and outcome bindings. `TEST-SPEC` gained negative cases for substitution, replay, races, temporal drift, scope mismatch and contradictory terminal receipts. Two independent final reviewers returned `PASS`, and the current five-entry packet digest was computed without accepting or authorizing it. No guard/CVR code, authorization, claim, receipt or authority directory was created because the external trust provider and related evidence remain absent.

## Open questions

- Can the current host supply a non-workspace one-shot authenticated launch handle, stable principal credentials, trusted UTC/nonces and proven create-exclusive semantics, or is a separate authority provider required?

## Next steps

- Evaluate the current host against the six external trust prerequisites recorded in `G-CVR-010` and `G-CVR-011`.
- After those prerequisites exist, freeze the five packet entries, collect the three authenticated owner acceptances and issue only the exact one-time GUARD bootstrap authorization and claim.
- Execute `SWU-ACI-CVR-GUARD-001` through the designated external executor/finalizer and require `T-CVR-AUTH1` through `T-CVR-AUTH5` plus a terminal `PASS` receipt before preparing CVR-001.

## Recommendation

Evaluate the host authority boundary first; it is the licensing fact for every later acceptance, authorization and implementation step.

## Files touched

- docs/features/agents-communication-infra/work-pack/tasks/TASK-CVR.md
- docs/features/agents-communication-infra/adrs/ADR-CVR-001.md
- docs/features/agents-communication-infra/specs/canonical-vault-reads.md
- docs/features/agents-communication-infra/TEST-SPEC.md
- docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md
- docs/features/agents-communication-infra/WORK-PACK.md
- docs/features/agents-communication-infra/work-pack/waves/W0.md
- docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md
- docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md
- docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md
- docs/features/agents-communication-infra/CHANGELOG.md
- docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-CVR-GUARD-001.json

## User directive

The user delegated autonomous orchestration and subagent review, then explicitly requested that this session be closed.
