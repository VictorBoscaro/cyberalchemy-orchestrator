# Repository agent policy

Every Codex subagent launch is governed by `.codex/hooks.json`.

- Never disable, bypass, or weaken the `Agent`/`spawn_agent` lifecycle hooks.
- A subagent may start only after the hook returns a YAML and ACI
  `launch-authorized` receipt.
- Let `PostToolUse`, `SubagentStop`, and `SessionEnd` complete the matching close.
- Do not manually append rows for hook-managed calls.
- If the hook blocks, repair the bridge, source-integrity, database, or ledger
  failure before retrying. Do not launch through another tool or shell process.
