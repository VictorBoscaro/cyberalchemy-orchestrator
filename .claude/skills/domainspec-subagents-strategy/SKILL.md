---
name: domainspec-subagents-strategy
description: Route any subagent dispatch — check the Principle-1 trigger, hold the human gate, enforce the universal invariants, then route by dispatch_type to the owning type skill (research, review, and experiment are LIVE; code/plan/suggestion are reserved). The record/sheet form is owned by register-dispatch; field definitions by constitution §5. This skill defines no field and no type-specific judgment — it routes.
---

**Governing doc:** operationalizes `internal_tools/subagents-dispatch-hooks/constitution/subagents-strategy-constitution-proposal.md` (v0.6.3-proposal). The live vault constitution is still v0.3.0; where the two conflict, v0.6.x wins (owner decision 2026-06-12; doc bumped 0.6.0 → 0.6.1 → 0.6.2 → 0.6.3 per §10 / §12 / §13 / §14). The wire `schema_version` is `"0.6.1"` (§10.1: it bumps only on a *row-schema* change — §14 added the `output_mode` key, so 0.6.0 → 0.6.1).

> **Read budget — do NOT open the constitution to run a dispatch.** The full operational form is inline: routing + invariants here, every field/enum/schema/skeleton/close-row in `register-dispatch`. The constitution (822 lines) is **authority-of-last-resort** — open it *only* to adjudicate a genuine conflict between this skill and the constitution, never as a routine lookup. The `§N` cites below are provenance anchors for that rare case, not an instruction to read.

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

*(The general helper-vs-dispatch boundary remains provisional; this exception settles only the
bounded discovery-authoring case above.)*

## Two-level planning model

Every non-trivial dispatch is built as two immutable projections over the same eventual full sheet:

1. **`StructuralGraphProposal`** — objective, boundaries, group/seat counts, abstract roles, probe /
   writer / reviewer positions, connections, `robot_talks`, `sequential` / `zig-zag` / `feedback`,
   loop ceilings, output joins, budget envelope and confirmation mode. It contains no persona names,
   concrete models, complete prompts, concrete sources or resolved tools.
2. **`ConcreteDispatchProposal`** — exact `seat_id`, agent/persona label, role/type/lens,
   provider/model/adapter, skills and digests, initial prompt, response contract, sources/snapshots,
   tool profile, command classes, write/network/sandbox scopes, exact budgets, reviewer
   instantiation and per-edge rounds. It references the exact structural revision/digest.

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

Do not implement delegated execution from structure-only approval. That requires a future
`DelegatedResolutionEnvelope` and SPEC decision.

### Invalidation

- A structural change creates a new structural revision and invalidates every concrete resolution
  and final confirmation derived from it.
- A concrete-only change creates a new concrete revision and invalidates final confirmation while
  preserving a still-matching structural confirmation.
- A physical retry changes attempt identity, not either proposal.
- Confirmation binds revision ID plus digest. A chat acknowledgement is not a durable runtime
  receipt; until ACI materializes these entities, report the gate as workflow evidence only.

## Lifecycle — the universal four steps (§3)

1. **Propose.** Build `StructuralGraphProposal` first. According to `confirmation_mode`, present it or
   continue to `ConcreteDispatchProposal`. Before concrete confirmation, run one read-only
   capability reviewer over every seat's logical tool profile; surface its allow/deny amendments
   with the proposal. The concrete proposal **states where artifacts land** (`working_folder` or
   inline), output mode, exact agents, prompts, sources, tools and limits. Before any user-facing
   proposal, run the **check-tension gate** over the applicable projection; only a PASS proceeds.
2. **Confirm.** Each required gate needs an explicit affirmative; silence or a question is not
   confirmation. Nothing registers, persists as a dispatch row, or executes before all gates required
   by the selected mode pass. Structure confirmation freezes only the structural revision. Final
   confirmation freezes the concrete proposal and artifact destination. Any later change applies the
   invalidation rules above and re-enters only the affected gate(s). The final confirmed concrete
   sheet remains the input to `register-dispatch`; the current wire row is unchanged.
3. **Register + run.** Append the dispatch row, then schedule groups **by dependency** (P4, amended 2026-06-12): a group is READY when every group with a `sequential`/`zig-zag` edge into it has produced what it must respond to (zig-zag counts only in its `from`→`to` direction — the `from` endpoint opens the exchange); launch all READY groups concurrently; `feedback` edges never count as dependencies; a sheet with no connections declares its groups independent; declared order is narration tiebreak only. Agents inside a group run in parallel. An agent error degrades to a **partial group result** that downstream groups and the `final_approver` must be told about.
4. **Close.** Report `exit_reason` + `agents_spawned` in chat — and in the persisted deliverable when there is one (`findings.md` for research; `review.md` for a `persisted` review; an `inline` review reports in chat only) — and append the close row. Two appends, one ledger, append-only (P3).

For the record shape, the appender, and the close-row mechanics: **register-dispatch owns them** — see Pointers.

## Universal invariants (every dispatch_type)

These bullets are operational restatements of constitution §4; §4 is authoritative on conflict.

- **P5 — pairwise tension.** Any n ≥ 2 group must be pairwise tensioned (predictable disagreement per pair, named axis, per-agent position); checked by the **check-tension gate** (two independent agents) before the human confirm — untensioned sheets go back to the strategist for revision.
- **P7 — aggregation is derived,** never a field: `robot_talks: true` → the group synthesizes; otherwise → concat. *(Non-binding note, per P7's own framing: a bare concat is never the dispatch's final deliverable.)*
- **P10 — claim ≤ proof** in every artifact produced.
- **P12 — final approval.** Every dispatch names a `final_approver`: `parent` (default) or a dedicated approver group whose single agent's role is `auditor` and that does no other work; never a working-group member (no self-approval); falls back to `parent` if its group never runs; the approver receives the full `working_folder`. One human gate only — the entry confirm.
- **Three dials, three scopes.** `layers` (group) / `loop_cap` (edge) / `max_loops` (dispatch) — one scenario, one dial; if two seem to fit, the smallest scope wins. Decision table: constitution §5.
- **exit_reason.** Closed vocabulary: `resolved | loop_ceiling_reached | dissent_irreconcilable | user_abort | error`. Precedence + decision procedure: constitution §5.
- **P8 — trust-but-verify.** If a subagent wrote files or claimed a check passed, inspect the actual diff / run the actual check before treating it as done.
- **P13 — meta + lineage.** A dispatch about dispatching is `meta: true`; `parent_dispatch_id` exists only on a dispatch planned by a meta dispatch; a meta-planned child re-enters the confirm gate.
- **P14 — robot-talks binding.** A group with `robot_talks: true` binds `vault/constitution/robot-talks-constitution.md`. Structural/final confirmations happen before execution and form one planning lifecycle; robot-talks may not introduce additional mid-run human gates. A synthesizer downstream of a robot-talks group MUST receive each agent's initial AND final positions (collapse detection).

## Routing by dispatch_type

LIVE status is **declared by constitution §5** (promoting a reserved type goes through §7's premise-debt re-confrontation — an owner act); a LIVE row must also point to an existing skill — a consistency check, not the definition. Routing to a RESERVED type: **refuse and tell the user** the type is not yet populated.

| dispatch_type | status | skill |
|---|---|---|
| `research` | LIVE | `.claude/skills/research/SKILL.md` — research-type judgment: canonical shape, roles, gates, outputs |
| `code` | RESERVED — must not be dispatched until populated | none |
| `review` | LIVE (populated 2026-06-12, owner decision) | `.claude/skills/review/SKILL.md` — red-team judgment: attack lenses, severity taxonomy, verification discipline, the change-request report. **One artifact: `review.md`** (the synthesis — no `attacks.md`, no `findings.md`); `output_mode` picks chat vs `<working_folder>/review.md` (§14) |
| `plan` | RESERVED — must not be dispatched until populated | none |
| `suggestion` | RESERVED — must not be dispatched until populated | none |
| `experiment` | LIVE (populated 2026-06-14, owner decision) | `.claude/skills/experiment/SKILL.md` — falsification judgment: pre-registered criterion freeze, validity gates, SURVIVED/FALSIFIED/INVALID verdict (propose phase only — INVALID may be rendered here; SURVIVED/FALSIFIED rendered at the separate downstream run) |

## Pointers (single owners)

- **Form — record/sheet fill mechanics:** `register-dispatch` (`.claude/skills/register-dispatch/SKILL.md`; appender `.claude/skills/register-dispatch/append-dispatch.cjs`) — field tables, enums, the appender, the close row, `invoked_by`.
- **Definitions + skeleton:** inline in `register-dispatch` (field tables, enums, schema v0.6.0, annotated example) — read there, not the constitution. Constitution §5 (parameter reference) / §6 (skeleton YAML) are the upstream authority only.
- **Agent names:** `telemetry/agents/agent-pool.yaml`.
- **Anti-bias design:** `.claude/skills/anti-bias-vector-composition/SKILL.md` (the `check-tension` gate enforces it; the vault discovery `implementation/domainspec/vault/discovery/anti-bias-vector-composition/` is the knowledge home).
- **Init-time tensioning gate:** `check-tension` (`.claude/skills/check-tension/SKILL.md`) — the two independent agents that verify Tests 1–4 before the human confirm; only "both PASS" reaches the human.
