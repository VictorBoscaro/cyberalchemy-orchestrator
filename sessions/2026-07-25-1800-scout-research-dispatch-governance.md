---
tags: [orchestration, agents, dispatch, architecture, ledger, skills, ui]
node_type: constitution
is_session: true
layer: [architecture, domain, application]
nature: [explanatory, technical]
status: active
created: 2026-07-25
timestamp: 2026-07-25T18:00:32-03:00
expires: 2026-09-23
decisions_made: true
contradictions_found: false
specs_updated: [implementations/UI-CONTRACT.md]
promoted_candidates: []
expected_importance: 9
importance_rationale: "The session established enforceable delegation and dispatch boundaries across governance skills, runtime infrastructure, UI contracts, research ownership, and independently validated execution evidence."
---

# Scout research and dispatch governance

## Summary

This session reconciled the planned Reference Scout research with the existing Agent Provenance Telemetry and Agents Communication Infrastructure boundaries. It established and validated a bounded delegation mode that allows research, review, experiment, and DomainSpec code dispatches without repetitive confirmation while preserving lifecycle hooks, ACI authorization, containment audits, budgets, and independent approval. It populated the LIVE code route through a DomainSpec implementation skill and strengthened dispatch registration with a closed readiness contract, task-scoped writes, and brownfield topology checks. Runtime readers, UI contracts, static views, source-integrity manifests, tests, an execution envelope, and a detached authorization receipt were synchronized and independently reviewed. A three-seat research dispatch collected scholarly standards, operational-system precedents, and an ownership critique for Reference Scout bibliography and reference logging. The accepted synthesis kept ACI runtime and delivery facts, host SourceObservation facts, Scout recommendation claims, and APT research semantics distinct, while identifying normalized bibliographic authority as an unresolved decision. The research artifacts were relocated from the repository root into the owning Agent Provenance Telemetry feature and indexed from its README. The research skill now defaults feature-owned research to `docs/features/<feature>/research/<dispatch-slug>/`, while root `research/` remains reserved for work with no clear feature owner. Targeted runtime, bridge, source-integrity, skill, JSON, hash, and diff validations passed.

## Open questions

- Should normalized bibliographic identity be owned by an APT `BibliographicReferenceRecord` or by an independent shared bibliography capability?

## Next steps

- Resolve the normalized bibliographic authority through a decision gate before changing APT or ACI specifications.
- Encode the destination policy as the smallest possible workflow rule: suggest one destination and require explicit human confirmation for every persisted research dispatch, without adding a new schema.
- Update the owning and consuming feature specifications after the authority decision.
- Preregister a narrow Crossref and OpenAlex reconciliation experiment before implementing provider acquisition.

## Recommendation

Resolve bibliographic ownership first, then encode the decided mandatory destination-confirmation rule.

## Files touched

- .claude/skills/domainspec-subagents-strategy/SKILL.md
- .agents/skills/domainspec-subagents-strategy/SKILL.md
- .claude/skills/domainspec-implement/SKILL.md
- .agents/skills/domainspec-implement/SKILL.md
- .claude/skills/register-dispatch/SKILL.md
- .claude/skills/register-dispatch/append-dispatch.cjs
- .agents/skills/register-dispatch/SKILL.md
- .agents/skills/register-dispatch/append-dispatch.cjs
- .claude/skills/research/SKILL.md
- .agents/skills/research/SKILL.md
- .claude/skills/experiment/SKILL.md
- .agents/skills/experiment/SKILL.md
- docs/features/agent-provenance-telemetry/README.md
- docs/features/agent-provenance-telemetry/research/reference-scout-bibliography/research.md
- docs/features/agent-provenance-telemetry/research/reference-scout-bibliography/findings.md
- docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
- docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.md
- docs/features/agent-provenance-telemetry/integration/stage-e/execution-receipt.sha256
- plans/governed-agent-work-infrastructure/workstreams/scout-aci-apt-delegated-execution-envelope.json
- plans/governed-agent-work-infrastructure/workstreams/reference-scout-bibliography-research-proposal.json
- .codex/delegation-receipts/scout-aci-apt-20260725-v1.json
- implementations/UI-CONTRACT.md
- implementations/server/ledger.py
- implementations/server/runtime/orchestration_bridge.py
- implementations/server/runtime/local_pilot.py
- implementations/static/ui/aurora/index.html
- implementations/static/ui/blueprint/index.html
- implementations/static/ui/cyberpunk/index.html
- implementations/static/ui/grimoire/index.html
- implementations/static/ui/linear/index.html
- implementations/static/ui/mission-control/index.html
- implementations/static/ui/radar/index.html
- implementations/static/ui/swiss/index.html
- implementations/static/ui/terminal/index.html
- implementations/tests/runtime/test_orchestration_bridge.py
- implementations/tests/test_ledger.py

## User direction

Prefer the simplest research-placement workflow: the orchestrator suggests one destination and the user explicitly confirms it every time.
