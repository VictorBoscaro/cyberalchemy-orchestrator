# Invoke Design transport

Status: ready for `invoke plan` only for L0/L1 (`1 completed producer → 1 required slot`) after the review-driven normative amendment and Design revalidation.

- Scope manifest: `design-selection/design-scope-manifest.json`
- Selection result: `design-selection/design-selection-result.json`
- Architecture: `ARCHITECTURE.md`
- Glossary check: `GLOSSARY-CONSISTENCY.md`
- Layering seed: `IMPLEMENTATION-LAYERING-SEED.md`
- Planned witnesses: `design-selection/planned-witnesses.json`

The normative amendment is recorded under `define/`, and the scope digests and fixed-point Design
selection were refreshed against the amended ACI aspects. Plan must preserve the legacy
connected-topology fence until the active implementation layer proves safe launch and must not
claim that planned witnesses have already run.
Fan-in, the full attackers → writer → skeptic topology and non-success producer policies remain L2
or later and cannot enter the first implementation plan without another spec version.
