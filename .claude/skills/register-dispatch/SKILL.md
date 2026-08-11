---
name: register-dispatch
description: Own and validate the append-only telemetry row mechanics for a subagent dispatch. Use through subagents-dispatch-lifecycle for parent-bound work, or directly only for an explicitly authorized standalone compatibility record. Dispatch types and availability come exclusively from the canonical infrastructure registry.
---

# register-dispatch

Record **one row per dispatch** in the repo ledger `telemetry/agents/subagents-dispatch.yaml`,
under the ledger schema declared by the canonical dispatch-type registry. A dispatch contributes exactly
**two appends** (constitution Principle 3): the **dispatch row** (the spec, at dispatch) and
the **close row** (`close_of` + outcome, at termination). The ledger is append-only — rows
are never edited in place.

## When to use

- Through `dispatch_workflow open` and `close` for every parent-bound dispatch. Those commands call
  this skill's appender; do not invoke it a second time.
- **Principle-2 gate:** append only after the human's explicit confirm of the sheet —
  the gate is coordinated by `subagents-dispatch-lifecycle` / constitution P2;
  never append before it.
- Register **once per dispatch**, not once per agent or per group. A dispatch with three
  groups and six agents is **one** row; `groups` is a JSON column.
- At termination, append the **close row** (see below). Both appends use the same appender.
- Skip when `domainspec-subagents-strategy` keeps the work inline or the selected capability owns a
  bounded, unregistered helper workflow. Do not infer that classification from agent count alone.

## The dispatch row

The appender **validates the incoming record strictly** and rejects (exit 2) on any
schema violation, listing every error. Unknown keys are rejected — keys in constitution
§7's removed table (`success_metric`, `constraints`, `created`) get an explicit
**removed by schema v0.5.2** error (historical: those keys were removed at v0.5.2); old
ledger-row-only keys (`status`, `agents` top level, `corpus`,
`topic_slug`, `session`) get a **legacy ledger-row key, not in the current schema**
error.

**Not enforced by the appender** (sheet-design rules owned by the selected capability and
the dispatch lifecycle): `final_approver` working-group membership (P12 no-self-approval),
the `dispatch_id` `YYYY-MM-DD-<slug>` format, and the `layers > 1`
not-on-a-zig-zag/feedback-endpoint corollary.

### Top level

`anti_bias_mode` is required and must be `enabled` or `disabled`. With `enabled`,
every group containing at least two agents must declare a non-empty `anti_bias`,
every agent in that group must declare a distinct non-empty `angle`, and
`anti_bias_pairs` must cover every unordered pair of agent indices exactly once.
`anti_bias_global` is additionally required when at least two groups each contain
at least two agents. With `disabled`, `anti_bias_global`, every group-level
`anti_bias`/`anti_bias_pairs`, and every agent-level `angle` are forbidden.

| Field | Required | Meaning / constraint |
|-------|----------|----------------------|
| `dispatch_id` | ✅ | Unique id, `YYYY-MM-DD-<slug>` (§5). Dedup key — re-registering the same id is a no-op. |
| `schema_version` | ✅ | Must equal `ledger_schema_version` from `implementations/contracts/dispatch-type-registry.v1.json`. |
| `dispatch_type` | ✅ | Must equal the resolved `ledger_dispatch_type` from the canonical registry. The appender rejects unknown and RESERVED values. This skill does not enumerate or route types. |
| `goal` | ✅ | Non-empty string — the human's objective, one or two sentences. |
| `context` | ✅ | Non-empty string — 2–4 sentences of framing; the only channel subagents get (§5). |
| `max_loops` | ✅ | Integer 1..5 — whole-sequence re-run ceiling. |
| `final_approver` | ✅ | Non-empty string: `parent` or the `agent_name` of a dedicated approver agent (no self-approval — P12). |
| `groups` | ✅ | **JSON column** — non-empty array of group objects (below). |
| `meta` | – | If present, must be boolean `true` (planning/framework dispatches only). |
| `parent_dispatch_id` | – | String (or null/omitted) — only on a dispatch planned by a meta dispatch. |
| `working_folder` | research/experiment: ✅ | Repo-relative path where outputs land. **Required when `dispatch_type` is `research` or `experiment`; must never start with `vault/`.** **Optional for `review`** — review is inline by default (findings delivered in chat, since 2026-06-16); set it only when the user confirms persistence at the gate. Whenever a `working_folder` is set, the lifecycle confirms the path with the user. |
| `output_mode` | review: ✅ | **Review-only** row field: `inline \| persisted` — where the single `review.md` artifact lands. **Required when `dispatch_type` is `review`**, declared at the confirm gate and recorded on the row (never inferred from an absent `working_folder`). `inline` (default) → rendered in chat, `working_folder` must be **absent**; `persisted` → written to `<working_folder>/review.md`, `working_folder` **required**. Rejected (exit 2) on any non-`review` type. |
| `code_contract` | code: ✅ | **Code-only** JSON object. Pins `type_skill_ref`/digest, `work_pack_ref`/digest, `test_spec_ref`/digest, and a closed `domainspec-code-readiness@1` `readiness_ref`/digest; declares `brownfield`, concrete repo-contained `write_scope`, exact `validation_commands`, and canonical group IDs. The appender verifies every file, planner PASS/capability receipt, scope and exact DomainSpec topology before registration. Rejected on non-`code` types. |
| `invoked_by` | – | Email of the invoking human. If omitted, the appender resolves it from `git config user.email` (fail-soft: warning + `null`). Tooling-level extension, not in constitution §5 (owner-directed 2026-06-12), pending a one-line constitutional amendment. |
| `connections` | – | **JSON column** — array of `{from, to, type, loop_cap?}` objects (below). |
| `project_dir` | – | Control key: repo-root fallback when `CLAUDE_PROJECT_DIR` is unset. Never emitted to the ledger. |
| `created` | stamped | ISO timestamp **stamped by the appender** — supplying it is rejected (removed by v0.5.2). |

### Each object in `groups`

For an enabled fan-out group, `anti_bias_pairs` contains exactly `n*(n-1)/2`
objects. Each object has exactly `left_index`, `right_index`, `question`,
`left_position`, `right_position`, and `evidence`. Indices must satisfy
`0 <= left_index < right_index < agents.length`; positions must equal the
corresponding agents' `angle`; `question`, both positions, and `evidence` must be
non-empty strings. Duplicate or missing pairs are rejected. These conditional
fields are forbidden on singleton groups.

| Key | Required | Meaning / constraint |
|-----|----------|----------------------|
| `group_id` | ✅ | Stable id, unique among groups; the target of `connections` references. A group has **no** `role` field — its function is read off its agents' roles, and its workflow position off its `connections`. |
| `agents` | ✅ | Non-empty array of agent objects (below). They run in parallel. |
| `n` | – | Integer ≥ 1; if present must equal `agents.length`. |
| `robot_talks` | – | Boolean — agents discuss after their parallel runs (n ≥ 2 only meaningful). |
| `layers` | – | Integer ≥ 1 — sequential invocations of this group. Unenforced: a group with `layers > 1` may not sit on a zig-zag/feedback endpoint (§5 layers corollary). |

### Each object in `groups[].agents`

| Key | Required | Meaning / constraint |
|-----|----------|----------------------|
| `role` | ✅ | `explorer \| synthesizer \| skeptic \| writer \| auditor \| planner \| coder`. |
| `model` | ✅ | Non-empty string — concrete model id, picked by difficulty. |
| `token_budget` | ✅ | Positive integer — declared output-length target; **no unlimited default** (§5). |
| `initial_prompt` | ✅ | Non-empty string — the full briefing the agent receives at launch. Newlines are fine: JSON.stringify escapes them into the single-line JSON column. |
| `agent_name` | – | String from the agent pool, or `null`. |

### Each object in `connections`

Exactly `{from, to, type, loop_cap?}` — any other key is rejected.

| Key | Required | Meaning / constraint |
|-----|----------|----------------------|
| `from` / `to` | ✅ | Must reference declared `group_id`s. |
| `type` | ✅ | `sequential \| zig-zag \| feedback`. |
| `loop_cap` | – | Positive integer. Allowed **only** on `zig-zag`/`feedback`; **must be absent on `sequential`** (§5). |

## How to write the row

The skill ships a deterministic appender; do **not** hand-edit the YAML. To check the
ledger (e.g. `dispatch_id` uniqueness), use the Read tool — the append-only hook blocks
Bash access to the file, even read-only commands.

1. Consume the complete dispatch record produced by `domainspec-subagents-strategy`; do not
   reconstruct, omit, or reinterpret upstream-owned fields. Serialize that record as JSON.
2. Write that JSON to a temp file (use the Write tool, so it is UTF-8 — do **not**
   pipe JSON through PowerShell, which mangles it to UTF-16):
   `<repo-root>/.register-dispatch.tmp.json`
3. Run the appender (prefer the Bash tool):
   ```sh
   node "$CLAUDE_PROJECT_DIR/.claude/skills/register-dispatch/append-dispatch.cjs" \
        "$CLAUDE_PROJECT_DIR/.register-dispatch.tmp.json"
   ```
   It creates `telemetry/agents/subagents-dispatch.yaml` (and its directories) with
   a header if absent, validates the record against the registry-declared schema (exit 2 with the
   full error list on violation), appends one row, and is idempotent on
   `dispatch_id`. Before appending it structurally self-checks the existing ledger
   (line shapes, JSON values, unique ids) and refuses with exit 1 if the ledger is
   corrupt — fix the corruption before registering anything else.
   The repo root is resolved as `$CLAUDE_PROJECT_DIR`, falling back to a
   `project_dir` key in the record, then to the current working directory — so
   if the env var is unset, run the appender from the repo root (or set
   `project_dir` in the JSON) and pass the temp file as a relative path.
4. Delete the temp file.

## Closing a dispatch (the close row)

The ledger is **append-only** — never edit the original row to mark a dispatch
finished (a hook denies direct edits). Instead, append the **close row**: run the
same appender with a record that has `close_of` (the original `dispatch_id`)
instead of `dispatch_id`:

```json
{
  "close_of": "2026-06-12-residue-precedent-sweep",
  "exit_reason": "resolved",
  "agents_spawned": {"total": 3, "tree": {"explorer": 2, "writer": 1, "helpers": 0}, "loops_used": 1},
  "feedback_prompts": ["Explorers: the formal-methods return cites no post-2020 source — re-sweep 2020+ venues for the same pattern."],
  "invoked_by": "victorboscaro@gmail.com"
}
```

| Field | Required | Meaning / constraint |
|-------|----------|----------------------|
| `close_of` | ✅ | The `dispatch_id` being closed. Dedup key — re-closing the same id is a no-op. Warns (but still appends) if no matching dispatch row exists — an orphan close row indicates a Principle-3 breach upstream (the dispatch row should have been written at dispatch). |
| `exit_reason` | ✅ | Closed vocabulary: `resolved \| loop_ceiling_reached \| dissent_irreconcilable \| user_abort \| error`. Precedence when several apply: §5. |
| `agents_spawned` | ✅ | **JSON column** — object with numeric `total`, object `tree` (keyed by **agent** role — `explorer \| synthesizer \| skeptic \| writer \| auditor \| planner \| coder` — plus a `helpers` bucket), and **required** non-negative integer `loops_used` (constitution §5 lists loop iterations used as a component of `agents_spawned`, not optional). |
| `feedback_prompts` | – | **JSON column** — array of strings: each `feedback`-edge ask, recorded **verbatim** in the close row (Principle 3 / §5 `feedback` semantics). |
| `invoked_by` | – | As on the dispatch row: record value, else `git config user.email`, else `null` with a warning. Tooling-level extension, not in constitution §5 (owner-directed 2026-06-12), pending a one-line constitutional amendment. |
| `project_dir` | – | Control key: repo-root fallback when `CLAUDE_PROJECT_DIR` is unset. Accepted by the appender, never emitted to the ledger. |
| `closed` | stamped | ISO timestamp **stamped by the appender** — supplying it is rejected. |

A close record must **not** carry `dispatch_id`, a top-level `agents` array, or any
other key not in this table — unknown keys are rejected (exit 2).

## Grandfathering (old rows)

Rows written under pre-v0.5.2 schemas (recognizable by the absence of
`schema_version`; they carry old keys like `status`, `agents`, `success_metric`)
are **valid historical artifacts and are never re-validated** against the new
schema. The appender's pre-append self-check over the existing ledger is
**structure-only** (line shapes, JSON values, unique ids) so old rows keep
passing forever. Strict validation against the current registry schema applies **only to the incoming
record**, before append. The ledger file's own header comment is likewise
historical — written once at creation, never edited; it may lag the current schema.
