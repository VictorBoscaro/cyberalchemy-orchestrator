# APT Stage A Governance Packet

Stage A freezes the APT side of the proposed ACI integration. It authorizes no runtime mutation.
ACI remains the sole owner of migrations, canonical bytes, artifact finalization, journal writes,
aggregate heads, projection transactions and durable receipts.

## Packet

- `profiles/*.json`: four closed, versioned registration requests required by APT.
- `profile-digests.sha256`: byte digests of the frozen requests.
- `contract-digests.sha256`: byte digests of event/canonicalizer schemas and the artifact policy.
- `evidence-digests.sha256`: byte digests of the review inputs and pending receipt template.
- `storage-artifact-policy-review.md`: bounded policy packet awaiting independent review.
- `SWU-ACI-APT-VS-001.md`: exact vertical-slice commands, events, endpoints, projections and tests.
- `mutation-gate-change-proposal.md`: owner change proposal; it is not an approval.
- `receipts/mutation-gate-post-change-review.pending.md`: independent post-change receipt template.
- TASK-105 accepted evidence lives at
  `../../session-evidence/TASK-105/acceptance-receipt.md`.

## Status

`documentation_ready_for_independent_review`. Profile contracts are frozen on the APT side, but
their ACI registrations and receipts remain pending. The storage policy and mutation-gate change
also remain pending independent review. Consequently `mutationGateStatus` remains `block`.
