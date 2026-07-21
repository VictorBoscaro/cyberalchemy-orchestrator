---
tags: [agent-pool, mcp-server, agent-selection, boundary-adjudication, dispatch-wiring]
node_type: spec
is_session: true
layer: architecture
nature: technical
status: active
created: 2026-07-20
timestamp: 2026-07-20T21:35:54-03:00
expires: 2026-09-18
conversation_id: 15084df5-0e93-498f-be44-402fd6eb8d58
decisions_made: true
contradictions_found: false
specs_updated: [telemetry/agents/agent-pool.yaml, research/agent-name-selection-arch/findings.md]
promoted_candidates: []
expected_importance: 6
importance_rationale: "New infra (MCP selection server) and a fixed latent YAML bug are built and verified, but not yet wired into the dispatch pipeline — impact is real but unrealized."
---

# agent_name selection becomes a cross-repo MCP server

## Summary

Ported the agent pool from domainspec-lean-formalization (v0.5.0, 419 entries under the new
`cited`+`tags` schema) into `telemetry/agents/agent-pool.yaml`, re-framing the header to the
subagents-strategy context while carrying entries verbatim. Diagnosed how `agent_name` selection
works today: a manual, nullable free string, tag-blind and disconnected from the check-tension
gate, so the v0.5.0 tags sit unused. At the user's request ran a tensioned two-agent research
dispatch (minimalist vs systems-retrieval) to choose the selection architecture, registered and
closed in the ledger; both poles rejected RAG and MCP-for-retrieval and ranked a deterministic
tag-overlap script #1 (findings.md). The user then surfaced a use the poles had not covered —
MCP-for-boundary-adjudication: an agent may coin a new tag only after we guarantee the concept is
not already in the vocabulary under another name, which a set-intersection cannot answer because
it is semantic, not lexical. Decision revised to a cross-repo MCP server with the canonical pool
kept here; built `tools/agent-pool-mcp/` — a deterministic core (`search_pool`, `check_vocab`)
plus a cheap-Haiku boundary adjudicator (`recommend_agents`) that validates names against the pool
and rejects an already-existing "new" tag. Verified with a deterministic smoke test and an
end-to-end MCP client handshake (three tools registered, calls return over the wire). Building it
exposed and fixed a latent bug: the pool's Markdown front-matter carried unquoted colon-space
scalars — invalid YAML no machine had parsed before. Investigated wiring the MCP into the dispatch
pipeline by hook rather than skill and found the pattern (a PreToolUse:Agent reminder hook emitting
`additionalContext`, like remind-register-dispatch.cjs). Finally, the user set a durable
portability constraint — the repo will be installed on other machines per user taste — which
revised the earlier global/absolute-path wiring plan toward repo-local, `$CLAUDE_PROJECT_DIR`-
relative, opt-in config; nothing is wired yet.

## Open questions

- Does naive tag-overlap miss enough conceptually-adjacent candidates to justify a static
  tag-cluster table? Undecided pending a measured false-negative rate of the deterministic scorer
  against real past dispatch angles.

## Next steps

- Wire the agent-pool MCP into the pipeline **repo-locally**: a project `.mcp.json` and a
  PreToolUse:Agent reminder hook, both `$CLAUDE_PROJECT_DIR`-relative — never global/absolute.
- Integrate `recommend_agents` as the selection step in `register-dispatch`, where `agent_name`
  is currently a bare string-or-null field.
- Point domainspec-lean-formalization at this server as a consumer instead of its pool copy.

## Recommendation

Wire the verified server into the pipeline repo-locally as the next concrete move. Licensing fact:
the end-to-end MCP handshake passed — the three tools are callable over the wire — so the server is
proven and only wiring plus the portability discipline remain. Keep the tag-cluster-table question
(Open questions) deferred until the wiring lands and the false-negative measurement exists.

## Files touched

- telemetry/agents/agent-pool.yaml
- telemetry/agents/subagents-dispatch.yaml
- tools/agent-pool-mcp/package.json
- tools/agent-pool-mcp/package-lock.json
- tools/agent-pool-mcp/README.md
- tools/agent-pool-mcp/src/pool.mjs
- tools/agent-pool-mcp/src/select.mjs
- tools/agent-pool-mcp/src/adjudicate.mjs
- tools/agent-pool-mcp/src/server.mjs
- tools/agent-pool-mcp/scripts/smoke.mjs
- tools/agent-pool-mcp/scripts/rpc-test.mjs
- research/agent-name-selection-arch/findings.md
- .gitignore
