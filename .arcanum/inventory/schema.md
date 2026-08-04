# Inventory Schema

Schema Artifact Role: package-conventions

This file documents package conventions. It is not the canonical
machine-readable schema artifact for evidence-cards or EvidenceSets.

## Storage

- Inventory root: `.arcanum/inventory/`
- Raw source manifests: `raw/`
- Generated wiki pages: `wiki/`
- Typed entries: `entries/`
- Query syntheses: `queries/`
- Lint reports: `lint/`
- Machine index: `index.json`
- Optional specialized indexes: `indexes/*.json`
- Optional CSV projections: `projections/*.csv`

## Source Policy

- Raw sources are immutable.
- **In-repo sources are referenced in place, not copied.** `raw/` holds
  manifests that record a repo-relative path, the commit or date read, and the
  selectors used. Copying a tracked repo file into `raw/` would create a second
  copy that silently ages; do not do it.
- Only material with no durable location in this repository (pasted text,
  external pages, transcripts) is stored as an actual file under `raw/`.
- Generated pages must cite source files, source headings, or source selectors
  when possible.
- Claims without direct source support must be marked as inference, synthesis,
  or open question.

## Page Frontmatter

Frontmatter is used in this repository. Every generated page carries:

```yaml
type: concept
status: active
tags: []
sources: []
updated: YYYY-MM-DD
confidence: high | moderate | low
related: []
```

## Entry Types

Default entry types:

- source
- entity
- concept
- architecture-layer
- implementation-pattern
- decision
- capability
- workflow
- interface
- dependency-rule
- test-pattern
- observability-signal
- question
- contradiction
- synthesis

Custom entry types must define purpose, required fields, evidence rules, tag
rules, and update behavior before first use.

## Link Policy

- Ordinary markdown links with repo-relative paths. No wiki links — this
  repository must stay portable across machines and checkouts.
- Every generated page should link to related pages when meaningful.

## Machine Index Policy

- `index.md` is the human-readable catalog.
- `index.json` is the primary machine-readable catalog and must parse with `jq`.
- Every generated page, typed entry, query file, lint report, evidence-card
  bundle, and EvidenceSet bundle has a stable row in `index.json`.
- Rows include stable ID, path, kind, type, title, summary, tags, sources,
  updated date, status, confidence when known, selectors, evidence-card IDs,
  EvidenceSet IDs, and unresolved residue.
- Derived lookup maps (`by_id`, `by_type`, `by_tag`, `by_source`, `by_status`,
  `by_evidence_card`, `by_evidence_set`) are maintained in `index.json`.
- No CSV projections are enabled at install. If one is added later it must
  declare `index.json` as its source and is never authoritative.

## Authority Boundary

Inventory records are candidate-level. Terminal promotion belongs to the owner
named in `promotion_owner`:

- governed meaning and relations → `vault/` (ontology-vault)
- canonical definitions → `definitions/` (definitions-governance)
- decisions of record → `docs/decisions/`, `OBLIGATIONS.md`
- dispatch/ledger facts → the subagents dispatch ledger

A handoff packet must carry non-authority language. `governed_ref` is filled in
only after the downstream owner creates the real governed artifact.

## ID Convention

- Entries: `inventory.entry.<slug>`
- Evidence-cards: `inventory.card.<slug>`
- EvidenceSets: `evidence-set.<slug>`
- Query syntheses: `inventory.query.<slug>`
- Lint reports: `inventory.lint.<YYYY-MM-DD>`

## Log Heading Pattern

```markdown
## [YYYY-MM-DD] <mode> | <short title>
```
