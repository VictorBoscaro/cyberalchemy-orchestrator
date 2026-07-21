# TASK-040 — Recovery, sealing, races and realtime

## Objective

Prove that the L0 runtime remains correct when failures, deadlines, cancellation, phased visibility
and reconnecting observers are introduced.

- **Layer/slice:** L1 / S-002 / W2.
- **Dependencies:** L0 pass; accepted OQ-VISIBILITY through OQ-SANDBOX ADRs.
- **Proposed write scope:** runtime policy/outbox/projections/API modules and fault/security tests.

## Smallest Working Units

- **SWU-ACI-012 — Generalized outbox/reconciler:** retries, pending/unknown states, startup recovery
  and explicit operator repair without weakening L0 materializer rules.
- **SWU-ACI-013 — Phase ACL and reveal barrier:** principal/run/seat/round/phase capabilities;
  atomic manifest publication; denial across API, SSE, artifacts, debug and workspace surfaces.
- **SWU-ACI-014 — Deadline/cancel/race policy:** accepted `deadline.fired`; cancellation lifecycle;
  enumerated allowed traces for last-position vs deadline and cancel vs completion/commit.
- **SWU-ACI-015 — Cursor projection and SSE:** ordered runtime cursor, reconnect, expired cursor ->
  consistent snapshot fallback, heartbeat and no sealed payload leakage.
- **SWU-ACI-016 — Minimal read-only sandbox/credential boundary:** fail closed when containment or
  minimum credential cannot be established.

| SWU | Dependencies | Write scope | Acceptance evidence | Validation | Owner |
|---|---|---|---|---|---|
| 012 | L0 pass | runtime outbox/reconciler | restart and pending/unknown recovery traces | fault suite | local-fallback |
| 013 | 012 + visibility ADR | policy/capability modules | cross-surface deny/redact matrix | security contract tests | local-fallback |
| 014 | 012 + timeout/cancel ADRs | domain policy/reactors | one allowed terminal per race ordering | deterministic race suite | local-fallback |
| 015 | 012 + realtime ADR | projections/API/SSE | ordered reconnect and snapshot fallback receipts | API/SSE tests | local-fallback |
| 016 | sandbox ADR | launcher/credential boundary | fail-closed and no-secret inspection report | adversarial sandbox tests | local-fallback |

## Done when

Every fault/race fixture has one allowed terminal, projections rebuild from the journal, stale
capabilities fail and no pre-reveal peer content is visible through any controlled surface.
