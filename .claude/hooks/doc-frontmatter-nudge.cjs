#!/usr/bin/env node
// PostToolUse guidance for newly created governed Markdown documents.
//
// Scope: root Markdown plus vault/, sessions/, research/, and docs/.
// Exclusions: .claude/, node_modules/, and any templates/ directory.
//
// This hook never edits the document and never supplies placeholder values.
// The creating agent must read .claude/skills/custom/frontmatter.md and author
// the frontmatter and edges. Review is intentionally out of scope for now.

const fs = require("fs");
const path = require("path");

const SCOPED_PREFIXES = ["vault/", "sessions/", "research/", "docs/"];
const ADD_FILE_PATTERN = /^\*\*\* Add File:\s+(.+?)\s*$/gm;

function readStdin() {
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

function repoRoot() {
  return (
    process.env.CLAUDE_PROJECT_DIR ||
    process.env.CODEX_PROJECT_DIR ||
    process.env.CODEX_WORKSPACE_ROOT ||
    process.cwd()
  );
}

function asForwardSlashes(value) {
  return value.split(path.sep).join("/");
}

function relativeGovernedMarkdown(root, candidate) {
  if (typeof candidate !== "string" || !candidate.trim()) return null;
  const absolute = path.isAbsolute(candidate)
    ? path.resolve(candidate)
    : path.resolve(root, candidate);
  const rel = asForwardSlashes(path.relative(root, absolute));
  if (!rel || rel.startsWith("../") || path.isAbsolute(rel)) return null;
  if (!rel.toLowerCase().endsWith(".md")) return null;
  if (
    rel.startsWith(".claude/") ||
    rel.includes("/node_modules/") ||
    rel.startsWith("node_modules/") ||
    rel.split("/").includes("templates")
  ) {
    return null;
  }
  const rootDocument = !rel.includes("/");
  if (!rootDocument && !SCOPED_PREFIXES.some((prefix) => rel.startsWith(prefix))) {
    return null;
  }
  return { absolute, rel };
}

function stringsInToolInput(toolInput) {
  if (typeof toolInput === "string") return [toolInput];
  if (!toolInput || typeof toolInput !== "object") return [];
  return Object.values(toolInput).filter((value) => typeof value === "string");
}

function candidatePaths(input) {
  const toolInput = input && input.tool_input;
  const candidates = new Set();
  if (toolInput && typeof toolInput === "object") {
    for (const key of ["file_path", "path", "filename"]) {
      if (typeof toolInput[key] === "string") candidates.add(toolInput[key]);
    }
  }
  for (const value of stringsInToolInput(toolInput)) {
    for (const match of value.matchAll(ADD_FILE_PATTERN)) {
      candidates.add(match[1]);
    }
  }
  return [...candidates];
}

function inspectDocument(text) {
  const hasFrontmatter = /^\uFEFF?---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/.test(text);
  const hasConnections = /^##\s+Connections\s*$/m.test(text);
  const gaps = [];
  if (!hasFrontmatter) gaps.push("YAML frontmatter");
  if (!hasConnections) gaps.push("a `## Connections` edge section");
  return gaps;
}

function main() {
  let input;
  try {
    input = JSON.parse(readStdin() || "{}");
  } catch {
    process.exit(0);
  }

  const root = path.resolve(repoRoot());
  const documents = [];

  for (const candidate of candidatePaths(input)) {
    const governed = relativeGovernedMarkdown(root, candidate);
    if (!governed || !fs.existsSync(governed.absolute)) continue;
    let content;
    try {
      content = fs.readFileSync(governed.absolute, "utf8");
    } catch {
      continue;
    }
    documents.push({ rel: governed.rel, gaps: inspectDocument(content) });
  }

  if (!documents.length) process.exit(0);

  const lines = documents.map(({ rel, gaps }) => {
    const observation = gaps.length
      ? `currently missing ${gaps.join(" and ")}`
      : "has both structural surfaces; verify their fields and edge semantics";
    return `- \`${rel}\`: ${observation}.`;
  });

  const message = [
    "Governed Markdown authoring obligation:",
    ...lines,
    "- Before finishing this creation, read `.claude/skills/custom/frontmatter.md`.",
    "- The creating agent must author the applicable frontmatter fields and meaningful typed Connections itself; the hook does not fill them.",
    "- Prefer the documented vocabularies. `artifact_kind: others` and edge type `other` are valid only after no listed value fits.",
    "- Never fabricate a connection target. If no real connection is known, keep `## Connections` and state that explicitly.",
    "- No automatic review is required at this stage.",
  ].join("\n");

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PostToolUse",
        additionalContext: message,
      },
    })
  );
}

main();
