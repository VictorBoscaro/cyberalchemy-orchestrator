# Compilation contract delta

Status: `repaired-candidate`; apply after
`../SPEC-ACI-DRAFT-GRAPH-001/COMPILATION-CONTRACT.md`. This delta wins on identity and role.

```text
compile(verified_compilation_context, draft, policy, catalog, resources,
        accepted_role_registry, normalized_agent_pool) -> ExecutionGraph | typed error
```

YAML I/O and v0.6→v0.7 migration are outside the pure compiler. The compiler receives closed,
immutable values only.

## Pool boundary

The source adapter parses exactly two YAML documents with duplicate-key rejection. It preserves the
real metadata document and the complete roster row shape. Canonical v0.7 accepts only
`agent_name`; exact Unicode source text becomes `display_name`. The one-time legacy migrator is
enabled only for the authority-pinned v0.6 bytes. It changes the identity key plus the three
declared metadata values (`version`, `last_updated`, prepended migration note) and proves all other
row data/order equal before emitting a candidate. Production v0.7 loading contains no `name` alias.

## Ordered gate

1. Reject duplicate JSON/YAML keys and closed-schema failures with a schema code and exact path.
2. Resolve `(role_registry.name, version)` through trusted authority; reject untrusted revision,
   missing/duplicate/disabled/extra roles, then verify the immutable digest.
3. Strictly normalize the canonical two-document pool; reject topology, identity, metadata and
   role-fit failures before allocation.
4. Validate compilation-context and allocator-evidence schemas.
5. Recompute context digest. A changed assignment/ref under old evidence is
   `DG_IDENTITY_CONTEXT_TAMPERED`.
6. Verify Ed25519 signature through trusted `key_id`; reject forged signatures, consumed
   `evidence_id`, `is_latest=false`, and `pair_is_unbound=false` separately.
7. Recompute registry and normalized-pool refs; reject context drift.
8. Require exactly one unique assignment for every DraftGraph node, no extra node, no reused
   identity, and exact pool membership.
9. Admit DraftGraph role through registry and policy. Require a signed non-empty override reason
   iff the selected identity lacks that role in `role_fit`.
10. Emit `agent.display_name` from the assignment and `agent.role` from DraftGraph. Emit no bytes or
    digest after any failure.

## Role configuration and telemetry

Registry v1 contains exactly the owner-selected eight roles. The source-pool schema admits only the
shape of a role ID; semantic normalization resolves every `role_fit` value against the selected
registry. A future v2 is new bytes at a new version/digest and must be selected by configuration;
changing the v1 file is substitution. Shared consumers must load the selected accepted registry (or
a generated artifact pinned to it), so adding an accepted future role requires coordinated
authority/policy/configuration data but no pool-schema or consumer source enum edit.

New telemetry openings use `schema_version: 0.7.0` and pin the selected registry ref; their close
rows use the same schema version and exact ref. Legacy openings `0.6.1`–`0.6.4` and legacy closes
remain byte-for-byte under their old parser branch. The resolver must reject new rows without refs,
legacy rows with retrofitted requirements, mixed-version pairs and close/open ref mismatch. `other`
becomes registrar-valid only with this atomic migration; before that, status is stale/block.

## Typed failures

Structural errors use `*_SCHEMA_INVALID` with a path. Semantic failures retain distinct codes for
pool document count/order, name missing/type/empty/ambiguity, legacy/unknown keys, identity
duplicates, metadata/source drift, untrusted/substituted registry, registry member errors, context
tamper, invalid signature, replay, stale evidence, authority conflict, ref drift, assignment
coverage/reuse/membership, unknown role and role-fit override errors. The executable manifest pins
the exact code/path behavior.
