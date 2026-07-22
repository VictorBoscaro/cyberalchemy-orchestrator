#!/usr/bin/env tsx
/**
 * validate-content.ts — DomainSpec v2 content validator (MT0: Entity exemplar).
 *
 * Checks each concept in an aspect file against the per-meta-type criterion loaded from
 * `spec/meta-types/**\/*.schema.yml` (SCHEMA-CONSTITUTION format). MT0 scope = the Entity criterion
 * (identity + typedness) applied as a decidable table-walk. It validates SHAPE only; it never imports
 * or re-derives the engine `src/rules` δ-algorithm (moat), and never checks semantic satisfiability.
 *
 * Build-from-owned: markdown-table parsing is modeled on `tools/validate-relationships.ts`.
 *
 * Usage:
 *   tsx tools/validate-content.ts                         # walk spec/features/**\/SPEC.md
 *   tsx tools/validate-content.ts --file <aspect.md>      # check one aspect file
 *   tsx tools/validate-content.ts --schema-dir spec/meta-types --mode strict|warn
 */

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join, relative, resolve } from "node:path";

import {
  loadRelationshipAuthority,
  validateRelationshipSpecFile,
} from "./lib/relationship-signatures";
import {
  attributeNonemptyViolation,
  assertCriterionPreflight,
  assertNoDuplicateSchemaKey,
  uiRepairViolation,
} from "./lib/ui-repair-rule-contract";

type Criterion = {
  rule: string;
  column?: string;
  truthy?: string[];
  pattern?: string;
  key?: string;
  value?: string;
  values?: string[];
};
type Schema = {
  meta_type: string;
  criterion?: Record<string, Criterion>;
  [key: string]: unknown;
};
type TableRow = { cells: string[]; authoredCells: string[]; line: number };
type MarkdownTable = { headers: string[]; rows: TableRow[] };
type Violation = {
  file: string;
  concept: string;
  type: string;
  reason: string;
  line: number;
};

const args = process.argv.slice(2);
const mode = getArg("--mode") || "strict";
const schemaDir = resolve(process.cwd(), getArg("--schema-dir") || "spec/meta-types");
const relationshipsPath = resolve(
  process.cwd(),
  getArg("--relationships") || "../definitions/relationships/relationships.yml",
);
const singleFile = getArg("--file");
const featuresRoot = resolve(process.cwd(), getArg("--features-root") || "spec/features");

const schemasByType = loadSchemas(schemaDir);
if (schemasByType.size === 0) {
  console.error(
    `validate-content: no .schema.yml found under ${toRelative(schemaDir)}`,
  );
  process.exit(1);
}

const targets = resolveTargets();
if (targets.length === 0) {
  console.log("validate-content: no aspect files to check");
  process.exit(0);
}

const violations: Violation[] = [];
let conceptsChecked = 0;
let edgesChecked = 0;
const relationshipAuthority = loadRelationshipAuthority(relationshipsPath);

for (const file of targets) {
  const lines = readFileSync(file, "utf-8").split(/\r?\n/);
  const relationshipResult = validateRelationshipSpecFile(file, relationshipAuthority);
  edgesChecked += relationshipResult.edgesChecked;
  for (const relationshipViolation of relationshipResult.violations) {
    violations.push({
      file: relationshipViolation.specPath,
      concept: relationshipViolation.value,
      type: "Relationship",
      reason: `${relationshipViolation.className}: ${relationshipViolation.detail}`,
      line: relationshipViolation.line,
    });
  }

  const registry = parseTableForSection(lines, "Concept Registry");
  if (!registry) {
    continue; // no declared concepts here (e.g. the sample fixture) — nothing to validate
  }
  const headerMap = toHeaderMap(registry.headers);
  const conceptIdx = headerMap.get("concept");
  const typeIdx = headerMap.get("type");
  if (conceptIdx === undefined || typeIdx === undefined) {
    continue;
  }

  for (const row of registry.rows) {
    const concept = (row.cells[conceptIdx] || "").trim();
    const type = (row.cells[typeIdx] || "").trim();
    if (!concept || !type) {
      continue;
    }
    const schema = schemasByType.get(type.toLowerCase());
    if (!schema) {
      continue; // meta-type not yet formalized (MT0 formalizes only Entity)
    }
    conceptsChecked += 1;

    const table = parseTableForSection(lines, concept);
    const sectionLines = getSectionLines(lines, concept);

    for (const [name, crit] of Object.entries(schema.criterion || {})) {
      const failure = applyCriterion(name, crit, table, sectionLines);
      if (failure) {
        violations.push({
          file: toRelative(file),
          concept,
          type,
          reason: failure,
          line: table?.rows[0]?.line ?? row.line,
        });
      }
    }
  }
}

if (violations.length === 0) {
  console.log(
    `validate-content: PASS (` +
      `${conceptsChecked} concept(s) checked, ` +
      `${edgesChecked} edge(s) checked in ${targets.length} file(s); ` +
      `schemas=${schemasByType.size})`,
  );
  process.exit(0);
}

for (const v of violations) {
  console.log(
    `[content:${mode}] ${v.file}:${v.line} | concept=${v.concept} | type=${v.type} | ${v.reason}`,
  );
}
console.log(`[content:${mode}] violations=${violations.length}`);

process.exit(mode === "warn" ? 0 : 1);

// ---------------------------------------------------------------------------
// criterion application (decidable table-walk — the only checking done here)
// ---------------------------------------------------------------------------

function applyCriterion(
  name: string,
  crit: Criterion,
  table: MarkdownTable | null,
  sectionLines: string[],
): string | null {
  // section-scoped rule: prose marker search over the whole concept section.
  if (crit.rule === "section-contains") {
    const pattern = (crit.pattern || "").toLowerCase();
    if (!pattern) {
      return `criterion '${name}': missing 'pattern'`;
    }
    if (!sectionLines.join("\n").toLowerCase().includes(pattern)) {
      return `criterion '${name}': concept section does not contain '${crit.pattern}'`;
    }
    return null;
  }

  if (crit.rule === "attribute-one-of") {
    if (!(crit.key || "").trim()) {
      return `criterion '${name}': attribute-one-of requires a non-empty 'key'`;
    }
    if (
      !Array.isArray(crit.values) ||
      crit.values.length === 0 ||
      crit.values.some((value) => typeof value !== "string" || value.trim() === "")
    ) {
      return `criterion '${name}': attribute-one-of requires a non-empty 'values' string array`;
    }
  }

  // all remaining rules operate on the concept's primary table.
  if (!table) {
    return `criterion '${name}': no table found in the concept section`;
  }
  const headerMap = toHeaderMap(table.headers);

  if (crit.rule === "table-has-column") {
    const colIdx = headerMap.get((crit.column || "").toLowerCase());
    if (colIdx === undefined) {
      return `criterion '${name}': table has no '${crit.column}' column`;
    }
    if (table.rows.length < 1) {
      return `criterion '${name}': column '${crit.column}' present but the table has no rows`;
    }
    return null;
  }

  // attribute-equals: read a declared "Attribute | Value" table (the concept's primary table)
  // and assert a declared key holds an expected value. Shape only — the author's declaration is
  // checked, never the semantics of the Formal cell (that would be the engine moat).
  if (crit.rule === "attribute-equals") {
    const attrIdx = headerMap.get("attribute");
    const valIdx = headerMap.get("value");
    if (attrIdx === undefined || valIdx === undefined) {
      return `criterion '${name}': expected an "Attribute | Value" table`;
    }
    const wantKey = (crit.key || "").toLowerCase();
    const match = table.rows.find(
      (r) => (r.cells[attrIdx] || "").trim().toLowerCase() === wantKey,
    );
    if (!match) {
      return uiRepairViolation(
        "ATTRIBUTE-MISSING",
        `criterion '${name}': attribute '${crit.key}' is not declared`,
      );
    }
    const authoredValue = match.authoredCells[valIdx];
    const presenceCode = attributeNonemptyViolation(true, authoredValue);
    if (presenceCode) {
      return uiRepairViolation(
        presenceCode,
        `criterion '${name}': attribute '${crit.key}' must contain its fixed value`,
      );
    }
    const actual = (authoredValue || "").trim().toLowerCase();
    if (actual !== (crit.value || "").toLowerCase()) {
      return uiRepairViolation(
        "FIXED-VALUE-MISMATCH",
        `criterion '${name}': attribute '${crit.key}'='${actual}' (expected '${crit.value}')`,
      );
    }
    return null;
  }

  // attribute-present: a declared key exists in the "Attribute | Value" table (any value).
  // Used where a type is defined by declaring a key with several valid values (e.g. interface_kind).
  if (crit.rule === "attribute-present") {
    const attrIdx = headerMap.get("attribute");
    if (attrIdx === undefined) {
      return `criterion '${name}': expected an "Attribute | Value" table`;
    }
    const wantKey = (crit.key || "").toLowerCase();
    const has = table.rows.some(
      (r) => (r.cells[attrIdx] || "").trim().toLowerCase() === wantKey,
    );
    if (!has) {
      return `criterion '${name}': attribute '${crit.key}' is not declared`;
    }
    return null;
  }

  if (crit.rule === "attribute-nonempty/v1") {
    const attrIdx = headerMap.get("attribute");
    const valIdx = headerMap.get("value");
    if (attrIdx === undefined || valIdx === undefined) {
      return uiRepairViolation(
        "ATTRIBUTE-MISSING",
        `criterion '${name}': expected an "Attribute | Value" table`,
      );
    }
    const wantKey = normalizeToken(crit.key || "");
    const match = table.rows.find(
      (row) => normalizeToken(row.cells[attrIdx] || "") === wantKey,
    );
    const authoredValue = match?.authoredCells[valIdx];
    const code = attributeNonemptyViolation(Boolean(match), authoredValue);
    if (code) {
      return uiRepairViolation(
        code,
        `criterion '${name}': attribute '${crit.key}' must contain non-whitespace text`,
      );
    }
    return null;
  }

  if (crit.rule === "attribute-one-of") {
    const attrIdx = headerMap.get("attribute");
    const valIdx = headerMap.get("value");
    if (attrIdx === undefined || valIdx === undefined) {
      return `criterion '${name}': expected an "Attribute | Value" table`;
    }
    const wantKey = normalizeToken(crit.key || "");
    const match = table.rows.find(
      (r) => normalizeToken(r.cells[attrIdx] || "") === wantKey,
    );
    if (!match) {
      return `criterion '${name}': attribute '${crit.key}' is not declared`;
    }
    const actual = normalizeToken(match.cells[valIdx] || "");
    const allowed = (crit.values || []).map(normalizeToken);
    if (!allowed.includes(actual)) {
      return `criterion '${name}': attribute '${crit.key}'='${actual}' (expected one of [${(crit.values || []).join(", ")}])`;
    }
    return null;
  }

  if (!["at-least-one", "none", "all-nonempty"].includes(crit.rule)) {
    return `criterion '${name}': unsupported rule '${crit.rule}'`;
  }

  const colIdx = headerMap.get((crit.column || "").toLowerCase());
  if (colIdx === undefined) {
    return `criterion '${name}': required column '${crit.column}' missing from the table`;
  }
  const cells = table.rows.map((r) => (r.cells[colIdx] || "").trim());
  const truthy = (crit.truthy || []).map((t) => t.toLowerCase());

  if (crit.rule === "at-least-one") {
    const hits = cells.filter((c) => truthy.includes(c.toLowerCase())).length;
    if (hits < 1) {
      return `criterion '${name}': no field flagged in column '${crit.column}' (need >=1 of [${(crit.truthy || []).join(", ")}])`;
    }
    return null;
  }

  if (crit.rule === "none") {
    const hits = cells.filter((c) => truthy.includes(c.toLowerCase())).length;
    if (hits > 0) {
      return `criterion '${name}': ${hits} field(s) flagged in column '${crit.column}' but none are allowed`;
    }
    return null;
  }

  if (crit.rule === "all-nonempty") {
    const empties = cells.filter((c) => c === "").length;
    if (empties > 0) {
      return `criterion '${name}': ${empties} field(s) have an empty '${crit.column}' cell`;
    }
    return null;
  }

  return null;
}

function normalizeToken(value: string): string {
  return value.trim().toLowerCase();
}

// ---------------------------------------------------------------------------
// schema loading (minimal SCHEMA-CONSTITUTION .schema.yml subset reader)
// supports: nested maps (2-space indent), `key: scalar`, `key: [flow, list]`, `# comments`.
// no block sequences, no multiline scalars — the schema files are authored to this subset.
// ---------------------------------------------------------------------------

function loadSchemas(dir: string): Map<string, Schema> {
  const out = new Map<string, Schema>();
  if (!existsSync(dir)) {
    return out;
  }
  const files = walk(dir)
    .filter((p) => p.endsWith(".schema.yml"))
    .sort();
  for (const file of files) {
    const where = toRelative(file);
    const schema = parseSchemaYml(readFileSync(file, "utf-8"), where) as Schema;
    assertCriterionPreflight(schema.criterion, where);
    const metaType = typeof schema.meta_type === "string" ? schema.meta_type : "";
    if (!metaType) {
      throw new Error(`validate-content: ${toRelative(file)} is missing 'meta_type'`);
    }
    out.set(metaType.toLowerCase(), schema);
  }
  return out;
}

function parseSchemaYml(raw: string, where: string): Record<string, unknown> {
  const root: Record<string, unknown> = {};
  const stack: Array<{ indent: number; node: Record<string, unknown> }> = [
    { indent: -1, node: root },
  ];
  const lines = raw.split(/\r?\n/);

  for (let i = 0; i < lines.length; i += 1) {
    const rawLine = lines[i] ?? "";
    if (rawLine.trim() === "" || rawLine.trim().startsWith("#")) {
      continue;
    }
    if (rawLine.includes("\t")) {
      throw new Error(`${where}:${i + 1}: tabs are not allowed in .schema.yml`);
    }
    const indent = rawLine.length - rawLine.trimStart().length;
    const content = rawLine.trim();
    const colon = content.indexOf(":");
    if (colon < 0) {
      throw new Error(`${where}:${i + 1}: expected 'key:' — got "${content}"`);
    }
    const key = content.slice(0, colon).trim();
    const rest = content.slice(colon + 1).trim();

    while (stack.length > 1 && (stack[stack.length - 1]?.indent ?? -1) >= indent) {
      stack.pop();
    }
    const parent = stack[stack.length - 1]?.node ?? root;
    assertNoDuplicateSchemaKey(parent, key, where, i + 1);

    if (rest === "") {
      const obj: Record<string, unknown> = {};
      parent[key] = obj;
      stack.push({ indent, node: obj });
    } else {
      parent[key] = parseScalarOrList(rest);
    }
  }
  return root;
}

function parseScalarOrList(value: string): string | string[] {
  if (value.startsWith("[") && value.endsWith("]")) {
    const inner = value.slice(1, -1).trim();
    if (inner === "") {
      return [];
    }
    return inner.split(",").map((s) => unquote(s.trim()));
  }
  return unquote(value);
}

function unquote(s: string): string {
  if (
    (s.startsWith('"') && s.endsWith('"')) ||
    (s.startsWith("'") && s.endsWith("'"))
  ) {
    return s.slice(1, -1);
  }
  return s;
}

// ---------------------------------------------------------------------------
// aspect-file targets
// ---------------------------------------------------------------------------

function resolveTargets(): string[] {
  if (singleFile) {
    const p = resolve(process.cwd(), singleFile);
    if (!existsSync(p)) {
      console.error(`validate-content: --file not found: ${singleFile}`);
      process.exit(1);
    }
    return [p];
  }
  if (!existsSync(featuresRoot)) {
    return [];
  }
  return walk(featuresRoot)
    .filter((p) => p.endsWith("/SPEC.md"))
    .sort();
}

// ---------------------------------------------------------------------------
// markdown-table parsing (build-from-owned: tools/validate-relationships.ts)
// ---------------------------------------------------------------------------

function parseTableForSection(
  lines: string[],
  sectionName: string,
): MarkdownTable | null {
  const sectionRanges = findSectionRanges(lines);
  const section = sectionRanges.find(
    (entry) => normalizeSectionName(entry.name) === normalizeSectionName(sectionName),
  );
  if (!section) {
    return null;
  }

  let start = section.start;
  while (start < section.end && !lines[start]?.trim().startsWith("|")) {
    start += 1;
  }
  if (start >= section.end) {
    return null;
  }

  const headerLine = lines[start] || "";
  const separatorLine = lines[start + 1] || "";
  if (!separatorLine.trim().startsWith("|")) {
    return null;
  }

  const headers = parseTableRow(headerLine);
  const separatorCells = parseTableRow(separatorLine);
  if (
    headers.length === 0 ||
    separatorCells.length === 0 ||
    !separatorCells.every((cell) => /^:?-{3,}:?$/.test(cell) || cell.length === 0)
  ) {
    return null;
  }

  const rows: TableRow[] = [];
  let rowIndex = start + 2;
  while (rowIndex < section.end) {
    const line = lines[rowIndex] || "";
    if (!line.trim().startsWith("|")) {
      break;
    }
    const authoredCells = parseAuthoredTableRow(line);
    const cells = authoredCells.map((cell) => cell.trim());
    if (!cells.every((cell) => /^:?-{3,}:?$/.test(cell) || cell.length === 0)) {
      rows.push({ cells, authoredCells, line: rowIndex + 1 });
    }
    rowIndex += 1;
  }

  return { headers, rows };
}

function parseTableRow(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|")) {
    return [];
  }
  const withoutEdges = trimmed.replace(/^\|/, "").replace(/\|$/, "");
  return withoutEdges.split("|").map((cell) => cell.trim());
}

function parseAuthoredTableRow(line: string): string[] {
  const trimmed = line.trim();
  if (!trimmed.startsWith("|")) return [];
  const withoutEdges = trimmed.replace(/^\|/, "").replace(/\|$/, "");
  return withoutEdges.split("|").map((cell) => {
    let authored = cell;
    if (authored.startsWith(" ")) authored = authored.slice(1);
    if (authored.endsWith(" ")) authored = authored.slice(0, -1);
    return authored;
  });
}

function toHeaderMap(headers: string[]): Map<string, number> {
  const map = new Map<string, number>();
  headers.forEach((header, index) => {
    map.set(header.trim().toLowerCase(), index);
  });
  return map;
}

function normalizeSectionName(name: string): string {
  return name.trim().toLowerCase().replace(/\s+/g, " ");
}

function getSectionLines(lines: string[], sectionName: string): string[] {
  const section = findSectionRanges(lines).find(
    (entry) => normalizeSectionName(entry.name) === normalizeSectionName(sectionName),
  );
  if (!section) {
    return [];
  }
  return lines.slice(section.start, section.end);
}

function findSectionRanges(
  lines: string[],
): Array<{ name: string; start: number; end: number }> {
  const headings: Array<{ name: string; line: number }> = [];
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i] || "";
    const match = /^##+\s+(.+)$/.exec(line.trim());
    if (!match?.[1]) {
      continue;
    }
    headings.push({ name: match[1].trim(), line: i });
  }

  const sections: Array<{ name: string; start: number; end: number }> = [];
  for (let i = 0; i < headings.length; i += 1) {
    const current = headings[i];
    if (!current) {
      continue;
    }
    const next = headings[i + 1];
    sections.push({
      name: current.name,
      start: current.line + 1,
      end: next ? next.line : lines.length,
    });
  }
  return sections;
}

function walk(root: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const fullPath = join(root, entry.name);
    if (entry.isDirectory()) {
      out.push(...walk(fullPath));
    } else if (entry.isFile()) {
      out.push(fullPath);
    }
  }
  return out;
}

function getArg(name: string): string | undefined {
  const index = args.indexOf(name);
  if (index < 0) {
    return undefined;
  }
  return args[index + 1];
}

function toRelative(absPath: string): string {
  return relative(process.cwd(), absPath).replace(/\\/g, "/");
}
