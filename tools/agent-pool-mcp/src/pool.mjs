// Canonical pool loader + derived closed vocabulary.
// Single source of truth lives in THIS repo (owner decision 2026-07-20):
//   cyberalchemy-orchestrator/telemetry/agents/agent-pool.yaml
// The server always resolves it relative to itself, so cross-repo consumers that
// point their MCP config at this server file read the same canonical pool.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import yaml from "js-yaml";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// src/ -> agent-pool-mcp/ -> tools/ -> <repo root>
const DEFAULT_POOL = path.resolve(__dirname, "../../../telemetry/agents/agent-pool.yaml");
const REPO_ROOT = path.resolve(__dirname, "../../..");
const ROLE_SELECTION_PATH = path.join(REPO_ROOT, "implementations/contracts/agent-role-registry-selection.json");
const POOL_AUTHORITY_PATH = path.join(REPO_ROOT, "implementations/contracts/agent-pool-authority.v1.json");

export const POOL_PATH = process.env.AGENT_POOL_PATH
  ? path.resolve(process.env.AGENT_POOL_PATH)
  : DEFAULT_POOL;

let _cache = null;

function sha256(raw) {
  return "sha256:" + crypto.createHash("sha256").update(raw).digest("hex");
}

function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map((key) => [key, stable(value[key])]));
  }
  return value;
}

function loadRoleRegistry() {
  const selection = JSON.parse(fs.readFileSync(ROLE_SELECTION_PATH, "utf8"));
  if (!selection || selection.schema !== "aci.role-registry-selection@1" || !selection.selected_ref ||
      typeof selection.registry_path !== "string" || typeof selection.authority_path !== "string") {
    throw new Error("agent role registry selection is malformed");
  }
  const resolveSelected = (relative) => {
    const selected = path.resolve(REPO_ROOT, relative);
    const prefix = REPO_ROOT.endsWith(path.sep) ? REPO_ROOT : REPO_ROOT + path.sep;
    if (!selected.startsWith(prefix)) throw new Error("agent role registry selection escapes repository root");
    return selected;
  };
  const registryPath = resolveSelected(selection.registry_path);
  const authorityPath = resolveSelected(selection.authority_path);
  const raw = fs.readFileSync(registryPath);
  const registry = JSON.parse(raw.toString("utf8"));
  const authority = JSON.parse(fs.readFileSync(authorityPath, "utf8"));
  if (!registry || registry.schema !== "aci.role-registry@1" || registry.name !== "aci.agent-roles" ||
      !Array.isArray(registry.roles) || registry.roles.length === 0 || !authority ||
      authority.schema !== "aci.role-registry-authority@1" || !Array.isArray(authority.accepted)) {
    throw new Error("agent role registry authority is malformed");
  }
  const ref = { name: registry.name, version: registry.version, digest: sha256(raw) };
  const accepted = authority.accepted.filter((row) => row && row.name === ref.name && row.version === ref.version);
  if (accepted.length !== 1 || accepted[0].digest !== ref.digest || JSON.stringify(selection.selected_ref) !== JSON.stringify(ref)) throw new Error("agent role registry is not the selected accepted immutable revision");
  const roleIds = registry.roles.map((row) => row?.role_id);
  if (new Set(roleIds).size !== roleIds.length || registry.roles.some((row) => !row || row.enabled !== true || typeof row.purpose !== "string" || !row.purpose.trim())) {
    throw new Error("agent role registry rows are invalid");
  }
  return { ref, roles: new Set(roleIds) };
}

// Loads once and re-parses only when the file's mtime changes (the pool churns —
// v0.5.0 landed the same day it was tagged — so we never want a stale in-memory copy).
export function loadPool() {
  const stat = fs.statSync(POOL_PATH);
  if (_cache && _cache.mtimeMs === stat.mtimeMs) return _cache;
  // The pool is Markdown-style front-matter (`---` header `---` body), i.e. TWO YAML
  // documents: the metadata header, then the `scientists:` list. Load both and take the
  // one that actually carries the roster.
  const raw = fs.readFileSync(POOL_PATH);
  const authority = JSON.parse(fs.readFileSync(POOL_AUTHORITY_PATH, "utf8"));
  if (!authority || authority.schema !== "aci.agent-pool-authority@1" || authority.source_raw_digest !== sha256(raw)) {
    throw new Error("canonical agent pool bytes differ from authority");
  }
  const docs = yaml.loadAll(raw.toString("utf8"));
  if (docs.length !== 2 || !docs[0] || typeof docs[0] !== "object" || !docs[1] ||
      typeof docs[1] !== "object" || Object.keys(docs[1]).length !== 1 || !Array.isArray(docs[1].scientists)) {
    throw new Error("canonical agent pool must contain metadata then one scientists roster");
  }
  const metadata = docs[0];
  const metadataKeys = ["profile", "name", "description", "node_type", "layer", "nature", "status", "version", "last_updated", "source", "notes"];
  if (Object.keys(metadata).sort().join("|") !== [...metadataKeys].sort().join("|") ||
      metadata.profile !== "subagents-strategy" || metadata.node_type !== "agent-pool" || metadata.status !== "active" || metadata.version !== "0.7.0") {
    throw new Error("canonical agent pool metadata drifted");
  }
  const roleRegistry = loadRoleRegistry();
  const allowedEntryKeys = new Set(["agent_name", "field", "era", "role_fit", "cited", "tags", "note"]);
  const entries = docs[1].scientists;
  const names = new Set();
  for (const [index, entry] of entries.entries()) {
    if (!entry || typeof entry !== "object" || Array.isArray(entry)) throw new Error(`scientists[${index}] must be an object`);
    const identityKeys = ["agent_name", "name", "agent-name"].filter((key) => Object.hasOwn(entry, key));
    if (identityKeys.length !== 1 || identityKeys[0] !== "agent_name") throw new Error(`scientists[${index}] must use only agent_name`);
    if (Object.keys(entry).some((key) => !allowedEntryKeys.has(key))) throw new Error(`scientists[${index}] has an unknown key`);
    if (typeof entry.agent_name !== "string" || !entry.agent_name.trim() || names.has(entry.agent_name)) throw new Error(`scientists[${index}].agent_name is invalid or duplicate`);
    if (!Array.isArray(entry.role_fit) || entry.role_fit.length === 0 || entry.role_fit.some((role) => !roleRegistry.roles.has(role))) throw new Error(`scientists[${index}].role_fit is outside the accepted registry`);
    names.add(entry.agent_name);
  }
  if (entries.length !== authority.entry_count) throw new Error("canonical agent pool entry count drifted");
  const tagged = entries.filter((e) => Array.isArray(e.tags) && e.tags.length);
  const vocab = new Set(tagged.flatMap((e) => e.tags));
  const normalized = { schema: "aci.normalized-agent-pool@1", name: metadata.name, version: metadata.version,
    agents: entries.map((entry) => ({ display_name: entry.agent_name, role_fit: entry.role_fit })) };
  const normalizedDigest = sha256(Buffer.from(JSON.stringify(stable(normalized)), "utf8"));
  if (!authority.agent_pool_ref || authority.agent_pool_ref.name !== metadata.name || authority.agent_pool_ref.version !== metadata.version || authority.agent_pool_ref.digest !== normalizedDigest) {
    throw new Error("canonical agent pool normalized reference drifted");
  }
  _cache = { mtimeMs: stat.mtimeMs, entries, tagged, vocab, names, roleRegistry };
  return _cache;
}
