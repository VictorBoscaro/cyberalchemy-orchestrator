# agent-pool-mcp

Cross-repo MCP server that selects subagent `agent_name`s from the **canonical agent
pool**. Point any repo's MCP config at this server and it reads one source of truth:
`cyberalchemy-orchestrator/telemetry/agents/agent-pool.yaml` (owner decision 2026-07-20).

## Why it exists

Today `agent_name` is a manual, nullable free string, tag-blind and disconnected from the
check-tension gate. A pure deterministic script can rank by tag-overlap but **cannot** tell
whether a concept a dispatcher wants is *already in the vocabulary under a different name* —
that needs semantic judgment. So this server splits the job:

- **deterministic core** (`select.mjs`) — vocab membership, tag-overlap ranking. Exact, testable.
- **cheap LLM boundary** (`adjudicate.mjs`) — a Haiku call that judges fit and coverage, with
  its picks **validated against the pool** and any "new" tag that already exists **rejected
  deterministically**. Two-layer guarantee against silently coining a duplicate tag.

## Tools

| tool | LLM? | returns |
|---|---|---|
| `recommend_agents({objective, tags, role?, exclude?, n?})` | yes (Haiku) | up to N names **unordered**, `proposed_new_tag` (or null), `proposed_already_exists`, `dropped_invalid`, vocab check |
| `search_pool({tags, role?, exclude?, k?})` | no | top-K candidates by `overlap ∩ role_fit`, deterministic order |
| `check_vocab({tags})` | no | `{known, unknown, suggestions}` — "does what I want already exist?" |

## Install & test

```sh
cd tools/agent-pool-mcp
npm install
npm run smoke          # deterministic paths, no API key needed
```

## Register (cross-repo, user scope)

Add to `~/.claude.json` (or a repo's `.mcp.json`) so every repo sees it:

```json
{
  "mcpServers": {
    "agent-pool": {
      "command": "node",
      "args": ["C:\\Users\\victo\\cyberalchemy-orchestrator\\tools\\agent-pool-mcp\\src\\server.mjs"],
      "env": { "ANTHROPIC_API_KEY": "sk-ant-..." }
    }
  }
}
```

Without `ANTHROPIC_API_KEY`, `recommend_agents` degrades gracefully to the deterministic
prefilter (mode `deterministic-fallback`); `search_pool` and `check_vocab` never need a key.

## Config

- `AGENT_POOL_PATH` — override the canonical pool path (default: resolved relative to the server).
- `AGENT_POOL_MODEL` — override the adjudicator model (default: `claude-haiku-4-5-20251001`).

## Consumers

`domainspec-lean-formalization` and future repos are **consumers** — they call this server
instead of porting a pool copy that drifts. The canonical pool lives here.
