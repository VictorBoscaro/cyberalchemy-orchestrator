#!/usr/bin/env node
import path from "node:path";
import { fileURLToPath } from "node:url";
import { BusError, PublicationBus } from "./bus.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

function contextFromEnvironment() {
  if (!process.env.BUS_CONTEXT_JSON) {
    throw new Error("BUS_CONTEXT_JSON is required; see README.md");
  }
  return JSON.parse(process.env.BUS_CONTEXT_JSON);
}

const bus = new PublicationBus({
  journalPath: process.env.BUS_JOURNAL_PATH || path.join(root, ".data", "journal.jsonl"),
  phaseStatePath: process.env.BUS_PHASE_STATE_PATH || path.join(root, ".data", "phase-state.json"),
  context: contextFromEnvironment(),
});

const tool = {
  name: "bus_publish",
  description: "Publish this seat's official contribution. Success returns the receipt that MUST be included in the final response. Identity and phase come from the authenticated server context, not tool arguments.",
  inputSchema: {
    type: "object",
    additionalProperties: false,
    required: ["idempotency_key", "operation_id", "round_id", "message_type", "payload"],
    properties: {
      idempotency_key: { type: "string", minLength: 1 },
      operation_id: { type: "string", minLength: 1 },
      round_id: { type: "string", minLength: 1 },
      message_type: { type: "string", minLength: 1 },
      reply_to_message_ids: { type: "array", items: { type: "string", minLength: 1 } },
      payload: { description: "JSON contribution to persist." },
    },
  },
};

function send(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function ok(id, result) {
  if (id !== undefined) send({ jsonrpc: "2.0", id, result });
}

function fail(id, code, message) {
  if (id !== undefined) send({ jsonrpc: "2.0", id, error: { code, message } });
}

async function dispatch(message) {
  const { id, method, params = {} } = message;
  if (method === "initialize") {
    ok(id, {
      protocolVersion: params.protocolVersion || "2024-11-05",
      capabilities: { tools: { listChanged: false } },
      serverInfo: { name: "agent-bus-publication-probe", version: "0.1.0" },
    });
  } else if (method === "ping") {
    ok(id, {});
  } else if (method === "tools/list") {
    ok(id, { tools: [tool] });
  } else if (method === "tools/call") {
    if (params.name !== tool.name) {
      fail(id, -32602, `unknown tool: ${params.name}`);
      return;
    }
    try {
      const receipt = await bus.publish(params.arguments);
      ok(id, { content: [{ type: "text", text: JSON.stringify(receipt, null, 2) }] });
    } catch (error) {
      const code = error instanceof BusError ? error.code : "internal_error";
      ok(id, {
        isError: true,
        content: [{ type: "text", text: JSON.stringify({ error: code, message: error.message }) }],
      });
    }
  } else if (!method.startsWith("notifications/")) {
    fail(id, -32601, `method not found: ${method}`);
  }
}

let input = "";
process.stdin.on("data", (chunk) => {
  input += chunk.toString("utf8");
  while (true) {
    const boundary = input.indexOf("\n");
    if (boundary < 0) return;
    const line = input.slice(0, boundary).replace(/\r$/, "");
    input = input.slice(boundary + 1);
    if (!line.trim()) continue;
    Promise.resolve().then(() => dispatch(JSON.parse(line))).catch((error) => {
      console.error(error.stack || error.message);
      process.exitCode = 1;
    });
  }
});
