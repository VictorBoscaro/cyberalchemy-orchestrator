---
tags: [ledger, dispatch, orchestration, architecture]
node_type: audit
is_session: false
layer: architecture, domain
nature: explanatory
status: active
veracity: high
conviction: high
version: 1.0.0
last_updated: 2026-07-21
---

# Ledger enum-drift finding — two close rows bypassed the validated appender

## Objective

Check whether every "close" record in the real ledger was written through the one validated
gate the project relies on — or whether some got in another way.

## Context

The ledger is the project's system of record: every batch of agent work is logged there, and
one rule is meant to keep it trustworthy — *every* write goes through a single validated
appender that rejects anything malformed. This audit found two records from 2026-07-18 that
could only have been added by hand, bypassing that gate. That matters because the project's
next big step — letting a button in the UI trigger real dispatches — assumes the ledger has
exactly one write path. Until we understand how those two records got in, that single-writer
rule stays unproven, and anything built on top of it is provisional. This is the audit the main
README flags as the keystone to resolve before that step.

> The canonical vault home for the finding [[engine-constitution]] EG-1 cites as its live
> counterexample. An audit, not a bet: it reports what the ledgers actually contain.

## The finding

An audit of the real ledgers (`implementations/tests/audit_enums.py`, run 2026-07-19) found
**10 `exit_reason` values outside the v0.6.0 closed enum** across 648 close rows, in two
distinct patterns:

1. **Free prose in the field** (8 cases, all 2026-06-12, in `domainspec` and
   `domainspec-lean-formalization`): long strings like `"success — 3 critics converged: …"`
   and `"synthesis_complete — KILL …"`. These pre-date the closed vocabulary — **grandfathering
   explains them** (EG-6: old rows are historical artifacts, never re-validated).

2. **Pure `success` (2 cases), dated 2026-07-18**, in `domainspec-lean-formalization`
   (`2026-07-18-strong-unification-first-law`, `2026-07-18-empirical-unification-preregistration`).
   **These are NOT historical.**

## Why it matters

`register-dispatch/append-dispatch.cjs` validates `exit_reason` against the closed set
`resolved | loop_ceiling_reached | dissent_irreconcilable | user_abort | error` and exits 2 on
anything else. A close row dated 2026-07-18 carrying `exit_reason: "success"` therefore
**cannot have passed the appender** — the validated write path was **bypassed** (probable manual
YAML edit), despite the append-only hook.

This is the live counterexample that holds **[[engine-constitution]] EG-1** ("one writer — every
ledger mutation goes through the validated appender") at `veracity: medium` and **blocks its
promotion**. It also propagates: **[[orchestration-infra]]**'s load-bearing claim (the bus's
lifecycle stream is a *projection* of the ledger, not a *duplicative* store) assumes EG-1's
one-writer spine; if a write path exists outside the appender, that projection's integrity
guarantee inherits the same hole.

Also noted by the same audit: `dispatch_type: code` appears 26× and `suggestion` 1× — RESERVED
types that, per `register-dispatch`, "signal an upstream violation" when registered.

## Repair path (open)

Reproduce how the two 2026-07-18 rows entered the file without passing `validateDispatch`. If a
write path outside the appender exists, either close it (restore EG-1 end-to-end) or amend EG-1 to
admit a second validated writer. Until then, EG-1 stays promotion-blocked and any design leaning on
it is provisional. **This is the keystone next step for Phase 2.**

## Connections

| Document | Type | Description |
|---|---|---|
| [[engine-constitution]] | `contradicts` | Refutes EG-1's aspired "one writer" invariant; the reason EG-1 is `veracity: medium` and promotion-blocked. |
| [[orchestration-infra]] | `grounds` | The infra hypothesis's bus-as-projection leans on EG-1; this finding is the evidence for the unresolved risk it already admits (caveat + collapse-test), not a conflict with it. |
| `implementations/server/ledger.py` | `contextualizes` | The reader that never writes (EG-1's other half); the appender, not this, owns writes. |
