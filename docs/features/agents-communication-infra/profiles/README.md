# Stage-A protocol profile registry

These four profile definitions are the complete dependency set for the bounded
`SWU-ACI-APT-VS-001` slice:

1. `aci.atomic-command-receipt-accepted-prefix-read-grouping@1`
2. `aci.transactional-semantic-uniqueness-result-mapping@1`
3. `aci.event-schema-canonicalizer-registry@1`
4. `apt.reference-probe-lineage@1`

Registration normatively imports the exact APT-owned request artifacts listed by repository path,
raw SHA-256 and `aci-cjson-1` canonical SHA-256 in the digest-bound
[registry manifest](../reviews/2026-07-23-stage-a-freeze/profile-registry-manifest.json) and
independent reviewer receipt. The files in this directory are non-authoritative review mirrors:
their parsed canonical projections must equal the imported APT artifacts, but they cannot replace,
summarize or weaken them. Registration therefore inherits every rule in the imported bytes,
including accepted-prefix rollback and complete-group reads, exact semantic collision mapping,
per-event schema/canonicalizer bindings, and probe recommendation lineage limits. A definition with
a different imported path, raw digest, canonical digest, version, command/event set or invariant is
a different profile and fails exact binding.

`aci-cjson-1` means compact JSON with recursively lexicographic object keys, array order preserved,
UTF-8, no insignificant whitespace and SHA-256 rendered as `sha256:<64 lowercase hex>`.

The reference-probe profile is included because the frozen local-pilot outcome implements its full
candidate -> parent verification -> official message -> APT lineage path. If that implementation
is removed, this profile must be removed from the selected SWU and no probe-lineage claim may
remain.

These files authorize no implementation until the cross-workpack predicate and exact named-SWU
receipt pass.
