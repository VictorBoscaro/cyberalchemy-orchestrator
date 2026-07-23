# Topic-emission instruction

The normative production instruction is the repository skill
[`emit-topic-tags`](../../../../.claude/skills/emit-topic-tags/SKILL.md). Keep a single source of truth:
the telemetry host invokes that skill at activation close instead of copying its body into another
prompt.

The skill emits only the agent-authored JSON string array. The telemetry host validates the mechanical
limits and adds the trusted lineage envelope described by the discovery.

Host implementation details live in
[`host-contract.md`](../../../../.claude/skills/emit-topic-tags/references/host-contract.md) and are not
loaded into the agent's ordinary emission context.
