---
tags: [orchestration, architecture, dispatch, agents]
node_type: discovery
is_session: true
layer: architecture, external
nature: explanatory, reference
status: active
created: 2026-07-21
timestamp: 2026-07-21T21:20:41-03:00
expires: 2026-09-19
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "First-hand verification reverses the conversational lean (Eve rejected on I1), settles the adopt-set (octopus narrow, zod), and confirms EG-1's seal must be built custom at every layer — gating the next implementation-plan, though scoped to one subsystem's tooling."
---

# External tools — build-vs-adopt verification for the Front-3 runtime

## Summary

The session began as a question about what cyberalchemy-orchestrator is and how PydanticAI and "eve" could help, and became a scouting of external runtimes against the already-specified Front-3 bus/deliberation design. After disambiguating "eve" as eve.dev (a durable TS agent runtime) and adding octopus-runtime as a third candidate, we stratified the target runtime into four layers — deliberation kernel + reveal barrier; runtime-host + adapters; effect governance; schemas/judgment — and mapped each tool to a layer, holding two hard invariants (I1 no second source of truth; I2 freeze-before-the-channel) plus the EG-1 single-writer gate. An orientation README was written at `docs/discovery/external-tools/`, framing build-vs-adopt and marking every tool characterization as second-hand and gated. The user chose to author a research dispatch to verify the tools first-hand rather than rest the discovery on conversational web reads. The check-tension gate rejected the first sheet's three-explorer "one tool each" group as a subject-partition, not a tension; it was recast as a confirm-fit ⊥ falsify-fit pair over the shared three-tool corpus (the ui-studio-verify precedent) plus an adopt ⊥ build pair, and both gate agents then passed. The dispatch `2026-07-21-external-tools-verification` ran four agents and was registered and closed `resolved`. The first-hand result converged and flipped the earlier conversational lean: Eve is rejected (fails I1 — Vercel Workflows' event log is a platform-locked canonical authority — and fails the CLI-driver role); octopus-runtime is adopt-narrow (governTool + inward ports + the no-storage octopus-evidence atom, Apache-2.0 / zero-dep / 83 tests) but its execute guard is advisory, so the EG-1 single-writer seal stays custom; PydanticAI is rejected for schemas in favor of zod to avoid a Python split. The keystone finding is that the EG-1 seal is delivered by none of the three and is custom at every layer, so the kernel/journal/barrier and a thin repo-local 5-op CLI adapter must be built while only octopus (effect) and zod (schema) are adopted.

## Contradictions

- `validates` [vault/hypothesis/orchestration-infra.md](../vault/hypothesis/orchestration-infra.md) (HYP-ORCH-INFRA) — the dispatch grounds the hypothesis's invariants with first-hand tool evidence; Eve failing bus-as-projection/I1 is a concrete Collapse-test pass for the design claim.
- `validates` [vault/constitution/engine-constitution.md](../vault/constitution/engine-constitution.md) (EG-1) — no external tool (Eve, octopus-runtime, PydanticAI) delivers the single-writer seal; corroborates, under a real-world tool survey, that the seal stays custom.

## Open questions

- Does a one-shot subprocess spawn for the 5-op CLI adapter preserve I1 under crash/retry **without** reinventing the durable event-log that got Eve rejected — where is the line between a stateless spawn and one that needs its own journal?

## Next steps

- Write `docs/discovery/external-tools/external-tools.md` — the landing discovery synthesizing the four notes (`research/external-tools-verification/`) with per-claim citations, in the agent-assertion-capture mould.
- Run the octopus probe: `governTool()` wrapping `append-dispatch.cjs` with the confirm marker as Draft approval; verify the advisory guard + a single-import lint yields an unbypassable single-writer path (EG-1) — an advisory-not-sealed guard risks repeating the 2026-07-18 enum-drift bypass ([vault/audit/ledger-enum-drift-finding.md](../vault/audit/ledger-enum-drift-finding.md)) — and that `octopus-evidence` stays a subordinate effect-audit plane (HYP-ORCH-INFRA Collapse-test 1).

## Recommendation

Write the discovery first — it is the decided labor the research was the input for — then run the octopus probe as the first executable test of the adopt-narrow verdict; licensed by the resolved research (four first-hand notes, dispatch closed `resolved`). The advisory-guard finding is the likeliest cost: attack it in the probe **before** committing octopus to the EG-1 path, since an advisory-not-sealed guard leaves exactly the bypass surface the enum-drift already exposed.

## Files touched

- docs/discovery/external-tools/README.md
- research/external-tools-verification/fit-confirmer.md
- research/external-tools-verification/fit-falsifier.md
- research/external-tools-verification/adopt-case.md
- research/external-tools-verification/build-case.md
- telemetry/agents/subagents-dispatch.yaml

## Extra section — user directive to register

When presenting a dispatch for the human Confirm, lead with a **plain agent roster** — each agent's name, its objective, and what it will fetch — not the gate/process narration. The user surfaced this mid-session ("cadê os agentes? não sei o nome, o objetivo, o que vão buscar") after a process-heavy presentation buried the roster. Confirm-time presentation is for the agents, not the machinery.
