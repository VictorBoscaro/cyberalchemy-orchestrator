# TASK-HTR-FANIN — Bounded complete DAG readiness

This task is roadmap-only until a new normative spec/design version authorizes L2.

## SWU-ACI-HTR-004A — Ordered complete fan-in

- Layer/slice/wave: L2 / S-003 / W2.
- Primary behavior: release a group only after every declared predecessor group and seat has an accepted terminal-response receipt, in canonical order, with one durable launch intent.
- Independent boundary: the research-shaped DAG passes entirely in deterministic tests without a live research run.
- Split analysis: group completeness, ordered slot construction and no-duplicate stage state jointly define one fan-in readiness predicate. Parent close authorization is independently testable and therefore HTR-004B.
- Dependencies: HTR-003.
- Source anchors: ACI mapping/materialization rules; current binding uniqueness; workflow-graph fan-in discovery only as non-authoritative context.
- Write scope: compiler/service readiness and their runtime tests, Stage-E manifest and pinned digest.
- Algorithm: evaluate complete declared predecessor sets; source receipts from terminal command receipts; order by predecessor declaration then seat index; persist stage identities; reject partial/non-success/tampered inputs.
- Edge cases: 3-seat partial group, two-predecessor partial fan-in, independent branches, retry, stale opening/route, failed/cancelled upstream, never-launched downstream.
- Done: 3→3→1 fixture advances 3, then 3, then 1 with two synthesis connection slots containing all six seat receipts and zero duplicate launches.
- Validation: compiler, bootstrap, abuse, binding and hook regression matrix.
- Execution owner: subagent or local fallback.
- Handoff: no cycles, conditional branches, close authorization or degraded-success policy.

## SWU-ACI-HTR-004B — Declared-seat close gate

- Primary behavior: authorize parent close only when every seat declared by the frozen opening record has one allowed terminal binding state, including groups that were initially unlaunched.
- Independent boundary: close tests pass without changing fan-in materialization.
- Split analysis: declared-seat accounting and close decision are one gate; launch/readiness remains HTR-004A.
- Dependencies: normative L2 revalidation and HTR-004A.
- Write scope: runtime close service/hook and focused close tests, Stage-E manifest and pinned digest.
- Algorithm: compare frozen declared `(group,seat,turn)` inventory against bindings; reject missing/running/unauthorized terminal outcomes; accept once idempotently only after complete accounting.
- Done: early close after roots/reviewers blocks; complete graph closes once; retry is identical.
- Validation: close-gate positive/negative/replay tests.
- Execution owner: subagent or local fallback.
- Handoff: non-success completion policy must come from the new normative version.
