---
name: research
description: >
  Subagent dispatch for synthesis, adversarial check, multi-perspective audit, or
  precedent sweep — routed here from domainspec-subagents-strategy as the work-type
  skill for `dispatch_type: research`. Defines research-type judgment only: roles as
  epistemic functions, skeptic gates, the canonical shape, and the
  findings verdict matrix. Trivial single lookups stay inline and never reach this skill.
---

# research — type skill for `dispatch_type: research`

**Purpose (read first).** Research is **not** novelty-hunting. Its job is to find what **already
exists and can be used** — owned, citable results deployable as building material. A
`build-from-owned` finding is a **first-class success**, not a kill; `novel-attempt`
(precedent-clean) is one outcome among several, not the goal. (Normative orientation — what we
value, not a measured frequency.) Finding an owner is a *win*: owned kills a novelty *claim*,
never a *use*. The only failures are `no-witness` and `tautological`.

This skill owns research dispatch judgment. `register-dispatch` owns whether and how the current
compatibility record represents that route. Division of responsibility:

- **When/whether to delegate and semantic routing** —
  `.claude/skills/domainspec-subagents-strategy/SKILL.md`.
- **Session-owned confirmation/register/run/close sequencing** —
  `.claude/skills/subagents-dispatch-lifecycle/SKILL.md`.
- **Research judgment, topology, evidence, outputs, and verdicts** — this skill.
- **Record/sheet mechanics** (the two appends, the appender, validation) —
  `register-dispatch` (`.claude/skills/register-dispatch/SKILL.md`).
- **Field definitions** — inline in `register-dispatch` (read there). This skill defines no persisted
  field; it says which **values** a good research dispatch puts in them.

## Initial-definition precondition

Before selecting research roles or proposing a governed
research dispatch, require `<research-folder>/research-initial-definitions.md`. If it is missing,
stop research design and route to `.claude/skills/research-initial-definitions/SKILL.md`; resume only
after that informational context exists.

Read the complete initial-definitions document before proposing the research. It supplies business
context, purpose, the refinable research question, confirmed product constraints, the current
evidence baseline, and known gaps. It does not define research methods, sources, roles, topology,
budgets, gates, or expected findings; those remain owned by this skill and the dispatch lifecycle after the
precondition is satisfied.

## Roles as epistemic functions

Each role guards a distinct failure mode; no agent guards two.

| agent `role` | guards against | model guidance |
|---|---|---|
| `explorer` | monoculture — investigates one declared research perspective | lighter — sweeps are mechanical |
| `skeptic` | folklore / vacuity — attacks **one named gate** each | heavier — adversarial work is hard |
| `writer` | "great research, no record" — the synthesizer, **conventionally a single writer (the §6 skeleton's `n: 1`)** | heavier for heavy synthesis |
| `auditor` | "passed because nothing was checked" — meta-evaluates, **placed by its incoming edge, downstream of the reviewers**, owns the verdict matrix | mid — checking, not generating |

A group's function is read off its agents' roles, its workflow position off its `connections`.

The model column is **guidance, not law**: `model` is chosen per agent by task difficulty
using the field contract in `register-dispatch`, and the human validates it at the confirm gate.

There is no `evaluator` role — criteria-scoring is a `skeptic` with a stated gate.

## Skeptic gates

One gate per skeptic, never two:

- **precedent** (ownership attribution — formerly `precedent-kill`) — is this already owned?
  Find the owner, not just "something similar". **Finding an owner is NOT a kill** — research
  exists to find what *already exists and can be used*, not only what is new. A found owner is a
  *positive* result: it *labels* the candidate `build-from-owned` (owner exists, repo does not
  yet deploy it — cite honestly and build) or `already-deployed`; an empty search certifies
  `precedent-clean` → `novel-attempt`. This gate never emits a terminal KILL.
- **non-vacuity** — build the smallest concrete witness by hand, or force a closed negative.
- **definitional-soundness** — does it collapse to something already named, re-skinned?

Use distinct skeptic gates when several skeptics run. The terminal KILLs come only from `non-vacuity` (no-witness) and
`definitional-soundness` (tautological) — never from `precedent`.

## Canonical research shape

```
explorers (a group of `explorer`s, n 2–4, with distinct research perspectives)
   │ sequential
synthesizer (1 `writer`) ◀──zig-zag──▶ reviewers (`skeptic`s;
   ▲                          │         robot_talks when the question
   └┄┄┄┄ feedback (conditional) ┄┘       needs confrontation, not collection)
```

The feedback back-edge is instantiated only when there is a reviewer/auditor group AND
material may be missing (Principle 6) — never by default. The older research pattern "writer drafts
candidates before skeptics attack them" **is** this synthesizer-midfield: same flow,
chassis names. The `auditor` sits in an optional group (its single agent's role is
`auditor`) placed by its incoming edge, downstream of the reviewers — which also makes it
the natural **dedicated `final_approver`** (Principle 12:
sole member, no other work, never in a working group).

**Early stop:** a confirmed kill — no candidate survives its collapse-test (no-witness or
tautological) — ends the dispatch early: bank the typed negative, then CLOSE `exit_reason:
resolved` (a confirmed-kill early-stop is a successful close, not an error). **Being OWNED is
NOT a confirmed kill and does not early-stop** — a found owner relabels the candidate
`build-from-owned` and the dispatch continues; the lone exception is owned **and already
deployed**, recorded as `already-deployed` provenance (still not a negative).
If the dispatch declared a dedicated approver and an early stop prevents that approver from acting,
stop for a new explicit approval decision. Never substitute `parent` silently. The dispatch closes
only after the confirmed approver accepts the typed negative.

## Longer sweeps: propose the structure first

For a short research — one explorer group, one skeptic gate, and a bounded corpus — prepare the
complete dispatch directly for lifecycle confirmation. For a large sweep — multiple explorer
groups, several stages, or a deep or multi-corpus search — first show the proposed research shape:
the research perspectives, groups, connections, expected outputs, and the one question the sweep answers. This is
a research-specific planning checkpoint, not a generic router mode or a separate work type.

Keep the proposal a decisive recommendation, not a survey of options; the user's accept/decline is the
only branch. On **accept**, resolve the complete dispatch and hand it to the lifecycle for final
confirmation. On **decline**, simplify the sweep and return one complete dispatch for confirmation;
decline means "run it lean," never "abort" or "skip confirmation." Silence is not acceptance.

## How to run

Hand the confirmed research shape to `subagents-dispatch-lifecycle`. The host/runtime owns launch,
dependency scheduling, retries, and effective inputs; this skill only supplies the research graph
and the semantic conditions on its handoffs.

## Research outputs

- **n ≥ 2:** `<working_folder>/research.md` (collected returns, verbatim) +
  `<working_folder>/findings.md` (cited synthesis — every load-bearing claim cites the
  collected return it rests on; the `final_approver` checks this).
- **n = 1:** `<working_folder>/findings.md` only.
- `working_folder`: when one feature clearly owns the research question, use
  `docs/features/<feature>/research/<dispatch-slug>/`. Use
  `research/<dispatch-slug>/` only for repository-wide research with no clear feature owner.
- The research requirement is the FILES, not who writes them — the strategist may
  write `findings.md` itself or delegate (no mandatory writer-agent machinery).

**Findings shape** — per candidate, a row in the verdict matrix. **Ownership is a label, not a
verdict**: the `owner` column is always filled (a citation, or `precedent-clean`) and being owned
never puts KILL in the verdict column:

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict | use-mode |
|---|---|---|---|---|---|

- **GO** — witnessed and sound. `use-mode` says how: `build-from-owned` (owned but unused — name
  the owner + the artifact/job it builds; cite honestly, never claim novel), `already-deployed`
  (owned and already wired — provenance only), or `novel-attempt` (precedent-clean — name the
  claim, its anchor, and the first obligation a follow-up faces). An owned-but-unused result is a
  GO, not a negative.
- **KILL** — **only** no-witness (non-vacuity) or tautological (definitional collapse); banked as
  a **typed negative**: what it would have contributed + the exact fact that zeroed it. **Owned is
  not a KILL.** A clean KILL is a successful run.

Close with the one-line answer to the dispatch `goal`. Research acceptance includes the citation
check above; `register-dispatch` owns the persisted close vocabulary.

## Standing rules

1. **Claim ≤ proof:** for research, demote, never inflate.
2. **Keystone claims carry their collapse-test inline** — the one fact that would zero them, same line.
3. **Precedent-first** — no "novel" verdict ships before a `precedent` skeptic ran. But a found
   owner is **not** a kill: research exists to find what already exists and can be used. A found
   owner relabels the candidate `build-from-owned` (cite, deploy, never claim novel); owned demotes
   only the novelty claim, and every artifact touching an owned result carries its owner label.
4. **Read-only by default** — research agents write only into `working_folder`, never the source tree.

## Names

Draw `agent_name` from `telemetry/agents/agent-pool.yaml` (ordered `role_fit`).
Prefer the primary `role_fit` entry and a `field` fit to the corpus. Never reuse a name
within one dispatch — the skeptic/auditor prohibition is the hard case of it. Never
invent a name outside the pool.

## Profiles

Repo-specific profiles may specialize this skill — the domainspec-lean-formalization
`research` skill (`domainspec-lean-formalization/.claude/skills/research/SKILL.md`,
sibling repo; unverifiable from this repo) is the math profile (old pre-v0.5.x schema,
pending realignment), as is
`vault/constitution/research-constitution.md` here (cite as pending realignment; do not
import its R-numbered machinery).
