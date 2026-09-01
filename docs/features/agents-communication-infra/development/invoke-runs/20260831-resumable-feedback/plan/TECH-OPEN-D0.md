---
title: TECH-OPEN-D0 - unresolved CONF to audit-opening authority gate
status: blocked
updatedAt: 2026-09-01
owner: agents-communication-infra
scope: infrastructure
---

# TECH-OPEN-D0 - unresolved CONF to audit-opening authority gate

This document bounds the technical work that is safe before `PRODUCT-PASS`. It records a real
contract mismatch and an unresolved authority choice. It does not select an architecture, define a
new authoritative envelope, or authorize OPEN.

## Objective and evidence boundary

The objective is to determine whether and how the runtime-managed CONF path may interact with the
legacy audit-opening 0.6.4 path without inventing authority, identity, or continuation semantics.

Current evidence establishes only the mismatch:

- The CONF contract accepts `execution_authority_mode=runtime-managed`, derives one logical
  `author -> reviewer -> author` graph, and reuses the same author Seat and logical
  `group_authoring` across author turns
  ([confirmation-authority.md](../../../../specs/confirmation-authority.md),
  [confirmation.py](../../../../../../../implementations/server/runtime/confirmation.py)).
- The executable registry currently admits only `legacy-managed` routes for every live 0.6.4 type
  ([dispatch-type-registry.v1.json](../../../../../../../implementations/contracts/dispatch-type-registry.v1.json)).
- The executable appender admits only its seven legacy agent roles, requires unique opening group
  IDs, stamps `created`, resolves omitted `invoked_by` from ambient Git configuration, and treats an
  existing `dispatch_id` as a successful no-op without comparing the existing row to the request
  ([append-dispatch.cjs](../../../../../../../.claude/skills/register-dispatch/append-dispatch.cjs)).
- `C2-TECH-D0` and the decision gate stop before opening and require product inputs plus new
  confirmation before consequential continuation work
  ([C2-TECH-D0.md](C2-TECH-D0.md), [DECISION-GATE.md](DECISION-GATE.md)).

The executable registry and appender are the evidence for current mechanics. The associated
[`register-dispatch` prose](../../../../../../../.claude/skills/register-dispatch/SKILL.md) does not
fully describe the executable immutable-route and replay behavior and requires a separate
documentation-sync change. This artifact neither repairs nor treats that prose as stronger evidence
than the code.

## Mismatch that must not be hidden

The runtime graph and a 0.6.4 opening row are different structures:

| Concern | Runtime CONF graph | Opening 0.6.4 | Consequence |
|---|---|---|---|
| Authority mode | `runtime-managed` | Current routes only admit `legacy-managed` | No authority-preserving conversion is approved. |
| Role vocabulary | `author`, `reviewer` | `explorer`, `synthesizer`, `skeptic`, `writer`, `auditor`, `planner`, `coder` | Any role mapping changes execution semantics. |
| Group identity | `group_authoring` appears in two operations | Group IDs must be unique | A direct row projection is invalid. |
| Seat identity | Same `seat_author` at turns 0 and 1 | Each opening agent entry launches a seat; no continuation key exists | Operation-scoped groups do not preserve the same Seat/session. |
| Interleaving | author, reviewer, same author | `layers=2` repeats one group without expressing reviewer interposition | Collapsing both author turns loses graph order. |
| Replay | Authority digest detects drift | Existing ID is a content-blind no-op | Appender exit 0 is insufficient replay evidence. |

Operation-scoped unique groups can therefore be used only in an **audit projection** that describes
the three logical operations. Under the current compiler/appender, they cannot be claimed to launch
or preserve the same `seat_author`, provider session, continuation, or runtime graph identity.

## Unresolved architecture and authority gate

One of the following options must be explicitly selected before any authoritative implementation.
Silence, a mechanically valid 0.6.4 row, or an L0 experiment does not select an option.

| Option | Authority contract | Benefit | Cost/risk | Evidence required before promotion |
|---|---|---|---|---|
| A - audit-only projection | A deterministic 0.6.4-shaped representation is non-authoritative and can never call the appender, launch an agent, satisfy OPEN, or advance Run/Group state. | Exposes exact field and topology gaps without mixing authorities. | Does not provide an execution path; a later authority decision remains necessary. | Closed experimental projector, explicit non-authority marker, mutation tests, and proof no production writer/effect consumes it. |
| B - ratified dual-authority composition | Runtime confirmation and a legacy route jointly authorize launch under a separately approved conjunctive contract. Neither authority substitutes for the other. | May reuse the existing host appender while preserving a runtime authority root. | Two revocation/drift/failure domains; easy to misstate precedence or let one path over-authorize the other. | A decision record must define precise approval subject, precedence, conjunctive admission, seat/task/effect authority, route drift, revocation, replay, receipt, failure and audit-query semantics. A golden proof must show neither side launches alone. |
| C - native runtime-managed registry/appender route | A new registry/appender version natively admits runtime-managed authority and represents or binds Seat/operation/continuation identity. | Avoids a legacy authority composition and can preserve runtime concepts explicitly. | Wider registry, schema, compiler, migration and compatibility change. Existing 0.6.4 consumers need a defined boundary. | Versioned registry/appender contract, compatibility matrix, migration/rollback plan, exact route/Seat/continuation fixtures, and independent authority review. |

Option B from an earlier draft is not ratified. Option C is not implicitly preferred. Option A is
the only work that can be explored before the gate because it expressly grants no launch authority.

## Non-authoritative L0 experiment

L0 may construct a pure experimental projection whose sole purpose is to measure representational
fit. It may produce:

- exact unstamped 0.6.4-shaped bytes using synthetic product values;
- operation-scoped unique audit group IDs and ordered bindings back to runtime operation IDs;
- explicit candidate role mappings, each labelled as an input rather than an inference;
- an immutable candidate route and route digest for drift tests; and
- a discrepancy report naming information that 0.6.4 cannot preserve, including shared Seat and
  continuation identity.

The experiment must not register a canonical schema name, alter CONF authority bytes, freeze a
`confirmed-authority@2`, invoke the appender against canonical telemetry, create an OPEN effect, or
be consumed as execution evidence. Its output is a hypothesis fixture, not authority.

## Normative wrapper behavior if an appender path is later authorized

This section is conditional on selection of B, or on C retaining equivalent append-only behavior.
It defines the minimum replay safety missing from the current appender; it does not authorize that
path.

The wrapper owns the complete unstamped row, comparison, idempotency state and durable receipt.
`created` is the only appender-owned opening-row field removed for comparison. `invoked_by` must be
explicit in the requested row and remains part of the comparison; ambient Git fallback is forbidden
for this path.

Before invocation, the wrapper durably records:

- exact canonical unstamped row bytes and digest;
- dispatch/idempotency key and a preallocated receipt identity;
- exact route object/digest and executable appender/registry digests; and
- state `prepared`, without claiming a ledger append.

Replay and conflict are defined by full-row equality, never by appender exit status:

1. If no ledger row exists, the wrapper may make one invocation and move to `outcome_unknown` until
   it verifies the physical row.
2. If a row exists, the wrapper parses the full row, removes only `created`, canonicalizes the
   remainder, and compares it byte-for-byte with the recorded unstamped row.
3. Exact equality finalizes or returns the **original durable receipt** under the preallocated
   receipt identity. A retry never mints a replacement receipt.
4. Any difference, including `invoked_by`, route, prompt, role, group, connection, goal, context or
   policy field, is a permanent conflict even though the appender itself would return exit 0.
5. If append succeeded but the caller lost the response, reconciliation reads and compares the
   physical row, then finalizes the reserved original receipt. It does not invoke again merely
   because the receipt response was lost.
6. If the physical result cannot be established, the state remains `outcome_unknown`; it never
   authorizes replacement append, OPEN verification, Run eligibility or downstream effects.

The original durable receipt binds the prepared request digest, exact physical row bytes/digest,
observed `created`, explicit `invoked_by`, route/appender/registry digests, ledger identity,
preallocated receipt identity and terminal comparison result. Appender stdout is diagnostic journal
evidence only and is never the receipt or copied into a dispatch working folder.

## Implementation layering

| Layer | Decision question | Minimum working unit | Explicitly deferred | Exit evidence | Promotion decision |
|---|---|---|---|---|---|
| L0 - non-authoritative oracle | After this layer, we know whether a 0.6.4-shaped audit projection can reproducibly expose every preserved and lost field without granting authority. | Pure projector/comparator, synthetic fixtures and discrepancy report. | Canonical schema, CONF change, appender call, OPEN and execution. | Byte equality, closed-shape mutations, shared-Seat/continuation loss witness, and proof of no production consumer. | Proceed only to the A/B/C decision gate; L0 cannot promote itself. |
| L1 - selected authority path | After this layer, we know whether the selected A, B or C contract is internally complete and testable. | A: durable non-authority audit artifact; B: ratified composition plus wrapper oracle; C: versioned native route/compiler oracle. | Runtime OPEN and positive Run transition. | Option-specific approval/evidence above, exact replay/conflict tests and independent authority review. | Continue only for the selected option; reject evidence borrowed from another option. |
| L2 - bounded OPEN seam | After this layer, we know whether the selected authority path can produce verified opening evidence without premature eligibility or replacement effects. | Journal state machine, original durable receipt, failpoints and reconciliation. | Resume, worker/provider execution and production cutover. | No-launch-without-authority proof, lost-response proof, full regression and independent review. | Promote only after product inputs and a new explicit confirmation of the exact approved authority package. |

### Layer boundary heuristic

L0 ends before authority because another projection feature adds less decision value than resolving
the A/B/C gate. L1 ends at the selected contract/oracle because external-effect and reconciliation
cost belongs to L2. L2 ends before resume/worker behavior because OPEN correctness is a separate
decision from provider execution.

## Smallest safe sequence

1. Implement only the L0 experimental oracle and discrepancy fixtures, if a separately bounded work
   pack/readiness receipt permits it.
2. Independently verify that it is unreachable from canonical confirmation, opening and execution
   writers.
3. Resolve the A/B/C architecture/authority gate with the required option-specific contract and
   evidence. Do not treat L0 success as approval.
4. Prepare a new bounded L1 design/work pack for the selected option.
5. Only after L1 review, compile the real product-owned package, show its exact authority subject to
   the user, and obtain explicit confirmation.
6. Implement L2 and stop again before positive Run, resume, worker or provider gates.

## L0 exact evidence

- Two independent implementations reproduce the same synthetic unstamped row bytes/digest.
- Missing, extra, reordered or mutated fields reject.
- Direct `author`/`reviewer` legacy roles and duplicate `group_authoring` rows reject under the
  executable appender contract.
- A witness proves that unique operation groups do not preserve same-Seat/continuation identity.
- A witness proves `layers=2` cannot represent the reviewer-interposed author sequence.
- Candidate route, registry, capability, tool-profile and role drift changes the experimental
  digest, without claiming that the digest grants authority.
- Supplying `created` rejects; omitting explicit `invoked_by` rejects in the experimental wrapper.
- Static reachability and test assertions show no canonical appender, effect, OPEN, Run or worker
  path consumes the fixture.

## Non-regression guardrails

- Human confirmation remains the runtime authority source; an audit row or experiment cannot
  substitute for it.
- CONF v1 fixture bytes and reviewed evidence remain unchanged.
- No `confirmed-authority@2` shape or binding is frozen before the A/B/C gate.
- Operation-scoped audit groups never claim to preserve logical Group, Seat, session or continuation
  identity.
- Appender `already registered` output never proves replay equality.
- Full unstamped-row equality and the original durable receipt are mandatory for any authorized
  wrapper path.
- Unknown physical outcome never authorizes replacement or downstream work.
- Registry/capability drift is fail-closed under whichever authority contract is selected.

## Product-owned inputs still blocked

- exact prompts and revision-instruction bytes/refs/digests;
- role, task, model, provider and tool/profile references;
- goal, context, loops, approver, output and anti-bias choices;
- resource, sandbox and execution/authority-fence policies;
- exact `invoked_by` identity mapping; and
- explicit confirmation of the final compiled authority subject.

The A/B/C selection also requires an architecture/authority decision; it is not a safe default
derivable from those product fields.

## Implementation readiness result

Implementation can proceed without product input only as the bounded, non-authoritative L0
experiment. No authoritative schema, CONF evolution, canonical appender invocation, OPEN integration
or execution path can proceed until the A/B/C authority gate is decided and its evidence contract
is satisfied.

## Implementation Layering Result

- Target: CONF to audit-opening authority boundary
- Artifact: `docs/features/agents-communication-infra/development/invoke-runs/20260831-resumable-feedback/plan/TECH-OPEN-D0.md`
- Mode: updated
- Layer count: 3
- Recommended next layer: L0 non-authoritative experiment
- Boundary heuristic: applied
- Key decision unlocked by L0: whether a deterministic audit projection exposes the mismatch without manufacturing authority
- Major deferred scope: A/B/C authority selection, authoritative envelope, real OPEN and execution
- Validation: executable appender/registry and CONF mechanics inspected; Markdown/link/whitespace checks pending
