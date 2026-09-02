# Validation — IMPL-ACI-AGENT-IDENTITY-ROLE-001

Status: `ready_for_review`; worker validation, not approval.

## Pool recovery and migration

```text
initial git status --short
PASS: telemetry/agents/agent-pool.yaml absent (clean against tracked HEAD)

recovery rewrite with ErrorActionPreference=Stop
PASS: migrated=414, lines=3186

Python structural comparison
PASS: migrate_legacy_pool(git-show HEAD bytes) == parse(current production pool)
PASS: 414 normalized unique agents
PASS: normalized ref sha256:a14b7f56e25528f6de77621d5cbde81407c2cb515abcfc55d81832531a7e8bd4

MCP deterministic smoke and RPC handshake
PASS: 414 entries, 721 tags; search returns agent_name; all three tools available
```

## Current-path validation

```text
python -m unittest <pool/role/compiler/confirmation/appender/hook/bridge focused modules>
PASS: 88 tests

python -m unittest implementations.tests.runtime.test_stage_b
PASS: 19 tests

python docs/features/agent-provenance-telemetry/contracts/verify_contracts.py
PASS: aci_vectors=6 positive=5 rejection=8 candidates=16

powershell -ExecutionPolicy Bypass -File tools/install-register-dispatch-runtime.ps1 -Target <repo> -Check
PASS: verified register-dispatch runtime 0.7.0

node tools/agent-pool-mcp/scripts/smoke.mjs
node tools/agent-pool-mcp/scripts/rpc-test.mjs
PASS: 414 entries, 721 tags, three tools; responses expose agent_name
```

The 88-test command covers `test_agent_roles`, `test_agent_pool`, `test_draft_graph_compiler`,
`test_runtime_confirmation`, `test_agent_reference_delivery`, `test_anti_bias_mode_appender`,
`test_host_dispatch_hook`, `test_host_ingestion_hook`, `test_host_workflow_binding`, and
`test_orchestration_bridge`.

## Explicit regression residue

`test_runtime_type_bootstrap` plus its abuse module currently pass 14/19. The five remaining cases
exercise sequential/feedback/zig-zag handoff materialization that is absent in both tracked `HEAD`
`dispatch_workflow.py` and the pre-task tests (the compiler always emitted `slots: []` and had no
connection/handoff implementation). The identity migration now stages the current v2 authority and
therefore reaches those pre-existing assertions; it did not remove that behavior. They are not
claimed green and must not be represented as identity/role conformance evidence.

The independent reviewer must decide whether this baseline workflow gap is admissible residue for
this SWU or requires a separately authorized implementation repair. All identity/role assertions in
those modules that reach the current appender/registry path are covered by the green focused suites
above.
