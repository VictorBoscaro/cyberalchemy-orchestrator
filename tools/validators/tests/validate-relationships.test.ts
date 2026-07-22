import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const thisDir = dirname(fileURLToPath(import.meta.url));
const implRoot = resolve(thisDir, "../../");
const validator = "tools/validate-relationships.ts";

function runValidator(args: string[]) {
  return spawnSync(process.execPath, ["--import", "tsx", validator, ...args], {
    cwd: implRoot,
    encoding: "utf-8",
  });
}

function runFixture(name: string) {
  return runValidator(["--features-root", `spec/__fixtures__/relationships/${name}`]);
}

test("valid relationship endpoints pass, including Workflow and Entity relations", () => {
  const r = runFixture("valid");
  assert.equal(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /PASS/);
  assert.match(r.stdout, /canonicalSignatures=30/);
});

for (const fixture of [
  "bad-operation-enforces-value-object",
  "bad-state-machine-enforces-operation",
  "bad-reversed-enforces",
  "bad-queries-target",
  "bad-operation-emits-event",
  "bad-saga-orchestrates-operation",
]) {
  test(`${fixture} is rejected as unconstructible`, () => {
    const r = runFixture(fixture);
    assert.equal(r.status, 1, r.stdout + r.stderr);
    assert.match(r.stdout, /unconstructible-edge/);
  });
}

test("generated owned-by inverse is not an authored canonical edge", () => {
  const r = runFixture("bad-generated-owned-by");
  assert.equal(r.status, 1, r.stdout + r.stderr);
  assert.match(r.stdout, /noncanonical-edge/);
  assert.match(r.stdout, /Generated inverse/);
});
