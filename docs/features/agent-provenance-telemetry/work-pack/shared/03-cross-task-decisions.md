# Cross-Task Decisions

| Decision | Status | Consequence |
|---|---|---|
| Node 22 + TypeScript under `tools/agent-provenance-telemetry/` | selected | Align with workspace tooling. |
| Separate construction, integration and enablement gates | selected | Pure tests cannot lift later gates. |
| Inject canonicalization; never invent authoritative bytes/digests | selected | L0 produces candidates only. |
| Test doubles stay in test paths and are not exported | selected | No accidental runtime authority. |
| TASK-105 pure L0 accepted after final review | selected | 27/27 bounded cases, typecheck and contract vectors support construction only. |
| Stage A APT integration packet uses one ACI writer and disposable projections | selected-for-review | No APT SQL connection, migration authority or direct artifact finalization. |
| Final answer bytes exist only in the protected ACI artifact BLOB | selected-for-review | Events, APT projections, receipts, logs, SSE and errors carry refs/digests only. |
| Owner authorizes the exact `SWU-ACI-APT-VS-001` mutation-test scope | selected | Stage-A APT review passed cycle 2/5 and ACI/TASK-000/W0 review passed cycle 5/5; code, migrations and tests may proceed only inside the frozen descriptor. Local serve and production/cutover remain blocked. |

`@victor` recorded the exact-SWU mutation decision on 2026-07-23 after the predicate in
`../../WORK-PACK.md` passed independent review. The change remains non-operative until its
post-change digest receipt is independently issued.
