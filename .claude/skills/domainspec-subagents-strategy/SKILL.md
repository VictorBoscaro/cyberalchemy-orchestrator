---
name: domainspec-subagents-strategy
description: Owner-directed current workflow contract for routing subagent dispatches, proposal and confirmation gates, universal workflow invariants, and dispatch-type routing. Use for workflow-level dispatch planning; register-dispatch owns persisted row mechanics, and ratified discovery/SPEC/ACI artifacts own runtime authority.
---

**Current workflow contract:** by owner direction dated 2026-07-23, use this skill for the current
dispatch workflow. Its additions remain workflow-level until ratified in discovery/SPEC/ACI; this
skill does not self-promote to runtime or governing authority. `register-dispatch` owns persisted
row mechanics. The historical
`internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md`
is absent; that absence grants no authority, and its former section citations are non-resolvable
provenance. The current wire `schema_version` remains `"0.6.1"`. By repository-owner direction on
2026-07-25, the LIVE generic `others` route is an in-place enum amendment; a future coordinated
schema migration may give it a new wire version.

## When to dispatch (P1) — and what is not a dispatch (P11)

Dispatch only when at least one trigger holds: **synthesis** (3+ sources to combine), **context protection** (raw output ≫ what the parent needs), **isolation** (discardable exploration), **parallelism** (independent tasks). Otherwise work inline.

**Helper rule (P11):** a single agent spawned *by* a running agent, within its parent's scope, is not a dispatch — no row, no gate; it is reported post-hoc in the parent's `agents_spawned`. It escalates to a real dispatch when it fans out (2+) or outgrows the parent's scope.

**Scoped discovery-authoring exception (owner direction, 2026-07-23):** the
`discovery-writing` workflow may use (a) one read-only validator followed by at most one read-only
acquisition helper per confirmed probe slot and (b) the review topology confirmed for that
discovery, bounded to 2–3 mutually isolated read-only reviewers per round and at most 5 rounds. They
remain helpers only while they produce no independent/persisted deliverable, stay within the
confirmed discovery target/source scopes, and are reported by the orchestrator. Any wider fan-out,
persisted review, target expansion, or separately consumable result is a real dispatch and re-enters
propose/confirm/register/close.

It may also use exactly one controlled writer that persists only the confirmed, parent-owned
discovery target and returns only `WriterHandoff`. That target is the parent's workflow artifact,
not an independently consumable writer deliverable, so this writer is not a dispatch. This is a
bootstrap exception because no LIVE `discovery` dispatch type exists. Never misclassify it as
`research`, `review`, or `experiment`. If a discovery dispatch type is ratified, its writer and
formal reviews must use register open/close.

*(The general helper-vs-dispatch boundary remains provisional; this exception settles only the
bounded discovery-authoring case above.)*

**Proposal-gate helper exception (owner direction, 2026-07-23):** one read-only capability
reviewer plus exactly two independent read-only check-tension helpers may inspect one pending
proposal revision without first registering a dispatch. They must not persist or independently
publish a deliverable. Any added helper, wider scope, persisted output, or separately consumable
result is a real dispatch and re-enters propose/confirm/register/close.

## Two-level planning model

The `StructuralGraphProposal` and `ConcreteDispatchProposal` names below apply only to real
dispatches. The unregistered discovery bootstrap uses the distinct
`DiscoveryBootstrapStructuralProposal` / `DiscoveryBootstrapConcreteProposal` contract owned by
`discovery-writing`; it does not pretend to be derived from a pending dispatch sheet.

Every non-trivial dispatch is built as two immutable, session-local projections derived from one
pending sheet:

1. **`StructuralGraphProposal`** — objective, boundaries, group/seat counts, abstract roles, probe /
   writer / reviewer positions, connections, `robot_talks`, `sequential` / `zig-zag` / `feedback`,
   loop ceilings, output joins, budget envelope and confirmation mode. It contains no persona names,
   concrete models, complete prompts, concrete sources or resolved tools.
2. **`ConcreteDispatchProposal`** — exact `seat_id`, agent/persona label, role/type/lens,
   `requested_provider`, `requested_model`, `requested_adapter`, skills and digests, immutable
   `prompt_template`, response contract,
   exact source path→SHA-256 bindings, `proposed_capability_profile`, command classes, proposed
   write/network/sandbox scopes, exact budgets, reviewer instantiation and per-edge rounds. Embed
   the capability review's result, amendments, task digest, and proposed-profile digest in this
   proposal. For every group include the anti-bias axis; for every seat include its angle/position;
   for every pair include the predicted disagreement question, both predicted positions, and
   evidence supporting that prediction. It references the exact structural revision/digest.

Each projection declares `projection_schema_version`, rejects duplicate object keys, and uses
RFC 8785 JSON Canonicalization Scheme (JCS) before SHA-256. If no conforming JCS implementation is
available, a locally sorted/compact JSON digest is workflow evidence only and must not be called
portable or durable. The projections are session-local approval evidence, not authorities or
partial dispatch records. When ACI support is materialized, `ConfirmedDispatch` / `DispatchSpec`
own the durable approved bytes and receipts.

The proposal records only a `proposed_capability_profile`. Effective model selection, grants, and
sandbox enforcement remain ACI/runtime-owned. Record `effective_enforcement:
observable | non_observable`. When observable, compare effective semantics with the confirmed
request and fail closed on mismatch; when non-observable, report the gap and never call requested
provider/model/adapter or proposed tools effective.

The orchestrator builds the structure first and the concrete resolution second even when the user
chooses to see only the final proposal. For now every seat and review/probe slot is resolved before
execution. Runtime changes to agent, lens, prompt, source or tools are deferred until a separate
reconfiguration-gate contract exists.

### Confirmation modes

The user selects one mode before the first confirmation:

- `structure_and_final` — show and confirm the structural graph, resolve the concrete proposal, then
  show and confirm every concrete field.
- `final_only` — build and digest the structure internally, then show one concrete proposal containing
  both topology and all resolved details for confirmation.
- `structure_only` — confirm only that planning may continue. It never authorizes execution; the
  resolved proposal must return for a final confirmation.
- `delegated_bounded` — the user confirms one versioned `DelegatedExecutionEnvelope` for a named
  objective. Later concrete proposals may execute without another human confirmation only when
  every field is proven to remain inside that envelope. Capability review, two independent
  check-tension PASS results, registration, hook authorization, final approval and close remain
  mandatory.

`structure_only` never implies delegated execution. Delegation exists only through
`delegated_bounded` and its explicit envelope.

### Bounded delegation

A `DelegatedExecutionEnvelope` is workflow authority for one finite objective, not global
permission or ACI runtime authority. It records:

- envelope ID, version, objective, issuing-user evidence and confirmation timestamp;
- allowed repositories, path scopes and dispatch types;
- allowed network, tool, sandbox and mutation classes;
- per-dispatch and aggregate agent, token and round budgets;
- required reviewers, final-approver policy and validation obligations;
- forbidden effects, secrets, production/deployment targets and destructive actions;
- expiry, stop conditions and the exact conditions requiring renewed human confirmation.

Canonicalize and digest-bind the envelope in a versioned authorization receipt that records the
user-evidence reference/digest and is outside every delegated write scope. The envelope must deny
mutation of itself and that receipt; deny rules override allow rules. A replacement requires a new
user confirmation and a new receipt version, never an in-place edit. Each structural and concrete
proposal records its envelope and authorization-receipt references and digests as workflow
evidence. Before registration, perform a total
containment check over dispatch type, objective, sources, paths, tools, capabilities, network,
mutation, agents, tokens, rounds, outputs and effects. An omitted dimension is denied.

In addition to capability review and check-tension, two independent read-only envelope auditors
must PASS the exact concrete-proposal/envelope digest pair. Any auditor mismatch, ambiguity, expired
budget, new credential, production/deployment action, destructive action, external side effect or
field outside the envelope returns to explicit human confirmation. The user may revoke the
envelope at any time.

Envelope confirmation never weakens `.codex/hooks.json`, append-only ledger mechanics, ACI launch
authorization, receipt reconciliation, P8 verification or the routed type skill. It only replaces
repetitive human confirmation for fully contained proposals.

### Invalidation

- A structural change creates a new structural revision and invalidates every concrete resolution
  and final confirmation derived from it.
- A concrete-only change creates a new concrete revision and invalidates final confirmation while
  preserving a still-matching structural confirmation.
- Under `delegated_bounded`, either change requires a fresh containment proof and two fresh
  envelope-auditor PASS results. A change outside the envelope invalidates delegation.
- A physical or protocol retry changes attempt identity, not either proposal.
- Confirmation binds revision ID plus digest. A chat acknowledgement is not a durable runtime
  receipt; until ACI materializes these entities, report the gate as workflow evidence only.

### Frozen prompts and dynamic inputs

Final confirmation freezes each `prompt_template`; later returns never amend it. Before a
downstream invocation, the host materializes the template's declared dynamic slots into a separate
workflow-only `WorkflowInputManifest`, canonicalized by the same rule. Each slot declares name,
authorized producer, data type/schema, cardinality, byte/token ceiling, purpose, and source/response
schema. Slots carry data only: instructions, authority, lenses, source boundaries, and output
contracts are forbidden. Bind every referenced file as `{path, sha256}` and digest the manifest.
Changing template text or any instruction/authority/lens/source-boundary/output contract
invalidates concrete confirmation; supplying conforming data does not. ACI alone owns a true
`EffectiveInputArtifact`. Every registered topology that needs post-confirmation downstream input
is `UNAVAILABLE` unless ACI/runtime persists and binds its manifest; this is not limited to
robot-talks. Unregistered bootstrap helper loops may use a `WorkflowInputManifest` as workflow
evidence only and never claim durable binding.

## Lifecycle — the universal four steps

1. **Propose.** Build `StructuralGraphProposal` first. According to `confirmation_mode`, present it or
   continue to `ConcreteDispatchProposal`. Before concrete confirmation, run one read-only
   capability reviewer over every seat's proposed logical tool profile and embed its result,
   amendments, and digests in the concrete proposal. The proposal **states where artifacts land**
   (`working_folder` or inline), output mode, exact agents, prompt templates, path→hash sources,
   proposed capabilities, and limits. Then run **two independent check-tension helpers** over the
   same concrete revision. Only two PASS results on its exact digest may reach concrete
   confirmation. Any failure returns the sheet for revision, recanonicalization, and two fresh
   checks; never average or waive the results.
2. **Confirm or prove delegation containment.** Each ordinary gate needs an explicit affirmative;
   silence or a question is not confirmation. Under `delegated_bounded`, the already-confirmed
   envelope plus a total containment proof and two envelope-auditor PASS results replace the
   per-dispatch human affirmative. Nothing registers or executes before the applicable route passes.
   Final confirmation or containment proof freezes the concrete proposal and artifact destination.
   Any later change applies the invalidation rules above. The final concrete sheet remains the input
   to `register-dispatch`; the current wire row is unchanged.
3. **Register + run.** Append the dispatch row, then schedule groups **by dependency** (P4, amended 2026-06-12): a group is READY when every group with a `sequential`/`zig-zag` edge into it has produced what it must respond to (zig-zag counts only in its `from`→`to` direction — the `from` endpoint opens the exchange); launch all READY groups concurrently; `feedback` edges never count as dependencies; a sheet with no connections declares its groups independent; declared order is narration tiebreak only. Agents inside a group run in parallel. An agent error degrades to a **partial group result** that downstream groups and the `final_approver` must be told about.
4. **Close.** Report `exit_reason` + `agents_spawned` in chat — and in the persisted deliverable when there is one (`findings.md` for research; `review.md` for a `persisted` review; an `inline` review reports in chat only) — and append the close row. Two appends, one ledger, append-only (P3).

For the record shape, the appender, and the close-row mechanics: **register-dispatch owns them** — see Pointers.
Steps 3–4 apply to actual dispatches. The scoped discovery bootstrap is not a dispatch: it performs
no ledger mutation and emits workflow terminal status only.

## Universal invariants (every dispatch_type)

By owner direction dated 2026-07-23, treat these as current workflow invariants. They remain
workflow-level until ratified in discovery/SPEC/ACI.

- **P5 — pairwise tension.** Any n ≥ 2 group must be pairwise tensioned (predictable disagreement per pair, named axis, per-agent position); two independent **check-tension** helpers must both PASS the exact concrete digest before human confirmation.
- **P7 — aggregation is derived,** never a field: `robot_talks: true` → the group synthesizes; otherwise → concat. *(Non-binding note, per P7's own framing: a bare concat is never the dispatch's final deliverable.)*
- **P10 — claim ≤ proof** in every artifact produced.
- **P12 — final approval.** Every dispatch names a `final_approver`: `parent` (default) or a dedicated approver group whose single agent's role is `auditor` and that does no other work; never a working-group member (no self-approval); falls back to `parent` if its group never runs. The approver receives the complete evidence bundle: for persisted output, the full `working_folder`; for inline review, the complete `review.md` payload plus the frozen target corpus as exact path/hash pairs. The selected confirmation lifecycle may contain one or two pre-run planning gates. P12 forbids adding a new human gate after execution begins.
- **Three dials, three scopes.** `layers` (group) / `loop_cap` (edge) / `max_loops` (dispatch) — one scenario, one dial; if two seem to fit, the smallest scope wins.
- **exit_reason.** Closed vocabulary: `resolved | loop_ceiling_reached | dissent_irreconcilable | user_abort | error`.
- **P8 — trust-but-verify.** If a subagent wrote files or claimed a check passed, inspect the actual diff / run the actual check before treating it as done.
- **P13 — meta + lineage.** A dispatch about dispatching is `meta: true`; `parent_dispatch_id` exists only on a dispatch planned by a meta dispatch; a meta-planned child re-enters the confirm gate.
- **P14 — robot-talks binding.** A group with `robot_talks: true` binds the existing
  `.claude/skills/robot-talks/SKILL.md`. Its historical constitution/rationale path is absent and
  is non-resolvable provenance. This strategy's single planning lifecycle overrides robot-talks'
  additional human-gate and session-preservation instructions for a dispatch. A downstream
  synthesizer's confirmed prompt template declares data-only slots for every agent's initial and
  final positions. For an unregistered workflow, the host may supply them through a separately
  digested `WorkflowInputManifest`. For a registered dispatch, ACI/runtime must persist and bind
  the dynamic input; otherwise this topology is `UNAVAILABLE`.

## Routing by dispatch_type

LIVE status is declared by this table; changing a reserved type is an owner act. A LIVE row must
also point to an existing skill. Routing to a RESERVED type: **refuse and tell the user** the type
is not yet populated.

| dispatch_type | status | skill |
|---|---|---|
| `research` | LIVE | `.claude/skills/research/SKILL.md` — research-type judgment: canonical shape, roles, gates, outputs |
| `code` | LIVE | `.claude/skills/domainspec-implement/SKILL.md` — DomainSpec-driven implementation from accepted specs and generated tests; requires planner/work-pack PASS, implementation axioms, context scaffold, independent alignment/layering review, tests, tagging and verification |
| `review` | LIVE (populated 2026-06-12, owner decision) | `.claude/skills/review/SKILL.md` — red-team judgment: attack lenses, severity taxonomy, verification discipline, the change-request report. **One artifact: `review.md`** (the synthesis — no `attacks.md`, no `findings.md`); `output_mode` picks chat vs `<working_folder>/review.md` |
| `others` | LIVE (added 2026-07-25, owner decision) | This strategy skill — bounded work for which no LIVE specialized dispatch type exists, including document and Plan-artifact authoring. The concrete proposal must name the work kind and output contract. `others` supplies only the universal lifecycle and invariants; it must not claim the stronger semantics of a future specialized type. |
| `plan` | RESERVED — must not be dispatched until populated | none |
| `suggestion` | RESERVED — must not be dispatched until populated | none |
| `experiment` | LIVE (populated 2026-06-14, owner decision) | `.claude/skills/experiment/SKILL.md` — falsification judgment: pre-registered criterion freeze, validity gates, SURVIVED/FALSIFIED/INVALID verdict (propose phase only — INVALID may be rendered here; SURVIVED/FALSIFIED rendered at the separate downstream run) |

## Pointers (single owners)

- **Form — record/sheet fill mechanics:** `register-dispatch` (`.claude/skills/register-dispatch/SKILL.md`; appender `.claude/skills/register-dispatch/append-dispatch.cjs`) — field tables, enums, the appender, the close row, `invoked_by`.
- **Definitions + skeleton:** inline in `register-dispatch` (field tables, enums, schema, annotated example).
- **Agent names:** `telemetry/agents/agent-pool.yaml`.
- **Anti-bias design:** `.claude/skills/anti-bias-vector-composition/SKILL.md` (the `check-tension` gate enforces it; the planned vault discovery `implementation/domainspec/vault/discovery/anti-bias-vector-composition/` is currently absent/non-resolvable, not an existing knowledge home).
- **Init-time tensioning gate:** `check-tension` (`.claude/skills/check-tension/SKILL.md`) — run two independent helpers against the same concrete digest; only "both PASS" reaches the human.
