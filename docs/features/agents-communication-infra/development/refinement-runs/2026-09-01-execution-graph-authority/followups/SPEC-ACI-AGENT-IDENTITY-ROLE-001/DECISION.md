# Agent identity and role decision

Status: `owner-selected / repaired-candidate`; this follow-up supersedes only the identity, role and
consumer-migration dimensions of `SPEC-ACI-DRAFT-GRAPH-001`. Historical reviews remain unchanged.

## Normative decision

1. `DraftGraph.nodes[].agent_request` authors `role` and binding keys, never `display_name`.
2. The canonical governed pool is a two-document YAML stream: document 0 is metadata and document 1
   is `{scientists: [...]}`. Canonical pool version `0.7.0` uses only `scientists[].agent_name`.
   `agent-name` is not a second permanent alias.
3. The current real pool is the trusted legacy source only when its version is `0.6.0`, its 414-row
   topology and metadata match, and its raw digest is
   `sha256:5c7b9745a336670ecb55df1276912166954a0d7960443f0df787405564099eba`.
   A one-time versioned migration renames `name` to `agent_name`, preserves row order and every
   `field`, `era`, `role_fit`, `cited`, `tags` and optional `note`, and performs only the declared
   metadata changes. Steady-state v0.7 loading rejects `name`, `agent-name`, dual spellings, unknown
   keys, duplicate YAML keys, document count/order changes and metadata drift.
4. The loader projects canonical `agent_name` to normalized `display_name`. The allocator assigns
   one normalized identity per node. Registry ref, pool ref and assignments are inside the signed
   compilation context. The pure compiler emits final `display_name` only from that assignment.
5. Registry `aci.agent-roles/1` is exactly eight enabled roles, in its immutable bytes:
   `explorer | synthesizer | skeptic | writer | auditor | planner | coder | other`. A trusted
   authority maps `(name, version)` to the accepted digest. Missing, extra, duplicate or disabled
   rows and same-version byte substitution fail closed.
6. Pool schemas validate role IDs structurally (`^[a-z][a-z0-9_]{0,63}$`); only the exact pinned
   registry decides which IDs are admitted. A future role requires a new registry
   revision/version/digest, authority admission, policy and consumer configuration updates, and a
   newly signed compilation context, but no pool-schema enum edit. Version 1 is never edited in
   place. The appender, MCP boundary, compiler, UI contract and enum audit must resolve this pinned
   registry rather than embed role constants.
7. `role_fit` remains advisory. A mismatch, including an assignment using `other`, requires a
   signed `role_fit_override=true` and non-empty reason. `other` is a closed role, not arbitrary
   text and not silently added to every pool entry.
8. Existing append-only telemetry openings `0.6.1` through `0.6.4` and their unversioned legacy
   closes are never rewritten or reinterpreted. New openings use schema `0.7.0` and require
   `agent_role_registry_ref`; their closes also carry `schema_version: 0.7.0` and the identical ref.
   Mixed legacy/new pairs or mismatched refs fail closed. This requires a dispatch-type registry
   successor and coordinated host-hook, appender, strict resolver and downstream snapshot migration.
   Until that migration lands, `other` is specified but production-stale.

## Authority chain

| Value | Producer | Trust/check | Consumer |
|---|---|---|---|
| v0.6 pool bytes | governed repository | fixed raw + metadata digest | one-time migrator |
| v0.7 `agent_name` | governed pool migration/author | strict two-doc loader | normalized pool |
| normalized `display_name` | loader | pool digest + exact membership | allocator/compiler |
| node assignment | allocator | Ed25519 evidence over full context | compiler |
| DraftGraph `role` | LLM from intent | immutable registry + policy | compiler/registrar |
| role registry | governed configuration author | trusted `(name,version)->digest` | all shared role consumers |

## Evidence ceiling

The executable fixtures verify the real v0.6 source and simulate its lossless data migration, but
do not change that file. They cryptographically verify fixture Ed25519 evidence; they do not prove a
production key service. Production pool, consumers, registrar, compiler and telemetry remain
unchanged until the implementation work pack passes independent review.
