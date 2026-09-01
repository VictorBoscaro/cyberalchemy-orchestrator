---
status: accepted
date: 2026-08-31
scope: agents-communication-infra-resumable-feedback
decision_id: ACI-CONT-001
---

# ACI resumable agent continuation

## Decision

ACI runtime-managed execution may park a provider session after one terminal turn and later attempt
to resume that same session when a confirmed input dependency becomes satisfied. The parked object
is not a running model invocation and does not poll the bus. The journal records dependency facts,
the materializer builds the next immutable effective input, and the effect worker asks the adapter
to resume or cancel the parked session.

Same-session continuation is preferred but is not the correctness boundary. Every parked turn must
also carry an immutable reconstruction snapshot. A successful same-session resume preserves the
same seat and agent instance. A definitively unavailable provider continuation may use a separately
confirmed reconstruction branch that preserves the seat but creates an explicit replacement agent
instance and a new attempt. An unknown resume-effect outcome blocks automatic reconstruction
because a second physical execution could duplicate work.

The first bounded workflow is finite and preconfirmed:

```text
author seat, turn 0 -> reviewer seat, turn 0 -> author seat, turn 1
```

The review output is a declared source for the author's turn-1 input. The author does not read or
subscribe to a generic inbox. The runtime expands the bounded feedback connection into an acyclic
turn-dependency graph with a loop ceiling of one; arbitrary cycles remain outside this decision.

## Authority and lifecycle boundary

- One physical [Attempt](../features/agents-communication-infra/specs/domain.md#attempt) ends before
  the wait begins; `waiting_tool` is not reused for peer-input waiting.
- A new `AgentContinuation` aggregate owns suspension, resume, cancellation and expiry facts.
- Resume produces a new attempt/turn. Provider-session continuity never substitutes for an exact
  `EffectiveInputArtifact` or execution-authority fence.
- The adapter owns host-native start/resume/cancel translation and observations only. It cannot
  decide eligibility, choose source artifacts or write the journal.
- Definitive continuation loss and unknown resume outcome are distinct observations with distinct
  fallback behavior.

## Evidence and limitations

The repository owner accepted this direction in the active 2026-08-31 session. The bounded
[host continuation probe](../features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/probes/host-continuation-probe.json)
shows that the observed Codex collaboration surface resumed one idle agent by the same agent
reference with prior-turn recall and accepted interruption of another active agent.

The probe does not prove survival across host restart, indefinite retention, durable cancellation,
or that the project adapter already exposes this capability. Those remain adapter conformance and
recovery obligations. Fake-adapter proof precedes live-provider promotion.

## Consequences

- Domain, state, operation, event, interface, workflow, rule and test contracts must be promoted
  together before implementation.
- Dispatch confirmation must freeze and preallocate the continuation identity, turn dependency,
  exact continuation input mappings and source message identities, resume policy,
  deadline, loop ceiling and reconstruction permission.
- The runtime work pack must admit separate bounded SWUs with independent brownfield audits and a
  verifier for every coder.
- This decision does not itself authorize runtime mutation or advertise `runtime-managed` routing.
