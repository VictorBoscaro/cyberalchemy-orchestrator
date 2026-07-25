# Stage F Mandatory Host Wrapper Execution Receipt

Date: 2026-07-24  
Status: `PASS / PROJECT_WRAPPER_IMPLEMENTED / ADMIN_ENFORCEMENT_NOT_INSTALLED`

## Accepted scope

Claude Code and Codex now share one fail-closed project hook implementation for Agent launches.
The wrapper performs the Stage-C integrity preflight, issues an operation-specific expiring
capability, appends the validated compatibility-ledger row, creates or reuses an ACI Session,
links the immutable ledger snapshot, accepts `orchestration.dispatch_opened@1`, and only then
authorizes the host tool call.

Completion, failure, stop, and session-end paths close or reconcile the same deterministic
dispatch. Hook state is written before bridge side effects, so exact retries converge instead of
creating a second lifecycle. Divergent reuse of a host tool-use identity is denied.

The YAML file remains the schema-v0.6.1 compatibility ledger. Host callers do not write it
directly; the mandatory wrapper owns the validated append while the SQLite event journal holds
the authoritative runtime history.

## Verification

- Integrated Python runtime suite: PASS, 60/60.
- Legacy/compatibility runtime suite: PASS, 31/31.
- TypeScript suite: PASS, 27/27.
- TypeScript typecheck: PASS.
- Total automated checks: PASS, 118/118.
- Mandatory host-hook focused suite: PASS, 6/6.
- Orchestration bridge focused suite: PASS, 10/10.
- `python -m compileall -q implementations/server/runtime implementations/tests/runtime`: PASS.
- `git diff --check`: PASS.
- Claude and Codex hook/policy JSON parse: PASS.
- Missing policy and malformed Agent input: PASS, structured fail-closed denial with no ledger
  mutation.

## Controlled Codex hook-wire lifecycle

The checked-in Codex launcher was exercised using the documented `PreToolUse`, `PostToolUse`,
and `SubagentStop` input shapes:

```text
dispatch_id: 2026-07-24-auto-codex-agent-08a6ac484bb6a21f
session_id: ses_7205060c8c8e73af64b1af74d6c1a1ee

offset 15  apt.session_started
  event_id: evt_0d477aff8c8498abb3bbddde6b017705
  command_id: cmd_f57a207dce65b4a37b4718201b8426a2

offset 16  apt.session_dispatch_linked
  event_id: evt_fb58f88d35648c48e10f2302b80f51b6
  command_id: cmd_b6cc1e38607700e5c4d84e66456c8975
  opening_row_digest: sha256:83ad0cf6946183d3b70907c522896edef311b3d8ab32130e217eac5f18ba3690

offset 17  orchestration.dispatch_opened@1
  event_id: evt_df16ed2e84d449ae4f88ce80c15c3fbe
  command_id: cmd_6e13708778493d4a1d9aacec13e864b8

offset 18  orchestration.dispatch_closed@1
  event_id: evt_e7886bddc4768c5ceefc208950884e46
  command_id: cmd_1669da1a6e2205526af46943df734a07
  closing_row_digest: sha256:bf726e66949bb931006494513031d8153096167a28a1a3ca6066340f554a9176
  exit_reason: resolved
```

After the close, the compatibility-ledger digest was
`sha256:0a2098653500ac5c39741bf2110d2a191859de5898ba1aa137ffb50152ec2899`.

A fresh installed Codex client (`0.146.0-alpha.3`) loaded the project hook configuration and
applied its SessionEnd timeout clamp, but the model did not emit an Agent tool call in three
requested smoke attempts. Therefore this receipt claims a real launcher/wire lifecycle and
complete adapter tests, not a successful model-originated subagent spawn. Claude CLI was not
installed on this machine; Claude behavior was verified with official lifecycle shapes and the
shared adapter test matrix.

## Enforcement boundary

The wrapper is mandatory and fail-closed after the checked-in project hooks are loaded. Repository
configuration alone cannot make either client load project hooks.

For Codex, non-disableable machine or organization enforcement requires an administrator-managed
`%ProgramData%\OpenAI\Codex\requirements.toml` with hooks pinned on and the hook implementation
deployed through the managed directory. Claude similarly requires the organization or machine to
enforce loading the project hook configuration. No administrator-level host policy was installed
by this project-scoped change.

## SHA-256 evidence

```text
c40b6566ec01565ce496fbd20803b1674957bef579065b3fe03365634c7b5534  implementations/server/runtime/host_dispatch_hook.py
c5a09739bd3a12d229867fbe92904e6c383a2c9b2c9e157116962d0806bf77ed  implementations/tests/runtime/test_host_dispatch_hook.py
dfe8cec9990b40988e7d57be7ed1af4fb2055e4e2819458ab3b0ef655e53310b  .claude/hooks/host-dispatch-hook.py
b63612eb50a731bf4890d6afffc08ac19315d456a9ec91a5e1bec43112e260a3  .claude/settings.json
cf675922efb75f149675bc0545fb035505fa89f4197b2b12010e4d5abef42af9  .codex/hooks.json
222ce3522853b9c3306351b0050bddfe371575bc0b8d0499625a98577ac1bc42  AGENTS.md
04eb5326c3223d4cda75facc3bc1b9f910b9cf4669ec02abd28546e801b752cb  CLAUDE.md
1c7c3349222ddec734e989c99b2505cf72dc17a0651805c98cdbc33cfd47810b  docs/features/agent-provenance-telemetry/integration/stage-f/host-hook-policy.json
f6d9b1090548800fe77b938313addfa43a927b49087e796cff18e8f92c2585a1  docs/features/agent-provenance-telemetry/integration/stage-e/source-manifest.json
550f28c1348c5f4c5cfa8e3bf6916f8cf829c43a9772e61d3a5325f2052615e3  implementations/server/runtime/local_pilot.py
```
