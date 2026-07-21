// Canonical pool loader + derived closed vocabulary.
// Single source of truth lives in THIS repo (owner decision 2026-07-20):
//   cyberalchemy-orchestrator/telemetry/agents/agent-pool.yaml
// The server always resolves it relative to itself, so cross-repo consumers that
// point their MCP config at this server file read the same canonical pool.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// src/ -> agent-pool-mcp/ -> tools/ -> <repo root>
const DEFAULT_POOL = path.resolve(__dirname, "../../../telemetry/agents/agent-pool.yaml");

export const POOL_PATH = process.env.AGENT_POOL_PATH
  ? path.resolve(process.env.AGENT_POOL_PATH)
  : DEFAULT_POOL;

let _cache = null;

// Loads once and re-parses only when the file's mtime changes (the pool churns —
// v0.5.0 landed the same day it was tagged — so we never want a stale in-memory copy).
export function loadPool() {
  const stat = fs.statSync(POOL_PATH);
  if (_cache && _cache.mtimeMs === stat.mtimeMs) return _cache;
  // The pool is Markdown-style front-matter (`---` header `---` body), i.e. TWO YAML
  // documents: the metadata header, then the `scientists:` list. Load both and take the
  // one that actually carries the roster.
  const docs = yaml.loadAll(fs.readFileSync(POOL_PATH, "utf8"));
  const doc = docs.find((d) => d && Array.isArray(d.scientists)) || {};
  const entries = (doc.scientists || []).filter((e) => e && e.name);
  const tagged = entries.filter((e) => Array.isArray(e.tags) && e.tags.length);
  const vocab = new Set(tagged.flatMap((e) => e.tags));
  const names = new Set(entries.map((e) => e.name));
  _cache = { mtimeMs: stat.mtimeMs, entries, tagged, vocab, names };
  return _cache;
}
