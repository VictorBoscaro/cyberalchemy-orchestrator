# Codex namespaced hook matcher repair receipt

Date: 2026-07-26

Status: `LOCAL_PASS / HOST_BINARY_RELOAD_REQUIRED`

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

## Corrected live-host diagnosis

A fresh trusted Codex session on 2026-07-26 reproduced the failure after the matcher repair and
after the exact hook definitions had been trusted. The host reported `CodexHooks` enabled and
executed other hook-capable function tools, but `collaboration.spawn_agent` ran internally as
`collaborationspawn_agent` without any `PreToolUse` event. It created a child thread while producing
no Codex hook state, YAML open/close, `dispatch_links`, or `launch-authorized` receipt.

The missing event is therefore not a matcher or trust failure. The embedded VS Code host binary,
`codex-cli 0.146.0-alpha.3.1`, does not route its multi-agent handler through the generic function
tool hook payload path. Upstream Codex changed that default in
`5c20513a1b3d15898429abd92b3676b76795a892` (`Default function tools into tool hooks`), and the
official `rust-v0.145.0` source contains the corrected path.

The user-scoped official Codex package `0.146.0-alpha.10.1` is installed and VS Code
`chatgpt.cliExecutable` points to its native executable. The already-running extension host still
uses `0.146.0-alpha.3.1`; it must be reloaded before another smoke.

A fresh Codex session must run one read-only helper smoke. Success requires all of:

1. a new Codex hook state file;
2. a matching append-only dispatch open and close;
3. a matching ACI `dispatch_links` row;
4. for a workflow-bound launch, a terminal `host_workflow_turn_bindings` row and
   `launch-authorized` receipt.

No review or code dispatch may resume until the extension reloads onto the replacement binary and
that live smoke passes. If the replacement binary still omits the event, disable multi-agent
dispatch for this repository and treat the limitation as an upstream host blocker rather than
changing the matcher again.
