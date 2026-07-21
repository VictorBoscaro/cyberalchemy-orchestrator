# Merge design — FRAMINGS.md ⊕ MAPPING.md → one stratified CT ledger

> **Status:** design complete, ready for APPLY. Read-only step; the only file written is this artifact.
> Binds to `sessions/2026-07-21-1141-framings-mapping-merge.md`. All output English. `claim ≤ proof` preserved (no strength upgraded).

---

## 1. File-name decision

**Keep `FRAMINGS.md` as the absorbing file; delete `MAPPING.md`.** Confirmed (default upheld).

**Rationale (verified by inbound count).** `FRAMINGS.md` carries far more inbound pointers than
`MAPPING.md`, and — decisively — **every** inbound *anchor* link targets `FRAMINGS.md`
(`#f1--…`, `#f6--…`, `#f7--…`); the only deep anchor into `MAPPING.md` is a single
`MAPPING.md#2` in an archived doc. Absorbing into `FRAMINGS.md` lets all F1–F7 anchor links keep
resolving with zero edits (just preserve the headings), so we touch only the ~12 links that point at
the deleted `MAPPING.md`. The reverse choice (keep MAPPING) would force rewriting every F1/F6/F7
anchor link. Name stays `FRAMINGS.md` (H1 title updated to reflect the widened scope).

---

## 2. Final section structure (exact ordered outline)

New H1: `# FRAMINGS — stratified CT ledger (framings · interpretation · join)`

| New heading (exact) | GitHub slug | Content that moves in |
|---|---|---|
| `## §0 — Status and conventions` | `#0--status-and-conventions` | **Union** of both files' status/preamble blocks, stated once (see §5 risks — do not lossy-pick). |
| `## §1 — Theory: the abstract types` | `#1--theory-the-abstract-types` | FRAMINGS F1–F7 + `Common thread`, **verbatim**, re-levelled `##`→`###` (see §3 anchor note). |
| `## §2 — Interpretation functor` | `#2--interpretation-functor` | MAPPING §1 seed table + its `(F7)` Note, and MAPPING §2 table — **verbatim** as `### 2.1 …` / `### 2.2 …`. |
| `## §3 — Join and soundness` | `#3--join-and-soundness` | **NEW** fibration table + gap map (§5 draft below), then MAPPING §3 collapse-tests folded in **verbatim**. |
| `## §4 — Open items and obligations` | `#4--open-items-and-obligations` | MAPPING §4 open items, **verbatim**. |

Body of §1: keep line `# FRAMINGS` content moved under `## §1`; the seven `### Fx — …` entries and
`### Common thread` follow. Body of §2: prepend one line stating the functor `I : AgentLang → CT`
(the formula is kept out of the heading to keep the slug clean), then the two sub-tables.

Verbatim vs. re-headed:
- **Verbatim (byte-identical text):** the seven F-headings and their bodies, the Common thread, all
  MAPPING table rows/cells, the `(F7)` Note, the four collapse-tests, the two §4 open items.
- **Re-headed only (text unchanged, `##`→`###`):** F1–F7 and Common thread nest under §1;
  MAPPING's `## 1.`/`## 2.` become `### 2.1`/`### 2.2`; MAPPING's `## 3.`/`## 4.` bodies move under §3/§4.
- **Rewritten (once):** only the §0 status block (merged union) and the H1 title.

---

## 3. Anchor-preservation strategy

**Preferred path taken: keep the F1–F7 heading text byte-identical, so all inbound anchors resolve unchanged.**

GitHub slugifies each heading independently of its nesting depth: lowercase → drop every char that
is not a letter/digit/space/hyphen → spaces to hyphens (each space becomes one hyphen, so an em-dash
between two spaces yields `--`). Therefore **re-levelling `##` → `###` does NOT change a slug** — only
editing the heading *text* would. APPLY must not alter one character of these seven headings:

| Heading (must stay byte-identical) | Anchor it preserves |
|---|---|
| `F1 — Residue = shadow ⊕ structure` | `#f1--residue--shadow--structure` |
| `F2 — Battery of shadows + ceiling` | `#f2--battery-of-shadows--ceiling` |
| `F3 — Count presupposes separation` | `#f3--count-presupposes-separation` |
| `F4 — Active-probe / passive-signal duality` | `#f4--active-probe--passive-signal-duality` |
| `F5 — Verb-rule` | `#f5--verb-rule` |
| `F6 — The Yoneda point as target, the anomaly as engine (the dynamics)` | `#f6--the-yoneda-point-as-target-the-anomaly-as-engine-the-dynamics` |
| `F7 — Two probe species = the two independent axes, with presentation order` | `#f7--two-probe-species--the-two-independent-axes-with-presentation-order` |

Confirmed live inbound anchors that resolve with **zero change** once headings are preserved:
`README.md:359` (`#f1--residue--shadow--structure`), `README.md:366`, `README.md:382`,
`BACKLOG.md:45` (all `#f6--the-yoneda-point-…`), `README.md:386` (`#f7--…`). **No edits required** to
any FRAMINGS.md anchor consumer.

The **one** anchor that must change is `MAPPING.md#2` (archived roadmap): its target section becomes
`FRAMINGS.md` §2, new slug `#2--interpretation-functor`. Handled in the inventory below.

---

## 4. Complete inbound-link inventory

Legend: **EDIT-REQ** = clickable link that would dangle after delete → must change. **EDIT-REC** =
live-doc prose/inline-code mention of the now-deleted filename (not a dangling *link*, but stale) →
should be corrected for honesty. **NO-CHANGE** = anchor still resolves, or the file is a frozen /
immutable record.

### 4a. FRAMINGS.md references — all NO-CHANGE (absorbing file keeps its name + headings)

| File:line | Current | Action |
|---|---|---|
| README.md:61, 146, 306, 464, 500 | `[…](FRAMINGS.md)` / prose | NO-CHANGE (name kept); see 4c for the *paired* MAPPING token on 61/146/464 |
| README.md:359, 366, 382, 386 | anchor links `FRAMINGS.md#f1…/#f6…/#f7…` | NO-CHANGE (headings preserved) |
| BACKLOG.md:45, 98 | `FRAMINGS.md#f6…` / `FRAMINGS.md` | NO-CHANGE |
| docs/PLAN.md:163, 319 | `[…](../FRAMINGS.md)` | NO-CHANGE (but see 4b — dedupe the paired MAPPING link on same lines) |
| lean-formalization/README.md:236 | `[…](../FRAMINGS.md)` | NO-CHANGE (paired MAPPING token removed, 4b) |
| vault/ontology-conventions.md:38, 384, 404, 512 | `[…](../FRAMINGS.md)` / prose | NO-CHANGE |
| vault/hypothesis/framework-self-similarity.md:37, 153 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| vault/hypothesis/claim-graph.md:74 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| vault/hypothesis/anti-noise-orchestration.md:208, 690 | `FRAMINGS.md` prose | NO-CHANGE |
| research/meta-ontology/SEED.md:34 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| vault/constitution/frontend-constitution.md:35, 329 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| vault/constitution/engine-constitution.md:42, 416 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| vault/audit/close-row-enrich-c.md:25, 71 | `[…](../../FRAMINGS.md)` | NO-CHANGE |
| research/repo-standing-investigation/investigator-theorist.md:123 | `` `FRAMINGS.md` `` | NO-CHANGE |
| docs/archive/PLAN-v0.3-detailed-roadmap.md:118, 131 | `[…](FRAMINGS.md)` | NO-CHANGE for FRAMINGS token (:131 also has a MAPPING token — see 4b) |

### 4b. MAPPING.md references — EDIT-REQ (clickable links)

| # | File:line | Current link | Required edit |
|---|---|---|---|
| 1 | README.md:61 | `([\`FRAMINGS.md\`](FRAMINGS.md), [\`MAPPING.md\`](MAPPING.md), [\`OBLIGATIONS.md\`](OBLIGATIONS.md))` | drop the MAPPING item → `([\`FRAMINGS.md\`](FRAMINGS.md), [\`OBLIGATIONS.md\`](OBLIGATIONS.md))` |
| 2 | README.md:146 | `**[MAPPING.md](MAPPING.md)** and **[FRAMINGS.md](FRAMINGS.md)** — the parallels between` | collapse to one file → `**[FRAMINGS.md](FRAMINGS.md)** — the parallels between` (rest of sentence unchanged) |
| 3 | README.md:409 | `lives in [\`MAPPING.md\`](MAPPING.md); this is the sample` | `lives in [\`FRAMINGS.md\` §2](FRAMINGS.md#2--interpretation-functor); this is the sample` |
| 4 | README.md:501 | doc-index row `\| [\`MAPPING.md\`](MAPPING.md) \| Living ledger of construct ⟷ CT type … \|` | **delete this table row**; broaden the FRAMINGS row (500) description — see 4d |
| 5 | lean-formalization/README.md:236 | `[\`MAPPING.md\`](../MAPPING.md), [\`FRAMINGS.md\`](../FRAMINGS.md), [\`OBLIGATIONS.md\`](../OBLIGATIONS.md)` | drop MAPPING → `[\`FRAMINGS.md\`](../FRAMINGS.md), [\`OBLIGATIONS.md\`](../OBLIGATIONS.md)` |
| 6 | docs/PLAN.md:162 | `*Home:* [\`MAPPING.md\`](../MAPPING.md) (construct ⟷ candidate CT type, single source) +` | dedupe (both links now = FRAMINGS) → `*Home:* [\`FRAMINGS.md\`](../FRAMINGS.md) (the merged CT ledger — F1–F7 anatomy + construct ⟷ CT type + join; single source) +` and delete the now-redundant `[\`FRAMINGS.md\`](../FRAMINGS.md) (the F1–F7 anatomy) + ` fragment on line 163 |
| 7 | docs/PLAN.md:319 | `\| [\`MAPPING.md\`](../MAPPING.md) · [\`FRAMINGS.md\`](../FRAMINGS.md) · [\`OBLIGATIONS.md\`](../OBLIGATIONS.md) \|` | drop MAPPING → `\| [\`FRAMINGS.md\`](../FRAMINGS.md) · [\`OBLIGATIONS.md\`](../OBLIGATIONS.md) \|` |
| 8 | vault/hypothesis/framework-self-similarity.md:40 | `[MAPPING.md](../../MAPPING.md)) is the *zoom*` | `[FRAMINGS.md §2](../../FRAMINGS.md#2--interpretation-functor)) is the *zoom*` |
| 9 | vault/hypothesis/framework-self-similarity.md:154 | `\| [MAPPING.md](../../MAPPING.md) \| \`grounds\` \| …` | `\| [FRAMINGS.md §2](../../FRAMINGS.md#2--interpretation-functor) \| \`grounds\` \| …` (note text unchanged) |
| 10 | docs/archive/PLAN-v0.3-detailed-roadmap.md:91 | `**The table lives in [MAPPING.md](MAPPING.md)**` | `**The table lives in [FRAMINGS.md §2](../../FRAMINGS.md#2--interpretation-functor)**` (also fixes a pre-existing wrong relative path — see §5) |
| 11 | docs/archive/PLAN-v0.3-detailed-roadmap.md:131 | `\| [MAPPING.md](MAPPING.md) + [OBL-E3](OBLIGATIONS.md) \|` | `\| [FRAMINGS.md §2](../../FRAMINGS.md#2--interpretation-functor) + [OBL-E3](OBLIGATIONS.md) \|` (change MAPPING token only) |
| 12 | docs/archive/PLAN-v0.3-detailed-roadmap.md:298 | `[MAPPING.md §2](MAPPING.md#2): feedback=2-cell,` | `[FRAMINGS.md §2](../../FRAMINGS.md#2--interpretation-functor): feedback=2-cell,` |

**Count: 12 required link edits across 8 files** (README.md ×4, docs/PLAN.md ×2, archive roadmap ×3,
lean-formalization/README.md ×1, framework-self-similarity.md ×2 — README's four are distinct lines).

### 4c. MAPPING.md references — EDIT-REC (live-doc prose, stale after delete)

| File:line | Current | Suggested edit |
|---|---|---|
| README.md:145 | `\`MAPPING.md\` is a typed candidate, not a result.` | `the CT mapping (now §2 of \`FRAMINGS.md\`) is a typed candidate, not a result.` |
| README.md:464 | dir-tree comment `├── FRAMINGS.md, MAPPING.md, OBLIGATIONS.md   # the thesis layer …` | drop `MAPPING.md, ` → `├── FRAMINGS.md, OBLIGATIONS.md   # the thesis layer (framings + CT mapping + join, falsifiable target)` |
| docs/essays/anti-noise-orchestrator/README.md:57 | `\`HYP-ORCH-NOISE\`, \`MAPPING.md\`, anti-bias discipline` | `\`HYP-ORCH-NOISE\`, \`FRAMINGS.md\` (CT mapping, §2), anti-bias discipline` |

### 4d. README.md:500 — broaden the surviving doc-index description (paired with deleting row 501)

Current: `| [\`FRAMINGS.md\`](FRAMINGS.md) | Ledger of framings F1–F7 — the anatomy of the categorical thesis. |`
New: `| [\`FRAMINGS.md\`](FRAMINGS.md) | Stratified CT ledger: F1–F7 framings anatomy (§1) + construct ⟷ CT-type mapping (§2) + join/soundness (§3) + open items (§4). |`

### 4e. NO-CHANGE — frozen / immutable records (do not edit)

| File(s) | Why |
|---|---|
| `telemetry/agents/subagents-dispatch.yaml:204,266,343,423,578,758` | append-only ledger; the appender itself blocks edits; historical dispatch prompts |
| `sessions/2026-07-20-2119-…`, `…-2136-…`, `…-2218-…`, `…-0205-…`, this session log | historical session records + frontmatter `specs_updated:` arrays, not resolvable links |
| `research/repo-standing-investigation/investigator-falsifier.md:50,52,114`, `investigator-theorist.md:122` | dated audit artifacts citing `MAPPING.md:15/:25` line numbers (already point-in-time); inline code, not clickable links |

> Rationale for leaving 4e: these are point-in-time records; rewriting them would falsify history and
> they contain no dangling *links* (inline-code mentions and frontmatter arrays, not `[..](..)`).
> If the reviewer insists on zero stale mentions anywhere, the falsifier/theorist inline mentions are
> the only borderline items — but their line-number citations are already stale by construction.

---

## 5. Draft of §3 — Join / soundness (NEW content, ready to paste)

> APPLY: paste the block below as the body of `## §3 — Join and soundness`, then append MAPPING's
> four collapse-tests verbatim under `### 3.3`. Everything here is **candidate / unreviewed** — no
> strength is upgraded; the section only *aligns* existing units.

```markdown
The interpretation functor (§2) and the abstract types (§1) are two views of one structure. This
stratum records the **join**: which framing each mapping row instantiates (the fibration), and —
the payoff of the merge — the **bidirectional gaps** where one side has no partner on the other.
Status of every claim below: **candidate, unreviewed** (`claim ≤ proof`).

### 3.1 Fibration — framing ⊣ the §2 rows that instantiate it

| Framing (§1) | Mapping rows that instantiate it (§2) | Strength |
|---|---|---|
| **F1** — residue = shadow ⊕ structure | concat/synthesis (§2.2); collapse-detection (§2.2); exit_reason (§2.2); residue-of-a-synthesis (§2.1) | candidate |
| **F3** — count presupposes separation | collapse-detection (§2.2); check-tension / anti-bias axes (§2.2, the *separation* face) | candidate |
| **F4** — active-probe / passive-signal duality | probe (recon, broad sense) (§2.1); check-tension / plural probe (§2.2) | candidate |
| **F6** — Yoneda point (target) / anomaly (engine) | check-tension / anti-bias axes (§2.2, axis = separator/anomaly) | candidate |
| **F7** — two probe species = two independent axes | probe: recon/connection species (§2.2); probe (recon) (§2.1) | candidate |

### 3.2 Gap map — the unmatched-on-both-sides (the merge payoff)

**(a) Framings with no / weak operational witness in §2:**

- **F5 (verb-rule)** has *no dedicated §2 row*, but it binds to the graph's **edge taxonomy**: the
  verbs are the edges (`sequential` / `zig-zag` / `feedback` / `dispatch`), and the §2 finding
  `feedback = 2-cell` is exactly F5's "a verb that does **not** preserve symmetry → generates
  residue." **Candidate join to author:** `F5 ⟷ edge-taxonomy + feedback-edge` (unwritten; worth a row).
- **F2 (battery of shadows + ceiling)** is only *grazed* by `exit_reason` (§2.2, the run's scalar
  shadow). It remains **theory with no operational witness** yet — flagged, not resolved.

**(b) §2 rows with no framing → candidate new framings F8/F9:**

- `feedback = 2-cell` (§2.2) — operational structure outside the 1-skeleton; the abstract theory has
  not absorbed 2-cells. → feeds the F5 candidate above and a possible **F8**.
- `meta + lineage = free monad (A6)` (§2.2) — self-application (`framework as its own instance`,
  thesis A6) has no framing. → candidate **F8: self-application / the endofunctor A6**.
- `final_approver = terminal cone / limit` (§2.2) — the auditor as an apex *outside* the diagram, the
  **dual** of the probe-colimit (F4/F7), has no framing. → candidate **F9: the auditor as the dual of
  the probe-colimit**.

> These are *candidates for new framings*, not framings — do not number them into §1 until reviewed.

### 3.3 Collapse-tests (folded from the former MAPPING §3)
```

Then paste MAPPING §3 verbatim under 3.3 (the four bullets: concat/synthesis, feedback = 2-cell,
plural probe, meta/A6).

---

## 6. Losslessness map (every current unit → destination)

| Source unit | Destination in merged FRAMINGS.md | Mode |
|---|---|---|
| FRAMINGS status/preamble block (lines 3–6) | §0 (union clause: probe-verified anchors, weak-anchor labelling) | merged once |
| MAPPING status/preamble block (lines 3–11) | §0 (union clause: `claim ≤ proof`, single-source-of-truth PLAN §3, inherited rule, operational base skill + constitution v0.6.3, created dates) | merged once |
| F1–F7 (7 entries) | §1 (`### Fx …`) | verbatim, re-levelled |
| Common thread | §1 (`### Common thread`) | verbatim, re-levelled |
| MAPPING §1 seed table (7 rows: probe-recon, probe-experiment, zig-zag, sequential, dispatch, feedback/robot-talks, residue-of-synthesis) | §2 → `### 2.1 Seed table (inherited from PLAN §4)` | verbatim |
| MAPPING §1 `(F7)` Note (recon broad-vs-species) | §2.1, immediately after the table | verbatim |
| MAPPING §2 table (9 rows: concat/synthesis, feedback edge, check-tension, meta+lineage, final_approver, exit_reason, dependency/READY, collapse-detection, probe-species) | §2 → `### 2.2 Parallels from the subagents-strategy skill` | verbatim |
| MAPPING §3 collapse-tests (4: concat/synthesis, feedback=2-cell, plural probe, meta/A6) | §3.3 | verbatim |
| MAPPING §4 open items (2: P-CT, OBL-E3 sub-3) | §4 | verbatim |
| — (new) fibration | §3.1 | new |
| — (new) gap map | §3.2 | new |

Reviewer check: 7 framings + thread + 7 seed rows + 1 note + 9 skill rows + 4 collapse-tests +
2 open items + 2 status blocks = **all accounted for**; only §0, H1, §3.1, §3.2 are authored/merged.

---

## 7. Risks / edge cases for APPLY

1. **Two status headers must UNION, not lossy-pick.** FRAMINGS' preamble (anchors probe-verified
   2026-07-18; weak-anchor labelling) and MAPPING's preamble (`claim ≤ proof`; single-source-of-truth
   for PLAN §3; the inherited "every construct → CT type + real-file anchor" rule; operational base
   `domainspec-subagents-strategy` SKILL + constitution v0.6.3; created 2026-07-19) carry *different*
   clauses. §0 must keep every distinct clause. Also record **both** provenance dates (framings
   session 2026-07-18; mapping created 2026-07-19).
2. **`(recon)` broad-vs-species disambiguation.** MAPPING §1's `(F7)` Note and FRAMINGS F7's own
   reconciliation label ("uses 'recognition' in a narrower scope than the '(recon)' of MAPPING §1 —
   reconciled 2026-07-20") now live in the same file. Keep BOTH verbatim; they agree — do not
   "dedupe" them into an apparent contradiction. Single source of truth for the term remains DEF-ORCH-004.
3. **DEF-ORCH / OBL-E3 references stay intact.** Do not rewrite `DEF-ORCH-001/003/004`, `OBL-E3 sub-3`,
   `P-CT`, `PRIZES.md`, or the `TO-ME/oble3-…` brief path — copy verbatim.
4. **Heading text is load-bearing for anchors.** Do not touch one character of the seven F-headings
   (§3 of this design). Re-levelling `##`→`###` is safe; text edits are not.
5. **New §2 slug is `#2--interpretation-functor` (double hyphen).** All three archived/self-similarity
   links must use exactly this; keep the heading formula-free so the slug stays stable.
6. **Archive roadmap had a pre-existing wrong relative path** (`[MAPPING.md](MAPPING.md)` from
   `docs/archive/` resolves to `docs/archive/MAPPING.md`, already broken). Edits #10–#12 both remove
   the dangling target and fix the path to `../../FRAMINGS.md`. Do not "preserve" the old broken path.
7. **Delete `MAPPING.md` last**, after every EDIT-REQ link is repointed, so nothing is orphaned.
8. **English-only:** both source files are already English; the §0 merged block and §3 draft above are
   English. The Portuguese session log is not part of the merged content.
9. **`claim ≤ proof`:** the merged ledger keeps `brainstorm/candidate, unreviewed`; §3 marks every new
   line `candidate`. No row, framing, or strength is upgraded.
```
