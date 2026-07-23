# Assay — Initial Considerations (the probe)

> **What this is.** A probe: a deeper assessment of the chosen first approach (measuring the prolixity
> of our own system) plus the scaffolding for the next research — what to investigate on the web and in
> this repo before/while building. It is the "prob" we use to decide what to do next; the
> [README](README.md) holds the high-level problem and the space of options. Written 2026-07-23 from a
> three-agent probe (advocate ⊥ skeptic + research-scout), synthesized with the coordinator's judgment.

---

## 1. Verdict on the first approach — committed

**Prolixity-of-own-system is the right first *target*. The README's full M1 (LM surprisal + behavioral
A/B) is the wrong first *build*.** The right first *move* is a **gzip-only, confound-guarded redundancy
audit** over our own instructions, which then *earns* the LM layer instead of assuming it.

This is not a retreat from prolixity — it is prolixity shipped in the order that de-risks it. The advocate
and skeptic, arguing from opposite sides, **converged** on three things: gzip ships first, the full
agent-replay falsifier is not v0, and the LM layer must beat gzip before it is trusted. The synthesis
below is built on that convergence, with one load-bearing correction from the skeptic and one
build-vs-adopt shortcut from the scout.

---

## 2. The decisive finding — the genre confound (must shape everything)

Surprisal-per-token assumes *low surprisal = redundant = cuttable*. **Instructions are the one genre where
this is false, even inverted.** The highest-compliance-value tokens are deliberately low-surprisal:
terse imperatives, and critical rules repeated on purpose ("never edit the ledger in place," restated
across three skills). A repeated critical rule scores near-zero `L(unit|rest)` *precisely because* it is
restated — so a naive prolixity rank puts **load-bearing repetition at the top of the cut list**, while a
rambling-but-novel aside scores high-density and is spared. On this corpus the raw metric is
**anti-correlated with cut-safety on exactly the units where a wrong cut is most dangerous.**

Two consequences, both non-negotiable:

- **P-GUARD (confound guard).** Any unit restated across ≥ 2 skills/sections is flagged **protected** —
  never top-cut, surfaced as "possibly deliberate repetition." Redundancy detection and *cut-safety* are
  different questions; the tool must never conflate them. Without this it is dangerous on its own first
  corpus.
- **Reframe "prolixity."** The useful output is not "low information" but "**redundant AND safe to
  remove**." The scalar answers the first half; the falsifier (below) and P-GUARD answer the second. The
  README's HARD CAVEAT is not a footnote — it is the core of the problem.

Secondary: short units (a rule is a handful of tokens) give per-token rate and the `Δ = L(u|∅) − L(u|rest)`
confidence signal huge variance — the tool is *least* reliable exactly where instructions are densest.
Mitigation: a **min-length floor (~100 tok)** — units below it are reported, not ranked.

---

## 3. The de-risked build ladder

Each rung ships something usable and *earns* the next; any rung can kill what follows (the tool must be
able to lose).

| Rung | What | Proves / decides | Infra needed |
|---|---|---|---|
| **S0** | Segment units + **conditioned-gzip** column (rest-of-corpus as preset dictionary) → ranked redundancy map + P-GUARD flag | The redundancy-map shape is useful; sets the baseline the LM must beat. **Honest MVP — ships in a day.** | stdlib only |
| **S1** | Embed units + FAISS neighbour table | Retrieval concentrates similar units; **names the merge partner** for free | sentence-transformers, FAISS |
| **S2** | Local logprob server → `L(u\|∅)` density | Logprob pipeline + reproducibility pinning; intrinsic column. **← evaluate ADOPT vs BUILD here (§5)** | llama.cpp/vLLM *or* wrap LLMLingua |
| **S3** | Retrieval-conditioned LOO → `L(u\|rest)` + differential `Δ` | Does conditioning actually move `L` on our private content (`Δ>0`)? If `Δ≈0` corpus-wide, defect-3 is fatal → fall back to S0+S1, still shippable | S2 + retrieval |
| **S4** | **LM-vs-gzip bake-off** | Does `L(u\|rest)` reorder gzip meaningfully? **Yes → LM earns its build. No → kill the LM layer.** | — |
| **S5 (M1)** | **Mask-and-regenerate** falsifier on top-k flags | Makes "the system already predicts this unit" testable **with no agent loop** | S2 |
| **M1.5** | Agent-replay on 5–10 real dispatches | Gold-standard behavioral check, cost-bounded | new harness (does not exist) |

**Metric decisions (settled):** rank on **bits/token** (rate, never total — here the length-extensivity
defect *is* the signal); keep **gzip (A) / LM (B) / differential (Δ) as three separate columns, never
blended** — the payload is the *disagreement cells* (low-B / high-A = looks-novel-but-system-predicts-it,
exactly where the LM earns its cost); rank-only for v0 (absolute bits/token is backend/quant-dependent and
non-portable). **Segmentation:** file-tier ranks (cut/merge/tighten act at file granularity),
section-tier is a *zoom* on top flags, never a sum (summing sections overcounts by the multi-information).
**Conditioning at ~66-skill scale:** retrieval-conditioned LOO (neighbours are where restatement lives, so
retrieval *concentrates* signal and yields the merge partner), not all-rest concatenation.

---

## 4. Why the falsifier changes shape — infra reality

The README crowned a **behavioral A/B** (swap instructions, re-run the agent, compare behavior) as the
standout eval. The probe found this is the **hidden iceberg**, not the cheap win:

- **The infra does not exist.** `implementations/` is a read-only control plane (write path disabled by
  design); `requirements.txt` is just `fastapi`+`uvicorn`; no logprob/llama.cpp/vLLM anywhere. There is no
  task-set runner, no instruction-swap rig, no behavior-differ.
- **Its denominator is the repo's own enemy.** Attributing a behavior *delta* to a trim (not to sampling
  noise) needs N repeats per task per variant — fighting exactly the agent noise this repo was founded to
  fight (`HYP-ORCH-NOISE`). Nobody has costed that repeat budget.

**Resolution:** the v0 falsifier is **mask-and-regenerate** — mask unit `u`, give the model `rest`, ask it
to reconstruct the instruction `u` governs, score overlap. High reconstruction ⇒ the system genuinely
predicts `u` ⇒ safe-to-cut evidence. This operationalizes the redundancy claim *self-containedly, with no
agent loop*. The full agent-replay is descoped to **M1.5 on a tiny real-dispatch sample**, an aspiration to
be costed — not a delivered v0 eval.

---

## 5. Build-vs-adopt — the biggest scope decision

The scout's load-bearing find: **LLMLingua / LongLLMLingua (Microsoft) already implement the M1 primitive.**
A small LM scores per-token perplexity to prune low-information tokens; LongLLMLingua's "perplexity of the
question conditioned on documents" is *literally* `L(unit | corpus)`. This means S2/S3 may be a **wrap, not
a build** — and it is external evidence that the LM layer *can* beat gzip (partly answering S4 before we
spend on it). **Decide adopt-vs-build at S2 before standing up a bespoke logprob server.**

---

## 6. Research map — what to investigate next (the scaffolding)

### Track 1 — web / external prior art
- **[load-bearing] LLMLingua family** — the M1 primitive already exists; read first (build-vs-adopt, §5).
- **[load-bearing] Behavioral-equivalence eval of compressed prompts** — the *weakest-covered* thread
  externally (papers measure benchmark deltas, not "same tool choices / gate outcomes"). **The gap is
  likely our contribution.** Search: prompt-compression *faithfulness*, instruction-following
  preservation, agent-trajectory equivalence.
- **[load-bearing] Instruction-redundancy for LLM agents** — partially real; found an external, independent
  statement of P-GUARD ("shrink the prompt as models absorb conventions, but tighten safety constraints as
  it shrinks"). Confirms the niche is open and hands us a ready articulation of the caveat.
- **[optional] MDL for text + gzip-as-baseline**; **[optional] near-dup at scale (MinHash/Jaccard)** — the
  latter only bites for "name the merge partner" once M1 works.
- **Not worth searching:** category-theory grounding (out of v0), Kolmogorov (uncomputable).

### Track 2 — in-repo assets to leverage/verify
- **The skills corpus** (`.claude/skills/`, ~66 `SKILL.md`, ~105k tok; median 1053 words, max 5754
  `necronomicon`, min 49) — the thing being measured; YAML `description:` frontmatter gives free labels;
  **composed spells (`paired-views`, `repository-harness`) likely duplicate their components' prose = a
  built-in ground-truth redundancy case** to validate the ranking against.
- **`telemetry/agents/subagents-dispatch.yaml`** — append-only, hook-guarded (Read only). Rows carry
  `goal`/`context`/`groups`/per-agent `role`/`angle`, gate outcomes → the **behavioral-falsifier task set**
  (verify replayability; ~700 rows). *Not* a claim corpus, so it cannot seed `K`.
- **`vault/hypothesis/claim-graph.md` (HYP-CLAIM-GRAPH)** — still a *hypothesis doc, not a queryable store*
  (confirms v1 novelty-vs-ledger is store-gated); its `contradicts`/`refines` schema and CT1
  (inter-annotator agreement) bind Layer 2 as a delta-proposer into the *existing* schema.
- **`tools/agent-pool-mcp`** — the pattern for shipping Assay as a repo-local MCP tool; **check for an
  existing logprob harness before standing one up.**
- **`experiment-harness` skill** (has `scripts/`+`templates/`) — natural host for the original-vs-trimmed
  A/B; verify it can drive a two-arm comparison.
- **`lean-formalization/`** — README only, zero `.lean`; do not gate v0 on it.

### Top research questions (ranked, tagged with the decision each unblocks)
1. **[web]** Does LLMLingua/LongLLMLingua already implement `L(unit|corpus)` well enough to *wrap*? → build-vs-adopt for all of Column B (biggest scope call).
2. **[repo]** Can `subagents-dispatch.yaml` rows be replayed as a task set with recorded expected behavior? → whether M1.5 agent-replay is buildable or needs a hand-built set.
3. **[web]** State of the art for *behavioral-equivalence* (not benchmark-score) eval of compressed prompts? → the falsifier's pass/fail metric, and likely the contribution gap.
4. **[repo]** Do the ~66 skills segment cleanly into scorable units, and do composed spells contain measurable duplication? → S0 feasibility + a built-in ground-truth positive.
5. **[repo]** Does conditioning move `L` on our private content (is `Δ > 0`)? → whether defect-3 (pretraining swamps K) is fatal here; run at S3.

---

## 7. Open forks for the owner
- **F1 — adopt vs build the LM layer** (§5). Recommendation: spike LLMLingua at S2 before building.
- **F2 — is gzip-only enough?** If S0+S4 show gzip already surfaces the redundancy usefully, the LM layer
  may never need to be built. Acceptable outcome, not a failure.
- **F3 — mask-and-regenerate vs agent-replay** as the *trusted* falsifier. v0 uses the former; whether the
  latter is ever worth its noise budget is a later, costed decision.
- **F4 — alternative first bindings** the skeptic raised, if prolixity stalls: **self-coherence** within one
  large governance doc (`contradicts` edges are *locally* human-checkable in seconds — more falsifiable than
  a prolixity rank, no harness), or the **claim-graph delta-proposer** (heavier, but seeds the `K` the
  north-star needs). Held as fallbacks, not the first move.

## 8. Gates before each escalation
- **P1 (LM earns its build):** ship S0 gzip-only; build `L(unit|rest)` *only if* S4 shows gzip fails to
  separate redundant from load-bearing.
- **P2 (confound guard, non-negotiable):** P-GUARD flag in the ranking from S0 onward.
- **P3 (falsifier honesty):** behavioral agent-replay is later optional validation, never a v0 gate; cost
  its repeat-budget before committing.

---

## 9. Next
This probe is the scaffolding for a forward research dispatch. A follow-on may add a `dispatch_type: probe`
to the subagents-strategy skill (a robuster-than-usual probe that both maps what to research *and* renders a
committed assessment, as this one does) — noted, not built here.
