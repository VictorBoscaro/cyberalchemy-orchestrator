#!/usr/bin/env tsx
/**
 * instances.ts — DomainSpec v2 machine-generated instance tooling (MT-INST).
 *
 * Two modes over the per-meta-type schemas in spec/meta-types/:
 *   generate  — for each <type>.schema.yml, emit a canonical example instance <type>.example.instance.yml
 *               (DEF-D3 source B) that CONFORMS to the schema. Shape is normalized from the schema's
 *               required_structure + criterion — it is NOT derived (no src/rules, no δ-algorithm), so this
 *               stays the PUBLIC structural authoring aid (validators-as-moat asset #1).
 *   validate  — validate machine-generated instances against their schema's criterion (the same rules
 *               validate-content applies to markdown, applied here to structured YAML instance data).
 *
 * Usage:
 *   tsx tools/instances.ts generate [--schema-dir spec/meta-types] [--out-dir spec/__generated__/instances]
 *   tsx tools/instances.ts validate [--schema-dir spec/meta-types] [--dir <d> | --file <f>] [--mode strict|warn]
 */

import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { join, relative, resolve } from "node:path";

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
  required_structure?: Record<string, unknown>;
  criterion?: Record<string, Criterion>;
  [k: string]: unknown;
};

const argv = process.argv.slice(2);
const mode = argv[0];
const validateMode = getArg("--mode") || "strict";
const schemaDir = resolve(process.cwd(), getArg("--schema-dir") || "spec/meta-types");
const outDir = resolve(process.cwd(), getArg("--out-dir") || "spec/__generated__/instances");

const schemas = loadSchemas(schemaDir);
if (schemas.length === 0) {
  console.error(`instances: no .schema.yml found under ${toRel(schemaDir)}`);
  process.exit(1);
}

if (mode === "generate") {
  runGenerate();
} else if (mode === "validate") {
  runValidate();
} else {
  console.error("instances: first arg must be 'generate' or 'validate'");
  process.exit(1);
}

// ---------------------------------------------------------------------------
// generate: schema -> canonical example instance (conforms by construction)
// ---------------------------------------------------------------------------

function runGenerate(): void {
  mkdirSync(outDir, { recursive: true });
  let count = 0;
  for (const schema of schemas) {
    const slug = schema.meta_type.trim().toLowerCase().replace(/\s+/g, "-");
    const yaml = emitInstance(buildInstance(schema));
    writeFileSync(join(outDir, `${slug}.example.instance.yml`), yaml, "utf-8");
    count += 1;
  }
  console.log(`instances: generated ${count} example instance(s) -> ${toRel(outDir)}`);
}

function buildInstance(schema: Schema): Record<string, unknown> {
  const rs = schema.required_structure || {};
  const crit = schema.criterion || {};
  const slug = schema.meta_type.trim().replace(/\s+/g, "");
  const inst: Record<string, unknown> = {
    meta_type: schema.meta_type,
    concept: `Example${slug}`,
  };

  if (rs.fields_table_columns) {
    const names = ["sample"];
    const types = ["String"];
    const identity = ["no"];
    let needIdentity = false;
    for (const c of Object.values(crit)) {
      if (c.rule === "at-least-one" && (c.column || "").toLowerCase() === "identity") {
        needIdentity = true;
      }
    }
    if (needIdentity) {
      names.unshift("id");
      types.unshift("Uuid");
      identity.unshift("yes");
    }
    // Keys are field_<column-lowercased> so the validator's `field_${column}` lookup resolves.
    inst.field_name = names;
    inst.field_type = types;
    inst.field_identity = identity;
    // section-contains criteria: emit a scalar carrying the required pattern
    for (const [name, c] of Object.entries(crit)) {
      if (c.rule === "section-contains") {
        inst[name] = `example ${inst.concept} are ${c.pattern} by fields`;
      }
    }
  } else if (rs.value_table_columns) {
    inst.values = ["ALPHA", "BETA", "GAMMA"];
  } else if (rs.attributes_table_columns) {
    const attrs: Record<string, string> = {};
    for (const [name, c] of Object.entries(crit)) {
      if (c.rule === "attribute-equals" && c.key) {
        attrs[c.key] = c.value ?? "";
      } else if (c.rule === "attribute-present" && c.key) {
        attrs[c.key] = `example-${c.key}`;
      } else if (c.rule === "attribute-nonempty/v1") {
        const key = (c.key || "").trim();
        if (!key) {
          throw new Error(
            uiRepairViolation(
              "ATTRIBUTE-MISSING",
              `instances: criterion '${name}': attribute-nonempty/v1 requires a non-empty 'key'`,
            ),
          );
        }
        attrs[key] = `example-${key}`;
      } else if (c.rule === "attribute-one-of") {
        const key = (c.key || "").trim();
        if (!key) {
          throw new Error(
            `instances: criterion '${name}': attribute-one-of requires a non-empty 'key'`,
          );
        }
        if (
          !Array.isArray(c.values) ||
          c.values.length === 0 ||
          c.values.some((value) => typeof value !== "string" || value.trim() === "")
        ) {
          throw new Error(
            `instances: criterion '${name}': attribute-one-of requires a non-empty 'values' string array`,
          );
        }
        attrs[key] = c.values[0]!.trim();
      }
    }
    inst.attributes = attrs;
  }
  return inst;
}

function emitInstance(inst: Record<string, unknown>): string {
  const lines: string[] = [];
  for (const [key, val] of Object.entries(inst)) {
    if (Array.isArray(val)) {
      lines.push(`${key}: [${val.join(", ")}]`);
    } else if (val && typeof val === "object") {
      lines.push(`${key}:`);
      for (const [k, v] of Object.entries(val as Record<string, unknown>)) {
        lines.push(`  ${k}: ${String(v)}`);
      }
    } else {
      lines.push(`${key}: ${String(val)}`);
    }
  }
  return `${lines.join("\n")}\n`;
}

// ---------------------------------------------------------------------------
// validate: instance data vs its schema criterion (shape only, no moat)
// ---------------------------------------------------------------------------

function runValidate(): void {
  const byType = new Map(schemas.map((s) => [s.meta_type.toLowerCase(), s]));
  const files = resolveInstanceFiles();
  if (files.length === 0) {
    console.log("instances: no instances to validate");
    process.exit(0);
  }

  const violations: string[] = [];
  let checked = 0;
  for (const file of files) {
    const inst = parseYamlSubset(readFileSync(file, "utf-8"), toRel(file));
    const metaType = typeof inst.meta_type === "string" ? inst.meta_type : "";
    const schema = byType.get(metaType.toLowerCase());
    if (!schema) {
      violations.push(`${toRel(file)} | declares meta_type '${metaType}' with no schema`);
      continue;
    }
    checked += 1;
    for (const [name, crit] of Object.entries(schema.criterion || {})) {
      const failure = applyInstanceCriterion(name, crit, inst);
      if (failure) {
        violations.push(`${toRel(file)} | concept=${String(inst.concept)} | ${failure}`);
      }
    }
  }

  if (violations.length === 0) {
    console.log(`instances: PASS (${checked} instance(s) validated; schemas=${schemas.length})`);
    process.exit(0);
  }
  for (const v of violations) {
    console.log(`[instance:${validateMode}] ${v}`);
  }
  console.log(`[instance:${validateMode}] violations=${violations.length}`);
  process.exit(validateMode === "warn" ? 0 : 1);
}

function applyInstanceCriterion(
  name: string,
  crit: Criterion,
  inst: Record<string, unknown>,
): string | null {
  if (crit.rule === "section-contains") {
    const hay = collectStrings(inst).join("\n").toLowerCase();
    if (!hay.includes((crit.pattern || "").toLowerCase())) {
      return `criterion '${name}': instance has no text containing '${crit.pattern}'`;
    }
    return null;
  }

  if (crit.rule === "attribute-one-of") {
    const key = (crit.key || "").trim();
    if (!key) {
      return `criterion '${name}': attribute-one-of requires a non-empty 'key'`;
    }
    if (
      !Array.isArray(crit.values) ||
      crit.values.length === 0 ||
      crit.values.some((value) => typeof value !== "string" || value.trim() === "")
    ) {
      return `criterion '${name}': attribute-one-of requires a non-empty 'values' string array`;
    }
    const attrs = (inst.attributes as Record<string, unknown>) || {};
    const match = Object.entries(attrs).find(
      ([attribute]) => normalizeToken(attribute) === normalizeToken(key),
    );
    if (!match) {
      return `criterion '${name}': attribute '${crit.key}' is not declared`;
    }
    const actual = normalizeToken(String(match[1]));
    const allowed = crit.values.map(normalizeToken);
    if (!allowed.includes(actual)) {
      return `criterion '${name}': attribute '${crit.key}'='${actual}' (expected one of [${crit.values.join(", ")}])`;
    }
    return null;
  }

  if (crit.rule === "attribute-nonempty/v1") {
    const key = (crit.key || "").trim();
    const attrs = (inst.attributes as Record<string, unknown>) || {};
    const match = Object.entries(attrs).find(
      ([attribute]) => normalizeToken(attribute) === normalizeToken(key),
    );
    const code = attributeNonemptyViolation(Boolean(match), match?.[1]);
    if (code) {
      return uiRepairViolation(
        code,
        `criterion '${name}': attribute '${crit.key}' must contain non-whitespace text`,
      );
    }
    return null;
  }

  if (crit.rule === "attribute-equals" || crit.rule === "attribute-present") {
    const attrs = (inst.attributes as Record<string, unknown>) || {};
    if (!(crit.key && crit.key in attrs)) {
      return uiRepairViolation(
        "ATTRIBUTE-MISSING",
        `criterion '${name}': attribute '${crit.key}' is not declared`,
      );
    }
    if (crit.rule === "attribute-equals") {
      const authoredValue = attrs[crit.key];
      const presenceCode = attributeNonemptyViolation(true, authoredValue);
      if (presenceCode) {
        return uiRepairViolation(
          presenceCode,
          `criterion '${name}': attribute '${crit.key}' must contain its fixed value`,
        );
      }
      const actual = String(authoredValue).toLowerCase();
      if (actual !== (crit.value || "").toLowerCase()) {
        return uiRepairViolation(
          "FIXED-VALUE-MISMATCH",
          `criterion '${name}': attribute '${crit.key}'='${actual}' (expected '${crit.value}')`,
        );
      }
    }
    return null;
  }

  if (crit.rule === "table-has-column" && (crit.column || "").toLowerCase() === "value") {
    const vals = inst.values;
    if (!Array.isArray(vals) || vals.length < 1) {
      return `criterion '${name}': instance has no non-empty 'values' list`;
    }
    return null;
  }

  if (!["at-least-one", "none", "all-nonempty"].includes(crit.rule)) {
    return `criterion '${name}': unsupported rule '${crit.rule}'`;
  }

  // column-over-fields rules: field_<column> parallel array
  const col = (crit.column || "").toLowerCase();
  const arr = inst[`field_${col}`];
  if (!Array.isArray(arr)) {
    return `criterion '${name}': instance has no 'field_${col}' array`;
  }
  const truthy = (crit.truthy || []).map((t) => t.toLowerCase());
  if (crit.rule === "at-least-one") {
    if (!arr.some((x) => truthy.includes(String(x).toLowerCase()))) {
      return `criterion '${name}': no '${crit.column}' flagged in field_${col}`;
    }
    return null;
  }
  if (crit.rule === "none") {
    if (arr.some((x) => truthy.includes(String(x).toLowerCase()))) {
      return `criterion '${name}': a '${crit.column}' is flagged in field_${col} but none allowed`;
    }
    return null;
  }
  if (crit.rule === "all-nonempty") {
    if (arr.some((x) => String(x).trim() === "")) {
      return `criterion '${name}': an entry in field_${col} is empty`;
    }
    return null;
  }
  return null;
}

function normalizeToken(value: string): string {
  return value.trim().toLowerCase();
}

function collectStrings(obj: unknown): string[] {
  if (typeof obj === "string") {
    return [obj];
  }
  if (Array.isArray(obj)) {
    return obj.flatMap(collectStrings);
  }
  if (obj && typeof obj === "object") {
    return Object.values(obj as Record<string, unknown>).flatMap(collectStrings);
  }
  return [];
}

function resolveInstanceFiles(): string[] {
  const file = getArg("--file");
  if (file) {
    const p = resolve(process.cwd(), file);
    if (!existsSync(p)) {
      console.error(`instances: --file not found: ${file}`);
      process.exit(1);
    }
    return [p];
  }
  const dir = resolve(process.cwd(), getArg("--dir") || relative(process.cwd(), outDir));
  if (!existsSync(dir)) {
    return [];
  }
  return readdirSync(dir)
    .filter((n) => n.endsWith(".instance.yml"))
    .sort()
    .map((n) => join(dir, n));
}

// ---------------------------------------------------------------------------
// schema loading + minimal YAML-subset reader (inlined; shared shape with
// validate-content.ts — a tools/lib refactor is tracked residue)
// ---------------------------------------------------------------------------

function loadSchemas(dir: string): Schema[] {
  if (!existsSync(dir)) {
    return [];
  }
  return walk(dir)
    .filter((p) => p.endsWith(".schema.yml"))
    .sort()
    .map((p) => {
      const where = toRel(p);
      const schema = parseYamlSubset(readFileSync(p, "utf-8"), where) as Schema;
      assertCriterionPreflight(schema.criterion, where);
      return schema;
    })
    .filter((s) => typeof s.meta_type === "string" && s.meta_type.length > 0);
}

function parseYamlSubset(raw: string, where: string): Record<string, unknown> {
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
      throw new Error(`${where}:${i + 1}: tabs are not allowed`);
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

function walk(root: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const full = join(root, entry.name);
    if (entry.isDirectory()) {
      out.push(...walk(full));
    } else if (entry.isFile()) {
      out.push(full);
    }
  }
  return out;
}

function getArg(name: string): string | undefined {
  const idx = argv.indexOf(name);
  return idx < 0 ? undefined : argv[idx + 1];
}

function toRel(abs: string): string {
  return relative(process.cwd(), abs).replace(/\\/g, "/");
}
