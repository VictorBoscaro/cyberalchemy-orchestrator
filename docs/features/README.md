---
tags: [docs, features, index, specs, work-pack, discovery]
node_type: readme
is_session: false
layer: [architecture, application]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/features

## 1. What is this?

One subfolder per feature build. Each package keeps its own discovery, specs, reviews and
work-pack together, so that everything governing a feature travels with it rather than being
scattered across the repository. This is the deepest and densest tree in `docs/`.

## 2. Business Context

Features here follow the DomainSpec chain — discovery, then `SPEC.md` and its companions
(`domain.md`, `events.md`, `interfaces.md`, `operations.md`, `queries.md`, `states.md`), then
`TEST-SPEC.md`, then a `WORK-PACK.md` decomposed into waves and tasks — with a decision record
under [`../decisions/`](../decisions/) supplying the scope authority. The two large packages are
at different points on that chain: `agents-communication-infra` carries a full spec and work-pack
set with five dated review rounds, while `agent-provenance-telemetry` is still at
`status: discovery` and declares `absorption_target: agents-communication-infra` — it is expected
to be absorbed into the other rather than shipped beside it.

## 3. Why it matters

Package status varies far more than the uniform folder listing suggests, and two of the six
subfolders are not features at all: `discovery-validator-fixture/` and `validator-fixture/` each
contain nothing but an empty `discovery/` directory and exist as fixtures for the discovery
validator. A reader who assumes six features in flight will be wrong by two. This index states
what each package actually is and how far along it is.

## 📁 Navigation

- **`agent-provenance-telemetry/`**: Provenance and telemetry for agent dispatch.
  `status: discovery`, v0.7.0, `authority: observational-only`,
  `absorption_target: agents-communication-infra`. The largest tree here — `contracts/`,
  `discovery/`, `integration/` (stages a–g), `probes/`, `prompts/`, `research/`, `reviews/`,
  `session-evidence/`, `specs/`, `work-pack/`. Has its own [README](agent-provenance-telemetry/README.md).
- **`agents-communication-infra/`**: "Infraestrutura de comunicação e deliberação entre agentes."
  `status: draft`, `authority: candidate`. The most complete package: `adrs/` with golden
  fixtures, `discovery/`, `experiments/` (including the executable `bus-publication-probe/`),
  `profiles/`, `reviews/` (five dated rounds), `specs/`, `work-pack/`. Has its own
  [README](agents-communication-infra/README.md).
- **`discovery-validator-fixture/`**: Not a feature. Contains one empty `discovery/` directory,
  used as a fixture for the discovery validator. No README of its own.
- **`skill-control-center/`**: The operator control plane over skills and dispatches. Phase 1 is
  bounded to read-only/draft-only by
  [`../decisions/skill-control-center-phase-1-scope.md`](../decisions/skill-control-center-phase-1-scope.md).
  Holds `SPEC.md`, `UI-SPEC.md`, `TEST-SPEC.md`, `architecture.md`, `glossary.md`,
  `interfaces.md`, `operations.md`, `queries.md`, `states.md`, `BACKLOG.md` and `discovery/`.
  No README of its own — start from `SPEC.md`.
- **`ui-studio/`**: Control plane plus UI-fitness harness. `status: draft`,
  `authority: candidate`, `verification: paired-audit-passed`. Three files:
  [README.md](ui-studio/README.md), `discovery.md`, `verification.md`.
- **`validator-fixture/`**: Not a feature. Contains one empty `discovery/` directory, used as a
  validator fixture. No README of its own.

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| governed-by | [`../decisions/`](../decisions/) — scope authority for these packages |
| sibling-of | [`../discovery/`](../discovery/) — discoveries not owned by a single feature |
| emits | [`../signals/pipeline-signals.jsonl`](../signals/pipeline-signals.jsonl) — every current signal names `agents-communication-infra` |
