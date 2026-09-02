---
name: domainspec-spec-feature
description: Create or evolve a feature specification using DomainSpec templates and taxonomy.
argument-hint: "<feature-name> [--update]"
agent: domainspec-spec-writer
allowed-tools: Read, Write, Glob, Grep, Task
---

<objective>
Produce complete and consistent DomainSpec documentation for one feature before implementation starts.
</objective>

<context>
Source references:
- domainspec/TAXONOMY.md
- domainspec/RELATIONSHIPS.md
- domainspec/templates/*.md
Target location:
- docs/features/{feature-name}/
</context>

<process>
0. **Discovery-existence precondition (soft gate).** Before any spec-authoring step:
   1. Determine the feature slug from the invocation context (the `<feature-name>` argument, path, or briefing).
   2. Parse skill arguments for `--skip-discovery`. If present, the next non-flag token (or the value after `=`) is the one-line waiver reason; capture it as `discovery_waiver_reason`. If `--skip-discovery` is absent, treat the gate as armed.
   3. Search for an existing discovery at BOTH:
      - `vault/discovery/<topic>-definitions/<slug>.md` (knowledge scope)
      - `docs/features/<feature>/discovery/<slug>.md` (application scope)
   4. If found → proceed to existing logic (step 1 below).
   5. If MISSING AND `--skip-discovery` was passed:
      - Proceed to existing logic, AND ensure the resulting SPEC.md frontmatter includes `discovery_waived: true` plus `discovery_waiver_reason: "<one-line reason supplied by user>"`. (The spec-writer agent applies the writeback during SPEC.md creation/update.)
   6. If MISSING AND no flag → HALT with a recommendation block (NOT a hard refuse). The exact wording must include:
      - "No discovery exists for <feature>."
      - Pointer: "Write the discovery first via `.claude/skills/custom/discovery-writing.md`."
      - Override: "Or pass `--skip-discovery` (with a one-line waiver reason) to proceed without one."
      - Bounce option: "Or invoke `domainspec-interviewer` for help classifying scope (knowledge → vault, application → feature folder)."
      - Wait for user response. Do NOT proceed until user resolves.

   **Document check (standing rule — fires inside steps 2–5, once per document, never batched at the end).** Immediately after writing each document (SPEC.md, architecture.md, glossary.md, and each individual aspect file) and before starting the next one:
   1. Spawn ONE subagent — a single helper, staying within the one-agent helper rule of `domainspec-subagents-strategy` (that boundary is a declared open question; never spawn a second agent per document). Give it the document path, its source template, and the governing discovery/SPEC. In one pass it (a) assesses the document — template conformance, taxonomy meta-type fit, cross-link/anchor integrity, authority trace (every claim maps to a discovery section or decision), formal-rule testability — and (b) adversarially challenges its own findings (claim ≤ proof) before returning a verdict `pass | fix` with a concrete fix-list.
   2. Apply the confirmed fixes, then have the SAME agent re-check by continuing its conversation — not a new spawn. If it still returns `fix` after one re-check, stop and surface the disagreement instead of looping.
   3. Report every helper post-hoc in the run summary (`agents_spawned`).

1. Create or update SPEC.md and concept table.
2. Generate or update `architecture.md` as a required default companion artifact from `domainspec/templates/architecture.md`, unless an equivalent feature architecture document already exists and is being updated in place. Populate Architecture Intent, Source Contracts, the six required architecture views, dependency/interface rules, decision log, risks, design transport notes, and Gate Result from current DomainSpec contracts.
3. Generate `glossary.md` as a default companion artifact from `domainspec/templates/glossary.md`, distilling one definition for every feature concept.
4. Generate relevant aspect files from templates, one file at a time — the Document check runs after each file, before the next one is started.
5. Ensure `SPEC.md` links to `architecture.md` and `glossary.md` when those artifacts exist.
6. Add formal rules, formulas, transitions, and invariants where applicable.
7. Validate the feature architecture contract: source contracts present or discovery mode explicitly approved, all six views present, dependency/interface rules recorded, decision log populated or explicitly empty with reason, Gate Result includes status and reason, and architecture-to-aspect references resolve.
8. Summarize what is ready and what remains undefined.
</process>
