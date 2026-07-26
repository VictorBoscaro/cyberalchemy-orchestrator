# `domainspec-spec-feature` Protocol Prototype

> Status: exploratory; not a ratified protocol, schema, recipe, or runtime contract.

This prototype tests a small human-readable protocol graph that can later compile into a closed
`DispatchSpec`.

Medium and High share the same review contract. Their difference is structural:

- **Medium** uses one SPEC writer, one SPEC review group, one persistent writer for all remaining
  artifacts and one persistent inline reviewer.
- **High** keeps the SPEC boundary but partitions architecture, glossary and applicable aspects
  into parallel specialist cells, followed by a dedicated integration writer.

Both graphs then run deterministic contract validation, fresh complete-corpus review and one final
high-level review.

## Start here

- [`protocol-design.md`](protocol-design.md) — provisional human-readable authority containing the
  shared review contract and compact Medium/High graph blocks.
- [`examples/medium.dispatch.example.yaml`](examples/medium.dispatch.example.yaml) — illustrative
  compiled Medium shape.
- [`examples/high.dispatch.example.yaml`](examples/high.dispatch.example.yaml) — illustrative
  compiled High shape.
- [`examples/confirmation-view.md`](examples/confirmation-view.md) — example user-facing
  confirmation.
- [`source-coverage.md`](source-coverage.md) — trace from source-skill obligations to graph
  elements and known gaps.

The YAML examples are explicitly non-confirmable because exact agents, prompts, source digests,
tools, permissions, budgets and unrolled interactions have not been resolved.
