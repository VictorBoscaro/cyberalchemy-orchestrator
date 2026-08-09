---
tags: [orchestration, permguard, pep, pdp, tool-call-authorization, runtime, security]
node_type: discovery
is_session: false
layer: architecture, runtime, external
nature: reference, technical
status: draft
veracity: medium
conviction: medium
version: 0.1.0
last_updated: 2026-08-09
---

# PermGuard PDP/PEP boundary in the ACI runtime

> **Status:** bounded follow-up research brief, not an architecture decision and not an
> implementation authorization. Owner direction for this pass was to leave the PDP/PEP ownership
> question explicitly open and to omit a separate `research-initial-definitions.md`. This document
> records the changed evidence, the candidate placements, and the tests that could discriminate
> among them.

## Question kept open

Where should the Policy Enforcement Point for agent tool calls live, and what role should the
current PermGuard executable play?

The live alternatives are:

1. the host `PreToolUse` hook is the PEP and PermGuard remains the PDP;
2. an ACI-owned broker is the PEP and calls PermGuard as its PDP;
3. a new PermGuard wrapper owns both decision and execution, combining PDP and PEP in one deployed
   component;
4. an OS/container sandbox is the load-bearing PEP, with a host hook or broker providing a narrower
   tool-call gate above it.

This brief does not select among them. In particular, shared packaging does not by itself collapse
the logical distinction: a PDP computes a policy decision; a PEP intercepts the attempted effect
and makes the decision effective.

## Why the 2026-07-20 result needs a follow-up

The earlier [`permguard-kernel` findings](../permguard-kernel/findings.md) returned
`DEFER-as-attempt-at-refutation`. That verdict is not silently reversed here. Two premises that
carried it are now stale, while its canonicalization and bypass objections remain live:

- The earlier research found no repository-local hook seam. The repository now ships
  `.codex/hooks.json` and `.claude/settings.json`, both pointing at the repository-owned host
  dispatch hook.
- The earlier research treated the Windows Lean/Mathlib build as an unresolved adoption risk. On
  2026-08-09 the sibling `lean-engineer` package completed `lake build` on Windows (951 jobs) and
  produced the PermGuard executable; the durable evidence is the sibling
  [`permguard-proof-carrying-boundaries` session](../../../domainspec-lean-formalization/theorem/sessions/2026-08-09-1508-permguard-proof-carrying-boundaries.md).
- PermGuard now rejects empty policies, packages parser-established facts in boundary objects,
  rechecks oldest-first history into `CheckedTrace` when the policy contains `secretSources`, and
  exposes separate pure models for enforcement and requirement compilation.
- The earlier objections about filesystem/URL/DNS canonicalization, TOCTOU, faithful history,
  deployment identity, and Bash-routed egress are not discharged by those additions.

The changed premises justify reopening the fit question. They do not establish that adopting the
Lean PDP is better than a smaller host-native policy check.

## What is the PEP in the repository today?

For `Agent`, `spawn_agent`, and `followup_task` launches, the current project-level enforcement path
is distributed across three pieces:

```text
host runtime
  -> PreToolUse hook configuration
  -> implementations/server/runtime/host_dispatch_hook.py
  -> allow the host tool call, or return permissionDecision: deny
```

Within a client that has loaded the project hooks and honors their result, this path is a
fail-closed PEP for the covered launch calls: the hook prepares the ACI/YAML opening state before
launch, and an exception returns a host-level denial. The host runtime supplies the final
enforcement because it is the component that either executes or suppresses the tool call.

That statement is deliberately conditional. The Stage-F documentation records that repository
configuration cannot force a client to load the hooks, administrator-managed configuration is
required for non-disableable machine or organization enforcement, and some host builds may bypass
the generic hook path. The present artifact is therefore not a universally non-bypassable PEP.

For filesystem, shell, and web effects, there is no equivalent general preventive PEP in the
checked-in hook configuration. Several such calls are observed through `PostToolUse` ingestion,
which provides lineage after the effect and cannot itself prevent that effect.

The following components are adjacent but are not, by themselves, PEPs:

- `CapabilityManager` issues, resolves, expires, and consumes scoped tokens;
- `LocalOrchestrationLoggingBridge` makes opening receipts a launch prerequisite;
- `RuntimeJournal` atomically accepts ordered events and receipts;
- PermGuard currently parses policy/request/history input and returns allow, deny, or error.

## Where PermGuard fits without creating a second authority

The authority source must be stated separately for each `ExecutionAuthorityMode`. PermGuard should
not infer or mint permissions from a prompt, skill, trace, or caller-authored policy in either mode.

| Mode | Current standing | PermGuard policy source |
|---|---|---|
| `legacy-managed` | current operational predecessor; workflow final confirmation and live register/session execution; no ACI `ConfirmedDispatch` or `Run` | **Open and blocked for implementation in this brief.** There is no ratified materializer from the current authority evidence to PermGuard policy bytes; adding one requires an explicit ownership decision and cannot invent a parallel grant. |
| `runtime-managed` | draft-specified, not a live runtime claim | Future ACI confirmation and runtime resolution may remain the authority for the effective permission grant, with deterministic policy materialization from the accepted capability resolution. |

The candidate `AgentToolProfile` already names the intended per-attempt representation of the one
capability resolution frozen by `DispatchSpec` in the proposed `runtime-managed` lane. If that lane
is implemented, it is the natural source for a deterministic PermGuard policy projection:

```text
Confirmed DispatchSpec capability resolution
  -> per-attempt AgentToolProfile
  -> deterministic PermGuard policy bytes + digest
  -> tool-call decision
```

The current live `legacy-managed` registry value `tool_profile_ref: host/inherited@1` is not yet such
a policy and must not be described as one. A future `runtime-managed` materializer would need to
preserve one authority: its policy bytes and digest must be a deterministic projection of the
confirmed capability resolution, not an independent grant record. A separate legacy materializer,
if chosen, needs its own ratified source and migration boundary.

## Candidate runtime flow

The following is a candidate `runtime-managed` flow for alternatives 1-3; the open issue is which
deployed component owns the interception and execution boundaries. It is not yet available to the
current `legacy-managed` path:

```text
agent proposes tool call
  -> PEP captures exact host payload
  -> adapter canonicalizes the supported request representation
  -> ACI resolves attempt-bound policy bytes and policy digest
  -> journal supplies the accepted oldest-first authorization history
  -> PermGuard returns allow / deny / error
  -> deny or error: PEP suppresses execution and records the outcome
  -> allow: PEP executes exactly the authorized request
  -> PEP records the execution result against the same request and policy digests
```

The authorization must bind the request actually executed. A free-standing `authorize(request)`
followed by an unrelated tool invocation leaves a substitution gap; the PEP must either execute the
captured request itself or require the host to prove that the authorized and executed payloads are
identical.

## Host-to-PermGuard mapping surface

The current PermGuard vocabulary is `read | write | edit | bash | webFetch | webSearch`. A runtime
adapter would need an explicit, versioned mapping rather than name guessing:

| Host surface | Candidate PermGuard request | Status to establish |
|---|---|---|
| `Read`, `read_file` | `read` plus canonical path segments | mapping and filesystem identity open |
| `Write`, `write_file` | `write` plus canonical path segments | mapping and filesystem identity open |
| `Edit`, `apply_patch` | `edit` plus every affected target | multi-target atomicity open |
| `Bash`, `shell_command`, `exec` | `bash` plus exact command | shell semantics and indirect effects open |
| `WebFetch` | `webFetch` plus scheme/host labels | URL, IDNA and DNS fidelity open |
| `WebSearch` | `webSearch` plus declared query fields | result-side effects and provider mapping open |
| MCP/app-specific tools | no current kernel constructor | coverage policy open; absence must not default allow |

Parser-boundary objects in the sibling Lean package certify only properties of the supplied
segments and labels. They do not certify `realpath`, symlink resolution, Windows case folding,
Unicode normalization, URL authority parsing, DNS resolution, or TOCTOU safety.

## Policy and history identity

PermGuard's current `versionId` is unauthenticated metadata. In an ACI integration, the authoritative
identity should instead be bound to accepted runtime evidence, at minimum:

- canonical policy bytes and their digest;
- the source capability-resolution reference and digest;
- dispatch, attempt, and agent/seat binding;
- policy schema and semantic-mapping versions;
- accepted journal offset or aggregate version;
- request digest and monotone event sequence.

There is also a current CLI branch that matters for the integration contract: `runGuardTrace`
executes `checkTrace` only when the policy document contains `secretSources`. If that field is absent,
the CLI parses the history but decides the current request without checking it. An integration that
claims checked history must therefore either (a) require `secretSources` on every trace-mode policy,
allowing `[]` when there are no classified sources, and reject the missing field before invoking the
CLI, or (b) first change PermGuard to check history unconditionally. This brief does not select
between those repairs.

The runtime journal already supplies transactions, compare-and-set aggregate versions,
idempotency receipts, ordered event IDs, payload digests, and authority-context digests. It does not
currently expose the exact PermGuard authorization-event projection required by `CheckedTrace`.
The history must be derived from PEP/runtime-owned accepted events; accepting a caller-provided
history would preserve logical consistency checking while losing completeness and provenance.

Possible event families, still unratified, are:

- `tool.authorization_decided`;
- `tool.execution_started`;
- `tool.execution_completed`;
- `tool.execution_failed`.

Their ownership, schemas, redaction rules, and relationship to existing ACI event authorities must
be settled before implementation. Operational telemetry must not silently become authorization
authority.

## Invariants any alternative must preserve

1. **Exactly one mode-specific grant authority.** In a future `runtime-managed` lane,
   `DispatchSpec.capability_resolution` remains the semantic source. In the current
   `legacy-managed` lane, no PermGuard policy may be materialized until that mode has a ratified
   source of grant authority. Neither lane may create or merge a parallel grant.
2. **Fail closed.** Missing policy, unknown tool mapping, malformed request, stale attempt binding,
   or unavailable PDP blocks the effect. Any integration claiming checked history must also reject
   missing trace-mode configuration and every trace mismatch; the current CLI does not establish
   that when `secretSources` is absent.
3. **Decision/execution identity.** The bytes or canonical value decided are the operation executed.
4. **Runtime-owned history.** The agent cannot select, omit, reorder, or rewrite the history used by
   the decision.
5. **Attempt and policy binding.** A decision cannot be replayed across attempts, policies, agents,
   or dispatches.
6. **No inferred complete mediation.** Hook presence is not proof that every effect path crosses the
   hook; each host/tool surface needs positive coverage and negative bypass evidence.
7. **No network claim through tool naming alone.** Allowing `bash` while denying `webFetch` does not
   establish egress confinement.
8. **Proof/runtime separation.** Lean theorems govern the modeled decision objects; deployment,
   host fidelity, canonicalization, secrets, credentials, and sandbox behavior remain separately
   evidenced obligations.

## Evidence that would discriminate among the placements

### Alternative 1: host hook as PEP, PermGuard as PDP

Evidence in favor would require a host matrix showing that every governed tool call invokes
`PreToolUse`, a denial prevents the effect, retries preserve request identity, and the hook cannot be
disabled within the claimed deployment boundary. A single relevant tool path that bypasses the hook
collapses the complete-mediation claim for that deployment.

### Alternative 2: ACI broker as PEP, PermGuard as PDP

Evidence in favor would require the agent to lack direct access to protected executors, credentials,
filesystem authority, and network routes while the broker holds them. If the agent can invoke the
same effect without the broker, broker placement adds logging and policy checks but not complete
mediation.

### Alternative 3: combined PermGuard PDP+PEP wrapper

Evidence in favor would require the wrapper to own execution rather than merely return an exit
code, plus a review showing that the enlarged trusted computing base does not blur ACI authority,
policy evaluation, host adaptation, and effect execution. If execution remains in the caller, this
is only combined packaging, not a combined PEP.

### Alternative 4: OS/container PEP

Evidence in favor would require effective-permission inspection and bypass tests demonstrating that
forbidden filesystem, process, credential, and network effects fail even when host hooks are absent.
This can provide a stronger outer boundary while leaving the hook/broker responsible for finer
tool semantics.

## Bounded first experiment after the research decision

A write/edit-only vertical is the smallest useful probe because it avoids claiming shell or network
confinement before their indirect-effect surfaces are modeled:

1. in a selected authority mode, materialize one attempt-bound policy from its ratified grant source
   without crossing or merging the `legacy-managed` and `runtime-managed` lanes;
2. map one single-target write and one single-target edit into PermGuard requests;
3. include an explicit `secretSources` array (empty is permitted) and run PermGuard from a
   `PreToolUse` enforcement path;
4. prove by filesystem observation that deny/error causes no target mutation;
5. verify that allow executes the same request digest that was decided;
6. reject policy substitution, stale attempt binding, trace tampering, replay, unknown tools, and
   unavailable-PDP cases;
7. record authorization and execution outcomes through the existing ACI journal authority.

This experiment can compare a host-hook PEP with a broker PEP without prejudging the architectural
question. It should not include `bash` or network claims.

## Open questions

- Which component should own the PEP boundary: host hook, ACI broker, combined PermGuard wrapper, or
  an OS/container boundary with one of the former above it?
- What deployment claim is intended: project-hook enforcement, administrator-managed host
  enforcement, broker-owned capability confinement, or OS-level complete mediation?
- What canonical representation makes host tool input and the executed operation equal enough for
  authorization?
- How should `AgentToolProfile` be ratified and materialized without becoming a second grant
  authority?
- Which accepted ACI events constitute the complete authorization history for `CheckedTrace`, and
  should trace checking become unconditional or remain gated by mandatory `secretSources`?
- Which tools must be unsupported or denied until their indirect filesystem/network effects are
  modeled?
- Does the formally checked PDP produce a measurable assurance gain over a smaller host-native PDP
  once the shared unverified canonicalization and mediation boundaries are held constant?

## Claims this brief does not make

- PermGuard is not currently a PEP.
- The checked-in host hooks are not universally non-disableable.
- The ACI journal is not yet a PermGuard trace authority merely because it stores ordered events.
- `AgentToolProfile` is a candidate, not a live runtime contract.
- The current `legacy-managed` path has no ratified PermGuard policy-materialization authority.
- PermGuard does not check supplied history when `secretSources` is absent.
- A successful Windows build is adoption feasibility evidence, not deployment assurance.
- This brief does not reverse the prior `DEFER` verdict or authorize implementation.

## Evidence anchors

- `research/permguard-kernel/{README.md,research.md,findings.md}` — prior fit research and its
  unresolved/null hypotheses.
- `.codex/hooks.json` and `.claude/settings.json` — current repository-local host hook wiring.
- `implementations/server/runtime/host_dispatch_hook.py` — current launch gate and conditional
  host-level denial.
- `implementations/server/runtime/{capabilities.py,journal.py,orchestration_bridge.py}` — scoped
  capabilities, accepted-event receipts, and launch prerequisites.
- `implementations/contracts/dispatch-type-registry.v1.json` — current
  `tool_profile_ref: host/inherited@1` routes.
- `docs/features/agents-communication-infra/discovery/agent-tools-and-delegated-supervision.md` —
  candidate `AgentToolProfile` and single-authority constraint.
- `docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md` — explicit
  enforcement boundary and host-loading limitations.
- `../domainspec-lean-formalization/lean-engineer/PermGuard.lean` and the imported
  `AgentPermissionKernel*.lean` modules — current PDP behavior, theorems, and stated trust borders.
- `../domainspec-lean-formalization/theorem/sessions/2026-08-09-1508-permguard-proof-carrying-boundaries.md`
  — durable Windows build, source-audit, and fixture evidence for the current PermGuard changes.

## Connections

| Document | Type | Description |
|---|---|---|
| `../permguard-kernel/findings.md` | `refines` | Reopens the old DEFER under changed implementation evidence without silently reversing it. |
| `../../docs/features/agents-communication-infra/discovery/agent-tools-and-delegated-supervision.md` | `depends-on` | Candidate single-authority path from confirmed resolution to an attempt-bound tool profile. |
| `../../docs/features/agent-provenance-telemetry/integration/stage-f/mandatory-host-wrapper.md` | `depends-on` | Current conditional host enforcement boundary. |
| `../../../domainspec-lean-formalization/lean-engineer/` | `depends-on` (external) | Sibling PermGuard PDP and proof artifacts; no local Lean proof is claimed. |
