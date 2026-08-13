---
title: Inventory canonical-source location
date: 2026-08-13
status: FOUND
route: read-only-source-investigation
---

# Inventory canonical-source location

## Verdict

**FOUND.** The declared source is not in this consuming repository, but it exists as a clean,
tracked canonical file in the sibling Arcanum source checkout:

`C:/Users/victo/Arcanum/arcana/inventory/SKILL.md`

That checkout is on `main...origin/main` at `a5c8bc5c010711721063e258ee92559f02dfc504`.
`git status -- arcana/inventory/SKILL.md tools/bootstrap_arcanum.sh registry/SIGILS.md` is clean.
No network fetch was performed, so `origin/main` means the locally known remote-tracking ref, not a
claim that the remote has not advanced.

The blocker is therefore no longer "orphaned canonical source." It is now a controlled
cross-checkout amendment and regeneration problem.

## Direct evidence

| Artifact | SHA-256 | Finding |
|---|---|---|
| `C:/Users/victo/Arcanum/arcana/inventory/SKILL.md` | `EFBF6C6EFDF9EE088A79A03C8CEB6C6E23D38BAE1321FC6E8ADDF7809C6E5163` | Current canonical source. |
| `.agents/skills/inventory/SKILL.md` | `DA87D1ED5DEF4E246AEE01A941FD6D2CBEC6E7A44E1A7A5B5901B7A9C9676645` | Generated consumer copy. |
| `.codex/skills/inventory/SKILL.md` | `DA87D1ED5DEF4E246AEE01A941FD6D2CBEC6E7A44E1A7A5B5901B7A9C9676645` | Generated consumer copy. |
| `.claude/skills/inventory/SKILL.md` | `DA87D1ED5DEF4E246AEE01A941FD6D2CBEC6E7A44E1A7A5B5901B7A9C9676645` | Generated consumer copy. |

The three consumer copies are byte-identical. Each declares:

- `surface_kind: generated-native-runtime-package`;
- `runtime: claude`;
- `canonical_source: arcana/inventory/SKILL.md`;
- `generated_by: tools/bootstrap_arcanum.sh --profile`;
- `mutation_policy: regenerate-from-canonical-source`.

The shared `runtime: claude` value is correct only for `.claude`; it is inconsistent with the
current repo-Codex generator for `.agents` and is unexplained for `.codex`.

After removing generated provenance and reversing only the documented Claude tool-name mapping
(`AskUserQuestion` to `AskQuestions`, `Agent` to `Task`), the installed content is an exact match
for Arcanum commit `824c7dc81c25bceb62c43c126c000d7659c6b592` (2026-06-23). It is therefore a
faithful but stale generated snapshot, not an independently edited fork.

The canonical source subsequently changed in:

- `0e01f3697103531a99b3c418ce842a37a2436ac6` (2026-07-23), projection conformance;
- `ab8af3e85f199addcea443fc37e96d4bea9e1cf5` (2026-07-27), faceted runtime package.

Concrete drift includes the canonical runtime-sync contract at `SKILL.md:86-101` and the
lookup-readiness gate at `SKILL.md:249+`, both absent from the installed copies. The current
authority boundary remains explicit at `SKILL.md:335-339`.

## Canonical package and regeneration mechanism

The source is a package, not only one Markdown file. Material runtime members include:

- `arcana/inventory/runtime-manifest.json` (`schema_version` at line 2, managed paths at lines
  3-12, `authority_boundary: generated-runtime-only` at line 41);
- `arcana/inventory/scripts/sync-runtime.sh` (check/apply interface at line 7, member and bundle
  digest verification at lines 47-97, bounded managed-member application around line 151, and
  authority boundary at line 185);
- top-level `README.md`, `bin/`, `lib/`, `schemas/`, `scripts/`, `templates/`, and `test/` content.

`C:/Users/victo/Arcanum/tools/bootstrap_arcanum.sh` is the declared generator:

- lines 795-806 emit provenance and the regeneration-only mutation policy;
- lines 821-875 copy all top-level support files and all support directories except
  `development/`;
- lines 1115-1153 generate one runtime package from its canonical source;
- lines 1226-1244 resolve `arcana/<sigil>/SKILL.md` and generate the selected package;
- lines 1315-1319 write repo-Codex packages to `.agents/skills` with `runtime: codex`;
- lines 1335-1395 write and validate the Claude surface.

The bootstrap deliberately refuses a partial forced replacement of an existing `.agents/skills`
surface (`bootstrap_arcanum.sh:1464-1494`) and points to the bounded tool:

`C:/Users/victo/Arcanum/tools/sync-generated-skill-package.sh`

That tool stages one capability in a temporary target, previews checksum-aware package changes by
default, supports `--profiles repo-codex,claude`, applies only the selected package with `--apply`,
backs up the previous package bytes, restores them if either application fails, and deletes the
temporary staging tree on exit. Its last recorded change is
`952fa42b401e746ab6d622096b7d2d484ba532a0` (2026-07-30).

## Correct recovery route

No source restoration into `cyberalchemy-orchestrator/arcana/` is warranted by the evidence. The
`canonical_source` value is a path relative to the Arcanum source checkout used by the generator;
the generated consumer package is intentionally a projection.

The supported bounded route is:

1. Amend and validate only `C:/Users/victo/Arcanum/arcana/inventory/` under its owner and Git
   history.
2. Preview, without `--apply`,
   `tools/sync-generated-skill-package.sh --target C:/Users/victo/cyberalchemy-orchestrator --sigil inventory --profiles repo-codex,claude`.
3. Review the exact package diff and canonical tests before any apply.
4. Apply the same command with `--apply` only after the required gate.
5. Verify `.agents/skills/inventory` carries `runtime: codex`, `.claude/skills/inventory` carries
   `runtime: claude`, package support matches the canonical managed set, and unrelated package
   hashes are unchanged.

Do not use a full `bootstrap_arcanum.sh --force` for this bounded change: full force intentionally
replaces the complete selected surfaces.

## Facts, inferences, and gaps

### Facts

- The canonical Inventory source exists in the sibling Arcanum checkout and is clean.
- Current consumer copies are byte-identical and exactly derive from the 2026-06-23 canonical
  revision after the documented Claude transformation.
- Current Arcanum provides a selective, preview-first, rollback-capable sync for `.agents` and
  `.claude`.
- Local commit `ed04e50d0a21f4f19ac6caee954dd3c783922829` added the tracked
  `.codex/skills/inventory/SKILL.md` on 2026-08-10. `.claude` is tracked; `.agents` is not listed by
  `git ls-files` in this repository.

### Inferences

- The three identical `runtime: claude` packages were likely mirrored from one Claude-generated
  package rather than independently regenerated for each runtime. The byte identity supports this,
  but the exact copying command was not recovered.
- "Canonical source absent" in runtime-blocker artifacts 10 and 11 meant absent from the consuming
  checkout or not yet located, not absent from the local Arcanum source repository.

### Unresolved gaps

- The current selective sync supports only `.agents` (`repo-codex`) and `.claude`. It does not name
  the repository's tracked `.codex/skills` surface. Current bootstrap can write a personal Codex
  home, but no inspected contract establishes that as the owner of this repo-local `.codex` tree.
  The `.codex` regeneration/retirement owner must be decided before claiming all native surfaces
  synchronized.
- No fetch was performed; current local upstream parity with the remote was not independently
  verified.
- This investigation establishes source provenance and recovery mechanics. It does not ratify the
  proposed bounded/unregistered semantic bootstrap or authorize mutation of the sibling checkout.

## Consequence for the D1 gate

The canonical-source-location condition in runtime-blocker artifacts 10 and 11 can change from
BLOCK to PASS-with-provenance. D1 remains blocked on owner ratification, the actual canonical
amendment, validation, the `.codex` surface decision, generated-package conformance, adversarial
review, and human authorization. Finding the source removes one blocker; it does not satisfy the
remaining lifecycle and epistemic gates.
