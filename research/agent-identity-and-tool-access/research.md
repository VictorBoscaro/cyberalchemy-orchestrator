# Collected research returns

Dispatch: `2026-07-24-agent-identity-tool-access-research`

The two formal returns below are preserved as the evidence basis used by `findings.md`.

## Liskov, Barbara — canonical identity and invocation data contract

Assigned canonical identity acknowledged: `Liskov, Barbara`.

The proposal JSON is not consumed as dispatch configuration. It is workflow-only approval evidence.
The parent manually maps a seat’s `task_name`, `prompt_template`, model, and budget into
`spawn_agent`; the mandatory hook observes that call but does not load the JSON or rewrite the
invocation. The strategy explicitly states that proposals are session-local projections, not
authorities or partial dispatch records.

All frozen source hashes matched. The allowed MCP smoke passed with 414 entries and 721 tags.

Current identity trace:

```text
agent-pool.yaml
  → MCP returns candidate/recommended canonical names
  → parent manually chooses one
  → parent manually writes name into prompt/proposal
  → spawn_agent receives task_name + unchanged prompt
  → hook derives label, then agent_name = _safe_part(label)
  → YAML/ACI opening occurs before provider agent_id exists
  → provider agent_id is observed afterward and retained only in hook state
```

The MCP validates recommended names against the pool, but returns recommendations rather than a
durable selection. Deterministic search returns candidate records
(`tools/agent-pool-mcp/src/select.mjs:39`); LLM recommendations return names and rationale
(`tools/agent-pool-mcp/src/adjudicate.mjs:70`). The canonical pool loader exposes entries, tags,
vocabulary, names, and an mtime cache (`tools/agent-pool-mcp/src/pool.mjs:23`).

Field-level findings:

- `agent_name`: the hook prioritizes `task_name`, `description`, or `name`, then applies
  `_safe_part` (`host_dispatch_hook.py:278-291`). Target: exact pool-validated canonical name for
  reasoning agents; typed tools use a separate identity.
- MCP result: recommendations are not durable authority. Target: an immutable
  `AgentSelectionReceipt`.
- Persona bytes: the wrapper copies prompt unchanged (`host_dispatch_hook.py:243,318`). Target:
  exact `persona_input_ref/digest` verified in `EffectiveInputArtifact`.
- `task_name`: routing only, never persona.
- `agent_instance_id`: ACI Seat expects it (`specs/domain.md:74`), but the hook does not create it.
- Provider `agent_id`: learned after launch and held only in hook state
  (`host_dispatch_hook.py:348,450`). Target: later mapping observation.
- ACI opening: binds Dispatch/Session/YAML but not name, instance, selection, persona, provider ID,
  or parent (`service.py:272,1132`).
- `parent_dispatch_id`: optional in the current ledger contract and absent from the host record
  (`append-dispatch.cjs:157`).
- Register `agent_name`: optional and only checked as a non-empty free string
  (`register-dispatch/SKILL.md:86`; `append-dispatch.cjs:209`).
- Existing ACI input separates role, task, and tool profile; preserve that separation
  (`specs/interfaces.md:210`).

Minimal receipt fields: schema/version, receipt ID, mode, query ref/digest, pool ref/digest,
selector ref/digest, candidates, selected canonical name, selected entry digest, authenticated
selector principal, and receipt digest. Manual selection is valid only as `manual-validated`.

Migration: new ledger/runtime schema, pool snapshot/entry digests, mandatory receipt/name for
reasoning agents, mutually exclusive typed-tool identity, persona bytes in effective input,
runtime instance before provider start, later provider mapping observation, authenticated immediate
parent edge, and old-row readability without in-place upgrade.

Negative tests include missing/unknown/sanitized names, task/persona substitution, pool drift,
selection outside candidates, recommendation as launch authority, missing persona bytes, persona
digest mismatch, caller-asserted runtime IDs, bad parent edges, typed Scout with a name, reasoning
Scout worker without one, and historical-row mutation.

Verdict: partially buildable from owned components. The pool, MCP, wrapper gate, ledger, artifacts,
and effective-input model are reusable; selection receipt, canonical validation, persona
materialization, runtime instance mapping, and nested lineage remain to implement.

## Gray, Jim — tool-profile compilation and non-escalation

Assigned canonical identity acknowledged: `Gray, Jim`.

Verdict: build from owned components, but do not claim the policy is operational. The corpus owns
the seams: logical tools are proposals; server confirmation freezes one capability resolution;
`AgentInvocationPlan.tool_profile_ref` points to per-attempt materialization; effective input
records presented tool contracts; launch validates sandbox and authority fence. Missing pieces are
the compiler, schema, provider enforcement evidence, and parent-child binding.

Three authority layers:

1. `RequestedLogicalToolProfile`: non-authoritative agent-kind/skill/user request with
   required/optional tools, removals, and requested scopes.
2. `ConfirmedCapabilityResolution`: single Dispatch authority, extended with authenticated parent
   ceiling, defaults/removals, support, enforcement, and closed rejection reasons.
3. `AgentToolProfile`: deterministic attempt-bound effective representation derived from the
   confirmed resolution and verified against effective input.

Agent kinds:

- `reasoning`: canonical name required; Scout default-on/removable; no dispatch capability.
- `orchestrator`: canonical name required; Scout plus governed dispatch gateway and digest-pinned
  strategy; may spawn inside the parent ceiling.
- `typed_tool:reference_scout`: canonical name forbidden; typed identity required.
- Scout-dispatched reasoning worker: canonical name required; ordinary reasoning defaults.
- Utility service: typed identity, no persona, no spawn.

Required fields include `agent_kind`, requested/removed tools, runtime-derived
`parent_dispatch_id`, immutable `parent_ceiling_ref/digest`, `tool_profile_ref/digest`, normalized
folder/source scopes, exact network/process/credential grants, digest-pinned skill refs,
per-dimension enforcement evidence, and `typed_tool_identity`.

Compiler:

```text
1. Authenticate parent and load its effective ceiling.
2. Validate reasoning versus typed-tool identity.
3. Expand kind defaults.
4. Apply explicit removals.
5. Add declared required/optional tools and scopes.
6. Resolve provider/adapter/runtime/policy compatibility.
7. Intersect every dimension with the authenticated parent ceiling.
8. Persist one ConfirmedCapabilityResolution.
9. Materialize AgentToolProfile deterministically per attempt.
10. Materialize provider input and tool schemas in EffectiveInputArtifact.
11. Verify resolution/profile/input/sandbox/parent-head bindings.
12. Seal and launch.
```

Every child dimension is a subset of the parent dimension; budget/deadline/depth can only narrow.
An agent may spawn only when it is an orchestrator. Default Scout expansion happens before parent
intersection, so a parent without Scout cannot produce a child with Scout. Normalized path and
symlink checks enforce folder scopes, and direct source access cannot bypass them.

Closed failures include missing/forbidden identity, bad kind, missing/stale/revoked parent ceiling,
unauthorized/deep delegation, tool/skill/folder/source/network/process/credential/budget
escalation, missing required capabilities, unobservable required restrictions, unconfirmed
optional degradation, digest mismatch, semantic drift, effective-input mismatch, sandbox mismatch,
and missing identity for a reasoning worker behind a typed tool.

Required tests include ordinary child requesting orchestration, unnamed orchestrator, named Scout
tool, unnamed Scout worker, default Scout escalation, path/symlink escape, direct source outside
scope, every grant/budget/depth escalation, unobservable required restriction, silent optional
degradation, attempt/profile drift, effective-input tool mismatch, changed retry digest, parent
revocation race, task-name persona substitution, and caller-asserted parent conflict.

Central design choice: defaults are request-compilation convenience, never ambient authority.
