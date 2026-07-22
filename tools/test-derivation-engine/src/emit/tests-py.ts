// Stage D (part 3) / P4 — emit_tests, PYTHON/pytest surface. Byte-for-byte mirror
// of emit/tests.ts, but rendering pytest module text instead of vitest TS. Same
// derivation contract:
//
//   * assertion-from-Formal (AST-eval): ternary deal-split, RANGE boundary cases,
//     COUNT_CAP at cap/cap+1. EXPECTED comes from the Formal AST, never the impl.
//   * closed-form value assertion (Fold / ArithExpr) over a binding fixture env.
//   * property-based (pure seeded generator, no dep) for universally-quantified
//     invariants (e.g. `newDebt >= 0`).
//   * @pytest.mark.skip + a `coverage_gap` annotation for everything needing a
//     human oracle. Counted + reported, NEVER faked.
//
// Two modes, mirroring tests.ts:
//   - WITHOUT a BindingSet: legacy stub mode — one skipped test per obligation.
//   - WITH a BindingSet: hybrid mode — real asserts where a binding + evaluable
//     Formal AST exist, honest skip coverage_gap everywhere else.
//
// Generation is PURE/total: same (obligations, bindings, graph) -> byte-identical
// file. The counting logic is identical to tests.ts; only the rendered text differs.
//
// STATED ASSUMPTION (no Python impl exists yet): the bound domain functions return
// objects with ATTRIBUTE access (`result.field`) and Python booleans. Each accessor
// site carries a note: if the impl returns dicts instead, switch to `["field"]`.

import type { ConceptGraph, Obligation } from "../ir/types.js";
import type { Binding, BindingSet } from "../bindings/index.js";
import { bindingFor } from "../bindings/index.js";
import type { HybridReport, HybridResult } from "./tests.js";
import { parseFormal } from "../formal/ast.js";
import { evalArith } from "../formal/eval.js";
import type { EvalEnv } from "../formal/eval.js";

// --- Local pure helpers (mirrors of tests.ts internals; not exported there) ----

/** Escape a string for safe embedding inside a Python `#` line comment. */
function commentSafe(s: string): string {
  return s.replace(/\r?\n/g, " ");
}

function sortObligations(obligations: readonly Obligation[]): Obligation[] {
  return [...obligations].sort((a, b) =>
    a.obligation_key < b.obligation_key
      ? -1
      : a.obligation_key > b.obligation_key
        ? 1
        : 0,
  );
}

/** Resolve the Formal/Formula text for an obligation (SPEC text, AST source only). */
function resolveFormal(
  o: Obligation,
  formalByAnchor: ReadonlyMap<string, string>,
): string {
  const fromParam = o.canonical_params.formal;
  if (typeof fromParam === "string" && fromParam !== "") return fromParam;
  return formalByAnchor.get(o.source_anchor) ?? "";
}

/** Index source nodes' formal/formula cells by source_anchor (pure). */
function buildFormalIndex(graph: ConceptGraph): Map<string, string> {
  const idx = new Map<string, string>();
  for (const n of graph.nodes) {
    const f = n.fields.formal ?? n.fields.formula;
    if (typeof f === "string" && f !== "") idx.set(n.source_anchor, f);
  }
  return idx;
}

/** JSON-encode a string (double-quoted, escaped) — valid Python string literal too. */
const p = (s: string): string => JSON.stringify(s);

/** A test title for an obligation, stable and unique by key prefix (as tests.ts). */
function title(o: Obligation): string {
  return `${o.rule_type}:${o.obligation_key.slice(0, 8)} ${o.description}`;
}

function paramStr(o: Obligation, key: string): string {
  const v = o.canonical_params[key];
  return v == null ? "" : String(v);
}

/** Replace every char that is not identifier-safe with `_`. */
function pyIdentSafe(s: string): string {
  return s.replace(/[^A-Za-z0-9_]/g, "_");
}

/**
 * A valid, UNIQUE Python test identifier `test_{rt}_{key8}`. Pure given the
 * current `used` set (does NOT mutate it — the caller adds on commit, so a body
 * and its fallback skip can share one name). Collisions extend the key prefix,
 * then fall back to a numeric suffix — deterministic because obligations are
 * emitted in sorted order.
 */
function nextName(o: Obligation, used: ReadonlySet<string>): string {
  const rt = pyIdentSafe(o.rule_type);
  const key = o.obligation_key;
  let len = 8;
  let name = `test_${rt}_${pyIdentSafe(key.slice(0, len))}`;
  while (used.has(name) && len < key.length) {
    len += 1;
    name = `test_${rt}_${pyIdentSafe(key.slice(0, len))}`;
  }
  const base = name;
  let suffix = 2;
  while (used.has(name)) {
    name = `${base}_${suffix}`;
    suffix += 1;
  }
  return name;
}

/** Render an arbitrary JSON value as a Python literal (true/false/null -> True/False/None). */
function pyLiteral(v: unknown): string {
  if (v === null) return "None";
  if (typeof v === "boolean") return v ? "True" : "False";
  if (typeof v === "number") return String(v);
  if (typeof v === "string") return JSON.stringify(v);
  if (Array.isArray(v)) return `[${v.map(pyLiteral).join(", ")}]`;
  if (typeof v === "object") {
    const entries = Object.entries(v as Record<string, unknown>).map(
      ([k, val]) => `${JSON.stringify(k)}: ${pyLiteral(val)}`,
    );
    return `{${entries.join(", ")}}`;
  }
  return "None";
}

// --- Legacy stub mode (no bindings) -------------------------------------------

/** Render obligations as a runnable pytest file (1 skipped test per obligation_key). */
export function emitTestsPython(obligations: readonly Obligation[]): string {
  const used = new Set<string>();
  const cases = sortObligations(obligations).map((o) => {
    const name = nextName(o, used);
    used.add(name);
    return [
      `# obligation_key: ${o.obligation_key}`,
      `# source: ${commentSafe(o.source_anchor)}`,
      `# ${commentSafe(title(o))}`,
      `@pytest.mark.skip(reason=${p("todo: replace with real test")})`,
      `def ${name}():`,
      `    pass`,
    ].join("\n");
  });
  return [
    `# AUTO-GENERATED by the deterministic test-derivation engine. Do not edit by hand.`,
    `# One skipped test per derived obligation_key; drop the skip to implement.`,
    `import pytest`,
    ``,
    cases.join("\n\n"),
    ``,
  ].join("\n");
}

// --- Hybrid mode (with bindings) ----------------------------------------------

/** A `coverage_gap` skipped case. Honest hole, counted, never faked. */
function emitSkip(o: Obligation, reason: string, name: string): string {
  return [
    `# obligation_key: ${o.obligation_key}`,
    `# source: ${commentSafe(o.source_anchor)}`,
    `# coverage_gap: ${reason}`,
    `# ${commentSafe(title(o))}`,
    `@pytest.mark.skip(reason=${p(reason)})`,
    `def ${name}():`,
    `    pass`,
  ].join("\n");
}

/**
 * Try to emit a REAL pytest body for an obligation+binding by evaluating the
 * Formal AST. Returns null when the AST is not in the evaluable grammar (caller
 * falls back to a coverage_gap skip). Pure: expected values are read from the AST.
 */
function emitAstEval(
  o: Obligation,
  b: Binding,
  formal: string,
  name: string,
): string | null {
  const ast = parseFormal(formal);
  const head = [
    `# obligation_key: ${o.obligation_key}`,
    `# source: ${commentSafe(o.source_anchor)}`,
    `# binding: ${b.symbol}() [${b.kind}] — expected derived from Formal AST, not from impl`,
    `# ${commentSafe(title(o))}`,
  ];

  if (b.kind === "ternary-deal-split" && ast.kind === "ternary") {
    const branch = paramStr(o, "branch"); // true-branch | false-branch
    const isTrue = branch === "true-branch";
    const expected = isTrue ? ast.thenLit.value : ast.elseLit.value;
    const thr = ast.threshold.value;
    const onBoundary = `NL${thr}`;
    const below = `NL${Math.max(0, thr - 90)}`;
    const trueInput =
      ast.op === ">" ? `NL${thr + 10}` : ast.op === "<" ? below : onBoundary;
    const falseInput =
      ast.op === ">" || ast.op === ">=" ? below : `NL${thr + 10}`;
    const input = isTrue ? trueInput : falseInput;
    const field = b.result_field ?? "player";
    return [
      ...head,
      `def ${name}():`,
      `    # ${branch}: limit ${input} ${ast.op} ${ast.threshold.raw} -> ${field} == ${expected}`,
      `    # accessor: assumes ${b.symbol}() returns an object with attribute .${field}; if the impl returns a dict, use ["${field}"].`,
      `    assert ${b.symbol}(${p(input)}).${field} == ${expected}`,
    ].join("\n");
  }

  if (b.kind === "range-date-filter" && ast.kind === "range") {
    const caseName = paramStr(o, "case");
    const start = "2026-01-01";
    const end = "2026-01-31";
    const dayBeforeStart = "2025-12-31";
    const dayAfterEnd = "2026-02-01";
    const lowerInclusive = ast.lowerOp === "<="; // start <= x
    const upperInclusive = ast.upperOp === "<="; // x <= end
    let recDate: string;
    let expectLen: number;
    switch (caseName) {
      case "lower-inclusive":
        recDate = start;
        expectLen = lowerInclusive ? 1 : 0;
        break;
      case "upper-inclusive":
        recDate = end;
        expectLen = upperInclusive ? 1 : 0;
        break;
      case "below":
        recDate = dayBeforeStart;
        expectLen = 0;
        break;
      case "above":
        recDate = dayAfterEnd;
        expectLen = 0;
        break;
      default:
        return null;
    }
    return [
      ...head,
      `def ${name}():`,
      `    # ${caseName}: record date ${recDate} vs [${start} ${ast.lowerOp} date ${ast.upperOp} ${end}]`,
      `    records = [{"date": ${p(recDate)}, "profit": 1, "rakeback": 0}]`,
      `    assert len(${b.symbol}(records, ${p(start)}, ${p(end)})) == ${expectLen}`,
    ].join("\n");
  }

  if (b.kind === "count-cap-makeup" || b.kind === "count-cap-payout") {
    if (ast.kind !== "count-cap") return null;
    const caseName = paramStr(o, "case"); // first-allowed | duplicate-capped
    const txType = b.tx_type ?? "";
    const field = b.decision_field ?? "";
    const endDate = "2026-01-31";
    const amountField =
      b.kind === "count-cap-makeup" ? "totalAppliedMakeup" : "totalPayout";
    const otherField =
      b.kind === "count-cap-makeup" ? "totalPayout" : "totalAppliedMakeup";
    const existing =
      caseName === "duplicate-capped"
        ? `[{"type": ${p(txType)}, "date": ${p(endDate)}}]`
        : `[]`;
    const expected = caseName === "duplicate-capped" ? "False" : "True";
    return [
      ...head,
      `def ${name}():`,
      `    # ${caseName}: cap ${ast.op} ${ast.cap} on ${txType} for endDate ${endDate}`,
      `    decision = ${b.symbol}({`,
      `        "existingTransactions": ${existing},`,
      `        "periodEnd": ${p(endDate)},`,
      `        "${amountField}": 100,`,
      `        "${otherField}": 0,`,
      `    })`,
      `    # accessor: assumes decision has attribute .${field}; if the impl returns a dict, use ["${field}"].`,
      `    assert decision.${field} == ${expected}`,
    ].join("\n");
  }

  return null;
}

/**
 * SWU-COB-004 — emit a REAL value assertion for a CLOSED-FORM obligation
 * (Fold / ArithExpr). Parse the SPEC Formal cell, evaluate it against the binding
 * fixture env to get EXPECTED ("read the spec, not the impl"). Returns null when
 * the Formal is not closed-form-derivable or the evaluation is partial.
 */
function emitClosedForm(
  o: Obligation,
  b: Binding,
  formal: string,
  name: string,
): string | null {
  if (b.fixture == null) return null;
  const ast = parseFormal(formal);
  if (
    ast.kind !== "fold" &&
    ast.kind !== "arith" &&
    ast.kind !== "num" &&
    ast.kind !== "var" &&
    ast.kind !== "piecewise"
  ) {
    return null; // not a closed form -> fall back to coverage_gap
  }
  if (ast.kind === "piecewise") return null; // reserved; no authored piecewise yet
  const env: EvalEnv = {
    vars: b.fixture.vars ?? {},
    collections: b.fixture.collections ?? {},
  };
  const expected = evalArith(ast, env);
  if (expected == null) return null; // partial eval -> coverage_gap (totality)
  const field = b.result_field ?? "";
  const accessor = field === "" ? "" : `.${field}`;
  const arg = pyLiteral(b.fixture.call_arg);
  const lines = [
    `# obligation_key: ${o.obligation_key}`,
    `# source: ${commentSafe(o.source_anchor)}`,
    `# binding: ${b.symbol}() [closed-form] — EXPECTED ${expected} derived from Formal AST over the fixture env, not from impl`,
    `# ${commentSafe(title(o))}`,
    `def ${name}():`,
    `    # closed-form: ${commentSafe(formal)} over the fixture -> ${expected}`,
  ];
  if (accessor !== "") {
    lines.push(
      `    # accessor: assumes ${b.symbol}() returns an object with attribute ${accessor}; if the impl returns a dict, use dict indexing.`,
    );
  }
  lines.push(`    assert ${b.symbol}(${arg})${accessor} == ${expected}`);
  return lines.join("\n");
}

/**
 * A property FULLY satisfies an obligation only when the Formal cell IS the
 * relation being asserted. A property bound to a `needs-formal` obligation is an
 * honest FLOOR, not coverage: the value-gap stays open (co-emit a coverage_gap).
 */
function propertyStandsInForMissingValue(o: Obligation): boolean {
  return o.rule_type === "needs-formal";
}

/** Emit a seeded property body in pure Python (no external generator dep). */
function emitProperty(
  o: Obligation,
  b: Binding,
  name: string,
): string | null {
  if (b.kind !== "non-negative-newdebt") return null;
  const field = b.result_field ?? "newDebt";
  // NOTE: the generator is named `nxt` (not `next`) to avoid shadowing the Python
  // builtin; it plays the role of `next()` from the vitest mirror.
  return [
    `# obligation_key: ${o.obligation_key}`,
    `# source: ${commentSafe(o.source_anchor)}`,
    `# binding: ${b.symbol}() [property] — seeded generator (no external dep)`,
    `# ${commentSafe(title(o))}`,
    `def ${name}():`,
    `    # property: for all generated inputs, ${b.symbol}(input).${field} >= 0`,
    `    seed = 0x9e3779b9  # fixed seed -> deterministic generation & kill set`,
    `    def nxt():`,
    `        # LCG (Numerical Recipes): pure, reproducible.`,
    `        nonlocal seed`,
    `        seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF`,
    `        return seed / 0xFFFFFFFF`,
    `    def span(n):`,
    `        return round((nxt() - 0.5) * 2 * n)`,
    `    for _ in range(200):`,
    `        result = ${b.symbol}({`,
    `            "previousDebt": span(10000),`,
    `            "totalProfit": span(10000),`,
    `            "totalRakeback": span(10000),`,
    `            "dealPlayerShare": nxt(),`,
    `        })`,
    `        # accessor: assumes result has attribute .${field}; if the impl returns a dict, use ["${field}"].`,
    `        assert result.${field} >= 0`,
  ].join("\n");
}

/** Map a coverage-gap obligation to a short reason tag (identical to tests.ts). */
function gapReason(o: Obligation): string {
  const rt = o.rule_type;
  if (rt === "needs-formal") return "needs-fixture-oracle (unparseable Formal)";
  if (rt === "valid-transition" || rt === "invalid-transition")
    return "out-of-pure-slice (state machine in use-cases)";
  if (rt === "contract") return "out-of-pure-slice (HTTP route)";
  if (rt === "event-obligation") return "out-of-pure-slice (side effect)";
  if (rt === "postcondition")
    return "side-effectful (pure half covered by R4/R5)";
  if (rt === "workflow-step" || rt === "query-behavior" || rt === "mapping-row")
    return "out-of-pure-slice (orchestration / mapping)";
  if (rt === "error-obligation") return "out-of-pure-slice (error routing)";
  if (rt === "invariant" || rt === "rule-validation")
    return "needs-fixture-oracle (no pure target / fixture universe)";
  if (rt === "calculation")
    return "needs-fixture-oracle (aggregate / bare call)";
  return "no-pure-target";
}

/**
 * Hybrid emit (Python). Pure/total over (obligations, bindings, graph) —
 * byte-identical output for identical inputs. Returns the file text plus the
 * derivable-vs-gap counts. Counting logic is identical to emitHybridTests.
 */
export function emitHybridTestsPython(
  obligations: readonly Obligation[],
  bindings: BindingSet,
  graph: ConceptGraph,
): HybridResult {
  const ordered = sortObligations(obligations);
  const formalByAnchor = buildFormalIndex(graph);
  const modules = new Map<string, Set<string>>();
  const used = new Set<string>();
  const bodies: string[] = [];
  let assertions = 0;
  let properties = 0;
  let coverageGaps = 0;

  for (const o of ordered) {
    const name = nextName(o, used);
    const b = bindingFor(o, bindings);
    if (b) {
      const body =
        b.strategy === "ast-eval"
          ? emitAstEval(o, b, resolveFormal(o, formalByAnchor), name)
          : b.strategy === "closed-form"
            ? emitClosedForm(o, b, resolveFormal(o, formalByAnchor), name)
            : emitProperty(o, b, name);
      if (body) {
        used.add(name);
        (
          modules.get(b.module) ??
          modules.set(b.module, new Set()).get(b.module)!
        ).add(b.symbol);
        bodies.push(body);
        if (b.strategy === "property") {
          properties += 1;
          if (propertyStandsInForMissingValue(o)) {
            const gapName = nextName(o, used);
            used.add(gapName);
            bodies.push(emitSkip(o, "needs-formal-value", gapName));
            coverageGaps += 1;
          }
        } else assertions += 1;
        continue;
      }
    }
    used.add(name);
    bodies.push(emitSkip(o, gapReason(o), name));
    coverageGaps += 1;
  }

  const imports = [...modules.entries()]
    .sort((a, b) => (a[0] < b[0] ? -1 : 1))
    .map(([mod, syms]) => `from ${mod} import ${[...syms].sort().join(", ")}`);

  const file = [
    `# AUTO-GENERATED by the deterministic test-derivation engine (hybrid emit_tests).`,
    `# Do not edit by hand. 1:1 with obligation_keys. Generation is pure/deterministic:`,
    `# same (spec + bindings) -> byte-identical file. Real assertions where the Formal`,
    `# AST is evaluable and a binding names a pure fn; honest pytest skip coverage_gap`,
    `# everywhere a human oracle is required (never faked).`,
    `#`,
    `# derivable: ${assertions} assertion(s) + ${properties} property(ies); coverage_gap: ${coverageGaps}.`,
    `import pytest`,
    ...imports,
    ``,
    `# derived obligations: ${commentSafe(bindings.feature)}`,
    ``,
    bodies.join("\n\n"),
    ``,
  ].join("\n");

  return {
    file,
    report: {
      total: ordered.length,
      assertions,
      properties,
      coverageGaps,
    } satisfies HybridReport,
  };
}
