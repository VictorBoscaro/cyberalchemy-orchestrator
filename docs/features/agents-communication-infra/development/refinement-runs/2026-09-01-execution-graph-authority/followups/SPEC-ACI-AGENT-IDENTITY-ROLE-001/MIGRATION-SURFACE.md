# Migration surface inventory

Status: `repaired-candidate`; file-level classification from the AIR-R9 search. A hit is not a write
target merely because it contains a legacy literal: active new-write selectors migrate, while
explicit compatibility fixtures and historical evidence remain immutable or keep a legacy branch.

## Active selectors and consumers in the atomic SWU

| Surface | Current dependency | Required migration/check |
|---|---|---|
| `tools/install-register-dispatch-runtime.ps1` | selects only runtime package v1 and registry v1 | default new installs to v2; explicit legacy-v1 mode only for historical verification; verify the selected package/registry schema, complete file set and digests |
| `.agents/skills/domainspec-subagents-strategy/SKILL.md` | names registry v1 as sole authority | name current v2 for new writes and v1 only as immutable legacy authority |
| `.codex/skills/domainspec-subagents-strategy/SKILL.md` | same | same; drift-check all three copies |
| `.claude/skills/domainspec-subagents-strategy/SKILL.md` | same | same; drift-check all three copies |
| three `register-dispatch/{SKILL.md,append-dispatch.cjs}` copies | registry-v1 path, schema 0.6.4 and seven-role literals | select accepted registry/package line; new open/close 0.7.0; preserve explicit legacy validation branch |
| `implementations/server/runtime/confirmation.py` | emits `appender_contract_version: 0.6.4` twice | resolve selected v2 contract/ref; effect and request must carry 0.7.0 plus the accepted agent-role ref |
| `implementations/server/runtime/dispatch_types.py` | hard-coded registry-v1 path/schema | version-aware resolver: v2 for new writes, v1 by explicit legacy verification path |
| `dispatch_workflow.py`, `host_dispatch_hook.py`, `host_ingestion_hook.py` | produce/stage current registry schema | emit only selected 0.7.0 new rows and identical refs |
| `legacy.py`, `orchestration_bridge.py`, `service.py`, `provenance.py` | resolve/project legacy snapshots | keep 0.6.1–0.6.4 branches and add strict 0.7.0/ref pairing without reinterpretation |
| `tools/agent-pool-mcp/src/{pool,select,adjudicate,server}.mjs` | legacy pool `name` and/or fixed role enum | consume canonical `agent_name` and selected role registry |
| `docs/features/agent-provenance-telemetry/contracts/verify_contracts.py` | real pool bytes/digest | update strict two-document v0.7 field/digest verification atomically |
| `implementations/UI-CONTRACT.md`, `implementations/tests/audit_enums.py` | seven-role literal | derive/pin the accepted registry rather than another enum |

## Affected tests and successor fixtures

- `implementations/tests/runtime/test_runtime_confirmation.py` plus new
  `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2/` prove both
  confirmation payloads select 0.7.0/ref. Existing `confirmed-dispatch-v1/` remains immutable.
- Appender/workflow/hook/resolver coverage includes `test_agent_reference_delivery.py`,
  `test_anti_bias_mode_appender.py`, `test_dispatch_workflow.py`, `test_host_dispatch_hook.py`,
  `test_host_ingestion_hook.py`, `test_host_workflow_binding.py`, `test_orchestration_bridge.py`,
  `test_runtime_type_bootstrap.py`, `test_runtime_type_bootstrap_abuse.py`, and `test_stage_b.py`.
  Legacy cases in these files may retain explicit 0.6.1–0.6.4 inputs; every new-write case must use
  the v2 selector and 0.7.0/ref.
- Pool/role coverage includes `test_draft_graph_compiler.py`, new `test_agent_pool.py` and
  `test_agent_roles.py`, MCP smoke/RPC tests, the provenance candidate snapshot, and the pool fixture
  inside `test_dispatch_workflow.py`.

## Immutable or non-live hits

- `implementations/contracts/dispatch-type-registry.v1.json` and
  `register-dispatch-runtime-package.v1.json` remain byte-identical authorities for explicit legacy
  verification. The SWU adds v2 siblings; it does not edit v1.
- Existing telemetry openings 0.6.1–0.6.4 and legacy close rows are append-only historical data.
- `implementations/experiments/aci_open_l0/**` is frozen experiment evidence, including its role and
  0.6.4 literals; it is not the current registrar authority.
- The three `skills/refine/scripts/generate-refine-dispatch.py` copies use a distinct
  `subagent_strategy.roles[].role_id` vocabulary (`route-choice-reviewer`, etc.), not telemetry
  `groups[].agents[].role`; they are active but outside this shared-role migration.
- `internal-tools/**`, `research/**`, `sessions/**`, prior reviews/specs and route receipts found by
  the broad search are historical or generated evidence. They are excluded unless an implementation
  worker proves one is executed by the current install/open/close path.
- Generic programming identifiers named `name` outside the governed agent-pool path are unrelated.

## Executable migration assertions

1. A repository surface scan classifies every hit for `0.6.4`, registry/package v1, the seven-role
   literal and governed-pool `scientists[].name`; an unclassified active hit fails the SWU.
2. Default installation resolves v2 and verifies all manifest digests. Legacy-v1 selection requires
   an explicit flag and cannot authorize a new row.
3. No new opening, close, confirmation effect or audit-opening request with schema 0.7.0 is emitted
   from an appender/package selector reporting 0.6.4.
4. Every 0.7.0 opening/close/effect/request carries the same accepted agent-role registry ref.
5. Legacy compatibility tests remain byte-/behavior-stable and are reported separately from current
   new-write tests.

The bounded search currently yields 28 selector/version files, 13 broad role-literal files and 7
governed-pool files. These counts are evidence for this snapshot, not a permanent allowlist; the
implementation SWU must rerun the search and classify new hits.
