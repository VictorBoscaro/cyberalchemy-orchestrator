import { existsSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { CANONICAL_DOCS } from "./provenance/index.js";

export interface ResolvedFeatureTarget {
  /** Stable feature root: generated artifacts are written beside the human TEST-SPEC. */
  readonly featureDir: string;
  /** Directory containing the canonical aspect documents consumed by the grammar. */
  readonly docsDir: string;
  readonly feature: string;
  readonly presentDocs: readonly string[];
}

function docsPresent(dir: string): string[] {
  const aspects = CANONICAL_DOCS.filter((file) => existsSync(join(dir, file)));
  if (aspects.length > 0) return [...aspects];
  return existsSync(join(dir, "SPEC.md")) ? ["SPEC.md"] : [];
}

/**
 * Resolve both supported feature layouts:
 *
 *   feature/{states,operations,...}.md
 *   feature/specs/{states,operations,...}.md
 *
 * Passing the nested `specs/` directory directly preserves the parent feature
 * identity and still places generated artifacts at the feature root.
 */
export function resolveFeatureTarget(
  arg: string,
  namedFeatureDir: (feature: string) => string,
): ResolvedFeatureTarget {
  const asPath = resolve(arg);
  const selected = existsSync(asPath) ? asPath : namedFeatureDir(arg);

  const selectedDocs = docsPresent(selected);
  if (selectedDocs.length > 0) {
    const selectedIsSpecs = basename(selected).toLowerCase() === "specs";
    const featureDir = selectedIsSpecs ? dirname(selected) : selected;
    return {
      featureDir,
      docsDir: selected,
      feature: basename(featureDir) || "feature",
      presentDocs: selectedDocs,
    };
  }

  const nested = join(selected, "specs");
  const nestedDocs = docsPresent(nested);
  if (nestedDocs.length > 0) {
    return {
      featureDir: selected,
      docsDir: nested,
      feature: basename(selected) || "feature",
      presentDocs: nestedDocs,
    };
  }

  return {
    featureDir: selected,
    docsDir: selected,
    feature: basename(selected) || "feature",
    presentDocs: [],
  };
}

export function emptyInputViolation(
  target: ResolvedFeatureTarget,
): string | null {
  return target.presentDocs.length === 0
    ? `no canonical input documents found in ${target.featureDir} or its specs/ directory`
    : null;
}
