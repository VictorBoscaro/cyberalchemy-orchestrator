---
tags: [anti-bias, subagent-dispatch, pairwise-validation, operator-ui]
artifact_kind: session
layer: feature
version: 0.1.0
created_at: 2026-08-03T16:15:07-03:00
updated_at: 2026-08-03T16:15:07-03:00
expires: 2026-10-02
decisions_made: true
contradictions_found: true
specs_updated: [.agents/skills/domainspec-subagents-strategy/SKILL.md, implementations/UI-CONTRACT.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session changes a dispatch-wide governance behavior from agent-count activation to explicit user choice while preserving compatibility and auditability."
---

# Optional anti-bias dispatch mode

## Summary

The repository objective served was to keep delegated agent work governed without forcing one judgment protocol onto every dispatch. The session objective was to make anti-bias an explicit user-controlled parameter and ensure that no skill other than the dispatch entry skill defines its policy. The chosen default is `anti_bias_mode: disabled`, and neither agent count, topology, work type, defaults, nor earlier dispatches may enable it. When enabled, schema `0.6.3` requires a structurally validated matrix covering every unordered agent pair, replacing the self-attested checker receipt while explicitly avoiding claims of semantic proof. Historical `0.6.1` and `0.6.2` records remain readable, and the host path emits `0.6.3` with the mode disabled. All ten operator UIs now distinguish enabled, disabled, and historical pending records and expose pairwise completeness when enabled. Independent reviews found stale automatic-gate language, an evidence overclaim, mutation of a frozen manifest, and insufficient behavioral UI coverage; each finding was corrected and rechecked as resolved. Validation finished with 118 runtime tests, 36 control-center tests, focused contract and manifest tests, Chromium execution across all ten UIs, verified Stage-E hashes, and a clean diff check.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [UI contract](../implementations/UI-CONTRACT.md) | `validates` | The session records browser and integration evidence for the pending-mode and pairwise-completeness behavior specified by the contract. |

## Open questions

- Should the external repository reached through the `domainspec/` junction be migrated before any installer from it is used, so its legacy mandatory `check-tension` skills cannot reintroduce the retired policy?

## Files touched

- `.agents/skills/domainspec-subagents-strategy/SKILL.md`
- `.agents/skills/register-dispatch/append-dispatch.cjs`
- `.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `.claude/skills/register-dispatch/append-dispatch.cjs`
- `README.md`
- `docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json`
- `docs/features/agents-communication-infra/adrs/fixtures/SWU-ACI-002-GOLDEN-MANIFEST-v0.6.3.json`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-input-v0.6.2-disabled.json`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-input-v0.6.2-enabled.json`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-input-v0.6.3-disabled.json`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-input-v0.6.3-enabled.json`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-v0.6.2-disabled.yaml`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-v0.6.2-enabled.yaml`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-v0.6.3-disabled.yaml`
- `docs/features/agents-communication-infra/adrs/fixtures/golden-opening-v0.6.3-enabled.yaml`
- `docs/features/agents-communication-infra/phase-2-confirm-handoff.md`
- `implementations/UI-CONTRACT.md`
- `implementations/contracts/dispatch-type-registry.v1.json`
- `implementations/server/runtime/host_dispatch_hook.py`
- `implementations/server/runtime/legacy.py`
- `implementations/server/runtime/local_pilot.py`
- `implementations/static/ui/aurora/index.html`
- `implementations/static/ui/blueprint/index.html`
- `implementations/static/ui/brutalist/index.html`
- `implementations/static/ui/cyberpunk/index.html`
- `implementations/static/ui/grimoire/index.html`
- `implementations/static/ui/linear/index.html`
- `implementations/static/ui/mission-control/index.html`
- `implementations/static/ui/radar/index.html`
- `implementations/static/ui/swiss/index.html`
- `implementations/static/ui/terminal/index.html`
- `implementations/tests/control_center/test_anti_bias_mode_ui.py`
- `implementations/tests/runtime/test_agent_reference_delivery.py`
- `implementations/tests/runtime/test_anti_bias_mode_appender.py`
- `implementations/tests/runtime/test_dispatch_workflow.py`
- `implementations/tests/runtime/test_golden_manifest_v063.py`
- `implementations/tests/runtime/test_host_dispatch_hook.py`
- `implementations/tests/runtime/test_host_workflow_binding.py`
- `implementations/tests/runtime/test_orchestration_bridge.py`
