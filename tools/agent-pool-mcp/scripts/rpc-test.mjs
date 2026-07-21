// End-to-end MCP handshake: spawn the server, list tools, call one deterministic tool.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const server = path.resolve(dir, "../src/server.mjs");

const transport = new StdioClientTransport({ command: process.execPath, args: [server] });
const client = new Client({ name: "rpc-test", version: "0" });
await client.connect(transport);

const { tools } = await client.listTools();
console.log("tools:", tools.map((t) => t.name).join(", "));

const r = await client.callTool({
  name: "check_vocab",
  arguments: { tags: ["category-theory", "sheaf-semantics", "not-a-real-tag"] },
});
console.log("check_vocab ->");
console.log(r.content[0].text);

await client.close();
