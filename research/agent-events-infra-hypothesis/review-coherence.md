---
title: "Coherence / anti-noise-fidelity review — HYP-ORCH-INFRA"
reviewer: coherence (anti-noise-fidelity axis)
target: vault/hypothesis/orchestration-infra.md (+ research/findings.md, research/research.md)
date: 2026-07-20
verdict: NEEDS-REVISION (light — two blocking items, both locally fixable)
---

# Coherence review — does the infra hypothesis stay honest and falsifiable?

## Method note (what I verified, not just read)

Every "the repo already does X" citation I could reach was checked against the artifact:

- `signature()` — real, at `ledger.py:790-808` (body 796-807), and it **does** drive SSE
  change-detection (`main.py:233,237` — `last`/`current = ledger.signature(...)`). Docstring
  confirms `mtime_ns + size`, covering ledger + pending sheets. **Claim holds.**
- `expires = created + 60 days` in session frontmatter — real (`close-session/SKILL.md:70`).
  **Claim holds**, and "no TTL/gc machinery (PENDING)" is honest: no gc code found.
- `spec_hash` / `corpus_hash_at_emit` / `expires` — **absent** from `implementations/server/**`
  (grep: no matches). Consistent with the doc treating them as KT-sourced, to be vendored.
- `connections` typed `sequential|zig-zag|feedback`, a JSON column of `{from,to,type}`, and
  `feedback_prompts` recorded verbatim in the close row — real (`register-dispatch/SKILL.md:62,
  95,210`). The "scheduling edges, not transport" reading holds (they reference `group_id`s,
  carry no message content).

So the **Context / "what already exists" section is clean on claim ≤ proof.** The problems below
are about *conclusions the prose reaches past that evidence*, and one self-contradiction.

---

## Priority 1 — BLOCKING

### P1. The "not a new store" thesis contradicts its own judgment stream, and Collapse-test 1 fires on the intended design

- **Location:** infra `line 35-36` ("The bus is not a new store; it is a projection … **plus
  the one thing the ledger lacks a home for** — the agent's frozen independent judgment"),
  `line 72` ("a **judgment stream** … which the ledger has no slot for today"), `line 75-78`
  ("Because it is a **projection, not a second authoritative store** …"), `line 163-165`
  (Collapse-test 1), and `line 178` (BET-BUS-PROJECTION: "**pure projection** of the ledger
  **plus the frozen-judgment stream** — no second authoritative store").
- **Issue:** the judgment stream is, by the doc's own words, **new authoritative content the
  ledger does not hold**. Collapse-test 1 states the thesis is false "*if it must hold
  authoritative content the ledger does not — then it is a second store*." That condition is
  **satisfied by the design on purpose** — so the collapse-test, read literally, kills the
  thesis by construction, and the headline "not a new store" / "pure projection … plus new
  content" is internally contradictory ("pure projection *plus* new content" is not a pure
  projection). This is the single least-honest seam in the doc: the load-bearing one-liner
  asserts more (a *pure* projection, no new store) than the construction delivers.
- **Fix (pick one, and make the collapse-test match):**
  (a) **Route frozen judgments through the appender** (extend the ledger schema, EG-1-compatible),
  so the bus genuinely is a projection of *both* streams and "not a new store" is literally true;
  or (b) **scope Collapse-test 1 to the *lifecycle* stream** and state plainly that the judgment
  stream is a **new artifact-class** that stays EG-1-safe *because it does not duplicate the
  ledger* (no drift risk), not because it is a projection. The doc already gestures at (b) at
  `line 192` ("a new retention/artifact-class axis for CONST-ENG to ratify") — surface that up
  into the thesis statement and reword `line 35-36`/`178` so "not a new store" means "not a
  **duplicative** store," which is the EG-1 concern, not "no new content."

### P2. findings.md pre-resolves the exact axis it says must stay open (the over-conclusion the author was warned about)

- **Location:** `findings.md line 29` — section header **"Reuse candidates (vendor the schema —
  never a runtime dep on KT's live files)"** — versus `findings.md line 57` (OQ-3: "Coupling vs
  vendoring — KT as vendored schema … vs runtime dep. … **This is the central undecided axis —
  do not resolve it prematurely.**") and `findings.md line 18` ("central tension … left open").
- **Issue:** the header **decides** vendor-over-couple ("never a runtime dep") — that *is* the
  answer to OQ-3, asserted as a settled constraint in the same document that calls the axis "the
  central undecided axis." This is precisely the "jumps to conclusions on reuse" failure the
  review was told to hunt for, living in the grounding findings that the hypothesis cites as
  `derives-from`.
- **Fix:** either (i) demote the header to a hypothesis ("**candidate** constraint: vendor, not
  couple — driven by the portability principle") and keep OQ-3 genuinely open, **or** (ii) if the
  portability principle really does settle vendor-vs-couple, then **say so** and stop calling it
  "the central undecided axis" — rename the truly-open axis to *how much to reuse vs build native*
  (see P3). You cannot have it both ways in one file.

---

## Priority 2 — should fix before this advances

### P3. "Held open" is partly performative — the vocabulary leans "vendor decided"

- **Location:** infra `line 140` (table: home = "**vendored from KT** (open: vendor vs. couple)"),
  `line 181-183` (**BET-VENDOR-NOT-COUPLE**, conviction: **medium**, "Explicitly held open"),
  `line 144-145` (OQ-1 "the central undecided axis").
- **Issue:** the table's *Home* column states "vendored from KT" as the resolved home while
  parenthetically hedging; the bet's **name itself encodes a direction** (VENDOR-**NOT**-COUPLE)
  and carries conviction:medium — a scale already tipped, not a neutral open question. Meanwhile
  the axis labelled "central undecided" (vendor vs couple) is the one the portability principle
  most nearly *settles*; the genuinely open axis — **reuse-KT at all vs build-native, and how
  much** — is never named as the central tension, even though the task framing and the honest
  uncertainty live there.
- **Fix:** rename the bet to a neutral, falsifiable form (e.g. **BET-REUSE-BOUNDARY**: "KT's
  reusable parts are *separable enough to vendor* and *sufficient* without a runtime dep"), give
  it a real falsifier (below), change the table *Home* cell to "candidate: vendored from KT — see
  OQ-1," and re-point "the central undecided axis" at reuse-vs-build/how-much rather than
  vendor-vs-couple.

### P4. BET-TWO-RESIDUES over-borrows M6's proof-strength across a bridge OQ-5 marks unproven

- **Location:** infra `line 108-113` ("**splits — per KT's Lean-proved M6 —** into instance
  residue ⊥ schema residue … Two counters, not one"), `line 184-185` (BET-TWO-RESIDUES,
  veracity: **medium**, "**Inherits KT's M6**"), against `line 154` (OQ-5: "is KT's two-kind
  residue **the same orthogonality** as the conceptual thesis's, subsumed, or new? — open").
- **Issue:** M6 (Lean, no `sorry`) proves η^sch ⊥ η^ins are independent **for KT's
  classification functor Δ: L1→L2.** That the orchestrator's *predicted↔produced theme
  divergence* **is an instance of Δ** is a modeling identification — exactly the thing OQ-5 leaves
  open. So `line 112`'s "splits — per KT's Lean-proved M6" reads as *proven* when the transfer is
  itself the bet; veracity:medium and "inherits M6" borrow a Lean proof for a mapping the doc's
  own OQ-5 has not closed. (Fidelity note: the doc is otherwise **correct** not to conflate
  η^sch⊥η^ins with `bias ⊕ noise` — OQ-5 keeps that open, which matches the sibling, where the
  seam revision already qualified the `bias ⊕ noise` ⊥ as "licensed, not free." Good. The
  problem is *only* the M6 over-borrow.)
- **Fix:** qualify `line 112` — "splits into two counters **if** the theme-prediction is modeled
  as a classification functor (M6 then gives their independence — but the identification is OQ-5,
  unproven)." Either lower BET-TWO-RESIDUES veracity to `low`, or state that the `medium` rests
  on M6 *conditional on* the functor identification.

### P5. Two of four bets have no falsifier at all; bets don't point to their collapse-tests

- **Location:** infra `line 176-185` (Registered bets) vs `line 160-173` (Collapse-tests). The
  four collapse-tests cover: projection-duplication, freeze-unenforceable, inversion-fails,
  macro-tag-ungovernable. **BET-VENDOR-NOT-COUPLE** and **BET-TWO-RESIDUES** have **no
  corresponding collapse-test**, and none of the four bets names its falsifier the way the sibling
  does.
- **Issue:** a "registered bet" with no stated falsifier is not falsifiable — it is an opinion
  with two confidence labels. BET-VENDOR-NOT-COUPLE especially: what observation would kill it?
  (e.g. "a reusable KT part proves inseparable from KT's live runtime — it cannot be copied
  without importing the engine.") That is stateable and absent.
- **Fix:** give each bet an explicit *Falsifier* line (or an explicit pointer to the collapse-test
  that carries it), and add the two missing conditions: vendoring-inseparability (for the reuse
  bet) and residue-non-independence (for the two-residue bet — "if tightening the a-priori rule
  also closes schema residue in practice, the two-counter design collapses to one").

### P6. Structure/voice drift from the sibling on two conventions

- **Location:** whole *Open questions* and *Registered bets* sections vs
  `anti-noise-orchestration.md`.
- **Issue:** (a) the sibling's bets use a **rich schema** — *Bet · Carries · Status · Falsifier ·
  Experiment · If it falls*; the infra bets are one-liners (`veracity/conviction`: claim). This
  is both a voice mismatch and the mechanical cause of P5. (b) The sibling states "Each [OQ]
  carries a **recommendation**, not just the question"; the infra OQs are bare questions. For OQ-1
  (coupling) a bare question is *correct* (hold it open), but for OQ-2/3/7 the sibling's convention
  would attach a recommendation.
- **Fix:** adopt the sibling's bet schema (at minimum add *Carries* + *Falsifier* per bet — this
  discharges P5), and add a one-line recommendation to the OQs where the doc actually has a lean
  (leaving OQ-1 explicitly recommendation-free, which is itself the honest signal).

---

## Priority 3 — nits / polish

- **P7 — "the only code change."** infra `line 104`: "The **only** code change for the live view
  is teaching `signature()` about the new dirs." Over-claim: serving `bus/`, `live/`, `pending/`
  over SSE also needs read endpoints + parse, not just the change-detector. Soften to
  "the only *change-detection* change."
- **P8 — definite-article over-assertion.** infra `line 71` ("**the** enforcement handle for
  freeze") and `line 48` ("**the single** integration point for anything served live") read as
  settled; both are carried by low-veracity bets/collapse-tests, so soften to "a candidate
  enforcement handle" / "the change-detection integration point."
- **P9 — freeze-before-the-channel, channel-sense narrowing (fidelity nuance).** infra `line
  84-88` and worked example `line 122-124` treat "the channel" as the **cross-agent bus / peers**.
  The sibling's adjustment 1 (`anti-noise-orchestration line 246-249`) literally says "**the reviewer** is a
  channel" (per-agent). The narrowing is actually *consistent* with the sibling's seam-revised
  placement (freeze = coupling-fiber nudge over `D(A^N)`, `anti-noise-orchestration line 154`), so it is not a
  contradiction — but the infra doc promotes the primitive without noting it has generalized the
  "channel" from reviewer to peers. One clause of acknowledgement would close the gap.
- **P10 — cross-ref hygiene.** infra `line 152` "Re-opens BET-TAG" — BET-TAG lives in the
  **sibling**, not this doc; wikilink it (`[[anti-noise-orchestration]]` BET-TAG) so a reader
  isn't hunting for a bet that isn't here. Same for the `signature()` citation, which points at
  the body range (796-807) rather than the `def` line (790) — harmless, but 790 is the anchor.

---

## What the doc gets right (so the verdict is read fairly)

- The **reframing away from "the infra hypothesis IS KT reuse"** toward "the substrate is a
  projection of the ledger + the frozen judgment the ledger has no home for" is the correct honest
  move — KT reuse is demoted to OQ-1 + a bet, not the thesis. The author clearly absorbed the
  over-conclusion warning at the *thesis* level (the residual leak is in findings.md, P2).
- **PENDINGs are placed where evidence stops** (TTL/gc, P14 persisted home, tagging-engine-is-a-
  spec) and every reachable "already does X" citation verified.
- **Collapse-tests 2-4 are real** (freeze-unenforceable, inversion-fails, macro-tag-ungovernable
  each state a condition that would actually kill their claim). Only Collapse-test 1 is defective
  (P1).
- **Bets sit at veracity:low** where nothing is built — honest calibration.
- **η^sch⊥η^ins is *not* conflated with `bias ⊕ noise`** (OQ-5 holds it open) — faithful to the
  sibling; the only residue-fidelity slip is the M6 over-borrow (P4).
- Overall **structure matches the sibling** (Opening → Context → central thesis → worked example →
  where-each-design-lives → OQs → collapse-tests → bets → connections) and the `> Status:` /
  bolded-one-line-claim voice is carried over.

---

## Verdict: NEEDS-REVISION (light)

Two items are genuine coherence/honesty failures, not polish: **P1** (a headline that outruns the
construction, and a collapse-test that fires on the intended design — the thesis is either
trivially "collapsed" or the claim must be requalified) and **P2** (findings.md settles the very
axis it declares undecided — the exact over-conclusion pattern flagged). Both have clean, local
fixes and do not require re-architecting the thesis. P3-P5 (performative openness, M6 over-borrow,
missing falsifiers) should be closed before any promotion toward a constitution, since they are
where "claim > proof" and un-falsifiable bets have crept in. With P1 and P2 corrected and P3-P6
addressed, this becomes READY-WITH-NOTES — the underlying reasoning is disciplined and the
evidence base is sound.
