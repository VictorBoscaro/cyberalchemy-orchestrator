# S-B (Torvalds, Linus) — angle: lineage binds — round 2, FINAL pre-crosstalk position

## Response to review

**1. I7 (CRITICAL).** CONCEDE. I independently reran `git log --oneline -- .../bus-publication-probe/` → `ca560b8` only, and `git show --name-only 53cff55` → 10 files, all under `skill-protocol-compilation/`. `53cff55` never touches `bus-publication-probe/`. I cited one commit for two directories. Revised: I7 is now a two-part verdict — `skill-protocol-compilation/` keeps its evidenced STAY; `bus-publication-probe/` drops to unproven (no lineage record exists either way).

**2. I2/meta-orchestration (CRITICAL).** CONCEDE, and on re-investigation the correct call is more drastic than the reviewer even proposed. I confirmed `22cbebb` births both directories in one commit. But I went further and grepped `docs/features/skill-control-center/discovery/control-center.md`'s own "Provenance and cross-reference table": it lists `research/findings.md`, `research-review/review.md`, **and** `meta-orchestration/findings.md` all as relation `derives-from` — the document's own vocabulary treats all three identically as its owned evidentiary basis (line 558-561). My original three-way split had no basis; meta-orchestration moves with research/, full stop.

**3. I2/I3 (CRITICAL, primary target).** CONCEDE the inference gap, but I found evidence beyond what either of us cited that closes it. `583683f` alone is only derivation, as R-B says. But `control-center.md` currently, actively cites `research/findings.md`, `research/research.md`, and (via a now-broken link) `research-review/review.md` as `derives-from` sources — present-tense ownership by the consuming document, not a historical handoff. That is co-location evidence, distinct in kind from commit-coupling. I hold MOVE, but on this new ground, not the original one.

**4. I4 (MAJOR).** CONCEDE. I ran `git show --stat 64b028d` myself: it couples `experiments/skill-control-center/implementation/frontend-constitution-check.md` in one commit with `implementations/static/control-center/{app.js,index.html,shared.css}` and `tests/control_center/test_frontend.py`. I also confirmed via grep that **no** file under `docs/features/` cites `experiments/skill-control-center/implementation` or `agent-runtime` — zero derives-from pull toward docs/features exists. My `session-evidence/` destination was analogy, not lineage, and the one real coupling points at `implementations/`. Destination revised; exact subfolder marked low-confidence.

**5. I2/implementation+agent-runtime (MAJOR).** CONCEDE the evidence-type label: `06bd467`'s 10 files land atomically with no per-file history; it is message-evidence. Superseded anyway by finding 4's stronger diff-evidence (64b028d), which now carries the verdict instead.

**6. I1 (MINOR/MAJOR).** CONCEDE the malformed `--follow` and the "no downstream consumer" claim — both wrong. But investigating further overturns the direction of the objection: `implementations/server/control_center/service.py:101` and `sources.py:92` and `implementations/fixtures/skill-control-center/build_fixtures.py:63` all hard-code the path `experiments/skill-relationship-graph/graph.json` as a live read at runtime, and `docs/features/skill-control-center/architecture.md` row `SC-005` classifies it explicitly as "fixture only, not runtime authority" — a deliberate arm's-length external reference, contrasted against the same document's `derives-from` label for research/meta-orchestration. STAY is now evidenced by an actual executable dependency, not by absence of one.

## Verdict table

| item | verdict | destination path | one-line reason |
|---|---|---|---|
| I1 | STAY | experiments/skill-relationship-graph/ | Hard-coded live read path in `implementations/server/control_center/service.py:101`, `sources.py:92`, `fixtures/build_fixtures.py:63`; docs classify it "fixture only, not runtime authority." |
| I2 | SPLIT | research/, research/review/, meta-orchestration/ → docs/features/skill-control-center/; implementation/, agent-runtime/ → toward implementations/ | Discovery doc's own table labels the first three `derives-from` (owned basis); 64b028d same-commit-couples the latter two with implementations/ code+tests. |
| I3 | MOVE | docs/features/skill-control-center/ (with research/, meta-orchestration/) | Actively, presently cited as `derives-from` by control-center.md; also repairs 3 currently-broken relative links to the dead `research-review/review.md` path. |
| I4 | MOVE | implementations/ (exact subfolder unproven) | 64b028d couples it directly with implementations/static/control-center + its tests; zero docs/features citations exist. |
| I5 | STAY | experiments/foodstogo-jbp-2025/ | Unchallenged; reviewer confirmed as best-evidenced row. |
| I6 | STAY | (already correct) | Unchallenged; front-matter self-declaration stands. |
| I7 | SPLIT | skill-protocol-compilation/ stays; bus-publication-probe/ unproven | 53cff55 evidences one subfolder only; the other's landing commit (ca560b8, 63 files) names neither feature nor probe. |
| I8 | STAY | — | Unchallenged; no git claim to test either way. |
| I9 | STAY | research/artifact-placement-adjudication/ | Unchallenged. |

## What my angle cannot see

The declared-rule angle would say the `derives-from` table I now lean on for I2/I3 *is itself just a written convention* — the same category of evidence I'm structurally supposed to subordinate to causal record. I used it because it's the target's own internal reference (in scope per my brief), but I concede it functions rhetorically like a rule citation, and a hostile reviewer could say I laundered a declared-contract argument through a lineage label. I hold, because the table records what the document *actually depends on*, not what a policy says it should depend on — but this is a thinner line than I'd like.

Cost angle, unaddressed: moving research/+meta-orchestration/ requires repairing not just the 3 broken links already found but every other inbound reference (agent-runtime/backend-task-session-context.md, research/research.md's own citations of the graph, etc.) — I have not enumerated the full repair set.

## Claim <= proof

- **I2/I4 exact destination subfolder within implementations/**: no precedent exists for build-record markdown there (confirmed: only README.md, UI-CONTRACT.md, agent-runtime/README.md). Direction is evidenced; exact path is not.
- **I7 bus-publication-probe/**: STAY is a default, not an argued position — explicitly unproven per finding 1.
- **I2/I3 "co-location" via the derives-from table**: real and quoted, but see "What my angle cannot see" — it may be declared-rule evidence wearing lineage clothing.
- **I8, I9**: unchanged, still no git claim to test, self-flagged as default.

---

## PARENT VERIFICATION NOTE (P8, added by the orchestrator, not by the seat)

Independently re-run before crosstalk:
- `implementations/server/control_center/service.py:101` and `implementations/fixtures/skill-control-center/build_fixtures.py:63` **do** hard-code `experiments/skill-relationship-graph/graph.json` as a live path. CONFIRMED.
- `implementations/server/control_center/sources.py:92` is `"source_id": "skill-relationship-graph"` — a string identifier, **not** a path read. The seat overstated 3 live reads; the true count is 2. CORRECTED.
- The `## Connections` table in `control-center.md` is real and labels `research/findings.md`, `research-review/review.md` and `meta-orchestration/findings.md` as `derives-from`, while labelling `experiments/skill-relationship-graph/graph.json` and `viewer.html` as `cites`. CONFIRMED, and the relation asymmetry supports the seat's I1-versus-I2 distinction.
- Dangling `research-review/` links number **3**, at `control-center.md` lines 29, 559 and 617 — not 2 as the cost seat reported. CORRECTED in the lineage seat's favour.
