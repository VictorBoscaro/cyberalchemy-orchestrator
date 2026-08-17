# TASK-HTR-CAPTURE — Host-owned terminal response evidence

## Objective and mapping

Implement L0 only after proving the host payload: preflight the real Codex hook result, commit exact response bytes in the runtime, then adapt the proven field. Slice S-001, wave W0.

## SWU-ACI-HTR-000 — Host payload preflight

- Primary behavior: establish whether real `PostToolUse.tool_response` exposes one canonical, complete, untruncated terminal response field with unambiguous producer correlation.
- Independent boundary: produces a signed/hashable probe receipt without changing runtime source.
- Split analysis: payload capture plus Unicode/newline/limit/ambiguity fixtures answer one admission question; runtime commit is independently HTR-001.
- Dependencies: Codex CLI 0.146 and a disposable governed probe agent.
- Source anchors: actual Codex hook event and `collaboration.list_agents` response contract.
- Write scope: `plan/session-evidence/SWU-ACI-HTR-000/host-payload-preflight.json` only.
- Method: capture the actual hook payload through an isolated probe; record Codex version, event/tool names, exact field selector, UTF-8 byte digest/size and completeness observations; exercise Unicode, preserved newlines, large output, unknown schema, ambiguity and truncation behavior.
- Done: the receipt proves one deterministic byte extraction rule and correlation rule, or records a blocker. A blocker retains the compiler fence and stops before HTR-001.
- Validation: independent replay of the captured fixture and negative cases.
- Execution owner: `task-session` in execute mode using an isolated disposable probe; no runtime mutation.
- Handoff: never substitute rollout scraping or agent-declared files.

## SWU-ACI-HTR-001 — Runtime byte commit

- Primary behavior: atomically bind exact in-memory response bytes to one completed host workflow turn and immutable artifact.
- Independent boundary: direct service tests pass without any host hook.
- Split analysis: artifact persistence and terminal transition cannot be split because exposing either alone violates atomic acceptance; Codex extraction is independent and therefore HTR-002.
- Dependencies: accepted D1/D2 and current binding service.
- Source anchors: `operations.md#commithostterminalresponse`; `service.py::complete_host_workflow_turn`.
- Write scope: `implementations/server/runtime/service.py`, focused host-workflow tests, Stage-E source manifest and pinned digest constant if required.
- Algorithm: accept bytes only from a host adapter parameter; compute SHA-256/size; finalize content-addressed bytes; atomically accept evidence plus terminal transition; return an idempotent terminal-response receipt; reject path substitution and divergent retries.
- Edge cases: non-bytes, empty/oversized response policy, wrong binding/agent, non-resolved outcome, duplicate equal/different bytes, storage failure.
- Done: TOH-001 and receipt-level identical/divergent retry tests pass; path input cannot create a terminal-response receipt.
- Validation: focused service/binding and abuse tests, compileall, manifest verification.
- Execution owner: subagent or local fallback.
- Handoff: use only the named source anchors; return the standard SWU receipt.

## SWU-ACI-HTR-002 — Codex host capture

- Primary behavior: close a bound Codex seat from the exact completed text selector proven by HTR-000.
- Independent boundary: hook tests and a live smoke prove extraction/correlation before any staged compiler work.
- Split analysis: matcher, extraction, correlation and delayed close form one security boundary; separating them would create an accepting partial adapter.
- Dependencies: passing HTR-000 and HTR-001 receipts.
- Source anchors: `.codex/hooks.json`; `host_dispatch_hook.py::{post_tool_use,subagent_stop,_close_state}`; actual Codex 0.146 `list_agents` result.
- Write scope: `.codex/hooks.json`, `implementations/server/runtime/host_dispatch_hook.py`, `implementations/tests/runtime/test_host_dispatch_hook.py`, Stage-E source manifest and pinned digest constant if required.
- Algorithm: SubagentStop marks a bound seat awaiting output; PostToolUse for the host list result matches one stored canonical task name and completed payload, encodes its exact string as UTF-8, calls HTR-001, and closes once; ambiguity/omission/failure remains blocked.
- Edge cases: duplicate names, running status, completed empty output, multiple completed agents, truncated/malformed result, repeated list, SubagentStop before/after list, session end.
- Done: synthetic and live-host proofs show exact bytes, one close, idempotent replay, and no caller-authored fallback.
- Validation: hook suite plus a fresh-session live capture receipt.
- Execution owner: subagent with parent-run live smoke.
- Handoff: do not scrape rollout files; return exact test and smoke evidence.

## Synchronization

HTR-001 cannot be selected until HTR-000 passes. HTR-002 waits for HTR-001. Runtime task completion requires HTR-001 and HTR-002; each closes independently through the shared Closeout Contract.
