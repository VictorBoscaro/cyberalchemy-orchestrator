#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";
import { verifyReceipt } from "./bus.mjs";

const [resultPath, journalPath] = process.argv.slice(2);
if (!resultPath || !journalPath) {
  console.error("usage: node src/verify-result.mjs <subagent-result.json> <journal.jsonl>");
  process.exit(2);
}

try {
  const result = JSON.parse(await readFile(path.resolve(resultPath), "utf8"));
  const event = await verifyReceipt({ journalPath, receipt: result.publication_receipt });
  console.log(JSON.stringify({ accepted: true, event_id: event.event_id, message_id: event.message_id }));
} catch (error) {
  console.error(JSON.stringify({ accepted: false, error: error.code || "invalid_result", message: error.message }));
  process.exit(1);
}
