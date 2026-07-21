---
tags: [agents, dispatch, skills, ledger]
node_type: audit
is_session: true
layer: architecture, domain
nature: explanatory
status: active
created: 2026-07-21
timestamp: 2026-07-21T02:13:38-03:00
expires: 2026-09-19
conversation_id: unknown
decisions_made: true
contradictions_found: true
specs_updated: [README.md, telemetry/agents/agent-pool.yaml, .claude/skills/register-dispatch/append-dispatch.cjs, .claude/skills/register-dispatch/SKILL.md, tools/agent-pool-mcp/src/server.mjs]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Corrected load-bearing README drift and extended the agent role vocabulary across appender/MCP/docs, but exposed an unresolved repo-local/global appender divergence and left the audit and pool sync uncommitted, so the value is contingent on follow-up landing."
---

# README audit, role-vocab extension to 7, and agent-pool re-sync to v0.6.0

## Summary

The session began as a first-orientation-plus-audit of the root README against the actual repository tree, run through three read-only explorer dispatches recorded in the ledger under the repo's own framework-as-instance discipline. The audit found the README's "~700 dispatches / 11 repos" figure conflated the cross-repo aggregate with this repo's own ~30-dispatch ledger, a dead `docs/readme-candidates` reference, an incomplete role enum, constitutions mislabeled "ratified" instead of candidate, and several missing artifacts (`vault/axioms`, `vault/audit`, two more hypotheses, named research, BACKLOG, sessions). With the user choosing a "factual + gaps" scope, nine fixes were applied, then two tensioned reviewers (accuracy-to-disk vs document-coherence) verified them and drove further corrections — 49 not 48 rows, a narrowed strict-appender wording so it no longer contradicts the enum-drift audit, `test_main.py`, a skill-name unification, and an axioms navigation row. On the user's instruction the agent role vocabulary was extended to seven — `synthesizer` (a pre-existing drift fix) plus `planner` and `coder` — scoped repo-local + MCP by the user's explicit choice, touching the repo-local appender's `AGENT_ROLES`, the MCP server's `ROLE` z.enum, the repo `SKILL.md`, and the README, deliberately leaving the machine-global `~/.claude` skill untouched to respect portability. This exposed a live divergence: the repo-local and global appenders now disagree (7 vs 5 roles) and their two `SKILL.md` copies point at different appenders. Finally the canonical `agent-pool.yaml` (v0.5.0) was re-synced against its upstream in `domainspec-lean-formalization` (v0.6.0): upstream entries were brought over verbatim (414 entries after 5 fabricated names were removed, 8 identity fixes, a new `management` field) while the repo-specific header framing was preserved and bumped to v0.6.0. The merge was verified — 414 entries, valid two-document YAML, LF line-endings, clean MCP load (`entries=414 tagged=414 vocab=721`). Nothing was committed by this session; the README audit and pool sync remain in the working tree, while a concurrent external actor committed the role change (`b3dec85`) and unrelated OBL-E3/meta-ontology work (`9e83252`).

## Contradictions

- validates `vault/audit/ledger-enum-drift-finding.md` — the README's strict-appender wording was narrowed specifically so it no longer overclaims past this audit's enum-drift finding; documentation was re-aligned to an established audit result, not disputed.
- contradicts `vault/constitution/engine-constitution.md` (EG-1, single-writer/strict-appender) — the newly surfaced repo-local/global appender divergence (7 vs 5 roles), together with the concurrent external commits to the same working tree, is a live counterexample to EG-1's single-writer/strict-appender guarantee; the session narrowed the README so it no longer asserts that guarantee holds unconditionally, and left EG-1 blocked rather than resolved.

## Open questions

- Should content edits to the agent pool be made in this repo — the copy the MCP actually loads — with other repos consuming via the MCP, or continue being made upstream in `domainspec-lean-formalization` and re-ported here? This session re-ported v0.6.0 rather than deciding; the "single canonical pool, N consumers" arrangement currently runs in reverse (this repo is the mirror, the upstream is the editor).
- Did the concurrent external commits observed during this session interleave safely? A second writer landing commits in the same working tree while this session worked is unverified against the append-only ledger's integrity.

## Next steps

- Populate `planner`/`coder` into the `role_fit` lists of the relevant entries in `telemetry/agents/agent-pool.yaml`; until then `search_pool(role:"planner")` returns empty even though the enum now accepts it.
- Commit the two working-tree artifacts left by this session — the `README.md` audit and the `agent-pool.yaml` v0.6.0 sync; the role-vocabulary change already landed externally as `b3dec85`.

## Recommendation

The keystone is the pool-flow question: decide where the pool is edited before it diverges again, licensed by the concrete fact that this session had to re-port upstream v0.6.0 by hand. The concurrent-writer open question is the higher risk though — a second writer in the same repo is the precise failure mode the enum-drift audit already named, so confirming the ledger was not interleaved should come before the next dispatch. Both are hunches pending verification, not established results.

## Files touched

- README.md
- telemetry/agents/agent-pool.yaml
- telemetry/agents/subagents-dispatch.yaml
- .claude/skills/register-dispatch/append-dispatch.cjs
- .claude/skills/register-dispatch/SKILL.md
- tools/agent-pool-mcp/src/server.mjs
