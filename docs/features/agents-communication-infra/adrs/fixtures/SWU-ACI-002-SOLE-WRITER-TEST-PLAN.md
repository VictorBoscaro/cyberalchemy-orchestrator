# SWU-ACI-002 sole-writer and compatibility test plan

This is a W0 test contract, not target-host evidence.

| ID | Test | Required result |
|---|---|---|
| `T-ACI-WRITER-001` | inventory every repository/deployed reference to `subagents-dispatch.yaml` | only the validated appender is a sanctioned writer |
| `T-ACI-WRITER-002` | direct Python/runtime open-for-write attempt | denied or detected; no bytes change |
| `T-ACI-WRITER-003` | alternate process invokes an unvalidated ledger write | denied by target-host controls |
| `T-ACI-WRITER-004` | legacy watcher and runtime ownership overlap | startup/cutover fails closed |
| `T-ACI-WRITER-005` | import/single-writer lint passes but ACL/process evidence is absent | bundle remains incomplete |
| `T-ACI-LEGACY-001` | strict well-formed opening resolves once | exact identity plus row-byte/semantic digests |
| `T-ACI-LEGACY-002` | duplicate opening, malformed row or duplicate top key | strict resolver rejects |
| `T-ACI-LEGACY-003` | lenient UI reader can display a row rejected by strict resolver | authorization remains rejected |
| `T-ACI-LEGACY-004` | same identity and identical normalized row | `verified` |
| `T-ACI-LEGACY-005` | same identity and divergent normalized row | `reconciliation_required` |
| `T-ACI-LEGACY-006` | complete link workflow | ledger byte hash unchanged |

TASK-020 must bind these results into a complete target-host `SoleWriterEvidenceBundle` containing
process identity, filesystem ACL, deployed writer inventory and negative bypass evidence before
materializer/cutover. W0 freezes only this schema, algorithm and test list.

