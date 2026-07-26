# Repository Leverage Priority — Collected Returns

Status: partial collection accepted by parent.

## Seat: dependency/value-stream

The dependency scout recommended `ACI-005`, the opening materializer, as the highest-centrality
missing runtime primitive. Its evidence showed that ACI-005 feeds the close materializer and fake
execution, which then feed the fixed protocol and query path. It also found that the skill protocol,
prompt/graph control plane, and macro-to-micro experiment remain useful but are not yet the first
executable dependency.

Primary cited evidence:

- `docs/features/agents-communication-infra/work-pack/shared/swu-manifest.md`
- `docs/features/agents-communication-infra/WORK-PACK.md`
- `docs/features/agents-communication-infra/work-pack/tasks/TASK-020.md`
- `docs/features/agents-communication-infra/work-pack/descriptors/SWU-ACI-BUS-DELIVERY-001.json`

## Seat: adversarial portfolio

The portfolio scout recommended first dogfooding the already implemented host-workflow binding and
BUS reveal/materialized-input capabilities as one end-to-end harness. Its argument was that this
creates fast feedback, is reversible, and can expose identity or authority duplication before a
larger runtime primitive is built.

Primary cited evidence:

- `implementations/tests/runtime/test_host_workflow_binding.py`
- `implementations/tests/runtime/test_bus_reveal_delivery.py`
- `implementations/server/runtime/host_dispatch_hook.py`
- `implementations/server/runtime/reveal_delivery.py`
- `docs/decisions/host-agent-dispatch-input-binding.md`

## Seat: runtime/build-test

The runtime scout's terminal return was not available to the parent after an interrupted join. The
dispatch is therefore synthesized as a partial three-seat result using two accepted independent
returns plus parent verification. No claim depends on an inferred third-seat conclusion.

## Parent verification and later readiness check

A subsequent read-only readiness helper found that the proposed dogfood seam already exists in
large part inside the BUS fixtures, but currently fails because the dispatch appender has moved to
schema `0.6.2` while multiple host/BUS producers, fixtures, mappings, goldens, and manifests remain
on `0.6.1`. It reported 12/12 focused tests failing at opening before their behavioral assertions.

This later check does not retroactively become a research seat. It is recorded as follow-on
readiness evidence that refines the implementation order.
