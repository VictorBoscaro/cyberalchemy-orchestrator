# Owner Mutation-Gate Change Proposal

- Proposal status: `applied-and-independently-reviewed`
- Current authoritative value: `mutationGateStatus=pass-for-exact-swu`
- Applied value: `mutationGateStatus=pass-for-exact-swu`
- Owner action: completed by `@victor` on 2026-07-23
- Independent post-change review: `PASS`, receipt
  `receipts/mutation-gate-post-change-review.md`

The owner may apply the proposed value only when the digest-bound TASK-105 acceptance receipt, all
four ACI registration receipts, the storage/artifact policy PASS receipt and this exact change's
independent documentation receipt are present and mutually consistent.

No conditional or partial PASS is permitted. A placeholder digest, pending receipt, wrong profile
version, superseded TASK-105 digest, or storage-policy objection keeps the value `block`.

When eligible, the owner change must update the root work-pack gate, TASK-110 entry evidence, W3
entry evidence and blocker table in one documentation change. The independent reviewer then hashes
that exact post-change corpus, records `PASS` or `FIX`, and does not mutate the reviewed files.

The applied decision authorizes mutation only inside the exact `SWU-ACI-APT-VS-001` descriptor.
Local serving, production, provider execution, audit materialization and cutover remain blocked.
