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

Only `@victor` may append a future mutation-gate decision after the exact predicate in
`../../WORK-PACK.md` is independently verified.
