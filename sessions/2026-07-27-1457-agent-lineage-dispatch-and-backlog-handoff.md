---
tags: [agent-reference-lineage, input-lineage, backlog-skills, agent-orchestration, research-workflows]
artifact_kind: session
layer: project
version: 0.1.0
last_updated: 2026-07-27
created: 2026-07-27
timestamp: 2026-07-27T14:57:35-03:00
expires: 2026-09-25
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session connects the original AgentReferenceLineage question to its specifications and implementation, exposes incomplete dispatch binding, and preserves the backlog-skill and research-lineage continuations."
---

# Agent lineage, dispatch binding, and backlog handoff

## Summary

The session began by inspecting the project plans and asking what `AgentReferenceLineage` means, where it is implemented, which APT and ACI specifications own it, and whether the specification surface still has gaps. The repository already models delivered references through ACI attempts, `EffectiveInputArtifact`, `AgentReferenceDelivery`, runtime tables, and APT lineage projections, but this is narrower than universal provenance for every task, work-pack, read, write, and produced artifact. Discussion of direct agent messaging established that the BUS is mediated through persistence, verification, reveal, and later input materialization rather than an unrestricted peer inbox. That led to an open ACI backlog candidate for a promotion-gated cross-dispatch work graph and to a reusable backlog skill. The backlog skill passed one independent FIX round followed by joined PASS verdicts, but final approval found that it lives only in the ignored `.agents` mirror while `.claude/skills` is the repository source of truth. The aggregate backlog-skill dispatch was opened and closed in the YAML ledger, yet none of its subagent launches produced an ACI `host_workflow_turn_bindings` row or persisted `WorkflowInputManifest`; the session-local proposal JSONs also remained non-authoritative scratch, and several did not match the strict runtime schema. The missing per-launch evidence is consistent with the previously recorded Codex function-tool hook coverage defect rather than proof that workflow binding ran. The conversation then separated the immediate work—canonicalize the backlog skill and repair launch binding—from the longer design work of decomposing the oversized `research` workflow and capturing read/write lineage. The owner decided that universal lineage should first be modeled as a bounded step inside the `research` decomposition, using attempt-centric operational evidence for observed reads and produced revisions, and generalized only after that use proves its shape. Scouts were considered but explicitly not launched, and factual acquisition should not inherit artificial tension requirements.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Agent Provenance Telemetry specification](../docs/features/agent-provenance-telemetry/specs/SPEC.md) | `contextualizes` | Owns the current `AgentReferenceLineage` query surface and its dependency on ACI delivery/effective-input evidence. |
| [Agents Communication Infrastructure backlog](../docs/features/agents-communication-infra/BACKLOG.md) | `contextualizes` | Records the cross-dispatch work-graph candidate that exposed the need to distinguish aggregate registration from bound child launches. |
| [Codex hook host-binary remediation](2026-07-27-1255-codex-hook-host-binary-remediation.md) | `validates` | The absence of new hook state and workflow bindings in this session is consistent with the previously recorded function-tool hook coverage blocker. |
| [Research skill](../.agents/skills/research/SKILL.md) | `contextualizes` | The continuation will decompose this workflow and use research-local read/write lineage as the first bounded case. |

## Open questions

- Does the existing `AgentReferenceLineage` remain intentionally reference-specific, with universal task/artifact input lineage introduced as a separate concept, or should its specification boundary expand?
- Which source artifact should canonically own the validated backlog skill, and which `.codex/workflow-inputs` scratch files should be removed after audit?
- Why did the live Codex collaboration surface bypass both compatibility dispatch registration and governed host-workflow binding despite the configured matcher?
- Which responsibilities in `research` are deterministic validators or compilers, and which must remain agent judgment?
- What is the smallest research-local lineage model that captures actual reads and writes without equating “read before write” with `derives-from`?
- After the bounded research use is proven, which portions belong generically to ACI capture, APT projection, work-pack/task schemas, and semantic ontology edges?

## Next steps

1. Promote the reviewed backlog skill to the canonical `.claude/skills/backlog` source, regenerate the `.agents` mirror, validate equality, and remove scratch files only after explicit cleanup authorization.
2. Repair and prove the launch path from `collaboration.spawn_agent`/`followup_task` through the mandatory hook to YAML open/close and terminal ACI workflow bindings.
3. In the new conversation, inventory every responsibility currently owned by `research` and classify it as deterministic validation, orchestration, evidence acquisition, synthesis, or judgment.
4. Define the research-local execution chain `Task -> Attempt -> observed-read/produced -> ArtifactRevision`, map existing reference-lineage/input-manifest pieces onto it, and defer universal promotion until the bounded model exposes no ownership conflict.

## Recommendation

Finish the canonical backlog skill first and make per-launch ACI binding fail-closed before trusting another multi-agent workflow here; begin the new conversation separately with the `research` responsibility inventory and attempt-centric lineage slice.

## Files touched

- `.agents/skills/backlog/SKILL.md`
- `.agents/skills/backlog/agents/openai.yaml`
- `.agents/skills/backlog/assets/backlog-template.md`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/capability-review-brief-v1.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/concrete-proposal-v1.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/dispatch-close.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/dispatch-open.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/feature-backlog-writer-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/reviewer-governance-round-1-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/reviewer-governance-round-2-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/reviewer-usability-round-1-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/reviewer-usability-round-2-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/skill-author-feedback-round-1.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/skill-author-manifest.json`
- `.codex/workflow-inputs/2026-07-27-backlog-skill-work/structural-proposal-v1.json`
- `docs/features/agents-communication-infra/BACKLOG.md`
- `sessions/2026-07-27-1457-agent-lineage-dispatch-and-backlog-handoff.md`
- `telemetry/agents/subagents-dispatch.yaml`
