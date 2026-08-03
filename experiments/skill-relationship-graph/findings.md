# Skill relationship graph — result

This is a static declaration graph, not runtime invocation proof.

## Verdict

**SURVIVED** — the graph is non-empty and exposes multiple structural classes.

## Summary

- Skills parsed: 72 / 72
- Inclusive edges: 258
- Strong (`SKILL.md` path) edges: 7
- Unresolved explicit paths: 0

## Strong view

- Sources: 3
- Sinks: 6
- Isolated: 63
- Connected: 0
- Non-isolated skills: `discovery-writing`, `domainspec-subagents-strategy`, `experiment`, `experiment-initial-definitions`, `register-dispatch`, `research`, `research-initial-definitions`, `review`, `subagents-dispatch-lifecycle`

## Inclusive structural classes

### source (6)

`discipline-governance`, `domainspec-emit-signals`, `domainspec-spec-feature`, `mint`, `orchestrate`, `reading-learning-package`

### sink (17)

`architecture-pattern-inventory`, `context-builder`, `decision-gate`, `definitions-governance`, `distill`, `domainspec-implement`, `experiment-initial-definitions`, `feature-glossary`, `implementation-layering`, `observability-setup`, `ontology-vault`, `research-initial-definitions`, `robot-talks`, `scope-interview`, `signal-observer`, `workflow-reflect`, `x-ray`

### isolated (6)

`backlog`, `close-session`, `commit-message`, `create-skill`, `domainspec-feature-glossary`, `emit-topic-tags`

### connected (43)

`arcanum-bootstrap`, `codex-goal-profile`, `constitution-governance`, `craft`, `discovery-to-inventory`, `discovery-writing`, `dispatch-spec`, `domainspec-subagents-strategy`, `engineer-view`, `experiment`, `experiment-harness`, `guide-architecture`, `implementation-readiness`, `interrogation`, `inventory`, `invoke`, `invoke-example-runner`, `necronomicon`, `observed-invocation-loop`, `ontology-harness`, `ontology-view`, `paired-views`, `publication-research-pipeline`, `refine`, `register-dispatch`, `repository-harness`, `research`, `research-evidence-harness`, `research-tower`, `residuality-spec`, `review`, `sigil-development`, `sigil-maintenance-loop`, `sigil-runtime-installer`, `skill-decomposer`, `skill-transcriptor`, `spellcraft`, `structured-interview-kits`, `subagents-dispatch-lifecycle`, `system-view`, `task-session`, `ux-evidence-validator`, `whisper`

## Highest-degree skills

| skill | in | out | total |
|---|---:|---:|---:|
| `orchestrate` | 0 | 44 | 44 |
| `necronomicon` | 2 | 22 | 24 |
| `invoke` | 10 | 11 | 21 |
| `decision-gate` | 16 | 0 | 16 |
| `sigil-development` | 11 | 5 | 16 |
| `spellcraft` | 11 | 4 | 15 |
| `task-session` | 12 | 2 | 14 |
| `context-builder` | 13 | 0 | 13 |
| `inventory` | 11 | 2 | 13 |
| `domainspec-subagents-strategy` | 6 | 6 | 12 |
| `experiment-harness` | 9 | 3 | 12 |
| `publication-research-pipeline` | 1 | 11 | 12 |
| `guide-architecture` | 1 | 10 | 11 |
| `ontology-harness` | 4 | 7 | 11 |
| `observed-invocation-loop` | 1 | 9 | 10 |

## Interpretation boundary

- `explicit_path` is strong evidence of a declared dependency or routing relation.
- `named_reference` is weaker: it proves a textual mention, not a call.
- A `source`, `sink`, or `isolated` label is structural, not a quality verdict.
- Runtime truth should later add edges from hooks, scripts, dispatches, and telemetry.

Machine-readable outputs: `graph.json` and `graph.dot`.
