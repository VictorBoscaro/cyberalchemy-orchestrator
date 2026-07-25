# Agent identity and tool-access findings

Dispatch: `2026-07-24-agent-identity-tool-access-research`  
Proposal: `agent-identity-tools-concrete-r1`  
Proposal digest: `sha256:af68d5d06b986a06456318c8fa16d241243c6652c415551b0f4ce29294920a94`  
Final approver: parent

## One-line answer

The existing agent-pool MCP, wrapper, ledger, ACI capability-resolution seam, effective-input
artifact, and Scout lifecycle are reusable, but the proposal JSON is not executable configuration
today. Implement one identity-selection/binding pipeline and one parent-bounded tool-profile
compiler before treating it as such.

## Verdict matrix

| Candidate | Owner | Witnessed? | Sound? | Verdict | Use mode |
|---|---|---:|---:|---|---|
| Canonical pool names | `telemetry/agents/agent-pool.yaml` | yes, 414 entries | yes | GO | already-deployed source of truth |
| Agent-name recommendation | `tools/agent-pool-mcp` | yes, smoke passes over 414 entries/721 tags | yes, output is recommendation only | GO | build-from-owned |
| Durable `AgentSelectionReceipt` | no current owner | no runtime record exists | proposed shape separates evidence from authority | GO | novel-attempt |
| Persona input binding | ACI `EffectiveInputArtifact` is the owning seam | current wrapper passes prompt unchanged | sound if exact provider-visible bytes are hashed | GO | build-from-owned |
| Runtime agent instance | ACI `Seat.agent_instance_id` is the owning seam | draft field exists; wrapper has only later provider ID | sound with explicit mapping event | GO | build-from-owned |
| Parent Dispatch lineage | register schema has optional `parent_dispatch_id` | current hook omits it | sound only when runtime-derived | GO | build-from-owned |
| Requested tool profile | delegated-supervision discovery | proposal-only | sound as non-authoritative request | GO | build-from-owned |
| Confirmed capability resolution | ACI `DispatchSpec`/confirmation | draft authority seam exists | sound as sole grant authority | GO | build-from-owned |
| Effective `AgentToolProfile` | `AgentInvocationPlan.tool_profile_ref` candidate seam | schema/compiler absent | sound if deterministic and attempt-bound | GO | build-from-owned |
| Default Scout access | Stage G typed Scout lifecycle | Scout is operational but not automatically injected | sound as a request default before parent intersection | GO | build-from-owned |
| Orchestrator dispatch access | strategy plus governed dispatch gateway | no compiled profile exists | sound only as an explicit agent kind | GO | build-from-owned |

No candidate is killed for non-vacuity or definitional collapse.

## Identity contract

These fields must remain distinct:

| Field | Contract |
|---|---|
| `agent_name` | Required exact canonical pool persona for every dispatched reasoning agent. Descriptive, non-authenticating, and reusable across Dispatches. |
| `task_name` | Operational routing label. It never substitutes for `agent_name`. |
| `agent_instance_id` | Runtime-issued immutable execution identity. |
| `provider_agent_id` | Later provider observation mapped to `agent_instance_id`; never authority. |
| `parent_dispatch_id` | Runtime-derived immutable edge to the immediate invoking Dispatch; null only for a root launch. |
| `selection_receipt_ref/digest` | Immutable evidence of pool snapshot, query, candidate set, chosen name, entry digest, selector version, and authenticated selector principal. |
| `persona_input_ref/digest` | Exact persona bytes actually presented to the model as part of the effective input. |
| `tool_profile_ref/digest` | Effective per-attempt authority derived from the single confirmed capability resolution. |
| `typed_tool_identity` | Service/schema/principal identity for Scout or another tool; mutually exclusive with reasoning-agent identity. |

The current violation is executable: `host_dispatch_hook.py` prioritizes `task_name`, derives
`agent_name = _safe_part(label)`, copies the prompt unchanged, learns provider `agent_id` only
after launch, and does not set `parent_dispatch_id`. The formal Liskov launch therefore passed the
name to the model through prompt text while its compatibility child row still recorded the task
label.

## Minimal AgentSelectionReceipt

```json
{
  "schema_version": "aci.agent-selection-receipt/1",
  "selection_receipt_id": "sel_...",
  "selection_mode": "recommended|deterministic|manual-validated",
  "query_ref": "artifact-id",
  "query_digest": "sha256:...",
  "pool_ref": "telemetry/agents/agent-pool.yaml",
  "pool_digest": "sha256:...",
  "selector_ref": "agent-pool-mcp@version",
  "selector_digest": "sha256:...",
  "candidate_names": ["..."],
  "selected_agent_name": "Liskov, Barbara",
  "selected_entry_digest": "sha256:...",
  "selected_by_principal": "authenticated principal",
  "receipt_digest": "sha256:..."
}
```

The MCP remains a recommender. A runtime/application command validates and freezes the final
selection; neither an LLM rationale nor a recommendation response authorizes launch.

## Agent kinds and default tools

| Agent kind | Canonical name | Scout | Dispatch gateway | Strategy skill | May spawn |
|---|---:|---|---|---|---:|
| `reasoning` | required | default-on, explicitly removable | absent | absent | no |
| `orchestrator` | required | default-on | required | required and digest-pinned | yes, inside parent ceiling |
| `typed_tool:reference_scout` | forbidden | n/a | absent | absent | no |
| Scout-dispatched reasoning worker | required | reasoning default subject to parent ceiling | absent unless explicitly orchestrator | absent unless explicitly orchestrator | by kind |
| utility/tool service | forbidden | n/a | absent | absent | no |

Scout defaulting is convenience during request compilation, never ambient authority. Expanding
defaults occurs before intersection with the authenticated parent ceiling. If the parent lacks
Scout, the child cannot obtain it through a default.

## Three tool-authority layers

1. `RequestedLogicalToolProfile`: agent-kind template, required/optional tools, explicit removals,
   requested folder/source/network/process/skill scopes. It is non-authoritative.
2. `ConfirmedCapabilityResolution`: the only frozen Dispatch grant authority. It binds the parent
   ceiling, defaults/removals, provider/adapter support, enforcement state, and closed failures.
3. `AgentToolProfile`: deterministic per-attempt materialization referenced by
   `AgentInvocationPlan.tool_profile_ref`. It binds the attempt, provider, adapter, sandbox,
   effective scopes, and enforcement observations without adding authority.

## Compiler

```text
1. Authenticate the parent Dispatch; root uses an explicit host-owned ceiling.
2. Validate the identity branch:
   reasoning/orchestrator => canonical agent_name + selection/persona refs;
   typed tool => typed_tool_identity and no agent_name.
3. Expand agent-kind defaults.
4. Apply explicit removals; removing a required orchestrator tool rejects or changes kind.
5. Add declared required/optional tools and requested scopes.
6. Resolve provider/adapter/runtime compatibility and enforcement observability.
7. Intersect tools, skills, folders, sources, network, processes, credentials,
   budgets, deadline, and spawn depth with the authenticated parent ceiling.
8. Reject every escalation or unconfirmed degradation.
9. Persist one canonical ConfirmedCapabilityResolution.
10. Materialize attempt-bound AgentToolProfile deterministically.
11. Materialize provider-visible EffectiveInputArtifact, including persona and tool schemas.
12. Verify profile, effective input, sandbox evidence, parent head/revocation, and authority fence.
13. Seal and launch.
```

Required invariants:

```text
child.tools       ⊆ parent.tools
child.skills      ⊆ parent.skills
child.folders     ⊆ parent.folders
child.sources     ⊆ parent.sources
child.network     ⊆ parent.network
child.processes   ⊆ parent.processes
child.credentials ⊆ parent.credentials
child.budget      ≤ parent.remaining_budget
child.deadline    ≤ parent.deadline
child.spawn_depth < parent.spawn_depth
```

`can_spawn(child)` requires an orchestrator parent. Folder inclusion uses normalized resolved paths
and rejects symlink or traversal ambiguity. A directly known source remains accessible only when it
is inside the effective folder/source scope; Scout recommendation is not a grant.

## Implementation sequence

1. Introduce a new dispatch/identity schema version while keeping v0.6.1 history immutable and
   readable.
2. Add pool snapshot and per-entry digests to the MCP core.
3. Add `select_agent` or `validate_selection` to create `AgentSelectionReceipt`.
4. Make `agent_name` plus receipt mandatory for reasoning-agent seats and validate exact pool
   membership at the appender/runtime boundary.
5. Add the mutually exclusive `typed_tool_identity` branch.
6. Change the launcher/wrapper input to carry `agent_name` separately from `task_name`; remove
   `_safe_part(label)` as persona derivation.
7. Materialize and verify `persona_input_ref/digest` in the provider-visible effective input.
8. Create `agent_instance_id` before provider start; record provider ID as a later observation.
9. Derive `parent_dispatch_id` from authenticated invocation context.
10. Specify and implement `RequestedLogicalToolProfile`, `ConfirmedCapabilityResolution`
    additions, and `AgentToolProfile`.
11. Implement the parent-ceiling subset compiler and closed failure vocabulary.
12. Wire agent-kind profiles:
    - reasoning: Scout default-on;
    - orchestrator: Scout + governed dispatch gateway + pinned strategy;
    - typed Scout: no persona.
13. Add provider/sandbox conformance evidence and fail closed where required restrictions are
    non-observable.
14. Only then make a proposal-derived artifact eligible as executable dispatch configuration.

## Mandatory negative tests

- Missing/null/unknown/case-changed/sanitized canonical name.
- `task_name` substituted for `agent_name`.
- Pool or selected-entry digest drift.
- Recommendation used directly as launch authority.
- Correct selection receipt but missing or changed persona bytes.
- Caller-supplied `agent_instance_id`, provider mapping, or parent edge conflict.
- Nested launch with missing/self/sibling/closed parent.
- Typed Scout with persona name; Scout worker without one.
- Ordinary reasoning agent requests dispatch gateway/strategy.
- Child gains default Scout when the parent ceiling excludes it.
- Folder traversal, symlink escape, or direct source outside scope.
- Network/process/credential/budget/deadline/delegation-depth escalation.
- Required restriction cannot be observed by the adapter.
- Optional capability disappears without frozen degradation.
- Attempt tool profile or effective-input tool schemas drift from confirmed resolution.
- Parent capability is revoked between compilation and sealing.
- Old v0.6.1 records remain readable but cannot be upgraded in place.

## Open decisions

- Whether manual validated selection may choose a canonical name outside MCP recommendations.
  Recommended: yes, but only with exact pool membership and receipt evidence.
- Whether Scout removal is permitted for every reasoning agent or may be prohibited by a
  task/organization policy. Recommended: default removable unless the confirmed task marks it
  required.
- Whether delegation depth is a scalar, tree budget, or both. This needs a SPEC decision before
  nested orchestration becomes runtime-managed.
- Which component owns compilation/registry lifecycle for skill execution profiles remains
  OQ-ATD3; ACI must still own effective runtime authority.

## Evidence

- `research.md` contains the collected Liskov and Gray returns.
- Agent-pool MCP smoke: PASS, 414 entries, 721 tags.
- Capability review: Parnas, David — PASS after exact-corpus and contract amendments.
- Tension checks: Lampson, Butler — PASS; Brooks, Frederick P. — PASS.

Exit reason: `resolved`. Agents spawned: two formal explorers plus one bounded mapping helper and
three proposal-gate helpers; all source work was read-only.
