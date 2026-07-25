import { describe, expect, it } from "vitest";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parse } from "./index.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ACI_DIR = resolve(
  __dirname,
  "../../../../docs/features/agents-communication-infra/specs",
);

describe("operations.md internal transitions", () => {
  it("anchors internal-transition tables to their named operations", () => {
    const { graph } = parse(ACI_DIR);
    const rules = graph.nodes.filter((node) => node.type === "Rule");
    const operationByRuleId = new Map(
      rules.map((node) => [node.fields.id, node.fields.op]),
    );

    expect(operationByRuleId.get("O-OPEN-1")).toBe("VerifyAuditOpening");
    expect(operationByRuleId.get("O-RUN-1")).toBe("StartRun");
    expect(operationByRuleId.get("O-GROUP-1")).toBe("StartGroup");

    for (const ruleId of ["O-OPEN-1", "O-RUN-1", "O-GROUP-1"]) {
      expect(operationByRuleId.get(ruleId)).not.toBe(
        "ConfirmRuntimeDispatch",
      );
    }
  });

  it("preserves canonical H2 operations around internal transitions", () => {
    const featureDir = mkdtempSync(
      join(tmpdir(), "domainspec-operation-headings-"),
    );
    try {
      writeFileSync(
        join(featureDir, "operations.md"),
        [
          "# Operations",
          "",
          "## CanonicalBefore",
          "",
          "### Rules",
          "",
          "| ID | Rule | Formal |",
          "| --- | --- | --- |",
          "| R-BEFORE | before | `before()` |",
          "",
          "### Internal transition — InternalStep",
          "",
          "### Rules",
          "",
          "| ID | Rule | Formal |",
          "| --- | --- | --- |",
          "| R-INTERNAL | internal | `internal()` |",
          "",
          "## CanonicalAfter",
          "",
          "### Rules",
          "",
          "| ID | Rule | Formal |",
          "| --- | --- | --- |",
          "| R-AFTER | after | `after()` |",
          "",
        ].join("\n"),
        "utf8",
      );

      const { graph, violations } = parse(featureDir);
      const rules = new Map(
        graph.nodes
          .filter((node) => node.type === "Rule")
          .map((node) => [node.fields.id, node.fields.op]),
      );
      const operations = graph.nodes
        .filter((node) => node.type === "Operation")
        .map((node) => node.fields.name);

      expect(violations).toEqual([]);
      expect(rules).toEqual(
        new Map([
          ["R-BEFORE", "CanonicalBefore"],
          ["R-INTERNAL", "InternalStep"],
          ["R-AFTER", "CanonicalAfter"],
        ]),
      );
      expect(operations).toEqual([
        "CanonicalAfter",
        "CanonicalBefore",
        "InternalStep",
      ]);
    } finally {
      rmSync(featureDir, { recursive: true, force: true });
    }
  });
});
