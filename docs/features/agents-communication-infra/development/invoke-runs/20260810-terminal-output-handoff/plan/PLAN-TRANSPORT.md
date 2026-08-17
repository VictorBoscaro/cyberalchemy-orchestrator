# Invoke Plan transport

- Observed capability: `invoke`, mode `plan`.
- Target owner/cycle: agents-communication-infra terminal-output handoff implementation cycle.
- Approved design: `../ARCHITECTURE.md` and `../CONTEXT.md`.
- Complexity/output: high, split.
- Layering: `IMPLEMENTATION-LAYERING.md`.
- Work-pack: `WORK-PACK.md`.
- Execution choreography: `EXECUTION-PACK.md`.
- Dispatch trace: `planning-dispatch.json` and `DISPATCH-TECHNIQUE-TRACE.md`.
- Distill: `DISTILL-VALIDATION.md`.
- Machine entry: `EXECUTION-ENTRY.json`.
- Next route: execute the evidence-only `task-session:execute` route for HTR-000 using an isolated disposable probe. A passing receipt allows Plan/Distill refresh and selection of HTR-001; no runtime mutation is currently admitted.

Invoke has authored planning only. No runtime source, authority, registry, deployment or research dispatch state is changed by this plan.
