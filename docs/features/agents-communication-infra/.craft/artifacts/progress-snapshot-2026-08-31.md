# Agents Communication Infrastructure — progress snapshot

Date: 2026-08-31

## Completed or evidenced

- Scope was narrowed to dispatch infrastructure; Schema Service is excluded.
- The target architecture separates deterministic coordination, adapters, mediated bus
  contributions, durable journal state and immutable effective inputs.
- Existing bounded runtime seams include SQLite migrations through 011, atomic journal command
  acceptance, stable receipts, artifact storage, host workflow binding and bounded bus delivery.
- The exact protocol-compilation SWU is implemented and verified within a non-authoritative
  candidate-only ceiling.
- ACI-CONT-001 accepts the parked-continuation model: a physical attempt terminates before waiting;
  the runtime later resumes or reconstructs from exact persisted input.
- Continuation DomainSpec contracts were aligned across capability, domain, states, events,
  operations, interfaces, mappings, rules, workflows, architecture, glossary and TEST-SPEC.
- The finite first graph is `author:0 -> reviewer:0 -> author:1` with exactly two frozen official
  contribution mappings.
- The host probe demonstrated same-agent-reference follow-up with prior-turn recall and active
  interruption on the observed Codex collaboration surface.
- A sequential three-SWU continuation plan, task context, reviewer topology and pre-mutation test
  baseline were prepared.
- Focused Stage-B tests passed 19/19 before continuation code entry.

## Not implemented

- No `AgentContinuation`, continuation mapping, reducer, suspension, resume, reconstruction,
  cancellation or expiry code has been added.
- No runtime-managed `ConfirmedDispatch` writer or confirmed expanded turn graph exists.
- No real Codex continuation adapter has been admitted.
- No production, multi-host or Schema Service work is authorized by this effort.

## Current blocker

TASK-CONT-001 requires O-CONT-S5 to validate that the continuation and both mappings were
preallocated by a confirmed turn graph. The current runtime has only the legacy `dispatch_links`
path and cannot use it as runtime-managed confirmation authority.

The owner must choose:

1. durable runtime confirmation, which proves the real JSON-to-`ConfirmedDispatch` path; or
2. a test-only seeded authority fixture, which proves only the local suspension consumer seam.

## Validation residue

The pre-mutation full runtime suite ran 152 tests with 1 failure and 26 errors from documented
pre-existing Stage-E manifest and fixture drift. New continuation work must add no new signature;
the existing drift remains a separate maintenance concern.

