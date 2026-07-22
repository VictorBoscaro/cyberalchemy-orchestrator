# TASK-050 — First real AgentAdapter

## Objective

Replace one fake seat profile with one real CLI provider while retaining the same kernel events,
state transitions and effect reconciliation contract.

- **Layer/slice:** L2 / S-003 / W3.
- **Dependencies:** L1 pass; OQ-CAPABILITIES, OQ-CREDENTIALS, OQ-UNKNOWN-EFFECT and
  OQ-RESOURCE-LIMITS accepted.
- **Write scope:** one provider adapter, shared conformance fixtures, credential/sandbox integration.
- **Implementation selection:** repository-local subprocess adapter behind `SandboxLauncher`; no Octopus/Eve kernel dependency and no PydanticAI dependency in this task.

## Smallest Working Units

- **SWU-ACI-017 — Adapter contract suite:** canonical request/result/event fixtures, capability
  declaration and tests reusable by every provider, including the `ProviderAdapterAdmissionGate` receipt.
- **SWU-ACI-018 — CLI adapter lifecycle:** idempotent start, cursor, status/reconciliation, result
  validation and cancellation; native metadata stays namespaced.
- **SWU-ACI-019 — Output/late/unknown policy:** malformed, partial, late and unreconciled outcomes
  map to explicit retry/repair/abstain/fail/unknown behavior.
- **SWU-ACI-020 — Resource and secret proof:** time/token/tool/payload/disk/queue limits plus
  inspection proving no host profile/secret is visible to the agent.

| SWU | Dependencies | Write scope | Acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|
| 017 | L1 + capability ADR | adapter contracts/fixtures | fake conformance receipt | shared contract suite | local-fallback |
| 018 | 017 + credential ADR | one provider adapter | canonical lifecycle trace | provider contract tests | local-fallback |
| 019 | 018 + unknown-effect ADR | adapter policy mapping | malformed/late/unknown fixture results | failure-injection suite | local-fallback |
| 020 | 018 + resource ADR | launcher/budget tests | limit events and secret inspection report | security/resource tests | local-fallback |

## Done when

The fake and real adapter pass the same operational conformance suite, unknown effects never appear
as success and no provider-specific branch is added to the kernel.

## DomainSpec Coverage

| Source Aspect | Coverage IDs |
|---|---|
| `domain.md` | `agents-communication-infra.EffectiveInputArtifact`, `agents-communication-infra.RawProviderOutput`, `agents-communication-infra.AgentExecutionRequest`, `agents-communication-infra.RetryClass` |
| `operations.md` | `agents-communication-infra.RecordUsageObservation` |
| `interfaces.md` | `agents-communication-infra.AgentAdapter`, `agents-communication-infra.SandboxLauncher` |
| `mappings.md` | `agents-communication-infra.AgentInvocationPlanToMaterializedInvocation`, `agents-communication-infra.RawProviderOutputToCanonicalObservations`, `agents-communication-infra.UsageObservationToRollups` |
| `events.md` | `agents-communication-infra.UsageObservation` |
| `persistence-and-replay.md` | `agents-communication-infra.PricingSource`, `agents-communication-infra.UsageRollup`, `agents-communication-infra.CostCalculation` |
| `rules.md` | `agents-communication-infra.ProviderAdapterAdmissionGate` |
