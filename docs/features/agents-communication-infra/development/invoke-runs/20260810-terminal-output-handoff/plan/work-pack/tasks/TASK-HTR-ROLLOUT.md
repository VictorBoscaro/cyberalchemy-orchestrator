# TASK-HTR-ROLLOUT — Research topology pilot

This task is roadmap-only until L2 is re-specified, implemented and proven.

## SWU-ACI-HTR-005 — Research pilot

- Layer/slice/wave: L3 / S-004 / W3.
- Primary behavior: execute and close the already-confirmed artifact-schema landscape research dispatch through explorers, reviewers and synthesis.
- Independent boundary: one governed research dispatch produces `research.md` and `findings.md` with complete lifecycle receipts.
- Split analysis: compile/open/launch/advance/close form one research-dispatch transaction; the separate `$review` has its own dispatch and artifact, so it is HTR-006.
- Dependencies: HTR-004 and a still-valid frozen proposal/route.
- Source anchors: `.codex/workflow-inputs/2026-08-16-artifact-schema-governance-landscape/opening-proposal.json`; research/review skill contracts.
- Write scope: `projects/schema-service/research/artifact-schema-governance-landscape/research.md`, `findings.md`, and dispatch-owned lifecycle evidence only; no runtime source edits.
- Procedure: compile roots; open parent once; launch exact bound prompts; after each group join call host list capture, advance, and launch newly ready seats; close only after all declared seats terminal; run required review over the synthesized artifact.
- Edge cases: missing seat, agent failure, capture omission, route drift, duplicate advance, review blocker.
- Done: ledger/open/terminal/handoff/stage/close receipts reconcile; `research.md` and `findings.md` exist; no bridge stdout is stored in working_folder.
- Validation: dispatch validator, runtime log reconciliation and research evidence checks.
- Execution owner: parent coordinator with governed subagents.
- Handoff: stop on any failed capture; a passing research receipt makes HTR-006 eligible but does not select it.

## SWU-ACI-HTR-006 — Independent review dispatch

- Primary behavior: invoke `$review` over `findings.md` after the research dispatch is closed, producing `review.md` and its own close receipt.
- Independent boundary: review can pass/block without reopening or mutating the research dispatch.
- Split analysis: one review dispatch, one target artifact and one verdict are atomic; research generation is HTR-005.
- Dependencies: passing HTR-005 owner receipt.
- Write scope: `projects/schema-service/research/artifact-schema-governance-landscape/review.md` and review-owned lifecycle evidence.
- Done: review receipt reconciles and `review.md` states actionable findings or pass.
- Validation: review contract plus dispatch log reconciliation.
- Execution owner: parent coordinator with `$review` governed subagents.
- Handoff: acceptance-critical findings block final closure status and route to a new plan/repair.

## TASK-VERIFY exemption

Closure-only verification has no mutation SWU. It runs the full runtime suite, compileall, source-manifest verification, `git diff --check`, scoped diff review, and records whether the research dispatch may resume.
