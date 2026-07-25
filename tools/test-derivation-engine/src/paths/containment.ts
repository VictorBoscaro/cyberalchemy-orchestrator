// Write-path containment guard (G3, SWU-4). A resolved output path MUST stay inside
// the allowed root and MUST NOT escape into the public `arcanum` submodule. Pure +
// unit-testable; used by both `derive --out` and `emit-tests`.

import path, { posix, win32 } from "node:path";

type PathApi = typeof posix;

const windowsAbsolutePath = /^(?:[a-zA-Z]:[\\/]|\\\\)/;

function pathApiFor(outPath: string, allowedRoot: string): PathApi {
  if (
    windowsAbsolutePath.test(outPath) ||
    windowsAbsolutePath.test(allowedRoot)
  ) {
    return win32;
  }
  if (outPath.startsWith("/") || allowedRoot.startsWith("/")) {
    return posix;
  }
  return path;
}

export function containmentError(
  outPath: string,
  allowedRoot: string,
): string | null {
  const pathApi = pathApiFor(outPath, allowedRoot);
  const resolved = pathApi.resolve(outPath);
  const root = pathApi.resolve(allowedRoot);
  const rel = pathApi.relative(root, resolved);
  if (
    rel === ".." ||
    rel.startsWith(`..${pathApi.sep}`) ||
    pathApi.isAbsolute(rel)
  ) {
    return `refusing to write outside the allowed root:\n  path: ${resolved}\n  root: ${root}`;
  }
  const segments = resolved.split(pathApi.sep);
  const isPublicArcanumSegment =
    pathApi === win32
      ? segments.some((segment) => segment.toLowerCase() === "arcanum")
      : segments.includes("arcanum");
  if (isPublicArcanumSegment) {
    return `refusing to write into the public arcanum submodule: ${resolved}`;
  }
  return null;
}
