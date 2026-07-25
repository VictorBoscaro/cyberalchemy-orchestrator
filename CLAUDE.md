# Repository agent policy

Every Claude Agent-tool launch is governed by the mandatory hooks in
`.claude/settings.json`.

- Never disable, bypass, or weaken the Agent lifecycle hooks.
- An Agent may start only after YAML and ACI opening receipts are accepted.
- Let the completion/failure/subagent/session hooks write the exact close.
- Do not manually append rows for hook-managed calls.
- If launch is denied, repair the named bridge failure before retrying.
