# Reconciled change-set — HYP-ORCH-NOISE critique red-team

> Source of authority: Stage-1 (5 attackers red-teaming the critique) + Stage-2
> (design + formal adjudication, robot-talks intra + zig-zag inter). This is the
> deconflicted change-set the editors apply to
> `vault/hypothesis/anti-noise-orchestration.md`. Dispatch `2026-07-21-anti-noise-critique-redteam`.
>
> **Governing principle:** concede every status-label / notation / oracle defect;
> hold every proven-under-conditions theorem; name (not build) every real gap as
> PENDING/open. The critique's "20 problems" collapse to ~5 real axes; ≥6 points were
> the document already quoting itself. The critique is WRONG to blanket-downgrade
> Seam 2 (genuinely categorical) and its central reformulation is ADOPT-**WITH-LOSS**
> (layer on top of the Bregman theorem, never replace it).

---

## PART A — FORMAL / STATISTICAL edits (Editor A)

### A1 [C2 keystone] — recast tension-vs-independence as covariance/decorrelation (lines ~103–115)
CURRENT (103–106):
> "And here is the core of the design: **tension and independence contradict each other.** Anti-bias *correlates* agents in deliberate opposition; anti-noise aggregation demands the opposite — independence (the average only cancels noise to the extent of independence; correlation ρ puts a floor on the gain). The resolution is **separation by stage**:"

NEW:
> "And here is the design's central subtlety, **stated honestly as covariance engineering**: tension and independence do **not** contradict — they are **two settings of one error-covariance knob**. The variance of the aggregate is governed by the full covariance matrix, `Var(ē) = σ²·[1 + (N−1)ρ̄] / N`, where ρ̄ is the mean pairwise error-correlation — **not** by independence per se. Independence (ρ̄=0) is the *convenient* case giving the clean 1/N; it is **sufficient, not necessary**. **Negative** error-correlation does strictly better — at ρ̄ = −1/(N−1) the aggregate variance goes to **zero**. Anti-bias tension *is* deliberately induced negative error-correlation, so it is not the enemy of noise reduction — it is the **best case** of the same lever. The design move is therefore not to separate two contradictory disciplines but to **place two points on one decorrelation axis** (ρ̄<0 = tension, ρ̄=0 = independence), staged where each is cheapest to obtain:"

CURRENT (114–115):
> "Two axes, two stages, two populations. This separation dissolves the contradiction and is the most load-bearing design principle of this thesis."

NEW:
> "Two points on one decorrelation axis, staged where each is cheap: engineer ρ̄<0 (opposed probes) where you can generate them; fall back to ρ̄=0 (independent, source-blind scorers) where you must. This is the most load-bearing design principle of this thesis — and separation-by-stage is a **practical allocation of the covariance knob**, not the resolution of a real mathematical tension (there was none)."

### A2 [C2 second face] — reconcile the FRAME two-arm passage (insert after line 182)
INSERT (after "This arm is new and not yet built."):
> "*(Consistency note, post-A1: the frame stage carrying **both** a tension arm and an independence arm is **not** a violation of the design principle. Under the covariance view both arms are points on the one decorrelation axis — tension is ρ̄<0, independent-dispersion is ρ̄=0 — so a single stage may legitimately hold both. "Two stages" is a placement heuristic for where each point is cheapest, not a partition theorem.)*"

### A3 [C3 + reformulation] — replace the Opening pull-quote + Revision (lines 30–40)
CURRENT (30):
> "> **`judgment residue = bias ⊕ noise`** — and reducing them calls for **distinct tools**, applied at **distinct stages** of the agent pipeline."
CURRENT (33–40): the "Revision (2026-07-20 … residue = bias * noise …)" block.

NEW (replace both with):
> "> **Core statement (honest framing).** Every judgment can be scored by an **expected loss** against an (unknown) target. That expected loss carries a **bias** part (systematic, directional error of the *aggregate*) and a **noise** part (dispersion of individual judgments about their aggregate). They are **not** free-standing orthogonal legs: whether they separate cleanly or interact through a cross term depends on an explicit **dependency object** — in the scoring regime the error-covariance Σ (A1), in the categorical/entropic regime the joint law `D(A^N)` / mutual information (Seam 2), formalized as the loss's convex potential `F` (the "anchored common scale"). The design (distinct tools at distinct stages) targets the two components; the *exact* separation is the conditional refinement below.
>
> > **Conditional theorem — proven under `F` (`seam-feasibility`; the "what we proved under F" refinement, NOT a weaker restatement).** *When* the loss is the Bregman divergence `D_F` of a Legendre potential `F`, **and** aggregation randomizes the **first** slot (M-projection / reverse-KL orientation), the expected loss splits **exactly**, Amari generalized-Pythagoras: a bias leg **⊥** a noise leg, **zero cross term** — this is the `⊕`. In that regime the aggregate is the **Banerjee-optimal** minimizer of expected loss (mechanical aggregation provably optimal), and the split is **exclusive to Bregman** (an iff, arXiv 2501.18581). **Without `F`, or with the slot flipped**, the honest form is `residue = R_bias + R_noise + R_interaction` (the doc's `bias * noise`): two entropic (KL) contributions **plus a non-zero Jensen cross term**, not orthogonal legs. **Two boundaries stay honest:** (i) `F = MAP / anchored common scale` is **asserted by naming, not constructed** — not yet shown to be a convex, divergence-generating Legendre potential (`[[OQ-10]]`); (ii) whether the split survives **composition of stages** is **OPEN** (the DPI contracts KL and plausibly rotates the residue out of ⊥ — the 4th collapse-test / OBL-E3). Proof and boundaries: `docs/essays/anti-noise-orchestrator/research/seam-feasibility/findings.md`."

### A4 [C3] — section header (line 94)
CURRENT: "### `bias ⊥ noise` — the reframe that reorganizes everything"
NEW: "### `bias ✻ noise` (⊥ only under `F`) — the covariance reframe that reorganizes everything"
(and where `⊕`/`⊥` recur informally downstream, they are licensed-under-F; add "(licensed by F; else += R_interaction)" once at the first such recurrence.)

### A5 [C4 + C17] — CT operationalization table row (line 284)
Replace the cell "**operational** (`seam-feasibility`): ⊕↦Amari-Pythagorean under `F`, √N↦regime-dependent concentration, aggregation↦m-projection, nudge↦morphism on the coupling fiber; **OPEN**: ⊥ surviving composition (DPI). See `[[BET-CT]]`" WITH:
> "**candidate — none yet adjudicated** (`seam-feasibility`; OQ-10). **One construct native-categorical:** nudge ↦ coupling-fiber morphism on `D(A^N)` (non-monic marginalization; no imported `F`; "acts on M not on A/B does not typecheck" is a genuine categorical *correction*). **One F-conditional and non-native:** bias✻noise ↦ Bregman/Amari split — **info-geometry / convex analysis, not CT** (findings.md: "non-native"), holding only under an **asserted** `F=MAP`. `√N`↦concentration and aggregation↦m-projection belong to `[[BET-√N]]`, **not this row**. Composition **OPEN** (⊥ vs DPI). **No decision has moved, so BET-CT's *corrects/predicts* clause is UNMET.** See `[[BET-CT]]`, `[[OQ-9]]`, `[[OQ-10]]`"
Also change the row's Axis cell from "CT" to "CT (Seam 2) · info-geom (Seam 1)".

### A6 [C4] — BET-CT status (lines 488–490)
Replace "*Status:* **survived once** (`seam-feasibility`: ⊕↦Amari-Pythagorean under `F`, √N↦regime-dependent concentration, nudge↦coupling-fiber). **In-test:** persona, tag, fork-guard." WITH:
> "*Status:* **candidate — not yet survived** (`seam-feasibility` exhibited *maps*, but no decision has moved; OQ-9 reserves "survived" for the predict/correct test, OQ-10 marks the identifications un-adjudicated). Of the maps: **nudge↦coupling-fiber is native-categorical** (Markov, no `F`); **bias✻noise↦Bregman/Amari is non-native (info-geometry) and F-conditional**, with `F=MAP` **asserted-by-naming, not constructed**; **`√N` and aggregation belong to `[[BET-√N]]`, not counted here** (removes the table/BET double-count OQ-9 flagged). **In-test:** persona, tag, fork-guard — and the *corrects/predicts* clause for the surviving maps."

### A7 [evidence-tier legend] — add near the "Where each principle's design lives" table intro
INSERT one line:
> "*Status legend (rising evidence): `mapped` (a formal map exists) < `proven-under-conditions` (theorem given stated conditions) < `survived` (a map changed ≥1 decision) < `operational` (used by default). Nothing in this thesis is yet `operational`.*"

### A8 [C5] — √N units, line 68 and lines 70–76
CURRENT (67–68): "the average of N **independent** judgments cancels noise on the order of √N."
NEW: "the average of N judgments shrinks the **standard error of the aggregate** by ~1/√N (a finite-variance / Bienaymé fact) — a reduction in the dispersion of the *mean*, not of any individual judgment, and 1/√N (not √N) in the estimator's units."

CURRENT (73–76): "State `√N` as the special case; the general guarantee is 'aggregation = m-projection onto the flat family, monotone under independence,' with a **regime-dependent exponent**. The design (aggregating independents) survives; the exponent is conditional."
NEW: "Disambiguate the four quantities '√N' silently conflates: **Var(ē) ∝ 1/N** (Bienaymé; finite variance only), **sd(ē) ∝ 1/√N** (its root — the literal gain), **SNR ∝ √N**, and the **large-deviation rate ∝ N** (Sanov tail exponent). The first three are L2/CLT facts governing *typical* fluctuations and hold generally with finite variance; the fourth governs the *tails* and is the genuinely regime-sensitive object (CLT and Sanov **coexist** — typical vs tail — they are not rival regimes). So: '1/√N' is the sd-gain, not conditional beyond finite variance; only the **LDP rate** is regime-dependent. The design (aggregating independents) survives; only the tail exponent is conditional."

### A9 [C13] — OQ-5 winner's curse (lines 352–353)
CURRENT: "**blind rubric selection** as default (an argmax robust to noise if the selection is blind); **fusion** only when…"
NEW: "**blind rubric selection** as default — but **argmax over noisy scores is *not* noise-robust**: the max of noisy estimates carries a **positive selection bias** (winner's / optimizer's curse), and blinding removes halo/source bias but not this max-inflation (the two are orthogonal). Control it with **aggregate-then-select** (rank on the panel score, not one draw), a **data-split** (select on fold A, estimate the winner's value on held-out fold B), or a **margin gate** (accept only if top − runner-up > k·σ). **Fusion** only when…"

### A10 [C16] — BET-√N falsifier + experiment (lines 509–513)
CURRENT falsifier: "…the average doesn't beat a single good scorer."
CURRENT experiment: "N scorers score a labeled set; measure error covariance vs. reference; compare average-error vs. best-individual-error."
NEW falsifier: "…the average doesn't beat a **pre-designated (ex-ante) single scorer**."
NEW experiment: "N scorers score a labeled set; measure error covariance vs. reference; compare average-error against a **pre-registered or expected/random single scorer** (**not** the ex-post argmin — an oracle unavailable at decision time that rigs the test toward falsification, and which contradicts this bet's own 'single good scorer'). Optionally data-split: pick the 'best' scorer on fold A, compare average vs. that scorer's error on held-out fold B."

### A11 [C18] — move the hedge to first mention (lines 122–123)
CURRENT: "native monotonicity (the data-processing inequality: channels *contract* KL) rotates the residue out of ⊥."
NEW: "native monotonicity (the data-processing inequality: channels *contract* KL) **plausibly** rotates the residue out of ⊥ — this is **conjectured, not proven** (see the compositionality collapse-test); the DPI *suggests* such a composite exists but no exhibit is in hand."

### A12 [C1] — OQ-4 agreement≠confidence (lines 336–337)
CURRENT: "strong agreement = low noise = high confidence; spread = ambiguous item **or** a bad boundary."
NEW: "strong agreement = low *observed* dispersion = low noise **only if raters are independent**, and even then warrants confidence only **pending the downstream-quality correlation** (agreement bounds *noise*, not *bias*: low-noise consensus among correlated raters is shared bias masquerading as reliability — the tag collapse-test and BET-TAG carry that check); spread = ambiguous item **or** a bad boundary."

### A13 [C15] — external-target discipline on the collapse-tests (append after lines 458–461; DO NOT cut the freeze-pair test)
APPEND:
> "**Discipline: dispersion is an *internal* quantity and cannot alone distinguish "ill-posed" from "rich" — that verdict needs an *external target* (downstream decision quality, a labeled reference, or a held-out outcome).** Without an external criterion, low-vs-high dispersion is unfalsifiable narration. This binds the tag collapse-test above too: "tag distribution correlates with downstream quality" **is** the external target; state it as primary, raw dispersion subordinate. (The freeze-pair / initial+final test remains valid **as-is** — it is a legitimate *mechanism-inertness* test, "does the ETE ever move?", not a stability-of-answer test; keep it.)"

---

## PART B — PIPELINE / CITATION edits (Editor B, on the A-edited file)

### B1 [C14 CRITICAL] — merge the two fork-guard table rows (lines 279–280)
Strike "; fork guard **PENDING**" from the "Mechanical aggregation > clinical" row. Replace the "Fork guard" row's last cell "`exit_reason: dissent_irreconcilable` **exists**" WITH:
> "**enum EXISTS** (`exit_reason: dissent_irreconcilable` — the escalation *channel*); **detector PENDING** (the structural dispersion≠fork classifier, `[[BET-FORK]]`). The channel to *report* a fork is built; the mechanism to *detect* one is not."

### B2 [C7 fork resolved] — retype node C (line 234) + append to OQ-1
CURRENT node C: `C["Per-agent reviewer/compressor<br/>short output · free inference"]`
NEW node C: `C["Per-agent reviewer/compressor<br/>short output · typed deltas {preserved/omitted/reformulated/inferred}"]`
APPEND to OQ-1:
> "*Preservation obligation (PENDING).* "Pure compressor" is only nominal unless the compressor is bound to a **preservation contract**: every span of its output is typed `{preserved, omitted, reformulated, inferred}`, and `inferred` is **flagged** so the cross-agent judge can **discount** it. Without this, "free inference" lets the compressor add/select/reinterpret — which *is* judging, contradicting adjustment 2. The detector is **not built (PENDING)**; the commitment now is to *name* the obligation. Whether compression choices themselves leak verdict-bias is **untested — a candidate for a future BET.**"

### B3 [C11] — annotation(TYPE) vs rubric(QUALITY); node F uses the rubric (OQ-2/OQ-4, node F line 237, table row 277)
APPEND a named distinction under OQ-2 (or as a short bridging note):
> "**Named distinction — annotation-schema (TYPE) vs evaluation-rubric (QUALITY).** The doc offers *two* candidates for "the anchored common scale" and must not conflate them: OQ-2's per-`dispatch_type` **rubric** scores *how good* a piece is (QUALITY); OQ-4's **6 facets** classify *what it is* (TYPE). They are orthogonal. **Node F judges on the QUALITY rubric (OQ-2); the TYPE facets (OQ-4) are an orthogonal annotation whose *dispersion* is a noise signal, not the judgment scale.** Whether facets feed a rubric dimension, coexist, or stay unwired is **PENDING**; and `source_confidence`/`content_certainty` sit inside the 6 facets yet read as quality-adjacent — whether they migrate to the rubric is an **open sub-question**. *(Cross-ref formal: findings.md identifies the 6 facets with the dual coordinates `η=∇F`; that makes them a **candidate carrier** for `F`, not a discharged one — do not promote "facets = F" to fact until OQ-10 bullet 1 is answered.)*"
Table row 277 last cell → "**PENDING** — two unreconciled components: OQ-2's per-`dispatch_type` quality rubric (scores) + the 6 `knowledge-taxonomy` facets (classify); their boundary (esp. `source_confidence`/`content_certainty`) is open."

### B4 [C8] — state which artifact node F scores (line 237)
Node F → add the clause (and the C10 rename): `F["Cross-agent judgment (scores the raw frozen finding B; compressed output C = audit/human digest, inferred-flagged deltas visible-but-discounted)<br/>anchored common scale · PRODUCER-BLIND — NOISE axis"]`
(Recommendation, connects to B2: judging the raw frozen finding keeps the independence axis clean; compression serves the digest/output-budget, not the score.)

### B5 [C6] — downgrade the two-level ETE claim (lines 226–229)
CURRENT: "The research flow designed in the sessions is, formally, a two-level **Estimate-Talk-Estimate** (Delphi): register independently → discuss → re-register, within each agent, and again among the synthesizers."
NEW: "The research flow combines two levels, **not symmetrically**. Within each agent: a full **Estimate-Talk-Estimate** (Delphi) — register independently → discuss → re-register (adjustments 1 & 4, the frozen pair). Among the synthesizers (F→G→H): **Estimate→Talk→Approve** — there is no re-register step after discussion today; a synthesizer-level re-register is **PENDING**, not built."

### B6 [C9] — name the two budgets (table row 283)
Last cell → "`token_budget` in schema v0.6.0 **exists** as one generic field; adjustment 3 needs **two** — `output_budget` (caps what the agent emits) and `deliberation_budget` (protects the evaluator's System-2 reasoning); a single field cannot encode both (they pull opposite ways). The split is **PENDING**, not built."

### B7 [C10] — rename source-blind → producer-blind (lines 112, 237, 278, 504) + one WHY clause
Replace "source-blind"/"SOURCE-BLIND" with "producer-blind"/"PRODUCER-BLIND" at lines 112, 237 (done in B4), 278, 504. Leave "source filter" (184) and "sources consulted" (204) untouched. On the table row 278, append the clause:
> "the evaluator is blind to **producer-identity** (`agent_name`/`model`/persona — kills halo) but **not** to the **scientific source** of the evidence (the paper key), because the citation-quality check (`supports` vs `mentioned`, `claim ≤ proof`) requires seeing where the evidence came from — hence **producer-blind, evidence-sighted**."

### B8 [C12] — inline pointer to OQ-8 (lines 181–182)
CURRENT: "…**frame dispersion as a first-class signal** (high dispersion = ill-posed problem; you don't average questions). This arm is new and not yet built."
NEW: "…**frame dispersion as a first-class signal** (high dispersion = ill-posed problem **— the trigger separating 'ill-posed' from 'rich' is unresolved, see `[[OQ-8]]`**; you don't average questions). This arm is new and not yet built."

### B9 [C19] — orphan handling by claim-class (OQ-7 lines 375–376, reconcile with line 210)
Replace OQ-7's "an orphan claim (no key) rejected by the observability-output validator." WITH a named policy:
> "orphan handling **by claim-class** (this resolves the main-text "suspect, not silently accepted" vs a flat "rejected"): **empirical/external claim, no key → blocked** (an empirical assertion with no evidence source is not evidence); **inferential claim carrying the explicit `reasoning`/self-evidence key → admitted** (the truth-by-reasoning valve; not an orphan); **un-typed claim (no key, no `reasoning`) → suspect** — surfaced and escalated to the judge, never silently accepted nor silently discarded. The routing rule is **PENDING**; the commitment now is to name the three classes rather than leave two contradicting sentences."

### B10 [C20] — work_id vs version_id (lines 200–203)
Replace "The key enables **dedup** (same key = same paper) and the query 'has this already been researched?'." WITH:
> "The key resolves an explicit **`(work_id, version_id)`** pair: `work_id` identifies the **work** (precedence DOI > arXiv > URL > hash), `version_id` a **separate slot** for the v1/v2 / preprint↔published distinction. **Dedup is by `work_id`**; **claim-anchoring/provenance by the full pair**. Fields are **PENDING**; naming the pair stops "same key = same paper" from conflating work-identity (what dedup needs) with version-identity (what provenance needs)."

---

## What is NOT changed (critique overstated / wrong — record, don't edit)
- **Seam 2 stays native-categorical** (critique C17 wrong to blanket-downgrade).
- **The freeze-pair collapse-test stays** (critique C15 wrong on that third test).
- **The reformulation is layered, not substituted** — the Bregman theorem, Banerjee-optimality (F-independent), exclusivity-iff, and co-location are preserved as the named refinement (A3).
- **Double-counting noted**: the 20 points are ~5 axes; ≥6 were the doc quoting itself. No new content invented; every fix either propagates an existing confession or names a real gap PENDING.
