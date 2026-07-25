import { describe, expect, it } from "vitest";
import { containmentError } from "./containment.js";

describe("containmentError", () => {
  const posixRoot =
    "/repo/validation/poker-team/docs/features/financial-settlement";
  const windowsRoot =
    String.raw`C:\repo\validation\poker-team\docs\features\financial-settlement`;

  it("allows a POSIX path inside the allowed root", () => {
    expect(
      containmentError(`${posixRoot}/TEST-SPEC.engine.md`, posixRoot),
    ).toBeNull();
  });

  it("rejects a POSIX path escaping the allowed root", () => {
    expect(
      containmentError(`${posixRoot}/../../../../etc/passwd`, posixRoot),
    ).toMatch(/outside the allowed root/);
  });

  it("allows a Windows path inside the allowed root", () => {
    expect(
      containmentError(
        String.raw`${windowsRoot}\TEST-SPEC.engine.md`,
        windowsRoot,
      ),
    ).toBeNull();
  });

  it("rejects a Windows path escaping the allowed root", () => {
    expect(
      containmentError(
        String.raw`${windowsRoot}\..\..\..\..\Windows\system.ini`,
        windowsRoot,
      ),
    ).toMatch(/outside the allowed root/);
  });

  it("does not mistake a dot-dot-prefixed child for an escape", () => {
    expect(
      containmentError(`${posixRoot}/..derived/x.test.ts`, posixRoot),
    ).toBeNull();
    expect(
      containmentError(
        String.raw`${windowsRoot}\..derived\x.test.ts`,
        windowsRoot,
      ),
    ).toBeNull();
  });

  it("rejects a POSIX path into the public arcanum submodule", () => {
    expect(containmentError("/repo/arcanum/spells/x.md", "/repo")).toMatch(
      /arcanum/,
    );
  });

  it("rejects a Windows path into the public arcanum submodule", () => {
    expect(
      containmentError(
        String.raw`C:\repo\arcanum\spells\x.md`,
        String.raw`C:\repo`,
      ),
    ).toMatch(/arcanum/);
  });

  it("rejects the arcanum directory itself", () => {
    expect(containmentError("/repo/arcanum", "/repo")).toMatch(/arcanum/);
    expect(
      containmentError(String.raw`C:\repo\ARCANUM`, String.raw`C:\repo`),
    ).toMatch(/arcanum/i);
  });

  it("does not mistake an arcanum-prefixed segment for the submodule", () => {
    expect(containmentError("/repo/arcanum-notes/x.md", "/repo")).toBeNull();
    expect(
      containmentError(
        String.raw`C:\repo\arcanum-notes\x.md`,
        String.raw`C:\repo`,
      ),
    ).toBeNull();
  });

  it("rejects a Windows path on a different drive", () => {
    expect(
      containmentError(String.raw`D:\output\x.md`, String.raw`C:\repo`),
    ).toMatch(
      /outside the allowed root/,
    );
  });

  it("allows a normal repo path under a broad root", () => {
    expect(
      containmentError(
        "/repo/validation/poker-team/backend/src/domain/__derived__/x.test.ts",
        "/repo",
      ),
    ).toBeNull();
  });
});
