---
tags: [docs, signals, telemetry, append-only, reflection-loop, index]
node_type: readme
is_session: false
layer: [application, runtime]
nature: reference
status: active
version: 0.1.0
last_updated: 2026-07-25
---

# docs/signals

## 1. What is this?

The append-only structured signal log emitted at the end of DomainSpec agent sessions. Each line
is one JSON signal envelope recording something the session observed about the pipeline itself —
a decision taken, a governance gap, a rework, a recurring pattern.

## 2. Business Context

Signals feed the asynchronous reflection loop: the machine writing specs is asked to record where
its own process leaked, so that the process can be corrected rather than the symptom re-fixed each
time. [`.claude/skills/domainspec-emit-signals/SKILL.md`](../../.claude/skills/domainspec-emit-signals/SKILL.md)
is the sole owner of this folder and is a mandatory session epilogue for every DomainSpec agent —
invoked at Step 10 when the full pipeline orchestrates a session, and by the agent's own final
step when it runs standalone.

## 3. Why it matters

This is a machine-written log with a contract that is not visible from inside the folder. The
owning skill states two rules an agent or human editing by hand would break: signals are
**appended as one JSON line each and existing content is never overwritten**
([SKILL.md:59](../../.claude/skills/domainspec-emit-signals/SKILL.md#L59)), and a new signal is
**skipped if the last 20 lines already carry the same `type`, `feature` and `data.description`**
([SKILL.md:70](../../.claude/skills/domainspec-emit-signals/SKILL.md#L70)). Reformatting the file,
sorting it, or rewriting a line destroys both the append-only guarantee and the deduplication
window that depends on line order.

## 📁 Navigation

- **[pipeline-signals.jsonl](pipeline-signals.jsonl)**: The signal log. One JSON object per line.
  As of 2026-07-25 it holds 13 records, all carrying `feature: agents-communication-infra`, split
  by `type` into 5 `decision`, 3 `rework`, 2 `pattern`, 1 `governance-gap`, 1 `proposal` and
  1 `spec-gap`; by `severity` into 9 `LOW`, 3 `MEDIUM` and 1 `HIGH`. Envelope fields include
  `id`, `timestamp`, `session`, `feature`, `domainspecVersion`, `pipelineMode`, `source`, `type`,
  `severity`, `category` and a nested `data` object. The envelope and type definitions are owned
  by `domainspec/templates/SIGNAL-SCHEMA.md`.

## Connections

| Edge | Target |
|---|---|
| indexed-by | [`../README.md`](../README.md) — the `docs/` index |
| written-by | [`../../.claude/skills/domainspec-emit-signals/SKILL.md`](../../.claude/skills/domainspec-emit-signals/SKILL.md) — sole writer, append-only |
| observed-by | `.claude/skills/signal-observer/SKILL.md` — the observer side of the reflection loop |
| about | [`../features/agents-communication-infra/`](../features/agents-communication-infra/) — the feature every current record names |
