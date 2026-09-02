# Work pack — IMPL-ACI-AGENT-IDENTITY-ROLE-001

Status: `ready_for_spec_recheck`; production entry remains blocked until the independent reviewer
returns `KEEP` on this repaired package.

## Objective and atomicity

Make final `display_name` allocator-owned, make the owner-selected eight-role registry the shared
configuration source, and migrate the real pool from v0.6 `name` to v0.7 `agent_name` without a
compatibility split. Pool, all direct readers and their tests move in one implementation SWU; on a
failed migration check, none of those writes is accepted.

## Exact implementation write scope

Pool and direct consumers:

- `telemetry/agents/agent-pool.yaml`;
- `tools/agent-pool-mcp/src/pool.mjs`, `select.mjs`, `adjudicate.mjs`, `server.mjs`;
- `tools/agent-pool-mcp/scripts/smoke.mjs`, `rpc-test.mjs`, and `README.md`;
- `docs/features/agent-provenance-telemetry/contracts/verify_contracts.py` and
  `contracts/fixtures/seed-registry-candidates-v01.json`;
- `implementations/tests/runtime/test_dispatch_workflow.py` pool fixture.

Registry, compiler, registrar, row-schema producers/readers and shared consumers:

- new `implementations/contracts/agent-role-registry.v1.json`,
  `agent-role-registry-authority.v1.json`, `agent-role-host-routing.v1.json`,
  `dispatch-ledger-row.v0.7.0.schema.json`, and a new immutable
  `implementations/contracts/dispatch-type-registry.v2.json` selecting ledger schema `0.7.0` plus
  the accepted agent-role ref; retain `dispatch-type-registry.v1.json` unchanged as legacy evidence;
- a successor `implementations/contracts/register-dispatch-runtime-package.v2.json`; retain v1
  unchanged. Include all selected registry/appender/skill digests in v2;
- `tools/install-register-dispatch-runtime.ps1`: default to the complete v2 package for new writes;
  expose v1 only through an explicit legacy-verification selection and validate either selected
  schema/file set/digest without mixing them;
- new `implementations/server/runtime/agent_roles.py`,
  `implementations/server/runtime/agent_pool.py`, plus
  `implementations/server/runtime/dispatch_types.py`;
- `implementations/server/runtime/draft_graph_compiler.py`,
  `implementations/tests/runtime/test_draft_graph_compiler.py`, and new focused
  `test_agent_pool.py` / `test_agent_roles.py` under the same test directory;
- all three `register-dispatch` pairs:
  `.agents/skills/register-dispatch/{append-dispatch.cjs,SKILL.md}`,
  `.codex/skills/register-dispatch/{append-dispatch.cjs,SKILL.md}`, and
  `.claude/skills/register-dispatch/{append-dispatch.cjs,SKILL.md}`;
- all three route-strategy copies:
  `.agents/skills/domainspec-subagents-strategy/SKILL.md`,
  `.codex/skills/domainspec-subagents-strategy/SKILL.md`, and
  `.claude/skills/domainspec-subagents-strategy/SKILL.md`;
- `implementations/server/runtime/dispatch_workflow.py`, `host_dispatch_hook.py`,
  `host_ingestion_hook.py`, `confirmation.py`, `legacy.py`, `orchestration_bridge.py`, `service.py`, and
  `provenance.py`; the latter three must at minimum preserve and compare the new ref wherever they
  resolve, pair or project opening/close snapshots;
- `implementations/UI-CONTRACT.md` and `implementations/tests/audit_enums.py`;
- registrar/workflow tests that stage or invoke the appender:
  `test_agent_reference_delivery.py`, `test_anti_bias_mode_appender.py`,
  `test_dispatch_workflow.py`, `test_host_workflow_binding.py`, `test_orchestration_bridge.py`,
  `test_runtime_type_bootstrap.py`, and `test_runtime_type_bootstrap_abuse.py`;
- directly affected hook/resolver tests: `test_host_dispatch_hook.py`,
  `test_host_ingestion_hook.py`, `test_runtime_confirmation.py`, and `test_stage_b.py`;
- new `docs/features/agents-communication-infra/specs/fixtures/confirmed-dispatch-v2/`; existing
  `confirmed-dispatch-v1/` remains immutable compatibility evidence.

`MIGRATION-SURFACE.md` is the traceability baseline for active writes, affected tests and immutable
hits. Historical telemetry rows, historical specs/reviews, v1 authorities and experimental oracle
fixtures are read-only. Any unclassified live hit for pool identity, role vocabulary, 0.6.4 or
registry/package selection joins this atomic scope before mutation.

## Ordered tasks

1. Re-run the consumer search and fail the SWU if a live `scientists[].name` or seven-role constant
   is outside the declared migration set. Also scan `0.6.4`, `dispatch-type-registry.v1.json`,
   `register-dispatch-runtime-package.v1.json` and both v1 schema identifiers. Classify every hit as
   active consumer, affected compatibility test/fixture or immutable historical evidence.
2. Install immutable role-registry v1 plus trusted authority and a common resolver. Make compiler,
   appender copies, MCP boundary, UI contract and enum audit consume the selected accepted registry
   or a generated artifact whose digest is checked against it. Add a drift test across three skill
   copies. Move `host_dispatch_hook.py` keyword-to-role inference into the pinned host-routing
   configuration; every configured target must exist in the selected role registry, and fallback
   must be explicit. Future roles may require routing/policy data changes but no Python/JS enum edit.
3. Make registrar validation version-aware without changing `0.6.4`: v1 dispatch-type registry and
   runtime package remain immutable; their parser accepts openings `0.6.1`–`0.6.4` and legacy closes
   exactly as today. Select v2 for new writes. Every new opening is `0.7.0` and requires
   `agent_role_registry_ref={name,version,digest}`; every new close is `0.7.0` and repeats the exact
   opening ref. Appender, host hook, workflow, bridge and strict resolver reject missing refs,
   mixed-version pairs and mismatched refs. Preserve the ref through snapshots/provenance. Accept
   singular `other`, reject `others`, and prove a synthetic future registry revision can be selected
   without editing consumer enums.
4. Migrate install/route/confirmation selection as one seam: default installer and route-strategy
   instructions select the v2 package; confirmation derives its appender version and role ref from
   that selected authority. Keep explicit v1 verification available, but reject any 0.7.0
   opening/close/effect/request emitted through a 0.6.4 selector. Add the v2 confirmation fixture and
   focused tests without editing the v1 fixture.
5. Implement the exact v0.6 authority check and deterministic v0.7 migration. Preserve two
   documents, metadata except the declared changes, all roster fields/order and 414 identities.
   Replace `name` with `agent_name` in the real YAML and every direct consumer/test in this SWU.
6. Make steady-state loading accept only canonical v0.7 `agent_name`. Reject duplicate YAML keys,
   document count/order, unknown keys, missing/dual/empty/non-string identity, duplicate identity
   and metadata drift. Remove/disable only the legacy pool-`name` runtime adapter once the atomic
   pool migration tests pass; retain the explicit telemetry-v1 verification branch above.
7. Extend compilation context with registry/pool refs and exact assignments. Verify context digest,
   trusted Ed25519 signature, evidence freshness, conflict and replay before compilation.
8. Remove DraftGraph `display_name`; implement registry/policy admission, assignment coverage,
   non-reuse, pool membership and explicit role-fit override. `other` always needs an override unless
   a future pool entry explicitly lists it.
9. Implement all AIR-N01..N41 vectors with exact codes/paths and no partial graph/digest, then run
   focused MCP, registrar, compiler, provenance-contract and broad runtime regressions.

## Done criteria

- real pool is canonical v0.7 with 414 unique `agent_name` rows and no roster `name`/`agent-name`;
- all migrated consumers and tests pass in one worktree state;
- v1 resolves to exactly eight enabled roles and immutable digest; `other` passes, `others` fails;
- a future accepted registry revision requires config/authority/policy data, not source enum edits;
- existing telemetry rows remain byte-for-byte unchanged; new `0.7.0` opening/close pairs pin one
  identical registry ref and legacy/new mixing fails;
- default installer, route instructions and confirmation producer select v2/0.7.0 for new writes;
  explicit v1 selection can verify legacy data but cannot emit a new row;
- no active literal/selector found by `MIGRATION-SURFACE.md` remains unclassified or outside its
  declared migration/compatibility treatment;
- changing any assignment/ref without valid fresh evidence fails before graph bytes/digest;
- final names are Popper/Dijkstra/Lamport from assignments and roles are skeptic/coder/auditor;
- an independent reviewer returns `KEEP`; no worker self-approves.
