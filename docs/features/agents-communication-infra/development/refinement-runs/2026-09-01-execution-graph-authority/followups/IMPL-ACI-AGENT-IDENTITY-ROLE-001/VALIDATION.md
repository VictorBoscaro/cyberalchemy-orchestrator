# Validation — IMPL-ACI-AGENT-IDENTITY-ROLE-001

Status: `ready_for_recheck`; forward-only worker validation, not approval.

## Pool recovery and migration

```text
initial git status --short
PASS: telemetry/agents/agent-pool.yaml absent (clean against tracked HEAD)

recovery rewrite with ErrorActionPreference=Stop
PASS: migrated=414, lines=3186

Python structural comparison
PASS: frozen fixture raw digest sha256:5c7b9745a336670ecb55df1276912166954a0d7960443f0df787405564099eba
PASS: migrate_legacy_pool(frozen v0.6 fixture) == parse(current production pool)
PASS: 414 normalized unique agents
PASS: normalized ref sha256:a14b7f56e25528f6de77621d5cbde81407c2cb515abcfc55d81832531a7e8bd4

MCP deterministic smoke and RPC handshake
PASS: 414 entries, 721 tags; search returns agent_name; all three tools available
```

## Current-path validation

```text
python -m unittest <role/pool/41-runtime-vectors/compiler/confirmation/appender/drift/hook/bridge/installer focused modules>
PASS: 96 tests

python -m unittest implementations.tests.runtime.test_stage_b implementations.tests.runtime.test_apt_stage_b
PASS: 25 tests

python ../SPEC-ACI-AGENT-IDENTITY-ROLE-001/validate_artifacts.py
PASS: frozen v0.6 -> current v0.7 exact 414-row projection
PASS: 41/41 specification vectors with exact codes and paths

python -m unittest implementations.tests.runtime.test_agent_identity_role_vectors
PASS: all 41 manifest operations execute against production pool/role/allocator/compiler code
PASS: every case emits a typed code/path and no compilation result

python docs/features/agent-provenance-telemetry/contracts/verify_contracts.py
PASS: aci_vectors=6 positive=5 rejection=8 candidates=16

powershell -ExecutionPolicy Bypass -File tools/install-register-dispatch-runtime.ps1 -Target <repo> -Check
PASS: verified register-dispatch runtime 0.7.0

python -m unittest implementations.tests.runtime.test_register_dispatch_installer
PASS: 3 tests; clean v2 install/check, clean frozen recoverable v1 projection check, v2 anti-mix rejection
LIMIT: the legacy check explicitly does not verify or reconstruct the inconsistent original root-v1 manifest authority

node tools/agent-pool-mcp/scripts/smoke.mjs
node tools/agent-pool-mcp/scripts/rpc-test.mjs
PASS: 414 entries, 721 tags, three tools; responses expose agent_name
```

The 96-test command covers `test_agent_roles`, `test_agent_pool`,
`test_agent_identity_role_vectors`, `test_draft_graph_compiler`,
`test_runtime_confirmation`, `test_agent_reference_delivery`, `test_anti_bias_mode_appender`,
`test_register_dispatch_copy_drift`,
`test_host_dispatch_hook`, `test_host_ingestion_hook`, `test_host_workflow_binding`, and
`test_orchestration_bridge`, plus `test_register_dispatch_installer`.

Craft validation: `PASS`, YAML parses, all 125 `by_id` pointers resolve, and artifact-path state is
41 present plus one intentionally absent planned review (`ART-ACI-ROADMAP-CLOSURE-REVIEW`), exactly
as its ledger row records.
`git diff --check`: `PASS` (line-ending conversion warnings only).

## 2026-09-02 committed-checkout portability addendum

Push preparation rebased the work and exposed that package/integrity metadata had pinned an
ignored host appender copy with mixed line endings rather than the canonical tracked LF blob. The
repair adds explicit LF attributes for the selected-registry contract and frozen-v1 archive,
repins the current v2 package to the tracked appender, and normalizes only CRLF/LF representation
in the three-host copy-drift assertion.

Copy-drift and installer suites pass 6/6, the current v2 package self-check passes, all four
frozen-v1 members match their existing manifest, and Stage-C passes 8/8. The prior independent
`KEEP` remains evidence for its reviewed behavior, but does not independently approve these later
portability metadata/test bytes; exact-byte re-review remains pending.

## Explicit regression residue

`test_runtime_type_bootstrap` plus its abuse module still pass 14/19. The five remaining cases
exercise sequential/feedback/zig-zag handoff materialization that is absent in both tracked `HEAD`
`dispatch_workflow.py` and the pre-task tests (the compiler always emitted `slots: []` and had no
connection/handoff implementation). The identity migration now stages the current v2 authority and
therefore reaches those pre-existing assertions; it did not remove that behavior. They are not
claimed green and must not be represented as identity/role conformance evidence.

The failing cases are one empty sequential-slot error and four missing fail-closed handoff checks;
they are classified separately from identity/role conformance and were not repaired in this SWU.
The independent reviewer must decide whether this baseline workflow gap is admissible residue or
requires a separately authorized implementation repair. All identity/role assertions that reach
the current appender/registry path are covered by the green focused suites above.
