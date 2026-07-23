# Shared Context

APT has three projection levels: Session, existing Dispatch and Research. `SessionDispatchLinked`
is the sole Session-to-Dispatch authority; `ResearchCapture.dispatch_id` is the sole
Dispatch-to-Research authority. Capture bytes are immutable and artifact-only; facts are
append-only versions; records are deterministic as-of projections.

APT is subordinate to ACI and must not own a durable bus, journal, appender, receipt, canonicalizer
registry, artifact store or Dispatch ledger. Controlling sources are `../../WORK-PACK.md`,
`../../specs/architecture.md`, `../../specs/domain.md`, `../../specs/rules.md`,
`../../specs/states.md`, `../../specs/queries.md`, and `../../TEST-SPEC.md`.
