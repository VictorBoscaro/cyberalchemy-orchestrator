# Stage-A protocol profile registry

These four profile definitions are the complete dependency set for the bounded
`SWU-ACI-APT-VS-001` slice:

1. `aci.atomic-command-receipt-accepted-prefix-read-grouping@1`
2. `aci.transactional-semantic-uniqueness-result-mapping@1`
3. `aci.event-schema-canonicalizer-registry@1`
4. `apt.reference-probe-lineage@1`

Registration requires canonical compact JSON with recursively lexicographic object keys, array
order preserved, UTF-8, no insignificant whitespace and SHA-256 rendered as
`sha256:<64 lowercase hex>`. The digest-bound
[registry manifest](../reviews/2026-07-23-stage-a-freeze/profile-registry-manifest.json) and
independent reviewer receipt are the registration evidence. A definition with a different byte
projection, version, digest, command/event set or invariant is a different profile and fails exact
binding.

The reference-probe profile is included because the frozen local-pilot outcome implements its full
candidate -> parent verification -> official message -> APT lineage path. If that implementation
is removed, this profile must be removed from the selected SWU and no probe-lineage claim may
remain.

These files authorize no implementation until the cross-workpack predicate and exact named-SWU
receipt pass.
