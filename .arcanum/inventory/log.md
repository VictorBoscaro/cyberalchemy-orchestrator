# Inventory Log

This log is append-only. Add one entry after each meaningful inventory
operation.

## [2026-08-04] install | Inventory package initialized

- Mode: install
- Actor: agent
- Summary: Inventory package created at `.arcanum/inventory/` alongside the
  existing `.arcanum/observability/` and `.arcanum/runtime/` layers. No existing
  repository knowledge surface was adopted or absorbed.
- Conventions selected:
  - root `.arcanum/inventory/`, tracked by git (not ignored);
  - in-repo sources referenced in place via manifests in `raw/`, never copied;
  - frontmatter enabled; ordinary markdown links only (no wiki links);
  - `index.json` primary machine index, no CSV projections;
  - observability integration on (`.arcanum/observability/` present).
- Adoption decision: `docs/`, `vault/`, `definitions/`, `research/`, and
  `plans/` remain independent and authoritative in their own right. They are
  ingest *sources* for inventory, not inventory pages. Rationale: Inventory is
  a non-authority read model; folding governed surfaces into it would put
  candidate-level records in the position of governed ones.
- Files changed: README.md, schema.md, index.md, index.json, log.md, tags.md,
  and empty `indexes/ raw/ wiki/ entries/ queries/ lint/`
- Follow-up: no ingest performed. First ingest target is unchosen — see
  `## Open Gaps` in [index.md](index.md).
