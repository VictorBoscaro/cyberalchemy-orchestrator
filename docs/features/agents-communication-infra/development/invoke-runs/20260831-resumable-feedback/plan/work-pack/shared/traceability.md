# Traceability

| Test obligation | Primary SWU | Contract |
|---|---|---|
| T-ACI-CONT1 | TASK-CONT-001 | Suspension and preallocated identity |
| T-ACI-CONT2 | TASK-CONT-002 | Journal-derived eligibility |
| T-ACI-CONT3 | TASK-CONT-002 | Exact official contribution materialization |
| T-ACI-CONT4 | TASK-CONT-002 | Same-session identity/new attempt |
| T-ACI-CONT5 | TASK-CONT-003 | Definitive-loss reconstruction |
| T-ACI-CONT6 | TASK-CONT-003 | Unknown is not unavailable |
| T-ACI-CONT7 | TASK-CONT-003 | Cancel/expire/resume race |
| T-ACI-CONT8 | TASK-CONT-002 then 003 | Atomicity and replay |
| T-ACI-CONT9 | TASK-CONT-001 then 003 | Invalid transition matrix |

Every SWU must preserve the existing runtime suite and append its accepted evidence here before its
task status changes to completed.

| Continuation invariant | Owning SWU |
|---|---|
| CONT-I1 — suspended means no active target attempt | TASK-CONT-001 |
| CONT-I2 — eligibility derives from complete slots/heads | TASK-CONT-002 |
| CONT-I3 — same-session still has exact effective input | TASK-CONT-002 |
| CONT-I4 — definitive loss differs from unknown | TASK-CONT-003 |
| CONT-I5 — at most one continuation terminal | TASK-CONT-003 |
| CONT-I6 — reconstruction preserves seat/replaces instance | TASK-CONT-003 |
| CONT-I7 — claimed abandoned target terminalizes before replacement | TASK-CONT-003 |
