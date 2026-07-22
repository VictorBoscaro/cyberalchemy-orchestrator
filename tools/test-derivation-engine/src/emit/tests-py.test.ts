// P4 — tests for the PYTHON (pytest) emitter `tests-py.ts`. The module mirrors
// `tests.ts`: identical obligation ordering, counts, binding/gap dispatch and
// report shape — only the RENDERED TEXT is pytest instead of vitest. These tests
// assert against the PYTEST OUTPUT CONTRACT, not against any implementation.
//
// Fixtures are built as minimal literal objects (Obligation / Binding / graph) so
// the suite is self-contained and the expected values are fully controlled here.
// A parallel agent authors `tests-py.ts`; until it lands, the import fails and the
// whole file errors — that is EXPECTED and must NOT be worked around by weakening.
import { describe, it, expect } from "vitest";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { writeFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import type { Obligation, ConceptGraph, RuleType } from "../ir/types.js";
import type { Binding, BindingSet } from "../bindings/index.js";
import { emitTestsPython, emitHybridTestsPython } from "./tests-py.js";
// TS emitter — used ONLY to prove Python report counts equal the vitest ones for
// the same input (the "counts match what tests.ts would produce" contract).
import { emitHybridTests } from "./tests.js";

// --- fixture builders ---------------------------------------------------------

const EMPTY_GRAPH: ConceptGraph = { nodes: [], edges: [] };

function mkOb(
  key: string,
  rule_type: RuleType,
  canonical_params: Record<string, string> = {},
  source_anchor = `doc#${key}`,
): Obligation {
  return {
    obligation_key: key,
    rule_type,
    source_anchor,
    canonical_params,
    description: `desc for ${key}`,
  };
}

function mkSet(bindings: readonly Binding[]): BindingSet {
  return {
    feature: "sample-feature",
    emit_dir: "out",
    test_file: "derived_test.py",
    bindings,
  };
}

// Bindings mirroring the four real strategies/kinds.
const TERNARY_BINDING: Binding = {
  match: { rule_type: "calculation", id: "C3" },
  module: "alpha_mod",
  symbol: "getDealSplit",
  strategy: "ast-eval",
  kind: "ternary-deal-split",
  result_field: "player",
};
const RANGE_BINDING: Binding = {
  match: { rule_type: "rule-validation", id: "R3" },
  module: "delta_mod",
  symbol: "filterRecordsByPeriod",
  strategy: "ast-eval",
  kind: "range-date-filter",
};
const COUNTCAP_BINDING: Binding = {
  match: { rule_type: "rule-validation", id: "R4" },
  module: "beta_mod",
  symbol: "decideSettlementSideEffects",
  strategy: "ast-eval",
  kind: "count-cap-makeup",
  tx_type: "MAKEUP_APPLIED",
  decision_field: "shouldCreateMakeupAppliedEvent",
};
const CLOSEDFORM_BINDING: Binding = {
  match: { rule_type: "calculation", id: "C1" },
  module: "beta_mod",
  symbol: "computeSettlement",
  strategy: "closed-form",
  kind: "fold-sum-profit",
  result_field: "totalProfit",
  fixture: {
    collections: { records: [{ profit: 10 }, { profit: 5 }] },
    call_arg: { records: [{ profit: 10 }, { profit: 5 }] },
  },
};
const PROPERTY_BINDING: Binding = {
  match: { rule_type: "needs-formal", id: "I1" },
  module: "gamma_mod",
  symbol: "applyMakeupPolicy",
  strategy: "property",
  kind: "non-negative-newdebt",
  result_field: "newDebt",
};

// Obligations that resolve each binding. Formal is carried in canonical_params so
// the graph can stay empty (resolveFormal prefers the param).
const TERNARY_OB = mkOb("c3000000aaaa", "calculation", {
  id: "C3",
  branch: "true-branch",
  formal: "playerShare = limit >= NL100 ? 0.5 : 0.4",
});
const RANGE_OB = mkOb("r3000000bbbb", "rule-validation", {
  id: "R3",
  case: "lower-inclusive",
  formal: "startDate <= stats.date <= endDate",
});
const COUNTCAP_OB = mkOb("r4000000cccc", "rule-validation", {
  id: "R4",
  case: "duplicate-capped",
  formal: "count(tx[type=MAKEUP_APPLIED,date=endDate]) <= 1",
});
const CLOSEDFORM_OB = mkOb("c1000000dddd", "calculation", {
  id: "C1",
  formal: "sum(records.profit)",
});
const PROPERTY_OB = mkOb("i1000000eeee", "needs-formal", {
  id: "I1",
  base_rule_type: "invariant",
});
const GAP_OB = mkOb("ct000000ffff", "contract", { id: "CT1" });

// --- python detection (for the syntax-validity test) --------------------------

function detectPython(): string | null {
  for (const cmd of ["python", "python3", "py"]) {
    try {
      const out = execFileSync(cmd, ["--version"], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
      });
      if (/Python \d/.test(out)) return cmd;
    } catch {
      // not this candidate — try next
    }
  }
  return null;
}
const PY = detectPython();

/** Parse `source` with the real interpreter; ok=false + stderr on a SyntaxError. */
function pyParses(source: string): { ok: boolean; err: string } {
  const tmp = join(
    tmpdir(),
    `tde-py-${Date.now()}-${Math.random().toString(36).slice(2)}.py`,
  );
  writeFileSync(tmp, source, "utf8");
  try {
    execFileSync(
      PY as string,
      [
        "-c",
        "import ast,sys; ast.parse(open(sys.argv[1], encoding='utf-8').read())",
        tmp,
      ],
      { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] },
    );
    return { ok: true, err: "" };
  } catch (e) {
    const err = e as { stderr?: string; message?: string };
    return { ok: false, err: String(err.stderr ?? err.message ?? e) };
  } finally {
    try {
      rmSync(tmp);
    } catch {
      // best-effort cleanup
    }
  }
}

// --- 1. legacy stub: empty file + determinism ---------------------------------

describe("emitTestsPython — legacy stub mode", () => {
  it("emits a well-formed empty file and is byte-stable across two calls", () => {
    const a = emitTestsPython([]);
    const b = emitTestsPython([]);
    expect(typeof a).toBe("string");
    expect(a).toBe(b); // determinism
    // A python comment header, never a JS one.
    expect(a).toContain("#");
    expect(a).not.toContain("//");
    expect(a).not.toContain("describe(");
    expect(a).not.toContain("it.todo");
  });

  it("renders one skipped pytest function per obligation, sorted by key", () => {
    // Provide OUT OF ORDER; the emitter must sort by obligation_key ascending.
    const obs = [
      mkOb("cccc3333xxxx", "needs-formal", { id: "X" }, "docs#c"),
      mkOb("aaaa1111zzzz", "calculation", { id: "A" }, "docs#a"),
      mkOb("bbbb2222yyyy", "rule-validation", { id: "B" }, "docs#b"),
    ];
    const out = emitTestsPython(obs);

    // Skip decorator with the legacy reason, one per obligation.
    const skipCount = (
      out.match(/@pytest\.mark\.skip\(reason="todo: replace with real test"\)/g) ??
      []
    ).length;
    expect(skipCount).toBe(3);

    // Function names: test_{rt}_{key8}; rt non-alnum -> "_"; key8 = first 8 chars.
    expect(out).toContain("def test_calculation_aaaa1111(");
    expect(out).toContain("def test_rule_validation_bbbb2222(");
    expect(out).toContain("def test_needs_formal_cccc3333(");

    // Every emitted def name is a valid, unique python identifier.
    const names = [...out.matchAll(/def (test_[A-Za-z0-9_]+)\(/g)].map(
      (m) => m[1],
    );
    expect(names.length).toBe(3);
    for (const n of names) expect(n).toMatch(/^test_[A-Za-z_][A-Za-z0-9_]*$/);
    expect(new Set(names).size).toBe(names.length); // unique

    // Skip bodies are `pass`, and the provenance comments are kept.
    expect(out).toContain("pass");
    expect(out).toContain("# obligation_key: aaaa1111zzzz");
    expect(out).toContain("# source: docs#a");

    // Sorted: aaaa before bbbb before cccc.
    const ia = out.indexOf("test_calculation_aaaa1111");
    const ib = out.indexOf("test_rule_validation_bbbb2222");
    const ic = out.indexOf("test_needs_formal_cccc3333");
    expect(ia).toBeGreaterThanOrEqual(0);
    expect(ia).toBeLessThan(ib);
    expect(ib).toBeLessThan(ic);

    // Never leaks python-literal case: no lowercase JS booleans / null.
    expect(out).not.toMatch(/\bnull\b/);
  });
});

// --- 2. hybrid: ternary AST-eval assertion ------------------------------------

describe("emitHybridTestsPython — ast-eval ternary", () => {
  const set = mkSet([TERNARY_BINDING]);
  const { file, report } = emitHybridTestsPython([TERNARY_OB], set, EMPTY_GRAPH);

  it("emits a real `assert fn(x).field == <expected-from-AST>`", () => {
    // true-branch, op ">=", threshold NL100 -> input NL100, expected 0.5 (thenLit).
    expect(file).toMatch(/getDealSplit\("NL100"\)\.player\s*==\s*0\.5/);
    // pytest style, not vitest.
    expect(file).toContain("assert ");
    expect(file).not.toContain(".toBe(");
  });

  it("counts the ternary as one assertion, no gaps/properties", () => {
    expect(report.assertions).toBe(1);
    expect(report.properties).toBe(0);
    expect(report.coverageGaps).toBe(0);
    expect(report.total).toBe(1);
  });
});

// --- 3. hybrid: count-cap renders a python dict, True/False not true/false -----

describe("emitHybridTestsPython — count-cap object literal", () => {
  const set = mkSet([COUNTCAP_BINDING]);
  const { file, report } = emitHybridTestsPython([COUNTCAP_OB], set, EMPTY_GRAPH);

  it("renders the argument object as a python dict with quoted keys", () => {
    // Nested existing-tx object -> {"type": "MAKEUP_APPLIED", "date": "..."}.
    expect(file).toMatch(/"type"\s*:/);
    expect(file).toMatch(/"MAKEUP_APPLIED"/);
  });

  it("uses python booleans (False), never JS lowercase true/false", () => {
    // duplicate-capped -> decision flag expected False.
    expect(file).toContain("== False");
    expect(file).not.toMatch(/\bfalse\b/);
    expect(file).not.toMatch(/\btrue\b/);
    expect(file).not.toMatch(/\bnull\b/);
  });

  it("counts the count-cap as one assertion", () => {
    expect(report.assertions).toBe(1);
    expect(report.coverageGaps).toBe(0);
  });
});

// --- 4. hybrid: coverage_gap for an unbound obligation ------------------------

describe("emitHybridTestsPython — coverage_gap", () => {
  const set = mkSet([TERNARY_BINDING]); // no binding matches a `contract`
  const { file, report } = emitHybridTestsPython([GAP_OB], set, EMPTY_GRAPH);

  it("emits a @pytest.mark.skip with a coverage_gap comment", () => {
    expect(file).toContain("@pytest.mark.skip(reason=");
    expect(file).toContain("# coverage_gap:");
    expect(file).toContain("def test_contract_ct000000(");
    expect(report.coverageGaps).toBe(1);
    expect(report.assertions).toBe(0);
  });

  it("produces the SAME report as the vitest emitter for the same input", () => {
    // Only the rendered text differs; ordering/dispatch/counts are identical.
    const ts = emitHybridTests([GAP_OB], set, EMPTY_GRAPH);
    expect(report).toEqual(ts.report);
  });
});

// --- 5. hybrid: sorted imports from two modules -------------------------------

describe("emitHybridTestsPython — imports block", () => {
  const set = mkSet([TERNARY_BINDING, CLOSEDFORM_BINDING]);
  const { file } = emitHybridTestsPython(
    [TERNARY_OB, CLOSEDFORM_OB],
    set,
    EMPTY_GRAPH,
  );

  it("emits one sorted `from <module> import <symbols>` line per module", () => {
    expect(file).toMatch(/from alpha_mod import getDealSplit/);
    expect(file).toMatch(/from beta_mod import computeSettlement/);
    // modules sorted: alpha_mod before beta_mod.
    const ia = file.indexOf("from alpha_mod import");
    const ib = file.indexOf("from beta_mod import");
    expect(ia).toBeGreaterThanOrEqual(0);
    expect(ib).toBeGreaterThan(ia);
    // pytest import, not vitest.
    expect(file).not.toContain('from "vitest"');
    expect(file).toContain("import pytest");
  });
});

// --- 6. no JS leaks in a known-good hybrid output -----------------------------

describe("emitHybridTestsPython — no leaked JavaScript", () => {
  const set = mkSet([TERNARY_BINDING, CLOSEDFORM_BINDING]);
  const { file } = emitHybridTestsPython(
    [TERNARY_OB, CLOSEDFORM_OB, GAP_OB],
    set,
    EMPTY_GRAPH,
  );

  it("contains no vitest/JS structural tokens", () => {
    // Boundary-aware: a real domain symbol may legitimately CONTAIN these letters
    // (e.g. `getDealSplit(` ends in "...plit("). We only ban them as standalone
    // vitest calls / matchers — a bare-word `it(`/`describe(`/`expect(` (not part
    // of a longer identifier) or the `.toBe(` matcher / JS arrow / `const `.
    const banned: readonly [string, RegExp][] = [
      ["it(", /(^|[^A-Za-z0-9_.])it\(/m],
      ["it.skip(/it.todo(", /\bit\.(skip|todo)\(/],
      ["describe(", /(^|[^A-Za-z0-9_.])describe\(/m],
      ["expect(", /(^|[^A-Za-z0-9_.])expect\(/m],
      [".toBe(", /\.toBe\(/],
      ["=> {", /=>\s*\{/],
      ["const ", /(^|[^A-Za-z0-9_.])const\s/m],
    ];
    for (const [label, re] of banned) {
      expect(file, `must not leak ${label}`).not.toMatch(re);
    }
  });
});

// --- 7. report parity with the vitest emitter across all strategies -----------

describe("emitHybridTestsPython — report parity with tests.ts", () => {
  const set = mkSet([
    TERNARY_BINDING,
    RANGE_BINDING,
    COUNTCAP_BINDING,
    CLOSEDFORM_BINDING,
    PROPERTY_BINDING,
  ]);
  const obs = [
    TERNARY_OB,
    RANGE_OB,
    COUNTCAP_OB,
    CLOSEDFORM_OB,
    PROPERTY_OB,
    GAP_OB,
  ];
  const py = emitHybridTestsPython(obs, set, EMPTY_GRAPH);
  const ts = emitHybridTests(obs, set, EMPTY_GRAPH);

  it("has byte-identical report to the vitest emitter", () => {
    expect(py.report).toEqual(ts.report);
  });

  it("emits a property body seeded with 0x9e3779b9", () => {
    // The property invariant path is pinned to seed 0x9e3779b9 (contract).
    expect(py.file).toMatch(/0x9e3779b9/i);
  });

  it("is byte-stable across two emissions (pure/deterministic)", () => {
    const again = emitHybridTestsPython(obs, set, EMPTY_GRAPH);
    expect(again.file).toBe(py.file);
  });
});

// --- 8. STRONG: the emitted text is valid python (real interpreter) -----------

describe("emitHybridTestsPython — python syntax validity", () => {
  const set = mkSet([
    TERNARY_BINDING,
    RANGE_BINDING,
    COUNTCAP_BINDING,
    CLOSEDFORM_BINDING,
    PROPERTY_BINDING,
  ]);
  const obs = [
    TERNARY_OB,
    RANGE_OB,
    COUNTCAP_OB,
    CLOSEDFORM_OB,
    PROPERTY_OB,
    GAP_OB,
  ];

  const runIt = PY ? it : it.skip;
  // NOTE: when PY is null there is no python interpreter on PATH; the test is
  // SKIPPED (not faked). In this environment `python --version` -> Python 3.x.
  runIt(
    `parses with \`${PY ?? "python (absent)"} -c ast.parse\` — every emit path`,
    () => {
      const outputs: Record<string, string> = {
        "legacy empty": emitTestsPython([]),
        "legacy stubs": emitTestsPython(obs),
        "hybrid all-strategies": emitHybridTestsPython(obs, set, EMPTY_GRAPH)
          .file,
      };
      for (const [label, src] of Object.entries(outputs)) {
        const { ok, err } = pyParses(src);
        expect(ok, `${label} must be valid python:\n${err}`).toBe(true);
      }
    },
  );
});
