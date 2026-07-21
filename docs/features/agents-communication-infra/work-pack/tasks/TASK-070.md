# TASK-070 — Second provider and mixed-group portability

## Objective

Show that provider choice is an adapter concern and that a mixed group uses one protocol, journal,
bus contract and realtime path.

- **Layer/slice:** L3 / S-005 / W5.
- **Dependencies:** TASK-060 decision is `continue`; provider ADRs accepted.
- **Write scope:** second provider adapter, capability matrix and mixed-provider fixtures.

## Smallest Working Units

- **SWU-ACI-024 — Capability matrix:** classify required, semantics-preserving emulable and
  incompatible capabilities; fallback is explicit before confirmation.
- **SWU-ACI-025 — Second adapter:** satisfy the same contract suite without kernel changes.
- **SWU-ACI-026 — Mixed group:** two provider implementations participate in one group; failure of
  one remains isolated and policy-visible.
- **SWU-ACI-027 — Portability audit:** compare canonical traces and assert only provider metadata
  differs; semantic identity of generated content is not required.

| SWU | Dependencies | Write scope | Acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|
| 024 | W4 continue | capability spec | reviewed matrix and rejection fixtures | schema/contract review | manual |
| 025 | 024 | second provider adapter | adapter conformance receipt | shared contract suite | local-fallback |
| 026 | 025 | mixed-run fixtures/config | single-protocol mixed trace | mixed integration tests | local-fallback |
| 027 | 026 | audit report only | no-kernel-fork finding | path/event diff review | manual |

## Done when

Fake, provider A, provider B and mixed runs use the same canonical state/event contracts and no
provider-specific store or UI path exists.
