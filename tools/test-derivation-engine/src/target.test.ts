import {
  mkdtempSync,
  mkdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import {
  emptyInputViolation,
  resolveFeatureTarget,
} from "./target.js";

const roots: string[] = [];

function fixture(): string {
  const root = mkdtempSync(join(tmpdir(), "derivation-target-"));
  roots.push(root);
  return root;
}

afterEach(() => {
  for (const root of roots.splice(0)) rmSync(root, { recursive: true });
});

describe("resolveFeatureTarget", () => {
  it("resolves canonical documents at the feature root", () => {
    const root = fixture();
    writeFileSync(join(root, "states.md"), "# states\n");

    const target = resolveFeatureTarget(root, () => root);

    expect(target.featureDir).toBe(root);
    expect(target.docsDir).toBe(root);
    expect(target.presentDocs).toEqual(["states.md"]);
    expect(emptyInputViolation(target)).toBeNull();
  });

  it("resolves nested specs while preserving feature identity and artifact root", () => {
    const root = fixture();
    const specs = join(root, "specs");
    mkdirSync(specs);
    writeFileSync(join(specs, "operations.md"), "# operations\n");

    const target = resolveFeatureTarget(root, () => root);
    const direct = resolveFeatureTarget(specs, () => specs);

    expect(target.featureDir).toBe(root);
    expect(target.docsDir).toBe(specs);
    expect(target.feature).toBe(direct.feature);
    expect(direct.featureDir).toBe(root);
    expect(direct.docsDir).toBe(specs);
  });

  it("marks a directory with no canonical documents as invalid input", () => {
    const root = fixture();
    const target = resolveFeatureTarget(root, () => root);

    expect(emptyInputViolation(target)).toMatch(/no canonical input documents/);
  });
});
