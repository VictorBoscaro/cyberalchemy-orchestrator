# Codex namespaced hook matcher repair receipt

Date: 2026-07-26

Status: `LOCAL_PASS / LIVE_HOST_RELOAD_REQUIRED`

## Problem

The shared hook implementation already normalizes `collaboration.spawn_agent`, but the Codex
configuration matcher admitted only bare suffix forms:

```text
(^Agent$|spawn_agent$|followup_task$)
```

Two registered dispatch attempts and one direct smoke helper produced no Codex hook state,
`dispatch_links`, or `host_workflow_turn_bindings`. The direct tool returned only a task name.

## Repair

`.codex/hooks.json` now admits only the closed set of supported bare, namespaced and flattened
agent-tool spellings:

```text
^(?:Agent|spawn_agent|followup_task|collaboration(?:[._])?spawn_agent|collaboration(?:[._])?followup_task)$
```

`implementations/tests/runtime/test_host_dispatch_hook.py` verifies every admitted spelling and
rejects near-miss names. The Stage-E source manifest and the `local_pilot` manifest pin were
refreshed after the change.

## Verification

The following seven-module suite passed with 48 tests:

```text
python -B -m unittest \
  implementations.tests.runtime.test_host_dispatch_hook \
  implementations.tests.runtime.test_host_ingestion_hook \
  implementations.tests.runtime.test_host_workflow_binding \
  implementations.tests.runtime.test_orchestration_bridge \
  implementations.tests.runtime.test_agent_reference_delivery \
  implementations.tests.runtime.test_bus_reveal_delivery \
  implementations.tests.runtime.test_aci_traceability -v
```

The Stage-E manifest check covered 47 files with zero digest mismatches. Its SHA-256 is
`5e1b9741be1e56bc5c7bbcf64dcdd7a6d42c98beaf703f3d62663617b633ab38`, equal to
`STAGE_E_SOURCE_MANIFEST_SHA256`.

## Live-host residue

The current Codex session did not hot-reload `.codex/hooks.json`: a post-repair
`collaboration.spawn_agent` smoke call returned successfully but still created no Codex hook state,
`dispatch_links`, or workflow binding. Therefore this receipt does not claim live-host activation.

A fresh Codex session must run one read-only helper smoke. Success requires all of:

1. a new Codex hook state file;
2. a matching append-only dispatch open and close;
3. a matching ACI `dispatch_links` row;
4. for a workflow-bound launch, a terminal `host_workflow_turn_bindings` row and
   `launch-authorized` receipt.

No review or code dispatch may resume until that live smoke passes.
