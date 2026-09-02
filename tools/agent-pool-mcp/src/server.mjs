#!/usr/bin/env node
// agent-pool MCP server. Cross-repo: point any repo's MCP config at THIS file; it always
// reads the canonical pool in cyberalchemy-orchestrator/telemetry/agents/agent-pool.yaml.
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { checkVocab, searchPool } from "./select.mjs";
import { recommendAgents } from "./adjudicate.mjs";
import { loadPool, POOL_PATH } from "./pool.mjs";

const acceptedRoles = [...loadPool().roleRegistry.roles];
const ROLE = z.string().refine((value) => acceptedRoles.includes(value), {
  message: `role must be one of ${acceptedRoles.join(" | ")}`,
});
const server = new McpServer({ name: "agent-pool", version: "0.1.0" });

server.tool(
  "recommend_agents",
  "Recommend up to N agent personas (unordered) from the pool for a subagent dispatch. Boundary path: deterministic prefilter + a cheap LLM that judges fit AND whether the objective needs a concept not yet in the closed tag vocabulary (guards against silently coining a duplicate tag). Names are validated against the pool before return.",
  {
    objective: z.string().describe("Short statement of what the agent will do."),
    tags: z.array(z.string()).describe("Desired topical tags, ideally from the closed vocabulary."),
    role: ROLE.optional(),
    exclude: z.array(z.string()).optional().describe("agent_names already chosen in this dispatch (avoid clones)."),
    n: z.number().int().positive().max(10).optional(),
  },
  async (args) => {
    const res = await recommendAgents({ ...args, n: args.n || 5 });
    return { content: [{ type: "text", text: JSON.stringify(res, null, 2) }] };
  },
);

server.tool(
  "search_pool",
  "Deterministic fast path (no LLM): rank pool entries by tag-overlap intersect role_fit. Use when the caller already knows the right vocabulary tags.",
  {
    tags: z.array(z.string()),
    role: ROLE.optional(),
    exclude: z.array(z.string()).optional(),
    k: z.number().int().positive().max(25).optional(),
  },
  async (args) => {
    const res = searchPool({ ...args, k: args.k || 10 });
    return { content: [{ type: "text", text: JSON.stringify(res, null, 2) }] };
  },
);

server.tool(
  "check_vocab",
  "Pure deterministic vocabulary membership: which tags exist in the closed vocabulary, which do not, and cheap 'did you mean' suggestions. Answers 'does what I want already exist?' before a new tag is coined.",
  { tags: z.array(z.string()) },
  async ({ tags }) => ({
    content: [{ type: "text", text: JSON.stringify(checkVocab(tags), null, 2) }],
  }),
);

const transport = new StdioServerTransport();
await server.connect(transport);
const p = loadPool();
console.error(`agent-pool MCP up · ${POOL_PATH} · ${p.entries.length} entries, ${p.vocab.size} tags`);
