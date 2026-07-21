#!/usr/bin/env node
// PostToolUse nudge (non-blocking) — reminds to add frontmatter + ## Connections
// when a governed .md document is written. See vault/ontology-conventions.md.
//
// Design (per user decision 2026-07-21):
//   - NUDGE, never blocks: emits additionalContext on exit 0, the Write always lands.
//   - Checks PRESENCE of a frontmatter block AND a `## Connections` section.
//   - Does NOT validate node_type against the enum — a doc may carry a not-yet-valid
//     type on purpose. Presence is the gate; the enum is offered as information only.
//   - Repo-local + path-relative via $CLAUDE_PROJECT_DIR (portability principle).
//
// Scope (docs of the repo): vault/, sessions/, research/, docs/, and root-level *.md.
// Excluded: .claude/, node_modules/, and any templates/ directory.

const fs = require("fs");
const path = require("path");

function readStdin() {
  try {
    return fs.readFileSync(0, "utf-8");
  } catch {
    return "";
  }
}

function main() {
  let input;
  try {
    input = JSON.parse(readStdin() || "{}");
  } catch {
    process.exit(0); // never break the tool on malformed input
  }

  const ti = input.tool_input || {};
  const filePath = ti.file_path;
  const content = typeof ti.content === "string" ? ti.content : "";
  if (!filePath || !filePath.toLowerCase().endsWith(".md")) process.exit(0);

  // Compute a repo-relative, forward-slashed path.
  const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  let rel = path.relative(root, filePath).split(path.sep).join("/");
  if (rel.startsWith("..")) process.exit(0); // outside the repo (e.g. memory files)

  // Exclusions win over inclusions.
  if (
    rel.startsWith(".claude/") ||
    rel.includes("node_modules/") ||
    rel.includes("templates/")
  ) {
    process.exit(0);
  }

  // Inclusions: a scoped subtree, or a root-level .md (no slash in the path).
  const scoped = ["vault/", "sessions/", "research/", "docs/"];
  const isRootDoc = !rel.includes("/");
  const inScope = isRootDoc || scoped.some((p) => rel.startsWith(p));
  if (!inScope) process.exit(0);

  const hasFrontmatter = /^﻿?---\r?\n[\s\S]*?\r?\n---/.test(content);
  const hasConnections = /^##\s+Connections\s*$/m.test(content);
  if (hasFrontmatter && hasConnections) process.exit(0);

  const missing = [];
  if (!hasFrontmatter) missing.push("YAML frontmatter (`---` … `---`)");
  if (!hasConnections) missing.push("a `## Connections` section");

  const msg =
    `ontology-conventions nudge — \`${rel}\` was written without ${missing.join(" and ")}.\n` +
    `The vault convention (vault/ontology-conventions.md) asks every governed doc to carry:\n` +
    `  frontmatter keys: tags, node_type, is_session, layer, nature, status, version, last_updated\n` +
    `    (+ veracity/conviction for belief nodes; + optional private)\n` +
    `  node_type ∈ {axiom, premise, constitution, discovery, implementation-plan, spec,\n` +
    `              audit, conceptual, essay, test, backlog, readme}  — informational; a\n` +
    `              not-yet-valid type is allowed, this nudge does not enforce the enum.\n` +
    `  a \`## Connections\` table of edges (derives-from, grounds, contradicts, …).\n` +
    `If this file is genuinely not a vault node, ignore this reminder.`;

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: msg,
      },
    })
  );
  process.exit(0);
}

main();
