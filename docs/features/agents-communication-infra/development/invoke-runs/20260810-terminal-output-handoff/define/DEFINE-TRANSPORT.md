# Invoke Define transport

- Mode: `define`
- Status: pass after review-driven amendment and Design refresh
- Target owner: Agents Communication Infrastructure specification lifecycle
- Spec outputs: `specs/SPEC.md`, `domain.md`, `operations.md`, `states.md`, `events.md`, `interfaces.md`
- Glossary output: `specs/glossary.md`
- Layering: existing `IMPLEMENTATION-LAYERING-SEED.md` remains a non-executable seed
- Discovery: existing workflow-graph discovery; no waiver
- Decisions: D1 exact terminal response artifact; D2 Python + SQLite baseline
- Unresolved target gap: implementation and executed witnesses remain absent
- Next route: refresh and revalidate `invoke design`; only then `invoke plan`

The review-driven amendment separates content from producer evidence; defines the L0
`SourceToSlotMapping`, manifest, binding, terminal-outcome, materialization and launch contracts;
adds persistence/crash semantics and legacy host-binding authority; and limits readiness to one
completed producer and one required slot. It does not relax the current connected-topology compiler
fence or claim fan-in readiness.
