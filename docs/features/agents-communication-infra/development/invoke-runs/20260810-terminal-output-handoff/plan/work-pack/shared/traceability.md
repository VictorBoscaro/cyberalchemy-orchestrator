# Traceability

| Obligation | Units | Evidence |
| --- | --- | --- |
| Host payload canonicality prerequisite | HTR-000 | actual PostToolUse payload receipt and byte fixtures |
| TOH-001 exact response receipt | HTR-001, HTR-002 | service receipt plus live-host capture tests |
| TOH-002 reject arbitrary paths | HTR-001, HTR-002, HTR-003 | commit, adapter and launch-gate abuse tests |
| TOH-003 terminal without artifact blocks | HTR-002, HTR-003 | hook/compiler tests |
| TOH-004 digest/size drift fails | HTR-003, HTR-004A | downstream verification abuse tests |
| TOH-005 identical retry is idempotent | HTR-001, HTR-003 | receipt and binding/launch replay tests |
| TOH-006 restart publishes once | HTR-003 | staged replay tests |
| TOH-007 all required slots before launch | HTR-003, HTR-004A | readiness/fan-in tests |
| TOH-008 exactly one launch intent | HTR-003 | 1→1 integration test |
| Research 3→3→1 topology | HTR-004A/B, HTR-005 | live research receipts |
| Required independent review | HTR-006 | review dispatch receipt and `review.md` |
