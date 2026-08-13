# Review — external composition research dispatch proposal

## Coverage

| attacker | lens | targets attacked | findings raised | zero-findings defence |
|---|---|---|---:|---|
| independent contract reviewer | fidelity / governance | `advice.md`, `route-receipt.json`, `opening-record.json`, `human-confirmation-sheet.md` | 1 | n/a |
| independent contract reviewer | mechanics / operability | `advice.md`, `route-receipt.json`, `opening-record.json`, `human-confirmation-sheet.md` | 1 | n/a |

Both lenses covered the complete proposal corpus. The checks included the accepted external RID,
the `research`, routing, lifecycle, and registration contracts, the canonical registry, the
legacy-managed compiler, its connected-topology test, agent-pool membership, record fields,
anti-bias state, corpus boundaries, verdict rules, outputs, and the human gate. No research,
registration, compilation, opening, or source browsing was performed.

## `route-receipt.json`

No surviving finding. The receipt matches the canonical live registry route: `research`,
`legacy-managed`, and `host/inherited@1`.

**Verdict:** KEEP

## `advice.md`

No surviving finding. It remains design advice, preserves composition as the general question,
uses four materially different collection perspectives, bounds source quality and volume, and
does not claim that one domain supplies the general theory.

**Verdict:** KEEP

## `opening-record.json`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 1 | `opening-record.json` | `"connections": [` followed by `{"from": "explorers", "to": "synthesizer", "type": "sequential"}` and three further connected edges | CRITICAL | Do not submit this record to confirmation or compilation. Either implement and govern downstream-input materialization, then revalidate this exact topology, or replace it with an explicitly staged set of separate connectionless dispatches, each with its own route, record, confirmation, artifacts, and close. |

The canonical research shape is semantically appropriate, but the current compiler rejects every
non-empty `connections` array before writing a launch plan. Removing the edges would not repair the
record: it would launch all nine seats independently with empty input manifests and falsely imply
that the writer, skeptics, and approver consumed upstream work.

The remaining static contract checks pass: schema and dispatch type match the route; the working
folder is repo-relative and outside `vault/`; `anti_bias_mode` is explicitly disabled and overlay
fields are absent; all nine unique names exist in the agent pool; roles, models, positive token
budgets, group cardinalities, prompts, gate separation, verdict vocabulary, and dedicated
approver shape are internally consistent. The requested external web capability still needs an
effective-tool check before any future launch because `host/inherited@1` only inherits what the
host actually supplies.

**Verdict:** FIX

## `human-confirmation-sheet.md`

| # | file | evidence (quoted from the artifact) | severity | proposed fix |
|---|---|---|---|---|
| 2 | `human-confirmation-sheet.md` | “The proposed output budget is 48,000 tokens across nine seats, with at most two synthesis/review loops.” | MAJOR | State separately that `max_loops: 2` is the whole-sequence rerun ceiling, while the proposed connected edges declare `zig-zag loop_cap: 2` and `feedback loop_cap: 1`; do not describe `max_loops` as the synthesis/review loop count. |

The sheet correctly says `BLOCKED BEFORE CONFIRMATION`, identifies the exact topology blocker,
forbids a `GO`, states that no lifecycle mutation occurred, exposes the web requirement and output
destination, and offers only honest next decisions. Its loop description is nevertheless
load-bearing confirmation information and currently conflates two distinct controls.

**Verdict:** FIX

## Change requests

1. **CRITICAL** — Keep the connected opening record blocked until governed downstream-input
   materialization exists, or redesign the work as separately confirmed and closed connectionless
   dispatches with artifact-based handoffs.
2. **MAJOR** — Correct the human sheet's loop semantics before it is used as the basis for any
   future confirmation.

## Review outcome

- Overall verdict: **FIX**
- The proposal is safe in its current state only because the sheet explicitly blocks execution.
- The next legitimate action is revision, not confirmation, compilation, registration, or launch.
- `exit_reason`: `resolved` (verified change requests delivered)
- `agents_spawned`: 1 independent reviewer; no research agents launched
