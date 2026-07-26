# S-C (Boehm, Barry) — angle: the cost of the move binds — round 1 return

All 23 target_bindings hashes verified — every SHA-256 matches. Proceeding on the bound corpus.

## Verdict table

| item | verdict | destination path or em-dash | one-line reason |
|---|---|---|---|
| I1 | STAY | — | Complete experiment (criterion+experiment+findings); 10 external inbound refs in 6 files; no reader is failing to find it. |
| I2 | STAY | — | 10 inbound refs from the feature discovery + 7 outbound `../../../` links inside the tree; cheaper instrument: bidirectional pointer lines (~2 edits vs 17+). |
| I3 | STAY | — | The only failing reader is caused by two WRONG links, not wrong placement; fix `research-review/` → `research/review/` in place (2-line edit). |
| I4 | STAY | — | Zero inbound refs means the move is cheap, but it is also unpaid-for: no currently-failing reader is named; a pointer line from `docs/features/skill-control-center/` suffices. |
| I5 | STAY | — | 1 real inbound ref (`.gitignore:39`); no reader failing; a one-line "client case, not a governed experiment" disclaimer is cheaper than a second relocation. |
| I6 | STAY | — | 23 files reference `reviews/2026-*` paths, including executable tests and data JSON; highest move cost in the inventory, breaks code, buys nothing. |
| I7 | STAY | — | `docs/features/README.md:48` already legitimizes the feature-owned home; 13 files bind those paths; the gap is a missing written rule — a README paragraph, not a move. |
| I8 | STAY | — | Remedy is exactly the cheap instrument my angle prefers: one index row in `README.md`'s directory tables; the failing reader (any README navigator) is real and named. |
| I9 | STAY | — | Only 4 self-referential files reference it; moving a live dispatch's working_folder mid-flight breaks `dispatch-open.json` bindings and the hook-managed ledger close. |

## Cost ledger

**I1** — Search: `grep -r "experiments/skill-relationship-graph"` → 26 occurrences / 9 files; excluding self (experiment's own files, this dispatch's proposals): ~10 refs in 6 external files (`docs/features/skill-control-center/discovery/control-center.md` ×6, `architecture.md` ×1, `research/prompt-control-plane-foundations/research-initial-definitions.md` ×1, two skill-control-center experiment files). A move edits 6 files. Payer if moved: discovery readers whose links break. Payer if kept: nobody identified — it satisfies the experiment contract where it sits.

**I2** — Search: `grep -r "experiments/skill-control-center"` → 7 files (3 self/dispatch); plus `grep -c` inside `docs/features/skill-control-center/discovery/control-center.md` → 10 refs; plus 7 outbound `../../../docs/features/...` links in `experiments/skill-control-center/meta-orchestration/research.md` that a move re-depths. Total surface ≈ 17+ link edits across ≥4 files, plus the internal `frontend-context-pack.md`/`backend-task-session.md` refs. Cheaper instrument: a pointer line in the feature package to the experiment tree and vice versa (2 edits). Payer if kept: a future feature-package reader who must hop once — priced at one hop after the pointer lands.

**I3** — Search above surfaced the decisive fact: `control-center.md:559` and `:617` link to `../../../../experiments/skill-control-center/research-review/review.md`, and `ls` confirms `research-review/` **does not exist** — the reader is failing TODAY, and a move fixes nothing because the links are wrong, not the location. Cheaper instrument: correct the two links to `research/review/review.md`. Payer either way: the discovery reader clicking "Research review".

**I4** — Search: `grep -r "final-review"` → 3 files, all this dispatch's own proposals. Zero organic inbound references; `ls docs/features/skill-control-center/` shows no `reviews/` dir exists to receive it. Cost of moving ≈ 0 link edits — I state that honestly; my STAY rests on the absent buyer, not on cost. Payer if kept: a hypothetical auditor of `implementations/` looking for its PASS record (unnamed — see Claim <= proof). Cheaper instrument: one pointer line.

**I5** — Search: `grep -r "foodstogo-jbp-2025"` → 4 files: 3 self-proposals + `.gitignore:39` (`/experiments/foodstogo-jbp-2025/out/`). `git log` shows commit `4e69b2f` already relocated it once. A move costs 1 gitignore edit plus a second provenance rupture for a tree with client deliverables. This is the cheapest possible move in the inventory; if lineage wins crosstalk here, my cost objection is weak and I say so. Payer if kept: the reader who infers experimental provenance from the directory name — served by a one-line disclaimer.

**I6** — Search: `grep -rl "reviews/2026"` → 23 files, including `implementations/tests/runtime/test_orchestration_bridge.py`, `test_host_dispatch_hook.py`, `internal-tools/ui-experimentation/data/dispatches.json`, work-pack descriptors, plans, sessions. Moving breaks running code and data, not just prose. Payer if moved: everyone. Payer if kept: none demonstrated.

**I7** — Search: `grep -rl "docs/features/agents-communication-infra/experiments"` → 13 files (SWU descriptors, `.codex` proposals, sessions, the probe's own README). And `docs/features/README.md:48` explicitly lists `experiments/` as feature-package content — so the feature-owned home is not lawless, it is documented; only the tiebreak rule ("governed/falsifiable → top-level; feature-embedded probe → feature") is unwritten. Cheaper instrument: write that rule where both homes' readers look. Payer if consolidated by force: 13 files of edits plus the probe's cohesion with its work-pack.

**I8** — Search: `grep "experiments/" README.md` → 0 matches; absence confirmed. Cost of the fix: one table row. The failing reader is concrete: anyone navigating by README's directory tables cannot discover `experiments/` exists. This is the inventory's best cost-per-benefit action and it is an edit, not a move.

**I9** — Search: `grep -rl "artifact-placement-adjudication"` → 4 files, all inside the working_folder itself. Moving it mid-dispatch invalidates the paths in `dispatch-open.json` and collides with the CLAUDE.md rule that hook-managed closes are written against the opened paths. Payer if moved: the parent's own close hooks.

## What my angle cannot see

The strongest objection, in its best form (declared-rule angle on I2): "Your ledger prices a move at N edits **once**, but prices the non-move at **zero**, because the readers harmed by a split home are future and unnamed — status-quo bias by construction. `docs/features/README.md` says the package keeps its discovery, specs, reviews and work-pack together; the recurring search cost of the split compounds per reader forever, and your grep can never count readers who haven't arrived." I concede the asymmetry is structurally real — inbound-reference counting is blind to recurring navigation cost. I hold the verdict anyway, because the concession is answerable inside my own instrument set: bidirectional pointers reduce the recurring cost to one hop at ~2 edits, versus 17+ edits plus a `../../../` re-depth for the move, and no observed reader failure (the only observed failure, I3's dangling links, is a typo the move would not fix). Where I genuinely yield ground is I5: its move cost is one line, so if the lineage angle shows the name asserts false provenance, cost cannot carry a veto there.

## Claim <= proof

Asserted without counting — treat as low-confidence:
- Muscle-memory, external-bookmark, and "git-blame continuity for readers" costs: invoked generically, never measured; `git mv` + `log --follow` preserves most blame utility, so my headline framing may overstate this.
- The I4 "auditor of implementations/" reader who would benefit from relocation: hypothesized, not observed in any file.
- "research/ is the conventional home for dispatch working folders" (I9): supported by one sibling example (`research/prompt-control-plane-foundations/`), not a written rule.
- The recurring per-reader cost of I2's split home: I neither measured it nor can; my 2-edit pointer remedy assumes one hop is acceptable without evidence about actual reader traffic.
- I5's claim that a disclaimer line serves the misled reader as well as a move: untested; no such reader has been observed either way.
