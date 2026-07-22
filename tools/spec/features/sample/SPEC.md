# Sample Feature — v2 validation fixture

Minimal **valid** feature pack so the validation-governance gate (`npm run validate`) runs
**non-vacuously green**:

- **C9 (link integrity):** no external links to break.
- **C11 (edge-law conformance):** no relation declarations, so nothing can violate the layering edge-law.

Replace/extend with real feature packs as DomainSpec v2 authors them; this fixture exists only so the
gate has a concrete, conforming feature to pass over (not an empty run).
