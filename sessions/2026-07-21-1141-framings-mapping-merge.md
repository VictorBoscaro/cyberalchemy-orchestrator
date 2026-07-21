---
tags: [category-theory, ledger, framings, mapping, refactor, single-source-of-truth]
node_type: conceptual
is_session: true
layer: architecture, domain
nature: explanatory, reference
status: active
version: 0.1
last_updated: 2026-07-21
created: 2026-07-21
timestamp: 2026-07-21T11:41:00-03:00
conversation_id: unknown
decisions_made: true
contradictions_found: false
specs_updated: []
promoted_candidates: []
expected_importance: 6
importance_rationale: "Decides to merge the two candidate CT ledgers (FRAMINGS + MAPPING) into a single stratified ledger, on the grounds that their mutual cross-reference density makes the file boundary do negative work; declarative reorganization, no collapse-test ran and no theorem changed. Value is structural: the merge surfaces the bidirectional gaps (framings with no operational witness; mapping rows with no framing) on one surface."
---

# Objective — merge FRAMINGS.md + MAPPING.md into one stratified CT ledger

## Objective (session 0 — the anchor)

Fuse the two root candidate ledgers — `FRAMINGS.md` (the F1–F7 abstract anatomy /
codomain `C`) and `MAPPING.md` (the construct ⟷ candidate-CT-type interpretation) — into a
**single stratified ledger**. Do **not** flatten: the merge preserves the two as internal
strata and *adds* a join stratum.

**Why (settled in conversation).** The two files reference each other on nearly every entry
(FRAMINGS F7 → MAPPING §1/§2; MAPPING cites F1/F3/F4/F6/F7 throughout, even writing "live
instance of F1/F3"). When two living ledgers cross-reference that densely, the file boundary
does *negative work* — it forces the reader to jump files to close a single thought. Merging:
(1) internalizes every cross-reference; (2) states the shared discipline once instead of in
two headers; (3) improves single-source-of-truth (PLAN §4 points to one place, not two);
(4) — the payoff — puts the **bidirectional gaps** on one surface, impossible to lose sight of.

## Target structure (the recommended default — the design step may refine)

One file, stratified — merge the *container*, keep the *typing*:

- **§0 — status + conventions**, stated once: `brainstorm/candidate, unreviewed`;
  `claim ≤ proof`; weak-anchor labelling; every claim anchored to a real Lean file;
  single-source-of-truth for the mapping.
- **§1 — Theory / abstract types** = F1–F7 + the "Common thread" (the codomain `C`, the
  thin/non-thin lever).
- **§2 — Interpretation functor** `I: AgentLang → CT` = MAPPING's two tables (construct ↦
  type ↦ anchor ↦ strength).
- **§3 — Join / soundness** (NEW content) = the fibration (which framing each mapping row
  instantiates) + the **unmatched on both sides** + the collapse-tests from MAPPING §3.
- **§4 — Open items / obligations** (P-CT, OBL-E3 sub-3, …).

## The join content that §3 must capture (drafted in conversation)

Fibration (framing ⊣ mapping rows that instantiate it):

- F1 shadow⊕structure → concat/synthesis, collapse-detection, exit_reason, residue-of-synthesis (§1)
- F3 count presupposes separation → collapse-detection, check-tension (separation)
- F4 active/passive probe → probe(recon) §1, check-tension (plural probe)
- F6 Yoneda point / anomaly-engine → check-tension (axis = separator/anomaly)
- F7 two probe species = two axes → probe: species §2, probe(recon) §1

The **gap map** (the actual payoff):

- **F5 (verb-rule)** has no dedicated row, but binds: the *verbs* are the graph edges
  (sequential/zig-zag/feedback/dispatch), and `feedback = 2-cell` is exactly "a verb that
  does NOT preserve symmetry → generates residue". F5 ⟷ edge-taxonomy + feedback-edge — worth writing.
- **F2 (battery of shadows + ceiling)** is only grazed (exit_reason) — theory with **no
  operational witness** yet.
- **`feedback = 2-cell`, `meta+lineage = free monad (A6)`, `final_approver = limit/cone`**
  have **no framing** — operational structure the abstract theory has not yet absorbed →
  candidates for new framings F8/F9 (self-application A6; the auditor as the *dual* of the probe-colimit).

## Constraints (binding on every downstream step)

1. **Everything in English.**
2. **Lossless.** Preserve every framing (F1–F7), every mapping row, every anchor, every
   strength label, every weak-anchor label, every collapse-test, and the "Common thread".
   Nothing dropped in the merge.
3. **Anchors / inbound links.** Many docs link to these files, including deep heading anchors
   (e.g. `README.md` links `FRAMINGS.md#f1--residue--shadow--structure`, `#f6--...`, `#f7--...`).
   Known inbound references to reconcile: `README.md` (multiple, incl. anchor links + the
   directory tree + the doc-index table), `docs/PLAN.md` (§ around lines 162–163 and 319),
   `docs/archive/PLAN-v0.3-detailed-roadmap.md`, `lean-formalization/README.md`, and any
   other hit for `MAPPING.md`/`FRAMINGS.md`. Either preserve heading anchors so links still
   resolve, or update every inbound link — no dangling links may remain.
4. **Deletion is honest.** Whichever source file is subsumed is deleted (not left as a stale
   duplicate); no content is orphaned.
5. **`claim ≤ proof` preserved.** The merged ledger keeps `candidate/unreviewed` status; the
   merge is a reorganization, not a promotion — no framing or row is upgraded in strength.

## Pipeline (three sequential agents, each gated on the previous)

1. **Design** — decide *how*: final section structure, file-name decision (default: keep
   `FRAMINGS.md` as the absorbing file, delete `MAPPING.md`; fewer inbound pointers to touch),
   anchor-preservation strategy, the complete inbound-link inventory, and a draft of §3.
   Read-only; produces a design/decision artifact.
2. **Apply** — execute the merge per the approved design: write the merged file, delete the
   subsumed one, update every inbound pointer.
3. **Review** — verify the result against this objective + the design: losslessness, anchor
   integrity (no dangling links), English-only, `claim ≤ proof` unchanged.

## Files expected to be touched

- `FRAMINGS.md` (absorbing target — TBD by design step)
- `MAPPING.md` (subsumed / deleted — TBD by design step)
- `README.md`, `docs/PLAN.md`, `docs/archive/PLAN-v0.3-detailed-roadmap.md`,
  `lean-formalization/README.md` (inbound-pointer updates)
- this session log

## Connections

| Edge | Target | Note |
|---|---|---|
| governs | `FRAMINGS.md` | absorbing target of the merge (§1 theory stratum) |
| governs | `MAPPING.md` | subsumed source (§2 interpretation stratum) |
| derives-from | `docs/PLAN.md` §4 | the mapping's declared single-source-of-truth pointer |
| touches | `OBLIGATIONS.md` (OBL-E3 sub-3) | referenced by the join/open-items stratum |
