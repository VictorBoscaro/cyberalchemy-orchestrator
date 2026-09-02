# Identity and role field consumers

Status: worker traceability evidence; independent review pending.

| Field | Authoritative producer | Enforcing consumer | Durable use |
|---|---|---|---|
| `agent_name` | canonical v0.7 pool row | strict Python pool loader and MCP pool loader | source value from which allocation obtains a human-readable identity |
| `display_name` | trusted allocator assignment, copied from one admitted pool `agent_name` | DraftGraph compiler coverage/membership/non-reuse gate | emitted node assignment and projected execution identity; never authored by DraftGraph |
| `role` | DraftGraph node | accepted role registry plus compiler role-fit/override policy; appender validates telemetry agent roles from the same registry | responsibility of a node/telemetry agent, independent of its display name |
| `role_fit` | canonical pool row | pool loader and compiler assignment admission | declares roles for which one pool identity is eligible; `other` needs explicit override unless listed |
| `agent_role_registry_ref` | dispatch registry v2 / signed compilation context | appender, host hook, strict open-close resolver, bridge, service and provenance projection | pins the exact vocabulary used by a 0.7.0 opening, close, confirmation effect/request or compilation |
| `agent_pool_ref` | pool authority and signed compilation context | allocator-context gate and compiler | pins the normalized pool from which assignments may be selected |
| `agent_assignments[].node_key` | trusted allocator context | compiler exact-coverage gate | joins one allocator assignment to exactly one DraftGraph node |
| `agent_assignments[].display_name` | trusted allocator context | compiler pool-membership/non-reuse/role-fit gate | selects the final identity without granting DraftGraph authority over names |
| `agent_assignments[].role_fit_override` | trusted allocator context | compiler override-policy gate | carries explicit evidence when selected identity does not list the node role |
| `agent-role-registry-selection.json` paths/ref | repository package configuration | Python loader, appender, MCP and installer | selects a versioned registry, authority and host-routing sibling without source-code filename changes; unknown/unpinned selections fail closed |

No alternate `agent-name`, legacy pool-row `name`, DraftGraph `display_name`, plural role `others`,
or unreferenced identity key is accepted on the current path. Existing 0.6.x telemetry remains
historical input to the explicit legacy resolver and is never rewritten as 0.7.0.
