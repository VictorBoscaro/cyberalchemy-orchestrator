# Document Information Estimator — working name **Assay**

> **What it is, in the folder name:** a tool that, for a given piece of text, estimates **how much
> information** it carries **relative to some body of knowledge** — and, optionally, **what structure**
> that information has (the claims it makes and how they relate, contradictions included) — rather than
> how many words or bytes it has.

Status: **pre-PoC brief.** Not a spec, not a decision — the shaped context for a research dispatch
that decides *whether and how* to build. First written 2026-07-22; refined 2026-07-23 to lead with the
general engine and to name the **first use case** (measuring the prolixity of our own operating
instructions). Moved to `internal-tools/research/` because it is a research artifact, not a shipped tool.

---

## 0. The one operation — the spine of the whole tool

Assay has exactly **one primitive**:

```
marginal_information(unit | corpus, model)  →  (scalar L, claim-graph G)
```

= the relative-surprisal / cross-entropy code-length of `unit` conditioned on `corpus`
(`L = Σᵢ −log₂ P(tokenᵢ | contextᵢ, corpus)`), plus the claim-graph over the same pair. **Everything
else in this document is a use case, and every use case is just a choice of what to plug in as `unit`
and what to plug in as `corpus`.** The engine is the operation; the use cases are *adapters* over it.

**The problem it answers.** Every knowledge system repeatedly asks one question in different clothes:
*given what I already have, how much does this new piece actually add?* A new document against
everything on file. A skill file against the rest of the toolkit. A paragraph against the paragraphs
around it. Today each is answered ad hoc — by word count, by vibe, or not at all. Assay computes one
mechanical quantity, and each of those questions becomes a binding of `(unit, corpus)`.

Intrinsic "standalone" information falls out as the degenerate binding `corpus = ∅`; it is not a rival
reading, just the special case with an empty prior.

---

## 1. The bindings — one engine, many use cases *(the options)*

| Binding `(unit, corpus)` | Measures | Decides | Readout | Status |
|---|---|---|---|---|
| **skill / `CLAUDE.md` section  \|  the rest of the system** | prolixity / redundancy | cut · merge · tighten · keep | scalar rate + `restates`/`entails` edges | **v0 — ships first (§3)** |
| section  \|  rest of the same document | self-coherence | localize internal contradiction | `contradicts` edges | later adapter |
| document  \|  the held-claim ledger `K` | novelty vs. what we hold | accept · rank · flag conflict | scalar rank + `D_to_K` edges | **north star — v1, store-gated (§4)** |
| any text  \|  ∅ | intrinsic surprise | compression/entropy baseline | scalar | degenerate case |

The rest of this README develops the **spine** (§0, §5–§7), the **first binding to ship** (§3), and the
**north-star binding and why it waits** (§4).

---

## 2. The two readouts — scalar ⊕ structure

Each binding produces up to two readouts of the same `(unit, corpus)`:

- **Layer 1 — the scalar `L` (magnitude).** Cheap. Ranks and gates. The direct answer to "how much."
- **Layer 2 — the claim-graph `G` (structure).** Nodes = atomic propositions extracted from `unit`;
  typed edges `{ entails, refines, restates(=redundant), contradicts }` among them and against `corpus`.
  Localizes: *which* claims are redundant, *which* conflict. **Contradiction is a native edge type.**

The two are **two readouts of the same document**, useful for different tasks (scalar for ranking, graph
for structure-sensitive tasks) — neither is the "shadow" of the other. A scalar *can* detect that a
document is inconsistent (one bit); it *cannot* localize which claims conflict. Localization is the
graph's job.

---

## 3. First use case (v0): **measure the prolixity of our own system**

**The target.** An orchestrator that runs on instructions — a `CLAUDE.md`, a ~80-skill library,
constitutions and vault docs — accretes prose faster than it prunes it. Nobody can tell, by reading,
*which* of those words are doing work and which are redundant restatements the model would have inferred
from the rest of the system. Assay's first job is to turn that guess into a measurement, per instruction
unit, so redundancy becomes a coordinate instead of a vibe.

**Why this is the right *first* binding — it de-risks the engine.** Prolixity is the easiest possible
target for the primitive, and it exercises every knob the general engine needs:

- **Prolixity is a *ratio*, not a magnitude** — surprisal per token. This turns the engine's biggest
  hazard (a length-extensive scalar, §6) *into the signal itself*: a verbose unit is one with **low
  density**. We rank on the rate, never the total.
- **The relative reading gets a clean meaning:** `L(unit | rest_of_system)` low ⇒ the rest of the system
  already predicts this unit ⇒ **cross-document redundancy** ⇒ a candidate to cut or merge.
- **The corpus is our own system:** bounded, in-repo, versioned. So the engine's worst v0 worry — *`K`
  can't fit the context window* (§6) — is **mild**: the self-corpus (or a relevant slice) fits. And
  because these instructions are idiosyncratic/out-of-distribution, *pretraining swamps `K` less* than
  on generic prose.
- **Units segment for free:** each `SKILL.md`, each `CLAUDE.md` section, each constitution rule = one
  unit. No fuzzy claim-extraction needed for v0 — the filesystem gives the units.
- **The falsifier is behavioral, not a vibe-rating** (below) — which the repo's `claim ≤ proof`
  discipline actually respects.

**What the owner does with the output — a redundancy map**, ranked, read as a shortlist:

- **Low `L(unit | rest)`** → the system already predicts this unit → **cut or merge** (name the merge
  partner: the other unit that most reduces this one's surprisal).
- **Low density but high `L(unit | rest)`** → verbose but genuinely novel → **tighten** (same new thing,
  fewer tokens).
- **High density** → leave alone.

### Minimal first build (M1)

1. **Segment units** from the filesystem (skills, `CLAUDE.md` sections, rules).
2. **Column A — `gzip`-ratio per unit** (`len(gzip(unit)) / len(unit)`, optionally with the rest of the
   corpus as a preset dictionary). Near-zero cost, no model. **This is the baseline the LM must beat** —
   if the LM ranking doesn't improve on gzip's, the LM layer loses. The tool must be able to *lose*.
3. **Column B — `L(unit | rest_of_system)`** via token logprobs from a pinned local LM (llama.cpp /
   vLLM), normalized by token count → density.
4. **Emit the redundancy map:** `unit · gzip_ratio · L_per_token(unit|rest) · verdict_hint`, most-prolix
   first.
5. **Behavioral falsifier (the standout eval).** Take the top-`k` flagged units, produce a **trimmed**
   system, run the agent over a fixed task set with both original and trimmed instructions, and check
   **behavior is preserved** (same tool choices, same gate outcomes, same artifacts). **Pass:** trimmed
   system preserves behavior on ≥ N/M tasks *and* the ranking predicted which trims were safe. If
   trimming a "redundant" unit *changes* behavior, that unit was load-bearing — the tool was wrong
   there, and that is real signal too.

### ⚠ HARD CAVEAT — prolix ≠ bad for instructions

Deliberate repetition of a critical rule (e.g. "never edit the ledger in place," restated across three
skills) is **functional** — the repetition *drives compliance*. The tool measures redundancy; it does
**not** know which redundancy is load-bearing. **The redundancy map is a review signal, never an
autocut.** The behavioral falsifier is exactly what separates safe-to-cut redundancy from
compliance-driving repetition. Treat "low information" as *a question to a human*, not a verdict.

---

## 4. The north-star binding: **novelty relative to the ledger** (deferred to v1)

The original vision: given a document `D` and the body of knowledge this repo holds `K` (the epistemic
ledger / claim store), estimate how much `D` would **update** what we hold — `L(D|K)` — and extract the
claim-graph `D` commits to, with `contradicts` edges drawn against `K`. This is the **intake instrument**
for the "golden graph of held-true nodes" the repo already intends to build (`vault/hypothesis/
HYP-CLAIM-GRAPH`): before a claim earns a place, you want to know whether it is new and whether it
conflicts with a held node. It honors `veracity ⊥ conviction` — `L(D|K)` is an evidence-side surprisal
readout, never a truth verdict.

**Why it waits.** All three engine defects (§6) converge on one missing dependency: **a queryable,
repo-private held-claim store does not yet exist.** The brief's own §K note is explicit — the *dispatch*
ledger (`telemetry/agents/subagents-dispatch.yaml`) is a **process log, not a corpus of held claims** —
so `K`-as-ledger cannot be built today. Shipping the `L(D|K)`-ranking product now would be building on a
corpus that isn't there.

**But pull one piece forward.** Layer 2's claim-graph (nodes = propositions, `contradicts` edges) is
*structurally the same object* as the repo's intended held-true graph. **Do not build a second schema.**
Build Layer 2 as a **graph-delta proposer** into `HYP-CLAIM-GRAPH`'s store — read the store, emit
candidate nodes/edges for owner promotion. That turns a duplication risk into the reason to co-develop
the store: **the tool and its own prerequisite co-evolve.**

**Ship order:** engine → prolixity (self-corpus, no store needed) → claim-graph delta-proposer against a
small hand-built held-claim seed (this *seeds* `K`) → full novelty-vs-`K` ranking (v1, gated on the store).

---

## 5. The engine, precisely — honest information theory

"Amount of information" is not one quantity; it is at least three, and they disagree. Assay leads with the
**relative** reading and treats the others as its `corpus = ∅` limit and its structural companion.

| Meaning | What it is | Mechanical estimator | Honest caveat |
|---|---|---|---|
| **Intrinsic / compression** | surprise / incompressibility | `len(gzip(unit))`; unigram entropy | Rewards noise. `gzip` ≠ idealized entropy; unigram is order-blind; true (Kolmogorov) information is **uncomputable**. |
| **Semantic / propositional** | the claims committed to | extract atomic claims, dedupe, graph | "distinct claim" is fuzzy under paraphrase/entailment; a count is a thin readout. |
| **Relative / novel** *(our pick)* | how much `unit` updates a prior `corpus` | cross-entropy code-length `L` (above) | In expectation this cross-entropy rate **upper-bounds the entropy** (expected excess = `KL(true‖P)`); a single realized `L` is one surprisal, **not** itself a bound. Bits only in log₂. |

**Correctness notes (do not regress):**

- It is **cross-entropy / surprisal**, not "the bit count," and **not `KL`** — `KL` is a distribution-level
  expectation needing two distributions; one document gives pointwise surprisal.
- Surprisal decomposes across levels **only via the chain rule** (each term conditioned on all prior
  context). Independent per-sentence scoring **overcounts** by the total correlation (multi-information)
  among units — pairwise mutual information only in the two-unit case. It does not compose "for free."
- **Report the differential `L(unit | ∅) − L(unit | corpus)`** — how many bits *this* corpus explains —
  as a confidence signal. When it is ≈ 0, the engine is telling you it cannot distinguish `corpus` from
  what the base model already knows (see §6, defect 3).

---

## 6. Known limits of the engine — the three defects, named once

These are properties of **the operation**, so they surface once at the engine/adapter seam instead of
hiding inside each use case:

1. **Length-extensive scalar.** `L` grows with `|unit|`, so raw `L` ranks long things as "more
   informative." **Fix in the contract:** expose a companion per-token **rate** `L / |unit|` and let each
   adapter declare which it ranks on. (Novelty wants near-total `L`; prolixity wants the rate — where the
   defect *becomes* the signal.) Never rank on raw `L` without saying so.
2. **`corpus` can't fit the context window.** The engine assumes a *fitted* `K`; assembling and
   trimming `corpus` down to the window (retrieval/chunking) is the **adapter's** job, not the core's.
   Prolixity's self-corpus makes this mild; novelty's real ledger makes it a hard prerequisite (§4).
3. **The base model swamps `corpus`.** `marginal_information` is only faithful to the extent the model's
   pretrained prior isn't *already* the corpus. For public, ledger-like content `L(unit|∅) ≈ L(unit|K)`,
   so conditioning barely moves `L`. The bite is smallest on **repo-private, idiosyncratic** content
   (our instructions; private findings). Mitigation is the differential in §5, reported as confidence —
   not a per-use-case patch.

---

## 7. Modularity — how to add a use case

A use case is a triple; the core `estimate()` never changes:

```
adapter = {
  unit:    how to carve the thing being scored   (a file, a section, a claim)
  corpus:  how to assemble K                      (the sibling skills, a dir of findings, the ledger)
  readout: which output it acts on                (scalar→rank/gate | graph→localize)
}
```

New use cases are **data (a triple), not a rewrite.** The contract is the `(unit, corpus)` binding and
nothing else — the same auto-discovery-by-schema instinct the rest of the repo uses. The first internal
customer is the system's own instructions (§3); the engine is dogfooded before it is generalized.

---

## 8. Category-theory grounding — an open thread, not a foundation

The sibling `lean-formalization/README.md` *describes* Lean objects that look like this shape
(`thin_codomain_noise_hom_subsingleton`, `thin_hom_readout_not_beatsCount`,
`functorial_strictly_dominates_count`). **These are typed candidates, not proof about this tool** — and
there are **no `.lean` files in-repo**, so it is a README citing a README. Applying them to documents
would require first exhibiting documents as objects of the relevant category and "information" as a
count-capped readout — neither is established. **v0 does not depend on the CT story.** Whether a real
functorial-entropy bridge exists (Baez–Fritz–Leinster; Vigneaux; Ellerman) is a **separate, optional**
research question. Default: **out of v0.**

---

## 9. Scope & sequencing

- **M1 (ships first):** the prolixity binding over our own system — segment → `gzip`-ratio + `L(unit|rest)`
  → redundancy map → **behavioral falsifier**. Self-contained; needs no external corpus, no store.
- **M2:** the claim-graph as a **delta-proposer** seeding a small held-claim store.
- **v1:** full novelty-vs-`K` ranking, gated on that store existing.
- **CT thread:** out.

### Estimator provider
Token logprobs from a **local llama.cpp or vLLM** server (full per-token logprobs, no per-call cost) or
the OpenAI completions `logprobs` field. **Anthropic is excluded** — the Messages API does not return
token logprobs. Pin one model so `L` is reproducible **within an identical backend + weights + settings**
(logprobs are sensitive to backend/quantization/hardware; "reproducible" means backend-pinned).

### Non-goals (v0)
True/Kolmogorov information (uncomputable); a fact-checking or truth system; claiming the CT formalization
grounds the design; multilingual (English only); documents beyond a single context window (chunking is
later); real-time/streaming; and **writing back to any ledger** (read-only over `corpus`).

---

## 10. Research map — techniques, references, tools

**A. Intrinsic / info-theoretic magnitude.** Shannon 1948; perplexity/cross-entropy; MDL (Rissanen;
Grünwald); Kolmogorov complexity & sophistication (Li & Vitányi); Bayesian surprise (Itti & Baldi 2009);
psycholinguistic surprisal (Hale 2001; Levy 2008); gzip-kNN (Jiang et al. 2023) as baseline and
cautionary tale.

**B. Semantic / structural.** OpenIE (Stanford, Angeli 2015); NLI (SNLI/MNLI; DeBERTa-v3-MNLI); FEVER
(Thorne 2018); factual-consistency: SummaC (Laban 2022), QAGS, FactScore (Min 2023); atomic-claim
decomposition; contradiction detection (de Marneffe 2008); k-ary consistency via SAT/SMT.

**C. Relative / novelty-vs-prior.** Bayesian surprise = KL(posterior‖prior); information gain / expected
value of information; TF-IDF/BM25 as the "prior" baseline; novelty/redundancy detection; active inference
/ free-energy (Friston).

**D. Categorical grounding (optional thread).** Baez–Fritz–Leinster (2011); Leinster, *Entropy and
Diversity* (2021); Vigneaux, information cohomology; Ellerman, logical entropy.

**E. Tools / build substrate.** Karpathy (nanoGPT/minGPT, llm.c, nanochat, "Zero-to-Hero"); token
**logprobs** via OpenAI or local **llama.cpp / vLLM**; HuggingFace `transformers`; `sentence-transformers`;
spaCy / AllenNLP for OpenIE + coref; DeBERTa-MNLI; **FAISS/hnswlib** for ANN pruning (note: cosine-ANN is
similarity-pruning and drops true contradictions — recover them with an NLI-tuned signal).

---

## 11. Name candidates

The folder name is deliberately explicit. A short codename is still open; **Assay** is the front-runner
(in alchemy/metallurgy an *assay* measures how much precious metal is really in an ore — exactly "how much
information is really in this text"; fits the cyberalchemy theme). Alternatives: **Titer** (measured
concentration), **Cupel** (the vessel that performs an assay), or the plain
`document-information-estimator`. Pick at the confirm gate; until then artifacts use `assay`.

---

## 12. Next

The forward-research scaffolding — a deeper assessment of the prolixity-first approach and a map of what
to research (on the web and inside this repo) — lands in **`initial-considerations.md`** in this folder.
That artifact is the "probe" we use to decide what to build and research next; this README is the
high-level problem and the space of options.

---

### One-line summary
Assay is one operation — `marginal_information(unit | corpus)` — read two ways (a scalar that ranks and a
claim-graph that localizes); its **first shipping use case** measures how prolix our own instructions are
(self-corpus, `gzip` baseline, behavioral falsifier), its **north star** is novelty against the epistemic
ledger (deferred until that store exists), and the category-theory grounding is held as an explicit open
question, not a foundation.
