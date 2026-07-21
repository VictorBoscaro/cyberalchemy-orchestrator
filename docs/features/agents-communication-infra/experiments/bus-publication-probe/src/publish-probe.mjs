#!/usr/bin/env node
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");

function option(name) {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : undefined;
}

const runId = option("--run-id");
const content = option("--content");
if (!runId || !/^[a-zA-Z0-9._-]+$/.test(runId) || !content) {
  console.error("usage: node src/publish-probe.mjs --run-id <safe-id> --content <contribution>");
  process.exit(2);
}

const runDir = path.join(root, ".data", runId);
const context = {
  run_id: runId,
  dispatch_id: `dispatch-${runId}`,
  group_id: "group-real-agent-probe",
  group_version: 1,
  seat_id: "seat-a",
  agent_instance_id: "real-subagent-a-1",
  attempt_id: "attempt-a-1",
  actor_principal_id: "principal-seat-a",
  phase: "collect",
};

const child = spawn(process.execPath, [path.join(here, "mcp-server.mjs")], {
  env: {
    ...process.env,
    BUS_CONTEXT_JSON: JSON.stringify(context),
    BUS_JOURNAL_PATH: path.join(runDir, "journal.jsonl"),
    BUS_PHASE_STATE_PATH: path.join(runDir, "phase-state.json"),
  },
  stdio: ["pipe", "pipe", "inherit"],
});

let nextId = 0;
let buffer = "";
const pending = new Map();
child.stdout.on("data", (chunk) => {
  buffer += chunk.toString("utf8");
  while (true) {
    const newline = buffer.indexOf("\n");
    if (newline < 0) return;
    const line = buffer.slice(0, newline).replace(/\r$/, "");
    buffer = buffer.slice(newline + 1);
    if (!line.trim()) continue;
    const message = JSON.parse(line);
    pending.get(message.id)?.(message);
    pending.delete(message.id);
  }
});

function rpc(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = ++nextId;
    const timeout = setTimeout(() => reject(new Error(`timeout waiting for ${method}`)), 5000);
    pending.set(id, (message) => {
      clearTimeout(timeout);
      if (message.error) reject(new Error(message.error.message));
      else resolve(message.result);
    });
    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`);
  });
}

try {
  await rpc("initialize", { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "real-subagent-probe", version: "0.1.0" } });
  const result = await rpc("tools/call", {
    name: "bus_publish",
    arguments: {
      idempotency_key: `position:seat-a:${runId}`,
      operation_id: `operation:${runId}:seat-a`,
      round_id: "round-1",
      message_type: "position",
      payload: { content },
    },
  });
  if (result.isError) throw new Error(result.content?.[0]?.text || "bus publication failed");
  const receipt = JSON.parse(result.content[0].text);
  console.log(JSON.stringify({ publication_receipt: receipt }));
} finally {
  child.kill();
}
