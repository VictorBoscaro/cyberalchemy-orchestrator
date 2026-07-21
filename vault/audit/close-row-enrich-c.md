---
tags: [vault, ledger, residue, category-theory, self-similarity]
node_type: audit
is_session: false
session_ref: 2026-07-21-root-hypothesis-tension
layer: domain
nature: technical
status: exploratory
veracity: high
conviction: medium
version: 0.1.0
last_updated: 2026-07-21
---

# AUDIT — does a close-row ever enrich `C`? (falsifier 1 of HYP-ORCH-FRACTAL)

> **Verdict: NO — and it is provable from the schema, not merely observed.** This **fires**
> falsifier 1 of [[framework-self-similarity]]: at the current ledger design the orchestration
> loop's close step is a **shadow** append, never a codomain enrichment. The finding is `veracity:
> high` because it follows from the appender's strict schema, not from a sample.

## The question

[[framework-self-similarity]]'s falsifier 1 asks: does any ledger close-row **enrich `C`** — add a
new distinction/type the vocabulary can now make (**structure**, [FRAMINGS.md F1](../../FRAMINGS.md)) —
or does every close merely **append state** against a fixed schema (**shadow**)? If no close ever
enriches `C`, the orchestration loop is a *thin/shadow* loop while the knowledge-ascension loop is
a *non-thin/structure* loop — **not the same structure**, and fractality drops to analogy on this axis.

## Method — decidable by construction, not by sweep

The `register-dispatch` appender validates strictly and **rejects unknown keys** (exit 2). A valid
**close row**'s entire admissible content is therefore fixed:

| Field | Kind | Can it add a distinction to the type vocabulary? |
|---|---|---|
| `close_of` | dedup key (a `dispatch_id`) | no — a reference |
| `exit_reason` | **closed enum** (`resolved \| loop_ceiling_reached \| dissent_irreconcilable \| user_abort \| error`) | no — a classifying map into a fixed **thin** object (a shadow, DEF-ORCH-003) |
| `agents_spawned` | JSON counts (`total`, `tree` by role, `loops_used`) | no — magnitudes (a shadow) |
| `feedback_prompts` | verbatim strings | no — natural-language content, not a type |
| `invoked_by` | email | no |

None of these is a codomain change. The **only** place the vocabulary (schema) evolves is a
`schema_version` **bump** (e.g. v0.5.2 → v0.6.0, retiring/adding keys) — a **governance act on the
appender**, at a different layer than the loop's close step. A close *cannot* add a distinction; it
records against the schema in force. (The [[ledger-enum-drift-finding]] out-of-enum `success` is a
**bypass/corruption**, not an enrichment — it confirms the enum is fixed, not that a close may grow it.)

## Consequence for HYP-ORCH-FRACTAL

- **Falsifier 1 fires** on the **current** ledger design: the orchestration-scale "enrich `C`" step
  — the moving part that must correspond to the ascension loop's codomain enrichment — is **absent**.
  So the `full+faithful` "≡" **cannot hold** as stated against today's ledger; the current-design
  instance of the hypothesis is **falsified**.
- What survives is **conditional**: fractality becomes *runnable* only if the ledger is redesigned so
  a close can carry a genuine codomain enrichment — i.e. **BL-3** (the typed-graph ledger). This
  **double-gates** HYP-ORCH-FRACTAL: below OBL-E3 (categoricity) **and** below BL-3 (enrich-capable
  close). It also tells BL-3 exactly what it must deliver for fractality to even be testable: a close
  step that changes what the vocabulary can distinguish.
- This is a **feature, not a defeat**: an asserted candidate counterexample is now an **adjudicated**
  one, and it names the concrete build (BL-3) that would move the hypothesis from falsified-at-current-
  design to runnable.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [[framework-self-similarity]] | `validates` | Fires its falsifier 1; converts an asserted counterexample into an adjudicated one and double-gates it on BL-3. |
| [[ledger-enum-drift-finding]] | `contextualizes` | The enum-drift bypass confirms the close vocabulary is fixed (not close-extensible) — supporting evidence, not enrichment. |
| [`.claude/skills/register-dispatch/SKILL.md`](../../.claude/skills/register-dispatch/SKILL.md) | `derives-from` | The strict close-row schema this audit reasons from. |
| [FRAMINGS.md](../../FRAMINGS.md) | `grounds` | F1 (shadow ⊕ structure) is the distinction the audit applies to the close-row. |
