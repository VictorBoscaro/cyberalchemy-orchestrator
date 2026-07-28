---
name: backlog
description: Create, add to, organize, and maintain BACKLOG.md files in any requested directory while preserving local conventions and existing entries. Use when a user asks to create a backlog, capture or add backlog items, reorganize backlog content, or maintain an existing backlog.
---

# Backlog

Create or extend a directory-local `BACKLOG.md` without turning a lightweight list of candidate
work into a project-management system. Preserve the file's established structure when one exists.

## Workflow

1. Resolve and canonicalize both the authorized root and target directory. Confirm that the
   resulting `BACKLOG.md` remains inside the authorized root. Stop and ask before writing if a
   missing path component, symbolic link, junction, reparse point, or other indirection makes
   containment ambiguous. Ask only if the target directory or intended backlog item is materially
   ambiguous.
2. Inspect applicable repository instructions and nearby Markdown conventions. Read the target
   `BACKLOG.md` completely when it exists.
3. Search the existing backlog for the proposed item's ID, title, objective, and close semantic
   matches. Update or extend the matching entry instead of creating a duplicate. If the request is
   already fully represented, make no change.
4. If `BACKLOG.md` is absent, create it from `assets/backlog-template.md`, adapting its title and
   connections. A request to create only the backlog file may produce an empty backlog with no
   entries; do not invent candidate work or topical tags. When the request includes an item,
   populate document and entry tags with concrete topics. If the file exists, preserve its
   unrelated frontmatter, prose, entries, ordering scheme, and formatting while making the
   smallest coherent change.
5. Apply the document and entry contracts below.
6. Re-read the result and ensure every newly created or substantially modified entry has
   the required literal ID/title, `Tags`, `Objective`, and `Description` structure. Preserve
   untouched legacy entries even when their structure differs. Mention legacy structure only when
   useful to the requested work. Verify preservation, uniqueness, meaningful connections,
   canonical containment, and idempotence. Run any local Markdown/frontmatter checks required by
   the repository.

## Document contract

- Use `artifact_kind: backlog` as the single document-kind discriminator for a new backlog or an
  existing backlog without a conflicting discriminator.
- Use free-form tags for concrete subjects the backlog covers. Do not use role, maturity, status,
  or priority words as topical tags merely to fill the list. An empty list is valid when an empty
  backlog has no grounded topic yet.
- Never add `node_type`. If an existing backlog already contains `node_type`, preserve it, report
  the discriminator incompatibility, and do not add `artifact_kind` unless the user explicitly
  authorizes that migration.
- Preserve locally required metadata. Treat `status`, priority, acceptance criteria, owner, and
  scheduling as optional unless the user requests them or the existing file/local contract
  requires them.
- Ensure a `## Connections` section exists. Add only real, meaningful typed relationships to
  known targets. If no relationship is known, state that plainly rather than fabricate a link.
- Keep backlog prose modal: entries are candidate work to evaluate, prioritize, schedule, or
  close, not claims that implementation is approved or complete.

## Entry contract

For every newly created or substantially changed entry, require:

- A stable, locally unique ID and title in the heading. Follow an established ID pattern; otherwise
  derive a short prefix from the backlog scope and allocate the next unused numeric suffix.
- `Tags`: topical labels specific to the item.
- `Objective`: the outcome or question the candidate work should address.
- `Description`: enough context, boundaries, and constraints to evaluate the item without
  presenting it as an accepted specification.

Keep existing labels as supplemental content when useful; they do not replace the literal
ID/title, `Tags`, `Objective`, and `Description` structure for an entry in the modification scope.
Fixing a typo, changing formatting, or merely moving an entry does not bring that entry into the
substantial-modification scope.
Add status, priority, acceptance criteria, owner, dates, estimates, or scheduling only when the
user asks for them or the local file already requires them. Do not invent unknown values.

## Preservation and duplicate rules

- Never replace the whole existing file merely to normalize it to the bundled template.
- Never delete or rewrite unrelated entries. Reorder entries only when the user explicitly asks
  to organize the backlog, and preserve each entry's content and identity.
- Leave untouched legacy entries structurally unchanged. Do not characterize preserved legacy
  structure as nonconformance; describe it neutrally only when it affects the requested work.
- Preserve established headings and field labels when they satisfy the required semantics.
- Treat matching IDs as the same item. Treat substantially matching title/objective pairs as
  likely duplicates and merge only the requested information into the existing entry.
- Repeating a request whose requested content is already fully recorded must produce an empty
  diff.
- If two plausible targets remain and choosing would alter different work items, ask one focused
  question before editing.

## Skill authority

Treat the `.claude` skill package as the canonical source. Other host-specific skill directories
are promoted mirrors: do not create or independently evolve a second authority. Promotion and
byte-for-byte mirror verification are coordinated outside this skill's backlog-editing workflow.

## Forward-test example

For a feature backlog request such as a promotion-gated cross-dispatch work graph, create one
stable feature-scoped entry (for example, `ACI-BL-001 — Promotion-gated cross-dispatch work
graph`) with topical `Tags`, an evaluative `Objective`, and a bounded `Description`. Preserve
links to feature architecture and work-pack context in `## Connections`; describe the item as an
open candidate and record a collapse condition when existing capabilities may already satisfy it.
