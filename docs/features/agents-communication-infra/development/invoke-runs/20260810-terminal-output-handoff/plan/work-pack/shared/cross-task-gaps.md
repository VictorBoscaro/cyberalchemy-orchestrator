# Cross-task gaps

| Gap | Severity | Owner | Repair/stop rule |
| --- | --- | --- | --- |
| Live Codex hook payload may omit, normalize or truncate completed text. | blocker before runtime mutation | `SWU-ACI-HTR-000` | Capture actual payload; fail W0 and retain fence on any uncertainty. |
| Host result may not expose an unambiguous agent identifier with the output. | blocker before runtime mutation | `SWU-ACI-HTR-000` | Prove exact correlation or block. |
| Fan-in and full topology exceed the accepted L0/L1 design version. | normative blocker | ACI design owner | Re-specify and revalidate before HTR-004A/B enter the frontier. |
| Current close checks only already-bound turns. | L2 roadmap gap | `SWU-ACI-HTR-004B` | Compare declared seats with terminal bindings before parent close. |
| Current confirmed research record cannot compile roots without future receipts. | known lifecycle defect | `SWU-ACI-HTR-003/004` | Stage compile/materialize/advance from durable facts. |
