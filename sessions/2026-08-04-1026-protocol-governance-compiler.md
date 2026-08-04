---
tags: [protocol-governance, skill-to-dag, dispatch-candidate, deterministic-compilation, authority-boundaries]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-04T10:26:57-03:00
updated_at: 2026-08-04T10:26:57-03:00
expires: 2026-10-03
decisions_made: true
contradictions_found: true
specs_updated: [docs/features/agents-communication-infra/specs/SPEC.md, docs/features/agents-communication-infra/specs/protocol-compilation.md, docs/features/agents-communication-infra/specs/architecture.md, docs/features/agents-communication-infra/specs/glossary.md, docs/features/agents-communication-infra/specs/TEST-SPEC.md, docs/features/agents-communication-infra/TEST-SPEC.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session establishes and implements the authority boundary that lets skills compile into deterministic DAG candidates without granting confirmation or runtime execution authority."
---

# Protocol Governance ownership and bounded skill-to-DAG compiler

## Summary

The repository objective is to keep agent work connected to its governing objectives, decisions, assumptions, actions, and evidence rather than treating locally correct execution as sufficient. This session set out to resolve the runtime-v2 review's ambiguous ownership of the skill-to-DAG contract and carry the resolution through specification, planning, implementation, and independent verification. It decided that ACI Protocol Governance owns execution profiles, skill bindings, protocol recipes/DAGs, and deterministic compilation through a non-authoritative `DispatchCandidate`, while ACI confirmation retains capability resolution, final `DispatchSpec`, and human acceptance and the runtime retains scheduling and effects. That boundary corrected the earlier tendency to let recipe compilation produce execution authority directly and prevented reuse of the historical `ACI-030` placeholder for this independent L0 adjunct. The session promoted the decision into discovery, architecture, glossary, normative protocol and test specifications, then created a dedicated work-pack and exact readiness contract. The bounded compiler now validates closed canonical inputs with total failure precedence, admits only two frozen tuples, returns exact compiled or unsupported results, and optionally stores only compiled candidate bytes through the existing ArtifactStore. Independent audits found and drove repairs for optional placeholders, closed output validation, test overstatement, and the complete Stage-E integrity chain. Final evidence is 12 protocol tests, one traceability test, 131 runtime tests, a consistent 58-file Stage-E manifest, matching receipt pins, and an independent verifier PASS, with coverage deliberately limited to the frozen bounded package. The remaining work belongs to separate governed units for candidate-to-`DispatchSpec` mapping, a persistent recipe registry, and real confirmation-boundary integration tests.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [ACI Protocol Governance ownership](../docs/decisions/aci-protocol-governance-ownership.md) | `validates` | The session implemented and independently verified the ownership and authority boundary accepted by ACI-PG-001. |
| [Protocol compilation contract](../docs/features/agents-communication-infra/specs/protocol-compilation.md) | `validates` | The implementation, frozen fixtures, focused tests, runtime suite, and verifier provide bounded executable evidence for this contract. |
| [Runtime-v2 migration inventory review](2026-08-03-1618-runtime-v2-migration-inventory-review.md) | `contextualizes` | This session resolves and implements the skill-to-DAG ownership and migration gap surfaced by that review. |

## Open questions

- What exact closed interface and failure model should the ACI confirmation owner use to map a `DispatchCandidate` into a final `DispatchSpec`?
- What versioning, revocation, admission, and migration rules should govern a persistent profile/binding/recipe registry beyond the two frozen tuples?

## Next steps

1. Create a separate governed SWU owned by ACI confirmation for `DispatchCandidate` to `DispatchSpec` mapping and real parser-boundary rejection tests.
2. Specify the persistent profile, binding, and recipe registry without expanding the current compiler's authority.
3. Add future integration tests that attempt to cross candidate bytes and digests through actual confirmation and runtime entrypoints.

## Recommendation

Preserve the compiler as a pure non-authoritative Protocol Governance calculation and make the confirmation-owned candidate-to-`DispatchSpec` boundary the next implementation slice; do not combine registry generalization, confirmation, and execution in one SWU.

## Files touched

- `.gitattributes`
- `docs/decisions/aci-protocol-governance-ownership.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `docs/features/agents-communication-infra/CHANGELOG.md`
- `docs/features/agents-communication-infra/EXECUTION-PACK.md`
- `docs/features/agents-communication-infra/IMPLEMENTATION-LAYERING.md`
- `docs/features/agents-communication-infra/TEST-SPEC.md`
- `docs/features/agents-communication-infra/WORK-PACK.md`
- `docs/features/agents-communication-infra/discovery/agent-tools-and-delegated-supervision.md`
- `docs/features/agents-communication-infra/discovery/agents-communication-protocols/README.md`
- `docs/features/agents-communication-infra/reviews/2026-08-03-protocol-compilation-spec-review/review.md`
- `docs/features/agents-communication-infra/specs/SPEC.md`
- `docs/features/agents-communication-infra/specs/TEST-SPEC.md`
- `docs/features/agents-communication-infra/specs/architecture.md`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/binding.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/candidate.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/compiler-contract.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/invocation.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/manifest.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/profile.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/recipe.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/result.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/skill-source.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/unsupported-binding.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/unsupported-invocation.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/unsupported-profile.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/unsupported-recipe.json`
- `docs/features/agents-communication-infra/specs/fixtures/protocol-compilation-v1/unsupported-result.json`
- `docs/features/agents-communication-infra/specs/glossary.md`
- `docs/features/agents-communication-infra/specs/protocol-compilation.md`
- `docs/features/agents-communication-infra/work-pack/context/SWU-ACI-PROTOCOL-COMPILATION-001-CONTEXT.index.json`
- `docs/features/agents-communication-infra/work-pack/context/SWU-ACI-PROTOCOL-COMPILATION-001-CONTEXT.md`
- `docs/features/agents-communication-infra/work-pack/context/SWU-ACI-PROTOCOL-COMPILATION-001-SCAFFOLD.md`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-PROTOCOL-COMPILATION-001.json`
- `docs/features/agents-communication-infra/work-pack/execution/SWU-ACI-PROTOCOL-COMPILATION-001-code-readiness.json`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-decisions.md`
- `docs/features/agents-communication-infra/work-pack/shared/cross-task-gaps.md`
- `docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md`
- `docs/features/agents-communication-infra/work-pack/shared/traceability.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-PROTOCOL-COMPILATION.md`
- `implementations/server/runtime/local_pilot.py`
- `implementations/server/runtime/protocol_compilation.py`
- `implementations/server/runtime/service.py`
- `implementations/tests/runtime/aci-test-traceability.json`
- `implementations/tests/runtime/test_aci_traceability.py`
- `implementations/tests/runtime/test_protocol_compilation.py`
