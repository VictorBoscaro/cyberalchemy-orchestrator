# Independent Review — Synthesis Dispatch

## Verdict

**AMEND**

The dispatch is schema-valid and substantially satisfies the approved Robot-Talks contract, but it
should not run until three contract gaps are repaired: the final reviewer is given an unpersisted
writer-owned frame, lifecycle receipt definitions omit required terminal-state fields, and no
owner records the human-gate presentation in `dialogue.md`.

## Deterministic validation

Command rerun:

```text
python .agents/skills/dispatch-spec/scripts/validate-dispatch.py internal-tools/need-driven-system-writing/robot-talks/2026-08-12-system-boundaries/synthesis-dispatch.json
```

Result:

```text
VALIDATION=pass
DISPATCH=internal-tools\need-driven-system-writing\robot-talks\2026-08-12-system-boundaries\synthesis-dispatch.json
```

The validator confirms the required top-level shape, step dependencies, gates, techniques,
boundary evidence, subagent strategy, stop conditions, observability, and promotion guardrails. A
passing deterministic result does not resolve the three semantic handoff and lifecycle issues
below.

## Checks that pass

### Schema validity

**PASS.** The repository-local validator passes. Every step has a recognized pattern, non-first
steps name prior inputs, the validation step names an evidence artifact, stop conditions are
explicit, and observability events are grouped under one `dispatch_id`.

### Eligible evidence restriction

**PASS.** All four declared review artifacts exist and end with an `Eligible for synthesis`
section. Their numbered item counts match the dispatch's expected handles:

| Review | Eligible items | Expected handles |
|---|---:|---|
| `01-author-sovereignty.review.md` | 4 | `01.1`–`01.4` |
| `02-shared-principles.review.md` | 4 | `02.1`–`02.4` |
| `03-operational-architecture.review.md` | 5 | `03.1`–`03.5` |
| `04-formalization-automation.review.md` | 5 | `04.1`–`04.5` |

The eligibility rule is strict: only those numbered formulations may support synthesis. Original
reports and other review sections are provenance or audit context only and may not strengthen a
claim. This implements `dialogue.md` Conversation protocol item 4.

The reviews use inconsistent heading levels (`#` in 01 and 04, `##` in 02 and 03), but the
dispatch identifies the final section by heading text rather than level. This is not a blocked
handoff; the extractor should accept heading levels 1–6 and the final matching section only.

### Output ownership and role separation

**PASS, subject to the repairs below.** The synthesis writer owns `s01`–`s02`, `findings.md`, and
the synthesis-phase append to `dialogue.md`. A different agent owns `s03` and only
`reports/05-synthesis.review.md`. The independent reviewer is forbidden to edit or silently repair
the synthesis. Root owns scheduling, receipts, closeout, and gate relay rather than substantive
synthesis or review.

### Independent final review

**PASS.** `s03` requires a distinct reviewer, verifies every tension and coverage entry against the
eligible formulations, produces a named evidence artifact, and returns only `PASS` or `BLOCK`.
`BLOCK` stops the current route before the human gate; any repair is assigned to a new synthesis
subagent route rather than to the reviewer.

### No implementation and promotion authority

**PASS.** Scope, step stop conditions, gates, boundary authority, promotion guardrails, and global
stop conditions all deny implementation, promotion, tension resolution, or inference of human
approval. This is consistent with `dialogue.md`, which authorizes exploration but no
implementation.

### Human gate

**PASS, subject to the session-record repair below.** `s04` can run only from a `PASS` review
decision, presents the allowed dispositions, and stops without treating silence or prior approval
as a decision. `g06` preserves the human's exclusive authority over every tension.

### Root is orchestration-only

**PASS, subject to a narrowly mechanical logging exception below.** The dispatch consistently
forbids root from extracting eligible findings, synthesizing, amending claims, reviewing, or
disposing tensions. Scheduling, lifecycle closeout, verbatim artifact relay, and append-only
recording of an event that root itself performs are orchestration work.

## Required repairs

### 1. Remove the writer-owned transient frame from the independent review handoff

**Problem:** `s01` outputs `eligible-evidence-frame` as `kind: frame`, not as a persisted artifact.
That handoff is possible inside the same synthesis-writer run from `s01` to `s02`, but `s03` belongs
to a different agent. No receipt stores the frame, while the root role permits relaying artifacts
and gate questions, not reconstructing or authoring evidence frames. More importantly, an
independent reviewer should derive eligibility from the review-owned source, not depend on the
synthesis writer's extraction.

**Exact repair:**

1. Remove `{ "kind": "frame", "ref": "eligible-evidence-frame" }` from `s03.inputs`.
2. Require the final reviewer to independently extract the numbered formulations from
   `source_artifacts.review_artifacts` and compare them with the coverage ledger in `findings.md`.
3. Amend `b03-independent-review.contract` to state that the reviewer receives frozen
   `findings.md`, the synthesis-phase `dialogue.md`, and the four review artifacts; the writer's
   internal frame is neither an authority nor a required handoff.
4. Keep `eligible-evidence-frame` as an internal `s01 → s02` handle only, or persist it as a clearly
   non-authoritative audit artifact if later evidence demonstrates a need. Do not make persistence
   necessary merely to satisfy the component design.

This repair removes an impossible or ambiguous cross-agent handle while strengthening reviewer
independence.

### 2. Make the receipt contracts include the lifecycle fields the strategy requires

**Problem:** `subagent_strategy.receipt_requirements` names `agent_id`, `role_id`, `spawn_status`,
`join_status`, `close_status`, and `reroute`, but the concrete receipts
`r01-synthesis-subagent.required_fields` and `r02-independent-review-subagent.required_fields` omit
those fields. They also omit `receipt_artifact`, which Dispatch Spec requires when a completed join
is claimed. As written, a producer can satisfy its local receipt definition without proving the
terminal lifecycle that the route requires before the human gate.

**Exact repair:**

1. Add `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, `receipt_artifact`, and
   `reroute` to both concrete receipt `required_fields` arrays. `residue` is already present.
2. Add `receipt_artifact` to `subagent_strategy.receipt_requirements`.
3. State that `receipt_artifact` is required when `join_status=completed`; blocked, timed-out, or
   handed-off states instead require named `residue` and a non-empty `reroute`.
4. Before `s04`, populate `subagent_lifecycle.agents` from those receipts and require terminal join
   and close states for both agents. Do not change `status: none` before runtime; it is truthful for
   an approved route that has not run.

### 3. Assign the post-review and human-gate session update without making root a synthesizer

**Problem:** `s02` instructs the synthesis writer to append a `pending independent-review` state to
`dialogue.md`. After `s03` passes, the reviewer may write only its review artifact, and `s04` emits
only a handoff and trace events. Consequently the session record can remain falsely pending after
review and does not record that the human gate was presented. The Robot-Talks persistence contract
requires `dialogue.md` to be updated after synthesis and the human gate
(`.agents/skills/robot-talks/SKILL.md:87-91`).

**Exact repair:**

1. Add `dialogue.md` as an `s04` output.
2. Authorize root to append only a mechanical gate record containing: the final review path and
   `PASS` verdict, both agents' terminal lifecycle status, the gate-presentation date, and
   `human disposition: pending`.
3. Add a boundary applying to `s04` that limits root's write to those lifecycle facts, forbids any
   change to findings or tension wording, and forbids recording a disposition before the human
   supplies one.
4. Amend `root_role` and `g04-root-orchestration-only` to make explicit that append-only recording
   of the review and gate events is lifecycle bookkeeping, not substantive authorship.
5. Retain the existing rule that actual human dispositions and any follow-up links are written only
   under a subsequent authorized route after the answer exists.

## Final assessment

The route is not blocked on research, missing reviews, schema invalidity, or absent authority. Its
substantive safeguards are strong: eligible inputs are bounded, synthesis and review are separated,
root cannot author conclusions, final review is mandatory, and the human gate stops all action.

The three repairs are required before execution because they close a real cross-agent handoff gap,
make lifecycle proof internally consistent, and prevent the durable session record from stating a
stale phase. After those exact amendments and a second deterministic validation pass, the dispatch
is eligible to run.

## Repair verification — 2026-08-12

**Verdict: PASS**

This verdict applies to the repaired `synthesis-dispatch.json` and supersedes the earlier `AMEND`
for that version. No synthesis or dispatch execution was performed during verification.

### Deterministic validation — PASS

The repository-local validator was rerun against the repaired file and returned:

```text
VALIDATION=pass
DISPATCH=internal-tools\need-driven-system-writing\robot-talks\2026-08-12-system-boundaries\synthesis-dispatch.json
```

### Repair 1: independent eligibility extraction — PASS

- `s03-independent-final-review.inputs` no longer contains the transient
  `eligible-evidence-frame`; it receives `findings.md`, `dialogue.md`, and the four review
  artifacts.
- Its evidence contract now requires the reviewer to independently extract every numbered item
  from each final `Eligible for synthesis` section, accepting heading levels 1–6, and compare that
  extraction with the `findings.md` coverage ledger.
- `b03-independent-review` explicitly says the writer's frame is neither authority nor a required
  cross-agent handoff.

The frame is now confined to the same-writer `s01 → s02` handoff, so no unpersisted writer-owned
state crosses into independent review.

### Repair 2: terminal lifecycle receipts — PASS

- `subagent_strategy.receipt_requirements` now includes `receipt_artifact` in addition to
  `agent_id`, `role_id`, `spawn_status`, `join_status`, `close_status`, and `reroute`.
- Two concrete top-level `lifecycle_receipts` — `r01-synthesis-subagent` and
  `r02-independent-review-subagent` — require all strategy fields, including terminal lifecycle
  state and `receipt_artifact`.
- Each receipt carries the conditional contract that a completed join requires
  `receipt_artifact`, while blocked, timed-out, or handed-off states require named residue and a
  non-empty reroute.
- `subagent_lifecycle.instruction` requires both attempted roles to be populated from these
  receipts and reach terminal join and close states before `s04` or any success report.

The separate `boundary_evidence.receipts` are now clearly named evidence-handoff receipts rather
than lifecycle receipts. Their smaller field sets do not weaken the dedicated lifecycle contract.
Keeping `subagent_lifecycle.status: none` before runtime remains truthful.

### Repair 3: append-only final gate record — PASS

- `s04-human-gate-handoff.outputs` now includes `dialogue.md`.
- Its evidence expectations require root, before presenting the gate, to verify both terminal
  lifecycle entries and append only the review path and `PASS`, terminal lifecycle states, gate
  date, and `human disposition: pending`.
- `b06-mechanical-final-gate-log` constrains that write and blocks any change to findings, tension
  wording, synthesis claims, prior content, or an as-yet-unprovided human disposition.
- `boundaries.root_role` and `g04-root-orchestration-only` explicitly classify this append as
  orchestration bookkeeping while continuing to forbid root from extraction, synthesis, review,
  claim amendment, or disposition.

This closes the stale-session-state gap without making root a substantive author.

### Execution eligibility

The repaired dispatch is schema-valid, has no impossible declared handoff, assigns each output and
state write to a bounded owner, preserves independent final review, requires terminal lifecycle
proof, stops at the human gate, and grants no implementation or promotion authority. It is
eligible to run under its existing approval and stop conditions.
