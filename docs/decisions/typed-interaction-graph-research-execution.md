---
tags: [decision, agents-communication-infra, research, typed-graph, dispatch-lifecycle]
node_type: decision
is_session: false
layer: [architecture, application]
nature: [normative, reference]
status: accepted
version: 0.1.0
last_updated: 2026-08-17
---

# Typed Interaction Graph Research Execution

## Decision

Execute the typed-interaction-graph research as a sequence of governed dispatches whose outputs are
materialized before the next stage: exploration, synthesis, independent gates, and final audit.

## Why this decision was required

The confirmed single-dispatch record represented the intended epistemic order with three
`sequential` connections. On 2026-08-17, `dispatch_workflow compile` failed before opening because
the compiler required `handoff-0-1.json` for `explorers -> synthesizer` before the explorers had
run. The record was structurally valid under ledger schema `0.6.4`, but the current
`legacy-managed` compiler cannot progressively materialize its own downstream handoffs.

## Options considered

1. **Governed staged dispatches — selected.** Preserves ordering, provenance, validation, and
   recoverability with the runtime that exists today. Costs additional lifecycle records.
2. **Repair the compiler first.** Removes the structural limitation but expands scope from research
   execution into runtime implementation.
3. **Stop.** Preserves the validated proposal without producing research results.

## Authority and consequences

The repository owner selected option 1 in this session on 2026-08-17. The staged records may reuse
the confirmed roles, prompts, budgets, and evidence contract, but each materialized opening still
requires exact lifecycle confirmation. No stage may simulate a missing handoff informally; every
downstream stage consumes persisted outputs from a closed upstream stage.

The decision does not claim that staged dispatches are the target architecture. It is an execution
adapter for the current runtime limitation and leaves the original typed-graph research question
unchanged.

## Remaining blockers

None for preparing the staged records. Each stage remains gated by its own lifecycle confirmation,
binding compilation, opening receipt, terminal outputs, and close receipt.

## Connections

| Edge | Target |
|---|---|
| `grounds` | `../features/agents-communication-infra/research/interaction-relations/dispatch-proposal.md` |
| `explains` | `../../.codex/workflow-inputs/2026-08-17-typed-interaction-graph-basis-research/opening.json` |
| `constrained-by` | `../../implementations/server/runtime/dispatch_workflow.py` |

