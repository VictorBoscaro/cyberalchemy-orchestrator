# TASK-CONT-002 — deterministic same-session feedback umbrella

## Status

`not-promoted / split-gated`. TASK-CONT-001 is `implemented-reviewed-pass`. C2-TECH-D0 is closed.
HEADS-001 and BUS-001 are `implemented-reviewed-pass / KEEP`. The complete CONT-002 path is now
stopped at PRODUCT-PASS.

## Objective

Eventually resolve the two exact official bus contributions, materialize the four-entry canonical
author-turn-1 input and drive one non-retryable same-session fake-adapter resume. No single SWU is
authorized to implement that whole objective.

## Required sequence

1. `SWU-ACI-RUNTIME-RUN-GROUP-HEADS-001` — migration 014 component foundation — IMPLEMENTED/REVIEWED PASS.
2. `BUS-001` — migration 015 official-publication component proof — IMPLEMENTED/REVIEWED PASS.
3. `PRODUCT-PASS` — exact missing bytes/policies and new dispatch identity/CONF v2 confirmation.
4. `OPEN` — real opening materialization/verification.
5. positive Run transition.
6. `RESUME` — migration 016 effective input/request/effect acceptance.
7. fake worker/adapter witness.
8. full verification.

See [C2-TECH-D0](../../C2-TECH-D0.md) and the preserved
[Robot Talks findings](../../../../../../robot-talks/2026-09-01-continuation-c2-split/findings.md).

## HEADS-001 claim

Component/foundation only: isolated Run/Group heads, total reducers, exact CAS/races/reopen and an
execution fence that stays closed for pending/reconciliation. Tests may inject verified positive
evidence directly through generic journal/DB seams but must label it harness-only. HEADS-001 creates
no opening materializer, API, service method, production positive writer or effect.

[HEADS evidence](../../evidence/TASK-HEADS-001.md) records final repaired bytes, both cross-pair
negatives, 177/177 runtime tests, incident lineage and independent `PASS / KEEP`.

## BUS-001 closed technical unit

Use the confirmed mapping's preallocated `source_message_id`; create completed attempt prerequisites
only through journal-backed test harnesses; prove candidate -> receipt -> official typed events ->
message -> completed attempt. Do not create initial-attempt production behavior, input, effect or
adapter.

The smallest BUS draft is component-only: a pure `confirmed_bus.py` plus generic
`RuntimeJournal.accept`/mutation closures owned by `test_runtime_confirmed_bus.py`. Neither
`service.py` nor `journal.py` changes. A public service writer before PRODUCT/opening would falsely
make Group phase and reviewer visibility production-reachable.

Official verification commits `attempt.result_accepted` first, then `position.accepted` for a
confirmed `author.output` or `critique.accepted` for a confirmed `reviewer.output`. Collecting and
deliberating prerequisites remain harness-only.

Historical BUS code entry was governed by descriptor
`sha256:cfc8f64d052f9adc5f85e5ce63985f6b90ed7ce6c55845c7d379ac117f21ca53`
and readiness
`sha256:b5d09dd470fd3beeb9d5e5d7be0d28df6f2c5af22baa653c9545afe52bd497e3`.

[Final evidence](../../evidence/TASK-BUS-001.md) records 23/23 focused tests, the complete 200-test
runtime suite and independent `PASS / KEEP`. The accepted stream contract places the candidate on
the Attempt stream, then appends `attempt.result_accepted` plus the typed official event on the
Group stream. The Attempt link is non-transitioning, the Group advances exactly `+2`, and the
Attempt head remains unchanged.

## Product decision gate

The user/product must supply exact revision-instruction bytes/ref/digest; actual prompt bytes/ref/
digests; role/task refs; `provider_ref` if distinct; concrete resource-budget, sandbox and
execution/authority-fence policies; and the complete canonical audit-opening 0.6.4 mapping,
including dispatch type/route, goal, context, approver, agents and all remaining required fields.
Because these values change `confirmed_authority_digest`, a new dispatch identity/CONF v2 and new
human confirmation are required. CONF v1 remains a component fixture.

## Hard stop

After BUS-001, do not materialize/verify opening, move the Run to `ready`, finalize effective input,
create `agent_resume`, release/claim an effect or call an adapter before PRODUCT-PASS. CONT-002 is not
implemented or ready for code as an umbrella task.
