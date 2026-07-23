# APT-P006 — Lineage resolution and replay

## Claim under test

Every topic/source observation can be resolved to one conversation, turn, dispatch, group, logical
seat and physical attempt, while retry/replay neither duplicates source facts nor accepts identity
asserted by the agent.

## Method

1. Use three synthetic conversations, each with at least two turns, two dispatches and one child
   dispatch. Include one dispatch without a conversation to cover CLI/scheduled origin.
2. Emit topic snapshots and source observations from two seats, with one retried physical attempt.
3. Build the graph only from append-only records and manifests; no transcript parsing may invent a
   missing edge.
4. Attempt independently to override every writer-owned field from the agent payload:
   `conversation_id`, `turn_id`, `dispatch_id`, `group_id`, `seat_id`, `attempt_id`, activation
   sequence and timestamp.
5. Replay the observation log twice and compare canonical graph/manifests and state hashes.
6. Simulate lost response after append, then retry the same operation/digest; simulate the same key
   with a different digest.

## Preregistered decision

- 100% of accepted observations resolve to exactly one dispatch/seat/attempt and to either exactly
  one conversation/turn or an explicit non-conversation origin.
- Agent-supplied writer fields are rejected, not ignored or normalized.
- Identical retry yields the same observation identity and no new logical record; divergent retry is
  a permanent conflict.
- Two replays produce the same graph, manifests and state hashes with zero writer/tool effects.
- A missing parent/origin ref remains explicit residue; the projector must not infer it from timestamps
  or similar text.

Any failure blocks claims that the feature provides a provenance spine; isolated topic/source capture
may continue only under a narrower “unlinked observations” label.

## Falsifiers and invalid runs

- `agent_name` is used as execution identity.
- Conversation and curated session-document identities are treated as the same namespace.
- A retry appends a second logical source/topic observation.
- The graph projector reads chat prose to repair a missing edge.

## Output

Synthetic input corpus, append trace, rejection matrix, two replay outputs, state hashes and a lineage
decision record.

