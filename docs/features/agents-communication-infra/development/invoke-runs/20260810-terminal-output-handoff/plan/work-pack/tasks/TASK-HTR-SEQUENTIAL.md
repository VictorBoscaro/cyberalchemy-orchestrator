# TASK-HTR-SEQUENTIAL — One producer to one consumer

## SWU-ACI-HTR-003

- Layer/slice/wave: L1 / S-002 / W1.
- Primary behavior: compile roots, materialize one authenticated handoff after producer completion, and emit one downstream launch intent exactly once.
- Independent boundary: a 1→1 topology passes restart/replay tests without fan-in.
- Split analysis: read-port, handoff materialization and stage emission are one end-to-end readiness transition; each alone cannot authorize the consumer. Fan-in remains HTR-004.
- Dependencies: HTR-001 and HTR-002 receipts.
- Source anchors: `dispatch_workflow.py::{_handoff_receipt,compile_bound_launch_plan}`; terminal command receipt validation in `service.py`.
- Write scope: `dispatch_workflow.py`, narrow service read port if required, dispatch/compiler/bootstrap tests, Stage-E manifest and pinned digest.
- Algorithm: compile only indegree-zero groups; query accepted terminal receipts from SQLite; verify opening/route digests; write-once-or-verify-identical handoff and stage plan; exclude already-bound seats; unlock exactly one successor when its single prerequisite is complete.
- Edge cases: partial producer, resolved without output, error/cancel, route drift, handoff tamper, repeated advance, crash between materialization and bind.
- Done: TOH-006–008 pass and connectionless compilation remains compatible.
- Validation: focused compiler/bootstrap/abuse suites and replay test.
- Execution owner: subagent or local fallback.
- Handoff: preserve the connected-topology fence outside the proven 1→1 shape.
