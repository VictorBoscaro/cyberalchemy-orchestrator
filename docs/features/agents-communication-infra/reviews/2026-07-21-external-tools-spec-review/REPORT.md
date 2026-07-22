---
feature: agents-communication-infra
review_date: 2026-07-21
final_review_set_sha256: 4ef43958a3df420ece44fd413ce710e4d32753cb01e19dfa4f979f52c3dba4a4
final_verdict: PASS
runtime_gate: block
---

# External Tool Adoption SPEC Review Report

Three independent reviewers evaluated authority/architecture, formal DomainSpec traceability and
delivery/security. The initial baseline returned `FIX/FIX/FIX`; all accepted findings were
remediated. The final closure baseline returned `PASS/PASS/PASS`.

Resolved findings:

- external tests moved to unique `T-ACI-ETA1`–`ETA5` identities and complete indexing;
- discovery Policy meta-types preserved through registry and glossary;
- glossary CommonMark table repaired;
- architecture now routes provider start through `SandboxLauncher`;
- B-003 split into W0 contract freeze versus TASK-020 target-host proof, removing the dependency
  cycle while retaining the materializer/cutover block;
- real-provider sandbox evidence aligned to S-003/L2/W3.

The approved implementation boundary is W0 documentation only. `SWU-ACI-001` may create the
persistence/replay ADR, canonical serialization policy and golden vectors. Runtime code remains
blocked.
