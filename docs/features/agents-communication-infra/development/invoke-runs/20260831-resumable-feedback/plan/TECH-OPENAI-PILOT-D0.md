---
title: TECH-OPENAI-PILOT-D0 - bounded real OpenAI provider pilot
status: proposed
updatedAt: 2026-09-01
owner: agents-communication-infra
scope: local-provider-pilot
---

# TECH-OPENAI-PILOT-D0 - bounded real OpenAI provider pilot

## Objective and evidence boundary

The objective is to reach one real OpenAI model result quickly without weakening ACI authority,
credential, sandbox or accounting claims. The first working unit is a response-only Codex CLI
adapter proof. It is real provider work, but it is not an ACI-governed dispatch until the selected
opening authority, exact CONF v2 package and verified opening fence are present.

Success is demonstrated in four separately named stages:

1. the local Codex CLI can authenticate through ChatGPT and return typed JSONL;
2. a repository-local adapter can enforce the response-only profile and fail closed;
3. a selected and reviewed OPEN authority path can release exactly one sealed request; and
4. the result and usage observation can return through the existing ACI attempt/journal contracts.

No stage may borrow the claim of a later stage.

## Current host facts

- Provider selection: OpenAI, selected by the user on 2026-09-01.
- Executable: Codex CLI `0.146.0-alpha.10.1` through the installed Windows `.cmd` shim.
- Authentication observation: `codex login status` returned `Logged in using ChatGPT`.
- API-key environment observation: `OPENAI_API_KEY`, `CODEX_API_KEY` and `OPENAI_BASE_URL` were
  absent during the probe. No secret bytes were read or persisted.
- Real provider probe: one `codex exec --ephemeral --sandbox read-only --ignore-user-config
  --ignore-rules --json` call returned `OPENAI_PROVIDER_SMOKE_OK` and a terminal usage object.
- The probe was deliberately outside a governed dispatch. It proves availability only.

## Locked local contracts reused

- The first real provider is a repository-local subprocess `AgentAdapter` behind
  `SandboxLauncher`; no PydanticAI or provider-specific kernel branch.
- `AgentAdapter` owns provider translation and observations, never runtime state.
- `SandboxLauncher` is the only creator of a provider process and must verify the sealed request,
  current authority fence and enforceable policy before creation.
- Fake conformance and target-host negative evidence precede real-provider admission.
- The validated audit-ledger appender remains the sole physical writer of official opening rows.

## Pilot capability profile

The first real profile is `openai-codex-response-only@1`:

- one prompt, one provider turn, one terminal response;
- model `gpt-5.6-terra`, chosen as the balanced current GPT-5.6 model for this bounded pilot;
- low reasoning effort initially, raised only by a later measured quality need;
- no tools, MCP, web search, shell, file reads/writes or child work initiated by the agent;
- Codex sandbox `read-only`, ephemeral rollout, ignored user config and ignored exec-policy rules;
- JSONL transport plus a closed final output schema;
- one attempt, no automatic retry after an unknown outcome;
- fixed wall timeout, input/output byte ceilings and terminal usage observation;
- provider/control-plane egress only; no agent-tool egress;
- no continuation or session-retention claim.

Any JSONL item reporting command execution, file change, MCP call, web search, nested agent or other
tool/effect is a permanent profile violation. Provider prose cannot override the observation.

## ChatGPT-only accounting fence

Before every real start the launcher must:

1. reject if `OPENAI_API_KEY`, `CODEX_API_KEY`, `OPENAI_BASE_URL` or an explicit alternate provider
   credential is present;
2. run the non-secret status command and require the exact ChatGPT-authenticated classification;
3. never read, copy, hash, log or persist `auth.json` or credential-store material;
4. reject API-key, unknown, signed-out or ambiguous authentication;
5. persist only the authentication class, CLI version, selected model/profile and usage observation.

This fence proves that the pilot does not intentionally use OpenAI Platform API billing. It does
not claim that ChatGPT plan limits or purchased ChatGPT credits are free or unlimited.

## Smallest implementation sequence

### P1 - adapter contract and offline conformance

Create a closed request/result/event fixture and a fake process runner. Prove command construction,
authentication classification, JSONL parsing, forbidden-event rejection, timeout, cancel, malformed
output, late output, unknown outcome and process-tree cleanup without calling OpenAI.

### P2 - target-host launcher admission

Run negative fixtures on this Windows host. Admission remains false unless process creation is
launcher-only, read-only/no-tool constraints are observable, environment forwarding is allowlisted,
API-key auth is rejected, cancellation cleans the process tree and every budget supported by the
profile fails closed. Unsupported hard token ceilings remain a blocker rather than becoming an
after-the-fact claim.

### P3 - opt-in real adapter conformance

Run one explicitly opt-in, response-only OpenAI call. Preserve request digest, JSONL event digests,
terminal response, provider thread identity when returned, timing and token usage. Do not write a
Run, opening, effect or official result from this standalone proof.

### P4 - governed ACI pilot

Only after the OPEN decision and exact CONF v2 confirmation: verify the official opening, advance
the Run through the ratified transition, claim one effect, call the admitted adapter and accept the
terminal observation through the existing journal contract. Unknown never becomes success and
never triggers an automatic replacement call.

## Gates that remain product or authority decisions

### OPEN architecture

`TECH-OPEN-D0` still requires an explicit A/B/C selection. Option A cannot launch. Option B composes
runtime confirmation with the legacy route and needs a conjunctive authority contract. Option C
adds a native runtime-managed registry/appender route. Adapter P1-P3 can proceed without selecting
B or C; P4 cannot.

### Exact CONF v2 authority package

Before P4, the package must freeze the exact prompt bytes, role/task/provider/model references,
resource budget, sandbox/tool/credential policy, authority fence, audit-opening mapping and every
digest-derived identity. Presenting that package changes the confirmation subject, so the user's
standing roadmap authorization cannot substitute for confirmation of those exact bytes.

## Recommended decision

Proceed now with P1-P3. In parallel, prepare Option C as the recommended OPEN path because it keeps
runtime-managed confirmation as one authority root and can preserve Seat/operation/continuation
identity. Keep Option B only as a documented fallback if a native route proves materially slower;
do not silently compose authorities.

The one remaining human gate should be a single confirmation of the final Option C + CONF v2
package. No additional confirmation is needed for offline tests, the already-authorized roadmap
work or the opt-in standalone provider conformance already authorized in this session.

## Non-goals

- No production cutover, deployment, commit or push.
- No workspace-write or mutating tool profile.
- No second provider, mixed group or portability claim.
- No same-session continuation claim in the first provider profile.
- No API-key fallback.
- No claim that the standalone adapter proof is an official ACI execution.
