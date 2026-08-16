# Dispatch State - Knowledge Formation

Launch state captured after dispatch specification and review, before any research seat launch.

- Launch timestamp (first research seat runtime creation): `2026-08-13T19:13:32.402Z`

## Dispatch

- Dispatch ID: `2026-08-13-knowledge-formation`
- Dispatch file: `research/knowledge-formation/dispatch.yaml`
- SHA-256: `12A1EDCCB443E344F587825A1A0E0B72B89568A21F3B1F7507F0EA56096FD151`
- Validation state: `accept`
- Seat count: 15

## Repository baselines

| Root | Branch | Commit | Dirty entries at capture |
|---|---|---|---:|
| `C:/Users/victo/cyberalchemy-orchestrator` | `master` | `48d5f7b830fc52773da8ce5191131ec2e05274f4` | 64 |
| `C:/Users/victo/domainspec-lean-formalization` | `main` | `2a7a5aecb2e3b06ca985f8f15fb7bb75fd0ea4f3` | 53 |

The dirty trees predate seat launch and belong to the user except for the known dispatch-created
paths below. Researchers must not treat working-tree presence as proof of authorship, authority, or
completion.

## Known dispatch-created paths before launch

- `research/knowledge-formation/research-initial-definitions.md`
- `research/knowledge-formation/dispatch.yaml`
- `research/knowledge-formation/review/review.md`
- `research/knowledge-formation/review/dispatch-review/review.md`
- `research/knowledge-formation/research/dispatch-state.md`
- `Codex/current_conversations/2026-08-13-knowledge-formation-initial-definitions.md`

## Mutation boundary

Research seats may write only their declared R12 record. The parent owns collected briefing
returns and dispatch state. Writers own only their declared synthesis artifacts. No seat may edit
the source corpora during this dispatch.

## Post-audit provenance recovery

The first audit identified missing per-return timestamps and missing separately persisted pre-exposure
Phase-A bytes for KF-L1A-E1 and KF-L1A-E2. The parent recovered both original `agent_message`
payloads byte-for-byte from their runtime JSONL events and recorded their event timestamps and hashes
in `research/knowledge-formation/research/briefing-returns-provenance.md`. This supplement does not
mutate the briefing collation used by the frozen descriptive synthesis.
