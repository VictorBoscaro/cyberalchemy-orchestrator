# Glossary consistency

- **Terminal response**: exact bytes observed by the host when a bound producer turn completes.
- **Artifact**: immutable content-addressed persistence of response bytes; identical bytes may be shared.
- **HostTerminalResponseArtifact**: immutable producer-turn evidence referencing the payload artifact.
- **HostTerminalResponseReceipt**: authoritative binding between producer-turn evidence and exact payload bytes.
- **SourceToSlotMapping**: confirmation-frozen authorization from one completed producer to one required L0 consumer slot.
- **Connection**: topology relation only; not inherently a data dependency or visibility grant.
- **Slot mapping**: pre-confirmed rule that names which accepted source populates a consumer slot.
- **WorkflowInputManifest**: ordered materialized slots and source digests for one consumer turn.
- **binding-output**: bounded Stage F source kind backed only by a valid terminal-response receipt.

No term above promotes Stage F evidence to provider-complete `EffectiveInputArtifact`, and no term redefines general workflow-graph semantics.
