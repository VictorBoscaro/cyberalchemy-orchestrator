# R-B (Randell, Brian) — lens: evidence sufficiency — round 1 review of S-B

## Verdict

FIX

## Findings

**1. I7 — a cited commit that does not cover half the object it is cited for. CRITICAL.**
Subject's claim: *"`git log` on the two subfolders: `53cff55 feat: record the rejected skill-protocol-compilation prototype` — the prototype's own history frames it as belonging to that feature's decision record."*
Record: `git log --oneline -- docs/features/agents-communication-infra/experiments/bus-publication-probe/` → `ca560b8 docs: expand vault, essays, research, and session logs`. `53cff55` touches only `skill-protocol-compilation/` (10 files, verified via `git show --name-only 53cff55`). The other subfolder was landed inside a 63-file omnibus commit whose subject names neither the feature nor the probe. One commit was presented as the history of two directories; the actual history of the second is a bulk drop with no individual provenance. Attack (1). Correction: I7's STAY rests on evidence for one subfolder only; `bus-publication-probe/` has no lineage record at all and must be marked unproven.

**2. I2/meta-orchestration — the split is refuted by the subject's own decisive rule. CRITICAL.**
Subject's claim: *"`meta-orchestration/` was born in `22cbebb`, the same commit as I1 … it stays with what it produced (I2's root), not with what research/ produced."*
Record: `git log --oneline -- experiments/skill-control-center/meta-orchestration/` → `22cbebb` only. `git log --oneline -- experiments/skill-control-center/research/` → `06bd467`, `583683f`, `22cbebb`. `git show --stat 22cbebb` shows `meta-orchestration/{findings,research}.md` and `research/{findings,research}.md` created in the *same* commit. The subject declares same-commit coupling "the load-bearing fact" for moving research/ (583683f), then discards it for meta-orchestration/ — where it points the other way — and substitutes topical content (`grep '../../..'`, which I reproduced: the links do cite `agent-provenance-telemetry` paths). Both attacks: the rule is applied selectively (1), and "cites APT paths" is a derives-from claim doing belongs-with work (2). Correction: under same-commit coupling, meta-orchestration/ and research/ share one birth event; the three-way SPLIT has no evidentiary basis and collapses to a two-way at most.

**3. I2/I3 — same-commit coupling proven, but the destination inference is unargued. CRITICAL (attack 2, primary target).**
Subject's claim: *"That is producer→target in the same breath — stronger than 'it came from here,' it is 'this commit's whole point was to hand this off there.'"*
Record: `git show --stat 583683f` reproduces the subject's four-file stat exactly (discovery/control-center.md 478+, research-review/review.md 92+, research/findings.md 95±, research/research.md 6±). The fact holds. The inference does not: a commit in which a producer is corrected *and its output written elsewhere* is equally evidence that the handoff already happened and the two now live apart. Nothing in 583683f's body (which I read in full) says where either side should live. Attack (2). Correction: 583683f proves derivation, not co-location; the MOVE of research/ + I3 needs an independent argument the return does not supply.

**4. I4 — "lineage-by-precedent" is not lineage, and the commit that *is* lineage points elsewhere. MAJOR.**
Subject's claim: *"Lineage-by-precedent says I4 and its siblings belong at the analogous `docs/features/skill-control-center/session-evidence/`."*
Record: the precedent directory is real — `docs/features/agent-provenance-telemetry/session-evidence/TASK-100/{context-pack.md,task-session.md}` and `TASK-105/layering-self-review.md` all exist as described, and `find implementations -maxdepth 3 -name "*.md"` returns exactly the three files claimed. But (a) `layering-self-review.md` line 1-2 reads "TASK-105 Layering and Authority **Self**-Review / Verdict: PASS for pure L0" — a self-review of domain-code layering, not an independent review of a runtime; the shape is analogous, not identical; (b) APT's evidence is keyed by ADR-bound `TASK-nnn` units that `experiments/skill-control-center/implementation/` has none of; (c) decisively, `git show --stat 64b028d` ("turn the skill topology into a caller/callee call map") couples `experiments/skill-control-center/implementation/frontend-constitution-check.md` in one commit with `implementations/static/control-center/{app.js,index.html}` and `tests/control_center/test_frontend.py`. The subject's own primary evidence type points I4 at `implementations/`, and the return neither cites 64b028d nor answers it. Both attacks. Correction: I4's destination is argued by structural analogy while the one same-commit coupling that exists points elsewhere; the verdict must either cite 64b028d and rebut it or drop to unproven.

**5. I2/implementation + agent-runtime — bulk-commit birth, argued from message not diff. MAJOR.**
Subject's claim: *"`implementation/` + `agent-runtime/` (commit `06bd467`, message: 'Keeps the context packs … so the implementation's provenance is readable from the repo')."*
Record: quote verified verbatim (the subject truncates "rather than only from the transcript" without distortion). But `git show --stat 06bd467` shows all 10 files added at once alongside a `.gitignore` change and the `research-review` rename — no per-file history exists. The placement argument rests on a commit *message* asserting an intent, plus one 100%-similarity rename. Attack (1). Correction: label this as message-evidence, not diff-evidence.

**6. I1 — malformed command, and the same-commit rule again unapplied. MINOR/MAJOR.**
Subject's claim: *"`git log --follow --stat -- experiments/skill-relationship-graph/` → one commit … Derives-from-here = belongs-here since no other object claims it as input."*
Record: `--follow` is defined for a single file, not a directory; run as cited it silently degrades to plain `git log`. The result (one commit, `22cbebb`) is nonetheless correct. But 22cbebb is a *two-experiment bulk commit* that also births all of skill-control-center's research/ and meta-orchestration/ — so under the subject's coupling rule I1 is bound to I2, which the verdict never confronts. And 22cbebb's body states the graph "answer[s] questions the UI work kept assuming"; 64b028d turns that topology into the shipped call map — i.e. something downstream *does* consume it. Both attacks. Correction: "no other object claims it as input" is contradicted by 22cbebb's own body and 64b028d; STAY may still be right, but not for the stated reason.

## Lineage that held

- **4e69b2f (I5)** — quote verified verbatim; `git show --stat` confirms 15 byte-for-byte renames + `.gitignore`, 16 files, 1 insertion/1 deletion. `git log --follow` survives the rename to `9385085 feat: add FOODSToGo JBP 2025 business-case experimentation`. `git grep -il foodstogo -- docs README.md plans research` returns only this dispatch's own proposal files — "no other tree references it" is confirmed. I5 STAY is the best-evidenced row in the return.
- **06bd467 rename** — `git log --diff-filter=R --find-renames --name-status` returns exactly `R100 …/research-review/review.md → …/research/review/review.md`. Quote accurate.
- **583683f stat** — reproduced exactly as quoted.
- **final-review.md line 9** — quoted string is verbatim at line 9.
- **implementations/ has no build-record docs** — reproduced exactly (README.md, UI-CONTRACT.md, agent-runtime/README.md).
- **APT session-evidence precedent exists** — TASK-100 and TASK-105 contents are as described.

## What I could not check

- Whether any live process consumes the `../../../` relative links (the subject concedes this too); I confirmed the links exist and cite `agent-provenance-telemetry` paths, not that anything resolves them.
- I6's front-matter claim — I did not re-run `head -10` on the two review files; it is co-location plus self-declaration, and it is not where the lineage angle is load-bearing.
- I8 and I9 rest on no git claim, so evidence sufficiency has nothing to test; the subject correctly self-flags I8 as a default rather than a proven claim.
- A repo-wide `grep -rl foodstogo` timed out at 120s; I substituted `git grep` over tracked `docs/`, `README.md`, `plans/`, `research/`, so untracked-file references are unchecked.
