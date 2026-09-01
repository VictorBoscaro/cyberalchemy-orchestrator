# Resumable Agent Continuation

This capability specifies the bounded decision in
[ACI-CONT-001](../../../../decisions/aci-resumable-agent-continuation.md): a terminal author turn is
parked without a running agent, reviewer feedback becomes an official bus contribution, and the
runtime deterministically resumes or reconstructs the author for one final turn.

## Outcome and boundary

The admitted graph is exactly `author:0 -> reviewer:0 -> author:1`, expanded to an acyclic turn
graph with loop ceiling one. Provider-native continuation is an optimization; correctness derives
from the reconstruction snapshot, two frozen input mappings, exact official contribution receipts
and a canonical effective-input artifact. The agents receive no inbox, bus-read or polling
capability.

## Contracts

| Aspect | Contract | Responsibility |
|---|---|---|
| Entity | [AgentContinuation](../domain.md#agentcontinuation) | Durable wait/resume identity and policy. |
| Entity | [ContinuationInputMapping](../domain.md#continuationinputmapping) | Exact author-output and review-output selectors and order. |
| Mapping | [ContinuationContributionsToEffectiveInput](../mappings.md#continuationcontributionstoeffectiveinput) | Resolve two official contributions into exact target-turn input. |
| State | [AgentContinuationLifecycle](../states.md#agentcontinuationlifecycle) | Suspend, resume, uncertainty, definitive loss, reconstruction and cancellation. |
| Events | [`continuation.*`](../events.md#continuationsuspended) | Journal every lifecycle, loss, reconstruction and terminal fact. |
| Operation | [SuspendAgentContinuation](../operations.md#suspendagentcontinuation) | Park a terminal turn without an external effect. |
| Operation | [ResumeAgentContinuation](../operations.md#resumeagentcontinuation) | Materialize exact mapped bus outputs and request same-session resume atomically. |
| Operation | [ReconstructAgentContinuation](../operations.md#reconstructagentcontinuation) | Create one replacement only after definitive no-start evidence. |
| Operation | [CancelAgentContinuation](../operations.md#cancelagentcontinuation) | Dispose or cancel the current continuation target safely. |
| Workflow | [ResumableFeedbackWorkflow](../workflows.md#resumablefeedbackworkflow) | Coordinate the finite author-reviewer-author turn graph. |
| Rule | [ACI-R21](../rules.md#aci-r21--continuation-is-resumable-state-never-hidden-authority) | Keep authority in confirmed mappings and journal facts. |
| Interface | [AgentAdapter](../interfaces.md#internal-agentadapter) | Resume, dispose and reconcile opaque provider continuation handles. |
| Tests | [T-ACI-CONT1 through T-ACI-CONT9](../../TEST-SPEC.md#bounded-resumable-feedback) | Verify identity, input, races, uncertainty, replay and all invalid transitions. |

## Runtime input path

Author and reviewer outputs enter the bus as candidates and become official only through receipt
verification. The scheduler reads the journal projection, not an agent-authored pointer, and
resolves exactly the two `ContinuationInputMapping` records. The resume transaction finalizes the
effective input in canonical order with the new target attempt, sealed request and one effect.

## Exclusions

Arbitrary cycles, open-ended conversations, implicit provider memory, generic subscriptions,
automatic fallback from an unknown effect, multiple reconstruction attempts and host-bound
`WorkflowInputManifest` materialization are outside this capability version.
